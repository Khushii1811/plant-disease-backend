"""
scripts/v1/build_results.py

Canonical script to compute all official release v1 headline numbers strictly via
src.models.predict.predict_tensor ON CPU and write reports/v1/results.json.

Source dataset:
  - Held-out test split (N=9,279) of curated dataset reports/v1/dataset_v1.csv,
    with all 181 near-duplicate test leakage frames quarantined via Patch P-007
    (cataloged in reports/v1/removed_p007_images.csv).

Outputs:
  - reports/v1/results.json (comprehensive metrics, bootstrap CIs, reliability diagram, tau table)
  - reports/v1/counts_table.json (tau sweep table across clean test)
"""

import argparse
import io
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd
import torch
import torch.nn.functional as F
from PIL import Image
from sklearn.metrics import f1_score
from torch.utils.data import DataLoader, Dataset
from tqdm import tqdm

ROOT = Path(__file__).resolve().parent.parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import config
from src.data.preprocess import get_val_transforms, load_image
from src.models.bundle_loader import load_model_bundle
from src.models.predict import predict_tensor


class EvalDataset(Dataset):
    def __init__(self, df: pd.DataFrame, transform, root_dir: Path):
        self.df = df.reset_index(drop=True)
        self.transform = transform
        self.root_dir = root_dir

    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):
        row = self.df.iloc[idx]
        p = Path(row["path"])
        if not p.exists():
            p = self.root_dir / p
        img = load_image(p)
        tensor = self.transform(img)
        return tensor, row["class_idx"], row["crop_idx"], idx


def compute_ece(confidences: np.ndarray, correct: np.ndarray, n_bins: int = 15) -> Tuple[float, List[Dict]]:
    bins = np.linspace(0.0, 1.0, n_bins + 1)
    bin_indices = np.digitize(confidences, bins) - 1
    bin_indices = np.clip(bin_indices, 0, n_bins - 1)

    ece = 0.0
    bin_details = []
    total_n = len(confidences)

    for b in range(n_bins):
        mask = bin_indices == b
        count = int(np.sum(mask))
        if count > 0:
            avg_conf = float(np.mean(confidences[mask]))
            avg_acc = float(np.mean(correct[mask]))
            ece += (count / total_n) * abs(avg_acc - avg_conf)
            bin_details.append({
                "bin": b,
                "range": [float(bins[b]), float(bins[b + 1])],
                "count": count,
                "confidence": avg_conf,
                "accuracy": avg_acc,
                "gap": abs(avg_acc - avg_conf),
            })
        else:
            bin_details.append({
                "bin": b,
                "range": [float(bins[b]), float(bins[b + 1])],
                "count": 0,
                "confidence": 0.0,
                "accuracy": 0.0,
                "gap": 0.0,
            })

    return float(ece), bin_details


def bootstrap_ci(
    y_true_c: np.ndarray,
    y_pred_c: np.ndarray,
    y_true_d: np.ndarray,
    y_pred_d: np.ndarray,
    y_pred_raw_d: np.ndarray,
    classes_ge10_set: set,
    n_classes: int,
    n_iterations: int = 1000,
    seed: int = 42,
) -> Dict[str, List[float]]:
    rng = np.random.RandomState(seed)
    n = len(y_true_c)
    crop_accs = []
    gated_accs = []
    raw_accs = []
    macro_f1_alls = []
    macro_f1_ge10s = []

    all_labels = list(range(n_classes))
    ge10_labels = sorted(list(classes_ge10_set))

    print(f"Running {n_iterations} bootstrap iterations on CPU...")
    for _ in tqdm(range(n_iterations), desc="Bootstrap CIs"):
        indices = rng.randint(0, n, size=n)
        b_true_c = y_true_c[indices]
        b_pred_c = y_pred_c[indices]
        b_true_d = y_true_d[indices]
        b_pred_d = y_pred_d[indices]
        b_pred_raw_d = y_pred_raw_d[indices]

        crop_accs.append(np.mean(b_true_c == b_pred_c) * 100.0)
        gated_accs.append(np.mean(b_true_d == b_pred_d) * 100.0)
        raw_accs.append(np.mean(b_true_d == b_pred_raw_d) * 100.0)

        f1_all = f1_score(b_true_d, b_pred_d, labels=all_labels, average="macro", zero_division=0) * 100.0
        macro_f1_alls.append(f1_all)

        f1_ge10 = f1_score(b_true_d, b_pred_d, labels=ge10_labels, average="macro", zero_division=0) * 100.0
        macro_f1_ge10s.append(f1_ge10)

    def ci(arr):
        return [round(float(np.percentile(arr, 2.5)), 2), round(float(np.percentile(arr, 97.5)), 2)]

    return {
        "crop_accuracy_95ci": ci(crop_accs),
        "soft_gated_disease_accuracy_95ci": ci(gated_accs),
        "raw_disease_accuracy_95ci": ci(raw_accs),
        "macro_f1_all_95ci": ci(macro_f1_alls),
        "macro_f1_ge10_95ci": ci(macro_f1_ge10s),
    }


