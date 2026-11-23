"""
scripts/data_cleaning_dashboard.py

Interactive Foliar Pathology Data Quality & Quarantine Studio (FastAPI + Modern Web UI)
1. ⚡ Automated AI Quality Issues:
   - Loads flagged issues from data/quality_audit/flagged_issues.json
   - Side-by-side near-duplicate and cross-split leakage twin inspection with similarity %.
   - Cleanvision blur, low-information, and semantic outlier cards with one-click quarantine/ignore.
2. 🔍 Class Split Explorer & Manual Quarantine:
   - Per-class navigation across all 206 foliar classes.
   - Split navigation across Train, Val, and Test with live counts.
   - Multi-select marking with batch quarantine to data/raw/quarantine_data_quality/{reason}/
   - Individual 1-click quick quarantine on any image.
   - High-resolution modal lightbox for micro-lesion inspection.
   - Complete audit trail logging in data/quality_audit/quarantine_actions.json
"""

import os
import sys
import subprocess
from pathlib import Path

# Self-bootstrap into project .venv if run with system python
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
_VENV_PY = _PROJECT_ROOT / ".venv" / "Scripts" / "python.exe"
if _VENV_PY.exists() and Path(sys.executable).resolve() != _VENV_PY.resolve():
    _res = subprocess.run([str(_VENV_PY)] + sys.argv)
    sys.exit(_res.returncode)

import json
import logging
import shutil
import time
import hashlib
import io
import random
from collections import defaultdict
from PIL import Image, ImageOps
import imagehash

import uvicorn
from fastapi import FastAPI, HTTPException, Body, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
AUDIT_DIR = PROJECT_ROOT / "data" / "quality_audit"
ISSUES_FILE = AUDIT_DIR / "flagged_issues.json"
ACTIONS_LOG = AUDIT_DIR / "quarantine_actions.json"
QUARANTINE_ROOT = PROJECT_ROOT / "data" / "raw" / "quarantine_data_quality"
QUARANTINE_ROOT.mkdir(parents=True, exist_ok=True)

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


app = FastAPI(title="Foliar Quality & Quarantine Studio")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# In-memory cache for class counts
CLASS_CACHE = {}
CACHE_TIMESTAMP = 0


def get_cached_classes():
    global CLASS_CACHE, CACHE_TIMESTAMP
    now = time.time()
    # Cache for 60 seconds unless invalidated
    if CLASS_CACHE and (now - CACHE_TIMESTAMP < 60):
        return CLASS_CACHE

    train_dir = PROCESSED_DIR / "train"
    val_dir = PROCESSED_DIR / "val"
    test_dir = PROCESSED_DIR / "test"

    if not train_dir.exists():
        return []

    classes_list = []
    for d in sorted(train_dir.iterdir()):
        if not d.is_dir():
            continue
        cname = d.name
        crop = cname.split(" - ")[0] if " - " in cname else cname.split("_")[0]
        
        train_cnt = len([p for p in d.iterdir() if p.suffix.lower() in IMAGE_EXTS])
        
        vd = val_dir / cname
        val_cnt = len([p for p in vd.iterdir() if p.suffix.lower() in IMAGE_EXTS]) if vd.exists() else 0
        
        td = test_dir / cname
        test_cnt = len([p for p in td.iterdir() if p.suffix.lower() in IMAGE_EXTS]) if td.exists() else 0
        
        classes_list.append({
            "class_name": cname,
            "crop": crop,
            "train_count": train_cnt,
            "val_count": val_cnt,
            "test_count": test_cnt,
            "total_count": train_cnt + val_cnt + test_cnt,
        })

    CLASS_CACHE = classes_list
    CACHE_TIMESTAMP = now
    return CLASS_CACHE


def invalidate_cache():
    global CACHE_TIMESTAMP
    CACHE_TIMESTAMP = 0


@app.get("/api/classes")
def list_classes():
    return get_cached_classes()


