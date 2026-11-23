"""
scripts/data/curation/prepare_p001_quarantine.py

Prepares Patch P-001: De-lists and quarantines the 3 Bell Pepper classes
overlapping with the Chilli dataset (Decision 59 / ADR-035) to transition
the benchmark from 198 to 195 clean classes.

DRY-RUN ONLY: Writes data/patches/P-001_bell_pepper_quarantine_PLAN.csv
Does NOT execute any file moves.
"""

import os
import sys
import argparse
from pathlib import Path
from collections import Counter
import pandas as pd

# Ensure line-buffered UTF-8 output on Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)
    sys.stderr.reconfigure(encoding="utf-8", line_buffering=True)

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
import config

TARGET_CLASSES = [
    "Bell Pepper - Leaf Curl Virus",
    "Bell Pepper - Nutrition Deficiency",
    "Bell Pepper - bell pepper powdery mildew"
]

EXPECTED_COUNTS = {
    "train": 196,
    "val": 26,
    "test": 31,
    "total": 253
}

def prepare_p001_quarantine(manifest_csv: Path, output_plan_csv: Path):
    print("=" * 80)
    print("PREPARING PATCH P-001 (BELL PEPPER CHILLI OVERLAP QUARANTINE)")
    print("   Mode: DRY-RUN ONLY (ZERO FILES MOVED)")
    print(f"   Manifest: {manifest_csv}")
    print(f"   Plan:     {output_plan_csv}")
    print("=" * 80)

    if not manifest_csv.exists():
        print(f"[ERROR] Manifest not found at: {manifest_csv}")
        sys.exit(1)

    df_manifest = pd.read_csv(manifest_csv)
    sub = df_manifest[df_manifest["class"].isin(TARGET_CLASSES)].copy()

    print(f"\n[1/3] Found {len(sub):,} images across {len(TARGET_CLASSES)} target classes.")

    # Breakdown per class and split
    print("\n[2/3] Planned Quarantine Images per Class and Split:")
    print("-" * 80)
    breakdown = sub.groupby(["class", "split"]).size().unstack(fill_value=0)
    breakdown["total"] = breakdown.sum(axis=1)
    print(breakdown.to_string())
    print("-" * 80)

    # Split totals
    split_counts = sub.groupby("split").size().to_dict()
    total_imgs = len(sub)
    print(f"\nActual Quarantine Totals by Split:")
    print(f"   Train: {split_counts.get('train', 0):4d} (Expected: {EXPECTED_COUNTS['train']:4d}) -> {'MATCH' if split_counts.get('train', 0) == EXPECTED_COUNTS['train'] else 'MISMATCH'}")
    print(f"   Val:   {split_counts.get('val', 0):4d} (Expected: {EXPECTED_COUNTS['val']:4d}) -> {'MATCH' if split_counts.get('val', 0) == EXPECTED_COUNTS['val'] else 'MISMATCH'}")
    print(f"   Test:  {split_counts.get('test', 0):4d} (Expected: {EXPECTED_COUNTS['test']:4d}) -> {'MATCH' if split_counts.get('test', 0) == EXPECTED_COUNTS['test'] else 'MISMATCH'}")
    print(f"   TOTAL: {total_imgs:4d} (Expected: {EXPECTED_COUNTS['total']:4d}) -> {'MATCH' if total_imgs == EXPECTED_COUNTS['total'] else 'MISMATCH'}")

    # Generate Plan CSV
    print(f"\n[3/3] Writing Plan CSV: {output_plan_csv}...")
    plan_rows = []
    for idx, r in sub.iterrows():
        plan_rows.append({
            "sha256": r["image_id"],
            "path": r["path"],
            "class": r["class"],
            "source": r["source"],
            "from_split": r["split"],
            "to_split": "quarantine_bell_pepper_chilli_overlap",
            "reason": "Decision 59 / ADR-035: Quarantine Bell Pepper classes overlapping with Chilli dataset"
        })

    output_plan_csv.parent.mkdir(parents=True, exist_ok=True)
    df_plan = pd.DataFrame(plan_rows)
    df_plan.to_csv(output_plan_csv, index=False)
    print(f"   [OK] Wrote {len(df_plan)} actions to {output_plan_csv}")

    print("\n" + "=" * 80)
    print("P-001 DRY-RUN COMPLETE: Zero files moved. Waiting for author approval.")
    print("=" * 80)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Prepare P-001 quarantine plan.")
    parser.add_argument("--manifest-csv", type=Path, default=config.DATA_DIR / "manifests/dataset_v1.csv", help="Path to dataset_v1.csv")
    parser.add_argument("--output-plan", type=Path, default=config.DATA_DIR / "patches/P-001_bell_pepper_quarantine_PLAN.csv", help="Output plan CSV")
    args = parser.parse_args()

    prepare_p001_quarantine(args.manifest_csv, args.output_plan)
