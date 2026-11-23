"""
scrape_bing.py — Scrape plant disease images from Bing Image Search API.

╔══════════════════════════════════════════════════════════════╗
║  Requires a FREE Bing Search API key from Azure (5 min setup) ║
║  Free tier: 1,000 queries/month, no rate limiting            ║
╚══════════════════════════════════════════════════════════════╝

How to get the free API key (takes ~5 minutes)
-----------------------------------------------
1. Go to https://portal.azure.com  (sign in with any Microsoft account)
2. Search for "Bing Search v7" in the marketplace
3. Create resource -> Free tier F1 (1000 queries/month free)
4. Go to Keys and Endpoint -> copy Key 1
5. Set the environment variable:
       $env:BING_API_KEY = "your_key_here"    (PowerShell)
   Or pass it directly:
       python scripts/scrape_bing.py --api-key YOUR_KEY

Why Bing over DuckDuckGo
-------------------------
- DuckDuckGo: unofficial scraping, blocks with 403 after ~5 requests
- Bing: official API, structured JSON, 1000 free queries/month, never rate-limits
  in the free tier

Output
------
- Images:   data/scraped_v2/<class_name>/img_bing_NNNNN.jpg
- Manifest: data/scraped_v2/scrape_manifest_bing.csv

Usage
-----
    $env:BING_API_KEY = "abc123..."
    python scripts/scrape_bing.py
    python scripts/scrape_bing.py --max-per-class 150
    python scripts/scrape_bing.py --classes "Raspberry - raspberry yellow rust"
    python scripts/scrape_bing.py --api-key YOUR_KEY

Comparison vs scrape_inaturalist.py
-------------------------------------
| Feature         | iNaturalist              | Bing (this)           |
|-----------------|-------------------------|-----------------------|
| API key needed  | No                      | Yes (free, 5 min)     |
| Image quality   | Research-grade verified | Mixed quality         |
| Volume/class    | 10-500+                 | Up to 150             |
| Rate limiting   | None                    | None (free tier)      |
| Best for        | All diseases (primary)  | Classes iNat misses   |

Recommendation
--------------
Use scrape_inaturalist.py FIRST.
Use this script as a SUPPLEMENT for classes where iNaturalist returned < 50 images.
The log from scrape_inaturalist.py will list exactly which classes need supplementing.
"""

import argparse
import csv
import io
import logging
import os
import time
from pathlib import Path

import imagehash
import requests
from PIL import Image

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUT_DIR      = PROJECT_ROOT / "data" / "scraped_v2"
MANIFEST     = OUT_DIR / "scrape_manifest_bing.csv"
TRAIN_DIR    = PROJECT_ROOT / "data" / "processed" / "train"

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
BING_ENDPOINT   = "https://api.bing.microsoft.com/v7.0/images/search"
MIN_RESOLUTION  = 150
PHASH_THRESHOLD = 10
REQUEST_TIMEOUT = 15
SLEEP_BETWEEN   = 0.3

