"""Measure where server RAM goes, one import at a time.

Run from the repo root:  uv run python scripts/eval/measure_memory_breakdown.py
Needs psutil (uv add --dev psutil) and the model bundle in models/v1/.
Output is for your own analysis; do not put numbers in docs until re-measured.
"""
import gc
import importlib
import os
import sys
import time

import psutil

sys.path.insert(0, os.getcwd())  # so "serving" and "src" resolve from repo root
proc = psutil.Process(os.getpid())
last = proc.memory_info().rss


def rss_mb() -> float:
    return proc.memory_info().rss / 1e6


def step(label: str) -> None:
    global last
    gc.collect()
    now = proc.memory_info().rss
    print(f"{label:<40} {now / 1e6:8.1f} MB   (+{(now - last) / 1e6:6.1f})")
    last = now


step("python + psutil (baseline)")

# Libraries the server likely needs. Add or remove names to match your code.
for name in ["numpy", "PIL", "torch", "torchvision", "fastapi", "uvicorn", "pydantic"]:
    try:
        importlib.import_module(name)
        step(f"import {name}")
    except ImportError:
        print(f"{name:<40} not installed (skipped)")

# Libraries that should NOT be needed at serving time. If these show a big jump
# when imported by your serving code, they are candidates to remove.
for name in ["pandas", "sklearn", "scipy", "matplotlib", "mlflow", "cv2"]:
    try:
        importlib.import_module(name)
        step(f"[check] import {name}")
    except ImportError:
        print(f"{name:<40} not installed (good for serving)")

# Now your real serving code. Adjust the module name if it differs.
t0 = time.time()
try:
    importlib.import_module("serving.inference")
    step("import serving.inference")
    print(f"   import time: {time.time() - t0:.2f} s")
except Exception as exc:
    print(f"Could not import serving.inference: {exc!r}")

print()
print("Next: load the model the same way serving/main.py does (copy its startup code here),")
print("call step('model loaded'), run one warmup prediction, call step('after 1 request').")
print(f"Final RSS: {rss_mb():.1f} MB")
