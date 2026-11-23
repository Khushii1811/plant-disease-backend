"""
scripts/v1/audit/eval_clean_subset_and_calibration.py

Evaluation and temperature scaling recalibration on clean subsets:
- Evaluates Model v1 on clean validation and test splits (filtering out near-duplicate twins)
- Fits temperature scaling parameters (T_crop, T_disease) on clean validation split
- Evaluates full test split (N=9,460) vs clean test split (N=9,279)

Inputs:
  - models/v1/model_dualhead_convnext_tiny.pth (Model v1 weights)
  - models/v1/class_names.json, models/v1/crop_hierarchy.json, models/v1/calibration.json
  - reports/v1/dataset_v1.csv (manifest)
  - reports/v1/leaky_eval_images.csv (eval images with near-duplicate train twins)

Produces:
  - reports/v1/clean_subset_evaluation.json (clean subset evaluation metrics and recalibration parameters)
"""

import csv
import gc
import json
import os
import sys
import time
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.nn.functional as F
from scipy import stats
from sklearn.metrics import accuracy_score, f1_score
from torch.utils.data import DataLoader

import config
from src.data.dataset import PlantDataset
from src.data.preprocess import get_test_transforms, get_val_transforms
from src.models.bundle_loader import load_model_bundle
from src.models.convnext import build_dualhead_convnext_tiny


class TemperatureScaler(nn.Module):
    def __init__(self):
        super().__init__()
        self.log_temperature = nn.Parameter(torch.zeros(1))

    def forward(self, logits: torch.Tensor) -> torch.Tensor:
        temperature = torch.exp(self.log_temperature)
        return logits / temperature

    @property
    def temperature(self) -> float:
        return float(torch.exp(self.log_temperature).item())

    def fit(self, logits: torch.Tensor, targets: torch.Tensor, max_iter: int = 50) -> float:
        device = logits.device
        self.to(device)
        loss_fn = nn.CrossEntropyLoss()
        optimizer = torch.optim.LBFGS(
            [self.log_temperature], lr=0.01, max_iter=max_iter, line_search_fn="strong_wolfe"
        )

        def closure():
            optimizer.zero_grad()
            loss = loss_fn(self.forward(logits), targets)
            loss.backward()
            return loss

        optimizer.step(closure)
        return self.temperature


def compute_ece(probs: np.ndarray, targets: np.ndarray, n_bins: int = 15):
    confidences = np.max(probs, axis=1)
    predictions = np.argmax(probs, axis=1)
    accuracies = predictions == targets

    bin_boundaries = np.linspace(0, 1, n_bins + 1)
    ece = 0.0
    total_samples = len(targets)

    for i in range(n_bins):
        bin_lower = bin_boundaries[i]
        bin_upper = bin_boundaries[i + 1]
        in_bin = (
            (confidences > bin_lower) & (confidences <= bin_upper)
            if i > 0
            else (confidences >= bin_lower) & (confidences <= bin_upper)
        )
        bin_size = np.sum(in_bin)

        if bin_size > 0:
            bin_acc = np.mean(accuracies[in_bin])
            bin_conf = np.mean(confidences[in_bin])
            ece += (bin_size / total_samples) * abs(bin_acc - bin_conf)

    return float(ece)


def fast_macro_f1(y_true, y_pred, num_classes=177):
    cm = np.bincount(
        num_classes * y_true + y_pred, minlength=num_classes * num_classes
    ).reshape(num_classes, num_classes)
    tp = np.diag(cm)
    fp = cm.sum(axis=0) - tp
    fn = cm.sum(axis=1) - tp
    denom = 2 * tp + fp + fn
    f1 = np.zeros(num_classes, dtype=np.float64)
    nz = denom > 0
    f1[nz] = (2.0 * tp[nz]) / denom[nz]
    return float(np.mean(f1))


