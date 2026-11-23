"""
src/models/train_dualhead.py — Dedicated training script for DualHeadConvNeXt-Tiny.

Trains the hierarchical Dual-Head ConvNeXt-Tiny (34 Crops -> 195 Plant Pathology Classes)
on the curated 99,751-image foliar benchmark using a 2-Phase Staged Transfer Learning protocol:
  - Phase 1 (Warmup): Freeze backbone; train only the Crop & Disease MLP heads.
  - Phase 2 (Discriminative Fine-Tuning): Unfreeze Stages 2 & 3 with layer-wise LR decay;
    keep Stem & Stage 0-1 permanently frozen.
  - Multi-Task Loss: L_total = (0.3 * L_crop) + (1.0 * L_disease) with label smoothing.
  - Evaluation: Tracks Crop Acc, Raw Disease Acc, and Masked Disease Acc (Dynamic Logit Masking).

Usage:
    # Standard 25-epoch 2-phase training
    python -m src.models.train_dualhead

    # Custom epochs or hyperparameters
    python -m src.models.train_dualhead --epochs 25 --warmup-epochs 5 --batch-size 16
"""

import argparse
from datetime import datetime, timedelta
import json
import logging
import os
import random
import time
from pathlib import Path
from typing import Dict, Any, Tuple, Optional, cast

# Enable PyTorch expandable segments to prevent CUDA memory fragmentation on 4GB-8GB GPUs
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"
os.environ["MLFLOW_DISABLE_AGENT_HINT"] = "1"

import config
import mlflow
import numpy as np
from sklearn.metrics import f1_score
from sklearn.utils.class_weight import compute_class_weight
import torch
from torch import nn
from torch.utils.data import DataLoader
from tqdm import tqdm

from ..data.dataset import get_dataloaders
from .convnext import build_dualhead_convnext_tiny, DualHeadLoss, DualHeadConvNeXt

logger = logging.getLogger("train_dualhead")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train DualHeadConvNeXt-Tiny Plant Pathology Model")
    parser.add_argument("--epochs", type=int, default=25, help="Total training epochs (default: 25)")
    parser.add_argument("--warmup-epochs", type=int, default=5, help="Phase 1 backbone frozen epochs (default: 5)")
    parser.add_argument("--batch-size", type=int, default=16, help="Batch size per step (default: 16)")
    parser.add_argument("--head-lr", type=float, default=2e-4, help="Classifier heads learning rate (default: 2e-4)")
    parser.add_argument("--stage3-lr", type=float, default=3e-5, help="ConvNeXt Stage 3 learning rate (default: 3e-5)")
    parser.add_argument("--stage2-lr", type=float, default=1e-5, help="ConvNeXt Stage 2 learning rate (default: 1e-5)")
    parser.add_argument("--unfreeze-stages", type=int, default=2, help="Number of stages to unfreeze in Phase 2 (default: 2)")
    parser.add_argument("--crop-weight", type=float, default=0.3, help="Loss weight for Crop head (default: 0.3)")
    parser.add_argument("--disease-weight", type=float, default=1.0, help="Loss weight for Disease head (default: 1.0)")
    parser.add_argument("--version", type=str, default="v1", help="Model version under models/ (default: v1)")
    parser.add_argument("--hierarchy-path", type=str, default=None, help="Path to crop_hierarchy.json (default: models/<version>/crop_hierarchy.json)")
    parser.add_argument("--checkpoint-path", type=str, default=None, help="Checkpoint save path (default: models/<version>/model_dualhead_convnext_tiny.pth)")
    parser.add_argument("--run-name", type=str, default=None, help="MLflow run name")
    parser.add_argument("--resume", type=str, default=None, help="Path to checkpoint to resume weights from")
    parser.add_argument("--fresh", action="store_true", help="Start fresh without resuming interrupted checkpoints")
    parser.add_argument("--dry-run", action="store_true", help="Run a quick dry-run with a few batches to verify the pipeline")
    parser.add_argument("--max-batches", type=int, default=None, help="Max batches per epoch for quick testing")
    args = parser.parse_args()
    if args.dry_run:
        args.epochs = 1
        args.warmup_epochs = 1
        if args.max_batches is None:
            args.max_batches = 5
    return args


