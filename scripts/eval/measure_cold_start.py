import os
import sys
import time
from pathlib import Path
import psutil
import torch

proc = psutil.Process(os.getpid())
t0 = time.perf_counter()

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

# Import serving bundle and measure startup
rss_start = proc.memory_info().rss / (1024 * 1024)
print(f"Initial Python base RSS: {rss_start:.2f} MB")

t_import_start = time.perf_counter()
from src.models.bundle_loader import load_model_bundle
from src.data.preprocess import load_image
from src.models.predict import predict_single_image
t_import = time.perf_counter() - t_import_start
print(f"Time to import modules: {t_import*1000:.1f} ms")

t_bundle_start = time.perf_counter()
bundle = load_model_bundle("v1", device="cpu")
t_bundle = time.perf_counter() - t_bundle_start
rss_after_bundle = proc.memory_info().rss / (1024 * 1024)
print(f"Model bundle load time: {t_bundle*1000:.1f} ms | RSS after bundle load: {rss_after_bundle:.2f} MB")

# Lifespan warm-up pass
t_warm_start = time.perf_counter()
bundle.model.eval()
with torch.no_grad():
    dummy = torch.zeros(1, 3, 256, 256, device="cpu")
    bundle.model(dummy)
t_warm = time.perf_counter() - t_warm_start
rss_idle = proc.memory_info().rss / (1024 * 1024)
print(f"Cold-start warm-up pass: {t_warm*1000:.1f} ms | Server idle RSS post-warmup: {rss_idle:.2f} MB")

# First single image prediction (cold-start request)
sample_img = Path("data/processed/test_in_the_wild/Citrus - citrus canker/IMG_20261029_091820.jpg")
t_pred_start = time.perf_counter()
res = predict_single_image(bundle, sample_img, heatmap=True)
t_first_pred = time.perf_counter() - t_pred_start
rss_post_pred = proc.memory_info().rss / (1024 * 1024)
print(f"First prediction latency (with Grad-CAM): {t_first_pred*1000:.1f} ms | RSS after 1st request: {rss_post_pred:.2f} MB")

# Second prediction (warm request)
t_pred2_start = time.perf_counter()
res2 = predict_single_image(bundle, sample_img, heatmap=True)
t_second_pred = time.perf_counter() - t_pred2_start
print(f"Second prediction latency (warm): {t_second_pred*1000:.1f} ms")

total_cold_start = t_bundle + t_warm + t_first_pred
print(f"Total time to first inference: {total_cold_start:.2f} s")
