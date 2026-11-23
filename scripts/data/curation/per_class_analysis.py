"""
scripts/per_class_analysis.py - Per-class accuracy analysis for ConvNeXt-Tiny.

Reads classification_report_tta_model_convnext_tiny.json and maps numeric
class indices to real class names, then prints a full performance breakdown.

Usage:
    python scripts/per_class_analysis.py
"""

import json
import sys
from pathlib import Path

# Force UTF-8 output on Windows to avoid cp1252 encoding errors
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]

# -- Load report --------------------------------------------------------------
report_path = Path("models/classification_report_tta_model_convnext_tiny.json")
with open(report_path) as f:
    report = json.load(f)

# -- Load class names (same sorted order used during training) ----------------
classes = sorted([d.name for d in Path("data/processed/train").iterdir() if d.is_dir()])

# -- Parse per-class metrics --------------------------------------------------
rows = []
for idx, name in enumerate(classes):
    r = report.get(str(idx), {})
    f1   = r.get("f1-score",  0.0)
    prec = r.get("precision", 0.0)
    rec  = r.get("recall",    0.0)
    sup  = int(r.get("support", 0))
    rows.append((f1, prec, rec, sup, name))

rows_by_f1_asc = sorted(rows, key=lambda x: x[0])

# -- Overall metrics ----------------------------------------------------------
overall_acc = report["accuracy"]
macro_f1    = report["macro avg"]["f1-score"]
weighted_f1 = report["weighted avg"]["f1-score"]
total_sup   = int(report["macro avg"]["support"])

perfect    = [r for r in rows if r[0] >= 0.999]
excellent  = [r for r in rows if 0.90 <= r[0] < 0.999]
good       = [r for r in rows if 0.75 <= r[0] < 0.90]
struggling = [r for r in rows if 0.40 <= r[0] < 0.75]
failing    = [r for r in rows if r[0] < 0.40]

HDR = f"{'F1':>6}  {'Prec':>6}  {'Rec':>6}  {'Sup':>5}  Class"
SEP = "-" * 85

print("=" * 85)
print("  PER-CLASS ACCURACY ANALYSIS -- ConvNeXt-Tiny (TTA evaluation)")
print("=" * 85)
print(f"  Overall accuracy  : {overall_acc * 100:.2f}%  ({int(overall_acc * total_sup)} / {total_sup} correct)")
print(f"  Macro F1          : {macro_f1 * 100:.2f}%")
print(f"  Weighted F1       : {weighted_f1 * 100:.2f}%")
print(f"  Total classes     : {len(classes)}")
print("=" * 85)

print()
print("-- PERFORMANCE TIER DISTRIBUTION --")
print(f"  PERFECT    (F1 >= 99%) : {len(perfect):>3} classes")
print(f"  EXCELLENT  (F1 90-99%) : {len(excellent):>3} classes")
print(f"  GOOD       (F1 75-90%) : {len(good):>3} classes")
print(f"  STRUGGLING (F1 40-75%) : {len(struggling):>3} classes")
print(f"  FAILING    (F1  < 40%) : {len(failing):>3} classes")

print()
print("-- WORST 25 CLASSES (lowest F1 -- highest priority for improvement) --")
print(f"  {'#':<4}  {HDR}")
print(f"  {SEP}")
for rank, (f1, prec, rec, sup, name) in enumerate(rows_by_f1_asc[:25], 1):
    tag = "  <-- ZERO F1" if f1 == 0.0 else ""
    print(f"  {rank:<4}  {f1*100:>5.1f}%  {prec*100:>5.1f}%  {rec*100:>5.1f}%  {sup:>5}  {name}{tag}")

print()
print("-- STRUGGLING CLASSES (F1 40-75%) --")
print(f"  {'#':<4}  {HDR}")
print(f"  {SEP}")
for rank, (f1, prec, rec, sup, name) in enumerate(sorted(struggling, key=lambda x: x[0]), 1):
    print(f"  {rank:<4}  {f1*100:>5.1f}%  {prec*100:>5.1f}%  {rec*100:>5.1f}%  {sup:>5}  {name}")

print()
print("-- PERFECT CLASSES (F1 = 100%) --")
print(f"  {'#':<4}  {HDR}")
print(f"  {SEP}")
for rank, (f1, prec, rec, sup, name) in enumerate(sorted(perfect, key=lambda x: x[4]), 1):
    print(f"  {rank:<4}  {f1*100:>5.1f}%  {prec*100:>5.1f}%  {rec*100:>5.1f}%  {sup:>5}  {name}")

# Small-support classes with low accuracy (data starvation candidates)
small_poor = [(f1, prec, rec, sup, name) for (f1, prec, rec, sup, name) in rows if sup < 10 and f1 < 0.60]
print()
print("-- WARNING: SMALL SUPPORT + LOW ACCURACY (sup < 10, F1 < 60%) -- likely data starvation --")
print(f"  {'#':<4}  {HDR}")
print(f"  {SEP}")
for rank, (f1, prec, rec, sup, name) in enumerate(sorted(small_poor, key=lambda x: x[0]), 1):
    print(f"  {rank:<4}  {f1*100:>5.1f}%  {prec*100:>5.1f}%  {rec*100:>5.1f}%  {sup:>5}  {name}")

print()
print("=" * 85)
