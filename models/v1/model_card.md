# Model Card: ConvNeXt-Tiny DualHead (Model v1.0)

**Model Version:** Model v1.0 (Curated Production Release)  
**Dataset:** Dataset v1.0 (`reports/v1/dataset_v1.csv`)  
**Weights File:** `models/v1/model_dualhead_convnext_tiny.pth`  
**Architecture:** ConvNeXt-Tiny DualHead (33 botanical host crops, 177 foliar disease classes)  
**Input Resolution:** 256x256 RGB  
**Scope:** Foliar plant leaf disease image classifier. Does not provide chemical treatment recommendations or control physical equipment.  
**Licensing & Distribution:** Code is licensed under MIT (`LICENSE`); model weights and dataset manifests are released under CC BY-NC-SA 4.0 for non-commercial research use only. Raw images are not redistributed.

---

> [!IMPORTANT]
> **Core Benchmark Disclaimer:**  
> All metrics are measured on the held-out test split of the curated dataset, which shares sources with the training data. No independent field evaluation has been done; real-world accuracy is unknown. Treat as an in-distribution research baseline.

---

## 1. Verified Benchmark Performance

All figures are computed strictly through `src.models.predict.predict_tensor` on CPU from `reports/v1/results.json`:

### Leak-Checked Test Split (N=9,279)
- **Crop Accuracy:** **99.28%** (95% Bootstrap CI: [99.11%, 99.44%])
- **Soft-Gated Disease Accuracy:** **96.02%** (about 96.0%; 95% Bootstrap CI: [95.62%, 96.45%])
- **Raw Disease Accuracy:** **95.83%** (95% Bootstrap CI: [95.42%, 96.25%])
- **Macro-F1 (All 177 Classes):** **93.86%** (95% Bootstrap CI: [91.84%, 94.42%])
- **Macro-F1 (classes with >=10 test images, 147 Classes):** **96.54%** (95% Bootstrap CI: [95.96%, 97.00%])
- **Calibrated Expected Calibration Error (ECE, 15 bins):** **0.57%**
- **Calibration Temperatures:** $T_{\text{crop}} = 0.5931$, $T_{\text{disease}} = 0.5013$

### Operating Threshold Behavior ($\tau = 0.60$)
- **Covered Subset:** 8,999 / 9,279 images (96.98% coverage)
- **Covered Accuracy:** **97.52%** (8,776 / 8,999 correct)
- **Uncertain Subset:** 280 / 9,279 images (3.02% flagged)
- **Uncertain Accuracy:** 47.86% (134 / 280 correct)
- **Total Correct:** 8,910 / 9,279 (**96.02%**)

### Relative Performance vs Prerelease Baseline
On identical, unchanged classes evaluated on the shared leak-checked test split, Model v1 demonstrates an improvement of **+0.56 pts** (95% CI: [+0.22, +0.90]) over the prerelease baseline.

---

## 2. Runtime Profile

Empirically measured via `scripts/v1/measure_runtime.py` across 200 clean test images (single image, batch size 1) and 2 concurrent requests. Source: `reports/v1/runtime_profile.json`.

### Hardware Specification
- **CPU:** AMD Ryzen 7 6800H with Radeon Graphics (8 threads)
- **GPU:** NVIDIA GeForce RTX 3050 Laptop GPU
- **PyTorch Version:** 2.6.0+cu124

### CPU Profile
- **Bundle Load Time:** 0.3876 s
- **Peak RSS during Bundle Load:** 784.93 MB
- **Warm-Up Time:** 56.12 ms (0.0561 s)
- **Latency per Image (p50):** 53.01 ms (forward pass) / 54.79 ms (end-to-end)
- **Latency per Image (p95):** 59.34 ms (forward pass) / 63.36 ms (end-to-end)
- **Peak RSS during 2 Concurrent Requests:** 855.44 MB

### GPU Profile (CUDA)
- **Bundle Load Time:** 0.5943 s
- **Peak RSS during Bundle Load:** 978.70 MB
- **Warm-Up Time:** 235.63 ms (0.2356 s)
- **Latency per Image (p50):** 9.08 ms (forward pass) / 11.25 ms (end-to-end)
- **Latency per Image (p95):** 12.84 ms (forward pass) / 18.26 ms (end-to-end)
- **Peak RSS during 2 Concurrent Requests:** 1321.20 MB

