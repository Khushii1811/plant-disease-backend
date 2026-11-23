"""
src/models/bundle_loader.py — Production Model Bundle Loader.

Loads models/<version>/ with mandatory integrity verification:
  1. Verifies SHA-256 checksums from models/<version>/checksums.txt.
  2. Asserts class_names.json contains exactly 195 classes (v1) or legacy classes (v0).
  3. Asserts crop_hierarchy.json contains exactly 34 crops and maps all disease classes.
  4. Loads calibration.json (T_disease, T_crop) and preprocess.json.
  5. Instantiates DualHeadConvNeXt and loads state_dict.
  6. Fails fast with descriptive errors if any check fails.
"""

import hashlib
import json
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Tuple

import torch
import torch.nn as nn

import config
from .convnext import build_dualhead_convnext_tiny, DualHeadConvNeXt

logger = logging.getLogger("bundle_loader")

PROJECT_ROOT = config.PROJECT_ROOT


@dataclass
class ModelBundle:
    version: str
    model: DualHeadConvNeXt
    class_names: List[str]
    crop_hierarchy: Dict[str, Any]
    calibration: Dict[str, Any]
    preprocess: Dict[str, Any]
    device: str
    membership_matrix: torch.Tensor

    @property
    def T_disease(self) -> float:
        return float(self.calibration.get("T_disease", 1.0))

    @property
    def T_crop(self) -> float:
        return float(self.calibration.get("T_crop", 1.0))


def verify_checksums(bundle_dir: Path) -> None:
    """Verifies SHA-256 checksums of all tracked files in the bundle directory."""
    checksum_file = bundle_dir / "checksums.txt"
    if not checksum_file.exists():
        raise FileNotFoundError(f"Missing checksums.txt in {bundle_dir}")

    for line in checksum_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split(maxsplit=1)
        if len(parts) != 2:
            continue
        expected_sha, fname = parts
        target_path = bundle_dir / fname.strip()
        if not target_path.exists():
            raise FileNotFoundError(f"Bundle integrity failure: missing file {fname} in {bundle_dir}")
        actual_sha = hashlib.sha256(target_path.read_bytes()).hexdigest()
        if actual_sha.lower() != expected_sha.lower():
            raise ValueError(
                f"Checksum mismatch for {fname} in {bundle_dir}!\n"
                f"  Expected: {expected_sha}\n"
                f"  Actual:   {actual_sha}"
            )
    logger.info("Checksum verification passed for bundle at %s", bundle_dir)


def verify_class_and_hierarchy_consistency(
    bundle_dir: Path,
    class_names: List[str],
    crop_hierarchy: Dict[str, Any],
) -> None:
    """
    Validates cross-consistency across:
      - class_names.json
      - class_to_idx.json
      - idx_to_class.json
      - crop_hierarchy.json
    Fails fast with descriptive error if any discrepancies, ordering mismatches,
    or invalid indices exist.
    """
    num_expected = len(class_names)
    if num_expected != 177:
        raise ValueError(f"Consistency failure: class_names.json must contain exactly 177 classes (v1 release), found {num_expected}")

    # 1. Verify class_to_idx.json
    c2i_path = bundle_dir / "class_to_idx.json"
    if not c2i_path.exists():
        raise FileNotFoundError(f"Consistency failure: missing {c2i_path}")
    class_to_idx = json.loads(c2i_path.read_text(encoding="utf-8"))
    if len(class_to_idx) != num_expected:
        raise ValueError(f"Consistency failure: class_to_idx.json has {len(class_to_idx)} entries, expected {num_expected}")
    for idx, name in enumerate(class_names):
        if name not in class_to_idx:
            raise ValueError(f"Consistency failure: class '{name}' missing from class_to_idx.json")
        if class_to_idx[name] != idx:
            raise ValueError(f"Consistency failure: class_to_idx['{name}']={class_to_idx[name]} != expected index {idx}")

    # 2. Verify idx_to_class.json
    i2c_path = bundle_dir / "idx_to_class.json"
    if not i2c_path.exists():
        raise FileNotFoundError(f"Consistency failure: missing {i2c_path}")
    idx_to_class = json.loads(i2c_path.read_text(encoding="utf-8"))
    if len(idx_to_class) != num_expected:
        raise ValueError(f"Consistency failure: idx_to_class.json has {len(idx_to_class)} entries, expected {num_expected}")
    for idx, name in enumerate(class_names):
        s_idx = str(idx)
        if s_idx not in idx_to_class:
            raise ValueError(f"Consistency failure: index {s_idx} missing from idx_to_class.json")
        if idx_to_class[s_idx] != name:
            raise ValueError(f"Consistency failure: idx_to_class[{s_idx}]='{idx_to_class[s_idx]}' != expected '{name}'")

    # 3. Verify crop_hierarchy.json
    crops_list = crop_hierarchy.get("crops", [])
    if len(crops_list) != 33:
        raise ValueError(f"Consistency failure: crop_hierarchy must contain exactly 33 crops (v1 release), found {len(crops_list)}")

    class_to_crop = crop_hierarchy.get("class_idx_to_crop_idx", [])
    if len(class_to_crop) != num_expected:
        raise ValueError(f"Consistency failure: class_idx_to_crop_idx has {len(class_to_crop)} mappings, expected {num_expected}")
    for i, c_idx in enumerate(class_to_crop):
        if not (0 <= c_idx < len(crops_list)):
            raise ValueError(f"Consistency failure: class_idx_to_crop_idx[{i}]={c_idx} out of range [0, {len(crops_list) - 1}]")

    # Check partition completeness in crop_to_class_indices
    crop_to_class = crop_hierarchy.get("crop_to_class_indices", {})
    all_assigned = []
    for c_name in crops_list:
        if c_name not in crop_to_class:
            raise ValueError(f"Consistency failure: crop '{c_name}' missing from crop_to_class_indices")
        all_assigned.extend(crop_to_class[c_name])

    if len(all_assigned) != num_expected or set(all_assigned) != set(range(num_expected)):
        missing = set(range(num_expected)) - set(all_assigned)
        dupes = len(all_assigned) - len(set(all_assigned))
        raise ValueError(f"Consistency failure in crop_to_class_indices: missing={missing}, duplicate_count={dupes}")

    logger.info("One-time consistency check PASSED across class_names, class_to_idx, idx_to_class, and crop_hierarchy.")


