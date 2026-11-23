# Model Card: ConvNeXt-Tiny DualHead (Model v1.0)

**Model Version:** Model v1.0 (Public Release)  
**Trained On:** Dataset v1.0 (`reports/v1/dataset_v1.csv`, SHA-256: `7267ec4595eff802731eff86618dc79de33820752037ee5e92b88468cda89c30`)  
**Weights File:** `models/v1/model_dualhead_convnext_tiny.pth` (SHA-256: `f28b568b89b089529f8318e2aecd71e6361271bd06c3461e188e6e64b2ea3d04`)  
**Architecture:** ConvNeXt-Tiny DualHead (34 botanical crops, 195 foliar disease classes)  
**Input Resolution:** 256x256 RGB  
**Scope:** Foliar plant leaf disease image classifier. Does not recommend chemical treatments or actuate machinery.

---

## 1. Verified Benchmark Performance

All figures verified directly from `reports/v1/results.json`:

### Purified Test Split (N=9,327, Certified Post Patch P-004)
- **Crop-Gated Disease Accuracy:** **95.27%** (95% Bootstrap CI: [94.83%, 95.70%])
- **Raw Disease Accuracy:** **95.21%**
- **Crop Accuracy:** **99.16%** (95% Bootstrap CI: [98.98%, 99.36%])
- **Headline Macro-F1 (192 Supported Classes):** **93.45%** (95% Bootstrap CI: [91.23%, 93.93%])
- **Secondary Macro-F1 (All 195 Classes, zero_division=0):** **92.01%** (95% Bootstrap CI: [89.83%, 92.48%])
- **Robust Macro-F1 (N >= 20, 116 Classes):** **96.65%**
- **Calibrated ECE:** **0.76%** ($T_{\text{crop}} = 0.6356$, $T_{\text{disease}} = 0.5327$)
> *Note: Confidence intervals assume independent images.*

- **Zero-Support Test Classes:**
  - `Jamun - Bacterial Spot` (N=0)
  - `Jamun - Brown Blight` (N=0)
  - `Jamun - Healthy` (N=0)

### Historical Full Split (N=10,426, Reference Only)
- **Crop-Gated Disease Accuracy:** 95.66%
- **Raw Disease Accuracy:** 95.61%
- **Crop Accuracy:** 99.23%
- **Macro-F1:** 93.58%
- **Calibrated ECE:** 0.40%

---

## 2. In-The-Wild Field Generalization (N=43 Citrus Field Images)
- **Field Top-1 Accuracy:** **41.86%** (18/43, with and without EXIF transposition)
- **Wilson 95% Confidence Interval:** **[28.38%, 56.67%]**
- **Thresholded Field Performance ($	au^* = 0.60$):**
  - **Coverage:** 44.19% (19/43 images with calibrated confidence $\ge 0.60$)
  - **Covered Accuracy:** **68.42%** (13/19, Wilson 95% CI: [46.01%, 84.64%])
  - **Uncertain Subset Accuracy:** 20.83% (5/24 flagged as `uncertain`)
- **Per-Class Breakdown:**
  - `Citrus - citrus canker`: 13/13 (100.0%)
  - `Citrus - citrus greening disease`: 4/11 (36.4%)
  - `Citrus - citrus scab`: 1/5 (20.0%)
  - `Citrus - Black spot`: 0/8 (0.0% recall, misdiagnosed as canker or other leaf spots)
  - `Citrus - Healthy`: 0/6 (0.0% recall)

---

## 3. Operational Limitations & Risk Factors

