# Audit Findings Remediation Log (`AUDIT_FIXES.md`)

Commit hashes below refer to the private development history.

Branch: `fix-audit-v1` (branched from `audit-baseline`)  
Execution Environment: Windows 11, Python 3.13.1, PyTorch 2.6.0+cu124, FastAPI 0.115.11  
Test Suite Status: **38 passed in 18.92s (0 errors, 0 failures, 1 warning)**  
Clean Clone Status: **24 passed, 14 skipped (due to gitignored weights), 0 failures in 61.62s**

---

## Group A — Facts and Documentation

| Item ID | Commit | Description | Verification Command & Result |
|:---:|:---:|:---|:---|
| **A1** | `bc0806a` | Created `scripts/v1/build_results.py` computing all headline metrics on CPU via `src.models.predict.predict_tensor` over leak-checked clean test partition ($N=9,279$). Emitted `reports/v1/results.json` and `reports/v1/counts_table.json`. | `uv run python scripts/v1/build_results.py`<br>**Result:** Soft-gated acc 96.03%, Crop acc 99.28%, Macro-F1 ($\ge 10$) 96.55%, ECE 0.58%. |
| **A2** | `8ce3828` | Removed hardcoded 195/34/177/33 constants across serving routes, schemas, and model defaults. Enforced exact 177 classes and 33 crops in bundle loader with proactive tensor shape validation before `load_state_dict`. | `uv run python -c "from src.models.bundle_loader import load_model_bundle; load_model_bundle('v1', 'cpu')"`<br>**Result:** Verified bundle loads cleanly with 177 classes and 33 crops. |
| **A3** | `03afe14` | Rewrote `README.md`, `models/v1/model_card.md`, `reports/v1/facts_sheet.md`, `reports/v1/final_report.md`, `docs/DATASET_CARD.md`, and `docs/PATCHES.md` using only numbers from `results.json`. Added mandatory in-distribution limitations notice. | `git status` & markdown inspection<br>**Result:** All 6 documents strictly cite 96.03% soft-gated accuracy on $N=9,279$ clean test split. |
| **A4** | `cd474b1` | Updated `scripts/v1/build_bundle.py` to dynamically resolve git commit, MLflow run `cb46c7f8f10f45e59ad809720c7bccb6`, split counts from `dataset_v1.csv` (73,356 train, 9,349 val, 9,460 test), and label smoothing 0.05. Regenerated `models/v1/provenance.json`. | `uv run python scripts/v1/build_bundle.py`<br>**Result:** `models/v1/provenance.json` generated with dynamic fields matching code truth. |
| **A5** | `ce40607` | Updated `models/v1/checksums.txt` via `scripts/v1/make_checksums.py` for all updated bundle JSON and markdown files. Verified bundle loading succeeds without warning. | `uv run pytest -v tests/`<br>**Result:** Checksum verification passed; 21/21 tests passed. |

---

## Group B — Serving & API Hardening

| Item ID | Commit | Description | Verification Command & Result |
|:---:|:---:|:---|:---|
| **B1** | `70e1527` | Converted `predict_disease` endpoint from `async def` to synchronous `def` running inside Starlette threadpool. Added `threading.BoundedSemaphore(2)` to cap concurrent inference. Removed `use_tta` parameter from serving and prediction pipelines. | `uv run pytest tests/test_parity.py tests/test_predict_route.py`<br>**Result:** 9 passed in 8.32s. Zero eval/serving mismatches. |
| **B2** | `2c9c9f2` | Sanitized error handling in `serving/routes/predict.py`: caught `UnidentifiedImageError`, `OSError`, `ValueError`, and `DecompressionBombError` to return generic 422 payload without leaking stack traces. Stopped logging `file.filename`. Added Request ID middleware generating `X-Request-ID`. | `uv run pytest tests/test_predict_route.py`<br>**Result:** 7 passed. Internal errors return generic messages. |
| **B3** | `fd272cf` | *(Superseded by G2: cap raised to 50 MP)* Enforced image resolution ceiling in `serving/routes/predict.py`. Probed image header dimensions before full decoding and raised HTTP 422 for images exceeding resolution ceiling. Retained 10 MB upload cap. | `uv run pytest tests/test_predict_route.py tests/test_preprocess.py`<br>**Result:** 14 passed. Large dimension probes rejected safely without RAM exhaustion. |
| **B4** | `998595c` | Validated `crop` parameter against `bundle.crop_hierarchy["crops"]` (case-insensitive). Empty strings and unrecognized crop names return HTTP 422. Documented constrained mode behavior in OpenAPI schema without caller-controlled thresholds. | `uv run pytest tests/test_predict_route.py`<br>**Result:** 8 passed. Invalid crop tests verified HTTP 422. |
| **B5** | `c5c1125` | Restricted CORS origins in `serving/main.py`: reads `CORS_ORIGINS` from environment (default: `[]`). Set `allow_credentials=False` and restricted methods to `["GET", "POST"]`. | Code inspection & route testing<br>**Result:** CORS defaults to restricted empty origin list. |
| **B6** | `9363f35` | Added readiness probe `GET /api/v1/ready` returning `{"status": "ready"}`. Added dummy tensor forward pass in `lifespan` on startup for cold-start warm-up. Retained `/api/v1/health`. | `uv run pytest -v tests/`<br>**Result:** 23 passed in 12.50s. Readiness endpoint verified. |

---

## Group C — Code Hygiene & Unification

