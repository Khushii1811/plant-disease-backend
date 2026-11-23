"""
Comprehensive Evaluation Suite for DualHeadConvNeXt-Tiny Plant Pathology Model.

Computes the complete production metric suite:
  1. Headline numbers: Top-1 (raw & masked), Macro-F1 (labels=range(195)), Weighted-F1,
     Macro Precision/Recall, Top-3 and Top-5 accuracy.
  2. Crop head metrics: Crop Accuracy & Crop Macro-F1.
  3. Per-class metrics: Precision, Recall, F1, Support saved as CSV and JSON.
     Identifies bottom 15 classes, F1 < 0.5, F1 < 0.8, and zero-support classes.
  4. Error analysis: Top 10 confusion pairs (True -> Pred), Same-Crop vs Cross-Crop error share.
  5. Calibration & Loss: Unweighted Cross-Entropy loss and Expected Calibration Error (ECE).
  6. Context: Split details, sample counts, checkpoint epoch metadata, and lab vs natural-background breakdown.
"""

import argparse
import csv
import json
import logging
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, cast

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.metrics import classification_report, confusion_matrix, f1_score, precision_score, recall_score
import torch
import torch.nn.functional as F
from torch.utils.data import DataLoader
from tqdm import tqdm

from ..data.dataset import get_dataloaders
from ..models.convnext import build_dualhead_convnext_tiny, DualHeadConvNeXt
from ..models.predict import predict_tensor

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("evaluate_dualhead")


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
        in_bin = (confidences > bin_lower) & (confidences <= bin_upper)
        prop_in_bin = np.mean(in_bin)

        if prop_in_bin > 0:
            accuracy_in_bin = np.mean(accuracies[in_bin])
            avg_confidence_in_bin = np.mean(confidences[in_bin])
            ece += np.abs(avg_confidence_in_bin - accuracy_in_bin) * prop_in_bin

    return float(ece)


def top_k_accuracy(logits: torch.Tensor, targets: torch.Tensor, k: int = 3) -> float:
    """Computes top-k accuracy given logits and true class indices."""
    with torch.no_grad():
        _, pred = logits.topk(k, dim=1, largest=True, sorted=True)
        correct = pred.eq(targets.view(-1, 1).expand_as(pred))
        return float(correct.any(dim=1).float().mean().item())


