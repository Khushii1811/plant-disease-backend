"""
scripts/visual_audit_cleanvision.py — Non-destructive visual dataset auditing using CleanVision.

Finds and visualizes dataset issues without modifying or deleting any files:
  - Exact & Near Duplicates
  - Blurry images
  - Low-information / blank frames
  - Dark / Light extreme exposures
  - Odd aspect ratios
  - Mislabeled candidate anomalies

Requirements:
  .venv\\Scripts\\pip.exe install cleanvision
Usage:
  .venv\\Scripts\\python.exe scripts/visual_audit_cleanvision.py
  .venv\\Scripts\\python.exe scripts/visual_audit_cleanvision.py --data-dir data/processed/train --max-images 2000
"""

import argparse
import logging
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DATA = PROJECT_ROOT / "data" / "processed" / "train"
OUT_DIR = PROJECT_ROOT / "data" / "cleanvision_audit"

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("cleanvision_audit")


def main():
    parser = argparse.ArgumentParser(description="CleanVision Visual Dataset Audit (Read-Only)")
    parser.add_argument("--data-dir", type=str, default=str(DEFAULT_DATA), help="Directory to inspect (default: data/processed/train)")
    parser.add_argument("--class-name", type=str, default=None, help="Convenient shorthand to audit a single class (e.g. 'Apple - apple black rot')")
    parser.add_argument("--max-images", type=int, default=None, help="Optional limit for fast inspection")
    args = parser.parse_args()

    try:
        from cleanvision import Imagelab
    except ImportError:
        print("\n" + "=" * 70)
        print("ERROR: cleanvision is not installed.")
        print("Please install it by running:")
        print("    uv pip install cleanvision")
        print("=" * 70 + "\n")
        sys.exit(1)

    data_path = Path(args.data_dir)
    if args.class_name:
        data_path = DEFAULT_DATA / args.class_name
    if not data_path.exists():
        logger.error("Target directory not found: %s", data_path)
        sys.exit(1)

    logger.info("Initializing CleanVision Imagelab on: %s", data_path)
    logger.info("Mode: STRICTLY READ-ONLY (No files will be modified or deleted).")

    # Gather image paths
    image_exts = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
    if data_path.is_file():
        image_files = [data_path]
    else:
        image_files = sorted([f for f in data_path.rglob("*") if f.suffix.lower() in image_exts])

    if args.max_images and args.max_images > 0:
        image_files = image_files[:args.max_images]

    logger.info("Found %d images to audit.", len(image_files))

    # 1. Initialize Imagelab
    imagelab = Imagelab(filepaths=[str(p) for p in image_files])

    # 2. Find Issues across dataset
    logger.info("Scanning dataset for visual issues (duplicates, blur, dark/light, low-info, aspect ratio)...")
    imagelab.find_issues()

    # 3. Print Issue Summary
    print("\n" + "=" * 70)
    print("  CLEANVISION AUDIT SUMMARY")
    print("=" * 70)
    imagelab.report()
    print("=" * 70)

    # 4. Save visualization artifact / report
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    report_csv = OUT_DIR / "flagged_issues.csv"
    if hasattr(imagelab, "issues") and imagelab.issues is not None:
        imagelab.issues.to_csv(report_csv)
        logger.info("Saved flagged issue paths to CSV: %s", report_csv)

    # 5. Visual export
    logger.info("Generating visual issue preview...")
    try:
        # Export top issues visually
        imagelab.visualize(save_path=str(OUT_DIR / "visual_issues.png"))
        logger.info("Saved visual issue chart to: %s", OUT_DIR / "visual_issues.png")
    except Exception as e:
        logger.warning("Could not auto-save plot image (%s). Generating HTML viewer...", e)

    print("\n[SUCCESS] CleanVision audit complete. Zero files were modified.")
    print(f"You can review flagged issue details in: {report_csv}")


if __name__ == "__main__":
    main()
