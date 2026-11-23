> Production architectural design for the 177-class, 33-crop Hale foliar classification engine (ConvNeXt-Tiny DualHead on 4GB VRAM). The release snapshot (v1.0: 177 classes, 33 crops, 91,984 active images) is documented in models/v1/model_card.md and docs/DATASET_CARD.md.

# 🌿 Chlorophyll & Convolutions: Designing a 177-Class Plant Disease Classifier Under 4GB VRAM Constraints

> ### ⚡ TL;DR: 5 Core Architectural Decisions
> 1. **ConvNeXt-Tiny over ViT/EfficientNet:** $7 \times 7$ depthwise kernels capture the necrotic center, water-soaked border, and chlorotic halo simultaneously in early stages, while LayerNorm ensures stable normalization at `batch_size=16` on 4GB VRAM.
> 2. **Pathology-Preserving Augmentations:** Hue jitter locked to `0.0` (hue shifts simulate nitrogen deficiency or mosaic virus on healthy foliage); minimum crop scale restricted to `0.75` to preserve lesion margin context.
> 3. **Shared-Trunk Dual-Head Multi-Tasking:** ConvNeXt backbone extracts shared 768-dim embeddings; auxiliary crop head regularizes the backbone while enabling runtime hierarchical gating to eliminate nonsensical cross-crop misdiagnoses.
> 4. **Probabilistic Soft Gating & Calibration:** Dismantled the "1.63% hard-masking ECE" denominator artifact; fitted validation temperatures ($T_d = 0.6228, T_c = 0.7016$) to calibrate raw logits (1.02% ECE) and soft joint gating ($P(d) = \sum_c P(c)P(d \mid c)$).
> 5. **Two-Phase Transfer Recipe:** Phase 1 head warmup (3 ep, frozen trunk, `AdamW`, $3 \times 10^{-4}$) + Phase 2 unfreezing Stages 2–3 (15 ep, cosine decay, layer-wise LR $1 \times 10^{-5}$) within a 4GB RTX 3050 envelope (~4.5 hours total runtime).
>
> 📖 **Companion Reading:** For the complete forensic dataset engineering journey behind this benchmark, see [The Data-Centric Odyssey Documentary](./DATA_CENTRIC_ODYSSEY_DOCUMENTARY.md). For current production metrics, see [v1.0 Model Card](../../models/v1/model_card.md).

Most tutorials in agricultural deep learning follow an identical, naive playbook: download a pretrained ResNet-50, slap a classification head on top, apply generic data augmentations, and report 98%+ test accuracy on clean laboratory images against uniform gray benches.

In real-world deployment, however, that assumption collapses. On an unconstrained flat disease head, my model misclassified a Potato Early Blight test leaf (`img_00039793.jpg`) directly into Apple Scab—a cross-species botanical confusion demonstrating that flat softmax over 195 fine-grained outputs lacks the structural inductive bias to separate cross-crop pathologies.

Diagnosing **195 foliar disease classes across 34 crops (spanning multiple botanical families)** from nearly **100,000 real-world images (99,751 split across train, val, and test)** is fundamentally different from standard image classification. Different pathogens produce visually identical concentric lesions across completely unrelated plant families. Generic color transforms can invert biological symptoms. And running modern vision models on consumer hardware—specifically an **NVIDIA GeForce RTX 3050 Laptop GPU with 4.0 GB of VRAM**—leaves virtually no margin for inefficient activations or unbounded memory overhead.

This document breaks down the concrete engineering decisions, botanical realities, and architectural blueprints behind my plant disease classification system.

---

### 🎯 What You Will Learn From This Document
1. **The Architecture Design Rationale (ConvNeXt-Tiny vs. ViT vs. EfficientNet):** Why standard Vision Transformers are memory-intensive under tight 4GB VRAM budgets, and why ConvNeXt's $7 \times 7$ depthwise kernels and LayerNorm provide strong spatial representations for microscopic lesion boundaries.
2. **The Botany Behind Data Augmentation:** Why popular computer vision transforms (hue shifts, extreme crops, grayscale) corrupt diagnostic pathology signals, and how to select transforms that improve generalization without altering biological truth.
3. **Hierarchical Multi-Task Learning vs. Flat Softmax:** Why flat 195-way classification leads to cross-species misdiagnoses (e.g., diagnosing an Apple disease on a Potato leaf), and how a dual-head model structures the hypothesis space to eliminate nonsensical cross-species outputs.
4. **Hardware-Constrained Training on a 4GB GPU:** The exact training recipe—mixed-precision (FP16), two-phase warmup, and differential learning rates—that allows a 28M-parameter model to train reliably without CUDA Out-Of-Memory (OOM) crashes.

---

## 🥊 Chapter 1: Architectural Design Rationale — What I Considered vs. What I Chose

When designing a classifier for 195 fine-grained foliar classes on a 4GB GPU, I evaluated structural architectural tradeoffs across the deep learning landscape. (Note: Preliminary exploratory runs comparing ConvNeXt-Tiny, ResNet-50, and MobileNetV3 were conducted on an earlier, retired dataset split that was decommissioned due to cross-split duplicate leakage; no comparative figures from that retired split are carried forward here. For broader model families, I weighed their documented theoretical and memory profiles on 4GB VRAM):

```
[The Heavyweight Past]          [The Transformer Wave]          [The Modernized Hybrid]
VGG-16 / ResNet-50 / Inception  ──►  ViT-Base / Swin-T / DeiT    ──►  ConvNeXt-Tiny & EfficientNet-V2
(3x3 filters, parameter-heavy)     (Global attention, memory-heavy)   (7x7 depthwise, LayerNorm, efficient)
```

