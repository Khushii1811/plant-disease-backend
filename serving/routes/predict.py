"""
serving/routes/predict.py — FastAPI router for inference endpoints.

Endpoints:
  POST /api/v1/predict   — Upload a leaf image, get a PredictionResponse.
  GET  /api/v1/classes   — List all supported disease class labels.
  GET  /api/v1/crops     — List all supported botanical host crops.
"""

import io
import json
import logging
import os
from pathlib import Path
import threading
from typing import List, Optional, Tuple
from fastapi import APIRouter, File, Form, HTTPException, UploadFile, status
from PIL import Image, UnidentifiedImageError

import config
from serving.inference import _bundle, _class_names, predict
from serving.schemas import ClassesResponse, CropsResponse, PredictionResponse

logger = logging.getLogger("routes.predict")

router = APIRouter(prefix="/api/v1", tags=["Inference"])

_INFERENCE_SEMAPHORE = threading.BoundedSemaphore(2)

_ALLOWED_CONTENT_TYPES = {
    "image/jpeg",
    "image/jpg",
    "image/png",
    "image/webp",
    "image/bmp",
    "image/tiff",
    "image/jfif",
    "image/pjpeg",
    "image/x-png",
    "application/octet-stream",
}
_ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tiff", ".jfif"}
_MAX_UPLOAD_BYTES = 10 * 1024 * 1024
_MAX_IMAGE_PIXELS = 50_000_000
_MAX_REQUEST_PIXELS = 100_000_000
Image.MAX_IMAGE_PIXELS = _MAX_IMAGE_PIXELS


def _get_valid_crops() -> List[str]:
    if _bundle is not None:
        return _bundle.crop_hierarchy.get("crops", [])
    hierarchy_file = config.MODELS_DIR / "v1" / "crop_hierarchy.json"
    if hierarchy_file.exists():
        with open(hierarchy_file, "r", encoding="utf-8") as f:
            return json.load(f).get("crops", [])
    return []


def _validate_and_read_image(upload_file: UploadFile) -> Tuple[bytes, int]:
    content_type = (getattr(upload_file, "content_type", "") or "").lower()
    ext = Path(getattr(upload_file, "filename", "") or "").suffix.lower()
    if content_type not in _ALLOWED_CONTENT_TYPES and ext not in _ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=(
                f"Unsupported file type '{content_type or ext}' for '{getattr(upload_file, 'filename', '')}'. "
                f"Accepted image formats: JPEG, PNG, WebP, BMP, TIFF."
            ),
        )

    if hasattr(upload_file, "file") and hasattr(upload_file.file, "read"):
        if hasattr(upload_file.file, "seek"):
            upload_file.file.seek(0)
        image_bytes = upload_file.file.read()
    else:
        image_bytes = upload_file.read()

    fname = getattr(upload_file, "filename", "image") or "image"
    if len(image_bytes) == 0:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=f"Uploaded file '{fname}' is empty (0 bytes).",
        )
    if len(image_bytes) > _MAX_UPLOAD_BYTES:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File '{fname}' exceeds maximum allowed size of {_MAX_UPLOAD_BYTES // (1024 * 1024)} MB.",
        )

    # Inspect image header dimensions before full decoding
    try:
        with Image.open(io.BytesIO(image_bytes)) as probe:
            width, height = probe.size
            pixel_count = width * height
            if pixel_count > _MAX_IMAGE_PIXELS:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                    detail=(
                        f"Image resolution {width}x{height} ({pixel_count:,} pixels) "
                        f"exceeds maximum allowed limit of 50 MP (50,000,000 pixels). "
                        f"Please downscale or resize your image below 50 MP before uploading."
                    ),
                )
    except HTTPException:
        raise
    except (UnidentifiedImageError, OSError, ValueError, Image.DecompressionBombError) as exc:
        logger.warning("Unprocessable image payload during header probe: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Invalid or unprocessable image payload.",
        ) from exc

    return image_bytes, pixel_count


