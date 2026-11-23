"""
tests/test_audit_hardening.py — Regression and invariant tests covering all audit findings.

Covers:
  1. Schema/docs vs bundle count parity (177 classes, 33 crops).
  2. Documentation numbers strictly equal reports/v1/results.json.
  3. Corrupt bytes upload returns HTTP 422.
  4. Images > 50 MP return HTTP 422.
  5. Invalid crop constraint returns HTTP 422.
  6. Bundle tensor-shape assertions prevent mismatched weights.
  7. Crop-partition completeness across all classes.
  8. EXIF orientations 1-8 transpose correctly.
  9. DualHead forward pass output shapes match bundle specification.
  10. Soft-gating zero-sum fallback handles constrained subsets correctly.
  11. Temperature scaling extreme values (T -> 0, T -> inf) remain bounded and valid.
"""

import io
import json
from pathlib import Path
import pytest
from PIL import Image
import torch
from fastapi import HTTPException

import config
from src.data.preprocess import load_image
from src.models.bundle_loader import load_model_bundle, verify_class_and_hierarchy_consistency
from src.models.convnext import build_dualhead_convnext_tiny
from src.models.predict import predict_tensor
from serving.routes.predict import predict_disease


class MockUploadFile:
    def __init__(self, filename: str, content_type: str, data: bytes):
        self.filename = filename
        self.content_type = content_type
        self.data = data
        self.file = io.BytesIO(data)

    def read(self):
        return self.data


HAS_WEIGHTS = (config.MODELS_DIR / "v1" / "model_dualhead_convnext_tiny.pth").exists()


@pytest.fixture(scope="module")
def bundle():
    if not HAS_WEIGHTS:
        pytest.skip("Requires models/v1/*.pth")
    return load_model_bundle("v1", device="cpu")


def test_schema_and_docs_bundle_count_parity(bundle):
    """Verify that class and crop counts strictly match across all bundle components."""
    assert len(bundle.class_names) == 177
    assert len(bundle.crop_hierarchy["crops"]) == 33
    assert bundle.crop_hierarchy["num_classes"] == 177
    assert bundle.crop_hierarchy["num_crops"] == 33
    assert bundle.model.crop_head[4].out_features == 33
    assert bundle.model.disease_head[4].out_features == 177


def test_docs_numbers_equal_results_json():
    """Verify that key metrics in documentation strictly match reports/v1/results.json."""
    results_path = config.REPORTS_DIR / "v1" / "results.json"
    assert results_path.exists(), "results.json must exist"
    with open(results_path, "r", encoding="utf-8") as f:
        results = json.load(f)

    metrics = results["headline_metrics"]
    # Core headline numbers
    assert metrics["clean_test_N"] == 9279
    assert metrics["num_classes"] == 177
    assert metrics["num_crops"] == 33
    assert metrics["soft_gated_disease_accuracy"] == 96.02
    assert metrics["crop_accuracy"] == 99.28
    assert metrics["macro_f1_classes_ge_10_test"] == 96.54
    assert metrics["calibrated_ece_15_bins_pct"] == 0.57

    # Check that README.md and model_card.md cite 96.02% / about 96.0% and 9,279
    readme_text = (config.PROJECT_ROOT / "README.md").read_text(encoding="utf-8")
    model_card_text = (config.MODELS_DIR / "v1" / "model_card.md").read_text(encoding="utf-8")
    dataset_card_text = (config.DOCS_DIR / "DATASET_CARD.md").read_text(encoding="utf-8")

    assert "96.02%" in readme_text
    assert "9,279" in readme_text
    assert "177" in readme_text
    assert "33" in readme_text
    assert "8,910" in readme_text

    assert "96.02%" in model_card_text
    assert "9,279" in model_card_text
    assert "8,910" in model_card_text

    assert "96.02%" in dataset_card_text
    assert "9,279" in dataset_card_text
    assert "8,910" in dataset_card_text