def evaluate_split(
    model: DualHeadConvNeXt,
    dataloader: DataLoader,
    class_to_crop_tensor: torch.Tensor,
    crop_hierarchy: Dict[str, Any],
    classes: List[str],
    crops_list: List[str],
    device: str,
    T_c: float = 1.0,
    T_d: float = 1.0,
    desc: str = "Evaluating",
) -> Dict[str, Any]:
    """Runs a complete forward pass over the split and extracts all diagnostic tensors."""
    model.eval()

    all_disease_targets = []
    all_crop_targets = []
    all_raw_disease_logits = []
    all_crop_logits = []
    all_joint_probs = []
    all_image_paths = getattr(dataloader.dataset, "image_paths", [])

    with torch.no_grad():
        pbar = tqdm(dataloader, desc=desc, dynamic_ncols=True, mininterval=1.0)
        for images, disease_targets in pbar:
            images = images.to(device, non_blocking=True)
            disease_targets = disease_targets.to(device, non_blocking=True)
            crop_targets = class_to_crop_tensor[disease_targets]

            out = predict_tensor(model, images, class_to_crop_tensor, T_c, T_d)
            crop_logits = out["c_logits"].float()
            disease_logits = out["d_logits"].float()
            p_joint = out["p_joint"].float()

            all_disease_targets.append(disease_targets.cpu())
            all_crop_targets.append(crop_targets.cpu())
            all_raw_disease_logits.append(disease_logits.cpu())
            all_crop_logits.append(crop_logits.cpu())
            all_joint_probs.append(p_joint.cpu())

    # Concatenate all batches
    y_true_disease = torch.cat(all_disease_targets).numpy()
    y_true_crop = torch.cat(all_crop_targets).numpy()
    raw_disease_logits = torch.cat(all_raw_disease_logits)
    crop_logits = torch.cat(all_crop_logits)
    joint_probs = torch.cat(all_joint_probs)

    y_pred_crop = crop_logits.argmax(dim=-1).numpy()
    y_pred_raw_disease = raw_disease_logits.argmax(dim=-1).numpy()
    y_pred_masked_disease = joint_probs.argmax(dim=-1).numpy()

    # Probabilities
    raw_disease_probs = F.softmax(raw_disease_logits, dim=-1).numpy()
    masked_disease_probs = joint_probs.numpy()

    # 1. Headline Numbers
    num_classes = len(classes)
    class_labels = list(range(num_classes))

    raw_top1_acc = float(np.mean(y_pred_raw_disease == y_true_disease))
    masked_top1_acc = float(np.mean(y_pred_masked_disease == y_true_disease))

    raw_top3_acc = top_k_accuracy(raw_disease_logits, torch.tensor(y_true_disease), k=3)
    raw_top5_acc = top_k_accuracy(raw_disease_logits, torch.tensor(y_true_disease), k=5)
    masked_top3_acc = top_k_accuracy(joint_probs, torch.tensor(y_true_disease), k=3)
    masked_top5_acc = top_k_accuracy(joint_probs, torch.tensor(y_true_disease), k=5)

    macro_f1 = float(f1_score(y_true_disease, y_pred_masked_disease, labels=class_labels, average="macro", zero_division=0))
    weighted_f1 = float(f1_score(y_true_disease, y_pred_masked_disease, labels=class_labels, average="weighted", zero_division=0))
    macro_precision = float(precision_score(y_true_disease, y_pred_masked_disease, labels=class_labels, average="macro", zero_division=0))
    macro_recall = float(recall_score(y_true_disease, y_pred_masked_disease, labels=class_labels, average="macro", zero_division=0))

    # Raw metrics for baseline comparison
    raw_macro_f1 = float(f1_score(y_true_disease, y_pred_raw_disease, labels=class_labels, average="macro", zero_division=0))
    raw_weighted_f1 = float(f1_score(y_true_disease, y_pred_raw_disease, labels=class_labels, average="weighted", zero_division=0))

    # 2. Crop Head Metrics
    crop_labels = list(range(len(crops_list)))
    crop_acc = float(np.mean(y_pred_crop == y_true_crop))
    crop_macro_f1 = float(f1_score(y_true_crop, y_pred_crop, labels=crop_labels, average="macro", zero_division=0))

    # 3. Calibration & Loss (Unweighted Cross-Entropy)
    unweighted_disease_ce = float(F.cross_entropy(raw_disease_logits, torch.tensor(y_true_disease)).item())
    ece_raw = compute_ece(raw_disease_probs, y_true_disease, n_bins=15)
    ece_masked = compute_ece(masked_disease_probs, y_true_disease, n_bins=15)

    # 4. Error Analysis
    # Same-crop vs cross-crop error breakdown (on raw predictions)
    pred_raw_crops = class_to_crop_tensor.cpu().numpy()[y_pred_raw_disease]
    raw_errors_mask = (y_pred_raw_disease != y_true_disease)
    total_raw_errors = int(np.sum(raw_errors_mask))

    cross_crop_errors = int(np.sum(raw_errors_mask & (pred_raw_crops != y_true_crop)))
    same_crop_errors = int(np.sum(raw_errors_mask & (pred_raw_crops == y_true_crop)))

    # On masked predictions
    masked_errors_mask = (y_pred_masked_disease != y_true_disease)
    total_masked_errors = int(np.sum(masked_errors_mask))

    # Top 10 Confusion Pairs
    confusion_pairs = {}
    for true_cls, pred_cls in zip(y_true_disease, y_pred_masked_disease):
        if true_cls != pred_cls:
            pair = (classes[true_cls], classes[pred_cls])
            confusion_pairs[pair] = confusion_pairs.get(pair, 0) + 1

    top_confusion_pairs = sorted(confusion_pairs.items(), key=lambda x: x[1], reverse=True)[:10]

    # 5. Per-Class Report
    rep_dict = cast(Dict[str, Any], classification_report(
        y_true_disease,
        y_pred_masked_disease,
        labels=class_labels,
        target_names=classes,
        output_dict=True,
        zero_division=0,
    ))
    raw_rep_dict = cast(Dict[str, Any], classification_report(
        y_true_disease,
        y_pred_raw_disease,
        labels=class_labels,
        target_names=classes,
        output_dict=True,
        zero_division=0,
    ))

    per_class_data = []
    classes_below_50 = 0
    classes_below_80 = 0
    classes_zero_support = 0

    for idx, cname in enumerate(classes):
        masked_item = rep_dict.get(cname, {})
        raw_item = raw_rep_dict.get(cname, {})

        f1 = float(masked_item.get("f1-score", 0.0))
        prec = float(masked_item.get("precision", 0.0))
        rec = float(masked_item.get("recall", 0.0))
        sup = int(masked_item.get("support", 0))

        raw_f1 = float(raw_item.get("f1-score", 0.0))
        raw_rec = float(raw_item.get("recall", 0.0))

        # Per-class crop accuracy
        mask_idx = (y_true_disease == idx)
        cls_crop_acc = float(np.mean(y_pred_crop[mask_idx] == y_true_crop[mask_idx])) if np.sum(mask_idx) > 0 else 0.0

        if sup == 0:
            classes_zero_support += 1
        else:
            if f1 < 0.5:
                classes_below_50 += 1
            if f1 < 0.8:
                classes_below_80 += 1

        # Extract Crop name
        crop_name = crops_list[int(class_to_crop_tensor[idx].item())]

        per_class_data.append({
            "class_id": idx,
            "crop": crop_name,
            "class_name": cname,
            "support": sup,
            "masked_accuracy": rec,
            "raw_accuracy": raw_rec,
            "accuracy_delta": rec - raw_rec,
            "masked_f1": f1,
            "raw_f1": raw_f1,
            "f1_delta": f1 - raw_f1,
            "masked_precision": prec,
            "crop_accuracy": cls_crop_acc,
        })

    # Bottom 15 classes by F1
    sorted_by_f1 = sorted([c for c in per_class_data if c["support"] > 0], key=lambda x: x["masked_f1"])
    bottom_15 = sorted_by_f1[:15]

    # Top 10 beneficiaries of masking (highest accuracy delta)
    top_mask_gainers = sorted(per_class_data, key=lambda x: x["accuracy_delta"], reverse=True)[:10]

    # 6. Heuristic background split
    lab_field_metrics = None
    if all_image_paths and len(all_image_paths) == len(y_true_disease):
        lab_indices = []
        field_indices = []
        for i, p in enumerate(all_image_paths):
            p_lower = str(p).lower()
            if "plantvillage" in p_lower or "lab" in p_lower or "segmented" in p_lower:
                lab_indices.append(i)
            else:
                field_indices.append(i)

        if lab_indices and field_indices:
            lab_acc = float(np.mean(y_pred_masked_disease[lab_indices] == y_true_disease[lab_indices]))
            field_acc = float(np.mean(y_pred_masked_disease[field_indices] == y_true_disease[field_indices]))
            lab_field_metrics = {
                "lab_samples": len(lab_indices),
                "lab_accuracy": lab_acc,
                "field_samples": len(field_indices),
                "field_accuracy": field_acc,
            }

    return {
        "headline": {
            "top1_masked_acc": masked_top1_acc,
            "top1_raw_acc": raw_top1_acc,
            "top3_masked_acc": masked_top3_acc,
            "top3_raw_acc": raw_top3_acc,
            "top5_masked_acc": masked_top5_acc,
            "top5_raw_acc": raw_top5_acc,
            "macro_f1": macro_f1,
            "weighted_f1": weighted_f1,
            "raw_macro_f1": raw_macro_f1,
            "raw_weighted_f1": raw_weighted_f1,
            "macro_precision": macro_precision,
            "macro_recall": macro_recall,
        },
        "crop_head": {
            "crop_accuracy": crop_acc,
            "crop_macro_f1": crop_macro_f1,
        },
        "calibration": {
            "unweighted_disease_ce": unweighted_disease_ce,
            "ece_raw": ece_raw,
            "ece_masked": ece_masked,
        },
        "error_analysis": {
            "total_raw_errors": total_raw_errors,
            "same_crop_errors": same_crop_errors,
            "cross_crop_errors": cross_crop_errors,
            "cross_crop_share": cross_crop_errors / max(1, total_raw_errors),
            "total_masked_errors": total_masked_errors,
            "top_confusion_pairs": [{"true": k[0], "pred": k[1], "count": v} for k, v in top_confusion_pairs],
        },
        "class_summary": {
            "total_classes": num_classes,
            "classes_f1_below_50": classes_below_50,
            "classes_f1_below_80": classes_below_80,
            "classes_zero_support": classes_zero_support,
            "bottom_15_classes": bottom_15,
            "top_mask_gainers": top_mask_gainers,
        },
        "per_class_data": per_class_data,
        "lab_field_metrics": lab_field_metrics,
        "confusion_matrix": confusion_matrix(y_true_disease, y_pred_masked_disease),
    }


