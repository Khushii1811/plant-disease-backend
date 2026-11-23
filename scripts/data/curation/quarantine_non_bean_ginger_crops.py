import os
import sys
import json
import shutil
import hashlib
from pathlib import Path
from collections import defaultdict

# Force UTF-8 on Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROC_DIR = PROJECT_ROOT / "data" / "processed"
AUDIT_FILE = PROJECT_ROOT / "data" / "raw" / "comprehensive_crop_audit_manifest.json"
QUARANTINE_DIR = PROJECT_ROOT / "data" / "raw" / "quarantine_non_bean_ginger_cropped_images"

def calculate_md5(file_path):
    hasher = hashlib.md5()
    with open(file_path, "rb") as f:
        while chunk := f.read(64 * 1024):
            hasher.update(chunk)
    return hasher.hexdigest()

def main():
    print("=" * 80)
    print("📦 QUARANTINING NON-BEAN / NON-GINGER CROPPED IMAGES")
    print(f"   Destination: {QUARANTINE_DIR}")
    print("=" * 80)

    if not AUDIT_FILE.exists():
        print(f"❌ Error: Audit manifest {AUDIT_FILE} not found.")
        sys.exit(1)

    with open(AUDIT_FILE, "r", encoding="utf-8") as f:
        audit_data = json.load(f)

    records = audit_data.get("records", [])

    # Filter: Keep Bean and Ginger, remove rest
    to_remove = []
    to_keep = []

    for r in records:
        cls_lower = r["class"].lower()
        if "bean" in cls_lower or "ginger" in cls_lower:
            to_keep.append(r)
        else:
            to_remove.append(r)

    print(f"📋 Total audited records:  {len(records)}")
    print(f"   • Kept intact (Bean & Ginger): {len(to_keep)}")
    print(f"   • To remove & quarantine:      {len(to_remove)}")

    QUARANTINE_DIR.mkdir(parents=True, exist_ok=True)

    quarantined_records = []
    removed_count = 0
    by_class_count = defaultdict(int)

    for item in to_remove:
        rel_proc = item["processed_path"]
        proc_file = PROJECT_ROOT / rel_proc

        if not proc_file.exists():
            print(f"   ⚠️ File not found: {rel_proc}")
            continue

        file_md5 = calculate_md5(proc_file)

        dest_folder = QUARANTINE_DIR / item["split"] / item["class"]
        dest_folder.mkdir(parents=True, exist_ok=True)
        dest_file = dest_folder / proc_file.name

        shutil.move(str(proc_file), str(dest_file))
        removed_count += 1
        by_class_count[item["class"]] += 1

        quarantined_records.append({
            "class": item["class"],
            "split": item["split"],
            "filename": proc_file.name,
            "md5": file_md5,
            "processed_size": item["processed_size"],
            "raw_size": item["raw_size"],
            "diff_w": item["diff_w"],
            "diff_h": item["diff_h"],
            "original_processed_path": rel_proc,
            "quarantine_path": str(dest_file.relative_to(PROJECT_ROOT))
        })

    # Save quarantine manifest
    manifest_path = QUARANTINE_DIR / "manifest.json"
    manifest_content = {
        "timestamp": audit_data.get("timestamp"),
        "total_quarantined": removed_count,
        "classes_affected_count": len(by_class_count),
        "reason": "Accidentally cropped images from Apple, Cabbage, Corn, and Broccoli permanently removed per user decision. Bean and Ginger classes were explicitly kept intact as is.",
        "by_class_count": dict(by_class_count),
        "records": quarantined_records
    }

    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest_content, f, indent=2)

    print("\n" + "=" * 80)
    print("✅ REMOVAL & QUARANTINE COMPLETED")
    print("=" * 80)
    print(f"Total images removed and quarantined: {removed_count} / {len(to_remove)}")
    print(f"Manifest written to: {manifest_path}")
    print("\nBreakdown of removed images:")
    for cls_name, cnt in sorted(by_class_count.items(), key=lambda x: x[1], reverse=True):
        print(f"   • {cls_name:35s}: {cnt} removed")
    print("=" * 80)

if __name__ == "__main__":
    main()