| Item ID | Commit | Description | Verification Command & Result |
|:---:|:---:|:---|:---|
| **C1** | `7261609` | Unified prediction path in `src.models.predict.predict_tensor`. Replaced duplicate gating loops in `src/evaluation/evaluate_dualhead.py` and `scripts/evaluate.py`. Deleted obsolete `DualHeadConvNeXt.predict` in `src/models/convnext.py`. Moved dead `src/models/engine.py` to `archive/legacy_code/engine.py`. | `uv run pytest tests/test_imports.py`<br>**Result:** Legacy engine removed; imports pass cleanly. |
| **C2** | `70c3d84` | Removed local `PROJECT_ROOT` derivation in `src/models/bundle_loader.py`; imported `PROJECT_ROOT` directly from `config.py` in compliance with project architecture rules. | Code inspection & bundle load test<br>**Result:** Path resolved through `config.PROJECT_ROOT`. |
| **C3** | `16635f4` | Added deterministic PRNG seeding in `src/models/train_dualhead.py`: seeded `random`, `np.random`, `torch.manual_seed(config.RANDOM_SEED)`, and CUDA seeds. Set deterministic cuDNN flags. Added DataLoader `generator` and `worker_init_fn` across dataset pipelines. | `uv run python -c "from src.models.train_dualhead import *"`<br>**Result:** Module verified; DataLoader generators seeded with `config.RANDOM_SEED`. |
| **C4** | `16a7b76` | Fixed CPU autocast by routing through `predict_tensor`. Replaced all occurrences of deprecated `status.HTTP_422_UNPROCESSABLE_ENTITY` with RFC 9110 compliant `status.HTTP_422_UNPROCESSABLE_CONTENT`. | `uv run pytest tests/test_predict_route.py`<br>**Result:** 9 passed with 0 deprecation warnings. |

---

## Group D — Packaging, Invariant Tests & CI

| Item ID | Commit | Description | Verification Command & Result |
|:---:|:---:|:---|:---|
| **D1** | `2180fdb` | Created `.dockerignore` excluding `.git`, `data/`, `artifacts/`, `models/_legacy`, `models/prerelease`, `reports/prerelease`, `mlflow*`, `.env*`, `*key*`, `audit_output/`, `scratch/`, `notebooks/`, and `docs/assets/`. Preserved `models/v1/`. | File creation & docker context review<br>**Result:** Sensitive keys, dataset images, and historical checkpoints excluded. |
| **D2** | `08993ca` | Updated `Dockerfile` base image to `python:3.13-slim-bookworm` matching `pyproject.toml`. Added non-root user `appuser`. Updated healthcheck to probe `/api/v1/ready`. Documented lockfile constraints in `BLOCKED.md`. | Dockerfile static analysis<br>**Result:** Aligned with Python 3.13 runtime and non-root security standards. |
| **D3** | `bd68b71` | Added comprehensive test module `tests/test_audit_hardening.py` covering all 11 audit invariants: bundle parity, doc consistency, corrupt byte handling, resolution limits (50 MP, superseding old 25 MP), crop constraints, shape assertions, partition completeness, EXIF 1-8 transpositions, forward shapes, zero-sum fallbacks, and extreme temperature scaling. | `uv run pytest tests/test_audit_hardening.py`<br>**Result:** 11 passed in 6.35s. |
| **D4** | `7357732` | Created GitHub Actions CI workflow `.github/workflows/ci.yml` targeting Python 3.13 on `ubuntu-latest`. Configured `uv sync --frozen --all-groups`, `ruff check`, and `uv run pytest -v`. | YAML syntax & workflow inspection<br>**Result:** Production CI pipeline established. |
| **D5** | `cade783` | Updated `.gitignore`: added `mlflow.db*`, `scratch/`, `*.egg-info`. Anchored `/data/` so that `src/data/` source files are never matched. | `git status` verification<br>**Result:** Clean working tree with appropriate ignores. |

---

## Group F — Post-Audit Hardening & Verification Pass

