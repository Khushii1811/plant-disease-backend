"""
scripts/ingest_kaggle_chilli_classes.py — Ingest and clean the Chilli dataset from Kaggle (suryiapooventhanr/chilli),
safely quarantining old Chilli classes and building strict, leak-free 80/10/10 train/val/test splits.
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

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
QUARANTINE_DIR = PROJECT_ROOT / "data" / "quarantine_old_chilli"
DOWNLOADS_DIR = Path.home() / "Downloads"

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".webp", ".tif", ".tiff"}

# Desired normalized class names mapped from folder keywords
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
    """
    Extracts the root leaf ID to group augmented variations (_bright, _flipped, _rotated, _sheared, _zoomed, _shifted)
    together, ensuring the same physical leaf never leaks across Train, Val, and Test splits.
    """
    stem = Path(filename).stem
    # Match patterns like "Bacterial Spot00001_bright_3" -> "Bacterial Spot00001"
    match = re.match(r"^(.*?)(?:_bright|_flipped|_rotated|_sheared|_shifted|_zoomed|_aug|\(\d+\)|_\d+$)", stem, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return stem


def find_dataset_source(user_path: str = None) -> Path:
    """Finds unzipped folder or .zip file for the chilli dataset."""
    if user_path:
        p = Path(user_path)
        if p.exists():
            return p
        raise FileNotFoundError(f"Source not found: {user_path}")

    candidates = [
        DOWNLOADS_DIR,
        PROJECT_ROOT / "data" / "raw",
        PROJECT_ROOT / "data",
        Path.home() / ".cache" / "kagglehub" / "datasets" / "suryiapooventhanr" / "chilli" / "versions",
    ]

    # Search for extracted directory
    for base in candidates:
        if not base.exists():
            continue
        for p in base.rglob("*"):
            if p.is_dir():
                name_low = p.name.lower()
                if "chili" in name_low or "chilli" in name_low:
                    # Check if it has disease subfolders
                    subdirs = [s.name.lower() for s in p.iterdir() if s.is_dir()]
                    if any(k in " ".join(subdirs) for k in ["bacterial", "curl", "white", "cercospora", "deficiency"]):
                        return p

    # Search for zip files
    for base in candidates:
        if not base.exists():
            continue
        for z in base.glob("*.zip"):
            zn = z.name.lower()
            if "chilli" in zn or "chili" in zn:
                return z

    return None


def main():
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass

    parser = argparse.ArgumentParser(description="Ingest Clean Chilli Classes with Leak-Free Splits")
    parser.add_argument("--source", type=str, default="", help="Path to zip or extracted folder")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for splitting")
    args = parser.parse_args()

    source = find_dataset_source(args.source)
    if not source:
        print("[ERROR] Could not find the Chilli dataset archive or extracted folder.")
        print("Please download from: https://www.kaggle.com/datasets/suryiapooventhanr/chilli")
        print(f"Place the zip in {DOWNLOADS_DIR} and rerun:")
        print("  python scripts/ingest_kaggle_chilli_classes.py")
        sys.exit(1)

    temp_extract = PROJECT_ROOT / "data" / "raw" / "chilli_extracted"
    if source.is_file() and source.suffix.lower() == ".zip":
        print(f"[INFO] Extracting archive {source.name}...")
        temp_extract.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(source, "r") as zf:
            zf.extractall(temp_extract)
        search_root = temp_extract
    else:
        search_root = source

    print(f"[INFO] Searching for class folders in {search_root}...")

    # Locate class folders
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

    if not discovered_classes:
        print("[ERROR] No matching Chilli disease classes found in dataset.")
        sys.exit(1)

    print("\n[DISCOVERED CLASSES]")
    for cname, imgs in sorted(discovered_classes.items()):
        print(f"  * {cname}: {len(imgs)} images")

    # Step 1: Safely quarantine old Chilli folders
    QUARANTINE_DIR.mkdir(parents=True, exist_ok=True)
    quarantined_count = 0

    for split in ["train", "val", "test"]:
        split_dir = PROCESSED_DIR / split
        if split_dir.exists():
            for folder in list(split_dir.glob("Chilli - *")):
                target_q = QUARANTINE_DIR / split / folder.name
                target_q.mkdir(parents=True, exist_ok=True)
                for f in folder.glob("*.*"):
                    shutil.move(str(f), str(target_q / f.name))
                    quarantined_count += 1
                # Remove empty folder
                try:
                    folder.rmdir()
                except Exception:
                    pass

    print(f"\n[INFO] Safely quarantined {quarantined_count} old images to {QUARANTINE_DIR}")

    # Step 2: Ingest each class with Leak-Free Group Splitting
    random.seed(args.seed)

    for target_class, img_list in sorted(discovered_classes.items()):
        # Group by base leaf ID to prevent data leakage
        leaf_groups = defaultdict(list)
        for img_path in img_list:
            base_id = extract_base_leaf_id(img_path.name)
            leaf_groups[base_id].append(img_path)

        unique_leaf_ids = list(leaf_groups.keys())
        random.shuffle(unique_leaf_ids)

        n_leaves = len(unique_leaf_ids)
        # Ensure at least 15 val & 15 test if sufficient images
        n_val_leaves = max(2, int(n_leaves * 0.10))
        n_test_leaves = max(2, int(n_leaves * 0.10))
        n_train_leaves = n_leaves - n_val_leaves - n_test_leaves

        train_ids = set(unique_leaf_ids[:n_train_leaves])
        val_ids = set(unique_leaf_ids[n_train_leaves:n_train_leaves + n_val_leaves])
        test_ids = set(unique_leaf_ids[n_train_leaves + n_val_leaves:])

        train_files = [f for lid in train_ids for f in leaf_groups[lid]]
        val_files = [f for lid in val_ids for f in leaf_groups[lid]]
        test_files = [f for lid in test_ids for f in leaf_groups[lid]]

        # Write to processed splits
        for split_name, flist in [("train", train_files), ("val", val_files), ("test", test_files)]:
            dest_dir = PROCESSED_DIR / split_name / target_class
            dest_dir.mkdir(parents=True, exist_ok=True)
            for idx, src_file in enumerate(flist, 1):
                ext = src_file.suffix.lower()
                clean_name = f"{target_class.replace(' ', '_').lower()}_{split_name}_{idx:05d}{ext}"
                shutil.copy2(str(src_file), str(dest_dir / clean_name))

        print(f"[INGESTED] {target_class}:")
        print(f"   Train: {len(train_files)} imgs | Val: {len(val_files)} imgs | Test: {len(test_files)} imgs (Total Unique Leaves: {n_leaves})")

    print("\n[SUCCESS] All Chilli classes cleanly ingested and split!")

    # Step 3: Refresh counts
    try:
        from generate_dataset_counts import main as refresh_counts
        refresh_counts()
    except Exception as e:
        print("[NOTE] Dataset count refresh:", e)


if __name__ == "__main__":
    main()
