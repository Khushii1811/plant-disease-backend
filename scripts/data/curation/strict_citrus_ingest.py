import os
import sys
import json
import shutil
import hashlib
from pathlib import Path
import numpy as np
import pandas as pd
from PIL import Image

# Ensure UTF-8 output on Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

import torch
import torchvision.transforms as T
from torchvision.models import mobilenet_v3_small, MobileNet_V3_Small_Weights

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
CANDIDATE_DIR = RAW_DIR / "citrus_sourabh2001" / "Leaves"
QUARANTINE_MELANOSE_DIR = RAW_DIR / "quarantine_citrus_melanose"
QUARANTINE_DUP_DIR = RAW_DIR / "quarantine_citrus_duplicates"

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def get_md5(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

def extract_features(image_paths, model, transform, batch_size=64):
    features = []
    valid_paths = []
    
    for i in range(0, len(image_paths), batch_size):
        batch_paths = image_paths[i:i + batch_size]
        tensors = []
        for p in batch_paths:
            try:
                with Image.open(p) as img:
                    img_rgb = img.convert("RGB")
                    tensors.append(transform(img_rgb))
                    valid_paths.append(p)
            except Exception as e:
                print(f"[WARN] Failed to load {p}: {e}")
                
        if not tensors:
            continue
            
        batch_tensor = torch.stack(tensors).to(DEVICE)
        with torch.no_grad():
            emb = model(batch_tensor)
            emb = torch.flatten(emb, 1)
            emb = torch.nn.functional.normalize(emb, p=2, dim=1)
            features.append(emb.cpu().numpy())
            
    if not features:
        return np.empty((0, 576), dtype=np.float32), []
    return np.vstack(features), valid_paths

def cluster_and_deduplicate(paths, model, transform, thresh=0.95):
    feats, valid = extract_features(paths, model, transform)
    if len(valid) == 0:
        return [], []
        
    sim = np.dot(feats, feats.T)
    n = len(valid)
    parent = list(range(n))
    
    def find(i):
        if parent[i] == i: return i
        parent[i] = find(parent[i])
        return parent[i]
        
    def union(i, j):
        root_i = find(i)
        root_j = find(j)
        if root_i != root_j:
            parent[root_i] = root_j

    for i in range(n):
        for j in range(i + 1, n):
            if sim[i, j] >= thresh:
                union(i, j)
                
    clusters = {}
    for idx in range(n):
        root = find(idx)
        clusters.setdefault(root, []).append(valid[idx])
        
    primaries = []
    duplicates = []
    for root, cluster_paths in clusters.items():
        # Keep the first image (or largest resolution)
        primaries.append(cluster_paths[0])
        duplicates.extend(cluster_paths[1:])
        
    return primaries, duplicates

def main():
    print("=" * 80)
    print("🍊 STRICT CITRUS DEDUPLICATION & MULTI-CLASS INGESTION PIPELINE")
    print(f"   Compute Device: {DEVICE}")
    print("=" * 80)
    
    QUARANTINE_MELANOSE_DIR.mkdir(parents=True, exist_ok=True)
    QUARANTINE_DUP_DIR.mkdir(parents=True, exist_ok=True)
    
    # Step 1: Quarantine Melanose
    melanose_src = CANDIDATE_DIR / "Melanose"
    melanose_files = list(melanose_src.glob("*.*"))
    print(f"\n[STEP 1] Quarantining {len(melanose_files)} Melanose images to {QUARANTINE_MELANOSE_DIR.name}...")
    for f in melanose_files:
        shutil.copy2(f, QUARANTINE_MELANOSE_DIR / f.name)
    with open(QUARANTINE_MELANOSE_DIR / "manifest.json", "w") as mf:
        json.dump([f.name for f in melanose_files], mf, indent=2)
    print(f"   [DONE] Melanose quarantined.")
    
    # Step 2: Initialize Neural Network
    print("\n[STEP 2] Initializing MobileNetV3-Small neural feature extractor on CUDA...")
    weights = MobileNet_V3_Small_Weights.DEFAULT
    model = mobilenet_v3_small(weights=weights)
    model.classifier = torch.nn.Identity()
    model = model.to(DEVICE)
    model.eval()
    
    transform = T.Compose([
        T.Resize((224, 224)),
        T.ToTensor(),
        T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    
    # Step 3: Deduplicate each class
    targets = {
        "healthy": {
            "source_folder": CANDIDATE_DIR / "healthy",
            "target_class": "Citrus - Healthy",
            "is_new": True
        },
        "Black spot": {
            "source_folder": CANDIDATE_DIR / "Black spot",
            "target_class": "Citrus - Black spot",
            "is_new": True
        },
        "canker": {
            "source_folder": CANDIDATE_DIR / "canker",
            "target_class": "Citrus - citrus canker",
            "is_new": False
        },
        "greening": {
            "source_folder": CANDIDATE_DIR / "greening",
            "target_class": "Citrus - citrus greening disease",
            "is_new": False
        }
    }
    
    rng = np.random.default_rng(42)
    total_added = 0
    
    for sub_name, info in targets.items():
        src_folder = info["source_folder"]
        target_cls = info["target_class"]
        all_imgs = sorted(list(src_folder.glob("*.*")))
        
        print(f"\n[STEP 3] Processing '{sub_name}' -> '{target_cls}':")
        print(f"   Raw images: {len(all_imgs)}")
        
        primaries, duplicates = cluster_and_deduplicate(all_imgs, model, transform, thresh=0.95)
        print(f"   Unique specimens: {len(primaries)} | Redundant burst duplicates: {len(duplicates)}")
        
        # Quarantine duplicates
        dup_sub_dir = QUARANTINE_DUP_DIR / sub_name
        dup_sub_dir.mkdir(parents=True, exist_ok=True)
        for d in duplicates:
            shutil.copy2(d, dup_sub_dir / d.name)
        with open(dup_sub_dir / "manifest.json", "w") as f:
            json.dump([d.name for d in duplicates], f, indent=2)
            
        # 80-10-10 Split
        n = len(primaries)
        idx = np.arange(n)
        rng.shuffle(idx)
        
        n_val = int(round(n * 0.10))
        n_test = int(round(n * 0.10))
        n_train = n - n_val - n_test
        
        splits = {
            "train": [primaries[i] for i in idx[:n_train]],
            "val": [primaries[i] for i in idx[n_train:n_train + n_val]],
            "test": [primaries[i] for i in idx[n_train + n_val:]]
        }
        
        print(f"   Partitioning {n} specimens: {len(splits['train'])} Train, {len(splits['val'])} Val, {len(splits['test'])} Test")
        
        for split, file_list in splits.items():
            dest_dir = PROCESSED_DIR / split / target_cls
            dest_dir.mkdir(parents=True, exist_ok=True)
            for f in file_list:
                dest_file = dest_dir / f"sourabh_{f.name}"
                shutil.copy2(f, dest_file)
                total_added += 1
                
        print(f"   [DONE] Ingested into '{target_cls}' across all splits.")
        
    print(f"\n[STEP 4] Total clean foliar specimens added: {total_added}")
    
    # Step 5: Cryptographic Zero Leakage Check across all Citrus classes
    print("\n[STEP 5] Cryptographic verification across all Citrus classes...")
    for target_cls in ["Citrus - Healthy", "Citrus - Black spot", "Citrus - citrus canker", "Citrus - citrus greening disease"]:
        hashes = {"train": set(), "val": set(), "test": set()}
        for split in ["train", "val", "test"]:
            p_dir = PROCESSED_DIR / split / target_cls
            if p_dir.exists():
                for f in p_dir.glob("*.*"):
                    hashes[split].add(get_md5(f))
                    
        tv = hashes["train"] & hashes["val"]
        tt = hashes["train"] & hashes["test"]
        vt = hashes["val"] & hashes["test"]
        assert len(tv) == 0 and len(tt) == 0 and len(vt) == 0, f"LEAKAGE DETECTED in {target_cls}!"
        print(f"   [PASS] {target_cls}: Train ({len(hashes['train'])}), Val ({len(hashes['val'])}), Test ({len(hashes['test'])}) -> Zero Leakage.")

    # Step 6: Rebuild global class counts
    print("\n[STEP 6] Rebuilding processed class counts...")
    train_dir = PROCESSED_DIR / "train"
    val_dir = PROCESSED_DIR / "val"
    test_dir = PROCESSED_DIR / "test"
    
    classes = sorted(list({d.name for d in train_dir.iterdir() if d.is_dir()}))
    rows = []
    
    for cls in classes:
        t_cnt = len(list((train_dir / cls).glob("*.*")))
        v_cnt = len(list((val_dir / cls).glob("*.*")))
        te_cnt = len(list((test_dir / cls).glob("*.*")))
        rows.append({
            "class_name": cls,
            "train_count": t_cnt,
            "val_count": v_cnt,
            "test_count": te_cnt,
            "total_count": t_cnt + v_cnt + te_cnt
        })
        
    df = pd.DataFrame(rows)
    csv_path = DATA_DIR / "processed_class_counts.csv"
    md_path = DATA_DIR / "processed_class_counts.md"
    
    df.to_csv(csv_path, index=False)
    
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("# Processed Dataset Class Distribution\n\n")
        f.write(f"- **Total Active Classes:** {len(df)}\n")
        f.write(f"- **Total Train Images:** {df['train_count'].sum():,}\n")
        f.write(f"- **Total Val Images:** {df['val_count'].sum():,}\n")
        f.write(f"- **Total Test Images:** {df['test_count'].sum():,}\n")
        f.write(f"- **Total Benchmark Images:** {df['total_count'].sum():,}\n\n")
        f.write(df.to_markdown(index=False))
        
    print(f"   [DONE] Class counts updated: {len(df)} classes, {df['total_count'].sum():,} total images.")

if __name__ == "__main__":
    main()
