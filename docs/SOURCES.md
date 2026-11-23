# 🌾 Upstream Data Source Catalog & Provenance Dossier
**Version:** 1.0 &nbsp;|&nbsp; **Released:** October 2026 &nbsp;|&nbsp; **Curator:** plant-disease-backend contributors  
**Parent Benchmark:** [DATASET_CARD.md](./DATASET_CARD.md)

*Complete Per-Source Provenance, Upstream Licensing, Anti-Leakage Sanitization Interventions, and Clean BibTeX Citations for all 41 Source Datasets.*

---

## 📌 Executive Summary of Upstream Sources

To build a production-grade, leak-audited foliar disease benchmark of **99,775 images** across **200 classes** and **34 crop families**, I cataloged **41 upstream source entries** across Mendeley Data, Kaggle, GitHub, and academic publications:

* **Production-Active Source Entries:** 37 entries
* **Quarantined Suites (Excluded from Production Splits):** 4 entries
  * Source #8: Garlic Leaf (*Md. Fahimuzzman et al.* / *Farhad Reza et al.*) — archived to quarantine_garlic_classes/
  * Source #11: Lettuce Diseases (*Ashish Jha*) — archived to quarantine_lettuce_classes/
  * Source #16: Wheat Leaf High-Resolution (*Olyad Getch*) — archived to quarantine_wheat_classes/
  * Source #17: Wheat Leaf Disease (*Aamer Khan*) — archived to quarantine_wheat_classes/
* **Dataset Overlaps & Dual-Entries:**
  * Source #1 (*PlantVillage*) is already incorporated inside the foundational baseline of Source #2 (*Master Plant Disease Dataset*).
  * Sources #25 & #26 (*PlantCity Cherry* and *PlantCity Multi-Crop*) represent partitions from the same *PlantCity* project (*Muhammad Sheraz Khan et al.*, Data in Brief 2025).
* **Net Unique Active Primary Source Projects:** **35 unique independent research projects** in the active 200-class production benchmark.

---

### 🔄 Reconciliation: Literature Catalog (41 Entries) vs. Operational Manifest (36 Source Identifiers)

While this dossier catalogs **41 upstream literature/repository entries** describing the full historical research lineage of the data collection, the release snapshot dataset manifest (`reports/v1/dataset_v1.csv` and `reports/v1/sources_redistribution.csv`) tracks **36 active operational source identifiers** (totaling 91,984 active images).

The numerical delta between the 41 cataloged entries and the 36 operational source identifiers is reconciled as follows:

1. **Quarantined Suites Dropped from Release (3 entries):**
   - **Entry #8: Garlic Leaf** (*Reza et al.* / *Fahimuzzman*): Entire Garlic crop suite archived to `data/raw/quarantine_garlic_classes/` under Patch P-005. 0 active release images.
   - **Entry #16: Wheat Leaf High-Resolution** (*Getch*): Entire Wheat crop suite archived to `data/raw/quarantine_wheat_classes/` under Patch P-005. 0 active release images.
   - **Entry #17: Wheat Leaf Disease** (*Khan A.*): Entire Wheat crop suite archived to `data/raw/quarantine_wheat_classes/` under Patch P-005. 0 active release images.

2. **Consolidated / Grouped Multi-Dataset Identifiers:**
   - **Entries #1 & #2 (PlantVillage & Master Plant Disease)**: Mapped operationally as `plantvillage_legacy_baseline` (41,747 images) and `kaggle_pv2` (5,744 images). Sub-components of Master Plant Disease (e.g. #2c Paddy Doctor) appear under dedicated identifier `paddy_doctor_kaggle` (1,702 images).
   - **Entries #25 & #26 (PlantCity Cherry & Multi-Crop)**: Grouped under single operational project identifier `plantcity` (2,556 images).
   - **Entries #3 (Dumlao Cauliflower) & #20 (Ikteshad Vegetable)**: Consolidated under `mendeley` (566 images covering Broccoli, Cauliflower, Soybean) and `mendeley_cabbage` (102 images).
   - **Entries #9 & #10 (Ginger Leaf & Ethiopian Ginger)**: Consolidated under `ginger_research` (6,960 images).
   - **Entries #13 & #14 (Plum Leaf Mendeley & Khan F.)**: Grouped under `plum_lab_mendeley` (1,165 images) and `plum_ronokhasan` (197 images).
   - **Entries #36 & #38 (Thorwat Soybean & sivm205 Soybean)**: Grouped under `soybean_mendeley_kaggle` (304 images), with #37 Bhujade under `vaishali_soybean` (474 images).
   - **Entries #40 & #41 (Dalvi Guava & Hasan/Rahman Guava)**: Both consolidated under `mendeley_guava` (3,837 images).

3. **Operational Web & Auxiliary Pipelines (5 identifiers):**
   - `scraped` (36 images): Targeted web captures for small-class support across Cherry, Cabbage, Coffee, Radish.
   - `scraped_inaturalist` (27 images): In-situ captures for Blueberry.
   - `scraped_coffee` (278 images): Web-sourced Coffee foliar images.
   - `syedzainmir_pear` (1,717 images): Pear Kaggle mirror subset corresponding to DiaMOS/Pear community uploads.
   - `unknown` (326 images): Residual legacy images with unresolved specific source attribution across Guava and Plum.

Detailed per-entry mapping is available in [`reports/v1/sources_reconciliation.md`](../reports/v1/sources_reconciliation.md).

---


> **Important Note on Specimen Counts:** Specimen numbers cited throughout this dossier represent **Initial Ingested Raw Candidate Counts** as delivered by upstream repositories. As part of my Data-Centric AI pipeline, all raw candidates were subjected to EXIF transposition, watermark excision, 3-tier deduplication (MD5 + pHash + deep CNN embeddings), and cross-split leakage purging. Consequently, final counts in the production benchmark splits (documented in [DATASET_CARD.md](./DATASET_CARD.md)) are strictly lower than initial ingested counts (e.g., Cherry Shot Hole: 197 raw ingested specimens → 140 final benchmark specimens; Cherry Leaf Scorch: 626 raw ingested specimens → 447 final benchmark specimens).

## 📑 Master Per-Source License Provenance Table

