"""
One-time setup script: reads the Kaggle "Master Plant Disease" dataset's
train/val/test manifest CSVs, cleans up duplicate class labels (whitespace and
search-engine-suffix artifacts), and copies each image into a standard
ImageFolder-compatible directory structure:

    data/processed/train/<clean_class_name>/<image>.jpg
    data/processed/val/<clean_class_name>/<image>.jpg
    data/processed/test/<clean_class_name>/<image>.jpg

This lets the rest of the pipeline (src/data/dataset.py) use torchvision's
ImageFolder unchanged, instead of writing a custom manifest-reading Dataset.

Usage:
    python scripts/organize_data.py
"""

import logging
import re
import shutil
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

IMAGES_BASE_DIR = RAW_DIR / "master_images" / "master_images"
METADATA_DIR = RAW_DIR / "outputs" / "outputs"

TRAIN_MANIFEST = METADATA_DIR / "train_split.csv"
VAL_MANIFEST = METADATA_DIR / "val_split.csv"
TEST_MANIFEST = METADATA_DIR / "test_split.csv"

# Suffixes added during data collection to indicate which search engine an
# image was sourced from (Bing/Google/Baidu) — these don't represent real
# class distinctions and should be stripped so duplicate classes merge.
SOURCE_ENGINE_SUFFIX_PATTERN = re.compile(r"\s+(Bing|Google|Baidu)\s*$", re.IGNORECASE)

logger = logging.getLogger(__name__)


def clean_class_name(raw_name: str) -> str:
    """
    Normalize a canonical_class label by stripping whitespace and removing
    trailing search-engine-source suffixes, so that near-duplicate labels
    (e.g. "Banana - banana anthracnose Bing" and "... Google") merge into
    a single class.

    Args:
        raw_name: The raw canonical_class value from the manifest CSV.

    Returns:
        A cleaned class name suitable for use as a folder name.
    """
    name = raw_name.strip()
    name = SOURCE_ENGINE_SUFFIX_PATTERN.sub("", name)
    name = name.strip()
    # Replace characters that are problematic in folder names.
    name = name.replace("/", "-").replace("\\", "-")
    return name


def organize_split(manifest_path: Path, split_name: str) -> None:
    """
    Read a manifest CSV and copy each listed image into
    data/processed/<split_name>/<clean_class_name>/.

    Args:
        manifest_path: Path to train_split.csv or test_split.csv.
        split_name: Either "train" or "test" — used as the output subfolder.

    Raises:
        FileNotFoundError: If the manifest or an individual image is missing.
    """
    if not manifest_path.exists():
        raise FileNotFoundError(f"Manifest not found: {manifest_path}")

    manifest = pd.read_csv(manifest_path)
    logger.info("Processing %s split: %d rows", split_name, len(manifest))

    split_output_dir = PROCESSED_DIR / split_name
    copied, skipped = 0, 0

    for _, row in manifest.iterrows():
        clean_name = clean_class_name(row["canonical_class"])
        class_dir = split_output_dir / clean_name
        class_dir.mkdir(parents=True, exist_ok=True)

        source_path = IMAGES_BASE_DIR / row["image_path"]
        dest_path = class_dir / Path(row["image_path"]).name

        if not source_path.exists():
            logger.warning("Missing source image, skipping: %s", source_path)
            skipped += 1
            continue

        shutil.copy2(source_path, dest_path)
        copied += 1

        if copied % 5000 == 0:
            logger.info("  ...%d images copied so far", copied)

    logger.info(
        "%s split done: %d copied, %d skipped (missing files)",
        split_name, copied, skipped,
    )


def main() -> None:
    organize_split(TRAIN_MANIFEST, "train")
    organize_split(VAL_MANIFEST, "val")
    organize_split(TEST_MANIFEST, "test")

    train_classes = {p.name for p in (PROCESSED_DIR / "train").iterdir() if p.is_dir()}
    val_classes = {p.name for p in (PROCESSED_DIR / "val").iterdir() if p.is_dir()}
    test_classes = {p.name for p in (PROCESSED_DIR / "test").iterdir() if p.is_dir()}

    logger.info(
        "Final class count — train: %d, val: %d, test: %d",
        len(train_classes), len(val_classes), len(test_classes),
    )

    mismatch = train_classes.symmetric_difference(test_classes)
    if mismatch:
        logger.warning(
            "%d classes appear in only one split (train or test), not both: %s",
            len(mismatch), sorted(mismatch),
        )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    main()
