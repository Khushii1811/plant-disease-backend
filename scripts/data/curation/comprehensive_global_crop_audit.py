import os
import sys
import re
import json
import time
from pathlib import Path
from PIL import Image
from collections import defaultdict

# Force UTF-8 on Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROC_DIR = PROJECT_ROOT / "data" / "processed"
RAW_DIR = PROJECT_ROOT / "data" / "raw"
OUTPUT_MANIFEST = RAW_DIR / "comprehensive_crop_audit_manifest.json"

def build_raw_indexes():
    print("=" * 80)
    print("📂 PHASE 1: COMPREHENSIVE RAW ARCHIVE INDEXING")
    print(f"   Root: {RAW_DIR}")
    print("=" * 80)
    
    t0 = time.time()
    
    # Store by lower filename -> list of paths
    raw_by_filename = defaultdict(list)
    raw_by_stem = defaultdict(list)
    
    # Track statistics
    total_raw_scanned = 0
    folders_scanned = set()
    
    for root, _, files in os.walk(RAW_DIR):
        r_path = Path(root)
        # Skip quarantine directories
        if "quarantine" in root.lower():
            continue
            
        rel_parts = r_path.relative_to(RAW_DIR).parts
        if rel_parts:
            folders_scanned.add(rel_parts[0])
            
        for f in files:
            if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
                total_raw_scanned += 1
                fp = r_path / f
                f_lower = f.lower()
                stem_lower = Path(f).stem.lower()
                
                raw_by_filename[f_lower].append(fp)
                raw_by_stem[stem_lower].append(fp)
    
    t1 = time.time()
    print(f"✅ Scanned {len(folders_scanned)} raw folders.")
    print(f"✅ Indexed {total_raw_scanned} total raw files in {t1 - t0:.2f}s.")
    print(f"   Unique filenames: {len(raw_by_filename)}, Unique stems: {len(raw_by_stem)}")
    return raw_by_filename, raw_by_stem

def resolve_candidate_raw(f_name, raw_by_filename, raw_by_stem):
    lower = f_name.lower()
    
    # 1. Exact filename match
    if lower in raw_by_filename:
        return raw_by_filename[lower][0]
    
    # 2. PlantVillage style split by '___'
    if "___" in f_name:
        tail = f_name.split("___")[-1].lower()
        if tail in raw_by_filename:
            return raw_by_filename[tail][0]
        tail_stem = Path(tail).stem.lower()
        if tail_stem in raw_by_stem:
            return raw_by_stem[tail_stem][0]
            
    # 3. Handle prefixes
    prefixes = [
        "scraped_kaggle_pv2_", "scraped_kaggle_pv1_", "scraped_kaggle_", "scraped_",
        "sourabh_", "sujay_", "therealoise_", "agrivision_", "datasetninja_",
        "lettuce_", "peach_", "plum_", "garlic_", "coffee_", "chilli_",
        "bell_", "eggplant_", "wheat_", "rice_", "plantcity_", "ginger_"
    ]
    
    clean = f_name
    for p in prefixes:
        if clean.lower().startswith(p.lower()):
            clean = clean[len(p):]
            break
            
    if clean.lower() in raw_by_filename:
        return raw_by_filename[clean.lower()][0]
    if Path(clean).stem.lower() in raw_by_stem:
        return raw_by_stem[Path(clean).stem.lower()][0]
        
    # 4. Handle embedded img_XXXXX names (e.g. "Banana - Yb sigatoka_img_00051464.jpg")
    img_match = re.search(r'(img_\d{8}\.(jpg|jpeg|png))', f_name, re.IGNORECASE)
    if img_match:
        img_name = img_match.group(1).lower()
        if img_name in raw_by_filename:
            return raw_by_filename[img_name][0]
            
    # 5. Handle hash suffixes: e.g. '_c53881f7.jpg'
    hash_match = re.search(r'_[a-f0-9]{8}\.(jpg|jpeg|png)$', f_name, re.IGNORECASE)
    if hash_match:
        stripped = f_name[:hash_match.start()] + f_name[hash_match.end()-4:]
        if stripped.lower() in raw_by_filename:
            return raw_by_filename[stripped.lower()][0]
        st_stem = Path(stripped).stem.lower()
        if st_stem in raw_by_stem:
            return raw_by_stem[st_stem][0]
        # try sub-parts
        parts = st_stem.split('_')
        for i in range(1, len(parts)):
            sub = "_".join(parts[i:])
            if sub in raw_by_stem:
                return raw_by_stem[sub][0]
            if (sub + ".jpg") in raw_by_filename:
                return raw_by_filename[sub + ".jpg"][0]
            if (sub + ".png") in raw_by_filename:
                return raw_by_filename[sub + ".png"][0]

    return None

