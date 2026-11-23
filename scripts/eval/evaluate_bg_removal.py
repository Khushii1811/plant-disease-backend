import os
import sys
import time
import json
from pathlib import Path
import numpy as np
import pandas as pd
from PIL import Image
from sklearn.metrics import f1_score
from sklearn.model_selection import StratifiedShuffleSplit
import torch

sys.path.insert(0, os.path.abspath('.'))

import config
from src.data.preprocess import get_val_transforms, load_image
from src.data.bg_removal import remove_background, get_rembg_session
from src.models.bundle_loader import load_model_bundle
from src.models.predict import predict_tensor

print("Configuring deterministic single-thread CPU execution for PyTorch model...", flush=True)
torch.set_num_threads(1)
torch.use_deterministic_algorithms(True)

print("Loading model bundle 'v1' on CPU...", flush=True)
bundle = load_model_bundle("v1", device="cpu")
bundle.model.eval()

class_names = bundle.class_names
crops = bundle.crop_hierarchy["crops"]
class_to_idx = {name: i for i, name in enumerate(class_names)}
crop_to_idx = {name: i for i, name in enumerate(crops)}
class_idx_to_crop = torch.tensor(bundle.crop_hierarchy["class_idx_to_crop_idx"], dtype=torch.long, device="cpu")

# Warm up rembg session
print("Warming up rembg session...", flush=True)
_ = get_rembg_session()
_dummy_img = Image.new('RGB', (256, 256), color=(60, 140, 70))
_ = remove_background(_dummy_img)
print("rembg session warmed up.", flush=True)

# Load test dataset manifest
df = pd.read_csv('reports/v1/dataset_v1.csv')
test_df = df[df['split'] == 'test'].copy().reset_index(drop=True)
print(f"Total test set images in manifest: {len(test_df)}", flush=True)

# Seeded stratified sampling of 1,500 images across all 177 classes
target_n = 1500
total_n = len(test_df)
sampled_dfs = []
for c, group in test_df.groupby('class'):
    n_sample = max(1, int(round(len(group) * target_n / total_n)))
    sampled_dfs.append(group.sample(n=min(len(group), n_sample), random_state=42))

sample_df = pd.concat(sampled_dfs).reset_index(drop=True)
if len(sample_df) > 1500:
    drop_candidates = sample_df[sample_df['class'].isin(sample_df['class'].value_counts()[sample_df['class'].value_counts() > 5].index)]
    drop_idx = drop_candidates.sample(n=len(sample_df) - 1500, random_state=42).index
    sample_df = sample_df.drop(drop_idx).reset_index(drop=True)
elif len(sample_df) < 1500:
    rem = test_df.drop(sample_df.index)
    add_df = rem.sample(n=1500 - len(sample_df), random_state=42)
    sample_df = pd.concat([sample_df, add_df]).reset_index(drop=True)

print(f"Sampled {len(sample_df)} images across {sample_df['class'].nunique()} unique classes.", flush=True)

transform = get_val_transforms()

y_true_disease = []
y_true_crop = []

y_pred_disease_clean = []
y_pred_crop_clean = []
latencies_clean = []

y_pred_disease_bg = []
y_pred_crop_bg = []
latencies_bg_rem = []
latencies_bg_inf = []

total_samples = len(sample_df)
t_start_all = time.time()

for i, row in sample_df.iterrows():
    p = Path(row["path"])
    if not p.exists():
        p = Path("e:/Sprayer/plant-disease-backend") / p
    
    true_d_idx = class_to_idx[row["class"]]
    true_c_idx = crop_to_idx[row["crop"]]
    y_true_disease.append(true_d_idx)
    y_true_crop.append(true_c_idx)

    img = load_image(p)

    # 1. Clean evaluation (without background removal)
    t0 = time.perf_counter()
    tensor_clean = transform(img).unsqueeze(0)
    out_clean = predict_tensor(
        bundle.model, tensor_clean, class_idx_to_crop, bundle.T_crop, bundle.T_disease, None
    )
    t1 = time.perf_counter()
    latencies_clean.append((t1 - t0) * 1000)

    pred_d_clean = int(out_clean["p_joint"].argmax(dim=-1).item())
    pred_c_clean = int(out_clean["c_logits"].argmax(dim=-1).item())
    y_pred_disease_clean.append(pred_d_clean)
    y_pred_crop_clean.append(pred_c_clean)

    # 2. Evaluation with background removal
    t2 = time.perf_counter()
    img_bg, _ = remove_background(img)
    t3 = time.perf_counter()
    latencies_bg_rem.append((t3 - t2) * 1000)

    tensor_bg = transform(img_bg).unsqueeze(0)
    t4 = time.perf_counter()
    out_bg = predict_tensor(
        bundle.model, tensor_bg, class_idx_to_crop, bundle.T_crop, bundle.T_disease, None
    )
    t5 = time.perf_counter()
    latencies_bg_inf.append((t5 - t4) * 1000)

    pred_d_bg = int(out_bg["p_joint"].argmax(dim=-1).item())
    pred_c_bg = int(out_bg["c_logits"].argmax(dim=-1).item())
    y_pred_disease_bg.append(pred_d_bg)
    y_pred_crop_bg.append(pred_c_bg)

    if (i + 1) % 100 == 0 or (i + 1) == total_samples:
        elapsed = time.time() - t_start_all
        rate = (i + 1) / elapsed
        rem_sec = (total_samples - (i + 1)) / rate
        print(f"Progress: [{i+1}/{total_samples}] ({rate:.1f} img/s) - ETA {rem_sec/60:.1f} min", flush=True)

