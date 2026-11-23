# Official Evaluation Report: Model v1.0 on Dataset v1.0

**Architecture:** ConvNeXt-Tiny DualHead (34 botanical crops, 195 foliar disease classes)  
**Single Source of Truth:** [`reports/v1/results.json`](results.json)  
**Checkpoint SHA-256:** `f28b568b89b089529f8318e2aecd71e6361271bd06c3461e188e6e64b2ea3d04`  
**Dataset Manifest SHA-256:** `7267ec4595eff802731eff86618dc79de33820752037ee5e92b88468cda89c30`  

---

## 1. Executive Summary & Certified Benchmarks

### Certified Purified Test Split (N=9,327, Post Patch P-004)
Following Patch P-003 and P-004 deduplication, 0 exact duplicates and 0 pHash <= 4 cross-split pairs remain between train, val, and test partitions:

- **Crop-Gated Disease Accuracy:** **95.27%** (95% CI: [94.83%, 95.70%])
- **Raw Disease Accuracy:** **95.21%**
- **Crop Identification Accuracy:** **99.16%** (95% CI: [98.98%, 99.36%])
- **Headline Macro-F1 (192 Supported Classes):** **93.45%** (95% CI: [91.23%, 93.93%])
- **Secondary Macro-F1 (All 195 Classes, zero_division=0):** **92.01%** (95% CI: [89.83%, 92.48%])
- **Robust Macro-F1 (N >= 20, 116 Classes):** **96.65%**
- **Calibrated Expected Calibration Error:** **0.76%** ($T_c = 0.6356, T_d = 0.5327$)
> *Note: Confidence intervals assume independent images.*

### Secondary Reference: Historical Test Split (N=10,426)
- **Crop-Gated Disease Accuracy:** **95.66%**
- **Crop Identification Accuracy:** **99.23%**
- **Macro-F1:** **93.58%**
- *Provenance Note:* Contains 1,099 images subsequently quarantined by Patches P-003 and P-004.
