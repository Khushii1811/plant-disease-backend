"""
scripts/ingest_mendeley_cauliflower_healthy.py — Ingest Mendeley Cauliflower Healthy Leaf dataset.

Handles both unzipped folders and downloaded .zip files from Mendeley Data.

Usage:
  python scripts/ingest_mendeley_cauliflower_healthy.py
  (Auto-detects Cauliflower zip or extracted folder in Downloads or data/)
  
  or specify exact path:
  python scripts/ingest_mendeley_cauliflower_healthy.py --source "C:/path/to/Cauliflower.zip"
"""

import argparse
import os
import random
import shutil
import sys
import zipfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
QUARANTINE_DIR = PROJECT_ROOT / "data" / "quarantine_old_cauliflower_healthy"
TEMP_EXTRACT_DIR = PROJECT_ROOT / "data" / "raw" / "mendeley_cauliflower_extracted"

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".webp", ".tif", ".tiff"}


def find_source_folder_or_zip(user_path: str = None) -> Path:
    """Find the Mendeley healthy leaf folder or zip file."""
    if user_path:
        p = Path(user_path)
        if p.exists():
            return p
        raise FileNotFoundError(f"Provided path not found: {user_path}")

    # Search common download locations
    candidates = [
        Path.home() / "Downloads",
        PROJECT_ROOT / "data" / "raw",
        PROJECT_ROOT / "data",
    ]

    # First search for extracted folders
    for base in candidates:
        if not base.exists():
            continue
        for p in base.rglob("*"):
            if p.is_dir():
                name_lower = p.name.lower()
                parent_lower = p.parent.name.lower()
                if "healthy" in name_lower and ("cauliflower" in parent_lower or "leaf" in parent_lower or "categorie" in parent_lower or "categories" in parent_lower):
                    imgs = [f for f in p.glob("*.*") if f.suffix.lower() in IMAGE_EXTS]
                    if len(imgs) > 5:
                        return p

    # Second search for .zip files in Downloads or data
    for base in candidates:
        if not base.exists():
            continue
        for z in base.glob("*.zip"):
            zn = z.name.lower()
            if "cauliflower" in zn or "x26px3xnmy" in zn or "leaf" in zn or "dataset" in zn:
                return z

    return None


def main():
    parser = argparse.ArgumentParser(description="Replace Cauliflower Healthy with Mendeley dataset")
    parser.add_argument(
        "--source",
        type=str,
        default="",
        help="Path to downloaded .zip or extracted 'Healthy' folder",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed for 80/10/10 split (default: 42)",
    )
    args = parser.parse_args()

    found_path = find_source_folder_or_zip(args.source)
    if not found_path:
        print("\n❌ Could not automatically find the Mendeley Cauliflower file or folder.")
        print("Please download the dataset from:")
        print("  👉 https://data.mendeley.com/datasets/x26px3xnmy/1")
        print("Then place the .zip in your Downloads folder and run:")
        print("  python scripts/ingest_mendeley_cauliflower_healthy.py\n")
        sys.exit(1)

    # If it is a zip file, extract it to temporary folder
    if found_path.is_file() and found_path.suffix.lower() == ".zip":
        print(f"📦 Found archive: {found_path}")
        print(f"Extracting archive to {TEMP_EXTRACT_DIR}...")
        TEMP_EXTRACT_DIR.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(found_path, "r") as zf:
            zf.extractall(TEMP_EXTRACT_DIR)

        # Unzip any nested zips
        for nested in TEMP_EXTRACT_DIR.rglob("*.zip"):
            try:
                with zipfile.ZipFile(nested, "r") as nzf:
                    nzf.extractall(nested.parent)
            except Exception:
                pass

        # Locate Leaf Categories / Healthy folder
        healthy_dir = None
        for p in TEMP_EXTRACT_DIR.rglob("*"):
            if p.is_dir():
                name_low = p.name.lower()
                parent_low = p.parent.name.lower()
                if "healthy" in name_low and ("leaf" in parent_low or "categorie" in parent_low or "categories" in parent_low):
                    healthy_dir = p
                    break
        
        if not healthy_dir:
            for p in TEMP_EXTRACT_DIR.rglob("*"):
                if p.is_dir() and "healthy" in p.name.lower() and "leaf" in str(p).lower():
                    healthy_dir = p
                    break

        if not healthy_dir:
            print("❌ Extracted archive, but could not locate 'Leaf Categories/Healthy' folder inside.")
            sys.exit(1)
        src_dir = healthy_dir
    else:
        src_dir = found_path

    print(f"\n📂 Source Healthy Leaf Folder: {src_dir}")
    source_images = sorted([f for f in src_dir.glob("*.*") if f.suffix.lower() in IMAGE_EXTS])
    print(f"Found {len(source_images)} clean healthy images.")

    if len(source_images) < 5:
        print("❌ Not enough images found in source folder.")
        sys.exit(1)

    # Step 1: Safely quarantine old images
    QUARANTINE_DIR.mkdir(parents=True, exist_ok=True)
    quarantined_count = 0

    for split in ["train", "val", "test"]:
        old_dir = PROCESSED_DIR / split / "Cauliflower - Healthy"
        if old_dir.exists():
            for f in list(old_dir.glob("*.*")):
                target_q = QUARANTINE_DIR / split / "Cauliflower - Healthy"
                target_q.mkdir(parents=True, exist_ok=True)
                shutil.move(str(f), str(target_q / f.name))
                quarantined_count += 1
            old_dir.mkdir(parents=True, exist_ok=True)
        else:
            old_dir.mkdir(parents=True, exist_ok=True)

    print(f"🔒 Safely moved {quarantined_count} old images to quarantine ({QUARANTINE_DIR})")

    # Step 2: Split 80 / 10 / 10
    random.seed(args.seed)
    shuffled = source_images.copy()
    random.shuffle(shuffled)

    n_total = len(shuffled)
    n_val = max(15, int(n_total * 0.10)) if n_total >= 50 else max(3, int(n_total * 0.10))
    n_test = max(15, int(n_total * 0.10)) if n_total >= 50 else max(3, int(n_total * 0.10))
    n_train = n_total - n_val - n_test

    train_imgs = shuffled[:n_train]
    val_imgs = shuffled[n_train:n_train + n_val]
    test_imgs = shuffled[n_train + n_val:]

    print(f"\n📊 Split Distribution (Total: {n_total}):")
    print(f"  • Train: {len(train_imgs)} images ({len(train_imgs)/n_total*100:.1f}%)")
    print(f"  • Val  : {len(val_imgs)} images ({len(val_imgs)/n_total*100:.1f}%)")
    print(f"  • Test : {len(test_imgs)} images ({len(test_imgs)/n_total*100:.1f}%)")

    # Step 3: Copy into data/processed/
    def copy_split(img_list, split_name):
        dest_dir = PROCESSED_DIR / split_name / "Cauliflower - Healthy"
        dest_dir.mkdir(parents=True, exist_ok=True)
        for i, src_f in enumerate(img_list, 1):
            dest_file = dest_dir / f"cauliflower_healthy_mendeley_{split_name}_{i:05d}{src_f.suffix.lower()}"
            shutil.copy2(str(src_f), str(dest_file))

    copy_split(train_imgs, "train")
    copy_split(val_imgs, "val")
    copy_split(test_imgs, "test")

    print("\n✅ Successfully replaced Cauliflower - Healthy with clean Mendeley data!")

    # Step 4: Refresh counts
    try:
        from scripts.generate_dataset_counts import main as refresh_counts
        refresh_counts()
    except Exception as e:
        print("Note: Count refresh error:", e)


if __name__ == "__main__":
    main()
