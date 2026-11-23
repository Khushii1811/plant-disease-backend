"""
scripts/v1/evaluate_common_test.py

Evaluates Baseline Model v0 and Production Release Model v1 (195 classes)
strictly on the COMMON test set (N=10,321 images matched by SHA-256).
Uses reports/history/v0_test_predictions.csv and data/processed/test.
Computes:
1. Overall Accuracy and Macro-F1 on common test set for v0 and v1.
2. Metrics excluding the 6 patched classes.
3. Individual contribution of each of the 6 patched classes.
4. Top 15 improved and top 15 regressed non-patched classes with support.
5. Total number of classes whose F1 changed by > 5 points (>0.05).
6. Cross-checks against v0 baseline numbers.
"""

import contextlib
import sys
import json
import logging
import hashlib
from pathlib import Path
from collections import defaultdict

import numpy as np
import pandas as pd
from PIL import Image
import torch
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
from sklearn.metrics import classification_report
from tqdm import tqdm

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
import config
from src.models.convnext import build_dualhead_convnext_tiny

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("common_test_eval")


def get_file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


class ExplicitImageDataset(Dataset):
    def __init__(self, samples, transform):
        self.samples = samples  # (Path, target_idx)
        self.transform = transform

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        path, target = self.samples[idx]
        with open(path, "rb") as f:
            img = Image.open(f).convert("RGB")
        return self.transform(img), target