def test_docs_numbers_equal_lineage_and_twin_check():
    """Verify that data lineage and twin audit numbers in docs match JSON artifacts."""
    lineage_path = config.REPORTS_DIR / "v1" / "lineage.json"
    twin_path = config.REPORTS_DIR / "v1" / "twin_check.json"
    assert lineage_path.exists(), "lineage.json must exist"
    assert twin_path.exists(), "twin_check.json must exist"

    with open(lineage_path, "r", encoding="utf-8") as f:
        lineage = json.load(f)

    with open(twin_path, "r", encoding="utf-8") as f:
        twin = json.load(f)

    # Lineage assertions
    assert lineage["stages"]["S1"]["total_images"] == 92165
    assert lineage["stages"]["S1"]["split_counts"]["train"] == 73356
    assert lineage["stages"]["S1"]["split_counts"]["val"] == 9349
    assert lineage["stages"]["S1"]["split_counts"]["test"] == 9460
    assert lineage["stages"]["S4"]["total_images"] == 91984
    assert lineage["stages"]["S4"]["split_counts"]["test"] == 9279
    assert lineage["removed_after_training"]["test"] == 181
    assert lineage["removed_after_training"]["train"] == 0
    assert lineage["removed_after_training"]["val"] == 0
    assert lineage["weights_trained_on_release_snapshot"] is False

    # Twin check assertions
    assert twin["exact_sha256_duplicates"]["total_duplicate_sets"] == 0
    pairs = twin["phash_hamming_le4"]["by_split_pair"]
    assert pairs["train_vs_val"]["total"] == 260
    assert pairs["train_vs_val"]["d0"] == 145
    assert pairs["train_vs_val"]["d1_4"] == 115
    assert pairs.get("train_vs_test", {}).get("total", 0) == 0
    assert pairs.get("val_vs_test", {}).get("total", 0) == 0

    # Verify docs cite real twin counts and split counts
    model_card_text = (config.MODELS_DIR / "v1" / "model_card.md").read_text(encoding="utf-8")
    dataset_card_text = (config.DOCS_DIR / "DATASET_CARD.md").read_text(encoding="utf-8")
    readme_text = (config.PROJECT_ROOT / "README.md").read_text(encoding="utf-8")

    for doc in (model_card_text, dataset_card_text, readme_text):
        assert "91,984" in doc
        assert "73,356" in doc
        assert "9,349" in doc
        assert "9,279" in doc
        assert "181" in doc
        assert "260" in doc
        assert "162" in doc


def test_corrupt_bytes_upload_returns_422():
    """Verify that corrupt or truncated payloads return HTTP 422."""
    corrupt_payloads = [
        b"NOT_A_VALID_JPEG_HEADER",
        b"\xff\xd8\xff\xe0" + b"\x00" * 32,  # Truncated JPEG header
        b"GIF89a" + b"\x00" * 16,            # Fake GIF header with bad payload
    ]
    for data in corrupt_payloads:
        upload = MockUploadFile(filename="test.jpg", content_type="image/jpeg", data=data)
        with pytest.raises(HTTPException) as exc_info:
            predict_disease(file=upload)
        assert exc_info.value.status_code == 422
        assert exc_info.value.detail == "Invalid or unprocessable image payload."