1. **Research Baseline Status:** High test accuracy (95.27%) reflects curated in-distribution benchmark splits. Outdoor field testing shows severe performance drop (41.86%).
2. **Guava Upstream Inconsistency & Multi-Symptom Leaves:** Upstream label inconsistency in Guava classes led to 700 images being quarantined under Patch P-004 across 7 classes (Anthracnose: 59, Canker: 90, Dot: 163, Healthy: 151, Mummification: 2, Rust: 150, Spiraling Whitefly: 85). Because ambiguous multi-symptom leaves were removed, the test set is simplified for these categories and does not evaluate performance on multi-symptom leaves.
3. **Out-of-Distribution Handling:** The model lacks OOD detection. Synthetic green or gray images receive low-confidence predictions flagged as `uncertain` by the serving API (threshold $\tau^* = 0.60$).
4. **Laboratory Concentration:** 43.6% of active images are from laboratory datasets on plain backgrounds.
5. **Post-Training Deduplication:** 571 training images were quarantined after model training; weights reflect exposure to original data.
6. **Class Support Imbalance:** 21 classes have <5 test images.

---

## 4. Complete Per-Class Support and Test F1-Score (195 Classes)

| # | Botanical Host Crop | Standardized Disease Class | Test Support (N) | Test F1-Score |
|:---:|:---|:---|:---:|:---:|
| 1 | **Apple** | `Apple - Healthy` | 51 | 99.01% |
| 2 | **Apple** | `Apple - Rust` | 42 | 98.82% |
| 3 | **Apple** | `Apple - apple alternaria leaf spot` | 52 | 100.00% |
| 4 | **Apple** | `Apple - apple black rot` | 48 | 100.00% |
| 5 | **Apple** | `Apple - apple mosaic virus` | 3 | 100.00% |
| 6 | **Apple** | `Apple - apple scab` | 39 | 100.00% |
| 7 | **Banana** | `Banana - Cordana` | 31 | 86.11% |
| 8 | **Banana** | `Banana - Healthy` | 96 | 100.00% |
| 9 | **Banana** | `Banana - Insectpest` | 68 | 96.45% |
| 10 | **Banana** | `Banana - Moko` | 44 | 98.88% |
| 11 | **Banana** | `Banana - Panama` | 111 | 94.78% |
| 12 | **Banana** | `Banana - Pestalotiopsis` | 52 | 95.41% |
| 13 | **Banana** | `Banana - Sigatoka` | 370 | 94.30% |
| 14 | **Banana** | `Banana - banana black leaf streak` | 7 | 50.00% |
| 15 | **Banana** | `Banana - banana bunchy top` | 14 | 90.32% |
| 16 | **Bean** | `Bean - Healthy` | 32 | 96.97% |
| 17 | **Bean** | `Bean - bean angular leaf spot` | 32 | 100.00% |
| 18 | **Bean** | `Bean - bean halo blight` | 4 | 28.57% |
| 19 | **Bean** | `Bean - bean leaf shot hole` | 19 | 100.00% |
| 20 | **Bean** | `Bean - bean mosaic virus` | 4 | 28.57% |
| 21 | **Bean** | `Bean - bean rust` | 46 | 88.37% |
| 22 | **Bell Pepper** | `Bell Pepper - Bacterial Spot` | 108 | 96.77% |
| 23 | **Bell Pepper** | `Bell Pepper - Healthy` | 134 | 98.88% |
| 24 | **Bell Pepper** | `Bell Pepper - bell pepper frogeye leaf spot` | 126 | 94.12% |
| 25 | **Blackgram** | `Blackgram - Anthracnose` | 23 | 97.87% |
| 26 | **Blackgram** | `Blackgram - Healthy` | 22 | 100.00% |
| 27 | **Blackgram** | `Blackgram - Leaf Crinkle` | 15 | 100.00% |
| 28 | **Blackgram** | `Blackgram - Powdery Mildew` | 17 | 97.14% |
| 29 | **Blackgram** | `Blackgram - Yellow Mosaic` | 23 | 97.87% |
| 30 | **Blueberry** | `Blueberry - Healthy` | 52 | 99.05% |
| 31 | **Blueberry** | `Blueberry - blueberry rust` | 4 | 88.89% |
| 32 | **Blueberry** | `Blueberry - blueberry scorch` | 3 | 100.00% |
| 33 | **Broccoli** | `Broccoli - Healthy` | 2 | 100.00% |
| 34 | **Broccoli** | `Broccoli - broccoli alternaria leaf spot` | 3 | 80.00% |
| 35 | **Cabbage** | `Cabbage - Healthy` | 7 | 93.33% |
| 36 | **Cabbage** | `Cabbage - Tip Burn` | 2 | 100.00% |
| 37 | **Cabbage** | `Cabbage - cabbage alternaria leaf spot` | 7 | 54.55% |
| 38 | **Cabbage** | `Cabbage - cabbage black rot` | 11 | 76.92% |
| 39 | **Cabbage** | `Cabbage - cabbage downy mildew` | 8 | 80.00% |
| 40 | **Cauliflower** | `Cauliflower - Blackrot` | 4 | 100.00% |
| 41 | **Cauliflower** | `Cauliflower - Downy mildew` | 15 | 96.77% |
| 42 | **Cauliflower** | `Cauliflower - Healthy` | 16 | 100.00% |
| 43 | **Cherry** | `Cherry - Healthy` | 61 | 98.36% |
| 44 | **Cherry** | `Cherry - cherry brown spot` | 55 | 100.00% |
| 45 | **Cherry** | `Cherry - cherry leaf scorch` | 57 | 99.12% |
| 46 | **Cherry** | `Cherry - cherry leaf spot` | 8 | 62.50% |
| 47 | **Cherry** | `Cherry - cherry powdery mildew` | 30 | 100.00% |
| 48 | **Cherry** | `Cherry - cherry purple leaf spot` | 55 | 100.00% |
| 49 | **Cherry** | `Cherry - cherry shot hole` | 18 | 100.00% |
| 50 | **Chilli** | `Chilli - Bacterial Spot` | 11 | 95.65% |
| 51 | **Chilli** | `Chilli - Cercospora Leaf Spot` | 15 | 93.33% |
| 52 | **Chilli** | `Chilli - Healthy` | 32 | 100.00% |
| 53 | **Chilli** | `Chilli - Leaf Curl Virus` | 39 | 100.00% |
| 54 | **Chilli** | `Chilli - Nutrition Deficiency` | 41 | 100.00% |
| 55 | **Chilli** | `Chilli - White Spot` | 14 | 100.00% |
| 56 | **Citrus** | `Citrus - Black spot` | 12 | 100.00% |
| 57 | **Citrus** | `Citrus - Healthy` | 41 | 100.00% |
| 58 | **Citrus** | `Citrus - citrus algal leaf spot` | 16 | 100.00% |
| 59 | **Citrus** | `Citrus - citrus canker` | 37 | 92.11% |
| 60 | **Citrus** | `Citrus - citrus greening disease` | 71 | 97.90% |
| 61 | **Citrus** | `Citrus - citrus scab` | 8 | 100.00% |
| 62 | **Coffee** | `Coffee - Healthy` | 33 | 100.00% |
| 63 | **Coffee** | `Coffee - Leaf Miner` | 35 | 97.14% |
| 64 | **Coffee** | `Coffee - Phoma` | 36 | 95.89% |
| 65 | **Coffee** | `Coffee - coffee leaf rust` | 42 | 96.30% |
| 66 | **Corn** | `Corn - Healthy` | 116 | 100.00% |
| 67 | **Corn** | `Corn - Northern Leaf Blight` | 87 | 92.49% |
| 68 | **Corn** | `Corn - Rust` | 51 | 97.09% |
| 69 | **Corn** | `Corn - corn gray leaf spot` | 54 | 88.07% |
| 70 | **Corn** | `Corn - corn holcus leaf spot` | 15 | 96.77% |
| 71 | **Cucumber** | `Cucumber - Healthy` | 15 | 100.00% |
| 72 | **Cucumber** | `Cucumber - cucumber angular leaf spot` | 19 | 87.80% |
| 73 | **Cucumber** | `Cucumber - cucumber bacterial wilt` | 25 | 100.00% |
| 74 | **Cucumber** | `Cucumber - cucumber powdery mildew` | 16 | 83.87% |
| 75 | **Eggplant** | `Eggplant - Cercospora Leaf Spot` | 20 | 91.89% |
| 76 | **Eggplant** | `Eggplant - Healthy` | 20 | 97.56% |
| 77 | **Eggplant** | `Eggplant - Little Leaf` | 18 | 100.00% |
| 78 | **Eggplant** | `Eggplant - Mosaic Virus` | 14 | 93.33% |
| 79 | **Eggplant** | `Eggplant - White Mold` | 20 | 97.56% |
| 80 | **Eggplant** | `Eggplant - Wilt` | 19 | 100.00% |
| 81 | **Fig** | `Fig - Healthy` | 21 | 95.24% |
| 82 | **Fig** | `Fig - fig brown spot` | 16 | 100.00% |
| 83 | **Fig** | `Fig - fig leaf blight` | 35 | 100.00% |
| 84 | **Fig** | `Fig - fig rust` | 21 | 100.00% |
| 85 | **Ginger** | `Ginger - Bacterial Wilt` | 9 | 94.12% |
| 86 | **Ginger** | `Ginger - Dehydrated` | 260 | 79.21% |
| 87 | **Ginger** | `Ginger - Healthy` | 108 | 82.50% |
| 88 | **Ginger** | `Ginger - Leaf Blight` | 215 | 83.29% |
| 89 | **Ginger** | `Ginger - Pest Damage` | 87 | 67.83% |
| 90 | **Ginger** | `Ginger - ginger leaf spot` | 2 | 100.00% |
| 91 | **Ginger** | `Ginger - ginger sheath blight` | 6 | 90.91% |
| 92 | **Grape** | `Grape - Black Rot` | 24 | 97.96% |
| 93 | **Grape** | `Grape - Esca (Black Measles)` | 50 | 98.99% |
| 94 | **Grape** | `Grape - Healthy` | 25 | 100.00% |
| 95 | **Grape** | `Grape - Leaf Blight` | 14 | 100.00% |
| 96 | **Grape** | `Grape - grape bacterial rot` | 10 | 100.00% |
| 97 | **Grape** | `Grape - grape downy mildew` | 96 | 98.95% |
| 98 | **Grape** | `Grape - grape leafroll disease` | 6 | 85.71% |
| 99 | **Grape** | `Grape - grape powdery mildew` | 39 | 97.50% |
| 100 | **Groundnut** | `Groundnut - Early leaf spot` | 111 | 97.37% |
| 101 | **Groundnut** | `Groundnut - Early rust` | 126 | 100.00% |
| 102 | **Groundnut** | `Groundnut - Healthy` | 25 | 100.00% |
| 103 | **Groundnut** | `Groundnut - Late leaf spot` | 177 | 98.57% |
| 104 | **Groundnut** | `Groundnut - Nutrition deficiency` | 155 | 100.00% |
| 105 | **Groundnut** | `Groundnut - Rust` | 147 | 100.00% |
| 106 | **Guava** | `Guava - Anthracnose` | 23 | 100.00% |
| 107 | **Guava** | `Guava - Canker` | 108 | 98.13% |
| 108 | **Guava** | `Guava - Dot` | 80 | 86.90% |
| 109 | **Guava** | `Guava - Healthy` | 190 | 95.42% |
| 110 | **Guava** | `Guava - Mummification` | 28 | 96.55% |
| 111 | **Guava** | `Guava - Rust` | 83 | 97.04% |
| 112 | **Guava** | `Guava - Spiraling Whitefly` | 79 | 98.72% |
| 113 | **Jamun** | `Jamun - Bacterial Spot` | 0 | N/A (N=0) |
| 114 | **Jamun** | `Jamun - Brown Blight` | 0 | N/A (N=0) |
| 115 | **Jamun** | `Jamun - Healthy` | 0 | N/A (N=0) |
| 116 | **Jamun** | `Jamun - Powdery Mildew` | 4 | 100.00% |
| 117 | **Jamun** | `Jamun - Sooty Mold` | 11 | 100.00% |
| 118 | **Mango** | `Mango - Anthracnose` | 49 | 100.00% |
| 119 | **Mango** | `Mango - Bacterial Canker` | 49 | 100.00% |
| 120 | **Mango** | `Mango - Cutting Weevil` | 50 | 100.00% |
| 121 | **Mango** | `Mango - Die Back` | 47 | 100.00% |
| 122 | **Mango** | `Mango - Gall Midge` | 50 | 100.00% |
| 123 | **Mango** | `Mango - Healthy` | 47 | 100.00% |
| 124 | **Mango** | `Mango - Powdery Mildew` | 50 | 100.00% |
| 125 | **Mango** | `Mango - Sooty Mould` | 50 | 100.00% |
| 126 | **Paddy** | `Paddy - Bacterial Leaf Blight` | 5 | 100.00% |
| 127 | **Paddy** | `Paddy - Blast` | 19 | 94.44% |
| 128 | **Paddy** | `Paddy - Brown Spot` | 19 | 92.31% |
| 129 | **Paddy** | `Paddy - Healthy` | 35 | 98.59% |
| 130 | **Paddy** | `Paddy - Leaf Scald` | 5 | 100.00% |
| 131 | **Paddy** | `Paddy - Narrow Brown Spot` | 2 | 100.00% |
| 132 | **Peach** | `Peach - Healthy` | 39 | 100.00% |
| 133 | **Peach** | `Peach - peach bacterial spot` | 60 | 100.00% |
| 134 | **Peach** | `Peach - peach leaf curl` | 13 | 96.30% |
| 135 | **Peach** | `Peach - peach leaf shot hole` | 3 | 85.71% |
| 136 | **Pear** | `Pear - Healthy` | 41 | 97.56% |
| 137 | **Pear** | `Pear - pear black spot` | 128 | 95.06% |
| 138 | **Pear** | `Pear - pear fire blight` | 18 | 100.00% |
| 139 | **Pear** | `Pear - pear leaf curl` | 6 | 85.71% |
| 140 | **Pear** | `Pear - pear slug damage` | 172 | 97.02% |
| 141 | **Plum** | `Plum - Healthy` | 13 | 86.67% |
| 142 | **Plum** | `Plum - plum insect hole` | 71 | 94.03% |
| 143 | **Plum** | `Plum - plum weevil` | 10 | 100.00% |
| 144 | **Plum** | `Plum - plum yellow leaf` | 76 | 97.44% |
| 145 | **Potato** | `Potato - Early Blight` | 136 | 94.81% |
| 146 | **Potato** | `Potato - Healthy` | 45 | 98.90% |
| 147 | **Potato** | `Potato - Late Blight` | 144 | 96.53% |
| 148 | **Potato** | `Potato - fungal diseases` | 41 | 94.12% |
| 149 | **Potato** | `Potato - pest damage` | 31 | 95.08% |
| 150 | **Potato** | `Potato - potato cyst nematode` | 24 | 94.12% |
| 151 | **Potato** | `Potato - potato virus` | 27 | 98.11% |
| 152 | **Radish** | `Radish - Black leaf spot` | 35 | 100.00% |
| 153 | **Radish** | `Radish - Downey mildew` | 43 | 100.00% |
| 154 | **Radish** | `Radish - Flea beetle` | 33 | 100.00% |
| 155 | **Radish** | `Radish - Healthy` | 46 | 100.00% |
| 156 | **Radish** | `Radish - Mosaic` | 42 | 98.82% |
| 157 | **Soybean** | `Soybean - Bacterial Blight` | 17 | 90.91% |
| 158 | **Soybean** | `Soybean - Bacterial Pustule` | 11 | 100.00% |
| 159 | **Soybean** | `Soybean - Brown Spot` | 3 | 75.00% |
| 160 | **Soybean** | `Soybean - Cercospora Leaf Blight` | 7 | 100.00% |
| 161 | **Soybean** | `Soybean - Downy Mildew` | 6 | 70.59% |
| 162 | **Soybean** | `Soybean - Frogeye Leaf Spot` | 18 | 87.18% |
| 163 | **Soybean** | `Soybean - Healthy` | 57 | 98.25% |
| 164 | **Soybean** | `Soybean - Powdery Mildew` | 10 | 95.24% |
| 165 | **Soybean** | `Soybean - Rust` | 24 | 86.96% |
| 166 | **Soybean** | `Soybean - Sudden Death Syndrome` | 11 | 95.65% |
| 167 | **Soybean** | `Soybean - Target Leaf Spot` | 11 | 91.67% |
| 168 | **Soybean** | `Soybean - Yellow Mosaic` | 11 | 100.00% |
| 169 | **Strawberry** | `Strawberry - Healthy` | 50 | 100.00% |
| 170 | **Strawberry** | `Strawberry - strawberry angular leaf spot` | 25 | 92.59% |
| 171 | **Strawberry** | `Strawberry - strawberry leaf scorch` | 44 | 98.88% |
| 172 | **Strawberry** | `Strawberry - strawberry leaf spot` | 20 | 90.48% |
| 173 | **Strawberry** | `Strawberry - strawberry powdery mildew` | 51 | 100.00% |
| 174 | **Sugarcane** | `Sugarcane - Healthy` | 12 | 100.00% |
| 175 | **Sugarcane** | `Sugarcane - Mosaic` | 2 | 80.00% |
| 176 | **Sugarcane** | `Sugarcane - Red Rot` | 20 | 95.24% |
| 177 | **Sugarcane** | `Sugarcane - Rust` | 4 | 66.67% |
| 178 | **Sugarcane** | `Sugarcane - Yellow` | 9 | 94.12% |
| 179 | **Tomato** | `Tomato - Bacterial Spot` | 220 | 93.68% |
| 180 | **Tomato** | `Tomato - Healthy` | 150 | 98.34% |
| 181 | **Tomato** | `Tomato - Spider Mites` | 167 | 94.01% |
| 182 | **Tomato** | `Tomato - Target Spot` | 141 | 93.33% |
| 183 | **Tomato** | `Tomato - tomato early blight` | 99 | 95.96% |
| 184 | **Tomato** | `Tomato - tomato late blight` | 195 | 97.44% |
| 185 | **Tomato** | `Tomato - tomato leaf mold` | 109 | 95.19% |
| 186 | **Tomato** | `Tomato - tomato mosaic virus` | 43 | 89.58% |
| 187 | **Tomato** | `Tomato - tomato septoria leaf spot` | 181 | 99.45% |
| 188 | **Tomato** | `Tomato - tomato yellow leaf curl virus` | 325 | 96.33% |
| 189 | **Zucchini** | `Zucchini - Healthy` | 6 | 83.33% |
| 190 | **Zucchini** | `Zucchini - zucchini angular leaf spot` | 8 | 66.67% |
| 191 | **Zucchini** | `Zucchini - zucchini anthracnose` | 4 | 54.55% |
| 192 | **Zucchini** | `Zucchini - zucchini bacterial leaf spot` | 2 | 50.00% |
| 193 | **Zucchini** | `Zucchini - zucchini downy mildew` | 12 | 63.16% |
| 194 | **Zucchini** | `Zucchini - zucchini powdery mildew` | 16 | 83.87% |
| 195 | **Zucchini** | `Zucchini - zucchini yellow mosaic virus` | 18 | 91.43% |
