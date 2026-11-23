"""
scripts/data/curation/purge_exact_cross_split_leakage.py

Purges exact cross-split hash collisions between Train, Val, and Test across the dataset.
Moves any training/validation duplicates to data/quarantine_leakage/ to ensure zero exact-hash
cross-split leakage.

Inputs:
  - data/processed/train, data/processed/val, data/processed/test
Outputs:
  - Quarantined duplicate images moved to data/quarantine_leakage/
"""

import hashlib
import shutil
import sys
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import config

DATA_DIR = config.DATA_DIR
PROCESSED_DIR = DATA_DIR / "processed"
TRAIN_DIR = PROCESSED_DIR / "train"
VAL_DIR = PROCESSED_DIR / "val"
TEST_DIR = PROCESSED_DIR / "test"
QUARANTINE_DIR = DATA_DIR / "quarantine_leakage"


def hash_file(p: Path):
    hasher = hashlib.md5()
    try:
        with open(p, "rb") as f:
            while chunk := f.read(65536):
                hasher.update(chunk)
        return hasher.hexdigest(), p
    except Exception:
        return None, p


def get_split_hashes(folder: Path):
    files = [
        p
        for p in folder.rglob("*")
        if p.is_file() and p.suffix.lower() in [".jpg", ".jpeg", ".png", ".bmp", ".webp"]
    ]
    with ThreadPoolExecutor(max_workers=16) as ex:
        results = list(ex.map(hash_file, files))
    hmap = defaultdict(list)
    for h, p in results:
        if h is not None:
            hmap[h].append(p)
    return hmap


def main():
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass

    print("=" * 75)
    print("  DATASET-WIDE ZERO-LEAKAGE PURGE & VERIFICATION PIPELINE")
    print("=" * 75)

    QUARANTINE_DIR.mkdir(parents=True, exist_ok=True)

    print("[1/4] Hashing Test split...")
    te_hashes = get_split_hashes(TEST_DIR)
    print(f"      Total Test Unique Hashes: {len(te_hashes)}")

    print("[2/4] Hashing Validation split...")
    va_hashes = get_split_hashes(VAL_DIR)
    print(f"      Total Val Unique Hashes:  {len(va_hashes)}")

    print("[3/4] Hashing Train split...")
    tr_hashes = get_split_hashes(TRAIN_DIR)
    print(f"      Total Train Unique Hashes: {len(tr_hashes)}")

    train_test_leaks = set(tr_hashes.keys()).intersection(set(te_hashes.keys()))
    train_val_leaks = set(tr_hashes.keys()).intersection(set(va_hashes.keys()))
    val_test_leaks = set(va_hashes.keys()).intersection(set(te_hashes.keys()))

    print("\n[INFO] Collisions detected:")
    print(f"  - Train vs Test collisions : {len(train_test_leaks)}")
    print(f"  - Train vs Val collisions  : {len(train_val_leaks)}")
    print(f"  - Val vs Test collisions   : {len(val_test_leaks)}")

    purged_train_count = 0
    purged_val_count = 0

    all_train_leaks = train_test_leaks.union(train_val_leaks)
    for h in all_train_leaks:
        for p in tr_hashes[h]:
            if p.exists():
                cname = p.parent.name
                dest = QUARANTINE_DIR / "from_train" / cname
                dest.mkdir(parents=True, exist_ok=True)
                shutil.move(str(p), str(dest / p.name))
                purged_train_count += 1

    for h in val_test_leaks:
        for p in va_hashes[h]:
            if p.exists():
                cname = p.parent.name
                dest = QUARANTINE_DIR / "from_val" / cname
                dest.mkdir(parents=True, exist_ok=True)
                shutil.move(str(p), str(dest / p.name))
                purged_val_count += 1

    print(f"\n[SUCCESS] Purged {purged_train_count} leaking files from Train -> {QUARANTINE_DIR / 'from_train'}")
    if purged_val_count > 0:
        print(f"[SUCCESS] Purged {purged_val_count} leaking files from Val -> {QUARANTINE_DIR / 'from_val'}")

    print("\n[4/4] Executing Final Verification...")
    new_tr = get_split_hashes(TRAIN_DIR)
    new_va = get_split_hashes(VAL_DIR)
    new_te = get_split_hashes(TEST_DIR)

    final_tr_va = set(new_tr.keys()).intersection(set(new_va.keys()))
    final_tr_te = set(new_tr.keys()).intersection(set(new_te.keys()))
    final_va_te = set(new_va.keys()).intersection(set(new_te.keys()))

    print(f"  - Final Train n Val Collisions  : {len(final_tr_va)}")
    print(f"  - Final Train n Test Collisions : {len(final_tr_te)}")
    print(f"  - Final Val n Test Collisions   : {len(final_va_te)}")

    assert len(final_tr_va) == 0, "Train-Val collision remained!"
    assert len(final_tr_te) == 0, "Train-Test collision remained!"
    assert len(final_va_te) == 0, "Val-Test collision remained!"

    print("Zero exact cross-split hash collisions verified.")


if __name__ == "__main__":
    main()
