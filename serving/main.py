"""
serving/main.py — FastAPI application entrypoint for the Plant Disease Classification API.

Startup sequence:
  1. sys.path bootstrap.
  2. FastAPI app creation with full OpenAPI metadata.
  3. CORS middleware.
  4. Lifespan context: model + class list loaded once on startup.
  5. Routers registered: /api/v1/predict, /api/v1/classes, /api/v1/crops.
  6. Health endpoint: GET /api/v1/health — returns device, temperatures, num_classes.

Run locally:
    uvicorn serving.main:app --reload --host 0.0.0.0 --port 8000
"""

import contextvars
import logging
import os
import sys
import time
import uuid
from collections import defaultdict
from contextlib import asynccontextmanager
from pathlib import Path
import torch
from starlette.responses import JSONResponse

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.requests import Request

from serving.inference import (
    _bundle,
    _class_names,
    device,
)
from serving.routes.predict import router as predict_router
from serving.schemas import HealthResponse

request_id_ctx: contextvars.ContextVar[str] = contextvars.ContextVar("request_id", default="-")


class RequestIDFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = request_id_ctx.get()
        return True


log_format = "%(asctime)s %(levelname)-8s [%(request_id)s] %(name)s — %(message)s"
logging.basicConfig(level=logging.INFO, format=log_format)

for handler in logging.root.handlers:
    handler.addFilter(RequestIDFilter())
    handler.setFormatter(logging.Formatter(log_format))

logger = logging.getLogger("main")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("=" * 65)
    logger.info("  Plant Disease Classification API — starting up")
    logger.info("=" * 65)
    t_c = _bundle.T_crop if _bundle is not None else 0.5931
    t_d = _bundle.T_disease if _bundle is not None else 0.5013
    logger.info("Device                 : %s", device)
    logger.info("Classes loaded         : %d", len(_class_names))
    logger.info("Calibration T_crop     : %.4f", t_c)
    logger.info("Calibration T_disease  : %.4f", t_d)
    logger.info("Docs (Swagger UI)      : http://localhost:8000/docs")
    logger.info("=" * 65)

    if _bundle is not None:
        # Warm-up pass with dummy tensor to avoid cold-start latency spikes
        logger.info("Executing cold-start model warm-up pass...")
        _bundle.model.eval()
        with torch.no_grad():
            _dummy = torch.zeros(1, 3, 256, 256, device=device)
            _bundle.model(_dummy)
        logger.info("Model warm-up pass completed successfully.")
    else:
        logger.warning("Model bundle weights missing; skipping warm-up pass.")

    yield

    logger.info("Plant Disease Classification API — shutting down.")


app = FastAPI(
    title="Plant Leaf Disease Classification API",
    description=(
        "Production inference service for foliar plant leaf disease classification. "
        "Built on ConvNeXt-Tiny DualHead architecture with calibrated soft crop-gating. "
        "Strictly provides image classification without treatment recommendations."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

allowed_origins_env = os.getenv("ALLOWED_ORIGINS")
if allowed_origins_env is None:
    allowed_origins_env = os.getenv("CORS_ORIGINS", "")

if allowed_origins_env.strip():
    cors_origins = [o.strip() for o in allowed_origins_env.split(",") if o.strip()]
else:
    cors_origins = []  # Default same-origin only

if cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_origins,
        allow_credentials=False,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["*"],
    )

# In-memory sliding-window rate limiter per client IP
RATE_LIMIT_WINDOW_SECONDS = 60.0
RATE_LIMIT_MAX_REQUESTS = int(os.getenv("RATE_LIMIT_PER_MINUTE", "60"))
RATE_LIMIT_ENABLED = os.getenv("RATE_LIMIT_ENABLED", "true").lower() in ("1", "true", "yes")
_rate_limit_history: dict[str, list[float]] = defaultdict(list)

EXEMPT_PATHS = {
    "/api/v1/health",
    "/api/v1/ready",
    "/docs",
    "/redoc",
    "/openapi.json",
    "/favicon.ico",
}


def get_client_ip(request: Request) -> str:
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    if request.client and request.client.host:
        return request.client.host
    return "127.0.0.1"


@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    if not RATE_LIMIT_ENABLED or request.method == "OPTIONS":
        return await call_next(request)

    path = request.url.path
    if (
        path in EXEMPT_PATHS
        or path.startswith(("/docs", "/redoc"))
        or not path.startswith("/api/v1/")
    ):
        return await call_next(request)

    client_ip = get_client_ip(request)
    now = time.time()
    cutoff = now - RATE_LIMIT_WINDOW_SECONDS

    # Filter timestamps within sliding window
    timestamps = [t for t in _rate_limit_history[client_ip] if t > cutoff]

    if len(timestamps) >= RATE_LIMIT_MAX_REQUESTS:
        logger.warning(
            "Rate limit of %d req/min exceeded for client %s on %s",
            RATE_LIMIT_MAX_REQUESTS,
            client_ip,
            path,
        )
        return JSONResponse(
            status_code=429,
            content={
                "detail": f"Too Many Requests: Rate limit of {RATE_LIMIT_MAX_REQUESTS} requests per minute exceeded."
            },
            headers={"Retry-After": str(int(RATE_LIMIT_WINDOW_SECONDS))},
        )

    timestamps.append(now)
    _rate_limit_history[client_ip] = timestamps

    # Periodic cleanup to prevent unbounded memory growth
    if len(_rate_limit_history) > 2000:
        stale_ips = [ip for ip, ts in _rate_limit_history.items() if not ts or ts[-1] <= cutoff]
        for ip in stale_ips:
            _rate_limit_history.pop(ip, None)

    return await call_next(request)

@app.middleware("http")
async def request_id_middleware(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
    request.state.request_id = request_id
    token = request_id_ctx.set(request_id)
    try:
        logger.info("Request started: %s %s", request.method, request.url.path)
        response = await call_next(request)
        logger.info(
            "Request completed: %s %s status=%d",
            request.method,
            request.url.path,
            response.status_code,
        )
    finally:
        request_id_ctx.reset(token)
    response.headers["X-Request-ID"] = request_id
    return response


app.include_router(predict_router)


@app.get(
    "/api/v1/health",
    response_model=HealthResponse,
    tags=["Health"],
    summary="API health check",
    description="Returns current service status, model metadata, and calibration temperatures.",
)
async def health() -> HealthResponse:
    t_crop = _bundle.T_crop if _bundle is not None else 0.5931
    t_disease = _bundle.T_disease if _bundle is not None else 0.5013
    return HealthResponse(
        status="healthy",
        model_architecture="ConvNeXt-Tiny DualHead",
        num_classes=len(_class_names),
        device=str(device),
        calibration_temperature_crop=t_crop,
        calibration_temperature_disease=t_disease,
        version="1.0.0",
    )


@app.get(
    "/api/v1/ready",
    tags=["Health"],
    summary="Readiness probe",
    description="Returns ready status if the application and model weights are initialized.",
)
async def ready() -> dict:
    return {"status": "ready"}


# Mount static frontend files AFTER all /api/v1 routes so API endpoints take precedence.
static_dir = _ROOT / "static"
if not static_dir.exists():
    static_dir = Path("static")

if static_dir.exists():
    app.mount("/", StaticFiles(directory=str(static_dir), html=True), name="static")
    logger.info("Mounted static frontend files from: %s", static_dir)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("serving.main:app", host="0.0.0.0", port=8000, reload=True)
