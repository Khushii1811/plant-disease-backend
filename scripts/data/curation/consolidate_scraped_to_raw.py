"""
scripts/consolidate_scraped_to_raw.py — Consolidate all scraped datasets into a unified folder.

Creates a unified directory in data/raw/ matching the exact class folder structure
of data/processed/train/.

Sources consolidated:
  1. data/scraped_v2/                 (iNaturalist & Bing scrape v2)
  2. data/scraped/                    (Targeted scrape v1)
  3. data/raw/scraped/kaggle/grape_diseases/
  4. data/raw/scraped/kaggle/plantvillage_v1/
  
  5. data/raw/scraped/kaggle/plantvillage_v2/

Workflow:
  Step 1: Consolidate scraped images into data/raw/unified_scraped/ (this script)
  Step 2: Run deduplication & quality cleaning on data/raw/unified_scraped/
  Step 3: Merge verified/cleaned images into data/processed/train/
"""

import argparse
import logging
import os
import shutil
import sys
from collections import defaultdict
from pathlib import Path
from tqdm import tqdm

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("unify_scraped")

PROJECT_ROOT = Path(__file__).resolve().parent.parent
TRAIN_DIR = PROJECT_ROOT / "data" / "processed" / "train"
UNIFIED_RAW_DIR = PROJECT_ROOT / "data" / "raw" / "unified_scraped"

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}

# Explicit mapping of source folder names to target class names in train
EXPLICIT_MAP = {
    # PlantVillage v1 / v2
    "Apple___Apple_scab": "Apple - apple scab",
    "Apple___Black_rot": "Apple - apple black rot",
    "Apple___Cedar_apple_rust": "Apple - Rust",
    "Apple___healthy": "Apple - Healthy",
    "Blueberry___healthy": "Blueberry - Healthy",
    "Cherry_(including_sour)___healthy": "Cherry - Healthy",
    "Cherry_(including_sour)___Powdery_mildew": "Cherry - cherry powdery mildew",
    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot": "Corn - corn gray leaf spot",
    "Corn_(maize)___Common_rust_": "Corn - Rust",
    "Corn_(maize)___Northern_Leaf_Blight": "Corn - Northern Leaf Blight",
    "Grape___Black_rot": "Grape - Black Rot",
    "Grape___healthy": "Grape - Healthy",
    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)": "Grape - grape leaf spot",
    "Orange___Haunglongbing_(Citrus_greening)": "Citrus - citrus greening disease",
    "Peach___healthy": "Peach - Healthy",
    "Pepper,_bell___Bacterial_spot": "Bell Pepper - Bacterial Spot",
    "Pepper,_bell___healthy": "Bell Pepper - Healthy",
    "Potato___Early_blight": "Potato - Early Blight",
    "Potato___healthy": "Potato - Healthy",
    "Potato___Late_blight": "Potato - Late Blight",
    "Raspberry___healthy": "Raspberry - Healthy",
    "Soybean___healthy": "Soybean - Healthy",
    "Squash___Powdery_mildew": "Squash - Powdery Mildew",
    "Strawberry___healthy": "Strawberry - Healthy",
    "Strawberry___Leaf_scorch": "Strawberry - strawberry leaf scorch",
    "Tomato___Bacterial_spot": "Tomato - Bacterial Spot",
    "Tomato___Early_blight": "Tomato - tomato early blight",
    "Tomato___healthy": "Tomato - Healthy",
    "Tomato___Late_blight": "Tomato - tomato late blight",
    "Tomato___Leaf_Mold": "Tomato - tomato leaf mold",
    "Tomato___Septoria_leaf_spot": "Tomato - tomato septoria leaf spot",
    "Tomato___Spider_mites Two-spotted_spider_mite": "Tomato - Spider Mites",
    "Tomato___Target_Spot": "Tomato - Target Spot",
    "Tomato___Tomato_mosaic_virus": "Tomato - tomato mosaic virus",
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus": "Tomato - tomato yellow leaf curl virus",

    # Grape Kaggle Dataset
    "grape_Black Rot": "Grape - Black Rot",
    "grape_Healthy": "Grape - Healthy",
    "grape_Leaf Blight": "Grape - grape leaf spot",

    # Scraped aliases
    "Banana - banana cordana leaf spot": "Banana - Cordana",
    "Banana - banana panama disease": "Banana - Panama",
    "Bell pepper - bell pepper bacterial spot": "Bell Pepper - Bacterial Spot",
    "Cauliflower - cauliflower bacterial soft rot": "Cauliflower - Bacterial Soft Rot",
    "Corn - corn northern leaf blight": "Corn - Northern Leaf Blight",
    "Corn - Leaf Blight": "Corn - Northern Leaf Blight",
    "Potato - potato early blight": "Potato - Early Blight",
    "Potato - potato late blight": "Potato - Late Blight",
    "Squash - squash powdery mildew": "Squash - Powdery Mildew",
}


def get_train_classes() -> list[str]:
    """Retrieve all standard class names from data/processed/train."""
    if not TRAIN_DIR.exists():
        logger.error("Train directory not found: %s", TRAIN_DIR)
        sys.exit(1)
    return sorted([d.name for d in TRAIN_DIR.iterdir() if d.is_dir()])


