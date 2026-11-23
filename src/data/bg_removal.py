"""
src/data/bg_removal.py — Background removal and leaf foreground isolation.

Uses U2-Net via rembg to segment the leaf foreground and composites it
onto a neutral light-grey background RGB(220, 220, 220).

Security & Integrity:
- Pinned SHA-256 checksum for u2net.onnx: 8d10d2f3bb75ae3b6d527c77944fc5e7dcd94b29809d47a739a7a728a912b491.
- Fails closed with RuntimeError on checksum mismatch.
"""

import base64
import hashlib
import io
import os
from pathlib import Path
import threading
from typing import Optional, Tuple
from PIL import Image

import config

U2NET_SHA256 = "8d10d2f3bb75ae3b6d527c77944fc5e7dcd94b29809d47a739a7a728a912b491"

_SESSION = None
_SESSION_LOCK = threading.Lock()


def verify_u2net_checksum(model_path: Path) -> None:
    """Verify SHA-256 checksum of u2net.onnx and fail closed on mismatch."""
    if not model_path.exists():
        raise FileNotFoundError(f"u2net model file not found at {model_path}")
    h = hashlib.sha256()
    with open(model_path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    actual_hash = h.hexdigest()
    if actual_hash != U2NET_SHA256:
        raise RuntimeError(
            f"Security verification failed: u2net.onnx SHA-256 mismatch. "
            f"Expected {U2NET_SHA256}, got {actual_hash}. Failing closed."
        )


def get_rembg_session():
    """Lazily initialize, verify checksum, and cache the rembg U2-Net session."""
    global _SESSION
    if _SESSION is None:
        with _SESSION_LOCK:
            if _SESSION is None:
                # Direct rembg to the local artifacts directory if present
                rembg_dir = config.ARTIFACTS_DIR / "rembg"
                model_file = rembg_dir / "u2net.onnx"
                if not model_file.exists():
                    model_file = Path.home() / ".u2net" / "u2net.onnx"

                if rembg_dir.exists():
                    os.environ.setdefault("U2NET_HOME", str(rembg_dir))

                # Verify checksum if model file exists locally
                if model_file.exists():
                    verify_u2net_checksum(model_file)

                from rembg import new_session

                _SESSION = new_session("u2net")

                # Verify downloaded file if it was downloaded during new_session
                if not model_file.exists():
                    home_model = Path.home() / ".u2net" / "u2net.onnx"
                    if home_model.exists():
                        verify_u2net_checksum(home_model)

    return _SESSION


def remove_background(
    img: Image.Image,
    bg_color: Tuple[int, int, int] = (220, 220, 220),
) -> Tuple[Image.Image, str]:
    """
    Remove background from a leaf image, composite onto neutral light-grey,
    and return both the composited PIL Image and its base64 JPEG data URL.

    Parameters:
        img: Input PIL Image (RGB or RGBA).
        bg_color: RGB tuple for background composite (default neutral grey 220, 220, 220).

    Returns:
        Tuple of (composited_rgb_image, base64_jpeg_data_url).
    """
    from rembg import remove

    session = get_rembg_session()

    img_rgb = img.convert("RGB")
    rgba_output = remove(img_rgb, session=session)

    # Composite foreground onto solid neutral light-grey background
    bg = Image.new("RGBA", rgba_output.size, (*bg_color, 255))
    composited = Image.alpha_composite(bg, rgba_output).convert("RGB")

    # Encode as JPEG base64 data URL
    buf = io.BytesIO()
    composited.save(buf, format="JPEG", quality=90)
    b64_str = base64.b64encode(buf.getvalue()).decode("ascii")
    processed_image_base64 = f"data:image/jpeg;base64,{b64_str}"

    return composited, processed_image_base64
