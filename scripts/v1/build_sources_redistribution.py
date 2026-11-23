"""
Map sources from dataset_v1.csv to metadata and output reports/v1/sources_redistribution.csv.
"""
import pandas as pd
from pathlib import Path
import csv

ROOT = Path(__file__).resolve().parent.parent.parent

df = pd.read_csv(ROOT / "reports" / "v1" / "dataset_v1.csv")
counts = df["source"].value_counts().to_dict()

# Detailed metadata for each of the 36 sources in dataset_v1.csv
source_info = {
    "plantvillage_legacy_baseline": {
        "url_doi_citation": "Hughes & Salathe (2015), arXiv:1511.08060; https://github.com/spMohanty/PlantVillage-Dataset",
        "license": "CC BY-SA 4.0",
        "notes": "Foundational laboratory baseline across multiple crops; non-commercial compilation restriction conflict with CC BY-SA terms.",
    },
    "ginger_research": {
        "url_doi_citation": "Wong (2024), TARUMT; https://github.com/wongxinjie/ginger-leaf-disease",
        "license": "MIT",
        "notes": "Verified permissive academic source; flatbed and macro ginger leaves.",
    },
    "kaggle_pv2": {
        "url_doi_citation": "PlantVillage Kaggle Mirror / Master Plant Disease Dataset (Tanniru, 2025)",
        "license": "CC BY-SA 4.0",
        "notes": "Derived from PlantVillage and Kaggle mirrors; shares CC BY-SA terms.",
    },
    "mendeley_grape_niphad": {
        "url_doi_citation": "Dharrao et al. (2023), Mendeley Data, doi:10.17632/89t4pdzbpd.1",
        "license": "CC BY 4.0",
        "notes": "Niphad region vineyard grape leaves; laboratory and natural-background specimens.",
    },
    "mendeley_guava": {
        "url_doi_citation": "Hasan & Rahman (2023), Mendeley Data, doi:10.17632/95d8524k5y.1",
        "license": "CC BY 4.0",
        "notes": "Guava foliar disease dataset from Bangladesh.",
    },
    "mango_mendeley": {
        "url_doi_citation": "Shah et al. (2023), Mendeley Data / Kaggle, doi:10.17632/ggh6nhpbt7.1",
        "license": "CC0 1.0",
        "notes": "Public domain mango leaves; Algal leaf spot, Anthracnose, Die back, Cutting weevil.",
    },
    "plantcity": {
        "url_doi_citation": "Khan et al. (2025), Data in Brief, doi:10.1016/j.dib.2025.111245",
        "license": "ODbL 1.0",
        "notes": "PlantCity urban and orchard foliar dataset; Share-Alike open database terms.",
    },
    "rice_lab": {
        "url_doi_citation": "Saputra (2022), Kaggle Rice Leafs Disease / ResearchGate",
        "license": "Unspecified",
        "notes": "High-resolution laboratory rice leaves; research use only.",
    },
    "syedzainmir_pear": {
        "url_doi_citation": "Syed Zain Mir (2023), Kaggle Pear Leaf Diseases",
        "license": "Unspecified",
        "notes": "Kaggle user dump of pear disease images; unverified upstream provenance.",
    },
    "paddy_doctor_kaggle": {
        "url_doi_citation": "Arjunan et al. (2022), IEEE DataPort / Kaggle Paddy Doctor",
        "license": "CC BY 4.0",
        "notes": "Paddy Doctor natural-background benchmark subset retained after wide-angle pruning.",
    },
    "mendeley_bell_pepper": {
        "url_doi_citation": "Elvsava et al. (2023), Mendeley Data, doi:10.17632/w9drvtxg9g.1",
        "license": "CC BY 4.0",
        "notes": "Mendeley bell pepper leaf images; Bell Pepper and Chilli overlaps quarantined in P-001.",
    },
    "corn_kaggle": {
        "url_doi_citation": "Ghose (2021), Kaggle Corn/Maize Leaf Disease Dataset",
        "license": "CC0 1.0",
        "notes": "Public domain corn leaves; Common Rust, Gray Leaf Spot, Blight.",
    },
    "jamun_foliar": {
        "url_doi_citation": "Bhowmik & Ahad (2023), Mendeley Data, doi:10.17632/43d75vptz4.2",
        "license": "CC BY 4.0",
        "notes": "Syzygium cumini foliar disease benchmark from Bangladesh.",
    },
    "potato_kaggle": {
        "url_doi_citation": "Hossin (2022), Kaggle Potato Leaf Disease",
        "license": "Unspecified",
        "notes": "Kaggle community mirror; unverified upstream licensing.",
    },
    "plum_lab_mendeley": {
        "url_doi_citation": "Nayeem et al. (2023), Mendeley Data, doi:10.17632/67t8v9t6h6.1",
        "license": "CC BY 4.0",
        "notes": "Laboratory plum leaves; non-foliar fruit images quarantined in P-005.",
    },
    "chilli_nirob": {
        "url_doi_citation": "Nirob et al. (2025), Data in Brief / Kaggle, doi:10.1016/j.dib.2025.111422",
        "license": "CC BY 4.0",
        "notes": "Verified primary chilli dataset; Leaf Curl, Cercospora, Bacterial Spot.",
    },
    "diamos": {
        "url_doi_citation": "Fenu & Malloci (2021), Agronomy, doi:10.3390/agronomy11050934",
        "license": "CC BY 4.0",
        "notes": "DiaMOS Plant pear and fruit orchard in-situ captures.",
    },
    "datasetninja": {
        "url_doi_citation": "DatasetNinja / Supervisely Plant Disease Aggregation",
        "license": "CC BY 4.0",
        "notes": "Re-annotated foliar pathology splits.",
    },
    "therealoise_bean": {
        "url_doi_citation": "Makerere AI Lab / therealoise Bean Disease Dataset (Kaggle)",
        "license": "Unspecified",
        "notes": "In-situ natural-background bean disease images from Uganda; thumb crops preserved in test.",
    },
    "eggplant_kaggle": {
        "url_doi_citation": "Kapadnis et al. (2023), Kaggle Eggplant Disease Dataset",
        "license": "Unspecified",
        "notes": "Eggplant Little Leaf and Mosaic Virus; mixed Cercospora folder quarantined in P-005.",
    },
    "sourabh2001": {
        "url_doi_citation": "Sourabh (2022), Kaggle Citrus Leaves Dataset",
        "license": "Unspecified",
        "notes": "Citrus Black Spot, Canker, Greening, Melanose.",
    },
    "peach_dataset": {
        "url_doi_citation": "Farman et al. (2022), Mendeley Data, doi:10.17632/5h7p4xft82.1",
        "license": "CC BY 4.0",
        "notes": "Peach foliar pathology; Bacterial Spot, Peach leaf curl.",
    },
    "mendeley": {
        "url_doi_citation": "Prem Kumar E. (2025), Mendeley Data, doi:10.17632/tywbtsjrJV.1",
        "license": "CC BY 4.0",
        "notes": "Multi-crop disease specimens (Banana, Cauliflower, Groundnut, Radish).",
    },
    "vaishali_soybean": {
        "url_doi_citation": "Thorwat et al. (2022), Mendeley Data, doi:10.17632/m638k43y9v.1",
        "license": "CC BY 4.0",
        "notes": "Soybean foliar diseases from Maharashtra, India.",
    },
    "coffee_kaggle": {
        "url_doi_citation": "Esgario et al. (2020), BrACoLD Coffee Dataset, doi:10.1016/j.compag.2020.105437",
        "license": "CC BY 4.0",
        "notes": "Brazilian Coffee Leaf Disease dataset; Rust, Brown Eye Spot, Miner, Cercospora.",
    },
    "kaggle_grape": {
        "url_doi_citation": "rm1000 (2021), Kaggle Grape Disease Dataset",
        "license": "CC0 1.0",
        "notes": "Public domain grape leaves.",
    },
    "unknown": {
        "url_doi_citation": "Uncataloged historical legacy ingestion paths",
        "license": "Unspecified",
        "notes": "Unverified legacy paths; non-commercial research use only.",
    },
    "sujay_kapadnis": {
        "url_doi_citation": "Kapadnis (2023), Kaggle Cucumber Disease Dataset",
        "license": "Unspecified",
        "notes": "Cucumber Downy Mildew, Powdery Mildew, Healthy.",
    },
    "soybean_mendeley_kaggle": {
        "url_doi_citation": "Bhujade (2023), Kaggle Soybean Disease Mirror",
        "license": "Unspecified",
        "notes": "Kaggle mirror of Indian soybean farm leaves.",
    },
    "scraped_coffee": {
        "url_doi_citation": "Targeted agronomic extension search queries for coffee pathology",
        "license": "Unspecified",
        "notes": "Targeted web downloads; non-commercial research use only.",
    },
    "mendeley_citrus_lemon": {
        "url_doi_citation": "Al Amin (2023), Mendeley Data, doi:10.17632/bvrw7px54t.1",
        "license": "CC BY 4.0",
        "notes": "Lemon leaf diseases; Citrus canker, leaf miner, algal spot.",
    },
    "plum_ronokhasan": {
        "url_doi_citation": "Hasan (2023), Kaggle Plum Leafs Field Dataset",
        "license": "Unspecified",
        "notes": "European plum natural-background captures from Bangladesh.",
    },
    "agrivision_zucchini": {
        "url_doi_citation": "Billah et al. (2023), Agri-Vision4 / Mendeley Data, doi:10.17632/k35623m4t6.1",
        "license": "CC BY 4.0",
        "notes": "Zucchini foliar diseases; Yellow mosaic, Powdery mildew, Downy mildew.",
    },
    "mendeley_cabbage": {
        "url_doi_citation": "Ayawli et al. (2023), Mendeley Data, doi:10.17632/wzrhnw7t3t.1",
        "license": "CC BY 4.0",
        "notes": "Cabbage foliar diseases; Black rot, Alternaria leaf spot, Downy mildew.",
    },
    "scraped": {
        "url_doi_citation": "Manual agronomic extension searches for missing rare disease controls",
        "license": "Unspecified",
        "notes": "Curated rare leaf images; research use only.",
    },
    "scraped_inaturalist": {
        "url_doi_citation": "iNaturalist Research-Grade Observations (inaturalist.org)",
        "license": "CC BY-NC 4.0",
        "notes": "Research-grade community observations; strictly non-commercial.",
    },
}

out_csv = ROOT / "reports" / "v1" / "sources_redistribution.csv"

rows = []
total_images = 0
for src, count in counts.items():
    meta = source_info.get(src, {
        "url_doi_citation": "NOT VERIFIABLE",
        "license": "Unspecified",
        "notes": "Uncataloged source",
    })
    rows.append({
        "source_name": src,
        "url_doi_citation": meta["url_doi_citation"],
        "license": meta["license"],
        "redistributable": "",  # Empty column as explicitly required
        "release_snapshot_image_count": count,
        "notes": meta["notes"],
    })
    total_images += count

assert total_images == 91984, f"Expected 91984 total images, got {total_images}"

with open(out_csv, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=[
        "source_name",
        "url_doi_citation",
        "license",
        "redistributable",
        "release_snapshot_image_count",
        "notes",
    ])
    writer.writeheader()
    writer.writerows(rows)

print(f"Successfully generated {out_csv} with {len(rows)} sources totaling {total_images} images.")
