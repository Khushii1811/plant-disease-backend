"""
scripts/v1/evaluate_final_test.py

FINAL TEST EVALUATION of the chosen v1 checkpoint (Epoch 20) on the full v1 test split (10,426 images).
Computes:
1. Raw, hard-masked, and soft-gated disease accuracy.
2. Macro-F1 over all 195 classes.
3. Macro-F1 over classes with >=20 test images only.
4. Crop-head accuracy.
5. ECE (raw and temperature-scaled).
6. Per-class precision, recall, F1, support (saved to reports/v1/test_per_class_metrics.csv).
7. Top 25 lowest-F1 classes with support.
8. Top 30 confusion pairs (flagging pairs where crops differ).
9. Healthy-vs-diseased foliar decision metric: overall and per-crop missed-disease rate and false-alarm rate.
10. Per-source accuracy using reports/v1/dataset_v1.csv.
"""

import contextlib
import sys
import json
import logging
from pathlib import Path
from collections import defaultdict, Counter

import numpy as np
import pandas as pd
from PIL import Image
import torch
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
from sklearn.metrics import classification_report, confusion_matrix, precision_recall_fscore_support
from tqdm import tqdm

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
import config
from src.models.convnext import build_dualhead_convnext_tiny

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("final_test_eval")


def compute_ece(probs: np.ndarray, labels: np.ndarray, n_bins: int = 15) -> float:
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
        count_in_bin = int(np.sum(in_bin))

        if count_in_bin > 0:
            acc = float(np.mean(accuracies[in_bin]))
            conf = float(np.mean(confidences[in_bin]))
            diff = abs(conf - acc)
            ece += diff * prop_in_bin

    return float(ece)


class ExplicitTestDataset(Dataset):
    def __init__(self, samples, transform):
        self.samples = samples # list of (Path, int, str)
        self.transform = transform

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        path, target, fname = self.samples[idx]
        with open(path, "rb") as f:
            img = Image.open(f).convert("RGB")
        if self.transform:
            img = self.transform(img)
        return img, target, fname


def compute_soft_gated_probs(crop_logits: torch.Tensor, disease_logits: torch.Tensor, crop_hierarchy: dict, num_classes: int) -> torch.Tensor:
    batch_size = crop_logits.shape[0]
    p_crop = F.softmax(crop_logits, dim=-1)
    crops_list = crop_hierarchy["crops"]
    crop_to_class_indices = crop_hierarchy["crop_to_class_indices"]
    p_disease_joint = torch.zeros((batch_size, num_classes), dtype=torch.float32, device=crop_logits.device)

    for c_idx, c_name in enumerate(crops_list):
        allowed_classes = crop_to_class_indices.get(c_name, [])
        if not allowed_classes:
            continue
        sub_logits = disease_logits[:, allowed_classes]
        p_disease_given_crop = F.softmax(sub_logits, dim=-1)
        prob_c = p_crop[:, c_idx].unsqueeze(1)
        p_disease_joint[:, allowed_classes] = prob_c * p_disease_given_crop

    return p_disease_joint


