"""
scripts/v1/run_calibration.py

Fits T_disease and T_crop on the VALIDATION split only for the chosen v1 checkpoint (Epoch 20).
Uses the exact same method as scripts/investigate_calibration_and_soft_gating.py:
- TemperatureScaler with L-BFGS optimizer minimizing Negative Log-Likelihood (CrossEntropyLoss).
- Computes uncalibrated ECE and calibrated ECE on the validation split.
- Writes models/v1/calibration.json.
"""

import contextlib
import sys
import json
import logging
from pathlib import Path
from datetime import datetime, timezone

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
from tqdm import tqdm

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import config
from src.models.convnext import build_dualhead_convnext_tiny

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("v1_calibration")


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


class TemperatureScaler(nn.Module):
    def __init__(self, init_t: float = 1.0):
        super().__init__()
        self.log_temperature = nn.Parameter(torch.tensor([float(init_t)]).log())

    @property
    def temperature(self) -> torch.Tensor:
        return self.log_temperature.exp()

    def forward(self, logits: torch.Tensor) -> torch.Tensor:
        return logits / self.temperature

    def fit(self, logits: torch.Tensor, targets: torch.Tensor, lr: float = 0.05, max_iter: int = 200) -> float:
        optimizer = torch.optim.LBFGS([self.log_temperature], lr=lr, max_iter=max_iter, line_search_fn="strong_wolfe")
        loss_fn = nn.CrossEntropyLoss()

        def closure():
            optimizer.zero_grad()
            scaled_logits = self.forward(logits)
            loss = loss_fn(scaled_logits, targets)
            loss.backward()
            return loss

        optimizer.step(closure)
        return float(self.temperature.item())


