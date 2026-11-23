"""
scripts/v1/audit/generate_leaky_eval_images.py

Identifies validation and test split images that share perceptual hash twins
(Hamming distance <= 4) with the training split, or test images sharing twins with validation.

Inputs:
  - reports/v1/dataset_v1.csv (manifest of active images)
  - scratch/image_hashes.json (precomputed pHash hex values per sha256)

Produces:
  - reports/v1/leaky_eval_images.csv (list of 343 leaky eval images: 162 val, 181 test)
"""

import csv
import os
import sys
import time
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import config
from scripts.v1.audit.twin_graph import build_twin_graph


def generate_leaky_eval_images(out_csv: Path = None):
    t0 = time.time()
    out_csv = out_csv or config.PROJECT_ROOT / "data" / "patches" / "history" / "leaky_eval_images_historical_343.csv"
    out_csv.parent.mkdir(parents=True, exist_ok=True)

    records, twin_pairs, _ = build_twin_graph()
    total_images = len(records)

    print("\nGenerating leaky evaluation image mapping...")
    image_twins = defaultdict(list)
    for idx1, idx2, dist in twin_pairs:
        image_twins[idx1].append((idx2, dist))
        image_twins[idx2].append((idx1, dist))

    leaky_eval_records = []
    for idx in range(total_images):
        rec = records[idx]
        split = rec["split"]
        if split in ("val", "test"):
            leak_reasons = []
            matching_train_twins = []
            matching_val_twins = []
            min_dist_train = 999
            min_dist_val = 999

            for t_idx, dist in image_twins[idx]:
                t_rec = records[t_idx]
                if t_rec["split"] == "train":
                    matching_train_twins.append(t_rec["path"])
                    if dist < min_dist_train:
                        min_dist_train = dist
                elif split == "test" and t_rec["split"] == "val":
                    matching_val_twins.append(t_rec["path"])
                    if dist < min_dist_val:
                        min_dist_val = dist

            if matching_train_twins:
                leak_reasons.append("twin_in_train")
            if matching_val_twins:
                leak_reasons.append("twin_in_val")

            if leak_reasons:
                leaky_eval_records.append({
                    "eval_image_id": rec["sha256"],
                    "eval_path": rec["path"],
                    "eval_split": split,
                    "eval_class": rec["class"],
                    "eval_crop": rec["crop"],
                    "leak_type": "+".join(leak_reasons),
                    "min_hamming_dist_train": min_dist_train if min_dist_train != 999 else "",
                    "num_train_twins": len(matching_train_twins),
                    "sample_train_twin": matching_train_twins[0] if matching_train_twins else "",
                    "min_hamming_dist_val": min_dist_val if min_dist_val != 999 else "",
                    "num_val_twins": len(matching_val_twins),
                    "sample_val_twin": matching_val_twins[0] if matching_val_twins else "",
                })

    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        fieldnames = [
            "eval_image_id", "eval_path", "eval_split", "eval_class", "eval_crop",
            "leak_type", "min_hamming_dist_train", "num_train_twins", "sample_train_twin",
            "min_hamming_dist_val", "num_val_twins", "sample_val_twin",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(leaky_eval_records)

    val_leaky = sum(1 for r in leaky_eval_records if r["eval_split"] == "val")
    test_leaky = sum(1 for r in leaky_eval_records if r["eval_split"] == "test")
    print(f"Total leaky eval images written -> {out_csv} ({len(leaky_eval_records)} total)")
    print(f"  Val Leaky:  {val_leaky}")
    print(f"  Test Leaky: {test_leaky}")
    print(f"Done in {time.time() - t0:.2f}s.")
    return leaky_eval_records


def main():
    generate_leaky_eval_images()


if __name__ == "__main__":
    main()
