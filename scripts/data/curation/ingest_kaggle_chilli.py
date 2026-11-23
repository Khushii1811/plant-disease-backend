"""
scripts/ingest_kaggle_chilli.py — Standalone extractor and ingestor for Kaggle Chilli Dataset.
Extracts classes, applies group-aware leak-free 80/10/10 splits, and safely quarantines old Chilli classes.
"""

import argparse
import os
import random
import re
import shutil
import sys
import zipfile
from collections import defaultdict
from pathlib import Path

try:
    from tqdm import tqdm
except ImportError:
    tqdm = None

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
QUARANTINE_DIR = PROJECT_ROOT / "data" / "quarantine_old_chilli"
TEMP_DOWNLOAD_DIR = PROJECT_ROOT / "data" / "raw" / "kaggle_chilli_download"
DOWNLOADS_DIR = Path.home() / "Downloads"

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".webp", ".tif", ".tiff"}

CLASS_MAPPING = {
    "bacterial": "Chilli - Bacterial Spot",
    "cercospora": "Chilli - Cercospora Leaf Spot",
    "curl": "Chilli - Leaf Curl Virus",
    "deficiency": "Chilli - Nutrition Deficiency",
    "nutrient": "Chilli - Nutrition Deficiency",
    "white": "Chilli - White Spot",
    "healthy": "Chilli - Healthy",
}


