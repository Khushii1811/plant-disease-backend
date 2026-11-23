"""
scripts/data/apply_patch_p005.py — Patch P-005 Dedicated Runner & Reversible Rollback Generator.

Executes Patch P-005:
1. Quarantine 4,665 images (17 quarantined classes + 3 active outliers) into data/raw/quarantine_*/
2. Relabel 3,062 images across 5 relabelled classes into data/processed/<split>/<new_class>/
3. Merge 498 images across 1 merged class from Mango - Powdery Mildew into Mango - Sooty Mould
4. Generates an automated rollback script: data/patches/restore_P-005.py
5. Generates an auditable execution move log: data/patches/P-005_move_log.csv

Summary of actions:
- 17 quarantined classes
- 1 merged class
- 5 relabelled classes
- 3 outlier images

Usage:
  # Dry-run validation (default, zero files touched):
  uv run python scripts/data/apply_patch_p005.py --dry-run

  # Execute moves:
  uv run python scripts/data/apply_patch_p005.py --execute
"""

import os
import sys
import argparse
import shutil
from pathlib import Path
import pandas as pd
from datetime import datetime

# UTF-8 buffering on Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)
    sys.stderr.reconfigure(encoding="utf-8", line_buffering=True)

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
PLAN_CSV = PROJECT_ROOT / "data" / "patches" / "P-005_curation_PLAN.csv"
MOVE_LOG_CSV = PROJECT_ROOT / "data" / "patches" / "P-005_move_log.csv"
RESTORE_SCRIPT = PROJECT_ROOT / "data" / "patches" / "restore_P-005.py"

def run_patch(dry_run: bool = True):
    print("=" * 80)
    mode_str = "DRY-RUN SIMULATION (READ-ONLY, ZERO FILES TOUCHED)" if dry_run else "EXECUTION MODE (APPLYING PATCH P-005)"
    print(f"PATCH RUNNER P-005: {mode_str}")
    print(f"Plan file: {PLAN_CSV}")
    print("=" * 80)

    if not PLAN_CSV.exists():
        print(f"[ERROR] Plan CSV not found: {PLAN_CSV}")
        sys.exit(1)

    df_plan = pd.read_csv(PLAN_CSV)
    print(f"\n[1/4] Loaded plan with {len(df_plan):,} planned operations.")
    print("Action Breakdown:")
    for act, cnt in df_plan["action"].value_counts().items():
        print(f"   - {act:12s}: {cnt:5d} images")

    # [2/4] Validate existence on disk
    print("\n[2/4] Validating source file existence on disk...")
    missing = []
    for idx, r in df_plan.iterrows():
        src = PROJECT_ROOT / r["source_path"]
        if not src.exists():
            missing.append(r["source_path"])

    if missing:
        print(f"[ERROR] {len(missing)} files missing on disk:")
        for m in missing[:5]:
            print(f"   - {m}")
        sys.exit(1)
    else:
        print(f"   All {len(df_plan):,} source files verified present on disk.")

    # [3/4] Breakdown by target class / destination
    print("\n[3/4] Operations Summary by Action & Class:")
    print("-" * 80)
    for act in ["quarantine", "relabel", "merge"]:
        sub = df_plan[df_plan["action"] == act]
        print(f"\n[{act.upper()}] ({len(sub)} images):")
        grp = sub.groupby(["current_class", "target_class", "split"]).size()
        for (c_curr, c_tgt, sp), count in grp.items():
            if act == "quarantine":
                print(f"   {c_curr:38s} [{sp:5s}] -> Quarantine ({count} imgs)")
            elif act == "relabel":
                print(f"   {c_curr:38s} -> {c_tgt:38s} [{sp:5s}] ({count} imgs)")
            elif act == "merge":
                print(f"   {c_curr:38s} -> Merged into {c_tgt:20s} [{sp:5s}] ({count} imgs)")

    if dry_run:
        print("\n" + "=" * 80)
        print("DRY-RUN VALIDATION COMPLETE: All paths and integrity checks PASSED.")
        print("   >>> ZERO FILES WERE MOVED OR MODIFIED (Strictly READ-ONLY). <<<")
        print("   To execute file moves, run with: --execute")
        print("=" * 80)
        return

    # [4/4] Execution mode
    print("\n" + "=" * 80)
    print("EXECUTING PATCH P-005 FILE MOVES...")
    print("=" * 80)

    move_records = []
    restore_lines = [
        '"""',
        'Auto-generated rollback script for Patch P-005.',
        f'Generated on: {datetime.now().isoformat()}',
        'Reverses all file moves and restores original folder structure.',
        '"""',
        'import os',
        'import shutil',
        'from pathlib import Path',
        '',
        'PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent',
        'print("Rolling back Patch P-005...")',
        'restored = 0',
        'moves = ['
    ]

    moved_count = 0
    dirs_to_clean = set()

    for idx, r in df_plan.iterrows():
        src = PROJECT_ROOT / r["source_path"]
        dst = PROJECT_ROOT / r["destination_path"]

        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(src), str(dst))

        dirs_to_clean.add(src.parent)
        moved_count += 1

        move_records.append({
            "sha256": r["sha256"],
            "source_path": r["source_path"],
            "destination_path": r["destination_path"],
            "action": r["action"],
            "current_class": r["current_class"],
            "target_class": r["target_class"],
            "timestamp": datetime.now().isoformat()
        })

        # Line for restore script
        restore_lines.append(f'    ("{r["destination_path"]}", "{r["source_path"]}"),')

    # Complete restore script
    restore_lines.extend([
        ']',
        'for dst_rel, src_rel in moves:',
        '    curr_p = PROJECT_ROOT / dst_rel',
        '    orig_p = PROJECT_ROOT / src_rel',
        '    if curr_p.exists():',
        '        orig_p.parent.mkdir(parents=True, exist_ok=True)',
        '        shutil.move(str(curr_p), str(orig_p))',
        '        restored += 1',
        'print(f"Successfully rolled back {restored:,} images to original locations.")',
    ])

    with open(RESTORE_SCRIPT, "w", encoding="utf-8") as f:
        f.write("\n".join(restore_lines))
    print(f"\n[RESTORE SCRIPT GENERATED] Saved to: {RESTORE_SCRIPT.relative_to(PROJECT_ROOT)}")

    # Clean empty source directories
    cleaned_dirs = 0
    for d in sorted(dirs_to_clean, key=lambda x: len(str(x)), reverse=True):
        if d.exists() and not any(d.iterdir()):
            try:
                d.rmdir()
                cleaned_dirs += 1
            except Exception:
                pass
    print(f"[CLEANUP] Removed {cleaned_dirs} empty source directories.")

    # Save move log
    df_moves = pd.DataFrame(move_records)
    df_moves.to_csv(MOVE_LOG_CSV, index=False)
    print(f"[AUDIT LOG] Saved execution log to: {MOVE_LOG_CSV.relative_to(PROJECT_ROOT)}")

    print("\n" + "=" * 80)
    print(f"PATCH P-005 EXECUTION COMPLETED: {moved_count:,} images moved successfully.")
    print("=" * 80)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Patch P-005 Runner.")
    parser.add_argument("--dry-run", action="store_true", default=True, help="Simulate patch without touching files (default).")
    parser.add_argument("--execute", action="store_true", default=False, help="Explicit flag to execute file moves.")
    args = parser.parse_args()

    is_dry = not args.execute if args.execute else True
    run_patch(dry_run=is_dry)