def main():
    parser = argparse.ArgumentParser(description="Build release v1 headline results on clean test partition")
    parser.add_argument(
        "--out-results",
        type=Path,
        default=ROOT / "reports" / "v1" / "results.json",
        help="Path to output results JSON file",
    )
    parser.add_argument(
        "--out-counts",
        type=Path,
        default=ROOT / "reports" / "v1" / "counts_table.json",
        help="Path to output counts table JSON file",
    )
    parser.add_argument(
        "--device",
        type=str,
        default="cpu",
        help="Device to evaluate on ('cpu' or 'cuda')",
    )
    args = parser.parse_args()

    print("=" * 80)
    print("BUILDING V1 HEADLINE RESULTS (CPU REFERENCE EXECUTION)")
    print("=" * 80)

    try:
        git_hash = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    except Exception:
        git_hash = "unknown"

    device = args.device
    if device == "cpu":
        torch.set_num_threads(1)
        os.environ["OMP_NUM_THREADS"] = "1"
        os.environ["MKL_NUM_THREADS"] = "1"
        torch.use_deterministic_algorithms(True)
    print(f"Loading bundle on {device} (threads={torch.get_num_threads()})...")
    bundle = load_model_bundle("v1", device=device)
    bundle.model.eval()

    class_idx_to_crop = torch.tensor(
        bundle.crop_hierarchy["class_idx_to_crop_idx"],
        dtype=torch.long,
        device=device,
    )

    df = pd.read_csv(ROOT / "reports" / "v1" / "dataset_v1.csv")
    test_df = df[df["split"] == "test"].copy()
    n_test = len(test_df)
    print(f"Total test split N: {n_test}")
    assert n_test == 9279, f"Expected 9279 test images, got {n_test}"

    clean_test_df = test_df.reset_index(drop=True)
    n_clean = len(clean_test_df)

    class_to_idx = {name: idx for idx, name in enumerate(bundle.class_names)}
    crop_to_idx = {name: idx for idx, name in enumerate(bundle.crop_hierarchy["crops"])}
    clean_test_df["class_idx"] = clean_test_df["class"].map(class_to_idx)
    clean_test_df["crop_idx"] = clean_test_df["crop"].map(crop_to_idx)

    transform = get_val_transforms()
    ds = EvalDataset(clean_test_df, transform, ROOT)
    loader = DataLoader(ds, batch_size=64, shuffle=False, num_workers=0)

    y_true_crop = []
    y_true_disease = []
    y_pred_crop = []
    y_pred_disease = []
    y_pred_raw_disease = []
    confidences = []

    print("\nRunning inference over clean test set via src.models.predict.predict_tensor...")
    t0 = time.time()
    for batch_tensors, b_disease_idx, b_crop_idx, _ in tqdm(loader, desc="Eval clean test"):
        batch_tensors = batch_tensors.to(device)
        out = predict_tensor(
            model=bundle.model,
            tensor=batch_tensors,
            class_idx_to_crop=class_idx_to_crop,
            T_c=bundle.T_crop,
            T_d=bundle.T_disease,
        )
        c_preds = out["c_logits"].argmax(dim=-1).cpu().numpy()
        d_raw_preds = out["d_logits"].argmax(dim=-1).cpu().numpy()
        d_preds = out["p_joint"].argmax(dim=-1).cpu().numpy()
        confs = out["p_joint"].max(dim=-1).values.cpu().numpy()

        y_true_crop.extend(b_crop_idx.numpy())
        y_true_disease.extend(b_disease_idx.numpy())
        y_pred_crop.extend(c_preds)
        y_pred_disease.extend(d_preds)
        y_pred_raw_disease.extend(d_raw_preds)
        confidences.extend(confs)

    elapsed = time.time() - t0
    print(f"Inference completed in {elapsed:.2f}s ({len(clean_test_df) / elapsed:.1f} img/s)")

    y_true_crop = np.array(y_true_crop)
    y_true_disease = np.array(y_true_disease)
    y_pred_crop = np.array(y_pred_crop)
    y_pred_disease = np.array(y_pred_disease)
    y_pred_raw_disease = np.array(y_pred_raw_disease)
    confidences = np.array(confidences)

    correct_crop = (y_true_crop == y_pred_crop)
    correct_disease = (y_true_disease == y_pred_disease)
    correct_raw_disease = (y_true_disease == y_pred_raw_disease)

    crop_acc = float(np.mean(correct_crop) * 100.0)
    gated_disease_acc = float(np.mean(correct_disease) * 100.0)
    raw_disease_acc = float(np.mean(correct_raw_disease) * 100.0)

    num_classes = len(bundle.class_names)
    num_crops = len(bundle.crop_hierarchy["crops"])
    all_classes_labels = list(range(num_classes))
    macro_f1_all = float(f1_score(y_true_disease, y_pred_disease, labels=all_classes_labels, average="macro", zero_division=0) * 100.0)

    class_counts = clean_test_df["class_idx"].value_counts().to_dict()
    classes_ge10 = {c_idx for c_idx in range(num_classes) if class_counts.get(c_idx, 0) >= 10}
    ge10_labels = sorted(list(classes_ge10))
    macro_f1_ge10 = float(f1_score(y_true_disease, y_pred_disease, labels=ge10_labels, average="macro", zero_division=0) * 100.0)

    ece_15, bin_details_15 = compute_ece(confidences, correct_disease.astype(float), n_bins=15)
    ece_15_pct = round(ece_15 * 100.0, 2)

    tau_sweep = [0.50, 0.55, 0.60, 0.65, 0.70]
    tau_results = []
    for tau in tau_sweep:
        cov_mask = confidences >= tau
        unc_mask = ~cov_mask
        n_cov = int(np.sum(cov_mask))
        n_unc = int(np.sum(unc_mask))
        c_cov = int(np.sum(correct_disease[cov_mask]))
        c_unc = int(np.sum(correct_disease[unc_mask]))
        total_c = c_cov + c_unc

        tau_results.append({
            "tau": float(tau),
            "covered_N": n_cov,
            "coverage_pct": round(n_cov / n_clean * 100.0, 2),
            "covered_correct": c_cov,
            "covered_accuracy_pct": round(c_cov / n_cov * 100.0, 2) if n_cov > 0 else 0.0,
            "uncertain_N": n_unc,
            "uncertain_pct": round(n_unc / n_clean * 100.0, 2),
            "uncertain_correct": c_unc,
            "uncertain_accuracy_pct": round(c_unc / n_unc * 100.0, 2) if n_unc > 0 else 0.0,
            "total_correct": total_c,
            "overall_accuracy_pct": round(total_c / n_clean * 100.0, 2),
        })

    cis = bootstrap_ci(
        y_true_crop, y_pred_crop, y_true_disease, y_pred_disease, y_pred_raw_disease,
        classes_ge10, num_classes, n_iterations=1000, seed=42
    )

    per_class_support = {bundle.class_names[c_idx]: int(class_counts.get(c_idx, 0)) for c_idx in range(num_classes)}

    # Generate per-class results table (reports/v1/per_class_results.csv)
    p006_plan_csv = ROOT / "data" / "patches" / "P-006_split_rebalance_PLAN.csv"
    p006_classes = set()
    if p006_plan_csv.exists():
        p006_df = pd.read_csv(p006_plan_csv)
        p006_classes = set(p006_df["class"].unique())

    all_labels = list(range(num_classes))
    per_class_f1 = f1_score(
        y_true_disease, y_pred_disease, labels=all_labels, average=None, zero_division=0
    )

    test_class_counts = test_df["class"].value_counts().to_dict()
    clean_class_counts = clean_test_df["class"].value_counts().to_dict()

    per_class_rows = []
    for c_idx, c_name in enumerate(bundle.class_names):
        crop_idx = bundle.crop_hierarchy["class_idx_to_crop_idx"][c_idx]
        crop_name = bundle.crop_hierarchy["crops"][crop_idx]

        n_test = int(test_class_counts.get(c_name, 0))
        n_clean_c = int(clean_class_counts.get(c_name, 0))

        mask = y_true_disease == c_idx
        if mask.sum() > 0:
            acc = float(np.mean(y_pred_disease[mask] == c_idx))
        else:
            acc = 0.0

        f1_val = float(per_class_f1[c_idx])
        flag_lt10 = bool(n_clean_c < 10)
        flag_p006 = bool(c_name in p006_classes)
        twin_share = round((n_test - n_clean_c) / n_test, 4) if n_test > 0 else 0.0

        per_class_rows.append({
            "class": c_name,
            "crop": crop_name,
            "test N": n_test,
            "clean test N": n_clean_c,
            "accuracy": round(acc, 4),
            "F1": round(f1_val, 4),
            "flagged <10 support": flag_lt10,
            "flagged P-006": flag_p006,
            "twin share": twin_share,
        })

    per_class_df = pd.DataFrame(per_class_rows)
    per_class_csv_path = ROOT / "reports" / "v1" / "per_class_results.csv"
    per_class_df.to_csv(per_class_csv_path, index=False)
    print(f"Written per-class results to: {per_class_csv_path}")

    results = {
        "metadata": {
            "script": "scripts/v1/build_results.py",
            "git_commit": git_hash,
            "model_version": "v1.0.0",
            "model_architecture": "ConvNeXt-Tiny DualHead (crop + disease)",
            "device": device,
            "cpu_threads": torch.get_num_threads() if device == "cpu" else None,
            "torch_version": torch.__version__,
            "deterministic_algorithms": torch.are_deterministic_algorithms_enabled(),
            "inference_engine": "src.models.predict.predict_tensor",
            "date_utc": datetime.now(timezone.utc).isoformat(),
            "source": "curated release test split (reports/v1/dataset_v1.csv, N=9,279 post-P-007)",
        },
        "headline_metrics": {
            "clean_test_N": n_clean,
            "num_classes": num_classes,
            "num_crops": num_crops,
            "classes_with_ge_10_clean_test": len(classes_ge10),
            "classes_with_lt_10_clean_test": num_classes - len(classes_ge10),
            "crop_accuracy": round(crop_acc, 2),
            "crop_accuracy_95ci": cis["crop_accuracy_95ci"],
            "soft_gated_disease_accuracy": round(gated_disease_acc, 2),
            "soft_gated_disease_accuracy_95ci": cis["soft_gated_disease_accuracy_95ci"],
            "raw_disease_accuracy": round(raw_disease_acc, 2),
            "raw_disease_accuracy_95ci": cis["raw_disease_accuracy_95ci"],
            "macro_f1_all_classes": round(macro_f1_all, 2),
            "macro_f1_all_classes_95ci": cis["macro_f1_all_95ci"],
            "macro_f1_classes_ge_10_test": round(macro_f1_ge10, 2),
            "macro_f1_classes_ge_10_test_95ci": cis["macro_f1_ge10_95ci"],
            "calibrated_ece_15_bins_pct": ece_15_pct,
            "calibration_temperatures": {
                "T_crop": bundle.T_crop,
                "T_disease": bundle.T_disease,
            },
        },
        "tau_table_clean_test": tau_results,
        "reliability_diagram_15_bins": bin_details_15,
        "per_class_support": per_class_support,
    }

    out_json = args.out_results
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"\nWritten canonical results to: {out_json}")

    counts_json = args.out_counts
    counts_table = {
        "metadata": results["metadata"],
        "clean_test_counts_table": tau_results,
    }
    counts_json.write_text(json.dumps(counts_table, indent=2), encoding="utf-8")
    print(f"Written counts table to: {counts_json}")

    print("\nHeadline Metrics Summary:")
    for k, v in results["headline_metrics"].items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()

