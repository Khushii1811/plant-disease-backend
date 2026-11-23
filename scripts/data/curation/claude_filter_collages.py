"""
scripts/claude_filter_collages.py — Auto-detect and remove collage/grid images
from data/raw/unified_scraped/.

Target pattern (as described):
  - 8 sub-images arranged in a grid (2x4, 4x2, etc.)
  - White border around the outer edge of the whole collage
  - White separator lines between grid panels inside

Detection logic (no ML, pure pixel analysis):
  Step 1 — White outer border: scan top/bottom/left/right N pixel strips.
            If >= 80% of those pixels are near-white (R,G,B > 220) on all 4 sides -> has border.
  Step 2 — Internal white separator lines: build row-wise and column-wise
            brightness profiles. Count runs of rows/cols that are >= 85% white.
  Step 3 — Panel count: (h_runs+1) x (v_runs+1). If >= MIN_PANELS -> collage.

Usage:
  python scripts/claude_filter_collages.py              # dry-run (lists flagged, no changes)
  python scripts/claude_filter_collages.py --move       # move flagged to data/claude_collage_flagged/
  python scripts/claude_filter_collages.py --delete     # permanently delete flagged
  python scripts/claude_filter_collages.py --panels 6   # only flag if >= 6 panels
  python scripts/claude_filter_collages.py --border 15  # wider border strip check
"""

import argparse
import shutil
import sys
from collections import Counter
from pathlib import Path

import numpy as np
from PIL import Image
from tqdm import tqdm

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore

ROOT        = Path(__file__).resolve().parent.parent
UNIFIED_RAW = ROOT / "data" / "raw" / "unified_scraped"
FLAGGED_DIR = ROOT / "data" / "claude_collage_flagged"
IMAGE_EXTS  = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}

WHITE_THRESH    = 220    # R,G,B must all be above this to count as near-white
BORDER_COVERAGE = 0.80   # fraction of border pixels that must be white
LINE_COVERAGE   = 0.85   # fraction of pixels in a row/col to call it a white separator line


def _white_fraction(pixels: np.ndarray) -> float:
    """Return fraction of pixels (shape N x 3) that are near-white."""
    return float(np.mean(np.all(pixels > WHITE_THRESH, axis=-1)))


def count_white_line_runs(profile: np.ndarray) -> int:
    """Count contiguous runs of white lines in a 1-D brightness profile."""
    in_run = False
    runs = 0
    for val in profile:
        if val >= LINE_COVERAGE:
            if not in_run:
                runs += 1
                in_run = True
        else:
            in_run = False
    return runs


def analyse_image(img_path: Path, border_width: int, min_panels: int) -> tuple[bool, str]:
    """
    Returns (is_collage: bool, reason: str).
    All thresholds passed as parameters — no module-level globals mutated.
    """
    try:
        with Image.open(img_path) as img:
            arr = np.array(img.convert("RGB"), dtype=np.uint8)
    except Exception as exc:
        return False, f"read error: {exc}"

    H, W, _ = arr.shape
    if H < border_width * 3 or W < border_width * 3:
        return False, "image too small"

    # Step 1 — white outer border
    top    = _white_fraction(arr[:border_width, :].reshape(-1, 3))
    bottom = _white_fraction(arr[-border_width:, :].reshape(-1, 3))
    left   = _white_fraction(arr[:, :border_width].reshape(-1, 3))
    right  = _white_fraction(arr[:, -border_width:].reshape(-1, 3))

    has_border = (top >= BORDER_COVERAGE and bottom >= BORDER_COVERAGE
                  and left >= BORDER_COVERAGE and right >= BORDER_COVERAGE)

    if not has_border:
        return False, "no white border"

    # Step 2 — internal white separator lines (exclude outer border pixels)
    inner = arr[border_width:-border_width, border_width:-border_width]
    row_profile = np.mean(np.all(inner > WHITE_THRESH, axis=-1), axis=1)
    col_profile = np.mean(np.all(inner > WHITE_THRESH, axis=-1), axis=0)

    h_runs = count_white_line_runs(row_profile)
    v_runs = count_white_line_runs(col_profile)

    # Step 3 — panel count
    total_panels = (h_runs + 1) * (v_runs + 1)

    if total_panels >= min_panels:
        return True, (
            f"WHITE BORDER + {total_panels}-panel grid "
            f"({h_runs+1} rows x {v_runs+1} cols, "
            f"{h_runs} h-sep, {v_runs} v-sep)"
        )

    return False, f"white border but only {total_panels} panel(s) — below threshold {min_panels}"


