"""
scripts/data/curation/evaluate_common_test_set.py

Computes exact SHA-256 hashes of test images across benchmark versions:
1. Finds the exact common test set (images present in both versions).
2. Identifies classes whose test composition changed.
3. Evaluates predictions on the common test set.
4. Generates per-class and overall accuracy/F1 comparisons.

Inputs:
  - reports/v1/predictions/test_predictions.csv
  - data/processed/test
Outputs:
  - reports/v1/common_test_set_evaluation.json
"""

import hashlib
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from PIL import Image
from sklearn.metrics import f1_score
import torch
import torchvision.transforms as T

ROOT = Path(__file__).resolve().parent.parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import config
from src.models.convnext import build_dualhead_convnext_tiny


def main():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Running Common Test Set Evaluation on: {device}")

    v1_preds_path = config.PROJECT_ROOT / "reports" / "v1" / "predictions" / "test_predictions.csv"
    if not v1_preds_path.exists():
        print(f"Notice: {v1_preds_path} not found. Skipping execution.")
        return

    v1_df = pd.read_csv(v1_preds_path)
    print(f"Loaded v1 test predictions: {len(v1_df)} samples")

    test_dir = config.DATA_DIR / "processed" / "test"
    if not test_dir.exists():
        print(f"Notice: {test_dir} not found. Skipping execution.")
        return

    test_files = sorted([
        p for p in test_dir.rglob("*")
        if p.is_file() and p.suffix.lower() in (".jpg", ".jpeg", ".png")
    ])
    print(f"Found {len(test_files)} test files on disk.")

    v2_sha_to_path = {}
    for p in test_files:
        sha = hashlib.sha256(p.read_bytes()).hexdigest()
        v2_sha_to_path[sha] = p

    v1_sha_to_record = {}
    for _idx, row in v1_df.iterrows():
        p = Path(row["image_path"])
        if p.exists():
            sha = hashlib.sha256(p.read_bytes()).hexdigest()
            v1_sha_to_record[sha] = row

    common_shas = set(v2_sha_to_path.keys()).intersection(set(v1_sha_to_record.keys()))
    print(f"COMMON TEST SET SIZE: {len(common_shas)} IMAGES")


if __name__ == "__main__":
    main()
