import csv
from pathlib import Path
from collections import defaultdict

processed = Path('data/processed')
splits = ['train', 'val', 'test']
image_exts = {'.jpg', '.jpeg', '.png', '.bmp', '.webp'}

counts = defaultdict(lambda: {s: 0 for s in splits})

for s in splits:
    split_dir = processed / s
    if split_dir.exists():
        for class_dir in split_dir.iterdir():
            if class_dir.is_dir():
                n_imgs = len([f for f in class_dir.iterdir() if f.is_file() and f.suffix.lower() in image_exts])
                counts[class_dir.name][s] = n_imgs

# Save to CSV
csv_path = Path('data/processed_class_counts.csv')
with open(csv_path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['class_name', 'train_count', 'val_count', 'test_count', 'total_count'])
    for cls in sorted(counts.keys()):
        tr = counts[cls]['train']
        va = counts[cls]['val']
        te = counts[cls]['test']
        writer.writerow([cls, tr, va, te, tr + va + te])

# Save to Markdown
md_path = Path('data/processed_class_counts.md')
total_tr = sum(v['train'] for v in counts.values())
total_va = sum(v['val'] for v in counts.values())
total_te = sum(v['test'] for v in counts.values())
grand_total = total_tr + total_va + total_te

lines = []
lines.append('# 📊 Processed Dataset Class Counts (Train / Val / Test)\n')
lines.append(f'> **Total Classes**: {len(counts)} | **Train**: {total_tr:,} | **Val**: {total_va:,} | **Test**: {total_te:,} | **Grand Total**: {grand_total:,}\n')
lines.append('| # | Class Name | Train | Val | Test | Total |')
lines.append('| :--- | :--- | :---: | :---: | :---: | :---: |')

for idx, cls in enumerate(sorted(counts.keys()), 1):
    tr = counts[cls]['train']
    va = counts[cls]['val']
    te = counts[cls]['test']
    tot = tr + va + te
    lines.append(f'| {idx} | **{cls}** | {tr:,} | {va:,} | {te:,} | {tot:,} |')

with open(md_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))

print(f'Done! Processed {len(counts)} classes.')
print(f'Train Total: {total_tr:,}')
print(f'Val Total  : {total_va:,}')
print(f'Test Total : {total_te:,}')
print(f'Grand Total: {grand_total:,}')
print(f'Files saved: {csv_path} & {md_path}')
