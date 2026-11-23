"""
scrape_inaturalist.py — Scrape plant disease images from iNaturalist.

╔══════════════════════════════════════════════════════════╗
║  NO API KEY REQUIRED.  Free, unlimited, research-grade.  ║
╚══════════════════════════════════════════════════════════╝

How it works
------------
iNaturalist is a citizen-science platform with millions of expert-verified
(research-grade) nature observations, each with one or more photos.

1. For each disease class, DISEASE_TAXON_MAP provides the scientific name
   of the pathogen.
2. GET /v1/taxa?q=<scientific_name> resolves it to a numeric taxon_id.
3. GET /v1/observations?taxon_id=<id>&quality_grade=research&photos=true
   pages through all research-grade observations with photos.
4. Photo URLs are collected (upgraded from 'square' to 'large').
5. Images are downloaded, quality-filtered, and saved.

Quality pipeline
----------------
- Min resolution: 150 x 150 px
- Perceptual hash dedup: hamming distance < 10 rejects near-duplicates
- Solid-colour placeholder rejection

Output
------
- Images:   data/scraped_v2/<class_name>/img_inat_NNNNN.jpg
- Manifest: data/scraped_v2/scrape_manifest_inat.csv

Usage
-----
    python scripts/scrape_inaturalist.py
    python scripts/scrape_inaturalist.py --max-per-class 200
    python scripts/scrape_inaturalist.py --dry-run
    python scripts/scrape_inaturalist.py --classes "Raspberry - raspberry yellow rust"

Comparison vs scrape_bing.py
-----------------------------
| Feature         | iNaturalist (this) | Bing (scrape_bing.py) |
|-----------------|--------------------|-----------------------|
| API key needed  | No                 | Yes (free Azure key)  |
| Image quality   | Research-grade     | Mixed                 |
| Volume/class    | 10-500+            | Up to 150             |
| Rate limiting   | None               | None (free tier)      |
| Best for        | Most diseases      | Supplement/fallback   |

Recommendation: run this first. For classes returning < 50 images,
supplement with scrape_bing.py.
"""

import argparse
import csv
import io
import logging
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
MANIFEST     = OUT_DIR / "scrape_manifest_inat.csv"
TRAIN_DIR    = PROJECT_ROOT / "data" / "processed" / "train"

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
INAT_TAXA_URL   = "https://api.inaturalist.org/v1/taxa"
INAT_OBS_URL    = "https://api.inaturalist.org/v1/observations"
MIN_RESOLUTION  = 150
PHASH_THRESHOLD = 10
REQUEST_TIMEOUT = 15
SLEEP_BETWEEN   = 0.5

