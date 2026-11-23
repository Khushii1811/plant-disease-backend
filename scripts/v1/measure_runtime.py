"""
scripts/v1/measure_runtime.py — Measure runtime latency, memory, and concurrency profiles.

Measures empirically on CPU (and GPU if available):
  1. Bundle load time and peak RSS during bundle load.
  2. Cold-start warm-up latency.
  3. p50 and p95 latency per image over 200 clean test images (batch size 1).
  4. Peak RSS during 2 concurrent inference requests.

Outputs:
  reports/v1/runtime_profile.json
"""

import argparse
import json
import platform
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any, Dict, List

import numpy as np
import pandas as pd
import psutil
import torch

_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import config
from src.data.preprocess import get_val_transforms, load_image
from src.models.bundle_loader import load_model_bundle
from src.models.predict import predict_single_image, predict_tensor


def get_cpu_model_name() -> str:
    """Retrieve human-readable CPU brand/model string."""
    try:
        import winreg

        key = winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE,
            r"HARDWARE\DESCRIPTION\System\CentralProcessor\0",
        )
        name, _ = winreg.QueryValueEx(key, "ProcessorNameString")
        winreg.CloseKey(key)
        return str(name).strip()
    except Exception:
        return platform.processor() or "Unknown CPU"


def get_clean_test_images(num_images: int = 200) -> List[Path]:
    """Retrieve verified test split image paths (test split is leak-checked N=9,279)."""
    dataset_csv = config.REPORTS_DIR / "v1" / "dataset_v1.csv"

    if not dataset_csv.exists():
        raise FileNotFoundError(f"Missing dataset manifest: {dataset_csv}")

    df = pd.read_csv(dataset_csv)
    test_df = df[df["split"] == "test"]
    clean_paths = [config.PROJECT_ROOT / p for p in test_df["path"].iloc[:num_images]]
    if len(clean_paths) < num_images:
        raise ValueError(
            f"Requested {num_images} clean test images, but only found {len(clean_paths)}"
        )
    return clean_paths


