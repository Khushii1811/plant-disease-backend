# Hale Documentation Index

Comprehensive technical documentation, data provenance records, and engineering guides for the Hale foliar plant leaf disease classification system.

---

## 🌟 Flagship Engineering Essays (Must-Read Deep Dives)

Written from first principles during development, these two long-form essays document the end-to-end reality of curating a massive real-world dataset and designing modern vision models under tight consumer hardware constraints:

### 1. [The Data-Centric Odyssey: How I Built a 99,775-Image Foliar Pathology Benchmark Without Losing My Mind](essays/DATA_CENTRIC_ODYSSEY_DOCUMENTARY.md)
*Part 1: Forensic data engineering, burst-photo leakage detection, and real-world curation lessons.*
> *"Everyone wants to build the Ferrari of neural network architectures. Almost nobody wants to change the muddy, flat tires of the dataset."*

- **The 99.4% Benchmark Illusion:** Why public computer vision benchmarks give inflated accuracy, and what happens when raw pixels are inspected: burst-shot duplicate leaves, paper figure collages, and tractors dumped into pathology folders.
- **The "Sanctity of Raw Data" & Quarantine Architecture:** Operating on a strict "Never `rm -rf`" philosophy—treating raw inputs as immutable and tracking every relabel, merge, and quarantine through auditable, reversible logs.
- **The Web Scraping Trap:** The temptation of dataset quantity over quality, and the decision to purge 11,000 scraped garbage images that lacked diagnostic pathology signal.
- **The "Missing Healthy" Blindspot:** Why open-source datasets collect only "exciting sickness" while neglecting healthy controls, and how 100% negative control baselines were enforced across all 34 botanical crop families.
- **Multi-Tier Cryptographic & Perceptual Leakage Defense:** Exposing why exact byte hashing (MD5/SHA-256) is blind to handheld camera bursts, and deploying 64-bit DCT perceptual hashing (`pHash` $d \le 4$) alongside deep CNN feature clustering to catch twin frames across splits.
- **The Paddy Case Study ("Hall of Mirrors"):** Uncovering identical photographic frames labeled with conflicting disease diagnoses, resolving resolution loss from wide-angle canopy shots, and the discipline to discard bad data.

### 2. [Chlorophyll & Convolutions: Designing a 177-Class Plant Disease Classifier Under 4GB VRAM Constraints](essays/CHLOROPHYLL_AND_CONVOLUTIONS.md)
*Part 2: Deep learning architecture, hardware constraints, and biological domain realities.*
> *"Most tutorials in agricultural deep learning follow an identical, naive playbook... In real-world deployment, however, that assumption collapses."*

- **The 4GB GPU Reality:** Why Vision Transformers (quadratic activation memory) and heavy legacy CNNs fail on an NVIDIA RTX 3050 Laptop GPU, and why ConvNeXt-Tiny's $7 \times 7$ depthwise kernels and LayerNorm provide the ideal spatial receptive field for lesion margins at `batch_size=16`.
- **Botany Behind Data Augmentations:** How standard computer vision transforms corrupt biological ground truth (hue jitter turns healthy leaves into nitrogen deficiency; extreme crops erase lesion halos), and how a pathology-preserving augmentation pipeline was established.
- **Hierarchical Dual-Head Architecture:** Replacing naive flat softmax with a shared-trunk dual head (host crop + foliar condition) that structures the hypothesis space to prevent cross-species hallucinations (e.g. diagnosing Apple Scab on a Potato leaf).
- **Two-Phase Staged Training Recipe:** Step-by-step training mechanics utilizing FP16 mixed precision, 3-epoch head warmup, and layer-wise learning rate decay across Stages 2–3 to train 28.6M parameters without CUDA Out-Of-Memory crashes.

---

## Core Technical Specifications & Lineage Records

Quick reference documents for engineers, auditors, and API integrators:

| Document | What It Contains | Who Should Read It |
|:---|:---|:---|
| [FEATURES_GUIDE.md](FEATURES_GUIDE.md) | Architecture, calibration, selective classification, features, guardrails | ML engineers and API consumers |
| [PATCH_LINEAGE.md](PATCH_LINEAGE.md) | Dataset history P-001 to P-007, Patch P-005 curation and evidence dossier, leakage, residual risks | Data scientists, reproducibility reviewers, and plant pathologists |
| [DATASET_CARD.md](DATASET_CARD.md) | Dataset contents, splits, sources | ML researchers and benchmark evaluators |
| [DATASET_LICENSE.md](DATASET_LICENSE.md) | Licences and withdrawn classes | Legal, compliance, and open-source reviewers |

---

## Recommended Reading Tracks

Choose the track based on your role and time:

### ⚡ Track A: Technical Specification Path (Fast Track — 5 to 10 Minutes)
For ML engineers, API consumers, and benchmark evaluators who need technical parameters, deployment guardrails, and provenance proofs:
1. [Main README](../README.md) — Problem statement, headline results, and quickstart.
2. [FEATURES_GUIDE.md](FEATURES_GUIDE.md) — Architecture, temperature calibration, selective abstention ($\tau=0.60$), and operational guardrails.
3. [PATCH_LINEAGE.md](PATCH_LINEAGE.md) — Chronological patch history P-001 to P-007, Patch P-005 evidence dossier, and cryptographic leak checks.
4. [DATASET_CARD.md](DATASET_CARD.md) — Dataset composition, split distributions, and botanical sources.
5. [DATASET_LICENSE.md](DATASET_LICENSE.md) — Upstream licensing terms, non-commercial restrictions, and withdrawn classes.

### 🌿 Track B: The Engineering Journey (Deep-Dive Narrative)
For practitioners and researchers wanting the full behind-the-scenes story of building a production vision system from scratch:
1. [The Data-Centric Odyssey](essays/DATA_CENTRIC_ODYSSEY_DOCUMENTARY.md) — Part 1: How messy real-world datasets were investigated, duplicate leaks were tracked, and a ~100k-image foliar benchmark was forged.
2. [Chlorophyll & Convolutions](essays/CHLOROPHYLL_AND_CONVOLUTIONS.md) — Part 2: How a 177-class ConvNeXt-Tiny DualHead architecture was engineered under strict 4GB VRAM laptop constraints.

---

> **Authority Notice:** If numbers differ between documents, `PATCH_LINEAGE.md` and `reports/v1/results.json` are authoritative.
