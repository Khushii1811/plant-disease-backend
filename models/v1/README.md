# Model Bundle: Hale ConvNeXt-Tiny DualHead (v1.0 Release)

This directory contains configuration, class mappings, temperature scaling calibration, and metadata for the official v1.0 release of the Hale foliar plant leaf disease classification engine.

## Model Checkpoint & Asset Distribution

The PyTorch weights file (`model_dualhead_convnext_tiny.pth`) is released as a standalone GitHub Release asset.

- **Architecture:** ConvNeXt-Tiny DualHead (shared backbone with independent crop and disease classification heads).
- **Target File:** `models/v1/model_dualhead_convnext_tiny.pth`
- **Classes:** 177 disease conditions across 33 crop families (post-Patch P-005 curation).
- **Input Size:** 256x256 RGB foliar leaf image.
- **SHA-256 Checksum:** `3bb5785efa957a5fd4eb9d071fa92ff57adbef9788275a810e9cce99cf016dcb`

To download or verify the weights file, run:
```bash
python scripts/download_weights.py
```

## Licensing

- **License:** [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)](https://creativecommons.org/licenses/by-nc-sa/4.0/)
- **Usage Restrictions:** Model weights and derived parameters are released strictly for academic, research, and non-commercial evaluation purposes. Commercial deployment and resale are prohibited under upstream dataset compilation terms.