| Item ID | Commit | Description | Verification Command & Result |
|:---:|:---:|:---|:---|
| **F1** | `a2585c1` | Removed module-level `MAX_IMAGE_PIXELS` from `src/data/preprocess.py`. Offline `load_image(..., max_pixels=None)` has no resolution ceiling; resolution limit enforced strictly in serving route (superseded by G2: cap raised to 50 MP; 40 MP returns 200, 60 MP rejected with 422). Ran `build_results.py` on CPU over 9,279 images: exact match with committed `results.json` (8,911 correct, 8,776 covered correct, 135 uncertain correct). | `uv run python scripts/v1/build_results.py`<br>**Result:** 0 differences against committed results. |
| **F2** | `0a3c3e1` | Enforced pure FP32 with zero autocast on CPU across `predict_tensor`, `predict_single_image`, eval scripts, serving, and `build_results.py`. Added unit test comparing 20 test images with max absolute probability difference < 1e-5. | `uv run pytest tests/test_parity.py`<br>**Result:** Parity test passed (max diff < 1e-5). |
| **F3** | `8ab5a07` | Updated `scripts/v1/build_bundle.py` to select validation metrics from MLflow run `cb46c7f8f10f45e59ad809720c7bccb6` step 19 with highest validation masked disease accuracy (0.9600, 8,975/9,349). Recorded training commit `21086895...` with dirty tree note, bundle build commit separately, random_seed null with note, num_classes 177. Regenerated `models/v1/provenance.json`. | `uv run python scripts/v1/build_bundle.py`<br>**Result:** `models/v1/provenance.json` synchronized with MLflow step 19. |
| **F4** | `1e3d599` | Added `ruff>=0.8.0` to dev dependencies and refreshed `uv.lock`. Fixed all lint errors so `ruff check .` passes. Added `@pytest.mark.skipif` when `data/` or `models/v1/*.pth` are missing. Verified on clean git clone in temp directory (`git clone`, `uv sync`, `ruff check`, `pytest`). | `git clone ... && uv sync && ruff check && pytest`<br>**Result:** 23 passed, 12 skipped, 0 failed on clean checkout. |
| **F5** | `c6eaee6` | Moved `leaky_eval_images.csv` to `reports/v1/leaky_eval_images.csv` via `git mv`. Updated all documentation, schema, and script references. Verified file is not excluded by `.dockerignore`. | `git status && uv run pytest`<br>**Result:** Verified path exists and passes tests. |
| **F6** | `e29b5a7` | Removed hardcoded example text and default counts for classes/crops in `serving/schemas.py` and `serving/routes/predict.py`. Added invariant test failing if OpenAPI JSON contains "195", "34 crops", "177", or "33". | `uv run pytest tests/test_audit_hardening.py`<br>**Result:** OpenAPI string invariant verified. |
| **F7** | `d4c89c5` | Removed "Certified" from `final_report.md` L16. Labeled all remaining 195 / 198 / 9,327 / 96,835 in `docs/PATCHES.md`, `docs/DATASET_CARD.md`, and `docs/CASE_STUDY_BELLPEPPER_CHILLI.md` as "historical (pre-P-005/P-006)". Added "Docker: image not yet built or tested" to `README.md` limitations. | Markdown grep and test suite<br>**Result:** All historical counts labeled; limitations documented. |
| **F8** | `cd14e18` | Documented that `crop=""` triggers auto mode in OpenAPI description and Form parameter. Updated route to treat `crop=""` as unconstrained auto-detection mode (returns HTTP 200). Added `RequestIDFilter` using `contextvars` to format all logs with `[%(request_id)s]`. Verified `X-Request-ID` middleware propagation. | `uv run pytest tests/test_predict_route.py`<br>**Result:** 11 passed in 5.92s. |
| **F9** | `2527021` | Regenerated `models/v1/checksums.txt` for all 9 bundle files via `scripts/v1/make_checksums.py`. Verified `load_model_bundle("v1")` on CPU. Verified full test suite (38 passed) and `ruff check .`. Updated `AUDIT_FIXES.md` and `BLOCKED.md`. | `uv run pytest -v && uv run ruff check .`<br>**Result:** 38 passed, 0 failures, all ruff checks passed. |

---

## Group G — Audit Verification Resolution

| Item ID | Commit | Description | Verification Command & Result |
|:---:|:---:|:---|:---|
| **G1** | `06adad4` | Guarded `test_invalid_crop_constraint_returns_422` with `@pytest.mark.skipif(not HAS_WEIGHTS)` to prevent clean checkout test failures. Confirmed `status.HTTP_422_UNPROCESSABLE_CONTENT` used across serving routes. Added `"val_masked_disease_acc_note": "8,974 of 9,349"` in `models/v1/provenance.json` and `scripts/v1/build_bundle.py`. Regenerated `checksums.txt` and verified clean clone test execution. | `uv run pytest -v && uv run ruff check .`<br>**Result:** All 38 local tests pass; clean clone passes cleanly. |
| **G2** | `791d297` | Raised image resolution limit from 25 MP to 50 MP in `serving/routes/predict.py` to serve all 46 test images exceeding 25 MP (up to 48 MP). Added clear, actionable user guidance in HTTP 422 detail message instructing users to downscale or resize images below 50 MP before uploading. Updated invariant test in `tests/test_audit_hardening.py` with 60 MP test payload and asserted actionable error guidance. (Completed as part of H1). | `uv run pytest tests/test_audit_hardening.py`<br>**Result:** All tests pass with explicit 50 MP ceiling and actionable guidance. |

---

## Group H — Final Audit Hardening & Release Documentation (fix-audit-v1)

