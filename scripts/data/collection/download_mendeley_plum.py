"""
scripts/download_mendeley_plum.py

High-Speed Resumable Multi-Stream Downloader for Mendeley Plum Dataset (6.75 GB).
Dataset DOI: 10.17632/w7sdx55m7z.1

Upgrades:
- Resumable: automatically inspects existing temp parts and resumes without redownloading.
- Robust Retry: catches ReadTimeoutError / ConnectionError and retries up to 5 times per stream.
- Extended timeout: 90 seconds to tolerate AWS S3 bandwidth throttling.
- Dynamic assembly & automatic extraction of the 'Original' folder.
"""

import argparse
import os
import sys
import threading
import time
import zipfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import requests
from tqdm import tqdm

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_ROOT / "data" / "raw" / "plum_raw"
DEST_ZIP = RAW_DIR / "mendeley_plum_dataset.zip"
EXTRACT_DIR = RAW_DIR / "mendeley_extracted"

NUM_THREADS = 16
READ_TIMEOUT = 90
MAX_RETRIES = 5


class DownloadProgressTracker:
    def __init__(self, total_size, initial=0, desc="🚀 Resumable Multi-Stream Download"):
        self.lock = threading.Lock()
        self.pbar = tqdm(
            total=total_size,
            initial=initial,
            unit="iB",
            unit_scale=True,
            unit_divisor=1024,
            desc=desc,
        )

    def update(self, n):
        with self.lock:
            self.pbar.update(n)

    def close(self):
        self.pbar.close()


def download_chunk_resumable(url, start_byte, end_byte, chunk_idx, temp_dir, tracker):
    chunk_file = temp_dir / f"part_{chunk_idx:03d}.tmp"
    expected_size = end_byte - start_byte + 1

    # Check already downloaded bytes
    downloaded = 0
    if chunk_file.exists():
        downloaded = chunk_file.stat().st_size
        if downloaded >= expected_size:
            # Already complete
            return chunk_idx, chunk_file

    retries = 0
    while retries < MAX_RETRIES:
        current_start = start_byte + downloaded
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Range": f"bytes={current_start}-{end_byte}",
        }

        try:
            resp = requests.get(url, headers=headers, stream=True, timeout=READ_TIMEOUT)
            if resp.status_code not in (200, 206):
                resp.raise_for_status()

            with open(chunk_file, "ab" if downloaded > 0 else "wb") as f:
                for b in resp.iter_content(chunk_size=1024 * 256):  # 256 KB buffer
                    if b:
                        f.write(b)
                        downloaded += len(b)
                        tracker.update(len(b))

            if downloaded >= expected_size:
                return chunk_idx, chunk_file

        except (requests.exceptions.RequestException, TimeoutError) as e:
            retries += 1
            time.sleep(2 * retries)
            if retries >= MAX_RETRIES:
                raise RuntimeError(f"Chunk {chunk_idx:03d} failed after {MAX_RETRIES} retries: {e}") from e

    return chunk_idx, chunk_file


