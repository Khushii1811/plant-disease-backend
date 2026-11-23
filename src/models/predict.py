"""
src/models/predict.py — Unified single-view prediction pipeline.

Shared between offline evaluation (scripts/evaluate.py) and production serving (serving/inference.py).
Enforces:
  1. Standard deterministic preprocessing via load_image() (EXIF orientation auto-corrected).
  2. Single-view inference (no multi-view TTA distortion).
  3. Calibrated temperature scaling via calibration.json (T_crop, T_disease).
  4. Crop-gated joint probability distribution: P(disease_j) = P(crop_k) * P(disease_j | crop_k).
  5. Calibrated confidence in range [0.0, 1.0].
  6. Configurable confidence threshold (status: "confident" vs "uncertain").
"""

import io
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from PIL import Image

import torch
import torch.nn.functional as F

from src.data.preprocess import get_val_transforms, load_image
from src.models.gradcam import generate_gradcam


CONFIDENCE_THRESHOLD = 0.60
CROP_GUARD_THRESHOLD = 0.15


def predict_tensor(
    model: torch.nn.Module,
    tensor: torch.Tensor,
    class_idx_to_crop: torch.Tensor,
    T_c: float,
    T_d: float,
    crop_constraint: Optional[int] = None,
) -> Dict[str, torch.Tensor]:
    """
    Shared core forward and gating logic for image tensors.

    Parameters:
        model: Evaluated PyTorch DualHeadConvNeXt model.
        tensor: Batch tensor (B, 3, H, W) on device.
        class_idx_to_crop: Mapping tensor (num_classes,) mapping disease class index to crop index.
        T_c: Crop head temperature scalar.
        T_d: Disease head temperature scalar.
        crop_constraint: Optional crop index to strictly filter predictions.

    Returns:
        dict containing 'c_logits', 'd_logits', 'p_crop', 'p_disease', 'p_joint'.
    """
    model.eval()
    with torch.no_grad():
        c_logits, d_logits = model(tensor)

    crop_valid_mass = 1.0
    if crop_constraint is not None:
        valid_mask = (class_idx_to_crop == crop_constraint)

        # Pre-Mask Probability Mass Check: unmasked calibrated disease probabilities
        p_unmasked = F.softmax(d_logits / T_d, dim=-1)
        crop_valid_mass = float(p_unmasked[:, valid_mask].sum().item())

        # Pre-softmax logit masking: mask invalid diseases with -inf before T_d scaling
        d_logits_masked = d_logits.clone()
        d_logits_masked[:, ~valid_mask] = float("-inf")

        # Softmax strictly across valid diseases of the selected crop
        p_disease = F.softmax(d_logits_masked / T_d, dim=-1)

        # Bypass joint crop multiplication (treat crop probability as 1.0)
        p_joint = p_disease

        p_crop = torch.zeros_like(c_logits)
        p_crop[:, crop_constraint] = 1.0
    else:
        # Unconstrained standard pipeline: temperature scaling + joint crop-gating
        p_crop = F.softmax(c_logits / T_c, dim=-1)
        p_disease = F.softmax(d_logits / T_d, dim=-1)
        p_joint = p_crop[:, class_idx_to_crop] * p_disease

    return {
        "c_logits": c_logits,
        "d_logits": d_logits,
        "p_crop": p_crop,
        "p_disease": p_disease,
        "p_joint": p_joint,
        "crop_valid_mass": crop_valid_mass,
    }


