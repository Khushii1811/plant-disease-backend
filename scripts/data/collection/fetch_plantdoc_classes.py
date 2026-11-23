"""
scripts/fetch_plantdoc_classes.py — Fast direct harvester for PlantDoc classes.

Fetches file paths via GitHub Git Trees API and streams raw images directly from
raw.githubusercontent.com without downloading the full 1GB git commit history.
Applies resolution validation, image integrity, and perceptual hash deduplication.

Target Classes:
- Corn leaf blight -> Corn - Leaf Blight
- Bell_pepper leaf spot -> Bell pepper - bell pepper frogeye leaf spot
- Tomato Septoria leaf spot -> Tomato - tomato septoria leaf spot
- Corn Gray leaf spot -> Corn - corn gray leaf spot

Usage:
    python scripts/fetch_plantdoc_classes.py
"""

import csv
import io
import logging
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from PIL import Image
import imagehash
import requests

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = PROJECT_ROOT / "data" / "scraped_v2"
MANIFEST_OUT = OUT_DIR / "scrape_manifest_plantdoc.csv"

TREE_URL = "https://api.github.com/repos/pratikkayal/PlantDoc-Dataset/git/trees/master?recursive=1"
RAW_BASE = "https://raw.githubusercontent.com/pratikkayal/PlantDoc-Dataset/master"

MIN_RESOLUTION = 150
PHASH_THRESHOLD = 10
NUM_WORKERS = 8

logger = logging.getLogger("fetch_plantdoc")

CLASS_MAPPING: dict[str, str] = {
    "Corn leaf blight": "Corn - Leaf Blight",
    "Bell_pepper leaf spot": "Bell pepper - bell pepper frogeye leaf spot",
    "Tomato Septoria leaf spot": "Tomato - tomato septoria leaf spot",
    "Corn Gray leaf spot": "Corn - corn gray leaf spot",
}


def load_existing_hashes() -> set[str]:
    seen: set[str] = set()
    manifests = [
        OUT_DIR / "scrape_manifest_inat.csv",
        OUT_DIR / "scrape_manifest_wikimedia.csv",
        PROJECT_ROOT / "data" / "scraped" / "scrape_manifest.csv",
        MANIFEST_OUT,
    ]
    for mpath in manifests:
        if not mpath.exists():
            continue
        try:
            with open(mpath, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    ph = row.get("phash", "").strip()
                    if ph:
                        seen.add(ph)
        except Exception:
            pass
    return seen


def is_duplicate(img_hash: str, seen_hashes: set[str], threshold: int = PHASH_THRESHOLD) -> bool:
    h = imagehash.hex_to_hash(img_hash)
    for s in seen_hashes:
        try:
            if h - imagehash.hex_to_hash(s) < threshold:
                return True
        except Exception:
            continue
    return False


def download_single(item_path: str, target_class: str, session: requests.Session) -> dict:
    url = f"{RAW_BASE}/{requests.utils.quote(item_path)}"
    try:
        r = session.get(url, timeout=20)
        if r.status_code != 200:
            return {"status": "error", "error": f"http_{r.status_code}", "path": item_path, "class": target_class}

        img = Image.open(io.BytesIO(r.content))
        img.load()
        if img.mode != "RGB":
            img = img.convert("RGB")

        w, h = img.size
        if w < MIN_RESOLUTION or h < MIN_RESOLUTION:
            return {"status": "error", "error": "low_res", "path": item_path, "class": target_class}

        ph = str(imagehash.phash(img))
        return {
            "status": "ok",
            "img": img,
            "phash": ph,
            "path": item_path,
            "class": target_class,
            "url": url,
        }
    except Exception as e:
        return {"status": "error", "error": str(e), "path": item_path, "class": target_class}


def main() -> None:
    logger.info("Fetching PlantDoc file tree...")
    r = requests.get(TREE_URL, timeout=30)
    if r.status_code != 200:
        logger.error("Failed to fetch tree from GitHub API: HTTP %d", r.status_code)
        return

    tree = r.json().get("tree", [])
    logger.info("Total items in PlantDoc tree: %d", len(tree))

    # Match items
    tasks: list[tuple[str, str]] = []  # (item_path, target_class)
    for item in tree:
        path = item.get("path", "")
        if not (path.lower().endswith(".jpg") or path.lower().endswith(".png") or path.lower().endswith(".jpeg")):
            continue
        for pd_class, target_class in CLASS_MAPPING.items():
            if f"/{pd_class}/" in f"/{path}":
                tasks.append((path, target_class))
                break

    logger.info("Identified %d candidate images across %d target classes", len(tasks), len(CLASS_MAPPING))

    seen_hashes = load_existing_hashes()
    logger.info("Loaded %d existing phashes for cross-deduplication", len(seen_hashes))

    session = requests.Session()
    manifest_rows = []
    saved_counts: dict[str, int] = {cls: 0 for cls in CLASS_MAPPING.values()}

    logger.info("Downloading images with %d workers...", NUM_WORKERS)
    with ThreadPoolExecutor(max_workers=NUM_WORKERS) as executor:
        futures = [executor.submit(download_single, path, cls, session) for path, cls in tasks]
        for f in as_completed(futures):
            res = f.result()
            cls_name = res["class"]
            if res["status"] != "ok":
                manifest_rows.append({
                    "class": cls_name,
                    "source_path": res["path"],
                    "url": f"{RAW_BASE}/{res['path']}",
                    "kept": False,
                    "reason": res.get("error", "unknown"),
                    "phash": "",
                    "filename": "",
                })
                continue

            ph = res["phash"]
            if is_duplicate(ph, seen_hashes):
                manifest_rows.append({
                    "class": cls_name,
                    "source_path": res["path"],
                    "url": res["url"],
                    "kept": False,
                    "reason": "phash_dup",
                    "phash": ph,
                    "filename": "",
                })
                continue

            # Save file
            target_dir = OUT_DIR / cls_name
            target_dir.mkdir(parents=True, exist_ok=True)
            idx = len(list(target_dir.glob("img_plantdoc_*.jpg")))
            dest_file = target_dir / f"img_plantdoc_{idx:05d}.jpg"

            res["img"].save(dest_file, "JPEG", quality=92)
            seen_hashes.add(ph)
            saved_counts[cls_name] += 1

            manifest_rows.append({
                "class": cls_name,
                "source_path": res["path"],
                "url": res["url"],
                "kept": True,
                "reason": "",
                "phash": ph,
                "filename": str(dest_file.relative_to(PROJECT_ROOT)),
            })

    # Write manifest
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(MANIFEST_OUT, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["class", "source_path", "url", "kept", "reason", "phash", "filename"])
        writer.writeheader()
        writer.writerows(manifest_rows)

    logger.info("")
    logger.info("=" * 70)
    logger.info("PlantDoc Harvest Summary:")
    logger.info("%-50s %8s", "Class", "Saved")
    logger.info("-" * 70)
    total_saved = 0
    for cls_name, count in saved_counts.items():
        logger.info("%-50s %8d", cls_name, count)
        total_saved += count
    logger.info("=" * 70)
    logger.info("Total PlantDoc images saved: %d", total_saved)
    logger.info("Manifest saved to: %s", MANIFEST_OUT)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)-8s %(message)s")
    main()