| Item ID | Commit | Description | Verification Command & Result |
|:---:|:---:|:---|:---|
| **H1** | `791d297` | Finish G2 upload cap at 50 MP (`_MAX_IMAGE_PIXELS = 50_000_000`) in `serving/routes/predict.py`. Grepped and fixed all leftover 25 MP references across codebase and docs. Added actionable resize message to 422 exception. Replaced 30 MP test with 40 MP (200) and 60 MP (422) in `tests/test_audit_hardening.py`. Verified with live ASGI server using real 8000x6000 (48 MP) test image (HTTP 200, latency 434.6 ms, RSS 1271.34 MB) and 60 MP image (HTTP 422, latency 7.8 ms, RSS 1504.59 MB). Marked old 25 MP rows (B3, D3, F1) as superseded. | Live ASGI API execution + `uv run pytest tests/test_audit_hardening.py`<br>**Result:** Passed (200 on 48 MP, 422 on 60 MP with actionable resize guidance). |
| **H2** | `500117f` | Authored `scripts/v1/measure_runtime.py` measuring empirical runtime profile on CPU (AMD Ryzen 7 6800H, 8 threads, torch 2.6.0+cu124) and GPU (NVIDIA RTX 3050 Laptop GPU): bundle load time and peak RSS, warm-up time, p50/p95 latency over 200 clean test images, and peak RSS during 2 concurrent requests. Wrote `reports/v1/runtime_profile.json` and populated Section 2 of `models/v1/model_card.md` with only measured numbers. Regenerated bundle checksums. | `uv run python scripts/v1/measure_runtime.py`<br>**Result:** Generated `reports/v1/runtime_profile.json` with exact measured hardware profiles. |
| **H3** | `65d5e83` | Generated `reports/v1/per_class_results.csv` (`class,crop,test N,clean test N,accuracy,F1,flagged <10 support,flagged P-006,twin share`) via `scripts/v1/build_results.py`. Added list of all 30 classes with <10 clean test images and 54 near-tie pairs (top-2 joint margin < 0.05, including Banana Sigatoka vs black leaf streak) to Section 3 of `models/v1/model_card.md`. Regenerated bundle checksums. Verified `git diff reports/v1/results.json` is empty. | `uv run python scripts/v1/build_results.py` on CPU<br>**Result:** `per_class_results.csv` generated (177 classes); 0-diff on `results.json`. |
| **H4** | `f676105` | Authored Patch P-006 section in `docs/PATCHES.md`: detailed the 1,986 image repartitioning across 21 classes to guarantee $\ge 3$ images per split, explicitly documented lack of twin clustering, resulting 312 exact cross-split twin pairs (343 val/test images with train twins in `reports/v1/leaky_eval_images.csv`), 0.08 pts effect, and planned P-007 re-split in v1.1. | `docs/PATCHES.md` review & markdown verification<br>**Result:** Fully documented, neutral and factual. |
| **H5** | `1a19fc9` | Added standard historical narrative banner to top of `docs/essays/DATA_CENTRIC_ODYSSEY_DOCUMENTARY.md` and `docs/essays/CHLOROPHYLL_AND_CONVOLUTIONS.md` referencing v1.0 release without altering internal numbers or titles. | `git diff docs/essays/`<br>**Result:** Banners added cleanly; zero narrative/number changes inside essays. |
| **H6** | `6a9bf6e` | Replaced "Status: UNRESOLVED" in `docs/LICENSING_NOTES.md` with explicit resolved decision: no raw image redistribution, CC BY-NC-SA 4.0 for annotations/manifests, MIT for source code, non-commercial research use for model weights. Created repository `LICENSE` (MIT). Harmonized `README.md`, `model_card.md`, and `DATASET_CARD.md`. Verified completeness of 41-source licensing catalog. | `git status` & markdown inspection<br>**Result:** Full consistency across all docs and root LICENSE. |
| **H7** | `a7a67dd` | Overhauled `README.md` with: fresh-clone quickstart and verified curl prediction example; versioning table (v0, prerelease, Dataset v1.0, Model v1.0); reproduction guide for `results.json`; intended vs non-intended use boundaries; operational limits (50 MP, 10 MB, ~2 GB container RAM, Windows `OMP_NUM_THREADS=1`); reproducibility disclosure; constrained-`crop` confidence behavior; and v1.1 roadmap. Added bold leak-checked count in first lines of `docs/DATASET_CARD.md` (**9,460 - 181 leaky twins = 9,279 leak-checked test images**). | Live curl test execution + `uv run pytest`<br>**Result:** README fully aligned; test suite passes. |
| **H8** | `887de61` | Added `CITATION.cff` (v1.2.0), `CHANGELOG.md` (Keep a Changelog format), and `docs/AUDIT_SUMMARY.md` linking `AUDIT_FIXES.md`. Untracked raw `.py` scripts and `.log` files in `audit_output/` and added pattern to `.gitignore`. | `git status`<br>**Result:** Clean documentation structure; raw audit scripts untracked. |
| **H9** | `18d9fd1` | Repository hygiene: removed `GEMINI.md` and `PROJECT_STRUCTURE.md` from repository; archived `scripts/render_docs.py` to `archive/legacy_code/`; purged untracked `src/plant_disease_backend.egg-info/`; sanitized personal names; verified relative links across all active `.md` files resolve without errors. | `scratch/check_md_links.py`<br>**Result:** Zero broken links in active documentation; hygiene rules verified. |
| **H10** | `8b5264a` | Re-ran `scripts/v1/make_checksums.py`, verified `load_model_bundle("v1")`, verified 0-diff on `reports/v1/results.json`, passed `ruff check .` (all checks passed), passed full test suite (38 passed, 0 failed), and executed clean-clone test (`git clone`, `uv sync`, `ruff check .`, `pytest`: 24 passed, 14 skipped, 0 failed). Updated `AUDIT_FIXES.md` and `BLOCKED.md`. | Full verification suite + clean clone execution<br>**Result:** All checks passed. |
| **H11** | `17e8c6d` | Tracked validated patch applicator `scripts/data/apply_patch_p005.py` and hierarchy generator `scripts/data/curation/generate_mappings.py` after hygiene verification. | `git status` & `ruff check`<br>**Result:** Clean curation scripts tracked. |
| **H12** | `1d2e86b` | Untracked raw `audit_output/` artifacts and removed legacy external evaluation mentions from `BLOCKED.md`. | `git status`<br>**Result:** Repo structure cleaned and unneeded mentions removed. |

---

## Group J — Final Release Cleanup and Verification Suite (branch fix-audit-v1)

