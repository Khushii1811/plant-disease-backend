# Audit Summary: Plant Leaf Disease Classification Benchmark (`plant-disease-backend`)

This document provides a concise executive overview of the comprehensive engineering, data curation, and model evaluation audit performed on `plant-disease-backend`.

For the granular item-by-item fix log and verification references, see [`AUDIT_FIXES.md`](../AUDIT_FIXES.md).

---

## 1. Audit Scope & Objectives

The audit evaluated five core pillars of the repository:
1. **Data Integrity & Partition Separation:** Verification of split independence, detection of cross-split duplicate images (exact SHA-256 and near-duplicate perceptual hash twins), and elimination of label contradictions.
2. **Evaluation Rigor & Metric Provenance:** Independent reproduction of all reported benchmark metrics strictly from execution scripts and raw predictions on held-out test splits.
3. **Serving Resilience & Input Validation:** Assessment of FastAPI inference endpoints against malformed, corrupt, oversized, and adversarial image payloads.
4. **Empirical Runtime Profile:** Hardware-pinned measurement of bundle load latency, memory consumption (peak RSS), inference throughput, and concurrency scaling.
5. **Documentation Integrity & Licensing Consistency:** Alignment of all documentation (`README.md`, `model_card.md`, `DATASET_CARD.md`, `PATCHES.md`, `SOURCES.md`) with code reality, explicit statement of operational boundaries, and resolution of upstream licensing terms.

---

## 2. Key Audit Findings & Implemented Fixes

### A. Data Curation & Split Purification (Patches P-001 through P-006)
- **Leakage Quarantine:** Quarantined 1,415 zero-bit pHash twin frames across splits (Patch P-003) and 1,245 cross-split duplicates / contradictory labels (Patch P-004).
- **Foliar Pathology Curation (Patch P-005 & P-007):** Quarantined 4,665 non-foliar or severe mixed images across 17 classes, relabeled 3,062 misidentified images, merged `Mango - Powdery Mildew` into `Mango - Sooty Mould`, and quarantined 181 near-duplicate test leakage frames under Patch P-007. This established the 177-class Curated Release v1.0 benchmark (91,984 active images across 33 crops, purified clean test $N=9,279$).
- **Split Rebalancing (Patch P-006):** Repartitioned 21 hoarded classes to ensure $\ge 3$ images per split, eliminating zero-support validation and test sets.
- **Residual Leakage Isolation:** Identified 343 validation/test images with near-duplicate twins ($d \le 4$) in the training set (`data/patches/history/leaky_eval_images_historical_343.csv`). Clean benchmark evaluation removes all 181 test twin images (`reports/v1/removed_p007_images.csv`), yielding a strictly leak-checked test split of $N=9,279$ images.

### B. Headline Metric Reproduction
- **Deterministic Evaluation:** Headline metrics are computed strictly on CPU using `src.models.predict.predict_tensor` over the 9,279 clean test images via `scripts/v1/build_results.py`:
  - **Crop Accuracy:** 99.28% (95% Bootstrap CI: [99.11%, 99.44%])
  - **Soft-Gated Disease Accuracy:** 96.03% (95% Bootstrap CI: [95.62%, 96.45%])
  - **Raw Disease Accuracy:** 95.84% (95% Bootstrap CI: [95.43%, 96.26%])
  - **Macro-F1 (All 177 classes):** 93.87% (95% Bootstrap CI: [91.85%, 94.43%])
  - **Macro-F1 ($\ge 10$ test images, 147 classes):** 96.55% (95% Bootstrap CI: [95.97%, 97.01%])
  - **Calibrated ECE (15 bins):** 0.58% ($T_{\text{crop}}=0.5931$, $T_{\text{disease}}=0.5013$)
- **Per-Class Breakdown:** Full support counts, accuracy, F1, and twin share per class are recorded in `reports/v1/per_class_results.csv`.

### C. Serving Hardening & Defensive Ingestion
- **Resolution Ceiling:** Enforced 50 MP (`50_000_000` pixels) upload cap with informative HTTP 422 rejection advising client-side downscaling.
- **Payload Size Cap:** Enforced 10 MB (`10_485_760` bytes) upload limit.
- **Defensive Header Probing:** Probes dimensions directly from image container headers using PIL before invoking full decompression, preventing decompression bomb denial-of-service vulnerabilities.
- **Input Error Handling:** Invalid MIME types, corrupt payloads, and unrecognized crop constraint filters return HTTP 422 instead of crashing or returning HTTP 500.

### D. Measured Runtime Profile (`reports/v1/runtime_profile.json`)
- **CPU (AMD Ryzen 7 6800H, 8 threads):** Bundle load: 0.388 s (peak RSS: 785 MB), warm-up: 56.1 ms, latency p50/p95: 54.8 ms / 63.4 ms end-to-end, concurrent requests peak RSS: 855 MB.
- **GPU (NVIDIA RTX 3050 Laptop GPU):** Bundle load: 0.594 s (peak RSS: 979 MB), warm-up: 235.6 ms, latency p50/p95: 11.3 ms / 18.3 ms end-to-end, concurrent requests peak RSS: 1,321 MB.

### E. Licensing & Provenance Resolution
- **Code:** Licensed under the [MIT License](../LICENSE).
- **Dataset Manifests & Metadata:** Released under [CC BY-NC-SA 4.0](./DATASET_LICENSE.md).
- **Image Policy:** Raw plant leaf images are **NOT** redistributed; users assemble splits locally from primary upstream archives using the provided manifests.
- **Upstream Catalog:** Complete audit of all 41 upstream source entries cataloged with per-source licenses in `docs/SOURCES.md` and `docs/LICENSING_NOTES.md`.

---

## 3. Detailed Fix Registry

For the complete chronologically tagged audit fix registry, see [`AUDIT_FIXES.md`](../AUDIT_FIXES.md).
