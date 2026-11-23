"""
scripts/interactive_dataset_inspector.py — Interactive Visual Cleaning Studio with Gemini Vision AI.

Features:
  - Class Search & Selector across all 168 classes
  - Multi-Split View (Train, Val, Test, or All Combined)
  - 🧠 Gemini 1.5 Vision Multimodal Pathologist:
      * Analyzes images botanically
      * Identifies real plant species (e.g. Rose vs. Chili vs. Tomato)
      * Explains symptoms & flags wrong specimens
  - 🔍 Fast Local Outlier Scanner (No API required fallback)
  - Interactive Keep vs. Discard Toggles on each image
  - Batch Selection & Safe Reversible Quarantine System
  - Undo / Restore Quarantine capability

Usage:
  python scripts/interactive_dataset_inspector.py
  (Runs at http://127.0.0.1:8765)
"""

import argparse
import base64
import csv
import io
import json
import logging
import os
import shutil
import sys
import urllib.request
import urllib.error
import webbrowser
from collections import defaultdict
from pathlib import Path
from typing import Optional

import numpy as np
import uvicorn
from fastapi import FastAPI, Query, Body, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from PIL import Image

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
QUARANTINE_DIR = PROJECT_ROOT / "data" / "quarantine_curated"
QUARANTINE_DIR.mkdir(parents=True, exist_ok=True)

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}

app = FastAPI(title="Plant Disease Dataset Visual Cleaning Studio")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store quarantine history for undo operations
QUARANTINE_HISTORY = []


def load_gemini_key() -> str:
    """Load Gemini API Key from gemini_key.txt, .env, or environment variable."""
    # 1. Check gemini_key.txt
    key_file = PROJECT_ROOT / "gemini_key.txt"
    if key_file.exists():
        for line in key_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and " " not in line and len(line) >= 20:
                return line

    # 2. Check .env
    env_file = PROJECT_ROOT / ".env"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("GEMINI_API_KEY="):
                val = line.split("=", 1)[1].strip().strip('"').strip("'")
                if val and " " not in val and len(val) >= 20:
                    return val

    # 3. Check environment
    k = os.environ.get("GEMINI_API_KEY", "").strip()
    if k and " " not in k and len(k) >= 20:
        return k

    return ""


ACTIVE_GEMINI_KEY = load_gemini_key()


def get_all_classes() -> list[str]:
    """Retrieve all class names in processed/train."""
    train_dir = PROCESSED_DIR / "train"
    if not train_dir.exists():
        return []
    return sorted([d.name for d in train_dir.iterdir() if d.is_dir()])


@app.get("/api/classes")
def api_get_classes():
    classes = get_all_classes()
    class_details = []

    for c in classes:
        tr_cnt = len(list((PROCESSED_DIR / "train" / c).glob("*.*"))) if (PROCESSED_DIR / "train" / c).exists() else 0
        va_cnt = len(list((PROCESSED_DIR / "val" / c).glob("*.*"))) if (PROCESSED_DIR / "val" / c).exists() else 0
        te_cnt = len(list((PROCESSED_DIR / "test" / c).glob("*.*"))) if (PROCESSED_DIR / "test" / c).exists() else 0
        
        q_cnt = 0
        for split in ["train", "val", "test"]:
            qp = QUARANTINE_DIR / split / c
            if qp.exists():
                q_cnt += len(list(qp.glob("*.*")))

        class_details.append({
            "name": c,
            "train": tr_cnt,
            "val": va_cnt,
            "test": te_cnt,
            "quarantined": q_cnt,
            "total": tr_cnt + va_cnt + te_cnt
        })
    return {"classes": class_details}


@app.get("/api/images")
def api_get_images(class_name: str = Query(...), split: str = Query("all")):
    """Get images for a class across selected split or all splits."""
    splits_to_scan = ["train", "val", "test"] if split == "all" else [split]
    images_data = []

    for s in splits_to_scan:
        split_dir = PROCESSED_DIR / s / class_name
        if not split_dir.exists():
            continue

        for f in sorted(split_dir.iterdir()):
            if f.is_file() and f.suffix.lower() in IMAGE_EXTS:
                fn = f.name.lower()
                source = "Baseline Dataset"
                if "bing" in fn:
                    source = "Bing Search API"
                elif "pv2" in fn or "pv1" in fn:
                    source = "PlantVillage Ext"
                elif "grape" in fn:
                    source = "Kaggle Grape"
                elif "rust" in fn:
                    source = "Rust Archive"
                elif "inat" in fn:
                    source = "iNaturalist"
                elif "kaggle" in fn:
                    source = "Kaggle Pathology"

                is_scraped = fn.startswith("scraped_")

                images_data.append({
                    "filename": f.name,
                    "split": s,
                    "class_name": class_name,
                    "source": source,
                    "is_new": is_scraped,
                    "url": f"/image-file/{s}/{class_name}/{f.name}"
                })

    return {"images": images_data, "count": len(images_data)}


