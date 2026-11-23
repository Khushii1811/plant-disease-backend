"""
scripts/download_kaggle_chilli.py — Dedicated downloader for Kaggle Chilli Dataset (suryiapooventhanr/chilli)
with real-time progress bar, live download speed, and ETA.
"""

import os
import sys
from pathlib import Path

# Ensure tqdm is available
try:
    from tqdm import tqdm
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "tqdm"])
    from tqdm import tqdm

PROJECT_ROOT = Path(__file__).resolve().parent.parent
TEMP_DOWNLOAD_DIR = PROJECT_ROOT / "data" / "raw" / "kaggle_chilli_download"
DOWNLOADS_DIR = Path.home() / "Downloads"


def main():
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass

    dataset_slug = "suryiapooventhanr/chilli"
    TEMP_DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)

    print("=" * 65)
    print(f"  ⬇️  DOWNLOADING KAGGLE DATASET: {dataset_slug}")
    print(f"  📁  Target Folder: {TEMP_DOWNLOAD_DIR}")
    print("=" * 65)

    # Check if already downloaded in Downloads or temp
    for candidate in [DOWNLOADS_DIR / "chilli.zip", DOWNLOADS_DIR / "CHILLI.zip", TEMP_DOWNLOAD_DIR / "chilli.zip"]:
        if candidate.exists() and candidate.stat().st_size > 50 * 1024 * 1024:
            print(f"\n[INFO] Found existing downloaded archive: {candidate}")
            print(f"File Size: {candidate.stat().st_size / (1024*1024):.1f} MB")
            print("Download already complete!")
            return

    try:
        import kaggle
        kaggle.api.authenticate()
        print("\n[INFO] Connecting to Kaggle API...")
        print("[INFO] Starting download with real-time stream progress:\n")
        
        kaggle.api.dataset_download_files(
            dataset_slug,
            path=str(TEMP_DOWNLOAD_DIR),
            quiet=False,
            unzip=False
        )

        zips = list(TEMP_DOWNLOAD_DIR.glob("*.zip"))
        if zips:
            zip_file = zips[0]
            size_mb = zip_file.stat().st_size / (1024 * 1024)
            print(f"\n[SUCCESS] Download completed successfully!")
            print(f"Saved to: {zip_file} ({size_mb:.1f} MB)")
            print("\nNext Step:")
            print("  Run the ingestion script to create splits:")
            print("  python scripts/ingest_kaggle_chilli.py")
        else:
            print("\n[NOTE] Files downloaded to target directory.")

    except Exception as e:
        print(f"\n[ERROR] Download error: {e}")
        print("\nAlternative: You can download the zip directly in your browser:")
        print(f"  👉 https://www.kaggle.com/datasets/{dataset_slug}")
        print(f"Place the zip in {DOWNLOADS_DIR} or {TEMP_DOWNLOAD_DIR} and run:")
        print("  python scripts/ingest_kaggle_chilli.py")


if __name__ == "__main__":
    main()