def main() -> None:
    parser = argparse.ArgumentParser(description="Collage/grid image filter for training or scraped data")
    parser.add_argument("--target-dir", type=str, default="data/processed/train", help="Directory to scan (e.g. data/processed/train or data/raw/unified_scraped)")
    parser.add_argument("--move",   action="store_true", help="Move flagged images to data/claude_collage_flagged/")
    parser.add_argument("--delete", action="store_true", help="Permanently delete flagged images")
    parser.add_argument("--border", type=int, default=10,  help="Border strip width in pixels (default 10)")
    parser.add_argument("--panels", type=int, default=4,   help="Min panel count to flag as collage (default 4)")
    parser.add_argument("--exclude-classes", type=str, default="Blueberry", help="Comma-separated class names or substrings to exclude from border checks (default: Blueberry)")
    args = parser.parse_args()

    if args.move and args.delete:
        print("ERROR: Use either --move or --delete, not both.")
        sys.exit(1)

    target_path = Path(args.target_dir)
    if not target_path.is_absolute():
        target_path = ROOT / target_path

    if not target_path.exists():
        print(f"ERROR: Target directory does not exist: {target_path}")
        sys.exit(1)

    excluded = [c.strip().lower() for c in args.exclude_classes.split(",") if c.strip()]

    print("=" * 70)
    print("  Collage / Grid Image Filter")
    print(f"  Target dir    : {target_path}")
    print(f"  Border strip  : {args.border} px  (coverage >= {BORDER_COVERAGE*100:.0f}%)")
    print(f"  Separator line: >= {LINE_COVERAGE*100:.0f}% white pixels per row/col")
    print(f"  Flag threshold: panels >= {args.panels}")
    print(f"  Exclusions    : {args.exclude_classes}")
    if args.move:
        print(f"  Action        : MOVE to {FLAGGED_DIR.name}/")
    elif args.delete:
        print(f"  Action        : DELETE permanently")
    else:
        print(f"  Action        : DRY-RUN (no files changed)")
    print("=" * 70)

    all_images = sorted(
        f for f in target_path.rglob("*") if f.suffix.lower() in IMAGE_EXTS
    )
    print(f"\nScanning {len(all_images):,} images …\n")

    flagged: list[tuple[Path, str]] = []
    clean_count = 0
    skipped_count = 0

    for img_path in tqdm(all_images, desc="Scanning", unit="img"):
        parent_name = img_path.parent.name.lower()
        if any(exc in parent_name for exc in excluded):
            skipped_count += 1
            clean_count += 1
            continue

        is_collage, reason = analyse_image(img_path, args.border, args.panels)
        if is_collage:
            flagged.append((img_path, reason))
        else:
            clean_count += 1

    # Summary
    print(f"\n{'=' * 70}")
    print(f"  RESULTS")
    print(f"{'=' * 70}")
    print(f"  Total scanned  : {len(all_images):,}")
    print(f"  Collages found : {len(flagged):,}")
    print(f"  Excluded/Clean : {clean_count:,} (Excluded: {skipped_count})")
    print(f"{'=' * 70}")

    if flagged:
        class_counts = Counter(p.parent.name for p, _ in flagged)
        print("\n  Collages per class (top 20):")
        for cls, cnt in class_counts.most_common(20):
            bar = "#" * min(cnt, 35)
            print(f"    {cnt:>5}  {bar:<35}  {cls}")

        print(f"\n  Flagged images list:")
        for p, reason in flagged:
            print(f"    [{p.parent.name}] {p.name} -> {reason}")

        if args.move:
            FLAGGED_DIR.mkdir(parents=True, exist_ok=True)
            moved = 0
            for p, _ in tqdm(flagged, desc="Moving", unit="file"):
                dst = FLAGGED_DIR / p.parent.name / p.name
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(p), str(dst))
                moved += 1
            print(f"\n  Moved {moved:,} collages → {FLAGGED_DIR}")

        elif args.delete:
            deleted = 0
            for p, _ in tqdm(flagged, desc="Deleting", unit="file"):
                try:
                    p.unlink()
                    deleted += 1
                except Exception:
                    pass
            print(f"\n  Deleted {deleted:,} collage images.")

        else:
            print(f"\n  Dry run done. Run with --move to quarantine or --delete to remove.")

    else:
        print("\n  No collages detected. Target directory is clean of grid images.")


if __name__ == "__main__":
    main()