def extract_base_leaf_id(filename: str) -> str:
    """Extract root leaf ID so augmented variants of the same leaf stay in the same split."""
    stem = Path(filename).stem
    match = re.match(r"^(.*?)(?:_bright|_flipped|_rotated|_sheared|_shifted|_zoomed|_aug|\(\d+\)|_\d+$)", stem, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return stem


def find_downloaded_archive(user_path: str = None) -> Path:
    """Finds downloaded .zip or extracted folder in known download locations."""
    if user_path and Path(user_path).exists():
        return Path(user_path)

    candidates = [
        TEMP_DOWNLOAD_DIR,
        DOWNLOADS_DIR,
        PROJECT_ROOT / "data" / "raw",
    ]

    for base in candidates:
        if not base.exists():
            continue
        # Check for zip
        for z in base.glob("*.zip"):
            zn = z.name.lower()
            if "chilli" in zn or "chili" in zn:
                return z

        # Check for extracted folder
        for p in base.glob("*"):
            if p.is_dir() and ("chilli" in p.name.lower() or "chili" in p.name.lower()):
                subdirs = [s.name.lower() for s in p.iterdir() if s.is_dir()]
                if any(k in " ".join(subdirs) for k in ["bacterial", "curl", "white", "cercospora", "deficiency"]):
                    return p

    return None


def main():
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass

    parser = argparse.ArgumentParser(description="Ingest Kaggle Chilli Dataset with Leak-Free Splits")
    parser.add_argument("--source", type=str, default="", help="Path to zip or extracted folder")
    parser.add_argument("--keep_anthracnose", action="store_true", default=True, help="Keep existing Chilli - Anthracnose class")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for splitting (default: 42)")
    args = parser.parse_args()

    archive_path = find_downloaded_archive(args.source)
    if not archive_path:
        print("\n[ERROR] Could not find the downloaded Chilli archive or extracted folder.")
        print("Please run the downloader first:")
        print("  python scripts/download_kaggle_chilli.py\n")
        sys.exit(1)

    print("=" * 65)
    print(f"  🌱  INGESTING CHILLI DATASET FROM: {archive_path.name}")
    print("=" * 65)

    # Step 1: Extraction
    extract_dir = TEMP_DOWNLOAD_DIR / "extracted"
    if archive_path.is_file() and archive_path.suffix.lower() == ".zip":
        extract_dir.mkdir(parents=True, exist_ok=True)
        print(f"\n[INFO] Extracting archive {archive_path.name}...")
        with zipfile.ZipFile(archive_path, 'r') as zf:
            members = [m for m in zf.infolist() if not m.is_dir() and Path(m.filename).suffix.lower() in IMAGE_EXTS]
            if tqdm:
                with tqdm(total=len(members), desc="Extracting images", unit="img") as pbar:
                    for member in members:
                        zf.extract(member, extract_dir)
                        pbar.update(1)
            else:
                zf.extractall(extract_dir)
        search_root = extract_dir
    else:
        search_root = archive_path

    # Step 2: Index and map classes
    print("\n[INFO] Indexing classes and grouping unique leaves...")
    discovered_classes = defaultdict(list)
    for p in search_root.rglob("*"):
        if p.is_dir():
            folder_name_low = p.name.lower()
            matched_target = None
            for key, target_name in CLASS_MAPPING.items():
                if key in folder_name_low:
                    matched_target = target_name
                    break
            if matched_target:
                imgs = [f for f in p.glob("*.*") if f.suffix.lower() in IMAGE_EXTS]
                if imgs:
                    discovered_classes[matched_target].extend(imgs)

    print("\nDiscovered classes:")
    for cname, imgs in sorted(discovered_classes.items()):
        unique_ids = set(extract_base_leaf_id(f.name) for f in imgs)
        print(f"  • {cname}: {len(imgs)} images ({len(unique_ids)} unique leaves)")

    # Step 3: Quarantine old classes
    print("\n[INFO] Quarantining old Chilli classes...")
    QUARANTINE_DIR.mkdir(parents=True, exist_ok=True)
    quarantined_count = 0

    classes_to_quarantine = ["Chilli - Healthy", "Chilli - Leafcurl", "Chilli - Leafspot", "Chilli - Whitefly", "Chilli - Yellowish"]
    if not args.keep_anthracnose:
        classes_to_quarantine.append("Chilli - Anthracnose")

    for split in ["train", "val", "test"]:
        split_dir = PROCESSED_DIR / split
        if split_dir.exists():
            for folder_name in classes_to_quarantine:
                target_folder = split_dir / folder_name
                if target_folder.exists():
                    target_q = QUARANTINE_DIR / split / folder_name
                    target_q.mkdir(parents=True, exist_ok=True)
                    for f in list(target_folder.glob("*.*")):
                        shutil.move(str(f), str(target_q / f.name))
                        quarantined_count += 1
                    try:
                        target_folder.rmdir()
                    except Exception:
                        pass

    print(f"Safely backed up {quarantined_count} old images into: {QUARANTINE_DIR}")
    if args.keep_anthracnose:
        print("ℹ️  Preserved: 'Chilli - Anthracnose' remains active in dataset.")

    # Step 4: Split & copy
    print("\n[INFO] Creating 80% train / 10% val / 10% test leak-free splits...")
    random.seed(args.seed)

    for target_class, img_list in sorted(discovered_classes.items()):
        leaf_groups = defaultdict(list)
        for img_path in img_list:
            base_id = extract_base_leaf_id(img_path.name)
            leaf_groups[base_id].append(img_path)

        unique_leaf_ids = sorted(list(leaf_groups.keys()))
        random.shuffle(unique_leaf_ids)

        n_leaves = len(unique_leaf_ids)
        n_val_leaves = max(2, int(n_leaves * 0.10))
        n_test_leaves = max(2, int(n_leaves * 0.10))
        n_train_leaves = n_leaves - n_val_leaves - n_test_leaves

        train_ids = set(unique_leaf_ids[:n_train_leaves])
        val_ids = set(unique_leaf_ids[n_train_leaves:n_train_leaves + n_val_leaves])
        test_ids = set(unique_leaf_ids[n_train_leaves + n_val_leaves:])

        train_files = [f for lid in train_ids for f in leaf_groups[lid]]
        val_files = [f for lid in val_ids for f in leaf_groups[lid]]
        test_files = [f for lid in test_ids for f in leaf_groups[lid]]

        for split_name, flist in [("train", train_files), ("val", val_files), ("test", test_files)]:
            dest_dir = PROCESSED_DIR / split_name / target_class
            dest_dir.mkdir(parents=True, exist_ok=True)
            for idx, src_file in enumerate(flist, 1):
                ext = src_file.suffix.lower()
                clean_name = f"{target_class.replace(' ', '_').lower()}_{split_name}_{idx:05d}{ext}"
                shutil.copy2(str(src_file), str(dest_dir / clean_name))

        print(f"✅ {target_class}:")
        print(f"   Train: {len(train_files)} imgs | Val: {len(val_files)} imgs | Test: {len(test_files)} imgs (Total Unique Leaves: {n_leaves})")

    # Step 5: Refresh counts
    print("\n[INFO] Refreshing dataset counts...")
    try:
        from scripts.generate_dataset_counts import main as refresh_counts
        refresh_counts()
    except Exception:
        pass

    print("\n[SUCCESS] Chilli dataset fully ingested and split with zero data leakage!")


if __name__ == "__main__":
    main()
