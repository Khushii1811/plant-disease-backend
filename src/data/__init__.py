"""src.data — Botanical leaf disease dataset classes, dataloaders, and preprocessing pipelines."""

from .dataset import PlantDataset, make_weighted_sampler, get_dataloaders, get_paths_and_labels
from .preprocess import (
    get_train_transforms,
    get_val_transforms,
    get_test_transforms,
    get_tta_transforms,
)

# Friendly alias for backward-compatibility
PlantDiseaseDataset = PlantDataset

__all__ = [
    "PlantDataset",
    "PlantDiseaseDataset",
    "make_weighted_sampler",
    "get_dataloaders",
    "get_paths_and_labels",
    "get_train_transforms",
    "get_val_transforms",
    "get_test_transforms",
    "get_tta_transforms",
]