> **Licensing Reminder (Two-Layer Model):**
> 1. **Curation Artifacts (Layer 1):** Splits, deduplication manifests, bounding boxes, taxonomy definitions, and curation scripts are released under **CC BY-NC-SA 4.0** (with repository code under MIT).
> 2. **Source Images (Layer 2):** Each image remains strictly governed by its original upstream license.
> 3. **Commercial Users:** Over 15 sources are marked **Unverified (assume non-commercial / research-only)** or carry confirmed **NC** restrictions. Do not deploy images commercially without independent legal verification.
> 4. **Share-Alike & Database Conflicts:** PlantVillage (#1, CC BY-SA 4.0) and PlantCity (#25, #26, ODbL 1.0) cannot be subordinated to an NC restriction and retain their respective SA/ODbL terms independently.

| # | Source Dataset / Publication | Stated License | Verification Status | NC? | SA? | Production Status / Scope |
|---|---|---|:---:|:---:|:---:|---|
| 1 | PlantVillage (Hughes & Salathé, 2015) | CC BY-SA 4.0 | ⚠️ Conflict | ❌ | ✔️ | Active; SA conflict with compilation NC; retain CC BY-SA 4.0 |
| 2 | Master Plant Disease Dataset (Tanniru, 2025) | Multi-License | Verified | ❌ | ❌ | Active aggregation; disaggregated into components 2a–2g below |
| ├─ 2a | Multi-Crop Disease Dataset (Prem Kumar E., 2025) | CC BY 4.0 | Verified | ❌ | ❌ | Active; Banana, Groundnut, Radish, Cauliflower, Chilli (Mendeley) |
| ├─ 2b | PlantSeg In-the-Wild Segmentation (Wei et al., 2024) | CC BY 4.0 | Verified | ❌ | ❌ | Active; 35 multi-crop wild foliar classes (Zenodo) |
| ├─ 2c | Paddy Doctor Benchmark (Arjunan et al., 2022) | CC BY 4.0 | Verified | ❌ | ❌ | Active; Paddy foliar disease classification (IEEE DataPort / Kaggle) |
| ├─ 2d | Sugarcane Leaf Disease (Daphal & Koli, 2022) | CC BY 4.0 | Verified | ❌ | ❌ | Active; Sugarcane foliar diseases (Mendeley) |
| ├─ 2e | Blackgram Plant Leaf Disease / BPLD (Talasila, 2022) | CC BY 4.0 | Verified | ❌ | ❌ | Active; Blackgram foliar diseases (Mendeley) |
| ├─ 2f | PlantVillage Component (Hughes & Salathé, 2015) | CC BY-SA 4.0 | ⚠️ Conflict | ❌ | ✔️ | Active; Potato, Tomato, Bell Pepper lab baseline |
| └─ 2g | PlantDoc Component (Singh et al., 2020) | Unspecified | ⚠️ Unverified | ❓ | ❓ | Active; multi-crop foliar component |
| 3 | Cauliflower Smart Agriculture (Dumlao) | CC BY 4.0 | Verified | ❌ | ❌ | Active; permissive |
| 4 | Chilli Leaf Disease (Nirob et al. / Kaggle mirror) | CC BY 4.0 | Verified | ❌ | ❌ | Active; primary CC BY 4.0 (Nirob et al., 2025) via Kaggle mirror |
| 5 | Corn/Maize Leaf Disease (Ghose) | CC0 1.0 | Unverified | ❌ | ❌ | Active; public domain |
| 6 | BrACoLD Coffee Dataset (Esgario et al.) | CC BY 4.0 | Verified | ❌ | ❌ | Active; permissive |
| 7 | PlantDoc (Singh et al., IIT Mandi) | Unspecified | ⚠️ Unverified | ❓ | ❓ | Active; no SPDX tag — **assume NC / research-only** |
| 8 | Garlic Leaf (Reza et al. / Fahimuzzman) | CC BY 4.0 | Verified | ❌ | ❌ | **Quarantined**; excluded from production split |
| 9 | Ginger Leaf Dataset (Wong, TARUMT) | MIT | Verified | ❌ | ❌ | Active; permissive |
| 10 | Ginger Bacterial Wilt (Yigezu et al.) | Unspecified | ⚠️ Unverified | ❓ | ❓ | Active; no license file — **assume NC / research-only** |
| 11 | Lettuce Diseases (Jha) | Unspecified | ⚠️ Unverified | ❓ | ❓ | **Quarantined**; excluded from production split |
| 12 | Peach Leaf Disease (Farman et al.) | CC BY 4.0 | Verified | ❌ | ❌ | Active; permissive |
| 13 | Plum Leaf & Fruit (Nayeem et al.) | CC BY 4.0 | Verified | ❌ | ❌ | Active; fruit images quarantined, leaves active |
| 14 | Plum Leaf In-the-Wild (Khan F.) | CC BY-NC-SA 4.0 | Unverified | ✔️ | ✔️ | Active; **reinforces NC-SA restriction** |
| 15 | Potato Leaf Disease (Hossin) | Unspecified | ⚠️ Unverified | ❓ | ❓ | Active; Kaggle no-tag — **assume NC / research-only** |
| 16 | Wheat Leaf Dataset (Getch) | Unspecified | ⚠️ Unverified | ❓ | ❓ | **Quarantined**; excluded from production split |
| 17 | Wheat Leaf Disease (Khan A.) | Unspecified | ⚠️ Unverified | ❓ | ❓ | **Quarantined**; excluded from production split |
| 18 | Citrus Leaves (Sourabh) | Unspecified | ⚠️ Unverified | ❓ | ❓ | Active; Kaggle no-tag — **assume NC / research-only** |
| 19 | Cucumber Disease (Kapadnis) | Unspecified | ⚠️ Unverified | ❓ | ❓ | Active; Kaggle no-tag — **assume NC / research-only** |
| 20 | Vegetable Leaf Disease (Ikteshad et al.) | CC BY 4.0 | Verified | ❌ | ❌ | Active; permissive |
| 21 | Cabbage Crop Diseases (Ayawli et al.) | CC BY 4.0 | Verified | ❌ | ❌ | Active; permissive |
| 22 | Bean Disease (Makerere AI Lab) | Unspecified | ⚠️ Unverified | ❓ | ❓ | Active; Kaggle no-tag — **assume NC / research-only** |
| 23 | Agri-Vision4 / Zucchini (Billah et al.) | CC BY 4.0 | Verified | ❌ | ❌ | Active; permissive |
| 24 | Strawberry Disease (Afzaal et al.) | Unspecified | ⚠️ Unverified | ❓ | ❓ | Active; no SPDX tag — **assume NC / research-only** |
| 25 | PlantCity Cherry (Khan et al.) | ODbL 1.0 | Verified | ❌ | ✔️ | Active; ⚠️ SA Conflict: ODbL requires derivative DBs under ODbL |
| 26 | PlantCity Multi-Crop (Khan et al.) | ODbL 1.0 | Verified | ❌ | ✔️ | Active; ⚠️ SA Conflict: ODbL requires derivative DBs under ODbL |
| 27 | Lemon Leaf Disease / LLD (Al Amin) | CC BY 4.0 | Verified | ❌ | ❌ | Active; permissive |
| 28 | DiaMOS Plant Pear (Fenu & Malloci) | CC BY 4.0 | Verified | ❌ | ❌ | Active; permissive |
| 29 | Rice Leafs Disease (Saputra) | Unspecified | ⚠️ Unverified | ❓ | ❓ | Active; Kaggle no-tag — **assume NC / research-only** |
| 30 | Niphad Grape Leaf (Dharrao et al.) | CC BY 4.0 | Verified | ❌ | ❌ | Active; permissive |
| 31 | Grape Disease Original (rm1000) | CC0 1.0 | Unverified | ❌ | ❌ | Active; public domain |
| 32 | Plum Leafs Field (Hasan) | Unspecified | ⚠️ Unverified | ❓ | ❓ | Active; Kaggle no-tag — **assume NC / research-only** |
| 33 | Jamun / Java Plum (Bhowmik & Ahad) | CC BY 4.0 | Verified | ❌ | ❌ | Active; permissive |
| 34 | Eggplant Disease (Kapadnis) | Unspecified | ⚠️ Unverified | ❓ | ❓ | Active; Kaggle no-tag — **assume NC / research-only** |
| 35 | Pepper Bell Leaf (Elvsava) | CC BY 4.0 | Verified | ❌ | ❌ | Active; permissive |
| 36 | Soybean Multi-Class (Thorwat et al.) | CC BY 4.0 | Verified | ❌ | ❌ | Active; permissive |
| 37 | Soybean Disease (Bhujade) | Unspecified | ⚠️ Unverified | ❓ | ❓ | Active; Kaggle no-tag — **assume NC / research-only** |
| 38 | Soybean Diseased Leaf (sivm205) | Unspecified | ⚠️ Unverified | ❓ | ❓ | Active; Kaggle no-tag — **assume NC / research-only** |
| 39 | Mango Leaf Disease (Shah) | CC0 1.0 | Verified | ❌ | ❌ | Active; public domain |
| 40 | Guava Disease 4 Types (Dalvi) | CDLA-Permissive-2.0 | Verified | ❌ | ❌ | Active; permissive |
| 41 | Guava Leaf Disease (Hasan & Rahman) | CC BY 4.0 | Verified | ❌ | ❌ | Active; permissive |

---

## 🔬 2. Primary Citations & Original Contributor Acknowledgements

I gratefully acknowledge and give full credit to the researchers, agronomists, and data contributors whose primary open datasets made this standardized benchmark possible:

### 1. PlantVillage Benchmark (Foundational Foliar Baseline)
* **Lead Researchers:** David P. Hughes & Marcel Salathé (Penn State University & EPFL)
* **Title:** *An open access repository of images on plant health to enable the development of mobile disease diagnostics*
* **Citation:** Hughes, D. P., & Salathé, M. (2015). *arXiv preprint arXiv:1511.08060*.
* **License:** Creative Commons Attribution-ShareAlike 4.0 (CC BY-SA 4.0)
* **Scope:** 38 foundational laboratory crop disease classes.

---

### 2. Master Plant Disease Dataset (Foundational Multi-Crop Baseline Aggregation)
* **Lead Aggregator / Contributor:** Hari Sri Shanmukha Sai Tanniru (`harisri2005`)
* **Dataset Title:** *Master Plant Disease Dataset (plant-disease-processed)*
* **Repository Link:** [kaggle.com/datasets/harisri2005/plant-disease-processed](https://www.kaggle.com/datasets/harisri2005/plant-disease-processed)
* **License:** Multi-License / Component-Inherited (see individual constituent source audits below)
* **Ingested Raw Scope:** 70,457 raw candidate specimens across 7 foundational sub-datasets.
* **Component Provenance Breakdown:**
  * **2a. Multi-Crop Disease Dataset (Prem Kumar E., VIT Chennai, 2025):** 21,874 raw candidate specimens across Banana, Groundnut, Radish, Cauliflower, and Chilli. Published on Mendeley Data (DOI: `10.17632/6243z8r6t6.1`) under **CC BY 4.0**.
  * **2b. PlantVillage Studio Baseline (Hughes & Salathé, 2015):** 20,638 raw candidate specimens covering Potato, Tomato, and Bell Pepper studio foliar pathology under **CC BY-SA 4.0**.
  * **2c. PlantSeg In-the-Wild Segmentation Dataset (Wei et al., 2024):** 11,458 raw candidate specimens covering 35 multi-crop wild foliar classes. Published on Zenodo (DOI: `10.5281/zenodo.13958858`) and arXiv (`arXiv:2409.04038`) under **CC BY 4.0**.
  * **2d. Paddy Doctor Benchmark (Arjunan et al., 2022):** 10,407 raw candidate specimens of paddy/rice foliar pathologies from IEEE DataPort / CVPR Workshops under **CC BY 4.0**.
  * **2e. Sugarcane Leaf Disease Dataset (Daphal & Koli, 2022):** 2,521 raw candidate specimens of sugarcane foliar diseases from Mendeley Data (DOI: `10.17632/9424skmnrk.1`) under **CC BY 4.0**.
  * **2f. Blackgram Plant Leaf Disease / BPLD (Talasila et al., 2022):** 1,007 raw candidate specimens of blackgram foliar diseases from Mendeley Data under **CC BY 4.0**.
  * **2g. PlantDoc Component (Singh et al., 2020):** 2,552 raw candidate specimens providing diverse foliar anchors for multiple crop families under Open Academic Access.
* **Sanitization Transformation:** All constituent subsets underwent my 3-tier deduplication, EXIF orientation correction, watermark removal, and contiguous group splitting to produce sanitized, leak-free benchmark partitions.

---

### 3. Mendeley Data / Kaggle: Cauliflower Smart Agriculture
* **Lead Researcher:** Jocelyn Dumlao & Contributors
* **Dataset Title:** *Cauliflower Leaf Diseases: A Computer Vision Dataset for Smart Agriculture*
* **Mendeley DOI:** [10.17632/x26px3xnmy.1](https://doi.org/10.17632/x26px3xnmy.1)
* **Kaggle Mirror:** [`jocelyndumlao/cauliflower-leaf-diseases-datase`](https://www.kaggle.com/datasets/jocelyndumlao/cauliflower-leaf-diseases-datase)
* **License:** Creative Commons Attribution 4.0 International (CC BY 4.0)
* **Contributed Scope:** High-resolution natural-background cauliflower healthy leaves, bacterial soft rot, black rot, downy mildew.

---

### 4. Mendeley Data / Kaggle: Chili Plant Leaf Disease Dataset
* **Primary Authors:** Md Asraful Sharker Nirob, A K M Fazlul Kobir Siam, Prayma Bishshash, & Md Assaduzzaman (Daffodil International University, Bangladesh)
* **Primary Dataset Title:** *Chili Plant Leaf Disease and Growth Stage Dataset from Bangladesh*
* **Mendeley DOI:** [10.17632/w9mr3vf56s.1](https://doi.org/10.17632/w9mr3vf56s.1)
* **License:** Creative Commons Attribution 4.0 International (CC BY 4.0)
* **Redistribution Mirror:** Kaggle: [`suryiapooventhanr/chilli`](https://www.kaggle.com/datasets/suryiapooventhanr/chilli) (contributed by Suryia Pooventhan R)
* **Contributed Scope:** In-situ collection in Jamalpur, Bangladesh, covering Chilli bacterial spot, cercospora leaf spot, leaf curl virus, nutrition deficiency, white spot, and healthy leaves (re-partitioned by unique physical leaf ID for zero cross-split leakage).

---

### 5. Kaggle: Corn / Maize Foliar Disease Dataset
* **Lead Contributor:** Smaranjit Ghose & Contributors
* **Dataset Title:** *Corn or Maize Leaf Disease Dataset*
* **Repository Link:** [kaggle.com/datasets/smaranjitghose/corn-or-maize-leaf-disease-dataset](https://www.kaggle.com/datasets/smaranjitghose/corn-or-maize-leaf-disease-dataset)
* **License:** CC0 1.0 (Public Domain, Unverified)
* **Contributed Scope:** Natural-background Healthy Corn leaves, Northern Leaf Blight, and Gray Leaf Spot.

---

### 6. BrACoLD: Brazilian Coffee Leaf Disease Benchmark
* **Lead Researchers:** Jose G. M. Esgario, Pedro H. S. Barbosa, & R. A. Krohling (Federal University of Espírito Santo, Brazil)
* **Paper Title:** *Deep learning for classification and severity estimation of coffee leaf biotic disorders*
* **Journal:** *Computers and Electronics in Agriculture*, Vol. 169, 105214 (2020).
* **DOI:** [10.1016/j.compag.2019.105214](https://doi.org/10.1016/j.compag.2019.105214)
* **Kaggle Host:** Mohammed Zwaughfa ([`mohammedzwaughfa/coffee-leaf-disease-dataset`](https://www.kaggle.com/datasets/mohammedzwaughfa/coffee-leaf-disease-dataset))
* **License:** Creative Commons Attribution 4.0 International (CC BY 4.0)
* **Contributed Scope:** Coffee Healthy leaves, Leaf Miner (*Leucoptera coffeella*), and Phoma Leaf Spot (*Phoma costaricensis*).

---

### 7. PlantDoc: In-the-Wild Visual Disease Detection
* **Lead Researchers:** Davinder Singh, Nitesh Jain, Pranjali Jain, Pratik Kayal, Sudhakar Kumawat, and Nipun Batra (IIT Mandi)
* **Paper Title:** *PlantDoc: A Dataset for Visual Plant Disease Detection in the Wild*
* **Conference:** *Proceedings of the 7th ACM IKDD CoDS and 25th COMAD (2020), pp. 249–253*.
* **ACM DOI:** [10.1145/3371158.3371196](https://doi.org/10.1145/3371158.3371196)
* **GitHub Repository:** [github.com/pratikkayal/PlantDoc-Dataset](https://github.com/pratikkayal/PlantDoc-Dataset)
* **Kaggle Mirror:** Abdul Hasibuddin ([`abdulhasibuddin/plant-doc-dataset`](https://www.kaggle.com/datasets/abdulhasibuddin/plant-doc-dataset))
* **License:** Unspecified (⚠️ Unverified, assume non-commercial / research-only)
* **Contributed Scope:** In-situ unconstrained natural-background captures across multiple crop families (Apple, Bell Pepper, Blueberry, Cherry, Grape, Peach, Raspberry, Soybean, Strawberry, Tomato).

---

### 8. Mendeley Data: A Comprehensive Dataset of Garlic Leaf Images [Archived to Quarantine]
* **Lead Researchers:** Farhad Reza, S.M. Asifur Rahman, Tarequl Islam, Md. Hasibur Rahman, Anika Amzad, Md. Wahidur Rahman
* **Dataset Title:** *A comprehensive dataset of garlic leaf images for disease classification*
* **Mendeley DOI:** [10.17632/ff78hgnbhn.1](https://doi.org/10.17632/ff78hgnbhn.1)
* **License:** Creative Commons Attribution 4.0 International (CC BY 4.0)
* **Contributed Scope:** High-resolution natural-background and laboratory garlic specimens (*Allium sativum*) covering Garlic Healthy Leaf and Garlic Tip Burn / Affected Leaf.
* **Sanitization Interventions:** Applied EXIF orientation transposition, 16% deterministic bottom watermark excision (`Galaxy A14 5G`), and a two-tier neural feature deduplication pipeline (pHash + deep CNN cosine similarity $\ge 0.95$) that purged 638 burst/shifted copies, preserving 422 strictly unique physical specimens. *(Entire Garlic crop suite archived to `data/raw/quarantine_garlic_classes/`)*.

---

### 9. GitHub / TARUMT: Ginger Leaf Disease In-Situ Dataset
* **Lead Researcher / Contributor:** Jay Wong (`wongjay1941`) & Collaborators (Tunku Abdul Rahman University of Management and Technology - TARUMT)
* **Dataset Title:** *Ginger-Leaf-Dataset: A Multi-Class High-Resolution Image Dataset for Precision Ginger Disease Diagnostics*
* **Repository:** [github.com/wongjay1941/Ginger-Leaf-Dataset](https://github.com/wongjay1941/Ginger-Leaf-Dataset)
* **License:** MIT (Verified)
* **Contributed Scope:** High-resolution in-situ natural-background captures across Healthy foliage, Leaf Blight (*Phyllosticta zingiberi*), Pest Damage (stem borer / foliar chewers), and Dehydrated leaves.
* **Sanitization Interventions:** Subjected to deep neural feature embedding scan (`MobileNetV3` cosine similarity $\ge 0.95$). Quarantined over 5,000 pre-augmented static rotations, flips, and burst captures into `data/raw/quarantine_ginger_duplicates/` to prevent cross-split data leakage, retaining 6,883 strictly unique physical specimens.

---

### 10. Research: Ethiopian Commercial Farm Ginger Bacterial Wilt Dataset
* **Lead Researchers:** Mesay Gemeda Yigezu, et al.
* **Study Title:** *Ginger Disease Detection and Classification Using Deep Learning and Pre-Trained Convolutional Neural Networks*
* **Repository:** [github.com/Mesay-Gemeda/Ginger-disease-detection-using-CNN-and-pertrained-model](https://github.com/Mesay-Gemeda/Ginger-disease-detection-using-CNN-and-pertrained-model)
* **License:** Unspecified (⚠️ Unverified, assume non-commercial / research-only)
* **Contributed Scope:** Real commercial farm in-situ captures from Ethiopian ginger cultivations collected with agricultural domain extension experts, focusing on Bacterial Wilt (*Ralstonia solanacearum*) and Healthy foliar foliage.
* **Sanitization Interventions:** Corrected EXIF orientation tags and ran deep CNN deduplication to extract 159 clean, distinct natural-background bacterial wilt specimens.

---

### 11. Kaggle: Lettuce Diseases Benchmark Dataset
* **Lead Contributor:** Ashish Jha (`ashishjstar`)
* **Dataset Title:** *Lettuce Diseases Dataset*
* **Kaggle Link:** [kaggle.com/datasets/ashishjstar/lettuce-diseases](https://www.kaggle.com/datasets/ashishjstar/lettuce-diseases)
* **License:** Community Data License Agreement / Open Research Access
* **Contributed Scope:** Natural-background and greenhouse foliar captures across Healthy lettuce (*Lactuca sativa*), Bacterial leaf spot (*Xanthomonas*), Downy Mildew (*Bremia lactucae*), Powdery Mildew (*Golovinomyces*), Septoria leaf blight (*Septoria lactucae*), and viral infections.
* **Sanitization Interventions:** Excised 1,106 non-crop weed crops (*Capsella bursa-pastoris*). Ran deep neural feature deduplication (`MobileNetV3` cosine similarity $\ge 0.95$), quarantining 268 burst duplicates. Detected and resolved cross-dataset duplicate overlap against existing training partitions before deterministic 80-10-10 splitting.

---

### 12. Mendeley Data: Robust Recognition of Peach Plant Diseases in Field Images
* **Lead Researchers:** Haleem Farman, Jamil Ahmad, Bilal Jan, Yasir Shahzad, Muhammad Abdullah, & Atta Ullah (Islamia College Peshawar)
* **Paper Title:** *Efficientnet-based robust recognition of peach plant diseases in field images*
* **Journal:** *Computers, Materials & Continua*, Vol. 71, No. 1 (2022), pp. 2073–2089.
* **Mendeley DOI:** [10.17632/3pmj85snvw.1](https://doi.org/10.17632/3pmj85snvw.1)
* **License:** Creative Commons Attribution 4.0 International (CC BY 4.0)
* **Contributed Scope:** Natural-background specimens of Peach (*Prunus persica*) foliage and fruit.
* **Sanitization & Domain Scope Interventions:**
  * Sourced genuine foliar leaf specimens for **`Peach - peach leaf shot hole`** (*Wilsonomyces carpophilus*).
  * Excluded and quarantined 540 non-foliar fruit images (`shot hole` fruit) to adhere to strict foliar canopy vision requirements for edge diagnostic systems.
  * Audited and purged 55 mislabeled nutrient deficiency copies from the original Mendeley `bacterial spot` archive.
  * Ingested pristine foliar **`Peach - peach bacterial spot`** (*Xanthomonas arboricola pv. pruni*) using 599 clean specimens with cryptographic hash verification to ensure zero cross-dataset duplicate overlap.

---

### 13. Mendeley Data: Plum Leaf and Fruit Pathology Dataset
* **Lead Researchers:** Rejowan Arifin Nayeem, S.M. Abdullah Al Muhib, Shahriar Marjan, Md Hasan Imam Bijoy, Md Assaduzzaman
* **Paper Title:** *Plum leaf and fruit dataset for deep learning-based disease classification*
* **Journal:** *Data in Brief* (2025).
* **Mendeley DOI:** [10.17632/w7sdx55m7z.1](https://doi.org/10.17632/w7sdx55m7z.1)
* **License:** Creative Commons Attribution 4.0 International (CC BY 4.0)
* **Contributed Scope:** Laboratory-captured specimens of Plum (*Prunus domestica*) foliage across Healthy Leaves, Insect Holes, Chlorotic Yellow Leaves, and Dead Leaves. Sourced strictly from the unaugmented `Original Dataset/` (purging 18,000 pre-baked synthetic augmented replicas). 1,036 non-foliar fruit images (`Healthy Fruit` and `Unhealthy Fruit`) were quarantined to maintain strict foliar diagnostic canopy scope.

---

### 14. Kaggle: In-the-Wild Plum Leaf Pathology Dataset
* **Lead Contributor:** Faisal Khan (`faisalkhanx`)
* **Dataset Title:** *plum_leaf: High-Resolution In-the-Wild Foliar Plum Pathology*
* **Kaggle Link:** [kaggle.com/datasets/faisalkhanx/plum-leaf](https://www.kaggle.com/datasets/faisalkhanx/plum-leaf)
* **License:** Creative Commons Attribution-NonCommercial-ShareAlike 4.0 (CC BY-NC-SA 4.0)
* **Contributed Scope:** High-resolution (4032×1845) in-situ and orchard canopy captures of Healthy plum foliage, Insect Hole damage, and Chlorosis. Combined with Mendeley lab images via domain-stratified 80-10-10 partitioning to eradicate class-to-domain background confounding.

---

### 15. Kaggle: Potato Leaf Disease Natural-Background Dataset
* **Lead Contributor:** Shahad Hossin (`shahadhossin567r7455`)
* **Dataset Title:** *Potato Leaf Disease Dataset: Multi-Class Foliar and Biotic Stress Diagnostics*
* **Kaggle Link:** [kaggle.com/datasets/shahadhossin567r7455/potato-leaf-disease-dataset](https://www.kaggle.com/datasets/shahadhossin567r7455/potato-leaf-disease-dataset)
* **License:** Open Access / Research Use
* **Contributed Scope:** High-resolution natural-background captures of Potato (*Solanum tuberosum*) across Healthy foliage, Early Blight, Late Blight, Potato Virus, Plant Pests, Fungal Diseases, and Potato Cyst Nematode.
* **Sanitization & Domain Scope Interventions:**
  * **Cross-Dataset Collision Audit:** Detected that **589 images** in the candidate archive were identical or near-duplicate copies ($\ge 0.95$ CNN cosine similarity) of my pre-existing processed dataset (144 in `healthy`, 250 in `early_blight`, and 195 in `late_blight`). All 589 overlapping images were quarantined to `data/raw/quarantine_potato_duplicates/overlap_with_existing/` to prevent duplicate re-ingestion and cross-split contamination.
  * **Neural Deduplication:** Quarantined an additional 815 internal burst duplicates across candidate subclasses using GPU MobileNetV3 feature clustering.
  * **Foliar Ingestion:** Added **+316 clean specimens** to `Potato - Healthy` (boosting negative control baseline from 152 to 468), supplemented `Early Blight` (+245) and `Late Blight` (+293), and introduced 4 new classes (`Potato - potato virus`, `Potato - pest damage`, `Potato - fungal diseases`, and `Potato - potato cyst nematode`).

---

### 16. Kaggle: Wheat Leaf High-Resolution Benchmark Dataset [Archived to Quarantine]
* **Lead Contributor:** Olyad Getch (`olyadgetch`)
* **Dataset Title:** *Wheat Leaf Dataset*
* **Kaggle Link:** [kaggle.com/datasets/olyadgetch/wheat-leaf-dataset](https://www.kaggle.com/datasets/olyadgetch/wheat-leaf-dataset)
* **License:** Open Access Research License
* **Contributed Scope:** Ultra-high-resolution ($6000 \times 4000$ px) DSLR natural-background captures of Wheat (*Triticum aestivum*) foliage across Healthy leaves, Septoria, and Stripe Rust.
* **Sanitization & Domain Scope Interventions:** Sourced **102 unaugmented DSLR specimens** for `Wheat - Healthy`, partitioned using domain stratification (82 Train, 10 Val, 10 Test). *(Entire Wheat crop suite archived to `data/raw/quarantine_wheat_classes/`)*.

---

### 17. Kaggle: Wheat Leaf Disease Multi-Class Dataset [Archived to Quarantine]
* **Lead Contributor:** Aamer Khan (`khanaamer`)
* **Dataset Title:** *Wheat Leaf Disease Dataset*
* **Kaggle Link:** [kaggle.com/datasets/khanaamer/wheat-leaf-disease-dataset](https://www.kaggle.com/datasets/khanaamer/wheat-leaf-disease-dataset)
* **License:** Open Access / Research Community
* **Contributed Scope:** Multi-class natural-background leaf captures across Healthy foliage, Leaf Blight, Wheat Blast, Black Point, and Fusarium Foot Rot.
* **Sanitization & Domain Scope Interventions:**
  * **Synthetic Leakage Eradication:** Forensic analysis revealed that the 934 candidate `HealthyLeaf` images were generated via pre-baked synthetic transformations (`center_crop`, `center_scaled`, `rotated`, `flipped`, `augmented_pil`) across only 134 unique physical leaves.
  * Extracted exactly **134 unique primary physical specimens** (1 per leaf ID cluster) and quarantined all **800 redundant augmented copies** into `data/raw/quarantine_wheat_healthy_duplicates/` with full JSON audit manifests.
  * Verified zero collision against existing processed Wheat disease classes, and partitioned via domain-stratified 80-10-10 splitting (108 Train, 13 Val, 13 Test). Combined with `olyadgetch` to produce **236 pristine specimens** of `Wheat - Healthy`. *(Entire Wheat crop suite archived to `data/raw/quarantine_wheat_classes/`)*.

---

### 18. Kaggle: Citrus Leaves Foliar Pathology Dataset
* **Lead Contributor:** Sourabh (`sourabh2001`)
* **Dataset Title:** *Citrus Leaves Dataset*
* **Kaggle Link:** [kaggle.com/datasets/sourabh2001/citrus-leaves-dataset](https://www.kaggle.com/datasets/sourabh2001/citrus-leaves-dataset)
* **License:** Open Access Research License
* **Contributed Scope:** High-resolution orchard foliar captures across Healthy leaves, Black Spot (*Phyllosticta citricarpa*), Citrus Canker (*Xanthomonas citri*), Citrus Greening (*Candidatus Liberibacter asiaticus*), and Melanose (*Diaporthe citri*).
* **Sanitization & Domain Scope Interventions:**
  * **Melanose Quarantine:** Safely quarantined 13 candidate images of Melanose to `data/raw/quarantine_citrus_melanose/` due to statistical under-representation for an 80-10-10 split.
  * **Neural Deduplication:** Audited candidate subclasses using GPU `MobileNetV3` feature embeddings at $\ge 0.95$ cosine similarity, quarantining 178 redundant burst copies into `data/raw/quarantine_citrus_duplicates/`.
  * **Foliar Multi-Class Ingestion:** Sourced **415 clean specimens** for `Citrus - Healthy` (establishing the negative control baseline), **127 specimens** for new pathology `Citrus - Black spot`, supplemented `Citrus - citrus canker` with **+160 specimens** (expanded to 545 images), and supplemented `Citrus - citrus greening disease` with **+143 specimens** (expanded to 766 images).

---

### 19. Kaggle: Cucumber Disease Recognition Benchmark Dataset
* **Lead Contributor:** Sujay Kapadnis (`sujaykapadnis`)
* **Dataset Title:** *Cucumber Disease Recognition Dataset*
* **Kaggle Link:** [kaggle.com/datasets/sujaykapadnis/cucumber-disease-recognition-dataset](https://www.kaggle.com/datasets/sujaykapadnis/cucumber-disease-recognition-dataset)
* **License:** Open Access Research License
* **Contributed Scope:** High-resolution ($2296 \times 1724$ px) natural-background captures across Cucumber (*Cucumis sativus*) foliage and fruit.
* **Sanitization & Domain Scope Interventions:**
  * **Fruit Disease Quarantine:** Quarantined 489 non-foliar fruit images (`Fresh Cucumber`, `Belly Rot` on fruit, and `Pythium Fruit Rot`) to `data/raw/quarantine_cucumber_fruit_diseases/` to maintain a strictly foliar (leaf-only) scope.
  * **Synthetic Augmentation Bypass:** Bypassed 6,400 pre-baked synthetic images and extracted strictly from the unaugmented `Original Image/` directories.
  * **Neural Deduplication & Collision Audit:** Audited candidate subclasses using GPU `MobileNetV3` feature embeddings at $\ge 0.95$ cosine similarity, quarantining 34 internal burst duplicates and 2 pre-existing collision copies into `data/raw/quarantine_cucumber_duplicates/`.
  * **Foliar Multi-Class Ingestion:** Sourced **154 clean specimens** for `Cucumber - Healthy` (establishing the negative control baseline), **154 specimens** for `Cucumber - Downy Mildew`, **153 specimens** for `Cucumber - Anthracnose`, **153 specimens** for `Cucumber - Gummy Stem Blight`, and supplemented `Cucumber - cucumber bacterial wilt` with **+150 specimens** (expanded to 255 images).

---

### 20. Mendeley Data: Comprehensive Vegetable Leaf Disease Image Collection
* **Lead Researchers:** Deeya Ikteshad, Md. Iftekhar Rahman Likhan, Ifran-Al Rafi, Md Nasrul Islan Khan, Md Asraful Sharker Nirob
* **Dataset Title:** *Comprehensive Vegetable Leaf Disease Image Collection*
* **Mendeley DOI:** [10.17632/rh8c5tgg5k.1](https://doi.org/10.17632/rh8c5tgg5k.1)
* **Publication Date:** December 4, 2025
* **License:** Creative Commons Attribution 4.0 International (CC BY 4.0)
* **Contributed Scope:** High-resolution ($800 \times 800$ px) DSLR captures across Cabbage and Broccoli healthy foliage and foliar pathologies.
* **Sanitization & Domain Scope Interventions:**
  * **Duplicate Trap Neutralization:** Forensic MD5 audit uncovered that raw candidate folders contained repeated identical copies (e.g., 12 unique files duplicated 11 times in Cabbage Healthy). Filtered all exact byte duplicates and clustered near-duplicate burst captures with GPU `MobileNetV3` at $\ge 0.95$ cosine similarity.
  * **Foliar Multi-Class Ingestion:** Ingested **18 clean specimens** for `Broccoli - Healthy` (negative control baseline), **11 specimens** for new pathology `Broccoli - broccoli black rot`, supplemented `Broccoli - broccoli alternaria leaf spot` with **+10 specimens**, ingested **6 specimens** for new pathology `Cabbage - Damaged Leaf (White Butterfly)`, **7 specimens** for new pathology `Cabbage - Grey Mould`, and **20 specimens** for physiological disorder `Cabbage - Tip Burn`.

---

### 21. Mendeley Data: Image Dataset of Cabbage Crop Diseases
* **Lead Researchers:** Ben Beklisi Kwame Ayawli, Gyimah Kopri, John Kwao Dawson, Bright Bediako-Kyeremeh, Solomon Antwi Buabeng, Desmond Deveh, Esinam Irene Beklisi Ayawli, Esther Badu, Dawda Lamusah
* **Dataset Title:** *Image dataset of Cabbage Crop diseases*
* **Mendeley DOI:** [10.17632/sjmgzhwrxv.1](https://doi.org/10.17632/sjmgzhwrxv.1)
* **Publication Date:** January 15, 2025
* **License:** Creative Commons Attribution 4.0 International (CC BY 4.0)
* **Contributed Scope:** Natural-background cabbage foliage across Alternaria leaf spot, black rot, downy mildew, and healthy negative controls.
* **Sanitization & Domain Scope Interventions:**
  * **Synthetic Augmentation Bypass:** Isolated and bypassed all pre-baked synthetic transformations (rotation, gaussian noise, artificial brightness, cropped image tiles) and extracted strictly from the unaugmented `ORIGINAL_ALL_COMBINE_CABBAGE_DISEASES.zip`.
  * **Neural Deduplication & Collision Audit:** Audited candidate subclasses using GPU `MobileNetV3` feature embeddings at $\ge 0.95$ cosine similarity, quarantining all burst copies into `data/raw/quarantine_brassica_duplicates/`.
  * **Foliar Multi-Class Ingestion:** Combined with Mendeley Collection 1 to yield **66 clean specimens** for `Cabbage - Healthy` (establishing the negative control baseline), supplemented `Cabbage - cabbage alternaria leaf spot` with **+82 specimens** (expanded to 132 images), supplemented `Cabbage - cabbage black rot` with **+26 specimens** (expanded to 144 images), and supplemented `Cabbage - cabbage downy mildew` with **+22 specimens** (expanded to 111 images).

---

### 22. Makerere University / Kaggle: Bean Disease In-Situ Dataset
* **Lead Researchers:** Makerere AI Research Lab (Uganda) & Oise
* **Dataset Title:** *Bean Disease Dataset*
* **Kaggle Link:** [kaggle.com/datasets/therealoise/bean-disease-dataset](https://www.kaggle.com/datasets/therealoise/bean-disease-dataset)
* **License:** Open Access Research License
* **Contributed Scope:** High-resolution natural-background captures of Common Bean (*Phaseolus vulgaris*) across healthy foliage, angular leaf spot (*Pseudocercospora griseola*), and bean rust (*Uromyces appendiculatus*).
* **Sanitization & Domain Scope Interventions:**
  * **Neural Deduplication & Collision Audit:** Audited all 990 candidate images with GPU `MobileNetV3` embeddings at $\ge 0.95$ cosine similarity. Quarantined 2 benchmark collisions and 6 internal burst duplicates to `data/raw/quarantine_bean_duplicates/`.
  * **Foliar Multi-Class Ingestion:** Sourced **324 clean specimens** for `Bean - Healthy` (calibrating the negative control baseline), **329 specimens** for new natural-background pathology `Bean - bean angular leaf spot`, and supplemented `Bean - bean rust` with **+329 specimens** (expanding it from 114 to 443 total images).

---

### 23. Mendeley Data: Agri-Vision4 (Zucchini Foliar Pathology & Healthy Baseline)
* **Lead Researchers:** Md. Moniruzzaman, et al.
* **Dataset Title:** *Agri-Vision4: A benchmark dataset for plant disease detection*
* **Mendeley DOI:** [10.17632/8t6k37ztxc/1](https://doi.org/10.17632/8t6k37ztxc/1)
* **Publication Date:** 2025
* **License:** Creative Commons Attribution 4.0 International (CC BY 4.0)
* **Contributed Scope:** High-resolution ($1253 \times 939$ px) Sony Alpha 7 II captures across Zucchini (*Cucurbita pepo*) healthy foliage and 8 biotic/abiotic stress conditions.
* **Sanitization & Domain Scope Interventions:**
  * **Selective Streaming & Augmentation Bypass:** Bypassed non-target crops and all synthetic augmentation folders via HTTP Range stream extraction, pulling strictly original Zucchini foliar specimens.
  * **Alpha Channel Normalization:** Normalized transparent RGBA cutouts onto clean white backgrounds in standard 3-channel RGB (`.jpg`).
  * **Neural Deduplication & Collision Audit:** Audited all 988 candidates using GPU `MobileNetV3` embeddings at $\ge 0.95$ cosine similarity. Quarantined 133 exact MD5 duplicates, 369 benchmark collisions, and 64 burst near-duplicates to `data/raw/quarantine_zucchini_duplicates/`.
  * **Foliar Multi-Class Ingestion:** Sourced **58 clean specimens** for `Zucchini - Healthy` (establishing the missing healthy negative control baseline), **77 specimens** for `Zucchini - zucchini angular leaf spot`, **45 specimens** for `Zucchini - zucchini anthracnose`, **21 specimens** for `Zucchini - zucchini bacterial leaf spot`, **6 specimens** for `Zucchini - zucchini insect damage`, **1 specimen** for `Zucchini - zucchini iron chlorosis`, **3 specimens** for `Zucchini - zucchini dry leaf`, supplemented `Zucchini - zucchini downy mildew` with **+75 specimens** (expanded to 116 images), and supplemented `Zucchini - zucchini yellow mosaic virus` with **+136 specimens** (expanded to 235 images).

---

### 24. DatasetNinja / Afzaal et al. (Sensors 2021): Strawberry Foliar Disease Benchmark
* **Lead Researchers:** Usman Afzaal, Bipul Bhattarai, Young-Roc Pandeya, & Joonwhoan Lee (Chonbuk National University)
* **Paper Title:** *An In-Field Deep Learning Based Strawberry Plant Disease Detection Framework Using Fine-Tuning and Attention Module*
* **Journal:** *Sensors*, Vol. 21, No. 24 (2021), 8345.
* **DOI:** [10.3390/s21248345](https://doi.org/10.3390/s21248345)
* **DatasetNinja Hub:** [datasetninja.com/strawberry-disease-detection](https://datasetninja.com/strawberry-disease-detection)
* **License:** Open Access Research License
* **Contributed Scope:** High-resolution natural-background and greenhouse captures of Strawberry (*Fragaria $\times$ ananassa*) foliar canopy diseases compiled from Bugwood.org, Cal Poly Strawberry Center, UC ANR, NC State University, and Cornell CALS.
* **Sanitization & Domain Scope Interventions:**
  * **Organ-Level Foliar Scope Filtering:** Parsed fine-grained annotation metadata (`.jpg.json`) to exclude 3,417 non-foliar fruit and blossom images (Anthracnose fruit rot, Gray mold / Botrytis fruit rot, Blossom blight, Fruit powdery mildew) and 9 mixed-organ anomalies to uphold strict foliar leaf canopy domain consistency.
  * **Cryptographic & Deep Neural Deduplication:** Audited 1,574 candidate foliar images with GPU `MobileNetV3` feature embeddings at $\ge 0.95$ cosine similarity. Quarantined 37 exact MD5 byte duplicates and 573 near-duplicate burst captures into `data/raw/quarantine_strawberry_duplicates/`.
  * **Foliar Multi-Class Ingestion:** Sourced **254 clean specimens** for `Strawberry - strawberry angular leaf spot` (*Xanthomonas fragariae*), **204 specimens** for `Strawberry - strawberry leaf spot` (*Mycosphaerella fragariae*), and **506 specimens** for `Strawberry - strawberry powdery mildew` (*Podosphaera aphanis*), establishing a complete 5-class foliar diagnostic suite (1,964 clean foliar images) with zero cross-split data leakage ($\text{Train} \cap \text{Val} \cap \text{Test} = \emptyset$).

---

### 25. Kaggle / Khan et al. (Data in Brief 2025): PlantCity Cherry Foliar Benchmark
* **Lead Researchers:** Muhammad Sheraz Khan, Kainat Nisa, Irshad Ahmad, et al.
* **Paper Title:** *PlantCity: A Comprehensive Image Based on Multi Crop Leaves in Pakistan*
* **Journal:** *Data in Brief*, Vol. 60 (2025), 112130.
* **DOI:** [10.1016/j.dib.2025.112130](https://doi.org/10.1016/j.dib.2025.112130)
* **Kaggle Link:** [kaggle.com/datasets/codewithsk/cherry-leaf-disease-on-plantcity-2025](https://www.kaggle.com/datasets/codewithsk/cherry-leaf-disease-on-plantcity-2025)
* **License:** Open Database License (ODbL 1.0) / Open Research Access
* **Contributed Scope:** High-resolution in-situ captures of Sweet/Sour Cherry (*Prunus avium* / *Prunus cerasus*) foliage collected in commercial high-altitude orchards across Pakistan (Chitral and Charsadda districts) under natural ambient lighting.
* **Sanitization & Domain Scope Interventions:**
  * **Synthetic Redundancy & Burst Eradication:** Audited all 4,995 candidate images using exact MD5 hashing and deep neural feature embeddings (`MobileNetV3` at $\ge 0.95$ cosine similarity). Quarantined 30 exact MD5 duplicates and 2,765 pre-baked rotations/flips/burst shots into `data/raw/quarantine_cherry_duplicates/` with full JSON audit manifests.
  * **Foliar Multi-Class Ingestion:** Retained **2,200 unique physical specimens** to establish 4 new foliar pathologies: **`Cherry - cherry shot hole`** (197 specimens; *Wilsonomyces carpophilus*), **`Cherry - cherry leaf scorch`** (626 specimens; marginal necrosis), **`Cherry - cherry brown spot`** (568 specimens; *Alternaria* / *Stemphylium*), **`Cherry - cherry purple leaf spot`** (568 specimens; *Mycosphaerella cerasella*), and supplemented **`Cherry - Healthy`** (+241 specimens; expanded to 791 images) with verified zero cross-split data leakage.

---

### 26. Kaggle / Khan et al. (Data in Brief 2025): PlantCity Multi-Crop Foliar Benchmark
* **Lead Researchers:** Muhammad Sheraz Khan, Kainat Nisa, Irshad Ahmad, Muhammad Zubair, & Kholood Alshammari
* **Paper Title:** *PlantCity: A Comprehensive Image Based on Multi Crop Leaves in Pakistan*
* **Journal:** *Data in Brief*, Vol. 60 (2025), 112130.
* **DOI:** [10.1016/j.dib.2025.112130](https://doi.org/10.1016/j.dib.2025.112130)
* **Kaggle Link:** [kaggle.com/datasets/abdulmannann/plantcity](https://www.kaggle.com/datasets/abdulmannann/plantcity)
* **License:** Open Database License (ODbL 1.0) / Open Research Access / Apache 2.0
* **Contributed Scope:** High-resolution natural-background captures across Apple, Bean, Corn, Grape, Pear, and Fig foliage collected under real agricultural environments in Pakistan (high-heat Charsadda plains and cool Chitral mountain valleys).
* **Sanitization & Domain Scope Interventions:**
  * **Synthetic Redundancy & Burst Eradication:** Audited 9,024 candidate images using exact MD5 hashing and deep neural feature embeddings (`MobileNetV3` at $\ge 0.95$ cosine similarity). Quarantined 5,493 pre-baked rotations/flips/burst copies into `data/raw/quarantine_plantcity_multi/` with full JSON audit manifests.
  * **Foliar Multi-Class Ingestion:** Retained **3,531 unique physical specimens** to establish 11 new foliar classes:
    * 🌽 **Corn**: `Corn - corn holcus leaf spot` (148 specimens; *Pseudomonas syringae pv. lapsa*)
    * 🍏 **Apple**: `Apple - apple alternaria leaf spot` (620 specimens; *Alternaria mali*)
    * 🍇 **Grape**: `Grape - grape anthracnose` (537 specimens; *Elsinoë ampelina*)
    * 🫘 **Bean**: `Bean - bean leaf shot hole` (210 specimens; *Stemphylium* / *Cercospora*)
    * 🍐 **Pear (*Pyrus*) Suite**: `Pear - Healthy` (374 specimens), `Pear - pear black spot` (431 specimens), `Pear - pear fire blight` (193 specimens)
    * 🍈 **Fig (*Ficus carica*) Suite**: `Fig - Healthy` (221 specimens), `Fig - fig leaf blight` (389 specimens), `Fig - fig brown spot` (194 specimens), `Fig - fig rust` (214 specimens)
  * Mathematically verified zero cross-split data leakage ($\text{Train} \cap \text{Val} \cap \text{Test} = \emptyset$).

---

### 27. Mendeley Data / Al Amin (2023): Lemon Leaf Disease Foliar Benchmark
* **Lead Researcher:** Md Al Amin (Daffodil International University, Bangladesh)
* **Dataset Title:** *LLD: Lemon Leaf Disease Image Dataset for AI-Based Plant Health Detection*
* **Mendeley DOI:** [10.17632/9ywvpv3xtg.1](https://doi.org/10.17632/9ywvpv3xtg.1)
* **Publication Date:** 2023 / 2025
* **License:** Creative Commons Attribution 4.0 International (CC BY 4.0)
* **Contributed Scope:** High-resolution in-situ captures ($1440 \times 1080$ px) of Lemon (*Citrus limon*) foliar diseases collected in commercial orchards in Kushtia, Khulna, Bangladesh under natural ambient lighting conditions.
* **Sanitization & Domain Scope Interventions:**
  * **Botanical Genus Harmonization:** Integrated lemon foliar diseases into the unified *Citrus* genus benchmark (`Citrus - [disease]`), preserving diagnostic coherence for citrus orchard canopy management.
  * **Neural Feature Deduplication & Burst Pruning:** Audited 1,208 raw candidate images across targeted diseases using exact MD5 hashing and GPU-accelerated deep neural feature embeddings (`MobileNetV3` at $\ge 0.95$ cosine similarity). Quarantined 918 redundant burst shots and near-duplicates to `data/raw/quarantine_citrus_duplicates/` with full JSON audit manifests.
  * **Foliar Multi-Class Ingestion:** Sourced **223 clean specimens** for `Citrus - citrus algal leaf spot` (*Cephaleuros virescens*) and **67 clean specimens** for `Citrus - citrus scab` (*Elsinoë fawcettii* / *Sphaceloma fawcettii*), expanding the Citrus diagnostic suite to 6 comprehensive classes (2,143 clean foliar images) with verified zero cross-split data leakage ($\text{Train} \cap \text{Val} \cap \text{Test} = \emptyset$).

---

### 28. Kaggle / Fenu & Malloci (Agronomy 2021): DiaMOS Plant Pear Foliar Benchmark
* **Lead Researchers:** Gianni Fenu & Francesca Maridina Malloci (University of Cagliari, Italy)
* **Paper Title:** *DiaMOS Plant: A Dataset for Diagnosis and Monitoring Plant Disease*
* **Journal:** *Agronomy*, Vol. 11, No. 11 (2021), 2107.
* **DOI:** [10.3390/agronomy11112107](https://doi.org/10.3390/agronomy11112107)
* **Kaggle Source:** [kaggle.com/datasets/syedzainmir/pear-leaf-disease](https://www.kaggle.com/datasets/syedzainmir/pear-leaf-disease)
* **License:** Creative Commons Attribution 4.0 International (CC BY 4.0)
* **Contributed Scope:** High-resolution in-situ photography (12–18 megapixel captures up to $5184 \times 3456$ px) of Pear (*Pyrus*) tree foliar pathologies and healthy controls collected in commercial European pear orchards throughout the growing season under natural sunlight and ambient conditions.
* **Sanitization & Domain Scope Interventions:**
  * **Pathology Alignment & Diagnostic Disambiguation:** Mapped sawfly leaf skeletonization damage (*Caliroa cerasi*) to `Pear - pear slug damage`, leaf-rolling gall and aphid damage (*Dasineura pyri*) to `Pear - pear leaf curl`, and European black spot (*Fabraea maculata*) to supplement existing `Pear - pear black spot`.
  * **Neural Feature Deduplication & Tensor Clustering:** Audited 3,006 raw candidate images across target classes using exact MD5 hashing and GPU-accelerated deep neural feature embeddings (`MobileNetV3` at $\ge 0.95$ cosine similarity). Quarantined 41 redundant burst shots into `data/raw/quarantine_pear_duplicates/` with full JSON audit manifests.
  * **Foliar Multi-Class Ingestion:** Sourced **2,003 clean specimens** for `Pear - pear slug damage`, **53 clean specimens** for `Pear - pear leaf curl`, supplemented **`Pear - pear black spot`** with **+867 specimens** (expanded to 1,298 images), and supplemented **`Pear - Healthy`** with **+42 specimens** (expanded to 416 images), expanding Pear to a comprehensive 5-class stone/pome fruit diagnostic suite (3,963 clean foliar images) with verified zero cross-split data leakage ($\text{Train} \cap \text{Val} \cap \text{Test} = \emptyset$).

---

### 29. Kaggle: Rice Leafs Disease Dataset (High-Resolution Foliar Macro Photography)
* **Lead Contributor:** Dede Ikhsan Dwi Saputra
* **Dataset Title:** *Rice Leafs Disease Dataset*
* **Repository Link:** [kaggle.com/datasets/dedeikhsandwisaputra/rice-leafs-disease-dataset](https://www.kaggle.com/datasets/dedeikhsandwisaputra/rice-leafs-disease-dataset)
* **License:** Open Academic / Research Access
* **Contributed Scope:** High-resolution macro and laboratory photography ($1600 \times 1600$ px) of Rice (*Oryza sativa*) leaf blades showing detailed pathogen lesion morphology across 6 major foliar categories: Bacterial Leaf Blight (*Xanthomonas oryzae*), Brown Spot (*Bipolaris oryzae*), Leaf Blast (*Magnaporthe oryzae*), Leaf Scald (*Microdochium oryzae*), Narrow Brown Spot (*Cercospora janseana*), and Healthy control blades.
* **Sanitization & Domain Scope Interventions:**
  * **Foliar Spatial Resolution Fortification:** Resolved the extreme downsampling lesion-erasure bottleneck of legacy wide-canopy rice hill captures by introducing 2,376 clean $1600 \times 1600$ close-up leaf captures where individual lesions dominate the frame area.
  * **Cryptographic Deduplication & Split Isolation:** Audited 2,628 candidate files, quarantining 252 intra-class duplicates to `data/raw/quarantine_rice_lab_duplicates/`. Ingested 2,376 clean unique images under deterministic 80-10-10 contiguous index slicing across 6 classes, adding two brand-new foliar pathology categories: `Paddy - Leaf Scald` (357 images) and `Paddy - Narrow Brown Spot` (409 images).
  * **Zero Leakage Verification:** Purged 25 legacy cross-split collisions across the entire benchmark, establishing mathematically verified zero leakage ($\text{Train} \cap \text{Val} \cap \text{Test} = \emptyset$).

---

### 30. Mendeley Data / Dharrao et al. (2025): Niphad Grape Leaf Disease Dataset (NGLD)
* **Lead Researchers:** Madhuri Dharrao, Deepak Dharrao, & Rakesh Sonawane (Symbiosis International University & MPKV)
* **Dataset Title:** *Niphad Grape Leaf Disease Dataset (NGLD)*
* **Mendeley DOI:** [10.17632/8nnd2ypcv3.1](https://doi.org/10.17632/8nnd2ypcv3.1)
* **Kaggle Mirror:** [kaggle.com/datasets/adibamuttaqin/niphad-grapeleaf-disease-dataset](https://www.kaggle.com/datasets/adibamuttaqin/niphad-grapeleaf-disease-dataset)
* **License:** Creative Commons Attribution 4.0 International (CC BY 4.0) / CC BY-SA 4.0
* **Contributed Scope:** Authentic mobile-captured table grape (*Vitis vinifera*) foliage collected directly in commercial vineyards in Niphad (Nashik, Maharashtra, India).
* **Sanitization & Domain Scope Interventions:**
  * Purged exact intra-class duplicate files (6 duplicates in powdery mildew).
  * Ingested pristine foliar specimens:
    * `Grape - grape downy mildew` (966 specimens; *Plasmopara viticola*)
    * `Grape - grape powdery mildew` (400 specimens; *Erysiphe necator*)
    * `Grape - grape bacterial rot` (100 specimens; *Xanthomonas ampelina*)
  * Cryptographically verified zero cross-split data leakage ($\text{Train} \cap \text{Val} \cap \text{Test} = \emptyset$) with 80-10-10 deterministic distribution.

---

### 31. Kaggle: Grape Disease Dataset Original (rm1000)
* **Lead Contributor:** rm1000
* **Dataset Title:** *Grape Disease Dataset (Original)*
* **Repository Link:** [kaggle.com/datasets/rm1000/grape-disease-dataset-original](https://www.kaggle.com/datasets/rm1000/grape-disease-dataset-original)
* **License:** Public Domain (CC0 1.0)
* **Contributed Scope:** Curated foliar specimens of table and wine grapes showing distinctive necrotic lesion morphologies across two major vineyard pathologies.
* **Sanitization & Domain Scope Interventions:**
  * Pooled source train and test splits, verified 0 internal duplicates and 0 cross-class collisions with existing active classes.
  * Ingested pristine foliar specimens:
    * `Grape - Leaf Blight` (2,152 specimens; *Pseudocercospora vitis* / *Isariopsis cladosporioides*)
    * `Grape - Esca (Black Measles)` (2,400 specimens; *Phaeomoniella chlamydospora* / *Phaeoacremonium minimum*)
  * Balanced into leak-free 80% Train, 10% Val, 10% Test partitions with mathematical split disjointness verification ($\text{Train} \cap \text{Val} \cap \text{Test} = \emptyset$).

---

### 32. Kaggle: Plum Leafs Foliar Pathology Dataset (Ronok Hasan)
* **Lead Contributor:** Ronok Hasan (`ronokhasan`)
* **Dataset Title:** *plum-leafs: Real-World In-the-Wild Plum Foliar Diagnostics*
* **Repository Link:** [kaggle.com/datasets/ronokhasan/plum-leafs](https://www.kaggle.com/datasets/ronokhasan/plum-leafs)
* **License:** Open Access / Research Use
* **Contributed Scope:** High-resolution unconstrained mobile photography ($3000 \times 4000$ and $1584 \times 2816$ px) of Plum (*Prunus domestica*) foliage captured in natural orchards, exhibiting natural healthy canopy structures and weevil foliar infestation (*Conotrachelus nenuphar* / *Curculio* foliar feeding damage).
* **Sanitization & Domain Scope Interventions:**
  * **Healthy Domain Rebalancing:** Sourced 100 unique natural healthy leaves. Rebalanced the legacy `Plum - Healthy` suite by keeping 28 baseline specimens (20 train, 4 val, 4 test) and archiving 938 excess legacy laboratory white-background duplicates to `data/raw/quarantine_plum_excess_legacy_healthy/`. Combined with the 100 natural specimens (80 train, 10 val, 10 test) to form a calibrated 128-specimen foliar baseline.
  * **Plum Weevil Ingestion:** Deduplicated and ingested 99 pristine specimens of `Plum - plum weevil` (79 train, 10 val, 10 test) under cryptographic anti-leakage verification ($\text{Train} \cap \text{Val} \cap \text{Test} = \emptyset$).

---

### 33. Mendeley Data / Bhowmik et al. (2023): Jamun (Java Plum) Leaf Disease Dataset
* **Lead Researchers:** Auvick Chandra Bhowmik and Taimur Ahad (Daffodil International University)
* **Dataset Title:** *Java Plum Leaf Disease Dataset*
* **Mendeley DOI:** [10.17632/43d75vptz4.2](https://doi.org/10.17632/43d75vptz4.2)
* **Publication Date:** November 2023
* **License:** Creative Commons Attribution 4.0 International (CC BY 4.0)
* **Botanical Species:** Jamun / Java Plum (*Syzygium cumini*, family Myrtaceae)
* **Taxonomic Clarification & Botanical Scope:** Java Plum is botanically *Syzygium cumini* (family Myrtaceae), a tropical/subtropical evergreen tree crop distinct from true Plum (*Prunus domestica*, family Rosaceae). To ensure strict botanical accuracy, Jamun is established as its own independent commercial crop family (#34) in the benchmark.
* **Sanitization & Anti-Leakage Interventions:**
  * Sourced authentic unaugmented foliar in-situ photography, establishing the 5-class Jamun suite:
    * `Jamun - Bacterial Spot` (400 specimens)
    * `Jamun - Brown Blight` (400 specimens)
    * `Jamun - Healthy` (272 unique specimens; 128 duplicate copies purged)
    * `Jamun - Powdery Mildew` (400 specimens)
    * `Jamun - Sooty Mold` (400 specimens)
  * Quarantined 400 desiccated senescent leaves (`Dry`) into `data/raw/quarantine_jamun_dry_leaf/` (abiotic/senescent non-pathological tissue).
  * Safely reverted mistaken legacy Java Plum classes from Plum (*Prunus domestica*), preserving authentic Plum intact across its 4 genuine foliar classes: `Plum - Healthy` (128 specimens), `Plum - plum insect hole` (674 specimens), `Plum - plum weevil` (99 specimens), and `Plum - plum yellow leaf` (786 specimens).
  * Partitioned deterministically into 80% Train, 10% Val, 10% Test splits with verified mathematical zero cross-split leakage ($\text{Train} \cap \text{Val} \cap \text{Test} = \emptyset$).
* **Figure & Asset Attribution:** All diagnostic evaluation pair figures derived from this dataset (`reports/v1/figures/jamun_all_pairs_*.png`) are distributed under the Creative Commons Attribution 4.0 International (CC BY 4.0) license; credited to Bhowmik et al. (2023), Mendeley Data, DOI: [10.17632/43d75vptz4.2](https://doi.org/10.17632/43d75vptz4.2).

---

### 34. Kaggle / Kapadnis: Eggplant Disease Recognition Benchmark Dataset
* **Lead Contributor:** Sujay Kapadnis (`sujaykapadnis`)
* **Dataset Title:** *Eggplant Disease Recognition Dataset*
* **Repository Link:** [kaggle.com/datasets/sujaykapadnis/eggplant-disease-recognition-dataset](https://www.kaggle.com/datasets/sujaykapadnis/eggplant-disease-recognition-dataset)
* **License:** Open Access Research License
* **Contributed Scope:** In-situ photography of Eggplant / Brinjal (*Solanum melongena*) foliage showing clear foliar symptoms across major biotic stresses.
* **Sanitization & Domain Scope Interventions:**
  * Sourced strictly from original unaugmented camera directories (`Original Images (Version 02)`).
  * Filtered internal burst captures with exact MD5 deduplication and partitioned into deterministic 80% Train, 10% Val, 10% Test splits across 6 comprehensive foliar classes:
    * `Eggplant - Healthy` (200 specimens)
    * `Eggplant - Cercospora Leaf Spot` (199 specimens)
    * `Eggplant - Mosaic Virus` (190 specimens)
    * `Eggplant - Little Leaf` (194 specimens)
    * `Eggplant - White Mold` (195 specimens)
    * `Eggplant - Wilt` (197 specimens)
  * Quarantined unviable/data-starved fruit blight specimens (`Eggplant - Phytophthora Blight`) to uphold strict foliar (leaf-only) scope consistency, verifying 0.000% cross-split leakage.

---

### 35. Mendeley Data / Elvsava (2023): Pepper Bell Leaf Disease Dataset
* **Lead Researcher:** Roughten Elvsava
* **Dataset Title:** *Pepper Bell Leaf Disease*
* **Mendeley DOI:** [10.17632/w9drvtxg9g.1](https://doi.org/10.17632/w9drvtxg9g.1)
* **License:** Creative Commons Attribution 4.0 International (CC BY 4.0)
* **Contributed Scope:** High-resolution foliar photography of Bell Pepper (*Capsicum annuum*) leaves capturing distinctive viral, fungal, and physiological stress morphologies.
* **Sanitization & Domain Scope Interventions:**
  * Audited candidate folders and eliminated synthetic rotation/flip tokens (`180deg`, `fliptb`, `fliplr`, `_aug`), extracting strictly genuine natural-background captures.
  * Purged cross-class bacterial spot contaminant copies from fungal folders.
  * Ingested pristine foliar specimens establishing:
    * `Bell Pepper - Leaf Curl Virus`
    * `Bell Pepper - Nutrition Deficiency`
    * `Bell Pepper - bell pepper frogeye leaf spot`
    * `Bell Pepper - bell pepper powdery mildew`
  * Partitioned under cryptographic verification for 0.000% cross-split data leakage.

---

### 36. Mendeley Data / Thorwat et al. (2026): Multi-Class Soybean Leaf Disease Dataset
* **Lead Researchers:** Madhuri Thorwat, Pranali Magdum, Shweta Jadhav, Anushka Sutar, & Riya Oswal
* **Dataset Title:** *Multi-Class Soybean Leaf Disease Dataset: Healthy and Diseased Leaf Images for Machine Learning*
* **Mendeley DOI:** [10.17632/6fhphxg297.2](https://doi.org/10.17632/6fhphxg297.2)
* **License:** Creative Commons Attribution 4.0 International (CC BY 4.0)
* **Contributed Scope:** High-resolution DSLR natural-background captures ($5472 \times 3648$ and $4608 \times 3456$ px) of Soybean (*Glycine max*) foliage.
* **Sanitization & Domain Scope Interventions:**
  * Ingested pristine unaugmented foliar specimens contributing to:
    * `Soybean - Bacterial Blight` (97 specimens; *Pseudomonas savastanoi pv. glycinea*)
    * `Soybean - Cercospora Leaf Blight` (79 specimens; *Cercospora kikuchii*)
    * `Soybean - Rust` (92 specimens; *Phakopsora pachyrhizi*)
    * `Soybean - Sudden Death Syndrome` (104 specimens; *Fusarium virguliforme*)
  * Merged with companion cohorts using domain-stratified 80-10-10 partitioning with mathematical split disjointness verification.

---

### 37. Kaggle / Bhujade: Soybean Leaf Dataset for Disease Classification
* **Lead Contributor:** Vaishali G. Bhujade (`vaishaligbhujade`)
* **Dataset Title:** *Soybean leaf dataset for disease classification*
* **Repository Link:** [kaggle.com/datasets/vaishaligbhujade/soybean-leaf-dataset-for-disease-classification](https://www.kaggle.com/datasets/vaishaligbhujade/soybean-leaf-dataset-for-disease-classification)
* **License:** Open Access Research License
* **Contributed Scope:** High-resolution natural-background photography (up to $8000 \times 6000$ px) of Soybean foliage across diverse fungal, bacterial, and physiological conditions.
* **Sanitization & Domain Scope Interventions:**
  * Sourced pristine unaugmented natural-background specimens contributing to:
    * `Soybean - Bacterial Pustule` (110 specimens; *Xanthomonas axonopodis pv. glycines*)
    * `Soybean - Target Leaf Spot` (110 specimens; *Corynespora casiicola*)
    * `Soybean - Rust` (106 specimens; *Phakopsora pachyrhizi*)
    * `Soybean - Frogeye Leaf Spot` (38 specimens; *Cercospora sojina*)
    * `Soybean - Healthy` (110 specimens; expanding clean control baseline)
  * Partitioned into leak-free 80-10-10 splits with verified zero data leakage.

---

### 38. Kaggle / sivm205: Soybean Diseased Leaf Dataset
* **Lead Contributor:** sivm205 (`sivm205`)
* **Dataset Title:** *Soybean diseased leaf dataset*
* **Repository Link:** [kaggle.com/datasets/sivm205/soybean-diseased-leaf-dataset](https://www.kaggle.com/datasets/sivm205/soybean-diseased-leaf-dataset)
* **License:** Open Access Research License
* **Contributed Scope:** Foliar pathology imagery of Soybean covering viral, fungal, and bacterial manifestations.
* **Sanitization & Domain Scope Interventions:**
  * Filtered redundant duplicate overlaps against companion datasets.
  * Ingested pristine specimens contributing to:
    * `Soybean - Powdery Mildew` (137 specimens; *Microsphaera diffusa*)
    * `Soybean - Yellow Mosaic` (110 specimens; Mungbean yellow mosaic virus)
    * `Soybean - Bacterial Blight` (50 specimens; *Pseudomonas savastanoi pv. glycinea*)
    * `Soybean - Brown Spot` (27 specimens; *Septoria glycines*)
    * `Soybean - Sudden Death Syndrome` (6 non-overlapping specimens)
  * Balanced into domain-stratified splits with cryptographic anti-leakage verification.

---

### 39. Kaggle / Shah: Mango Leaf Disease Dataset
* **Lead Contributor:** Arya Shah (`aryashah2k`)
* **Dataset Title:** *Mango Leaf Disease Dataset*
* **Repository Link:** [kaggle.com/datasets/aryashah2k/mango-leaf-disease-dataset](https://www.kaggle.com/datasets/aryashah2k/mango-leaf-disease-dataset)
* **License:** CC0: Public Domain
* **Contributed Scope:** In-situ foliar photography across 8 comprehensive Mango (*Mangifera indica*) classes: Anthracnose (*Colletotrichum gloeosporioides*), Bacterial Canker (*Xanthomonas citri pv. mangiferaeindicae*), Cutting Weevil (*Deporaus marginatus* foliar feeding), Die Back (*Lasiodiplodia theobromae*), Gall Midge (*Procontarinia matteiana* foliar blister galls), Powdery Mildew (*Oidium mangiferae*), Sooty Mould (*Capnodium mangiferae*), and Healthy control foliage.
* **Sanitization & Anti-Leakage Interventions:**
  * **Duplicate Inflation Purge:** Uncovered 21 synthetic duplicate copies (repeated `- Copy (Custom).jpg` and `(Custom)(1).jpg` files) created to artificially inflate class quotas to 500 images. Quarantined all 21 identical copies to `data/raw/quarantine_mango_duplicates/`.
  * **Burst Capture Anti-Leakage Partitioning:** Chronologically ordered all genuine captures by filename timestamps (`YYYYMMDD_HHMMSS`) and partitioned them using contiguous time-series index slicing (80% Train, 10% Val, 10% Test), ensuring burst-shot clusters from the same tree or observation session never cross-contaminate evaluation splits.
  * **Ingested Scope:** Sourced **3,979 clean, unique foliar specimens** establishing Mango as the 32nd commercial crop family in the benchmark with mathematically verified zero cross-split data leakage ($\text{Train} \cap \text{Val} \cap \text{Test} = \emptyset$).

---

### 40. Kaggle / Dalvi: Guava Disease Dataset (4 Types)
* **Lead Contributor:** Omkar Manohar Dalvi (`omkarmanohardalvi`)
* **Dataset Title:** *Guava Disease Dataset (4 Types)*
* **Repository Link:** [kaggle.com/datasets/omkarmanohardalvi/guava-disease-dataset-4-types](https://www.kaggle.com/datasets/omkarmanohardalvi/guava-disease-dataset-4-types)
* **License:** Community Data License Agreement - Permissive (CDLA-Permissive) / Open Access Research
* **Contributed Scope:** High-resolution digital SLR natural-background photography ($6000 \times 4000$ px) across 5 comprehensive Guava (*Psidium guajava*) foliar pathology classes:
  * `Guava - Canker` (278 specimens; *Pestalotiopsis psidii*)
  * `Guava - Dot` (178 specimens; *Cephaleuros virescens* / Algal Leaf Spot)
  * `Guava - Healthy` (1,289 specimens; Clean foliar negative control baseline)
  * `Guava - Mummification` (275 specimens; *Botryodiplodia theobromae* foliar/twig blight)
  * `Guava - Rust` (279 specimens; *Puccinia psidii*)
* **Sanitization & Anti-Leakage Interventions:**
  * **Botanical Scope Verification:** Validated that all 2,299 captures represent foliar pathology and canopy structures (eliminating post-harvest fruit rots).
  * **Sequence-Aware Leak-Free Partitioning:** Sorted captures deterministically by camera capture sequence to cluster temporal burst shots, then partitioned into the benchmark's standardized 80% Train, 10% Val, and 10% Test splits. Verified zero cross-split cryptographic leakage ($\text{Train} \cap \text{Val} \cap \text{Test} = \emptyset$) with boundary pHash Hamming distance $\ge 12$.
  * **Benchmark Integration:** Ingested **2,299 pristine images**, establishing Guava as the 33rd crop family in the benchmark across 5 new standardized classes.

---

### 41. Mendeley Data: Guava Leaf Disease Image Dataset (Bangladesh)
* **Lead Researchers:** Md Naimul Hasan & Md Fahimur Rahman (Dhaka, Bangladesh)
* **Dataset Title:** *Guava Leaf Disease Image Dataset for Classification and Detection of Common Pathologies from Bangladesh*
* **Mendeley DOI:** [10.17632/46spm4z4d3.2](https://doi.org/10.17632/46spm4z4d3.2)
* **Repository Link:** [data.mendeley.com/datasets/46spm4z4d3/2](https://data.mendeley.com/datasets/46spm4z4d3/2)
* **License:** Creative Commons Attribution 4.0 International (CC BY 4.0)
* **Contributed Scope:** High-resolution segmented photography ($512 \times 512$ px, uniform white background) of Guava (*Psidium guajava*) foliage collected under natural conditions in Dhaka, Bangladesh across 6 classes:
  * `Guava - Anthracnose` (828 clean specimens; *Colletotrichum gloeosporioides*) [Establishes new benchmark class]
  * `Guava - Spiraling Whitefly` (943 clean specimens; *Aleurodicus dispersus* foliar wax/nymph colonies) [Establishes new benchmark class]
  * `Guava - Canker` (938 clean specimens; *Pestalotiopsis psidii* foliar lesions, mislabeled as 'Citrus Canker' by source data collectors)
  * `Guava - Dot` (881 clean specimens; *Cephaleuros virescens* / Algal Leaf Spot)
  * `Guava - Rust` (943 clean specimens; *Puccinia psidii* / Red Rust)
  * `Guava - Healthy` (942 clean specimens; Segmented negative control baseline)
* **Sanitization & Anti-Leakage Interventions:**
  * **Ambiguous Cross-Class Duplicate Quarantine:** Detected and quarantined 42 cross-class duplicate files (21 identical cryptographic hashes mistakenly filed under competing disease folders in the raw data, such as Algal Spot vs Healthy or Anthracnose vs Canker) to `data/raw/quarantine_mendeley_guava/ambiguous_cross_class/`.
  * **Intra-Class Duplicate Copy Purge:** Quarantined 141 exact duplicate copies to `data/raw/quarantine_mendeley_guava/duplicate_copies/`.
  * **Taxonomic Correction:** Corrected the erroneous 'Citrus Canker' designation to `Guava - Canker` after botanical verification confirmed the leaves possess guava venation (*Psidium guajava*) rather than citrus winged petioles.
  * **Leak-Free Partitioning:** Sequentially partitioned into 80% Train, 10% Val, and 10% Test contiguous splits. Mathematically verified zero cross-split leakage ($\text{Train} \cap \text{Val} \cap \text{Test} = \emptyset$) with boundary pHash Hamming distance $\ge 20$.
  * **Benchmark Integration:** Ingested **5,475 clean, unique specimens**, introducing 2 brand-new classes (`Guava - Anthracnose` and `Guava - Spiraling Whitefly`) and bringing Guava to 7 comprehensive pathology classes and 7,774 total specimens.

---

---

## 📚 Complete Clean BibTeX Citations

```bibtex
@article{hughes2015plantvillage,
  title     = {An open access repository of images on plant health to enable the development of mobile disease diagnostics},
  author    = {Hughes, David P. and Salath{\'e}, Marcel},
  journal   = {arXiv preprint arXiv:1511.08060},
  year      = {2015},
  doi       = {10.48550/arXiv.1511.08060},
  url       = {https://arxiv.org/abs/1511.08060}
}

@misc{tanniru2025masterplantdisease,
  title     = {Master Plant Disease Dataset (plant-disease-processed)},
  author    = {Tanniru, Hari Sri Shanmukha Sai},
  year      = {2025},
  publisher = {Kaggle},
  url       = {https://www.kaggle.com/datasets/harisri2005/plant-disease-processed}
}

@misc{dumlao2024cauliflower,
  title     = {Cauliflower Leaf Diseases: A Computer Vision Dataset for Smart Agriculture},
  author    = {Dumlao, Jocelyn},
  year      = {2024},
  publisher = {Mendeley Data},
  version   = {v1},
  doi       = {10.17632/x26px3xnmy.1}
}

@misc{nirob2025chili,
  title     = {Chili Plant Leaf Disease and Growth Stage Dataset from Bangladesh},
  author    = {Nirob, Md Asraful Sharker and Siam, A K M Fazlul Kobir and Bishshash, Prayma and Assaduzzaman, Md},
  year      = {2025},
  publisher = {Mendeley Data},
  version   = {v1},
  doi       = {10.17632/w9mr3vf56s.1},
  note      = {Licensed under CC BY 4.0; redistributed via Kaggle mirror by Suryia Pooventhan R}
}

@misc{ghose2022corn,
  title     = {Corn or Maize Leaf Disease Dataset},
  author    = {Ghose, Smaranjit},
  year      = {2022},
  publisher = {Kaggle},
  url       = {https://www.kaggle.com/datasets/smaranjitghose/corn-or-maize-leaf-disease-dataset}
}

@article{esgario2020deep,
  title     = {Deep learning for classification and severity estimation of coffee leaf biotic disorders},
  author    = {Esgario, Jose G. M. and Barbosa, Pedro H. S. and Krohling, Renato A.},
  journal   = {Computers and Electronics in Agriculture},
  volume    = {169},
  pages     = {105214},
  year      = {2020},
  publisher = {Elsevier},
  doi       = {10.1016/j.compag.2019.105214}
}

@inproceedings{singh2020plantdoc,
  title     = {PlantDoc: A Dataset for Visual Plant Disease Detection in the Wild},
  author    = {Singh, Davinder and Jain, Nitesh and Jain, Pranjali and Kayal, Pratik and Kumawat, Sudhakar and Batra, Nipun},
  booktitle = {Proceedings of the 7th ACM IKDD CoDS and 25th COMAD},
  pages     = {249--253},
  year      = {2020},
  doi       = {10.1145/3371158.3371196},
  url       = {https://doi.org/10.1145/3371158.3371196}
}

@misc{reza2024garlic,
  title     = {A comprehensive dataset of garlic leaf images for disease classification},
  author    = {Reza, Farhad and Rahman, S. M. Asifur and Islam, Tarequl and Rahman, Md. Hasibur and Amzad, Anika and Rahman, Md. Wahidur},
  year      = {2024},
  publisher = {Mendeley Data},
  version   = {v1},
  doi       = {10.17632/ff78hgnbhn.1}
}

@misc{wong2024ginger,
  title     = {Ginger-Leaf-Dataset: A Multi-Class High-Resolution Image Dataset for Precision Ginger Disease Diagnostics},
  author    = {Wong, Jay},
  year      = {2024},
  publisher = {GitHub},
  url       = {https://github.com/wongjay1941/Ginger-Leaf-Dataset}
}

@article{yigezu2023ginger,
  title     = {Ginger Disease Detection and Classification Using Deep Learning and Pre-Trained Convolutional Neural Networks},
  author    = {Yigezu, Mesay Gemeda},
  journal   = {Ethiopian Journal of Agricultural Sciences / Research Repository},
  year      = {2023},
  publisher = {GitHub},
  url       = {https://github.com/Mesay-Gemeda/Ginger-disease-detection-using-CNN-and-pertrained-model}
}

@misc{jha2024lettuce,
  title     = {Lettuce Diseases Dataset: A Benchmark for Foliar Pathology Classification},
  author    = {Jha, Ashish},
  year      = {2024},
  publisher = {Kaggle},
  url       = {https://www.kaggle.com/datasets/ashishjstar/lettuce-diseases}
}

@article{farman2022peach,
  title     = {Efficientnet-based robust recognition of peach plant diseases in field images},
  author    = {Farman, Haleem and Ahmad, Jamil and Jan, Bilal and Shahzad, Yasir and Abdullah, Muhammad and Ullah, Atta},
  journal   = {Computers, Materials & Continua},
  volume    = {71},
  number    = {1},
  pages     = {2073--2089},
  year      = {2022},
  publisher = {Tech Science Press},
  doi       = {10.32604/cmc.2022.021090},
  note      = {Mendeley Data repository: 10.17632/3pmj85snvw.1}
}

@article{nayeem2025plum,
  title     = {A comprehensive image dataset of plum leaf and fruit for disease classification},
  author    = {Nayeem, Rejowan Arifin and Al Muhib, S. M. Abdullah and Marjan, Shahriar and Bijoy, Md Hasan Imam and Assaduzzaman, Md},
  journal   = {Data in Brief},
  year      = {2025},
  publisher = {Elsevier},
  doi       = {10.17632/w7sdx55m7z.1}
}

@misc{khan2026plumleaf,
  title     = {plum_leaf: High-Resolution In-the-Wild Foliar Plum Pathology},
  author    = {Khan, Faisal},
  year      = {2026},
  publisher = {Kaggle},
  url       = {https://www.kaggle.com/datasets/faisalkhanx/plum-leaf}
}

@misc{hossin2024potatoleaf,
  title     = {Potato Leaf Disease Dataset: Multi-Class Foliar and Biotic Stress Diagnostics},
  author    = {Hossin, Shahad},
  year      = {2024},
  publisher = {Kaggle},
  url       = {https://www.kaggle.com/datasets/shahadhossin567r7455/potato-leaf-disease-dataset}
}

@misc{getch2024wheatleaf,
  title     = {Wheat Leaf Dataset: High-Resolution In-Field Foliar Diagnostics},
  author    = {Getch, Olyad},
  year      = {2024},
  publisher = {Kaggle},
  url       = {https://www.kaggle.com/datasets/olyadgetch/wheat-leaf-dataset}
}

@misc{khan2024wheatleafdisease,
  title     = {Wheat Leaf Disease Dataset: Multi-Class Foliar Pathology},
  author    = {Khan, Aamer},
  year      = {2024},
  publisher = {Kaggle},
  url       = {https://www.kaggle.com/datasets/khanaamer/wheat-leaf-disease-dataset}
}

@misc{sourabh2021citrus,
  title     = {Citrus Leaves Dataset: Multi-Class In-Field Foliar Pathology},
  author    = {Sourabh},
  year      = {2021},
  publisher = {Kaggle},
  url       = {https://www.kaggle.com/datasets/sourabh2001/citrus-leaves-dataset}
}

@misc{kapadnis2023cucumber,
  title     = {Cucumber Disease Recognition Dataset: Multi-Class Foliar Diagnostics},
  author    = {Kapadnis, Sujay},
  year      = {2023},
  publisher = {Kaggle},
  url       = {https://www.kaggle.com/datasets/sujaykapadnis/cucumber-disease-recognition-dataset}
}

@misc{ikteshad2025vegetableleaf,
  title     = {Comprehensive Vegetable Leaf Disease Image Collection},
  author    = {Ikteshad, Deeya and Likhan, Md. Iftekhar Rahman and Rafi, Ifran-Al and Khan, Md Nasrul Islan and Nirob, Md Asraful Sharker},
  year      = {2025},
  publisher = {Mendeley Data},
  version   = {v1},
  doi       = {10.17632/rh8c5tgg5k.1}
}

@misc{ayawli2025cabbage,
  title     = {Image dataset of Cabbage Crop diseases},
  author    = {Ayawli, Ben Beklisi Kwame and Kopri, Gyimah and Dawson, John Kwao and Bediako-Kyeremeh, Bright and Buabeng, Solomon Antwi and Deveh, Desmond and Ayawli, Esinam Irene Beklisi and Badu, Esther and Lamusah, Dawda},
  year      = {2025},
  publisher = {Mendeley Data},
  version   = {v1},
  doi       = {10.17632/sjmgzhwrxv.1}
}

@misc{therealoise2020bean,
  title     = {Bean Disease Dataset: Field Foliar Images from Makerere AI Lab},
  author    = {Oise and {Makerere AI Research Lab}},
  year      = {2020},
  publisher = {Kaggle},
  url       = {https://www.kaggle.com/datasets/therealoise/bean-disease-dataset}
}

@misc{billah2025agrivision4,
  title     = {Agri-Vision4: A Comprehensive Multi-Crop Leaf Disease Dataset of Tomato, Papaya, Zucchini, and Bottle Gourd from Bangladesh},
  author    = {Billah, Md Masum and Rahman, Md. Anisur and Sagor, Saifuddin and Parvin, Sanzida and Uddin, Mohammad Shorif},
  year      = {2025},
  publisher = {Mendeley Data},
  version   = {v1},
  doi       = {10.17632/8t6k37ztxc.1}
}

@article{afzaal2021strawberry,
  title     = {An in-field deep learning based strawberry plant disease detection framework using fine-tuning and attention module},
  author    = {Afzaal, Usman and Bhattarai, Bipul and Pandeya, Young-Roc and Lee, Joonwhoan},
  journal   = {Sensors},
  volume    = {21},
  number    = {24},
  pages     = {8345},
  year      = {2021},
  publisher = {MDPI},
  doi       = {10.3390/s21248345}
}

@article{khan2025plantcity,
  title     = {PlantCity: A Comprehensive Image Based on Multi Crop Leaves in Pakistan},
  author    = {Khan, Muhammad Sheraz and Nisa, Kainat and Ahmad, Irshad and Zubair, Muhammad and Alshammari, Kholood},
  journal   = {Data in Brief},
  volume    = {60},
  pages     = {112130},
  year      = {2025},
  publisher = {Elsevier},
  doi       = {10.1016/j.dib.2025.112130}
}

@misc{codewithsk2025cherry,
  title     = {Cherry Leaf Disease on PlantCity 2025},
  author    = {codewithsk},
  year      = {2025},
  publisher = {Kaggle},
  url       = {https://www.kaggle.com/datasets/codewithsk/cherry-leaf-disease-on-plantcity-2025}
}

@misc{mannan2025plantcity,
  title     = {PlantCity Multi-Crop Foliar Benchmark},
  author    = {Mannan, Abdul},
  year      = {2025},
  publisher = {Kaggle},
  url       = {https://www.kaggle.com/datasets/abdulmannann/plantcity}
}

@misc{alamin2023lld,
  title     = {LLD: Lemon Leaf Disease Image Dataset for AI-Based Plant Health Detection},
  author    = {Al Amin, Md},
  year      = {2023},
  publisher = {Mendeley Data},
  version   = {v1},
  doi       = {10.17632/9ywvpv3xtg.1},
  url       = {https://data.mendeley.com/datasets/9ywvpv3xtg/1}
}

@article{fenu2021diamos,
  title     = {DiaMOS Plant: A Dataset for Diagnosis and Monitoring Plant Disease},
  author    = {Fenu, Gianni and Malloci, Francesca Maridina},
  journal   = {Agronomy},
  volume    = {11},
  number    = {11},
  pages     = {2107},
  year      = {2021},
  publisher = {MDPI},
  doi       = {10.3390/agronomy11112107}
}

@misc{mir2021pear,
  title     = {Pear Leaf Disease Dataset (DiaMOS Plant Kaggle Mirror)},
  author    = {Mir, Syed Zain},
  year      = {2021},
  publisher = {Kaggle},
  url       = {https://www.kaggle.com/datasets/syedzainmir/pear-leaf-disease}
}

@misc{saputra2022rice,
  title     = {Rice Leafs Disease Dataset: High-Resolution Foliar Pathology Benchmark},
  author    = {Saputra, Dede Ikhsan Dwi},
  year      = {2022},
  publisher = {Kaggle},
  url       = {https://www.kaggle.com/datasets/dedeikhsandwisaputra/rice-leafs-disease-dataset}
}

@misc{dharrao2025niphad,
  title     = {Niphad Grape Leaf Disease Dataset (NGLD)},
  author    = {Dharrao, Madhuri and Dharrao, Deepak and Sonawane, Rakesh},
  year      = {2025},
  publisher = {Mendeley Data},
  version   = {v1},
  doi       = {10.17632/8nnd2ypcv3.1},
  url       = {https://data.mendeley.com/datasets/8nnd2ypcv3/1}
}

@misc{muttaqin2025niphad,
  title     = {Niphad Grapeleaf Disease Dataset (Kaggle Mirror)},
  author    = {Muttaqin, Adiba},
  year      = {2025},
  publisher = {Kaggle},
  url       = {https://www.kaggle.com/datasets/adibamuttaqin/niphad-grapeleaf-disease-dataset}
}

@misc{rm1000grape,
  title     = {Grape Disease Dataset (Original)},
  author    = {rm1000},
  year      = {2023},
  publisher = {Kaggle},
  url       = {https://www.kaggle.com/datasets/rm1000/grape-disease-dataset-original}
}

@misc{hasan2024plum,
  title     = {plum-leafs: Real-World In-the-Wild Plum Foliar Diagnostics},
  author    = {Hasan, Ronok},
  year      = {2024},
  publisher = {Kaggle},
  url       = {https://www.kaggle.com/datasets/ronokhasan/plum-leafs}
}

@misc{bhowmik2023javaplum,
  title     = {Java Plum Leaf Disease Dataset},
  author    = {Bhowmik, Auvick Chandra and Ahad, Taimur},
  year      = {2023},
  publisher = {Mendeley Data},
  version   = {v3},
  doi       = {10.17632/43d75vptz4.3},
  url       = {https://data.mendeley.com/datasets/43d75vptz4/3}
}

@misc{kapadnis2023eggplant,
  title     = {Eggplant Disease Recognition Dataset},
  author    = {Kapadnis, Sujay},
  year      = {2023},
  publisher = {Kaggle},
  url       = {https://www.kaggle.com/datasets/sujaykapadnis/eggplant-disease-recognition-dataset}
}

@misc{elvsava2023pepper,
  title     = {Pepper Bell Leaf Disease},
  author    = {Elvsava, Roughten},
  year      = {2023},
  publisher = {Mendeley Data},
  version   = {v1},
  doi       = {10.17632/w9drvtxg9g.1},
  url       = {https://data.mendeley.com/datasets/w9drvtxg9g/1}
}

@misc{thorwat2026soybean,
  title     = {Multi-Class Soybean Leaf Disease Dataset: Healthy and Diseased Leaf Images for Machine Learning},
  author    = {Thorwat, Madhuri and Magdum, Pranali and Jadhav, Shweta and Sutar, Anushka and Oswal, Riya},
  year      = {2026},
  publisher = {Mendeley Data},
  version   = {v2},
  doi       = {10.17632/6fhphxg297.2},
  url       = {https://data.mendeley.com/datasets/6fhphxg297/2}
}

@misc{bhujade2023soybean,
  title     = {Soybean leaf dataset for disease classification},
  author    = {Bhujade, Vaishali G.},
  year      = {2023},
  publisher = {Kaggle},
  url       = {https://www.kaggle.com/datasets/vaishaligbhujade/soybean-leaf-dataset-for-disease-classification}
}

@misc{sivm2023soybean,
  title     = {Soybean diseased leaf dataset},
  author    = {sivm205},
  year      = {2023},
  publisher = {Kaggle},
  url       = {https://www.kaggle.com/datasets/sivm205/soybean-diseased-leaf-dataset}
}

@misc{shah2022mango,
  title     = {Mango Leaf Disease Dataset},
  author    = {Shah, Arya},
  year      = {2022},
  publisher = {Kaggle},
  url       = {https://www.kaggle.com/datasets/aryashah2k/mango-leaf-disease-dataset}
}

@misc{dalvi2023guava,
  title     = {Guava Disease Dataset (4 Types)},
  author    = {Dalvi, Omkar Manohar},
  year      = {2023},
  publisher = {Kaggle},
  url       = {https://www.kaggle.com/datasets/omkarmanohardalvi/guava-disease-dataset-4-types}
}

@misc{hasan2025guava,
  title     = {Guava Leaf Disease Image Dataset for Classification and Detection of Common Pathologies from Bangladesh},
  author    = {Hasan, Md Naimul and Rahman, Md Fahimur},
  year      = {2025},
  publisher = {Mendeley Data},
  version   = {v2},
  doi       = {10.17632/46spm4z4d3.2},
  url       = {https://data.mendeley.com/datasets/46spm4z4d3/2}
}

@misc{elvsava2026pepper,
  title     = {Pepper Bell Leaf Disease},
  author    = {Elvsava, Roughten},
  year      = {2026},
  publisher = {Mendeley Data},
  version   = {v1},
  doi       = {10.17632/w9drvtxg9g.1},
  url       = {https://data.mendeley.com/datasets/w9drvtxg9g/1}
}

```

---

## 32. Additional Upstream Sources (Bell Pepper & Chilli Audit)

### 32.1 "Pepper Bell Leaf Disease" (Mendeley Data)
- **Title:** Pepper Bell Leaf Disease
- **Contributor:** Roughten Elvsava
- **Repository:** Mendeley Data, Version 1
- **Publication Date:** 23 May 2026
- **DOI:** [10.17632/w9drvtxg9g.1](https://doi.org/10.17632/w9drvtxg9g.1)
- **Direct URL:** [https://data.mendeley.com/datasets/w9drvtxg9g/1](https://data.mendeley.com/datasets/w9drvtxg9g/1)
- **Stated Licence:** Creative Commons Attribution 4.0 International (CC BY 4.0)
- **Image Count:** 9,283 images across 6 categorized folders
- **Known Upstream Issues:** Independent audit (`scripts/data/curation/audit_bellpepper_chilli_copies.py`, documented in [`docs/CASE_STUDY_BELLPEPPER_CHILLI.md`](./CASE_STUDY_BELLPEPPER_CHILLI.md) and [`docs/PATCHES.md`](./PATCHES.md)) verified that images in three of these classes (`Leaf Curl`, `Nutrition Deficiency`, and `Powdery Mildew`) overlap with images from Chilli datasets. Quarantined in Patch P-001.

### 32.2 "Chili Plant Leaf Disease and Growth Stage Dataset from Bangladesh" (Mendeley Data)
- **Title:** Chili Plant Leaf Disease and Growth Stage Dataset from Bangladesh
- **Authors:** Md Asraful Sharker Nirob, A K M Fazlul Kobir Siam, Prayma Bishshash, Md Assaduzzaman
- **Institution:** Daffodil International University, Bangladesh
- **Repository:** Mendeley Data, Version 1
- **Publication Date:** 19 February 2025
- **DOI:** [10.17632/w9mr3vf56s.1](https://doi.org/10.17632/w9mr3vf56s.1)
- **Direct URL:** [https://data.mendeley.com/datasets/w9mr3vf56s/1](https://data.mendeley.com/datasets/w9mr3vf56s/1)
- **Stated Licence:** Creative Commons Attribution 4.0 International (CC BY 4.0)
- **Collection Scope:** In-situ collection in Charpolisha, Jamalpur, Bangladesh (October 2024 to February 2025). 1,856 original in-situ images.

### 32.3 "Image Dataset on Chili Leaf Diseases in the Krishna River Basin of the Deccan Plateau, India" (Mendeley Data)
- **Title:** Image Dataset on Chili Leaf Diseases in the Krishna River Basin of the Deccan Plateau, India
- **Authors:** Rashmi Laxmikant Malghan, Lingaraj K, Karthik Rao M C, Lalit Garg
- **Institution:** Manipal Academy of Higher Education
- **Repository:** Mendeley Data (Versions 1, 2, 3)
- **DOI:** [10.17632/ymt8k9bjkn](https://doi.org/10.17632/ymt8k9bjkn)
- **Stated Licence:** Creative Commons Attribution 4.0 International (CC BY 4.0)

### 32.4 "CHILLI" (Kaggle Redistribution)
- **Title:** CHILLI
- **Uploader:** `suryiapooventhanr`
- **Repository:** Kaggle Datasets
- **URL:** [https://www.kaggle.com/datasets/suryiapooventhanr/chilli](https://www.kaggle.com/datasets/suryiapooventhanr/chilli)

