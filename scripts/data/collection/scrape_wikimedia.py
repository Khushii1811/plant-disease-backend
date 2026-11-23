"""
scripts/scrape_wikimedia.py — Scrape plant disease images from Wikimedia Commons.

Wikimedia Commons is completely open:
- NO API key required
- NO account required
- Research, museum, and university pathology photos

This script targets rare classes that were missing or had very few observations
in iNaturalist and PlantDoc.

Usage:
    python scripts/scrape_wikimedia.py [--max-per-class 50]
"""

import argparse
import csv
import io
import logging
from pathlib import Path
import time

from PIL import Image
import imagehash
import requests

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = PROJECT_ROOT / "data" / "scraped_v2"
MANIFEST_OUT = OUT_DIR / "scrape_manifest_wikimedia.csv"

COMMONS_API_URL = "https://commons.wikimedia.org/w/api.php"
MIN_RESOLUTION = 150
PHASH_THRESHOLD = 10
REQUEST_TIMEOUT = 20
SLEEP_BETWEEN = 0.5

USER_AGENT = "PlantDiseaseClassifier/1.0 (academic research; contact: botanical-ai@research.org)"

logger = logging.getLogger("scrape_wikimedia")

# Classes needing data with tailored Wikimedia Commons search terms
WIKI_TARGETS: dict[str, list[str]] = {
    "Zucchini - zucchini yellow mosaic virus": [
        "zucchini yellow mosaic virus",
        "ZYMV virus squash",
        "yellow mosaic virus cucurbit",
    ],
    "Plum - plum pox virus": [
        "plum pox virus plant",
        "sharka virus Prunus",
        "plum pox leaf disease",
    ],
    "Zucchini - zucchini bacterial wilt": [
        "Erwinia tracheiphila",
        "bacterial wilt cucurbit",
        "bacterial wilt squash",
    ],
    "Sugarcane - Mosaic": [
        "sugarcane mosaic virus",
        "SCMV sugarcane disease",
    ],
    "Blueberry - blueberry scorch": [
        "blueberry scorch virus",
        "blueberry scorch disease",
    ],
    "Tobacco - tobacco blue mold": [
        "Peronospora tabacina",
        "tobacco blue mold",
    ],
    "Ginger - ginger leaf spot": [
        "ginger leaf spot disease",
        "Phyllosticta zingiberis",
    ],
    "Banana - banana cigar end rot": [
        "banana cigar end rot",
        "Verticillium theobromae",
        "Trachysphaera fructigena",
    ],
    "Carrot - carrot alternaria leaf blight": [
        "Alternaria dauci",
        "carrot leaf blight Alternaria",
    ],
    "Eggplant - eggplant cercospora leaf spot": [
        "eggplant cercospora leaf spot",
        "Cercospora melongenae",
    ],
    "Eggplant - eggplant phytophthora blight": [
        "Phytophthora capsici eggplant",
        "eggplant phytophthora",
    ],
    "Garlic - garlic leaf blight": [
        "Stemphylium garlic leaf blight",
        "Botrytis garlic blight",
    ],
    "Tobacco - tobacco frogeye leaf spot": [
        "Cercospora nicotianae",
        "tobacco frogeye leaf spot",
    ],
    "Banana - Sigatoka": [
        "Pseudocercospora musae",
        "banana yellow sigatoka",
        "banana sigatoka leaf",
    ],
    "Banana - banana cordana leaf spot": [
        "Cordana musae",
        "banana cordana leaf spot",
    ],
    "Banana - banana panama disease": [
        "Fusarium oxysporum cubense",
        "banana panama disease wilt",
    ],
    "Lettuce - lettuce mosaic virus": [
        "lettuce mosaic virus",
        "LMV lettuce leaf",
    ],
    "Chilli - Leafspot": [
        "chilli leaf spot Cercospora",
        "pepper leaf spot disease Xanthomonas",
    ],
    "Tobacco - tobacco mosaic virus": [
        "tobacco mosaic virus TMV leaf",
        "tobacco mosaic symptoms",
    ],
    "Raspberry - raspberry leaf spot": [
        "raspberry leaf spot Sphaerulina",
        "Mycosphaerella rubi raspberry",
    ],
}


