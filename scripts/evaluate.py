"""
scripts/evaluate.py — Comprehensive Versioned Model Evaluator.

Usage:
    python scripts/evaluate.py --version v1 [--split {purified,historical}] [--batch-size 64] [--device cuda]

Performs evaluation against official benchmarks in reports/v1/results.json:
  1. Loads verified model bundle via load_model_bundle(version).
  2. Evaluates either the headline Purified test split (N=9,327) or Historical split (N=10,426).
  3. Computes Crop, Raw Disease, and Crop-Gated Disease predictions across all 195 classes.
  4. Exports per-class metrics and predictions summary.
  5. Validates computed metrics against expected single source of truth in results.json.
"""

import argparse
import json
import logging
import os
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import numpy as np
import pandas as pd
from sklearn.metrics import classification_report, f1_score
import torch
import torch.nn.functional as F
from tqdm import tqdm
from PIL import Image

import config
from src.data.preprocess import get_val_transforms, load_image
from src.models.bundle_loader import load_model_bundle
from src.models.predict import predict_tensor

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("evaluate")


def compute_ece(probs: np.ndarray, labels: np.ndarray, n_bins: int = 15) -> float:
    """Computes Expected Calibration Error (ECE) with equal-width confidence bins."""
    confidences = np.max(probs, axis=1)
    predictions = np.argmax(probs, axis=1)
    accuracies = (predictions == labels).astype(float)

    bin_boundaries = np.linspace(0, 1, n_bins + 1)
    ece = 0.0

    for i in range(n_bins):
        bin_lower = bin_boundaries[i]
        bin_upper = bin_boundaries[i + 1]
        in_bin = (confidences > bin_lower) & (confidences <= bin_upper) if i > 0 else (confidences >= bin_lower) & (confidences <= bin_upper)
        prop_in_bin = np.mean(in_bin)

        if prop_in_bin > 0:
            accuracy_in_bin = np.mean(accuracies[in_bin])
            avg_confidence_in_bin = np.mean(confidences[in_bin])
            ece += np.abs(avg_confidence_in_bin - accuracy_in_bin) * prop_in_bin

    return float(ece)


