"""
scripts/auto_screen_and_clean_dataset.py

Sequential Class-by-Class Auto-Screening & Autonomous Cleaning Engine.

Workflow (Class-by-Class Sequential Pipeline):
For each disease class in the dataset:
  1. Deep screening across Train, Val, and Test:
     - Exact cryptographic MD5 duplicates.
     - Multi-rotation & mirrored perceptual dHash (hamming distance <= 3 on 32x32 thumbnails).
     - Corrupted or unreadable image files.
  2. Strict Anti-Leakage & Dedup Resolution (User Rules):
     - Cross-Split Leakage involving Train:
       * ALL copies in Train are safely purged (including any internal duplicates in Train)
         to preserve uncompromised eval benchmarks.
     - Cross-Split Leakage between Val and Test only:
       * 1 copy kept randomly, other copy quarantined.
     - Within-Split Internal Duplicates:
       * 1 unique copy kept randomly, redundant duplicates quarantined.
  3. Safe Non-Destructive Quarantine:
     - Relocates images to data/raw/quarantine_data_quality/{reason}/{class_name}/.
     - Logs each action to data/quality_audit/quarantine_actions.json.
     - Purges quarantined paths from data/quality_audit/flagged_issues.json.
  4. Moves sequentially to the next class.

Can be run:
  - From CLI: python scripts/auto_screen_and_clean_dataset.py [--commit] [--crop CROP] [--class CLASS]
  - Or invoked in background by the Data Quality Dashboard.
"""

import argparse
import hashlib
import io
import json
import logging
import random
import shutil
import sys
import time
from collections import defaultdict
from pathlib import Path

import imagehash
from PIL import Image, ImageOps

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
AUDIT_DIR = PROJECT_ROOT / "data" / "quality_audit"
ISSUES_FILE = AUDIT_DIR / "flagged_issues.json"
ACTIONS_LOG = AUDIT_DIR / "quarantine_actions.json"
QUARANTINE_ROOT = PROJECT_ROOT / "data" / "raw" / "quarantine_data_quality"
REPORT_FILE = AUDIT_DIR / "auto_cleaning_report.json"

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}


def compute_multirot_dhashes(thumb: Image.Image) -> list:
    """Computes dHash across 0, 90, 180, 270 deg rotations and mirror on a 32x32 thumbnail."""
    dhs = [int(str(imagehash.dhash(thumb)), 16)]
    for a in (90, 180, 270):
        dhs.append(int(str(imagehash.dhash(thumb.rotate(a))), 16))
    dhs.append(int(str(imagehash.dhash(ImageOps.mirror(thumb))), 16))
    return dhs


def compute_dihedral_dhashes(thumb: Image.Image) -> dict:
    """
    Computes 8 dihedral symmetry dHashes (0°, 90°, 180°, 270°, and horizontal flips).
    Used for Direct Pairwise Matching without transitive chaining.
    """
    hashes = {}
    hashes["0°"] = int(str(imagehash.dhash(thumb)), 16)
    for a in (90, 180, 270):
        hashes[f"{a}°"] = int(str(imagehash.dhash(thumb.rotate(a))), 16)
    m = ImageOps.mirror(thumb)
    hashes["H-Flip"] = int(str(imagehash.dhash(m)), 16)
    for a in (90, 180, 270):
        hashes[f"H-Flip+{a}°"] = int(str(imagehash.dhash(m.rotate(a))), 16)
    return hashes


class DisjointSet:
    def __init__(self, elements):
        self.parent = {e: e for e in elements}

    def find(self, i):
        if self.parent[i] == i:
            return i
        self.parent[i] = self.find(self.parent[i])
        return self.parent[i]

    def union(self, i, j):
        root_i = self.find(i)
        root_j = self.find(j)
        if root_i != root_j:
            self.parent[root_i] = root_j