def main():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    logger.info("Using device: %s", device)

    # 1. Load Bundle Metadata
    v1_dir = PROJECT_ROOT / "models" / "v1"
    with open(v1_dir / "class_names.json", "r", encoding="utf-8") as f:
        class_names = json.load(f)
    with open(v1_dir / "class_to_idx.json", "r", encoding="utf-8") as f:
        class_to_idx = json.load(f)
    with open(v1_dir / "crop_hierarchy.json", "r", encoding="utf-8") as f:
        crop_hierarchy = json.load(f)
    with open(v1_dir / "calibration.json", "r", encoding="utf-8") as f:
        calibration = json.load(f)

    num_classes = len(class_names)
    num_crops = len(crop_hierarchy["crops"])
    t_disease = float(calibration["T_disease"])
    t_crop = float(calibration["T_crop"])
    class_idx_to_crop = torch.tensor(crop_hierarchy["class_idx_to_crop_idx"], dtype=torch.long)

    logger.info("Bundle loaded: %d classes, %d crops, T_disease=%.4f, T_crop=%.4f", num_classes, num_crops, t_disease, t_crop)

    # 2. Case-Insensitive Deduplicated Test Set Assembly
    test_dir = config.DATA_DIR / "processed" / "test"
    test_transform = transforms.Compose([
        transforms.Resize((256, 256)),
        transforms.ToTensor(),
        transforms.Normalize(mean=config.NORMALIZE_MEAN, std=config.NORMALIZE_STD),
    ])

    samples = []
    for class_name in class_names:
        cdir = test_dir / class_name
        if not cdir.exists():
            continue
        c_idx = class_to_idx[class_name]
        files = sorted([f for f in cdir.iterdir() if f.is_file() and f.suffix.lower() in [".jpg", ".jpeg", ".png", ".webp", ".bmp"]])
        for f in files:
            samples.append((f, c_idx, f.name))

    num_test_images = len(samples)
    logger.info("Assembled test split: %d images across %d classes", num_test_images, len(class_names))
    assert num_test_images == 10426, f"Expected exactly 10,426 test images, got {num_test_images}"

    test_dataset = ExplicitTestDataset(samples, transform=test_transform)
    test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False, num_workers=0, pin_memory=torch.cuda.is_available())

    # 3. Load Model
    model = build_dualhead_convnext_tiny(num_crops=num_crops, num_classes=num_classes, pretrained=False)
    weights_path = v1_dir / "model_dualhead_convnext_tiny.pth"
    model.load_state_dict(torch.load(weights_path, map_location="cpu", weights_only=False))
    model.to(device)
    model.eval()

    # 4. Extract Test Logits
    all_crop_logits = []
    all_disease_logits = []
    all_targets = []
    all_fnames = []

    logger.info("Extracting test logits...")
    with torch.no_grad():
        for images, targets, fnames in tqdm(test_loader, desc="Test Inference"):
            images = images.to(device, non_blocking=True)
            autocast_ctx = torch.amp.autocast(device_type="cuda", dtype=torch.float16) if device.type == "cuda" else contextlib.nullcontext()
            with autocast_ctx:
                crop_logits, disease_logits = model(images)
            all_crop_logits.append(crop_logits.float().cpu())
            all_disease_logits.append(disease_logits.float().cpu())
            all_targets.append(targets)
            all_fnames.extend(fnames)

    test_crop_logits = torch.cat(all_crop_logits)
    test_disease_logits = torch.cat(all_disease_logits)
    test_targets = torch.cat(all_targets).numpy()
    test_crop_targets = class_idx_to_crop[torch.tensor(test_targets)].numpy()

    # 5. Crop-Head Accuracy
    crop_preds = test_crop_logits.argmax(dim=-1).numpy()
    crop_accuracy = float(np.mean(crop_preds == test_crop_targets))
    logger.info("Crop-Head Accuracy: %.4f (%.2f%%)", crop_accuracy, crop_accuracy * 100)

    # 6. Raw Disease Predictions & ECE
    p_raw = F.softmax(test_disease_logits, dim=-1).numpy()
    raw_preds = np.argmax(p_raw, axis=1)
    raw_acc = float(np.mean(raw_preds == test_targets))
    raw_ece = compute_ece(p_raw, test_targets)

    # Calibrated Raw ECE
    p_cal = F.softmax(test_disease_logits / t_disease, dim=-1).numpy()
    cal_ece = compute_ece(p_cal, test_targets)

    # 7. Hard-Masked Disease Predictions
    masked_logits = test_disease_logits.clone()
    crops_list = crop_hierarchy["crops"]
    all_indices = set(range(num_classes))
    for i in range(len(test_targets)):
        c_name = crops_list[crop_preds[i]]
        allowed = set(crop_hierarchy["crop_to_class_indices"].get(c_name, []))
        disallowed = list(all_indices - allowed)
        if disallowed:
            masked_logits[i, disallowed] = -1e9

    p_hard = F.softmax(masked_logits, dim=-1).numpy()
    hard_preds = np.argmax(p_hard, axis=1)
    hard_acc = float(np.mean(hard_preds == test_targets))

    # 8. Soft-Gated Disease Predictions
    test_crop_scaled = test_crop_logits / t_crop
    test_disease_scaled = test_disease_logits / t_disease
    p_soft = compute_soft_gated_probs(test_crop_scaled, test_disease_scaled, crop_hierarchy, num_classes).numpy()
    soft_preds = np.argmax(p_soft, axis=1)
    soft_acc = float(np.mean(soft_preds == test_targets))
    soft_ece = compute_ece(p_soft, test_targets)

    # 9. Macro-F1 metrics
    report_dict = classification_report(test_targets, soft_preds, target_names=class_names, output_dict=True, zero_division=0)
    macro_f1_all = report_dict["macro avg"]["f1-score"]

    # Macro-F1 on classes with >= 20 test support
    support_per_class = np.array([report_dict[c]["support"] for c in class_names])
    f1_per_class = np.array([report_dict[c]["f1-score"] for c in class_names])
    mask_ge20 = (support_per_class >= 20)
    macro_f1_ge20 = float(np.mean(f1_per_class[mask_ge20]))

    logger.info("FINAL TEST RESULTS (N=%d):", num_test_images)
    logger.info("  Raw Accuracy          : %.2f%%", raw_acc * 100)
    logger.info("  Hard-Masked Accuracy  : %.2f%%", hard_acc * 100)
    logger.info("  Soft-Gated Accuracy   : %.2f%%", soft_acc * 100)
    logger.info("  Crop-Head Accuracy    : %.2f%%", crop_accuracy * 100)
    logger.info("  Macro-F1 (All 195)    : %.2f%%", macro_f1_all * 100)
    logger.info("  Macro-F1 (Support>=20): %.2f%% (%d classes)", macro_f1_ge20 * 100, int(np.sum(mask_ge20)))
    logger.info("  Raw ECE               : %.2f%%", raw_ece * 100)
    logger.info("  Calibrated ECE        : %.2f%% (T_disease=%.4f)", cal_ece * 100, t_disease)
    logger.info("  Soft-Gated ECE        : %.2f%%", soft_ece * 100)

    # 10. Per-Class Precision / Recall / F1 / Support CSV
    reports_dir = PROJECT_ROOT / "reports" / "v1"
    reports_dir.mkdir(parents=True, exist_ok=True)

    rows = []
    for c in class_names:
        r = report_dict[c]
        rows.append({
            "class_name": c,
            "crop": c.split(" - ")[0] if " - " in c else c,
            "precision": round(r["precision"], 4),
            "recall": round(r["recall"], 4),
            "f1_score": round(r["f1-score"], 4),
            "support": int(r["support"])
        })
    df_classes = pd.DataFrame(rows)
    csv_path = reports_dir / "test_per_class_metrics.csv"
    df_classes.to_csv(csv_path, index=False)
    logger.info("Saved per-class metrics to %s", csv_path)

    # 11. Top 25 Lowest-F1 Classes
    lowest_25 = df_classes.sort_values(by=["f1_score", "support"]).head(25)
    logger.info("Top 25 Lowest-F1 Classes:\n%s", lowest_25[["class_name", "f1_score", "support"]].to_string())

    # 12. Confusion Pairs (Top 30, flagging cross-crop)
    cm = confusion_matrix(test_targets, soft_preds, labels=list(range(num_classes)))
    np.fill_diagonal(cm, 0)
    confusion_pairs = []
    for i in range(num_classes):
        for j in range(num_classes):
            cnt = cm[i, j]
            if cnt > 0:
                true_c = class_names[i]
                pred_c = class_names[j]
                true_crop = true_c.split(" - ")[0] if " - " in true_c else true_c
                pred_crop = pred_c.split(" - ")[0] if " - " in pred_c else pred_c
                confusion_pairs.append({
                    "true_class": true_c,
                    "pred_class": pred_c,
                    "true_crop": true_crop,
                    "pred_crop": pred_crop,
                    "cross_crop": (true_crop != pred_crop),
                    "error_count": int(cnt)
                })
    df_confusion = pd.DataFrame(confusion_pairs).sort_values(by="error_count", ascending=False).head(30)
    logger.info("Top 30 Confusion Pairs:\n%s", df_confusion.to_string())

    # 13. Healthy-vs-Diseased Foliar Decision Metric
    # Healthy defined as 'healthy' in class name
    is_true_healthy = np.array(["healthy" in c.lower() for c in [class_names[t] for t in test_targets]])
    is_pred_healthy = np.array(["healthy" in c.lower() for c in [class_names[p] for p in soft_preds]])

    # True diseased predicted healthy = missed disease (false negative for disease)
    # True healthy predicted diseased = false alarm (false positive for disease)
    total_diseased = int(np.sum(~is_true_healthy))
    missed_disease = int(np.sum((~is_true_healthy) & is_pred_healthy))
    missed_rate = missed_disease / total_diseased if total_diseased > 0 else 0.0

    total_healthy = int(np.sum(is_true_healthy))
    false_alarm = int(np.sum(is_true_healthy & (~is_pred_healthy)))
    false_alarm_rate = false_alarm / total_healthy if total_healthy > 0 else 0.0

    logger.info("FOLIAR HEALTH DECISION METRICS (Overall):")
    logger.info("  Total True Diseased: %d | Missed Disease (pred Healthy): %d (%.2f%%)", total_diseased, missed_disease, missed_rate * 100)
    logger.info("  Total True Healthy : %d | False Alarm (pred Diseased)   : %d (%.2f%%)", total_healthy, false_alarm, false_alarm_rate * 100)

    # Per-Crop Foliar Decision Metric
    per_crop_decision = []
    test_crop_names = [class_names[t].split(" - ")[0] if " - " in class_names[t] else class_names[t] for t in test_targets]
    for crop in sorted(set(test_crop_names)):
        crop_mask = np.array([c == crop for c in test_crop_names])
        c_true_healthy = is_true_healthy[crop_mask]
        c_pred_healthy = is_pred_healthy[crop_mask]

        c_tot_dis = int(np.sum(~c_true_healthy))
        c_missed = int(np.sum((~c_true_healthy) & c_pred_healthy))
        c_miss_rate = c_missed / c_tot_dis if c_tot_dis > 0 else 0.0

        c_tot_heal = int(np.sum(c_true_healthy))
        c_false_alm = int(np.sum(c_true_healthy & (~c_pred_healthy)))
        c_alm_rate = c_false_alm / c_tot_heal if c_tot_heal > 0 else 0.0

        per_crop_decision.append({
            "crop": crop,
            "total_diseased": c_tot_dis,
            "missed_disease": c_missed,
            "missed_disease_rate": round(c_miss_rate, 4),
            "total_healthy": c_tot_heal,
            "false_alarms": c_false_alm,
            "false_alarm_rate": round(c_alm_rate, 4),
        })
    df_per_crop_decision = pd.DataFrame(per_crop_decision)

    # 14. Per-Source Accuracy
    manifest_v1_path = reports_dir / "dataset_v1.csv"
    if manifest_v1_path.exists():
        df_manifest = pd.read_csv(manifest_v1_path)
        # Create map from filename to source
        df_test_manifest = df_manifest[df_manifest["split"] == "test"]
        fname_to_source = {Path(p).name: s for p, s in zip(df_test_manifest["path"], df_test_manifest["source"])}

        sources = [fname_to_source.get(fn, "unknown") for fn in all_fnames]
        correct = (soft_preds == test_targets)

        source_stats = []
        for src in sorted(set(sources)):
            s_mask = np.array([s == src for s in sources])
            cnt = int(np.sum(s_mask))
            acc = float(np.mean(correct[s_mask]))
            source_stats.append({
                "source": src,
                "count": cnt,
                "share": round(cnt / len(test_targets), 4),
                "accuracy": round(acc, 4)
            })
        df_sources = pd.DataFrame(source_stats).sort_values(by="count", ascending=False)
        logger.info("Per-Source Accuracy:\n%s", df_sources.to_string())
    else:
        df_sources = pd.DataFrame()

    # Save summary results JSON
    results = {
        "num_test_images": num_test_images,
        "num_classes": num_classes,
        "num_crops": num_crops,
        "crop_head_accuracy": crop_accuracy,
        "disease_head": {
            "raw_accuracy": raw_acc,
            "hard_masked_accuracy": hard_acc,
            "soft_gated_accuracy": soft_acc,
            "raw_ece": raw_ece,
            "calibrated_raw_ece": cal_ece,
            "soft_gated_ece": soft_ece,
            "macro_f1_all_classes": macro_f1_all,
            "macro_f1_ge20_support": macro_f1_ge20,
            "num_classes_ge20_support": int(np.sum(mask_ge20)),
        },
        "foliar_decision_metrics_overall": {
            "total_diseased": total_diseased,
            "missed_disease": missed_disease,
            "missed_disease_rate": missed_rate,
            "total_healthy": total_healthy,
            "false_alarms": false_alarm,
            "false_alarm_rate": false_alarm_rate,
        },
        "top_25_lowest_f1": lowest_25.to_dict(orient="records"),
        "top_30_confusion_pairs": df_confusion.to_dict(orient="records"),
        "per_crop_decision": df_per_crop_decision.to_dict(orient="records"),
        "per_source_stats": df_sources.to_dict(orient="records") if not df_sources.empty else []
    }

    out_json = reports_dir / "final_test_evaluation.json"
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    logger.info("Saved final test evaluation results to %s", out_json)


if __name__ == "__main__":
    main()