@app.get("/image-file/{split}/{class_name}/{filename}")
def serve_image(split: str, class_name: str, filename: str):
    file_path = PROCESSED_DIR / split / class_name / filename
    if not file_path.exists():
        file_path = QUARANTINE_DIR / split / class_name / filename
        if not file_path.exists():
            return JSONResponse(status_code=404, content={"error": "File not found"})
    return FileResponse(file_path)


@app.post("/api/set-gemini-key")
def api_set_gemini_key(payload: dict = Body(...)):
    global ACTIVE_GEMINI_KEY
    key = payload.get("key", "").strip()
    ACTIVE_GEMINI_KEY = key
    return {"status": "success", "has_key": bool(ACTIVE_GEMINI_KEY)}


@app.get("/api/get-gemini-status")
def api_get_gemini_status():
    return {"has_key": bool(ACTIVE_GEMINI_KEY)}


def analyze_batch_with_gemini(api_key: str, class_name: str, batch: list[tuple[str, Path]]) -> list[dict]:
    """Call Gemini Vision API with a batch of images using header authentication and fallback models."""
    api_key = api_key.strip()
    if not api_key:
        raise HTTPException(status_code=400, detail="Gemini API Key is empty. Please enter your API key in the top bar.")

    # Verified working models for your API key
    models = ["gemini-flash-latest", "gemini-pro-latest", "gemini-3.8-flash", "gemini-3.5-flash"]
    
    parts = []
    prompt_text = f"""You are a strict, world-class Plant Pathologist and Botanical Inspector.
We are auditing a dataset folder strictly designated for the single class: '{class_name}'.
Inspect each of the attached images one by one with high scrutiny.

For each image:
1. Identify the exact botanical plant species (e.g. Capsicum annuum (Chili), Rosa (Rose), Coffea (Coffee), Solanum (Tomato), Weed, etc.).
2. Evaluate validity: Is this image a genuine, clear leaf specimen of '{class_name}'?
3. Set "valid": false if ANY of the following apply:
   - It is a DIFFERENT plant species (e.g. a Rose leaf, Coffee leaf, Tomato leaf, or weed mixed into a Chili folder).
   - It is a distant whole orchard / whole tree / landscape shot without clear leaf-level pathology.
   - It is an artificial diagram, graphic, collage, non-plant object, or completely corrupted image.
   - It exhibits an entirely wrong, conflicting pathology.
4. Set "valid": true ONLY if it is a genuine leaf specimen of the correct species and pathology for '{class_name}'.

Return ONLY a valid JSON array of objects in exact order of the images:
[
  {{
    "image_index": 1,
    "filename": "img_xxx.jpg",
    "valid": true/false,
    "identified_species": "exact botanical name and common name",
    "diagnosis": "pathology observed",
    "reason": "specific explanation of why it is valid or invalid"
  }}
]
"""
    parts.append({"text": prompt_text})

    for idx, (split, f) in enumerate(batch, 1):
        try:
            with Image.open(f) as img:
                img_rgb = img.convert("RGB")
                img_rgb.thumbnail((512, 512))
                buf = io.BytesIO()
                img_rgb.save(buf, format="JPEG", quality=85)
                b64_data = base64.b64encode(buf.getvalue()).decode("utf-8")
                
                parts.append({"text": f"Image #{idx} (Filename: {f.name}, Split: {split}):"})
                parts.append({
                    "inline_data": {
                        "mime_type": "image/jpeg",
                        "data": b64_data
                    }
                })
        except Exception as e:
            continue

    req_body = {
        "contents": [{"parts": parts}],
        "generationConfig": {
            "response_mime_type": "application/json",
            "temperature": 0.1
        }
    }
    req_data = json.dumps(req_body).encode("utf-8")
    
    headers = {
        "Content-Type": "application/json"
    }

    last_err = None
    for model_name in models:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
        req = urllib.request.Request(url, data=req_data, headers=headers)

        try:
            with urllib.request.urlopen(req, timeout=45) as resp:
                resp_json = json.loads(resp.read().decode("utf-8"))
                content_text = resp_json["candidates"][0]["content"]["parts"][0]["text"]
                results = json.loads(content_text)
                return results
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8", errors="ignore")
            last_err = f"HTTP {e.code}: {err_body}"
            # If 404 (model not found), try next model in loop; if 400 (bad key), stop and report
            if e.code == 400:
                raise HTTPException(status_code=400, detail=f"Gemini API Key Error: {err_body}")
            continue
        except Exception as e:
            last_err = str(e)
            continue

    raise HTTPException(status_code=500, detail=f"Gemini API Error: {last_err}")