# ---------------------------------------------------------------------------
# Disease -> Scientific name mapping
# Covers the 60 DDG-rate-limited classes + 15 under-50-image classes
# ---------------------------------------------------------------------------
DISEASE_TAXON_MAP: dict[str, str] = {
    # Apple
    "Apple - apple black rot":                          "Botryosphaeria obtusa",
    "Apple - apple scab":                               "Venturia inaequalis",
    "Apple - Rust":                                     "Gymnosporangium juniperi-virginianae",
    # Banana
    "Banana - banana black leaf streak":                "Mycosphaerella fijiensis",
    "Banana - banana cordana leaf spot":                "Cordana musae",
    "Banana - Sigatoka":                                "Mycosphaerella musicola",
    "Banana - banana cigar end rot":                    "Trachysphaera fructigena",
    "Banana - banana panama disease":                   "Fusarium oxysporum",
    # Bean
    "Bean - bean halo blight":                          "Pseudomonas savastanoi",
    "Bean - bean mosaic virus":                         "Potyvirus",
    "Bean - bean rust":                                 "Uromyces appendiculatus",
    # Bell pepper
    "Bell pepper - bell pepper frogeye leaf spot":      "Cercospora capsici",
    "Bell pepper - bell pepper powdery mildew":         "Leveillula taurica",
    # Blueberry
    "Blueberry - blueberry scorch":                     "Blueberry scorch virus",
    "Blueberry - blueberry anthracnose":                "Colletotrichum acutatum",
    "Blueberry - blueberry rust":                       "Thekopsora minima",
    "Blueberry - blueberry mummy berry":                "Monilinia vaccinii-corymbosi",
    # Broccoli
    "Broccoli - broccoli alternaria leaf spot":         "Alternaria brassicicola",
    "Broccoli - broccoli downy mildew":                 "Hyaloperonospora parasitica",
    # Cabbage
    "Cabbage - cabbage alternaria leaf spot":           "Alternaria brassicicola",
    # Carrot
    "Carrot - carrot alternaria leaf blight":           "Alternaria dauci",
    # Cauliflower
    "Cauliflower - cauliflower alternaria leaf spot":   "Alternaria brassicicola",
    "Cauliflower - cauliflower bacterial soft rot":     "Pectobacterium carotovorum",
    # Celery
    "Celery - celery anthracnose":                      "Colletotrichum acutatum",
    "Celery - celery early blight":                     "Cercospora apii",
    # Cherry
    "Cherry - cherry powdery mildew":                   "Podosphaera clandestina",
    # Chilli
    "Chilli - Leafspot":                                "Cercospora capsici",
    "Chilli - Whitefly":                                "Bemisia tabaci",
    # Coffee
    "Coffee - coffee berry blotch":                     "Cercospora coffeicola",
    # Corn
    "Corn - corn gray leaf spot":                       "Cercospora zeae-maydis",
    "Corn - corn northern leaf blight":                 "Setosphaeria turcica",
    "Corn - Leaf Blight":                               "Helminthosporium maydis",
    "Corn - Rust":                                      "Puccinia sorghi",
    # Cucumber
    "Cucumber - cucumber angular leaf spot":            "Pseudomonas syringae",
    # Eggplant
    "Eggplant - eggplant cercospora leaf spot":         "Cercospora solani",
    "Eggplant - eggplant phomopsis fruit rot":          "Phomopsis vexans",
    "Eggplant - eggplant phytophthora blight":          "Phytophthora capsici",
    # Garlic
    "Garlic - garlic leaf blight":                      "Botrytis porri",
    # Ginger
    "Ginger - ginger leaf spot":                        "Phyllosticta zingiberi",
    # Grape
    "Grape - Black Rot":                                "Guignardia bidwellii",
    "Grape - grape downy mildew":                       "Plasmopara viticola",
    # Lettuce
    "Lettuce - lettuce mosaic virus":                   "Lettuce mosaic virus",
    # Paddy
    "Paddy - Bacterial Leaf Blight":                    "Xanthomonas oryzae",
    # Plum
    "Plum - plum bacterial spot":                       "Xanthomonas arboricola",
    "Plum - plum pocket disease":                       "Taphrina pruni",
    "Plum - plum pox virus":                            "Plum pox potyvirus",
    "Plum - plum rust":                                 "Tranzschelia pruni-spinosae",
    # Potato
    "Potato - potato late blight":                      "Phytophthora infestans",
    # Raspberry
    "Raspberry - raspberry fire blight":                "Erwinia amylovora",
    "Raspberry - raspberry gray mold":                  "Botrytis cinerea",
    "Raspberry - raspberry leaf spot":                  "Sphaerulina rubi",
    "Raspberry - raspberry yellow rust":                "Phragmidium rubi-idaei",
    # Soybean
    "Soybean - soybean brown spot":                     "Septoria glycines",
    "Soybean - soybean frog eye leaf spot":             "Cercospora sojina",
    # Squash
    "Squash - Powdery Mildew":                          "Podosphaera xanthii",
    # Strawberry
    "Strawberry - strawberry leaf scorch":              "Diplocarpon earlianum",
    "Strawberry - strawberry anthracnose":              "Colletotrichum acutatum",
    # Sugarcane
    "Sugarcane - Mosaic":                               "Sugarcane mosaic virus",
    "Sugarcane - Rust":                                 "Puccinia melanocephala",
    # Tobacco
    "Tobacco - tobacco blue mold":                      "Peronospora tabacina",
    "Tobacco - tobacco frogeye leaf spot":              "Cercospora nicotianae",
    "Tobacco - tobacco mosaic virus":                   "Tobacco mosaic virus",
    "Tobacco - tobacco brown spot":                     "Alternaria alternata",
    # Tomato
    "Tomato - tomato early blight":                     "Alternaria solani",
    "Tomato - tomato late blight":                      "Phytophthora infestans",
    "Tomato - tomato mosaic virus":                     "Tobamovirus",
    "Tomato - tomato septoria leaf spot":               "Septoria lycopersici",
    "Tomato - tomato yellow leaf curl virus":           "Begomovirus",
    # Wheat
    "Wheat - wheat leaf rust":                          "Puccinia triticina",
    "Wheat - wheat septoria blotch":                    "Zymoseptoria tritici",
    # Zucchini
    "Zucchini - zucchini bacterial wilt":               "Erwinia tracheiphila",
    "Zucchini - zucchini downy mildew":                 "Pseudoperonospora cubensis",
    "Zucchini - zucchini powdery mildew":               "Podosphaera xanthii",
    "Zucchini - zucchini yellow mosaic virus":          "Zucchini yellow mosaic virus",
}

