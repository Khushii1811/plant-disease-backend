import os
import sys
import hashlib
from pathlib import Path
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor
from PIL import Image
import imagehash
from tqdm import tqdm

def process_file(file_info):
    path_str, split, class_name, crop_name = file_info
    p = Path(path_str)
    try:
        data = p.read_bytes()
        sha256 = hashlib.sha256(data).hexdigest()
        with Image.open(p) as img:
            ph = str(imagehash.phash(img))
        return {
            'path': path_str,
            'rel_path': str(p.relative_to('data/processed')).replace('\\', '/'),
            'split': split,
            'class': class_name,
            'crop': crop_name,
            'sha256': sha256,
            'phash': ph,
            'size': len(data)
        }
    except Exception:
        return None

def collect_files():
    files = []
    base = Path('data/processed')
    for split in ['train', 'val', 'test']:
        split_dir = base / split
        if not split_dir.exists():
            continue
        for class_dir in split_dir.iterdir():
            if not class_dir.is_dir():
                continue
            class_name = class_dir.name
            crop_name = class_name.split('___')[0] if '___' in class_name else class_name.split(' - ')[0]
            for img_path in class_dir.iterdir():
                if img_path.is_file() and img_path.suffix.lower() in {'.jpg', '.jpeg', '.png', '.bmp', '.webp'}:
                    files.append((str(img_path), split, class_name, crop_name))
    return files

def main():
    print("=" * 80)
    print("STEP 1 INTEGRITY AND LEAKAGE RE-SCAN (POST-P004 QUARANTINE)")
    print("=" * 80)
    all_files = collect_files()
    print(f"Total images found on disk in data/processed: {len(all_files):,}")

    max_workers = min(16, os.cpu_count() or 4)
    results = []
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        for res in tqdm(executor.map(process_file, all_files, chunksize=200), total=len(all_files), desc="Hashing"):
            if res:
                results.append(res)

    print(f"\nSuccessfully hashed {len(results):,} images.")

    # 1. Exact SHA-256 Duplicates
    sha_map = defaultdict(list)
    for it in results:
        sha_map[it['sha256']].append(it)

    exact_cross_split_pairs = 0
    exact_contradictory_pairs = 0
    exact_dup_hashes = {h: items for h, items in sha_map.items() if len(items) > 1}
    print("\n1. Exact SHA-256 Duplicates:")
    print(f"   Unique duplicate hashes: {len(exact_dup_hashes)}")
    for h, items in exact_dup_hashes.items():
        splits = set(x['split'] for x in items)
        classes = set(x['class'] for x in items)
        if len(splits) > 1:
            exact_cross_split_pairs += 1
        if len(classes) > 1:
            exact_contradictory_pairs += 1
            print(f"   [CONTRADICTORY] hash {h[:10]}: {classes} across {splits}")

    print(f"   Exact SHA-256 cross-split duplicates: {exact_cross_split_pairs}")
    print(f"   Exact SHA-256 contradictory labels:   {exact_contradictory_pairs}")

    # 2. Perceptual Hash (pHash <= 4)
    print("\n2. Perceptual Hash (pHash <= 4) Cross-Split Search:")
    int_hashes = []
    valid_items = []
    for it in results:
        int_hashes.append(int(it['phash'], 16))
        valid_items.append(it)

    masks = [
        (0x1FFF, 0),
        (0x1FFF, 13),
        (0x1FFF, 26),
        (0x1FFF, 39),
        (0xFFF, 52),
    ]
    table = [defaultdict(list) for _ in range(5)]
    for idx, h in enumerate(int_hashes):
        for block_idx, (mask, shift) in enumerate(masks):
            key = (h >> shift) & mask
            table[block_idx][key].append(idx)

    candidate_pairs = set()
    for block_idx in range(5):
        for key, id_list in table[block_idx].items():
            if len(id_list) > 1:
                for i in range(len(id_list)):
                    id1 = id_list[i]
                    s1 = valid_items[id1]['split']
                    for j in range(i + 1, len(id_list)):
                        id2 = id_list[j]
                        s2 = valid_items[id2]['split']
                        if s1 != s2:
                            candidate_pairs.add((min(id1, id2), max(id1, id2)))

    print(f"   Candidate cross-split pairs to verify: {len(candidate_pairs):,}")
    cross_split_phash_le4 = 0
    contradictory_phash_le4 = 0

    for id1, id2 in candidate_pairs:
        h1 = int_hashes[id1]
        h2 = int_hashes[id2]
        dist = bin(h1 ^ h2).count('1')
        if dist <= 4:
            cross_split_phash_le4 += 1
            it1 = valid_items[id1]
            it2 = valid_items[id2]
            if it1['class'] != it2['class']:
                contradictory_phash_le4 += 1
                print(f"   [PHASH CONFLICT dist={dist}] {it1['split']} '{it1['class']}' vs {it2['split']} '{it2['class']}'")

    print(f"   Cross-split pHash <= 4 pairs:        {cross_split_phash_le4}")
    print(f"   Cross-split pHash <= 4 conflicts:    {contradictory_phash_le4}")

    # Summary Check
    print("\n" + "=" * 80)
    print("STEP 1 VERIFICATION RESULTS:")
    print(f"   - Exact duplicates across splits: {exact_cross_split_pairs} (Requirement: 0)")
    print(f"   - pHash <= 4 pairs across splits: {cross_split_phash_le4} (Requirement: 0)")
    print(f"   - Contradictory labels:           {exact_contradictory_pairs + contradictory_phash_le4} (Requirement: 0)")
    print("=" * 80)
    if exact_cross_split_pairs == 0 and cross_split_phash_le4 == 0 and (exact_contradictory_pairs + contradictory_phash_le4) == 0:
        print("[SUCCESS] All Step 1 criteria verified with 0 cross-split duplicates and 0 conflicts.")
    else:
        print("[FAILURE] Step 1 criteria not fully satisfied!")

if __name__ == '__main__':
    main()