# ---------------------------------------------------------------------------
# Disease -> search query mapping
# Combines common name + scientific name for precision.
# For Bing, specific queries work better than generic ones.
# ---------------------------------------------------------------------------
DISEASE_QUERY_MAP: dict[str, str] = {
    # Apple
    "Apple - apple black rot":                          "apple black rot Botryosphaeria obtusa disease leaf",
    "Apple - apple scab":                               "apple scab Venturia inaequalis disease leaf",
    "Apple - Rust":                                     "apple rust Gymnosporangium disease leaf",
    # Banana
    "Banana - banana black leaf streak":                "banana black leaf streak Mycosphaerella fijiensis",
    "Banana - banana cordana leaf spot":                "banana cordana leaf spot Cordana musae disease",
    "Banana - Sigatoka":                                "banana sigatoka Mycosphaerella musicola leaf",
    "Banana - banana cigar end rot":                    "banana cigar end rot Trachysphaera disease",
    "Banana - banana panama disease":                   "banana panama disease Fusarium oxysporum wilt",
    # Bean
    "Bean - bean halo blight":                          "bean halo blight Pseudomonas savastanoi leaf",
    "Bean - bean mosaic virus":                         "bean common mosaic virus disease leaf",
    "Bean - bean rust":                                 "bean rust Uromyces appendiculatus leaf",
    # Bell pepper
    "Bell pepper - bell pepper frogeye leaf spot":      "bell pepper frogeye leaf spot Cercospora capsici",
    "Bell pepper - bell pepper powdery mildew":         "pepper powdery mildew Leveillula taurica leaf",
    # Blueberry
    "Blueberry - blueberry scorch":                     "blueberry scorch virus disease leaf",
    "Blueberry - blueberry anthracnose":                "blueberry anthracnose Colletotrichum disease",
    "Blueberry - blueberry rust":                       "blueberry rust Thekopsora minima leaf",
    "Blueberry - blueberry mummy berry":                "blueberry mummy berry Monilinia vaccinii disease",
    # Broccoli
    "Broccoli - broccoli alternaria leaf spot":         "broccoli alternaria leaf spot Alternaria brassicicola",
    "Broccoli - broccoli downy mildew":                 "broccoli downy mildew Hyaloperonospora disease",
    # Cabbage
    "Cabbage - cabbage alternaria leaf spot":           "cabbage alternaria leaf spot Alternaria brassicicola",
    # Carrot
    "Carrot - carrot alternaria leaf blight":           "carrot alternaria leaf blight Alternaria dauci",
    # Cauliflower
    "Cauliflower - cauliflower alternaria leaf spot":   "cauliflower alternaria leaf spot Alternaria",
    "Cauliflower - cauliflower bacterial soft rot":     "cauliflower bacterial soft rot Pectobacterium",
    # Celery
    "Celery - celery anthracnose":                      "celery anthracnose Colletotrichum disease leaf",
    "Celery - celery early blight":                     "celery early blight Cercospora apii disease",
    # Cherry
    "Cherry - cherry powdery mildew":                   "cherry powdery mildew Podosphaera clandestina",
    # Chilli
    "Chilli - Leafspot":                                "chilli leaf spot Cercospora capsici disease",
    "Chilli - Whitefly":                                "chilli whitefly Bemisia tabaci infestation leaf",
    # Coffee
    "Coffee - coffee berry blotch":                     "coffee berry blotch Cercospora coffeicola disease",
    # Corn
    "Corn - corn gray leaf spot":                       "corn gray leaf spot Cercospora zeae-maydis",
    "Corn - corn northern leaf blight":                 "corn northern leaf blight Setosphaeria turcica",
    "Corn - Leaf Blight":                               "corn leaf blight Helminthosporium disease",
    "Corn - Rust":                                      "corn rust Puccinia sorghi leaf disease",
    # Cucumber
    "Cucumber - cucumber angular leaf spot":            "cucumber angular leaf spot Pseudomonas disease",
    # Eggplant
    "Eggplant - eggplant cercospora leaf spot":         "eggplant cercospora leaf spot Cercospora disease",
    "Eggplant - eggplant phomopsis fruit rot":          "eggplant phomopsis fruit rot Phomopsis vexans",
    "Eggplant - eggplant phytophthora blight":          "eggplant phytophthora blight Phytophthora capsici",
    # Garlic
    "Garlic - garlic leaf blight":                      "garlic leaf blight Botrytis porri disease",
    # Ginger
    "Ginger - ginger leaf spot":                        "ginger leaf spot Phyllosticta zingiberi disease",
    # Grape
    "Grape - Black Rot":                                "grape black rot Guignardia bidwellii leaf",
    "Grape - grape downy mildew":                       "grape downy mildew Plasmopara viticola leaf",
    # Lettuce
    "Lettuce - lettuce mosaic virus":                   "lettuce mosaic virus disease leaf",
    # Paddy
    "Paddy - Bacterial Leaf Blight":                    "rice bacterial leaf blight Xanthomonas oryzae",
    # Plum
    "Plum - plum bacterial spot":                       "plum bacterial spot Xanthomonas arboricola disease",
    "Plum - plum pocket disease":                       "plum pocket disease Taphrina pruni",
    "Plum - plum pox virus":                            "plum pox virus sharka disease leaf",
    "Plum - plum rust":                                 "plum rust Tranzschelia pruni-spinosae leaf",
    # Potato
    "Potato - potato late blight":                      "potato late blight Phytophthora infestans leaf",
    # Raspberry
    "Raspberry - raspberry fire blight":                "raspberry fire blight Erwinia amylovora disease",
    "Raspberry - raspberry gray mold":                  "raspberry gray mold Botrytis cinerea disease",
    "Raspberry - raspberry leaf spot":                  "raspberry leaf spot Sphaerulina rubi disease",
    "Raspberry - raspberry yellow rust":                "raspberry yellow rust Phragmidium rubi-idaei",
    # Soybean
    "Soybean - soybean brown spot":                     "soybean brown spot Septoria glycines disease leaf",
    "Soybean - soybean frog eye leaf spot":             "soybean frogeye leaf spot Cercospora sojina",
    # Squash
    "Squash - Powdery Mildew":                          "squash powdery mildew Podosphaera xanthii leaf",
    # Strawberry
    "Strawberry - strawberry leaf scorch":              "strawberry leaf scorch Diplocarpon earlianum",
    "Strawberry - strawberry anthracnose":              "strawberry anthracnose Colletotrichum disease",
    # Sugarcane
    "Sugarcane - Mosaic":                               "sugarcane mosaic virus disease leaf",
    "Sugarcane - Rust":                                 "sugarcane rust Puccinia melanocephala leaf",
    # Tobacco
    "Tobacco - tobacco blue mold":                      "tobacco blue mold Peronospora tabacina disease",
    "Tobacco - tobacco frogeye leaf spot":              "tobacco frogeye leaf spot Cercospora nicotianae",
    "Tobacco - tobacco mosaic virus":                   "tobacco mosaic virus TMV disease leaf",
    "Tobacco - tobacco brown spot":                     "tobacco brown spot Alternaria alternata disease",
    # Tomato
    "Tomato - tomato early blight":                     "tomato early blight Alternaria solani disease leaf",
    "Tomato - tomato late blight":                      "tomato late blight Phytophthora infestans leaf",
    "Tomato - tomato mosaic virus":                     "tomato mosaic virus ToMV disease leaf",
    "Tomato - tomato septoria leaf spot":               "tomato septoria leaf spot Septoria lycopersici",
    "Tomato - tomato yellow leaf curl virus":           "tomato yellow leaf curl virus TYLCV disease",
    # Wheat
    "Wheat - wheat leaf rust":                          "wheat leaf rust Puccinia triticina disease",
    "Wheat - wheat septoria blotch":                    "wheat septoria blotch Zymoseptoria tritici",
    # Zucchini
    "Zucchini - zucchini bacterial wilt":               "zucchini bacterial wilt Erwinia tracheiphila",
    "Zucchini - zucchini downy mildew":                 "zucchini downy mildew Pseudoperonospora cubensis",
    "Zucchini - zucchini powdery mildew":               "zucchini powdery mildew Podosphaera disease",
    "Zucchini - zucchini yellow mosaic virus":          "zucchini yellow mosaic virus ZYMV disease",
}

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Bing search
# ---------------------------------------------------------------------------

