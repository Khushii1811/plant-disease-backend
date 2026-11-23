"""
scripts/data/curation/generate_crop_hierarchy.py

Parses class_names.json (or classes.json) and builds crop_hierarchy.json:
- crop classes with crop_to_idx / idx_to_crop mappings
- crop_to_class_indices: mapping each crop to its allowed disease indices
- class_idx_to_crop_idx: array for multi-task loss target extraction

Inputs:
  - models/<version>/class_names.json
Outputs:
  - models/<version>/crop_hierarchy.json
"""

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import config


def build_crop_hierarchy(model_dir: Path):
    classes_path = model_dir / "class_names.json"
    if not classes_path.exists():
        classes_path = model_dir / "classes.json"
    if not classes_path.exists():
        raise FileNotFoundError(f"Missing classes file in {model_dir}")

    with open(classes_path, "r", encoding="utf-8") as f:
        classes = json.load(f)

    print(f"Total disease classes: {len(classes)}")

    crop_to_class_indices = {}
    class_idx_to_crop_idx = []

    crops_set = set()
    for name in classes:
        parts = name.split(" - ")
        crop = parts[0].strip()
        crops_set.add(crop)

    crops = sorted(list(crops_set))
    crop_to_idx = {crop: idx for idx, crop in enumerate(crops)}
    idx_to_crop = {idx: crop for idx, crop in enumerate(crops)}

    print(f"Total unique crops identified: {len(crops)}")

    for crop in crops:
        crop_to_class_indices[crop] = []

    for class_idx, name in enumerate(classes):
        crop = name.split(" - ")[0].strip()
        crop_idx = crop_to_idx[crop]
        crop_to_class_indices[crop].append(class_idx)
        class_idx_to_crop_idx.append(crop_idx)

    hierarchy = {
        "num_crops": len(crops),
        "num_classes": len(classes),
        "crops": crops,
        "crop_to_idx": crop_to_idx,
        "idx_to_crop": idx_to_crop,
        "crop_to_class_indices": crop_to_class_indices,
        "class_idx_to_crop_idx": class_idx_to_crop_idx,
    }

    out_path = model_dir / "crop_hierarchy.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(hierarchy, f, indent=2)

    print(f"Successfully generated {out_path}")
    return hierarchy


def main():
    parser = argparse.ArgumentParser(description="Generate crop hierarchy from class names")
    parser.add_argument(
        "--model-dir",
        type=Path,
        default=config.MODELS_DIR / "v1",
        help="Path to model directory containing class_names.json",
    )
    args = parser.parse_args()
    build_crop_hierarchy(args.model_dir)


if __name__ == "__main__":
    main()
