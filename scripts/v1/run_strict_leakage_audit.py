"""
scripts/v1/run_strict_leakage_audit.py

High-performance vectorized Multi-Metric Leakage Audit on v1 data across all 195 classes:
1. STRICT criterion: Exact SHA-256 OR 8-dihedral pHash <= 4 (D_4 group: 4 rotations x 2 flips).
   - Uses precomputed SHA-256 from reports/v1/dataset_v1.csv.
   - Computes standard pHash once per train image, vectorized hamming distance via bitwise operations.
2. LOOSE criterion: Pretrained MobileNetV3 feature cosine similarity >= 0.95 without strict match.
3. Outputs:
   - reports/v1/leakage_strict_per_class.csv
   - reports/v1/leakage_strict_audit_summary.json
   - reports/v1/figures/contact_sheet_strict_leakage_20.png
   - reports/v1/figures/contact_sheet_loose_leakage_20.png
"""

import contextlib
import sys
import json
import logging
from pathlib import Path
from collections import defaultdict

import numpy as np
import pandas as pd
from PIL import Image
import imagehash
import torch
import torchvision.models as models
from torchvision import transforms
from sklearn.metrics import classification_report
from tqdm import tqdm

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
import config
from src.models.convnext import build_dualhead_convnext_tiny

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("strict_leakage_audit")


def phash_to_uint64(hash_obj) -> int:
    # 64-bit integer representation of 8x8 boolean array
    return int(str(hash_obj), 16)


def get_8_dihedral_uint64(im: Image.Image) -> list:
    hashes = []
    for rot in [0, 90, 180, 270]:
        r_im = im.rotate(rot, expand=True) if rot > 0 else im
        h1 = imagehash.phash(r_im)
        h2 = imagehash.phash(r_im.transpose(Image.FLIP_LEFT_RIGHT))
        hashes.append(phash_to_uint64(h1))
        hashes.append(phash_to_uint64(h2))
    return hashes


def count_set_bits(n):
    return bin(n).count("1")


def min_dihedral_dist_vectorized(test_8_uint64: list, train_uint64_array: np.ndarray) -> tuple[int, int]:
    # Returns (min_distance, best_train_idx)
    best_dist = 64
    best_idx = -1
    for t_val in test_8_uint64:
        xors = np.bitwise_xor(train_uint64_array, t_val)
        bitcounts = np.bitwise_count(xors)
        min_idx = int(np.argmin(bitcounts))
        min_d = int(bitcounts[min_idx])
        if min_d < best_dist:
            best_dist = min_d
            best_idx = min_idx
            if best_dist == 0:
                return 0, best_idx
    return best_dist, best_idx


def extract_mobilenet_features(paths: list, model, transform, device) -> np.ndarray:
    features = []
    with torch.no_grad():
        for i in range(0, len(paths), 64):
            batch_paths = paths[i:i+64]
            tensors = []
            for p in batch_paths:
                with open(p, "rb") as f:
                    im = Image.open(f).convert("RGB")
                tensors.append(transform(im))
            t_batch = torch.stack(tensors).to(device)
            feats = model(t_batch)
            feats = torch.flatten(feats, 1)
            feats = torch.nn.functional.normalize(feats, p=2, dim=1)
            features.append(feats.cpu().numpy())
    return np.concatenate(features, axis=0) if features else np.zeros((0, 960))


