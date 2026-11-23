# 🌿 Model Card: DualHead ConvNeXt-Tiny (v1 Baseline)

## 1. Model Details
- **Model Name:** DualHead ConvNeXt-Tiny (v1)
- **Architecture:** Hierarchical Dual-Head Convolutional Network
  - **Backbone:** ConvNeXt-Tiny (7×7 depthwise convolutions, LayerNorm, 768-dim embedding)
  - **Crop Head:** Linear(768 → 256) → LayerNorm → GELU → Dropout(0.2) → Linear(256 → 34)
  - **Disease Head:** Linear(768 → 512) → LayerNorm → GELU → Dropout(0.3) → Linear(512 → 198)
- **Parameter Count:** 28,642,726 parameters (~109 MB state_dict)
- **Primary Configuration:** **Autonomous Soft Hierarchical Gating with Validation Temperature Scaling**
  - Disease temperature: $T_{\text{disease}} = 0.6228$
  - Crop temperature: $T_{\text{crop}} = 0.7016$
  - Joint scoring across all 198 classes: $P(\text{disease}_i) = P(\text{crop}=\text{crop}(i)) \times P(\text{disease}_i \mid \text{crop}=\text{crop}(i))$
  - Decision: $\arg\max_{i \in \{1,\dots,198\}} P(\text{disease}_i)$
- **Release Version:** `v1` (Frozen Baseline)
- **Release Date:** October 2026

---

## 2. Intended Use
- **Primary Domain:** Automated foliar screening for commercial agricultural robotics and targeted foliar diagnosis.
- **Input Modality:** Single-leaf RGB photographic captures ($256 \times 256$ pixels).
- **Supported Taxa:** 34 agricultural crops spanning 198 fine-grained pathological conditions and healthy controls.

---

## 3. Evaluation Benchmark (Held-Out Test Set: 10,458 Images)

The table below contrasts the three decision configurations separately on the exact same 10,458 test samples:

| Metric | Raw Disease Head (Unassisted) | Hard Binary Masking | **Soft Hierarchical Gating (Primary)** |
| :--- | :---: | :---: | :---: |
| **Top-1 Accuracy** | **`92.26%`** (9,649 / 10,458) | **`92.40%`** (9,663 / 10,458) | **`92.42%`** (9,665 / 10,458) |
| **Total Test Errors** | 809 errors | 795 errors | **793 errors** |
| **Net Gain vs. Raw** | Baseline | +14 images | **+16 images** |
| **Rescued vs. Raw** | — | 31 images | **32 images** |
| **Broken vs. Raw** | — | 17 images | **16 images** |
| **Macro-F1 (198 classes)**| 88.35% | 88.51% | **88.51%** |
| **Weighted-F1** | 92.18% | 92.32% | **92.34%** |
| **Macro-Precision** | 88.12% | 88.40% | **88.41%** |
| **Macro-Recall** | 90.65% | 90.79% | **90.80%** |
| **Expected Calibration Error (ECE)** | **`1.02%`** (Temp-Scaled, $T=0.623$) | 1.63% (Truncated Denominator) | **2.63%** (Joint Calibrated) |
| **Maximum Calibration Error (MCE)** | **`5.99%`** | 24.25% | **37.30%** |

### Botanical Crop Head Performance:
- **Crop Accuracy:** **`98.50%`** (10,301 / 10,458 leaves correctly identified across 34 crops)
- **Crop Macro-F1:** **`96.51%`**

---

## 4. Known Limitations & Failure Modes

1. **Collapsed 0%-F1 Classes (Cross-Dataset Source Confounding):**
   - `Citrus - citrus greening disease` (71 test images) collapsed to **0.0% F1** (69 misclassified as `Citrus - Black spot`). Proven to be caused by source confounding: training data was 100% PlantVillage laboratory studio images, while test data was 100% Sourabh field images where all training specimens were `Black spot`.
   - `Soybean - Healthy` (60 test images) collapsed to **0.0% F1** (misclassified as `Downy Mildew` and `Rust`). Caused because test images came 100% from Vaishali field photography, whose training images were exclusively diseased.
2. **Limited Separability in *Capsicum annuum* (Chilli vs. Bell Pepper):**
   - Chilli and Bell Pepper are cultivars of the exact same botanical species (*Capsicum annuum*). Fungal and viral leaf-curl symptoms exhibit **limited separability** from foliar blade morphology alone in the absence of mature fruit pods, accounting for 71 cross-crop errors.
3. **Not Validated on External Field Data:**
   - Although train, val, and test splits are strictly disjoint at the image level, they are partitioned from the same upstream repository sources. The model has **not yet been validated on external out-of-distribution field data** (e.g., completely independent smartphone captures from diverse geographic regions).
4. **Minority Class Noise:**
   - 49 classes contain fewer than 15 test samples (e.g. `Broccoli - Healthy` $N=2$). High variance exists on these small cohorts; Wilson score intervals are recommended when interpreting individual minority metrics.