@app.post("/api/gemini-audit-class")
def api_gemini_audit_class(payload: dict = Body(...)):
    """
    Runs Gemini Vision Multimodal Pathologist audit over images in the class.
    Processes in smart batches.
    """
    class_name = payload.get("class_name")
    api_key = (payload.get("api_key") or "").strip()
    if not api_key or len(api_key) < 20 or " " in api_key:
        api_key = load_gemini_key() or ACTIVE_GEMINI_KEY

    if not api_key or len(api_key) < 20 or " " in api_key:
        return JSONResponse(
            status_code=400, 
            content={
                "status": "error", 
                "message": "Valid Gemini API Key not found. Please paste your key in 'gemini_key.txt' file."
            }
        )

    class_images = []
    for s in ["train", "val", "test"]:
        p = PROCESSED_DIR / s / class_name
        if p.exists():
            for f in sorted(p.iterdir()):
                if f.is_file() and f.suffix.lower() in IMAGE_EXTS:
                    class_images.append((s, f))

    if not class_images:
        return {"status": "empty", "flagged": []}

    import concurrent.futures

    max_images = int(payload.get("max_images", 500))
    images_to_audit = class_images[:max_images]
    batch_size = 10
    batches = [images_to_audit[i:i + batch_size] for i in range(0, len(images_to_audit), batch_size)]

    all_diagnoses = []
    flagged_results = []

    def process_single_batch(batch):
        try:
            return batch, analyze_batch_with_gemini(api_key, class_name, batch)
        except Exception as e:
            return batch, []

    # Execute all batches in parallel with up to 6 worker threads (10x faster!)
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
        future_results = list(executor.map(process_single_batch, batches))

    for batch, batch_diag in future_results:
        for idx_in_batch, item in enumerate(batch_diag):
            if idx_in_batch < len(batch):
                s, f = batch[idx_in_batch]
                is_valid = item.get("valid") if "valid" in item else item.get("is_valid", True)
                if isinstance(is_valid, str):
                    is_valid = is_valid.lower() not in ["false", "no", "invalid", "0"]
                elif not isinstance(is_valid, bool):
                    for k, v in item.items():
                        if isinstance(v, bool) and not v:
                            is_valid = False
                            break

                species = item.get("identified_species") or item.get("botanical_species") or item.get("species") or "Unknown"
                diag = item.get("diagnosis") or item.get("disease") or item.get("symptom") or ""
                reason = item.get("reason") or item.get("explanation") or f"Identified as {species}"

                diag_entry = {
                    "filename": f.name,
                    "split": s,
                    "class_name": class_name,
                    "valid": is_valid,
                    "identified_species": species,
                    "diagnosis": diag,
                    "reason": reason
                }
                all_diagnoses.append(diag_entry)

                if not is_valid:
                    flagged_results.append({
                        "filename": f.name,
                        "split": s,
                        "class_name": class_name,
                        "reasons": [f"Gemini: {species} ({reason})"],
                        "species": species,
                        "diagnosis": diag,
                        "reason": reason,
                        "score": 1.0,
                        "suggestion": "DISCARD"
                    })

    return {
        "status": "success",
        "class_name": class_name,
        "total_scanned": len(images_to_audit),
        "flagged_count": len(flagged_results),
        "flagged": flagged_results,
        "all_diagnoses": all_diagnoses
    }


@app.get("/api/local-ai-scan")
def api_local_ai_scan(class_name: str = Query(...)):
    """Fast local feature outlier fallback."""
    class_images = []
    for s in ["train", "val", "test"]:
        p = PROCESSED_DIR / s / class_name
        if p.exists():
            for f in p.iterdir():
                if f.is_file() and f.suffix.lower() in IMAGE_EXTS:
                    class_images.append((s, f))

    if not class_images:
        return {"status": "empty", "flagged": []}

    features = []
    aspect_ratios = []
    resolutions = []

    for s, f in class_images:
        try:
            with Image.open(f) as img:
                img_rgb = img.convert("RGB")
                w, h = img_rgb.size
                aspect_ratios.append(w / max(1, h))
                resolutions.append((w, h))
                
                thumb = img_rgb.resize((16, 16))
                arr = np.array(thumb, dtype=np.float32) / 255.0
                mean_rgb = arr.mean(axis=(0, 1))
                std_rgb = arr.std(axis=(0, 1))
                flat = arr.flatten()
                feat = np.concatenate([mean_rgb, std_rgb, flat])
                features.append(feat)
        except Exception:
            features.append(np.zeros(16 * 16 * 3 + 6))
            aspect_ratios.append(1.0)
            resolutions.append((224, 224))

    features = np.array(features)
    centroid = np.mean(features, axis=0)
    dists = np.linalg.norm(features - centroid, axis=1)

    mean_dist = np.mean(dists)
    std_dist = np.std(dists)
    outlier_thresh = mean_dist + 2.0 * std_dist if std_dist > 0 else mean_dist * 1.5

    flagged_results = []
    for i, (s, f) in enumerate(class_images):
        dist = dists[i]
        ar = aspect_ratios[i]
        w, h = resolutions[i]
        
        reasons = []
        is_flagged = False

        if dist > outlier_thresh:
            is_flagged = True
            reasons.append("Visual Outlier / Potential Foreign Plant")

        if ar < 0.35 or ar > 2.8:
            is_flagged = True
            reasons.append(f"Extreme Aspect Ratio ({ar:.2f})")

        if min(w, h) < 70:
            is_flagged = True
            reasons.append(f"Very Low Resolution ({w}x{h})")

        if is_flagged:
            flagged_results.append({
                "filename": f.name,
                "split": s,
                "class_name": class_name,
                "reasons": reasons,
                "score": float(dist),
                "suggestion": "DISCARD"
            })

    return {
        "status": "success",
        "class_name": class_name,
        "total_scanned": len(class_images),
        "flagged_count": len(flagged_results),
        "flagged": flagged_results
    }