# Metrics computation
y_true_disease = np.array(y_true_disease)
y_true_crop = np.array(y_true_crop)

y_pred_disease_clean = np.array(y_pred_disease_clean)
y_pred_crop_clean = np.array(y_pred_crop_clean)

y_pred_disease_bg = np.array(y_pred_disease_bg)
y_pred_crop_bg = np.array(y_pred_crop_bg)

# Clean metrics
correct_crop_clean = int(np.sum(y_true_crop == y_pred_crop_clean))
crop_acc_clean = float(correct_crop_clean / total_samples * 100.0)
correct_disease_clean = int(np.sum(y_true_disease == y_pred_disease_clean))
disease_acc_clean = float(correct_disease_clean / total_samples * 100.0)
macro_f1_clean = float(f1_score(y_true_disease, y_pred_disease_clean, average="macro", zero_division=0) * 100.0)
avg_lat_clean = float(np.mean(latencies_clean))

# Background removal metrics
correct_crop_bg = int(np.sum(y_true_crop == y_pred_crop_bg))
crop_acc_bg = float(correct_crop_bg / total_samples * 100.0)
correct_disease_bg = int(np.sum(y_true_disease == y_pred_disease_bg))
disease_acc_bg = float(correct_disease_bg / total_samples * 100.0)
macro_f1_bg = float(f1_score(y_true_disease, y_pred_disease_bg, average="macro", zero_division=0) * 100.0)
avg_lat_bg_rem = float(np.mean(latencies_bg_rem))
avg_lat_bg_inf = float(np.mean(latencies_bg_inf))
avg_lat_bg_total = avg_lat_bg_rem + avg_lat_bg_inf

# Comparison
changed_mask = (y_pred_disease_clean != y_pred_disease_bg)
num_changed = int(np.sum(changed_mask))

clean_corr_bg_wrong = int(np.sum((y_pred_disease_clean == y_true_disease) & (y_pred_disease_bg != y_true_disease)))
clean_wrong_bg_corr = int(np.sum((y_pred_disease_clean != y_true_disease) & (y_pred_disease_bg == y_true_disease)))
both_correct = int(np.sum((y_pred_disease_clean == y_true_disease) & (y_pred_disease_bg == y_true_disease)))
both_wrong = int(np.sum((y_pred_disease_clean != y_true_disease) & (y_pred_disease_bg != y_true_disease)))

results = {
    "metadata": {
        "evaluation_target": "Background Removal (BETA) vs Raw Image",
        "sample_size": total_samples,
        "sample_strategy": "Seeded stratified sample (1 per class + proportional remainder, seed=42)",
        "num_classes": len(class_names),
        "num_crops": len(crops),
        "device": "cpu",
        "threads": 1,
        "deterministic": True,
        "bg_color": "RGB(220, 220, 220)",
        "model_architecture": "ConvNeXt-Tiny DualHead (bundle v1)",
    },
    "without_bg_removal": {
        "correct_crop": correct_crop_clean,
        "crop_accuracy_pct": round(crop_acc_clean, 2),
        "correct_disease": correct_disease_clean,
        "soft_gated_disease_accuracy_pct": round(disease_acc_clean, 2),
        "macro_f1_pct": round(macro_f1_clean, 2),
        "latency_per_image_ms": round(avg_lat_clean, 2),
    },
    "with_bg_removal": {
        "correct_crop": correct_crop_bg,
        "crop_accuracy_pct": round(crop_acc_bg, 2),
        "correct_disease": correct_disease_bg,
        "soft_gated_disease_accuracy_pct": round(disease_acc_bg, 2),
        "macro_f1_pct": round(macro_f1_bg, 2),
        "rembg_latency_ms": round(avg_lat_bg_rem, 2),
        "inference_latency_ms": round(avg_lat_bg_inf, 2),
        "total_latency_per_image_ms": round(avg_lat_bg_total, 2),
    },
    "impact_comparison": {
        "num_predictions_changed": num_changed,
        "pct_predictions_changed": round(num_changed / total_samples * 100.0, 2),
        "both_correct": both_correct,
        "both_wrong": both_wrong,
        "clean_correct_but_bg_wrong (degraded)": clean_corr_bg_wrong,
        "clean_wrong_but_bg_correct (improved)": clean_wrong_bg_corr,
        "net_accuracy_delta_pct": round(disease_acc_bg - disease_acc_clean, 2),
        "net_crop_accuracy_delta_pct": round(crop_acc_bg - crop_acc_clean, 2),
        "net_macro_f1_delta_pct": round(macro_f1_bg - macro_f1_clean, 2),
    }
}

out_path = Path("scratch/site_audit/bg_removal_eval.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)

print("\n--- RESULTS SUMMARY ---", flush=True)
print(f"Clean Soft-Gated Accuracy: {disease_acc_clean:.2f}% (Correct: {correct_disease_clean}/{total_samples})", flush=True)
print(f"BG-Rem Soft-Gated Accuracy: {disease_acc_bg:.2f}% (Correct: {correct_disease_bg}/{total_samples})", flush=True)
print(f"Net Accuracy Delta: {disease_acc_bg - disease_acc_clean:+.2f}%", flush=True)
print(f"Predictions Changed: {num_changed}/{total_samples} ({num_changed/total_samples*100:.2f}%)", flush=True)
print(f"Degraded: {clean_corr_bg_wrong}, Improved: {clean_wrong_bg_corr}", flush=True)
print(f"Output saved to {out_path}", flush=True)
