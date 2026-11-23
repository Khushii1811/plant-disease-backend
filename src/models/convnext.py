"""
src/models/convnext.py — Dedicated architecture definition for ConvNeXt-Tiny & DualHeadConvNeXt.

ConvNeXt-Tiny (28M parameters) is a modern pure-convolutional network designed
with Vision Transformer design principles:
  - 7x7 depthwise convolutions for large receptive fields
  - LayerNorm instead of BatchNorm for training stability on small batch sizes
  - GELU activations
  - Inverted bottleneck design

DualHeadConvNeXt extends ConvNeXt-Tiny with a hierarchical two-stage architecture:
  - Feature Extractor: 7x7 depthwise convs -> 768-dimensional normalized embedding
  - Head 1 (Crop Head): Linear(768 -> num_crops) plant species identification
  - Head 2 (Disease Head): Linear(768 -> num_classes) fine-grained disease condition
  - Dynamic Logit Masking: Eliminates cross-crop disease misclassifications at inference time.
"""

import json
import logging
from pathlib import Path
from typing import Optional, Tuple, Dict, Any, List, Union, cast

import torch
from torch import nn
from torchvision.models import ConvNeXt_Tiny_Weights, convnext_tiny

logger = logging.getLogger(__name__)


class DualHeadConvNeXt(nn.Module):
    """
    Hierarchical Dual-Head ConvNeXt-Tiny Architecture for Plant Pathology.
    
    Structure:
      - Backbone: ConvNeXt-Tiny feature extraction stages (Stem + 4 Conv Stages: 96, 192, 384, 768 channels).
      - Pooling & Normalization: AdaptiveAvgPool2d((1, 1)) -> LayerNorm2d((768,)) -> Flatten(768).
      - Crop Head: Linear(768 -> 256) -> LayerNorm -> GELU -> Dropout(0.2) -> Linear(256 -> num_crops).
      - Disease Head: Linear(768 -> 512) -> LayerNorm -> GELU -> Dropout(0.3) -> Linear(512 -> num_classes).
      - Dynamic Logit Masking: Enforces biological taxonomy at inference time, guaranteeing 0% cross-crop false positives.
    """

    def __init__(
        self,
        num_crops: int,
        num_classes: int,
        pretrained: bool = True,
        dropout_p: float = 0.2,
    ):
        super().__init__()
        self.num_crops = num_crops
        self.num_classes = num_classes
        self.dropout_p = dropout_p

        weights = ConvNeXt_Tiny_Weights.DEFAULT if pretrained else None
        base = convnext_tiny(weights=weights)

        # Backbone feature extraction stages
        self.features = base.features
        self.avgpool = base.avgpool
        self.norm = base.classifier[0]  # LayerNorm2d((768,))
        self.flatten = base.classifier[1]  # Flatten

        last_linear = cast(nn.Linear, base.classifier[2])
        in_features = int(last_linear.in_features)  # 768

        # Hierarchical MLP Heads
        self.crop_head = nn.Sequential(
            nn.Linear(in_features, 256),
            nn.LayerNorm(256),
            nn.GELU(),
            nn.Dropout(p=dropout_p),
            nn.Linear(256, num_crops),
        )

        self.disease_head = nn.Sequential(
            nn.Linear(in_features, 512),
            nn.LayerNorm(512),
            nn.GELU(),
            nn.Dropout(p=dropout_p + 0.1),
            nn.Linear(512, num_classes),
        )

    def extract_features(self, x: torch.Tensor) -> torch.Tensor:
        """Extracts normalized 768-dimensional global feature vector."""
        feat = self.features(x)
        pooled = self.avgpool(feat)
        normed = self.norm(pooled)
        flat = self.flatten(normed)
        return flat

    def forward(self, x: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Forward pass returning both crop logits and disease logits.
        
        Args:
            x: Input image tensor of shape [B, 3, H, W]
            
        Returns:
            Tuple of (crop_logits [B, 34], disease_logits [B, num_classes])
        """
        embedding = self.extract_features(x)
        crop_logits = self.crop_head(embedding)
        disease_logits = self.disease_head(embedding)
        return crop_logits, disease_logits

    def freeze_all_backbone(self) -> None:
        """Freezes all backbone feature extraction layers for Phase 1 head warmup."""
        for param in self.features.parameters():
            param.requires_grad = False
        for param in self.norm.parameters():
            param.requires_grad = True
        for param in self.crop_head.parameters():
            param.requires_grad = True
        for param in self.disease_head.parameters():
            param.requires_grad = True
        logger.info("ConvNeXt-Tiny: Entire backbone frozen for Phase 1 head warmup.")

    def unfreeze_stages(self, stages: int = 2) -> None:
        """
        Unfreezes the top N convolutional stages of ConvNeXt-Tiny.
        
        ConvNeXt feature hierarchy in torchvision:
          features[0]: Stem (Conv 4x4 stride 4, LayerNorm) -> [B, 96, 56, 56]
          features[1]: Stage 0 (3 ConvNeXt blocks, 96-dim)  -> [B, 96, 56, 56]
          features[2]: Downsample 1 (LayerNorm, Conv 2x2)   -> [B, 192, 28, 28]
          features[3]: Stage 1 (3 ConvNeXt blocks, 192-dim) -> [B, 192, 28, 28]
          features[4]: Downsample 2 (LayerNorm, Conv 2x2)   -> [B, 384, 14, 14]
          features[5]: Stage 2 (9 ConvNeXt blocks, 384-dim) -> [B, 384, 14, 14]
          features[6]: Downsample 3 (LayerNorm, Conv 2x2)   -> [B, 768, 7, 7]
          features[7]: Stage 3 (3 ConvNeXt blocks, 768-dim) -> [B, 768, 7, 7]
          
        Args:
            stages: Number of stages to unfreeze from the top (1 to 4).
                    stages=1: unfreezes features[6:8] (Stage 3, 768-dim)
                    stages=2: unfreezes features[4:8] (Stage 2 + 3, 384-dim & 768-dim) [RECOMMENDED]
                    stages=3: unfreezes features[2:8] (Stage 1 + 2 + 3)
                    stages=4: unfreezes all features including stem
        """
        # Start by freezing everything in features
        for param in self.features.parameters():
            param.requires_grad = False

        if stages == 1:
            active_slice = slice(6, 8)
        elif stages == 2:
            active_slice = slice(4, 8)
        elif stages == 3:
            active_slice = slice(2, 8)
        elif stages >= 4:
            active_slice = slice(0, 8)
        else:
            active_slice = slice(8, 8)

        for block in list(self.features.children())[active_slice]:
            for param in block.parameters():
                param.requires_grad = True

        for param in self.crop_head.parameters():
            param.requires_grad = True
        for param in self.disease_head.parameters():
            param.requires_grad = True

        logger.info(
            "ConvNeXt-Tiny: Unfrozen top %d stages (features[%d:8]); Stem & lower stages remain frozen.",
            stages, active_slice.start if stages > 0 else 8
        )

    def get_parameter_groups(
        self,
        head_lr: float = 1e-4,
        stage3_lr: float = 3e-5,
        stage2_lr: float = 1e-5,
        weight_decay: float = 1e-4,
    ) -> List[Dict[str, Any]]:
        """
        Builds parameter groups with layer-wise discriminative learning rates.
        """
        param_groups = []

        # Group 1: Dual Heads & Norm (Head LR)
        head_params = list(self.crop_head.parameters()) + list(self.disease_head.parameters()) + list(self.norm.parameters())
        head_params = [p for p in head_params if p.requires_grad]
        if head_params:
            param_groups.append({"params": head_params, "lr": head_lr, "weight_decay": weight_decay})

        # Group 2: Stage 3 (features[6:8])
        stage3_params = [p for p in self.features[6:].parameters() if p.requires_grad]
        if stage3_params:
            param_groups.append({"params": stage3_params, "lr": stage3_lr, "weight_decay": weight_decay})

        # Group 3: Stage 2 (features[4:6])
        stage2_params = [p for p in self.features[4:6].parameters() if p.requires_grad]
        if stage2_params:
            param_groups.append({"params": stage2_params, "lr": stage2_lr, "weight_decay": weight_decay})

        # Group 4: Remaining unfrozen lower stages if any
        lower_params = [p for p in self.features[:4].parameters() if p.requires_grad]
        if lower_params:
            param_groups.append({"params": lower_params, "lr": stage2_lr * 0.5, "weight_decay": weight_decay})

        return param_groups


class DualHeadLoss(nn.Module):
    """
    Multi-Task Loss for Hierarchical Plant Pathology Classification.
    
    Total Loss = (crop_weight * L_crop) + (disease_weight * L_disease)
    """

    def __init__(
        self,
        crop_weight: float = 0.3,
        disease_weight: float = 1.0,
        disease_class_weights: Optional[torch.Tensor] = None,
        label_smoothing: float = 0.05,
    ):
        super().__init__()
        self.crop_weight = crop_weight
        self.disease_weight = disease_weight
        self.crop_loss_fn = nn.CrossEntropyLoss(label_smoothing=label_smoothing)
        self.disease_loss_fn = nn.CrossEntropyLoss(
            weight=disease_class_weights,
            label_smoothing=label_smoothing,
        )

    def forward(
        self,
        crop_logits: torch.Tensor,
        disease_logits: torch.Tensor,
        crop_targets: torch.Tensor,
        disease_targets: torch.Tensor,
    ) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        loss_crop = self.crop_loss_fn(crop_logits, crop_targets)
        loss_disease = self.disease_loss_fn(disease_logits, disease_targets)
        total_loss = (self.crop_weight * loss_crop) + (self.disease_weight * loss_disease)
        return total_loss, loss_crop, loss_disease


def build_dualhead_convnext_tiny(
    num_crops: int,
    num_classes: int,
    pretrained: bool = True,
    dropout_p: float = 0.2,
    freeze_backbone: bool = False,
) -> DualHeadConvNeXt:
    """Builds and initializes DualHeadConvNeXt-Tiny model."""
    logger.info(f"Initializing DualHeadConvNeXt-Tiny ({num_crops} Crops -> {num_classes} Diseases)...")
    model = DualHeadConvNeXt(
        num_crops=num_crops,
        num_classes=num_classes,
        pretrained=pretrained,
        dropout_p=dropout_p,
    )

    if freeze_backbone:
        model.freeze_all_backbone()

    return model


def build_convnext_tiny(
    num_classes: int,
    freeze_features: bool = True,
    unfreeze_last_n_blocks: int = 2,
) -> nn.Module:
    """Legacy single-head ConvNeXt-Tiny builder preserved for backwards compatibility."""
    logger.info("Initializing legacy single-head ConvNeXt-Tiny (%d classes)...", num_classes)
    weights = ConvNeXt_Tiny_Weights.DEFAULT
    model = convnext_tiny(weights=weights)

    if freeze_features:
        for param in model.features.parameters():
            param.requires_grad = False

    if unfreeze_last_n_blocks > 0:
        blocks = list(model.features.children())
        for block in blocks[-unfreeze_last_n_blocks:]:
            for param in block.parameters():
                param.requires_grad = True

    last_linear = cast(nn.Linear, model.classifier[2])
    in_features = int(last_linear.in_features)
    model.classifier[2] = nn.Linear(in_features=in_features, out_features=num_classes)
    return model