def save_reports(results: Dict[str, Any], output_dir: Path, split_name: str) -> None:
    """Exports CSV, JSON, and Confusion Matrix artifacts."""
    output_dir.mkdir(parents=True, exist_ok=True)

    # 1. Save Per-Class CSV
    csv_path = output_dir / f"per_class_metrics_{split_name}.csv"
    per_class_data = results["per_class_data"]
    if per_class_data:
        keys = list(per_class_data[0].keys())
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(per_class_data)
        logger.info("Saved per-class CSV -> %s", csv_path)

    # 2. Save JSON Report (excluding numpy arrays)
    json_path = output_dir / f"evaluation_report_{split_name}.json"
    clean_results = {k: v for k, v in results.items() if k != "confusion_matrix"}
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(clean_results, f, indent=2)
    logger.info("Saved JSON report -> %s", json_path)

    # 3. Save Confusion Matrix CSV
    cm = results["confusion_matrix"]
    cm_csv_path = output_dir / f"confusion_matrix_{split_name}.csv"
    np.savetxt(cm_csv_path, cm, fmt="%d", delimiter=",")
    logger.info("Saved Confusion Matrix CSV -> %s", cm_csv_path)


def print_terminal_summary(results: Dict[str, Any], split_name: str, num_samples: int) -> None:
    """Prints a beautiful, comprehensive executive summary to the terminal."""
    h = results["headline"]
    c = results["crop_head"]
    cal = results["calibration"]
    err = results["error_analysis"]
    cs = results["class_summary"]
    lf = results["lab_field_metrics"]

    print("\n" + "=" * 80)
    print(f"[DUAL-HEAD CONVNEXT-TINY EVALUATION REPORT] [{split_name.upper()} SET: {num_samples:,} images]")
    print("=" * 80)

    print("\n📌 1. HEADLINE NUMBERS (Main Performance Indicators):")
    print(f"  • Top-1 Masked Disease Accuracy : {h['top1_masked_acc']*100:6.2f}%   (Production Gated)")
    print(f"  • Top-1 Raw Disease Accuracy    : {h['top1_raw_acc']*100:6.2f}%   (Unassisted Backbone)")
    print(f"  • Masking Advantage (Delta)     : { (h['top1_masked_acc'] - h['top1_raw_acc'])*100:+6.2f}%")
    print(f"  • Macro-F1 (195-class avg)      : {h['macro_f1']*100:6.2f}%   ⭐ (Key metric for class imbalance)")
    print(f"  • Weighted-F1                   : {h['weighted_f1']*100:6.2f}%")
    print(f"  • Macro-Precision               : {h['macro_precision']*100:6.2f}%")
    print(f"  • Macro-Recall                  : {h['macro_recall']*100:6.2f}%")
    print(f"  • Top-3 Accuracy                : {h['top3_masked_acc']*100:6.2f}%")
    print(f"  • Top-5 Accuracy                : {h['top5_masked_acc']*100:6.2f}%   (Shows near-misses)")

    print("\n🌱 2. CROP HEAD METRICS (Botanical Taxonomy Gating):")
    print(f"  • Crop Accuracy (34 crops)      : {c['crop_accuracy']*100:6.2f}%")
    print(f"  • Crop Macro-F1                 : {c['crop_macro_f1']*100:6.2f}%")

    print("\n📉 3. CALIBRATION & UNWEIGHTED LOSS:")
    print(f"  • Unweighted Cross-Entropy Loss : {cal['unweighted_disease_ce']:6.4f}   (Undistorted by class weights)")
    print(f"  • Expected Calibration Error    : {cal['ece_masked']:6.4f}   (ECE - probability calibration reliability)")

    print("\n🔍 4. ERROR ANALYSIS & HIERARCHY VALUE:")
    print(f"  • Total Raw Errors              : {err['total_raw_errors']:,}")
    print(f"  • Same-Crop Errors              : {err['same_crop_errors']:,} ({err['same_crop_errors']/max(1,err['total_raw_errors'])*100:.1f}%)")
    print(f"  • Cross-Crop Errors Caught      : {err['cross_crop_errors']:,} ({err['cross_crop_share']*100:.1f}% of all errors eliminated by mask!)")
    print(f"  • Remaining Masked Errors       : {err['total_masked_errors']:,}")

    print("\n⚠️ 5. TOP 5 CONFUSION PAIRS (Most Common Look-Alikes):")
    for i, p in enumerate(err["top_confusion_pairs"][:5], 1):
        print(f"  {i}. {p['true']}  ──>  {p['pred']} ({p['count']} occurrences)")

    print("\n📊 6. PER-CLASS SUMMARY & WEAK-SPOT RADAR:")
    print(f"  • Total Evaluated Classes       : {cs['total_classes']}")
    print(f"  • Classes with F1 < 0.50        : {cs['classes_f1_below_50']}")
    print(f"  • Classes with F1 < 0.80        : {cs['classes_f1_below_80']}")
    print(f"  • Classes with 0 Support        : {cs['classes_zero_support']}")

    print("\n🔻 BOTTOM 5 CLASSES BY F1-SCORE (Areas for Targeted Natural-Background Data):")
    for item in cs["bottom_15_classes"][:5]:
        print(f"  • {item['class_name']:<45} | F1: {item['masked_f1']*100:5.1f}% | Acc: {item['masked_accuracy']*100:5.1f}% (N={item['support']})")

    if lf:
        print("\n🔬 7. HYBRID DATASET AUDIT (Studio vs Natural Backgrounds):")
        print(f"  • Plain / Studio Images           : {lf['lab_samples']:,} samples | Accuracy: {lf['lab_accuracy']*100:.2f}%")
        print(f"  • Natural Background Images       : {lf['field_samples']:,} samples | Accuracy: {lf['field_accuracy']*100:.2f}%")

    print("\n" + "=" * 80 + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate DualHeadConvNeXt-Tiny on Val or Test Split")
    default_ckpt = "models/v1/model_dualhead_convnext_tiny.pth"
    parser.add_argument("--checkpoint", type=str, default=default_ckpt, help="Checkpoint path")
    parser.add_argument("--split", type=str, choices=["val", "test", "both"], default="test", help="Dataset split to evaluate")
    parser.add_argument("--batch-size", type=int, default=32, help="Evaluation batch size")
    parser.add_argument("--device", type=str, default="cuda" if torch.cuda.is_available() else "cpu", help="Compute device")
    parser.add_argument("--output-dir", type=str, default="reports/v1/metrics", help="Output directory for reports")
    args = parser.parse_args()

    checkpoint_path = Path(args.checkpoint)
    if not checkpoint_path.exists():
        raise FileNotFoundError(f"Checkpoint not found at: {checkpoint_path}")

    # Load Hierarchy
    hierarchy_path = Path("models/v1/crop_hierarchy.json")
    if not hierarchy_path.exists():
        raise FileNotFoundError(f"Missing crop hierarchy at {hierarchy_path}")
    crop_hierarchy = json.loads(hierarchy_path.read_text(encoding="utf-8"))
    num_crops = crop_hierarchy["num_crops"]
    crops_list = crop_hierarchy["crops"]
    class_to_crop_tensor = torch.tensor(crop_hierarchy["class_idx_to_crop_idx"], dtype=torch.long, device=args.device)

    # Load Data
    train_loader, val_loader, test_loader, classes = get_dataloaders(batch_size=args.batch_size)
    num_classes = len(classes)

    logger.info("Initializing DualHeadConvNeXt-Tiny with %d crops and %d disease classes...", num_crops, num_classes)
    model = build_dualhead_convnext_tiny(
        num_crops=num_crops,
        num_classes=num_classes,
        pretrained=False,
    ).to(args.device)

    logger.info("Loading weights from %s...", checkpoint_path)
    state = torch.load(checkpoint_path, map_location=args.device, weights_only=True)
    if "model_state" in state:
        state = state["model_state"]
    model.load_state_dict(state, strict=True)
    logger.info("Successfully loaded checkpoint weights!")

    splits_to_eval = ["val", "test"] if args.split == "both" else [args.split]

    calib_path = Path("models/v1/calibration.json")
    t_crop, t_disease = 1.0, 1.0
    if calib_path.exists():
        try:
            calib = json.loads(calib_path.read_text(encoding="utf-8"))
            t_crop = float(calib.get("T_crop", 1.0))
            t_disease = float(calib.get("T_disease", 1.0))
        except Exception:
            pass

    for split_name in splits_to_eval:
        loader = val_loader if split_name == "val" else test_loader
        n_images = len(cast(Any, loader.dataset))
        logger.info("Starting comprehensive evaluation on '%s' split (%d images)...", split_name, n_images)
        results = evaluate_split(
            model=model,
            dataloader=loader,
            class_to_crop_tensor=class_to_crop_tensor,
            crop_hierarchy=crop_hierarchy,
            classes=classes,
            crops_list=crops_list,
            device=args.device,
            T_c=t_crop,
            T_d=t_disease,
            desc=f"Evaluating {split_name.upper()} Set",
        )

        save_reports(results, Path(args.output_dir), split_name)
        print_terminal_summary(results, split_name, n_images)


if __name__ == "__main__":
    main()