---

### 1. Legacy Architectures (VGG-16, Inception-V3, DenseNet-201): *Structural Bottlenecks*
* **VGG-16 (138 Million Parameters):** 138 million parameters create excessive memory overhead during backpropagation, making fine-tuning on a 195-class head at reasonable batch sizes prohibitive on a 4GB GPU.
* **DenseNet-201 (20 Million Parameters):** While parameter-efficient, DenseNet concatenates feature maps across layers (`torch.cat`), which significantly increases peak activation memory during the backward pass.
* **Inception-V3:** Requires a rigid $299 \times 299$ input resolution, includes multiple auxiliary heads, and uses asymmetric factorized filters that can fragment small lesion boundary signals.

---

### 2. Pure Vision Transformers (ViT-Base-16, DeiT): *Quadratic Activation Footprint*
Vision Transformers (ViT) model global dependencies via patch-level self-attention:
$$\text{Attention}(Q, K, V) = \text{Softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V$$
* **Activation Memory:** Self-attention scales quadratically $\mathcal{O}(N^2)$ with the number of patches $N$. On an 86M-parameter ViT-Base with 195 output classes, training on a 4GB laptop GPU requires dropping the batch size to very small values, which can destabilize gradient estimates unless using extensive gradient accumulation.
* **Inductive Bias on Fine-Grained Features:** ViTs lack the localized 2D convolutional translation equivariance that helps CNNs identify tiny 3-pixel-wide bacterial puncta without requiring massive pretraining datasets (e.g. JFT-300M).

---

### 3. The Modern Efficient CNNs: EfficientNet-V2 vs. ConvNeXt-Tiny
EfficientNet-V2 is an effective, lightweight architecture (21M parameters). I chose **ConvNeXt-Tiny** (28.6M parameters) based on two specific pathology-driven design considerations:

#### Consideration A: Kernel Size & Receptive Field ($3 \times 3$ vs. $7 \times 7$)
* **EfficientNet-V2** relies primarily on **$3 \times 3$ convolutional filters** (Fused-MBConv). A $3 \times 3$ window covers a local patch and requires multiple cascaded layers to build a wide enough effective receptive field to encompass an entire lesion.
* **ConvNeXt** employs large **$7 \times 7$ depthwise convolutions**. A $7 \times 7$ window captures **the necrotic center, the water-soaked boundary, and the outer chlorotic halo simultaneously** within earlier feature stages.

#### Consideration B: Normalization Behavior Under Small Batch Budgets
* **Batch Normalization (BatchNorm) in EfficientNet-V2:** BatchNorm computes running mean and variance across the current mini-batch. At `batch_size=16` over 195 diverse classes, batch-level statistics exhibit higher variance between steps.
* **Layer Normalization (LayerNorm) in ConvNeXt:** Like Transformers, LayerNorm normalizes across the channel dimensions of each sample independently, ensuring stable normalization that does not depend on mini-batch size.

---

### 🏆 Selected Architecture: ConvNeXt-Tiny (28.6M Parameters)
ConvNeXt modernizes the standard ResNet backbone using design patterns inspired by Swin Transformers:

```
Standard ResNet-50                    ConvNeXt-Tiny (My Choice)
─────────────────────────────────     ──────────────────────────────────────────
• 3x3 Standard Convolutions           • 7x7 Depthwise Convolutions (Large Receptive Field)
• Batch Normalization                 • Layer Normalization (Batch-size Independent)
• ReLU Activations                    • GELU Activations (Smooth non-linear gradients)
• Stem: 7x7 Conv + 3x3 MaxPool (4x)   • Stem: 4x4 Patchify Conv (4x non-overlapping stride)
• 25.6M parameters                    • 28.6M parameters (Balanced for 4GB VRAM)
```

**Key Advantages for my 195-Class Benchmark:**
1. **Transformer-Like Representation, Convolutional Memory:** Delivers large-receptive-field spatial reasoning without the quadratic self-attention memory overhead.
2. **Hardware Compatibility:** Operates smoothly at `batch_size=16` under Mixed Precision (`torch.cuda.amp.autocast`) within 4GB VRAM.
3. **Multi-Scale Feature Extraction:** Preserves both global leaf geometry (for crop recognition) and local textural lesions (for disease classification).

---

## 📚 Chapter 2: The Two Research Papers & The Two-Stage Epiphany

Before writing a single line of training code, I reviewed two pivotal academic papers in plant pathology computer vision:

---

### 📄 Paper 1: The Two-Stage Approach (IEEE ICECE 2022)
* **Title:** *"A Two-stage Approach for Plant Disease Classification Based on Deep Neural Networks and Transfer Learning"* (Showrav et al.)
* **The Core Discovery:**
  When standard classifiers predict all classes in a flat output layer, models can suffer from **cross-species symptom confusion**. An *Alternaria* leaf spot on Tomato shares concentric ring morphology with *Alternaria* on Eggplant, occasionally causing the model to identify the pathogen correctly while confusing the host crop.
* **The Two-Stage Idea:**
  1. **Stage 1:** Classify the **Plant Species** first (Apple vs. Tomato vs. Grape).
  2. **Stage 2:** Route the image to a specialized model that **only evaluates diseases possible on that host species**.
  * **Evaluation Context:** On small, controlled laboratory partitions with uniform backgrounds (PlantVillage), Showrav et al. reported that decoupling crop identification from disease classification substantially boosted diagnostic reliability. However, on my challenging 195-class real-world benchmark across 34 crops, hierarchical gating delivered a modest $+0.14\%$ top-1 accuracy gain. Its primary operational value in my pipeline is **botanical taxonomy enforcement**—structuring the hypothesis space and eliminating nonsensical cross-species errors.

#### 🚨 The Architectural Bottleneck in Multi-Model Setups:
The two-stage concept is conceptually elegant, but deploying individual physical networks for every crop is impractical:
* Training separate networks for **34 crops** would require managing 35 distinct model checkpoints.
* In edge foliar inference, switching models dynamically creates memory churn and pipeline latency.

---

### 📄 Paper 2: The Multi-Scale Attention Insight (Heliyon / Elsevier 2024)
* **Title:** *"A novel hierarchical framework for plant leaf disease detection using residual vision transformer"* (Vallabhajosyula et al.)
* **The Core Discovery:**
  Foliar diagnosis benefits from a **two-level feature hierarchy**:
  * **Level 1 (Global Canopy & Leaf Contour):** Understanding overall blade geometry and separating leaf boundaries from natural soil/background.
  * **Level 2 (Localized Pathology):** Resolving fine lesion margins, chlorotic halos, and sporulation textures.

---

### 🚀 My Synthesis: The Unified Dual-Head ConvNeXt

I unified the **Two-Stage Decoupling** concept and the **Multi-Scale Representation** into a **Single-Backbone, Dual-Head Architecture**:

```
                              ┌──────────────────────────────────────────────┐
                              │            Input Leaf Image (256x256)        │
                              └──────────────────────┬───────────────────────┘
                                                     │
                                                     ▼
                              ┌──────────────────────────────────────────────┐
                              │         Shared ConvNeXt-Tiny Backbone        │
                              │       (Extracts 768-dim Visual Vector)       │
                              └──────────────────────┬───────────────────────┘
                                                     │
                         ┌───────────────────────────┴───────────────────────────┐
                         ▼                                                       ▼
       ┌───────────────────────────────────┐                   ┌───────────────────────────────────┐
       │       HEAD 1: Crop Classifier     │                   │     HEAD 2: Disease Classifier    │
       │          Linear(768, 34)          │                   │          Linear(768, 195)         │
       └─────────────────┬─────────────────┘                   └─────────────────┬─────────────────┘
                         │                                                       │
                         ▼                                                       ▼
                Predicts: 34 Crops                                      Predicts: 195 Classes
             (Apple, Tomato, Mango...)                                (Crop-Disease Pairs)
                         │                                                       │
                         └───────────────────────┬───────────────────────────────┘
                                                 │
                                                 ▼
                               ┌───────────────────────────────────┐
                               │     Hierarchical Gating Layer     │
                               │  Restricts Logits to Target Crop  │
                               └─────────────────┬─────────────────┘
                                                 │
                                                 ▼
                                     Final Precision Diagnosis:
                                       "Tomato - Early Blight"
                                  (Taxonomically Consistent)
```

### Architectural Tradeoffs:
1. **Unified Footprint:** A single ~109MB checkpoint handles both crop identification and disease diagnosis in one forward pass.
2. **Shared Representation Hypothesis:** By learning across all 78,955 training images simultaneously, the shared backbone is exposed to common fungal and bacterial patterns (such as powdery mildews or leaf spots) across multiple host species.
3. **Operational Modes & Error Propagation:**
   * **Crop-Conditioned Mode (User / Sensor Specified):** When an operator or host sensor confirms the crop (e.g. *"Tomato"*), non-target diseases are zeroed out. In this mode, cross-crop false positives are mathematically impossible.
   * **Autonomous Mode:** Head 1 predicts the crop autonomously, achieving **98.50% accuracy** on the test set. However, on the 1.50% of images where the crop head is wrong, hard gating forces a disease misclassification. This key bottleneck motivated my transition from hard masking to soft probabilistic gating in Chapter 7.

---

## 🎨 Chapter 3: Domain-Specific Data Augmentation for Foliar Pathology

Data augmentation in plant pathology requires domain-specific boundaries. In standard computer vision (e.g. object detection), aggressive color shifts and extreme crops are commonplace. In plant pathology, **unconstrained color and scale transforms can corrupt diagnostic biological signals**.

```
[Transforms Avoided for Pathology]            [Selected Domain-Specific Transforms]
❌ hue_shift = 0.1 (Inverts chlorosis signals) ✅ RandomHorizontalFlip (Leaves have no natural upright)
❌ RandomGrayscale (Removes necrosis cues)     ✅ RandomRotation(15°) (Natural wind & leaf tilt)
❌ scale = (0.2, 1.0) (Loses halo context)     ✅ scale = (0.75, 1.0) (Preserves margin context)
                                               ✅ RandomErasing (Simulates dew & partial occlusion)
```

---

### 1. Transforms Restricted to Preserve Pathology

#### Restricted #1: Hue Shifts (`transforms.ColorJitter(hue=0.1)`)
* **Impact on Pathology:** Foliar color is a primary diagnostic indicator:
  * A hue shift of `0.1` alters green leaf chlorophyll toward yellow, artificially mimicking the visual appearance of **Nitrogen Deficiency** or **Yellow Mosaic Virus** on healthy tissue.
  * It shifts reddish-brown *Puccinia* rust pustules toward unnatural hues.
* **Design Decision:** `hue` is locked to `0.0`. Modifying chlorophyll hues corrupts the label semantics.

#### Restricted #2: Grayscale Conversion (`transforms.RandomGrayscale(p=0.2)`)
* **Impact on Pathology:** In grayscale, a chlorotic yellow halo around a fungal lesion becomes difficult to separate from healthy green parenchyma under shadow. Stripping color removes critical diagnostic features.
* **Design Decision:** Excluded from the training pipeline.

#### Restricted #3: Aggressive Cropping (`transforms.RandomResizedCrop(scale=(0.2, 1.0))`)
* **Impact on Pathology:** On a $500 \times 500$ pixel leaf capture, a 20% area crop covers approximately $224 \times 224$ pixels. While not a 100×100 patch, cropping 20% often isolates an interior patch of a lesion while discarding the outer chlorotic margin and overall leaf structure needed to identify the host species.
* **Design Decision:** I adopt a conservative range: `scale=(0.75, 1.0)`. This aims to ensure that each crop retains at least $75\%$ to $100\%$ of the leaf area, keeping lesion borders and leaf outlines intact without severe interpolation artifacts.

---

### 2. The Four Preserved Transforms

1. **Spatial Invariance (Flips & Gentle Rotation):**
   * `RandomHorizontalFlip(p=0.5)`
   * `RandomVerticalFlip(p=0.5)`
   * `RandomRotation(degrees=15)`
   * *Rationale:* Leaves present at various angles across the canopy. A $\pm 15^\circ$ rotation introduces natural pose variation without generating excessive black border padding.
2. **Illumination Variance with Locked Hue:**
   * `ColorJitter(brightness=0.18, contrast=0.18, saturation=0.12, hue=0.0)`
   * *Rationale:* Simulates variable natural lighting conditions (direct sunlight vs. overcast sky) while strictly preserving chlorophyll color authenticity.
3. **Context-Preserving Receptive Field:**
   * `RandomResizedCrop((256, 256), scale=(0.75, 1.0), ratio=(0.85, 1.15))`
   * *Rationale:* Trims peripheral non-leaf borders while ensuring the model sees both lesion margins and leaf blade geometry.
4. **Occlusion Training via RandomErasing:**
   * `RandomErasing(p=0.2, scale=(0.02, 0.12), value=0)`
   * *Rationale:* Encourages the network to inspect distributed leaf regions rather than fixating on a single dominant spot. (Note: While RandomErasing reduces reliance on specific local pixels, image-level background shortcuts across datasets still require careful provenance auditing, as shown in Chapter 7).

---

## ⚖️ Chapter 4: Class Imbalance & Loss Formulation

My benchmark contains **195 classes** with high natural frequency imbalance:
* Large classes: `Banana - Sigatoka` (2,842 train images), `Tomato - Yellow Leaf Curl` (2,585 train images), `Ginger - Dehydrated` (2,096 train images).
* Minority conditions: `Broccoli - Healthy` (11 train images), `Cabbage - Tip Burn` (13 train images), `Ginger - ginger leaf spot` (13 train images).

To prevent large classes from dominating gradient updates, I combined two complementary sampling and loss mechanisms:

```
[Imbalanced Distribution: 11 to 2,842 images]
                       │
                       ▼
┌────────────────────────────────────────────────────────┐
│ 1. WeightedRandomSampler: Equalizes batch draw rates   │
│ 2. Class-Weighted Cross-Entropy: Adjusts gradients     │
│ 3. Label Smoothing (0.1): Smooths decision margins     │
│ 4. Multi-Task Combined Loss: Regularizes shared trunk  │
└────────────────────────────────────────────────────────┘
```

### 1. The Interaction Between `WeightedRandomSampler` and Loss Weighting
In my training configuration, I applied both `WeightedRandomSampler` and class-weighted Cross-Entropy loss:
* **`WeightedRandomSampler`:** Samples images with draw probability inversely proportional to class frequency ($w_i = 1 / N_{c}$), equalizing the expected number of exposures per class in each epoch.
* **Double-Weighting Nuance:** Applying inverse-frequency loss weights on top of an already-balanced sampling distribution represents an aggressive design choice against class collapse. However, it effectively amplifies minority-class updates twice: the sampler equalizes batch presence, and the loss weights multiply their gradient magnitude a second time.
* **Empirical Tradeoff:** This dual weighting encourages the model to over-predict small classes to minimize rare-class penalties, which directly aligns with my observed test benchmark where **Macro-Recall (90.79%) exceeds Macro-Precision (88.40%)**. This gradient distortion is also a recognized contributor to raw confidence miscalibration, necessitating post-hoc temperature scaling.
* **[Status as of v1.0]:** In the v1.0 release pipeline, retaining the dual-weighting scheme proved necessary to maintain viable recall across tail classes (<15 samples) without collapsing into majority-class modes. An isolated three-way ablation benchmark (Sampler-Only vs. Loss-Weights-Only vs. Focal Loss) is formally earmarked for future release iterations.

### 2. Label Smoothing (`0.1`) & Its Impact on Model Confidence
Standard one-hot Cross-Entropy targets assign probability $1.0$ to the true class and $0.0$ to all others:
$$\text{Target} = [0, 0, 1.0, 0, \dots, 0]$$
With **Label Smoothing ($\alpha = 0.1$)** across $K = 195$ classes, the target distribution becomes:
$$y_k = (1 - \alpha)\mathbf{1}_{k=y} + \frac{\alpha}{K} \approx 0.9005 \quad (\text{target}), \quad 0.0005 \quad (\text{non-targets})$$
* **The Smoothing Tradeoff:** Label smoothing successfully acts as a regularizer, softening decision boundaries between visually similar conditions (e.g. *Tomato Early Blight* vs. *Tomato Late Blight*).
* **The Underconfidence Consequence:** Spreading $10\%$ of probability mass across 194 non-target classes suppresses the peak logit during training. Combined with softmax dispersion over 195 outputs, this directly contributed to the model's observed **underconfidence** on the test set (where unscaled mean confidence was only $67.79\%$ despite $92.26\%$ accuracy), requiring validation temperature scaling ($T=0.6228$) to restore calibration.

### 3. Multi-Task Combined Loss
$$\mathcal{L}_{\text{total}} = \mathcal{L}_{\text{disease}} + 0.4 \times \mathcal{L}_{\text{crop}}$$
The auxiliary crop classification task forces the backbone to maintain macro-botanical features alongside micro-pathological lesion patterns.

---

## ⏱️ Chapter 5: Two-Phase Fine-Tuning on 4GB VRAM: Complete Training Recipe

Training ConvNeXt-Tiny across 78,955 training images on an NVIDIA GeForce RTX 3050 Laptop GPU (4.0 GB VRAM) was managed via a structured two-phase schedule implemented in `src/models/train_dualhead.py`:

### 1. Hardware, Precision & Memory Envelope
* **Mixed Precision (`torch.cuda.amp.autocast(dtype=torch.float16)`):** Activations and linear projections execute in FP16 via an automatic gradient scaler (`GradScaler`), reducing peak activation memory by ~48% and leveraging Tensor Cores.
* **Batch Budget:** Standardized at `batch_size=16` at input resolution $256 \times 256$, fitting comfortably within ~3.6 GB peak VRAM.
* **Wall-Clock Training Time:** Approximately **4.5 hours** across the full 18-epoch schedule on consumer hardware.

### 2. The Two-Phase Staged Training Recipe

```
Phase 1: Head Warmup (Epochs 1–3)           Phase 2: Joint Fine-Tuning (Epochs 4–18)
─────────────────────────────────────────   ──────────────────────────────────────────────
• Backbone: 100% FROZEN (requires_grad=F)   • Backbone: UNFROZEN Stages 2 & 3 (Layer-decay)
• Heads: TRAINED (LR = 3e-4)                • Heads: TRAINED (LR = 1.5e-4, 50% warmup LR)
• Optimizer: AdamW (weight_decay=1e-4)      • Stage 3 LR: 1e-5 | Stage 2 LR: 5e-6
• Scheduler: None (Constant LR)             • Scheduler: CosineAnnealingLR (T_max=15, eta_min=1e-6)
• Goal: Stabilize random MLP projections    • Goal: Gentle foliar feature adaptation
```

#### Detailed Phase Mechanics:
1. **Phase 1 (Heads Warmup — Epochs 1 to 3):**
   - **Backbone State:** All 4 ConvNeXt stages frozen (`model.freeze_all_backbone()`).
   - **Optimizer:** `torch.optim.AdamW(params, lr=3e-4, weight_decay=1e-4)`.
   - **Rationale:** Randomly initialized linear heads produce high initial gradient variance. Freezing the trunk prevents these early gradients from shattering pretrained ImageNet representations.
2. **Phase 2 (Joint Fine-Tuning — Epochs 4 to 18):**
   - **Backbone State:** Stages 2 and 3 unfreezed (`model.unfreeze_stages(stages=[2, 3])`), keeping Stage 0 and Stage 1 stem filters frozen to preserve fundamental edge/color primitives.
   - **Differential Parameter Groups:**
     $$\eta_{\text{heads}} = 1.5 \times 10^{-4}, \quad \eta_{\text{stage3}} = 1.0 \times 10^{-5}, \quad \eta_{\text{stage2}} = 5.0 \times 10^{-6}$$
   - **Optimizer & Scheduler:** `torch.optim.AdamW(params, weight_decay=1e-4)` modulated by `torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=15, eta_min=1e-6)`.
3. **Model Selection & Checkpointing:**
   - Production weights are saved strictly whenever the validation **crop-masked disease accuracy** reaches a new high (`masked_acc > best_masked_acc`).
   - Resumable state checkpoints serialize `model_state`, `optimizer_state`, `scheduler_state`, `scaler_state`, and active MLflow run identifiers, enabling fault-tolerant resumption if thermally throttled.

---

## 🚀 Chapter 6: Production Inference & Operational Modes

Why is hierarchical gating executed dynamically in the serving pipeline rather than hard-wired into static model weights?
Decoupling the gating logic from the neural network backbone allows a single unified checkpoint (~109MB) to serve two fundamentally different real-world operational workflows with zero memory overhead:
1. **Operator-Guided Mode:** When a human operator specifies their host crop, non-target categories are zeroed out at inference time, mathematically eliminating cross-species misdiagnoses.
2. **Autonomous Screening Mode:** When scouting unassisted, the model computes joint soft probabilities across all candidate crops, propagating uncertainty rather than propagating brittle hard decisions.

Here is the operational implementation deployed in `serving/inference.py`:

```python
@app.post("/predict")
async def predict_plant_disease(
    file: UploadFile = File(...),
    crop: Optional[str] = Query(None, description="Optional: specific crop name (e.g. 'Tomato')")
):
    image_tensor = preprocess(file)
    
    # 1. Forward pass through ConvNeXt-Tiny
    crop_logits, disease_logits = model(image_tensor)
    
    # 2. Temperature scaling (fitted on validation split)
    T_disease = 0.6228
    T_crop = 0.7016
    
    if crop is not None:
        # Mode A: Crop-Conditioned (Farmer / Sensor confirmed)
        # Evaluates disease logits strictly within the specified crop family
        allowed_indices = crop_hierarchy["crop_to_class_indices"][crop]
        sub_logits = disease_logits[:, allowed_indices] / T_disease
        p_disease = softmax(sub_logits, dim=-1)
        best_local_idx = argmax(p_disease)
        best_global_idx = allowed_indices[best_local_idx]
        
        return {
            "mode": "crop_conditioned",
            "crop": crop,
            "disease": class_names[best_global_idx],
            "confidence": float(p_disease[best_local_idx]),
            "cross_crop_error_risk": "0.000% (Enforced by user crop lock)"
        }
    else:
        # Mode B: True Autonomous Joint Soft Gating
        # Vectorized scoring across all 195 classes:
        # P(disease_i) = sum_c [ P(crop = c) * P(disease_i | crop = c) ]
        # M is precomputed (34, 195) binary mask: 0.0 for members, -inf for non-members
        p_crop = softmax(crop_logits / T_crop, dim=-1)                        # (1, 34)
        masked_d = (disease_logits.unsqueeze(1) / T_disease) + M.unsqueeze(0) # (1, 34, 195)
        p_d_given_c = softmax(masked_d, dim=-1)                               # (1, 34, 195)
        p_joint = (p_crop.unsqueeze(-1) * p_d_given_c).sum(dim=1).squeeze(0) # (195,)
        
        # Globally optimal disease selected over all 195 classes
        best_global_idx = argmax(p_joint)
        predicted_crop = class_to_crop_name[best_global_idx]
        
        return {
            "mode": "autonomous_soft_gated",
            "predicted_crop": predicted_crop,
            "disease": class_names[best_global_idx],
            "calibrated_confidence": float(p_joint[best_global_idx]),
            "crop_head_error_margin": "1.50% (Test set crop head error rate)"
        }
```
*(Note on class indexing: In early prototype drafts, 198 raw classes were indexed before retiring unviable singletons to achieve the 195-class prerelease baseline; the active v1.0 release is standardized to 177 classes across 33 crops).*

### The Two User Experiences:
1. **The Casual Gardener (Autonomous Mode):**
   * Uploads an image without knowing what plant it is.
   * Head 1 identifies the plant as `Grape` (e.g. $99.6\%$ confidence, illustrative example).
   * Soft gating evaluates joint probabilities, diagnosing `Grape - Black Rot` (e.g. $98.1\%$ confidence, illustrative example).
2. **The Commercial Farmer (Crop-Conditioned Mode):**
   * Selects `Apple` in the app.
   * The model immediately zeros out all non-apple disease logits.
   * The diagnosis is selected strictly from the 6 Apple classes. **Cross-crop false positives drop to 0.000% within the evaluated partition (assuming the user correctly selects the host crop).**

---

## 🔬 Chapter 7: Post-Training Reality — What the Model Taught Me, What Broke, and What I Changed

> ⚠️ **Historical Context Note:** The failure modes, provenance audits, and calibration metrics in this chapter document my 195-class prerelease checkpoint ($N=9,327$ test images). For the official v1.0 production release metrics ($N=9,658$ purified test split, 177 classes, 33 crops), refer to [v1.0 Model Card](../../models/v1/model_card.md) and [Dataset Card](../DATASET_CARD.md).

Training completed at Epoch 17, producing a model with **95.27% test accuracy** and **93.45% macro-F1** across 9,327 unseen images. But real engineering begins when you stop looking at aggregate averages and audit the failure modes.

Here is what I observed in the trenches after training, what broke under scrutiny, and the concrete mathematical and architectural changes I introduced.

---

### 1. The Zero-F1 Mystery: Why Large Classes Failed Completely

Two large test classes collapsed to **0.0% F1-score**, despite the crop head correctly identifying their botanical family:
* `Citrus - citrus greening disease` (71 test images) $\rightarrow$ 0% accuracy, 69 misclassified as `Citrus - Black spot`.
* `Soybean - Healthy` (60 test images) $\rightarrow$ 0% accuracy, 26 misclassified as `Soybean - Downy Mildew`, 25 as `Soybean - Rust`.

When classes with 60–70 test images fail completely while their crop head is 100% correct, the issue is almost never "visual ambiguity". An exhaustive provenance audit across image filenames and source datasets revealed the root cause: **Cross-Dataset Source Shift**.

```
[Citrus Greening]
Train: 100% PlantVillage Lab Images (Uniform Gray Backgrounds)
Test : 100% Sourabh Natural-Background Images (Natural Sunlight & Foliage)
Train Sourabh Data: 100% Citrus - Black spot!
──► Result: The model learned "Sourabh photographic style = Black spot".
```

* In the training set, `Citrus - citrus greening disease` was sourced entirely from PlantVillage laboratory studio images (`UF.Citrus_HLB` / `CREC`). The test set was sourced entirely from the Sourabh dataset. But in the training set, all Sourabh specimens belonged to `Citrus - Black spot`! When presented with a Sourabh test image, the model latched onto camera, illumination, and background signatures rather than foliar pathology, routing 69 of 71 leaves to Black spot.
* In `Soybean - Healthy`, training data was 100% PlantVillage lab images, while test images came 100% from the Vaishali natural-background dataset. During training, the only Vaishali images the network ever saw had severe rust lesions. When shown a healthy natural-background leaf from the same camera distribution, the network defaulted to `Soybean - Rust` or `Downy Mildew`.

**[Planned] Remediation:**
* Update diagnostic benchmarks to treat these failures as domain shifts rather than intrinsic visual confusions.
* Restructure future benchmark splits using **source-stratified partitioning** so that multi-source classes have balanced domain representation across train, val, and test partitions.

---

### 2. The Symptom Overlap in Ginger: Label Granularity Under Review

`Ginger - Dehydrated` achieved only **45.8% accuracy** on 262 test images, confounding heavily with `Ginger - Pest Damage` (109 errors) and `Ginger - Leaf Blight` (32 errors).

* **The Biological Reality:** In ginger (*Zingiber officinale*), severe drought stress, fungal blight (*Phyllosticta zingiberi*), and stem borer damage all culminate in identical curled, necrotic brown leaf margins.
* **[Planned] Remediation:** 
  1. Audit a representative sample of 50 images per class to establish clearer annotation guidelines.
  2. For targeted foliar pathology identification, investigate grouping overlapping stress categories when model confidence is split.
  3. Implement a selective prediction threshold (predicting "uncertain / defer to human scout") when margins between these classes are narrow.

---

### 3. The Capsicum Overlap: Chilli vs. Bell Pepper

`Bell Pepper - Leaf Curl Virus` suffered **0% crop accuracy** on 14 test images, with all 14 routed to Chilli. Reciprocally, `Chilli - Leaf Curl Virus` confused 23 times with Bell Pepper.

* **The Botanical Reality:** Chilli and Bell Pepper are cultivars of the exact **same botanical species (*Capsicum annuum*)**, distinguished primarily by fruit pungency and pod shape rather than foliar anatomy. Viral leaf curl morphology (begomovirus transmitted by whiteflies) produces identical upward leaf curling and stunted vein thickening on both varieties. Expecting a foliar vision model to separate them reliably from leaves alone is botanically unrealistic.
* **[Planned] Remediation:**
  * Treat *Capsicum* as a unified botanical clade for foliar gating, or provide dedicated paired high-resolution canopy data to separate Bell Pepper and Chilli prior to disease diagnosis.

---

### 4. The ECE Calibration Illusion: From Denominator Truncation to True Temperature Scaling

My initial evaluation report claimed that Expected Calibration Error (ECE) plummeted from **24.5% (raw)** to **1.63% (hard-masked)**.

On closer mathematical inspection, this claim was misleading:
1. **Why Raw ECE was 24.5%:** The unassisted 195-class head had **92.26% test accuracy**, but an average top-1 softmax confidence of only **67.79%**. Due to probability dispersion over 195 logits, class-weighted cross-entropy loss, and label smoothing, the raw model was **underconfident by 24.47%**.
2. **Why Hard Masking showed 1.63%:** Setting 190+ logits to $-10^9$ truncated the softmax denominator from 198 down to $\sim 5.8$ classes per crop. This mathematical truncation artificially boosted mean confidence from 67.79% up to **91.96%**. Because 91.96% coincidentally matched test accuracy (95.27%), ECE appeared to vanish ($|91.96 - 92.26| \approx 0.44\%$). It was an artifact of denominator truncation, not authentic probability calibration.

```
[Raw 195-Class Softmax]                     [Hard-Masked Sub-Softmax]
Denominator: 195 classes                    Denominator: ~5 classes per crop
Mean Confidence: 67.79% (Underconfident)    Mean Confidence: 91.96% (Artificially Inflated)
Accuracy: 92.26% ──► ECE = 24.47%           Accuracy: 95.27% ──► ECE = 1.63% (Denominator Artifact)
```

**What I Changed & Why:**
* **Validation Temperature Scaling:** I fit a scalar temperature parameter on the held-out **validation set** via L-BFGS to minimize Negative Log-Likelihood:
  $$T_{\text{disease}} = 0.6228, \quad T_{\text{crop}} = 0.7016$$
  Because $T < 1.0$, temperature scaling sharpens the underconfident logits.
  * **Result:** Raw backbone ECE dropped from **24.47% down to 1.02%**, and Maximum Calibration Error (MCE) dropped from **45.89% down to 5.99%**! The raw backbone is natively well-calibrated once temperature-scaled.
* **Generated Full Reliability Diagrams:** Plotted complete 4-panel calibration curves and confidence histograms in `models/reliability_diagrams_comprehensive.png`.

---

### 5. Architectural Upgrade: Soft Gating over Hard Masking

In my original design, I used hard binary masking:
$$\text{logits}_{\text{disallowed}} = -10^9$$

* **Why Hard Masking Broke:** Hard masking implicitly assumes the crop head has $100\%$ accuracy ($P(\text{crop})=1.0$). While hard masking rescued 32 cross-crop raw errors, **it broke 17 images where the raw disease head was correct but the crop head made an error**, completely locking out the true disease.
* **The Soft Gating Formulation:** I replaced hard truncation with a mathematically sound joint probability distribution:
  $$P(\text{disease}_i) = P(\text{crop} = \text{crop}(i)) \times P(\text{disease}_i \mid \text{crop} = \text{crop}(i))$$
  where $P(\text{crop})$ is the temperature-scaled softmax over the 34 crop logits, and $P(\text{disease}_i \mid c)$ is the softmax over the disease logits belonging to that crop.

```
                                  Input Image
                                       │
                      ┌────────────────┴────────────────┐
                      ▼                                 ▼
               Crop Head Logits               Disease Head Logits
                      │                                 │
             Softmax / T_crop                  Softmax / T_disease
                      │                       (Restricted to Crop)
                      ▼                                 ▼
                   P(Crop)               ×      P(Disease | Crop)
                      └────────────────┬────────────────┘
                                       │
                                       ▼
                       Joint Probability P(Disease)
                      (Sums strictly to 1.0 over 195 classes!)
```

#### The Empirical Comparison on 9,327 Held-Out Test Images:

| Gating Mechanism | Top-1 Accuracy | Rescued vs. Raw | Broken vs. Raw | Net Image Delta | Calibrated ECE |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Raw Disease Head** | 92.26% | — | — | Baseline | **1.02%** (Temp Scaled) |
| **Hard Binary Masking** | 95.27% | 32 images | 17 images | +15 images | 1.63% (Truncated) |
| **Soft Hierarchical Gating** | **`92.42%`** | **32 images** | **16 images** | **`+16 images`** | **`2.63%`** (Joint Calibrated) |

* **Balanced Analysis:** Soft gating provides a modest net gain of $+1$ image over hard masking (+16 vs +15 over raw). Its principal advantage is theoretical and operational soundness: it yields a valid probability measure ($\sum P_i = 1.0$) that natively propagates crop uncertainty, whereas hard masking assumes infallible crop detection. Note that its ECE (2.63%) is slightly higher than the temperature-scaled raw head (1.02%) because it integrates crop head uncertainty into the joint confidence distribution.

---

## ⚠️ Chapter 8: Known Limitations & Next Steps

A credible benchmark requires clear documentation of its experimental boundaries:

1. **Single Evaluation Run & Variance:** All reported numbers stem from a single training run. Evaluating across 3 random seeds to report mean $\pm$ standard deviation and calculating bootstrap confidence intervals (e.g. for Macro-F1) is necessary before publishing formal benchmark claims.
2. **Independence Assumptions in Statistical Tests:** McNemar's test yielded $p = 0.045$ on the 49 discordant samples ($b=32, c=17$). However, near-duplicate images across video bursts or sequential captures in source datasets can violate sample independence, making this marginal significance indicative rather than definitive.
3. **Shared Source Split Limitation:** Although train, val, and test splits are strictly disjoint at the image level, they are partitioned from the same upstream datasets. This setup evaluates within-distribution generalization, but does not measure robustness against external distribution shifts.
4. **Minority Class Noise:** Classes with fewer than 15 test samples (e.g. `Broccoli - Healthy` with $N=2$, `Zucchini - bacterial leaf spot` with $N=2$) have high empirical variance; Wilson score intervals are needed to convey uncertainty on small cohorts.
5. **[Planned] External Generalization Benchmark:** The definitive validation of my model will be evaluating against completely external datasets (e.g. PlantDoc) and self-captured natural-background photographs from local farms. No independent field evaluation has been conducted.

---

## 🏆 Epilogue: The Architecture Manifesto

Building an agricultural AI system is not about downloading the heaviest model on Hugging Face and claiming high validation scores. It requires an honest intersection of **biology, optics, mathematics, and hardware constraints**:

1. **Architecture:** I selected **ConvNeXt-Tiny** because its $7 \times 7$ kernels capture lesion halos natively, and its LayerNorm provides batch-size independent normalization within a 4GB RTX 3050 budget.
2. **Hierarchy:** I transitioned from naive independent models to a **single unified dual-head model**, and advanced from brittle hard masking to **probabilistic soft gating** ($P(\text{disease}) = P(\text{crop}) \times P(\text{disease} \mid \text{crop})$).
3. **Calibration:** I dismantled the ECE denominator illusion and proved that validation-fitted temperature scaling ($T=0.623$) achieves an authentic **1.02% ECE** on the raw backbone.
4. **Data Preprocessing & Provenance:** I constrained dangerous hue shifts to protect chlorophyll biology while tracking cross-dataset source shifts to detect domain artifacts.

The model serves as a strong, memory-efficient laboratory and benchmark prototype. Addressing dataset domain shifts, establishing confidence intervals, and validating against truly external natural-background captures remain the necessary steps before real-world deployment. No independent field evaluation has been conducted.

---

## 📚 References

1. **Showrav, M. T. T., Bain, S., Hossain, M., Ahmed, K. I., Fattah, S. A., & Ahmed, S. (2022).** *"A Two-stage Approach for Plant Disease Classification Based on Deep Neural Networks and Transfer Learning."* In *2022 12th International Conference on Electrical and Computer Engineering (ICECE)*, Dhaka, Bangladesh, pp. 248–251. DOI: [10.1109/ICECE57408.2022.10088574](https://doi.org/10.1109/ICECE57408.2022.10088574).
2. **Vallabhajosyula, S., et al. (2024).** *"A novel hierarchical framework for plant leaf disease detection using residual vision transformer."* *Heliyon*, 10(8), e29912. DOI: [10.1016/j.heliyon.2024.e29912](https://doi.org/10.1016/j.heliyon.2024.e29912).
3. **Liu, Z., Mao, H., Wu, C. Y., Feichtenhofer, C., Darrell, T., & Xie, S. (2022).** *"A ConvNet for the 2020s."* In *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)*, pp. 11976–11986. DOI: [10.1109/CVPR52688.2022.01167](https://doi.org/10.1109/CVPR52688.2022.01167).
4. **Guo, C., Pleiss, G., Sun, Y., & Weinberger, K. Q. (2017).** *"On Calibration of Modern Neural Networks."* In *International Conference on Machine Learning (ICML)*, PMLR 70, pp. 1321–1330.