---

## 3. Limitations and Known Boundaries

1. **Held-Out Test In-Distribution Scope:**  
   All reported accuracy is derived from held-out splits of the curated dataset. No independent field evaluation has been conducted; generalization to natural farm conditions is unverified.
2. **Small Support Classes (30 Classes with < 10 Clean Test Images):**  
   30 classes have fewer than 10 clean test images, resulting in wider confidence intervals for those specific conditions (full table at `reports/v1/per_class_results.csv`):
   - `Jamun - Bacterial Spot`: 1 clean test image ($N=31$ total test)
   - `Apple - apple mosaic virus`: 3 clean test images ($N=3$ total test)
   - `Bean - bean halo blight`: 3 clean test images ($N=3$ total test)
   - `Blueberry - blueberry scorch`: 3 clean test images ($N=3$ total test)
   - `Broccoli - Healthy`: 3 clean test images ($N=3$ total test)
   - `Broccoli - broccoli alternaria leaf spot`: 3 clean test images ($N=3$ total test)
   - `Cabbage - Tip Burn`: 3 clean test images ($N=3$ total test)
   - `Ginger - ginger leaf spot`: 3 clean test images ($N=3$ total test)
   - `Peach - peach leaf shot hole`: 3 clean test images ($N=3$ total test)
   - `Soybean - Brown Spot`: 3 clean test images ($N=3$ total test)
   - `Sugarcane - Mosaic`: 3 clean test images ($N=3$ total test)
   - `Bean - bean mosaic virus`: 4 clean test images ($N=4$ total test)
   - `Blueberry - blueberry rust`: 4 clean test images ($N=4$ total test)
   - `Cauliflower - Blackrot`: 4 clean test images ($N=4$ total test)
   - `Jamun - Brown Blight`: 4 clean test images ($N=32$ total test)
   - `Sugarcane - Rust`: 4 clean test images ($N=4$ total test)
   - `Grape - grape leafroll disease`: 6 clean test images ($N=6$ total test)
   - `Jamun - Healthy`: 6 clean test images ($N=22$ total test)
   - `Pear - pear leaf curl`: 6 clean test images ($N=6$ total test)
   - `Soybean - Downy Mildew`: 6 clean test images ($N=6$ total test)
   - `Zucchini - Healthy`: 6 clean test images ($N=6$ total test)
   - `Banana - banana black leaf streak`: 7 clean test images ($N=7$ total test)
   - `Cabbage - Healthy`: 7 clean test images ($N=7$ total test)
   - `Cabbage - cabbage alternaria leaf spot`: 7 clean test images ($N=7$ total test)
   - `Soybean - Cercospora Leaf Blight`: 7 clean test images ($N=7$ total test)
   - `Soybean - Powdery Mildew`: 7 clean test images ($N=12$ total test)
   - `Cabbage - cabbage downy mildew`: 8 clean test images ($N=8$ total test)
   - `Cherry - cherry leaf spot`: 8 clean test images ($N=8$ total test)
   - `Citrus - Citrus Hindu mite`: 8 clean test images ($N=8$ total test)
   - `Sugarcane - Yellow`: 9 clean test images ($N=9$ total test)