@router.post(
    "/predict",
    response_model=PredictionResponse,
    summary="Predict plant disease from 1 to 3 leaf images (Multi-view consensus)",
    description=(
        "Upload 1 to 3 JPG/PNG/WebP leaf photos (max 10 MB per image, max 50 MP per image, max 100 MP aggregate budget per request). "
        "Supports backward-compatible single-file upload via 'file', or multi-file upload via 'files'. "
        "When multiple views are uploaded, probability distributions are ensembled via soft-voting "
        "and consensus agreement is computed. Returns the top-1 diagnosis, top-3 alternatives, "
        "calibrated confidence scores in range [0, 1], Grad-CAM localized heatmaps per view, "
        "and uncertainty status (fixed threshold tau=0.60).\n\n"
        "Constrained Mode: Optionally supply 'crop' (case-insensitive, matched against "
        "the supported botanical host crops) to strictly constrain predictions and "
        "alternatives to diseases associated with that crop. An empty string (crop='') "
        "or omitting the parameter triggers unconstrained auto-detection mode. "
        "Supplying an unrecognized crop name returns HTTP 422."
    ),
    status_code=status.HTTP_200_OK,
)
def predict_disease(
    file: Optional[UploadFile] = File(
        None,
        description="Single leaf image file (backward-compatible, JPEG, PNG, WebP, BMP, TIFF)",
    ),
    files: Optional[List[UploadFile]] = File(
        None,
        description="1 to 3 leaf image files for multi-view consensus diagnosis",
    ),
    crop: Optional[str] = Form(
        None,
        description="Optional crop name to constrain disease prediction. Setting crop=\"\" (empty string) or omitting triggers auto-detect mode.",
    ),
    remove_bg: bool = Form(
        False,
        description="Optional toggle to remove background and isolate leaf foreground before inference.",
    ),
    heatmap: bool = Form(
        False,
        description="Optional toggle to generate Grad-CAM localization heatmap (default false).",
    ),
) -> PredictionResponse:
    upload_list: List[UploadFile] = []
    if isinstance(files, (list, tuple)):
        upload_list = [f for f in files if f and hasattr(f, "filename") and f.filename and f.filename.strip()]

    if not upload_list and file is not None and not hasattr(file, "default"):
        if hasattr(file, "filename") and file.filename and file.filename.strip():
            upload_list = [file]

    if not upload_list:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="No leaf image provided. Please upload at least 1 image (up to 3 images).",
        )

    if len(upload_list) > 3:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=f"Maximum 3 images allowed for multi-view consensus diagnosis. Received {len(upload_list)} images.",
        )

    image_bytes_list: List[bytes] = []
    total_request_pixels = 0
    for f in upload_list:
        b_data, px_count = _validate_and_read_image(f)
        total_request_pixels += px_count
        image_bytes_list.append(b_data)

    if total_request_pixels > _MAX_REQUEST_PIXELS:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=(
                f"Total request resolution ({total_request_pixels:,} pixels, {total_request_pixels / 1e6:.1f} MP "
                f"across {len(upload_list)} images) exceeds maximum aggregate budget of 100 MP (100,000,000 pixels). "
                f"Please downscale or reduce the number of uploaded images."
            ),
        )

    valid_crops = _get_valid_crops()
    valid_crops_map = {c.lower(): c for c in valid_crops}

    crop_name = None
    if isinstance(crop, str):
        if crop == "":
            crop_name = None
        else:
            trimmed = crop.strip()
            if not trimmed or trimmed.lower() not in valid_crops_map:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                    detail=(
                        f"Invalid crop constraint '{crop}'. "
                        f"Must be one of the {len(valid_crops)} supported crops: {', '.join(sorted(valid_crops))}."
                    ),
                )
            crop_name = valid_crops_map[trimmed.lower()]
    elif crop is not None and not hasattr(crop, "default"):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=f"Invalid crop constraint: expected string, got {type(crop).__name__}.",
        )
    # Sanitize boolean form parameters (supports direct function calls with Form defaults)
    is_remove_bg = False
    if isinstance(remove_bg, bool):
        is_remove_bg = remove_bg
    elif hasattr(remove_bg, "default"):
        is_remove_bg = bool(remove_bg.default)
    elif isinstance(remove_bg, str):
        is_remove_bg = remove_bg.lower() in ("true", "1", "yes")

    if is_remove_bg and os.getenv("ENABLE_BG_REMOVAL") != "1":
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=(
                "Background removal is disabled in production (ENABLE_BG_REMOVAL=1 required). "
                "Empirical audit demonstrated a ~30-point degradation in foliar disease classification accuracy."
            ),
        )

    is_heatmap = False
    if isinstance(heatmap, bool):
        is_heatmap = heatmap
    elif hasattr(heatmap, "default"):
        is_heatmap = bool(heatmap.default)
    elif isinstance(heatmap, str):
        is_heatmap = heatmap.lower() in ("true", "1", "yes")

    try:
        with _INFERENCE_SEMAPHORE:
            response = predict(
                image_bytes=image_bytes_list,
                crop=crop_name,
                remove_bg=is_remove_bg,
                heatmap=is_heatmap,
            )
            return response
    except (UnidentifiedImageError, OSError, ValueError, Image.DecompressionBombError) as exc:
        logger.warning("Unprocessable image payload: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Invalid or unprocessable image payload.",
        ) from exc
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Inference failed: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal inference error.",
        ) from exc


@router.get(
    "/classes",
    response_model=ClassesResponse,
    summary="List all supported disease classes",
    description="Returns the full list of botanical disease class labels recognized by the model.",
)
async def list_classes() -> ClassesResponse:
    return ClassesResponse(
        total_classes=len(_class_names),
        classes=sorted(_class_names),
    )


@router.get(
    "/crops",
    response_model=CropsResponse,
    summary="List all supported botanical host crops",
    description="Returns the canonical list of host crops supported by the dual-head hierarchy.",
)
async def list_crops() -> CropsResponse:
    crops = _get_valid_crops()
    return CropsResponse(
        total_crops=len(crops),
        crops=sorted(crops),
    )