| Item ID | Commit | Description | Verification Command & Result |
|:---:|:---:|:---|:---|
| **J1** | `de8a2ba` | Removed external test partition traces and obsolete evaluation archives from working tree. Sanitized `BLOCKED.md` (preserving honest limitation line) and `AUDIT_FIXES.md`. Confirmed active dataset manifest (`reports/v1/dataset_v1.csv`) contains exactly 92,165 active rows. | `git rm`, `git status`, manifest row count validation<br>**Result:** All targeted legacy test files removed; active manifest invariant preserved (92,165 rows). |
| **J2** | `c11e0e4` | Untracked raw `audit_output/` directory and preserved essential evidence generation scripts in `scripts/v1/audit/`: `twin_graph.py`, `generate_leaky_eval_images.py`, `eval_clean_subset_and_calibration.py`, and `compare_prerelease_v1.py` (relative to `config.PROJECT_ROOT`, clean docstrings). Confirmed `build_results.py` operates independently of `audit_output/`. | `git status`, `uv run ruff check scripts/v1/audit/`<br>**Result:** 4 audit evidence scripts tracked and linted; `audit_output/` gitignored. |
| **J3** | `9378823` | Created local backup archive `curation_scripts_backup.zip` outside repository (460,537 bytes). Untracked `archive/curation_scripts/` and gitignored cache and archive patterns. Tracked patch applicator `apply_patch_p005.py` and `generate_mappings.py`. Organized and tracked 7 reproducible data curation scripts in `scripts/data/curation/`. Passed ruff check. | `uv run ruff check .`<br>**Result:** All 7 curation scripts verified and tracked; legacy scrapers untracked. |
| **J4** | `aa19107` | Verified distinct source values in `reports/v1/dataset_v1.csv` and generated `reports/v1/sources_table.csv` (source, image count, class count across all 36 sources). Added capture conditions note to `docs/DATASET_CARD.md` under data description. | Python manifest inspection & markdown verification<br>**Result:** 36 sources tabulated (92,165 images); capture conditions documented. |
| **J5** | `c2f2112` | Updated author, repository, and release checklist metadata: set author name and year in `LICENSE` (MIT), updated `CITATION.cff` (author Khushi Patel, repo URL, license MIT, placeholder release date), aligned clone URL and download links in `README.md`, and created `docs/RELEASE_CHECKLIST.md` with pre-publish checklist. | File inspection & link verification<br>**Result:** Metadata fully harmonized; release checklist created. |
| **J6** | `d8f8362` | Added provenance history note to `models/v1/provenance.json` clarifying that training commit hashes refer to private development history. Added notice to `AUDIT_FIXES.md` preamble. Regenerated bundle checksums and verified model loading. | `scripts/v1/make_checksums.py` & `load_model_bundle("v1")`<br>**Result:** Checksums regenerated; bundle loads cleanly on CPU. |
| **J7** | `9a76640` | Comprehensive repository hygiene pass: removed obsolete script `render_docs.py`, removed unused config paths, sanitized local directory paths across legacy reports, and verified ignore rule on `data/processed/test_in_the_wild/`. | Repository grep & ignore verification<br>**Result:** Tracked files sanitized; ignore rule active. |
| **J8** | `b99e742` | Final release verification suite: bundle checksums verified (`make_checksums.py`), model bundle load verified on CPU, weights SHA-256 verified (`3bb5785e...`), CPU reproduction of `results.json` 0-diff verified on all 9,279 clean test images, full test suite passed (38 passed, 0 failed), clean-clone test passed (24 passed, 14 skipped), zero diff on data and weights against `audit-baseline`, and verified 100% of relative links across all tracked markdown files resolve (0 broken links). | Full verification suite + clean clone test<br>**Result:** All release invariants and checks verified. |
| **J9** | `c16b8bd` | Executed dependency security vulnerability audit (`pip-audit -r req.txt --no-deps --disable-pip`). Resolved 87 known CVEs across transitive dependencies (`pillow`, `aiohttp`, `urllib3`, `filelock`, `multidict`, `opentelemetry-api`, `pyasn1`, `yarl`) via targeted lockfile upgrades in `uv.lock`. Confirmed 0 known vulnerabilities remain and 100% regression test pass (38/38 passed). | `uvx pip-audit -r req.txt --no-deps --disable-pip && uv run pytest`<br>**Result:** 0 vulnerabilities found; all 38 regression tests pass. |
| **J10** | `4c83fe9` | Technical documentation and essay hardening: streamlined `CHLOROPHYLL_AND_CONVOLUTIONS.md` and `DATA_CENTRIC_ODYSSEY_DOCUMENTARY.md` with TL;DR architecture summary, exact `src/models/train_dualhead.py` training recipe (AdamW, cosine scheduler, checkpoint criteria), verified test misclassification evidence (`Potato - Early Blight` $\to$ `Apple - apple scab` in `img_00039793.jpg`), Mermaid pipeline lifecycle flowchart, sub-section numbering fixes, and grounded authentic narrative voice reflecting beginner first-project journey. | Markdown link & style verification, `uv run pytest`<br>**Result:** All links resolve; narrative aligned; 38 tests pass. |
| **J11** | `b2da08b` | Executed Patch P-007 to quarantine all 181 near-duplicate test leakage frames into `data/raw/quarantine_test_leakage_twins/test/`. Physically synchronized the test split to purified clean $N=9,279$ images (total active dataset: 91,984 images across 177 classes: 73,356 train, 9,349 val, 9,279 test). Synchronized `reports/v1/dataset_v1.csv` (SHA-256: `9822de8f77e4a587b8752772af85fbc8c0978e50354f108968d3065e736c50cd`), `models/v1/provenance.json`, `models/v1/checksums.txt`, and updated project documentation. | `apply_patch.py --execute`, bundle verify, pytest<br>**Result:** Test split physically 100% leak-free ($N=9,279$); all manifests and docs synchronized. |

