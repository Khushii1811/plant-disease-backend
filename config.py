"""
Project-wide configuration: paths, image parameters, and constants.

Centralizing these values here (instead of hardcoding them across scripts)
means changing a path or image size only requires editing one file.
"""

from pathlib import Path

# --- Directory paths -------------------------------------------------------

PROJECT_ROOT: Path = Path(__file__).resolve().parent

DATA_DIR: Path = PROJECT_ROOT / "data"
RAW_DATA_DIR: Path = DATA_DIR / "raw"
PROCESSED_DATA_DIR: Path = DATA_DIR / "processed"

TRAIN_DIR: Path = PROCESSED_DATA_DIR / "train"
VAL_DIR: Path = PROCESSED_DATA_DIR / "val"
TEST_DIR: Path = PROCESSED_DATA_DIR / "test"

MODELS_DIR: Path = PROJECT_ROOT / "models"
ARTIFACTS_DIR: Path = PROJECT_ROOT / "artifacts"
CACHED_FEATURES_DIR: Path = ARTIFACTS_DIR / "cached_features"
CHECKPOINTS_DIR: Path = ARTIFACTS_DIR / "checkpoints"
REPORTS_DIR: Path = PROJECT_ROOT / "reports"
DOCS_DIR: Path = PROJECT_ROOT / "docs"

# --- Image / dataloader parameters -----------------------------------------

IMAGE_SIZE: tuple[int, int] = (256, 256)  # ConvNeXt-Tiny DualHead training resolution
BATCH_SIZE: int = 32
NUM_WORKERS: int = 4  # parallel data-loading workers; lower if on CPU-only machine

# ImageNet normalization stats (required for ImageNet-pretrained backbones)
NORMALIZE_MEAN: tuple[float, float, float] = (0.485, 0.456, 0.406)
NORMALIZE_STD: tuple[float, float, float] = (0.229, 0.224, 0.225)

# --- Reproducibility ---------------------------------------------------------

RANDOM_SEED: int = 42