def resolve_duplicate_clusters(clusters: list) -> tuple:
    """
    Enforces exact user priority rules for duplicate clusters:
    1. Cross-Split Leakage involving Train:
       - ALL train copies in the cluster are safely purged (including internal duplicates).
       - For remaining eval copies (val/test):
         * If both val & test exist: randomly keep 1, quarantine others under 'cross_split_leakage_val_test'.
         * If only val or only test exists: randomly keep 1, quarantine redundant duplicates under 'near_duplicate_redundancy'.
    2. Cross-Split Leakage between Val and Test only:
       - Randomly keep 1, quarantine others under 'cross_split_leakage_val_test'.
    3. Within-Split Internal Duplicates:
       - Randomly keep 1, quarantine others under 'near_duplicate_redundancy'.
    """
    to_quarantine = []
    to_keep = []
    stats = {
        "clusters_resolved": len(clusters),
        "leakage_train_clusters": 0,
        "leakage_val_test_clusters": 0,
        "within_clusters": 0,
        "quarantined_by_split": defaultdict(int),
        "quarantined_by_reason": defaultdict(int),
    }

    for cluster in clusters:
        train_members = [r for r in cluster if r["split"] == "train"]
        val_members = [r for r in cluster if r["split"] == "val"]
        test_members = [r for r in cluster if r["split"] == "test"]

        has_train = len(train_members) > 0
        has_val = len(val_members) > 0
        has_test = len(test_members) > 0

        # Case 1: Leakage involving train
        if has_train and (has_val or has_test):
            stats["leakage_train_clusters"] += 1
            for tr in train_members:
                to_quarantine.append((tr, "cross_split_leakage_from_train"))

            eval_members = val_members + test_members
            if has_val and has_test:
                chosen = random.choice(eval_members)
                to_keep.append(chosen)
                for ev in eval_members:
                    if ev != chosen:
                        to_quarantine.append((ev, "cross_split_leakage_val_test"))
            else:
                chosen = random.choice(eval_members)
                to_keep.append(chosen)
                for ev in eval_members:
                    if ev != chosen:
                        to_quarantine.append((ev, "near_duplicate_redundancy"))

        # Case 2: Leakage between val and test only
        elif has_val and has_test:
            stats["leakage_val_test_clusters"] += 1
            eval_members = val_members + test_members
            chosen = random.choice(eval_members)
            to_keep.append(chosen)
            for ev in eval_members:
                if ev != chosen:
                    to_quarantine.append((ev, "cross_split_leakage_val_test"))

        # Case 3: Within single split only
        else:
            stats["within_clusters"] += 1
            chosen = random.choice(cluster)
            to_keep.append(chosen)
            for m in cluster:
                if m != chosen:
                    to_quarantine.append((m, "near_duplicate_redundancy"))

    for r, reason in to_quarantine:
        stats["quarantined_by_split"][r["split"]] += 1
        stats["quarantined_by_reason"][reason] += 1

    # Generate pairwise visual mapping representations for side-by-side dashboard review
    visual_pairs = []
    for cluster in clusters:
        chosen_candidates = [k for k in to_keep if any(k["path"] == c["path"] for c in cluster)]
        chosen = chosen_candidates[0] if chosen_candidates else cluster[0]
        for m in cluster:
            if m["path"] != chosen["path"]:
                assigned_reason = next((rea for rec, rea in to_quarantine if rec["path"] == m["path"]), "near_duplicate_redundancy")
                is_cross = (m["split"] != chosen["split"])
                sim = 1.0 if m.get("md5") == chosen.get("md5") else 0.96

                if is_cross:
                    iss_type = "cross_split_leakage"
                    severity = "HIGH"
                    if m["split"] == "train":
                        title = f"🚨 Cross-Split Leakage Twin ({m['split']} ↔ {chosen['split']})"
                        desc = f"Simulated Action: Purge from Train ({m['name']}) to protect {chosen['split']} ({chosen['name']}) evaluation benchmark."
                    else:
                        title = f"🚨 Val-Test Leakage Twin ({m['split']} ↔ {chosen['split']})"
                        desc = f"Simulated Action: Keep {chosen['split']} ({chosen['name']}), Quarantine {m['split']} ({m['name']})."
                else:
                    iss_type = "near_duplicate"
                    severity = "MEDIUM"
                    title = f"👯 Redundant Duplicate ({m['split']})"
                    desc = f"Simulated Action: Keep unique copy ({chosen['name']}), Quarantine redundant copy ({m['name']})."

                visual_pairs.append({
                    "type": iss_type,
                    "severity": severity,
                    "title": title,
                    "description": desc,
                    "similarity": sim,
                    "primary_image": {
                        "class": chosen["class"],
                        "split": chosen["split"],
                        "filename": chosen["name"],
                        "path": chosen["path"],
                    },
                    "secondary_image": {
                        "class": m["class"],
                        "split": m["split"],
                        "filename": m["name"],
                        "path": m["path"],
                    },
                })

    return to_quarantine, to_keep, stats, visual_pairs