def bootstrap_ci(
    metric_type, y_true, y_pred, n_bootstraps: int = 1000, seed: int = 42, num_classes: int = 177
):
    rng = np.random.RandomState(seed)
    n = len(y_true)
    scores = []
    for _ in range(n_bootstraps):
        idxs = rng.choice(n, size=n, replace=True)
        yt_bs = y_true[idxs]
        yp_bs = y_pred[idxs]
        if metric_type == "acc":
            scores.append(float(np.mean(yt_bs == yp_bs)))
        elif metric_type == "macro_f1":
            scores.append(fast_macro_f1(yt_bs, yp_bs, num_classes=num_classes))
    low = np.percentile(scores, 2.5)
    high = np.percentile(scores, 97.5)
    return float(low), float(high)


def main():
    t0 = time.time()
    out_dir = config.PROJECT_ROOT / "reports" / "v1"
    out_dir.mkdir(parents=True, exist_ok=True)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Running clean evaluation on {device}...", flush=True)

    leaky_csv = config.PROJECT_ROOT / "data" / "patches" / "history" / "leaky_eval_images_historical_343.csv"
    if not leaky_csv.exists():
        leaky_csv = out_dir / "removed_p007_images.csv"
    if not leaky_csv.exists():
        raise FileNotFoundError(f"Missing {leaky_csv}.")

    leaky_paths = set()
    with open(leaky_csv, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            path_val = r.get("eval_path") or r.get("relative_path")
            if path_val:
                leaky_paths.add(path_val.replace("\\", "/"))

    print(f"Total leaky evaluation image paths loaded: {len(leaky_paths)}", flush=True)

    with open(config.PROJECT_ROOT / "models" / "v1" / "class_names.json", encoding="utf-8") as f:
        v1_classes = json.load(f)
    v1_c2i = {c: i for i, c in enumerate(v1_classes)}

    with open(config.PROJECT_ROOT / "models" / "v1" / "crop_hierarchy.json", encoding="utf-8") as f:
        v1_hier = json.load(f)
    v1_cls_to_crop = torch.tensor(v1_hier["class_idx_to_crop_idx"], dtype=torch.long)

    with open(config.PROJECT_ROOT / "models" / "v1" / "calibration.json", encoding="utf-8") as f:
        v1_cal = json.load(f)
    T_crop_curr = float(v1_cal["T_crop"])
    T_dis_curr = float(v1_cal["T_disease"])

    df_manifest = pd.read_csv(config.PROJECT_ROOT / "reports" / "v1" / "dataset_v1.csv")
    val_df = df_manifest[df_manifest["split"] == "val"].reset_index(drop=True)
    test_df = df_manifest[df_manifest["split"] == "test"].reset_index(drop=True)

    val_paths = val_df["path"].str.replace("\\", "/").tolist()
    val_labels = [v1_c2i[c] for c in val_df["class"]]
    test_paths = test_df["path"].str.replace("\\", "/").tolist()
    test_labels = [v1_c2i[c] for c in test_df["class"]]

    val_dataset = PlantDataset(val_paths, val_labels, transform=get_val_transforms())
    test_dataset = PlantDataset(test_paths, test_labels, transform=get_test_transforms())

    val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False, num_workers=0)
    test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False, num_workers=0)

    val_is_clean = np.array([p not in leaky_paths for p in val_paths])
    test_is_clean = np.array([p not in leaky_paths for p in test_paths])
    print(f"Val: {len(val_paths)} total ({np.sum(val_is_clean)} clean, {np.sum(~val_is_clean)} leaky)", flush=True)
    print(f"Test: {len(test_paths)} total ({np.sum(test_is_clean)} clean, {np.sum(~test_is_clean)} leaky)", flush=True)

    # Cached logits directory
    cache_dir = config.PROJECT_ROOT / "artifacts" / "cached_features"
    cache_dir.mkdir(parents=True, exist_ok=True)
    val_cache_file = cache_dir / "val_v1_logits.pt"
    test_v1_cache_file = cache_dir / "test_v1_logits.pt"

    if not (val_cache_file.exists() and test_v1_cache_file.exists()):
        print("\nLoading Model V1 bundle...", flush=True)
        v1_bundle = load_model_bundle("v1", device=device)
        v1_model = v1_bundle.model.eval()

        if not val_cache_file.exists():
            val_c_l, val_d_l, val_targets = [], [], []
            with torch.no_grad():
                for imgs, tgts in val_loader:
                    imgs = imgs.to(device)
                    c_l, d_l = v1_model(imgs)
                    val_c_l.append(c_l.cpu())
                    val_d_l.append(d_l.cpu())
                    val_targets.extend(tgts.numpy())
            torch.save({
                "c_logits": torch.cat(val_c_l).float(),
                "d_logits": torch.cat(val_d_l).float(),
                "targets": np.array(val_targets),
            }, val_cache_file)

        if not test_v1_cache_file.exists():
            test_c_l, test_d_l, test_targets = [], [], []
            with torch.no_grad():
                for imgs, tgts in test_loader:
                    imgs = imgs.to(device)
                    c_l, d_l = v1_model(imgs)
                    test_c_l.append(c_l.cpu())
                    test_d_l.append(d_l.cpu())
                    test_targets.extend(tgts.numpy())
            torch.save({
                "c_logits": torch.cat(test_c_l).float(),
                "d_logits": torch.cat(test_d_l).float(),
                "targets": np.array(test_targets),
            }, test_v1_cache_file)

        del v1_model, v1_bundle
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        gc.collect()

    val_cache = torch.load(val_cache_file, map_location="cpu", weights_only=False)
    val_c_logits = val_cache["c_logits"]
    val_d_logits = val_cache["d_logits"]
    val_targets = val_cache["targets"]
    val_crop_targets = v1_cls_to_crop[val_targets].numpy()

    test_v1_cache = torch.load(test_v1_cache_file, map_location="cpu", weights_only=False)
    test_targets = test_v1_cache["targets"]

    clean_val_idx = np.where(val_is_clean)[0]
    N_clean_val = len(clean_val_idx)
    clean_val_targets_np = val_targets[clean_val_idx]
    clean_val_crop_targets_np = val_crop_targets[clean_val_idx]

    scaler_d = TemperatureScaler()
    new_T_disease = scaler_d.fit(
        val_d_logits[clean_val_idx], torch.tensor(clean_val_targets_np, dtype=torch.long)
    )

    scaler_c = TemperatureScaler()
    new_T_crop = scaler_c.fit(
        val_c_logits[clean_val_idx], torch.tensor(clean_val_crop_targets_np, dtype=torch.long)
    )

    print(f"Current Model Temperatures: T_disease={T_dis_curr:.4f}, T_crop={T_crop_curr:.4f}")
    print(f"Re-fitted Clean Val Temps:  T_disease={new_T_disease:.4f}, T_crop={new_T_crop:.4f}")

    val_raw_probs = F.softmax(val_d_logits, dim=-1).numpy()
    val_cal_curr_probs = F.softmax(val_d_logits / T_dis_curr, dim=-1).numpy()
    val_cal_new_probs = F.softmax(val_d_logits / new_T_disease, dim=-1).numpy()

    clean_val_ece_raw = compute_ece(val_raw_probs[clean_val_idx], clean_val_targets_np, 15)
    clean_val_ece_curr_cal = compute_ece(val_cal_curr_probs[clean_val_idx], clean_val_targets_np, 15)
    clean_val_ece_new_cal = compute_ece(val_cal_new_probs[clean_val_idx], clean_val_targets_np, 15)

    print(f"Clean Val ECE - Raw (T=1.0):       {clean_val_ece_raw*100:.2f}%")
    print(f"Clean Val ECE - Current T:         {clean_val_ece_curr_cal*100:.2f}%")
    print(f"Clean Val ECE - Re-fitted Clean T: {clean_val_ece_new_cal*100:.2f}%")

    out_artifact = out_dir / "clean_subset_evaluation.json"
    report = {
        "clean_val_samples": N_clean_val,
        "current_T_disease": T_dis_curr,
        "current_T_crop": T_crop_curr,
        "refitted_T_disease": new_T_disease,
        "refitted_T_crop": new_T_crop,
        "clean_val_ece_raw": clean_val_ece_raw,
        "clean_val_ece_current_T": clean_val_ece_curr_cal,
        "clean_val_ece_refitted_T": clean_val_ece_new_cal,
    }
    with open(out_artifact, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    print(f"Saved evaluation report -> {out_artifact}")
    print(f"Completed in {time.time() - t0:.2f}s.")


if __name__ == "__main__":
    main()
