# Official Evaluation Report: Model v1.0 on Dataset v1.0

**Architecture:** ConvNeXt-Tiny DualHead (33 botanical crops, 177 foliar disease classes)  
**Single Source of Truth:** [`reports/v1/results.json`](results.json)  
**Weights Checkpoint:** `models/v1/model_dualhead_convnext_tiny.pth`  
**Dataset Manifest:** `reports/v1/dataset_v1.csv`  

---

> [!IMPORTANT]
> **Core Benchmark Disclaimer:**  
> All metrics are measured on the held-out test split of the curated dataset, which shares sources with the training data. No independent field evaluation has been done; real-world accuracy is unknown. Treat as an in-distribution research baseline.

---

## 1. Executive Summary & Evaluated Benchmarks

All headline metrics are computed on the leak-checked test split ($N=9,279$) strictly via `src.models.predict.predict_tensor` on CPU:

### Leak-Checked Test Split (N=9,279)
- **Host Crop Accuracy:** **99.28%** (95% Bootstrap CI: [99.11%, 99.44%])
- **Soft-Gated Disease Accuracy:** **96.03%** (95% Bootstrap CI: [95.62%, 96.45%])
- **Raw Disease Accuracy:** **95.84%** (95% Bootstrap CI: [95.43%, 96.26%])
- **Macro-F1 (All 177 Classes):** **93.87%** (95% Bootstrap CI: [91.85%, 94.43%])
- **Macro-F1 (classes with >=10 test images, 147 Classes):** **96.55%** (95% Bootstrap CI: [95.97%, 97.01%])
- **Calibrated Expected Calibration Error (ECE, 15 bins):** **0.58%**
- **Calibration Temperatures:** $T_{\text{crop}} = 0.5931$, $T_{\text{disease}} = 0.5013$

### Operating Threshold Performance ($\tau = 0.60$)
- **Covered Subset:** 8,999 / 9,279 images (96.98% coverage)
- **Covered Accuracy:** **97.52%** (8,776 / 8,999 correct)
- **Uncertain Subset:** 280 / 9,279 images (3.02% flagged)
- **Uncertain Accuracy:** 48.21% (135 / 280 correct)
- **Total Correct:** 8,911 / 9,279 (**96.03%**)

### Relative Comparison: Model v1 vs Prerelease Baseline
On identical, unchanged classes evaluated across the shared clean test samples, Model v1 achieves an improvement of **+0.56 pts** (95% CI: [+0.22, +0.90]) over the prerelease baseline.

---

## 2. Verified Limitations & Methodological Caveats

1. **Held-Out Test In-Distribution Scope:** All metrics reflect held-out test splits sharing laboratory/curated collection sources with the training split. No independent field evaluation has been conducted.
2. **Small Support Classes (30 Classes with < 10 Clean Test Images):** 30 classes have fewer than 10 test images.
3. **P-006 Relabeled Classes:** 9 classes modified under Patch P-006 have clean test support $N < 10$ and are not independently evaluated.
4. **Near-Duplicate Twins in Training Split:** 343 validation and test images have near-duplicate twin pairs ($d \le 4$) in the training split (`reports/v1/leaky_eval_images.csv`).
5. **Operating Threshold:** $\tau = 0.60$ was tuned strictly on the curated validation split.
6. **Calibration Mechanics:** Post-hoc scaling parameters ($T_{\text{crop}}=0.5931$, $T_{\text{disease}}=0.5013$) are below 1.0; label smoothing is only a hypothesis.
7. **Confidence Computation Discrepancy:** Auto mode uses a raw joint product $P(\text{crop}) \times P(\text{disease})$, while crop-constrained mode renormalizes probabilities.
8. **No Out-of-Distribution Detector:** Arbitrary non-plant images produce low-confidence predictions among botanical classes.
9. **Darkness Vulnerability:** Severe underexposure can produce confident false-positive predictions.
