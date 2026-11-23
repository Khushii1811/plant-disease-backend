# Patch History & Dataset Quarantine Log (`docs/PATCHES.md`)

> [!IMPORTANT]
> All metrics are measured on the held-out test split of the curated dataset, which shares sources with the training data. No independent field evaluation has been done; real-world accuracy is unknown. Treat as an in-distribution research baseline.

This log provides an auditable tracking record of all data curation and partitioning patches applied to `plant-disease-backend` (Dataset v1.0).

---

## Patch Inventory Summary

| Patch ID | Date | Git Commit / Ref | Images Moved | Target Quarantine Folder | Primary Reason | Verification Status |
|:---:|:---:|:---:|:---:|:---|:---|:---:|
| **P-001** | 2026-10-25 | `50399bd9` | 253 | `data/raw/quarantine_bell_pepper_chilli_duplicates/` | Duplicate Mendeley Bell Pepper images overlapping with Chilli | Verified (Quarantined) |
| **P-002** | 2026-10-25 | `50399bd9` | 0 | None (split rebalancing) | Stratified repartitioning for Citrus Greening & Soybean Healthy to 80/10/10 | Verified (Rebalanced) |
| **P-003** | 2026-10-30 | `32560655` | 1,415 | `data/raw/quarantine_zero_bit_leakage/` | 0-bit perceptual hash cross-split twin frames across train/val/test | Verified (0 twins remain) |
| **P-004** | 2026-10-31 | `bd973568` | 1,245 | `data/raw/quarantine_label_conflict/` (941)<br>`data/raw/quarantine_cross_split_dups/` (304) | Cross-split duplicates and contradictory labels for identical hashes | Verified (0 duplicates remain) |
| **P-005** | 2026-11-05 | Executed | 8,225 (4,665 quarantined, 3,062 relabeled, 498 merged) | `data/raw/quarantine_*/` | Comprehensive 34-crop visual audit: non-foliar, misidentifications, mergers. Transitions Pre-release Baseline [historical (pre-P-005/P-006)] (195 classes [historical (pre-P-005/P-006)]) to Official Launch Release v1.0 (177 classes) | Executed & Verified ([Dossier](PATCH_LINEAGE.md#3-patch-p-005-deep-botanical-curation-dossier-5-relabels-1-merge-17-quarantined-classes-3-outlier-images--195-to-177-classes)) |
| **P-006** | 2026-11-06 | Executed | 1,986 (repartitioned) | None (split rebalancing) | Stratified 80/10/10 split rebalancing across 21 imbalanced classes. Enforces zero empty splits and minimum >= 3 images in val/test across all 177 classes | Executed & Verified |
| **P-007** | 2026-11-18 | Executed | 181 (quarantined) | `data/raw/quarantine_test_leakage_twins/` | Quarantines all 181 near-duplicate test leakage frames. Physically locks test split to purified leak-free N=9,279 across 177 classes (total active: 91,984) | Executed & Verified |

---

## Detailed Patch Dossiers

### Patch P-001: Mendeley Bell Pepper / Chilli Duplication
- **Date:** October 25, 2026
- **Git Commit / Ref:** `50399bd928251edb3d41de0e41db7e13c0e62b5d`
- **Count of Images Moved:** 253 images
  - Train: 202
  - Val: 25
  - Test: 26
- **Target Folder:** `data/raw/quarantine_bell_pepper_chilli_duplicates/`
- **Reason:** Ingestion audit of Mendeley dataset `w9drvtxg9g.1` revealed identical photographic specimens ingested under both `Bell Pepper` and `Chilli` classes. The Bell Pepper duplicates were quarantined to prevent inter-crop label confusion.
- **Verification Status:** Verified. All 253 files logged in `quarantine_log.csv`. Zero duplicate hashes remain between Bell Pepper and Chilli from that source.

---

### Patch P-002: Stratified Split Rebalancing
- **Date:** October 25, 2026
- **Git Commit / Ref:** `50399bd928251edb3d41de0e41db7e13c0e62b5d`
- **Count of Images Moved:** 0 images (no images quarantined; partition re-allocation only)
- **Reason:** Historical splits for `Citrus - citrus greening disease` (Mendeley `3f83gxmv57.2`) and `Soybean - Healthy` (PlantVillage) had severe split imbalance (e.g. 98% test allocation or random fragmenting). Repartitioned using stratified group slicing to enforce exact 80/10/10 train/val/test allocation.
- **Verification Status:** Verified. Splits conform to 80/10/10 ratio; split disjointness verified by SHA-256 hash sets ($\text{Train} \cap \text{Val} \cap \text{Test} = \emptyset$).

---

### Patch P-003: Cross-Split 0-Bit Perceptual Hash Leakage
- **Date:** October 30, 2026
- **Git Commit / Ref:** `32560655f9d1b0a25a5ccb4219df2e99964d20c0`
- **Count of Images Moved:** 1,415 images
  - Train: 316
  - Val: 331
  - Test: 768
- **Target Folder:** `data/raw/quarantine_zero_bit_leakage/`
- **Reason:** Perceptual hash audit across train, val, and test splits identified 1,415 images sharing exact 0-bit pHash distance across partition boundaries (burst captures with camera jitter, slight recompressions, or unstratified multi-angle shots of identical leaves).
- **Verification Status:** Verified. Restored split independence. Evaluation on the resulting leak-checked baseline test split ($N=9,658$) yielded 95.36% crop-gated disease accuracy.

---

### Patch P-004: Deduplication & Label Contradiction Purification
- **Date:** October 31, 2026
- **Git Commit / Ref:** `bd973568ed80446f2b308099953eb568279271c5`
- **Count of Images Moved:** 1,245 images total:
  - **Label Conflicts:** 941 images moved to `data/raw/quarantine_label_conflict/`
    - Train: 418
    - Val: 259
    - Test: 264
    - *Reason:* Identical images (SHA-256 or pHash $\le 4$) assigned contradictory disease labels across classes (e.g., Guava Dot vs. Guava Rust; Ginger Bacterial Wilt vs. Paddy Narrow Brown Spot). Both contradictory copies were quarantined.
  - **Cross-Split Duplicates:** 304 images moved to `data/raw/quarantine_cross_split_dups/`
    - Train: 0 (preserved)
    - Val: 237
    - Test: 67
    - *Reason:* Same-class cross-split twin frames (pHash $\le 4$). Retained earliest partition (Train > Val > Test).
- **Detection Method Breakdown (P-004):**
  | Detection Method | Label Conflicts | Cross-Split Duplicates | Total Quarantined |
  |:---|:---:|:---:|:---:|
  | **Exact SHA-256 Match** | 2 | 0 | 2 |
  | **pHash $\le 4$ Only** | 939 | 304 | 1,243 |
  | **Total Quarantined** | **941** | **304** | **1,245** |
  > *Note: pHash-only removals include false positives (121 cross-crop pairs) to be reviewed in v1.1.*
- **Post-Patch Active Dataset Inventory [historical (pre-P-005/P-006)]:**
  - Active Images: 96,835 [historical (pre-P-005/P-006)]
  - Train: 78,187 (80.74%) [historical (pre-P-005/P-006)]
  - Val: 9,321 (9.63%) [historical (pre-P-005/P-006)]
  - Test: 9,327 (9.63%) [historical (pre-P-005/P-006)]
- **Verification Status & Clarifications:**
  - *Full Hash Scan:* Verified 0 exact SHA-256 duplicates across all classes and splits, and 0 cross-split pairs with pHash $\le 4$.
  - *pHash False Positives:* 121 pairs between different crops (e.g. Ginger vs. Paddy, Guava vs. Jamun) were captured by the pHash $\le 4$ threshold due to plain background cardboards and elongated leaf aspect ratios. These were retained in quarantine to maintain conservative separation, and are scheduled for case-by-case re-inspection in v1.1.
  - *Citrus Filename Collision Correction:* Prior claim that 3 Citrus Healthy / Citrus Canker example pairs were duplicates due to filename collision was corrected upon byte-for-byte verification. The files have distinct byte lengths and distinct SHA-256 hashes (`sourabh_15.pn.png`: 71,960 vs 73,102 bytes; `sourabh_3.png.png`: 60,312 vs 77,472 bytes; `sourabh_17.pn.png`: 83,484 vs 65,588 bytes). They were independent images that shared generic sequential filenames assigned upstream, not duplicate images.

---

### Patch P-005: Comprehensive Foliar Pathology Curation & Quarantine (Executed)
- **Status:** Executed & Verified ([Full Evidence Dossier](PATCH_LINEAGE.md#3-patch-p-005-deep-botanical-curation-dossier-5-relabels-1-merge-17-quarantined-classes-3-outlier-images--195-to-177-classes))
- **Execution Date:** November 5, 2026 via `scripts/data/apply_patch_p005.py --execute`
- **Audit Move Log:** `data/patches/P-005_move_log.csv` (8,225 moves)
- **Automated Reversible Rollback:** `data/patches/restore_P-005.py`
- **Scope & Transition:**
  - Transitions dataset from **Pre-release Baseline (195 classes [historical (pre-P-005/P-006)], 34 crops [historical (pre-P-005/P-006)], 96,835 images [historical (pre-P-005/P-006)])** to **Official Production Release v1.0 (177 classes, 33 crops, 92,165 images)**.
  - Quarantined: 4,665 images (17 entire non-foliar/severe mixed classes + Fig crop + 3 single leaf outliers) into `data/raw/quarantine_*/`.
  - Relabeled: 3,062 images across 5 classes (Citrus Alternaria, Hindu mite, Groundnut Tikka, Guava Insect Damage, Guava Algal leaf spot).
  - Merged: 498 images (`Mango - Powdery Mildew` into `Mango - Sooty Mould`).
- **Post-Patch Active Dataset Inventory (Official Release v1.0):**
  - Train: 177 classes, 73,356 images (79.59%)
  - Val: 177 classes, 9,349 images (10.14%)
  - Test: 177 classes, 9,460 images (10.26%)
  - Total Active Images: 92,165 across 177 classes and 33 crops.

---

### Patch P-006: Stratified 80/10/10 Split Rebalancing (Executed)
- **Status:** Executed & Verified
- **Execution Date:** November 6, 2026 via `scripts/data/apply_patch.py --plan-csv data/patches/P-006_split_rebalance_PLAN.csv --execute`
- **Plan File:** `data/patches/P-006_split_rebalance_PLAN.csv` (1,986 planned file moves)
- **What Was Done:**
  - Audit revealed 21 classes where images were severely hoarded in `train` (e.g. Jamun Brown Blight with 0 val / 0 test; Jamun Bacterial Spot with 0 test; Jamun Healthy with 0 test; Paddy Narrow Brown Spot with 1 test).
  - Repartitioned 1,986 images across 21 classes using deterministic seed 42 into 80% Train, 10% Val, 10% Test allocations with a hard lower bound to guarantee $\ge 3$ images per split ($\min(\text{Val}) \ge 3$, $\min(\text{Test}) \ge 3$, $\min(\text{Train}) \ge 9$).
- **Methodology Limitation:**
  - No twin clustering or near-duplicate grouping was performed during this repartitioning.
- **Consequence:**
  - Re-splitting without perceptual hash clustering introduced 312 exact cross-split twin pairs, resulting in 343 val/test images that have near-duplicate twins in the training set (162 in validation, 181 in test; historically cataloged at `data/patches/history/leaky_eval_images_historical_343.csv`).
  - The 181 quarantined test image paths are logged in `reports/v1/removed_p007_images.csv`.
- **Measured Performance Effect:**
  - The measured effect of filtering these leaky twin images from the test split is 0.08 percentage points (96.10% accuracy on unpurified test vs. 96.02% on clean test).
- **Remediation Plan:**
  - Patch P-007 physically quarantined all 181 near-duplicate test leakage twins into `data/raw/quarantine_test_leakage_twins/test/`, locking the test split to purified clean $N=9,279$.
- **Verification Outcomes:**
  - Classes with 0 images in Val: **0**
  - Classes with 0 images in Test: **0**
  - Minimum images in Val across all 177 classes: **3**
  - Minimum images in Test across all 177 classes: **3** (pre-P-007) / **1** (post-P-007, Jamun Bacterial Spot $N=1$)
  - Minimum images in Train across all 177 classes: **9**
  - All 177 classes active across all 3 splits (`train`: 177, `val`: 177, `test`: 177).

---

### Patch P-007: Test Split Leakage Quarantine (Executed)
- **Status:** Executed & Verified
- **Execution Date:** November 18, 2026 via `scripts/data/apply_patch.py --plan-csv data/patches/P-007_test_leakage_quarantine_PLAN.csv --execute`
- **Plan & Move Log File:** `data/patches/P-007_test_leakage_quarantine_PLAN.csv` (181 planned and executed file moves)
- **Restore Script:** `data/patches/restore_P-007.py`
- **What Was Done:**
  - Safely moved all 181 near-duplicate test leakage frames out of `data/processed/test/` into `data/raw/quarantine_test_leakage_twins/test/` (logged in `reports/v1/removed_p007_images.csv`).
  - Counts by split: Train: 0 moved, Val: 0 moved, Test: 181 moved. Total active: 91,984 (Train: 73,356, Val: 9,349, Test: 9,279).
  - Physically synchronized the filesystem with the official purified benchmark split ($N=9,279$).
- **Post-Patch Active Dataset Inventory:**
  - Active Images: 91,984 across 177 classes and 33 crops
  - Train: 73,356 (79.75%)
  - Val: 9,349 (10.16%)
  - Test: 9,279 (10.09%)
- **Verification Outcomes:**
  - All 181 files verified moved to quarantine; 0 files missing on disk.
  - Active test split verified physically at exactly $N = 9,279$ images, achieving 100% leak-free test partition.
  - Verified by `reports/v1/twin_check.json`: 0 perceptual hash cross-split twin pairs remain between test and train (`train_vs_test`: 0) and between test and val (`val_vs_test`: 0) at $d \le 4$.
  - Manifest `reports/v1/dataset_v1.csv` synchronized to 91,984 rows (SHA-256: `9822de8f77e4a587b8752772af85fbc8c0978e50354f108968d3065e736c50cd`).

---

## Evaluation Limitations & Known Residual Risks

1. **30 classes with < 10 clean test images**: While every class has at least 1 test image, 30 classes have fewer than 10 clean test images, limiting statistical power on rare classes.
2. **9 P-006 classes not independently evaluated**: Nine classes touched by P-006 have clean test $N < 10$ due to quarantine of near-duplicate frames with the training set.
3. **162 validation images with near-duplicate twins in train**: 260 cross-split perceptual hash ($d \le 4$) twin pairs exist between train and val affecting 162 unique validation images (`reports/v1/twin_check.json`, dry-run removal plan saved at `reports/v1/p008_plan_DRYRUN.csv`). Test split leakage is completely resolved via Patch P-007 (all 181 test twins physically quarantined, logged in `reports/v1/removed_p007_images.csv`; test split purified clean at $N=9,279$).
4. **Coverage threshold ($\tau=0.60$)**: Tuned on the curated validation split; natural-background behavior under non-standard illumination or unrepresented diseases may vary. No independent field evaluation has been conducted.
5. **Temperature parameters ($T < 1$)**: Post-hoc temperature calibration found $T_{\text{crop}}=0.5931$ and $T_{\text{disease}}=0.5013$. Label smoothing (0.05) is only a hypothesis for why logits are under-confident relative to accuracy.
6. **Confidence metric**: The serving confidence is a raw joint product $P(\text{crop}) \times P(\text{disease} \mid \text{crop})$.