def load_model_bundle(
    version: str = "v1",
    device: str = "cuda" if torch.cuda.is_available() else "cpu",
    verify_integrity: bool = True,
) -> ModelBundle:
    """
    Loads and validates a complete, versioned model bundle from models/<version>/.
    
    Args:
        version: Model version folder name (default: "v1")
        device: Target torch device ("cuda" or "cpu")
        verify_integrity: If True, validates SHA-256 checksums, class consistency, and crop hierarchy.
        
    Returns:
        ModelBundle populated with model, mappings, calibration parameters, and precomputed mask.
        
    Raises:
        FileNotFoundError, ValueError, AssertionError if validation fails.
    """
    bundle_dir = PROJECT_ROOT / "models" / version
    if not bundle_dir.exists():
        raise FileNotFoundError(f"Model bundle directory not found at: {bundle_dir}")

    if verify_integrity:
        verify_checksums(bundle_dir)

    # 1. Load and validate class names
    class_names_path = bundle_dir / "class_names.json"
    class_names = json.loads(class_names_path.read_text(encoding="utf-8"))

    # 2. Load crop hierarchy
    hierarchy_path = bundle_dir / "crop_hierarchy.json"
    crop_hierarchy = json.loads(hierarchy_path.read_text(encoding="utf-8"))
    crops_list = crop_hierarchy.get("crops", [])

    # 3. Perform comprehensive cross-file consistency check
    if verify_integrity:
        verify_class_and_hierarchy_consistency(bundle_dir, class_names, crop_hierarchy)

    # 4. Load calibration and preprocessing metadata
    calib_path = bundle_dir / "calibration.json"
    if not calib_path.exists():
        raise FileNotFoundError(f"Missing required calibration.json in {bundle_dir}")
    calibration = json.loads(calib_path.read_text(encoding="utf-8"))

    preprocess_path = bundle_dir / "preprocess.json"
    if not preprocess_path.exists():
        raise FileNotFoundError(f"Missing required preprocess.json in {bundle_dir}")
    preprocess = json.loads(preprocess_path.read_text(encoding="utf-8"))

    # 4. Build membership matrix for vectorized soft gating (num_crops x num_classes)
    num_crops = len(crops_list)
    num_classes = len(class_names)
    M = torch.full((num_crops, num_classes), float("-inf"), device=device)
    for c_idx, c_name in enumerate(crops_list):
        idx = crop_hierarchy["crop_to_class_indices"].get(c_name, [])
        M[c_idx, idx] = 0.0

    # 5. Build and load model weights
    weights_path = bundle_dir / "model_dualhead_convnext_tiny.pth"
    state_dict = torch.load(weights_path, map_location=device, weights_only=True)
    if "model_state" in state_dict:
        state_dict = state_dict["model_state"]

    # Assert tensor shapes against metadata before instantiation and loading
    c_weight = state_dict.get("crop_head.4.weight", state_dict.get("crop_head.weight"))
    d_weight = state_dict.get("disease_head.4.weight", state_dict.get("disease_head.weight"))
    if c_weight is None or d_weight is None:
        raise KeyError(f"Corrupt weights checkpoint in {weights_path}: missing crop_head or disease_head.")

    assert c_weight.shape[0] == num_crops, (
        f"Tensor shape mismatch: weights crop_head has {c_weight.shape[0]} outputs, "
        f"but crop_hierarchy.json specifies {num_crops} crops"
    )
    assert d_weight.shape[0] == num_classes, (
        f"Tensor shape mismatch: weights disease_head has {d_weight.shape[0]} outputs, "
        f"but class_names.json specifies {num_classes} classes"
    )

    model = build_dualhead_convnext_tiny(
        num_crops=num_crops,
        num_classes=num_classes,
        pretrained=False,
    )
    model.load_state_dict(state_dict, strict=True)
    model.to(device)
    model.eval()

    logger.info("Successfully loaded verified model bundle '%s' on %s", version, device)

    return ModelBundle(
        version=version,
        model=model,
        class_names=class_names,
        crop_hierarchy=crop_hierarchy,
        calibration=calibration,
        preprocess=preprocess,
        device=device,
        membership_matrix=M,
    )