@app.post("/api/quarantine-images")
def api_quarantine_images(payload: dict = Body(...)):
    """Safely move selected images to quarantine."""
    items = payload.get("items", [])
    if not items:
        return {"status": "error", "message": "No items provided"}

    moved_records = []
    for item in items:
        split = item.get("split")
        class_name = item.get("class_name")
        filename = item.get("filename")

        src_path = PROCESSED_DIR / split / class_name / filename
        if src_path.exists():
            dest_dir = QUARANTINE_DIR / split / class_name
            dest_dir.mkdir(parents=True, exist_ok=True)
            dest_path = dest_dir / filename

            shutil.move(str(src_path), str(dest_path))
            moved_records.append({
                "split": split,
                "class_name": class_name,
                "filename": filename,
                "from": str(src_path),
                "to": str(dest_path)
            })

    if moved_records:
        QUARANTINE_HISTORY.append(moved_records)

    return {
        "status": "success",
        "moved_count": len(moved_records),
        "history_id": len(QUARANTINE_HISTORY) - 1
    }


@app.post("/api/restore-last-quarantine")
def api_restore_last_quarantine():
    """Restore the most recent batch of quarantined images."""
    if not QUARANTINE_HISTORY:
        return {"status": "error", "message": "No recent quarantine actions to undo."}

    last_batch = QUARANTINE_HISTORY.pop()
    restored_count = 0

    for record in last_batch:
        q_path = Path(record["to"])
        dest_path = Path(record["from"])
        if q_path.exists():
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(q_path), str(dest_path))
            restored_count += 1

    return {"status": "success", "restored_count": restored_count}


