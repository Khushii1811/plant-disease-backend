# Release Checklist (`RELEASE_CHECKLIST.md`)

This checklist documents mandatory pre-flight verification items before public release and repository publishing.

---

## Pre-Flight Audit & Verification Checklist

- [x] **Model Weights SHA-256 Verification:**  
  Model v1.0 weights file verified at `3bb5785efa957a5fd4eb9d071fa92ff57adbef9788275a810e9cce99cf016dcb` in `models/v1/model_dualhead_convnext_tiny.pth`. Bundle loader passes with 0 warnings.

- [x] **Clean Test Split Parity ($N=9,279$):**  
  Test directory `data/processed/test/` verified physically identical in file count ($N=9,279$) and byte-for-byte SHA-256 hash sets to `reports/v1/dataset_v1.csv` test split.

- [x] **Patch P-007 Execution & Quarantine:**  
  Patch P-007 executed. All 181 near-duplicate test leakage frames quarantined into `data/raw/quarantine_test_leakage_twins/test/`. Move log (`data/patches/P-007_test_leakage_quarantine_PLAN.csv`), log file (`reports/v1/removed_p007_images.csv`), and restore script (`data/patches/restore_P-007.py`) verified.

- [x] **Data Lineage Documentation (Stages S1–S4):**  
  Data lineage formally documented in `reports/v1/lineage.json` and rendered between automated markers in `docs/DATASET_CARD.md` and `models/v1/model_card.md` via `scripts/v1/render_lineage_md.py`.

- [x] **Release Snapshot Twin Check:**  
  Full-dataset twin audit executed on 91,984 active images (`reports/v1/twin_check.json`). Confirmed 0 exact SHA-256 duplicates, 0 cross-split test twin pairs with train or val ($d \le 4$). 260 cross-split pairs identified between train and val (affecting 162 val images).

- [ ] **Redistribution Rights Clearance:**  
  `reports/v1/sources_redistribution.csv` generated across all 36 sources (91,984 images). Legal clearance of individual redistributability flags remains pending; raw images are strictly not redistributed.
  - **Website Wiki Sample Images Audit (X7):** Out of 177 condition sample images, 111 carry verified permissive licenses (CC BY-SA 4.0, CC BY 4.0, CC0 1.0, ODbL 1.0, MIT). The remaining 66 images lack permissive commercial clearance (including 31 plantseg and 8 PlantDoc search-engine classes, and 27 previously withdrawn classes) and have been replaced with neutral placeholders (*"Image not available: licence unverified"*) in `plant-disease-frontend/assets/wiki_samples/`:
    1. `bean_bean_angular_leaf_spot.webp` (Source: `therealoise_bean` - Unspecified)
    2. `bean_healthy.webp` (Source: `therealoise_bean` - Unspecified)
    3. `blueberry_blueberry_rust.webp` (Source: `scraped_inaturalist` - CC BY-NC 4.0)
    4. `citrus_alternaria_leaf_spot.webp` (Source: `sourabh2001` - Unspecified)
    5. `citrus_healthy.webp` (Source: `sourabh2001` - Unspecified)
    6. `coffee_coffee_leaf_rust.webp` (Source: `scraped_coffee` - Unspecified)
    7. `cucumber_healthy.webp` (Source: `sujay_kapadnis` - Unspecified)
    8. `eggplant_healthy.webp` (Source: `eggplant_kaggle` - Unspecified)
    9. `eggplant_little_leaf.webp` (Source: `eggplant_kaggle` - Unspecified)
    10. `eggplant_mosaic_virus.webp` (Source: `eggplant_kaggle` - Unspecified)
    11. `eggplant_white_mold.webp` (Source: `eggplant_kaggle` - Unspecified)
    12. `eggplant_wilt.webp` (Source: `eggplant_kaggle` - Unspecified)
    13. `paddy_bacterial_leaf_blight.webp` (Source: `rice_lab` - Unspecified)
    14. `paddy_blast.webp` (Source: `rice_lab` - Unspecified)
    15. `paddy_brown_spot.webp` (Source: `rice_lab` - Unspecified)
    16. `paddy_healthy.webp` (Source: `rice_lab` - Unspecified)
    17. `paddy_leaf_scald.webp` (Source: `rice_lab` - Unspecified)
    18. `paddy_narrow_brown_spot.webp` (Source: `rice_lab` - Unspecified)
    19. `pear_pear_slug_damage.webp` (Source: `syedzainmir_pear` - Unspecified)
    20. `plum_plum_weevil.webp` (Source: `plum_ronokhasan` - Unspecified)
    21. `potato_early_blight.webp` (Source: `potato_kaggle` - Unspecified)
    22. `potato_healthy.webp` (Source: `potato_kaggle` - Unspecified)
    23. `potato_pest_damage.webp` (Source: `potato_kaggle` - Unspecified)
    24. `potato_potato_virus.webp` (Source: `potato_kaggle` - Unspecified)
    25. `soybean_brown_spot.webp` (Source: `soybean_mendeley_kaggle` - Unspecified)
    26. `soybean_powdery_mildew.webp` (Source: `soybean_mendeley_kaggle` - Unspecified)
    27. `soybean_yellow_mosaic.webp` (Source: `soybean_mendeley_kaggle` - Unspecified)
  - **Hero Background (`hero-bg.jpg`):** Provenance and upstream license are NOT VERIFIED. Withdrawn and replaced with a procedural CSS gradient.

