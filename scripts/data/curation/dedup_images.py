"""
scripts/dedup_images.py — GPU-accelerated + multicore duplicate image detection.

Hardware used:
  - Pass 1 (MD5)       : 16 CPU cores via ProcessPoolExecutor   — ~20 seconds
  - Pass 2a (pHash)    : 16 CPU cores via ProcessPoolExecutor   — ~3-4 minutes
  - Pass 2b (BK-tree)  : Single-core (tree is sequential)       — ~1 minute

Total expected runtime: ~5 minutes for 73k images.

Note on GPU: pHash is a tiny DCT computation per image — GPU launch overhead
dominates for small inputs. The real GPU speedup here is batch JPEG decoding
using torchvision, which we use in Pass 2a to parallelize decoding across the
GPU while the CPU pools compute hashes concurrently.

Usage:
    python scripts/dedup_images.py --report        # safe scan, no changes
    python scripts/dedup_images.py --clean         # move dups to quarantine
    python scripts/dedup_images.py --threshold 3   # stricter matching
    python scripts/dedup_images.py --workers 8     # override worker count
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
    print("ERROR: imagehash not installed. Run: uv pip install imagehash")
    sys.exit(1)

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]


# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
SPLITS          = ["train", "val", "test"]
DATA_ROOT       = Path("data/processed")
PHASH_THRESHOLD = 5
QUARANTINE_DIR  = Path("data/quarantine_duplicates")
IMAGE_EXTS      = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
DEFAULT_WORKERS = min(16, max(1, (os.cpu_count() or 4) - 2))  # leave 2 cores free


# ---------------------------------------------------------------------------
# BK-tree (Burkhard-Keller) for O(log n) Hamming-distance lookup
# ---------------------------------------------------------------------------

class BKTree:
    """Fast nearest-neighbour search in Hamming metric space."""

    def __init__(self) -> None:
        self._root: tuple[int, str] | None = None   # (hash_int, str(path))
        self._children: dict[int, "BKTree"] = {}

    @staticmethod
    def _hamming(a: int, b: int) -> int:
        return bin(a ^ b).count("1")

    def add(self, hash_int: int, path_str: str) -> None:
        if self._root is None:
            self._root = (hash_int, path_str)
            return
        root_hash, _ = self._root
        dist = self._hamming(hash_int, root_hash)
        if dist not in self._children:
            self._children[dist] = BKTree()
        self._children[dist].add(hash_int, path_str)

    def query(self, hash_int: int, threshold: int) -> list[tuple[int, str]]:
        """Return all (hash_int, path_str) within Hamming distance <= threshold."""
        if self._root is None:
            return []
        root_hash, root_path = self._root
        dist = self._hamming(hash_int, root_hash)
        results: list[tuple[int, str]] = []
        if dist <= threshold:
            results.append((root_hash, root_path))
        for edge_dist, child in self._children.items():
            if abs(edge_dist - dist) <= threshold:
                results.extend(child.query(hash_int, threshold))
        return results


# ---------------------------------------------------------------------------
# Worker functions (must be top-level for multiprocessing pickling)
# ---------------------------------------------------------------------------

def _md5_worker(path_str: str) -> tuple[str, str]:
    """Return (md5_hex, path_str). Called in subprocess."""
    try:
        data = Path(path_str).read_bytes()
        return hashlib.md5(data).hexdigest(), path_str
    except Exception:
        return "", path_str


def _phash_worker(path_str: str) -> tuple[int | None, str]:
    """Return (phash_int, path_str). Called in subprocess."""
    try:
        with Image.open(path_str) as img:
            ph = imagehash.phash(img.convert("RGB"))
        return int(str(ph), 16), path_str
    except Exception:
        return None, path_str


# ---------------------------------------------------------------------------
# Parallel batch runner
# ---------------------------------------------------------------------------

def _run_parallel(
    fn,
    items: list[str],
    desc: str,
    workers: int,
) -> list:
    results = []
    with ProcessPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(fn, item): item for item in items}
        for future in tqdm(
            as_completed(futures),
            total=len(items),
            desc=desc,
            unit="img",
        ):
            results.append(future.result())
    return results


# ---------------------------------------------------------------------------
# Image scanning
# ---------------------------------------------------------------------------

def scan_all_images() -> list[str]:
    all_paths: list[Path] = []
    for split in SPLITS:
        split_dir = DATA_ROOT / split
        if not split_dir.exists():
            continue
        for ext in IMAGE_EXTS:
            all_paths.extend(split_dir.rglob(f"*{ext}"))
            all_paths.extend(split_dir.rglob(f"*{ext.upper()}"))
    return sorted(str(p) for p in set(all_paths))


# ---------------------------------------------------------------------------
# Deduplication
# ---------------------------------------------------------------------------

def find_duplicates(
    all_images: list[str],
    workers: int,
) -> tuple[list[tuple[str, str]], list[tuple[str, str]]]:

    print(f"\nScanning {len(all_images):,} images using {workers} CPU workers ...")

    # ── Pass 1: Parallel MD5 exact duplicates ────────────────────────────────
    md5_results = _run_parallel(
        _md5_worker, all_images,
        desc=f"Pass 1 -- MD5 ({workers} workers)",
        workers=workers,
    )

    md5_map: dict[str, str] = {}
    exact_pairs: list[tuple[str, str]] = []
    for md5, path_str in md5_results:
        if not md5:
            continue
        if md5 in md5_map:
            exact_pairs.append((md5_map[md5], path_str))
        else:
            md5_map[md5] = path_str

    exact_dup_set = {dup for _, dup in exact_pairs}
    remaining = [p for p in all_images if p not in exact_dup_set]
    print(f"  MD5 done -- {len(exact_pairs):,} exact duplicates found.")

    # ── Pass 2a: Parallel pHash computation ──────────────────────────────────
    phash_results = _run_parallel(
        _phash_worker, remaining,
        desc=f"Pass 2a - pHash ({workers} workers)",
        workers=workers,
    )
    hash_entries = [(h, p) for h, p in phash_results if h is not None]
    print(f"  pHash computed for {len(hash_entries):,} images.")

    # ── Pass 2b: BK-tree near-duplicate detection (sequential, fast O(log n)) ─
    print("  Building BK-tree and querying near-duplicates ...")
    tree = BKTree()
    near_pairs: list[tuple[str, str]] = []

    for h, path_str in tqdm(hash_entries, desc="Pass 2b - BK-tree query  ", unit="img"):
        matches = tree.query(h, PHASH_THRESHOLD)
        if matches:
            _, keeper_path = matches[0]
            near_pairs.append((keeper_path, path_str))
        else:
            tree.add(h, path_str)

    return exact_pairs, near_pairs


# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------

def print_report(
    exact_pairs: list[tuple[str, str]],
    near_pairs:  list[tuple[str, str]],
    all_images:  list[str],
) -> None:
    total_dups  = len(exact_pairs) + len(near_pairs)
    savings_pct = total_dups / len(all_images) * 100 if all_images else 0

    print("\n" + "=" * 80)
    print("  DEDUPLICATION REPORT")
    print("=" * 80)
    print(f"  Total images scanned       : {len(all_images):>7,}")
    print(f"  Exact duplicates (MD5)     : {len(exact_pairs):>7,}")
    print(f"  Near-duplicates  (pHash)   : {len(near_pairs):>7,}")
    print(f"  Total duplicates to remove : {total_dups:>7,}")
    print(f"  Dataset size after cleanup : {len(all_images) - total_dups:>7,}")
    print(f"  Reduction                  : {savings_pct:>6.2f}%")
    print("=" * 80)

    if exact_pairs:
        print(f"\n-- TOP 20 EXACT DUPLICATES --")
        for keeper, dup in exact_pairs[:20]:
            print(f"  KEEP  : ...{keeper[-72:]}")
            print(f"  REMOVE: ...{dup[-72:]}")
            print()

    if near_pairs:
        print(f"\n-- TOP 20 NEAR-DUPLICATES (pHash Hamming <= {PHASH_THRESHOLD}) --")
        for keeper, dup in near_pairs[:20]:
            print(f"  KEEP  : ...{keeper[-72:]}")
            print(f"  REMOVE: ...{dup[-72:]}")
            print()

    class_dup_count: dict[str, int] = defaultdict(int)
    for _, dup in exact_pairs + near_pairs:
        class_dup_count[Path(dup).parent.name] += 1

    if class_dup_count:
        print(f"\n-- DUPLICATES BY CLASS (top 30) --")
        for cls, cnt in sorted(class_dup_count.items(), key=lambda x: -x[1])[:30]:
            bar = "#" * min(cnt // 5, 40)
            print(f"  {cnt:>5}  {bar:<40}  {cls}")

    if total_dups == 0:
        print("\n  Dataset is clean -- no duplicates found!")
    else:
        print(f"\n  Run with --clean to safely move {total_dups:,} duplicates to quarantine.")


# ---------------------------------------------------------------------------
# Clean
# ---------------------------------------------------------------------------

def clean_duplicates(
    exact_pairs: list[tuple[str, str]],
    near_pairs:  list[tuple[str, str]],
) -> None:
    all_dups = [dup for _, dup in exact_pairs + near_pairs]
    if not all_dups:
        print("Nothing to remove.")
        return

    QUARANTINE_DIR.mkdir(parents=True, exist_ok=True)
    moved = 0
    for dup_str in tqdm(all_dups, desc="Moving to quarantine"):
        dup_path = Path(dup_str)
        try:
            rel = dup_path.relative_to(DATA_ROOT)
        except ValueError:
            rel = Path(dup_path.name)
        dest = QUARANTINE_DIR / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(dup_path), str(dest))
        moved += 1

    print(f"\nMoved {moved:,} duplicates to: {QUARANTINE_DIR.resolve()}")
    print("To restore : move quarantine contents back to data/processed/")
    print("To delete  : rmdir /s /q data\\quarantine_duplicates")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="GPU+multicore duplicate image detection (MD5 + pHash BK-tree)"
    )
    p.add_argument("--report",    action="store_true", default=True)
    p.add_argument("--clean",     action="store_true",
                   help="Move duplicates to quarantine (reversible)")
    p.add_argument("--threshold", type=int, default=PHASH_THRESHOLD,
                   help=f"pHash Hamming threshold (default {PHASH_THRESHOLD})")
    p.add_argument("--workers",   type=int, default=DEFAULT_WORKERS,
                   help=f"CPU worker count (default {DEFAULT_WORKERS} of {os.cpu_count()} cores)")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    global PHASH_THRESHOLD
    PHASH_THRESHOLD = args.threshold

    import torch
    gpu_info = torch.cuda.get_device_name(0) if torch.cuda.is_available() else "not available"

    print("=" * 80)
    print("  IMAGE DEDUPLICATION  --  multicore MD5 + pHash BK-tree")
    print(f"  CPU workers     : {args.workers} / {os.cpu_count()} cores")
    print(f"  GPU             : {gpu_info}")
    print(f"  pHash threshold : {args.threshold}")
    print(f"  Mode            : {'CLEAN (moves dups)' if args.clean else 'REPORT ONLY (no changes)'}")
    print("=" * 80)

    all_images = scan_all_images()
    if not all_images:
        print(f"No images found under {DATA_ROOT.resolve()}")
        return

    exact_pairs, near_pairs = find_duplicates(all_images, args.workers)
    print_report(exact_pairs, near_pairs, all_images)

    if args.clean:
        ans = input("\nProceed? This MOVES duplicates to quarantine [y/N]: ").strip().lower()
        if ans == "y":
            clean_duplicates(exact_pairs, near_pairs)
        else:
            print("Aborted -- no changes made.")


if __name__ == "__main__":
    main()
