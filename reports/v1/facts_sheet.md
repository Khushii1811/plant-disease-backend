# Project Facts Sheet & Verified Inventory (Release v1.0)

**Project:** Foliar Plant Leaf Disease Classification (`plant-disease-backend`)  
**Release Tag:** Model v1.0 trained on Dataset v1.0  
**Single Source of Truth:** `reports/v1/results.json`  

---

> [!IMPORTANT]
> **Core Benchmark Disclaimer:**  
> All metrics are measured on the held-out test split of the curated dataset, which shares sources with the training data. No independent field evaluation has been done; real-world accuracy is unknown. Treat as an in-distribution research baseline.

---

## 1. Verified Inventory & Reference Files

| File Path | Description | Verification Status |
|:---|:---|:---|
| `models/v1/model_dualhead_convnext_tiny.pth` | PyTorch Weights Checkpoint | Validated (177 disease heads, 33 crop heads) |
| `reports/v1/dataset_v1.csv` | Dataset Manifest | Active curated dataset (91,984 images post-P-007) |
| `reports/v1/results.json` | Evaluation Single Source of Truth | Recomputed on CPU via `src.models.predict.predict_tensor` |
| `reports/v1/counts_table.json` | Calibrated Coverage Sweep Table | Self-consistent with `results.json` |

---

## 2. Key Performance Metrics (Clean Test Split, N=9,279)

All figures verified directly from `reports/v1/results.json`:

- **Host Crop Accuracy:** **99.28%** (95% Bootstrap CI: [99.11%, 99.44%])
- **Soft-Gated Disease Accuracy:** **96.03%** (95% Bootstrap CI: [95.62%, 96.45%])
- **Raw Disease Accuracy:** **95.84%** (95% Bootstrap CI: [95.43%, 96.26%])
- **Macro-F1 (All 177 Classes):** **93.87%** (95% Bootstrap CI: [91.85%, 94.43%])
- **Macro-F1 (classes with >=10 test images, 147 Classes):** **96.55%** (95% Bootstrap CI: [95.97%, 97.01%])
- **Calibrated Expected Calibration Error (ECE, 15 bins):** **0.58%**
- **Calibration Temperatures:** $T_{\text{crop}} = 0.5931$, $T_{\text{disease}} = 0.5013$

### Operating Threshold Performance ($\tau = 0.60$)
- **Covered N:** 8,999 (96.98% coverage)
- **Covered Correct:** 8,776 (**97.52%** accuracy)
- **Uncertain N:** 280 (3.02% flagged)
- **Uncertain Correct:** 135 (48.21% accuracy)
- **Total Correct:** 8,911 (**96.03%** accuracy strictly matching model performance)

### Model v1 vs Prerelease Baseline Delta
- Delta on shared clean test samples across unchanged classes: **+0.56 pts** (95% CI: [+0.22, +0.90]).

---

## 3. Verified Operational Limitations

1. **In-Distribution Held-Out Split:** All metrics evaluate held-out splits of the curated dataset; no independent field evaluation has been conducted.
2. **Small Test Support:** 30 classes have fewer than 10 clean test images.
3. **P-006 Relabeled Classes:** 9 classes touched by Patch P-006 have clean test support $N < 10$ and are not independently evaluated.
4. **Near-Duplicate Twins:** 343 validation/test images have near-duplicate twins ($d \le 4$) in the training split (`reports/v1/leaky_eval_images.csv`).
5. **Operating Threshold:** $\tau = 0.60$ was tuned on the curated validation split.
6. **Calibration Mechanics:** Temperatures are below 1.0 ($T_{\text{crop}}=0.5931$, $T_{\text{disease}}=0.5013$); label smoothing is only a hypothesis.
7. **Confidence Definition:** Auto mode confidence is a raw joint product $P(\text{crop}) \times P(\text{disease})$, whereas crop-constrained mode renormalizes probabilities.
8. **Out-of-Distribution Behavior:** The model lacks a "not a plant" class; non-plant images receive low-confidence botanical predictions.
9. **Sensitivity to Darkness:** Severe underexposure can lead to confident false-positive predictions.