def execute_quarantine_moves(to_quarantine: list, commit: bool = True) -> list:
    """Executes quarantine file relocations and logs actions."""
    if not commit:
        return []

    QUARANTINE_ROOT.mkdir(parents=True, exist_ok=True)
    success_actions = []
    quarantined_paths = []

    for r, reason in to_quarantine:
        norm_path = r["path"].replace("\\", "/").strip()
        src = PROJECT_ROOT / norm_path
        if not src.exists():
            fname = Path(norm_path).name
            candidates = list((PROJECT_ROOT / "data" / "processed").rglob(fname))
            if candidates:
                src = candidates[0]
        if not src.exists():
            continue

        class_name = r.get("class") or src.parent.name
        dest_dir = QUARANTINE_ROOT / reason / class_name
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest_file = dest_dir / src.name
        if dest_file.exists():
            dest_file = dest_dir / f"{src.stem}_{int(time.time())}_{random.randint(1000, 9999)}{src.suffix}"

        shutil.move(str(src), str(dest_file))
        actual_rel = str(src.relative_to(PROJECT_ROOT)).replace("\\", "/")
        quarantined_rel = str(dest_file.relative_to(PROJECT_ROOT)).replace("\\", "/")
        quarantined_paths.extend([norm_path, actual_rel, src.name])

        success_actions.append({
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "original_path": actual_rel,
            "quarantined_path": quarantined_rel,
            "reason": reason,
        })

    # Purge from flagged_issues.json
    if quarantined_paths and ISSUES_FILE.exists():
        try:
            with open(ISSUES_FILE, "r", encoding="utf-8") as f:
                issue_data = json.load(f)
            target_norms = {p.replace("\\", "/").strip().lower() for p in quarantined_paths}
            target_fns = {Path(p).name.lower() for p in quarantined_paths}

            rem = []
            for it in issue_data.get("issues", []):
                p1 = it.get("primary_image", {})
                p2 = it.get("secondary_image", {})
                p1_path = p1.get("path", "").replace("\\", "/").strip().lower()
                p1_fn = p1.get("filename", "").lower() or Path(p1_path).name.lower()
                p2_path = p2.get("path", "").replace("\\", "/").strip().lower() if p2 else ""
                p2_fn = (p2.get("filename", "").lower() or Path(p2_path).name.lower()) if p2 else ""

                if (p1_path in target_norms or p1_fn in target_fns) or (p2 and (p2_path in target_norms or p2_fn in target_fns)):
                    continue
                rem.append(it)
            issue_data["issues"] = rem
            issue_data["total_issues"] = len(rem)
            with open(ISSUES_FILE, "w", encoding="utf-8") as f:
                json.dump(issue_data, f, indent=2)
        except Exception:
            pass

    # Append to quarantine_actions.json
    if success_actions:
        existing = []
        if ACTIONS_LOG.exists():
            try:
                with open(ACTIONS_LOG, "r", encoding="utf-8") as f:
                    existing = json.load(f)
            except Exception:
                existing = []
        existing.extend(success_actions)
        with open(ACTIONS_LOG, "w", encoding="utf-8") as f:
            json.dump(existing, f, indent=2)

    return success_actions


