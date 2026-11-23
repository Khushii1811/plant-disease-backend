FROM python:3.13-slim-bookworm

# Streaming logs without Python buffering; non-root home and torch cache in /tmp
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    HOME=/tmp \
    TORCH_HOME=/tmp \
    PORT=7860

# Non-root user required by Hugging Face Spaces (UID 1000)
RUN useradd -m -u 1000 user

WORKDIR /app

# Install CPU-only PyTorch and runtime packages
COPY requirements.txt /app/
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir torch==2.6.0 torchvision==0.21.0 --index-url https://download.pytorch.org/whl/cpu && \
    pip install --no-cache-dir -r requirements.txt

# Copy application runtime code, weights, and static assets
COPY --chown=user:user config.py /app/config.py
COPY --chown=user:user serving/ /app/serving/
COPY --chown=user:user src/ /app/src/
COPY --chown=user:user models/v1/ /app/models/v1/
COPY --chown=user:user static/ /app/static/

USER user

EXPOSE 7860

CMD ["uvicorn", "serving.main:app", "--host", "0.0.0.0", "--port", "7860", "--workers", "1"]
