"""
scripts/claude_leakage_audit.py — Independent data leakage & redundancy auditor.

Written from scratch with a different approach than any other audit script.

My Strategy (3-Layer Defence):
  Layer 1 — SHA-256 exact byte match  (100% certainty, zero false positives)
  Layer 2 — pHash BK-tree candidate lookup, then aHash verified on the SAME
             reference image. This is the critical fix vs. using two independent
             BK-trees: it eliminates cross-image false positives where phash
             matches image A but ahash matches a different image B.
  Layer 3 — Internal dedup within unified_scraped itself (exact + near-dup)

Cross-referenced against ALL three processed splits: train, val, test.
Candidate source: data/raw/unified_scraped/

Output:
  - Console summary per class + totals
  - data/claude_audit_report.csv   (every flagged file, reason, matched file)
  - data/claude_clean_manifest.txt (one path per line of 100% clean images)

Usage:
  python scripts/claude_leakage_audit.py              # dry-run report
  python scripts/claude_leakage_audit.py --quarantine # move flagged to quarantine
  python scripts/claude_leakage_audit.py --threshold 5  # default threshold
"""

import argparse
import csv
import hashlib
import io
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
    print("ERROR: imagehash not installed. Run: pip install imagehash")
    sys.exit(1)

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore

# ── Paths ─────────────────────────────────────────────────────────────────────
ROOT        = Path(__file__).resolve().parents[2]
PROCESSED   = ROOT / "data" / "processed"
UNIFIED_RAW = ROOT / "data" / "raw" / "unified_scraped"
QUARANTINE  = ROOT / "data" / "claude_quarantine"
REPORT_CSV  = ROOT / "data" / "claude_audit_report.csv"
CLEAN_LIST  = ROOT / "data" / "patches" / "history" / "claude_clean_manifest.txt"

IMAGE_EXTS  = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
SPLITS      = ["train", "val", "test"]
WORKERS     = min(14, max(1, (os.cpu_count() or 4) - 2))


# ── Dual-hash worker (top-level so ProcessPoolExecutor can pickle it) ──────────
def _compute_hashes(path_str: str) -> tuple:
    """Returns (path_str, sha256_hex, phash_int, ahash_int, file_size)."""
    p = Path(path_str)
    try:
        raw    = p.read_bytes()
        sha256 = hashlib.sha256(raw).hexdigest()
        size   = len(raw)
        with Image.open(io.BytesIO(raw)) as img:
            rgb = img.convert("RGB")
            ph  = int(str(imagehash.phash(rgb)), 16)
            ah  = int(str(imagehash.average_hash(rgb)), 16)
        return path_str, sha256, ph, ah, size
    except Exception:
        return path_str, "", None, None, 0


# ── Hamming distance ───────────────────────────────────────────────────────────
def _hamming(a: int, b: int) -> int:
    return bin(a ^ b).count("1")


# ── BK-tree for O(log n) phash candidate retrieval ────────────────────────────
class BKTree:
    """
    Stores (phash_int, path_str) entries.
    candidates() returns all entries within Hamming threshold —
    used as a FIRST-PASS FILTER ONLY; the caller must verify ahash
    against the SAME returned path before declaring a near-duplicate.
    """

    def __init__(self) -> None:
        self._root = None
        self._children: dict = {}

    def insert(self, ph: int, label: str) -> None:
        if self._root is None:
            self._root = (ph, label)
            return
        d = _hamming(ph, self._root[0])
        self._children.setdefault(d, BKTree()).insert(ph, label)

    def candidates(self, ph: int, threshold: int) -> list:
        """Return list of (phash_int, label) within Hamming threshold."""
        if self._root is None:
            return []
        root_ph, root_label = self._root
        d = _hamming(ph, root_ph)
        results = []
        if d <= threshold:
            results.append((root_ph, root_label))
        for edge, child in self._children.items():
            if abs(edge - d) <= threshold:
                results.extend(child.candidates(ph, threshold))
        return results