def screen_and_clean_class(
    class_name: str,
    commit: bool = True,
    dhash_threshold: int = 3,
    matching_mode: str = "cluster",
) -> dict:
    """
    Performs complete deep screening and cleaning on a single disease class.
    Supports two matching algorithms:
    1. 'cluster' (default): Transitive DisjointSet clustering (proven for heterogeneous foliar crops).
    2. 'direct_pairwise': Direct 1-to-1 rotated/flipped/exact matching without transitive chaining
       (ideal for studio-shot leaves like Ginger and Paddy where chaining causes false positives).
    Returns audit metrics dictionary for that class.
    """
    records = []
    before_counts = {"train": 0, "val": 0, "test": 0}

    for split in ["train", "val", "test"]:
        cdir = PROCESSED_DIR / split / class_name
        if not cdir.exists():
            continue
        flist = sorted([p for p in cdir.iterdir() if p.suffix.lower() in IMAGE_EXTS])
        before_counts[split] = len(flist)
        for p in flist:
            rel = str(p.relative_to(PROJECT_ROOT)).replace("\\", "/")
            records.append({
                "id": len(records),
                "path": rel,
                "name": p.name,
                "split": split,
                "class": class_name,
                "abs_path": str(p),
            })

    total_images = len(records)
    if total_images < 2:
        return {
            "class_name": class_name,
            "total_images": total_images,
            "clusters_resolved": 0,
            "quarantined_count": 0,
            "before": before_counts,
            "after": before_counts,
            "quarantined_by_split": {"train": 0, "val": 0, "test": 0},
            "quarantined_by_reason": {},
        }

    # Extract MD5 and 32x32 thumbnails
    dset = DisjointSet([r["path"] for r in records])
    md5_map = defaultdict(list)
    dhashes = []
    dihedral_hashes = []
    unreadable = []

    for r in records:
        try:
            data = Path(r["abs_path"]).read_bytes()
            if len(data) == 0:
                unreadable.append((r, "unreadable_corrupt"))
                continue
            h_md5 = hashlib.md5(data).hexdigest()
            r["md5"] = h_md5
            md5_map[h_md5].append(r["path"])

            with Image.open(io.BytesIO(data)) as im:
                rgb = im.convert("RGB")
                thumb = rgb.resize((32, 32), Image.Resampling.BILINEAR)
                if matching_mode == "direct_pairwise":
                    dihedral_hashes.append(compute_dihedral_dhashes(thumb))
                else:
                    dhashes.append(compute_multirot_dhashes(thumb))
        except Exception:
            unreadable.append((r, "unreadable_corrupt"))

    if matching_mode == "direct_pairwise":
        # -------------------------------------------------------------
        # DIRECT PAIRWISE MATCHING (Strict Rotated / Flipped / Exact)
        # Eliminates transitive DisjointSet chaining
        # -------------------------------------------------------------
        valid_records = [r for r in records if "md5" in r and len(dihedral_hashes) > r["id"]]
        candidate_pairs = []
        n_valid = len(valid_records)

        for i in range(n_valid):
            r_i = valid_records[i]
            dh_i = dihedral_hashes[i]
            for j in range(i + 1, n_valid):
                r_j = valid_records[j]

                # 1. Exact MD5 check
                if r_i["md5"] == r_j["md5"]:
                    candidate_pairs.append((r_i, r_j, "Exact MD5 Clone", 0, 1.0))
                    continue

                # 2. Strict Dihedral dHash check (compare base 0° against 8 dihedral orientations of j)
                dh_i_base = dh_i["0°"]
                dh_j = dihedral_hashes[j]
                min_dh = 64
                best_tr = "0°"
                for t2, val2 in dh_j.items():
                    dist = (dh_i_base ^ val2).bit_count()
                    if dist < min_dh:
                        min_dh = dist
                        best_tr = t2
                        if min_dh == 0:
                            break

                if min_dh <= min(2, dhash_threshold):
                    sim = round(1.0 - min_dh / 64.0, 4)
                    label = f"Rotated/Flipped Twin ({best_tr})" if best_tr != "0°" else "Near-Identical Twin"
                    candidate_pairs.append((r_i, r_j, f"{label} (dist={min_dh})", min_dh, sim))

        # Sort: exact MD5 first, then smallest distance
        candidate_pairs.sort(key=lambda x: x[3])

        to_quarantine = []
        to_keep = []
        quarantined_paths = set()
        visual_pairs = []
        stats = {
            "clusters_resolved": len(candidate_pairs),
            "leakage_train_clusters": 0,
            "leakage_val_test_clusters": 0,
            "within_clusters": 0,
            "quarantined_by_split": defaultdict(int),
            "quarantined_by_reason": defaultdict(int),
        }

        for r1, r2, label, dist, sim in candidate_pairs:
            has_train = (r1["split"] == "train" or r2["split"] == "train")
            is_cross = (r1["split"] != r2["split"])

            if is_cross and has_train:
                quarantined_rec = r1 if r1["split"] == "train" else r2
                kept_rec = r2 if r1["split"] == "train" else r1
                reason = "cross_split_leakage_from_train"
                stats["leakage_train_clusters"] += 1
                iss_type = "cross_split_leakage"
                severity = "HIGH"
                title = f"🚨 Direct Cross-Split Leakage Twin ({quarantined_rec['split']} ↔ {kept_rec['split']})"
            elif is_cross:
                quarantined_rec = r1
                kept_rec = r2
                reason = "cross_split_leakage_val_test"
                stats["leakage_val_test_clusters"] += 1
                iss_type = "cross_split_leakage"
                severity = "HIGH"
                title = "🚨 Direct Cross-Split Leakage Twin (val ↔ test)"
            else:
                quarantined_rec = r1
                kept_rec = r2
                reason = "near_duplicate_redundancy"
                stats["within_clusters"] += 1
                iss_type = "near_duplicate"
                severity = "MEDIUM"
                title = f"👯 Direct Rotated/Flipped Twin ({label})"

            if quarantined_rec["path"] not in quarantined_paths and kept_rec["path"] not in quarantined_paths:
                to_quarantine.append((quarantined_rec, reason))
                quarantined_paths.add(quarantined_rec["path"])
                to_keep.append(kept_rec)
                stats["quarantined_by_split"][quarantined_rec["split"]] += 1
                stats["quarantined_by_reason"][reason] += 1

            desc = f"Direct pairwise match ({label}, similarity {int(sim*100)}%). " + (
                "Purged train duplicate to safeguard evaluation integrity."
                if reason == "cross_split_leakage_from_train"
                else "Redundant copy quarantined."
            )
            visual_pairs.append({
                "id": f"{quarantined_rec['name']}_vs_{kept_rec['name']}_{len(visual_pairs)}",
                "type": iss_type,
                "severity": severity,
                "title": title,
                "description": desc,
                "similarity": sim,
                "class_name": class_name,
                "primary_image": kept_rec,
                "secondary_image": quarantined_rec,
            })

        dup_clusters = candidate_pairs

    else:
        # -------------------------------------------------------------
        # STANDARD CLUSTER MATCHING (DisjointSet Transitive Clustering)
        # Proven default algorithm for natural foliar crops
        # -------------------------------------------------------------
        # A. Exact MD5 matches
        for h, paths in md5_map.items():
            if len(paths) > 1:
                for i in range(len(paths) - 1):
                    dset.union(paths[i], paths[i + 1])

        # B. Perceptual dHash <= dhash_threshold
        valid_records = [r for r in records if "md5" in r and len(dhashes) > r["id"]]
        n_valid = len(valid_records)
        for i in range(n_valid):
            dh_i = dhashes[i]
            p_i = valid_records[i]["path"]
            for j in range(i + 1, n_valid):
                p_j = valid_records[j]["path"]
                if dset.find(p_i) == dset.find(p_j):
                    continue
                min_dh = 64
                for h1 in dh_i:
                    for h2 in dhashes[j]:
                        dist = (h1 ^ h2).bit_count()
                        if dist < min_dh:
                            min_dh = dist
                            if min_dh <= dhash_threshold:
                                break
                    if min_dh <= dhash_threshold:
                        break
                if min_dh <= dhash_threshold:
                    dset.union(p_i, p_j)

        # Form clusters
        cluster_groups = defaultdict(list)
        for r in valid_records:
            root = dset.find(r["path"])
            cluster_groups[root].append(r)

        dup_clusters = [c for c in cluster_groups.values() if len(c) > 1]
        to_quarantine, to_keep, stats, visual_pairs = resolve_duplicate_clusters(dup_clusters)

    # Include unreadable corrupt images
    for ur, ur_reason in unreadable:
        to_quarantine.append((ur, ur_reason))
        stats["quarantined_by_split"][ur["split"]] += 1
        stats["quarantined_by_reason"][ur_reason] += 1

    if commit:
        execute_quarantine_moves(to_quarantine, commit=True)

    after_counts = {
        "train": before_counts["train"] - stats["quarantined_by_split"]["train"],
        "val": before_counts["val"] - stats["quarantined_by_split"]["val"],
        "test": before_counts["test"] - stats["quarantined_by_split"]["test"],
    }

    return {
        "class_name": class_name,
        "total_images": total_images,
        "clusters_resolved": len(dup_clusters),
        "quarantined_count": len(to_quarantine),
        "quarantined_by_split": dict(stats["quarantined_by_split"]),
        "quarantined_by_reason": dict(stats["quarantined_by_reason"]),
        "before": before_counts,
        "after": after_counts,
        "visual_issues": visual_pairs,
    }



