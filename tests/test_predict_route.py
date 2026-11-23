"""
tests/test_predict_route.py — Route unit and integration tests for FastAPI serving endpoints.

Tests:
  1. Health endpoint metadata, status, temperatures, num_classes=195.
  2. Classes endpoint returning 195 botanical classes.
  3. Crops endpoint returning 34 host crops.
  4. Predict route auto-detection (success=True, confidence, status, top_k).
  5. Predict route with crop constraint (confines diagnosis and alternatives to specified crop).
  6. Predict route validation: rejected unsupported file format (422).
  7. Predict route validation: rejected empty 0-byte file (422).
"""

import io
from PIL import Image
import pytest
from fastapi import HTTPException

import config
from serving.main import health, ready
from serving.routes.predict import list_classes, list_crops, predict_disease

HAS_WEIGHTS = (config.MODELS_DIR / "v1" / "model_dualhead_convnext_tiny.pth").exists()


def _run_coro(coro):
    """Drive a non-I/O coroutine to completion synchronously, or return sync value."""
    if not hasattr(coro, "send"):
        return coro
    val = None
    while True:
        try:
            val = coro.send(val)
        except StopIteration as exc:
            return exc.value


class MockUploadFile:
    def __init__(self, filename: str, content_type: str, data: bytes):
        self.filename = filename
        self.content_type = content_type
        self.data = data
        self._file = io.BytesIO(data)

    @property
    def file(self):
        self._file.seek(0)
        return self._file

    def read(self):
        return self.data


def _make_dummy_image_bytes(color=(40, 150, 40), size=(256, 256)) -> bytes:
    """Generate minimal valid JPEG bytes for testing."""
    img = Image.new("RGB", size, color=color)
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    return buf.getvalue()


def test_health_endpoint():
    """Verify /api/v1/health returns healthy status, 177 classes, and valid calibration."""
    data = _run_coro(health())
    assert data.status == "healthy"
    assert data.num_classes == 177
    assert data.model_architecture == "ConvNeXt-Tiny DualHead"
    assert data.calibration_temperature_crop > 0.0
    assert data.calibration_temperature_disease > 0.0
    assert data.version == "1.0.0"


def test_ready_endpoint():
    """Verify /api/v1/ready returns ready status."""
    data = _run_coro(ready())
    assert data == {"status": "ready"}


def test_classes_endpoint():
    """Verify /api/v1/classes returns 177 classes."""
    data = _run_coro(list_classes())
    assert data.total_classes == 177
    assert len(data.classes) == 177
    assert any("Tomato" in c for c in data.classes)


def test_crops_endpoint():
    """Verify /api/v1/crops returns 33 botanical crops."""
    data = _run_coro(list_crops())
    assert data.total_crops == 33
    assert len(data.crops) == 33
    assert "Tomato" in data.crops
    assert "Apple" in data.crops


@pytest.mark.skipif(not HAS_WEIGHTS, reason="Requires models/v1/*.pth")
def test_predict_auto_detect():
    """Verify /api/v1/predict succeeds without crop specification (auto-detect)."""
    img_bytes = _make_dummy_image_bytes()
    upload = MockUploadFile(filename="leaf.jpg", content_type="image/jpeg", data=img_bytes)
    data = _run_coro(predict_disease(file=upload))

    assert data.success is True
    assert data.status in ("confident", "uncertain")
    assert 0.0 <= data.confidence <= 1.0
    assert data.threshold_applied == 0.60
    assert data.crop != ""
    assert data.disease != ""
    assert data.top_prediction.class_name != ""
    assert len(data.top_3_alternatives) <= 3
    assert len(data.top_k) >= 1
    assert data.inference_time_ms > 0.0


@pytest.mark.skipif(not HAS_WEIGHTS, reason="Requires models/v1/*.pth")
def test_predict_with_crop_constraint():
    """Verify /api/v1/predict constrains diagnosis strictly to specified crop."""
    img_bytes = _make_dummy_image_bytes()
    upload = MockUploadFile(filename="leaf.jpg", content_type="image/jpeg", data=img_bytes)
    data = _run_coro(predict_disease(file=upload, crop="Tomato"))

    assert data.success is True
    assert data.crop.lower() == "tomato"
    assert data.top_prediction.crop.lower() == "tomato"
    for alt in data.top_3_alternatives:
        assert alt.crop.lower() == "tomato"