def main():
    parser = argparse.ArgumentParser(description="Evaluate a versioned model bundle.")
    parser.add_argument("--version", type=str, default="v1", help="Model version to evaluate (e.g. 'v1')")
    parser.add_argument("--split", type=str, choices=["purified", "historical"], default="purified",
                        help="Test split to evaluate: 'purified' (N=9,327, headline) or 'historical' (N=10,426)")
    parser.add_argument("--batch-size", type=int, default=64, help="Batch size for evaluation")
    parser.add_argument("--device", type=str, default="cuda" if torch.cuda.is_available() else "cpu", help="Device")
    parser.add_argument("--no-cache", action="store_true", default=False, help="Do not use cached logits")
    args = parser.parse_args()

    version = args.version
    device = args.device
    split_choice = args.split
    reports_dir = ROOT_DIR / "reports" / version
    pred_dir = reports_dir / "predictions"
    metrics_dir = reports_dir / "metrics"
    pred_dir.mkdir(parents=True, exist_ok=True)
    metrics_dir.mkdir(parents=True, exist_ok=True)

    results_json_path = reports_dir / "results.json"
    if not results_json_path.exists():
        logger.error("results.json not found at %s. Please generate it first.", results_json_path)
        sys.exit(1)

    with open(results_json_path, "r", encoding="utf-8") as f:
        truth = json.load(f)

    if split_choice == "historical":
        print("\n" + "=" * 80)
        print("HISTORICAL TEST SPLIT (N=10,426) - REFERENCE ONLY")
        print("=" * 80)
        print("Notice: The historical split is reference only and not reproducible from the")
        print("current repository state with a single command, as 1,099 leak/duplicate images")
        print("(768 from P-003, 331 from P-004) are quarantined in data/raw/quarantine_*/.")
        hist = truth.get("historical_full_test_split", {})
        print(f"Historical Crop Accuracy:               {hist.get('crop_accuracy', 0.0)*100:.2f}%")
        print(f"Historical Raw Disease Accuracy:        {hist.get('raw_disease_accuracy', 0.0)*100:.2f}%")
        print(f"Historical Crop-Gated Disease Accuracy: {hist.get('crop_gated_disease_accuracy', 0.0)*100:.2f}%")
        print(f"Historical Macro-F1 (All 195 Classes):  {hist.get('macro_f1_all_195_classes', 0.0)*100:.2f}%")
        print("=" * 80)
        return

    logger.info("Loading model bundle '%s' on %s...", version, device)
    bundle = load_model_bundle(version=version, device=device)
    num_classes = len(bundle.class_names)
    class_idx_to_crop = torch.tensor(bundle.crop_hierarchy["class_idx_to_crop_idx"], dtype=torch.long, device=device)
    T_c = bundle.T_crop
    T_d = bundle.T_disease

    # 1. Dataset loading
    transform = get_val_transforms()
    class_to_idx = {name: idx for idx, name in enumerate(bundle.class_names)}

    test_dir = config.DATA_DIR / "processed" / "test"
    image_records = []
    for cname in sorted(os.listdir(test_dir)):
        cdir = test_dir / cname
        if not cdir.is_dir() or cname not in class_to_idx:
            continue
        for img_f in sorted(os.listdir(cdir)):
            if img_f.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
                image_records.append((str(cdir / img_f), class_to_idx[cname]))

    N_test = len(image_records)
    logger.info("Evaluating split '%s': %d samples across %d classes", split_choice, N_test, num_classes)

    cache_path = ROOT_DIR / "scratch" / "cached_purified_test_logits.pt"
    if not args.no_cache and cache_path.exists():
        logger.info("Loading cached logits from %s", cache_path)
        cached = torch.load(cache_path, weights_only=False)
        test_crop_logits = torch.as_tensor(cached["crop_logits"]).to(device)
        test_disease_logits = torch.as_tensor(cached["disease_logits"]).to(device)
        test_targets = torch.as_tensor(cached["targets"], dtype=torch.long).to(device)
    else:
        logger.info("Computing forward pass for %d images...", N_test)
        all_crops = []
        all_diseases = []
        all_targets = []

        batch_size = args.batch_size
        for i in tqdm(range(0, N_test, batch_size), desc="Forward Pass"):
            batch = image_records[i:i+batch_size]
            tensors = []
            targets = []
            for path, target in batch:
                try:
                    img = load_image(path)
                    tensors.append(transform(img))
                    targets.append(target)
                except Exception as e:
                    logger.warning("Failed to load %s: %s", path, e)
            if not tensors:
                continue
            batch_tensor = torch.stack(tensors).to(device)
            out = predict_tensor(bundle.model, batch_tensor, class_idx_to_crop, T_c, T_d)
            all_crops.append(out["c_logits"].cpu())
            all_diseases.append(out["d_logits"].cpu())
            all_targets.extend(targets)

        test_crop_logits = torch.cat(all_crops).to(device)
        test_disease_logits = torch.cat(all_diseases).to(device)
        test_targets = torch.tensor(all_targets, dtype=torch.long, device=device)

        cache_path.parent.mkdir(parents=True, exist_ok=True)
        torch.save({
            "crop_logits": test_crop_logits.cpu(),
            "disease_logits": test_disease_logits.cpu(),
            "targets": test_targets.cpu()
        }, cache_path)

    y_true_disease = test_targets.cpu().numpy()
    y_true_crop = class_idx_to_crop[test_targets].cpu().numpy()

    # Predictions
    pred_raw_disease = test_disease_logits.argmax(dim=-1).cpu().numpy()
    pred_crop = test_crop_logits.argmax(dim=-1).cpu().numpy()

    # Crop-gating (joint probability)
    p_crop_scaled = F.softmax(test_crop_logits / T_c, dim=-1)
    p_disease_scaled = F.softmax(test_disease_logits / T_d, dim=-1)
    p_joint = p_crop_scaled[:, class_idx_to_crop] * p_disease_scaled
    pred_crop_gated = p_joint.argmax(dim=-1).cpu().numpy()

    # Metrics
    crop_acc = float(np.mean(pred_crop == y_true_crop))
    raw_acc = float(np.mean(pred_raw_disease == y_true_disease))
    crop_gated_acc = float(np.mean(pred_crop_gated == y_true_disease))

    supported_classes = sorted(list(set(y_true_disease)))
    headline_macro_f1 = float(f1_score(y_true_disease, pred_crop_gated, labels=supported_classes, average="macro", zero_division=0))
    secondary_macro_f1 = float(f1_score(y_true_disease, pred_crop_gated, labels=list(range(num_classes)), average="macro", zero_division=0))

    calibrated_ece = compute_ece(p_joint.cpu().numpy(), y_true_disease, n_bins=15)

    rep = classification_report(
        y_true_disease,
        pred_crop_gated,
        labels=list(range(num_classes)),
        target_names=bundle.class_names,
        output_dict=True,
        zero_division=0,
    )
    robust_f1s = [rep[cname]["f1-score"] for cname in bundle.class_names if rep[cname]["support"] >= 20]
    robust_macro_f1 = float(np.mean(robust_f1s)) if robust_f1s else 0.0

    expected = truth["purified_test_split"]

    print("\n" + "=" * 80)
    print(f"EVALUATION ACCEPTANCE CHECK: Model v1.0 on PURIFIED split (N={N_test})")
    print("=" * 80)
    print(f"{'Metric':<38} | {'Computed':<10} | {'Expected':<10} | {'Delta':<10}")
    print("-" * 80)

    checks = [
        ("Crop Accuracy", crop_acc, expected["crop_accuracy"]),
        ("Raw Disease Accuracy", raw_acc, expected["raw_disease_accuracy"]),
        ("Crop-Gated Disease Accuracy", crop_gated_acc, expected["crop_gated_disease_accuracy"]),
        (f"HEADLINE Macro-F1 ({len(supported_classes)} Supported Classes)", headline_macro_f1, expected["headline_macro_f1"]),
        ("SECONDARY Macro-F1 (All 195 Classes)", secondary_macro_f1, expected["secondary_macro_f1_all_195_classes"]),
        ("Robust Macro-F1 (N >= 20)", robust_macro_f1, expected["robust_macro_f1_support_ge_20"]),
        ("Expected Calibration Error (ECE)", calibrated_ece, expected["expected_calibration_error_calibrated"]),
    ]

    all_passed = True
    for label, comp, exp in checks:
        delta = abs(comp - exp)
        status_str = "OK" if delta < 1e-4 else "MISMATCH"
        if delta >= 1e-4:
            all_passed = False
        print(f"{label:<38} | {comp:<10.6f} | {exp:<10.6f} | {delta:<10.6f} [{status_str}]")

    print("=" * 80)
    if all_passed:
        print("[ACCEPTANCE VERIFIED] All computed metrics match reports/v1/results.json exactly.")
    else:
        print("[ACCEPTANCE FAILED] Some metrics deviated from reports/v1/results.json.")
        sys.exit(1)


if __name__ == "__main__":
    main()
