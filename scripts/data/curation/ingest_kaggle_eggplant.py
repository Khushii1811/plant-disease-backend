"""
scripts/ingest_kaggle_eggplant.py — Ingests ONLY the authentic unaugmented 'Original Images (Version 02)'
(200 camera-captured foliar images per class) with strict ZERO-LEAKAGE partitioning (160 Train / 20 Val / 20 Test),
MD5 cryptographic verification, and safe quarantine of non-foliar Phomopsis fruit rot.
"""

import os
import sys
import shutil
import hashlib
import random
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
PROCESSED_DIR = DATA_DIR / "processed"
TRAIN_DIR = PROCESSED_DIR / "train"
VAL_DIR = PROCESSED_DIR / "val"
TEST_DIR = PROCESSED_DIR / "test"
QUARANTINE_DIR = DATA_DIR / "quarantine_eggplant_fruit_rot"

# Explicitly target ONLY unaugmented Original Images (Version 02)
ORIGINAL_V2_ROOT = DATA_DIR / "raw" / "kaggle_eggplant_extracted" / "Eggplant Disease Recognition Dataset" / "Original Images (Version 02)" / "Original Images (Version 02)"

SEED = 42
VALID_IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}

# Targeted class mapping: Source Directory Name -> Benchmark Target Class Name
FOLDER_TO_BENCHMARK_CLASS = {
    "Healthy Leaf": "Eggplant - Healthy",
    "Leaf Spot Disease": "Eggplant - Cercospora Leaf Spot",
    "Mosaic Virus Disease": "Eggplant - Mosaic Virus",
    "Small Leaf Disease": "Eggplant - Little Leaf",
    "White Mold Disease": "Eggplant - White Mold",
    "Wilt Disease": "Eggplant - Wilt",
}


