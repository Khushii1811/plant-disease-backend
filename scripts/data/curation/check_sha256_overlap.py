"""
scripts/data/curation/check_sha256_overlap.py

Computes SHA-256 hashes of all existing Bell Pepper and Chilli images in
data/processed and data/raw, and compares against external dataset manifests.

Inputs:
  - --mendeley-dump: path to JSON manifest dump (defaults to scratch/mendeley_dump.json)
  - data/processed/ (train, val, test)
Outputs:
  - Prints exact SHA-256 hash overlap breakdown per class
"""

import argparse
import hashlib
import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import config

FOLDER_MAP = {
    "15e8ef89-a07f-45b0-be6f-4c16918545cb": "Bacterial Spot",
    "38bc4b65-1e1f-4e74-a670-d4d7a9afff22": "Cercospora Leaf Spot",
    "aa7c00d5-4db2-44fc-9ad8-20415e1b2092": "Healthy",
    "cf23d57d-42e0-4f99-ab0c-28c1b0da3245": "Leaf Curl",
    "c3fa371e-effb-4d26-a6a3-49cb9de3cb07": "Nutrition Deficiency",
    "52b1c6fd-9bf8-4a43-99c0-c2c576db24c6": "Powdery Mildew (White spot)",
}


def get_sha256(file_path: Path) -> str:
    h = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest().lower()


def main():
    parser = argparse.ArgumentParser(description="Check SHA256 overlap with external dataset dump")
    parser.add_argument(
        "--mendeley-dump",
        type=Path,
        default=config.PROJECT_ROOT / "scratch" / "mendeley_dump.json",
        help="Path to JSON dump of dataset files",
    )
    args = parser.parse_args()

    dump_path = args.mendeley_dump
    if not dump_path.exists():
        print(f"Dump file not found at {dump_path}. Skipping external comparison.")
        return

    with open(dump_path, "r", encoding="utf-8") as f:
        text = f.read()

    if "---" in text:
        json_str = text.split("---", 1)[1].strip()
    else:
        json_str = text
    data = json.loads(json_str)
    mendeley_files = data.get("files", [])

    mendeley_by_sha = {}
    for mf in mendeley_files:
        sha = mf.get("content_details", {}).get("sha256_hash")
        if sha:
            mendeley_by_sha[sha.lower()] = mf

    print(f"Total external files with sha256: {len(mendeley_by_sha)}")

    processed_dir = config.DATA_DIR / "processed"
    print("Scanning data/processed for Bell Pepper and Chilli images...")
    processed_files = []
    for split in ["train", "val", "test"]:
        split_dir = processed_dir / split
        if not split_dir.exists():
            continue
        for cls_dir in split_dir.iterdir():
            if cls_dir.is_dir() and any(
                k in cls_dir.name.lower() for k in ["pepper", "chilli", "capsicum"]
            ):
                for img_file in cls_dir.iterdir():
                    if img_file.is_file() and img_file.suffix.lower() in [".jpg", ".jpeg", ".png"]:
                        processed_files.append((split, cls_dir.name, img_file))

    print(f"Total processed pepper/chilli files found: {len(processed_files)}")

    matches = defaultdict(list)
    for _split, cls_name, img_file in processed_files:
        img_sha = get_sha256(img_file)
        if img_sha in mendeley_by_sha:
            mf = mendeley_by_sha[img_sha]
            folder_name = FOLDER_MAP.get(mf.get("folder_id"), "Unknown")
            matches[folder_name].append((cls_name, img_file.name, mf.get("name")))

    print("\n--- EXACT SHA256 OVERLAP WITH data/processed ---")
    for folder_name, match_list in matches.items():
        print(f"\nFolder '{folder_name}' has {len(match_list)} exact matches in data/processed:")
        by_cls = defaultdict(int)
        for c, _, _ in match_list:
            by_cls[c] += 1
        for c, count in by_cls.items():
            print(f"    - {c}: {count} files")


if __name__ == "__main__":
    main()
