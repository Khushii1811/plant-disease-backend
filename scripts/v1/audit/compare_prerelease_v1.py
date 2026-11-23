"""
scripts/v1/audit/compare_prerelease_v1.py

Paired statistical comparison between Model v1 and the Prerelease baseline on
the clean shared held-out test subset (excluding Mango - Sooty Mould, the single
shared class modified in Patch P-005).

Inputs:
  - models/v1/class_names.json, models/prerelease/class_names.json
  - models/v1/crop_hierarchy.json, models/prerelease/crop_hierarchy.json
  - models/v1/calibration.json
  - reports/v1/dataset_v1.csv
  - reports/v1/leaky_eval_images.csv

Produces:
  - reports/v1/comparison_prerelease_v1.json (paired delta, bootstrap 95% CI, McNemar test)
"""

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import numpy as np
import pandas as pd
import torch
from scipy import stats

import config


def mcnemar_test(y_true, y_pred1, y_pred2):
    c1 = y_pred1 == y_true
    c2 = y_pred2 == y_true

    n00 = int(np.sum(~c1 & ~c2))
    n01 = int(np.sum(~c1 & c2))  # model 2 correct, model 1 incorrect
    n10 = int(np.sum(c1 & ~c2))  # model 1 correct, model 2 incorrect
    n11 = int(np.sum(c1 & c2))

    b = n10
    c = n01
    chi2 = ((abs(b - c) - 1.0) ** 2) / (b + c) if (b + c) > 0 else 0.0
    p_val = stats.chi2.sf(chi2, df=1) if (b + c) > 0 else 1.0
    exact_p = stats.binomtest(b, b + c, p=0.5).pvalue if (b + c) > 0 else 1.0

    return {
        "contingency_table": {
            "both_correct": n11,
            "both_incorrect": n00,
            "pre_only": b,
            "v1_only": c,
        },
        "chi2": float(chi2),
        "p_value_chi2": float(p_val),
        "p_value_exact": float(exact_p),
    }


