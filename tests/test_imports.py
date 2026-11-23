"""
tests/test_imports.py — Regression test verifying all production modules and directory contracts.
"""

from pathlib import Path
import pytest


def test_import_config_and_verify_paths():
    """Verify that config.py defines all required paths and they exist on disk."""
    import config

    assert config.PROJECT_ROOT.exists(), f"PROJECT_ROOT missing: {config.PROJECT_ROOT}"
    assert config.MODELS_DIR.exists(), f"MODELS_DIR missing: {config.MODELS_DIR}"
    assert config.REPORTS_DIR.exists(), f"REPORTS_DIR missing: {config.REPORTS_DIR}"
    assert config.DOCS_DIR.exists(), f"DOCS_DIR missing: {config.DOCS_DIR}"

    assert (config.MODELS_DIR / "v1" / "crop_hierarchy.json").exists(), "crop_hierarchy.json missing in models/v1/"

    if not config.RAW_DATA_DIR.exists():
        pytest.skip("local raw/processed datasets absent on clean checkout.")

    assert config.DATA_DIR.exists(), f"DATA_DIR missing: {config.DATA_DIR}"
    assert config.RAW_DATA_DIR.exists(), f"RAW_DATA_DIR missing: {config.RAW_DATA_DIR}"
    assert config.PROCESSED_DATA_DIR.exists(), f"PROCESSED_DATA_DIR missing: {config.PROCESSED_DATA_DIR}"
    assert config.TRAIN_DIR.exists(), f"TRAIN_DIR missing: {config.TRAIN_DIR}"
    assert config.VAL_DIR.exists(), f"VAL_DIR missing: {config.VAL_DIR}"
    assert config.TEST_DIR.exists(), f"TEST_DIR missing: {config.TEST_DIR}"

    if not (config.MODELS_DIR / "v1" / "model_dualhead_convnext_tiny.pth").exists():
        pytest.skip("Large binary artifacts (weights/cached features) absent on clean checkout.")

    assert config.ARTIFACTS_DIR.exists(), f"ARTIFACTS_DIR missing: {config.ARTIFACTS_DIR}"
    assert config.CACHED_FEATURES_DIR.exists(), f"CACHED_FEATURES_DIR missing: {config.CACHED_FEATURES_DIR}"
    assert config.CHECKPOINTS_DIR.exists(), f"CHECKPOINTS_DIR missing: {config.CHECKPOINTS_DIR}"
    assert (config.CACHED_FEATURES_DIR / "eval_logits.pt").exists(), "eval_logits.pt missing in CACHED_FEATURES_DIR"
    assert (config.MODELS_DIR / "v1" / "model_dualhead_convnext_tiny.pth").exists(), "model_dualhead_convnext_tiny.pth missing in models/v1/"


def test_import_data_modules():
    """Verify all data modules import successfully."""
    import src.data
    import src.data.dataset
    import src.data.preprocess

    assert hasattr(src.data.dataset, "PlantDataset")
    assert hasattr(src.data.dataset, "get_dataloaders")
    assert hasattr(src.data.preprocess, "get_train_transforms")
    assert hasattr(src.data, "PlantDiseaseDataset")


def test_import_model_modules():
    """Verify all model architecture and training modules import successfully."""
    import src.models
    import src.models.convnext
    import src.models.bundle_loader
    import src.models.train_dualhead

    assert hasattr(src.models.convnext, "DualHeadConvNeXt")
    assert hasattr(src.models.convnext, "build_dualhead_convnext_tiny")
    assert hasattr(src.models.bundle_loader, "load_model_bundle")
    assert hasattr(src.models.train_dualhead, "train_epoch")
    assert hasattr(src.models.train_dualhead, "validate_epoch")




def test_import_evaluation_modules():
    """Verify evaluation suite imports successfully."""
    import src.evaluation
    import src.evaluation.evaluate_dualhead

    assert hasattr(src.evaluation.evaluate_dualhead, "evaluate_split")


def test_import_serving_modules():
    """Verify production API modules and routes import successfully."""
    import serving.main
    import serving.inference
    import serving.schemas
    import serving.routes.predict

    assert hasattr(serving.main, "app")
    assert hasattr(serving.inference, "predict")
    assert hasattr(serving.schemas, "PredictionResponse")
    assert hasattr(serving.routes.predict, "router")

