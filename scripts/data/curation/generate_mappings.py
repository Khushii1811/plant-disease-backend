"""
scripts/data/curation/generate_mappings.py

Generates authoritative metadata files for models/v1 based on the active 195-class dataset
in data/processed/train:
- models/v1/class_names.json
- models/v1/class_to_idx.json
- models/v1/idx_to_class.json
- models/v1/crop_hierarchy.json
- models/v1/preprocess.json
"""

import json
import logging
import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config import TRAIN_DIR, MODELS_DIR

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("generate_mappings")


def main() -> None:
    v1_dir = MODELS_DIR / "v1"
    v1_dir.mkdir(parents=True, exist_ok=True)
    logger.info("Setting up v1 model directory at: %s", v1_dir)

    train_classes = sorted([d.name for d in TRAIN_DIR.iterdir() if d.is_dir()])
    num_classes = len(train_classes)
    logger.info("Found %d classes in %s", num_classes, TRAIN_DIR)

    # 1. Class mappings
    class_to_idx = {cls_name: i for i, cls_name in enumerate(train_classes)}
    idx_to_class = {str(i): cls_name for i, cls_name in enumerate(train_classes)}

    (v1_dir / "class_names.json").write_text(json.dumps(train_classes, indent=2), encoding="utf-8")
    (v1_dir / "class_to_idx.json").write_text(json.dumps(class_to_idx, indent=2), encoding="utf-8")
    (v1_dir / "idx_to_class.json").write_text(json.dumps(idx_to_class, indent=2), encoding="utf-8")
    logger.info("Saved class_names.json, class_to_idx.json, and idx_to_class.json")

    # 2. Crop hierarchy
    crops_set = set()
    for name in train_classes:
        crop = name.split(" - ")[0].strip()
        crops_set.add(crop)

    crops = sorted(list(crops_set))
    num_crops = len(crops)
    crop_to_idx = {crop: idx for idx, crop in enumerate(crops)}
    idx_to_crop = {str(idx): crop for idx, crop in enumerate(crops)}

    crop_to_class_indices = {crop: [] for crop in crops}
    class_idx_to_crop_idx = []

    for class_idx, name in enumerate(train_classes):
        crop = name.split(" - ")[0].strip()
        c_idx = crop_to_idx[crop]
        crop_to_class_indices[crop].append(class_idx)
        class_idx_to_crop_idx.append(c_idx)

    hierarchy = {
        "num_crops": num_crops,
        "num_classes": num_classes,
        "crops": crops,
        "crop_to_idx": crop_to_idx,
        "idx_to_crop": idx_to_crop,
        "crop_to_class_indices": crop_to_class_indices,
        "class_idx_to_crop_idx": class_idx_to_crop_idx,
    }
    (v1_dir / "crop_hierarchy.json").write_text(json.dumps(hierarchy, indent=2), encoding="utf-8")
    logger.info("Saved crop_hierarchy.json: %d crops, %d classes", num_crops, num_classes)

    # 3. Preprocess configuration
    preprocess_data = {
        "version": "v1.0.0",
        "image_size": [256, 256],
        "mean": [0.485, 0.456, 0.406],
        "std": [0.229, 0.224, 0.225],
        "interpolation": "bilinear",
        "resize_rule": "Direct resize to (256, 256) without aspect-ratio crop for inference and evaluation",
        "normalization": "Standard ImageNet z-score normalization on [0, 1] RGB tensors",
        "tta_views": ["original", "horizontal_flip", "center_crop_scale_1.08"],
    }
    (v1_dir / "preprocess.json").write_text(json.dumps(preprocess_data, indent=2), encoding="utf-8")
    logger.info("Saved preprocess.json")

    # 4. Consistency verification
    assert len(class_idx_to_crop_idx) == num_classes, "class_idx_to_crop_idx length mismatch"
    assert sum(len(indices) for indices in crop_to_class_indices.values()) == num_classes, "crop_to_class_indices sum mismatch"
    logger.info("All consistency assertions PASSED for v1 metadata!")


if __name__ == "__main__":
    main()