def load_existing_hashes() -> set[str]:
    seen: set[str] = set()
    manifests = [
        OUT_DIR / "scrape_manifest_inat.csv",
        OUT_DIR / "scrape_manifest_plantdoc.csv",
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


def search_wikimedia(query: str, limit: int = 50) -> list[dict]:
    """Queries Wikimedia Commons API for image files."""
    headers = {"User-Agent": USER_AGENT}
    params = {
        "action": "query",
        "generator": "search",
        "gsrsearch": f"{query} filetype:bitmap",
        "gsrnamespace": "6",  # File namespace
        "gsrlimit": min(limit, 50),
        "prop": "imageinfo",
        "iiprop": "url|size|mime|extmetadata",
        "format": "json",
    }
    try:
        r = requests.get(COMMONS_API_URL, params=params, headers=headers, timeout=REQUEST_TIMEOUT)
        if r.status_code != 200:
            logger.warning("Wikimedia API HTTP %d for query: %s", r.status_code, query)
            return []
        data = r.json()
        pages = data.get("query", {}).get("pages", {})
        results = []
        for pid, page in pages.items():
            title = page.get("title", "")
            imageinfo = page.get("imageinfo", [])
            if not imageinfo:
                continue
            info = imageinfo[0]
            url = info.get("url")
            mime = info.get("mime", "")
            if not url or not mime.startswith("image/"):
                continue
            # Skip vector or non-photographic formats
            if mime in ("image/svg+xml", "image/tiff"):
                continue
            results.append({
                "title": title,
                "url": url,
                "mime": mime,
                "width": info.get("width", 0),
                "height": info.get("height", 0),
            })
        return results
    except Exception as e:
        logger.warning("Search failed for query '%s': %s", query, e)
        return []


def download_and_filter(url: str, session: requests.Session) -> tuple[Image.Image | None, str | None]:
    try:
        r = session.get(url, timeout=REQUEST_TIMEOUT)
        if r.status_code != 200:
            return None, f"http_{r.status_code}"
        img = Image.open(io.BytesIO(r.content))
        img.load()
        if img.mode != "RGB":
            img = img.convert("RGB")
        w, h = img.size
        if w < MIN_RESOLUTION or h < MIN_RESOLUTION:
            return None, "low_res"
        return img, None
    except Exception as e:
        return None, str(e)


def main() -> None:
    parser = argparse.ArgumentParser(description="Scrape plant disease photos from Wikimedia Commons")
    parser.add_argument("--max-per-class", type=int, default=50, help="Max images per class to scrape")
    args = parser.parse_args()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    seen_hashes = load_existing_hashes()
    logger.info("Loaded %d existing phashes", len(seen_hashes))

    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT})

    manifest_rows = []
    class_saved: dict[str, int] = {}

    for cls_name, queries in WIKI_TARGETS.items():
        logger.info("Processing target class: %s", cls_name)
        target_dir = OUT_DIR / cls_name
        target_dir.mkdir(parents=True, exist_ok=True)
        class_saved[cls_name] = 0

        # Existing files in target folder
        existing_count = len(list(target_dir.glob("img_wiki_*.jpg")))

        seen_urls = set()
        for query in queries:
            if class_saved[cls_name] + existing_count >= args.max_per_class:
                break

            hits = search_wikimedia(query, limit=args.max_per_class)
            time.sleep(SLEEP_BETWEEN)

            for hit in hits:
                url = hit["url"]
                if url in seen_urls:
                    continue
                seen_urls.add(url)

                if class_saved[cls_name] + existing_count >= args.max_per_class:
                    break

                img, err = download_and_filter(url, session)
                time.sleep(SLEEP_BETWEEN)

                if img is None:
                    manifest_rows.append({
                        "class": cls_name,
                        "title": hit["title"],
                        "url": url,
                        "kept": False,
                        "reason": err,
                        "phash": "",
                        "filename": "",
                    })
                    continue

                ph = str(imagehash.phash(img))
                if is_duplicate(ph, seen_hashes):
                    manifest_rows.append({
                        "class": cls_name,
                        "title": hit["title"],
                        "url": url,
                        "kept": False,
                        "reason": "phash_dup",
                        "phash": ph,
                        "filename": "",
                    })
                    continue

                # Save valid image
                idx = existing_count + class_saved[cls_name]
                filename = f"img_wiki_{idx:05d}.jpg"
                dest_file = target_dir / filename
                img.save(dest_file, "JPEG", quality=90)

                seen_hashes.add(ph)
                class_saved[cls_name] += 1

                manifest_rows.append({
                    "class": cls_name,
                    "title": hit["title"],
                    "url": url,
                    "kept": True,
                    "reason": "",
                    "phash": ph,
                    "filename": str(dest_file.relative_to(PROJECT_ROOT)),
                })
                logger.info("   [SAVED] %s -> %s", cls_name, filename)

    # Save manifest
    write_header = not MANIFEST_OUT.exists()
    with open(MANIFEST_OUT, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["class", "title", "url", "kept", "reason", "phash", "filename"])
        if write_header:
            writer.writeheader()
        writer.writerows(manifest_rows)

    logger.info("")
    logger.info("=" * 70)
    logger.info("Wikimedia Commons Scraping Summary:")
    logger.info("%-50s %8s", "Class", "Saved")
    logger.info("-" * 70)
    total_saved = 0
    for cls_name, count in class_saved.items():
        logger.info("%-50s %8d", cls_name, count)
        total_saved += count
    logger.info("=" * 70)
    logger.info("Total images saved from Wikimedia Commons: %d", total_saved)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)-8s %(message)s")
    main()