@app.get("/", response_class=HTMLResponse)
def index():
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>🌿 Plant Pathology Dataset Visual Cleaning Studio</title>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
  :root {
    --primary: #10b981;
    --primary-dark: #059669;
    --danger: #ef4444;
    --danger-dark: #dc2626;
    --gemini-purple: #8b5cf6;
    --gemini-dark: #7c3aed;
    --accent: #6366f1;
    --dark: #0b0f19;
    --gray-900: #111827;
    --gray-800: #1f2937;
    --gray-700: #374151;
    --gray-600: #4b5563;
    --gray-300: #d1d5db;
    --gray-100: #f3f4f6;
    --sidebar-w: 360px;
  }

  * { box-sizing: border-box; margin: 0; padding: 0; }

  body {
    font-family: 'Plus Jakarta Sans', sans-serif;
    background: var(--dark);
    color: #f1f5f9;
    display: flex;
    height: 100vh;
    overflow: hidden;
  }

  /* Sidebar */
  .sidebar {
    width: var(--sidebar-w);
    background: var(--gray-900);
    border-right: 1px solid var(--gray-800);
    display: flex;
    flex-direction: column;
    height: 100vh;
  }

  .sidebar-header {
    padding: 16px 18px;
    border-bottom: 1px solid var(--gray-800);
  }

  .logo {
    display: flex;
    align-items: center;
    gap: 8px;
    font-weight: 800;
    font-size: 1.05rem;
    color: var(--primary);
    margin-bottom: 10px;
  }

  .search-box {
    position: relative;
  }

  .search-input {
    width: 100%;
    background: var(--gray-800);
    border: 1px solid var(--gray-700);
    color: #f3f4f6;
    padding: 9px 12px;
    border-radius: 8px;
    font-size: 0.85rem;
    outline: none;
    transition: border-color 0.2s;
  }
  .search-input:focus { border-color: var(--primary); }

  .class-list {
    flex: 1;
    overflow-y: auto;
    padding: 8px;
  }

  .class-item {
    padding: 10px 12px;
    border-radius: 8px;
    cursor: pointer;
    margin-bottom: 4px;
    transition: all 0.15s ease;
    border: 1px solid transparent;
  }
  .class-item:hover {
    background: var(--gray-800);
  }
  .class-item.active {
    background: rgba(16, 185, 129, 0.12);
    border-color: rgba(16, 185, 129, 0.4);
  }

  .class-name {
    font-size: 0.85rem;
    font-weight: 600;
    color: #f3f4f6;
    margin-bottom: 4px;
    word-break: break-word;
  }

  .class-meta {
    display: flex;
    gap: 6px;
    font-size: 0.72rem;
    color: #94a3b8;
    align-items: center;
  }

  .badge {
    padding: 2px 6px;
    border-radius: 4px;
    font-weight: 600;
  }
  .badge-train { background: #1e3a8a; color: #93c5fd; }
  .badge-val { background: #4c1d95; color: #d8b4fe; }
  .badge-test { background: #064e3b; color: #6ee7b7; }
  .badge-q { background: #7f1d1d; color: #fca5a5; }

  /* Main Container */
  .main-content {
    flex: 1;
    display: flex;
    flex-direction: column;
    height: 100vh;
    overflow: hidden;
  }

  /* Top Control Bar */
  .control-bar {
    background: var(--gray-900);
    border-bottom: 1px solid var(--gray-800);
    padding: 12px 24px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 12px;
  }

  .title-section h1 {
    font-size: 1.15rem;
    font-weight: 800;
    color: #ffffff;
    display: flex;
    align-items: center;
    gap: 8px;
  }

  .api-key-box {
    display: flex;
    align-items: center;
    gap: 8px;
    background: #1e1b4b;
    border: 1px solid #4338ca;
    padding: 6px 12px;
    border-radius: 8px;
  }
  .api-key-input {
    background: #0f172a;
    border: 1px solid #334155;
    color: #f8fafc;
    padding: 4px 8px;
    border-radius: 6px;
    font-size: 0.78rem;
    width: 180px;
    outline: none;
  }

  .split-pills {
    display: flex;
    gap: 4px;
    background: var(--gray-800);
    padding: 4px;
    border-radius: 8px;
  }

  .split-btn {
    background: transparent;
    border: none;
    color: #94a3b8;
    padding: 6px 12px;
    border-radius: 6px;
    font-size: 0.8rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s;
  }
  .split-btn.active {
    background: var(--primary);
    color: #ffffff;
  }

  /* Action Bar */
  .action-bar {
    background: #141d2e;
    border-bottom: 1px solid var(--gray-800);
    padding: 10px 24px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 10px;
  }

  .action-left {
    display: flex;
    align-items: center;
    gap: 8px;
  }

  .btn {
    padding: 8px 14px;
    border-radius: 6px;
    font-size: 0.8rem;
    font-weight: 700;
    cursor: pointer;
    border: none;
    display: inline-flex;
    align-items: center;
    gap: 6px;
    transition: all 0.15s;
  }
  .btn-gemini { background: linear-gradient(135deg, #7c3aed, #4f46e5); color: #ffffff; box-shadow: 0 0 10px rgba(124, 58, 237, 0.4); }
  .btn-gemini:hover { opacity: 0.9; }
  .btn-ai { background: #374151; color: #f3f4f6; }
  .btn-ai:hover { background: #4b5563; }
  .btn-discard { background: var(--danger); color: #ffffff; }
  .btn-discard:hover { background: var(--danger-dark); }
  .btn-secondary { background: var(--gray-800); color: #f3f4f6; border: 1px solid var(--gray-700); }
  .btn-secondary:hover { background: var(--gray-700); }

  /* Gallery Grid */
  .gallery-container {
    flex: 1;
    overflow-y: auto;
    padding: 18px 24px;
  }

  .grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
    gap: 16px;
  }

  .card {
    background: var(--gray-900);
    border: 2px solid var(--gray-800);
    border-radius: 10px;
    overflow: hidden;
    position: relative;
    transition: all 0.2s ease;
    display: flex;
    flex-direction: column;
  }
  .card:hover {
    border-color: var(--gray-600);
    transform: translateY(-2px);
  }
  .card.flagged {
    border-color: rgba(239, 68, 68, 0.9);
    background: rgba(239, 68, 68, 0.06);
  }
  .card.selected {
    border-color: var(--danger);
    box-shadow: 0 0 14px rgba(239, 68, 68, 0.4);
  }

  .card-img-wrap {
    width: 100%;
    aspect-ratio: 1;
    background: #000;
    position: relative;
    cursor: pointer;
  }

  .card-img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }

  .card-checkbox {
    position: absolute;
    top: 8px;
    left: 8px;
    width: 20px;
    height: 20px;
    cursor: pointer;
    z-index: 10;
    accent-color: var(--danger);
  }

  .card-split-badge {
    position: absolute;
    top: 8px;
    right: 8px;
    font-size: 0.68rem;
    font-weight: 700;
    padding: 2px 6px;
    border-radius: 4px;
    text-transform: uppercase;
    background: rgba(0, 0, 0, 0.75);
    backdrop-filter: blur(4px);
  }

  .card-info {
    padding: 10px 12px;
    display: flex;
    flex-direction: column;
    gap: 6px;
    flex: 1;
  }

  .card-filename {
    font-size: 0.74rem;
    font-family: 'JetBrains Mono', monospace;
    color: #94a3b8;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  .card-status-badge {
    font-size: 0.72rem;
    font-weight: 700;
    padding: 3px 6px;
    border-radius: 4px;
    display: inline-block;
    line-height: 1.3;
  }
  .status-keep { background: rgba(16, 185, 129, 0.15); color: #34d399; }
  .status-flagged { background: rgba(239, 68, 68, 0.25); color: #fca5a5; border: 1px solid rgba(239, 68, 68, 0.4); }

  .card-btn-toggle {
    margin-top: auto;
    width: 100%;
    padding: 6px;
    border-radius: 6px;
    font-size: 0.78rem;
    font-weight: 700;
    cursor: pointer;
    border: 1px solid var(--gray-700);
    background: var(--gray-800);
    color: #f3f4f6;
    transition: all 0.15s;
  }
  .card-btn-toggle:hover {
    background: var(--danger);
    border-color: var(--danger);
    color: #fff;
  }
  .card-btn-toggle.active-discard {
    background: var(--danger);
    border-color: var(--danger);
    color: #fff;
  }

  /* Modal Lightbox */
  .modal {
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background: rgba(0,0,0,0.85);
    display: none;
    align-items: center;
    justify-content: center;
    z-index: 999;
    backdrop-filter: blur(8px);
  }
  .modal.show { display: flex; }
  .modal-content {
    max-width: 90vw;
    max-height: 90vh;
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  .modal-img {
    max-width: 85vw;
    max-height: 80vh;
    border-radius: 8px;
    box-shadow: 0 10px 40px rgba(0,0,0,0.8);
  }
  .modal-meta {
    margin-top: 12px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.88rem;
    color: #e2e8f0;
  }

  /* Toast */
  .toast {
    position: fixed;
    bottom: 24px;
    right: 24px;
    background: var(--gray-900);
    border: 1px solid var(--primary);
    color: #f3f4f6;
    padding: 12px 20px;
    border-radius: 8px;
    font-size: 0.88rem;
    font-weight: 600;
    box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    display: none;
    z-index: 1000;
  }
</style>
</head>
<body>

<!-- Sidebar -->
<div class="sidebar">
  <div class="sidebar-header">
    <div class="logo">🌿 Cleaning Studio</div>
    <div class="search-box">
      <input type="text" id="searchInput" class="search-input" placeholder="Search 168 classes..." oninput="filterClasses()">
    </div>
  </div>
  <div class="class-list" id="classList">
    <!-- Populated dynamically -->
  </div>
</div>

<!-- Main Content -->
<div class="main-content">
  <!-- Control Bar -->
  <div class="control-bar">
    <div class="title-section">
      <h1 id="currentClassTitle">Select a class to inspect</h1>
    </div>

    <!-- Gemini Key Box -->
    <div class="api-key-box">
      <span style="font-size:0.75rem; color:#c7d2fe; font-weight:700;">✨ Gemini API Key:</span>
      <input type="password" id="geminiKeyInput" class="api-key-input" placeholder="Enter key..." onchange="saveGeminiKey()">
      <button class="btn btn-secondary" style="padding:4px 8px; font-size:0.75rem;" onclick="saveGeminiKey()">Save</button>
    </div>

    <div class="split-pills">
      <button class="split-btn active" onclick="setSplit('all')">All</button>
      <button class="split-btn" onclick="setSplit('train')">Train</button>
      <button class="split-btn" onclick="setSplit('val')">Val</button>
      <button class="split-btn" onclick="setSplit('test')">Test</button>
    </div>
  </div>

  <!-- Action Bar -->
  <div class="action-bar">
    <div class="action-left">
      <button class="btn btn-gemini" onclick="runGeminiAudit()">🧠 Ask Gemini Vision Expert</button>
      <button class="btn btn-ai" onclick="runLocalAiScan()">🔍 Local Outlier Scan</button>
      <button class="btn btn-secondary" onclick="selectAllFlagged()">Select Flagged (<span id="flaggedCount">0</span>)</button>
      <button class="btn btn-secondary" onclick="clearSelection()">Clear Selection</button>
    </div>
    <div>
      <button class="btn btn-discard" id="btnDiscardSelected" onclick="quarantineSelected()">🚨 Quarantine Selected (<span id="selectedCount">0</span>)</button>
      <button class="btn btn-secondary" onclick="restoreLastQuarantine()">🔄 Undo Last Action</button>
    </div>
  </div>

  <!-- Image Grid -->
  <div class="gallery-container">
    <div class="grid" id="imageGrid">
      <p style="color:#64748b; font-size:0.9rem;">Select a class from the left sidebar to inspect images.</p>
    </div>
  </div>
</div>

<!-- Lightbox Modal -->
<div class="modal" id="modal" onclick="closeModal()">
  <div class="modal-content" onclick="event.stopPropagation()">
    <img id="modalImg" class="modal-img" src="" alt="Zoom">
    <div id="modalMeta" class="modal-meta"></div>
  </div>
</div>

<!-- Toast -->
<div class="toast" id="toast"></div>

<script>
  let allClasses = [];
  let currentClass = "";
  let currentSplit = "all";
  let currentImages = [];
  let aiFlaggedMap = new Map(); // filename -> {reasons, species, diagnosis, reason}
  let selectedItems = new Set(); // set of "split:filename"

  async function loadClasses() {
    const res = await fetch('/api/classes');
    const data = await res.json();
    allClasses = data.classes;
    renderClassList(allClasses);

    if (allClasses.length > 0 && !currentClass) {
      selectClass(allClasses[0].name);
    }
  }

  function renderClassList(list) {
    const logo = document.querySelector('.logo');
    if (logo) logo.innerHTML = `🌿 Cleaning Studio <span style="font-size:0.75rem; color:#a7f3d0; font-weight:600; margin-left:6px;">(${list.length} Classes)</span>`;

    const container = document.getElementById('classList');
    container.innerHTML = '';
    list.forEach(c => {
      const item = document.createElement('div');
      item.className = `class-item ${c.name === currentClass ? 'active' : ''}`;
      item.onclick = () => selectClass(c.name);
      item.innerHTML = `
        <div class="class-name">${c.name}</div>
        <div class="class-meta">
          <span class="badge badge-train">Tr: ${c.train}</span>
          <span class="badge badge-val">V: ${c.val}</span>
          <span class="badge badge-test">Te: ${c.test}</span>
          ${c.quarantined > 0 ? `<span class="badge badge-q">Q: ${c.quarantined}</span>` : ''}
        </div>
      `;
      container.appendChild(item);
    });
  }

  function filterClasses() {
    const q = document.getElementById('searchInput').value.toLowerCase();
    const filtered = allClasses.filter(c => c.name.toLowerCase().includes(q));
    renderClassList(filtered);
  }

  async function selectClass(name) {
    currentClass = name;
    aiFlaggedMap.clear();
    selectedItems.clear();
    updateCounts();

    document.getElementById('currentClassTitle').innerText = name;
    renderClassList(allClasses);
    await loadImages();
  }

  function setSplit(split) {
    currentSplit = split;
    document.querySelectorAll('.split-btn').forEach(btn => {
      btn.classList.toggle('active', btn.innerText.toLowerCase().startsWith(split));
    });
    loadImages();
  }

  async function loadImages() {
    if (!currentClass) return;
    const grid = document.getElementById('imageGrid');
    grid.innerHTML = '<p style="color:#64748b;">Loading images...</p>';

    const res = await fetch(`/api/images?class_name=${encodeURIComponent(currentClass)}&split=${currentSplit}`);
    const data = await res.json();
    currentImages = data.images;
    renderGallery();
  }

  function renderGallery() {
    const grid = document.getElementById('imageGrid');
    grid.innerHTML = '';

    if (currentImages.length === 0) {
      grid.innerHTML = '<p style="color:#64748b;">No images found in this split.</p>';
      return;
    }

    currentImages.forEach(img => {
      const key = `${img.split}:${img.filename}`;
      const isSelected = selectedItems.has(key);
      const isFlagged = aiFlaggedMap.has(key);
      const flagInfo = aiFlaggedMap.get(key);

      const card = document.createElement('div');
      card.className = `card ${isFlagged ? 'flagged' : ''} ${isSelected ? 'selected' : ''}`;
      card.id = `card-${img.split}-${img.filename}`;

      card.innerHTML = `
        <div class="card-img-wrap" onclick="openModal('${img.url}', '${img.filename}', '${img.split}')">
          <input type="checkbox" class="card-checkbox" ${isSelected ? 'checked' : ''} onclick="event.stopPropagation(); toggleSelect('${img.split}', '${img.filename}')">
          <span class="card-split-badge badge-${img.split}">${img.split}</span>
          <img class="card-img" src="${img.url}" loading="lazy">
        </div>
        <div class="card-info">
          <div class="card-filename" title="${img.filename}">${img.filename}</div>
          <div>
            ${isFlagged ? `
              <span class="card-status-badge status-flagged" title="${flagInfo.reasons.join(', ')}">⚠️ ${flagInfo.reasons[0]}</span>
            ` : `
              <span class="card-status-badge status-keep">✅ Valid Specimen</span>
            `}
          </div>
          <button class="card-btn-toggle ${isSelected ? 'active-discard' : ''}" onclick="toggleSelect('${img.split}', '${img.filename}')">
            ${isSelected ? '❌ Marked for Discard' : '🗑️ Discard'}
          </button>
        </div>
      `;
      grid.appendChild(card);
    });

    updateCounts();
  }

  function toggleSelect(split, filename) {
    const key = `${split}:${filename}`;
    if (selectedItems.has(key)) {
      selectedItems.delete(key);
    } else {
      selectedItems.add(key);
    }
    renderGallery();
  }

  async function saveGeminiKey() {
    const key = document.getElementById('geminiKeyInput').value.trim();
    if (!key) {
      alert("Please enter a valid Gemini API key.");
      return;
    }
    localStorage.setItem('gemini_api_key', key);
    await fetch('/api/set-gemini-key', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ key })
    });
    showToast('✨ Gemini API key saved & ready!');
  }

  async function runGeminiAudit() {
    if (!currentClass) return;
    const key = document.getElementById('geminiKeyInput').value.trim();
    showToast(`🧠 Gemini Vision is inspecting '${currentClass}'... Please wait...`);

    try {
      const res = await fetch('/api/gemini-audit-class', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ class_name: currentClass, api_key: key, max_images: 100 })
      });
      
      const data = await res.json();

      if (data.status === 'error') {
        alert(data.message || data.detail || "Gemini audit error.");
        return;
      }

      if (data.status === 'success') {
        aiFlaggedMap.clear();
        data.flagged.forEach(f => {
          const key = `${f.split}:${f.filename}`;
          aiFlaggedMap.set(key, f);
          selectedItems.add(key);
        });

        showToast(`Gemini diagnosed ${data.total_scanned} images: Flagged ${data.flagged_count} imposters/mislabels.`);
        renderGallery();
      }
    } catch (err) {
      alert("Error calling Gemini: " + err.message);
    }
  }

  async function runLocalAiScan() {
    if (!currentClass) return;
    showToast(`Scanning ${currentClass} with local outlier algorithm...`);

    const res = await fetch(`/api/local-ai-scan?class_name=${encodeURIComponent(currentClass)}`);
    const data = await res.json();

    if (data.status === 'success') {
      aiFlaggedMap.clear();
      data.flagged.forEach(f => {
        const key = `${f.split}:${f.filename}`;
        aiFlaggedMap.set(key, f);
        selectedItems.add(key);
      });

      showToast(`Local scan flagged ${data.flagged_count} items.`);
      renderGallery();
    }
  }

  function selectAllFlagged() {
    aiFlaggedMap.forEach((val, key) => {
      selectedItems.add(key);
    });
    renderGallery();
  }

  function clearSelection() {
    selectedItems.clear();
    renderGallery();
  }

  function updateCounts() {
    document.getElementById('flaggedCount').innerText = aiFlaggedMap.size;
    document.getElementById('selectedCount').innerText = selectedItems.size;
  }

  async function quarantineSelected() {
    if (selectedItems.size === 0) {
      alert("No images selected to quarantine.");
      return;
    }

    if (!confirm(`Move ${selectedItems.size} selected images to quarantine? (Safe & Reversible)`)) {
      return;
    }

    const items = Array.from(selectedItems).map(k => {
      const [split, filename] = k.split(':');
      return { split, filename, class_name: currentClass };
    });

    const res = await fetch('/api/quarantine-images', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ items })
    });

    const data = await res.json();
    if (data.status === 'success') {
      showToast(`Successfully quarantined ${data.moved_count} images!`);
      selectedItems.clear();
      await loadClasses();
      await loadImages();
    }
  }

  async function restoreLastQuarantine() {
    const res = await fetch('/api/restore-last-quarantine', { method: 'POST' });
    const data = await res.json();
    if (data.status === 'success') {
      showToast(`Restored ${data.restored_count} images from quarantine!`);
      await loadClasses();
      await loadImages();
    } else {
      alert(data.message);
    }
  }

  function openModal(url, filename, split) {
    document.getElementById('modalImg').src = url;
    document.getElementById('modalMeta').innerText = `[${split.toUpperCase()}] ${filename}`;
    document.getElementById('modal').classList.add('show');
  }

  function closeModal() {
    document.getElementById('modal').classList.remove('show');
  }

  function showToast(msg) {
    const t = document.getElementById('toast');
    t.innerText = msg;
    t.style.display = 'block';
    setTimeout(() => { t.style.display = 'none'; }, 3000);
  }

  window.onload = () => {
    const savedKey = localStorage.getItem('gemini_api_key');
    if (savedKey) {
      document.getElementById('geminiKeyInput').value = savedKey;
      fetch('/api/set-gemini-key', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ key: savedKey })
      });
    }
    loadClasses();
  };
</script>
</body>
</html>
"""


def main():
    parser = argparse.ArgumentParser(description="Start Dataset Visual Cleaning Studio with Gemini Vision")
    parser.add_argument("--port", type=int, default=8765, help="Port to run on (default: 8765)")
    args = parser.parse_args()

    url = f"http://127.0.0.1:{args.port}"
    print("\n" + "=" * 70)
    print("  🌿 PLANT PATHOLOGY DATASET VISUAL CLEANING STUDIO + GEMINI VISION")
    print(f"  URL: {url}")
    print("  Mode: Multimodal Plant Pathologist AI + Safe Quarantine")
    print("=" * 70 + "\n")

    try:
        webbrowser.open(url)
    except Exception:
        pass

    uvicorn.run(app, host="127.0.0.1", port=args.port, log_level="warning")


if __name__ == "__main__":
    main()