def search_bing(query: str, api_key: str, count: int = 150) -> list[str]:
    """Call Bing Image Search API and return a list of image URLs."""
    headers = {"Ocp-Apim-Subscription-Key": api_key}
    params = {
        "q": query,
        "count": min(count, 150),   # Bing max per request
        "imageType": "Photo",
        "size": "Medium",
        "safeSearch": "Off",
    }
    try:
        resp = requests.get(BING_ENDPOINT, headers=headers, params=params,
                            timeout=REQUEST_TIMEOUT)
        if resp.status_code == 401:
            raise ValueError("Invalid Bing API key. Check BING_API_KEY env var.")
        resp.raise_for_status()
        data = resp.json()
        urls = [item["contentUrl"] for item in data.get("value", [])]
        logger.info("  Bing returned %d URLs for query: %s", len(urls), query)
        return urls
    except ValueError:
        raise
    except Exception as e:
        logger.warning("  Bing search failed: %s", e)
        return []


# ---------------------------------------------------------------------------
# Download & quality filter (same as scrape_inaturalist.py)
# ---------------------------------------------------------------------------

def is_solid_colour(img: Image.Image, threshold: float = 0.02) -> bool:
    arr = list(img.getdata())
    return len(set(arr)) / len(arr) < threshold


def download_and_filter(url: str, seen_hashes: set) -> Image.Image | None:
    try:
        resp = requests.get(url, timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()
        img = Image.open(io.BytesIO(resp.content)).convert("RGB")
    except Exception:
        return None

    if min(img.size) < MIN_RESOLUTION:
        return None
    if is_solid_colour(img):
        return None

    phash = str(imagehash.phash(img))
    for seen in seen_hashes:
        if imagehash.hex_to_hash(phash) - imagehash.hex_to_hash(seen) < PHASH_THRESHOLD:
            return None

    seen_hashes.add(phash)
    return img


# ---------------------------------------------------------------------------
# Per-class scraping
# ---------------------------------------------------------------------------

def scrape_class(
    class_name: str,
    query: str,
    api_key: str,
    max_per_class: int,
    dry_run: bool,
) -> list[dict]:
    logger.info("")
    logger.info("[%s]", class_name)
    logger.info("  Query: %s", query)

    urls = search_bing(query, api_key, count=max_per_class + 50)
    time.sleep(SLEEP_BETWEEN)

    out_dir = OUT_DIR / class_name
    if not dry_run:
        out_dir.mkdir(parents=True, exist_ok=True)

    seen_hashes: set[str] = set()
    rows: list[dict] = []
    saved = 0

    for url in urls:
        if saved >= max_per_class:
            break
        time.sleep(0.15)

        img = download_and_filter(url, seen_hashes)
        row = {
            "class": class_name,
            "query": query,
            "source_url": url,
            "source": "bing",
            "kept": False,
            "reason": "filtered",
            "filename": "",
        }

        if img is not None:
            fname = out_dir / f"img_bing_{saved:05d}.jpg"
            row["kept"] = True
            row["reason"] = ""
            row["filename"] = str(fname.relative_to(PROJECT_ROOT))
            if not dry_run:
                img.save(fname, "JPEG", quality=90)
            saved += 1

        rows.append(row)

    logger.info("  Done -> saved %d images", saved)
    return rows


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--api-key", default=os.environ.get("BING_API_KEY", ""),
                        help="Bing Search API key (or set BING_API_KEY env var)")
    parser.add_argument("--max-per-class", type=int, default=150)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--classes", nargs="+", default=None)
    args = parser.parse_args()

    if not args.api_key:
        print(
            "\nERROR: No Bing API key provided.\n"
            "  Option 1: Set env var:  $env:BING_API_KEY = 'your_key'\n"
            "  Option 2: Pass flag:    --api-key YOUR_KEY\n"
            "\nGet a free key at https://portal.azure.com (Bing Search v7, Free tier F1)\n"
        )
        raise SystemExit(1)

    log_dir = PROJECT_ROOT / "logs"
    log_dir.mkdir(exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)-8s %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(log_dir / "scrape_bing.log", mode="w"),
        ],
    )

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    targets = args.classes or list(DISEASE_QUERY_MAP.keys())

    logger.info("Bing scraper — %d target classes, max %d per class",
                len(targets), args.max_per_class)
    if args.dry_run:
        logger.info("DRY RUN — no images will be downloaded")

    all_rows: list[dict] = []
    for cls in targets:
        query = DISEASE_QUERY_MAP.get(cls)
        if not query:
            logger.warning("No query for '%s'", cls)
            continue
        rows = scrape_class(cls, query, args.api_key, args.max_per_class, args.dry_run)
        all_rows.extend(rows)
        time.sleep(SLEEP_BETWEEN)

    if not args.dry_run and all_rows:
        fieldnames = ["class", "query", "source_url", "source", "kept", "reason", "filename"]
        with open(MANIFEST, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=fieldnames)
            w.writeheader()
            w.writerows(all_rows)
        logger.info("Manifest -> %s", MANIFEST)

    kept = [r for r in all_rows if r["kept"]]
    logger.info("")
    logger.info("=" * 60)
    logger.info("Total images saved : %d", len(kept))
    logger.info("Next: update ingest_scraped.py to point to scraped_v2/ then re-run finetune")


if __name__ == "__main__":
    main()
