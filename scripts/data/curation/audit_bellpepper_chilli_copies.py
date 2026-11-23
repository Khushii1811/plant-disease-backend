"""
scripts/data/curation/audit_bellpepper_chilli_copies.py

Audits and proves which images in 3 Bell Pepper classes:
  - 'Bell Pepper - Leaf Curl Virus'
  - 'Bell Pepper - Nutrition Deficiency'
  - 'Bell Pepper - bell pepper powdery mildew'
are copies of images in the Chilli classes across train, val, and test splits.

Matching Criteria:
  1. Exact SHA-256 cryptographic match (identical bit-for-bit file).
  2. Perceptual Hash (pHash) Hamming distance <= threshold (default 4).
     Justification: In a 64-bit DCT-based pHash, a Hamming distance <= 4 corresponds to
     >= 93.75% frequency feature overlap, reliably detecting re-encoded, resized, or
     lightly compressed image twins from the same camera/in-situ capture while strictly
     preventing cross-specimen false positives.

Outputs:
  data/quality_audit/bellpepper_chilli/manifest.csv
  data/quality_audit/bellpepper_chilli/unmatched.csv
"""

import argparse
import csv
import hashlib
import sys
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from PIL import Image
import imagehash

# Bootstrap project root
PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import config


TARGET_BELL_CLASSES = [
    "Bell Pepper - Leaf Curl Virus",
    "Bell Pepper - Nutrition Deficiency",
    "Bell Pepper - bell pepper powdery mildew",
]

SPLITS = ["train", "val", "test"]
VALID_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}


def compute_sha256(path: Path) -> str:
    """Computes SHA-256 hash of a file."""
    hasher = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            hasher.update(chunk)
    return hasher.hexdigest().lower()


def compute_phash(path: Path) -> Optional[imagehash.ImageHash]:
    """Computes 64-bit DCT-based perceptual hash of an image."""
    try:
        with Image.open(path) as img:
            return imagehash.phash(img.convert("RGB"))
    except Exception as exc:
        print(f"[WARN] Failed to compute pHash for {path}: {exc}", file=sys.stderr)
        return None