def main():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    logger.info("Using device: %s", device)

    processed_dir = config.DATA_DIR / "processed"
    reports_dir = PROJECT_ROOT / "reports" / "v1"
    figures_dir = reports_dir / "figures"
    reports_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    # 1. Load Manifest for Instant SHA-256 Lookup
    v1_csv_path = reports_dir / "dataset_v1.csv"
    logger.info("Loading SHA-256 lookup from %s...", v1_csv_path)
    df_manifest = pd.read_csv(v1_csv_path)
    path_to_sha = {r["path"]: r["image_id"] for _, r in df_manifest.iterrows()}
    fname_to_sha = {Path(r["path"]).name: r["image_id"] for _, r in df_manifest.iterrows()}

    # 2. Load Classes
    with open(PROJECT_ROOT / "models" / "v1" / "class_names.json", "r", encoding="utf-8") as f:
        class_names = json.load(f)

    # 3. Setup MobileNetV3 for loose matching
    mobilenet = models.mobilenet_v3_small(weights=models.MobileNet_V3_Small_Weights.DEFAULT)
    mobilenet = mobilenet.features.to(device).eval()
    feature_transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    per_class_leakage = []
    test_strict_twins_total = 0
    test_images_total = 0

    all_test_has_strict = {}
    strict_pairs_pool = []
    loose_pairs_pool = []

    # Chilli tracking
    chilli_classes = [
        "Chilli - Leaf Curl Virus",
        "Chilli - Nutrition Deficiency",
        "Chilli - White Spot"
    ]
    chilli_audit = {c: {"total": 0, "strict_twin": 0, "loose_only": 0, "no_twin": 0, "test_files": []} for c in chilli_classes}

    logger.info("Executing optimized Leakage Audit across %d classes...", len(class_names))

    for cname in tqdm(class_names, desc="Leakage Audit"):
        train_p = processed_dir / "train" / cname
        val_p = processed_dir / "val" / cname
        test_p = processed_dir / "test" / cname

        train_files = sorted([f for f in train_p.iterdir() if f.is_file() and f.suffix.lower() in [".jpg", ".jpeg", ".png", ".webp"]]) if train_p.exists() else []
        val_files = sorted([f for f in val_p.iterdir() if f.is_file() and f.suffix.lower() in [".jpg", ".jpeg", ".png", ".webp"]]) if val_p.exists() else []
        test_files = sorted([f for f in test_p.iterdir() if f.is_file() and f.suffix.lower() in [".jpg", ".jpeg", ".png", ".webp"]]) if test_p.exists() else []

        test_images_total += len(test_files)

        if not train_files or (not test_files and not val_files):
            per_class_leakage.append({
                "class_name": cname,
                "train_count": len(train_files),
                "val_count": len(val_files),
                "test_count": len(test_files),
                "val_strict_twins": 0,
                "val_strict_share": 0.0,
                "test_strict_twins": 0,
                "test_strict_share": 0.0,
                "test_loose_twins": 0,
                "test_loose_share": 0.0
            })
            continue

        # Train SHA-256 set
        train_shas = {}
        for tf in train_files:
            rel = tf.relative_to(PROJECT_ROOT).as_posix()
            sha = path_to_sha.get(rel, fname_to_sha.get(tf.name))
            if sha:
                train_shas[sha] = tf

        # Train 1 pHash per image (fast!)
        train_phashes_u64 = []
        for tf in train_files:
            try:
                with Image.open(tf) as im:
                    train_phashes_u64.append(phash_to_uint64(imagehash.phash(im.convert("RGB"))))
            except Exception:
                train_phashes_u64.append(0)
        train_phashes_arr = np.array(train_phashes_u64, dtype=np.uint64)

        # Deep embeddings for Chilli classes and top suspects
        train_feats = None
        if cname.startswith("Chilli") or len(test_files) <= 60:
            train_feats = extract_mobilenet_features(train_files, mobilenet, feature_transform, device)

        # Test check
        test_strict_cnt = 0
        test_loose_cnt = 0
        test_feats = extract_mobilenet_features(test_files, mobilenet, feature_transform, device) if train_feats is not None and len(train_files) > 0 and len(test_files) > 0 else None

        for idx, tf in enumerate(test_files):
            rel = tf.relative_to(PROJECT_ROOT).as_posix()
            t_sha = path_to_sha.get(rel, fname_to_sha.get(tf.name))
            is_strict = False
            twin_file = None

            # 1. SHA-256 match
            if t_sha and t_sha in train_shas:
                is_strict = True
                twin_file = train_shas[t_sha]
            else:
                # 2. 8-dihedral pHash <= 4
                try:
                    with Image.open(tf) as im:
                        t_8_u64 = get_8_dihedral_uint64(im.convert("RGB"))
                    min_d, best_idx = min_dihedral_dist_vectorized(t_8_u64, train_phashes_arr)
                    if min_d <= 4 and best_idx >= 0:
                        is_strict = True
                        twin_file = train_files[best_idx]
                except Exception:
                    pass

            is_loose = False
            loose_twin_file = None
            if not is_strict and test_feats is not None and train_feats is not None and len(train_feats) > 0:
                sims = np.dot(train_feats, test_feats[idx])
                max_idx = int(np.argmax(sims))
                if sims[max_idx] >= 0.95:
                    is_loose = True
                    loose_twin_file = train_files[max_idx]

            all_test_has_strict[str(tf.resolve())] = is_strict

            if is_strict:
                test_strict_cnt += 1
                if len(strict_pairs_pool) < 40:
                    strict_pairs_pool.append((cname, tf, twin_file))
            elif is_loose:
                test_loose_cnt += 1
                if len(loose_pairs_pool) < 40:
                    loose_pairs_pool.append((cname, tf, loose_twin_file))

            # Chilli classification
            if cname in chilli_audit:
                chilli_audit[cname]["total"] += 1
                status = "strict_twin" if is_strict else ("loose_only" if is_loose else "no_twin")
                chilli_audit[cname][status] += 1
                chilli_audit[cname]["test_files"].append((str(tf.resolve()), status))

        test_strict_twins_total += test_strict_cnt

        # Val check (strict only)
        val_strict_cnt = 0
        for vf in val_files:
            rel = vf.relative_to(PROJECT_ROOT).as_posix()
            v_sha = path_to_sha.get(rel, fname_to_sha.get(vf.name))
            is_v_strict = False
            if v_sha and v_sha in train_shas:
                is_v_strict = True
            else:
                try:
                    with Image.open(vf) as im:
                        v_8_u64 = get_8_dihedral_uint64(im.convert("RGB"))
                    min_d, _ = min_dihedral_dist_vectorized(v_8_u64, train_phashes_arr)
                    if min_d <= 4:
                        is_v_strict = True
                except Exception:
                    pass
            if is_v_strict:
                val_strict_cnt += 1

        per_class_leakage.append({
            "class_name": cname,
            "train_count": len(train_files),
            "val_count": len(val_files),
            "test_count": len(test_files),
            "val_strict_twins": val_strict_cnt,
            "val_strict_share": round(val_strict_cnt / len(val_files), 4) if val_files else 0.0,
            "test_strict_twins": test_strict_cnt,
            "test_strict_share": round(test_strict_cnt / len(test_files), 4) if test_files else 0.0,
            "test_loose_twins": test_loose_cnt,
            "test_loose_share": round(test_loose_cnt / len(test_files), 4) if test_files else 0.0
        })

    # Save CSV
    df_leakage = pd.DataFrame(per_class_leakage)
    csv_path = reports_dir / "leakage_strict_per_class.csv"
    df_leakage.to_csv(csv_path, index=False)
    logger.info("Saved strict leakage audit CSV to %s", csv_path)

    top_25_test_leakage = df_leakage.sort_values(by=["test_strict_twins", "test_strict_share"], ascending=False).head(25)
    total_test_strict_pct = (test_strict_twins_total / test_images_total) * 100
    logger.info("TOTAL STRICT TEST LEAKAGE: %d / %d images (%.2f%%)", test_strict_twins_total, test_images_total, total_test_strict_pct)

    # 4. Model Evaluation on Twin-Free Test Subset
    with open(PROJECT_ROOT / "models" / "v1" / "class_to_idx.json", "r", encoding="utf-8") as f:
        class_to_idx = json.load(f)

    test_dir = config.DATA_DIR / "processed" / "test"
    clean_test_samples = []
    for cname in class_names:
        cdir = test_dir / cname
        if not cdir.exists():
            continue
        c_idx = class_to_idx[cname]
        files = sorted([f for f in cdir.iterdir() if f.is_file() and f.suffix.lower() in [".jpg", ".jpeg", ".png", ".webp"]])
        for f in files:
            if not all_test_has_strict.get(str(f.resolve()), False):
                clean_test_samples.append((f, c_idx, cname))

    num_clean_test = len(clean_test_samples)
    logger.info("Twin-free clean test subset: %d / %d (%.2f%%)", num_clean_test, test_images_total, (num_clean_test / test_images_total) * 100)

    model = build_dualhead_convnext_tiny(num_crops=34, num_classes=195, pretrained=False)
    model.load_state_dict(torch.load(PROJECT_ROOT / "models" / "v1" / "model_dualhead_convnext_tiny.pth", map_location="cpu", weights_only=False))
    model.to(device).eval()

    eval_transform = transforms.Compose([
        transforms.Resize((256, 256)),
        transforms.ToTensor(),
        transforms.Normalize(mean=config.NORMALIZE_MEAN, std=config.NORMALIZE_STD),
    ])

    clean_preds = []
    clean_targets = []
    with torch.no_grad():
        for i in range(0, len(clean_test_samples), 32):
            batch = clean_test_samples[i:i+32]
            imgs = []
            for p, target, _ in batch:
                with open(p, "rb") as f:
                    im = Image.open(f).convert("RGB")
                imgs.append(eval_transform(im))
            t_imgs = torch.stack(imgs).to(device)
            autocast_ctx = torch.amp.autocast(device_type="cuda", dtype=torch.float16) if device.type == "cuda" else contextlib.nullcontext()
            with autocast_ctx:
                _, d_logits = model(t_imgs)
            clean_preds.extend(d_logits.argmax(dim=-1).cpu().tolist())
            clean_targets.extend([b[1] for b in batch])

    clean_acc = float(np.mean(np.array(clean_preds) == np.array(clean_targets)))
    clean_rep = classification_report(clean_targets, clean_preds, labels=list(range(len(class_names))), target_names=class_names, output_dict=True, zero_division=0)
    clean_macro_f1 = clean_rep["macro avg"]["f1-score"]

    logger.info("TWIN-FREE TEST SUBSET PERFORMANCE (N=%d):", num_clean_test)
    logger.info("  Clean Test Accuracy: %.2f%%", clean_acc * 100)
    logger.info("  Clean Test Macro-F1: %.2f%%", clean_macro_f1 * 100)

    # 5. Chilli 3-Way Category Evaluation
    chilli_metrics = {}
    for cname in chilli_classes:
        c_idx = class_to_idx[cname]
        files_info = chilli_audit[cname]["test_files"]
        c_preds = {}
        for p_str, status in files_info:
            p = Path(p_str)
            with open(p, "rb") as f:
                im = Image.open(f).convert("RGB")
            t_im = eval_transform(im).unsqueeze(0).to(device)
            autocast_ctx = torch.amp.autocast(device_type="cuda", dtype=torch.float16) if device.type == "cuda" else contextlib.nullcontext()
            with torch.no_grad(), autocast_ctx:
                _, d_logits = model(t_im)
            pred_idx = int(d_logits.argmax(dim=-1).item())
            is_corr = (pred_idx == c_idx)
            if status not in c_preds:
                c_preds[status] = []
            c_preds[status].append(is_corr)

        chilli_metrics[cname] = {
            "total_test": len(files_info),
            "strict_twin_count": chilli_audit[cname]["strict_twin"],
            "strict_twin_accuracy": float(np.mean(c_preds.get("strict_twin", [1.0]))) if c_preds.get("strict_twin") else None,
            "loose_only_count": chilli_audit[cname]["loose_only"],
            "loose_only_accuracy": float(np.mean(c_preds.get("loose_only", [1.0]))) if c_preds.get("loose_only") else None,
            "no_twin_count": chilli_audit[cname]["no_twin"],
            "no_twin_accuracy": float(np.mean(c_preds.get("no_twin", [1.0]))) if c_preds.get("no_twin") else None,
        }

    # 6. Contact Sheets
    def create_contact_sheet(pairs, out_path, title):
        import matplotlib.pyplot as plt
        n = min(20, len(pairs))
        if n == 0:
            return
        fig, axes = plt.subplots(n, 2, figsize=(8, n * 2.8))
        if n == 1:
            axes = np.expand_dims(axes, 0)
        fig.suptitle(title, fontsize=13, fontweight='bold', y=1.001)

        for i in range(n):
            cname, test_p, train_p = pairs[i]
            with Image.open(test_p) as im1:
                axes[i, 0].imshow(im1)
            axes[i, 0].set_title(f"Test: {cname}\n{Path(test_p).name}", fontsize=7)
            axes[i, 0].axis('off')

            with Image.open(train_p) as im2:
                axes[i, 1].imshow(im2)
            axes[i, 1].set_title(f"Train Twin:\n{Path(train_p).name}", fontsize=7)
            axes[i, 1].axis('off')

        plt.tight_layout()
        plt.savefig(out_path, dpi=150, bbox_inches='tight')
        plt.close()
        logger.info("Saved contact sheet: %s", out_path)

    if strict_pairs_pool:
        create_contact_sheet(strict_pairs_pool, figures_dir / "contact_sheet_strict_leakage_20.png", "Top 20 Strict Leakage Twin Pairs (SHA-256 / 8-Dihedral pHash <= 4)")
    if loose_pairs_pool:
        create_contact_sheet(loose_pairs_pool, figures_dir / "contact_sheet_loose_leakage_20.png", "Top 20 Loose-Only Leakage Pairs (MobileNetV3 Cosine >= 0.95)")

    results = {
        "strict_criterion": "Exact SHA-256 OR 8-dihedral pHash <= 4",
        "loose_criterion": "ImageNet MobileNetV3 cosine >= 0.95 (without strict match)",
        "total_test_images": test_images_total,
        "total_test_strict_twins": test_strict_twins_total,
        "test_strict_leakage_percentage": round(total_test_strict_pct, 2),
        "twin_free_test_subset": {
            "num_images": num_clean_test,
            "share_of_test": round(num_clean_test / test_images_total, 4),
            "test_accuracy": round(clean_acc, 4),
            "test_macro_f1": round(clean_macro_f1, 4)
        },
        "top_25_classes_strict_test_leakage": top_25_test_leakage.to_dict(orient="records"),
        "chilli_leakage_breakdown": chilli_metrics,
        "auto_screening_status": {
            "decisions_54_to_58": "Decision 54 auto-purged Chilli - Bacterial Spot using MD5 exact, multi-rotation dHash <= 3, and MobileNetV3 cosine >= 0.985 (1,752 images quarantined). The remaining 5 Chilli classes were NEVER screened by the automated pipeline (Decisions 55-58)."
        }
    }

    out_json = reports_dir / "leakage_strict_audit_summary.json"
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    logger.info("Saved strict leakage audit summary to %s", out_json)


if __name__ == "__main__":
    main()
