"""
scripts/v1/audit/twin_graph.py

Full-dataset 64-bit perceptual hash (pHash) twin-graph analysis across all 92,165 active images.
Uses 5-table bitwise sub-string indexing (Pigeonhole Principle) for Hamming distance <= 4.

Inputs:
  - reports/v1/dataset_v1.csv (manifest of active images)
  - scratch/image_hashes.json (precomputed pHash hex values per sha256)

Produces:
  - reports/v1/twin_graph_summary.json (graph connected components, cross-split clusters, twin counts)
  - reports/v1/phash_cache.csv (per-image pHash mapping)
"""

import csv
import json
import os
import sys
import time
from collections import defaultdict
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parent.parent.parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import config


def build_twin_graph(
    manifest_path: Path = None,
    hashes_path: Path = None,
    out_dir: Path = None,
):
    t0 = time.time()
    manifest_path = manifest_path or config.PROJECT_ROOT / "reports" / "v1" / "dataset_v1.csv"
    hashes_path = hashes_path or config.PROJECT_ROOT / "scratch" / "image_hashes.json"
    out_dir = out_dir or config.PROJECT_ROOT / "reports" / "v1"
    out_dir.mkdir(parents=True, exist_ok=True)

    print("1. Loading image hashes and manifest...")
    with open(hashes_path, "r", encoding="utf-8") as f:
        precomputed = json.load(f)

    sha_to_phash = {
        item["sha256"]: item["phash"]
        for item in precomputed
        if item.get("sha256") and item.get("phash")
    }
    # Add single missing image hash
    sha_to_phash["d5953f5fc6e27dd0124ff99803c07a5593c44427411dc340b72b6cf9cda5cedd"] = "dd25060a1fbe78b8"

    records = []
    with open(manifest_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for idx, row in enumerate(reader):
            sha = row["image_id"]
            ph_str = sha_to_phash.get(sha)
            if not ph_str:
                raise ValueError(f"Missing pHash for {row['path']}")
            ph_int = int(ph_str, 16)
            records.append({
                "idx": idx,
                "sha256": sha,
                "path": row["path"],
                "crop": row["crop"],
                "class": row["class"],
                "split": row["split"],
                "source": row["source"],
                "phash_hex": ph_str,
                "phash_int": ph_int,
            })

    total_images = len(records)
    print(f"Loaded {total_images} active images in {time.time() - t0:.2f}s.")

    # Save phash_cache.csv
    cache_path = out_dir / "phash_cache.csv"
    print(f"Writing pHash cache -> {cache_path}...")
    with open(cache_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f, fieldnames=["image_id", "path", "crop", "class", "split", "phash_hex"]
        )
        writer.writeheader()
        for r in records:
            writer.writerow({
                "image_id": r["sha256"],
                "path": r["path"],
                "crop": r["crop"],
                "class": r["class"],
                "split": r["split"],
                "phash_hex": r["phash_hex"],
            })

    print("2. Building bitwise bucketing tables for Hamming distance <= 4...")
    masks = [
        (0x1FFF, 0),    # bits 0..12 (13 bits)
        (0x1FFF, 13),   # bits 13..25 (13 bits)
        (0x1FFF, 26),   # bits 26..38 (13 bits)
        (0x1FFF, 39),   # bits 39..51 (13 bits)
        (0x0FFF, 52),   # bits 52..63 (12 bits)
    ]
    tables = [defaultdict(list) for _ in range(5)]
    phash_ints = np.array([r["phash_int"] for r in records], dtype=np.uint64)

    for idx in range(total_images):
        h = int(phash_ints[idx])
        for t_idx, (mask, shift) in enumerate(masks):
            key = (h >> shift) & mask
            tables[t_idx][key].append(idx)

    print("Collecting candidate pairs...")
    candidate_pairs = set()
    for t_idx in range(5):
        for key, bucket in tables[t_idx].items():
            if len(bucket) > 1:
                b_len = len(bucket)
                for i in range(b_len):
                    idx1 = bucket[i]
                    for j in range(i + 1, b_len):
                        idx2 = bucket[j]
                        if idx1 < idx2:
                            candidate_pairs.add((idx1, idx2))
                        else:
                            candidate_pairs.add((idx2, idx1))

    print(f"Candidate pairs to verify: {len(candidate_pairs):,}")

    twin_pairs = []
    d0_count = 0
    d1_4_count = 0

    for idx1, idx2 in candidate_pairs:
        h1 = int(phash_ints[idx1])
        h2 = int(phash_ints[idx2])
        dist = (h1 ^ h2).bit_count()
        if dist <= 4:
            twin_pairs.append((idx1, idx2, dist))
            if dist == 0:
                d0_count += 1
            else:
                d1_4_count += 1

    total_twin_pairs = len(twin_pairs)
    print(f"Total twin pairs (d <= 4): {total_twin_pairs:,}")
    print(f"  Exact pHash (d = 0):     {d0_count:,}")
    print(f"  Near-duplicate (d 1..4): {d1_4_count:,}")

    # Build connected components
    adj = defaultdict(list)
    for idx1, idx2, _ in twin_pairs:
        adj[idx1].append(idx2)
        adj[idx2].append(idx1)

    visited = set()
    clusters = []
    for idx in range(total_images):
        if idx not in visited and idx in adj:
            cluster = []
            queue = [idx]
            visited.add(idx)
            while queue:
                curr = queue.pop()
                cluster.append(curr)
                for neighbor in adj[curr]:
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append(neighbor)
            clusters.append(cluster)

    multi_item_clusters = [c for c in clusters if len(c) > 1]
    cross_split_clusters = []
    for c in multi_item_clusters:
        splits = {records[i]["split"] for i in c}
        if len(splits) > 1:
            cross_split_clusters.append(c)

    summary = {
        "total_active_images": total_images,
        "total_twin_pairs_d_le_4": total_twin_pairs,
        "exact_phash_d0_pairs": d0_count,
        "near_duplicate_d1_4_pairs": d1_4_count,
        "total_multi_image_clusters": len(multi_item_clusters),
        "cross_split_clusters": len(cross_split_clusters),
    }

    summary_path = out_dir / "twin_graph_summary.json"
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print(f"Summary written -> {summary_path}")
    print(f"Completed twin graph analysis in {time.time() - t0:.2f}s.")
    return records, twin_pairs, summary


def main():
    build_twin_graph()


if __name__ == "__main__":
    main()
