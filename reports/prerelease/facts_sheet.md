# Project Facts Sheet & Verified Inventory (Release v1.0)

**Project:** Foliar Plant Leaf Disease Classification (`plant-disease-backend`)  
**Release Tag:** Model v1.0 trained on Dataset v1.0  
**Single Source of Truth:** `reports/v1/results.json`  

---

## 1. Verified Files & SHA-256 Checksums

| File Path | Description | Checksum / Status |
| :--- | :--- | :--- |
| `models/v1/model_dualhead_convnext_tiny.pth` | PyTorch Weights Checkpoint | `f28b568b89b089529f8318e2aecd71e6361271bd06c3461e188e6e64b2ea3d04` |
| `reports/v1/dataset_v1.csv` | Dataset Manifest | `7267ec4595eff802731eff86618dc79de33820752037ee5e92b88468cda89c30` |
| `reports/v1/results.json` | Evaluation Single Source of Truth | Validated self-consistent |

---

## 2. Key Performance Metrics

- **Purified Test Split (N=9,327):**
  - Crop-Gated Disease Accuracy: **95.27%** (95% CI: [94.83%, 95.70%])
  - Crop Accuracy: **99.16%** (95% CI: [98.98%, 99.36%])
  - Headline Macro-F1 (192 Classes): **93.45%** (95% CI: [91.23%, 93.93%])
  - Secondary Macro-F1 (195 Classes): **92.01%** (95% CI: [89.83%, 92.48%])
  - Robust Macro-F1 (N >= 20): **96.65%**
  - Calibrated ECE: **0.76%**
> *Note: Confidence intervals assume independent images.*

---

## 3. Physical Quarantine Inventory (`data/raw/quarantine_*`)

