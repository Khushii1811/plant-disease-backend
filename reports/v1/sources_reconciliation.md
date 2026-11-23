# Upstream Sources Reconciliation Report (Release v1.0)

**Date:** October 2026  
**Curator:** Khushi Patel  
**Branch:** `fix-audit-v1`  
**Reference Manifest:** `reports/v1/sources_redistribution.csv` (36 operational sources, 91,984 images)  
**Reference Literature Catalog:** `docs/SOURCES.md` (41 numbered literature entries)

---

## 1. Overview & Objective

This report provides the formal reconciliation between the **41 numbered literature and repository entries** cataloged in `docs/SOURCES.md` and the **36 operational source identifiers** tracked in the release snapshot manifest (`reports/v1/dataset_v1.csv` and `reports/v1/sources_redistribution.csv`).

---

## 2. Master Reconciliation Table (41 Literature Entries vs. 36 Operational Sources)

| Literature Catalog # | Primary Dataset Name / Citation | Operational Source ID in CSV | Release Images | Status / Reconciliation Notes |
|:---:|---|---|---:|---|
| 1 | PlantVillage (Hughes & Salathé, 2015) | `plantvillage_legacy_baseline` | 41,747 | Active foundational baseline |
| 2 | Master Plant Disease Dataset (Tanniru, 2025) | `kaggle_pv2` | 5,744 | Active multi-crop aggregation mirror |
| 2c | Paddy Doctor Benchmark (Arjunan et al., 2022) | `paddy_doctor_kaggle` | 1,702 | Component of Master Dataset tracked as dedicated source |
| 3 | Cauliflower Smart Agriculture (Dumlao) | `mendeley` | (in 566) | Consolidated with Vegetable Leaf Disease into `mendeley` |
| 4 | Chilli Leaf Disease (Nirob et al., 2025) | `chilli_nirob` | 1,055 | Active verified primary chilli dataset |
| 5 | Corn/Maize Leaf Disease (Ghose) | `corn_kaggle` | 1,509 | Active public domain corn leaves |
| 6 | BrACoLD Coffee Dataset (Esgario et al.) | `coffee_kaggle` | 402 | Active Brazilian coffee benchmark |
| 7 | PlantDoc (Singh et al., IIT Mandi) | `scraped` / `unknown` | (in 36) | Selective ingestion for rare foliar classes |
| 8 | Garlic Leaf (Reza et al. / Fahimuzzman) | *(quarantined)* | 0 | **Quarantined in P-005**: Entire Garlic crop suite dropped |
| 9 | Ginger Leaf Dataset (Wong, TARUMT) | `ginger_research` | 6,960 | Active verified academic ginger benchmark |
| 10 | Ginger Bacterial Wilt (Yigezu et al.) | `ginger_research` | (in 6,960) | Consolidated with TARUMT ginger dataset |
| 11 | Lettuce Diseases (Jha) | `mendeley` / `unknown` | (in 566) | Sourced via Mendeley vegetable collection |
| 12 | Peach Leaf Disease (Farman et al.) | `peach_dataset` | 631 | Active peach foliar benchmark |
| 13 | Plum Leaf and Fruit (Nayeem et al.) | `plum_lab_mendeley` | 1,165 | Active laboratory plum specimens |
| 14 | Plum Leaf In-the-Wild (Khan F.) | `plum_lab_mendeley` / `plum_ronokhasan` | (in active) | Merged with companion plum cohorts |
| 15 | Potato Leaf Disease (Hossin) | `potato_kaggle` | 1,326 | Active potato leaf dataset |
| 16 | Wheat Leaf High-Resolution (Getch) | *(quarantined)* | 0 | **Quarantined in P-005**: Entire Wheat crop suite dropped |
| 17 | Wheat Leaf Disease (Khan A.) | *(quarantined)* | 0 | **Quarantined in P-005**: Entire Wheat crop suite dropped |
| 18 | Citrus Leaves (Sourabh) | `sourabh2001` | 817 | Active natural-background citrus leaves |
| 19 | Cucumber Disease (Kapadnis) | `sujay_kapadnis` | 304 | Active foliar cucumber dataset |
| 20 | Vegetable Leaf Disease (Ikteshad et al.) | `mendeley` | (in 566) | Active brassica and vegetable foliar classes |
| 21 | Cabbage Crop Diseases (Ayawli et al.) | `mendeley_cabbage` | 102 | Active cabbage foliar diseases |
| 22 | Bean Disease (Makerere AI Lab) | `therealoise_bean` | 873 | Active Ugandan in-situ bean diseases |
| 23 | Agri-Vision4 / Zucchini (Billah et al.) | `agrivision_zucchini` | 193 | Active zucchini foliar diseases |
| 24 | Strawberry Disease (Afzaal et al.) | `datasetninja` | 941 | Active strawberry foliar benchmark |
| 25 | PlantCity Cherry (Khan et al., 2025) | `plantcity` | (in 2,556) | Grouped under unified `plantcity` identifier |
| 26 | PlantCity Multi-Crop (Khan et al., 2025) | `plantcity` | (in 2,556) | Grouped under unified `plantcity` identifier |
| 27 | Lemon Leaf Disease / LLD (Al Amin) | `mendeley_citrus_lemon` | 255 | Active lemon foliar diseases |
| 28 | DiaMOS Plant Pear (Fenu & Malloci) | `diamos` | 956 | Active pear orchard foliar dataset |
| 29 | Rice Leafs Disease (Saputra) | `rice_lab` | 2,018 | Active laboratory rice leaves |
| 30 | Niphad Grape Leaf (Dharrao et al.) | `mendeley_grape_niphad` | 5,298 | Active vineyard grape leaf benchmark |
| 31 | Grape Disease Original (rm1000) | `kaggle_grape` | 395 | Active public domain grape specimens |
| 32 | Plum Leafs Field (Hasan) | `plum_ronokhasan` | 197 | Active European plum natural-background captures |
| 33 | Jamun / Java Plum (Bhowmik & Ahad) | `jamun_foliar` | 1,392 | Active Java plum foliar benchmark |
| 34 | Eggplant Disease (Kapadnis) | `eggplant_kaggle` | 867 | Active eggplant foliar diseases |
| 35 | Pepper Bell Leaf (Elvsava) | `mendeley_bell_pepper` | 1,554 | Active bell pepper foliar dataset |
| 36 | Soybean Multi-Class (Thorwat et al.) | `soybean_mendeley_kaggle` | (in 304) | Grouped with Mendeley soybean cohort |
| 37 | Soybean Disease (Bhujade) | `vaishali_soybean` | 474 | Active natural-background soybean dataset |
| 38 | Soybean Diseased Leaf (sivm205) | `soybean_mendeley_kaggle` | (in 304) | Grouped with Mendeley soybean cohort |
| 39 | Mango Leaf Disease (Shah) | `mango_mendeley` | 3,460 | Active public domain mango leaves |
| 40 | Guava Disease 4 Types (Dalvi) | `mendeley_guava` | (in 3,837) | Consolidated into unified guava cohort |
| 41 | Guava Leaf Disease (Hasan & Rahman) | `mendeley_guava` | (in 3,837) | Consolidated into unified guava cohort |

---

## 3. Operational Identifiers for Auxiliary / Pipeline Sources

The following 5 operational identifiers in `sources_redistribution.csv` correspond to specific ingestion and curation channels rather than single published literature papers:

| Operational Source ID | Release Images | Description & Ingestion Channel |
|---|---:|---|
| `syedzainmir_pear` | 1,717 | Community mirror upload of pear foliar diseases on Kaggle |
| `scraped_coffee` | 278 | Verified web-sourced coffee foliar images |
| `unknown` | 326 | Residual legacy specimens with unverified exact origin across Guava and Plum |
| `scraped` | 36 | Web-sourced single-specimen augmentations for rare classes (Cherry, Cabbage, Coffee, Radish) |
| `scraped_inaturalist` | 27 | Verified Wikimedia/iNaturalist specimens for Blueberry |

**Total Images Across All 36 Operational Sources:** 91,984
