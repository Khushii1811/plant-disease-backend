"""
scripts/data/curation/anti_leakage_and_dedup.py

Anti-leakage guard and deduplication engine:
1. Anti-leakage: Ensures candidate images from data/raw/unified_scraped/ do not match
   images in data/processed/val or data/processed/test (exact MD5 or pHash Hamming distance <= threshold).
2. Train redundancy: Quarantines candidate images identical to existing training data.
3. Within-class deduplication: Deduplicates multiple identical/near-identical downloads.

Inputs:
  - data/processed/val, data/processed/test, data/processed/train
  - data/raw/unified_scraped/
Outputs:
  - Quarantined duplicates moved to data/quarantine_leakage/, data/quarantine_train_dups/, data/quarantine_internal_dups/
"""

import argparse
import hashlib
import os
import shutil
import sys
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

from PIL import Image
from tqdm import tqdm

try:
    import imagehash
except ImportError:
    imagehash = None

ROOT = Path(__file__).resolve().parent.parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import config

if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]

PROJECT_ROOT = config.PROJECT_ROOT
PROCESSED_ROOT = PROJECT_ROOT / "data" / "processed"
UNIFIED_RAW = PROJECT_ROOT / "data" / "raw" / "unified_scraped"
QUARANTINE_LEAK = PROJECT_ROOT / "data" / "quarantine_leakage"
QUARANTINE_TRAIN_DUP = PROJECT_ROOT / "data" / "quarantine_train_dups"
QUARANTINE_INTERNAL = PROJECT_ROOT / "data" / "quarantine_internal_dups"

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
DEFAULT_WORKERS = min(16, max(1, (os.cpu_count() or 4) - 2))


def _hamming(a: int, b: int) -> int:
    return bin(a ^ b).count("1")


class BKTree:
    """Fast nearest-neighbour search in Hamming metric space for pHash."""

    def __init__(self) -> None:
        self._root: tuple[int, str] | None = None
        self._children: dict[int, "BKTree"] = {}

    def add(self, hash_int: int, identifier: str) -> None:
        if self._root is None:
            self._root = (hash_int, identifier)
            return
        root_hash, _ = self._root
        dist = _hamming(hash_int, root_hash)
        if dist not in self._children:
            self._children[dist] = BKTree()
        self._children[dist].add(hash_int, identifier)

    def query(self, hash_int: int, threshold: int) -> list[tuple[int, str]]:
        if self._root is None:
            return []
        root_hash, root_id = self._root
        dist = _hamming(hash_int, root_hash)
        results: list[tuple[int, str]] = []
        if dist <= threshold:
            results.append((root_hash, root_id))
        for edge_dist, child in self._children.items():
            if abs(edge_dist - dist) <= threshold:
                results.extend(child.query(hash_int, threshold))
        return results


def _hash_worker(path_str: str) -> tuple[str, str, int | None]:
    """Computes (path_str, md5_hex, phash_int) in worker."""
    try:
        raw = Path(path_str).read_bytes()
        md5_val = hashlib.md5(raw).hexdigest()
        if imagehash is not None:
            with Image.open(path_str) as img:
                ph = imagehash.phash(img.convert("RGB"))
            return path_str, md5_val, int(str(ph), 16)
        return path_str, md5_val, None
    except Exception:
        return path_str, "", None


def scan_folder(folder: Path, desc: str, workers: int) -> list[tuple[str, str, int | None]]:
    if not folder.exists():
        return []
    paths = []
    for ext in IMAGE_EXTS:
        paths.extend(str(p) for p in folder.rglob(f"*{ext}"))
        paths.extend(str(p) for p in folder.rglob(f"*{ext.upper()}"))
    paths = sorted(set(paths))
    if not paths:
        return []

    results = []
    with ProcessPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(_hash_worker, p): p for p in paths}
        for future in tqdm(as_completed(futures), total=len(paths), desc=desc, unit="img"):
            results.append(future.result())
    return results