def run_sequential_pipeline(
    target_crop: str = None,
    target_class: str = None,
    commit: bool = True,
    matching_mode: str = "cluster",
    progress_callback = None,
) -> dict:
    """
    Sequentially processes each class in the dataset one by one.
    matching_mode:
      - 'cluster': Standard Transitive DisjointSet clustering (proven for foliar crops).
      - 'direct_pairwise': Direct 1-to-1 rotated/flipped/exact twin matching (for Ginger, Paddy, studio leaves).
    Reports progress via progress_callback(pct, class_index, total_classes, class_name, msg, stats).
    """
    train_dir = PROCESSED_DIR / "train"
    if not train_dir.exists():
        return {"status": "error", "message": "Train directory does not exist."}

    all_class_dirs = sorted([d.name for d in train_dir.iterdir() if d.is_dir()])
    if target_class:
        all_class_dirs = [c for c in all_class_dirs if c == target_class or target_class.lower() in c.lower()]
    elif target_crop:
        norm_crop = target_crop.lower().strip()
        all_class_dirs = [c for c in all_class_dirs if c.lower().startswith(norm_crop) or norm_crop in c.lower()]

    total_classes = len(all_class_dirs)
    if total_classes == 0:
        return {"status": "error", "message": "No matching classes found."}

    print("=" * 80, flush=True)
    print("  🤖 AUTONOMOUS SEQUENTIAL CLASS-BY-CLASS SCREENING & CLEANING ENGINE", flush=True)
    print(f"  Mode           : {'LIVE COMMIT (QUARANTINE)' if commit else 'DRY RUN (AUDIT ONLY)'}", flush=True)
    print(f"  Matching Engine: {matching_mode.upper()} {'(Direct Rotated/Flipped 1-to-1)' if matching_mode == 'direct_pairwise' else '(Transitive Clusters)'}", flush=True)
    print(f"  Total Classes  : {total_classes}", flush=True)
    print("=" * 80, flush=True)

    pipeline_start = time.time()
    total_quarantined = 0
    total_clusters = 0
    total_train_purged = 0
    total_val_purged = 0
    total_test_purged = 0
    classes_with_issues = 0
    results_per_class = []
    all_visual_issues = []

    for idx, cname in enumerate(all_class_dirs):
        t0 = time.time()
        pct = int((idx / total_classes) * 100)
        msg = f"Screening [{idx + 1}/{total_classes}]: {cname} ({matching_mode})..."

        if progress_callback:
            progress_callback(
                pct=pct,
                class_index=idx + 1,
                total_classes=total_classes,
                class_name=cname,
                message=msg,
                total_quarantined=total_quarantined,
                total_train_purged=total_train_purged,
            )

        res = screen_and_clean_class(cname, commit=commit, matching_mode=matching_mode)
        results_per_class.append(res)
        all_visual_issues.extend(res.get("visual_issues", []))

        q_cnt = res["quarantined_count"]
        c_cnt = res["clusters_resolved"]
        tr_q = res["quarantined_by_split"].get("train", 0)
        v_q = res["quarantined_by_split"].get("val", 0)
        te_q = res["quarantined_by_split"].get("test", 0)

        total_quarantined += q_cnt
        total_clusters += c_cnt
        total_train_purged += tr_q
        total_val_purged += v_q
        total_test_purged += te_q

        if q_cnt > 0:
            classes_with_issues += 1
            print(f"  [{idx + 1:3d}/{total_classes}] 🧹 {cname:<45} | Quarantined: {q_cnt:3d} (Tr:{tr_q:2d}, V:{v_q:2d}, Te:{te_q:2d}) in {time.time()-t0:.1f}s", flush=True)
        else:
            if (idx + 1) % 10 == 0 or idx + 1 == total_classes:
                print(f"  [{idx + 1:3d}/{total_classes}] ✅ {cname:<45} | Clean (0 issues) in {time.time()-t0:.1f}s", flush=True)

    elapsed_total = round(time.time() - pipeline_start, 1)

    # Save visual mapping twin issues into flagged_issues.json for side-by-side dashboard review
    if not commit or len(all_visual_issues) > 0:
        try:
            ISSUES_FILE.parent.mkdir(parents=True, exist_ok=True)
            with open(ISSUES_FILE, "w", encoding="utf-8") as f:
                json.dump({
                    "total_scanned": sum(r.get("total_images", 0) for r in results_per_class),
                    "target_crop": target_crop,
                    "total_issues": len(all_visual_issues),
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "issues": all_visual_issues,
                }, f, indent=2)
            print(f"  📸 Saved {len(all_visual_issues)} side-by-side mapping pairs to flagged_issues.json for interactive visual review!", flush=True)
        except Exception as e:
            print(f"Error saving visual pairs: {e}", flush=True)

    summary = {
        "status": "completed",
        "commit": commit,
        "total_classes": total_classes,
        "classes_with_issues": classes_with_issues,
        "total_clusters_resolved": total_clusters,
        "total_quarantined": total_quarantined,
        "quarantined_from_train": total_train_purged,
        "quarantined_from_val": total_val_purged,
        "quarantined_from_test": total_test_purged,
        "total_visual_issues": len(all_visual_issues),
        "elapsed_seconds": elapsed_total,
        "results_per_class": [r for r in results_per_class if r["quarantined_count"] > 0],
    }

    # Save summary report
    try:
        REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(REPORT_FILE, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2)
    except Exception:
        pass

    print("\n" + "=" * 80, flush=True)
    print("  🎉 SEQUENTIAL DATASET CLEANING PIPELINE COMPLETED!", flush=True)
    print(f"  Classes Processed        : {total_classes} classes", flush=True)
    print(f"  Classes Cleaned          : {classes_with_issues} classes had duplicates/leakage", flush=True)
    print(f"  Total Images Quarantined : {total_quarantined} images", flush=True)
    print(f"    - Purged from Train    : {total_train_purged} (cross-split leakage / redundancy)", flush=True)
    print(f"    - Purged from Val      : {total_val_purged}", flush=True)
    print(f"    - Purged from Test     : {total_test_purged}", flush=True)
    print(f"  Total Time Elapsed       : {elapsed_total}s", flush=True)
    print("=" * 80, flush=True)

    if progress_callback:
        progress_callback(
            pct=100,
            class_index=total_classes,
            total_classes=total_classes,
            class_name="ALL COMPLETE",
            message=f"Pipeline complete! Quarantined {total_quarantined} images across {classes_with_issues} classes.",
            total_quarantined=total_quarantined,
            total_train_purged=total_train_purged,
        )

    return summary


def main():
    parser = argparse.ArgumentParser(description="Sequential Class-by-Class Dataset Auto-Screening & Cleaning")
    parser.add_argument("--commit", action="store_true", help="Execute quarantine moves to data/raw/quarantine_data_quality/")
    parser.add_argument("--crop", type=str, default=None, help="Filter to specific crop name (e.g. Chilli, Rice)")
    parser.add_argument("--class-name", type=str, default=None, help="Run on specific class only")
    parser.add_argument("--matching-mode", type=str, choices=["cluster", "direct_pairwise"], default="cluster", help="Matching engine: cluster (transitive) or direct_pairwise (strict 1-to-1 rotated/flipped)")
    args = parser.parse_args()

    run_sequential_pipeline(
        target_crop=args.crop,
        target_class=args.class_name,
        commit=args.commit,
        matching_mode=args.matching_mode,
    )


if __name__ == "__main__":
    main()
