"""
tests/test_parity.py — Strict mathematical parity test between Evaluation and Serving pipelines.

Verifies:
  1. 50 deterministic test images evaluated under both evaluation and serving pipelines
     produce 100% identical predicted labels and calibrated probabilities within 1e-6.
  2. The 5 previously mismatched images from Audit 3.4 now produce identical predictions.
"""

from pathlib import Path
import random
import pytest
import torch
import torch.nn.functional as F

import config
from src.data.preprocess import get_val_transforms, load_image
from src.models.predict import predict_single_image, predict_tensor
from serving.inference import _bundle, predict

HAS_DATA = (config.DATA_DIR / "processed" / "test").exists() and any((config.DATA_DIR / "processed" / "test").glob("**/*.jpg"))
HAS_WEIGHTS = (config.MODELS_DIR / "v1" / "model_dualhead_convnext_tiny.pth").exists()


@pytest.mark.skipif(not HAS_DATA or not HAS_WEIGHTS, reason="Requires data/ and models/v1/*.pth")
def test_eval_vs_serving_parity_50_images():
    """Verify eval pipeline and serving pipeline produce identical outputs within 1e-6."""
    device = _bundle.device
    transform = get_val_transforms()
    class_idx_to_crop = torch.tensor(
        _bundle.crop_hierarchy["class_idx_to_crop_idx"], dtype=torch.long, device=device
    )
    T_c = _bundle.T_crop
    T_d = _bundle.T_disease

    test_dir = config.DATA_DIR / "processed" / "test"
    all_images = sorted(list(test_dir.glob("**/*.jpg")))
    assert len(all_images) >= 50, f"Expected at least 50 test images, found {len(all_images)}"

    random.seed(42)
    sample_images = random.sample(all_images, 50)

    max_prob_diff = 0.0
    mismatched_labels = 0

    for img_path in sample_images:
        # Evaluation code path
        img = load_image(img_path)
        tensor = transform(img).unsqueeze(0).to(device)
        eval_out = predict_tensor(_bundle.model, tensor, class_idx_to_crop, T_c, T_d)
        eval_prob = float(eval_out["p_joint"].max().item())
        eval_pred_idx = int(eval_out["p_joint"].argmax().item())
        eval_class_name = _bundle.class_names[eval_pred_idx]

        # Serving code path
        img_bytes = img_path.read_bytes()
        serv_resp = predict(img_bytes)
        serv_class_name = serv_resp.top_prediction.class_name
        serv_prob = serv_resp.confidence

        if eval_class_name != serv_class_name:
            mismatched_labels += 1

        prob_diff = abs(eval_prob - serv_prob)
        if prob_diff > max_prob_diff:
            max_prob_diff = prob_diff

    assert mismatched_labels == 0, f"Found {mismatched_labels} label mismatches between eval and serving!"
    assert max_prob_diff < 1e-6, f"Max probability difference {max_prob_diff} exceeds 1e-6 threshold!"


@pytest.mark.skipif(not HAS_DATA or not HAS_WEIGHTS, reason="Requires data/ and models/v1/*.pth")
def test_audit_historical_mismatches_resolved():
    """Verify the 5 images identified in Audit 3.4 now match identically."""
    test_dir = config.DATA_DIR / "processed" / "test"
    mismatch_filenames = [
        "img_00043506.jpg",
        "img_00043507.jpg",
        "img_00035755.jpg",
        "img_00003474.jpg",
        "img_00003711.jpg",
    ]

    for fn in mismatch_filenames:
        matches = list(test_dir.glob(f"**/{fn}"))
        if not matches:
            continue
        p = matches[0]

        # Serving call
        serv_resp = predict(p.read_bytes())
        # Internal eval call
        single_res = predict_single_image(_bundle, p)

        assert serv_resp.top_prediction.class_name == single_res["top_prediction"]["class_name"]
        assert abs(serv_resp.confidence - single_res["confidence"]) < 1e-6


@pytest.mark.skipif(not HAS_DATA or not HAS_WEIGHTS, reason="Requires data/ and models/v1/*.pth")
def test_predict_tensor_vs_predict_single_image_20_images():
    """Verify predict_tensor vs predict_single_image on 20 test images on CPU has max abs prob diff < 1e-5."""
    from src.models.bundle_loader import load_model_bundle
    bundle = load_model_bundle("v1", device="cpu")
    transform = get_val_transforms()
    class_idx_to_crop = torch.tensor(
        bundle.crop_hierarchy["class_idx_to_crop_idx"], dtype=torch.long, device="cpu"
    )

    test_dir = config.DATA_DIR / "processed" / "test"
    all_images = sorted(list(test_dir.glob("**/*.jpg")))
    assert len(all_images) >= 20, f"Expected at least 20 test images, found {len(all_images)}"

    random.seed(42)
    sample_images = random.sample(all_images, 20)

    max_prob_diff = 0.0
    for img_path in sample_images:
        img = load_image(img_path)
        tensor = transform(img).unsqueeze(0).to("cpu")

        out_tensor = predict_tensor(
            model=bundle.model,
            tensor=tensor,
            class_idx_to_crop=class_idx_to_crop,
            T_c=bundle.T_crop,
            T_d=bundle.T_disease,
        )
        p_joint = out_tensor["p_joint"][0].detach().cpu().numpy()
        top_tensor_prob = float(p_joint.max())
        pred_class_idx = int(p_joint.argmax())
        pred_class_name = bundle.class_names[pred_class_idx]

        out_single = predict_single_image(bundle, img_path)
        single_conf = out_single["confidence"]
        single_class_name = out_single["top_prediction"]["class_name"]

        assert pred_class_name == single_class_name
        prob_diff = abs(top_tensor_prob - single_conf)
        if prob_diff > max_prob_diff:
            max_prob_diff = prob_diff

    assert max_prob_diff < 1e-5, f"Max probability difference {max_prob_diff} exceeds 1e-5 threshold!"