def main() -> None:
    parser = argparse.ArgumentParser(description="Strict anti-leakage and deduplication scanner")
    parser.add_argument(
        "--quarantine", action="store_true", help="Move duplicate & leaking images to quarantine"
    )
    parser.add_argument(
        "--threshold", type=int, default=4, help="pHash Hamming threshold for near-duplicate (default 4)"
    )
    parser.add_argument(
        "--workers", type=int, default=DEFAULT_WORKERS, help="Parallel worker threads"
    )
    args = parser.parse_args()

    print("=" * 80)
    print("  ANTI-LEAKAGE & DEDUPLICATION ENGINE")
    print(f"  CPU Workers     : {args.workers}")
    print(f"  pHash Threshold : {args.threshold} Hamming bits")
    print(f"  Action          : {'QUARANTINE DETECTED DUPLICATES' if args.quarantine else 'DRY RUN / AUDIT'}")
    print("=" * 80)

    val_hashes = scan_folder(PROCESSED_ROOT / "val", "Indexing Val set", args.workers)
    test_hashes = scan_folder(PROCESSED_ROOT / "test", "Indexing Test set", args.workers)

    val_test_md5: dict[str, str] = {}
    val_test_tree = BKTree()

    for p, md5, ph in val_hashes + test_hashes:
        if md5:
            val_test_md5[md5] = p
        if ph is not None:
            val_test_tree.add(ph, p)

    print(f"\nIndexed {len(val_hashes)} val + {len(test_hashes)} test images for Leakage Protection.")

    train_hashes = scan_folder(PROCESSED_ROOT / "train", "Indexing Train set", args.workers)
    train_md5: dict[str, str] = {}
    train_tree = BKTree()
    for p, md5, ph in train_hashes:
        if md5:
            train_md5[md5] = p
        if ph is not None:
            train_tree.add(ph, p)

    print(f"Indexed {len(train_hashes)} existing train images for Redundancy Protection.\n")

    raw_candidates = scan_folder(UNIFIED_RAW, "Scanning Unified Raw", args.workers)
    print(f"\nTotal incoming candidates in unified_scraped: {len(raw_candidates)}")

    leakage_detected: list[tuple[str, str, str]] = []
    train_dups: list[tuple[str, str, str]] = []
    internal_dups: list[tuple[str, str, str]] = []

    seen_raw_md5: dict[str, str] = {}
    raw_class_trees: dict[str, BKTree] = defaultdict(BKTree)
    verified_clean: list[str] = []

    for path_str, md5, ph in tqdm(raw_candidates, desc="Auditing Candidates", unit="img"):
        if not md5 or ph is None:
            continue
        p = Path(path_str)
        cls_name = p.parent.name

        if md5 in val_test_md5:
            leakage_detected.append((path_str, val_test_md5[md5], "Exact MD5 match with Val/Test"))
            continue
        matches = val_test_tree.query(ph, args.threshold)
        if matches:
            leakage_detected.append(
                (path_str, matches[0][1], f"Near-match (pHash dist <= {args.threshold}) with Val/Test")
            )
            continue

        if md5 in train_md5:
            train_dups.append((path_str, train_md5[md5], "Exact MD5 match with existing Train"))
            continue
        matches_tr = train_tree.query(ph, min(args.threshold, 3))
        if matches_tr:
            train_dups.append((path_str, matches_tr[0][1], "Near-match with existing Train"))
            continue

        if md5 in seen_raw_md5:
            internal_dups.append((path_str, seen_raw_md5[md5], "Exact MD5 duplicate in unified_scraped"))
            continue
        matches_int = raw_class_trees[cls_name].query(ph, args.threshold)
        if matches_int:
            internal_dups.append((path_str, matches_int[0][1], "Near-duplicate in unified_scraped"))
            continue

        seen_raw_md5[md5] = path_str
        raw_class_trees[cls_name].add(ph, path_str)
        verified_clean.append(path_str)

    print("\n" + "=" * 80)
    print("  ANTI-LEAKAGE & DEDUPLICATION AUDIT SUMMARY")
    print("=" * 80)
    print(f"  Total Candidates Audited       : {len(raw_candidates):>7,}")
    print(f"  DATA LEAKAGE BLOCKED (Val/Test): {len(leakage_detected):>7,}")
    print(f"  Existing Train Duplicates      : {len(train_dups):>7,}")
    print(f"  Internal Scrape Duplicates     : {len(internal_dups):>7,}")
    print(f"  Total Flagged for Quarantine   : {len(leakage_detected) + len(train_dups) + len(internal_dups):>7,}")
    print(f"  VERIFIED CLEAN & UNIQUE IMAGES : {len(verified_clean):>7,}")
    print("=" * 80)

    if args.quarantine:
        print("\nExecuting Quarantine...")
        for raw, _, _ in leakage_detected:
            dest = QUARANTINE_LEAK / Path(raw).parent.name / Path(raw).name
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(raw, str(dest))

        for raw, _, _ in train_dups:
            dest = QUARANTINE_TRAIN_DUP / Path(raw).parent.name / Path(raw).name
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(raw, str(dest))

        for raw, _, _ in internal_dups:
            dest = QUARANTINE_INTERNAL / Path(raw).parent.name / Path(raw).name
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(raw, str(dest))

        print(f"Quarantine complete! Only {len(verified_clean):,} images remain.")


if __name__ == "__main__":
    main()