def fast_resumable_download(url, dest_path, num_workers=NUM_THREADS):
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    temp_dir = dest_path.parent / "temp_parts"
    temp_dir.mkdir(parents=True, exist_ok=True)

    print(f"Connecting to remote server...")
    head_resp = requests.head(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=20, allow_redirects=True)
    head_resp.raise_for_status()

    total_size = int(head_resp.headers.get("content-length", 0))
    print(f"File size confirmed: {total_size / (1024 * 1024):.1f} MB ({total_size / (1024**3):.2f} GB)")

    # Check for existing partial downloads
    initial_bytes = 0
    part_size = total_size // num_workers
    ranges = []
    for i in range(num_workers):
        start = i * part_size
        end = total_size - 1 if i == num_workers - 1 else (i + 1) * part_size - 1
        pfile = temp_dir / f"part_{i:03d}.tmp"
        if pfile.exists():
            existing = pfile.stat().st_size
            if existing <= (end - start + 1):
                initial_bytes += existing
            else:
                pfile.unlink()  # corrupted / larger than expected chunk
        ranges.append((start, end, i))

    if initial_bytes > 0:
        print(f"🔄 Resuming from {initial_bytes / (1024 * 1024):.1f} MB already downloaded on disk!")

    print(f"Launching {num_workers} parallel Range streams with auto-retry...")
    tracker = DownloadProgressTracker(total_size, initial=initial_bytes)
    part_files = {}

    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        futures = {
            executor.submit(download_chunk_resumable, url, r[0], r[1], r[2], temp_dir, tracker): r[2]
            for r in ranges
        }
        for future in as_completed(futures):
            idx, pfile = future.result()
            part_files[idx] = pfile

    tracker.close()

    print(f"\n📦 Assembling {num_workers} parts into {dest_path.name}...")
    with open(dest_path, "wb") as out_f:
        for i in range(num_workers):
            pfile = part_files[i]
            with open(pfile, "rb") as in_f:
                while chunk := in_f.read(1024 * 1024 * 4):  # 4 MB buffer
                    out_f.write(chunk)
            pfile.unlink()
    temp_dir.rmdir()
    print(f"✅ Assembly complete: {dest_path.stat().st_size / (1024 * 1024):.1f} MB")


def extract_zip(zip_path, extract_to):
    print(f"\n📂 Extracting {zip_path.name} to {extract_to.relative_to(PROJECT_ROOT)}...")
    extract_to.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, "r") as z:
        z.extractall(extract_to)
    print("✅ Extraction complete!")

    for nested in list(extract_to.rglob("*.zip")):
        print(f"📦 Extracting nested archive: {nested.name}...")
        with zipfile.ZipFile(nested, "r") as nz:
            nz.extractall(nested.parent)


def audit_extracted_contents(extract_to):
    print("\n" + "=" * 80)
    print("  📁 EXTRACTED DATASET AUDIT")
    print("=" * 80)
    found_original = None
    for p in extract_to.rglob("*"):
        if p.is_dir():
            files = [f for f in p.iterdir() if f.is_file()]
            if files:
                rel = p.relative_to(extract_to)
                print(f"  📁 {rel}: {len(files)} files")
                if "original" in str(p).lower():
                    found_original = p

    if found_original:
        print(f"\n✅ Located target 'Original' folder at: {found_original.relative_to(PROJECT_ROOT)}")


def main():
    parser = argparse.ArgumentParser(description="Resumable multi-threaded downloader for Mendeley Plum dataset")
    parser.add_argument("--url", type=str, default=None, help="Direct download URL or S3 URL")
    parser.add_argument("--threads", type=int, default=NUM_THREADS, help="Number of parallel download threads (default: 8)")
    args = parser.parse_args()

    print("=" * 80)
    print("  🍑 RESUMABLE MULTI-STREAM MENDELEY PLUM DATASET DOWNLOADER")
    print("  DOI: 10.17632/w7sdx55m7z.1")
    print("=" * 80)

    url = args.url
    if not url:
        if DEST_ZIP.exists() and DEST_ZIP.stat().st_size > 1024 * 1024:
            print(f"✅ Found existing archive: {DEST_ZIP.name} ({DEST_ZIP.stat().st_size / (1024*1024):.1f} MB)")
            extract_zip(DEST_ZIP, EXTRACT_DIR)
            audit_extracted_contents(EXTRACT_DIR)
            return

        print("\nUsage:")
        print("  python scripts/download_mendeley_plum.py --url \"<URL>\"")
        return

    fast_resumable_download(url, DEST_ZIP, num_workers=args.threads)
    extract_zip(DEST_ZIP, EXTRACT_DIR)
    audit_extracted_contents(EXTRACT_DIR)


if __name__ == "__main__":
    main()
