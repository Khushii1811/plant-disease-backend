"""
scripts/consolidate_redundant_classes.py — Consolidate duplicate and redundant dataset class folders.

Merges the 13 redundant class directories in data/processed/train, val, and test into
standardized canonical class folders (reducing classes from 181 to 168 unique categories).
Preserves all images, safely handles filename conflicts, and removes empty redundant folders.

Usage:
    python scripts/consolidate_redundant_classes.py
    python scripts/consolidate_redundant_classes.py --dry-run
"""

import argparse
import logging
import os
import shutil
from pathlib import Path
from typing import Dict, List

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("consolidate_classes")

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
SPLITS = ["train", "val", "test"]

# Mapping of redundant class folder name -> target canonical folder name
MERGE_MAP: Dict[str, str] = {
    # 1. Apple Rust
    "Apple - apple rust": "Apple - Rust",
    
    # 2. Banana Cordana
    "Banana - banana cordana leaf spot": "Banana - Cordana",
    
    # 3. Banana Panama
    "Banana - banana panama disease": "Banana - Panama",
    
    # 4. Bell Pepper Bacterial Spot
    "Bell pepper - bell pepper bacterial spot": "Bell Pepper - Bacterial Spot",
    
    # 5. Cauliflower Bacterial Soft Rot (fixing double space typo and standardizing)
    "Cauliflower - Bacterial  spot  rot": "Cauliflower - Bacterial Soft Rot",
    "Cauliflower - cauliflower bacterial soft rot": "Cauliflower - Bacterial Soft Rot",
    
    # 6. Corn Northern Leaf Blight (standardizing generic 'Leaf Blight' to 'Northern Leaf Blight')
    "Corn - Leaf Blight": "Corn - Northern Leaf Blight",
    "Corn - corn northern leaf blight": "Corn - Northern Leaf Blight",
    
    # 7. Corn Rust
    "Corn - corn rust": "Corn - Rust",
    
    # 8. Grape Black Rot
    "Grape - grape black rot": "Grape - Black Rot",
    
    # 9. Potato Early Blight
    "Potato - potato early blight": "Potato - Early Blight",
    
    # 10. Potato Late Blight
    "Potato - potato late blight": "Potato - Late Blight",
    
    # 11. Rice / Paddy Blast (merging into Paddy - Blast)
    "Rice - rice blast": "Paddy - Blast",
    
    # 12. Squash Powdery Mildew
    "Squash - squash powdery mildew": "Squash - Powdery Mildew",
    
    # 13. Tomato Bacterial Spot
    "Tomato - tomato bacterial leaf spot": "Tomato - Bacterial Spot",
}


def merge_split(split_name: str, dry_run: bool = False) -> None:
    split_dir = PROCESSED_DIR / split_name
    if not split_dir.exists():
        logger.warning("Split directory %s does not exist, skipping.", split_dir)
        return

    logger.info("--- Processing split: %s ---", split_name)
    total_moved = 0

    for source_name, target_name in MERGE_MAP.items():
        src_folder = split_dir / source_name
        dst_folder = split_dir / target_name

        if not src_folder.exists():
            continue

        if not dry_run:
            dst_folder.mkdir(parents=True, exist_ok=True)

        images = [f for f in src_folder.iterdir() if f.is_file() and not f.name.startswith(".")]
        if not images:
            logger.info("Source '%s' is empty.", source_name)
            if not dry_run:
                try:
                    src_folder.rmdir()
                except Exception:
                    pass
            continue

        logger.info("Merging '%s' (%d images) -> '%s'", source_name, len(images), target_name)

        for img in images:
            target_path = dst_folder / img.name
            if target_path.exists() and target_path != img:
                # Resolve filename collision
                stem = img.stem
                suffix = img.suffix
                counter = 1
                while target_path.exists():
                    target_path = dst_folder / f"{stem}_merged_{counter}{suffix}"
                    counter += 1

            if not dry_run:
                shutil.move(str(img), str(target_path))
            total_moved += 1

        if not dry_run:
            try:
                # Remove leftover source dir
                shutil.rmtree(str(src_folder), ignore_errors=True)
            except Exception as e:
                logger.warning("Could not remove %s: %s", src_folder, e)

    logger.info("Split '%s' complete: %d images consolidated.\n", split_name, total_moved)


def main() -> None:
    parser = argparse.ArgumentParser(description="Consolidate redundant plant disease classes")
    parser.add_argument("--dry-run", action="store_true", help="Simulate without modifying files")
    args = parser.parse_args()

    train_classes_before = sorted([d.name for d in (PROCESSED_DIR / "train").iterdir() if d.is_dir()])
    logger.info("Classes before consolidation: %d", len(train_classes_before))

    for split in SPLITS:
        merge_split(split, dry_run=args.dry_run)

    if not args.dry_run:
        train_classes_after = sorted([d.name for d in (PROCESSED_DIR / "train").iterdir() if d.is_dir()])
        logger.info("Classes after consolidation: %d", len(train_classes_after))
        logger.info("Successfully merged all 13 redundant class groups into canonical categories!")


if __name__ == "__main__":
    main()
