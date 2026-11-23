# Case Study: Investigating Cross-Dataset Image Overlap Between Bell Pepper and Chilli

**Author:** plant-disease-backend contributors  
**Project:** Foliar Plant Leaf Disease Classification  
**Document Status:** Working Draft for Technical Interviews & Architecture Portfolio  
**Date:** 25 October 2026

---

## 1. Executive Summary

During acceptance testing of my pre-release prototype model (v0.1 baseline, held-out exploratory test split), three Bell Pepper classes collapsed to exactly **0.00% F1-score**. In 100% of cases, the model predicted these images as their corresponding Chilli counterparts.

A visual review by the author identified small chilli fruits in the canopy. I subsequently built a reproducible hash-based audit tool (`scripts/data/curation/audit_bellpepper_chilli_copies.py`). The audit proved that **116 of 253 unique images** across the three Bell Pepper classes have perceptual duplicate twins (where at most 4 of 64 hash bits differ) in the Chilli classes, with 100% disease-class alignment forming 119 match pairs.

This case study documents:
1. How the anomaly was detected through hierarchical error analysis.
2. The visual inspection process.
3. The cryptographic (SHA-256) and perceptual (pHash) methodology.
4. Why the datasets show partial rather than 100% overlap, and the hypotheses formulated.
5. Ingestion pipeline limitations and the cross-crop deduplication rule established.
6. The data-centric engineering decisions taken for Dataset v1.0 and Model v1.0 release.

---

## 2. Detection: The Anomaly in the Confusion Matrix

The architecture employs a hierarchical Dual-Head design:
$$\text{Input Image} \longrightarrow \text{Backbone (ConvNeXt-Tiny)} \longrightarrow \begin{cases} \text{Crop Head} \to 34 \text{ crops [historical (pre-P-005/P-006)]} \\ \text{Disease Head} \to 195 \text{ classes [historical (pre-P-005/P-006)]} \end{cases}$$

During baseline v0.1 evaluation, global raw accuracy reached 92.26% and crop head accuracy reached 98.50%. However, per-class breakdown revealed an acute anomaly:

| Evaluated Class | Test Support | Precision | Recall | F1-Score | Model Prediction (100% of Samples) |
| :--- | :---: | :---: | :---: | :---: | :--- |
| `Bell Pepper - Leaf Curl Virus` | 14 | 0.000 | 0.000 | **0.000** | $\to$ `Chilli - Leaf Curl Virus` (14/14) |
| `Bell Pepper - Nutrition Deficiency` | 9 | 0.000 | 0.000 | **0.000** | $\to$ `Chilli - Nutrition Deficiency` (9/9) |
| `Bell Pepper - bell pepper powdery mildew` | 8 | 0.000 | 0.000 | **0.000** | $\to$ `Chilli - White Spot` (8/8) |

### Test Prediction Confidence Analysis
Analysis of the 31 test samples from `reports/v1/predictions/test_predictions.csv` and `reports/v1/predictions/probs.npy` revealed that the model was highly confident in its Chilli predictions:

| Suspect Class | Test Samples | Verified pHash Twins | Mean Crop Conf | Min Crop Conf | Mean Disease Conf | Min Disease Conf |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| `Bell Pepper - Leaf Curl Virus` | 14 | 6 / 14 | 0.8475 | 0.5387 | 0.9180 | 0.6177 |
| `Bell Pepper - Nutrition Deficiency` | 9 | 4 / 9 | 0.9416 | 0.7462 | 0.9775 | 0.8413 |
| `Bell Pepper - bell pepper powdery mildew` | 8 | 1 / 8 | 0.9704 | 0.9489 | 0.9932 | 0.9600 |
| **Combined Suspect Classes** | **31** | **11 / 31** | **0.9065** | **0.5387** | **0.9551** | **0.6177** |

Across all 31 samples, the crop head assigned an average confidence of 90.65% (minimum 53.87%) to `Chilli`, and the disease head assigned an average probability of 95.51% (minimum 61.77%) to the corresponding Chilli disease. In contrast, the probability assigned to the true Bell Pepper label averaged only 4.05% (minimum 0.00%).

### Diagnostic: Architecture Failure or Data Issue?
To determine whether the Dual-Head crop head was broadly incapable of separating Bell Pepper from Chilli, I evaluated the remaining Bell Pepper classes:
- `Bell Pepper - Healthy` (139 test images): **99.3% accuracy** (138/139 correct)
- `Bell Pepper - Bacterial Spot` (108 test images): **96.3% accuracy** (104/108 correct)
- `Bell Pepper - bell pepper frogeye leaf spot` (141 test images): **95.2% accuracy** (128/141 correct)