def test_images_resolution_limits_40mp_200_and_60mp_422():
    """Verify that a 40 MP image returns 200 (under 50 MP cap) and a 60 MP image returns 422."""
    # 1. Test 40 MP image (8000 x 5000 = 40,000,000 pixels) -> returns 200
    img_40mp = Image.new("RGB", (8000, 5000), color="green")
    buf_40mp = io.BytesIO()
    img_40mp.save(buf_40mp, format="JPEG", quality=10)
    data_40mp = buf_40mp.getvalue()

    # Offline loading succeeds with max_pixels=50_000_000
    img_40mp_loaded = load_image(data_40mp, max_pixels=50_000_000)
    assert img_40mp_loaded.size == (8000, 5000)

    # API returns 200 (PredictionResponse) when model weights available
    upload_40mp = MockUploadFile(filename="test_40mp.jpg", content_type="image/jpeg", data=data_40mp)
    if HAS_WEIGHTS:
        resp_40mp = predict_disease(file=upload_40mp)
        assert resp_40mp.success is True
        assert resp_40mp.top_prediction is not None

    # 2. Test 60 MP image (8000 x 7500 = 60,000,000 pixels) -> returns 422
    img_60mp = Image.new("RGB", (8000, 7500), color="green")
    buf_60mp = io.BytesIO()
    img_60mp.save(buf_60mp, format="JPEG", quality=10)
    data_60mp = buf_60mp.getvalue()

    # Offline loading succeeds without resolution ceiling
    img_offline = load_image(data_60mp)
    assert img_offline.size == (8000, 7500)

    # Offline loading with explicit max_pixels limit raises ValueError
    with pytest.raises(ValueError, match="exceeds maximum allowed limit"):
        load_image(data_60mp, max_pixels=50_000_000)

    # API rejects at header probe with 422 and helpful error message
    upload_60mp = MockUploadFile(filename="large_res.jpg", content_type="image/jpeg", data=data_60mp)
    with pytest.raises(HTTPException) as exc_info:
        predict_disease(file=upload_60mp)
    assert exc_info.value.status_code == 422
    assert "exceeds maximum allowed limit of 50 MP (50,000,000 pixels)" in exc_info.value.detail
    assert "Please downscale or resize your image below 50 MP before uploading" in exc_info.value.detail


@pytest.mark.skipif(not HAS_WEIGHTS, reason="Requires models/v1/*.pth")
def test_invalid_crop_constraint_returns_422():
    """Verify that unknown or malformed crop names return HTTP 422."""
    img = Image.new("RGB", (256, 256), color="green")
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    data = buf.getvalue()

    invalid_crops = ["Pineapple", "Wheat_Field", "   ", "123Crop"]
    for c in invalid_crops:
        upload = MockUploadFile(filename="leaf.jpg", content_type="image/jpeg", data=data)
        with pytest.raises(HTTPException) as exc_info:
            predict_disease(file=upload, crop=c)
        assert exc_info.value.status_code == 422

    # An empty string crop="" triggers unconstrained auto-detection mode (HTTP 200)
    upload_empty = MockUploadFile(filename="leaf.jpg", content_type="image/jpeg", data=data)
    res_empty = predict_disease(file=upload_empty, crop="")
    assert res_empty.success is True


@pytest.mark.skipif(not HAS_WEIGHTS, reason="Requires models/v1/*.pth")
def test_bundle_tensor_shape_assertion():
    """Verify that bundle loader enforces tensor shape consistency against class_names."""
    bundle_dir = config.MODELS_DIR / "v1"
    class_names = json.loads((bundle_dir / "class_names.json").read_text(encoding="utf-8"))
    crop_hierarchy = json.loads((bundle_dir / "crop_hierarchy.json").read_text(encoding="utf-8"))

    # Valid check passes
    verify_class_and_hierarchy_consistency(bundle_dir, class_names, crop_hierarchy)

    # Inconsistent class list raises ValueError
    with pytest.raises(ValueError, match="Consistency failure"):
        verify_class_and_hierarchy_consistency(bundle_dir, class_names[:-1], crop_hierarchy)


def test_crop_partition_completeness(bundle):
    """Verify that every disease class is strictly partitioned into exactly one crop."""
    num_classes = len(bundle.class_names)
    crop_to_class = bundle.crop_hierarchy["crop_to_class_indices"]
    class_to_crop = bundle.crop_hierarchy["class_idx_to_crop_idx"]

    # 1. Total indices covered by crop map equals num_classes
    all_mapped_indices = []
    for c_name, indices in crop_to_class.items():
        assert len(indices) > 0, f"Crop {c_name} has no associated disease classes"
        all_mapped_indices.extend(indices)

    assert len(all_mapped_indices) == num_classes
    assert set(all_mapped_indices) == set(range(num_classes)), "Missing or duplicate class indices in crop_to_class"

    # 2. class_idx_to_crop_idx maps each class to valid crop index
    assert len(class_to_crop) == num_classes
    assert all(0 <= idx < len(bundle.crop_hierarchy["crops"]) for idx in class_to_crop)