def main():
    print("=" * 80)
    print("PAIRED COMPARISON: MODEL V1 vs PRERELEASE BASELINE ON CLEAN SHARED TEST SET")
    print("=" * 80)

    with open(config.PROJECT_ROOT / "models" / "v1" / "class_names.json", encoding="utf-8") as f:
        v1_classes = json.load(f)
    with open(config.PROJECT_ROOT / "models" / "prerelease" / "class_names.json", encoding="utf-8") as f:
        pre_classes = json.load(f)

    shared_classes = sorted(list(set(v1_classes).intersection(set(pre_classes))))
    print(f"Total shared classes: {len(shared_classes)}")

    eval_classes = [c for c in shared_classes if c != "Mango - Sooty Mould"]
    print(f"Evaluation classes (excluding Mango - Sooty Mould): {len(eval_classes)}")
    eval_set = set(eval_classes)

    manifest = pd.read_csv(config.PROJECT_ROOT / "reports" / "v1" / "dataset_v1.csv")
    test_manifest = manifest[manifest["split"] == "test"].reset_index(drop=True)

    leaky_csv = config.PROJECT_ROOT / "data" / "patches" / "history" / "leaky_eval_images_historical_343.csv"
    if not leaky_csv.exists():
        leaky_csv = config.PROJECT_ROOT / "reports" / "v1" / "removed_p007_images.csv"
    leaky_df = pd.read_csv(leaky_csv)
    col = "eval_path" if "eval_path" in leaky_df.columns else "relative_path"
    split_col = "eval_split" if "eval_split" in leaky_df.columns else "split"
    leaky_test_paths = set(
        leaky_df[leaky_df[split_col] == "test"][col].str.replace("\\", "/")
    )

    test_manifest["is_clean"] = [
        p.replace("\\", "/") not in leaky_test_paths for p in test_manifest["path"]
    ]
    test_manifest["in_eval_classes"] = test_manifest["class"].isin(eval_set)

    target_mask = (test_manifest["is_clean"] & test_manifest["in_eval_classes"]).to_numpy()
    N_eval = int(target_mask.sum())
    print(f"Target Clean Shared Test Images: N = {N_eval:,}")

    # Check cached logits or audit_output cache
    cache_dir = config.PROJECT_ROOT / "artifacts" / "cached_features"
    alt_cache_dir = config.PROJECT_ROOT / "audit_output" / "phase2b"

    v1_logits_path = (
        cache_dir / "test_v1_logits.pt"
        if (cache_dir / "test_v1_logits.pt").exists()
        else alt_cache_dir / "test_v1_logits.pt"
    )
    pre_logits_path = (
        cache_dir / "test_prerelease_logits.pt"
        if (cache_dir / "test_prerelease_logits.pt").exists()
        else alt_cache_dir / "test_prerelease_logits.pt"
    )

    if not (v1_logits_path.exists() and pre_logits_path.exists()):
        print(f"Cached logits missing ({v1_logits_path}, {pre_logits_path}).")
        print("Run scripts/v1/audit/eval_clean_subset_and_calibration.py to generate cached logits.")
        return

    v1_logits_data = torch.load(v1_logits_path, map_location="cpu", weights_only=False)
    pre_logits_data = torch.load(pre_logits_path, map_location="cpu", weights_only=False)

    with open(config.PROJECT_ROOT / "models" / "v1" / "calibration.json", encoding="utf-8") as f:
        v1_cal = json.load(f)
    v1_Tc = float(v1_cal["T_crop"])
    v1_Td = float(v1_cal["T_disease"])

    with open(config.PROJECT_ROOT / "models" / "v1" / "crop_hierarchy.json", encoding="utf-8") as f:
        v1_hier = json.load(f)
    v1_cls_to_crop = torch.tensor(v1_hier["class_idx_to_crop_idx"], dtype=torch.long)

    v1_pc = torch.softmax(v1_logits_data["c_logits"] / v1_Tc, dim=-1)
    v1_pd = torch.softmax(v1_logits_data["d_logits"] / v1_Td, dim=-1)
    v1_pjoint = v1_pc[:, v1_cls_to_crop] * v1_pd
    v1_preds_idx = v1_pjoint.argmax(dim=-1).numpy()
    v1_preds_class = np.array([v1_classes[i] for i in v1_preds_idx])

    pre_Tc = 0.6356
    pre_Td = 0.5327
    with open(config.PROJECT_ROOT / "models" / "prerelease" / "crop_hierarchy.json", encoding="utf-8") as f:
        pre_hier = json.load(f)
    pre_cls_to_crop = torch.tensor(pre_hier["class_idx_to_crop_idx"], dtype=torch.long)

    pre_pc = torch.softmax(pre_logits_data["c_logits"] / pre_Tc, dim=-1)
    pre_pd = torch.softmax(pre_logits_data["d_logits"] / pre_Td, dim=-1)
    pre_pjoint = pre_pc[:, pre_cls_to_crop] * pre_pd
    pre_preds_idx = pre_pjoint.argmax(dim=-1).numpy()
    pre_preds_class = np.array([pre_classes[i] for i in pre_preds_idx])

    y_true = test_manifest["class"].to_numpy()[target_mask]
    v1_sub = v1_preds_class[target_mask]
    pre_sub = pre_preds_class[target_mask]

    v1_corr = v1_sub == y_true
    pre_corr = pre_sub == y_true

    v1_acc = float(v1_corr.mean())
    pre_acc = float(pre_corr.mean())
    delta = v1_acc - pre_acc

    rng = np.random.RandomState(42)
    boot_deltas = []
    for _ in range(1000):
        b_idx = rng.choice(N_eval, size=N_eval, replace=True)
        b_v1_acc = v1_corr[b_idx].mean()
        b_pre_acc = pre_corr[b_idx].mean()
        boot_deltas.append(b_v1_acc - b_pre_acc)

    ci_lower = float(np.percentile(boot_deltas, 2.5))
    ci_upper = float(np.percentile(boot_deltas, 97.5))

    mcnemar = mcnemar_test(y_true, pre_sub, v1_sub)

    print("-" * 80)
    print(f"RESULTS ON CLEAN SHARED TEST SET (N = {N_eval:,}, 172 Classes):")
    print(f"  Prerelease Accuracy : {pre_acc*100:.2f}% ({pre_corr.sum()}/{N_eval})")
    print(f"  Model v1 Accuracy   : {v1_acc*100:.2f}% ({v1_corr.sum()}/{N_eval})")
    print(f"  Accuracy Delta      : {delta*100:+.2f}% (95% Bootstrap CI: [{ci_lower*100:+.2f}%, {ci_upper*100:+.2f}%])")
    print(f"  McNemar chi2        : {mcnemar['chi2']:.2f} (p = {mcnemar['p_value_chi2']:.4e})")
    print("-" * 80)

    out_payload = {
        "n_eval_images": N_eval,
        "n_classes": len(eval_classes),
        "prerelease_accuracy": pre_acc,
        "v1_accuracy": v1_acc,
        "delta": delta,
        "ci_95": [ci_lower, ci_upper],
        "mcnemar": mcnemar,
    }

    out_path = config.PROJECT_ROOT / "reports" / "v1" / "comparison_prerelease_v1.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out_payload, f, indent=2)
    print(f"Saved comparison report -> {out_path}")


if __name__ == "__main__":
    main()
