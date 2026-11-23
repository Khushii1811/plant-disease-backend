"""
scripts/clean_legacy_models_and_setup_mapping.py

Performs a clean-slate reset for the model & fine-tuning subsystem:
1. Cleans all obsolete model weights, classification reports, and stale features:
   - models/*.pth, models/*.json, models/*.png
   - models_saved/*.pt
   - cached_features/*.pt
   - scripts/fast_finetune_consolidated.py
   - scripts/calibrate.py
2. Preserves the directory architecture (models/, models_saved/, cached_features/, src/, data/, scripts/).
3. Preserves all data creation, ingestion, scraping, audit, and quarantine scripts.
4. Generates fresh, authoritative 200-class mappings directly from data/processed/train:
   - models/class_to_idx.json
   - models/idx_to_class.json
   - models/classes.json
5. Verifies 100% consistency across data/processed/{train, val, test}.
"""

import json
import os
import shutil
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MODELS_DIR = PROJECT_ROOT / "models"
MODELS_SAVED_DIR = PROJECT_ROOT / "models_saved"
CACHED_FEATURES_DIR = PROJECT_ROOT / "cached_features"
SCRIPTS_DIR = PROJECT_ROOT / "scripts"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"


def clean_legacy_artifacts():
    print("=" * 80)
    print("🧹 CLEANING LEGACY MODEL & FINETUNING ARTIFACTS")
    print("=" * 80)

    # 1. Clean models/ directory
    if MODELS_DIR.exists():
        for item in MODELS_DIR.iterdir():
            if item.is_file():
                print(f"  🗑️ Removed legacy model artifact: {item.name}")
                item.unlink()
    MODELS_DIR.mkdir(parents=True, exist_ok=True)

    # 2. Clean models_saved/ directory
    if MODELS_SAVED_DIR.exists():
        for item in MODELS_SAVED_DIR.iterdir():
            if item.is_file():
                print(f"  🗑️ Removed legacy saved head: {item.name}")
                item.unlink()
    MODELS_SAVED_DIR.mkdir(parents=True, exist_ok=True)

    # 3. Clean cached_features/ directory
    if CACHED_FEATURES_DIR.exists():
        for item in CACHED_FEATURES_DIR.iterdir():
            if item.is_file():
                print(f"  🗑️ Removed stale cached feature: {item.name}")
                item.unlink()
    CACHED_FEATURES_DIR.mkdir(parents=True, exist_ok=True)

    # 4. Remove obsolete finetune/calibrate scripts in scripts/
    obsolete_scripts = [
        SCRIPTS_DIR / "fast_finetune_consolidated.py",
        SCRIPTS_DIR / "calibrate.py"
    ]
    for s_path in obsolete_scripts:
        if s_path.exists():
            print(f"  🗑️ Removed obsolete finetuning script: {s_path.name}")
            s_path.unlink()

    print("✅ All obsolete checkpoints, reports, cached features, and scripts removed.")


def generate_authoritative_mappings():
    print("\n" + "=" * 80)
    print("📋 GENERATING AUTHORITATIVE 200-CLASS INDEX MAPPINGS")
    print("=" * 80)

    train_dir = PROCESSED_DIR / "train"
    val_dir = PROCESSED_DIR / "val"
    test_dir = PROCESSED_DIR / "test"

    assert train_dir.exists(), f"Train directory not found: {train_dir}"

    train_classes = sorted([d.name for d in train_dir.iterdir() if d.is_dir()])
    val_classes = sorted([d.name for d in val_dir.iterdir() if d.is_dir()])
    test_classes = sorted([d.name for d in test_dir.iterdir() if d.is_dir()])

    print(f"  Train classes count: {len(train_classes)}")
    print(f"  Val classes count:   {len(val_classes)}")
    print(f"  Test classes count:  {len(test_classes)}")

    assert train_classes == val_classes, "Discrepancy between Train and Val class sets!"
    assert train_classes == test_classes, "Discrepancy between Train and Test class sets!"
    assert len(train_classes) == 200, f"Expected 200 classes, found {len(train_classes)}!"

    class_to_idx = {cls_name: idx for idx, cls_name in enumerate(train_classes)}
    idx_to_class = {str(idx): cls_name for idx, cls_name in enumerate(train_classes)}

    # Save to models/ directory
    c2i_path = MODELS_DIR / "class_to_idx.json"
    i2c_path = MODELS_DIR / "idx_to_class.json"
    classes_path = MODELS_DIR / "classes.json"

    with open(c2i_path, "w", encoding="utf-8") as f:
        json.dump(class_to_idx, f, indent=2)

    with open(i2c_path, "w", encoding="utf-8") as f:
        json.dump(idx_to_class, f, indent=2)

    with open(classes_path, "w", encoding="utf-8") as f:
        json.dump(train_classes, f, indent=2)

    print(f"  ✨ Generated {c2i_path} ({len(class_to_idx)} entries)")
    print(f"  ✨ Generated {i2c_path} ({len(idx_to_class)} entries)")
    print(f"  ✨ Generated {classes_path} ({len(train_classes)} entries)")
    print("✅ 100% verified cross-split class consistency across all 200 classes!")


def main():
    clean_legacy_artifacts()
    generate_authoritative_mappings()
    print("\n" + "=" * 80)
    print("🎉 CLEAN SLATE & 200-CLASS MAPPING COMPLETE!")
    print("=" * 80)


if __name__ == "__main__":
    main()