def main():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    logger.info("Using device: %s", device)

    # 1. Load Baseline v0 Test Predictions
    v0_preds_path = PROJECT_ROOT / "reports" / "history" / "v0_test_predictions.csv"
    v0_df = pd.read_csv(v0_preds_path)
    logger.info("Loaded v0 test predictions: %d samples", len(v0_df))

    # 2. Map current test files in data/processed/test
    v1_test_files = sorted([p for p in (config.DATA_DIR / "processed" / "test").rglob("*") if p.is_file() and p.suffix.lower() in ('.jpg', '.jpeg', '.png')])
    logger.info("Found %d test files on disk.", len(v1_test_files))

    v1_sha_to_path = {}
    v1_path_to_sha = {}
    for p in v1_test_files:
        sha = get_file_sha256(p)
        v1_sha_to_path[sha] = p
        v1_path_to_sha[str(p.resolve())] = sha

    v0_sha_to_row = {}
    for idx, row in v0_df.iterrows():
        p = Path(row["image_path"])
        p_res = str(p.resolve())
        if p_res in v1_path_to_sha:
            sha = v1_path_to_sha[p_res]
            v0_sha_to_row[sha] = row
        elif p.exists():
            sha = get_file_sha256(p)
            v0_sha_to_row[sha] = row

    # Intersection: images present in both v0 test and v1 test
    common_shas = sorted(list(set(v1_sha_to_path.keys()).intersection(set(v0_sha_to_row.keys()))))
    logger.info("COMMON TEST SET SIZE: %d IMAGES", len(common_shas))
    assert len(common_shas) in (10321, 9553), f"Expected 10,321 or 9,553 common images, got {len(common_shas)}"

    # Load bundle metadata
    with open(PROJECT_ROOT / "models" / "v0" / "class_names.json", "r", encoding="utf-8") as f:
        v0_classes = json.load(f)
    v0_class_to_idx = {c: i for i, c in enumerate(v0_classes)}

    with open(PROJECT_ROOT / "models" / "v1" / "class_names.json", "r", encoding="utf-8") as f:
        v1_classes = json.load(f)
    v1_class_to_idx = {c: i for i, c in enumerate(v1_classes)}

    eval_transform = transforms.Compose([
        transforms.Resize((256, 256)),
        transforms.ToTensor(),
        transforms.Normalize(mean=config.NORMALIZE_MEAN, std=config.NORMALIZE_STD),
    ])

    v0_samples = []
    v1_samples = []
    class_labels = []

    for sha in common_shas:
        p = v1_sha_to_path[sha]
        cname = p.parent.name
        class_labels.append(cname)
        v0_samples.append((p, v0_class_to_idx[cname]))
        v1_samples.append((p, v1_class_to_idx[cname]))

    # Load models
    logger.info("Loading Baseline Model v0...")
    model_v0 = build_dualhead_convnext_tiny(num_crops=34, num_classes=198, pretrained=False)
    model_v0.load_state_dict(torch.load(PROJECT_ROOT / "models" / "v0" / "model_dualhead_convnext_tiny.pth", map_location="cpu", weights_only=False))
    model_v0.to(device).eval()

    logger.info("Loading Production Model v1...")
    model_v1 = build_dualhead_convnext_tiny(num_crops=34, num_classes=195, pretrained=False)
    model_v1.load_state_dict(torch.load(PROJECT_ROOT / "models" / "v1" / "model_dualhead_convnext_tiny.pth", map_location="cpu", weights_only=False))
    model_v1.to(device).eval()

    loader_v0 = DataLoader(ExplicitImageDataset(v0_samples, eval_transform), batch_size=32, shuffle=False, num_workers=0)
    loader_v1 = DataLoader(ExplicitImageDataset(v1_samples, eval_transform), batch_size=32, shuffle=False, num_workers=0)

    # Inference v0
    v0_preds = []
    v0_targets = []
    with torch.no_grad():
        for imgs, tgts in tqdm(loader_v0, desc="v0 Common Eval"):
            imgs = imgs.to(device)
            autocast_ctx = torch.amp.autocast(device_type="cuda", dtype=torch.float16) if device.type == "cuda" else contextlib.nullcontext()
            with autocast_ctx:
                _, d_logits = model_v0(imgs)
            preds = torch.argmax(d_logits, dim=-1).cpu().numpy()
            v0_preds.extend(preds)
            v0_targets.extend(tgts.numpy())

    v0_preds = np.array(v0_preds)
    v0_targets = np.array(v0_targets)

    # Inference v1
    v1_preds = []
    v1_targets = []
    with torch.no_grad():
        for imgs, tgts in tqdm(loader_v1, desc="v1 Common Eval"):
            imgs = imgs.to(device)
            autocast_ctx = torch.amp.autocast(device_type="cuda", dtype=torch.float16) if device.type == "cuda" else contextlib.nullcontext()
            with autocast_ctx:
                _, d_logits = model_v1(imgs)
            preds = torch.argmax(d_logits, dim=-1).cpu().numpy()
            v1_preds.extend(preds)
            v1_targets.extend(tgts.numpy())

    v1_preds = np.array(v1_preds)
    v1_targets = np.array(v1_targets)

    # 1. Overall Metrics
    v0_acc = float(np.mean(v0_preds == v0_targets))
    v1_acc = float(np.mean(v1_preds == v1_targets))

    report_v0 = classification_report(v0_targets, v0_preds, target_names=v0_classes, output_dict=True, zero_division=0)
    report_v1 = classification_report(v1_targets, v1_preds, target_names=v1_classes, output_dict=True, zero_division=0)

    v0_macro_f1 = report_v0["macro avg"]["f1-score"]
    v1_macro_f1 = report_v1["macro avg"]["f1-score"]

    logger.info("OVERALL COMMON TEST METRICS (N=%d):", len(common_shas))
    logger.info("  v0 Baseline Accuracy : %.4f (%.2f%%)", v0_acc, v0_acc * 100)
    logger.info("  v1 Release Accuracy  : %.4f (%.2f%%)", v1_acc, v1_acc * 100)
    logger.info("  Accuracy Delta       : %+.4f (%+.2f%%)", v1_acc - v0_acc, (v1_acc - v0_acc) * 100)
    logger.info("  v0 Baseline Macro-F1 : %.4f (%.2f%%)", v0_macro_f1, v0_macro_f1 * 100)
    logger.info("  v1 Release Macro-F1  : %.4f (%.2f%%)", v1_macro_f1, v1_macro_f1 * 100)
    logger.info("  Macro-F1 Delta       : %+.4f (%+.2f%%)", v1_macro_f1 - v0_macro_f1, (v1_macro_f1 - v0_macro_f1) * 100)

    # 2. Metrics Excluding Patched Classes
    patched_classes = [
        "Bell Pepper - Leaf Curl",
        "Bell Pepper - Nutrition",
        "Bell Pepper - Powdery Mildew",
        "Bell Pepper - Bacterial Spot",
        "Citrus - citrus greening disease",
        "Soybean - healthy"
    ]

    non_patched_mask = np.array([c not in patched_classes for c in class_labels])
    v0_acc_excl = float(np.mean(v0_preds[non_patched_mask] == v0_targets[non_patched_mask]))
    v1_acc_excl = float(np.mean(v1_preds[non_patched_mask] == v1_targets[non_patched_mask]))

    non_patched_classes = [c for c in v1_classes if c not in patched_classes]
    v0_f1_excl = np.mean([report_v0[c]["f1-score"] for c in non_patched_classes])
    v1_f1_excl = np.mean([report_v1[c]["f1-score"] for c in non_patched_classes])

    logger.info("METRICS EXCLUDING 6 PATCHED CLASSES (N=%d):", int(np.sum(non_patched_mask)))
    logger.info("  v0 Accuracy (excl) : %.4f (%.2f%%)", v0_acc_excl, v0_acc_excl * 100)
    logger.info("  v1 Accuracy (excl) : %.4f (%.2f%%)", v1_acc_excl, v1_acc_excl * 100)
    logger.info("  Accuracy Delta     : %+.4f (%+.2f%%)", v1_acc_excl - v0_acc_excl, (v1_acc_excl - v0_acc_excl) * 100)
    logger.info("  v0 Macro-F1 (excl) : %.4f (%.2f%%)", v0_f1_excl, v0_f1_excl * 100)
    logger.info("  v1 Macro-F1 (excl) : %.4f (%.2f%%)", v1_f1_excl, v1_f1_excl * 100)
    logger.info("  Macro-F1 Delta     : %+.4f (%+.2f%%)", v1_f1_excl - v0_f1_excl, (v1_f1_excl - v0_f1_excl) * 100)

    # 3. Individual Contribution of Each Patched Class
    logger.info("INDIVIDUAL CONTRIBUTIONS OF PATCHED CLASSES:")
    patched_stats = {}
    for pc in patched_classes:
        mask = np.array([c == pc for c in class_labels])
        supp = int(np.sum(mask))
        if supp > 0:
            pc_acc_v0 = float(np.mean(v0_preds[mask] == v0_targets[mask]))
            pc_acc_v1 = float(np.mean(v1_preds[mask] == v1_targets[mask]))
            f1_v0 = report_v0[pc]["f1-score"] if pc in report_v0 else 0.0
            f1_v1 = report_v1[pc]["f1-score"] if pc in report_v1 else 0.0
            patched_stats[pc] = {
                "support": supp,
                "v0_acc": pc_acc_v0,
                "v1_acc": pc_acc_v1,
                "acc_delta": pc_acc_v1 - pc_acc_v0,
                "v0_f1": f1_v0,
                "v1_f1": f1_v1,
                "f1_delta": f1_v1 - f1_v0
            }
            logger.info("  %s (N=%d): v0 F1=%.4f -> v1 F1=%.4f (Delta: %+.4f, Acc Delta: %+.2f%%)",
                        pc, supp, f1_v0, f1_v1, f1_v1 - f1_v0, (pc_acc_v1 - pc_acc_v0) * 100)

    # 4. Top 15 Improved & Top 15 Regressed Non-Patched Classes
    deltas = []
    for c in non_patched_classes:
        f1_v0 = report_v0[c]["f1-score"]
        f1_v1 = report_v1[c]["f1-score"]
        diff = f1_v1 - f1_v0
        supp = report_v0[c]["support"]
        deltas.append({
            "class_name": c,
            "crop": c.split(" - ")[0] if " - " in c else c,
            "support": int(supp),
            "v0_f1": round(f1_v0, 4),
            "v1_f1": round(f1_v1, 4),
            "f1_delta": round(diff, 4)
        })

    df_deltas = pd.DataFrame(deltas)
    top_improved = df_deltas.sort_values(by="f1_delta", ascending=False).head(15)
    top_regressed = df_deltas.sort_values(by="f1_delta", ascending=True).head(15)
    num_changed_gt5 = int(np.sum(np.abs(df_deltas["f1_delta"]) > 0.05))

    logger.info("Number of non-patched classes changing by > 5 F1 points: %d", num_changed_gt5)

    reports_dir = PROJECT_ROOT / "reports" / "v1"
    reports_dir.mkdir(parents=True, exist_ok=True)
    out_json = reports_dir / "common_test_comparison.json"
    results = {
        "num_common_images": len(common_shas),
        "overall_common": {
            "v0_accuracy": v0_acc,
            "v1_accuracy": v1_acc,
            "accuracy_delta": v1_acc - v0_acc,
            "v0_macro_f1": v0_macro_f1,
            "v1_macro_f1": v1_macro_f1,
            "macro_f1_delta": v1_macro_f1 - v0_macro_f1
        },
        "excluding_patched_classes": {
            "num_images": int(np.sum(non_patched_mask)),
            "v0_accuracy": v0_acc_excl,
            "v1_accuracy": v1_acc_excl,
            "accuracy_delta": v1_acc_excl - v0_acc_excl,
            "v0_macro_f1": v0_f1_excl,
            "v1_macro_f1": v1_f1_excl,
            "macro_f1_delta": v1_f1_excl - v0_f1_excl
        },
        "patched_classes_contribution": patched_stats,
        "classes_changed_gt_5_f1_points": num_changed_gt5,
        "top_15_improved": top_improved.to_dict(orient="records"),
        "top_15_regressed": top_regressed.to_dict(orient="records")
    }

    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    df_deltas.to_csv(reports_dir / "common_test_per_class_deltas.csv", index=False)
    logger.info("Saved comparison results to %s", out_json)


if __name__ == "__main__":
    main()
