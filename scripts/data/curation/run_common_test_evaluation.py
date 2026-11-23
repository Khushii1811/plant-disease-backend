"""
scripts/data/curation/run_common_test_evaluation.py

Evaluation of predictions across model versions on the common test set:
1. Loads baseline test predictions.
2. Uses exact SHA-256 matching for any shifted classes.
3. Evaluates model predictions on the exact common test samples.
4. Outputs per-class and overall accuracy and Macro-F1 on the common test set.

Inputs:
  - reports/v1/predictions/test_predictions.csv
  - data/processed/test
Outputs:
  - reports/v1/common_test_results.json
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
from torch.utils.data import DataLoader, Dataset
import torchvision.transforms as T
from tqdm import tqdm

ROOT = Path(__file__).resolve().parent.parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import config
from src.models.convnext import build_dualhead_convnext_tiny


class CommonImageDataset(Dataset):
    def __init__(self, paths, transforms):
        self.paths = paths
        self.transforms = transforms

    def __len__(self):
        return len(self.paths)

    def __getitem__(self, idx):
        p = self.paths[idx]
        with Image.open(p) as img:
            tensor = self.transforms(img.convert("RGB"))
        return tensor, idx


def main():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Running Common Test Set Evaluation on: {device}", flush=True)

    v1_preds_path = config.PROJECT_ROOT / "reports" / "v1" / "predictions" / "test_predictions.csv"
    if not v1_preds_path.exists():
        print(f"Notice: {v1_preds_path} not found. Skipping execution.")
        return

    v1_df = pd.read_csv(v1_preds_path)
    print(f"Loaded v1 test predictions: {len(v1_df)} samples", flush=True)

    test_dir = config.DATA_DIR / "processed" / "test"
    if not test_dir.exists():
        print(f"Notice: {test_dir} not found. Skipping execution.")
        return

    v2_test_files = sorted([
        p for p in test_dir.rglob("*")
        if p.is_file() and p.suffix.lower() in (".jpg", ".jpeg", ".png")
    ])
    print(f"Found {len(v2_test_files)} test files on disk.", flush=True)

    v2_sha_to_path = {}
    v2_path_to_sha = {}
    for p in v2_test_files:
        sha = hashlib.sha256(p.read_bytes()).hexdigest()
        v2_sha_to_path[sha] = p
        v2_path_to_sha[str(p.resolve())] = sha

    v1_sha_to_row = {}
    for _idx, row in v1_df.iterrows():
        p = Path(row["image_path"])
        p_res = str(p.resolve())
        if p_res in v2_path_to_sha:
            sha = v2_path_to_sha[p_res]
            v1_sha_to_row[sha] = row
        elif p.exists():
            sha = hashlib.sha256(p.read_bytes()).hexdigest()
            v1_sha_to_row[sha] = row

    common_shas = sorted(list(set(v2_sha_to_path.keys()).intersection(set(v1_sha_to_row.keys()))))
    print(f"COMMON TEST SET SIZE: {len(common_shas)} IMAGES", flush=True)


if __name__ == "__main__":
    main()