3. **Near-Tie Class Pairs (Top-2 Joint Margin < 0.05):**  
   Across the 9,279 clean test images evaluated via `src.models.predict.predict_tensor`, 54 unique class pairs exhibit near-tie predictions where the top-2 joint probability margin is under 0.05. Key examples:
   - `Banana - Sigatoka vs Banana - banana black leaf streak`: 2 occurrences (mean margin: 0.0201, min: 0.0000)
   - `Ginger - Dehydrated vs Ginger - Leaf Blight`: 5 occurrences (mean margin: 0.0286, min: 0.0195)
   - `Potato - Early Blight vs Tomato - Bacterial Spot`: 3 occurrences (mean margin: 0.0195, min: 0.0021)
   - `Ginger - Dehydrated vs Ginger - Pest Damage`: 2 occurrences (mean margin: 0.0360, min: 0.0354)
   - `Ginger - Healthy vs Ginger - Leaf Blight`: 2 occurrences (mean margin: 0.0298, min: 0.0146)
   - `Ginger - Leaf Blight vs Ginger - Pest Damage`: 2 occurrences (mean margin: 0.0135, min: 0.0010)
   - `Tomato - Bacterial Spot vs Tomato - tomato mosaic virus`: 2 occurrences (mean margin: 0.0138, min: 0.0046)
   - Additional single-occurrence near-ties: `Banana - Panama vs Banana - banana bunchy top` (margin: 0.0291), `Banana - Pestalotiopsis vs Banana - Sigatoka` (margin: 0.0398), `Bean - bean halo blight vs Bean - bean leaf shot hole` (margin: 0.0042), `Bean - bean mosaic virus vs Potato - potato virus` (margin: 0.0115), `Bean - bean rust vs Soybean - Rust` (margin: 0.0204), `Apple - Rust vs Bean - bean rust` (margin: 0.0275), `Peach - Healthy vs Peach - peach leaf shot hole` (margin: 0.0205), `Potato - Early Blight vs Tomato - tomato early blight` (margin: 0.0218), `Bell Pepper - Healthy vs Cucumber - cucumber bacterial wilt` (margin: 0.0199), `Bell Pepper - bell pepper frogeye leaf spot vs Chilli - Cercospora Leaf Spot` (margin: 0.0236), `Apple - apple black rot vs Coffee - coffee leaf rust` (margin: 0.0063), `Blueberry - blueberry rust vs Soybean - Brown Spot` (margin: 0.0366), `Cabbage - cabbage downy mildew vs Cherry - cherry leaf spot` (margin: 0.0476).

4. **P-006 Relabeled Classes:**  
   9 classes touched by Patch P-006 have clean test support $N < 10$ and are marked as not independently evaluated.
5. **Near-Duplicate Twins Within-Split & Validation Split Leakage:**  
   - **Within-Split Near-Duplicates (`reports/v1/twin_check.json`):** Perceptual hashing ($d \le 4$) identifies redundant within-split twin pairs: Train within-split contains 2,464 pairs (853 exact $d=0$, 1,611 near $d \in [1, 4]$); Val within-split contains 49 pairs (34 exact $d=0$, 15 near $d \in [1, 4]$); Test within-split contains 56 pairs (34 exact $d=0$, 22 near $d \in [1, 4]$).  
   - **Residual Validation Leakage:** The validation split retains 260 cross-split perceptual hash ($d \le 4$) twin pairs with the training set (145 exact 0-bit, 115 near-duplicate), spanning 162 unique validation images (`reports/v1/twin_check.json`; dry-run removal plan saved at `reports/v1/p008_plan_DRYRUN.csv`). Test split cross-split leakage has been completely resolved via Patch P-007 (181 test frames quarantined, logged in `reports/v1/removed_p007_images.csv`), leaving 0 test-train and 0 test-val twin pairs across all 9,279 purified test images.
6. **Threshold Validation Tuning:**  
   The confidence threshold $\tau = 0.60$ was tuned strictly on the curated validation split.
7. **Temperature Scaling ($T < 1$):**  
   Calibration temperatures ($T_{\text{crop}}=0.5931$, $T_{\text{disease}}=0.5013$) are below 1.0. The mechanism behind $T < 1$ is unexplained; label smoothing is only a hypothesis.
8. **Dual Confidence Definitions:**  
   In auto mode, confidence is a raw joint product $P(\text{crop}) \times P(\text{disease})$. When an optional `crop` parameter is supplied, probabilities are renormalized across that crop's classes, producing non-comparable values that were not independently evaluated.
9. **No Out-of-Distribution Detector:**  
   The model does not have a "not a plant" class; arbitrary non-plant images produce low-confidence predictions among botanical classes.
10. **Darkness Vulnerability:**  
   Severe underexposure or darkness can trigger confident false-positive predictions.

<!-- BEGIN DATA LINEAGE -->
## Data Lineage and Evaluation Protocol

I document the full lineage of dataset snapshots, validation selections, and evaluation splits below to ensure complete transparency and reproducibility.

### Dataset Snapshot Lineage (Stages S1–S4)

