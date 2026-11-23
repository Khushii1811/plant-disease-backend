---
title: Hale
emoji: 🌿
colorFrom: green
colorTo: emerald
sdk: docker
app_port: 7860
pinned: false
license: cc-by-nc-sa-4.0
---

# 🌿 Hale — Botanical Leaf Disease Classification Engine

Hale is a research prototype for foliar plant leaf disease classification powered by a DualHead ConvNeXt-Tiny deep learning architecture.

## ⚠️ Important Notices & Disclaimers
- **Non-Commercial Research Prototype:** Licensed under **Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)**. Strictly not for commercial use.
- **Curated Dataset Benchmark:** Tested on curated research images (92,165 images, 177 classes, 33 crops). Field performance in uncontrolled farm environments has not yet been measured.
- **Not for Diagnostic or Agronomic Decisions:** This application is an educational and screening exploration tool. It must not be relied upon for critical agricultural, commercial, or crop management decisions.
- **Cold Start Notice:** On Hugging Face Spaces CPU Basic (free tier), the application sleeps when idle. The first request after sleep may take up to 60 seconds while the container initializes and loads the PyTorch model weights into memory. Subsequent inferences execute in real-time.

## 🏗️ Architecture
- **Model:** ConvNeXt-Tiny DualHead (hierarchical crop gating + 177-class disease head) with post-hoc temperature scaling calibration.
- **Interpretability:** Integrated Grad-CAM saliency heatmaps visualizing convolutional attention.
- **Backend:** FastAPI running in Python 3.13 with CPU-optimized PyTorch 2.6.0.
- **Frontend:** Static, privacy-focused browser interface with zero telemetry and client-side PDF diagnostic report generation.