The model separated genuine Bell Pepper from Chilli with high precision ($\ge 95\%$). The collapse was strictly confined to those specific three classes.

---

## 3. Visual Review by Author

The author inspected the images in the three failing folders:
1. **Canopy Fruit Traces:** In several images across the folders, small, elongated chilli fruit pods were visible in the plant canopy.
2. **Author Exemplar Checklist:** TODO(author): list 6 to 10 specific filenames showing visible chilli fruits across the three classes.
3. **Caveat:** Visual inspection provided initial direction, but proving shared image origins required systematic perceptual hash matching against candidate Chilli datasets.

---

## 4. Empirical Proof: Hash-Based Audit

I implemented a dedicated audit script: `scripts/data/curation/audit_bellpepper_chilli_copies.py`.

### 4.1 Cryptographic Hash (SHA-256)
- **Result:** **0 exact SHA-256 matches** between processed Bell Pepper and Chilli files.
- **Technical Explanation:** Cryptographic hashes operate on exact byte streams. Applying JPEG recompression, format conversion, or resizing altered byte representations between datasets.

### 4.2 Perceptual Hash (pHash)
- **Methodology:** I utilized 64-bit DCT perceptual hashing (`imagehash.phash`), setting the matching threshold such that **at most 4 of 64 hash bits differ**.
- **Audit Findings:**
  - Total Bell Pepper images evaluated: **253** across `train`, `val`, and `test`.
  - Total Chilli images indexed: **1,268** across all 6 Chilli classes in `data/processed/`.
  - **Matched Images:** **116 of 253 unique images (45.8%)** matched a Chilli image, yielding **119 match pairs**.

#### Table 1: Class-Level Overlap & Disease Alignment
| Suspect Bell Pepper Class | Evaluated Images | Matched Unique Images | Match Pairs | Target Chilli Class | Counterpart Mapping Consistency |
| :--- | :---: | :---: | :---: | :--- | :---: |
| `Bell Pepper - Leaf Curl Virus` | 125 | 64 (51.2%) | 67 | `Chilli - Leaf Curl Virus` | 100% (67/67) |
| `Bell Pepper - Nutrition Deficiency` | 71 | 36 (50.7%) | 36 | `Chilli - Nutrition Deficiency` | 100% (36/36) |
| `Bell Pepper - bell pepper powdery mildew` | 57 | 16 (28.1%) | 16 | `Chilli - White Spot` | 100% (16/16) |
| **Total** | **253** | **116 (45.8%)** | **119** | | **100% (119/119)** |

In 100% of matched pairs, the Bell Pepper image mapped strictly to its corresponding disease in Chilli; zero pairs matched an unrelated Chilli class.

#### Table 2: Split Pair Distribution Matrix
| Split Combination (Bell $\times$ Chilli) | Pair Count | Type | Implication |
| :--- | :---: | :--- | :--- |
| `train` $\times$ `train` | 69 | Same-split redundancy | Duplicate image pairs within training |
| `train` $\times$ `val` | 13 | Cross-split leakage | Contaminates validation benchmark |
| `train` $\times$ `test` | 14 | Cross-split leakage | Contaminates test benchmark |
| `val` $\times$ `train` | 10 | Cross-split leakage | Contaminates validation benchmark |
| `val` $\times$ `test` | 1 | Cross-split leakage | Contaminates evaluation splits |
| `test` $\times$ `train` | 9 | Cross-split leakage | Test samples seen during training |
| `test` $\times$ `test` | 3 | Same-split redundancy | Duplicate evaluation samples |
| **Total Pairs** | **119** | **72 Same-split / 47 Cross-split** | **116 unique images involved** |

Among the 31 suspect test images, exactly 11 have a verified pHash twin in Chilli.

---

## 5. Investigating the Unmatched Images (137 of 253)

While 116 unique images had confirmed twins at distance $\le 4$, 137 images did not match any image in my active Chilli dataset within that threshold.

### Hypotheses Formulated:
1. **HYPOTHESIS 1 (Geometric Transformation):** Standard DCT pHash varies under dihedral transformations (horizontal/vertical flips, 90°/180°/270° rotations) and heavy cropping. If upstream sources applied synthetic augmentation prior to upload, matches would exceed the distance threshold.
2. **HYPOTHESIS 2 (Divergent Subsampling):** Upstream uploaders of the Mendeley Bell Pepper and Kaggle Chilli collections may have drawn non-identical subsets from an underlying primary camera collection.

