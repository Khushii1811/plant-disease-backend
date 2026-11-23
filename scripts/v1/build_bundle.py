"""
scripts/v1/build_bundle.py

Constructs the complete production model bundle for models/v1/:
- class_names.json (177 classes)
- class_to_idx.json
- idx_to_class.json
- crop_hierarchy.json (33 crops, 177 classes)
- preprocess.json
- provenance.json
"""

import csv
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
import config


def get_file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def get_git_commit() -> str:
    try:
        res = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=str(PROJECT_ROOT),
            capture_output=True,
            text=True,
            check=True,
        )
        return res.stdout.strip()
    except Exception:
        return "unknown"


def main():
    models_v1_dir = PROJECT_ROOT / "models" / "v1"
    models_v1_dir.mkdir(parents=True, exist_ok=True)

    # 1. Classes and Hierarchy from processed/train directory names
    train_dir = config.DATA_DIR / "processed" / "train"
    class_names = sorted([d.name for d in train_dir.iterdir() if d.is_dir()])
    num_classes = len(class_names)
    assert num_classes == 177, f"Expected 177 classes in v1, got {num_classes}"

    class_to_idx = {name: idx for idx, name in enumerate(class_names)}
    idx_to_class = {str(idx): name for idx, name in enumerate(class_names)}

    # Crops
    crops = sorted(list({c.split(" - ")[0] if " - " in c else c for c in class_names}))
    num_crops = len(crops)
    assert num_crops == 33, f"Expected 33 crops in v1, got {num_crops}"
    crop_to_idx = {c: i for i, c in enumerate(crops)}

    crop_to_class_indices = {c: [] for c in crops}
    class_idx_to_crop_idx = []
    for idx, cname in enumerate(class_names):
        c = cname.split(" - ")[0] if " - " in cname else cname
        crop_to_class_indices[c].append(idx)
        class_idx_to_crop_idx.append(crop_to_idx[c])

    crop_hierarchy = {
        "num_crops": num_crops,
        "num_classes": num_classes,
        "crops": crops,
        "crop_to_idx": crop_to_idx,
        "idx_to_crop": {str(i): c for i, c in enumerate(crops)},
        "crop_to_class_indices": crop_to_class_indices,
        "class_idx_to_crop_idx": class_idx_to_crop_idx,
    }

    # Save Class & Hierarchy JSON files
    with open(models_v1_dir / "class_names.json", "w", encoding="utf-8") as f:
        json.dump(class_names, f, indent=2)

    with open(models_v1_dir / "class_to_idx.json", "w", encoding="utf-8") as f:
        json.dump(class_to_idx, f, indent=2)

    with open(models_v1_dir / "idx_to_class.json", "w", encoding="utf-8") as f:
        json.dump(idx_to_class, f, indent=2)

    with open(models_v1_dir / "crop_hierarchy.json", "w", encoding="utf-8") as f:
        json.dump(crop_hierarchy, f, indent=2)

    # Preprocess JSON
    preprocess = {
        "version": "v1.0.0",
        "image_size": [256, 256],
        "mean": [0.485, 0.456, 0.406],
        "std": [0.229, 0.224, 0.225],
        "interpolation": "bilinear",
        "resize_rule": "Direct resize to (256, 256) without aspect-ratio crop for inference and evaluation",
        "normalization": "Standard ImageNet z-score normalization on [0, 1] RGB tensors",
        "tta_views": [
            "original",
            "horizontal_flip",
            "center_crop_scale_1.08"
        ]
    }
    with open(models_v1_dir / "preprocess.json", "w", encoding="utf-8") as f:
        json.dump(preprocess, f, indent=2)

    # Dynamic Split Counts from dataset_v1.csv
    dataset_v1_csv_path = PROJECT_ROOT / "reports" / "v1" / "dataset_v1.csv"
    dataset_v1_sha = get_file_sha256(dataset_v1_csv_path) if dataset_v1_csv_path.exists() else "unknown"
    split_counts = {"train": 0, "val": 0, "test": 0}
    if dataset_v1_csv_path.exists():
        with open(dataset_v1_csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                s = row.get("split", "")
                if s in split_counts:
                    split_counts[s] += 1
    total_curated_images = sum(split_counts.values())
    assert split_counts == {"train": 73356, "val": 9349, "test": 9279}, (
        f"Unexpected split counts: {split_counts}"
    )

    git_commit = get_git_commit()
    mlflow_run_id = "cb46c7f8f10f45e59ad809720c7bccb6"

    # Query MLflow for validation selection metrics and training commit
    import sqlite3
    mlflow_db_path = PROJECT_ROOT / "mlflow.db"
    if mlflow_db_path.exists():
        conn = sqlite3.connect(mlflow_db_path)
        cur = conn.cursor()
        cur.execute(
            """
            SELECT step, value FROM metrics 
            WHERE run_uuid = ? AND key = 'val_masked_disease_acc'
            ORDER BY value DESC LIMIT 1
            """,
            (mlflow_run_id,)
        )
        row = cur.fetchone()
        best_step = int(row[0]) if row else 19
        best_val_masked_acc = float(row[1]) if row else 0.9599957214675366

        cur.execute(
            "SELECT key, value FROM metrics WHERE run_uuid = ? AND step = ?",
            (mlflow_run_id, best_step)
        )
        step_metrics = {k: v for k, v in cur.fetchall()}

        cur.execute(
            "SELECT value FROM tags WHERE run_uuid = ? AND key = 'mlflow.source.git.commit'",
            (mlflow_run_id,)
        )
        tag_row = cur.fetchone()
        training_git_commit = tag_row[0] if tag_row else "21086895979c683ed3c2044da7b9ca919f1dbaa0"
        conn.close()
    else:
        best_step = 19
        best_val_masked_acc = 0.9599957214675366
        step_metrics = {
            "val_loss": 3.1527064936545357,
            "val_crop_acc": 0.995828430848219,
            "val_raw_disease_acc": 0.9588191250401112,
            "val_masked_disease_acc": 0.9599957214675366,
            "val_macro_f1": 0.9495217036878213,
        }
        training_git_commit = "21086895979c683ed3c2044da7b9ca919f1dbaa0"

    print(
        f"MLflow Run {mlflow_run_id}: Step {best_step} highest val_masked_disease_acc = "
        f"{best_val_masked_acc:.4f} ({round(best_val_masked_acc * 9349)} of 9,349)"
    )

    # Calibration parameters if available
    calib_path = models_v1_dir / "calibration.json"
    if calib_path.exists():
        with open(calib_path, "r", encoding="utf-8") as f:
            calib = json.load(f)
            t_disease = calib.get("T_disease", 0.5013)
            t_crop = calib.get("T_crop", 0.5931)
    else:
        t_disease = 0.5013
        t_crop = 0.5931

    provenance = {
        "model_name": "DualHead ConvNeXt-Tiny",
        "version": "v1.0.0",
        "status": "production_release",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "random_seed": None,
        "random_seed_note": "training run was not seeded; seeding added later in 16635f4",
        "initialization": {
            "source": "ImageNet-22k pretrained / 1k fine-tuned (convnext_tiny.fb_in22k_ft_in1k via timm)",
            "no_v0_weights_used": True,
            "no_v0_resume_used": True,
            "code_paths_verified": [
                "src/models/train_dualhead.py: build_dualhead_convnext_tiny(pretrained=True)",
                "src/models/convnext.py: timm.create_model('convnext_tiny.fb_in22k_ft_in1k', pretrained=True)",
                "CLI arguments: --version v1 --epochs 25 --warmup-epochs 5 (no --resume flag passed)"
            ]
        },
        "source_code": {
            "repository": "https://github.com/TODO/plant-disease-backend",
            "training_git_commit": training_git_commit,
            "training_tree_dirty": True,
            "training_tree_dirty_note": "Working tree had uncommitted modifications during training run cb46c7f8f10f45e59ad809720c7bccb6",
            "bundle_build_git_commit": git_commit,
            "training_script": "src/models/train_dualhead.py"
        },
        "dataset_provenance": {
            "manifest_sha256": dataset_v1_sha,
            "manifest_path": "reports/v1/dataset_v1.csv",
            "total_curated_images": total_curated_images,
            "num_classes": num_classes,
            "num_crops": num_crops,
            "patches_applied": [
                "P-001: Quarantined 253 Bell Pepper synthetic duplicate impostors",
                "P-002: Rebalanced Citrus Greening and Soybean Healthy splits to 80/10/10",
                "P-003: Quarantined 1,415 0-bit cross-split perceptual hash leakage twin frames",
                "P-004: Quarantined 1,245 label conflicts (941) and cross-split duplicates (304)",
                "P-005: Quarantined 4,665 non-foliar/severe mixed images; relabeled 3,062; merged 498",
                "P-006: Repartitioned 21 hoarded classes to 80/10/10 with min(val)>=3, min(test)>=3"
            ],
            "split_counts": split_counts
        },
        "training_run": {
            "mlflow_run_id": mlflow_run_id,
            "mlflow_experiment": "dualhead_convnext_tiny",
            "chosen_epoch": best_step + 1,
            "total_epochs_configured": 25,
            "wall_clock_time_hours": 2.13,
            "training_environment": {
                "python_version": "3.13.1",
                "pytorch_version": "2.6.0+cu124",
                "cuda_version": "12.4",
                "os": "Windows 11",
                "hardware": "NVIDIA GeForce RTX 3050 Laptop GPU (4096 MiB, Driver 566.07)"
            },
            "hyperparameters": {
                "epochs": 25,
                "warmup_epochs": 5,
                "batch_size": 16,
                "head_lr": 0.0002,
                "stage3_lr": 3e-05,
                "stage2_lr": 1e-05,
                "unfreeze_stages": 2,
                "crop_loss_weight": 0.3,
                "disease_loss_weight": 1.0,
                "label_smoothing": 0.05,
                "optimizer": "AdamW",
                "weight_decay": 0.01
            }
        },
        "validation_selection_metrics": {
            "step": best_step,
            "epoch": best_step + 1,
            "val_loss": round(float(step_metrics.get("val_loss", 3.15271)), 5),
            "val_crop_acc": round(float(step_metrics.get("val_crop_acc", 0.99583)), 5),
            "val_raw_disease_acc": round(float(step_metrics.get("val_raw_disease_acc", 0.95882)), 5),
            "val_masked_disease_acc": round(float(step_metrics.get("val_masked_disease_acc", 0.96000)), 5),
            "val_masked_disease_acc_note": "8,974 of 9,349",
            "val_macro_f1": round(float(step_metrics.get("val_macro_f1", 0.94952)), 5)
        },
        "calibration": {
            "T_disease": t_disease,
            "T_crop": t_crop,
            "method": "Vectorized Platt Temperature Scaling (L-BFGS NLL minimization on 9,349 Val samples)"
        }
    }

    with open(models_v1_dir / "provenance.json", "w", encoding="utf-8") as f:
        json.dump(provenance, f, indent=2)

    print(f"[DONE] Successfully generated all bundle metadata in {models_v1_dir}")


if __name__ == "__main__":
    main()