logger = logging.getLogger(__name__)
session = requests.Session()
session.headers.update({"User-Agent": "PlantDiseaseML/1.0 (educational research)"})


# ---------------------------------------------------------------------------
# iNaturalist helpers
# ---------------------------------------------------------------------------

def resolve_taxon_id(scientific_name: str) -> int | None:
    """Resolve a scientific name to an iNaturalist taxon_id."""
    try:
        resp = session.get(
            INAT_TAXA_URL,
            params={"q": scientific_name, "rank": "species,genus,family", "per_page": 5},
            timeout=REQUEST_TIMEOUT,
        )
        resp.raise_for_status()
        results = resp.json().get("results", [])
        if results:
            taxon_id = results[0]["id"]
            matched_name = results[0]["name"]
            logger.info("  Taxon: '%s' -> id=%d (%s)", scientific_name, taxon_id, matched_name)
            return taxon_id
    except Exception as e:
        logger.warning("  Taxa lookup failed for '%s': %s", scientific_name, e)
    return None


def fetch_photo_urls(taxon_id: int, max_photos: int) -> list[str]:
    """Page through research-grade observations and collect photo URLs."""
    urls: list[str] = []
    page = 1
    per_page = 50

    while len(urls) < max_photos:
        try:
            resp = session.get(
                INAT_OBS_URL,
                params={
                    "taxon_id": taxon_id,
                    "quality_grade": "research",
                    "photos": "true",
                    "per_page": per_page,
                    "page": page,
                    "order": "desc",
                    "order_by": "votes",
                },
                timeout=REQUEST_TIMEOUT,
            )
            resp.raise_for_status()
            data = resp.json()
            results = data.get("results", [])
            if not results:
                break

            for obs in results:
                for photo in obs.get("photos", []):
                    url = photo.get("url", "").replace("/square.", "/large.")
                    if url and url not in urls:
                        urls.append(url)
                        if len(urls) >= max_photos:
                            break
                if len(urls) >= max_photos:
                    break

            total = data.get("total_results", 0)
            logger.info("  Page %d: %d URLs collected (iNat total: %d)", page, len(urls), total)

            if page * per_page >= total:
                break
            page += 1
            time.sleep(SLEEP_BETWEEN)

        except Exception as e:
            logger.warning("  Observation fetch failed (page %d): %s", page, e)
            break

    return urls


# ---------------------------------------------------------------------------
# Download & quality filter
# ---------------------------------------------------------------------------

def is_solid_colour(img: Image.Image, threshold: float = 0.02) -> bool:
    arr = list(img.getdata())
    return len(set(arr)) / len(arr) < threshold


