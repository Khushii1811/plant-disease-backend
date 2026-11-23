"""src.models — Model architecture definitions (EfficientNet-B0, ConvNeXt-Tiny, DualHeadConvNeXt)."""

from .convnext import (
    DualHeadConvNeXt,
    DualHeadLoss,
    build_dualhead_convnext_tiny,
    build_convnext_tiny,
)

__all__ = [
    "DualHeadConvNeXt",
    "DualHeadLoss",
    "build_dualhead_convnext_tiny",
    "build_convnext_tiny",
]
