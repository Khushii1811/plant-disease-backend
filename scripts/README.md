# Hale Scripts Catalog & Audit Trail Guide

This directory contains executable verification tools, evaluation benchmarks, model packaging utilities, and scientific curation scripts for the Hale plant leaf disease classification model.

> [!NOTE]
> **Dataset Availability & Audit Trail Scope:**  
> Scripts in scripts/data/ and scripts/v1/ that require the private raw image folders (data/raw/, data/quarantine_*/) or processed image directories are provided strictly as an **audit trail**. They document how the dataset was curated, deduplicated, and evaluated across patches. Because the dataset comprises 92,000+ images with non-commercial, share-alike, or proprietary upstream terms, raw images are not distributed in this repository.  
> The trained model weights and inference server run standalone without the private training images.

---

## Script Lookup & Navigation Table

| Script Path | Purpose | Needs Private Dataset? | Runnable by Reader? | Related Documentation |
| :--- | :--- | :---: | :---: | :--- |
| **scripts/check_doc_consistency.py** | Automated cross-document metric, link, and table consistency validator. | **No** | **Yes** | Root README.md, docs/README.md |
| **scripts/build_space_bundle.py** | Packages minimal bundle and weights for Hugging Face Spaces deployment. | **No** | **Yes** | docs/FEATURES_GUIDE.md |
| **scripts/evaluate.py** | Universal CLI evaluation runner for release checkpoints. | Yes | No (requires test images) | docs/RELEASE_CHECKLIST.md |
| **scripts/verify_step1_leakage.py** | Verifies zero byte-exact SHA-256 cross-split collisions. | Yes | No | docs/PATCH_LINEAGE.md |
| **scripts/v1/build_bundle.py** | Generates production bundle metadata, class mappings, and checksums. | **No** | **Yes** | docs/PATCHES.md |
| **scripts/v1/build_lineage.py** | Compiles commit hashes, dataset SHAs, and patch timelines. | **No** | **Yes** | docs/PATCH_LINEAGE.md |
| **scripts/v1/build_results.py** | Compiles all release metrics into 
eports/v1/results.json. | Yes | No | docs/AUDIT_SUMMARY.md |
| **scripts/v1/build_sources_redistribution.py** | Compiles redistribution permissions across 41 source datasets. | **No** | **Yes** | docs/SOURCES.md, docs/LICENSING_NOTES.md |
| **scripts/v1/evaluate_common_test.py** | Evaluates Common Test Set across historical releases. | Yes | No | docs/CASE_STUDY_BELLPEPPER_CHILLI.md |
| **scripts/v1/evaluate_final_test.py** | Official test evaluation script producing production metrics. | Yes | No | docs/AUDIT_SUMMARY.md, 
eports/v1/ |
| **scripts/v1/make_checksums.py** | Computes cryptographic SHA-256 checksums for release bundle. | **No** | **Yes** | models/v1/sha256_checksums.txt |
| **scripts/v1/make_dataset_manifest.py** | Generates dataset manifest summary and split counts. | Yes | No | docs/DATASET_CARD.md |
| **scripts/v1/measure_runtime.py** | Profiles inference latency (preprocess, forward, decode). | **No** | **Yes** | docs/FEATURES_GUIDE.md |
| **scripts/v1/render_lineage_md.py** | Renders markdown lineage tables from JSON audit records. | **No** | **Yes** | docs/PATCH_LINEAGE.md |
| **scripts/v1/run_calibration.py** | Fits Platt temperature scaling on validation set logits. | Yes | No | docs/FEATURES_GUIDE.md |
| **scripts/v1/run_determinism_test.py** | Verifies bit-exact forward pass reproducibility across seeds. | **No** | **Yes** | docs/RELEASE_CHECKLIST.md |
| **scripts/v1/run_strict_leakage_audit.py** | Generates Hamming distance graphs and leakage contact sheets. | Yes | No | docs/PATCH_LINEAGE.md |
| **scripts/eval/measure_cold_start.py** | Measures container cold-start and model initialization time. | **No** | **Yes** | docs/FEATURES_GUIDE.md |
| **scripts/eval/measure_hosting_metrics.py** | Measures process RSS footprint and steady-state memory. | **No** | **Yes** | docs/FEATURES_GUIDE.md |
| **scripts/eval/measure_memory_breakdown.py** | Profiles granular CPU/GPU RSS memory breakdown across loads. | **No** | **Yes (needs psutil)** | docs/FEATURES_GUIDE.md |
| **scripts/eval/evaluate_bg_removal.py** | Measures accuracy delta under synthetic background removal. | Yes | No | Root README.md |
| **scripts/eval/bench_concurrency.py** | Profiles multi-threaded request throughput and peak RSS. | **No** | **Yes** | docs/FEATURES_GUIDE.md |
| **scripts/data/apply_patch.py** | Generic patch engine for moving and quarantining images. | Yes | No | data/patches/ |
| **scripts/data/apply_patch_p005.py** | Deterministic Patch P-005 migration engine. | Yes | No | docs/PATCH_LINEAGE.md |
| **scripts/data/curation/*.py** | Forensic data curation scripts (pHash twin graphs, label audits). | Yes | No | docs/PATCH_LINEAGE.md |
| **scripts/data/collection/download_kaggle_chilli.py** | Downloader for documented open Kaggle Chilli dataset. | **No** | **Yes** | docs/SOURCES.md |
| **scripts/data/collection/download_kaggle_coffee.py** | Downloader for documented open Kaggle Coffee dataset. | **No** | **Yes** | docs/SOURCES.md |
| **scripts/data/collection/download_kaggle_corn.py** | Downloader for documented open Kaggle Corn dataset. | **No** | **Yes** | docs/SOURCES.md |
| **scripts/data/collection/download_mendeley_plum.py** | Resumable downloader for Mendeley Plum dataset (CC BY 4.0). | **No** | **Yes** | docs/SOURCES.md |
| **scripts/data/collection/fetch_plantdoc_classes.py** | Direct streaming harvester for PlantDoc benchmark classes. | **No** | **Yes** | docs/SOURCES.md |
| **scripts/data/collection/scrape_wikimedia.py** | Downloader for open Wikimedia Commons botanical leaf images. | **No** | **Yes** | docs/SOURCES.md |
| **scripts/data/collection/scrape_bing.py** | Audit trail: provenance script for 19 Bing images (images not redistributed). | **No** | **Yes** | docs/DATASET_LICENSE.md |
| **scripts/data/collection/scrape_inaturalist.py** | Audit trail: provenance script for 27 iNaturalist images (images not redistributed). | **No** | **Yes** | docs/DATASET_LICENSE.md |