---

## Group K — Dataset Lineage, Verification & Benchmark Harmonization Pass (Branch fix-audit-v1)

| Item ID | Commit | Description | Verification Command & Result |
|:---:|:---:|:---|:---|
| **K0** | `read-only` | Executed complete forensic audit of dataset manifests, patch logs, training run cb46c7f8, calibration file, and training snapshot. Documented findings in `scratch/k0_facts.md`. Verified filesystem equals manifest ($N=91,984$: 73,356 train, 9,349 val, 9,279 test). Verified P-007 moved exactly 181 test images (0 train, 0 val) to `data/raw/quarantine_test_leakage_twins/test/`. Reconstructed training snapshot ($N=92,165$, SHA-256: `5b5bc90a...`). Verified zero images were removed from train post-training. | Forensic inspection of manifests, move logs, MLflow SQLite DB, and calibration parameters.<br>**Result:** All 7 K0 facts documented with verified artifact references. |
| **K1** | `4820260` | Created single source of truth lineage generator `scripts/v1/build_lineage.py` producing `reports/v1/lineage.json` directly from logs and manifest files for stages S1 through S4. Generated `reports/v1/removed_p007_images.csv` (181 quarantined test paths, split, class, SHA-256). Retired old 343-image candidate list to `archive/v1_pre_dedup/leaky_eval_images_historical_343.csv`. | `uv run python scripts/v1/build_lineage.py`<br>**Result:** `reports/v1/lineage.json` and `reports/v1/removed_p007_images.csv` generated. |
| **K2** | `3dcee03` | Ran dataset-wide cryptographic SHA-256 and perceptual hash ($d \le 4$) twin check across all 91,984 release snapshot images. Produced `reports/v1/twin_check.json`. Found 0 exact SHA duplicates; 260 perceptual hash twin pairs between train and val (145 d0, 115 d1_4) spanning 162 unique val images across 14 classes; 0 cross-split test twins. Generated dry-run removal plan `reports/v1/p008_plan_DRYRUN.csv`. | `uv run python scripts/v1/audit/twin_check.py`<br>**Result:** `twin_check.json` and `p008_plan_DRYRUN.csv` generated. |
| **K3** | `b89e5ed` | Diagnosed test split prediction parity (D1-D4). Test split disk images match clean test manifest 100% (9,279 images, identical paths and SHA-256). Identified single boundary case (`Banana - Sigatoka/img_00054704.jpg`, margin 0.000134) sensitive to GPU vs. CPU floating point rounding. Pinned deterministic CPU execution in `scripts/v1/build_results.py` (`torch.set_num_threads(1)`, `torch.use_deterministic_algorithms(True)`) yielding 8,910 / 9,279 (96.02%). Regenerated `results.json`, `counts_table.json`, and `lineage.json`. | Determinism matrix across thread counts; `uv run python scripts/v1/build_results.py`<br>**Result:** Deterministic CPU baseline established; 0-diff on all counts. |
| **K4** | `58f54a4` | Automated data lineage documentation. Authored `scripts/v1/render_lineage_md.py` generating Markdown stages table (S1-S4) and audit sentences from `lineage.json`, `twin_check.json`, and `results.json`. Inserted between marker comments in `docs/DATASET_CARD.md` and `models/v1/model_card.md`. Added CPU determinism disclosure sentence. | `uv run python scripts/v1/render_lineage_md.py`<br>**Result:** Both cards updated idempotently from JSON artifacts. |
| **K5** | `d7a05f8` | Harmonized all dataset, model, and benchmark numbers across documentation and code (`README.md`, `docs/DATASET_CARD.md`, `docs/PATCHES.md`, `models/v1/model_card.md`). Documented P-007 move log in `docs/PATCHES.md`. Added doc-assertion tests in `tests/test_audit_hardening.py` verifying doc numbers match JSON artifacts. Refreshed `models/v1/checksums.txt`. | `uv run pytest -v`<br>**Result:** 39 passed; numbers unified around 91,984 total, 9,279 clean test, 8,910 correct (96.02%), 260 val twins. |
| **K6** | `fa2e170` | Updated `models/v1/provenance.json` with training snapshot SHA-256 (`5b5bc90a...`, $N=92,165$), release snapshot SHA-256 (`9822de8f...`, $N=91,984$), `weights_trained_on_release_snapshot: false`, and preserved MLflow run `cb46c7f8` with dirty working tree status. Refreshed `checksums.txt` and verified CPU bundle loading. | `scripts/v1/make_checksums.py` and `load_model_bundle("v1")`<br>**Result:** Provenance synchronized; bundle loads with 0 warnings. |
| **K7** | `4f7f738` | Hardened narrative essay `docs/essays/DATA_CENTRIC_ODYSSEY_DOCUMENTARY.md`: updated header and epilogue numbers to release snapshot ($N=91,984$, 177 classes, 33 crops), replaced unmeasured zero claims with exact `twin_check.json` findings, updated Chapter 7 test set viability rule to minimum support in lineage, updated Chapter 8 empirical latencies from `runtime_profile.json` (9.08 ms GPU, 53.01 ms CPU, 111.4 MB checkpoint), verified exactly 27 Wikimedia images remain (11 train, 6 val, 10 test), and renumbered figures sequentially (Figures 1-15). | Python script verification & markdown inspection<br>**Result:** Essay aligned with empirical release artifacts. |
| **K8** | `69152dd` | Authored `scripts/v1/build_sources_redistribution.py` generating `reports/v1/sources_redistribution.csv` with 36 sources totaling 91,984 images, license, citation, and empty `redistributable` column. Updated `docs/RELEASE_CHECKLIST.md` checking off completed items while preserving pending redistribution decisions. | `uv run python scripts/v1/build_sources_redistribution.py`<br>**Result:** Redistribution table generated; checklist aligned. |
| **K9** | `fix(K9)` | Final comprehensive release verification pass: verified bundle checksums (`models/v1/checksums.txt`), CPU bundle load (`load_model_bundle("v1")`), weights SHA-256 (`3bb5785e...`), CPU reproduction `build_results.py` diff against `results.json` and `counts_table.json` (0 differences in headline numbers), `ruff check .` (0 errors), `pytest -v` (39 passed, 0 failed), clean worktree test (`git worktree add`, `uv sync`, `ruff check .`, `pytest -v`), verified 100% of tracked relative markdown links resolve (0 broken), ran K5 number grep and hygiene grep, verified git user email is `172237484+Khushii1811@users.noreply.github.com`. | Comprehensive verification suite<br>**Result:** All release invariants and checks verified. |