def find_chilli_classes(processed_dir: Path) -> List[str]:
    """Identifies all Chilli classes present in the processed dataset."""
    chilli_set = set()
    for s in SPLITS:
        s_dir = processed_dir / s
        if s_dir.exists():
            for d in s_dir.iterdir():
                if d.is_dir() and d.name.lower().startswith("chilli"):
                    chilli_set.add(d.name)
    return sorted(list(chilli_set))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Audit and prove copies of Chilli images in Bell Pepper folders."
    )
    parser.add_argument(
        "--phash-threshold",
        type=int,
        default=4,
        help="Maximum Hamming distance for pHash matching (default: 4; <=4 ensures >=93.75 percent frequency match).",
    )

    parser.add_argument(
        "--output-dir",
        type=Path,
        default=config.DATA_DIR / "quality_audit" / "bellpepper_chilli",
        help="Directory where manifest.csv and unmatched.csv will be saved.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    phash_threshold = args.phash_threshold
    output_dir: Path = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    processed_dir = config.PROCESSED_DATA_DIR
    chilli_classes = find_chilli_classes(processed_dir)

    print("=" * 80)
    print("BELL PEPPER vs. CHILLI COPY AUDIT")
    print("=" * 80)
    print(f"Target Bell Pepper classes ({len(TARGET_BELL_CLASSES)}):")
    for c in TARGET_BELL_CLASSES:
        print(f"  - {c}")
    print(f"\nAll Chilli classes searched ({len(chilli_classes)}):")
    for c in chilli_classes:
        print(f"  - {c}")
    print(f"\nPerceptual Hash Threshold: Hamming distance <= {phash_threshold}")
    print(
        f"Justification: Threshold {phash_threshold}/64 represents >= {((64 - phash_threshold) / 64) * 100:.2f}% "
        f"DCT perceptual feature agreement, standard for identifying compression/resize copies."
    )
    print(f"Output Directory: {output_dir}")
    print("=" * 80)

    # 1. Index Chilli images
    print("\n[Step 1/3] Indexing Chilli images across train, val, and test...")
    chilli_records = []
    # Index by sha256: sha -> list of records
    chilli_by_sha = defaultdict(list)

    for s in SPLITS:
        for c in chilli_classes:
            c_dir = processed_dir / s / c
            if not c_dir.exists():
                continue
            for f in sorted(c_dir.iterdir()):
                if f.is_file() and f.suffix.lower() in VALID_EXTS:
                    sha = compute_sha256(f)
                    ph = compute_phash(f)
                    rec = {
                        "file": f.name,
                        "class": c,
                        "split": s,
                        "path": f,
                        "sha256": sha,
                        "phash": ph,
                    }
                    chilli_records.append(rec)
                    chilli_by_sha[sha].append(rec)

    print(f"Total Chilli images indexed: {len(chilli_records)}")

    # 2. Index Bell Pepper target images
    print("\n[Step 2/3] Indexing Bell Pepper target images...")
    bell_records = []
    for s in SPLITS:
        for c in TARGET_BELL_CLASSES:
            b_dir = processed_dir / s / c
            if not b_dir.exists():
                continue
            for f in sorted(b_dir.iterdir()):
                if f.is_file() and f.suffix.lower() in VALID_EXTS:
                    sha = compute_sha256(f)
                    ph = compute_phash(f)
                    bell_records.append({
                        "file": f.name,
                        "class": c,
                        "split": s,
                        "path": f,
                        "sha256": sha,
                        "phash": ph,
                    })

    print(f"Total Bell Pepper images to audit: {len(bell_records)}")

    # 3. Matching
    print("\n[Step 3/3] Performing cross-crop matching (SHA-256 exact + pHash)...")
    manifest_rows = []
    unmatched_rows = []

    # Per-class counters
    # class -> {"total": 0, "exact": 0, "perceptual": 0, "unmatched": 0}
    stats_per_bell_class = defaultdict(lambda: {"total": 0, "exact": 0, "perceptual": 0, "unmatched": 0})
    split_pair_counts = defaultdict(int)  # (bell_split, chilli_split) -> count
    mapping_counts = defaultdict(int)     # (bell_class, chilli_class) -> count

    for b in bell_records:
        b_class = b["class"]
        b_split = b["split"]
        b_file = b["file"]
        stats_per_bell_class[b_class]["total"] += 1

        # Check exact SHA-256 match first
        sha_matches = chilli_by_sha.get(b["sha256"], [])
        if sha_matches:
            stats_per_bell_class[b_class]["exact"] += 1
            for m in sha_matches:
                manifest_rows.append({
                    "bell_file": b_file,
                    "bell_class": b_class,
                    "bell_split": b_split,
                    "chilli_file": m["file"],
                    "chilli_class": m["class"],
                    "chilli_split": m["split"],
                    "match_type": "sha256",
                    "hash_or_distance": b["sha256"],
                })
                split_pair_counts[(b_split, m["split"])] += 1
                mapping_counts[(b_class, m["class"])] += 1
            continue

        # Check perceptual hash match if no exact match
        b_ph = b["phash"]
        if b_ph is None:
            stats_per_bell_class[b_class]["unmatched"] += 1
            unmatched_rows.append({
                "bell_file": b_file,
                "bell_class": b_class,
                "bell_split": b_split,
                "reason": "phash_failed_to_compute",
                "min_distance": "",
                "closest_chilli_file": "",
                "closest_chilli_class": "",
                "closest_chilli_split": "",
            })
            continue

        # Find all Chilli matches within threshold
        phash_matches = []
        min_dist = 999
        closest_chilli = None

        for ch in chilli_records:
            if ch["phash"] is None:
                continue
            dist = b_ph - ch["phash"]
            if dist < min_dist:
                min_dist = dist
                closest_chilli = ch
            if dist <= phash_threshold:
                phash_matches.append((dist, ch))

        if phash_matches:
            stats_per_bell_class[b_class]["perceptual"] += 1
            # Sort by lowest distance
            phash_matches.sort(key=lambda x: x[0])
            # Record best match (or all top tied matches)
            best_dist = phash_matches[0][0]
            top_matches = [m for m in phash_matches if m[0] == best_dist]
            for dist, m in top_matches:
                manifest_rows.append({
                    "bell_file": b_file,
                    "bell_class": b_class,
                    "bell_split": b_split,
                    "chilli_file": m["file"],
                    "chilli_class": m["class"],
                    "chilli_split": m["split"],
                    "match_type": "phash",
                    "hash_or_distance": str(dist),
                })
                split_pair_counts[(b_split, m["split"])] += 1
                mapping_counts[(b_class, m["class"])] += 1
        else:
            stats_per_bell_class[b_class]["unmatched"] += 1
            unmatched_rows.append({
                "bell_file": b_file,
                "bell_class": b_class,
                "bell_split": b_split,
                "reason": f"min_phash_dist_{min_dist}_exceeds_threshold_{phash_threshold}",
                "min_distance": str(min_dist),
                "closest_chilli_file": closest_chilli["file"] if closest_chilli else "",
                "closest_chilli_class": closest_chilli["class"] if closest_chilli else "",
                "closest_chilli_split": closest_chilli["split"] if closest_chilli else "",
            })

    # Write manifest.csv
    manifest_path = output_dir / "manifest.csv"
    with open(manifest_path, "w", newline="", encoding="utf-8") as f:
        fieldnames = [
            "bell_file",
            "bell_class",
            "bell_split",
            "chilli_file",
            "chilli_class",
            "chilli_split",
            "match_type",
            "hash_or_distance",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(manifest_rows)

    # Write unmatched.csv
    unmatched_path = output_dir / "unmatched.csv"
    with open(unmatched_path, "w", newline="", encoding="utf-8") as f:
        fieldnames = [
            "bell_file",
            "bell_class",
            "bell_split",
            "reason",
            "min_distance",
            "closest_chilli_file",
            "closest_chilli_class",
            "closest_chilli_split",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(unmatched_rows)

    print(f"\nSaved match manifest to: {manifest_path} ({len(manifest_rows)} match pairs)")
    print(f"Saved unmatched ledger to: {unmatched_path} ({len(unmatched_rows)} unmatched images)")

    # 4. Print Summary Tables
    print("\n" + "=" * 80)
    print("TABLE 1: SUMMARY PER BELL PEPPER CLASS")
    print("=" * 80)
    print(f"{'Bell Pepper Class':<42} | {'Total':>5} | {'Exact':>5} | {'pHash':>5} | {'Unmatched':>9} | {'Match %':>7}")
    print("-" * 80)
    total_all = 0
    total_exact = 0
    total_perceptual = 0
    total_unmatched = 0

    for c in TARGET_BELL_CLASSES:
        st = stats_per_bell_class[c]
        matched = st["exact"] + st["perceptual"]
        pct = (matched / st["total"] * 100) if st["total"] > 0 else 0.0
        print(
            f"{c:<42} | {st['total']:>5} | {st['exact']:>5} | {st['perceptual']:>5} | {st['unmatched']:>9} | {pct:>6.1f}%"
        )
        total_all += st["total"]
        total_exact += st["exact"]
        total_perceptual += st["perceptual"]
        total_unmatched += st["unmatched"]

    total_matched = total_exact + total_perceptual
    total_pct = (total_matched / total_all * 100) if total_all > 0 else 0.0
    print("-" * 80)
    print(
        f"{'TOTAL':<42} | {total_all:>5} | {total_exact:>5} | {total_perceptual:>5} | {total_unmatched:>9} | {total_pct:>6.1f}%"
    )

    print("\n" + "=" * 80)
    print("TABLE 2: SPLIT-COMBINATION PAIR DISTRIBUTION (Bell Split x Chilli Split)")
    print("=" * 80)
    print(f"{'Bell Pepper Split':<20} | {'Chilli Split':<20} | {'Match Pair Count':>16}")
    print("-" * 65)
    for b_s in SPLITS:
        for ch_s in SPLITS:
            cnt = split_pair_counts[(b_s, ch_s)]
            if cnt > 0:
                print(f"{b_s:<20} | {ch_s:<20} | {cnt:>16}")
            else:
                print(f"{b_s:<20} | {ch_s:<20} | {0:>16}")

    print("\n" + "=" * 80)
    print("TABLE 3: BELL PEPPER CLASS TO CHILLI CLASS MAPPING")
    print("=" * 80)
    print(f"{'Source Bell Pepper Class':<42} -> {'Destination Chilli Class':<30} : {'Pairs':>6}")
    print("-" * 85)
    for (b_cls, ch_cls), cnt in sorted(mapping_counts.items(), key=lambda x: -x[1]):
        print(f"{b_cls:<42} -> {ch_cls:<30} : {cnt:>6}")
    print("=" * 80)


if __name__ == "__main__":
    main()
