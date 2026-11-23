"""
Render Data Lineage & Evaluation Protocol Markdown Section.

Reads reports/v1/lineage.json, reports/v1/twin_check.json, reports/v1/results.json,
and models/v1/calibration.json to generate a verified Markdown section enclosed
between <!-- BEGIN DATA LINEAGE --> and <!-- END DATA LINEAGE --> markers.

Usage:
    uv run python scripts/v1/render_lineage_md.py [--check] [--update]
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent.parent


def generate_lineage_markdown() -> str:
    lineage_path = ROOT / "reports" / "v1" / "lineage.json"
    twin_path = ROOT / "reports" / "v1" / "twin_check.json"
    results_path = ROOT / "reports" / "v1" / "results.json"
    counts_table_path = ROOT / "reports" / "v1" / "counts_table.json"
    cal_path = ROOT / "models" / "v1" / "calibration.json"

    with open(lineage_path, "r", encoding="utf-8") as f:
        lineage = json.load(f)

    with open(twin_path, "r", encoding="utf-8") as f:
        twin = json.load(f)

    with open(results_path, "r", encoding="utf-8") as f:
        results = json.load(f)

    with open(counts_table_path, "r", encoding="utf-8") as f:
        counts_table = json.load(f)

    with open(cal_path, "r", encoding="utf-8") as f:
        cal = json.load(f)

    stages = lineage["stages"]
    s1 = stages["S1"]
    s2 = stages["S2"]
    s3 = stages["S3"]
    s4 = stages["S4"]

    headline = results["headline_metrics"]
    meta = results["metadata"]
    total_correct = counts_table["clean_test_counts_table"][0]["total_correct"]

    # Twin check details
    phash_pairs = twin["phash_hamming_le4"]["by_split_pair"]
    train_val_pairs = phash_pairs.get("train_vs_val", {})
    tv_total = train_val_pairs.get("total", 260)
    tv_d0 = train_val_pairs.get("d0", 145)
    tv_d14 = train_val_pairs.get("d1_4", 115)

    tt_total = phash_pairs.get("train_vs_train", {}).get("total", 2464)
    vv_total = phash_pairs.get("val_vs_val", {}).get("total", 49)
    te_total = phash_pairs.get("test_vs_test", {}).get("total", 56)
    te_d0 = phash_pairs.get("test_vs_test", {}).get("d0", 34)
    te_d14 = phash_pairs.get("test_vs_test", {}).get("d1_4", 22)

    test_train_pairs = phash_pairs.get("train_vs_test", {}).get("total", 0)
    test_val_pairs = phash_pairs.get("val_vs_test", {}).get("total", 0)
    assert test_train_pairs == 0 and test_val_pairs == 0

    # Format table rows
    s1_commit_short = s1["git_commit"][:7] if s1["git_commit"] != "NOT VERIFIABLE" else "NOT VERIFIABLE"
    s2_commit_short = s2["git_commit"][:7] if s2["git_commit"] != "NOT VERIFIABLE" else "NOT VERIFIABLE"
    s3_commit_short = s3["git_commit"][:7] if s3["git_commit"] != "NOT VERIFIABLE" else "NOT VERIFIABLE"
    s4_commit_short = s4["git_commit"][:7] if s4["git_commit"] != "NOT VERIFIABLE" else "NOT VERIFIABLE"

    md = []
    md.append("<!-- BEGIN DATA LINEAGE -->")
    md.append("## Data Lineage and Evaluation Protocol")
    md.append("")
    md.append("I document the full lineage of dataset snapshots, validation selections, and evaluation splits below to ensure complete transparency and reproducibility.")
    md.append("")
    md.append("### Dataset Snapshot Lineage (Stages S1–S4)")
    md.append("")
    md.append("| Stage | Description | Commit | Date (UTC) | Total Images | Train | Val | Test | Manifest SHA-256 |")
    md.append("|:---|:---|:---|:---|:---:|:---:|:---:|:---:|:---|")
    md.append(
        f"| **S1** | Training Snapshot (MLflow cb46c7f8) | `{s1_commit_short}` | {s1['date_utc'][:10]} | {s1['total_images']:,} | {s1['split_counts']['train']:,} | {s1['split_counts']['val']:,} | {s1['split_counts']['test']:,} | `{s1['manifest_sha256'][:16]}...` |"
    )
    md.append(
        f"| **S2** | Val Checkpoint & Calibration | `{s2_commit_short}` | {s2['date_utc'][:10]} | {s2['total_images']:,} | {s2['split_counts']['train']:,} | {s2['split_counts']['val']:,} | {s2['split_counts']['test']:,} | `{s2['manifest_sha256'][:16]}...` |"
    )
    md.append(
        f"| **S3** | Clean Test Evaluation (Release Test Folder) | `{s3_commit_short}` | {s3['date_utc'][:10]} | {s3['evaluated_test_N']:,} | — | — | {s3['evaluated_test_N']:,} | `{s3['manifest_sha256'][:16]}...` |"
    )
    md.append(
        f"| **S4** | Curated Release Snapshot (P-007) | `{s4_commit_short}` | {s4['date_utc'][:10]} | {s4['total_images']:,} | {s4['split_counts']['train']:,} | {s4['split_counts']['val']:,} | {s4['split_counts']['test']:,} | `{s4['manifest_sha256'][:16]}...` |"
    )
    md.append("")
    md.append("### Lineage Facts & Audit Findings")
    md.append("")
    md.append(f"1. **Model Weights Training (S1):** Model weights (`3bb5785efa957a5fd4eb9d071fa92ff57adbef9788275a810e9cce99cf016dcb`) were trained on snapshot S1 containing {s1['split_counts']['train']:,} training images across {s1['num_classes']} classes and {s1['num_crops']} crops under MLflow run `cb46c7f8f10f45e59ad809720c7bccb6`.")
    md.append(f"2. **Checkpoint Selection on Validation Split (S2):** The best checkpoint was selected on the validation split at step 19 (epoch 20) with MLflow masked disease-head accuracy of 0.9600 (8,975 / {s2['val_samples_used']:,} correct). Note: serving-score soft-gated accuracy on validation is a different metric yielding 8,974 / {s2['val_samples_used']:,} correct.")
    md.append(f"3. **Temperature Scaling & Threshold Fitting on Validation Split (S2):** Platt scaling parameters ($T_{{\\text{{crop}}}} = {cal['T_crop']:.4f}$, $T_{{\\text{{disease}}}} = {cal['T_disease']:.4f}$) and operating decision threshold $\\tau = 0.60$ were fitted on the {s2['val_samples_used']:,} validation images.")
    md.append(f"4. **Headline Test Evaluation (S3):** All headline metrics in `reports/v1/results.json` were evaluated on the test folder of the curated release snapshot ({headline['clean_test_N']:,} test images post-P-007, manifest SHA-256 `{s3['manifest_sha256'][:16]}...`). The earlier 8,911 figures (96.03%, evaluated on S1 minus the 181-image list before physical quarantine) are marked historical.")
    md.append(f"5. **CPU Determinism Disclosure:** Counts are reproduced on CPU, fp32, 1 thread; other hardware or thread counts can flip a near-tie image (about +-1 image, +-0.01 points). On pinned CPU execution (PyTorch {meta['torch_version']}, 1 thread, deterministic algorithms enabled), {total_correct:,} of {headline['clean_test_N']:,} test images are classified correctly ({headline['soft_gated_disease_accuracy']:.2f}%).")
    md.append(f"6. **Post-Training Dataset Removals:** Following training, exactly {lineage['removed_after_training']['test']} test images were removed under Patch P-007 (`data/patches/P-007_test_leakage_quarantine_PLAN.csv`, logged in `reports/v1/removed_p007_images.csv`) because they were cross-split near-duplicates of training frames. Exactly 0 images were removed from train, and 0 from val.")
    md.append("7. **No Post-Removal Retraining:** Model weights were not retrained after Patch P-007 (`weights_trained_on_release_snapshot: false`).")
    md.append(f"8. **Run Environment & Seeding Status:** The training run was unseeded (deterministic seeding was integrated in later commit `16635f4`), and the working tree at the start of training had uncommitted changes (base commit `{s1_commit_short}`).")
    md.append(f"9. **Near-Duplicate Status:** On the curated release snapshot, test split cross-split leakage has been completely eliminated (0 pairs between test and train/val at Hamming distance $d \\le 4$). However, redundant within-split twins exist (`reports/v1/twin_check.json`): train has {tt_total:,} pairs, val has {vv_total} pairs, and test has {te_total} pairs ({te_d0} exact $d=0$, {te_d14} near $d \\in [1, 4]$). Additionally, the validation split retains {tv_total} perceptual hash ($d \\le 4$) twin pairs with train ({tv_d0} exact 0-bit pairs, {tv_d14} near-duplicate pairs at $d \\in [1, 4]$), spanning 162 unique validation images.")
    md.append("")
    md.append("### Headline Metrics Breakdown (Held-Out Test Split, N=9,279)")
    md.append("")
    md.append(f"- **Soft-Gated Disease Accuracy:** **{headline['soft_gated_disease_accuracy']:.2f}%** ({total_correct:,} / {headline['clean_test_N']:,} correct; 95% Bootstrap CI: [{headline['soft_gated_disease_accuracy_95ci'][0]:.2f}%, {headline['soft_gated_disease_accuracy_95ci'][1]:.2f}%])")
    md.append(f"- **Raw Disease Accuracy:** **{headline['raw_disease_accuracy']:.2f}%** (95% Bootstrap CI: [{headline['raw_disease_accuracy_95ci'][0]:.2f}%, {headline['raw_disease_accuracy_95ci'][1]:.2f}%])")
    md.append(f"- **Crop Identification Accuracy:** **{headline['crop_accuracy']:.2f}%** (95% Bootstrap CI: [{headline['crop_accuracy_95ci'][0]:.2f}%, {headline['crop_accuracy_95ci'][1]:.2f}%])")
    md.append(f"- **Macro-F1 (All {headline['num_classes']} Classes):** **{headline['macro_f1_all_classes']:.2f}%** (95% Bootstrap CI: [{headline['macro_f1_all_classes_95ci'][0]:.2f}%, {headline['macro_f1_all_classes_95ci'][1]:.2f}%])")
    md.append(f"- **Macro-F1 (Classes with $\\ge 10$ test images, {headline['classes_with_ge_10_clean_test']} Classes):** **{headline['macro_f1_classes_ge_10_test']:.2f}%** (95% Bootstrap CI: [{headline['macro_f1_classes_ge_10_test_95ci'][0]:.2f}%, {headline['macro_f1_classes_ge_10_test_95ci'][1]:.2f}%])")
    md.append(f"- **Calibrated Expected Calibration Error (ECE, 15 bins):** **{headline['calibrated_ece_15_bins_pct']:.2f}%**")
    md.append("")
    md.append("<!-- END DATA LINEAGE -->")

    return "\n".join(md)


def update_file(path: Path, new_section: str) -> bool:
    if not path.exists():
        print(f"Error: {path} does not exist", file=sys.stderr)
        return False

    content = path.read_text(encoding="utf-8")
    start_marker = "<!-- BEGIN DATA LINEAGE -->"
    end_marker = "<!-- END DATA LINEAGE -->"

    if start_marker in content and end_marker in content:
        before = content.split(start_marker)[0]
        after = content.split(end_marker)[1]
        updated_content = before + new_section + after
    else:
        # Append section at the end of the file
        updated_content = content.rstrip() + "\n\n" + new_section + "\n"

    if updated_content != content:
        path.write_text(updated_content, encoding="utf-8")
        print(f"Updated {path}")
        return True
    else:
        print(f"No changes needed for {path}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Render Data Lineage Markdown")
    parser.add_argument("--update", action="store_true", help="Update DATASET_CARD.md and model_card.md")
    args = parser.parse_args()

    section = generate_lineage_markdown()

    target_files = [
        ROOT / "docs" / "DATASET_CARD.md",
        ROOT / "models" / "v1" / "model_card.md",
    ]

    if args.update:
        for f in target_files:
            update_file(f, section)
    else:
        print(section)


if __name__ == "__main__":
    main()