def test_exif_orientations_1_to_8_transpose():
    """Verify that load_image correctly handles all 8 EXIF orientation tags."""
    for orientation in range(1, 9):
        img = Image.new("RGB", (30, 40), color="blue")
        exif = img.getexif()
        exif[274] = orientation  # Tag 274: Orientation
        buf = io.BytesIO()
        img.save(buf, format="JPEG", exif=exif)

        loaded = load_image(buf.getvalue())
        assert isinstance(loaded, Image.Image)
        if orientation in (1, 2, 3, 4):
            assert loaded.size == (30, 40)
        else:
            assert loaded.size == (40, 30)


def test_dualhead_forward_output_shape(bundle):
    """Verify that model forward pass produces expected crop and disease logits shapes."""
    dummy_input = torch.zeros(2, 3, 256, 256, device="cpu")
    bundle.model.eval()
    with torch.no_grad():
        c_logits, d_logits = bundle.model(dummy_input)

    assert c_logits.shape == (2, 33)
    assert d_logits.shape == (2, 177)


def test_soft_gating_zero_sum_fallback(bundle):
    """Verify that soft-gating under crop constraint renormalizes to sum to 1.0."""
    dummy_input = torch.zeros(1, 3, 256, 256, device="cpu")
    class_idx_to_crop = torch.tensor(bundle.crop_hierarchy["class_idx_to_crop_idx"], dtype=torch.long)

    # Unconstrained
    out_unconstrained = predict_tensor(
        bundle.model, dummy_input, class_idx_to_crop, bundle.T_crop, bundle.T_disease, crop_constraint=None
    )
    p_unconstrained = out_unconstrained["p_joint"]
    assert torch.all(p_unconstrained >= 0.0)
    assert torch.all(p_unconstrained <= 1.0)

    # Constrained to crop index 0 (Apple)
    out_constrained = predict_tensor(
        bundle.model, dummy_input, class_idx_to_crop, bundle.T_crop, bundle.T_disease, crop_constraint=0
    )
    p_constrained = out_constrained["p_joint"]
    assert torch.all(p_constrained >= 0.0)
    assert abs(float(p_constrained.sum().item()) - 1.0) < 1e-5


def test_temperature_scaling_extreme_values(bundle):
    """Verify that temperature scaling behaves stably at extreme temperatures."""
    dummy_input = torch.zeros(1, 3, 256, 256, device="cpu")
    class_idx_to_crop = torch.tensor(bundle.crop_hierarchy["class_idx_to_crop_idx"], dtype=torch.long)

    # T -> 0 (Sharp, low temperature)
    out_cold = predict_tensor(
        bundle.model, dummy_input, class_idx_to_crop, T_c=0.01, T_d=0.01
    )
    p_cold = out_cold["p_joint"]
    assert not torch.isnan(p_cold).any()
    assert not torch.isinf(p_cold).any()

    # T -> inf (Uniform, high temperature)
    out_hot = predict_tensor(
        bundle.model, dummy_input, class_idx_to_crop, T_c=1000.0, T_d=1000.0
    )
    p_hot = out_hot["p_joint"]
    assert not torch.isnan(p_hot).any()
    assert not torch.isinf(p_hot).any()
    # At very high temperature, probability differences across classes become very small
    p_hot_np = p_hot[0].numpy()
    assert (p_hot_np.max() - p_hot_np.min()) < 0.01


def test_openapi_contains_no_hardcoded_class_or_crop_counts():
    """Verify that the OpenAPI JSON schema contains no hardcoded count strings."""
    from serving.main import app
    openapi_str = json.dumps(app.openapi())
    forbidden_patterns = ["195", "34 crops", "177", "33"]
    found = [p for p in forbidden_patterns if p in openapi_str]
    assert not found, f"OpenAPI JSON contains hardcoded count text: {found}"
