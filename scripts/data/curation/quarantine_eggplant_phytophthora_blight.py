"""
scripts/quarantine_eggplant_phytophthora_blight.py

Quarantines all brinjal/fruit-only images from:
  - data/processed/train/Eggplant - eggplant phytophthora blight
  - data/processed/val/Eggplant - eggplant phytophthora blight
  - data/processed/test/Eggplant - eggplant phytophthora blight

Moves them to:
  - data/raw/quarantine_eggplant_fruit_blight/
"""

import shutil
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
QUARANTINE_DIR = PROJECT_ROOT / "data" / "raw" / "quarantine_eggplant_fruit_blight"

SPLITS = ["train", "val", "test"]
TARGET_CLASS = "Eggplant - eggplant phytophthora blight"

def main():
    QUARANTINE_DIR.mkdir(parents=True, exist_ok=True)
    moved_count = 0

    for split in SPLITS:
        split_dir = PROCESSED_DIR / split / TARGET_CLASS
        if not split_dir.exists():
            continue
        
        split_quarantine = QUARANTINE_DIR / split
        split_quarantine.mkdir(parents=True, exist_ok=True)

        for img_path in list(split_dir.iterdir()):
            if img_path.is_file():
                dest = split_quarantine / img_path.name
                shutil.move(str(img_path), str(dest))
                moved_count += 1
        
        # Remove empty folder
        try:
            if not any(split_dir.iterdir()):
                split_dir.rmdir()
                print(f"[CLEANUP] Removed empty directory: {split_dir}")
        except Exception as e:
            print(f"[WARN] Could not remove {split_dir}: {e}")

    print(f"\n[SUCCESS] Quarantined {moved_count} images from '{TARGET_CLASS}' across {SPLITS}.")
    print(f"Archived safely in: {QUARANTINE_DIR}")

if __name__ == "__main__":
    main()