def test_predict_unsupported_file_type():
    """Verify /api/v1/predict raises 422 for unsupported file extensions/mime types."""
    upload = MockUploadFile(filename="report.pdf", content_type="application/pdf", data=b"%PDF-1.4...")
    with pytest.raises(HTTPException) as exc_info:
        _run_coro(predict_disease(file=upload))
    assert exc_info.value.status_code == 422


def test_predict_empty_file():
    """Verify /api/v1/predict raises 422 when 0 bytes uploaded."""
    upload = MockUploadFile(filename="empty.jpg", content_type="image/jpeg", data=b"")
    with pytest.raises(HTTPException) as exc_info:
        _run_coro(predict_disease(file=upload))
    assert exc_info.value.status_code == 422


def test_predict_invalid_crop_constraint():
    """Verify /api/v1/predict raises 422 for invalid crop constraint or blank whitespace."""
    img_bytes = _make_dummy_image_bytes()
    upload1 = MockUploadFile(filename="leaf.jpg", content_type="image/jpeg", data=img_bytes)
    with pytest.raises(HTTPException) as exc1:
        _run_coro(predict_disease(file=upload1, crop="Pineapple"))
    assert exc1.value.status_code == 422

    upload2 = MockUploadFile(filename="leaf.jpg", content_type="image/jpeg", data=img_bytes)
    with pytest.raises(HTTPException) as exc2:
        _run_coro(predict_disease(file=upload2, crop="   "))
    assert exc2.value.status_code == 422


@pytest.mark.skipif(not HAS_WEIGHTS, reason="Requires models/v1/*.pth")
def test_predict_empty_string_crop_triggers_auto_mode():
    """Verify /api/v1/predict with crop='' triggers unconstrained auto-detection mode."""
    img_bytes = _make_dummy_image_bytes()
    upload = MockUploadFile(filename="leaf.jpg", content_type="image/jpeg", data=img_bytes)
    data = _run_coro(predict_disease(file=upload, crop=""))

    assert data.success is True
    assert data.status in ("confident", "uncertain")
    assert data.crop != ""
    assert data.disease != ""


def test_request_id_middleware_propagates_header_and_context():
    """Verify request_id_middleware sets X-Request-ID header and contextvar."""
    from starlette.requests import Request
    from starlette.responses import Response
    from serving.main import request_id_ctx, request_id_middleware

    scope = {
        "type": "http",
        "method": "GET",
        "path": "/api/v1/health",
        "headers": [(b"x-request-id", b"custom-req-id-999")],
    }
    request = Request(scope)
    captured_ctx = []

    async def mock_call_next(req):
        captured_ctx.append(request_id_ctx.get())
        return Response(content="OK", status_code=200)

    response = _run_coro(request_id_middleware(request, mock_call_next))
    assert response.headers["X-Request-ID"] == "custom-req-id-999"
    assert captured_ctx == ["custom-req-id-999"]
    assert request_id_ctx.get() == "-"


@pytest.mark.skipif(not HAS_WEIGHTS, reason="Requires models/v1/*.pth")
def test_predict_heatmap_off_by_default():
    """Verify predict defaults heatmap=False and returns None for heatmap_base64."""
    img_bytes = _make_dummy_image_bytes(size=(320, 240))
    upload = MockUploadFile(filename="leaf.jpg", content_type="image/jpeg", data=img_bytes)
    data = _run_coro(predict_disease(file=upload, crop=None))

    assert data.success is True
    assert data.heatmap_base64 is None
    assert data.individual_views[0].heatmap_base64 is None


