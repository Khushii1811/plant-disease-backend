# Audit Remediation Blocked Items & Engineering Constraints (`BLOCKED.md`)

This document records architectural, dependency, and scope constraints encountered during the audit remediation of `plant-disease-backend` on branch `fix-audit-v1`.

---

## 1. Model Retraining & Weights Preservation
- **Status:** BLOCKED BY DESIGN INVARIANT
- **Constraint:** Remediation instructions strictly forbade retraining the backbone or classifier heads, altering model weights tensor values (`model_dualhead_convnext_tiny.pth`), or shifting images between `train`, `val`, and `test` splits.
- **Impact:** All calibration, gating, and confidence thresholds operate on the existing frozen checkpoint (`models/v1/model_dualhead_convnext_tiny.pth`). Temperature scaling ($T_{\text{crop}}=0.5931$, $T_{\text{disease}}=0.5013$) and soft crop-gating were unified across all evaluation and inference paths without modifying underlying model weights.

---

## 2. Independent Field Evaluation
- **Status:** EXCLUDED FROM CORE BENCHMARK (NO INDEPENDENT FIELD DATASET EXISTS)
- No independent field evaluation has been conducted.

---

## 3. Docker CPU-Only Wheel Resolution
- **Status:** BLOCKED FROM LOCAL BUILD WITHOUT LOCKFILE MUTATION
- **Constraint:** In `pyproject.toml` and `uv.lock`, PyTorch is pinned to CUDA 12.4 wheels (`url = "https://download.pytorch.org/whl/cu124"`). Building a minimal CPU-only Docker image requires altering `[tool.uv.sources]` to CPU wheels (`https://download.pytorch.org/whl/cpu`) and re-running `uv lock`, which would alter dependencies for the host environment and violate the lockfile preservation mandate.
- **Mitigation:** The `Dockerfile` has been updated to use `python:3.13-slim-bookworm`, non-root execution (`USER appuser`), and the `/api/v1/ready` healthcheck probe. Dedicated CPU-only wheel resolution should be managed via target-specific build arguments or separate CI deployment targets.

---

## 4. Docker Environment Testing Status
- **Status:** IMAGE NOT YET BUILT OR RUN LOCALLY
- **Constraint:** Docker daemon is not active in the local verification environment. Documented in `README.md` limitations ("Docker: image not yet built or tested").
- **Mitigation:** Base image (`python:3.13-slim-bookworm`), non-root execution (`USER appuser`), `/api/v1/ready` healthcheck probe, and `.dockerignore` filters were audited and verified statically.

---

## 5. Metric Invariance Guarantee
- **Status:** VERIFIED UNCHANGED
- **Guarantee:** Across all post-audit remediation tasks (F1 through F9, and H1 through H10), no reported headline or per-class evaluation metrics changed. Re-running `scripts/v1/build_results.py` on CPU across all 9,279 clean test images yielded exact 0-diff parity with `reports/v1/results.json` (8,911 correct, 8,776 covered correct, 135 uncertain correct, soft-gated accuracy 96.03%, crop accuracy 99.28%).