def train_epoch(
    model: DualHeadConvNeXt,
    dataloader: DataLoader,
    loss_fn: DualHeadLoss,
    optimizer: torch.optim.Optimizer,
    scaler: Optional[torch.amp.GradScaler],
    class_to_crop_tensor: torch.Tensor,
    device: str,
    desc: str = "Training",
    max_batches: Optional[int] = None,
) -> Tuple[float, float, float, float]:
    """Runs one full training epoch over the dataloader."""
    model.train()
    total_loss, total_loss_crop, total_loss_disease = 0.0, 0.0, 0.0
    crop_correct, disease_correct = 0, 0
    total_samples = 0

    pbar = tqdm(dataloader, desc=desc, dynamic_ncols=True, mininterval=1.0)
    for batch_idx, (images, disease_targets) in enumerate(pbar):
        if max_batches is not None and batch_idx >= max_batches:
            break
        images = images.to(device, non_blocking=True)
        disease_targets = disease_targets.to(device, non_blocking=True)
        crop_targets = class_to_crop_tensor[disease_targets]

        optimizer.zero_grad()

        if scaler is not None:
            with torch.amp.autocast(device_type="cuda", dtype=torch.float16):
                crop_logits, disease_logits = model(images)
                loss, loss_c, loss_d = loss_fn(crop_logits, disease_logits, crop_targets, disease_targets)
            scaler.scale(loss).backward()
            scaler.step(optimizer)
            scaler.update()
        else:
            crop_logits, disease_logits = model(images)
            loss, loss_c, loss_d = loss_fn(crop_logits, disease_logits, crop_targets, disease_targets)
            loss.backward()
            optimizer.step()

        batch_sz = disease_targets.size(0)
        total_samples += batch_sz
        total_loss += loss.item() * batch_sz
        total_loss_crop += loss_c.item() * batch_sz
        total_loss_disease += loss_d.item() * batch_sz

        with torch.no_grad():
            crop_preds = crop_logits.argmax(dim=-1)
            disease_preds = disease_logits.argmax(dim=-1)
            crop_correct += (crop_preds == crop_targets).sum().item()
            disease_correct += (disease_preds == disease_targets).sum().item()

        pbar.set_postfix({
            "loss": f"{total_loss / total_samples:.4f}",
            "c_acc": f"{crop_correct / total_samples:.3f}",
            "d_acc": f"{disease_correct / total_samples:.3f}",
        })

    return (
        total_loss / total_samples,
        total_loss_crop / total_samples,
        total_loss_disease / total_samples,
        disease_correct / total_samples,
    )