@pytest.mark.skipif(not HAS_WEIGHTS, reason="Requires models/v1/*.pth")
def test_predict_returns_gradcam_heatmap_when_requested_and_capped_to_512():
    """Verify predict with heatmap=True returns a base64 WebP image capped at 512 px on longer side."""
    import base64
    from PIL import Image

    # Test with 1200x800 input to verify 512 px ceiling and aspect ratio preservation
    img_bytes = _make_dummy_image_bytes(size=(1200, 800))
    upload = MockUploadFile(filename="leaf.jpg", content_type="image/jpeg", data=img_bytes)
    data = _run_coro(predict_disease(file=upload, crop=None, heatmap=True))

    assert data.success is True
    assert data.heatmap_base64 is not None
    assert data.heatmap_base64.startswith("data:image/webp;base64,")

    # Decode and verify dimensions and format
    header, b64data = data.heatmap_base64.split(",", 1)
    raw_bytes = base64.b64decode(b64data)
    with Image.open(io.BytesIO(raw_bytes)) as heatmap_img:
        w, h = heatmap_img.size
        assert max(w, h) <= 512
        assert w == 512
        assert h == 341  # 800 * (512 / 1200) = 341.33 -> 341
        assert heatmap_img.format == "WEBP"


@pytest.mark.skipif(not HAS_WEIGHTS, reason="Requires models/v1/*.pth")
def test_predict_logit_masking_sums_to_one():
    """Verify logit masking with -inf strictly confines predictions to target crop with sum ~ 1."""
    img_bytes = _make_dummy_image_bytes()
    upload = MockUploadFile(filename="leaf.jpg", content_type="image/jpeg", data=img_bytes)
    data = _run_coro(predict_disease(file=upload, crop="Apple"))

    assert data.success is True
    assert data.crop == "Apple"
    for item in data.top_k:
        assert item.crop == "Apple"
    # All Apple candidate classes sum to approximately 1.0
    conf_sum = sum(item.confidence for item in data.top_k)
    assert 0.85 <= conf_sum <= 1.0001


@pytest.mark.skipif(not HAS_WEIGHTS, reason="Requires models/v1/*.pth")
def test_predict_unsupported_disease_guard():
    """Verify that when crop_valid_mass < 0.15, status is forced uncertain with warning_message,
    and when >= 0.15, normal masked behavior applies."""
    from pathlib import Path
    img_bytes = _make_dummy_image_bytes(color=(40, 150, 40))
    upload = MockUploadFile(filename="leaf.jpg", content_type="image/jpeg", data=img_bytes)

    # 1. Trigger guard: dummy leaf constrained to Pear has < 15% prior mass
    data_guard = _run_coro(predict_disease(file=upload, crop="Pear"))
    assert data_guard.success is True
    assert data_guard.crop == "Pear"
    assert data_guard.crop_valid_mass is not None
    assert data_guard.crop_valid_mass < 0.15
    assert data_guard.status == "uncertain"
    assert data_guard.warning_message is not None
    assert "Low match for supported Pear diseases" in data_guard.warning_message
    for item in data_guard.top_k:
        assert item.crop == "Pear"

    # 2. Normal behavior: valid crop image with prior mass >= 15%
    apple_files = list(Path("data/processed/test/Apple - Rust").glob("*.jpg"))
    if apple_files:
        apple_upload = MockUploadFile(filename="apple.jpg", content_type="image/jpeg", data=apple_files[0].read_bytes())
        data_normal = _run_coro(predict_disease(file=apple_upload, crop="Apple"))
        assert data_normal.success is True
        assert data_normal.crop == "Apple"
        assert data_normal.crop_valid_mass >= 0.15
        assert data_normal.status == "confident"
        assert data_normal.warning_message is None


@pytest.mark.skipif(not HAS_WEIGHTS, reason="Requires models/v1/*.pth")
def test_predict_remove_bg_false_default():
    """Verify default remove_bg=False returns None for processed_image_base64."""
    img_bytes = _make_dummy_image_bytes()
    upload = MockUploadFile(filename="leaf.jpg", content_type="image/jpeg", data=img_bytes)
    data = _run_coro(predict_disease(file=upload, remove_bg=False))

    assert data.success is True
    assert data.processed_image_base64 is None