def download_and_filter(url: str, seen_hashes: set) -> Image.Image | None:
    try:
        resp = session.get(url, timeout=REQUEST_TIMEOUT)
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
    scientific_name: str,
    max_per_class: int,
    dry_run: bool,
) -> list[dict]:
    logger.info("")
    logger.info("[%s]", class_name)
    logger.info("  Scientific name: %s", scientific_name)

    taxon_id = resolve_taxon_id(scientific_name)
    time.sleep(SLEEP_BETWEEN)

    if taxon_id is None:
        logger.warning("  Could not resolve taxon — skipping.")
        return [{"class": class_name, "scientific_name": scientific_name,
                 "taxon_id": "", "source_url": "", "source": "inaturalist",
                 "kept": False, "reason": "taxon_not_found", "filename": ""}]

    urls = fetch_photo_urls(taxon_id, max_photos=max_per_class * 3)
    logger.info("  %d candidate URLs fetched", len(urls))

    out_dir = OUT_DIR / class_name
    if not dry_run:
        out_dir.mkdir(parents=True, exist_ok=True)

    seen_hashes: set[str] = set()
    rows: list[dict] = []
    saved = 0

    for url in urls:
        if saved >= max_per_class:
            break
        time.sleep(0.1)

        img = download_and_filter(url, seen_hashes)
        row = {
            "class": class_name,
            "scientific_name": scientific_name,
            "taxon_id": taxon_id,
            "source_url": url,
            "source": "inaturalist",
            "kept": False,
            "reason": "filtered",
            "filename": "",
        }

        if img is not None:
            fname = out_dir / f"img_inat_{saved:05d}.jpg"
            row["kept"] = True
            row["reason"] = ""
            row["filename"] = str(fname.relative_to(PROJECT_ROOT))
            if not dry_run:
                img.save(fname, "JPEG", quality=90)
            saved += 1

        rows.append(row)

    logger.info("  Done -> saved %d / %d images", saved, max_per_class)
    return rows


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-per-class", type=int, default=200)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--classes", nargs="+", default=None)
    args = parser.parse_args()

    log_dir = PROJECT_ROOT / "logs"
    log_dir.mkdir(exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)-8s %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(log_dir / "scrape_inat.log", mode="w"),
        ],
    )

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    targets = args.classes or list(DISEASE_TAXON_MAP.keys())

    logger.info("iNaturalist scraper — %d target classes, max %d per class",
                len(targets), args.max_per_class)
    if args.dry_run:
        logger.info("DRY RUN — no images will be downloaded")

    all_rows: list[dict] = []
    for cls in targets:
        sci = DISEASE_TAXON_MAP.get(cls)
        if not sci:
            logger.warning("No scientific name for '%s' — add it to DISEASE_TAXON_MAP", cls)
            continue
        rows = scrape_class(cls, sci, args.max_per_class, args.dry_run)
        all_rows.extend(rows)
        time.sleep(SLEEP_BETWEEN)

    if not args.dry_run and all_rows:
        fieldnames = ["class", "scientific_name", "taxon_id", "source_url",
                      "source", "kept", "reason", "filename"]
        with open(MANIFEST, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=fieldnames)
            w.writeheader()
            w.writerows(all_rows)
        logger.info("Manifest -> %s", MANIFEST)

    kept = [r for r in all_rows if r["kept"]]
    zero_classes = [r["class"] for r in all_rows
                    if r["source"] == "inaturalist" and not r["kept"] and r["reason"] == "taxon_not_found"]

    logger.info("")
    logger.info("=" * 60)
    logger.info("Total images saved : %d", len(kept))
    if zero_classes:
        logger.info("Classes with 0 results (use scrape_bing.py for these):")
        for c in set(zero_classes):
            logger.info("  - %s", c)
    logger.info("Next: python scripts/ingest_scraped.py  (point to scraped_v2/)")


if __name__ == "__main__":
    main()
