"""
tests/test_modal_app.py — Test suite for Modal serverless ASGI deployment configuration.
"""

import os
from pathlib import Path

# Provide sandbox-safe config path if unset
if "MODAL_CONFIG_PATH" not in os.environ:
    os.environ["MODAL_CONFIG_PATH"] = str(Path(__file__).resolve().parent / "dummy_modal.toml")


def test_modal_app_configuration():
    """Verify Modal App metadata, container image specs, and entrypoint function."""
    import modal
    import serving.modal_app as modal_app

    assert modal_app.app.name == "plant-disease-backend"
    assert hasattr(modal_app, "fastapi_app")
    assert isinstance(modal_app.fastapi_app, modal.functions.Function)
    assert modal_app.fastapi_app._is_web_endpoint
    assert modal_app.PROJECT_ROOT.exists()
    assert (modal_app.PROJECT_ROOT / "config.py").exists()
    assert (modal_app.PROJECT_ROOT / "models" / "v1").exists()