def validate_epoch(
    model: DualHeadConvNeXt,
    dataloader: DataLoader,
    loss_fn: DualHeadLoss,
    class_to_crop_tensor: torch.Tensor,
    crop_hierarchy: Dict[str, Any],
    device: str,
    desc: str = "Validation",
    max_batches: Optional[int] = None,
) -> Dict[str, float]:
    """Runs evaluation on the validation split with and without dynamic logit masking."""
    model.eval()
    total_loss, total_loss_crop, total_loss_disease = 0.0, 0.0, 0.0
    crop_correct = 0
    raw_disease_correct = 0
    masked_disease_correct = 0
    total_samples = 0

    all_targets = []
    all_masked_preds = []

    crops_list = crop_hierarchy["crops"]
    all_indices = set(range(model.num_classes))

    with torch.no_grad():
        pbar = tqdm(dataloader, desc=desc, dynamic_ncols=True, mininterval=1.0)
        for batch_idx, (images, disease_targets) in enumerate(pbar):
            if max_batches is not None and batch_idx >= max_batches:
                break
            images = images.to(device, non_blocking=True)
            disease_targets = disease_targets.to(device, non_blocking=True)
            crop_targets = class_to_crop_tensor[disease_targets]

            crop_logits, disease_logits = model(images)
            loss, loss_c, loss_d = loss_fn(crop_logits, disease_logits, crop_targets, disease_targets)

            batch_sz = disease_targets.size(0)
            total_samples += batch_sz
            total_loss += loss.item() * batch_sz
            total_loss_crop += loss_c.item() * batch_sz
            total_loss_disease += loss_d.item() * batch_sz

            crop_preds = crop_logits.argmax(dim=-1)
            raw_disease_preds = disease_logits.argmax(dim=-1)

            crop_correct += (crop_preds == crop_targets).sum().item()
            raw_disease_correct += (raw_disease_preds == disease_targets).sum().item()

            # Dynamic Logit Masking: Mask out all diseases not belonging to predicted crop
            masked_logits = disease_logits.clone()
            for i in range(batch_sz):
                c_name = crops_list[crop_preds[i].item()]
                allowed = set(crop_hierarchy["crop_to_class_indices"].get(c_name, []))
                disallowed = list(all_indices - allowed)
                if disallowed:
                    masked_logits[i, disallowed] = -1e9

            masked_disease_preds = masked_logits.argmax(dim=-1)
            masked_disease_correct += (masked_disease_preds == disease_targets).sum().item()

            all_targets.extend(disease_targets.cpu().numpy())
            all_masked_preds.extend(masked_disease_preds.cpu().numpy())

    macro_f1 = float(f1_score(all_targets, all_masked_preds, average="macro", zero_division=0))

    return {
        "val_loss": total_loss / total_samples,
        "val_loss_crop": total_loss_crop / total_samples,
        "val_loss_disease": total_loss_disease / total_samples,
        "crop_accuracy": crop_correct / total_samples,
        "raw_disease_accuracy": raw_disease_correct / total_samples,
        "masked_disease_accuracy": masked_disease_correct / total_samples,
        "macro_f1": macro_f1,
    }


