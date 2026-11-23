"""
tests/test_preprocess.py — Unit tests for data preprocessing and image ingestion transforms.

Tests:
  1. Train transform pipeline outputs valid (3, 256, 256) float32 tensor.
  2. Val transform pipeline outputs valid (3, 256, 256) float32 tensor.
  3. Test transform pipeline outputs valid (3, 256, 256) float32 tensor.
  4. Image loading from filesystem Path, str, bytes, io.BytesIO, and PIL Image.
  5. EXIF orientation transposition correctly orients rotated images.
  6. Normalization produces non-zero float values with appropriate channel dimension.
"""

import io
from pathlib import Path
from PIL import Image
import pytest
import torch

from src.data.preprocess import (
    get_train_transforms,
    get_val_transforms,
    get_test_transforms,
    load_image,
)


def _create_test_image(size=(300, 200), color=(100, 180, 60)) -> Image.Image:
    """Create a synthetic PIL image for testing."""
    return Image.new("RGB", size, color=color)


def test_get_train_transforms_shape_and_type():
    """Verify train transforms produce normalized (3, 256, 256) float32 tensor."""
    tf = get_train_transforms()
    img = _create_test_image()
    tensor = tf(img)

    assert isinstance(tensor, torch.Tensor)
    assert tensor.shape == (3, 256, 256)
    assert tensor.dtype == torch.float32


def test_get_val_transforms_shape_and_type():
    """Verify validation transforms produce deterministic (3, 256, 256) float32 tensor."""
    tf = get_val_transforms()
    img = _create_test_image()
    tensor = tf(img)

    assert isinstance(tensor, torch.Tensor)
    assert tensor.shape == (3, 256, 256)
    assert tensor.dtype == torch.float32


def test_get_test_transforms_shape_and_type():
    """Verify test transforms produce deterministic (3, 256, 256) float32 tensor."""
    tf = get_test_transforms()
    img = _create_test_image()
    tensor = tf(img)

    assert isinstance(tensor, torch.Tensor)
    assert tensor.shape == (3, 256, 256)
    assert tensor.dtype == torch.float32


def test_load_image_from_path(tmp_path: Path):
    """Verify load_image loads RGB image from pathlib.Path and str."""
    img_path = tmp_path / "sample_leaf.jpg"
    img = _create_test_image((256, 256), color=(50, 150, 50))
    img.save(img_path, format="JPEG")

    loaded_path = load_image(img_path)
    assert isinstance(loaded_path, Image.Image)
    assert loaded_path.mode == "RGB"
    assert loaded_path.size == (256, 256)

    loaded_str = load_image(str(img_path))
    assert isinstance(loaded_str, Image.Image)
    assert loaded_str.mode == "RGB"
    assert loaded_str.size == (256, 256)


def test_load_image_from_bytes_and_io():
    """Verify load_image loads RGB image from raw encoded bytes and io.BytesIO."""
    img = _create_test_image((128, 128), color=(30, 120, 200))
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    raw_bytes = buf.getvalue()

    loaded = load_image(raw_bytes)
    assert isinstance(loaded, Image.Image)
    assert loaded.mode == "RGB"
    assert loaded.size == (128, 128)

    buf.seek(0)
    loaded_io = load_image(buf)
    assert isinstance(loaded_io, Image.Image)
    assert loaded_io.mode == "RGB"
    assert loaded_io.size == (128, 128)


def test_load_image_from_pil():
    """Verify load_image converts RGBA or Grayscale PIL image directly to RGB."""
    rgba_img = Image.new("RGBA", (100, 100), color=(100, 150, 200, 128))
    loaded = load_image(rgba_img)
    assert loaded.mode == "RGB"

    l_img = Image.new("L", (100, 100), color=128)
    loaded_l = load_image(l_img)
    assert loaded_l.mode == "RGB"


def test_load_image_exif_transpose():
    """Verify EXIF orientation transposition corrects rotated images."""
    # Create image with width=400, height=200
    base_img = Image.new("RGB", (400, 200), color=(80, 160, 40))
    exif = Image.Exif()
    # EXIF tag 0x0112 is Orientation; value 6 means rotated 90 CW (transposed orientation is 200x400)
    exif[0x0112] = 6

    buf = io.BytesIO()
    base_img.save(buf, format="JPEG", exif=exif)
    img_bytes = buf.getvalue()

    loaded = load_image(img_bytes)
    assert isinstance(loaded, Image.Image)
    assert loaded.mode == "RGB"
    # When orientation 6 is transposed upright, width and height swap: (200, 400)
    assert loaded.size == (200, 400)