def measure_device(device_name: str, clean_images: List[Path]) -> Dict[str, Any]:
    """Profile runtime characteristics on specified compute device (cpu or cuda)."""
    proc = psutil.Process()
    print(f"\n[INFO] Measuring runtime profile on: {device_name.upper()}...")

    # 1. Bundle load time and peak RSS during loading
    rss_start = proc.memory_info().rss / (1024 * 1024)
    peak_rss = rss_start
    stop_monitor = False

    def monitor_rss():
        nonlocal peak_rss
        while not stop_monitor:
            try:
                curr = proc.memory_info().rss / (1024 * 1024)
                if curr > peak_rss:
                    peak_rss = curr
            except Exception:
                pass
            time.sleep(0.005)

    mon_thread = threading.Thread(target=monitor_rss, daemon=True)
    mon_thread.start()

    t0 = time.perf_counter()
    bundle = load_model_bundle("v1", device=device_name)
    load_time_s = time.perf_counter() - t0

    stop_monitor = True
    mon_thread.join()

    rss_after_load = proc.memory_info().rss / (1024 * 1024)
    peak_rss = max(peak_rss, rss_after_load)
    print(f"  Bundle load time      : {load_time_s:.4f} s")
    print(f"  Peak RSS during load  : {peak_rss:.2f} MB")

    # 2. Cold-start warm-up pass
    bundle.model.eval()
    dummy = torch.zeros(1, 3, 256, 256, device=device_name)
    if device_name == "cuda":
        torch.cuda.synchronize()
    t0 = time.perf_counter()
    with torch.no_grad():
        bundle.model(dummy)
    if device_name == "cuda":
        torch.cuda.synchronize()
    warmup_time_s = time.perf_counter() - t0
    print(f"  Warm-up latency       : {warmup_time_s * 1000:.2f} ms ({warmup_time_s:.4f} s)")

    # 3. Latency over 200 clean test images (single image, batch 1)
    e2e_latencies_ms: List[float] = []
    forward_latencies_ms: List[float] = []

    transform = get_val_transforms()
    class_idx_to_crop = torch.tensor(
        bundle.crop_hierarchy["class_idx_to_crop_idx"],
        dtype=torch.long,
        device=device_name,
    )

    for img_path in clean_images:
        # Measure end-to-end single-image prediction
        if device_name == "cuda":
            torch.cuda.synchronize()
        t_e2e_0 = time.perf_counter()
        _ = predict_single_image(bundle, img_path)
        if device_name == "cuda":
            torch.cuda.synchronize()
        t_e2e_1 = time.perf_counter()
        e2e_latencies_ms.append((t_e2e_1 - t_e2e_0) * 1000.0)

        # Measure pure model forward pass alone on preprocessed tensor
        img = load_image(img_path)
        tensor = transform(img).unsqueeze(0).to(device_name)
        if device_name == "cuda":
            torch.cuda.synchronize()
        t_fwd_0 = time.perf_counter()
        with torch.no_grad():
            _ = predict_tensor(
                bundle.model, tensor, class_idx_to_crop, bundle.T_crop, bundle.T_disease
            )
        if device_name == "cuda":
            torch.cuda.synchronize()
        t_fwd_1 = time.perf_counter()
        forward_latencies_ms.append((t_fwd_1 - t_fwd_0) * 1000.0)

    p50_e2e = float(np.percentile(e2e_latencies_ms, 50))
    p95_e2e = float(np.percentile(e2e_latencies_ms, 95))
    p50_fwd = float(np.percentile(forward_latencies_ms, 50))
    p95_fwd = float(np.percentile(forward_latencies_ms, 95))

    print(f"  Forward pass latency  : p50={p50_fwd:.2f} ms, p95={p95_fwd:.2f} ms")
    print(f"  End-to-end latency    : p50={p50_e2e:.2f} ms, p95={p95_e2e:.2f} ms")

    # 4. RSS during 2 concurrent requests
    rss_during_concurrent: List[float] = []
    concurrent_stop = False

    def sample_concurrent_rss():
        while not concurrent_stop:
            try:
                rss_during_concurrent.append(proc.memory_info().rss / (1024 * 1024))
            except Exception:
                pass
            time.sleep(0.005)

    rss_thread = threading.Thread(target=sample_concurrent_rss, daemon=True)
    rss_thread.start()

    with ThreadPoolExecutor(max_workers=2) as executor:
        f1 = executor.submit(predict_single_image, bundle, clean_images[0])
        f2 = executor.submit(predict_single_image, bundle, clean_images[1])
        _ = f1.result()
        _ = f2.result()

    concurrent_stop = True
    rss_thread.join()

    peak_concurrent_rss = (
        max(rss_during_concurrent)
        if rss_during_concurrent
        else proc.memory_info().rss / (1024 * 1024)
    )
    print(f"  Peak RSS (2 concurrent requests): {peak_concurrent_rss:.2f} MB")

    return {
        "device": device_name,
        "bundle_load_time_seconds": round(load_time_s, 4),
        "bundle_load_peak_rss_mb": round(peak_rss, 2),
        "warmup_time_seconds": round(warmup_time_s, 4),
        "warmup_time_ms": round(warmup_time_s * 1000, 2),
        "latency_forward_pass_p50_ms": round(p50_fwd, 2),
        "latency_forward_pass_p95_ms": round(p95_fwd, 2),
        "latency_end_to_end_p50_ms": round(p50_e2e, 2),
        "latency_end_to_end_p95_ms": round(p95_e2e, 2),
        "concurrent_2_requests_peak_rss_mb": round(peak_concurrent_rss, 2),
    }


def main():
    parser = argparse.ArgumentParser(description="Measure runtime profile for Model v1.")
    parser.add_argument(
        "--num-images",
        type=int,
        default=200,
        help="Number of clean test images to evaluate (default: 200).",
    )
    args = parser.parse_args()

    clean_images = get_clean_test_images(num_images=args.num_images)
    cpu_model = get_cpu_model_name()
    thread_count = torch.get_num_threads()
    torch_version = torch.__version__
    cuda_available = torch.cuda.is_available()

    hardware_info: Dict[str, Any] = {
        "cpu_model": cpu_model,
        "cpu_thread_count": thread_count,
        "torch_version": torch_version,
        "cuda_available": cuda_available,
    }
    if cuda_available:
        hardware_info["gpu_model"] = torch.cuda.get_device_name(0)

    print("=" * 70)
    print("RUNTIME PROFILE BENCHMARK")
    print("=" * 70)
    print(f"CPU Model          : {cpu_model}")
    print(f"CPU Threads        : {thread_count}")
    print(f"PyTorch Version    : {torch_version}")
    print(f"CUDA Available     : {cuda_available}")
    if cuda_available:
        print(f"GPU Model          : {hardware_info['gpu_model']}")
    print(f"Benchmark Dataset  : {len(clean_images)} clean test images")

    profiles: Dict[str, Any] = {}
    profiles["cpu"] = measure_device("cpu", clean_images)

    if cuda_available:
        profiles["cuda"] = measure_device("cuda", clean_images)

    output_data = {
        "hardware": hardware_info,
        "profiles": profiles,
    }

    out_file = config.REPORTS_DIR / "v1" / "runtime_profile.json"
    out_file.parent.mkdir(parents=True, exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=2)

    print("\n" + "=" * 70)
    print(f"Runtime profile successfully written to: {out_file}")
    print("=" * 70)


if __name__ == "__main__":
    main()
