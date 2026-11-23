"""
scripts/v1/run_determinism_test.py

Runs the determinism matrix for L1(c):
Evaluates 3 runs each for:
  1. threads=1, deterministic=True
  2. threads=1, deterministic=False
  3. threads=default (8), deterministic=True
  4. threads=default (8), deterministic=False
  5. threads=4, deterministic=True
  6. threads=4, deterministic=False

Shows live tqdm progress bars and prints total correct for each run.
"""

import os
import sys
import time
import torch
import pandas as pd
from pathlib import Path
from torch.utils.data import DataLoader, Dataset
from tqdm import tqdm

ROOT = Path(__file__).resolve().parent.parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.data.preprocess import get_val_transforms, load_image
from src.models.bundle_loader import load_model_bundle
from src.models.predict import predict_tensor

def main():
    print("=" * 70, flush=True)
    print("STARTING DETERMINISM MATRIX TEST (L1.c)", flush=True)
    print("=" * 70, flush=True)

    print("Loading model bundle on CPU...", flush=True)
    bundle = load_model_bundle("v1", device="cpu")
    transform = get_val_transforms()

    df = pd.read_csv(ROOT / "reports" / "v1" / "dataset_v1.csv")
    test_df = df[df["split"] == "test"].reset_index(drop=True)
    print(f"Total test images to evaluate: {len(test_df)}", flush=True)

    class_to_idx = {name: i for i, name in enumerate(bundle.class_names)}
    class_idx_to_crop = torch.tensor(
        [bundle.crop_hierarchy["class_idx_to_crop_idx"][i] for i in range(len(bundle.class_names))],
        device="cpu"
    )

    class FastEvalDataset(Dataset):
        def __init__(self, df, transform):
            self.df = df
            self.transform = transform

        def __len__(self):
            return len(self.df)

        def __getitem__(self, idx):
            row = self.df.iloc[idx]
            img = load_image(row["path"])
            t = self.transform(img)
            d_idx = class_to_idx[row["class"]]
            return t, d_idx

    dataset = FastEvalDataset(test_df, transform)
    loader = DataLoader(dataset, batch_size=128, shuffle=False, num_workers=0)

    print("\nPhase 1: Pre-loading all 9,279 images into memory (done once)...", flush=True)
    all_tensors = []
    all_labels = []
    for batch_t, b_d in tqdm(loader, desc="Preloading images", file=sys.stdout):
        all_tensors.append(batch_t)
        all_labels.append(b_d)
        sys.stdout.flush()

    default_threads = torch.get_num_threads()
    settings = [
        ("OMP_NUM_THREADS=1, deterministic=True", 1, True),
        ("OMP_NUM_THREADS=1, deterministic=False", 1, False),
        (f"threads=default ({default_threads}), deterministic=True", default_threads, True),
        (f"threads=default ({default_threads}), deterministic=False", default_threads, False),
        ("OMP_NUM_THREADS=4, deterministic=True", 4, True),
        ("OMP_NUM_THREADS=4, deterministic=False", 4, False),
    ]

    print("\nPhase 2: Running Determinism Matrix (3 runs per setting)...", flush=True)
    matrix_results = {}

    for s_idx, (name, th, det) in enumerate(settings, 1):
        torch.set_num_threads(th)
        torch.use_deterministic_algorithms(det)
        run_scores = []
        print(f"\n[{s_idx}/6] Setting: {name}", flush=True)

        for r in range(1, 4):
            correct = 0
            desc = f"  Run {r}/3"
            t0 = time.time()
            with torch.no_grad():
                for batch_t, b_d in tqdm(zip(all_tensors, all_labels), total=len(all_tensors), desc=desc, file=sys.stdout):
                    out = predict_tensor(
                        model=bundle.model,
                        tensor=batch_t,
                        class_idx_to_crop=class_idx_to_crop,
                        T_c=bundle.T_crop,
                        T_d=bundle.T_disease
                    )
                    preds = torch.argmax(out["p_joint"], dim=1)
                    correct += int((preds == b_d).sum().item())
            dt = time.time() - t0
            run_scores.append(correct)
            print(f"  Run {r}/3: Total Correct = {correct} / {len(test_df)} ({dt:.1f}s)", flush=True)
            sys.stdout.flush()

        matrix_results[name] = run_scores

    print("\n" + "=" * 70, flush=True)
    print("DETERMINISM MATRIX SUMMARY TABLE", flush=True)
    print("=" * 70, flush=True)
    for name, scores in matrix_results.items():
        is_ident = len(set(scores)) == 1
        print(f"{name:50} -> Runs: {scores} | Identical: {is_ident}")

if __name__ == "__main__":
    main()