def resolve_class_name(folder_name: str, train_classes_set: set[str]) -> str | None:
    """Resolve a source folder name to the standardized train class name."""
    if folder_name in train_classes_set:
        return folder_name

    if folder_name in EXPLICIT_MAP:
        target = EXPLICIT_MAP[folder_name]
        if target in train_classes_set:
            return target

    # Case-insensitive direct match
    folder_lower = folder_name.lower().strip()
    for tc in train_classes_set:
        if tc.lower().strip() == folder_lower:
            return tc

    return None


def collect_source_files(
    src_dir: Path,
    source_prefix: str,
    train_classes_set: set[str],
    max_per_class: int,
    is_grape_special: bool = False,
) -> dict[str, list[Path]]:
    """Scan directory and group image files by target class name."""
    matched_files: dict[str, list[Path]] = defaultdict(list)

    if not src_dir.exists():
        return matched_files

    if is_grape_special:
        # Grape dataset has train/test/val subfolders with "Black Rot", "Leaf Blight", etc.
        for img_path in src_dir.rglob("*"):
            if img_path.suffix.lower() in IMAGE_EXTS:
                parent_name = img_path.parent.name
                key = f"grape_{parent_name}"
                target_cls = resolve_class_name(key, train_classes_set)
                if target_cls:
                    if len(matched_files[target_cls]) < max_per_class:
                        matched_files[target_cls].append(img_path)
        return matched_files

    # Standard scanning
    for class_folder in src_dir.iterdir():
        if not class_folder.is_dir():
            continue

        target_cls = resolve_class_name(class_folder.name, train_classes_set)
        if not target_cls:
            continue

        files = [f for f in class_folder.rglob("*") if f.suffix.lower() in IMAGE_EXTS]
        # Limit to max_per_class
        for f in files:
            if len(matched_files[target_cls]) < max_per_class:
                matched_files[target_cls].append(f)

    return matched_files


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Merge and organize scraped data into a unified raw folder matching train classes."
    )
    parser.add_argument(
        "--dest",
        type=str,
        default=str(UNIFIED_RAW_DIR),
        help="Destination directory in data/raw (default: data/raw/unified_scraped)",
    )
    parser.add_argument(
        "--max-per-class",
        type=int,
        default=300,
        help="Maximum images to ingest per class across scraped sources (default: 300)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulate the merge without copying files to disk",
    )
    args = parser.parse_args()

    dest_dir = Path(args.dest)
    max_per_class = args.max_per_class
    dry_run = args.dry_run

    train_classes = get_train_classes()
    train_classes_set = set(train_classes)
    logger.info("Found %d classes in %s", len(train_classes), TRAIN_DIR)

    # Pre-create all class folders in destination (or show in plan)
    if not dry_run:
        dest_dir.mkdir(parents=True, exist_ok=True)
        for tc in train_classes:
            (dest_dir / tc).mkdir(parents=True, exist_ok=True)
        logger.info("Initialized %d class directories in %s", len(train_classes), dest_dir)

    sources = [
        ("data/scraped_v2", "scraped_v2", False),
        ("data/scraped", "scraped_v1", False),
        ("data/raw/scraped/kaggle/grape_diseases", "kaggle_grape", True),
        ("data/raw/scraped/kaggle/plantvillage_v1", "kaggle_pv1", False),
        ("data/raw/scraped/kaggle/plantvillage_v2/plantvillage dataset/color", "kaggle_pv2", False),
    ]

    total_scanned = 0
    total_staged = 0
    class_stats: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))

    logger.info("=" * 70)
    logger.info("Scanning scraped sources...")

    for src_rel, prefix, is_grape in sources:
        src_path = PROJECT_ROOT / src_rel
        if not src_path.exists():
            logger.info("Source not found, skipping: %s", src_rel)
            continue

        matched = collect_source_files(
            src_dir=src_path,
            source_prefix=prefix,
            train_classes_set=train_classes_set,
            max_per_class=max_per_class,
            is_grape_special=is_grape,
        )

        source_total = sum(len(v) for v in matched.values())
        logger.info("Source: %-45s -> %5d matched images across %2d classes", src_rel, source_total, len(matched))

        # Stage or copy files
        for cls_name, files in matched.items():
            target_class_dir = dest_dir / cls_name
            for src_file in files:
                dest_file_name = f"{prefix}_{src_file.name}"
                dest_file_path = target_class_dir / dest_file_name

                # Respect class limit in destination
                current_total = sum(class_stats[cls_name].values())
                if current_total >= max_per_class:
                    break

                if not dry_run:
                    if not dest_file_path.exists():
                        shutil.copy2(src_file, dest_file_path)

                class_stats[cls_name][prefix] += 1
                total_staged += 1

    mode_str = "[DRY-RUN] " if dry_run else ""
    logger.info("=" * 70)
    logger.info("%sConsolidation Complete!", mode_str)
    logger.info("Total images staged into unified raw folder: %d", total_staged)
    logger.info("Classes enriched: %d / %d", len(class_stats), len(train_classes))
    logger.info("=" * 70)

    # Print top enriched classes
    print("\nSummary of classes enriched in unified raw folder:")
    print(f"{'Class Name':<50} | {'Total Ingested':<15} | {'Source Breakdown'}")
    print("-" * 90)
    for cls_name in sorted(class_stats.keys()):
        counts = class_stats[cls_name]
        total = sum(counts.values())
        breakdown = ", ".join(f"{k}: {v}" for k, v in counts.items())
        print(f"{cls_name:<50} | {total:<15} | {breakdown}")


if __name__ == "__main__":
    main()
