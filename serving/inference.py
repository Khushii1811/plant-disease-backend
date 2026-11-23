"""
serving/inference.py — Production inference service for the DualHead ConvNeXt-Tiny model.

Responsibilities:
  - Load the verified model bundle once at module import.
  - Expose single public function:
        predict(image_bytes: bytes, crop: Optional[str] = None) -> PredictionResponse
    calling the shared prediction engine (src.models.predict).
  - Strictly returns botanical disease diagnosis without actuation or treatment decisions.
"""

import json
import logging
from pathlib import Path
from typing import List, Optional, Union

import torch

import config
from src.models.bundle_loader import load_model_bundle
from src.models.predict import CONFIDENCE_THRESHOLD, predict_multi_images, predict_single_image
from serving.schemas import ClassPrediction, PredictionResponse, SingleViewAnalysis

logger = logging.getLogger("serving.inference")

_device = "cuda" if torch.cuda.is_available() else "cpu"
logger.info("Initializing inference bundle on %s...", _device)
_bundle = None
try:
    _bundle = load_model_bundle("v1", device=_device)
    _class_names = _bundle.class_names
except Exception as e:
    logger.warning("Could not load model bundle on module import (weights missing): %s", e)
    _bundle = None
    _names_file = config.MODELS_DIR / "v1" / "class_names.json"
    if _names_file.exists():
        with open(_names_file, "r", encoding="utf-8") as f:
            _class_names = json.load(f)
    else:
        _class_names = []
device = _device


def predict(
    image_bytes: Union[bytes, List[bytes]],
    crop: Optional[str] = None,
    threshold: float = CONFIDENCE_THRESHOLD,
    remove_bg: bool = False,
    heatmap: bool = False,
) -> PredictionResponse:
    """
    Execute plant leaf disease classification on input image bytes.

    Parameters:
        image_bytes: Raw binary bytes of uploaded leaf image, or list of bytes (1-3 images).
        crop: Optional host crop constraint to restrict candidate diagnoses.
        threshold: Calibrated confidence threshold for uncertainty flagging.
        remove_bg: Optional toggle to remove background and isolate leaf foreground.

    Returns:
        PredictionResponse schema with top prediction, alternatives, and calibrated confidence.
    """
    if _bundle is None:
        raise RuntimeError("Model bundle not loaded: weights missing.")

    inputs = image_bytes if isinstance(image_bytes, list) else [image_bytes]

    result = predict_multi_images(
        bundle=_bundle,
        image_inputs=inputs,
        crop_constraint_name=crop,
        threshold=threshold,
        remove_bg=remove_bg,
        heatmap=heatmap,
    )

    top_pred = ClassPrediction(**result["top_prediction"])
    alternatives = [ClassPrediction(**alt) for alt in result["top_3_alternatives"]]
    top_k_preds = [ClassPrediction(**item) for item in result["top_k"]]
    views_list = (
        [SingleViewAnalysis(**v) for v in result["individual_views"]]
        if result.get("individual_views")
        else None
    )

    return PredictionResponse(
        success=True,
        status=result["status"],
        threshold_applied=result["threshold_applied"],
        crop=result["crop"],
        disease=result["disease"],
        confidence=result["confidence"],
        top_prediction=top_pred,
        top_3_alternatives=alternatives,
        top_k=top_k_preds,
        heatmap_base64=result.get("heatmap_base64"),
        crop_valid_mass=result.get("crop_valid_mass"),
        warning_message=result.get("warning_message"),
        processed_image_base64=result.get("processed_image_base64"),
        num_views=result.get("num_views", len(inputs)),
        consensus_score=result.get("consensus_score"),
        consensus_agreement=result.get("consensus_agreement"),
        crop_confidence=result.get("crop_confidence"),
        disease_confidence=result.get("disease_confidence"),
        crop_status=result.get("crop_status"),
        disease_status=result.get("disease_status"),
        failure_attribution=result.get("failure_attribution"),
        individual_views=views_list,
        inference_time_ms=result["inference_time_ms"],
        timestamp=result["timestamp"],
    )


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        img_path = Path(sys.argv[1])
        if img_path.exists():
            data = img_path.read_bytes()
            resp = predict(data)
            print(f"Prediction: {resp.crop} - {resp.disease} (Confidence: {resp.confidence:.4f}, Status: {resp.status})")
        else:
            print(f"File not found: {img_path}")
    else:
        print("Usage: python serving/inference.py <image_path>")