- [ ] **Patch P-008 Execution (Validation Split Twin Quarantine):**  
  Dry-run removal plan for 162 validation images with near-duplicate train twins generated at `reports/v1/p008_plan_DRYRUN.csv`. Execution pending user decision.

- [ ] **Independent Field Benchmark:**  
  No independent field evaluation has been conducted to date. All reported metrics represent held-out in-distribution evaluation.

---

## TODO-BEFORE-PUBLISH

- [ ] **Hugging Face Model Upload (`<HF_LINK>`):**  
  Upload the official Model v1.0 weights (`models/v1/model_dualhead_convnext_tiny.pth`, SHA-256: `3bb5785efa957a5fd4eb9d071fa92ff57adbef9788275a810e9cce99cf016dcb`) and model bundle artifacts to the Hugging Face Model Hub. Replace the literal placeholder `<HF_LINK>` in `README.md` with the permanent URL.

- [ ] **Docker Build & Health Probe Verification:**  
  Start the Docker daemon and build the production container image:
  ```bash
  docker build -t plant-disease-backend:v1.0.0 .
  docker run --rm -p 8000:8000 plant-disease-backend:v1.0.0
  curl http://localhost:8000/api/v1/ready
  ```
  Verify non-root user execution (`appuser`) and healthy probe status (`{"status":"ready"}`).

- [ ] **Dependency Security Audit (`pip-audit`):**  
  Execute dependency vulnerability auditing on locked environment dependencies:
  ```bash
  uv run pip-audit
  ```
  Verify zero high or critical CVE vulnerabilities.

- [ ] **Secrets & Leak Detection Scan (`gitleaks`):**  
  Run static secret detection across the full git commit history:
  ```bash
  gitleaks detect --source . -v
  ```
  Verify that zero private keys, API tokens, or secrets exist across all historical commits.

- [ ] **Release Date Filling (`date-released`):**  
  In `CITATION.cff`, replace the literal string `"YYYY-MM-DD"` with the actual calendar release date at the moment of git tagging:
  ```yaml
  date-released: "2026-XX-XX"
  ```

- [ ] **Final Repository Hygiene Grep:**  
  Execute comprehensive regex scan across all tracked files to verify zero forbidden words, local workstation absolute paths, or personal credentials:
  ```powershell
  git grep -n -i -e "E:\" -e "C:\Users" -e "gemini_key" -- .
  ```