---

## 6. Upstream Provenance Trail

I traced candidate upstream sources:
1. **Bell Pepper Upload:** Mendeley Data entry *"Pepper Bell Leaf Disease"* (doi: 10.17632/w9drvtxg9g.1, 23 May 2026, contributor Roughten Elvsava). Contains 9,283 images across 6 classes without farm or camera metadata.
2. **Earliest Known Primary Record:** Mendeley Data entry *"Chili Plant Leaf Disease and Growth Stage Dataset from Bangladesh"* (doi: 10.17632/w9mr3vf56s.1, 19 Feb 2025, Nirob et al., Daffodil International University). Collected in Charpolisha, Jamalpur, Bangladesh, containing 1,856 original and 12,000 augmented images across identical classes (`Bacterial Spot`, `Curl Virus`, `Cercospora Leaf Spot`, `Nutrition Deficiency`, `White Spot`, `Healthy`).
3. **Dual Record:** Mendeley Data entry *"Image Dataset on Chili Leaf Diseases in the Krishna River Basin of the Deccan Plateau, India"* (doi: 10.17632/ymt8k9bjkn, Malghan et al., Manipal Academy of Higher Education). Lists identical image counts and classes.
   - *HYPOTHESIS:* The relationship between these records remains to be verified via hash comparison (TODO(step-1d)).
4. **Kaggle Redistribution:** Kaggle dataset titled *"CHILLI"* (`suryiapooventhanr/chilli`). Contains 6 folders matching the taxonomy in Nirob et al.

---

## 7. Audit Limitations & Ingestion Lesson Learned

### Audit Limitations
1. Cryptographic hashes (SHA-256) could not detect overlap on processed files due to pipeline re-encoding and resizing.
2. In `scripts/data/curation/strict_bell_pepper_ingest.py`, exact cryptographic checks indexed all crops across `data/processed/`, but missed files with altered compression. Crucially, the perceptual deduplication step (`perceptual_dedup`) was executed strictly *intra-class* (within incoming Bell Pepper folders) and was never evaluated against other crops or existing classes.

### Lesson Learned: Cross-Crop Deduplication Rule
Ingestion scripts must never limit perceptual deduplication to intra-class checks. When ingesting new classes, pipelines must enforce a **cross-crop perceptual deduplication rule**: compute perceptual hashes against all existing classes in `data/processed/` (especially across botanically related species/genera) before admitting new data.

---

## 8. Data-Centric Remediation: Why Not Just Relabel?

When engineers discover misattributed classes, a common reflex is to simply relabel them into the target class. In this case, **direct relabeling was rejected**:
- My split-combination analysis demonstrated that 72 pairs exist in same-split combinations (69 in `train` $\times$ `train`) and 47 pairs exist across splits (including 14 Bell train images matching Chilli test images, and 9 Bell test images matching Chilli train images).
- Moving Bell Pepper images directly into Chilli without deduplication would inject 72 redundant duplicate pairs and 47 cross-split leakage pairs into Chilli classes.
- **Adopted Engineering Decision (Decision 59):** The three compromised classes are quarantined and de-listed from the active benchmark in Dataset v1.0 (reducing active classes from 198 [historical (pre-P-005/P-006)] to 195 [historical (pre-P-005/P-006)]). Model bundle v1.0 was retrained on this clean taxonomy.

---

## 9. TODO Checklist

- [ ] **TODO(step-1d):** Run control-group pHash audit on the other 3 Bell Pepper classes against Chilli to benchmark baseline false-positive collision rates.
- [ ] **TODO(step-1d):** Run 8-dihedral symmetry pHash (rotations + flips) on the 137 unmatched images against the Chilli dataset to test HYPOTHESIS 1.
- [ ] **TODO(step-1d):** Perform binary SHA-256 comparison directly on original unzipped source archives before pipeline resizing.
- [ ] **TODO(step-1d):** Programmatically compare raw image hashes between Nirob et al. (2025) and Malghan et al. to test HYPOTHESIS regarding shared corpus.
- [ ] **TODO(author):** Add verified list of 6 to 10 exemplar filenames showing visible chilli fruits in the canopy.
- [x] **Completed:** Retrain model bundle v1.0 on the sanitized 195-class taxonomy [historical (pre-P-005/P-006)] and publish verified benchmark metrics.
