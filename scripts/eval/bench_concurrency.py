import sys
import time
from pathlib import Path

ROOT = Path("E:/Sprayer/plant-disease-backend")
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import pandas as pd
import torch
from torch.utils.data import DataLoader, Dataset
from src.data.preprocess import get_val_transforms, load_image
from src.models.bundle_loader import load_model_bundle
from src.models.predict import predict_tensor

class FastEvalDataset(Dataset):
    def __init__(self, df: pd.DataFrame, transform, root_dir: Path):
        self.df = df.reset_index(drop=True)
        self.transform = transform
        self.root_dir = root_dir

    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):
        row = self.df.iloc[idx]
        p = Path(row["path"])
        if not p.exists():
            p = self.root_dir / p
        img = load_image(p)
        tensor = self.transform(img)
        return tensor, row["class_idx"], row["crop_idx"]

df = pd.read_csv(ROOT / "reports/v1/dataset_v1.csv")
test_df = df[df["split"] == "test"].copy().reset_index(drop=True)

bundle = load_model_bundle("v1", device="cpu")
bundle.model.eval()
c2i = {c: i for i, c in enumerate(bundle.class_names)}
crop2i = {c: i for i, c in enumerate(bundle.crop_hierarchy["crops"])}
test_df["class_idx"] = test_df["class"].map(c2i)
test_df["crop_idx"] = test_df["crop"].map(crop2i)

ds = FastEvalDataset(test_df.iloc[:320], get_val_transforms(), ROOT)
loader = DataLoader(ds, batch_size=64, shuffle=False)
c2c = torch.tensor(bundle.crop_hierarchy["class_idx_to_crop_idx"], dtype=torch.long)

for th in [1, 4, 8]:
    torch.set_num_threads(th)
    t0 = time.time()
    for batch_tensors, b_d, b_c in loader:
        out = predict_tensor(bundle.model, batch_tensors, c2c, bundle.T_crop, bundle.T_disease)
    elapsed = time.time() - t0
    print(f"Threads={th}: 320 images (5 batches) in {elapsed:.2f}s ({320/elapsed:.1f} img/s)")