| Quarantine Folder | Image Count | Exclusion Reason |
| :--- | :--- | :--- |
| `quarantine_accidentally_cropped_images` | 265 | Physical quarantine for data quality, cross-split leakage, or non-foliar exclusion |
| `quarantine_banana_anthracnose_fruit` | 64 | Non-foliar fruit or blossom pathology |
| `quarantine_banana_bract_mosaic_fruit` | 399 | Non-foliar fruit or blossom pathology |
| `quarantine_basil_downy_mildew` | 62 | Physical quarantine for data quality, cross-split leakage, or non-foliar exclusion |
| `quarantine_bean_duplicates` | 8 | Physical quarantine for data quality, cross-split leakage, or non-foliar exclusion |
| `quarantine_bell_pepper_chilli_overlap` | 253 | Patch P-001: Duplicate impostors of Chilli classes |
| `quarantine_bell_pepper_duplicates` | 111 | Physical quarantine for data quality, cross-split leakage, or non-foliar exclusion |
| `quarantine_blueberry_anthracnose_fruit` | 33 | Non-foliar fruit or blossom pathology |
| `quarantine_blueberry_botrytis_blossom` | 51 | Physical quarantine for data quality, cross-split leakage, or non-foliar exclusion |
| `quarantine_brassica_duplicates` | 1,045 | Physical quarantine for data quality, cross-split leakage, or non-foliar exclusion |
| `quarantine_carrot_classes` | 87 | Physical quarantine for data quality, cross-split leakage, or non-foliar exclusion |
| `quarantine_cauliflower_soft_rot_curd` | 189 | Physical quarantine for data quality, cross-split leakage, or non-foliar exclusion |
| `quarantine_celery_classes` | 63 | Physical quarantine for data quality, cross-split leakage, or non-foliar exclusion |
| `quarantine_cherry_duplicates` | 1,188 | Physical quarantine for data quality, cross-split leakage, or non-foliar exclusion |
| `quarantine_chilli_anthracnose` | 188 | Physical quarantine for data quality, cross-split leakage, or non-foliar exclusion |
| `quarantine_chilli_bacterial_spot_duplicates` | 1,752 | Physical quarantine for data quality, cross-split leakage, or non-foliar exclusion |
| `quarantine_citrus_duplicates` | 1,096 | Physical quarantine for data quality, cross-split leakage, or non-foliar exclusion |
| `quarantine_citrus_melanose` | 13 | Physical quarantine for data quality, cross-split leakage, or non-foliar exclusion |
| `quarantine_cross_split_dups` | 304 | Patch P-004: Cross-split duplicate images (kept earliest split) |
| `quarantine_cucumber_anthracnose` | 153 | Physical quarantine for data quality, cross-split leakage, or non-foliar exclusion |
| `quarantine_cucumber_duplicates` | 36 | Physical quarantine for data quality, cross-split leakage, or non-foliar exclusion |
| `quarantine_cucumber_fruit_diseases` | 489 | Non-foliar fruit or blossom pathology |
| `quarantine_cucumber_sujay_mislabeled` | 307 | Physical quarantine for data quality, cross-split leakage, or non-foliar exclusion |
| `quarantine_data_quality` | 16,051 | Physical quarantine for data quality, cross-split leakage, or non-foliar exclusion |
| `quarantine_eggplant_fruit_blight` | 48 | Non-foliar fruit or blossom pathology |
| `quarantine_garlic_classes` | 599 | Physical quarantine for data quality, cross-split leakage, or non-foliar exclusion |
| `quarantine_garlic_shifted_duplicates` | 638 | Physical quarantine for data quality, cross-split leakage, or non-foliar exclusion |
| `quarantine_ginger_duplicates` | 5,368 | Physical quarantine for data quality, cross-split leakage, or non-foliar exclusion |
| `quarantine_grape_wrongly_ingested_classes` | 897 | Physical quarantine for data quality, cross-split leakage, or non-foliar exclusion |
| `quarantine_jamun_dry_leaf` | 400 | Physical quarantine for data quality, cross-split leakage, or non-foliar exclusion |
| `quarantine_jamun_dupes` | 128 | Physical quarantine for data quality, cross-split leakage, or non-foliar exclusion |
| `quarantine_label_conflict` | 941 | Patch P-004: Conflicting labels for identical perceptual hash pairs |
| `quarantine_lettuce_classes` | 1,094 | Physical quarantine for data quality, cross-split leakage, or non-foliar exclusion |
| `quarantine_lettuce_duplicates` | 268 | Physical quarantine for data quality, cross-split leakage, or non-foliar exclusion |
| `quarantine_mango_duplicates` | 21 | Physical quarantine for data quality, cross-split leakage, or non-foliar exclusion |
| `quarantine_mendeley_guava` | 183 | Physical quarantine for data quality, cross-split leakage, or non-foliar exclusion |
| `quarantine_non_bean_ginger_cropped_images` | 20 | Physical quarantine for data quality, cross-split leakage, or non-foliar exclusion |
| `quarantine_old_wild_paddy` | 10,436 | Physical quarantine for data quality, cross-split leakage, or non-foliar exclusion |
| `quarantine_peach_duplicates` | 1 | Physical quarantine for data quality, cross-split leakage, or non-foliar exclusion |
| `quarantine_peach_fruit_scab` | 61 | Non-foliar fruit or blossom pathology |
| `quarantine_pear_duplicates` | 0 | Physical quarantine for data quality, cross-split leakage, or non-foliar exclusion |
| `quarantine_plantcity_multi` | 906 | Physical quarantine for data quality, cross-split leakage, or non-foliar exclusion |
| `quarantine_plum_dead_leaf` | 516 | Physical quarantine for data quality, cross-split leakage, or non-foliar exclusion |
| `quarantine_plum_dry_leaf` | 800 | Physical quarantine for data quality, cross-split leakage, or non-foliar exclusion |
| `quarantine_plum_duplicates` | 51 | Physical quarantine for data quality, cross-split leakage, or non-foliar exclusion |
| `quarantine_plum_excess_legacy_healthy` | 927 | Physical quarantine for data quality, cross-split leakage, or non-foliar exclusion |
| `quarantine_plum_pox_virus` | 15 | Physical quarantine for data quality, cross-split leakage, or non-foliar exclusion |
| `quarantine_plum_rust` | 30 | Physical quarantine for data quality, cross-split leakage, or non-foliar exclusion |
| `quarantine_potato_duplicates` | 1,404 | Physical quarantine for data quality, cross-split leakage, or non-foliar exclusion |
| `quarantine_pruned_unviable_classes` | 76 | Physical quarantine for data quality, cross-split leakage, or non-foliar exclusion |
| `quarantine_raspberry_classes` | 461 | Physical quarantine for data quality, cross-split leakage, or non-foliar exclusion |
| `quarantine_raspberry_gray_mold` | 29 | Physical quarantine for data quality, cross-split leakage, or non-foliar exclusion |
| `quarantine_rice_lab_duplicates` | 252 | Physical quarantine for data quality, cross-split leakage, or non-foliar exclusion |
| `quarantine_soybean_brown_spot` | 41 | Physical quarantine for data quality, cross-split leakage, or non-foliar exclusion |
| `quarantine_soybean_mosaic` | 111 | Physical quarantine for data quality, cross-split leakage, or non-foliar exclusion |
| `quarantine_squash_powdery_mildew` | 529 | Physical quarantine for data quality, cross-split leakage, or non-foliar exclusion |
| `quarantine_strawberry_anthracnose` | 54 | Physical quarantine for data quality, cross-split leakage, or non-foliar exclusion |
| `quarantine_strawberry_duplicates` | 610 | Physical quarantine for data quality, cross-split leakage, or non-foliar exclusion |
| `quarantine_tobacco_classes` | 156 | Physical quarantine for data quality, cross-split leakage, or non-foliar exclusion |
| `quarantine_wheat_classes` | 1,319 | Physical quarantine for data quality, cross-split leakage, or non-foliar exclusion |
| `quarantine_wheat_head_diseases` | 441 | Physical quarantine for data quality, cross-split leakage, or non-foliar exclusion |
| `quarantine_wheat_healthy_duplicates` | 800 | Physical quarantine for data quality, cross-split leakage, or non-foliar exclusion |
| `quarantine_zero_bit_leakage` | 1,415 | Patch P-003: 0-bit cross-split twin frames |
| `quarantine_zucchini_bacterial_wilt` | 61 | Physical quarantine for data quality, cross-split leakage, or non-foliar exclusion |
| `quarantine_zucchini_duplicates` | 566 | Physical quarantine for data quality, cross-split leakage, or non-foliar exclusion |
| **Total Quarantined Images** | **56,880** | **All preserved on disk with CSV logs** |