# ── Unified reference index with same-image ahash verification ────────────────
class ReferenceIndex:
    """
    Stores all images indexed by SHA-256 (exact) and phash (BK-tree).
    Also maintains a path -> ahash lookup so that when a phash candidate
    is found, we can verify ahash distance against that SAME image.

    This eliminates the false-positive failure mode of two independent trees
    where phash tree returns image A and ahash tree returns image B, causing
    spurious flags even though no single image is close in both hashes.
    """

    def __init__(self) -> None:
        self.sha_map:    dict = {}      # sha256  -> path
        self.ph_tree:    BKTree = BKTree()
        self.path_ahash: dict = {}      # path    -> ahash_int

    def add(self, path_str: str, sha: str, ph, ah) -> None:
        if sha:
            self.sha_map[sha] = path_str
        if ph is not None:
            self.ph_tree.insert(ph, path_str)
        if ah is not None:
            self.path_ahash[path_str] = ah

    def find_near_dup(self, ph: int, ah: int, threshold: int):
        """
        Returns path of a reference image that is within threshold of the
        query in BOTH phash AND ahash — on the SAME reference image.
        Returns None if no such image exists.
        """
        for _cand_ph, cand_path in self.ph_tree.candidates(ph, threshold):
            cand_ah = self.path_ahash.get(cand_path)
            if cand_ah is not None and _hamming(ah, cand_ah) <= threshold:
                return cand_path
        return None


# ── Parallel folder scanner ────────────────────────────────────────────────────
def _scan(folder: Path, desc: str) -> list:
    paths = sorted({
        str(p) for ext in IMAGE_EXTS
        for p in list(folder.rglob(f"*{ext}")) + list(folder.rglob(f"*{ext.upper()}"))
    })
    if not paths:
        return []
    results = []
    with ProcessPoolExecutor(max_workers=WORKERS) as ex:
        futs = {ex.submit(_compute_hashes, p): p for p in paths}
        for f in tqdm(as_completed(futs), total=len(paths), desc=desc, unit="img"):
            results.append(f.result())
    return results


# ── Build reference index from processed train/val/test ───────────────────────
def build_reference_index() -> ReferenceIndex:
    ref = ReferenceIndex()
    for split in SPLITS:
        split_dir = PROCESSED / split
        if not split_dir.exists():
            continue
        records = _scan(split_dir, f"Indexing {split:5s}")
        for path_str, sha, ph, ah, _ in records:
            if sha:
                ref.add(path_str, sha, ph, ah)
    return ref


