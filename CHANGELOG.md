# Changelog

All notable changes to `plant-disease-backend` are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-11-06

### Added
- Curated Production Release v1.0 encompassing 177 foliar disease classes across 33 botanical host crops (91,984 active images post-Patch P-007).
- DualHead ConvNeXt-Tiny architecture (`models/v1/model_dualhead_convnext_tiny.pth`) with soft joint probability gating $P(\text{crop}) \times P(\text{disease})$.
- Leak-checked evaluation benchmark with purified leak-free test partition ($N=9,279$ clean test images, 181 near-duplicate frames quarantined under Patch P-007), achieving 96.02% soft-gated accuracy, 99.28% crop accuracy, and 93.86% macro-F1 across all 177 classes.
- Post-hoc vectorized Platt temperature scaling ($T_{\text{crop}}=0.5931$, $T_{\text{disease}}=0.5013$) achieving calibrated Expected Calibration Error (ECE) of 0.57%.
- Operational serving limits in FastAPI: 50 MP resolution ceiling with actionable resize guidance and 10 MB payload upload limit.
- Verified runtime profile measured on CPU (AMD Ryzen 7 6800H) and GPU (NVIDIA RTX 3050 Laptop GPU), recording bundle load time, peak RSS, p50/p95 latency, and concurrent execution memory (`reports/v1/runtime_profile.json`).
- Exhaustive per-class evaluation metrics report (`reports/v1/per_class_results.csv`).
- Comprehensive regression and invariant test suite covering API error handling, bundle parity, EXIF orientation transposition, and calibration edge cases.

### Changed
- Patch P-005: 34-crop visual audit quarantining 4,665 non-foliar/mixed images, relabeling 3,062 misidentifications, and merging `Mango - Powdery Mildew` into `Mango - Sooty Mould`.
- Patch P-006: Stratified repartitioning across 21 classes guaranteeing $\ge 3$ images per split and eliminating zero-support validation/test classes.
- Patch P-007: Physically quarantined all 181 near-duplicate test leakage frames into `data/raw/quarantine_test_leakage_twins/test/`, locking the active test split to purified clean $N=9,279$ images (total active dataset: 91,984 images).
- Model card rewritten to contain strictly verified empirical numbers without unmeasured claims.
- Documentation unified across `README.md`, `model_card.md`, `DATASET_CARD.md`, and `PATCHES.md`.

### Fixed
- Isolated 343 validation and test images sharing near-duplicate perceptual hash twins with training data (`archive/v1_pre_dedup/leaky_eval_images_historical_343.csv`, 181 test images removed under P-007 logged in `reports/v1/removed_p007_images.csv`).
- Hardened image payload ingestion with fast PIL header probing before full memory decoding.
- Resolved licensing status: MIT license for repository code, CC BY-NC-SA 4.0 for annotations/manifests, and explicit policy that raw images are not redistributed.

## [0.9.0-prerelease] - 2026-10-30

### Added
- Pre-release baseline prototype model and dataset covering 195 classes across 34 crops (96,835 active images).
- Patches P-001 and P-002: initial duplicate purging for Bell Pepper/Chilli and stratified split rebalancing.
- Patch P-003: 0-bit perceptual hash cross-split leakage quarantine (1,415 images quarantined).
- Patch P-004: Deduplication and cross-split label contradiction quarantine (1,245 images quarantined).

## [0.1.0-alpha] - 2026-10-15

### Added
- Initial unstratified prototype baseline across 200 candidate classes (~99,775 images).
