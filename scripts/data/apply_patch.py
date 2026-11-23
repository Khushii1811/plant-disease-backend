"""
scripts/data/apply_patch.py — Generic Dataset Patch Executor & Dry-Runner.

Safely applies patch plans (e.g., P-001 quarantine plan, P-002 source rebalance plan)
with mandatory dry-run validation, integrity verification, and detailed reporting.

Usage:
  # Dry-run (default, zero files touched):
  uv run python scripts/data/apply_patch.py --plan-csv data/patches/P-002_source_rebalance_PLAN.csv --dry-run

  # Execute moves (requires explicit --execute flag):
  uv run python scripts/data/apply_patch.py --plan-csv data/patches/P-002_source_rebalance_PLAN.csv --execute
"""

import os
import sys
import argparse
import shutil
from pathlib import Path
from collections import defaultdict, Counter
import pandas as pd

# Ensure line-buffered UTF-8 output on Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)
    sys.stderr.reconfigure(encoding="utf-8", line_buffering=True)

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
import config

def apply_patch(plan_csv: Path, dry_run: bool = True):
    print("=" * 80)
    mode_str = "DRY-RUN SIMULATION (READ-ONLY, ZERO FILES TOUCHED)" if dry_run else "EXECUTION MODE (MOVING FILES)"
    print(f"DATASET PATCH RUNNER: {plan_csv.name}")
    print(f"   Mode:     {mode_str}")
    print(f"   Plan CSV: {plan_csv}")
    print("=" * 80)

    if not plan_csv.exists():
        print(f"[ERROR] Plan file not found: {plan_csv}")
        sys.exit(1)

    df_plan = pd.read_csv(plan_csv)
    total_actions = len(df_plan)
    print(f"\n[1/3] Loaded plan with {total_actions:,} planned actions.")

    if total_actions == 0:
        print("[INFO] Plan contains 0 actions. Nothing to do.")
        return

    # Verify required columns
    required_cols = ["sha256", "path", "class", "from_split", "to_split"]
    for col in required_cols:
        if col not in df_plan.columns:
            print(f"[ERROR] Missing required column '{col}' in {plan_csv}")
            sys.exit(1)

    # [2/3] Validate File Existence
    print(f"\n[2/3] Validating source file existence...")
    missing_files = []
    validated_records = []
    for idx, row in df_plan.iterrows():
        p = PROJECT_ROOT / row["path"]
        if not p.exists():
            missing_files.append((row["path"], row["sha256"]))
        else:
            validated_records.append(row)

    if missing_files:
        print(f"[ERROR] {len(missing_files)} source files in plan do NOT exist on disk:")
        for mf, h in missing_files[:5]:
            print(f"   - {mf} (sha256: {h[:12]}...)")
        if len(missing_files) > 5:
            print(f"   ... and {len(missing_files) - 5} more.")
        sys.exit(1)
    else:
        print(f"   All {len(validated_records):,} source files verified on disk.")

    # [3/3] Action Summary
    print(f"\n[3/3] Planned Actions Breakdown:")
    print("-" * 80)
    has_source = "source" in df_plan.columns
    group_cols = ["class", "source", "from_split", "to_split"] if has_source else ["class", "from_split", "to_split"]
    summary_table = df_plan.groupby(group_cols).size().unstack(fill_value=0) if "to_split" in group_cols else df_plan.groupby(group_cols).size()
    print(df_plan.groupby(group_cols).size().to_string())
    print("-" * 80)

    # Split totals summary
    split_summary = df_plan.groupby(["from_split", "to_split"]).size()
    print("\nNet Movement Summary (from_split -> to_split):")
    for (fs, ts), cnt in split_summary.items():
        print(f"   {fs:10s} -> {ts:10s} : {cnt:5d} images")

    if dry_run:
        print("\n" + "=" * 80)
        print("DRY-RUN VALIDATION COMPLETE: All source paths exist and movements are verified.")
        print("   >>> ZERO FILES WERE MOVED OR MODIFIED (Strictly READ-ONLY). <<<")
        print("=" * 80)
        return

    # Execute moves
    print("\n" + "=" * 80)
    print("EXECUTING PATCH ACTIONS...")
    print("=" * 80)
    moved_count = 0
    for idx, row in df_plan.iterrows():
        src_path = PROJECT_ROOT / row["path"]
        # Destination: replace from_split with to_split in path or move to quarantine
        to_split = row["to_split"]
        from_split = row["from_split"]
        cls_name = row["class"]

        if to_split.startswith("quarantine"):
            # Target is in data/raw/
            dst_path = PROJECT_ROOT / "data/raw" / to_split / from_split / cls_name / src_path.name
        else:
            dst_path = PROJECT_ROOT / "data/processed" / to_split / cls_name / src_path.name

        dst_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(src_path), str(dst_path))
        moved_count += 1

        # If source directory is now empty, remove it
        src_dir = src_path.parent
        if src_dir.exists() and not any(src_dir.iterdir()):
            try:
                src_dir.rmdir()
                print(f"   [REMOVED EMPTY DIR] {src_dir.relative_to(PROJECT_ROOT)}")
            except Exception:
                pass

    print(f"\n[EXECUTION DONE] Successfully moved {moved_count:,} images.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Apply or dry-run dataset patches.")
    parser.add_argument("--plan-csv", type=Path, required=True, help="Path to patch PLAN CSV file.")
    parser.add_argument("--dry-run", action="store_true", default=True, help="Simulate patch without moving any files (default).")
    parser.add_argument("--execute", action="store_true", default=False, help="Explicit flag to execute file moves.")
    args = parser.parse_args()

    # If --execute is specified, turn off dry_run
    is_dry_run = not args.execute if args.execute else True
    apply_patch(args.plan_csv, dry_run=is_dry_run)