def main():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    logger.info("Using device: %s", device)

    # 1. Validation Dataset and Loader
    val_dir = config.DATA_DIR / "processed" / "val"
    val_transform = transforms.Compose([
        transforms.Resize(config.IMAGE_SIZE),
        transforms.ToTensor(),
        transforms.Normalize(mean=config.NORMALIZE_MEAN, std=config.NORMALIZE_STD),
    ])

    val_dataset = datasets.ImageFolder(str(val_dir), transform=val_transform)
    num_val_images = len(val_dataset)
    hierarchy_path = PROJECT_ROOT / "models" / "v1" / "crop_hierarchy.json"
    if not hierarchy_path.exists():
        raise FileNotFoundError(f"Missing crop hierarchy at {hierarchy_path}")
    crop_hierarchy = json.loads(hierarchy_path.read_text(encoding="utf-8"))
    expected_classes = crop_hierarchy["num_classes"]
    num_crops = crop_hierarchy["num_crops"]
    num_classes = len(val_dataset.classes)
    logger.info("Validation samples: %d across %d classes", num_val_images, num_classes)
    assert num_classes == expected_classes, f"Expected {expected_classes} classes in v1, got {num_classes}"

    val_loader = DataLoader(
        val_dataset,
        batch_size=32,
        shuffle=False,
        num_workers=config.NUM_WORKERS,
        pin_memory=True if device.type == "cuda" else False,
    )

    # 2. Crop mapping
    class_idx_to_crop_idx = torch.tensor(crop_hierarchy["class_idx_to_crop_idx"], dtype=torch.long)
    logger.info("Total Crops: %d", num_crops)

    # 3. Load Model
    model = build_dualhead_convnext_tiny(num_crops=num_crops, num_classes=num_classes, pretrained=False)
    ckpt_path = PROJECT_ROOT / "models" / "v1" / "model_dualhead_convnext_tiny.pth"
    if not ckpt_path.exists():
        ckpt_path = PROJECT_ROOT / "artifacts" / "checkpoints" / "train_checkpoint_v1.pth"
        raw_state = torch.load(ckpt_path, map_location="cpu", weights_only=False)
        model.load_state_dict(raw_state["model_state"])
    else:
        model.load_state_dict(torch.load(ckpt_path, map_location="cpu", weights_only=False))
    model.to(device)
    model.eval()

    # 4. Extract Validation Logits
    all_crop_logits = []
    all_disease_logits = []
    all_targets = []

    logger.info("Extracting validation logits...")
    with torch.no_grad():
        for images, targets in tqdm(val_loader, desc="Val Inference"):
            images = images.to(device, non_blocking=True)
            autocast_ctx = torch.amp.autocast(device_type="cuda", dtype=torch.float16) if device.type == "cuda" else contextlib.nullcontext()
            with autocast_ctx:
                crop_logits, disease_logits = model(images)
            all_crop_logits.append(crop_logits.float().cpu())
            all_disease_logits.append(disease_logits.float().cpu())
            all_targets.append(targets.cpu())

    val_crop_logits = torch.cat(all_crop_logits)
    val_disease_logits = torch.cat(all_disease_logits)
    val_targets = torch.cat(all_targets)
    val_crop_targets = class_idx_to_crop_idx[val_targets]

    # 5. Compute Uncalibrated Metrics
    p_raw_val = F.softmax(val_disease_logits, dim=-1).numpy()
    raw_val_acc = float(np.mean(np.argmax(p_raw_val, axis=1) == val_targets.numpy()))
    raw_val_ece = compute_ece(p_raw_val, val_targets.numpy())
    logger.info("Uncalibrated Disease Head: Acc=%.4f, ECE=%.4f (%.2f%%)", raw_val_acc, raw_val_ece, raw_val_ece * 100)

    p_crop_val = F.softmax(val_crop_logits, dim=-1).numpy()
    raw_crop_acc = float(np.mean(np.argmax(p_crop_val, axis=1) == val_crop_targets.numpy()))
    raw_crop_ece = compute_ece(p_crop_val, val_crop_targets.numpy())
    logger.info("Uncalibrated Crop Head: Acc=%.4f, ECE=%.4f (%.2f%%)", raw_crop_acc, raw_crop_ece, raw_crop_ece * 100)

    # 6. Fit Temperature Scaling
    logger.info("Fitting TemperatureScaler for Disease Head...")
    scaler_disease = TemperatureScaler()
    t_disease = scaler_disease.fit(val_disease_logits, val_targets)

    logger.info("Fitting TemperatureScaler for Crop Head...")
    scaler_crop = TemperatureScaler()
    t_crop = scaler_crop.fit(val_crop_logits, val_crop_targets)

    # 7. Compute Calibrated Metrics
    p_cal_disease = F.softmax(val_disease_logits / t_disease, dim=-1).numpy()
    cal_disease_ece = compute_ece(p_cal_disease, val_targets.numpy())

    p_cal_crop = F.softmax(val_crop_logits / t_crop, dim=-1).numpy()
    cal_crop_ece = compute_ece(p_cal_crop, val_crop_targets.numpy())

    logger.info("CALIBRATION RESULTS:")
    logger.info("  T_disease : %.4f (Val ECE: %.2f%% -> %.2f%%)", t_disease, raw_val_ece * 100, cal_disease_ece * 100)
    logger.info("  T_crop    : %.4f (Val ECE: %.2f%% -> %.2f%%)", t_crop, raw_crop_ece * 100, cal_crop_ece * 100)

    # 8. Save models/v1/calibration.json
    out_dir = PROJECT_ROOT / "models" / "v1"
    out_dir.mkdir(parents=True, exist_ok=True)
    calib_json = {
        "version": "v1.0.0",
        "T_disease": round(t_disease, 4),
        "T_crop": round(t_crop, 4),
        "optimization_method": "L-BFGS minimization of Negative Log-Likelihood (NLL)",
        "fitted_split": "val",
        "num_validation_samples": num_val_images,
        "val_disease_ece_uncalibrated": round(raw_val_ece, 4),
        "val_disease_ece_calibrated": round(cal_disease_ece, 4),
        "val_crop_ece_uncalibrated": round(raw_crop_ece, 4),
        "val_crop_ece_calibrated": round(cal_crop_ece, 4),
        "uncalibrated_temperature": 1.0,
        "date_fitted": datetime.now(timezone.utc).strftime("%Y-%m-%d")
    }

    calib_path = out_dir / "calibration.json"
    with open(calib_path, "w", encoding="utf-8") as f:
        json.dump(calib_json, f, indent=2)
    logger.info("Saved calibration JSON to %s", calib_path)


if __name__ == "__main__":
    main()