# ── Main audit ─────────────────────────────────────────────────────────────────
def run_audit(threshold: int, do_quarantine: bool) -> None:
    print("=" * 80)
    print("  CLAUDE — Independent Leakage & Redundancy Auditor  (v2)")
    print(f"  Strategy  : SHA-256 exact  +  pHash BK-tree -> aHash verify on SAME image")
    print(f"  Near-dup  : pHash <= {threshold} bits AND aHash <= {threshold} bits of the SAME ref image")
    print(f"  Workers   : {WORKERS}  |  Source: data/raw/unified_scraped")
    print(f"  Mode      : {'QUARANTINE' if do_quarantine else 'DRY-RUN'}")
    print("=" * 80)

    print("\n[Step 1] Building ground-truth index (train + val + test) …")
    ref = build_reference_index()
    print(f"         {len(ref.sha_map):,} reference images indexed.\n")

    print("[Step 2] Scanning unified_scraped candidates …")
    candidates = _scan(UNIFIED_RAW, "Scanning unified_scraped")
    print(f"         {len(candidates):,} candidate images found.\n")

    print("[Step 3] Auditing candidates …\n")
    internal = ReferenceIndex()
    flagged: list = []
    clean:   list = []
    per_class_clean:   dict = defaultdict(int)
    per_class_flagged: dict = defaultdict(int)

    for path_str, sha, ph, ah, _ in tqdm(candidates, desc="Auditing", unit="img"):
        cls = Path(path_str).parent.name

        if not sha or ph is None or ah is None:
            per_class_flagged[cls] += 1
            flagged.append({"path": path_str, "reason": "Corrupt/unreadable", "matched": ""})
            continue

        # Layer 1: exact SHA-256 vs processed
        if sha in ref.sha_map:
            per_class_flagged[cls] += 1
            flagged.append({"path": path_str,
                            "reason": "Exact SHA-256 match with processed data",
                            "matched": ref.sha_map[sha]})
            continue

        # Layer 2: near-dup vs processed (same-image aHash verification)
        m = ref.find_near_dup(ph, ah, threshold)
        if m is not None:
            per_class_flagged[cls] += 1
            flagged.append({"path": path_str,
                            "reason": f"Near-dup vs processed (pHash+aHash <= {threshold} on same ref)",
                            "matched": m})
            continue

        # Layer 3: exact SHA-256 within unified_scraped
        if sha in internal.sha_map:
            per_class_flagged[cls] += 1
            flagged.append({"path": path_str,
                            "reason": "Exact SHA-256 duplicate within unified_scraped",
                            "matched": internal.sha_map[sha]})
            continue

        # Layer 4: near-dup within unified_scraped
        im = internal.find_near_dup(ph, ah, threshold)
        if im is not None:
            per_class_flagged[cls] += 1
            flagged.append({"path": path_str,
                            "reason": f"Near-dup within unified_scraped (pHash+aHash <= {threshold})",
                            "matched": im})
            continue

        # Clean
        internal.add(path_str, sha, ph, ah)
        per_class_clean[cls] += 1
        clean.append(path_str)

    # Per-class summary
    print("\n" + "=" * 80)
    print("  PER-CLASS SUMMARY  (only classes with flagged images shown)")
    print(f"  {'Class':<44} | {'Clean':>6} | {'Flagged':>8}")
    print("  " + "-" * 64)
    for cls in sorted(set(per_class_clean) | set(per_class_flagged)):
        c  = per_class_clean.get(cls, 0)
        fl = per_class_flagged.get(cls, 0)
        if fl > 0:
            print(f"  {cls:<44} | {c:>6} | {fl:>8}")

    # Totals
    n_exact  = sum(1 for f in flagged if "Exact SHA-256 match with processed" in f["reason"])
    n_near   = sum(1 for f in flagged if "same ref" in f["reason"])
    n_int_e  = sum(1 for f in flagged if "Exact SHA-256 duplicate within" in f["reason"])
    n_int_n  = sum(1 for f in flagged if "within unified_scraped" in f["reason"] and "Exact" not in f["reason"])
    n_corrupt= sum(1 for f in flagged if "Corrupt" in f["reason"])

    print("\n" + "=" * 80)
    print("  CLAUDE AUDIT FINAL RESULTS  (v2)")
    print("=" * 80)
    print(f"  Candidates scanned                      : {len(candidates):>8,}")
    print(f"  Exact SHA-256 leakage (train/val/test)  : {n_exact:>8,}")
    print(f"  Near-dup leakage (same-image verified)  : {n_near:>8,}")
    print(f"  Internal exact duplicates               : {n_int_e:>8,}")
    print(f"  Internal near-duplicates                : {n_int_n:>8,}")
    print(f"  Corrupt / unreadable                    : {n_corrupt:>8,}")
    print(f"  ─────────────────────────────────────────────────────────")
    print(f"  Total flagged                           : {len(flagged):>8,}")
    print(f"  VERIFIED CLEAN & UNIQUE                 : {len(clean):>8,}")
    print("=" * 80)

    # Write CSV report
    REPORT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with open(REPORT_CSV, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=["path", "reason", "matched"])
        writer.writeheader()
        writer.writerows(flagged)
    print(f"\n  Detailed report  → {REPORT_CSV}")

    # Write clean manifest
    with open(CLEAN_LIST, "w", encoding="utf-8") as fh:
        fh.write("\n".join(clean))
    print(f"  Clean manifest   → {CLEAN_LIST}")

    # Quarantine
    if do_quarantine:
        print(f"\n[Step 4] Moving {len(flagged):,} flagged images to quarantine …")
        QUARANTINE.mkdir(parents=True, exist_ok=True)
        moved = 0
        for item in tqdm(flagged, desc="Quarantining", unit="file"):
            src = Path(item["path"])
            dst = QUARANTINE / src.parent.name / src.name
            dst.parent.mkdir(parents=True, exist_ok=True)
            try:
                shutil.move(str(src), str(dst))
                moved += 1
            except Exception:
                pass
        print(f"  Done. {moved:,} files quarantined → {QUARANTINE}")
        print(f"  {len(clean):,} verified clean images remain in unified_scraped.")
    else:
        print("\n  Run with --quarantine to move flagged files to data/claude_quarantine/")


def main() -> None:
    p = argparse.ArgumentParser(description="Claude — independent leakage & redundancy auditor (v2)")
    p.add_argument("--quarantine", action="store_true")
    p.add_argument("--threshold",  type=int, default=5)
    args = p.parse_args()
    run_audit(threshold=args.threshold, do_quarantine=args.quarantine)


if __name__ == "__main__":
    main()
