"""
serving/schemas.py — Pydantic Data Contracts for Plant Disease Classification API.

Defines strict request/response data models for:
- Live plant leaf disease prediction
- Calibrated probability outputs in range [0.0, 1.0]
- Top-k alternative diagnoses
- Health and class metadata endpoints
"""

from typing import List, Optional
from pydantic import BaseModel, Field


class ClassPrediction(BaseModel):
    """Individual class prediction with confidence."""
    class_name: str = Field(
        ...,
        description="Canonical label (e.g. 'Tomato - Late Blight')."
    )
    crop: str = Field(
        ...,
        description="Identified host crop species (e.g. 'Tomato', 'Corn', 'Apple')."
    )
    disease: str = Field(
        ...,
        description="Identified pathogen, condition, or 'Healthy'."
    )
    confidence: float = Field(
        ...,
        description="Calibrated probability score in range [0.0, 1.0]."
    )


class SingleViewAnalysis(BaseModel):
    """Analysis payload for an individual image view in multi-angle consensus mode."""
    view_index: int = Field(
        ...,
        description="0-based index of this image view."
    )
    crop: str = Field(
        ...,
        description="Predicted crop for this view."
    )
    disease: str = Field(
        ...,
        description="Predicted disease for this view."
    )
    confidence: float = Field(
        ...,
        description="Calibrated confidence for this view in range [0.0, 1.0]."
    )
    heatmap_base64: Optional[str] = Field(
        default=None,
        description="Grad-CAM localization heatmap for this view."
    )
    processed_image_base64: Optional[str] = Field(
        default=None,
        description="Background-removed leaf image for this view."
    )


class PredictionResponse(BaseModel):
    """Response payload returned by POST /api/v1/predict."""
    success: bool = Field(
        default=True,
        description="Status flag indicating successful inference."
    )
    status: str = Field(
        default="confident",
        description="Confidence status: 'confident' (confidence >= threshold) or 'uncertain' (confidence < threshold)."
    )
    threshold_applied: float = Field(
        default=0.60,
        description="Confidence threshold applied for uncertainty status (selected on validation split)."
    )
    crop: str = Field(
        ...,
        description="Identified host crop species."
    )
    disease: str = Field(
        ...,
        description="Identified disease diagnosis or 'Healthy'."
    )
    confidence: float = Field(
        ...,
        description="Calibrated prediction confidence score in range [0.0, 1.0]."
    )
    top_prediction: ClassPrediction = Field(
        ...,
        description="Top-1 highest confidence disease diagnosis."
    )
    top_3_alternatives: List[ClassPrediction] = Field(
        default_factory=list,
        description="Next 3 highest-probability alternative diagnoses."
    )
    top_k: List[ClassPrediction] = Field(
        default_factory=list,
        description="Ranked list of top-k predicted candidate classes with calibrated confidences."
    )
    heatmap_base64: Optional[str] = Field(
        default=None,
        description="Base64 PNG data URL of Grad-CAM localization heatmap."
    )
    crop_valid_mass: Optional[float] = Field(
        default=None,
        description="Unmasked prior probability mass for target crop (range [0.0, 1.0])."
    )
    warning_message: Optional[str] = Field(
        default=None,
        description="Warning explanation when unsupported disease or crop mismatch is detected."
    )
    processed_image_base64: Optional[str] = Field(
        default=None,
        description="Base64 JPEG data URL of the background-removed leaf image."
    )
    num_views: int = Field(
        default=1,
        description="Number of image views evaluated for consensus (1 to 3)."
    )
    consensus_score: Optional[str] = Field(
        default=None,
        description="Consensus summary ratio across views e.g. '3/3 views agree'."
    )
    consensus_agreement: Optional[float] = Field(
        default=None,
        description="Agreement fraction across views in range [0.0, 1.0]."
    )
    crop_confidence: Optional[float] = Field(
        default=None,
        description="Calibrated probability score for the host crop head in range [0.0, 1.0]."
    )
    disease_confidence: Optional[float] = Field(
        default=None,
        description="Calibrated probability score for the disease head in range [0.0, 1.0]."
    )
    crop_status: Optional[str] = Field(
        default=None,
        description="Host crop diagnosis status: 'pass', 'uncertain', or 'mismatch'."
    )
    disease_status: Optional[str] = Field(
        default=None,
        description="Pathology diagnosis status: 'pass' or 'uncertain'."
    )
    failure_attribution: Optional[str] = Field(
        default=None,
        description="Specific reason explaining which neural head caused uncertainty."
    )
    individual_views: Optional[List[SingleViewAnalysis]] = Field(
        default=None,
        description="Detailed breakdown of individual image views in multi-angle mode."
    )
    inference_time_ms: float = Field(
        ...,
        description="Elapsed inference latency in milliseconds."
    )
    timestamp: str = Field(
        ...,
        description="ISO 8601 UTC timestamp of inference request."
    )


class HealthResponse(BaseModel):
    """Response payload returned by GET /api/v1/health."""
    status: str = Field(
        default="healthy",
        description="Overall service operational health status."
    )
    model_architecture: str = Field(
        default="ConvNeXt-Tiny DualHead",
        description="Underlying deep learning backbone."
    )
    num_classes: int = Field(
        ...,
        description="Total number of active disease classes recognized by the loaded model bundle.",
    )
    device: str = Field(
        ...,
        description="Active compute device (e.g. 'cuda:0' or 'cpu')."
    )
    calibration_temperature_crop: float = Field(
        ...,
        description="Currently loaded post-hoc calibration temperature scalar for crop head."
    )
    calibration_temperature_disease: float = Field(
        ...,
        description="Currently loaded post-hoc calibration temperature scalar for disease head."
    )
    version: str = Field(
        default="1.0.0",
        description="API service version."
    )


class ClassesResponse(BaseModel):
    """Response payload returned by GET /api/v1/classes."""
    total_classes: int = Field(
        ...,
        description="Count of all classes."
    )
    classes: List[str] = Field(
        ...,
        description="Alphabetically sorted list of all supported class labels."
    )


class CropsResponse(BaseModel):
    """Response payload returned by GET /api/v1/crops."""
    total_crops: int = Field(
        ...,
        description="Count of botanical host crops."
    )
    crops: List[str] = Field(
        ...,
        description="Alphabetically sorted list of all supported host crops."
    )
