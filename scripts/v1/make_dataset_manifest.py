"""
scripts/v1/make_dataset_manifest.py

Generates reports/v1/dataset_v1.csv and reports/v1/dataset_v1.summary.txt.
Indexes all images currently present in data/processed (train, val, test) across 195 classes.
"""

import hashlib
import sys
from pathlib import Path
from collections import defaultdict, Counter
import pandas as pd
from tqdm import tqdm

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
import config


def get_file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def main():
    processed_dir = config.DATA_DIR / "processed"
    lookup_csv_path = config.DATA_DIR / "manifests" / "dataset_v1.csv"
    manifests_dir = PROJECT_ROOT / "reports" / "v1"
    manifests_dir.mkdir(parents=True, exist_ok=True)

    print("Loading baseline lookup table...")
    sha_to_meta = {}
    path_to_meta = {}
    if lookup_csv_path.exists():
        lookup_df = pd.read_csv(lookup_csv_path)
        for _, r in lookup_df.iterrows():
            sha = r.get("image_id", "")
            src = r.get("source", "unknown")
            rule = r.get("source_rule", "unknown")
            p = r.get("path", "")
            fname = Path(p).name
            sha_to_meta[sha] = (src, rule)
            path_to_meta[fname] = (src, rule)
        print(f"Loaded {len(sha_to_meta):,} records from baseline manifest")

    print("Indexing all images in data/processed for v1 release...")
    records = []
    split_counts = Counter()
    class_counts = defaultdict(lambda: Counter())
    source_counts = Counter()
    unknown_count = 0

    splits = ["train", "val", "test"]
    for split in splits:
        split_p = processed_dir / split
        if not split_p.exists():
            continue
        for class_dir in sorted(split_p.iterdir()):
            if not class_dir.is_dir():
                continue
            class_name = class_dir.name
            crop_name = class_name.split(" - ")[0] if " - " in class_name else class_name

            for img_p in class_dir.glob("*"):
                if not img_p.is_file() or img_p.suffix.lower() not in ('.jpg', '.jpeg', '.png'):
                    continue

                fname = img_p.name
                size_bytes = img_p.stat().st_size

                if fname in path_to_meta:
                    src, rule = path_to_meta[fname]
                    sha = get_file_sha256(img_p)
                else:
                    sha = get_file_sha256(img_p)
                    if sha in sha_to_meta:
                        src, rule = sha_to_meta[sha]
                    else:
                        src, rule = "curated_addition", "disk_walk"

                if src == "unknown":
                    unknown_count += 1

                records.append({
                    "image_id": sha,
                    "path": str(img_p.relative_to(PROJECT_ROOT)).replace("\\", "/"),
                    "crop": crop_name,
                    "class": class_name,
                    "split": split,
                    "source": src,
                    "source_rule": rule,
                    "size_bytes": size_bytes
                })

                split_counts[split] += 1
                class_counts[class_name][split] += 1
                source_counts[src] += 1

    df = pd.DataFrame(records)
    out_csv = manifests_dir / "dataset_v1.csv"
    df.to_csv(out_csv, index=False)
    print(f"\n[DONE] Saved v1 manifest: {out_csv} ({len(df):,} images)")

    manifest_sha = get_file_sha256(out_csv)
    print(f"SHA-256 of {out_csv.name}: {manifest_sha}")

    out_summary = manifests_dir / "dataset_v1.summary.txt"
    with open(out_summary, "w", encoding="utf-8") as sm:
        sm.write("================================================================================\n")
        sm.write("DATASET SNAPSHOT SUMMARY (v1.0 Production Release)\n")
        sm.write("================================================================================\n")
        sm.write(f"Total Images: {len(df):,}\n")
        sm.write(f"Manifest SHA-256: {manifest_sha}\n")
        sm.write(f"Train Images: {split_counts['train']:,}\n")
        sm.write(f"Val Images:   {split_counts['val']:,}\n")
        sm.write(f"Test Images:  {split_counts['test']:,}\n")
        sm.write(f"Num Classes:  {len(class_counts)}\n")
        sm.write(f"Unknown Sources: {unknown_count} ({unknown_count/len(df)*100:.2f}%)\n\n")

        sm.write("COUNTS PER SPLIT:\n")
        for s, c in split_counts.items():
            sm.write(f"  {s:10s}: {c:7d}\n")
        sm.write("\nTOP 20 SOURCES:\n")
        for src, cnt in source_counts.most_common(20):
            sm.write(f"  {src:30s}: {cnt:6d} ({cnt/len(df)*100:.2f}%)\n")

    print(f"Saved v1 summary: {out_summary}")


if __name__ == "__main__":
    main()
