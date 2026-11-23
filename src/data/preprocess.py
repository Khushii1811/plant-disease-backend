"""
Image preprocessing transform pipelines for train/val/test splits.

Training uses aggressive data augmentation targeting rare-class generalization.
Validation and test use a deterministic pipeline (no augmentation) so evaluation
results are stable and repeatable.

Augmentation rationale (see docs/essays/docs/essays/CHLOROPHYLL_AND_CONVOLUTIONS.md for full context):
- RandomResizedCrop: simulates varying camera distance and partial views
- ColorJitter: handles lighting, shadow, and color cast variation
- RandomVerticalFlip: plant disease images have no fixed orientation
- RandomErasing: simulates occlusion (leaves overlapping, partial damage)
These are especially beneficial for rare/low-support classes that have few
training images, as each epoch now presents meaningfully different views.

TTA note (see get_tta_transforms):
Test-Time Augmentation applies moderate random transforms to already-normalised
tensors at inference time. Only tensor-compatible geometric transforms are used
here - there is no PIL step and no risk of double-normalisation.
"""

import io
from pathlib import Path
from typing import Callable, Optional, Union
from PIL import Image, ImageOps
from torchvision import transforms

import config


def load_image(
    path_or_bytes: Union[str, Path, bytes, io.BytesIO, Image.Image],
    max_pixels: Optional[int] = None,
) -> Image.Image:
    """
    Unified image loading function.

    Applies PIL.ImageOps.exif_transpose() to correctly orient camera
    images according to EXIF metadata and converts to RGB mode.
    Optional max_pixels parameter enforces resolution ceiling when specified.
    """
    if isinstance(path_or_bytes, (str, Path)):
        with open(path_or_bytes, "rb") as f:
            data = f.read()
        with Image.open(io.BytesIO(data)) as img:
            if max_pixels is not None and img.width * img.height > max_pixels:
                raise ValueError(
                    f"Image resolution {img.width}x{img.height} ({img.width * img.height} pixels) "
                    f"exceeds maximum allowed limit of {max_pixels} pixels."
                )
            img = ImageOps.exif_transpose(img)
            return img.convert("RGB")
    elif isinstance(path_or_bytes, (bytes, io.BytesIO)):
        buf = io.BytesIO(path_or_bytes) if isinstance(path_or_bytes, bytes) else path_or_bytes
        with Image.open(buf) as img:
            if max_pixels is not None and img.width * img.height > max_pixels:
                raise ValueError(
                    f"Image resolution {img.width}x{img.height} ({img.width * img.height} pixels) "
                    f"exceeds maximum allowed limit of {max_pixels} pixels."
                )
            img = ImageOps.exif_transpose(img)
            return img.convert("RGB")
    elif isinstance(path_or_bytes, Image.Image):
        if max_pixels is not None and path_or_bytes.width * path_or_bytes.height > max_pixels:
            raise ValueError(
                f"Image resolution {path_or_bytes.width}x{path_or_bytes.height} ({path_or_bytes.width * path_or_bytes.height} pixels) "
                f"exceeds maximum allowed limit of {max_pixels} pixels."
            )
        img = ImageOps.exif_transpose(path_or_bytes)
        return img.convert("RGB")
    else:
        raise TypeError(f"Unsupported image input type: {type(path_or_bytes)}")


def get_train_transforms() -> transforms.Compose:
    """
    Botanically safe augmentation pipeline for training data.

    Enforces strict botanical constraints (see docs/essays/CHLOROPHYLL_AND_CONVOLUTIONS.md):
    - Conservative crop (0.75 to 1.0): Prevents cutting out focal lesions or severe over-zooming.
    - Flips & Moderate Rotation (15 deg): Simulates foliage angles without corner-cut distortion.
    - ColorJitter with locked hue (hue=0.0): Preserves biological chlorophyll and rust pustule
      colors while simulating real solar illumination and camera exposure shifts.
    - NO RandomGrayscale: Grayscale destroys chlorosis and necrosis color diagnostics.
    - RandomErasing: Simulates natural occlusion (overlapping leaves, shadows, dirt specks).
    - ImageNet normalization required by pretrained ConvNeXt backbone.
    """
    return transforms.Compose([
        transforms.RandomResizedCrop(config.IMAGE_SIZE, scale=(0.75, 1.0)),
        transforms.RandomHorizontalFlip(p=0.5),
        transforms.RandomVerticalFlip(p=0.5),
        transforms.RandomRotation(degrees=15),
        transforms.ColorJitter(
            brightness=0.15,
            contrast=0.15,
            saturation=0.10,
            hue=0.0,  # CRITICAL: Locked to 0.0 to prevent synthetic chlorosis / color-shifting pathogens
        ),
        transforms.ToTensor(),
        transforms.Normalize(mean=config.NORMALIZE_MEAN, std=config.NORMALIZE_STD),
        transforms.RandomErasing(p=0.2, scale=(0.02, 0.12), value="random"),
    ])


def get_val_transforms() -> transforms.Compose:
    """
    Deterministic preprocessing pipeline for validation data.

    No augmentation - validation metrics should reflect the model's
    performance on stable, unmodified inputs.
    """
    return transforms.Compose([
        transforms.Resize(config.IMAGE_SIZE),
        transforms.ToTensor(),
        transforms.Normalize(mean=config.NORMALIZE_MEAN, std=config.NORMALIZE_STD),
    ])


def get_test_transforms() -> transforms.Compose:
    """
    Deterministic preprocessing pipeline for test data.

    Identical to validation transforms - both should evaluate the model
    under the same, unaugmented conditions.
    """
    return get_val_transforms()


def get_tta_transforms() -> transforms.Compose:
    """
    Tensor-level augmentation pipeline for Test-Time Augmentation (TTA).

    IMPORTANT: This transform is applied to already-normalised image tensors
    produced by get_val_transforms(). It must NOT include ToTensor() or
    Normalize() - doing so would double-normalise the inputs and degrade accuracy.

    Only geometric transforms that operate directly on tensors are used:
    - RandomHorizontalFlip / RandomVerticalFlip: mirror symmetry variants
    - RandomRotation(15 deg): moderate rotation - tighter than training (30 deg) to
      avoid introducing artefacts on already-cropped, normalised tensors
    """
    return transforms.Compose([
        transforms.RandomHorizontalFlip(p=0.5),
        transforms.RandomVerticalFlip(p=0.3),
        transforms.RandomRotation(degrees=15),
    ])