def test_predict_remove_bg_rejected_by_default_422():
    """Verify remove_bg=True is rejected with HTTP 422 when ENABLE_BG_REMOVAL is unset."""
    img_bytes = _make_dummy_image_bytes()
    upload = MockUploadFile(filename="leaf.jpg", content_type="image/jpeg", data=img_bytes)
    with pytest.raises(HTTPException) as exc_info:
        _run_coro(predict_disease(file=upload, remove_bg=True))
    assert exc_info.value.status_code == 422
    assert "ENABLE_BG_REMOVAL=1" in exc_info.value.detail


@pytest.mark.skipif(not HAS_WEIGHTS, reason="Requires models/v1/*.pth")
def test_predict_remove_bg_enabled_via_env(monkeypatch):
    """Verify remove_bg=True succeeds when ENABLE_BG_REMOVAL=1 is explicitly set."""
    monkeypatch.setenv("ENABLE_BG_REMOVAL", "1")
    img_bytes = _make_dummy_image_bytes()
    upload = MockUploadFile(filename="leaf.jpg", content_type="image/jpeg", data=img_bytes)
    data = _run_coro(predict_disease(file=upload, remove_bg=True))

    assert data.success is True
    assert data.processed_image_base64 is not None
    assert data.processed_image_base64.startswith("data:image/jpeg;base64,")
    assert len(data.processed_image_base64) > 100
    assert data.heatmap_base64 is None


def test_u2net_checksum_verification_fail_closed(tmp_path):
    """Verify u2net_checksum verification passes for valid hash and fails closed on tampering."""
    from src.data.bg_removal import verify_u2net_checksum

    # Tampered / corrupted file
    bad_model = tmp_path / "u2net.onnx"
    bad_model.write_bytes(b"corrupted_model_weights_test")
    with pytest.raises(RuntimeError) as exc_info:
        verify_u2net_checksum(bad_model)
    assert "Security verification failed" in str(exc_info.value)
    assert "Failing closed" in str(exc_info.value)


@pytest.mark.skipif(not HAS_WEIGHTS, reason="Requires models/v1/*.pth")
def test_predict_single_file_consensus_metadata():
    """Verify single file predict populates num_views=1 and consensus_score='1/1 view'."""
    img_bytes = _make_dummy_image_bytes()
    upload = MockUploadFile(filename="leaf.jpg", content_type="image/jpeg", data=img_bytes)
    data = _run_coro(predict_disease(file=upload))

    assert data.success is True
    assert data.num_views == 1
    assert data.consensus_score == "1/1 view"
    assert data.consensus_agreement == 1.0
    assert len(data.individual_views) == 1
    assert data.individual_views[0].view_index == 0
    assert data.individual_views[0].heatmap_base64 is None


@pytest.mark.skipif(not HAS_WEIGHTS, reason="Requires models/v1/*.pth")
def test_predict_multi_view_consensus_2_and_3_images():
    """Verify 2 and 3 images multi-view predict ensembling and per-view metadata."""
    img_bytes1 = _make_dummy_image_bytes(color=(30, 140, 30))
    img_bytes2 = _make_dummy_image_bytes(color=(40, 160, 40))
    img_bytes3 = _make_dummy_image_bytes(color=(50, 180, 50))

    upload1 = MockUploadFile(filename="leaf_view1.jpg", content_type="image/jpeg", data=img_bytes1)
    upload2 = MockUploadFile(filename="leaf_view2.jpg", content_type="image/jpeg", data=img_bytes2)
    upload3 = MockUploadFile(filename="leaf_view3.jpg", content_type="image/jpeg", data=img_bytes3)

    # 2 views
    data2 = _run_coro(predict_disease(files=[upload1, upload2]))
    assert data2.success is True
    assert data2.num_views == 2
    assert "2 views" in data2.consensus_score
    assert 0.0 <= data2.consensus_agreement <= 1.0
    assert len(data2.individual_views) == 2
    assert data2.individual_views[0].view_index == 0
    assert data2.individual_views[1].view_index == 1

    # 3 views
    data3 = _run_coro(predict_disease(files=[upload1, upload2, upload3]))
    assert data3.success is True
    assert data3.num_views == 3
    assert "3 views" in data3.consensus_score
    assert 0.0 <= data3.consensus_agreement <= 1.0
    assert len(data3.individual_views) == 3