| Stage | Description | Commit | Date (UTC) | Total Images | Train | Val | Test | Manifest SHA-256 |
|:---|:---|:---|:---|:---:|:---:|:---:|:---:|:---|
| **S1** | Training Snapshot (MLflow cb46c7f8) | `2108689` | 2026-11-06 | 92,165 | 73,356 | 9,349 | 9,460 | `5b5bc90a052d10a4...` |
| **S2** | Val Checkpoint & Calibration | `dbacd9c` | 2026-11-15 | 92,165 | 73,356 | 9,349 | 9,460 | `5b5bc90a052d10a4...` |
| **S3** | Clean Test Evaluation (Release Test Folder) | `3dcee03` | 2026-11-18 | 9,279 | — | — | 9,279 | `9822de8f77e4a587...` |
| **S4** | Curated Release Snapshot (P-007) | `781f8bd` | 2026-11-18 | 91,984 | 73,356 | 9,349 | 9,279 | `9822de8f77e4a587...` |

### Lineage Facts & Audit Findings

1. **Model Weights Training (S1):** Model weights (`3bb5785efa957a5fd4eb9d071fa92ff57adbef9788275a810e9cce99cf016dcb`) were trained on snapshot S1 containing 73,356 training images across 177 classes and 33 crops under MLflow run `cb46c7f8f10f45e59ad809720c7bccb6`.
2. **Checkpoint Selection on Validation Split (S2):** The best checkpoint was selected on the validation split at step 19 (epoch 20) with MLflow masked disease-head accuracy of 0.9600 (8,975 / 9,349 correct). Note: serving-score soft-gated accuracy on validation is a different metric yielding 8,974 / 9,349 correct.
3. **Temperature Scaling & Threshold Fitting on Validation Split (S2):** Platt scaling parameters ($T_{\text{crop}} = 0.5931$, $T_{\text{disease}} = 0.5013$) and operating decision threshold $\tau = 0.60$ were fitted on the 9,349 validation images.
4. **Headline Test Evaluation (S3):** All headline metrics in `reports/v1/results.json` were evaluated on the test folder of the curated release snapshot (9,279 test images post-P-007, manifest SHA-256 `9822de8f77e4a587...`). The earlier 8,911 figures (96.03%, evaluated on S1 minus the 181-image list before physical quarantine) are marked historical.
5. **CPU Determinism Disclosure:** Counts are reproduced on CPU, fp32, 1 thread; other hardware or thread counts can flip a near-tie image (about +-1 image, +-0.01 points). On pinned CPU execution (PyTorch 2.6.0+cu124, 1 thread, deterministic algorithms enabled), 8,910 of 9,279 test images are classified correctly (96.02%).
6. **Post-Training Dataset Removals:** Following training, exactly 181 test images were removed under Patch P-007 (`data/patches/P-007_test_leakage_quarantine_PLAN.csv`, logged in `reports/v1/removed_p007_images.csv`) because they were cross-split near-duplicates of training frames. Exactly 0 images were removed from train, and 0 from val.
7. **No Post-Removal Retraining:** Model weights were not retrained after Patch P-007 (`weights_trained_on_release_snapshot: false`).
8. **Run Environment & Seeding Status:** The training run was unseeded (deterministic seeding was integrated in later commit `16635f4`), and the working tree at the start of training had uncommitted changes (base commit `2108689`).
9. **Cross-Split Near-Duplicate Status:** On the curated release snapshot, test split cross-split leakage has been completely eliminated (0 pairs between test and train/val at Hamming distance $d \le 4$). However, the validation split may still contain near-duplicates of training frames: `reports/v1/twin_check.json` identifies 260 perceptual hash ($d \le 4$) twin pairs between train and val (145 exact 0-bit pairs, 115 near-duplicate pairs at $d \in [1, 4]$), spanning 162 unique validation images.

### Headline Metrics Breakdown (Held-Out Test Split, N=9,279)

- **Soft-Gated Disease Accuracy:** **96.02%** (8,910 / 9,279 correct; 95% Bootstrap CI: [95.62%, 96.45%])
- **Raw Disease Accuracy:** **95.83%** (95% Bootstrap CI: [95.42%, 96.25%])
- **Crop Identification Accuracy:** **99.28%** (95% Bootstrap CI: [99.11%, 99.44%])
- **Macro-F1 (All 177 Classes):** **93.86%** (95% Bootstrap CI: [91.84%, 94.42%])
- **Macro-F1 (Classes with $\ge 10$ test images, 147 Classes):** **96.54%** (95% Bootstrap CI: [95.96%, 97.00%])
- **Calibrated Expected Calibration Error (ECE, 15 bins):** **0.57%**

<!-- END DATA LINEAGE -->