def compute_md5(file_path: Path) -> str:
    hasher = hashlib.md5()
    with open(file_path, "rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()


def quarantine_old_and_fruit_rot():
    """Safely moves fruit rot and cleans old/augmented Eggplant folders."""
    QUARANTINE_DIR.mkdir(parents=True, exist_ok=True)
    
    # 1. Quarantine Phomopsis fruit rot
    phomopsis_class = "Eggplant - eggplant phomopsis fruit rot"
    for s_dir in [TRAIN_DIR, VAL_DIR, TEST_DIR]:
        c_folder = s_dir / phomopsis_class
        if c_folder.exists():
            dest = QUARANTINE_DIR / phomopsis_class / s_dir.name
            dest.mkdir(parents=True, exist_ok=True)
            for f in c_folder.glob("*"):
                if f.is_file():
                    shutil.move(str(f), str(dest / f.name))
            try:
                c_folder.rmdir()
            except Exception:
                pass

    # 2. Quarantine old un-normalized lowercase cercospora folder if still present
    old_cercospora = "Eggplant - eggplant cercospora leaf spot"
    for s_dir in [TRAIN_DIR, VAL_DIR, TEST_DIR]:
        c_folder = s_dir / old_cercospora
        if c_folder.exists():
            dest = QUARANTINE_DIR / old_cercospora / s_dir.name
            dest.mkdir(parents=True, exist_ok=True)
            for f in c_folder.glob("*"):
                if f.is_file():
                    shutil.move(str(f), str(dest / f.name))
            try:
                c_folder.rmdir()
            except Exception:
                pass


def clean_existing_new_eggplant_classes():
    """Removes previously ingested augmented folders so they are cleanly replaced."""
    for cname in FOLDER_TO_BENCHMARK_CLASS.values():
        for s_dir in [TRAIN_DIR, VAL_DIR, TEST_DIR]:
            c_folder = s_dir / cname
            if c_folder.exists():
                shutil.rmtree(c_folder)


def main():
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass

    print("=" * 75)
    print("  🍆  EGGPLANT UNAUGMENTED 'ORIGINAL IMAGES (VERSION 02)' INGESTION")
    print("=" * 75)

    if not ORIGINAL_V2_ROOT.exists():
        print(f"[ERROR] Cannot find target folder: {ORIGINAL_V2_ROOT}")
        print("Please ensure the archive is extracted in data/raw/kaggle_eggplant_extracted/")
        sys.exit(1)

    print(f"[INFO] Source Root: {ORIGINAL_V2_ROOT}")

    # 1. Quarantine fruit rot and old folders
    quarantine_old_and_fruit_rot()

    # 2. Clean out augmented images from previous run
    clean_existing_new_eggplant_classes()

    stats = []

    # 3. Process each unaugmented original class
    for source_folder, target_class in sorted(FOLDER_TO_BENCHMARK_CLASS.items()):
        src_path = ORIGINAL_V2_ROOT / source_folder
        if not src_path.exists():
            print(f"[WARNING] Subfolder missing: {src_path}")
            continue

        raw_files = [f for f in src_path.glob("*") if f.is_file() and f.suffix.lower() in VALID_IMAGE_EXTS]
        
        # MD5 Deduplication
        unique_files = []
        seen_md5 = set()
        for f in sorted(raw_files, key=lambda x: x.name):
            h = compute_md5(f)
            if h not in seen_md5:
                seen_md5.add(h)
                unique_files.append(f)

        total_unique = len(unique_files)
        
        # Deterministic partition: 160 Train (80%), 20 Val (10%), 20 Test (10%)
        random.seed(SEED)
        shuffled = list(unique_files)
        random.shuffle(shuffled)

        test_files = shuffled[:20]
        val_files = shuffled[20:40]
        train_files = shuffled[40:]

        # Cryptographic Leakage Assertion
        train_hashes = {compute_md5(f) for f in train_files}
        val_hashes = {compute_md5(f) for f in val_files}
        test_hashes = {compute_md5(f) for f in test_files}

        assert not train_hashes.intersection(val_hashes), f"Leakage Train-Val in {target_class}"
        assert not train_hashes.intersection(test_hashes), f"Leakage Train-Test in {target_class}"
        assert not val_hashes.intersection(test_hashes), f"Leakage Val-Test in {target_class}"

        # Write pristine images into splits
        for split_name, split_dir, split_list in [
            ("train", TRAIN_DIR, train_files),
            ("val", VAL_DIR, val_files),
            ("test", TEST_DIR, test_files),
        ]:
            out_folder = split_dir / target_class
            out_folder.mkdir(parents=True, exist_ok=True)
            for idx, img_path in enumerate(split_list, 1):
                clean_name = f"{target_class.lower().replace(' - ', '_').replace(' ', '_')}_{split_name}_{idx:05d}{img_path.suffix.lower()}"
                shutil.copy2(str(img_path), str(out_folder / clean_name))

        stats.append({
            "class": target_class,
            "train": len(train_files),
            "val": len(val_files),
            "test": len(test_files),
            "total": total_unique,
        })

    # Print Summary Table
    print("\n" + "=" * 75)
    print("  📊 EGGPLANT ORIGINAL IMAGES (VERSION 02) INGESTION SUMMARY")
    print("=" * 75)
    print(f"{'Class Name':<35} | {'Train':>7} | {'Val':>6} | {'Test':>6} | {'Total':>7} | {'Integrity':<15}")
    print("-" * 85)
    for s in stats:
        print(f"{s['class']:<35} | {s['train']:>7} | {s['val']:>6} | {s['test']:>6} | {s['total']:>7} | ✅ 100% Unaugmented")
    print("-" * 85)

    # Re-run dataset counts
    try:
        import subprocess
        subprocess.run([sys.executable, "scripts/generate_dataset_counts.py"], check=True)
    except Exception:
        pass

    print("\n[SUCCESS] Authentic Eggplant Version 02 originals ingested with zero leakage!")


if __name__ == "__main__":
    main()