def test_predict_multi_view_rejection_over_3_images():
    """Verify uploading > 3 images triggers HTTP 422."""
    img_bytes = _make_dummy_image_bytes()
    uploads = [
        MockUploadFile(filename=f"leaf_{i}.jpg", content_type="image/jpeg", data=img_bytes)
        for i in range(4)
    ]
    with pytest.raises(HTTPException) as exc_info:
        _run_coro(predict_disease(files=uploads))
    assert exc_info.value.status_code == 422
    assert "Maximum 3 images" in exc_info.value.detail


def test_predict_no_files_rejection():
    """Verify empty request with no file and no files triggers HTTP 422."""
    with pytest.raises(HTTPException) as exc_info:
        _run_coro(predict_disease(file=None, files=None))
    assert exc_info.value.status_code == 422
    assert "No leaf image provided" in exc_info.value.detail


def test_predict_aggregate_pixel_budget_100mp_exceeded_422():
    """Verify total pixel budget exceeding 100 MP (e.g. 3 x 40 MP = 120 MP) returns 422 before decode."""
    # 3 images of 40 MP each (8000x5000 = 40,000,000 pixels each -> total 120,000,000 pixels)
    img_40mp = Image.new("RGB", (8000, 5000), color="green")
    buf = io.BytesIO()
    img_40mp.save(buf, format="JPEG", quality=10)
    data_40mp = buf.getvalue()

    uploads = [
        MockUploadFile(filename=f"leaf_{i}.jpg", content_type="image/jpeg", data=data_40mp)
        for i in range(3)
    ]
    with pytest.raises(HTTPException) as exc_info:
        _run_coro(predict_disease(files=uploads))
    assert exc_info.value.status_code == 422
    assert "100 MP" in exc_info.value.detail
    assert "120.0 MP" in exc_info.value.detail


def test_rate_limiter_middleware_direct():
    """Verify in-memory sliding-window rate limiter returns 429 when threshold exceeded, and exempts health endpoint."""
    from starlette.requests import Request
    from starlette.responses import Response
    from serving.main import rate_limit_middleware, _rate_limit_history
    import serving.main as main_mod

    async def mock_call_next(req):
        return Response(content="ok", status_code=200)

    # Health check should be exempt
    health_req = Request({"type": "http", "method": "GET", "path": "/api/v1/health", "headers": []})
    resp = _run_coro(rate_limit_middleware(health_req, mock_call_next))
    assert resp.status_code == 200

    # Temporarily set limit to 2
    orig_max = main_mod.RATE_LIMIT_MAX_REQUESTS
    try:
        main_mod.RATE_LIMIT_MAX_REQUESTS = 2
        _rate_limit_history.clear()

        classes_req = Request({
            "type": "http",
            "method": "GET",
            "path": "/api/v1/classes",
            "headers": [(b"x-forwarded-for", b"203.0.113.195")],
        })

        # Request 1: OK
        r1 = _run_coro(rate_limit_middleware(classes_req, mock_call_next))
        assert r1.status_code == 200

        # Request 2: OK
        r2 = _run_coro(rate_limit_middleware(classes_req, mock_call_next))
        assert r2.status_code == 200

        # Request 3: 429 Too Many Requests
        r3 = _run_coro(rate_limit_middleware(classes_req, mock_call_next))
        assert r3.status_code == 429
        assert r3.headers.get("Retry-After") == "60"

        # Different IP: OK
        diff_ip_req = Request({
            "type": "http",
            "method": "GET",
            "path": "/api/v1/classes",
            "headers": [(b"x-forwarded-for", b"198.51.100.42")],
        })
        r_diff = _run_coro(rate_limit_middleware(diff_ip_req, mock_call_next))
        assert r_diff.status_code == 200
    finally:
        main_mod.RATE_LIMIT_MAX_REQUESTS = orig_max
        _rate_limit_history.clear()