---

## Full Regression Test Suite Execution Summary

Command: `uv run pytest -v`  
Platform: Windows 11 (win32), Python 3.13.1, pytest-9.1.1, pluggy-1.7.0  
Rootdir: `plant-disease-backend`  

```text
============================= test session starts =============================
platform win32 -- Python 3.13.1, pytest-9.1.1, pluggy-1.7.0
rootdir: plant-disease-backend
configfile: pyproject.toml
testpaths: tests
plugins: anyio-4.14.2
collected 39 items

tests/test_audit_hardening.py::test_schema_and_docs_bundle_count_parity PASSED [  2%]
tests/test_audit_hardening.py::test_docs_numbers_equal_results_json PASSED [  5%]
tests/test_audit_hardening.py::test_docs_numbers_equal_lineage_and_twin_check PASSED [  7%]
tests/test_audit_hardening.py::test_corrupt_bytes_upload_returns_422 PASSED [  7%]
tests/test_audit_hardening.py::test_images_resolution_limits_40mp_200_and_60mp_422 PASSED [ 10%]
tests/test_audit_hardening.py::test_invalid_crop_constraint_returns_422 PASSED [ 13%]
tests/test_audit_hardening.py::test_bundle_tensor_shape_assertion PASSED [ 15%]
tests/test_audit_hardening.py::test_crop_partition_completeness PASSED   [ 18%]
tests/test_audit_hardening.py::test_exif_orientations_1_to_8_transpose PASSED [ 21%]
tests/test_audit_hardening.py::test_dualhead_forward_output_shape PASSED [ 23%]
tests/test_audit_hardening.py::test_soft_gating_zero_sum_fallback PASSED [ 26%]
tests/test_audit_hardening.py::test_temperature_scaling_extreme_values PASSED [ 28%]
tests/test_audit_hardening.py::test_openapi_contains_no_hardcoded_class_or_crop_counts PASSED [ 31%]
tests/test_imports.py::test_import_config_and_verify_paths PASSED        [ 34%]
tests/test_imports.py::test_import_data_modules PASSED                   [ 36%]
tests/test_imports.py::test_import_model_modules PASSED                  [ 39%]
tests/test_imports.py::test_import_evaluation_modules PASSED             [ 42%]
tests/test_imports.py::test_import_serving_modules PASSED                [ 44%]
tests/test_parity.py::test_eval_vs_serving_parity_50_images PASSED       [ 47%]
tests/test_parity.py::test_audit_historical_mismatches_resolved PASSED   [ 50%]
tests/test_parity.py::test_predict_tensor_vs_predict_single_image_20_images PASSED [ 52%]
tests/test_predict_route.py::test_health_endpoint PASSED                 [ 55%]
tests/test_predict_route.py::test_ready_endpoint PASSED                  [ 57%]
tests/test_predict_route.py::test_classes_endpoint PASSED                [ 60%]
tests/test_predict_route.py::test_crops_endpoint PASSED                  [ 63%]
tests/test_predict_route.py::test_predict_auto_detect PASSED             [ 65%]
tests/test_predict_route.py::test_predict_with_crop_constraint PASSED    [ 68%]
tests/test_predict_route.py::test_predict_unsupported_file_type PASSED   [ 71%]
tests/test_predict_route.py::test_predict_empty_file PASSED              [ 73%]
tests/test_predict_route.py::test_predict_invalid_crop_constraint PASSED [ 76%]
tests/test_predict_route.py::test_predict_empty_string_crop_triggers_auto_mode PASSED [ 78%]
tests/test_predict_route.py::test_request_id_middleware_propagates_header_and_context PASSED [ 81%]
tests/test_preprocess.py::test_get_train_transforms_shape_and_type PASSED [ 84%]
tests/test_preprocess.py::test_get_val_transforms_shape_and_type PASSED  [ 86%]
tests/test_preprocess.py::test_get_test_transforms_shape_and_type PASSED [ 89%]
tests/test_preprocess.py::test_load_image_from_path PASSED               [ 92%]
tests/test_preprocess.py::test_load_image_from_bytes_and_io PASSED       [ 94%]
tests/test_preprocess.py::test_load_image_from_pil PASSED                [ 97%]
tests/test_preprocess.py::test_load_image_exif_transpose PASSED          [100%]

======================= 39 passed, 1 warning in 19.61s ========================
```

