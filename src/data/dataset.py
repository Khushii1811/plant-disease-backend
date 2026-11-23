"""
Dataset loading utilities for the plant disease classification pipeline.

Uses a custom Dataset class (rather than torchvision's ImageFolder) to
gracefully handle corrupt/unreadable image files with a clear error,
which matters given this dataset was aggregated from 7 different sources
and may contain a small number of bad files.
"""

import logging
import os
from typing import Callable, List, Optional, Tuple

import torch
from PIL import Image
from torch.utils.data import DataLoader, Dataset, WeightedRandomSampler

import config
from .preprocess import get_test_transforms, get_train_transforms, get_val_transforms, load_image

logger = logging.getLogger(__name__)


class PlantDataset(Dataset):
    """
    Custom PyTorch Dataset for loading plant disease images and labels
    from explicit path and label lists, with graceful per-image error handling.
    """

    def __init__(
        self,
        image_paths: List[str],
        labels: List[int],
        transform: Optional[Callable] = None,
    ):
        self.image_paths = image_paths
        self.labels = labels
        self.transform = transform

    def __len__(self) -> int:
        return len(self.image_paths)

    def __getitem__(self, idx: int) -> Tuple[torch.Tensor, int]:
        img_path = self.image_paths[idx]
        label = self.labels[idx]

        try:
            image = load_image(img_path)
        except Exception as e:
            raise IOError(f"Failed to load image at {img_path}: {e}")

        if self.transform:
            image = self.transform(image)

        return image, label


def make_weighted_sampler(
    labels: List[int],
    generator: Optional[torch.Generator] = None,
) -> WeightedRandomSampler:
    """
    Build a WeightedRandomSampler that over-samples rare classes so that
    every training batch sees each class at roughly the same rate.

    This is the primary fix for the class-imbalance problem: CrossEntropyLoss
    with class weights corrects the *gradient*, but without this sampler the
    model still *sees* rare classes proportionally less during training.
    Combining both (sampler + weighted loss) gives the strongest signal.

    Args:
        labels: Integer class label for every sample in the training set.
        generator: Optional PyTorch Generator for reproducible pseudo-random sampling.

    Returns:
        A WeightedRandomSampler configured for len(labels) draws with replacement.
    """
    label_tensor = torch.tensor(labels, dtype=torch.long)
    class_counts = torch.bincount(label_tensor)
    # Avoid division-by-zero for classes that somehow have 0 samples
    class_counts = class_counts.clamp(min=1)
    class_weights = 1.0 / class_counts.float()
    sample_weights = class_weights[label_tensor]
    return WeightedRandomSampler(
        weights=sample_weights,
        num_samples=len(sample_weights),
        replacement=True,
        generator=generator,
    )


def get_paths_and_labels(base_dir: str) -> Tuple[List[str], List[int], List[str]]:
    """
    Scan a directory structured as base_dir/class_name/image.jpg and
    extract file paths and integer class labels.

    Args:
        base_dir: Root directory containing one subfolder per class.

    Returns:
        (image_paths, labels, class_names) — class_names is sorted, and
        labels are integer indices into class_names.

    Raises:
        FileNotFoundError: If base_dir doesn't exist.
    """
    if not os.path.exists(base_dir):
        raise FileNotFoundError(f"Directory not found: {base_dir}")

    image_paths: List[str] = []
    labels: List[int] = []

    classes = sorted(
        d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))
    )
    class_to_idx = {cls_name: idx for idx, cls_name in enumerate(classes)}

    for cls_name, class_idx in class_to_idx.items():
        cls_folder = os.path.join(base_dir, cls_name)
        for root, _, files in os.walk(cls_folder):
            for file in files:
                if file.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".webp")):
                    image_paths.append(os.path.join(root, file))
                    labels.append(class_idx)

    return image_paths, labels, classes


def get_dataloaders(
    train_dir: Optional[str] = None,
    val_dir: Optional[str] = None,
    test_dir: Optional[str] = None,
    batch_size: Optional[int] = None,
    num_workers: Optional[int] = None,
    generator: Optional[torch.Generator] = None,
    worker_init_fn: Optional[Callable[[int], None]] = None,
) -> Tuple[DataLoader, DataLoader, DataLoader, List[str]]:
    """
    Build train/val/test DataLoaders from the configured (or explicitly
    passed) directories.

    Any argument left as None falls back to the corresponding value in
    config.py, so the pipeline stays consistent by default while still
    allowing overrides (e.g. a smaller batch_size for quick local testing).

    Raises:
        FileNotFoundError: If any directory doesn't exist.
        ValueError: If train/val/test splits have mismatched class sets.

    Returns:
        (train_loader, val_loader, test_loader, class_names)
    """
    train_dir = train_dir or str(config.TRAIN_DIR)
    val_dir = val_dir or str(config.VAL_DIR)
    test_dir = test_dir or str(config.TEST_DIR)
    batch_size = batch_size or config.BATCH_SIZE
    num_workers = num_workers if num_workers is not None else config.NUM_WORKERS

    train_paths, train_labels, train_classes = get_paths_and_labels(train_dir)
    val_paths, val_labels, val_classes = get_paths_and_labels(val_dir)
    test_paths, test_labels, test_classes = get_paths_and_labels(test_dir)

    for split_name, classes in [("val", val_classes), ("test", test_classes)]:
        mismatch = set(train_classes).symmetric_difference(classes)
        if mismatch:
            raise ValueError(
                f"Class mismatch between 'train' and '{split_name}': {mismatch}"
            )

    train_dataset = PlantDataset(train_paths, train_labels, transform=get_train_transforms())
    val_dataset = PlantDataset(val_paths, val_labels, transform=get_val_transforms())
    test_dataset = PlantDataset(test_paths, test_labels, transform=get_test_transforms())

    # WeightedRandomSampler over-samples rare classes so every batch has
    # balanced class representation. shuffle=True is replaced by the sampler
    # (they are mutually exclusive in PyTorch's DataLoader).
    train_sampler = make_weighted_sampler(train_labels, generator=generator)
    train_loader = DataLoader(
        train_dataset, batch_size=batch_size, sampler=train_sampler,
        num_workers=num_workers, pin_memory=torch.cuda.is_available(),
        generator=generator, worker_init_fn=worker_init_fn,
    )
    val_loader = DataLoader(
        val_dataset, batch_size=batch_size, shuffle=False,
        num_workers=num_workers, pin_memory=torch.cuda.is_available(),
        generator=generator, worker_init_fn=worker_init_fn,
    )
    test_loader = DataLoader(
        test_dataset, batch_size=batch_size, shuffle=False,
        num_workers=num_workers, pin_memory=torch.cuda.is_available(),
        generator=generator, worker_init_fn=worker_init_fn,
    )

    logger.info(
        "Loaded dataset: %d train / %d val / %d test images, %d classes",
        len(train_dataset), len(val_dataset), len(test_dataset), len(train_classes),
    )

    return train_loader, val_loader, test_loader, train_classes


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    train_loader, val_loader, test_loader, classes = get_dataloaders()
    print(f"Classes ({len(classes)}): {classes}")