def predict_single_image(
    bundle: Any,
    image_input: Union[str, Path, bytes, io.BytesIO, Image.Image],
    crop_constraint_name: Optional[str] = None,
    threshold: float = CONFIDENCE_THRESHOLD,
    top_k_count: int = 4,
    remove_bg: bool = False,
    heatmap: bool = False,
) -> Dict[str, Any]:
    """
    High-level prediction function for a single leaf image.

    Returns strict data payload matching API and evaluation contracts:
    crop, disease, confidence (in [0, 1]), status ("confident" | "uncertain"), top_k.
    """
    t0 = time.perf_counter()

    if isinstance(image_input, Image.Image):
        img = image_input.convert("RGB")
    else:
        img = load_image(image_input)

    processed_image_base64 = None
    if remove_bg:
        from src.data.bg_removal import remove_background
        img, processed_image_base64 = remove_background(img)

    transform = get_val_transforms()
    norm_tensor = transform(img).unsqueeze(0).to(bundle.device)

    class_idx_to_crop = torch.tensor(
        bundle.crop_hierarchy["class_idx_to_crop_idx"],
        dtype=torch.long,
        device=bundle.device,
    )
    crops_list = bundle.crop_hierarchy["crops"]
    crop_constraint_idx = None
    if crop_constraint_name:
        for idx, cname in enumerate(crops_list):
            if cname.lower() == crop_constraint_name.strip().lower():
                crop_constraint_idx = idx
                break

    # Standard Single-View Unified Pipeline
    out = predict_tensor(
        bundle.model, norm_tensor, class_idx_to_crop, bundle.T_crop, bundle.T_disease, crop_constraint_idx
    )
    p_joint = out["p_joint"]
    c_logits = out["c_logits"]

    conf_val, pred_disease_idx = p_joint[0].max(dim=-1)
    confidence = float(conf_val.item())
    pred_disease_idx = int(pred_disease_idx.item())

    # Crop prediction
    if crop_constraint_idx is not None:
        pred_crop_idx = crop_constraint_idx
        pred_crop_name = crops_list[pred_crop_idx]
    else:
        pred_crop_idx = int(c_logits[0].argmax(dim=-1).item())
        pred_crop_name = crops_list[pred_crop_idx]

    pred_class_label = bundle.class_names[pred_disease_idx]
    if " - " in pred_class_label:
        crop_part, disease_part = pred_class_label.split(" - ", 1)
    else:
        crop_part = pred_crop_name
        disease_part = pred_class_label

    # Build Top-K
    top_k_vals, top_k_indices = torch.topk(p_joint[0], k=min(top_k_count, len(bundle.class_names)))
    top_k_list = []
    for k_val, k_idx in zip(top_k_vals, top_k_indices):
        c_idx_int = int(k_idx.item())
        c_label = bundle.class_names[c_idx_int]
        c_crop, c_dis = c_label.split(" - ", 1) if " - " in c_label else (pred_crop_name, c_label)
        top_k_list.append({
            "class_name": c_label,
            "crop": c_crop,
            "disease": c_dis,
            "confidence": float(k_val.item()),
        })

    # Generate Grad-CAM heatmap aligned to original image dimensions (if requested)
    heatmap_base64 = None
    if heatmap:
        heatmap_base64 = generate_gradcam(
            bundle.model,
            norm_tensor,
            pred_disease_idx,
            target_size=img.size,
        )

    crop_valid_mass = out.get("crop_valid_mass", 1.0)
    status_str = "confident" if confidence >= threshold else "uncertain"
    warning_message = None

    p_crop = out["p_crop"]
    p_disease = out["p_disease"]

    if crop_constraint_idx is not None:
        crop_conf = round(float(crop_valid_mass), 4)
        crop_status = "mismatch" if crop_valid_mass < CROP_GUARD_THRESHOLD else "pass"
    else:
        c_pred_idx = int(p_crop[0].argmax(dim=-1).item())
        crop_conf = round(float(p_crop[0, c_pred_idx].item()), 4)
        crop_status = "pass" if crop_conf >= threshold else "uncertain"

    disease_conf = round(float(p_disease[0, pred_disease_idx].item()), 4)
    disease_status = "pass" if (confidence >= threshold or disease_conf >= threshold) else "uncertain"

    # Unsupported Disease Guard for constrained mode
    if crop_constraint_idx is not None and crop_valid_mass < CROP_GUARD_THRESHOLD:
        status_str = "uncertain"
        warning_message = (
            f"Low match for supported {pred_crop_name} diseases ({crop_valid_mass:.1%} prior mass). "
            f"This disease may not be in our {pred_crop_name} database, or the selected crop may not match the leaf."
        )

    failure_attribution = None
    if status_str == "uncertain":
        if crop_status == "mismatch":
            failure_attribution = (
                f"Crop Mismatch: Leaf has low prior match ({crop_valid_mass:.1%}) for {pred_crop_name}. "
                f"The leaf likely belongs to another crop, or this condition is unsupported in our {pred_crop_name} database."
            )
        elif crop_status != "pass" and disease_status != "pass":
            failure_attribution = (
                "Both Host Crop and Disease symptoms are ambiguous. Re-photograph leaf with clearer framing and balanced daylight."
            )
        elif crop_status != "pass":
            failure_attribution = (
                f"Host Crop recognition uncertain ({crop_conf:.1%}). Leaf structure may be obscured or species unsupported."
            )
        elif disease_status != "pass":
            failure_attribution = (
                f"Host Crop verified ({crop_conf:.1%}), but foliar pathology symptoms are ambiguous or low confidence ({confidence:.1%})."
            )

    latency_ms = (time.perf_counter() - t0) * 1000.0

    single_view_entry = {
        "view_index": 0,
        "crop": crop_part,
        "disease": disease_part,
        "confidence": confidence,
        "heatmap_base64": heatmap_base64,
        "processed_image_base64": processed_image_base64,
    }

    return {
        "success": True,
        "status": status_str,
        "threshold_applied": threshold,
        "crop": crop_part,
        "disease": disease_part,
        "confidence": confidence,
        "crop_confidence": crop_conf,
        "disease_confidence": disease_conf,
        "crop_status": crop_status,
        "disease_status": disease_status,
        "failure_attribution": failure_attribution,
        "num_views": 1,
        "consensus_score": "1/1 view",
        "consensus_agreement": 1.0,
        "individual_views": [single_view_entry],
        "crop_valid_mass": round(crop_valid_mass, 4),
        "warning_message": warning_message,
        "top_prediction": top_k_list[0] if top_k_list else None,
        "top_3_alternatives": top_k_list[1:4] if len(top_k_list) > 1 else [],
        "top_k": top_k_list,
        "heatmap_base64": heatmap_base64,
        "processed_image_base64": processed_image_base64,
        "inference_time_ms": round(latency_ms, 2),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def predict_multi_images(
    bundle: Any,
    image_inputs: List[Union[str, Path, bytes, io.BytesIO, Image.Image]],
    crop_constraint_name: Optional[str] = None,
    threshold: float = CONFIDENCE_THRESHOLD,
    top_k_count: int = 4,
    remove_bg: bool = False,
    heatmap: bool = False,
) -> Dict[str, Any]:
    """
    Multi-view consensus prediction pipeline.
    Accepts 1 to 3 images, runs individual forward passes and Grad-CAM,
    and averages the calibrated probability distributions across all views.
    """
    if not image_inputs:
        raise ValueError("At least one image input is required.")

    if len(image_inputs) == 1:
        return predict_single_image(
            bundle=bundle,
            image_input=image_inputs[0],
            crop_constraint_name=crop_constraint_name,
            threshold=threshold,
            top_k_count=top_k_count,
            remove_bg=remove_bg,
            heatmap=heatmap,
        )

    t0 = time.perf_counter()
    num_views = len(image_inputs)

    class_idx_to_crop = torch.tensor(
        bundle.crop_hierarchy["class_idx_to_crop_idx"],
        dtype=torch.long,
        device=bundle.device,
    )
    crops_list = bundle.crop_hierarchy["crops"]
    crop_constraint_idx = None
    if crop_constraint_name:
        for idx, cname in enumerate(crops_list):
            if cname.lower() == crop_constraint_name.strip().lower():
                crop_constraint_idx = idx
                break

    transform = get_val_transforms()

    p_joint_list = []
    c_logits_list = []
    crop_valid_mass_list = []
    p_crop_list = []
    p_disease_list = []
    individual_views = []

    for view_idx, img_input in enumerate(image_inputs):
        if isinstance(img_input, Image.Image):
            img = img_input.convert("RGB")
        else:
            img = load_image(img_input)

        proc_b64 = None
        if remove_bg:
            from src.data.bg_removal import remove_background
            img, proc_b64 = remove_background(img)

        norm_tensor = transform(img).unsqueeze(0).to(bundle.device)

        out = predict_tensor(
            bundle.model, norm_tensor, class_idx_to_crop, bundle.T_crop, bundle.T_disease, crop_constraint_idx
        )
        p_joint_i = out["p_joint"]
        c_logits_i = out["c_logits"]
        p_joint_list.append(p_joint_i)
        c_logits_list.append(c_logits_i)
        p_crop_list.append(out["p_crop"])
        p_disease_list.append(out["p_disease"])
        crop_valid_mass_list.append(out.get("crop_valid_mass", 1.0))

        conf_i, pred_d_idx_i = p_joint_i[0].max(dim=-1)
        pred_d_idx_int = int(pred_d_idx_i.item())

        if crop_constraint_idx is not None:
            c_name_i = crops_list[crop_constraint_idx]
        else:
            c_name_i = crops_list[int(c_logits_i[0].argmax(dim=-1).item())]

        c_label_i = bundle.class_names[pred_d_idx_int]
        if " - " in c_label_i:
            crop_part_i, dis_part_i = c_label_i.split(" - ", 1)
        else:
            crop_part_i, dis_part_i = c_name_i, c_label_i

        cam_b64 = None
        if heatmap:
            cam_b64 = generate_gradcam(
                bundle.model,
                norm_tensor,
                pred_d_idx_int,
                target_size=img.size,
            )

        individual_views.append({
            "view_index": view_idx,
            "crop": crop_part_i,
            "disease": dis_part_i,
            "confidence": round(float(conf_i.item()), 4),
            "heatmap_base64": cam_b64,
            "processed_image_base64": proc_b64,
        })

    # Ensemble Multi-View Averaging across views
    p_joint_avg = torch.stack(p_joint_list, dim=0).mean(dim=0)
    c_logits_avg = torch.stack(c_logits_list, dim=0).mean(dim=0)

    conf_val, pred_disease_idx = p_joint_avg[0].max(dim=-1)
    confidence = float(conf_val.item())
    pred_disease_idx = int(pred_disease_idx.item())

    if crop_constraint_idx is not None:
        pred_crop_name = crops_list[crop_constraint_idx]
    else:
        pred_crop_name = crops_list[int(c_logits_avg[0].argmax(dim=-1).item())]

    pred_class_label = bundle.class_names[pred_disease_idx]
    if " - " in pred_class_label:
        crop_part, disease_part = pred_class_label.split(" - ", 1)
    else:
        crop_part = pred_crop_name
        disease_part = pred_class_label

    # Multi-View Consensus Agreement Calculation
    agree_count = sum(1 for v in individual_views if v["disease"].strip().lower() == disease_part.strip().lower())
    agreement_fraction = agree_count / num_views
    consensus_score = f"{agree_count}/{num_views} views agree"

    # Top-K candidates from averaged probability distribution
    top_k_vals, top_k_indices = torch.topk(p_joint_avg[0], k=min(top_k_count, len(bundle.class_names)))
    top_k_list = []
    for k_val, k_idx in zip(top_k_vals, top_k_indices):
        c_idx_int = int(k_idx.item())
        c_label = bundle.class_names[c_idx_int]
        c_crop, c_dis = c_label.split(" - ", 1) if " - " in c_label else (pred_crop_name, c_label)
        top_k_list.append({
            "class_name": c_label,
            "crop": c_crop,
            "disease": c_dis,
            "confidence": float(k_val.item()),
        })

    avg_crop_valid_mass = sum(crop_valid_mass_list) / num_views
    status_str = "confident" if confidence >= threshold else "uncertain"
    warning_message = None

    p_crop_avg = torch.stack(p_crop_list, dim=0).mean(dim=0)
    p_disease_avg = torch.stack(p_disease_list, dim=0).mean(dim=0)

    if crop_constraint_idx is not None:
        crop_conf = round(float(avg_crop_valid_mass), 4)
        crop_status = "mismatch" if avg_crop_valid_mass < CROP_GUARD_THRESHOLD else "pass"
    else:
        c_pred_idx = int(p_crop_avg[0].argmax(dim=-1).item())
        crop_conf = round(float(p_crop_avg[0, c_pred_idx].item()), 4)
        crop_status = "pass" if crop_conf >= threshold else "uncertain"

    disease_conf = round(float(p_disease_avg[0, pred_disease_idx].item()), 4)
    disease_status = "pass" if (confidence >= threshold or disease_conf >= threshold) else "uncertain"

    if crop_constraint_idx is not None and avg_crop_valid_mass < CROP_GUARD_THRESHOLD:
        status_str = "uncertain"
        warning_message = (
            f"Low match for supported {pred_crop_name} diseases ({avg_crop_valid_mass:.1%} prior mass). "
            f"This disease may not be in our {pred_crop_name} database, or the selected crop may not match the leaf."
        )

    failure_attribution = None
    if status_str == "uncertain":
        if crop_status == "mismatch":
            failure_attribution = (
                f"Crop Mismatch: Leaf views have low prior match ({avg_crop_valid_mass:.1%}) for {pred_crop_name}. "
                f"The leaves likely belong to another crop, or this condition is unsupported in our {pred_crop_name} database."
            )
        elif crop_status != "pass" and disease_status != "pass":
            failure_attribution = (
                "Both Host Crop and Disease symptoms are ambiguous across views. Re-photograph with clearer framing and daylight."
            )
        elif crop_status != "pass":
            failure_attribution = (
                f"Host Crop recognition uncertain across views ({crop_conf:.1%}). Leaf structure may be obscured or species unsupported."
            )
        elif disease_status != "pass":
            failure_attribution = (
                f"Host Crop verified ({crop_conf:.1%}), but foliar pathology symptoms are ambiguous across views ({confidence:.1%})."
            )

    latency_ms = (time.perf_counter() - t0) * 1000.0

    return {
        "success": True,
        "status": status_str,
        "threshold_applied": threshold,
        "crop": crop_part,
        "disease": disease_part,
        "confidence": confidence,
        "crop_confidence": crop_conf,
        "disease_confidence": disease_conf,
        "crop_status": crop_status,
        "disease_status": disease_status,
        "failure_attribution": failure_attribution,
        "num_views": num_views,
        "consensus_score": consensus_score,
        "consensus_agreement": round(agreement_fraction, 4),
        "individual_views": individual_views,
        "crop_valid_mass": round(avg_crop_valid_mass, 4),
        "warning_message": warning_message,
        "top_prediction": top_k_list[0] if top_k_list else None,
        "top_3_alternatives": top_k_list[1:4] if len(top_k_list) > 1 else [],
        "top_k": top_k_list,
        "heatmap_base64": individual_views[0]["heatmap_base64"] if individual_views else None,
        "processed_image_base64": individual_views[0].get("processed_image_base64") if individual_views else None,
        "inference_time_ms": round(latency_ms, 2),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
