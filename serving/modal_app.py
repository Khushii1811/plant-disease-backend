"""
serving/modal_app.py — Serverless ASGI Deployment on Modal (modal.com).

Exposes the production FastAPI application (`serving.main:app`) via Modal's serverless
infrastructure with containerized PyTorch inference, automatic scale-to-zero,
and CORS support for external frontend clients.

Deployment command:
    uv run modal deploy serving/modal_app.py

Interactive / ephemeral test command:
    uv run modal serve serving/modal_app.py
"""

from pathlib import Path
import modal

# Define project directories relative to this file
_SERVING_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = _SERVING_DIR.parent

RELEASE_WEIGHTS_URL = (
    "https://github.com/Khushii1811/plant-disease-backend/releases/download/v1.0.0/model_dualhead_convnext_tiny.pth"
)
EXPECTED_SHA256 = "3bb5785efa957a5fd4eb9d071fa92ff57adbef9788275a810e9cce99cf016dcb"

# Modal container image specification
# Debian slim with CPU-optimized PyTorch wheels for fast container cold-starts and minimal image footprint
image = (
    modal.Image.debian_slim(python_version="3.11")
    .apt_install("curl")
    .pip_install(
        "torch>=2.0.0",
        "torchvision>=0.15.0",
        extra_index_url="https://download.pytorch.org/whl/cpu",
    )
    .pip_install(
        "fastapi>=0.115.0",
        "uvicorn[standard]>=0.30.0",
        "pydantic>=2.8.0",
        "pydantic-settings>=2.4.0",
        "pillow>=10.0.0",
        "python-multipart>=0.0.9",
        "scikit-learn>=1.3.0",
        "numpy>=1.24.0",
        "rembg>=2.0.69",
        "onnxruntime>=1.20.0",
    )
    # Add application source code
    .add_local_file(PROJECT_ROOT / "config.py", remote_path="/app/config.py", copy=True)
    .add_local_dir(PROJECT_ROOT / "src", remote_path="/app/src", ignore=["*.pyc", "**/__pycache__"], copy=True)
    .add_local_dir(PROJECT_ROOT / "serving", remote_path="/app/serving", ignore=["*.pyc", "**/__pycache__"], copy=True)
    # Add metadata and class hierarchy configs (exclude 108MB pth file so local upload takes < 1 second!)
    .add_local_dir(
        PROJECT_ROOT / "models" / "v1",
        remote_path="/app/models/v1",
        ignore=["*.pyc", "*.pth"],
        copy=True,
    )
    # Fetch verified production weights directly into container layer from GitHub Release CDN and verify checksum
    .run_commands(
        f"curl -fsSL -o /app/models/v1/model_dualhead_convnext_tiny.pth {RELEASE_WEIGHTS_URL}",
        f"python -c \"import hashlib; h = hashlib.sha256(open('/app/models/v1/model_dualhead_convnext_tiny.pth', 'rb').read()).hexdigest(); assert h == '{EXPECTED_SHA256}', f'Checksum mismatch: {{h}}'\"",
    )
    .workdir("/app")
    .env({
        "PYTHONPATH": "/app",
        "CORS_ORIGINS": "*",
        "ALLOWED_ORIGINS": "*",
        "RATE_LIMIT_ENABLED": "false",  # Modal manages rate limiting and auto-scaling
    })
)

app = modal.App("plant-disease-backend", image=image)


@app.function(
    memory=4096,           # 4 GB RAM: safe headroom for high-res decompression & ConvNeXt features
    cpu=2.0,               # 2 vCPUs: fast multi-threaded tensor operations
    timeout=120,           # 120s timeout per invocation
    scaledown_window=300,  # Keep container warm for 5 minutes after last request
)
@modal.asgi_app()
def fastapi_app():
    import sys
    if "/app" not in sys.path:
        sys.path.insert(0, "/app")

    from serving.main import app as web_app
    return web_app
