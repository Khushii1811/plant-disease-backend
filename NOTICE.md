# Third-Party Notices & Attribution

## Scope of Software License

The [MIT License](LICENSE) governing this repository applies strictly to the source code, API services, CLI utilities, test suites, and configuration files of the `plant-disease-backend` repository.

The MIT License **DOES NOT** cover or grant commercial rights to:
1. **Upstream Research Datasets & Benchmarks:** Aggregated training and evaluation data.
2. **Model Weights & Derived Parameters:** Binary checkpoints and feature representations derived from non-commercial or academic research datasets.
3. **Third-Party Research Assets:** External figures, documentation samples, and diagnostic evidence assets.

---

## 1. Upstream Research Datasets & Benchmarks

The machine learning models developed in this repository were trained and evaluated on aggregated foliar plant leaf disease datasets collected from independent academic research projects, open-science repositories (including Mendeley Data, Zenodo, and IEEE DataPort), and public agricultural archives.

- **Upstream Terms & Licenses:** Individual constituent datasets remain governed by their respective upstream licenses (including CC BY 4.0, CC BY-SA 4.0, CC0 1.0, ODbL 1.0, MIT, and academic non-commercial terms).
- **Single Source of Truth:** Full per-dataset provenance, publication citations, persistent DOIs, upstream licensing declarations, and redistribution permissions are cataloged in [docs/SOURCES.md](docs/SOURCES.md) and machine-readable in [reports/v1/sources_redistribution.csv](reports/v1/sources_redistribution.csv).
- **No Raw Image Redistribution:** In compliance with copyright terms and compilation restrictions, raw leaf pathology images are strictly not redistributed within this repository.

---

## 2. Model Weights & Derived Parameters

- **License:** Model weights, calibration matrices, and derived parameters are released under the [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License (CC BY-NC-SA 4.0)](https://creativecommons.org/licenses/by-nc-sa/4.0/).
- **Non-Commercial Restriction:** Because training data incorporates components with non-commercial terms or unverified upstream web collection rights, the model weights are provided exclusively for academic research, education, and non-commercial evaluation. They are not licensed for commercial deployment.
- **Further Details:** See [docs/DATASET_LICENSE.md](docs/DATASET_LICENSE.md) and [models/v1/README.md](models/v1/README.md) for full licensing terms, checksum verifications, and download instructions.

---

## 3. Visual Assets & Documentation Evidence

- **Permissive Visual Evidence:** Photographic evidence specimens retained in [docs/assets/p005/](docs/assets/p005/) originate exclusively from verified permissive repositories (Mendeley Data CC BY 4.0 and CC0 1.0) and are attributed to their source publications.
- **Diagnostic Pair Figures:** Figures derived from the Jamun foliar leaf dataset (`reports/v1/figures/jamun_all_pairs_*.png`) are distributed under the Creative Commons Attribution 4.0 International (CC BY 4.0) license; credited to Bhowmik et al. (2023), Mendeley Data.
- **Asset Clearance Tracking:** Tracking of asset clearance statuses and visual placeholders is maintained in [docs/RELEASE_CHECKLIST.md](docs/RELEASE_CHECKLIST.md).