@app.get("/api/class-images")
def get_class_images(
    class_name: str = Query(..., description="Target foliar disease class"),
    split: str = Query("train", description="Split: train, val, or test"),
    page: int = Query(1, ge=1),
    limit: int = Query(48, ge=1, le=200)
):
    if split not in ["train", "val", "test"]:
        raise HTTPException(status_code=400, detail="Split must be 'train', 'val', or 'test'")

    target_dir = PROCESSED_DIR / split / class_name
    if not target_dir.exists() or not target_dir.is_dir():
        return {
            "class_name": class_name,
            "split": split,
            "total_images": 0,
            "page": page,
            "total_pages": 0,
            "images": []
        }

    all_files = sorted([p for p in target_dir.iterdir() if p.suffix.lower() in IMAGE_EXTS])
    total_images = len(all_files)
    total_pages = max(1, (total_images + limit - 1) // limit)

    start_idx = (page - 1) * limit
    end_idx = start_idx + limit
    page_files = all_files[start_idx:end_idx]

    images_data = []
    for p in page_files:
        rel = str(p.relative_to(PROJECT_ROOT)).replace("\\", "/")
        try:
            size_kb = round(p.stat().st_size / 1024, 1)
        except:
            size_kb = 0.0
        images_data.append({
            "filename": p.name,
            "path": rel,
            "size_kb": size_kb
        })

    return {
        "class_name": class_name,
        "split": split,
        "total_images": total_images,
        "page": page,
        "total_pages": total_pages,
        "limit": limit,
        "images": images_data
    }


@app.get("/api/issues")
def get_issues():
    if not ISSUES_FILE.exists():
        return JSONResponse(
            content={"total_issues": 0, "issues": []},
            headers={"Cache-Control": "no-cache, no-store, must-revalidate", "Pragma": "no-cache", "Expires": "0"}
        )
    with open(ISSUES_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return JSONResponse(
        content=data,
        headers={"Cache-Control": "no-cache, no-store, must-revalidate", "Pragma": "no-cache", "Expires": "0"}
    )


@app.get("/api/image")
def get_image(path: str):
    p = PROJECT_ROOT / path
    if not p.exists() or not p.is_file():
        raise HTTPException(status_code=404, detail="Image not found")
    return FileResponse(p)


def remove_quarantined_from_issues(quarantined_paths: list):
    """Permanently purges quarantined or dismissed image issues from flagged_issues.json."""
    if not ISSUES_FILE.exists():
        return
    try:
        with open(ISSUES_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        target_norms = set()
        target_filenames = set()
        for qp in quarantined_paths:
            if not qp:
                continue
            clean = str(qp).replace("\\", "/").strip().lower()
            target_norms.add(clean)
            target_filenames.add(Path(clean).name.lower())

        remaining_issues = []
        for issue in data.get("issues", []):
            p1 = issue.get("primary_image", {})
            p2 = issue.get("secondary_image", {})

            p1_path = p1.get("path", "").replace("\\", "/").strip().lower()
            p1_fn = p1.get("filename", "").strip().lower() or Path(p1_path).name.lower()

            p2_path = p2.get("path", "").replace("\\", "/").strip().lower() if p2 else ""
            p2_fn = (p2.get("filename", "").strip().lower() or Path(p2_path).name.lower()) if p2 else ""

            hit_p1 = (p1_path in target_norms) or (p1_fn in target_filenames)
            hit_p2 = bool(p2) and ((p2_path in target_norms) or (p2_fn in target_filenames))

            # If either image of a pair or the single specimen is quarantined/dismissed, eliminate the card
            if hit_p1 or hit_p2:
                continue
            remaining_issues.append(issue)

        data["issues"] = remaining_issues
        data["total_issues"] = len(remaining_issues)

        with open(ISSUES_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"Error updating flagged_issues.json: {e}")


@app.post("/api/quarantine")
def quarantine_image(payload: dict = Body(...)):
    raw_path = payload.get("path")
    reason = payload.get("reason", "manual_quarantine")

    if not raw_path:
        raise HTTPException(status_code=400, detail="Missing relative image path")

    norm_path = raw_path.replace("\\", "/").strip()
    src = PROJECT_ROOT / norm_path

    # Fallback search by filename in processed data if path has split discrepancy or escaped slashes
    if not src.exists():
        fname = Path(norm_path).name
        candidates = list((PROJECT_ROOT / "data" / "processed").rglob(fname))
        if candidates:
            src = candidates[0]

    # If still not found, check if already in quarantine
    if not src.exists():
        fname = Path(norm_path).name
        quarantined_candidates = list((PROJECT_ROOT / "data" / "raw" / "quarantine_data_quality").rglob(fname))
        if quarantined_candidates:
            remove_quarantined_from_issues([raw_path, norm_path, fname])
            invalidate_cache()
            return {"status": "already_moved", "message": f"File is already in quarantine: {fname}"}
        return {"status": "error", "message": f"File does not exist: {norm_path}"}

    class_name = src.parent.name
    dest_dir = QUARANTINE_ROOT / reason / class_name
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest_file = dest_dir / src.name

    shutil.move(str(src), str(dest_file))
    invalidate_cache()

    actual_rel = str(src.relative_to(PROJECT_ROOT)).replace("\\", "/")
    remove_quarantined_from_issues([raw_path, norm_path, actual_rel, src.name])

    log_entry = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "original_path": actual_rel,
        "quarantined_path": str(dest_file.relative_to(PROJECT_ROOT)).replace("\\", "/"),
        "reason": reason,
    }

    actions = []
    if ACTIONS_LOG.exists():
        try:
            with open(ACTIONS_LOG, "r", encoding="utf-8") as f:
                actions = json.load(f)
        except:
            actions = []
    actions.append(log_entry)
    with open(ACTIONS_LOG, "w", encoding="utf-8") as f:
        json.dump(actions, f, indent=2)

    return {"status": "success", "quarantined_to": str(dest_file.relative_to(PROJECT_ROOT)).replace("\\", "/")}


@app.post("/api/quarantine-batch")
def quarantine_batch(payload: dict = Body(...)):
    paths = payload.get("paths", [])
    reason = payload.get("reason", "manual_inspection")

    if not paths:
        raise HTTPException(status_code=400, detail="No image paths provided")

    success_list = []
    quarantined_rel_paths = []

    for raw_path in paths:
        norm_path = raw_path.replace("\\", "/").strip()
        src = PROJECT_ROOT / norm_path

        if not src.exists():
            fname = Path(norm_path).name
            candidates = list((PROJECT_ROOT / "data" / "processed").rglob(fname))
            if candidates:
                src = candidates[0]

        if src.exists():
            class_name = src.parent.name
            dest_dir = QUARANTINE_ROOT / reason / class_name
            dest_dir.mkdir(parents=True, exist_ok=True)
            dest_file = dest_dir / src.name
            shutil.move(str(src), str(dest_file))

            actual_rel = str(src.relative_to(PROJECT_ROOT)).replace("\\", "/")
            quarantined_rel_paths.extend([raw_path, norm_path, actual_rel, src.name])

            success_list.append({
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "original_path": actual_rel,
                "quarantined_path": str(dest_file.relative_to(PROJECT_ROOT)).replace("\\", "/"),
                "reason": reason,
            })

    invalidate_cache()
    if quarantined_rel_paths:
        remove_quarantined_from_issues(quarantined_rel_paths)

    if success_list:
        actions = []
        if ACTIONS_LOG.exists():
            try:
                with open(ACTIONS_LOG, "r", encoding="utf-8") as f:
                    actions = json.load(f)
            except:
                actions = []
        actions.extend(success_list)
        with open(ACTIONS_LOG, "w", encoding="utf-8") as f:
            json.dump(actions, f, indent=2)

    return {"status": "success", "quarantined_count": len(success_list)}


@app.post("/api/dismiss-issue")
def dismiss_issue(payload: dict = Body(...)):
    """Permanently dismisses an issue from flagged_issues.json so it does not reappear on refresh."""
    p1 = payload.get("primary_path", "")
    p2 = payload.get("secondary_path", "")
    to_dismiss = [p for p in [p1, p2] if p]

    if not to_dismiss:
        raise HTTPException(status_code=400, detail="Missing paths to dismiss")

    remove_quarantined_from_issues(to_dismiss)
    return {"status": "success", "message": "Issue dismissed permanently"}


# ==============================================================================
# ⚡ AUTOMATED DE-DUPLICATION & CROSS-SPLIT ANTI-LEAKAGE MECHANISM
# ==============================================================================

def compute_multirot_dhashes(thumb: Image.Image) -> list:
    """Computes dHash across 0, 90, 180, 270 deg rotations and mirror on a 32x32 thumbnail."""
    dhs = [int(str(imagehash.dhash(thumb)), 16)]
    for a in (90, 180, 270):
        dhs.append(int(str(imagehash.dhash(thumb.rotate(a))), 16))
    dhs.append(int(str(imagehash.dhash(ImageOps.mirror(thumb))), 16))
    return dhs


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
    Resolves duplicate clusters according to strict anti-leakage & dedup rules:
    1. Cross-Split Leakage involving Train:
       - Safely remove ALL copies in Train (including any internal duplicates in Train).
       - For remaining Eval copies (in Val and/or Test):
         * If both Val and Test copies exist: randomly keep 1, quarantine others under 'cross_split_leakage_val_test'.
         * If only Val (or only Test) copies exist: randomly keep 1, quarantine extra duplicates under 'near_duplicate_redundancy'.
    2. Cross-Split Leakage between Val and Test only:
       - Randomly keep 1, quarantine others under 'cross_split_leakage_val_test'.
    3. Within-Split Internal Duplicates only:
       - Randomly keep 1, quarantine all other |C|-1 duplicates under 'near_duplicate_redundancy'.
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

    return to_quarantine, to_keep, stats


def execute_quarantine_moves(to_quarantine: list) -> list:
    """Executes file relocations to quarantine_data_quality/{reason}/{class_name}."""
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

    invalidate_cache()
    if quarantined_paths:
        remove_quarantined_from_issues(quarantined_paths)

    if success_actions:
        existing_actions = []
        if ACTIONS_LOG.exists():
            try:
                with open(ACTIONS_LOG, "r", encoding="utf-8") as f:
                    existing_actions = json.load(f)
            except Exception:
                existing_actions = []
        existing_actions.extend(success_actions)
        with open(ACTIONS_LOG, "w", encoding="utf-8") as f:
            json.dump(existing_actions, f, indent=2)

    return success_actions


@app.post("/api/auto-resolve-pair")
def auto_resolve_pair(payload: dict = Body(...)):
    """
    Auto-resolves a single pair of duplicates/leakage according to user rules:
    - If leakage involves train: purges train copy (leaves eval copy).
    - If leakage between val and test: randomly keeps one, purges the other.
    - If within the same split: randomly keeps one, purges the redundant duplicate.
    """
    p1_raw = payload.get("primary_path", "")
    p2_raw = payload.get("secondary_path", "")
    if not p1_raw or not p2_raw:
        raise HTTPException(status_code=400, detail="Missing image paths for pair")

    def make_rec(p_raw):
        norm = p_raw.replace("\\", "/").strip()
        src = PROJECT_ROOT / norm
        if not src.exists():
            candidates = list((PROJECT_ROOT / "data" / "processed").rglob(Path(norm).name))
            if candidates:
                src = candidates[0]
        if not src.exists():
            return None
        actual_rel = str(src.relative_to(PROJECT_ROOT)).replace("\\", "/")
        split = "train"
        if "/val/" in actual_rel or "\\val\\" in str(src):
            split = "val"
        elif "/test/" in actual_rel or "\\test\\" in str(src):
            split = "test"
        return {
            "path": actual_rel,
            "name": src.name,
            "split": split,
            "class": src.parent.name,
        }

    r1 = make_rec(p1_raw)
    r2 = make_rec(p2_raw)

    if not r1 and not r2:
        raise HTTPException(status_code=404, detail="Neither image file exists on disk")

    if not r1 or not r2:
        remove_quarantined_from_issues([p1_raw, p2_raw])
        return {"status": "already_resolved", "message": "One of the images was already quarantined or missing."}

    cluster = [r1, r2]
    to_quarantine, to_keep, stats = resolve_duplicate_clusters([cluster])
    actions = execute_quarantine_moves(to_quarantine)

    remove_quarantined_from_issues([p1_raw, p2_raw, r1["path"], r2["path"]])

    quarantined_names = [Path(x[0]["path"]).name for x in to_quarantine]
    kept_names = [Path(x["path"]).name for x in to_keep]
    reason = to_quarantine[0][1] if to_quarantine else "unknown"

    if reason == "cross_split_leakage_from_train":
        explanation = f"Purged train duplicate ({quarantined_names[0]}) to eliminate leakage into evaluation benchmark ({kept_names[0]})."
    elif reason == "cross_split_leakage_val_test":
        explanation = f"Randomly retained {kept_names[0]} and quarantined twin {quarantined_names[0]} to resolve Val/Test leakage."
    else:
        explanation = f"Randomly retained unique copy {kept_names[0]} and quarantined duplicate {quarantined_names[0]}."

    return {
        "status": "success",
        "explanation": explanation,
        "quarantined": quarantined_names,
        "kept": kept_names,
        "reason": reason,
    }


@app.post("/api/auto-resolve-all")
def auto_resolve_all(payload: dict = Body(...)):
    """
    Batch resolves duplicate redundancy & cross-split leakage.
    Source 'issues': resolves flagged pairs in flagged_issues.json.
    Source 'class_scan': scans target class on disk using MD5 + multirot dHash and resolves all clusters.
    """
    source = payload.get("source", "issues")
    target_class = payload.get("target_class") or None

    if source == "class_scan":
        if not target_class:
            raise HTTPException(status_code=400, detail="Target class is required for direct disk scan")

        records = []
        before_counts = {"train": 0, "val": 0, "test": 0}
        for split in ["train", "val", "test"]:
            cdir = PROCESSED_DIR / split / target_class
            if not cdir.exists():
                continue
            files = sorted([p for p in cdir.iterdir() if p.suffix.lower() in IMAGE_EXTS])
            before_counts[split] = len(files)
            for p in files:
                rel = str(p.relative_to(PROJECT_ROOT)).replace("\\", "/")
                records.append({
                    "id": len(records),
                    "path": rel,
                    "name": p.name,
                    "split": split,
                    "class": target_class,
                    "abs_path": str(p),
                })

        if len(records) < 2:
            return {
                "status": "success",
                "message": f"Class '{target_class}' has {len(records)} images. No duplicate clusters found.",
                "clusters_resolved": 0,
                "quarantined_count": 0,
                "before": before_counts,
                "after": before_counts,
            }

        dset = DisjointSet([r["path"] for r in records])
        md5_map = defaultdict(list)
        dhashes = []

        for r in records:
            data = Path(r["abs_path"]).read_bytes()
            h_md5 = hashlib.md5(data).hexdigest()
            r["md5"] = h_md5
            md5_map[h_md5].append(r["path"])

            with Image.open(io.BytesIO(data)) as im:
                rgb = im.convert("RGB")
                thumb = rgb.resize((32, 32), Image.Resampling.BILINEAR)
                dhashes.append(compute_multirot_dhashes(thumb))

        # A. Union exact MD5
        for h, paths in md5_map.items():
            if len(paths) > 1:
                for i in range(len(paths) - 1):
                    dset.union(paths[i], paths[i + 1])

        # B. Union dHash <= 3
        n = len(records)
        for i in range(n):
            dh_i = dhashes[i]
            p_i = records[i]["path"]
            for j in range(i + 1, n):
                p_j = records[j]["path"]
                if dset.find(p_i) == dset.find(p_j):
                    continue
                min_dh = 64
                for h1 in dh_i:
                    for h2 in dhashes[j]:
                        dist = (h1 ^ h2).bit_count()
                        if dist < min_dh:
                            min_dh = dist
                            if min_dh <= 3:
                                break
                    if min_dh <= 3:
                        break
                if min_dh <= 3:
                    dset.union(p_i, p_j)

        cluster_groups = defaultdict(list)
        for r in records:
            root = dset.find(r["path"])
            cluster_groups[root].append(r)

        dup_clusters = [c for c in cluster_groups.values() if len(c) > 1]
        to_quarantine, to_keep, stats = resolve_duplicate_clusters(dup_clusters)
        actions = execute_quarantine_moves(to_quarantine)

        after_counts = {
            "train": before_counts["train"] - stats["quarantined_by_split"]["train"],
            "val": before_counts["val"] - stats["quarantined_by_split"]["val"],
            "test": before_counts["test"] - stats["quarantined_by_split"]["test"],
        }

        return {
            "status": "success",
            "class_name": target_class,
            "clusters_resolved": len(dup_clusters),
            "quarantined_count": len(to_quarantine),
            "quarantined_by_split": dict(stats["quarantined_by_split"]),
            "quarantined_by_reason": dict(stats["quarantined_by_reason"]),
            "before": before_counts,
            "after": after_counts,
            "message": f"Successfully resolved {len(dup_clusters)} clusters in '{target_class}'. Quarantined {len(to_quarantine)} duplicate/leak images.",
        }

    else:  # source == 'issues'
        if not ISSUES_FILE.exists():
            return {
                "status": "no_issues",
                "message": "No flagged issues file found.",
                "clusters_resolved": 0,
                "quarantined_count": 0,
            }

        with open(ISSUES_FILE, "r", encoding="utf-8") as f:
            issue_data = json.load(f)

        issues = issue_data.get("issues", [])
        candidate_issues = []
        for it in issues:
            if it.get("type") in ["near_duplicate", "cross_split_leakage"]:
                p1 = it.get("primary_image", {})
                p2 = it.get("secondary_image", {})
                if target_class:
                    c1 = p1.get("class", "")
                    c2 = p2.get("class", "")
                    if c1 != target_class and c2 != target_class:
                        continue
                candidate_issues.append(it)

        if not candidate_issues:
            return {
                "status": "no_issues",
                "message": f"No duplicate or leakage issues found for '{target_class or 'all classes'}'.",
                "clusters_resolved": 0,
                "quarantined_count": 0,
            }

        path_record_map = {}

        def get_or_make_record(img_dict):
            p_raw = img_dict.get("path", "")
            norm = p_raw.replace("\\", "/").strip()
            if norm not in path_record_map:
                src = PROJECT_ROOT / norm
                if not src.exists():
                    fname = img_dict.get("filename") or Path(norm).name
                    candidates = list((PROJECT_ROOT / "data" / "processed").rglob(fname))
                    if candidates:
                        src = candidates[0]
                actual_rel = str(src.relative_to(PROJECT_ROOT)).replace("\\", "/") if src.exists() else norm
                split = img_dict.get("split") or ("val" if "/val/" in actual_rel else ("test" if "/test/" in actual_rel else "train"))
                path_record_map[norm] = {
                    "path": actual_rel,
                    "name": img_dict.get("filename") or Path(norm).name,
                    "split": split,
                    "class": img_dict.get("class") or (src.parent.name if src.exists() else ""),
                }
            return path_record_map[norm]

        all_paths = set()
        for it in candidate_issues:
            p1 = it.get("primary_image", {})
            p2 = it.get("secondary_image", {})
            if p1 and p2:
                r1 = get_or_make_record(p1)
                r2 = get_or_make_record(p2)
                all_paths.add(r1["path"])
                all_paths.add(r2["path"])

        dset = DisjointSet(all_paths)
        for it in candidate_issues:
            p1 = it.get("primary_image", {})
            p2 = it.get("secondary_image", {})
            if p1 and p2:
                r1 = get_or_make_record(p1)
                r2 = get_or_make_record(p2)
                dset.union(r1["path"], r2["path"])

        cluster_groups = defaultdict(list)
        path_to_rec = {r["path"]: r for r in path_record_map.values()}
        for p in all_paths:
            root = dset.find(p)
            if p in path_to_rec:
                cluster_groups[root].append(path_to_rec[p])

        dup_clusters = [c for c in cluster_groups.values() if len(c) > 1]
        to_quarantine, to_keep, stats = resolve_duplicate_clusters(dup_clusters)
        actions = execute_quarantine_moves(to_quarantine)

        return {
            "status": "success",
            "clusters_resolved": len(dup_clusters),
            "quarantined_count": len(to_quarantine),
            "quarantined_by_split": dict(stats["quarantined_by_split"]),
            "quarantined_by_reason": dict(stats["quarantined_by_reason"]),
            "message": f"Successfully auto-resolved {len(dup_clusters)} duplicate/leakage clusters. Quarantined {len(to_quarantine)} images.",
        }


SCAN_STATE = {
    "status": "idle",
    "progress": 0,
    "stage": "",
    "message": "Ready to scan.",
    "target_class": None,
    "target_crop": None,
    "target_issue": None,
    "total_images": 0,
    "issues_found": 0,
    "elapsed_sec": 0,
    "error": None,
}

SCAN_CANCEL_REQUESTED = False


def run_scan_in_background(target_crop, target_class, max_per_class, target_issue):
    global SCAN_STATE, SCAN_CANCEL_REQUESTED
    SCAN_CANCEL_REQUESTED = False
    start_time = time.time()
    SCAN_STATE["status"] = "running"
    SCAN_STATE["progress"] = 2
    SCAN_STATE["stage"] = "Initializing"
    SCAN_STATE["message"] = "Preparing candidate images..."
    SCAN_STATE["target_class"] = target_class
    SCAN_STATE["target_crop"] = target_crop
    SCAN_STATE["target_issue"] = target_issue
    SCAN_STATE["issues_found"] = 0
    SCAN_STATE["error"] = None

    def on_progress(pct, stage, msg):
        global SCAN_CANCEL_REQUESTED
        if SCAN_CANCEL_REQUESTED:
            raise InterruptedError("Scan cancelled by user.")
        SCAN_STATE["progress"] = pct
        SCAN_STATE["stage"] = stage
        SCAN_STATE["message"] = msg
        SCAN_STATE["elapsed_sec"] = round(time.time() - start_time, 1)

    try:
        if str(PROJECT_ROOT) not in sys.path:
            sys.path.insert(0, str(PROJECT_ROOT))
        try:
            from scripts.data_cleaning_scanner import scan_dataset
        except ImportError:
            from data_cleaning_scanner import scan_dataset

        out_file = scan_dataset(
            target_crop=target_crop,
            target_class=target_class,
            max_per_class=max_per_class,
            n_jobs=1,
            target_issue=target_issue,
            progress_callback=on_progress,
        )
        total_issues = 0
        if out_file and Path(out_file).exists():
            with open(out_file, "r", encoding="utf-8") as f:
                d = json.load(f)
                total_issues = d.get("total_issues", 0)

        SCAN_STATE["status"] = "completed"
        SCAN_STATE["progress"] = 100
        SCAN_STATE["stage"] = "Done"
        SCAN_STATE["issues_found"] = total_issues
        SCAN_STATE["message"] = f"Audit complete! {total_issues} issues flagged."
        SCAN_STATE["elapsed_sec"] = round(time.time() - start_time, 1)
    except InterruptedError:
        SCAN_STATE["status"] = "idle"
        SCAN_STATE["progress"] = 0
        SCAN_STATE["stage"] = "Cancelled"
        SCAN_STATE["message"] = "Scan cancelled by user."
        SCAN_STATE["elapsed_sec"] = round(time.time() - start_time, 1)
    except Exception as e:
        SCAN_STATE["status"] = "error"
        SCAN_STATE["error"] = str(e)
        SCAN_STATE["message"] = f"Scan failed: {str(e)}"
        SCAN_STATE["elapsed_sec"] = round(time.time() - start_time, 1)


@app.get("/api/scan/status")
def get_scan_status():
    global SCAN_STATE
    return SCAN_STATE


@app.post("/api/scan/cancel")
def cancel_scan():
    global SCAN_CANCEL_REQUESTED, SCAN_STATE
    SCAN_CANCEL_REQUESTED = True
    SCAN_STATE["status"] = "idle"
    SCAN_STATE["stage"] = "Cancelled"
    SCAN_STATE["message"] = "Scan cancelled by user."
    return {"status": "cancelled", "message": "Scan cancellation signal sent."}


@app.post("/api/scan/start")
def start_scan(payload: dict = Body(...)):
    global SCAN_STATE
    if SCAN_STATE["status"] == "running":
        return {"status": "already_running", "message": "A scan is already in progress."}

    target_crop = payload.get("crop") or None
    target_class = payload.get("class_name") or None
    target_issue = payload.get("issue") or None
    if target_issue in ["all", ""]:
        target_issue = None
    max_images = int(payload.get("max_images", 50))

    import threading
    t = threading.Thread(
        target=run_scan_in_background,
        args=(target_crop, target_class, max_images, target_issue),
        daemon=True,
    )
    t.start()
    return {"status": "started", "message": "Scan started in background."}


# ==============================================================================
# 🤖 AUTONOMOUS SEQUENTIAL CLASS-BY-CLASS AUTO-SCREENING & CLEANING PIPELINE
# ==============================================================================

AUTO_PIPELINE_STATE = {
    "status": "idle",  # "idle", "running", "completed", "error"
    "progress": 0,
    "current_index": 0,
    "total_classes": 0,
    "current_class": "",
    "message": "Ready to run sequential pipeline.",
    "total_quarantined": 0,
    "total_train_purged": 0,
    "total_val_purged": 0,
    "total_test_purged": 0,
    "classes_with_issues": 0,
    "recent_logs": [],
    "elapsed_sec": 0,
    "error": None,
    "summary": None,
}

PIPELINE_CANCEL_REQUESTED = False


def run_pipeline_in_background(target_crop=None, target_class=None, commit=True, matching_mode="cluster"):
    global AUTO_PIPELINE_STATE, PIPELINE_CANCEL_REQUESTED
    PIPELINE_CANCEL_REQUESTED = False
    start_time = time.time()

    AUTO_PIPELINE_STATE["status"] = "running"
    AUTO_PIPELINE_STATE["progress"] = 0
    AUTO_PIPELINE_STATE["current_index"] = 0
    AUTO_PIPELINE_STATE["current_class"] = "Initializing..."
    AUTO_PIPELINE_STATE["message"] = f"Preparing classes for sequential pipeline ({matching_mode})..."
    AUTO_PIPELINE_STATE["total_quarantined"] = 0
    AUTO_PIPELINE_STATE["total_train_purged"] = 0
    AUTO_PIPELINE_STATE["total_val_purged"] = 0
    AUTO_PIPELINE_STATE["total_test_purged"] = 0
    AUTO_PIPELINE_STATE["classes_with_issues"] = 0
    AUTO_PIPELINE_STATE["recent_logs"] = []
    AUTO_PIPELINE_STATE["elapsed_sec"] = 0
    AUTO_PIPELINE_STATE["error"] = None
    AUTO_PIPELINE_STATE["summary"] = None

    def pipeline_callback(pct, class_index, total_classes, class_name, message, total_quarantined=0, total_train_purged=0):
        global PIPELINE_CANCEL_REQUESTED
        if PIPELINE_CANCEL_REQUESTED:
            raise InterruptedError("Pipeline cancelled by user.")
        AUTO_PIPELINE_STATE["progress"] = pct
        AUTO_PIPELINE_STATE["current_index"] = class_index
        AUTO_PIPELINE_STATE["total_classes"] = total_classes
        AUTO_PIPELINE_STATE["current_class"] = class_name
        AUTO_PIPELINE_STATE["message"] = message
        AUTO_PIPELINE_STATE["total_quarantined"] = total_quarantined
        AUTO_PIPELINE_STATE["total_train_purged"] = total_train_purged
        AUTO_PIPELINE_STATE["elapsed_sec"] = round(time.time() - start_time, 1)

    try:
        if str(PROJECT_ROOT) not in sys.path:
            sys.path.insert(0, str(PROJECT_ROOT))
        try:
            from scripts.auto_screen_and_clean_dataset import run_sequential_pipeline
        except ImportError:
            from auto_screen_and_clean_dataset import run_sequential_pipeline

        summary = run_sequential_pipeline(
            target_crop=target_crop,
            target_class=target_class,
            commit=commit,
            matching_mode=matching_mode,
            progress_callback=pipeline_callback,
        )

        AUTO_PIPELINE_STATE["status"] = "completed"
        AUTO_PIPELINE_STATE["progress"] = 100
        AUTO_PIPELINE_STATE["message"] = f"Pipeline complete! Quarantined {summary['total_quarantined']} images across {summary['classes_with_issues']} classes ({matching_mode})."
        AUTO_PIPELINE_STATE["total_quarantined"] = summary["total_quarantined"]
        AUTO_PIPELINE_STATE["total_train_purged"] = summary["quarantined_from_train"]
        AUTO_PIPELINE_STATE["total_val_purged"] = summary["quarantined_from_val"]
        AUTO_PIPELINE_STATE["total_test_purged"] = summary["quarantined_from_test"]
        AUTO_PIPELINE_STATE["classes_with_issues"] = summary["classes_with_issues"]
        AUTO_PIPELINE_STATE["summary"] = summary
        AUTO_PIPELINE_STATE["elapsed_sec"] = round(time.time() - start_time, 1)
        invalidate_cache()
    except InterruptedError:
        AUTO_PIPELINE_STATE["status"] = "idle"
        AUTO_PIPELINE_STATE["progress"] = 0
        AUTO_PIPELINE_STATE["message"] = "Pipeline stopped by user."
        AUTO_PIPELINE_STATE["elapsed_sec"] = round(time.time() - start_time, 1)
        invalidate_cache()
    except Exception as e:
        AUTO_PIPELINE_STATE["status"] = "error"
        AUTO_PIPELINE_STATE["error"] = str(e)
        AUTO_PIPELINE_STATE["message"] = f"Pipeline failed: {str(e)}"
        AUTO_PIPELINE_STATE["elapsed_sec"] = round(time.time() - start_time, 1)


@app.get("/api/pipeline/status")
def get_pipeline_status():
    global AUTO_PIPELINE_STATE
    return AUTO_PIPELINE_STATE


@app.post("/api/pipeline/cancel")
def cancel_pipeline():
    global PIPELINE_CANCEL_REQUESTED, AUTO_PIPELINE_STATE
    PIPELINE_CANCEL_REQUESTED = True
    AUTO_PIPELINE_STATE["status"] = "idle"
    AUTO_PIPELINE_STATE["message"] = "Pipeline cancellation requested."
    return {"status": "cancelled", "message": "Pipeline cancellation signal sent."}


@app.post("/api/pipeline/start")
def start_pipeline(payload: dict = Body(...)):
    global AUTO_PIPELINE_STATE
    if AUTO_PIPELINE_STATE["status"] == "running":
        return {"status": "already_running", "message": "A pipeline is already running."}

    target_crop = payload.get("crop") or None
    target_class = payload.get("class_name") or None
    commit = bool(payload.get("commit", True))
    matching_mode = payload.get("matching_mode", "cluster")

    import threading
    t = threading.Thread(
        target=run_pipeline_in_background,
        args=(target_crop, target_class, commit, matching_mode),
        daemon=True,
    )
    t.start()
    return {"status": "started", "message": f"Sequential screening pipeline started using '{matching_mode}' engine."}



@app.get("/", response_class=HTMLResponse)
def index():
    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🌿 Foliar Pathology Quality Studio</title>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-base: #090d16;
            --bg-surface: #111827;
            --bg-card: #182234;
            --border-subtle: #243247;
            --border-hover: #38bdf8;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --accent-primary: #38bdf8;
            --accent-green: #22c55e;
            --accent-red: #ef4444;
            --accent-amber: #f59e0b;
            --accent-purple: #a855f7;
        }

        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            background-color: var(--bg-base);
            color: var(--text-main);
            font-family: 'Plus Jakarta Sans', sans-serif;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }

        /* Header */
        header {
            background: rgba(17, 24, 39, 0.95);
            backdrop-filter: blur(12px);
            border-bottom: 1px solid var(--border-subtle);
            padding: 14px 32px;
            position: sticky;
            top: 0;
            z-index: 50;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .brand {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .brand-icon {
            font-size: 24px;
            background: linear-gradient(135deg, #0284c7, #38bdf8);
            padding: 8px;
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .brand h1 { font-size: 18px; font-weight: 700; letter-spacing: -0.02em; }
        .brand p { font-size: 12px; color: var(--text-muted); }

        /* Top Nav View Switcher */
        .nav-tabs {
            display: flex;
            gap: 6px;
            background: #0d131f;
            padding: 4px;
            border-radius: 10px;
            border: 1px solid var(--border-subtle);
        }

        .nav-tab-btn {
            background: transparent;
            color: var(--text-muted);
            border: none;
            padding: 8px 18px;
            border-radius: 8px;
            font-size: 13px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s ease;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .nav-tab-btn:hover { color: var(--text-main); }
        .nav-tab-btn.active {
            background: #1e293b;
            color: var(--accent-primary);
            box-shadow: 0 0 12px rgba(56, 189, 248, 0.2);
        }

        .stats-badge {
            background: var(--bg-card);
            border: 1px solid var(--border-subtle);
            padding: 6px 14px;
            border-radius: 9999px;
            font-size: 13px;
            display: flex;
            gap: 8px;
            align-items: center;
        }
        .stats-badge span { color: var(--accent-primary); font-weight: 700; font-family: 'JetBrains Mono', monospace; }

        /* Sub-Toolbars */
        .toolbar {
            background: var(--bg-surface);
            border-bottom: 1px solid var(--border-subtle);
            padding: 12px 32px;
            display: flex;
            align-items: center;
            gap: 12px;
            flex-wrap: wrap;
        }

        .filter-btn {
            background: transparent;
            color: var(--text-muted);
            border: 1px solid transparent;
            padding: 6px 14px;
            border-radius: 8px;
            font-size: 13px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s ease;
            white-space: nowrap;
        }

        .filter-btn:hover { background: var(--bg-card); color: var(--text-main); }
        .filter-btn.active {
            background: #1e293b;
            color: var(--accent-primary);
            border-color: #38bdf840;
            box-shadow: 0 0 12px #38bdf81a;
        }

        /* Class Inspector Controls */
        .inspector-bar {
            background: #0f172a;
            border-bottom: 1px solid var(--border-subtle);
            padding: 14px 32px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 16px;
            flex-wrap: wrap;
        }

        .selector-group {
            display: flex;
            align-items: center;
            gap: 12px;
            flex-wrap: wrap;
        }

        .custom-select {
            background: #182234;
            color: var(--text-main);
            border: 1px solid var(--border-subtle);
            padding: 8px 14px;
            border-radius: 8px;
            font-size: 13px;
            font-weight: 600;
            outline: none;
            cursor: pointer;
            font-family: inherit;
        }
        .custom-select:focus { border-color: var(--accent-primary); }

        .search-input {
            background: #182234;
            color: var(--text-main);
            border: 1px solid var(--border-subtle);
            padding: 8px 14px;
            border-radius: 8px;
            font-size: 13px;
            outline: none;
            width: 220px;
        }
        .search-input:focus { border-color: var(--accent-primary); }

        /* Split Pills */
        .split-pill-group {
            display: flex;
            background: #090d16;
            padding: 3px;
            border-radius: 8px;
            border: 1px solid var(--border-subtle);
        }

        .split-pill {
            background: transparent;
            color: var(--text-muted);
            border: none;
            padding: 6px 14px;
            border-radius: 6px;
            font-size: 12px;
            font-weight: 600;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 6px;
            transition: all 0.15s ease;
        }
        .split-pill.active {
            background: #1e293b;
            color: #38bdf8;
            font-weight: 700;
        }
        .split-pill span {
            background: #0f172a;
            padding: 2px 6px;
            border-radius: 4px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 11px;
        }

        /* Batch Action Bar */
        .batch-bar {
            background: #131d2e;
            border-bottom: 1px solid var(--border-subtle);
            padding: 10px 32px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 16px;
        }

        .batch-info {
            display: flex;
            align-items: center;
            gap: 12px;
            font-size: 13px;
            color: var(--text-muted);
        }
        .batch-info strong { color: var(--accent-primary); font-family: 'JetBrains Mono', monospace; }

        .batch-controls {
            display: flex;
            align-items: center;
            gap: 10px;
        }

        /* Main Content Container */
        main {
            flex: 1;
            padding: 28px 32px;
            max-width: 1700px;
            margin: 0 auto;
            width: 100%;
        }

        /* Issue Grid */
        .issue-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(480px, 1fr));
            gap: 24px;
        }

        /* Class Image Grid */
        .class-image-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(210px, 1fr));
            gap: 16px;
        }

        /* Card Styles */
        .card {
            background: var(--bg-surface);
            border: 1px solid var(--border-subtle);
            border-radius: 14px;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            transition: transform 0.2s, border-color 0.2s, box-shadow 0.2s;
        }

        .card:hover {
            border-color: var(--border-hover);
            transform: translateY(-2px);
            box-shadow: 0 12px 24px rgba(0, 0, 0, 0.35);
        }

        /* Leaf Image Card (Inspector) */
        .leaf-card {
            background: var(--bg-surface);
            border: 1px solid var(--border-subtle);
            border-radius: 10px;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            position: relative;
            cursor: pointer;
            transition: all 0.15s ease;
        }
        .leaf-card:hover {
            border-color: #38bdf888;
            transform: translateY(-2px);
        }
        .leaf-card.selected {
            border-color: var(--accent-primary);
            box-shadow: 0 0 16px rgba(56, 189, 248, 0.4);
            background: #132238;
        }

        .leaf-img-box {
            position: relative;
            width: 100%;
            height: 180px;
            background: #000;
            overflow: hidden;
        }

        .leaf-img-box img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: transform 0.25s ease;
        }
        .leaf-card:hover .leaf-img-box img {
            transform: scale(1.04);
        }

        .select-checkbox-overlay {
            position: absolute;
            top: 8px;
            left: 8px;
            z-index: 10;
            width: 22px;
            height: 22px;
            accent-color: var(--accent-primary);
            cursor: pointer;
        }

        .quick-quarantine-overlay {
            position: absolute;
            top: 8px;
            right: 8px;
            z-index: 10;
            background: rgba(239, 68, 68, 0.85);
            color: #fff;
            border: none;
            width: 26px;
            height: 26px;
            border-radius: 6px;
            font-size: 13px;
            font-weight: 700;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            opacity: 0.85;
            transition: all 0.15s ease;
        }
        .quick-quarantine-overlay:hover {
            opacity: 1;
            transform: scale(1.1);
            background: #dc2626;
        }

        .leaf-card-footer {
            padding: 8px 10px;
            display: flex;
            flex-direction: column;
            gap: 2px;
            background: #111a28;
        }
        .leaf-card-fn {
            font-size: 11px;
            font-family: 'JetBrains Mono', monospace;
            color: #cbd5e1;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }
        .leaf-card-size {
            font-size: 10px;
            color: var(--text-muted);
            font-family: 'JetBrains Mono', monospace;
        }

        /* Card Header & Body */
        .card-header {
            padding: 14px 18px;
            border-bottom: 1px solid var(--border-subtle);
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: #131d2e;
        }

        .badge-type {
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            padding: 4px 10px;
            border-radius: 6px;
            font-family: 'JetBrains Mono', monospace;
        }

        .badge-cross_split_leakage { background: #ef444426; color: #f87171; border: 1px solid #ef44444d; }
        .badge-near_duplicate { background: #f59e0b26; color: #fbbf24; border: 1px solid #f59e0b4d; }
        .badge-watermark_or_text { background: #a855f726; color: #c084fc; border: 1px solid #a855f74d; }
        .badge-severe_blur { background: #06b6d426; color: #38bdf8; border: 1px solid #06b6d44d; }
        .badge-semantic_outlier { background: #ec489926; color: #f472b6; border: 1px solid #ec48994d; }

        .card-title { font-size: 14px; font-weight: 700; color: var(--text-main); }
        .card-body {
            padding: 16px;
            display: flex;
            flex-direction: column;
            gap: 12px;
            flex: 1;
        }
        .card-desc { font-size: 12px; color: var(--text-muted); line-height: 1.4; }

        /* Image Display Layout (Side-by-side or Single) */
        .image-pair-container {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 12px;
            background: #0d131f;
            padding: 10px;
            border-radius: 10px;
            border: 1px solid var(--border-subtle);
        }

        .image-single-container {
            display: flex;
            justify-content: center;
            background: #0d131f;
            padding: 10px;
            border-radius: 10px;
            border: 1px solid var(--border-subtle);
        }

        .img-box {
            display: flex;
            flex-direction: column;
            gap: 6px;
            cursor: pointer;
        }

        .img-box img {
            width: 100%;
            height: 220px;
            object-fit: cover;
            border-radius: 8px;
            background: #000;
            border: 1px solid #1e293b;
        }

        .img-meta {
            font-size: 11px;
            font-family: 'JetBrains Mono', monospace;
            color: #cbd5e1;
            display: flex;
            flex-direction: column;
            gap: 2px;
        }

        .meta-class { font-weight: 700; color: var(--accent-primary); overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
        .meta-split { color: var(--accent-amber); font-weight: 600; }
        .meta-fn { color: #64748b; font-size: 10px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }

        /* Card Actions */
        .card-actions {
            padding: 12px 16px;
            border-top: 1px solid var(--border-subtle);
            background: #111a28;
            display: flex;
            gap: 8px;
            justify-content: flex-end;
            flex-wrap: wrap;
        }

        .btn {
            font-size: 12px;
            font-weight: 600;
            padding: 8px 14px;
            border-radius: 8px;
            cursor: pointer;
            border: 1px solid transparent;
            transition: all 0.2s ease;
            display: inline-flex;
            align-items: center;
            gap: 6px;
            font-family: inherit;
        }

        .btn-keep { background: #1e293b; color: #94a3b8; border-color: #334155; }
        .btn-keep:hover { background: #334155; color: #fff; }

        .btn-quarantine { background: #ef4444; color: #fff; }
        .btn-quarantine:hover { background: #dc2626; box-shadow: 0 0 12px #ef444440; }

        .btn-quarantine-left { background: #f97316; color: #fff; }
        .btn-quarantine-left:hover { background: #ea580c; }

        .btn-quarantine-right { background: #e11d48; color: #fff; }
        .btn-quarantine-right:hover { background: #be123c; }

        .btn-primary { background: #0284c7; color: #fff; }
        .btn-primary:hover { background: #0369a1; }

        .btn-auto-resolve {
            background: linear-gradient(135deg, #7c3aed, #a855f7);
            color: #fff;
            border: 1px solid #c084fc4d;
            box-shadow: 0 0 12px rgba(168, 85, 247, 0.25);
        }
        .btn-auto-resolve:hover {
            background: linear-gradient(135deg, #6d28d9, #9333ea);
            box-shadow: 0 0 16px rgba(168, 85, 247, 0.45);
            transform: translateY(-1px);
        }

        .btn-pipeline {
            background: linear-gradient(135deg, #059669, #10b981);
            color: #fff;
            border: 1px solid #34d3994d;
            box-shadow: 0 0 16px rgba(16, 185, 129, 0.3);
            font-weight: 700;
            padding: 8px 16px;
            border-radius: 8px;
            font-size: 13px;
            cursor: pointer;
            transition: all 0.2s ease;
            display: inline-flex;
            align-items: center;
            gap: 8px;
        }
        .btn-pipeline:hover {
            background: linear-gradient(135deg, #047857, #059669);
            box-shadow: 0 0 20px rgba(16, 185, 129, 0.5);
            transform: translateY(-1px);
        }

        /* Pipeline Modal */
        #pipeline-modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.88);
            backdrop-filter: blur(12px);
            z-index: 260;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        .live-log-box {
            background: #090e17;
            border: 1px solid #1e293b;
            border-radius: 8px;
            padding: 12px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 11px;
            color: #94a3b8;
            max-height: 180px;
            overflow-y: auto;
            line-height: 1.6;
        }
        .live-log-box .log-clean { color: #22c55e; }
        .live-log-box .log-quarantine { color: #f59e0b; }
        .live-log-box .log-leak { color: #ef4444; }

        /* Auto-Resolve Modal */
        #auto-resolve-modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.85);
            backdrop-filter: blur(10px);
            z-index: 250;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        .ar-modal-box {
            background: #111827;
            border: 1px solid #243247;
            box-shadow: 0 20px 48px rgba(0, 0, 0, 0.6), 0 0 24px rgba(168, 85, 247, 0.2);
            border-radius: 16px;
            width: 100%;
            max-width: 680px;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            animation: fadeInScale 0.25s cubic-bezier(0.16, 1, 0.3, 1);
        }
        @keyframes fadeInScale {
            from { opacity: 0; transform: scale(0.95); }
            to { opacity: 1; transform: scale(1); }
        }
        .ar-modal-header {
            background: linear-gradient(135deg, #182234, #131d2e);
            border-bottom: 1px solid #243247;
            padding: 18px 24px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        .ar-modal-title {
            font-size: 16px;
            font-weight: 700;
            color: #f8fafc;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .ar-modal-body {
            padding: 24px;
            display: flex;
            flex-direction: column;
            gap: 18px;
            max-height: 75vh;
            overflow-y: auto;
        }
        .ar-rule-card {
            background: #0d131f;
            border: 1px solid #1e293b;
            border-radius: 10px;
            padding: 14px 18px;
            font-size: 13px;
            line-height: 1.5;
            color: #cbd5e1;
        }
        .ar-rule-card strong { color: #a855f7; }
        .ar-rule-list {
            margin-top: 8px;
            padding-left: 20px;
            display: flex;
            flex-direction: column;
            gap: 6px;
            font-size: 12px;
            color: #94a3b8;
        }
        .ar-stat-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 12px;
            font-family: 'JetBrains Mono', monospace;
            margin-top: 10px;
        }
        .ar-stat-table th, .ar-stat-table td {
            padding: 8px 12px;
            text-align: left;
            border-bottom: 1px solid #1e293b;
        }
        .ar-stat-table th {
            color: #94a3b8;
            font-weight: 600;
            background: #0f172a;
        }
        .ar-stat-table td { color: #f8fafc; }
        .ar-modal-footer {
            background: #0f172a;
            border-top: 1px solid #243247;
            padding: 16px 24px;
            display: flex;
            justify-content: flex-end;
            gap: 12px;
        }

        /* Pagination Bar */
        .pagination-bar {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 16px;
            margin-top: 28px;
            padding: 16px;
            background: var(--bg-surface);
            border-radius: 10px;
            border: 1px solid var(--border-subtle);
        }

        /* Modal Lightbox */
        #lightbox {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.88);
            backdrop-filter: blur(8px);
            z-index: 200;
            align-items: center;
            justify-content: center;
            flex-direction: column;
            padding: 24px;
        }
        #lightbox img {
            max-width: 90vw;
            max-height: 82vh;
            border-radius: 8px;
            border: 1px solid var(--border-hover);
            box-shadow: 0 0 32px rgba(56, 189, 248, 0.3);
        }
        #lightbox-caption {
            margin-top: 14px;
            font-size: 13px;
            font-family: 'JetBrains Mono', monospace;
            color: #f8fafc;
            background: #182234;
            padding: 6px 16px;
            border-radius: 6px;
        }

        /* Computation Progress Banner */
        .comp-banner {
            background: linear-gradient(135deg, rgba(13, 27, 42, 0.98), rgba(19, 34, 56, 0.98));
            backdrop-filter: blur(16px);
            border-bottom: 2px solid var(--accent-primary);
            box-shadow: 0 8px 32px rgba(56, 189, 248, 0.15);
            padding: 16px 32px;
            display: flex;
            flex-direction: column;
            gap: 10px;
            position: sticky;
            top: 69px;
            z-index: 45;
            animation: fadeInDown 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        }
        @keyframes fadeInDown {
            from { opacity: 0; transform: translateY(-10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .comp-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        .comp-title {
            display: flex;
            align-items: center;
            gap: 10px;
            font-size: 14px;
            font-weight: 700;
            color: #f8fafc;
        }
        .pulse-indicator {
            width: 10px;
            height: 10px;
            border-radius: 50%;
            background: var(--accent-primary);
            box-shadow: 0 0 10px var(--accent-primary);
            animation: pulseGlow 1.2s infinite alternate;
        }
        .pulse-indicator.done {
            background: var(--accent-green);
            box-shadow: 0 0 10px var(--accent-green);
            animation: none;
        }
        .pulse-indicator.error {
            background: var(--accent-red);
            box-shadow: 0 0 10px var(--accent-red);
            animation: none;
        }
        @keyframes pulseGlow {
            from { transform: scale(0.9); opacity: 0.6; }
            to { transform: scale(1.3); opacity: 1; }
        }
        .comp-meta {
            display: flex;
            align-items: center;
            gap: 14px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 13px;
        }
        .comp-pct {
            color: var(--accent-primary);
            font-weight: 800;
            font-size: 15px;
        }
        .progress-track {
            width: 100%;
            height: 8px;
            background: rgba(15, 23, 42, 0.8);
            border-radius: 9999px;
            overflow: hidden;
            border: 1px solid var(--border-subtle);
        }
        .progress-fill {
            height: 100%;
            width: 0%;
            background: linear-gradient(90deg, #0284c7, #38bdf8, #22c55e);
            border-radius: 9999px;
            transition: width 0.35s ease;
            box-shadow: 0 0 12px rgba(56, 189, 248, 0.6);
        }
        .progress-fill.done {
            background: linear-gradient(90deg, #16a34a, #22c55e);
        }
        .progress-fill.error {
            background: linear-gradient(90deg, #dc2626, #ef4444);
        }
        .comp-msg {
            font-size: 12px;
            color: #94a3b8;
            font-family: 'JetBrains Mono', monospace;
        }

        /* Scan Control Bar in Issues View */
        .scan-bar {
            background: #0f172a;
            border-bottom: 1px solid var(--border-subtle);
            padding: 12px 32px;
            display: flex;
            align-items: center;
            gap: 16px;
            flex-wrap: wrap;
        }
        .scan-group {
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .scan-label {
            font-size: 12px;
            font-weight: 700;
            color: var(--accent-primary);
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        .btn-scan-run {
            background: linear-gradient(135deg, #0284c7, #0284c7 40%, #0369a1);
            color: #fff;
            font-size: 13px;
            font-weight: 700;
            padding: 8px 18px;
            border-radius: 8px;
            cursor: pointer;
            border: 1px solid #38bdf866;
            box-shadow: 0 0 16px rgba(2, 132, 199, 0.4);
            transition: all 0.2s ease;
            display: inline-flex;
            align-items: center;
            gap: 8px;
        }
        .btn-scan-run:hover {
            background: linear-gradient(135deg, #0369a1, #0284c7);
            transform: translateY(-1px);
            box-shadow: 0 0 22px rgba(56, 189, 248, 0.6);
        }
        .btn-scan-run:disabled {
            opacity: 0.5;
            cursor: not-allowed;
            transform: none;
            box-shadow: none;
        }
        .badge-background_blur {
            background: #14b8a626;
            color: #2dd4bf;
            border: 1px solid #14b8a64d;
        }
    </style>
</head>
<body>
    <header>
        <div class="brand">
            <div class="brand-icon">🍃</div>
            <div>
                <h1>Foliar Pathology Data Quality Studio</h1>
                <p>Interactive Screening, Side-by-Side Twins & Zero-Leakage Quarantine</p>
            </div>
        </div>

        <div class="nav-tabs">
            <button id="tab-btn-issues" class="nav-tab-btn active" onclick="switchView('issues')">
                ⚡ Automated AI Quality Issues
            </button>
            <button id="tab-btn-inspector" class="nav-tab-btn" onclick="switchView('inspector')">
                🔍 Class Split Explorer & Manual Quarantine
            </button>
        </div>

        <div style="display: flex; align-items: center; gap: 14px;">
            <button id="btn-open-pipeline" class="btn btn-pipeline" onclick="openPipelineModal()">
                🤖 Run Auto Screening & Automatic Deletion
            </button>
            <div class="stats-badge">
                <span id="badge-label">Flagged Issues:</span> <span id="badge-count">0</span>
            </div>
        </div>
    </header>

    <!-- REAL-TIME COMPUTATION PROGRESS BANNER -->
    <div id="computation-banner" class="comp-banner" style="display: none;">
        <div class="comp-header">
            <div class="comp-title">
                <div id="pulse-dot" class="pulse-indicator"></div>
                <span id="comp-stage">CleanVision Quality Screening</span>
            </div>
            <div class="comp-meta">
                <span id="comp-timer">⏱️ 0.0s</span>
                <span id="comp-pct" class="comp-pct">0%</span>
                <button id="btn-cancel-scan" onclick="cancelCurrentScan()" class="btn btn-quarantine" style="padding: 4px 10px; font-size: 11px; margin: 0 6px; display: inline-flex; align-items: center; gap: 4px; border-radius: 6px;">🛑 Stop Scan</button>
                <button onclick="dismissBanner()" style="background:transparent; border:none; color:#64748b; font-size:16px; cursor:pointer; padding:0 6px;" title="Dismiss banner">✕</button>
            </div>
        </div>
        <div class="progress-track">
            <div id="progress-fill" class="progress-fill" style="width: 0%;"></div>
        </div>
        <div class="comp-msg" id="comp-message">Preparing candidate images...</div>
    </div>

    <!-- VIEW 1: AUTOMATED AI ISSUES -->
    <div id="view-issues">
        <!-- Unified Quality Control & Navigation Bar -->
        <div class="toolbar" style="justify-content: space-between; gap: 14px; padding: 12px 32px;">
            <div style="display: flex; align-items: center; gap: 12px; flex-wrap: wrap;">
                <div class="scan-group">
                    <label class="scan-label">Target Class:</label>
                    <select id="scan-class-select" class="custom-select" onchange="onScanClassChange()" style="min-width: 250px; max-width: 350px;">
                        <option value="">All Dataset Classes</option>
                    </select>
                    <button class="btn btn-keep" id="btn-jump-inspector" onclick="goToManualInspector(document.getElementById('scan-class-select').value)" title="Open this class in Manual Inspector" style="display: none; padding: 7px 12px; font-size: 12px; align-items: center; gap: 4px;">
                        🔍 Inspect Class Images
                    </button>
                </div>

                <div style="display: flex; gap: 6px; flex-wrap: wrap;">
                    <button class="filter-btn active" onclick="setFilter('all', this)">All Flagged Issues</button>
                    <button class="filter-btn" onclick="setFilter('severe_blur', this)">🌫️ Severe Blur</button>
                    <button class="filter-btn" onclick="setFilter('background_blur', this)">🍃 Background Blur (Safe)</button>
                    <button class="filter-btn" onclick="setFilter('near_duplicate', this)">👯 Near-Duplicates</button>
                    <button class="filter-btn" onclick="setFilter('cross_split_leakage', this)">🚨 Cross-Split Leakage</button>
                    <button class="filter-btn" onclick="setFilter('semantic_outlier', this)">🎯 Outliers</button>
                </div>
            </div>

            <div style="display: flex; align-items: center; gap: 10px; flex-wrap: nowrap;">
                <select id="scan-max-select" class="custom-select" style="width: 100px; padding: 7px 10px; font-size: 12px;">
                    <option value="25">25 imgs</option>
                    <option value="50" selected>50 imgs</option>
                    <option value="100">100 imgs</option>
                    <option value="250">250 imgs</option>
                    <option value="0">All imgs</option>
                </select>
                <button id="btn-run-scan" class="btn-scan-run" onclick="triggerScanFromBar()" style="white-space: nowrap;">
                    ⚡ Scan All Issues
                </button>
                <button id="btn-auto-resolve-issues" class="btn btn-auto-resolve" onclick="openAutoResolveModal('issues')" style="white-space: nowrap;">
                    ⚡ Auto-Resolve Studio
                </button>
                <button id="btn-quick-commit-queue" class="btn btn-quarantine" onclick="quickCleanAllMappedTwins()" style="white-space: nowrap; font-weight: 700; background: linear-gradient(135deg, #b91c1c, #ef4444); border: 1px solid #f8717166;" title="Clean & quarantine all displayed twins in 0 seconds using the pre-computed dry-run mappings directly">
                    🧹 Clean Displayed Twins Now
                </button>
            </div>
        </div>

        <main>
            <div id="issue-grid" class="issue-grid">
                <!-- AI cards rendered dynamically -->
            </div>
        </main>
    </div>

    <!-- VIEW 2: CLASS SPLIT EXPLORER & MANUAL QUARANTINE -->
    <div id="view-inspector" style="display: none;">
        <div class="inspector-bar">
            <div class="selector-group">
                <label style="font-size: 13px; font-weight: 700; color: var(--accent-primary);">Target Foliar Class:</label>
                <input type="text" id="class-filter-input" class="search-input" placeholder="Search class (e.g. Rice, Tomato)..." oninput="filterClassDropdown()">
                <select id="class-dropdown" class="custom-select" onchange="onClassChange()" style="min-width: 280px; max-width: 420px;">
                    <option value="">Loading classes...</option>
                </select>
                <button class="btn btn-primary" onclick="scanCurrentInspectorClass()" style="white-space: nowrap;">
                    ⚡ Scan This Class
                </button>
                <button id="btn-auto-resolve-class" class="btn btn-auto-resolve" onclick="openAutoResolveModal('class')" style="white-space: nowrap;">
                    ⚡ Auto-Dedup & Anti-Leakage
                </button>
            </div>

            <!-- Split Selector Pills -->
            <div class="split-pill-group">
                <button class="split-pill active" id="pill-train" onclick="setSplit('train')">
                    Train <span id="count-train">0</span>
                </button>
                <button class="split-pill" id="pill-val" onclick="setSplit('val')">
                    Val <span id="count-val">0</span>
                </button>
                <button class="split-pill" id="pill-test" onclick="setSplit('test')">
                    Test <span id="count-test">0</span>
                </button>
            </div>
        </div>

        <!-- Batch Action Bar -->
        <div class="batch-bar">
            <div class="batch-info">
                <span>Marked for Quarantine: <strong id="selected-count">0</strong> images</span>
                <button class="btn btn-keep" onclick="selectAllOnPage()">Select All on Page</button>
                <button class="btn btn-keep" onclick="deselectAll()">Deselect All</button>
            </div>

            <div class="batch-controls">
                <label style="font-size: 12px; color: var(--text-muted); font-weight: 600;">Reason:</label>
                <select id="batch-reason-select" class="custom-select" style="padding: 6px 12px; font-size: 12px;">
                    <option value="manual_inspection">📋 Manual Inspection Outlier</option>
                    <option value="motion_blur">🌫️ Motion Blur / Severe Defocus</option>
                    <option value="background_blur">🍃 Background Blur (Defocus / Bokeh)</option>
                    <option value="near_duplicate">👯 Near-Duplicate / Burst Twin</option>
                    <option value="cross_split_leakage">🚨 Cross-Split Leakage</option>
                    <option value="watermark_or_text">🏷️ Watermark / Stamp / Border</option>
                    <option value="non_foliar">🍂 Non-Leaf / Heavy Clutter</option>
                    <option value="mislabeled_disease">⚠️ Mislabeled Disease Pathology</option>
                </select>

                <button class="btn btn-quarantine" onclick="quarantineMarkedBatch()">
                    🚨 Quarantine Selected (<span id="btn-selected-count">0</span>)
                </button>
            </div>
        </div>

        <main>
            <div id="class-image-grid" class="class-image-grid">
                <!-- Class image thumbnails rendered dynamically -->
            </div>

            <div class="pagination-bar" id="pagination-controls">
                <button class="btn btn-keep" id="btn-prev-page" onclick="changePage(-1)">◀ Prev Page</button>
                <span id="page-indicator" style="font-size: 13px; font-family: 'JetBrains Mono', monospace;">Page 1 of 1</span>
                <button class="btn btn-keep" id="btn-next-page" onclick="changePage(1)">Next Page ▶</button>
            </div>
        </main>
    </div>

    <!-- Full-resolution Lightbox -->
    <div id="lightbox" onclick="closeLightbox()">
        <img id="lightbox-img" src="" onclick="event.stopPropagation()">
        <div id="lightbox-caption" onclick="event.stopPropagation()"></div>
    </div>

    <!-- Auto-Resolve Duplicates & Anti-Leakage Modal -->
    <div id="auto-resolve-modal" onclick="closeAutoResolveModal()">
        <div class="ar-modal-box" onclick="event.stopPropagation()">
            <div class="ar-modal-header">
                <div class="ar-modal-title">
                    <span>⚡</span>
                    <span id="ar-modal-header-text">Automated De-Duplication & Anti-Leakage Studio</span>
                </div>
                <button onclick="closeAutoResolveModal()" style="background:transparent; border:none; color:#94a3b8; font-size:18px; cursor:pointer;" title="Close">✕</button>
            </div>
            <div class="ar-modal-body">
                <div class="ar-rule-card">
                    <strong>🛡️ Enforced Anti-Leakage & Dedup Logic:</strong>
                    <div class="ar-rule-list">
                        <div>• <strong>Cross-Split Leakage (Train vs Eval):</strong> If copies exist in Train and Val/Test, all copies in <strong>Train are safely purged</strong> (protects eval integrity).</div>
                        <div>• <strong>Multiple Train Duplicates + Leakage:</strong> If Train has internal duplicates AND leaks to Val/Test, <strong>all Train duplicates are safely removed</strong>.</div>
                        <div>• <strong>Val vs Test Twins:</strong> 1 copy is randomly retained in Val or Test, and the twin copy is quarantined.</div>
                        <div>• <strong>Internal Split Duplicates:</strong> 1 unique specimen is kept randomly, redundant copies are quarantined.</div>
                    </div>
                </div>

                <div style="display:flex; flex-direction:column; gap:8px;">
                    <label style="font-size:12px; font-weight:700; color:var(--accent-primary); text-transform:uppercase;">Operation Mode & Target:</label>
                    <div style="display:flex; gap:16px; align-items:center; flex-wrap:wrap;">
                        <label style="display:flex; align-items:center; gap:6px; font-size:13px; cursor:pointer;">
                            <input type="radio" name="ar-source-radio" value="issues" checked onchange="onArSourceChange()">
                            Resolve Flagged Queue Issues
                        </label>
                        <label style="display:flex; align-items:center; gap:6px; font-size:13px; cursor:pointer;">
                            <input type="radio" name="ar-source-radio" value="class_scan" onchange="onArSourceChange()">
                            Deep Direct Scan on Target Class
                        </label>
                    </div>
                </div>

                <div id="ar-class-target-group" style="display:flex; flex-direction:column; gap:6px;">
                    <label style="font-size:12px; color:var(--text-muted); font-weight:600;">Target Class:</label>
                    <select id="ar-class-select" class="custom-select" style="width:100%; max-width:100%;">
                        <option value="">All Flagged Classes (Queue Mode Only)</option>
                    </select>
                </div>

                <!-- Progress / Status Area -->
                <div id="ar-status-area" style="display:none; padding:12px 16px; background:#0f172a; border-radius:8px; border:1px solid #1e293b; font-size:13px; font-family:'JetBrains Mono', monospace;">
                    <div style="display:flex; align-items:center; gap:10px;">
                        <div id="ar-spinner" class="pulse-indicator"></div>
                        <span id="ar-status-text">Processing duplicate clusters...</span>
                    </div>
                </div>

                <!-- Results Area -->
                <div id="ar-results-area" style="display:none;">
                    <div style="font-size:13px; font-weight:700; color:#22c55e; margin-bottom:8px;" id="ar-results-summary">
                        ✅ Resolution Complete
                    </div>
                    <div id="ar-results-table-container"></div>
                </div>
            </div>
            <div class="ar-modal-footer">
                <button class="btn btn-keep" onclick="closeAutoResolveModal()">Cancel / Close</button>
                <button id="btn-execute-ar" class="btn btn-auto-resolve" onclick="executeAutoResolveFromModal()">
                    ⚡ Execute Auto-Resolve
                </button>
            </div>
        </div>
    </div>

    <!-- 🤖 SEQUENTIAL PIPELINE MODAL (ONE-BY-ONE AUTO SCREENING & CLEANING) -->
    <div id="pipeline-modal">
        <div class="ar-modal-card" style="max-width: 680px;">
            <div class="ar-modal-header" style="background: linear-gradient(135deg, #064e3b, #065f46); border-bottom: 1px solid #05966966;">
                <div>
                    <h3 style="font-size: 16px; font-weight: 800; color: #6ee7b7; display: flex; align-items: center; gap: 8px;">
                        🤖 Autonomous Class-by-Class Screening & Cleaning Pipeline
                    </h3>
                    <p style="font-size: 12px; color: #a7f3d0; margin-top: 3px;">
                        Sequentially screens every class one-by-one, resolves duplicates, purges train leakage, and updates dataset splits live.
                    </p>
                </div>
                <button class="btn-modal-close" onclick="closePipelineModal()">✕</button>
            </div>

            <div class="ar-modal-body" style="padding: 20px; display: flex; flex-direction: column; gap: 16px;">
                <!-- Pipeline Config Form (visible when idle / stopped / completed) -->
                <div id="pipeline-config-area">
                    <!-- Dynamic Notification / Previous Run Status Banner -->
                    <div id="pipeline-config-banner" style="display: none; background: #064e3b33; border: 1px solid #05966966; border-radius: 8px; padding: 12px 14px; margin-bottom: 14px; color: #6ee7b7; font-size: 12px;">
                        <div style="display: flex; justify-content: space-between; align-items: center; gap: 10px; flex-wrap: wrap;">
                            <span id="pipeline-config-banner-text">✅ Previous pipeline run completed successfully.</span>
                            <button id="btn-banner-view-twins" class="btn btn-primary" onclick="viewMappedTwinsInGrid()" style="padding: 5px 12px; font-size: 11px; display: none;">
                                👀 View Mapped Twins
                            </button>
                        </div>
                    </div>

                    <div class="ar-rule-box" style="background: #064e3b22; border-color: #05966955; margin-bottom: 14px;">
                        <div style="font-weight: 700; color: #34d399; margin-bottom: 6px; font-size: 12px;">
                            📋 Strict Automated Decision Rules Applied:
                        </div>
                        <ul style="margin: 0; padding-left: 18px; font-size: 11px; color: #cbd5e1; line-height: 1.5;">
                            <li><strong>Cross-Split Leakage with Train:</strong> Safely purges ALL copies from Train (including any internal duplicates in Train) to guarantee pure, uncompromised test & validation sets.</li>
                            <li><strong>Leakage between Val and Test:</strong> Randomly keeps 1 copy, quarantines others to prevent split contamination.</li>
                            <li><strong>Within-Split Redundancy:</strong> Keeps 1 unique exemplar, quarantines redundant near-identical copies.</li>
                            <li><strong>Zero Data Loss:</strong> Quarantined files are safely moved to <code>data/raw/quarantine_data_quality/</code> with an audit trail.</li>
                        </ul>
                    </div>

                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px;">
                        <div>
                            <label style="font-size: 12px; font-weight: 700; color: var(--text-main); display: block; margin-bottom: 6px;">
                                Scope / Crop Filter:
                            </label>
                            <select id="pipeline-crop-select" class="custom-select" style="width: 100%;">
                                <option value="">🌍 Entire Dataset (All 201 Classes)</option>
                                <option value="Chilli">🌶️ Chilli</option>
                                <option value="Tomato">🍅 Tomato</option>
                                <option value="Potato">🥔 Potato</option>
                                <option value="Rice">🌾 Rice</option>
                                <option value="Wheat">🌾 Wheat</option>
                                <option value="Corn">🌽 Corn (Maize)</option>
                                <option value="Apple">🍎 Apple</option>
                                <option value="Grape">🍇 Grape</option>
                                <option value="Blueberry">🫐 Blueberry</option>
                                <option value="Cauliflower">🥦 Cauliflower</option>
                                <option value="Strawberry">🍓 Strawberry</option>
                                <option value="Peach">🍑 Peach</option>
                                <option value="Cotton">🌱 Cotton</option>
                            </select>
                        </div>
                        <div>
                            <label style="font-size: 12px; font-weight: 700; color: var(--text-main); display: block; margin-bottom: 6px;">
                                Execution Mode:
                            </label>
                            <select id="pipeline-mode-select" class="custom-select" style="width: 100%;">
                                <option value="live">⚡ Live Commit (Auto Quarantine)</option>
                                <option value="dry_run">🔍 Dry Run (Screening Audit Only)</option>
                            </select>
                        </div>
                    </div>

                    <div style="margin-top: 14px;">
                        <label style="font-size: 12px; font-weight: 700; color: var(--text-main); display: block; margin-bottom: 6px;">
                            Matching Algorithm Strategy:
                        </label>
                        <select id="pipeline-matching-mode" class="custom-select" style="width: 100%;">
                            <option value="cluster" selected>🌐 Standard Cluster Matching (Transitive — Proven for Foliar Crops)</option>
                            <option value="direct_pairwise">🎯 Direct Pairwise Matching (Strict 1-to-1 Rotated/Flipped — Recommended for Ginger & Paddy)</option>
                        </select>
                        <div style="font-size: 11px; color: var(--text-muted); margin-top: 4px; line-height: 1.4;">
                            Direct Pairwise evaluates strict 1-to-1 rotated (90°/180°/270°), flipped, and exact twins without transitive chaining, preventing unrelated studio leaves from being grouped together.
                        </div>
                    </div>
                </div>

                <!-- Live Progress Tracking Area (visible when running/completed) -->
                <div id="pipeline-live-area" style="display: none; flex-direction: column; gap: 14px;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <span id="pipeline-status-badge" style="font-size: 11px; font-weight: 700; padding: 3px 8px; border-radius: 4px; background: #05966933; color: #34d399; border: 1px solid #05966966;">
                                RUNNING
                            </span>
                            <span id="pipeline-timer" style="font-size: 12px; color: var(--text-muted); margin-left: 8px;">⏱️ 0.0s</span>
                        </div>
                        <div id="pipeline-progress-text" style="font-size: 13px; font-weight: 700; color: var(--accent-primary);">
                            Class 0 / 201 (0%)
                        </div>
                    </div>

                    <div class="progress-track" style="height: 10px;">
                        <div id="pipeline-progress-bar" class="progress-fill" style="width: 0%; background: linear-gradient(90deg, #059669, #34d399);"></div>
                    </div>

                    <div style="display: flex; align-items: center; gap: 8px; font-size: 13px; color: #e2e8f0;">
                        <span>Currently Processing:</span>
                        <strong id="pipeline-current-class" style="color: #6ee7b7; font-family: 'JetBrains Mono', monospace;">-</strong>
                    </div>

                    <!-- Live KPI Cards -->
                    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px;">
                        <div style="background: #0d1522; border: 1px solid #1e293b; border-radius: 8px; padding: 10px; text-align: center;">
                            <div style="font-size: 11px; color: var(--text-muted);">Total Quarantined</div>
                            <div id="pipeline-stat-quarantined" style="font-size: 18px; font-weight: 800; color: #ef4444; margin-top: 4px;">0</div>
                        </div>
                        <div style="background: #0d1522; border: 1px solid #1e293b; border-radius: 8px; padding: 10px; text-align: center;">
                            <div style="font-size: 11px; color: var(--text-muted);">Train Leaks Purged</div>
                            <div id="pipeline-stat-train" style="font-size: 18px; font-weight: 800; color: #f59e0b; margin-top: 4px;">0</div>
                        </div>
                        <div style="background: #0d1522; border: 1px solid #1e293b; border-radius: 8px; padding: 10px; text-align: center;">
                            <div style="font-size: 11px; color: var(--text-muted);">Classes with Issues</div>
                            <div id="pipeline-stat-classes-issues" style="font-size: 18px; font-weight: 800; color: #38bdf8; margin-top: 4px;">0</div>
                        </div>
                    </div>

                    <!-- Live Terminal Log Box -->
                    <div>
                        <div style="font-size: 11px; font-weight: 700; color: var(--text-muted); margin-bottom: 6px;">Live Execution Log:</div>
                        <div id="pipeline-live-logs" class="live-log-box">
                            <div style="color: #64748b;">Ready to begin sequential screening pipeline...</div>
                        </div>
                    </div>

                    <!-- View Side-by-Side Twins in Grid Action Button -->
                    <div id="pipeline-view-twins-box" style="display: none; margin-top: 4px;">
                        <button id="btn-view-twins" class="btn btn-primary" onclick="viewMappedTwinsInGrid()" style="width: 100%; justify-content: center; padding: 11px 16px; font-size: 13px; font-weight: 700; background: linear-gradient(135deg, #0284c7, #38bdf8); border: none; box-shadow: 0 0 16px rgba(56, 189, 248, 0.4);">
                            👀 View Mapped Side-by-Side Twins in Dashboard Grid
                        </button>
                    </div>
                </div>
            </div>

            <div class="ar-modal-footer" style="justify-content: space-between;">
                <div>
                    <button id="btn-pipeline-cancel" class="btn btn-quarantine" onclick="cancelPipeline()" style="display: none;">
                        🛑 Stop Pipeline
                    </button>
                </div>
                <div style="display: flex; gap: 8px;">
                    <button class="btn btn-keep" onclick="closePipelineModal()">Close</button>
                    <button id="btn-pipeline-start" class="btn btn-pipeline" onclick="startSequentialPipeline()">
                        🚀 Start Auto Screening & Deletion
                    </button>
                </div>
            </div>
        </div>
    </div>

    <div id="toast"></div>

    <script>
        // Global State
        let currentView = 'issues';
        let allIssues = [];
        let currentFilter = 'all';

        let allClasses = [];
        let selectedClass = '';
        let currentSplit = 'train';
        let currentPage = 1;
        let totalPages = 1;
        let selectedPaths = new Set();
        let currentClassImages = [];

        // View Switcher
        function switchView(view) {
            currentView = view;
            const tabIssues = document.getElementById('tab-btn-issues');
            const tabInspector = document.getElementById('tab-btn-inspector');
            if (tabIssues) tabIssues.classList.toggle('active', view === 'issues');
            if (tabInspector) tabInspector.classList.toggle('active', view === 'inspector');

            const viewIssues = document.getElementById('view-issues');
            const viewInspector = document.getElementById('view-inspector');
            if (viewIssues) viewIssues.style.display = view === 'issues' ? 'block' : 'none';
            if (viewInspector) viewInspector.style.display = view === 'inspector' ? 'block' : 'none';

            if (view === 'issues') {
                const label = document.getElementById('badge-label');
                if (label) label.innerText = 'Flagged Issues:';
                renderIssues();
            } else {
                const label = document.getElementById('badge-label');
                if (label) label.innerText = 'Class Images:';
                updateInspectorBadge();
                if (selectedClass && currentClassImages.length === 0) {
                    loadClassImages();
                }
            }
        }

        function updateInspectorBadge() {
            const cls = allClasses.find(c => c.class_name === selectedClass);
            if (cls) {
                const cnt = currentSplit === 'train' ? cls.train_count : (currentSplit === 'val' ? cls.val_count : cls.test_count);
                const badge = document.getElementById('badge-count');
                if (badge) badge.innerText = cnt;
            } else {
                const badge = document.getElementById('badge-count');
                if (badge) badge.innerText = '0';
            }
        }

        // --- AUTOMATED ISSUES LOGIC ---
        async function loadIssues() {
            try {
                const res = await fetch('/api/issues?t=' + Date.now());
                const data = await res.json();
                allIssues = data.issues || [];
                renderIssues();
            } catch (err) {
                console.error('Failed to load issues', err);
            }
        }

        function onScanClassChange() {
            const val = document.getElementById('scan-class-select') ? document.getElementById('scan-class-select').value : '';
            if (val) {
                selectedClass = val;
                const classDd = document.getElementById('class-dropdown');
                if (classDd) classDd.value = val;
                updateSplitCounts();
            }
            updateScanButtonText();
            renderIssues();
        }

        function updateScanButtonText() {
            const val = document.getElementById('scan-class-select') ? document.getElementById('scan-class-select').value : '';
            const btn = document.getElementById('btn-run-scan');
            if (btn) {
                if (val) {
                    btn.innerHTML = `⚡ Scan "${val.split(' - ').pop()}"`;
                } else {
                    btn.innerHTML = '⚡ Scan All Issues';
                }
            }
            const jumpBtn = document.getElementById('btn-jump-inspector');
            if (jumpBtn) {
                jumpBtn.style.display = val ? 'inline-flex' : 'none';
            }
        }

        function toPosix(p) {
            return p ? String(p).split('\\\\').join('/') : '';
        }

        function goToManualInspector() {
            const val = document.getElementById('scan-class-select') ? document.getElementById('scan-class-select').value : '';
            if (val) {
                selectedClass = val;
                const dd = document.getElementById('class-dropdown');
                if (dd) dd.value = val;
                updateSplitCounts();
                currentPage = 1;
                loadClassImages();
            }
            switchView('inspector');
        }

        async function triggerScanForSelectedClass() {
            const val = document.getElementById('scan-class-select') ? document.getElementById('scan-class-select').value : '';
            const maxImages = parseInt(document.getElementById('scan-max-select').value) || 50;
            await startScanJob(val, null, maxImages);
        }

        function setFilter(type, btn) {
            currentFilter = type;
            document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
            if (btn) btn.classList.add('active');
            updateScanButtonText();
            renderIssues();
        }

        function renderIssues() {
            const grid = document.getElementById('issue-grid');
            if (!grid) return;
            grid.innerHTML = '';

            const targetClassFilter = document.getElementById('scan-class-select') ? document.getElementById('scan-class-select').value : '';

            let filtered = allIssues || [];

            if (targetClassFilter) {
                const normFilter = targetClassFilter.toLowerCase().trim();
                filtered = filtered.filter(it => {
                    const c1 = (it.primary_image && it.primary_image.class || '').toLowerCase().trim();
                    const c2 = (it.secondary_image && it.secondary_image.class || '').toLowerCase().trim();
                    return c1 === normFilter || c2 === normFilter || (c1 && normFilter.includes(c1)) || (c2 && normFilter.includes(c2));
                });
            }

            const classIssueCount = filtered.length;

            if (currentFilter !== 'all') {
                filtered = filtered.filter(it => it.type === currentFilter);
            }

            if (currentView === 'issues') {
                const countBadge = document.getElementById('badge-count');
                if (countBadge) countBadge.innerText = filtered.length;
            }

            if (filtered.length === 0) {
                if (classIssueCount > 0 && currentFilter !== 'all') {
                    const typesPresent = Array.from(new Set(allIssues.map(it => it.type))).join(', ');
                    grid.innerHTML = `
                    <div style="grid-column: 1/-1; text-align:center; padding:50px 24px; color:#94a3b8; background:#111827; border-radius:12px; border:1px solid #243247; max-width:680px; margin:30px auto;">
                        <div style="font-size:36px; margin-bottom:12px;">🔍</div>
                        <h3 style="font-size:17px; color:#f8fafc; font-weight:700; margin-bottom:8px;">${classIssueCount} issue(s) found in other categories</h3>
                        <p style="font-size:13px; color:#94a3b8; margin-bottom:20px; line-height:1.5;">The active filter (<strong>${currentFilter}</strong>) has 0 defects, but this class has issues categorized under: <strong>${typesPresent}</strong>.</p>
                        <button class="btn btn-primary" onclick="setFilter('all', document.querySelector('.filter-btn'))">👀 Show All ${classIssueCount} Issues</button>
                    </div>`;
                } else if (targetClassFilter) {
                    grid.innerHTML = `
                    <div style="grid-column: 1/-1; text-align:center; padding:50px 24px; color:#94a3b8; background:#111827; border-radius:12px; border:1px solid #243247; max-width:680px; margin:30px auto;">
                        <div style="font-size:36px; margin-bottom:12px;">🌿</div>
                        <h3 style="font-size:17px; color:#f8fafc; font-weight:700; margin-bottom:8px;">No flagged issues found for "${targetClassFilter}"</h3>
                        <p style="font-size:13px; color:#64748b; margin-bottom:20px; line-height:1.5;">This class has either not been scanned yet or has 0 detected quality defects in this filter.</p>
                        <div style="display:flex; justify-content:center; gap:12px; flex-wrap:wrap;">
                            <button class="btn btn-primary" onclick="triggerScanForSelectedClass()">⚡ Scan This Class Now</button>
                            <button class="btn btn-keep" onclick="goToManualInspector()">🔍 Open in Manual Inspector</button>
                        </div>
                    </div>`;
                } else {
                    grid.innerHTML = '<div style="grid-column: 1/-1; text-align:center; padding:60px; color:#64748b;">✅ No flagged issues found in this category!</div>';
                }
                return;
            }

            filtered.forEach((it, idx) => {
                const cardId = `card-${idx}`;
                it._cardId = cardId;
                const isPair = Boolean(it.secondary_image);

                const card = document.createElement('div');
                card.id = cardId;
                card.className = 'card';

                let imageHtml = '';
                let actionsHtml = '';

                if (isPair) {
                    const p1 = it.primary_image || {};
                    const p2 = it.secondary_image || {};
                    const p1Path = toPosix(p1.path);
                    const p2Path = toPosix(p2.path);

                    imageHtml = `
                    <div class="image-pair-container">
                        <div class="img-box" onclick="openLightbox('/api/image?path=${encodeURIComponent(p1Path)}', '${p1.class || ''} [${(p1.split || '').toUpperCase()}] ${p1.filename || ''}')">
                            <img src="/api/image?path=${encodeURIComponent(p1Path)}" loading="lazy">
                            <div class="img-meta">
                                <span class="meta-class">${p1.class || ''}</span>
                                <span class="meta-split">[Split: ${(p1.split || '').toUpperCase()}]</span>
                                <span class="meta-fn">${p1.filename || ''}</span>
                            </div>
                        </div>
                        <div class="img-box" onclick="openLightbox('/api/image?path=${encodeURIComponent(p2Path)}', '${p2.class || ''} [${(p2.split || '').toUpperCase()}] ${p2.filename || ''}')">
                            <img src="/api/image?path=${encodeURIComponent(p2Path)}" loading="lazy">
                            <div class="img-meta">
                                <span class="meta-class">${p2.class || ''}</span>
                                <span class="meta-split">[Split: ${(p2.split || '').toUpperCase()}]</span>
                                <span class="meta-fn">${p2.filename || ''}</span>
                            </div>
                        </div>
                    </div>
                    `;

                    actionsHtml = `
                    <button class="btn btn-keep" onclick="dismissIssue('${cardId}', '${p1Path}', '${p2Path}')">Keep Both</button>
                    ${(it.type === 'near_duplicate' || it.type === 'cross_split_leakage') ? `<button class="btn btn-auto-resolve" onclick="autoResolveCard('${cardId}', '${p1Path}', '${p2Path}')" title="Auto-purge train leakage, or randomly resolve val/test / within-split">⚡ Auto-Resolve</button>` : ''}
                    <button class="btn btn-quarantine-left" onclick="quarantineSingle('${cardId}', '${p1Path}', '${it.type}')">Quarantine Left</button>
                    <button class="btn btn-quarantine-right" onclick="quarantineSingle('${cardId}', '${p2Path}', '${it.type}')">Quarantine Right</button>
                    <button class="btn btn-quarantine" onclick="quarantineBoth('${cardId}', '${p1Path}', '${p2Path}', '${it.type}')">Quarantine Both</button>
                    `;
                } else {
                    const p = it.primary_image || {};
                    const pPath = toPosix(p.path);
                    imageHtml = `
                    <div class="image-single-container">
                        <div class="img-box" style="max-width: 320px; width: 100%;" onclick="openLightbox('/api/image?path=${encodeURIComponent(pPath)}', '${p.class || ''} [${(p.split || '').toUpperCase()}] ${p.filename || ''}')">
                            <img src="/api/image?path=${encodeURIComponent(pPath)}" loading="lazy">
                            <div class="img-meta">
                                <span class="meta-class">${p.class || ''}</span>
                                <span class="meta-split">[Split: ${(p.split || '').toUpperCase()}]</span>
                                <span class="meta-fn">${p.filename || ''}</span>
                            </div>
                        </div>
                    </div>
                    `;

                    actionsHtml = `
                    <button class="btn btn-keep" onclick="dismissIssue('${cardId}', '${pPath}', '')">Mark Clean / Keep</button>
                    <button class="btn btn-quarantine" onclick="quarantineSingle('${cardId}', '${pPath}', '${it.type}')">Quarantine Specimen</button>
                    `;
                }

                card.innerHTML = `
                    <div class="card-header">
                        <span class="badge-type badge-${it.type}">${it.type}</span>
                        <span style="font-size:12px; color:#38bdf8; font-family:'JetBrains Mono', monospace; font-weight:700;">
                            ${it.similarity > 0 ? (it.similarity * 100).toFixed(1) + '% Sim' : ''}
                        </span>
                    </div>
                    <div class="card-body">
                        <div class="card-title">${it.title}</div>
                        <div class="card-desc">${it.description}</div>
                        ${imageHtml}
                    </div>
                    <div class="card-actions">
                        ${actionsHtml}
                    </div>
                `;

                grid.appendChild(card);
            });
        }

        async function quarantineSingle(cardId, path, reason) {
            try {
                const cleanPath = toPosix(path);
                const res = await fetch('/api/quarantine', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ path: cleanPath, reason: reason })
                });
                const data = await res.json();
                if (data.status === 'success' || data.status === 'already_moved') {
                    const fname = cleanPath.split('/').pop();
                    showToast(`Quarantined: ${fname}`);
                    const el = document.getElementById(cardId);
                    if (el) el.remove();
                    allIssues = allIssues.filter(it => it._cardId !== cardId);
                    document.getElementById('badge-count').innerText = allIssues.length;
                } else {
                    showToast(`Quarantine note: ${data.message || data.status}`);
                }
            } catch (err) {
                alert('Quarantine failed: ' + err);
            }
        }

        async function quarantineBoth(cardId, p1Path, p2Path, reason) {
            try {
                const clean1 = toPosix(p1Path);
                const clean2 = toPosix(p2Path);
                const res = await fetch('/api/quarantine-batch', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ paths: [clean1, clean2], reason: reason })
                });
                const data = await res.json();
                if (data.status === 'success') {
                    showToast(`Quarantined pair successfully`);
                    const el = document.getElementById(cardId);
                    if (el) el.remove();
                    allIssues = allIssues.filter(it => it._cardId !== cardId);
                    document.getElementById('badge-count').innerText = allIssues.length;
                } else {
                    showToast(`Quarantine note: ${data.message || data.status}`);
                }
            } catch (err) {
                alert('Quarantine failed: ' + err);
            }
        }

        async function dismissIssue(cardId, p1Path, p2Path) {
            try {
                const el = document.getElementById(cardId);
                if (el) el.remove();
                allIssues = allIssues.filter(it => it._cardId !== cardId);
                document.getElementById('badge-count').innerText = allIssues.length;

                await fetch('/api/dismiss-issue', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        primary_path: toPosix(p1Path),
                        secondary_path: toPosix(p2Path)
                    })
                });
                showToast('Marked clean & kept');
            } catch (err) {
                console.error('Failed to dismiss issue:', err);
            }
        }

        // --- ⚡ AUTOMATED DE-DUPLICATION & ANTI-LEAKAGE STUDIO LOGIC ---
        async function autoResolveCard(cardId, p1Path, p2Path) {
            try {
                const res = await fetch('/api/auto-resolve-pair', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        primary_path: toPosix(p1Path),
                        secondary_path: toPosix(p2Path)
                    })
                });
                const data = await res.json();
                if (data.status === 'success' || data.status === 'already_resolved') {
                    showToast(`⚡ ${data.explanation || data.message || 'Auto-resolved pair'}`);
                    const el = document.getElementById(cardId);
                    if (el) el.remove();
                    allIssues = allIssues.filter(it => it._cardId !== cardId);
                    document.getElementById('badge-count').innerText = allIssues.length;
                    // Refresh class lists/counts in background
                    loadClasses();
                } else {
                    showToast(`Notice: ${data.detail || data.message || 'Auto-resolve notice'}`);
                }
            } catch (err) {
                alert('Auto-resolve failed: ' + err);
            }
        }

        async function quickCleanAllMappedTwins() {
            const queueTwins = (allIssues || []).filter(it => it.type === 'near_duplicate' || it.type === 'cross_split_leakage');
            if (queueTwins.length === 0) {
                showToast('No duplicate or leakage twins currently in queue to clean.');
                return;
            }
            const targetClass = document.getElementById('scan-class-select') ? document.getElementById('scan-class-select').value : '';
            const scopeLabel = targetClass ? `for class '${targetClass}'` : `across all ${queueTwins.length} displayed twins`;
            
            const confirmed = confirm(`⚡ Quick Clean (0s Recalculation):\n\nDo you want to clean & quarantine all ${queueTwins.length} mapped duplicate/leakage twins ${scopeLabel}?\n\nThis will execute the quarantine moves immediately using the current dry-run mappings directly without re-scanning or recalculating.`);
            if (!confirmed) return;

            showToast('🧹 Quarantining pre-mapped twins...');
            try {
                const res = await fetch('/api/auto-resolve-all', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        source: 'issues',
                        target_class: targetClass || null
                    })
                });
                const data = await res.json();
                if (data.status === 'success') {
                    showToast(`✅ Successfully cleaned & quarantined ${data.quarantined_count} images!`);
                    await loadClasses();
                    await loadIssues();
                } else {
                    showToast(data.message || 'Auto-resolve complete');
                    await loadClasses();
                    await loadIssues();
                }
            } catch (err) {
                alert('Clean failed: ' + err);
            }
        }

        function openAutoResolveModal(source) {
            const modal = document.getElementById('auto-resolve-modal');
            if (!modal) return;

            // Populate modal class dropdown
            const arSelect = document.getElementById('ar-class-select');
            if (arSelect) {
                arSelect.innerHTML = '<option value="">All Flagged Classes (Queue Mode Only)</option>';
                allClasses.forEach(c => {
                    const opt = document.createElement('option');
                    opt.value = c.class_name;
                    opt.innerText = `${c.class_name} (${c.total_count} imgs - Tr:${c.train_count}/V:${c.val_count}/Te:${c.test_count})`;
                    arSelect.appendChild(opt);
                });
            }

            // Set source radio
            const radios = document.getElementsByName('ar-source-radio');
            radios.forEach(r => {
                if (source === 'class' && r.value === 'class_scan') r.checked = true;
                if (source === 'issues' && r.value === 'issues') r.checked = true;
            });

            // If a class is selected in inspector or issues bar, pre-select it
            let targetCls = selectedClass;
            const scanSelect = document.getElementById('scan-class-select');
            if (currentView === 'issues' && scanSelect && scanSelect.value) {
                targetCls = scanSelect.value;
            }
            if (targetCls && arSelect) {
                arSelect.value = targetCls;
            }

            // Reset modal status and results
            document.getElementById('ar-status-area').style.display = 'none';
            document.getElementById('ar-results-area').style.display = 'none';
            document.getElementById('btn-execute-ar').disabled = false;
            onArSourceChange();

            modal.style.display = 'flex';
        }

        function closeAutoResolveModal() {
            const modal = document.getElementById('auto-resolve-modal');
            if (modal) modal.style.display = 'none';
        }

        function onArSourceChange() {
            const radios = document.getElementsByName('ar-source-radio');
            let sel = 'issues';
            radios.forEach(r => { if (r.checked) sel = r.value; });

            const arSelect = document.getElementById('ar-class-select');
            const btn = document.getElementById('btn-execute-ar');

            if (sel === 'class_scan') {
                if (arSelect && !arSelect.value && allClasses.length > 0) {
                    arSelect.value = selectedClass || allClasses[0].class_name;
                }
                btn.innerHTML = '⚡ Deep Scan & Dedup Target Class';
            } else {
                btn.innerHTML = '⚡ Auto-Resolve Flagged Queue';
            }
        }

        async function executeAutoResolveFromModal() {
            const radios = document.getElementsByName('ar-source-radio');
            let sel = 'issues';
            radios.forEach(r => { if (r.checked) sel = r.value; });

            const arSelect = document.getElementById('ar-class-select');
            const targetClass = arSelect ? arSelect.value : '';

            if (sel === 'class_scan' && !targetClass) {
                alert('Please select a target class for direct disk scan.');
                return;
            }

            const btn = document.getElementById('btn-execute-ar');
            btn.disabled = true;

            const statusArea = document.getElementById('ar-status-area');
            const statusText = document.getElementById('ar-status-text');
            const resultsArea = document.getElementById('ar-results-area');

            statusArea.style.display = 'block';
            resultsArea.style.display = 'none';
            statusText.innerText = sel === 'class_scan' ? `Deep scanning & deduping '${targetClass}'...` : 'Clustering and resolving duplicate queue...';

            try {
                const res = await fetch('/api/auto-resolve-all', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        source: sel,
                        target_class: targetClass || null
                    })
                });
                const data = await res.json();
                statusArea.style.display = 'none';

                if (data.status === 'success') {
                    resultsArea.style.display = 'block';
                    document.getElementById('ar-results-summary').innerHTML = `✅ ${data.message}`;

                    let tableHtml = `
                    <table class="ar-stat-table">
                        <tr><th>Metric</th><th>Count</th></tr>
                        <tr><td>Clusters Resolved</td><td><strong>${data.clusters_resolved}</strong></td></tr>
                        <tr><td>Total Images Quarantined</td><td style="color:#ef4444;"><strong>${data.quarantined_count}</strong></td></tr>
                    `;

                    if (data.quarantined_by_split) {
                        tableHtml += `
                        <tr><td>Quarantined from Train</td><td>${data.quarantined_by_split.train || 0} (cross-split leakage / redundancy)</td></tr>
                        <tr><td>Quarantined from Val</td><td>${data.quarantined_by_split.val || 0}</td></tr>
                        <tr><td>Quarantined from Test</td><td>${data.quarantined_by_split.test || 0}</td></tr>
                        `;
                    }

                    if (data.before && data.after) {
                        tableHtml += `
                        <tr><th colspan="2" style="background:#131d2e; color:#38bdf8;">Split Distribution Update</th></tr>
                        <tr><td>Train Split</td><td>${data.before.train} &rarr; <strong>${data.after.train}</strong> images</td></tr>
                        <tr><td>Val Split</td><td>${data.before.val} &rarr; <strong>${data.after.val}</strong> images</td></tr>
                        <tr><td>Test Split</td><td>${data.before.test} &rarr; <strong>${data.after.test}</strong> images</td></tr>
                        `;
                    }

                    tableHtml += '</table>';
                    document.getElementById('ar-results-table-container').innerHTML = tableHtml;

                    showToast(`✅ Quarantined ${data.quarantined_count} duplicates/leaks!`);
                    btn.disabled = false;

                    // Refresh global state
                    await loadClasses();
                    await loadIssues();
                    if (currentView === 'inspector' && selectedClass) {
                        updateSplitCounts();
                        loadClassImages();
                    }
                } else {
                    resultsArea.style.display = 'block';
                    document.getElementById('ar-results-summary').innerHTML = `ℹ️ ${data.message || 'No action needed'}`;
                    document.getElementById('ar-results-table-container').innerHTML = '';
                    btn.disabled = false;
                }
            } catch (err) {
                statusArea.style.display = 'none';
                btn.disabled = false;
                alert('Auto-resolve failed: ' + err);
            }
        }

        // --- 🤖 SEQUENTIAL CLASS-BY-CLASS PIPELINE FRONTEND LOGIC ---
        let pipelinePollInterval = null;

        function populatePipelineCropSelect() {
            const cropSelect = document.getElementById('pipeline-crop-select');
            if (!cropSelect) return;
            const currentVal = cropSelect.value;
            cropSelect.innerHTML = '<option value="">🌍 Entire Dataset (All 201 Classes)</option>';

            const cropMap = new Map();
            allClasses.forEach(c => {
                const cropName = c.crop || c.class_name.split(' - ')[0].split('___')[0].trim();
                cropMap.set(cropName, (cropMap.get(cropName) || 0) + 1);
            });

            const sortedCrops = Array.from(cropMap.keys()).sort((a, b) => a.localeCompare(b));
            sortedCrops.forEach(cr => {
                const opt = document.createElement('option');
                opt.value = cr;
                opt.innerText = `🌱 ${cr} (${cropMap.get(cr)} classes)`;
                cropSelect.appendChild(opt);
            });

            if (currentVal) cropSelect.value = currentVal;
        }

        function openPipelineModal() {
            const modal = document.getElementById('pipeline-modal');
            if (!modal) return;
            populatePipelineCropSelect();
            modal.style.display = 'flex';

            // Check status: if running, show live tracking; otherwise show dropdown config view
            checkPipelineStatus();
        }

        function closePipelineModal() {
            const modal = document.getElementById('pipeline-modal');
            if (modal) modal.style.display = 'none';
        }

        function resetPipelineToConfig(bannerMsg) {
            const liveArea = document.getElementById('pipeline-live-area');
            const configArea = document.getElementById('pipeline-config-area');
            const startBtn = document.getElementById('btn-pipeline-start');
            const cancelBtn = document.getElementById('btn-pipeline-cancel');
            const banner = document.getElementById('pipeline-config-banner');
            const bannerText = document.getElementById('pipeline-config-banner-text');

            if (liveArea) liveArea.style.display = 'none';
            if (configArea) configArea.style.display = 'block';
            if (cancelBtn) cancelBtn.style.display = 'none';
            if (startBtn) {
                startBtn.style.display = 'inline-flex';
                startBtn.disabled = false;
                startBtn.innerText = '🚀 Start Auto Screening & Deletion';
            }

            if (banner && bannerText) {
                if (bannerMsg) {
                    banner.style.display = 'block';
                    bannerText.innerHTML = bannerMsg;
                } else {
                    banner.style.display = 'none';
                }
            }

            populatePipelineCropSelect();
        }

        async function viewMappedTwinsInGrid() {
            closePipelineModal();
            switchView('issues');
            const allBtn = document.querySelector('.filter-btn');
            if (allBtn) setFilter('all', allBtn);
            await loadIssues();
            window.scrollTo({ top: 0, behavior: 'smooth' });
            showToast('👀 Showing all mapped side-by-side twins in Dashboard grid!');
        }

        async function checkPipelineStatus() {
            try {
                const res = await fetch('/api/pipeline/status');
                const data = await res.json();
                updatePipelineUI(data);
                if (data.status === 'running') {
                    if (!pipelinePollInterval) {
                        pipelinePollInterval = setInterval(checkPipelineStatus, 800);
                    }
                } else {
                    if (pipelinePollInterval) {
                        clearInterval(pipelinePollInterval);
                        pipelinePollInterval = null;
                    }
                }
            } catch (err) {
                console.error('Failed to check pipeline status:', err);
            }
        }

        async function startSequentialPipeline() {
            const crop = document.getElementById('pipeline-crop-select').value;
            const mode = document.getElementById('pipeline-mode-select').value;
            const matchingMode = document.getElementById('pipeline-matching-mode') ? document.getElementById('pipeline-matching-mode').value : 'cluster';
            const commit = mode === 'live';

            const startBtn = document.getElementById('btn-pipeline-start');
            startBtn.disabled = true;

            const configBanner = document.getElementById('pipeline-config-banner');
            if (configBanner) configBanner.style.display = 'none';

            try {
                const res = await fetch('/api/pipeline/start', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        crop: crop || null,
                        commit: commit,
                        matching_mode: matchingMode
                    })
                });
                const data = await res.json();
                if (data.status === 'started') {
                    showToast('🚀 Pipeline started sequentially!');
                    document.getElementById('pipeline-live-area').style.display = 'flex';
                    document.getElementById('pipeline-config-area').style.display = 'none';
                    document.getElementById('btn-pipeline-cancel').style.display = 'inline-flex';
                    document.getElementById('btn-pipeline-cancel').disabled = false;
                    startBtn.style.display = 'none';

                    // Clear logs
                    const logsBox = document.getElementById('pipeline-live-logs');
                    if (logsBox) logsBox.innerHTML = '<div>🚀 Initializing sequential engine...</div>';

                    if (!pipelinePollInterval) {
                        pipelinePollInterval = setInterval(checkPipelineStatus, 800);
                    }
                } else {
                    alert(data.message || 'Could not start pipeline');
                    startBtn.disabled = false;
                }
            } catch (err) {
                alert('Pipeline start request failed: ' + err);
                startBtn.disabled = false;
            }
        }

        async function cancelPipeline() {
            try {
                if (pipelinePollInterval) {
                    clearInterval(pipelinePollInterval);
                    pipelinePollInterval = null;
                }
                const res = await fetch('/api/pipeline/cancel', { method: 'POST' });
                showToast('🛑 Pipeline stopped. Returned to crop selection.');
            } catch (err) {
                console.error('Cancel failed:', err);
            }
            // Immediately return to the dropdown page!
            resetPipelineToConfig('🛑 <strong>Pipeline stopped by user.</strong> Select a crop below to start a new run.');
        }

        function updatePipelineUI(state) {
            if (!state) return;

            const liveArea = document.getElementById('pipeline-live-area');
            const configArea = document.getElementById('pipeline-config-area');
            const startBtn = document.getElementById('btn-pipeline-start');
            const cancelBtn = document.getElementById('btn-pipeline-cancel');

            if (state.status === 'running') {
                liveArea.style.display = 'flex';
                configArea.style.display = 'none';
                cancelBtn.style.display = 'inline-flex';
                cancelBtn.disabled = false;
                startBtn.style.display = 'none';

                document.getElementById('pipeline-status-badge').innerText = 'RUNNING';
                document.getElementById('pipeline-status-badge').style.background = '#05966933';
                document.getElementById('pipeline-status-badge').style.color = '#34d399';
            } else if (state.status === 'completed') {
                // Immediately return to dropdown configuration page!
                liveArea.style.display = 'none';
                configArea.style.display = 'block';
                cancelBtn.style.display = 'none';
                startBtn.style.display = 'inline-flex';
                startBtn.disabled = false;
                startBtn.innerText = '🚀 Start Auto Screening & Deletion';

                if (pipelinePollInterval) {
                    clearInterval(pipelinePollInterval);
                    pipelinePollInterval = null;
                }

                // Show rich status banner at top of config area
                const configBanner = document.getElementById('pipeline-config-banner');
                const configBannerText = document.getElementById('pipeline-config-banner-text');
                const bannerTwinsBtn = document.getElementById('btn-banner-view-twins');

                const totalMapped = state.total_quarantined || (state.summary && state.summary.total_visual_issues) || 0;
                const isDryRun = state.summary ? !state.summary.commit : false;
                const modeLabel = isDryRun ? 'Dry-Run Audit' : 'Live Quarantine';

                if (configBanner && configBannerText) {
                    configBanner.style.display = 'block';
                    configBannerText.innerHTML = `🎉 <strong>${modeLabel} Complete!</strong> Processed ${state.total_classes || 0} classes. Found/quarantined <strong>${totalMapped}</strong> duplicate & leaking images (${state.total_train_purged || 0} from Train). Choose next crop below:`;
                    if (bannerTwinsBtn) {
                        if (totalMapped > 0) {
                            bannerTwinsBtn.style.display = 'inline-flex';
                            bannerTwinsBtn.innerText = `👀 View ${totalMapped} Mapped Twins in Grid`;
                        } else {
                            bannerTwinsBtn.style.display = 'none';
                        }
                    }
                }

                populatePipelineCropSelect();
            } else {
                // idle / error
                liveArea.style.display = 'none';
                configArea.style.display = 'block';
                cancelBtn.style.display = 'none';
                startBtn.style.display = 'inline-flex';
                startBtn.disabled = false;
                startBtn.innerText = '🚀 Start Auto Screening & Deletion';
                populatePipelineCropSelect();
            }

            const pct = state.progress || 0;
            const curIdx = state.current_index || 0;
            const total = state.total_classes || 0;

            const progBar = document.getElementById('pipeline-progress-bar');
            if (progBar) progBar.style.width = `${pct}%`;

            const progText = document.getElementById('pipeline-progress-text');
            if (progText) progText.innerText = `Class ${curIdx} / ${total} (${pct}%)`;

            const curClassEl = document.getElementById('pipeline-current-class');
            if (curClassEl) curClassEl.innerText = state.current_class || '-';

            const timerEl = document.getElementById('pipeline-timer');
            if (timerEl) timerEl.innerText = `⏱️ ${(state.elapsed_sec || 0).toFixed(1)}s`;

            const qEl = document.getElementById('pipeline-stat-quarantined');
            if (qEl) qEl.innerText = state.total_quarantined || 0;

            const trEl = document.getElementById('pipeline-stat-train');
            if (trEl) trEl.innerText = state.total_train_purged || 0;

            const cEl = document.getElementById('pipeline-stat-classes-issues');
            if (cEl) cEl.innerText = state.classes_with_issues || 0;

            if (state.message) {
                const logsBox = document.getElementById('pipeline-live-logs');
                if (logsBox) {
                    const line = document.createElement('div');
                    line.innerText = `[${new Date().toLocaleTimeString()}] ${state.message}`;
                    if (!logsBox.lastElementChild || logsBox.lastElementChild.innerText !== line.innerText) {
                        logsBox.appendChild(line);
                        logsBox.scrollTop = logsBox.scrollHeight;
                    }
                }
            }

            // Refresh global counts if completed
            if (state.status === 'completed' && !state._refreshed) {
                state._refreshed = true;
                loadClasses();
                loadIssues();
            }
        }

        // --- CLASS SPLIT EXPLORER & MANUAL INSPECTION LOGIC ---
        async function loadClasses() {
            try {
                const res = await fetch('/api/classes');
                allClasses = await res.json();
                populateClassDropdown(allClasses);

                if (allClasses.length > 0) {
                    selectedClass = allClasses[0].class_name;
                    document.getElementById('class-dropdown').value = selectedClass;
                    updateSplitCounts();
                    loadClassImages();
                }
            } catch (err) {
                console.error('Failed to load classes', err);
            }
        }

        function populateClassDropdown(classes) {
            const dd = document.getElementById('class-dropdown');
            const scanDd = document.getElementById('scan-class-select');

            dd.innerHTML = '';
            if (scanDd) {
                scanDd.innerHTML = '<option value="">All Dataset Classes</option>';
            }

            classes.forEach(c => {
                const opt = document.createElement('option');
                opt.value = c.class_name;
                opt.innerText = `${c.class_name} (${c.total_count} imgs - Tr:${c.train_count} / V:${c.val_count} / Te:${c.test_count})`;
                dd.appendChild(opt);

                if (scanDd) {
                    const optScan = document.createElement('option');
                    optScan.value = c.class_name;
                    optScan.innerText = `${c.class_name} (${c.total_count} imgs)`;
                    scanDd.appendChild(optScan);
                }
            });

            populatePipelineCropSelect();
        }

        function filterClassDropdown() {
            const query = document.getElementById('class-filter-input').value.toLowerCase();
            const filtered = allClasses.filter(c => c.class_name.toLowerCase().includes(query) || c.crop.toLowerCase().includes(query));
            populateClassDropdown(filtered);
            if (filtered.length > 0) {
                selectedClass = filtered[0].class_name;
                document.getElementById('class-dropdown').value = selectedClass;
                updateSplitCounts();
                currentPage = 1;
                loadClassImages();
            }
        }

        function onClassChange() {
            selectedClass = document.getElementById('class-dropdown').value;
            currentPage = 1;
            selectedPaths.clear();
            updateSelectedCounter();
            updateSplitCounts();
            loadClassImages();
        }

        function setSplit(split) {
            currentSplit = split;
            document.getElementById('pill-train').classList.toggle('active', split === 'train');
            document.getElementById('pill-val').classList.toggle('active', split === 'val');
            document.getElementById('pill-test').classList.toggle('active', split === 'test');
            currentPage = 1;
            selectedPaths.clear();
            updateSelectedCounter();
            updateInspectorBadge();
            loadClassImages();
        }

        function updateSplitCounts() {
            const cls = allClasses.find(c => c.class_name === selectedClass);
            if (cls) {
                document.getElementById('count-train').innerText = cls.train_count;
                document.getElementById('count-val').innerText = cls.val_count;
                document.getElementById('count-test').innerText = cls.test_count;
            }
            updateInspectorBadge();
        }

        async function loadClassImages() {
            if (!selectedClass) return;
            const grid = document.getElementById('class-image-grid');
            grid.innerHTML = '<div style="grid-column:1/-1; text-align:center; padding:40px; color:#94a3b8;">Loading foliar specimens...</div>';

            try {
                const res = await fetch(`/api/class-images?class_name=${encodeURIComponent(selectedClass)}&split=${currentSplit}&page=${currentPage}&limit=48`);
                const data = await res.json();
                currentClassImages = data.images || [];
                totalPages = data.total_pages || 1;

                document.getElementById('page-indicator').innerText = `Page ${data.page} of ${totalPages} (${data.total_images} total in ${currentSplit})`;
                document.getElementById('btn-prev-page').disabled = currentPage <= 1;
                document.getElementById('btn-next-page').disabled = currentPage >= totalPages;

                renderClassGrid();
            } catch (err) {
                grid.innerHTML = `<div style="grid-column:1/-1; text-align:center; padding:40px; color:#ef4444;">Failed to load images: ${err}</div>`;
            }
        }

        function renderClassGrid() {
            const grid = document.getElementById('class-image-grid');
            grid.innerHTML = '';

            if (currentClassImages.length === 0) {
                grid.innerHTML = '<div style="grid-column:1/-1; text-align:center; padding:60px; color:#64748b;">No images found in this split.</div>';
                return;
            }

            currentClassImages.forEach(img => {
                const card = document.createElement('div');
                const isSelected = selectedPaths.has(img.path);
                card.className = `leaf-card ${isSelected ? 'selected' : ''}`;
                const safeCardId = encodeURIComponent(img.path).split('%').join('_');
                card.id = `leaf-card-${safeCardId}`;
                const cleanImgPath = toPosix(img.path);

                card.innerHTML = `
                    <input type="checkbox" class="select-checkbox-overlay" ${isSelected ? 'checked' : ''} onclick="event.stopPropagation(); toggleSelect('${cleanImgPath}')">
                    <button class="quick-quarantine-overlay" title="Quick Quarantine This Specimen" onclick="event.stopPropagation(); quickQuarantineOne('${cleanImgPath}')">✕</button>
                    <div class="leaf-img-box" onclick="openLightbox('/api/image?path=${encodeURIComponent(cleanImgPath)}', '${img.filename}')">
                        <img src="/api/image?path=${encodeURIComponent(cleanImgPath)}" loading="lazy">
                    </div>
                    <div class="leaf-card-footer" onclick="toggleSelect('${cleanImgPath}')">
                        <span class="leaf-card-fn">${img.filename}</span>
                        <span class="leaf-card-size">${img.size_kb} KB</span>
                    </div>
                `;

                grid.appendChild(card);
            });
        }

        function toggleSelect(path) {
            const cleanPath = toPosix(path);
            if (selectedPaths.has(cleanPath)) {
                selectedPaths.delete(cleanPath);
            } else {
                selectedPaths.add(cleanPath);
            }
            updateSelectedCounter();
            const safeCardId = encodeURIComponent(cleanPath).split('%').join('_');
            const el = document.getElementById(`leaf-card-${safeCardId}`);
            if (el) {
                const isSel = selectedPaths.has(cleanPath);
                el.classList.toggle('selected', isSel);
                const cb = el.querySelector('.select-checkbox-overlay');
                if (cb) cb.checked = isSel;
            }
        }

        function selectAllOnPage() {
            currentClassImages.forEach(img => selectedPaths.add(img.path));
            updateSelectedCounter();
            renderClassGrid();
        }

        function deselectAll() {
            selectedPaths.clear();
            updateSelectedCounter();
            renderClassGrid();
        }

        function updateSelectedCounter() {
            const count = selectedPaths.size;
            document.getElementById('selected-count').innerText = count;
            document.getElementById('btn-selected-count').innerText = count;
        }

        function changePage(delta) {
            const next = currentPage + delta;
            if (next >= 1 && next <= totalPages) {
                currentPage = next;
                loadClassImages();
            }
        }

        async function quickQuarantineOne(path) {
            const reasonSelect = document.getElementById('batch-reason-select');
            const reason = reasonSelect ? reasonSelect.value : 'manual_inspection';
            const reasonText = reasonSelect ? reasonSelect.options[reasonSelect.selectedIndex].text : reason;
            const fn = path.split('/').pop();
            if (!confirm(`Quarantine specimen "${fn}" with reason:\n[${reasonText}]?`)) return;

            try {
                const res = await fetch('/api/quarantine', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ path: path, reason: reason })
                });
                const data = await res.json();
                if (data.status === 'success' || data.status === 'already_moved') {
                    showToast(`Quarantined: ${fn} [${reason}]`);
                    selectedPaths.delete(path);
                    updateSelectedCounter();
                    await refreshClassCounts();
                    loadClassImages();
                }
            } catch (err) {
                alert('Quarantine failed: ' + err);
            }
        }

        async function quarantineMarkedBatch() {
            if (selectedPaths.size === 0) {
                alert('Please select at least one image to quarantine.');
                return;
            }

            const reasonSelect = document.getElementById('batch-reason-select');
            const reason = reasonSelect ? reasonSelect.value : 'manual_inspection';
            const reasonText = reasonSelect ? reasonSelect.options[reasonSelect.selectedIndex].text : reason;
            const count = selectedPaths.size;
            if (!confirm(`Are you sure you want to quarantine ${count} marked images with reason:\n[${reasonText}]?`)) return;

            try {
                const pathsArray = Array.from(selectedPaths);
                const res = await fetch('/api/quarantine-batch', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ paths: pathsArray, reason: reason })
                });
                const data = await res.json();
                if (data.status === 'success') {
                    showToast(`Successfully quarantined ${data.quarantined_count} images to [${reason}]!`);
                    selectedPaths.clear();
                    updateSelectedCounter();
                    await refreshClassCounts();
                    loadClassImages();
                }
            } catch (err) {
                alert('Batch quarantine failed: ' + err);
            }
        }

        async function refreshClassCounts() {
            try {
                const res = await fetch('/api/classes');
                allClasses = await res.json();
                updateSplitCounts();
            } catch (err) {
                console.error('Failed to refresh counts', err);
            }
        }

        // --- SCAN EXECUTION & REAL-TIME PROGRESS POLLING ---
        let scanPollTimer = null;

        async function triggerScanFromBar() {
            const targetClass = document.getElementById('scan-class-select').value;
            let targetIssue = currentFilter;
            if (targetIssue === 'severe_blur' || targetIssue === 'background_blur') {
                targetIssue = 'blurry';
            } else if (targetIssue === 'all') {
                targetIssue = null;
            }
            const maxImages = parseInt(document.getElementById('scan-max-select').value) || 50;

            await startScanJob(targetClass, targetIssue, maxImages);
        }

        async function scanCurrentInspectorClass() {
            if (!selectedClass) {
                alert('Please select a class first.');
                return;
            }
            switchView('issues');
            const scanSelect = document.getElementById('scan-class-select');
            if (scanSelect) scanSelect.value = selectedClass;
            await startScanJob(selectedClass, 'all', 50);
        }

        async function startScanJob(className, issue, maxImages) {
            try {
                showBanner();
                const res = await fetch('/api/scan/start', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        class_name: className,
                        issue: issue,
                        max_images: maxImages
                    })
                });
                const data = await res.json();
                if (data.status === 'already_running') {
                    showToast('A scan is already in progress!');
                } else {
                    showToast('Quality scan started!');
                }
                startPollingScan();
            } catch (err) {
                alert('Failed to start scan: ' + err);
            }
        }

        function showBanner() {
            const banner = document.getElementById('computation-banner');
            banner.style.display = 'flex';
            document.getElementById('pulse-dot').className = 'pulse-indicator';
            document.getElementById('progress-fill').className = 'progress-fill';
            const btn = document.getElementById('btn-run-scan');
            if (btn) btn.disabled = true;
        }

        function dismissBanner() {
            document.getElementById('computation-banner').style.display = 'none';
        }

        async function cancelCurrentScan() {
            try {
                const btn = document.getElementById('btn-cancel-scan');
                if (btn) {
                    btn.disabled = true;
                    btn.innerText = 'Stopping...';
                }
                await fetch('/api/scan/cancel', { method: 'POST' });
                showToast('🛑 Scan cancellation requested.');
                if (scanPollTimer) {
                    clearInterval(scanPollTimer);
                    scanPollTimer = null;
                }
                document.getElementById('comp-stage').innerText = '🛑 Scan Cancelled';
                document.getElementById('comp-message').innerText = 'Computation stopped by user.';
                document.getElementById('progress-fill').className = 'progress-fill error';
                const runBtn = document.getElementById('btn-run-scan');
                if (runBtn) runBtn.disabled = false;
                setTimeout(() => { dismissBanner(); }, 2500);
            } catch (err) {
                console.error('Error cancelling scan', err);
            }
        }

        function startPollingScan() {
            if (scanPollTimer) clearInterval(scanPollTimer);
            scanPollTimer = setInterval(pollScanStatus, 600);
            pollScanStatus();
        }

        async function pollScanStatus() {
            try {
                const res = await fetch('/api/scan/status');
                const state = await res.json();

                if (state.status === 'running') {
                    document.getElementById('computation-banner').style.display = 'flex';
                    document.getElementById('comp-stage').innerText = state.stage || 'Computing...';
                    document.getElementById('comp-pct').innerText = `${state.progress}%`;
                    document.getElementById('progress-fill').style.width = `${state.progress}%`;
                    document.getElementById('comp-timer').innerText = `⏱️ ${state.elapsed_sec}s`;
                    document.getElementById('comp-message').innerText = state.message || '';
                    const btn = document.getElementById('btn-run-scan');
                    if (btn) btn.disabled = true;
                } else if (state.status === 'completed') {
                    if (scanPollTimer) {
                        clearInterval(scanPollTimer);
                        scanPollTimer = null;
                    }

                    document.getElementById('comp-stage').innerText = '✅ Scan Completed!';
                    document.getElementById('comp-pct').innerText = '100%';
                    document.getElementById('progress-fill').style.width = '100%';
                    document.getElementById('progress-fill').className = 'progress-fill done';
                    document.getElementById('pulse-dot').className = 'pulse-indicator done';
                    document.getElementById('comp-timer').innerText = `⏱️ ${state.elapsed_sec}s`;
                    document.getElementById('comp-message').innerText = state.message;
                    const btn = document.getElementById('btn-run-scan');
                    if (btn) btn.disabled = false;

                    showToast(`✅ ${state.message}`);
                    if (state.issues_found > 0) {
                        currentFilter = 'all';
                        document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
                        const allBtn = document.querySelector('.filter-btn');
                        if (allBtn) allBtn.classList.add('active');
                    }
                    await loadIssues();

                    // Auto-hide banner after 5 seconds
                    setTimeout(() => {
                        if (!scanPollTimer) dismissBanner();
                    }, 5000);
                } else if (state.status === 'error') {
                    if (scanPollTimer) {
                        clearInterval(scanPollTimer);
                        scanPollTimer = null;
                    }

                    document.getElementById('comp-stage').innerText = '❌ Scan Error';
                    document.getElementById('progress-fill').className = 'progress-fill error';
                    document.getElementById('pulse-dot').className = 'pulse-indicator error';
                    document.getElementById('comp-message').innerText = state.error || 'Unknown error occurred';
                } else if (state.status === 'idle') {
                    if (scanPollTimer) {
                        clearInterval(scanPollTimer);
                        scanPollTimer = null;
                    }
                    const btn = document.getElementById('btn-run-scan');
                    if (btn) btn.disabled = false;
                }
            } catch (err) {
                console.error('Error polling scan status', err);
            }
        }

        // Lightbox
        function openLightbox(src, caption) {
            const lb = document.getElementById('lightbox');
            document.getElementById('lightbox-img').src = src;
            document.getElementById('lightbox-caption').innerText = caption;
            lb.style.display = 'flex';
        }

        function closeLightbox() {
            document.getElementById('lightbox').style.display = 'none';
        }

        // Toast
        function showToast(msg) {
            const t = document.getElementById('toast');
            t.innerText = msg;
            t.style.display = 'block';
            setTimeout(() => { t.style.display = 'none'; }, 2800);
        }

        // Init
        window.onload = async () => {
            await loadClasses();
            await loadIssues();
            updateScanButtonText();
            try {
                const res = await fetch('/api/scan/status');
                const state = await res.json();
                if (state.status === 'running') {
                    startPollingScan();
                }
            } catch (e) {
                console.error('Error checking scan status', e);
            }
        };
    </script>
</body>
</html>
"""
    return HTMLResponse(
        content=html,
        headers={
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Expires": "0"
        }
    )


if __name__ == "__main__":
    print("=" * 70)
    print("  🚀 FOLIAR QUALITY STUDIO & QUARANTINE DASHBOARD")
    print("=" * 70)
    print("Running local dashboard at: http://127.0.0.1:8765")
    uvicorn.run(app, host="127.0.0.1", port=8765, log_level="warning")
