"""
scripts/ingest_plantdoc.py — Ingest PlantDoc dataset images for under-represented classes.

PlantDoc is an open academic dataset (CC-BY 4.0) containing 2,569 natural-condition
plant disease images. This script maps relevant classes from PlantDoc to our target taxonomy,
applies perceptual hash deduplication to avoid duplicates, and ingests them into the training set.

Usage:
    python scripts/ingest_plantdoc.py [--dry-run]
"""

import argparse
import csv
import logging
import shutil
from pathlib import Path
from PIL import Image
import imagehash

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PLANTDOC_DIR = PROJECT_ROOT / "data" / "plantdoc_raw"
TRAIN_DIR = PROJECT_ROOT / "data" / "processed" / "train"
OUT_MANIFEST = PROJECT_ROOT / "data" / "scraped_v2" / "scrape_manifest_plantdoc.csv"
PREV_MANIFESTS = [
    PROJECT_ROOT / "data" / "scraped_v2" / "scrape_manifest_inat.csv",
    PROJECT_ROOT / "data" / "scraped" / "scrape_manifest.csv",
]

MIN_RESOLUTION = 150
PHASH_THRESHOLD = 10

logger = logging.getLogger("ingest_plantdoc")

# Direct mapping from PlantDoc folder names to our 181-class taxonomy
PLANTDOC_MAPPING: dict[str, str] = {
    "Corn leaf blight": "Corn - Leaf Blight",
    "Bell_pepper leaf spot": "Bell pepper - bell pepper frogeye leaf spot",
    "Corn Gray leaf spot": "Corn - corn gray leaf spot",
    "Tomato Septoria leaf spot": "Tomato - tomato septoria leaf spot",
    "Tomato Early blight leaf": "Tomato - tomato early blight",
    "Corn rust leaf": "Corn - Rust",
    "Potato leaf early blight": "Potato - potato early blight",
    "Potato leaf late blight": "Potato - potato late blight",
    "Squash Powdery mildew leaf": "Squash - Powdery Mildew",
    "Tomato leaf bacterial spot": "Tomato - tomato bacterial spot",
    "Tomato leaf late blight": "Tomato - tomato late blight",
    "Tomato leaf mosaic virus": "Tomato - tomato mosaic virus",
    "Tomato leaf yellow virus": "Tomato - tomato yellow leaf curl virus",
    "Apple Scab Leaf": "Apple - apple scab",
    "Apple rust leaf": "Apple - Rust",
    "grape leaf black rot": "Grape - Black Rot",
}


def load_existing_hashes() -> set[str]:
    seen: set[str] = set()
    for mpath in PREV_MANIFESTS:
        if not mpath.exists():
            continue
        try:
            with open(mpath, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row.get("kept") in (True, "True", "true"):
                        # If manifest recorded phash, or calculate on demand
                        ph = row.get("phash", "").strip()
                        if ph:
                            seen.add(ph)
        except Exception as e:
            logger.warning("Error reading manifest %s: %s", mpath, e)
    return seen


def is_duplicate(img_hash: str, seen_hashes: set[str], threshold: int = PHASH_THRESHOLD) -> bool:
    h = imagehash.hex_to_hash(img_hash)
    for s in seen_hashes:
        try:
            if h - imagehash.hex_to_hash(s) < threshold:
                return True
        except Exception:
            continue
    return False


def main() -> None:
    parser = argparse.ArgumentParser(description="Ingest PlantDoc images into training set")
    parser.add_argument("--dry-run", action="store_true", help="Simulate without copying files")
    args = parser.parse_args()

    if not PLANTDOC_DIR.exists():
        logger.error("PlantDoc directory not found at: %s", PLANTDOC_DIR)
        return

    dest_classes = {d.name for d in TRAIN_DIR.iterdir() if d.is_dir()}
    seen_hashes = load_existing_hashes()
    logger.info("Loaded %d existing phashes for cross-deduplication", len(seen_hashes))

    manifest_rows = []
    stats: dict[str, dict] = {}

    # Scan both train and test subdirectories of PlantDoc
    subdirs = [PLANTDOC_DIR / "train", PLANTDOC_DIR / "test"]

    for subdir in subdirs:
        if not subdir.exists():
            continue
        for pd_class_dir in subdir.iterdir():
            if not pd_class_dir.is_dir():
                continue
            pd_name = pd_class_dir.name
            if pd_name not in PLANTDOC_MAPPING:
                continue

            target_class = PLANTDOC_MAPPING[pd_name]
            s = stats.setdefault(target_class, {"copied": 0, "rejected_res": 0, "rejected_phash": 0, "exists": 0})

            if target_class not in dest_classes:
                logger.warning("Target class %s not found in train dir!", target_class)
                continue

            dest_folder = TRAIN_DIR / target_class
            image_files = sorted(list(pd_class_dir.glob("*.jpg")) + list(pd_class_dir.glob("*.png")) + list(pd_class_dir.glob("*.jpeg")))

            for img_path in image_files:
                try:
                    with Image.open(img_path) as img:
                        w, h = img.size
                        if w < MIN_RESOLUTION or h < MIN_RESOLUTION:
                            s["rejected_res"] += 1
                            manifest_rows.append({"class": target_class, "source_file": str(img_path), "kept": False, "reason": "low_res"})
                            continue

                        cur_hash = str(imagehash.phash(img))
                        if is_duplicate(cur_hash, seen_hashes):
                            s["rejected_phash"] += 1
                            manifest_rows.append({"class": target_class, "source_file": str(img_path), "kept": False, "reason": "phash_dup"})
                            continue

                        dest_file = dest_folder / f"img_plantdoc_{img_path.name}"
                        if dest_file.exists():
                            s["exists"] += 1
                            continue

                        seen_hashes.add(cur_hash)
                        if not args.dry_run:
                            dest_folder.mkdir(parents=True, exist_ok=True)
                            shutil.copy2(img_path, dest_file)

                        s["copied"] += 1
                        manifest_rows.append({
                            "class": target_class,
                            "source_file": str(img_path),
                            "phash": cur_hash,
                            "kept": True,
                            "reason": "",
                            "filename": str(dest_file.relative_to(PROJECT_ROOT))
                        })

                except Exception as e:
                    logger.debug("Error processing %s: %s", img_path, e)

    # Save manifest
    if not args.dry_run and manifest_rows:
        OUT_MANIFEST.parent.mkdir(parents=True, exist_ok=True)
        with open(OUT_MANIFEST, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["class", "source_file", "phash", "kept", "reason", "filename"])
            writer.writeheader()
            writer.writerows(manifest_rows)

    # Summary
    mode = "[DRY RUN] " if args.dry_run else ""
    logger.info("")
    logger.info("=" * 80)
    logger.info("%sPlantDoc Ingestion Summary:", mode)
    logger.info("%-50s %8s %8s %8s %8s", "Class", "Copied", "Exists", "LowRes", "DupPhash")
    logger.info("-" * 80)
    total_copied = 0
    for cls, s in sorted(stats.items()):
        logger.info("%-50s %8d %8d %8d %8d", cls, s["copied"], s["exists"], s["rejected_res"], s["rejected_phash"])
        total_copied += s["copied"]
    logger.info("=" * 80)
    logger.info("%sTotal images copied from PlantDoc: %d", mode, total_copied)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)-8s %(message)s")
    main()
