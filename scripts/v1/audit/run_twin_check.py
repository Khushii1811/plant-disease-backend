"""
scripts/v1/audit/run_twin_check.py

Executes full-dataset exact (sha256) and perceptual hash (Hamming <= 4) duplicate check
on the release snapshot (reports/v1/dataset_v1.csv, N=91,984).
Generates:
  - reports/v1/twin_check.json
  - reports/v1/p008_plan_DRYRUN.csv (if cross-split twins remain)
"""

import csv
import json
import sys
import time
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Set, Tuple

import numpy as np

ROOT = Path(__file__).resolve().parent.parent.parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import config
from scripts.v1.audit.twin_graph import build_twin_graph


def run_twin_check():
    t0 = time.time()
    manifest_path = config.PROJECT_ROOT / "reports" / "v1" / "dataset_v1.csv"
    out_dir = config.PROJECT_ROOT / "reports" / "v1"

    print("=== Step 1: Checking exact SHA-256 duplicates across manifest ===")
    sha_to_rows = defaultdict(list)
    with open(manifest_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for idx, row in enumerate(reader):
            sha_to_rows[row["image_id"]].append(row)

    exact_sha_duplicates = {sha: rows for sha, rows in sha_to_rows.items() if len(rows) > 1}
    print(f"Unique SHA-256 hashes: {len(sha_to_rows):,}")
    print(f"Exact SHA-256 duplicate sets: {len(exact_sha_duplicates)}")

    exact_sha_by_split_pair = defaultdict(int)
    exact_sha_by_class = defaultdict(int)
    for sha, rows in exact_sha_duplicates.items():
        for i in range(len(rows)):
            for j in range(i + 1, len(rows)):
                s1, s2 = sorted([rows[i]["split"], rows[j]["split"]])
                exact_sha_by_split_pair[f"{s1}_vs_{s2}"] += 1
                cls1 = rows[i]["class"]
                exact_sha_by_class[cls1] += 1

    print("\n=== Step 2: Running pHash twin graph analysis (d <= 4) ===")
    records, twin_pairs, summary = build_twin_graph(manifest_path=manifest_path, out_dir=out_dir)

    # Breakdown by split pair
    split_pair_counts = defaultdict(lambda: {"d0": 0, "d1_4": 0, "total": 0})
    class_pair_counts = defaultdict(lambda: {"within_split": 0, "cross_split": 0, "total": 0})
    class_cross_split_pairs = defaultdict(list)

    for idx1, idx2, dist in twin_pairs:
        r1, r2 = records[idx1], records[idx2]
        s1, s2 = sorted([r1["split"], r2["split"]])
        pair_key = f"{s1}_vs_{s2}"
        
        split_pair_counts[pair_key]["total"] += 1
        if dist == 0:
            split_pair_counts[pair_key]["d0"] += 1
        else:
            split_pair_counts[pair_key]["d1_4"] += 1

        cls1 = r1["class"]
        cls2 = r2["class"]
        # In this dataset, twins are mostly in the same class, but track both
        for c in {cls1, cls2}:
            class_pair_counts[c]["total"] += 1
            if s1 == s2:
                class_pair_counts[c]["within_split"] += 1
            else:
                class_pair_counts[c]["cross_split"] += 1

        if s1 != s2:
            class_cross_split_pairs[(cls1, pair_key)].append((idx1, idx2, dist))

    print("\n--- Twin Pairs by Split Pair ---")
    for pair, cnts in sorted(split_pair_counts.items()):
        print(f"  {pair:15s}: total={cnts['total']:5d} (d0={cnts['d0']:4d}, d1..4={cnts['d1_4']:4d})")

    # Step 3: Graph Connected Components
    adj = defaultdict(list)
    for idx1, idx2, dist in twin_pairs:
        adj[idx1].append((idx2, dist))
        adj[idx2].append((idx1, dist))

    visited = set()
    clusters = []
    for idx in range(len(records)):
        if idx not in visited and idx in adj:
            cluster = []
            queue = [idx]
            visited.add(idx)
            while queue:
                curr = queue.pop()
                cluster.append(curr)
                for neighbor, _ in adj[curr]:
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append(neighbor)
            clusters.append(cluster)

    cross_split_clusters = []
    for c_idx, cluster in enumerate(clusters):
        splits = {records[i]["split"] for i in cluster}
        if len(splits) > 1:
            cross_split_clusters.append((c_idx, cluster))

    print(f"\nTotal clusters: {len(clusters)}")
    print(f"Cross-split clusters: {len(cross_split_clusters)}")

    # Step 4: Dry-run P-008 Plan
    # Rule: "keep the train copy, remove the evaluation copy"
    p008_removals = []
    affected_classes = set()
    removals_by_split = defaultdict(int)

    for c_id, cluster in cross_split_clusters:
        train_members = [i for i in cluster if records[i]["split"] == "train"]
        val_members = [i for i in cluster if records[i]["split"] == "val"]
        test_members = [i for i in cluster if records[i]["split"] == "test"]

        if train_members:
            # We have a train anchor; remove evaluation copies in this cluster
            eval_members = val_members + test_members
            sample_train = records[train_members[0]]
            for ev in eval_members:
                ev_rec = records[ev]
                # Find minimum distance to any train member
                min_d = min(
                    (int(records[tr]["phash_int"]) ^ int(ev_rec["phash_int"])).bit_count()
                    for tr in train_members
                )
                p008_removals.append({
                    "cluster_id": c_id,
                    "image_id": ev_rec["sha256"],
                    "path": ev_rec["path"],
                    "crop": ev_rec["crop"],
                    "class": ev_rec["class"],
                    "split": ev_rec["split"],
                    "action": f"quarantine_{ev_rec['split']}_leakage_twin",
                    "train_counterpart_path": sample_train["path"],
                    "min_hamming_dist_to_train": min_d,
                })
                removals_by_split[ev_rec["split"]] += 1
                affected_classes.add(ev_rec["class"])
        else:
            # Cluster has no train members (e.g. val vs test only)
            # Under rule "keep train, remove eval", if no train copy exists, check if val vs test
            sample_val = records[val_members[0]]
            for tst in test_members:
                tst_rec = records[tst]
                min_d = min(
                    (int(records[v]["phash_int"]) ^ int(tst_rec["phash_int"])).bit_count()
                    for v in val_members
                )
                p008_removals.append({
                    "cluster_id": c_id,
                    "image_id": tst_rec["sha256"],
                    "path": tst_rec["path"],
                    "crop": tst_rec["crop"],
                    "class": tst_rec["class"],
                    "split": tst_rec["split"],
                    "action": "quarantine_test_val_twin",
                    "train_counterpart_path": sample_val["path"],
                    "min_hamming_dist_to_train": min_d,
                })
                removals_by_split[tst_rec["split"]] += 1
                affected_classes.add(tst_rec["class"])

    # Check class support impact
    current_val_support = defaultdict(int)
    current_test_support = defaultdict(int)
    for r in records:
        if r["split"] == "val":
            current_val_support[r["class"]] += 1
        elif r["split"] == "test":
            current_test_support[r["class"]] += 1

    removals_per_class_split = defaultdict(lambda: {"val": 0, "test": 0})
    for rem in p008_removals:
        removals_per_class_split[rem["class"]][rem["split"]] += 1

    classes_below_3 = []
    for cls in affected_classes:
        cur_v = current_val_support[cls]
        cur_t = current_test_support[cls]
        rem_v = removals_per_class_split[cls]["val"]
        rem_t = removals_per_class_split[cls]["test"]
        post_v = cur_v - rem_v
        post_t = cur_t - rem_t
        if post_v < 3 or post_t < 3:
            classes_below_3.append({
                "class": cls,
                "val_before": cur_v,
                "val_after": post_v,
                "test_before": cur_t,
                "test_after": post_t,
            })

    print("\n--- P-008 Dry Run Removal Summary ---")
    print(f"Total images flagged for removal: {len(p008_removals)}")
    for s, cnt in removals_by_split.items():
        print(f"  From {s}: {cnt}")
    print(f"Affected classes: {len(affected_classes)}")
    print(f"Classes where val or test support falls below 3: {len(classes_below_3)}")
    if classes_below_3:
        for item in classes_below_3:
            print(f"  WARNING: {item['class']} -> val: {item['val_before']}->{item['val_after']}, test: {item['test_before']}->{item['test_after']}")

    # Write p008_plan_DRYRUN.csv
    p008_csv_path = out_dir / "p008_plan_DRYRUN.csv"
    with open(p008_csv_path, "w", newline="", encoding="utf-8") as f:
        fieldnames = [
            "cluster_id", "image_id", "path", "crop", "class", "split",
            "action", "train_counterpart_path", "min_hamming_dist_to_train"
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(p008_removals)
    print(f"\nWritten {p008_csv_path} with {len(p008_removals)} rows.")

    # Write twin_check.json
    twin_check_data = {
        "manifest_path": "reports/v1/dataset_v1.csv",
        "total_images": len(records),
        "exact_sha256_duplicates": {
            "total_duplicate_sets": len(exact_sha_duplicates),
            "by_split_pair": dict(exact_sha_by_split_pair),
            "by_class": dict(exact_sha_by_class),
        },
        "phash_hamming_le4": {
            "total_pairs": len(twin_pairs),
            "d0_exact_phash_pairs": summary["exact_phash_d0_pairs"],
            "d1_4_near_duplicate_pairs": summary["near_duplicate_d1_4_pairs"],
            "by_split_pair": {k: dict(v) for k, v in split_pair_counts.items()},
            "by_class": {k: dict(v) for k, v in class_pair_counts.items() if v["total"] > 0},
        },
        "clustering": {
            "total_clusters": len(clusters),
            "multi_image_clusters": summary["total_multi_image_clusters"],
            "cross_split_clusters": len(cross_split_clusters),
        },
        "p008_dryrun_summary": {
            "total_flagged_images": len(p008_removals),
            "removals_by_split": dict(removals_by_split),
            "num_affected_classes": len(affected_classes),
            "classes_support_below_3": classes_below_3,
        }
    }

    twin_check_json_path = out_dir / "twin_check.json"
    with open(twin_check_json_path, "w", encoding="utf-8") as f:
        json.dump(twin_check_data, f, indent=2)
    print(f"Written {twin_check_json_path}")
    print(f"Total twin check completed in {time.time() - t0:.2f}s.")
    return twin_check_data


if __name__ == "__main__":
    run_twin_check()
