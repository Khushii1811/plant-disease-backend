#!/usr/bin/env python3
"""
scripts/download_weights.py

Downloads and validates the production ConvNeXt-Tiny DualHead model weights
for the Hale plant leaf disease classification benchmark (v1.0 release).

Expected Model Checksum:
  Target File: models/v1/model_dualhead_convnext_tiny.pth
  SHA-256:     3bb5785efa957a5fd4eb9d071fa92ff57adbef9788275a810e9cce99cf016dcb
"""

import sys
import os
import hashlib
import urllib.request
from pathlib import Path

# Commented production release asset URL (fill in after creating GitHub Release):
# RELEASE_URL = "https://github.com/Khushii1811/plant-disease-backend/releases/download/v1.0.0/model_dualhead_convnext_tiny.pth"
RELEASE_URL = None

EXPECTED_SHA256 = "3bb5785efa957a5fd4eb9d071fa92ff57adbef9788275a810e9cce99cf016dcb"
TARGET_PATH = Path("models/v1/model_dualhead_convnext_tiny.pth")


def compute_sha256(path: Path) -> str:
    """Computes SHA-256 checksum in 64 KB chunks."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    root = Path(__file__).resolve().parent.parent
    os.chdir(root)
    target = root / TARGET_PATH

    print(f"Target weights path: {target}")

    if target.exists():
        print(f"Local file found ({target.stat().st_size / (1024*1024):.2f} MB). Verifying SHA-256...")
        digest = compute_sha256(target)
        if digest == EXPECTED_SHA256:
            print("SHA-256 checksum verified successfully:")
            print(f"  {digest} == {EXPECTED_SHA256}")
            print("Weights are verified and ready for inference.")
            sys.exit(0)
        else:
            print("WARNING: Checksum mismatch for local file:")
            print(f"  Found:    {digest}")
            print(f"  Expected: {EXPECTED_SHA256}")

    if not RELEASE_URL:
        print("\nNotice: RELEASE_URL is currently unset.")
        print(f"Please download 'model_dualhead_convnext_tiny.pth' from GitHub Releases")
        print(f"and place it at '{target}'.")
        print(f"Expected SHA-256: {EXPECTED_SHA256}")
        sys.exit(1)

    print(f"Downloading from {RELEASE_URL}...")
    target.parent.mkdir(parents=True, exist_ok=True)
    temp_target = target.with_suffix(".tmp")
    urllib.request.urlretrieve(RELEASE_URL, temp_target)

    digest = compute_sha256(temp_target)
    if digest == EXPECTED_SHA256:
        temp_target.replace(target)
        print("Download complete and SHA-256 verified successfully.")
        sys.exit(0)
    else:
        temp_target.unlink(missing_ok=True)
        print("ERROR: Downloaded file checksum mismatch.")
        print(f"  Found:    {digest}")
        print(f"  Expected: {EXPECTED_SHA256}")
        sys.exit(1)


if __name__ == "__main__":
    main()