def main() -> None:
    args = parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

    # Deterministic PRNG seeding
    seed = config.RANDOM_SEED
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False

    g = torch.Generator()
    g.manual_seed(seed)

    def seed_worker(worker_id: int):
        worker_seed = torch.initial_seed() % 2**32
        np.random.seed(worker_seed)
        random.seed(worker_seed)

    device = "cuda" if torch.cuda.is_available() else "cpu"
    logger.info("Initializing DualHeadConvNeXt Training on device: %s (Seed: %d)", device, seed)

    # 1. Load Data
    train_loader, val_loader, _, classes = get_dataloaders(
        batch_size=args.batch_size,
        generator=g,
        worker_init_fn=seed_worker,
    )
    num_classes = len(classes)
    n_train = len(cast(Any, train_loader.dataset))
    n_val = len(cast(Any, val_loader.dataset))
    logger.info("Loaded %d classes (%d train images, %d val images)",
                num_classes, n_train, n_val)

    # 2. Load Hierarchy
    hierarchy_path = Path(args.hierarchy_path) if args.hierarchy_path else Path(f"models/{args.version}/crop_hierarchy.json")
    if not hierarchy_path.exists():
        raise FileNotFoundError(f"Missing crop hierarchy at {hierarchy_path}")
    crop_hierarchy = json.loads(hierarchy_path.read_text(encoding="utf-8"))
    num_crops = crop_hierarchy["num_crops"]
    if num_classes != crop_hierarchy["num_classes"]:
        raise ValueError(
            f"Dataloader classes ({num_classes}) != crop_hierarchy classes ({crop_hierarchy['num_classes']}). "
            f"Run scripts/data/curation/generate_mappings.py to update metadata."
        )
    class_to_crop_tensor = torch.tensor(crop_hierarchy["class_idx_to_crop_idx"], dtype=torch.long, device=device)

    # 3. Compute Class Weights for Imbalance
    ds = cast(Any, train_loader.dataset)
    train_labels = [label for _, label in ds.samples] if hasattr(ds, "samples") else getattr(ds, "labels", [])
    unique_classes = np.unique(train_labels)
    computed_weights = compute_class_weight("balanced", classes=unique_classes, y=train_labels)
    full_weights = np.ones(num_classes, dtype=np.float32)
    for cls_idx, w in zip(unique_classes, computed_weights):
        full_weights[cls_idx] = w
    disease_class_weights = torch.tensor(full_weights, dtype=torch.float, device=device)

    # 4. Build Model
    model = build_dualhead_convnext_tiny(
        num_crops=num_crops,
        num_classes=num_classes,
        pretrained=True,
        freeze_backbone=True,  # Start with Phase 1 frozen backbone
    ).to(device)

    loss_fn = DualHeadLoss(
        crop_weight=args.crop_weight,
        disease_weight=args.disease_weight,
        disease_class_weights=disease_class_weights,
        label_smoothing=0.05,
    )

    scaler = torch.amp.GradScaler("cuda") if device == "cuda" else None

    # Checkpoint paths
    default_ckpt = Path(f"models/{args.version}/model_dualhead_convnext_tiny.pth")
    checkpoint_path = Path(args.checkpoint_path) if args.checkpoint_path else default_ckpt
    checkpoint_path.parent.mkdir(parents=True, exist_ok=True)
    resumable_ckpt_path = Path("artifacts/checkpoints") / f"train_checkpoint_{args.version}.pth"
    resumable_ckpt_path.parent.mkdir(parents=True, exist_ok=True)
    if args.run_name is None:
        args.run_name = f"train_dualhead_convnext_{args.version}"

    start_epoch = 1
    best_masked_acc = 0.0
    best_macro_f1 = 0.0
    resumed_run_id = None
    optimizer = None
    scheduler = None

    # Determine resume source (auto-detect resumable checkpoint unless --fresh is passed)
    resume_source = None
    if not args.fresh:
        if args.resume and Path(args.resume).exists():
            resume_source = Path(args.resume)
        elif resumable_ckpt_path.exists():
            resume_source = resumable_ckpt_path

    if resume_source and resume_source.exists():
        logger.info("Found checkpoint at: %s. Inspecting for resume...", resume_source)
        ckpt_data = torch.load(resume_source, map_location=device, weights_only=False)
        if isinstance(ckpt_data, dict) and "model_state" in ckpt_data:
            model.load_state_dict(ckpt_data["model_state"], strict=True)
            start_epoch = ckpt_data["epoch"] + 1
            best_masked_acc = ckpt_data.get("best_masked_acc", 0.0)
            best_macro_f1 = ckpt_data.get("best_macro_f1", 0.0)
            resumed_run_id = ckpt_data.get("mlflow_run_id")

            # Restore correct phase model unfreezing and optimizer structure
            if start_epoch <= args.warmup_epochs:
                model.freeze_all_backbone()
                optimizer = torch.optim.AdamW(
                    model.get_parameter_groups(head_lr=args.head_lr, stage3_lr=0.0, stage2_lr=0.0),
                    weight_decay=1e-4,
                )
                scheduler = None
            else:
                model.unfreeze_stages(stages=args.unfreeze_stages)
                optimizer = torch.optim.AdamW(
                    model.get_parameter_groups(
                        head_lr=args.head_lr * 0.5,
                        stage3_lr=args.stage3_lr,
                        stage2_lr=args.stage2_lr,
                    ),
                    weight_decay=1e-4,
                )
                remaining_epochs = max(1, args.epochs - args.warmup_epochs)
                scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
                    optimizer, T_max=remaining_epochs, eta_min=1e-6
                )

            if ckpt_data.get("optimizer_state") and optimizer:
                try:
                    optimizer.load_state_dict(ckpt_data["optimizer_state"])
                except Exception as e:
                    logger.warning("Could not restore optimizer state: %s", e)
            if ckpt_data.get("scheduler_state") and scheduler:
                try:
                    scheduler.load_state_dict(ckpt_data["scheduler_state"])
                except Exception as e:
                    logger.warning("Could not restore scheduler state: %s", e)
            if ckpt_data.get("scaler_state") and scaler:
                try:
                    scaler.load_state_dict(ckpt_data["scaler_state"])
                except Exception as e:
                    logger.warning("Could not restore scaler state: %s", e)

            logger.info("Successfully resumed! Continuing from Epoch %d/%d (Best Masked Acc so far: %.4f)",
                        start_epoch, args.epochs, best_masked_acc)
        else:
            model.load_state_dict(ckpt_data, strict=True)
            logger.info("Loaded raw model weights from %s. Starting from epoch 1.", resume_source)

    if start_epoch > args.epochs:
        logger.info("Training already complete (%d/%d epochs). Nothing to do. Run with --epochs %d or --fresh to start over.",
                    args.epochs, args.epochs, args.epochs + 10)
        return

    # 5. MLflow Tracking Setup
    mlflow.set_experiment("dualhead_convnext_tiny")
    with mlflow.start_run(run_name=args.run_name, run_id=resumed_run_id):
        active_run = mlflow.active_run()
        active_run_id = active_run.info.run_id if active_run else None

        if resumed_run_id is None:
            mlflow.log_params({
                "architecture": "DualHeadConvNeXt-Tiny",
                "num_crops": num_crops,
                "num_classes": num_classes,
                "total_epochs": args.epochs,
                "warmup_epochs": args.warmup_epochs,
                "batch_size": args.batch_size,
                "head_lr": args.head_lr,
                "stage3_lr": args.stage3_lr,
                "stage2_lr": args.stage2_lr,
                "unfreeze_stages": args.unfreeze_stages,
                "crop_weight": args.crop_weight,
                "disease_weight": args.disease_weight,
                "optimizer": "AdamW",
            })

        logger.info("================================================================================")
        logger.info("Starting Staged Training: Epochs %d..%d of %d (Phase 1 Warmup: %d ep, Phase 2 Fine-tune: %d ep)",
                    start_epoch, args.epochs, args.epochs, args.warmup_epochs, args.epochs - args.warmup_epochs)
        logger.info("================================================================================")

        overall_start_time = time.time()
        try:
            for epoch in range(start_epoch, args.epochs + 1):
                epoch_start = time.time()

                # --- PHASE TRANSITION MANAGEMENT ---
                if epoch <= args.warmup_epochs and optimizer is None:
                    logger.info("[PHASE 1 START] Epoch %d..%d: Warmup - Backbone 100%% Frozen; training Dual MLP Heads only.", epoch, args.warmup_epochs)
                    model.freeze_all_backbone()
                    optimizer = torch.optim.AdamW(
                        model.get_parameter_groups(head_lr=args.head_lr, stage3_lr=0.0, stage2_lr=0.0),
                        weight_decay=1e-4,
                    )
                    scheduler = None

                elif epoch == args.warmup_epochs + 1:
                    logger.info("[PHASE 2 START] Epoch %d..%d: Unfreezing Stages 2 & 3 with Layer-wise LR Decay.", epoch, args.epochs)
                    model.unfreeze_stages(stages=args.unfreeze_stages)
                    optimizer = torch.optim.AdamW(
                        model.get_parameter_groups(
                            head_lr=args.head_lr * 0.5,
                            stage3_lr=args.stage3_lr,
                            stage2_lr=args.stage2_lr,
                        ),
                        weight_decay=1e-4,
                    )
                    remaining_epochs = max(1, args.epochs - args.warmup_epochs)
                    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
                        optimizer, T_max=remaining_epochs, eta_min=1e-6
                    )

                # --- TRAIN STEP ---
                assert optimizer is not None, "Optimizer must be initialized before training epoch"
                current_phase = 1 if epoch <= args.warmup_epochs else 2
                train_loss, train_loss_c, train_loss_d, train_d_acc = train_epoch(
                    model=model,
                    dataloader=train_loader,
                    loss_fn=loss_fn,
                    optimizer=optimizer,
                    scaler=scaler,
                    class_to_crop_tensor=class_to_crop_tensor,
                    device=device,
                    desc=f"Epoch {epoch}/{args.epochs} [P{current_phase}] Train",
                    max_batches=args.max_batches,
                )

                # --- VALIDATION STEP ---
                val_metrics = validate_epoch(
                    model=model,
                    dataloader=val_loader,
                    loss_fn=loss_fn,
                    class_to_crop_tensor=class_to_crop_tensor,
                    crop_hierarchy=crop_hierarchy,
                    device=device,
                    desc=f"Epoch {epoch}/{args.epochs} [P{current_phase}] Val",
                    max_batches=args.max_batches,
                )

                if scheduler is not None:
                    scheduler.step()

                epoch_dur = time.time() - epoch_start
                masked_acc = val_metrics["masked_disease_accuracy"]
                macro_f1 = val_metrics["macro_f1"]

                # Time calculations & ETA
                total_elapsed = time.time() - overall_start_time
                epochs_done = epoch - start_epoch + 1
                epochs_remaining = args.epochs - epoch
                avg_epoch_dur = total_elapsed / epochs_done
                est_remaining_sec = avg_epoch_dur * epochs_remaining
                est_finish_dt = datetime.now() + timedelta(seconds=est_remaining_sec)

                elapsed_fmt = f"{int(total_elapsed // 3600):02d}h {int((total_elapsed % 3600) // 60):02d}m {int(total_elapsed % 60):02d}s"
                remaining_fmt = f"{int(est_remaining_sec // 3600):02d}h {int((est_remaining_sec % 3600) // 60):02d}m"
                finish_fmt = est_finish_dt.strftime("%I:%M %p")

                logger.info(
                    "Epoch %2d/%2d [P%d] (%.1fs) | Train Loss: %.4f, Acc: %.3f | Val Loss: %.4f | Crop Acc: %.3f | Raw Disease Acc: %.3f | Masked Disease Acc: %.3f | Macro-F1: %.3f",
                    epoch, args.epochs, current_phase, epoch_dur,
                    train_loss, train_d_acc,
                    val_metrics["val_loss"],
                    val_metrics["crop_accuracy"],
                    val_metrics["raw_disease_accuracy"],
                    masked_acc,
                    macro_f1,
                )
                logger.info(
                    "  [TIME TRACKER] Elapsed: %s | Est Remaining: %s | Est Completion: %s (Avg: %.1fs/ep)",
                    elapsed_fmt, remaining_fmt, finish_fmt, avg_epoch_dur,
                )

                # Log metrics to MLflow
                mlflow.log_metrics({
                    "train_loss": train_loss,
                    "train_disease_acc": train_d_acc,
                    "val_loss": val_metrics["val_loss"],
                    "val_crop_acc": val_metrics["crop_accuracy"],
                    "val_raw_disease_acc": val_metrics["raw_disease_accuracy"],
                    "val_masked_disease_acc": masked_acc,
                    "val_macro_f1": macro_f1,
                }, step=epoch)

                # 1. Save best production model weights
                if masked_acc > best_masked_acc:
                    best_masked_acc = masked_acc
                    best_macro_f1 = macro_f1
                    torch.save(model.state_dict(), str(checkpoint_path))
                    logger.info("  --> Saved new best model to %s (Masked Acc: %.4f, Macro-F1: %.4f)",
                                checkpoint_path, best_masked_acc, best_macro_f1)

                # 2. Save full resumable state (allows pausing & resuming anytime)
                resumable_state = {
                    "epoch": epoch,
                    "model_state": model.state_dict(),
                    "optimizer_state": optimizer.state_dict() if optimizer else None,
                    "scheduler_state": scheduler.state_dict() if scheduler else None,
                    "scaler_state": scaler.state_dict() if scaler else None,
                    "best_masked_acc": best_masked_acc,
                    "best_macro_f1": best_macro_f1,
                    "mlflow_run_id": active_run_id,
                }
                torch.save(resumable_state, str(resumable_ckpt_path))

            logger.info("Training complete. Best Validation Masked Disease Accuracy: %.4f | Macro-F1: %.4f",
                        best_masked_acc, best_macro_f1)
            mlflow.log_metric("best_val_masked_disease_accuracy", best_masked_acc)
            mlflow.log_metric("best_val_macro_f1", best_macro_f1)

        except KeyboardInterrupt:
            logger.info("\n[PAUSED] Training paused by user (Ctrl+C). Progress is safely saved to %s.", resumable_ckpt_path)
            logger.info("To resume from the exact epoch, simply run the command again without --fresh.")


if __name__ == "__main__":
    main()
