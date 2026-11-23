"""
scripts/data/curation/prune_unviable_classes.py

Prunes statistically unviable singleton/sub-15 classes from data/processed/ to
data/raw/quarantine_pruned_unviable_classes/ with a JSON audit manifest.

Inputs:
  - data/processed/ (train, val, test)
Outputs:
  - data/raw/quarantine_pruned_unviable_classes/
  - data/raw/quarantine_pruned_unviable_classes/pruning_manifest.json
"""

import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import config

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

PROJECT_ROOT = config.PROJECT_ROOT
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
QUARANTINE_DIR = PROJECT_ROOT / "data" / "raw" / "quarantine_pruned_unviable_classes"

TARGET_CLASSES = [
    "Zucchini - zucchini iron chlorosis",
    "Zucchini - zucchini dry leaf",
    "Lettuce - Leaf Blight",
    "Cabbage - Damaged Leaf (White Butterfly)",
    "Zucchini - zucchini insect damage",
    "Cabbage - Grey Mould",
    "Broccoli - broccoli black rot",
    "Plum - plum bacterial spot",
]


def main():
    print("=" * 80)
    print("PRUNING 8 STATISTICALLY UNVIABLE SINGLETON/SUB-15 CLASSES")
    print("=" * 80)

    QUARANTINE_DIR.mkdir(parents=True, exist_ok=True)
    manifest = []
    total_pruned = 0

    for cls_name in TARGET_CLASSES:
        print(f"\n--- Pruning: {cls_name} ---")
        cls_summary = {"class_name": cls_name, "splits": {}, "total_images": 0}

        for split in ["train", "val", "test"]:
            src_dir = PROCESSED_DIR / split / cls_name
            dest_dir = QUARANTINE_DIR / split / cls_name

            if src_dir.exists():
                images = list(src_dir.glob("*.*"))
                count = len(images)
                cls_summary["splits"][split] = count
                cls_summary["total_images"] += count
                total_pruned += count

                dest_dir.mkdir(parents=True, exist_ok=True)
                for img in images:
                    shutil.move(str(img), str(dest_dir / img.name))

                try:
                    src_dir.rmdir()
                except Exception as e:
                    print(f"  [WARN] Could not remove empty dir {src_dir}: {e}")

                print(f"   {split:<5}: {count:2d} images moved -> {dest_dir.relative_to(PROJECT_ROOT)}")
            else:
                cls_summary["splits"][split] = 0

        manifest.append(cls_summary)

    manifest_path = QUARANTINE_DIR / "pruning_manifest.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    print("\n" + "=" * 80)
    print("PRUNING SUMMARY")
    print("=" * 80)
    print(f"Total classes pruned : {len(TARGET_CLASSES)}")
    print(f"Total images archived: {total_pruned}")
    print(f"Manifest saved to    : {manifest_path.relative_to(PROJECT_ROOT)}")
    print("=" * 80)


if __name__ == "__main__":
    main()