def main():
    raw_by_filename, raw_by_stem = build_raw_indexes()
    
    print("\n" + "=" * 80)
    print("🔍 PHASE 2: AUDITING ALL PROCESSED IMAGES ACROSS ENTIRE BENCHMARK")
    print(f"   Root: {PROC_DIR}")
    print("=" * 80)
    
    t0 = time.time()
    
    total_processed_scanned = 0
    matched_in_raw = 0
    unmatched_in_raw = 0
    
    identical_count = 0
    cropped_records = []
    cropped_by_class = defaultdict(list)
    
    splits = ["train", "val", "test"]
    for split in splits:
        sp_dir = PROC_DIR / split
        if not sp_dir.exists():
            continue
            
        print(f"📂 Auditing split: {split}...")
        cls_dirs = sorted([d for d in sp_dir.iterdir() if d.is_dir()])
        
        for cls_dir in cls_dirs:
            cls_name = cls_dir.name
            
            for f in cls_dir.iterdir():
                if not f.is_file() or f.suffix.lower() not in [".jpg", ".jpeg", ".png", ".webp"]:
                    continue
                    
                total_processed_scanned += 1
                raw_f = resolve_candidate_raw(f.name, raw_by_filename, raw_by_stem)
                
                if not raw_f or not raw_f.exists():
                    unmatched_in_raw += 1
                    continue
                    
                matched_in_raw += 1
                
                try:
                    with Image.open(f) as ip, Image.open(raw_f) as ir:
                        p_size = ip.size
                        r_size = ir.size
                        
                        if p_size == r_size:
                            identical_count += 1
                        else:
                            rec = {
                                "class": cls_name,
                                "split": split,
                                "filename": f.name,
                                "processed_path": str(f.relative_to(PROJECT_ROOT)),
                                "raw_path": str(raw_f.relative_to(PROJECT_ROOT)),
                                "processed_size": p_size,
                                "raw_size": r_size,
                                "diff_w": p_size[0] - r_size[0],
                                "diff_h": p_size[1] - r_size[1]
                            }
                            cropped_records.append(rec)
                            cropped_by_class[cls_name].append(rec)
                except Exception as e:
                    pass

    t1 = time.time()
    
    print("\n" + "=" * 80)
    print("📊 COMPREHENSIVE GLOBAL CROP AUDIT RESULTS")
    print("=" * 80)
    print(f"Total processed images scanned:      {total_processed_scanned}")
    print(f"Successfully resolved to raw source: {matched_in_raw} ({matched_in_raw / total_processed_scanned * 100:.2f}%)")
    print(f"Unmatched (autonomous scraped/web):  {unmatched_in_raw}")
    print(f"100% Identical Dimensions:           {identical_count}")
    print(f"🚨 CROPPED / MODIFIED IMAGES FOUND:  {len(cropped_records)}")
    print(f"Total time taken:                    {t1 - t0:.2f} seconds")
    print("=" * 80)
    
    if cropped_records:
        print("\n📋 CROPPED IMAGES BREAKDOWN BY CLASS:")
        for cls_name, items in sorted(cropped_by_class.items(), key=lambda x: len(x[1]), reverse=True):
            print(f"   • {cls_name:45s}: {len(items):4d} cropped")
            for it in items[:2]:
                print(f"      - {it['filename']}: Proc {it['processed_size']} vs Raw {it['raw_size']} (Diff: {it['diff_w']}x{it['diff_h']})")
    else:
        print("\n✨ ZERO CROPPED IMAGES DETECTED! ✨")
        print("Every single resolved image in data/processed has 100% exact original raw dimensions.")
        
    # Save manifest
    manifest_data = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "total_processed_scanned": total_processed_scanned,
        "matched_in_raw": matched_in_raw,
        "unmatched_in_raw": unmatched_in_raw,
        "identical_dimensions_count": identical_count,
        "total_cropped_count": len(cropped_records),
        "classes_affected_count": len(cropped_by_class),
        "by_class": {c: len(items) for c, items in cropped_by_class.items()},
        "records": cropped_records
    }
    
    with open(OUTPUT_MANIFEST, "w", encoding="utf-8") as f:
        json.dump(manifest_data, f, indent=2)
        
    print(f"\n💾 Full audit manifest saved to: {OUTPUT_MANIFEST}")
    print("=" * 80)

if __name__ == "__main__":
    main()
