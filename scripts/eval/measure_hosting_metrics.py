import os
import sys
import time
from pathlib import Path
import psutil

# 1. Checkpoint size
ckpt_path = Path("models/v1/model_dualhead_convnext_tiny.pth")
if ckpt_path.exists():
    ckpt_bytes = ckpt_path.stat().st_size
    ckpt_mb = ckpt_bytes / (1024 * 1024)
    print(f"Checkpoint size: {ckpt_bytes} bytes ({ckpt_mb:.2f} MB)")
else:
    print("Checkpoint not found!")

# 2. Frontend assets size
frontend_path = Path("../plant-disease-frontend")
if not frontend_path.exists():
    frontend_path = Path("../hale-public-frontend")
if frontend_path.exists():
    total_fe_bytes = sum(f.stat().st_size for f in frontend_path.rglob("*") if f.is_file())
    wiki_bytes = sum(f.stat().st_size for f in (frontend_path / "assets" / "wiki_samples").glob("*") if f.is_file())
    print(f"Total frontend size: {total_fe_bytes / (1024*1024):.2f} MB")
    print(f"Wiki samples size: {wiki_bytes / (1024*1024):.2f} MB ({len(list((frontend_path / 'assets' / 'wiki_samples').glob('*')))} files)")

# 3. Backend docs/assets size
backend_assets = Path("docs/assets")
if backend_assets.exists():
    be_assets_bytes = sum(f.stat().st_size for f in backend_assets.rglob("*") if f.is_file())
    print(f"Backend docs/assets size: {be_assets_bytes / (1024*1024):.2f} MB ({len(list(backend_assets.rglob('*')))} files)")