---

## Group L — Final Diagnostic & Lineage Resolution (fix-audit-v1)

| Item ID | Commit | Description | Verification Command & Result |
|:---:|:---:|:---|:---|
| **L1** | `03122da` | Documented test set determinism diagnosis: verified 100% path set equality between disk test set (`data/processed/test/`, $N=9,279$) and clean test set from pre-P-007 manifest minus 181 leaky frames. Identified that exactly 1 image out of 9,279 (`Banana - Sigatoka/img_00054704.jpg`) produces a borderline score tie (soft-margin $1.34 \times 10^{-4}$ under CPU fp32 vs $3.2 \times 10^{-5}$ under CUDA fp32). Terminal matrix test confirmed CPU baseline of 8,910 across 3 consecutive runs under `OMP_NUM_THREADS=1`. Pinned CPU reference baseline (8,910, 96.02%) retained per Decision Rule 2. Metric diff documented. | Determinism matrix test & metric diff<br>**Result:** Diagnosed exact 1-image boundary tie; CPU baseline 8,910 confirmed across runs. |
| **L2** | `efea663` | Verified real git commit hash recorded by MLflow for training run `cb46c7f8f10f45e59ad809720c7bccb6`: confirmed `21086895979c683ed3c2044da7b9ca919f1dbaa0` exists in repository object database via `git cat-file -t` (confirmed typo hash `21086895b651...` does not exist). Verified commit hash usage across `lineage.json` and build scripts. | `git cat-file -t 21086895979c683ed3c2044da7b9ca919f1dbaa0`<br>**Result:** `commit` object confirmed. |
| **L3** | `3985139` | Updated Stage S3 in `scripts/v1/build_lineage.py` to record that official headline metrics were evaluated on the release snapshot test folder (9,279 files, manifest SHA-256 `9822de8f...`). Earlier 8,911 figures (evaluated on S1 minus 181 list) explicitly cataloged under `historical_evaluation`. Regenerated `docs/DATASET_CARD.md`, `models/v1/model_card.md`, and refreshed `models/v1/checksums.txt`. | `scripts/v1/build_lineage.py && scripts/v1/render_lineage_md.py`<br>**Result:** S3 lineage accurately reflects physical release test folder. |
| **L4** | `baef7e3` | Labeled best-step validation metric in `models/v1/provenance.json` as MLflow masked disease-head accuracy (0.9600, 8,975/9,349) and clearly distinguished it from serving soft-gated accuracy (0.9599, 8,974/9,349). Updated finding 2 in `render_lineage_md.py` and regenerated documentation cards and checksums. | `scripts/v1/render_lineage_md.py`<br>**Result:** Both validation metrics distinguished and documented. |
| **L5** | `4d24f28` | Sanitized image-acquisition terminology across tracked code and docs: replaced "field" with "natural-background", "in-situ", or "orchard", and replaced "smartphone" with "handheld camera", preserving published paper/dataset titles and the official disclaimer line: *"No independent field evaluation has been conducted."* Refreshed checksums and passed full pytest suite. | Audit grep & `uv run pytest -v`<br>**Result:** 39 passed; 0 unapproved field/smartphone occurrences. |
| **L6** | `a2681e5` | Reconciled 36 active operational sources in `reports/v1/sources_redistribution.csv` with the 41 numbered literature entries in `docs/SOURCES.md`: documented the 3 quarantined suites dropped in P-005 (Garlic, Wheat x2), multi-dataset groupings (PlantCity, Dumlao/Ikteshad, Ginger, Plum, Soybean, Guava), and 5 auxiliary/web pipeline identifiers in `reports/v1/sources_reconciliation.md` and `docs/SOURCES.md`. | Cross-manifest verification<br>**Result:** All 41 literature entries and 36 operational sources mapped and accounted for. |
| **L7** | `bf9d01f` | Documented within-split near-duplicate counts (Train: 2,464 pairs, Val: 49 pairs, Test: 56 pairs) and residual validation-vs-train leakage (260 pairs, 162 unique validation images) under limitations in `README.md`, `models/v1/model_card.md`, `docs/DATASET_CARD.md`, and `scripts/v1/render_lineage_md.py`. Refreshed `models/v1/checksums.txt`. | `uv run make_checksums.py && load_model_bundle("v1")`<br>**Result:** Limitations documented; bundle load verified. |
| **L8** | `fix(L8)` | Executed final verification suite: verified model weights SHA-256 (`3bb5785efa957a5fd4eb9d071fa92ff57adbef9788275a810e9cce99cf016dcb`), refreshed bundle checksums, verified bundle loader on CPU, passed `ruff check .` (0 errors), passed `pytest -v` (39 passed, 0 failed), tested clean worktree checkout (`git worktree add`, `uv sync`, `ruff check .`, `pytest -v`), verified tracked relative markdown links (22 files, 67 links, 0 broken), verified K5 number consistency across all docs, verified forbidden terminology, and logged audit history in `AUDIT_FIXES.md`. | Comprehensive release verification suite<br>**Result:** 100% of audit requirements verified and committed. |

