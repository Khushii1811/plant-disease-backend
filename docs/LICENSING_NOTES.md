# Dataset Licensing Notes and Provenance Categorization

**Associated Artifact:** Dataset v1.0 (`reports/v1/dataset_v1.csv`)  
**Associated Model:** Model v1.0 (`models/v1/model_dualhead_convnext_tiny.pth`)  
**Status:** RESOLVED — Raw images are not redistributed. Dataset annotations and manifests are released under CC BY-NC-SA 4.0 for non-commercial research use; source code is licensed under the MIT License; model weights are released for non-commercial academic evaluation only.

---

## 1. Distribution Scope & Image Redistribution Notice

**Crucial Policy:** This repository does **NOT** redistribute raw plant leaf images.

All source imagery remains the intellectual property of their original primary researchers, photographers, and institutional collectors. This repository distributes exclusively:
1. Manifests with relative filepaths and cryptographic SHA-256 hashes (`reports/v1/dataset_v1.csv`).
2. Per-split annotations, botanical crop mappings, and disease category definitions.
3. Automated curation, audit, and patch scripts to reconstruct splits from primary upstream archives.
4. Model weights, evaluation metrics, and inference service source code.

---

## 2. Upstream Source License Categorization

Based on the audit of all 41 upstream source entries cataloged in [`docs/SOURCES.md`](./SOURCES.md), upstream licenses are categorized into four distinct classes:

### Category A: Compatible / Permissive (Open, CC-BY, Public Domain)
These sources provide explicit rights for academic and derivative use with attribution:
- **CC-BY 4.0:**
  - Multi-Crop Disease Dataset (*Prem Kumar E., 2025*, Mendeley Data)
  - PlantSeg In-the-Wild (*Wei et al., 2024*, Zenodo)
  - Paddy Doctor Benchmark (*Arjunan et al., 2022*, IEEE DataPort)
  - Sugarcane Leaf Disease (*Daphal & Koli, 2022*, Mendeley Data)
  - Blackgram Plant Leaf Disease (*Talasila, 2022*, Mendeley Data)
  - Cauliflower Smart Agriculture (*Dumlao*, Mendeley Data)
  - Chilli Leaf Disease (*Nirob et al., 2025*, Kaggle mirror)
  - BrACoLD Coffee Dataset (*Esgario et al.*)
  - Peach Leaf Disease (*Farman et al.*)
  - Plum Leaf & Fruit (*Nayeem et al.*)
  - Vegetable Leaf Disease (*Ikteshad et al.*)
  - Cabbage Crop Diseases (*Ayawli et al.*)
  - Agri-Vision4 / Zucchini (*Billah et al.*)
  - Lemon Leaf Disease / LLD (*Al Amin*)
  - DiaMOS Plant Pear (*Fenu & Malloci*)
  - Niphad Grape Leaf (*Dharrao et al.*)
  - Jamun / Java Plum (*Bhowmik & Ahad*)
  - Pepper Bell Leaf (*Elvsava*)
  - Soybean Multi-Class (*Thorwat et al.*)
  - Guava Leaf Disease (*Hasan & Rahman*)
- **CC0 1.0 (Public Domain Dedication):**
  - Corn/Maize Leaf Disease (*Ghose*)
  - Grape Disease Original (*rm1000*)
  - Mango Leaf Disease (*Shah*)
- **MIT License:**
  - Ginger Leaf Dataset (*Wong*, TARUMT)
- **CDLA-Permissive-2.0:**
  - Guava Disease 4 Types (*Dalvi*)

### Category B: Conflicting Upstream Licenses (ShareAlike vs. Non-Commercial)
These sources impose structural viral or restriction clauses that cannot be legally co-mingled into a single unified outbound license:
- **PlantVillage Baseline (CC BY-SA 4.0):**
  - *Hughes & Salathé, 2015* (38 classes, 42,213 images).
  - Imposes **ShareAlike (SA)**: any downstream adaptation must be shared under the same CC BY-SA 4.0 license.
- **PlantCity Multi-Crop & Cherry (ODbL 1.0):**
  - *Muhammad Sheraz Khan et al., 2025* (Data in Brief).
  - Open Database License 1.0: requires derivative databases to be shared under ODbL 1.0.
- **Plum Leaf In-the-Wild (CC BY-NC-SA 4.0):**
  - *Khan F.*
  - Imposes **NonCommercial (NC)** in combination with ShareAlike (SA).
- **Core Legal Incompatibility:** CC BY-SA 4.0 forbids adding NonCommercial restrictions, whereas CC BY-NC-SA 4.0 explicitly forbids commercial use. An aggregation containing both cannot be redistributed as a single unified bundle under either license.

### Category C: Unspecified Licenses (Kaggle / GitHub Unlabeled Dumps)
Upstream repositories that did not specify a license file, terms of use, or SPDX identifier:
- PlantDoc component (*Singh et al., IIT Mandi*) — no explicit license file.
- Ginger Bacterial Wilt (*Yigezu et al.*) — unverified repository dump.
- Potato Leaf Disease (*Hossin*, Kaggle) — no SPDX license tag.
- Citrus Leaves (*Sourabh*, Kaggle) — no SPDX license tag.
- Cucumber Disease (*Kapadnis*, Kaggle) — no SPDX license tag.
- Bean Disease (*Makerere AI Lab*, Kaggle mirror) — unverified terms.
- Strawberry Disease (*Afzaal et al.*) — unverified terms.
- Rice Leafs Disease (*Saputra*, Kaggle) — no SPDX license tag.
- Plum Leafs Field (*Hasan*, Kaggle) — no SPDX license tag.
- Eggplant Disease (*Kapadnis*, Kaggle) — no SPDX license tag.
- Soybean Disease (*Bhujade*, Kaggle) — no SPDX license tag.
- Soybean Diseased Leaf (*sivm205*, Kaggle) — no SPDX license tag.

### Category D: Unknown / Untraced Image Sources
- Approximately 326 images (0.34% of Dataset v1.0) originating from historical aggregated scrapers whose original upload URL could not be resolved to a specific research institution or repository.

---

## 3. Legal Status & Resolution Recommendations

### Current Formal Status
**RESOLVED — Raw images are not redistributed. Dataset annotations and manifests are released under CC BY-NC-SA 4.0 for non-commercial research use; source code is licensed under the MIT License; model weights are released for non-commercial academic evaluation only.**

### Key Action Items for Project Owner:
1. **Maintain Image Distribution Embargo:**
   - Under no circumstances should the physical image files in `data/processed/` or `data/raw/` be zipped and redistributed publicly on Hugging Face, Zenodo, or Kaggle under a blanket license.
2. **Reconstruction-Only Distribution:**
   - Only distribute the CSV manifest (`reports/v1/dataset_v1.csv`), file hashes, class mapping files, and download reconstruction scripts. End-users assemble the dataset locally by downloading each primary archive directly from its author.
3. **Outbound Code vs. Model Licensing:**
   - Inference and evaluation code: Permissive MIT License.
   - Model weights checkpoint (`models/v1/model_dualhead_convnext_tiny.pth`): Research-only / Non-Commercial evaluation license (trained on a mixed corpus containing NC and SA data).
4. **Resolution of Unspecified Sources:**
   - For classes derived from Kaggle dumps with no license (e.g., Kapadnis, Sourabh), contact original authors or substitute with confirmed CC-BY primary datasets in future Dataset v1.1.
