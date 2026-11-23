# Dataset Card: Multi-Crop Foliar Disease Benchmark

**Official Purified Benchmark: 9,279 leak-free test images (181 leaky frames quarantined under Patch P-007)**

> [!NOTE]
> **Release History & Nomenclature:**
> - **Pre-release Baseline (Dataset prerelease / Model prerelease):** 96,835 active images [historical (pre-P-005/P-006)] across 34 crops [historical (pre-P-005/P-006)] and 195 classes [historical (pre-P-005/P-006)] (archived in `models/prerelease/` and `reports/prerelease/`).
> - **Official Launch Release v1.0 (Curated Production Dataset):** Curated via Patches P-005/P-006/P-007 into 91,984 active foliar images across 33 crops and 177 verified classes (target: `models/v1/` and `reports/v1/`).

**Dataset Version:** Dataset v1.0 (Official Launch Release)  
**Total Active Images (Official Release v1.0):** 91,984 active images across 33 crops and 177 classes  
**Split Allocation:** Train: 73,356 (79.75%) | Val: 9,349 (10.16%) | Test: 9,279 (10.09%)  
**Manifest File:** [`reports/v1/dataset_v1.csv`](../reports/v1/dataset_v1.csv)  
**Licensing Notes:** [`docs/LICENSING_NOTES.md`](./LICENSING_NOTES.md) (CC BY-NC-SA 4.0 for annotations/manifests, MIT for code; raw images are not redistributed)  
**Patch History:** [`docs/PATCHES.md`](./PATCHES.md)  

---

> [!IMPORTANT]
> **Core Benchmark Disclaimer:**  
> All metrics are measured on the held-out test split of the curated dataset, which shares sources with the training data. No independent field evaluation has been done; real-world accuracy is unknown. Treat as an in-distribution research baseline.

---

## 1. Summary & Verified Evaluation Metrics (Clean Test Split, N=9,279)
Dataset v1.0 provides an auditable benchmark for foliar plant leaf disease classification. Images were harmonized across 41 source entries, with cross-split duplicate twins and label contradictions quarantined under Patches P-001, P-002, P-003, P-004, P-005, and P-007.

Images come from multiple upstream sources, which differ in capture conditions (for example plain or controlled backgrounds versus natural backgrounds). Per-source counts and licences are listed in docs/SOURCES.md.

All metrics are evaluated strictly on the leak-checked test split ($N=9,279$) from `reports/v1/results.json`:
- **Soft-Gated Disease Accuracy:** **96.02%** (about 96.0%; 95% Bootstrap CI: [95.62%, 96.45%])
- **Crop Identification Accuracy:** **99.28%** (95% Bootstrap CI: [99.11%, 99.44%])
- **Raw Disease Accuracy:** **95.83%** (95% Bootstrap CI: [95.42%, 96.25%])
- **Macro-F1 (All 177 Classes):** **93.86%** (95% Bootstrap CI: [91.84%, 94.42%])
- **Macro-F1 (classes with >=10 test images, 147 Classes):** **96.54%** (95% Bootstrap CI: [95.96%, 97.00%])
- **Expected Calibration Error (ECE, 15 bins):** **0.57%** ($T_{\text{crop}}=0.5931$, $T_{\text{disease}}=0.5013$)

---

## 2. Limitations & Operational Caveats

1. **Held-Out Test In-Distribution Scope:** All reported accuracy comes from the curated dataset's held-out test split. No independent field evaluation has been done; real-world accuracy is unknown.
2. **Small Test Support (30 Classes with < 10 Clean Test Images):** 30 classes have fewer than 10 test images.
3. **P-006 Relabeled Classes:** 9 classes touched by Patch P-006 have clean test support $N < 10$ and are not independently evaluated.
4. **Near-Duplicate Twins Within-Split & Validation Split Leakage:**  
   - **Within-Split Near-Duplicates (`reports/v1/twin_check.json`):** Perceptual hashing ($d \le 4$) identifies redundant within-split twin pairs: Train within-split contains 2,464 pairs (853 exact $d=0$, 1,611 near $d \in [1, 4]$); Val within-split contains 49 pairs (34 exact $d=0$, 15 near $d \in [1, 4]$); Test within-split contains 56 pairs (34 exact $d=0$, 22 near $d \in [1, 4]$).  
   - **Residual Validation Leakage:** 260 cross-split perceptual hash ($d \le 4$) twin pairs exist between train and val (145 exact 0-bit pairs, 115 near-duplicate pairs at $d \in [1, 4]$), spanning 162 unique validation images (`reports/v1/twin_check.json`, planned for removal in `reports/v1/p008_plan_DRYRUN.csv`). All 181 test split leakage twins are physically quarantined under Patch P-007 (`reports/v1/removed_p007_images.csv`), leaving 0 test-train and 0 test-val twin pairs ($N=9,279$).
5. **Validation Tuning:** Operating threshold $\tau = 0.60$ was tuned strictly on the curated validation split.
6. **Calibration Mechanics ($T < 1$):** Post-hoc scaling temperatures are below 1.0; label smoothing is strictly a hypothesis.
7. **Confidence Definition:** Auto mode confidence is a raw joint product $P(\text{crop}) \times P(\text{disease})$; crop-constrained mode renormalizes probabilities.
8. **No Non-Plant Class:** The model lacks an out-of-distribution anomaly detector; non-plant images receive low-confidence predictions among botanical classes.
9. **Darkness Vulnerability:** Severe underexposure can produce confident false-positive diagnoses.
10. **Model Improvement:** Model v1 achieves +0.56 pts (95% CI: [+0.22, +0.90]) over the prerelease baseline on unchanged classes.

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
