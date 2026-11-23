"""
Balanced 1:2 Foliar-Centered Framing for Ginger - Bacterial Wilt
----------------------------------------------------------------
Eliminates dead white side space while enforcing a natural 1:2 portrait
aspect ratio centered gracefully on the leaf.
- Always reads from pristine raw archive: data/raw/original_unmodified_ginger_bacterial_wilt/
- Leaves natural white cushions on both left and right (never touches leaf borders).
- Eliminates harsh 1:5 geometric stretching when resized to 224x224.
- Reduces false-positive duplicate collisions in Clean Studio.
- Updates processed splits in data/processed/{train, val, test}/Ginger - Bacterial Wilt/
"""

import os
import sys
import shutil
import numpy as np
from PIL import Image

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")
RAW_ARCHIVE_DIR = os.path.join(BASE_DIR, "data", "raw", "original_unmodified_ginger_bacterial_wilt")

TARGET_CLASS = "Ginger - Bacterial Wilt"
SPLITS = ["train", "val", "test"]

def crop_foliar_balanced_1_2(img: Image.Image):
    """
    Finds the leaf center and bounds, then crops with a balanced 1:2 aspect ratio
    (Width = Height / 2) centered symmetrically on the leaf with natural white cushioning.
    """
    arr = np.array(img.convert("RGB"))
    H, W, _ = arr.shape
    
    # White background threshold: pixels where R, G, B are all > 230
    is_leaf = ~((arr[:, :, 0] > 230) & (arr[:, :, 1] > 230) & (arr[:, :, 2] > 230))
    coords = np.argwhere(is_leaf) # returns (y, x)
    
    if len(coords) < 100:
        # Fallback if no leaf found
        return img, (0, 0, W, H), 0.0, 0, 0
    
    ymin, xmin = coords.min(axis=0)
    ymax, xmax = coords.max(axis=0)
    
    leaf_w = xmax - xmin
    leaf_h = ymax - ymin
    center_x = (xmin + xmax) / 2.0
    
    # Target height = H, Target width = H / 2 (1:2 ratio)
    target_h = H
    target_w = max(int(target_h / 2.0), int(leaf_w * 1.25))
    target_w = min(target_w, W)
    
    c_xmin = int(center_x - target_w / 2.0)
    c_xmax = c_xmin + target_w
    if c_xmin < 0:
        c_xmax += -c_xmin
        c_xmin = 0
    if c_xmax > W:
        c_xmin -= (c_xmax - W)
        c_xmax = W
    c_xmin = max(0, c_xmin)
    c_xmax = min(W, c_xmax)
    
    left_cushion = xmin - c_xmin
    right_cushion = c_xmax - xmax
    
    cropped = img.crop((c_xmin, 0, c_xmax, target_h))
    trimmed_pct = 100.0 * (1.0 - (c_xmax - c_xmin) * target_h / (W * H))
    
    return cropped, (c_xmin, 0, c_xmax, target_h), trimmed_pct, left_cushion, right_cushion

def main():
    print("=" * 75)
    print("  🌿 BALANCED 1:2 FOLIAR-CENTERED FRAMING: Ginger - Bacterial Wilt")
    print("=" * 75)
    
    if not os.path.exists(RAW_ARCHIVE_DIR):
        print(f"[ERROR] Raw archive directory not found: {RAW_ARCHIVE_DIR}")
        return
        
    total_processed = 0
    
    for split in SPLITS:
        raw_folder = os.path.join(RAW_ARCHIVE_DIR, split, TARGET_CLASS)
        proc_folder = os.path.join(PROCESSED_DIR, split, TARGET_CLASS)
        
        if not os.path.exists(raw_folder):
            print(f"[-] Split raw archive not found: {raw_folder}")
            continue
            
        os.makedirs(proc_folder, exist_ok=True)
        files = sorted([f for f in os.listdir(raw_folder) if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
        print(f"\n[*] Processing split '{split}': {len(files)} images from raw archive...")
        
        saved_widths = []
        for i, f in enumerate(files, 1):
            raw_path = os.path.join(raw_folder, f)
            proc_path = os.path.join(proc_folder, f)
            
            with Image.open(raw_path) as img:
                orig_w, orig_h = img.size
                cropped_img, (c_xmin, c_ymin, c_xmax, c_ymax), trimmed_pct, l_cush, r_cush = crop_foliar_balanced_1_2(img)
                crop_w, crop_h = cropped_img.size
                saved_widths.append(crop_w)
                
                # Save high quality
                cropped_img.save(proc_path, quality=95)
                total_processed += 1
                
            if i <= 3 or i == len(files):
                print(f"    [{i}/{len(files)}] {f}: {orig_w}x{orig_h} -> {crop_w}x{crop_h} (Aspect 1:{(crop_h/crop_w):.1f}, Cushions L:{l_cush}px / R:{r_cush}px)")

        avg_w = np.mean(saved_widths) if saved_widths else 0
        print(f"    Split '{split}' done: Avg width set to {avg_w:.0f}px (Balanced 1:2 portrait framing).")
        
    print("\n" + "=" * 75)
    print(f"[SUCCESS] Total images processed and framed: {total_processed}")
    print(f"[SUCCESS] Permanent untouched raw originals preserved at:\n         {RAW_ARCHIVE_DIR}")
    print("=" * 75)

if __name__ == "__main__":
    main()
