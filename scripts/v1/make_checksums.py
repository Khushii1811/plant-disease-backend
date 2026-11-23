"""
scripts/v1/make_checksums.py

Generates or regenerates models/v1/checksums.txt.
Hashes all files in models/v1/ (excluding checksums.txt).
"""

import sys
import hashlib
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


def get_file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def generate_checksums():
    v1_dir = PROJECT_ROOT / "models" / "v1"
    checksum_file = v1_dir / "checksums.txt"

    lines = []
    # Consistent ordering matching release convention
    desired_order = [
        "model_dualhead_convnext_tiny.pth",
        "class_names.json",
        "class_to_idx.json",
        "idx_to_class.json",
        "crop_hierarchy.json",
        "calibration.json",
        "preprocess.json",
        "model_card.md",
        "provenance.json",
    ]

    for fname in desired_order:
        fpath = v1_dir / fname
        if fpath.exists():
            sha = get_file_sha256(fpath)
            lines.append(f"{sha}  {fname}")
        else:
            print(f"[WARNING] Missing expected file: {fname}")

    # Check for any extra files
    for f in sorted(v1_dir.iterdir()):
        if f.is_file() and f.name not in desired_order and f.name != "checksums.txt":
            sha = get_file_sha256(f)
            lines.append(f"{sha}  {f.name}")

    checksum_file.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"[DONE] Successfully generated {checksum_file} with {len(lines)} files:")
    for line in lines:
        print(f"  {line}")


if __name__ == "__main__":
    generate_checksums()


if __name__ == "__main__":
    generate_checksums()
