"""
scripts/ingest_scraped.py — Ingest verified scraped images into the training set.

Reads one or more scrape manifests, filters to rows where kept=True,
and copies each image into data/processed/train/<class_name>/ so the
existing get_dataloaders() pipeline picks them up automatically.

Rules:
- Only copies images where kept == True (passed scraper's quality filter)
- Skips any class folder that does not exist in data/processed/train/
  (prevents creating new classes that would break val/test consistency)
- Skips files that already exist at destination (idempotent)
- Verifies source file exists and is not zero bytes
- Logs a comprehensive per-class and total summary

Usage:
    # Ingest iNaturalist scraped_v2 (default)
    python scripts/ingest_scraped.py

    # Dry-run first to check
    python scripts/ingest_scraped.py --dry-run

    # Specify a custom manifest
    python scripts/ingest_scraped.py --manifest data/scraped_v2/scrape_manifest_inat.csv

    # Ingest all available manifests (v1 and v2)
    python scripts/ingest_scraped.py --all
"""

import argparse
import logging
import os
import shutil
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_MANIFEST_V2 = PROJECT_ROOT / "data" / "scraped_v2" / "scrape_manifest_inat.csv"
DEFAULT_MANIFEST_V1 = PROJECT_ROOT / "data" / "scraped" / "scrape_manifest.csv"
TRAIN_DIR = PROJECT_ROOT / "data" / "processed" / "train"

logger = logging.getLogger("ingest_scraped")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Ingest scraped images into training set")
    p.add_argument(
        "--manifest",
        type=str,
        default=None,
        help="Path to manifest CSV. Defaults to scraped_v2 if available, else scraped v1.",
    )
    p.add_argument(
        "--all",
        action="store_true",
        help="Ingest from all discovered manifests in sequence.",
    )
    p.add_argument(
        "--dest-dir",
        type=str,
        default=str(TRAIN_DIR),
        help="Target directory for training classes (default: data/processed/train)",
    )
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would be copied without writing files to disk",
    )
    return p.parse_args()


def ingest_manifest(manifest_path: Path, dest_dir: Path, dry_run: bool = False) -> int:
    """Ingests kept images from a given manifest path into dest_dir."""
    if not manifest_path.exists():
        logger.error("Manifest not found: %s", manifest_path)
        return 0

    logger.info("=" * 75)
    logger.info("Reading manifest: %s", manifest_path)
    df = pd.read_csv(manifest_path)
    total_rows = len(df)

    if "kept" not in df.columns:
        logger.error("Manifest does not contain 'kept' column: %s", manifest_path)
        return 0

    # Filter to kept == True
    kept = df[df["kept"] == True].copy()  # noqa: E712
    if len(kept) == 0:
        kept = df[df["kept"].astype(str).str.strip().str.lower() == "true"].copy()

    logger.info("Found %d kept images out of %d rows in %s", len(kept), total_rows, manifest_path.name)

    # Validate target classes
    dest_classes = {d.name for d in dest_dir.iterdir() if d.is_dir()} if dest_dir.exists() else set()

    stats: dict[str, dict] = {}
    copied_count = 0

    for _, row in kept.iterrows():
        class_name = str(row["class"]).strip()
        filename = str(row["filename"]).strip()

        # Normalise path across Windows / POSIX
        norm_path = filename.replace("\\", "/")
        src_path = PROJECT_ROOT / Path(norm_path)

        s = stats.setdefault(class_name, {"copied": 0, "skipped_exists": 0, "skipped_no_folder": 0, "missing": 0})

        if not src_path.exists() or src_path.stat().st_size == 0:
            s["missing"] += 1
            continue

        if class_name not in dest_classes:
            s["skipped_no_folder"] += 1
            continue

        target_dir = dest_dir / class_name
        dest_path = target_dir / src_path.name

        if dest_path.exists():
            s["skipped_exists"] += 1
            continue

        if dry_run:
            s["copied"] += 1
            copied_count += 1
        else:
            target_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src_path, dest_path)
            s["copied"] += 1
            copied_count += 1

    # Print table
    mode = "[DRY RUN] " if dry_run else ""
    logger.info("")
    logger.info("%sIngestion summary for %s:", mode, manifest_path.name)
    logger.info("%-55s %8s %8s %8s %8s", "Class", "Copied", "Exists", "NoFldr", "Missing")
    logger.info("-" * 90)

    for cls, s in sorted(stats.items()):
        logger.info(
            "%-55s %8d %8d %8d %8d",
            cls, s["copied"], s["skipped_exists"], s["skipped_no_folder"], s["missing"],
        )

    logger.info("-" * 90)
    logger.info("%sTotal copied from %s: %d", mode, manifest_path.name, copied_count)
    logger.info("=" * 75)
    return copied_count


def main() -> None:
    args = parse_args()
    dest_dir = Path(args.dest_dir).resolve()

    if not dest_dir.exists():
        raise FileNotFoundError(f"Destination directory does not exist: {dest_dir}")

    manifest_list: list[Path] = []
    if args.all:
        for p in [DEFAULT_MANIFEST_V1, DEFAULT_MANIFEST_V2]:
            if p.exists():
                manifest_list.append(p)
    elif args.manifest:
        manifest_list.append(Path(args.manifest).resolve())
    else:
        # Default to v2 if available, else v1
        if DEFAULT_MANIFEST_V2.exists():
            manifest_list.append(DEFAULT_MANIFEST_V2)
        elif DEFAULT_MANIFEST_V1.exists():
            manifest_list.append(DEFAULT_MANIFEST_V1)
        else:
            raise FileNotFoundError(f"No default manifests found at {DEFAULT_MANIFEST_V2} or {DEFAULT_MANIFEST_V1}")

    grand_total = 0
    for m in manifest_list:
        grand_total += ingest_manifest(m, dest_dir, dry_run=args.dry_run)

    mode = "[DRY RUN] " if args.dry_run else ""
    logger.info("%sGrand total images %s: %d", mode, "to be copied" if args.dry_run else "copied", grand_total)
    if not args.dry_run and grand_total > 0:
        logger.info("Ingestion complete! All images are now in %s", dest_dir)
        logger.info("Next step: Proceed to fine-tuning or class weight calibration.")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)-8s %(message)s",
    )
    main()
