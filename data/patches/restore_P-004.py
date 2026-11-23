"""Restore script for Patch P-004."""
import shutil
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
def restore():
    restored = 0
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Apple - apple alternaria leaf spot/plantcity_apple_apple_alternaria_leaf_spot_test_00025.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Apple - apple alternaria leaf spot/plantcity_apple_apple_alternaria_leaf_spot_test_00025.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Apple - apple alternaria leaf spot/plantcity_apple_apple_alternaria_leaf_spot_test_00056.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Apple - apple alternaria leaf spot/plantcity_apple_apple_alternaria_leaf_spot_test_00056.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Banana - Healthy/img_00046870.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Banana - Healthy/img_00046870.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Banana - Panama/img_00049168.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Banana - Panama/img_00049168.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Banana - Pestalotiopsis/img_00061428.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Banana - Pestalotiopsis/img_00061428.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Banana - Sigatoka/img_00046701.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Banana - Sigatoka/img_00046701.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Banana - Sigatoka/img_00062628.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Banana - Sigatoka/img_00062628.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Bell Pepper - Healthy/img_00027265.JPG"
    dst_p = PROJECT_ROOT / "data/processed/test/Bell Pepper - Healthy/img_00027265.JPG"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Bell Pepper - Healthy/img_00027271.JPG"
    dst_p = PROJECT_ROOT / "data/processed/test/Bell Pepper - Healthy/img_00027271.JPG"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Bell Pepper - Healthy/img_00027361.JPG"
    dst_p = PROJECT_ROOT / "data/processed/test/Bell Pepper - Healthy/img_00027361.JPG"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Bell Pepper - Healthy/img_00027769.JPG"
    dst_p = PROJECT_ROOT / "data/processed/test/Bell Pepper - Healthy/img_00027769.JPG"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Bell Pepper - Healthy/img_00027948.JPG"
    dst_p = PROJECT_ROOT / "data/processed/test/Bell Pepper - Healthy/img_00027948.JPG"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Bell Pepper - bell pepper frogeye leaf spot/bell_pepper_frogeye_mendeley_test_00011.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Bell Pepper - bell pepper frogeye leaf spot/bell_pepper_frogeye_mendeley_test_00011.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Bell Pepper - bell pepper frogeye leaf spot/bell_pepper_frogeye_mendeley_test_00015.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Bell Pepper - bell pepper frogeye leaf spot/bell_pepper_frogeye_mendeley_test_00015.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Bell Pepper - bell pepper frogeye leaf spot/bell_pepper_frogeye_mendeley_test_00019.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Bell Pepper - bell pepper frogeye leaf spot/bell_pepper_frogeye_mendeley_test_00019.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Bell Pepper - bell pepper frogeye leaf spot/bell_pepper_frogeye_mendeley_test_00035.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Bell Pepper - bell pepper frogeye leaf spot/bell_pepper_frogeye_mendeley_test_00035.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Bell Pepper - bell pepper frogeye leaf spot/bell_pepper_frogeye_mendeley_test_00047.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Bell Pepper - bell pepper frogeye leaf spot/bell_pepper_frogeye_mendeley_test_00047.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Bell Pepper - bell pepper frogeye leaf spot/bell_pepper_frogeye_mendeley_test_00061.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Bell Pepper - bell pepper frogeye leaf spot/bell_pepper_frogeye_mendeley_test_00061.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Bell Pepper - bell pepper frogeye leaf spot/bell_pepper_frogeye_mendeley_test_00071.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Bell Pepper - bell pepper frogeye leaf spot/bell_pepper_frogeye_mendeley_test_00071.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Bell Pepper - bell pepper frogeye leaf spot/bell_pepper_frogeye_mendeley_test_00082.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Bell Pepper - bell pepper frogeye leaf spot/bell_pepper_frogeye_mendeley_test_00082.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Bell Pepper - bell pepper frogeye leaf spot/bell_pepper_frogeye_mendeley_test_00097.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Bell Pepper - bell pepper frogeye leaf spot/bell_pepper_frogeye_mendeley_test_00097.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Bell Pepper - bell pepper frogeye leaf spot/bell_pepper_frogeye_mendeley_test_00103.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Bell Pepper - bell pepper frogeye leaf spot/bell_pepper_frogeye_mendeley_test_00103.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Bell Pepper - bell pepper frogeye leaf spot/bell_pepper_frogeye_mendeley_test_00108.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Bell Pepper - bell pepper frogeye leaf spot/bell_pepper_frogeye_mendeley_test_00108.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Bell Pepper - bell pepper frogeye leaf spot/bell_pepper_frogeye_mendeley_test_00114.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Bell Pepper - bell pepper frogeye leaf spot/bell_pepper_frogeye_mendeley_test_00114.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Bell Pepper - bell pepper frogeye leaf spot/bell_pepper_frogeye_mendeley_test_00121.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Bell Pepper - bell pepper frogeye leaf spot/bell_pepper_frogeye_mendeley_test_00121.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Bell Pepper - bell pepper frogeye leaf spot/bell_pepper_frogeye_mendeley_test_00123.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Bell Pepper - bell pepper frogeye leaf spot/bell_pepper_frogeye_mendeley_test_00123.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Bell Pepper - bell pepper frogeye leaf spot/bell_pepper_frogeye_mendeley_test_00127.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Bell Pepper - bell pepper frogeye leaf spot/bell_pepper_frogeye_mendeley_test_00127.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Cherry - cherry leaf scorch/plantcity_cherry_cherry_leaf_scorch_test_00015.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Cherry - cherry leaf scorch/plantcity_cherry_cherry_leaf_scorch_test_00015.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Chilli - Healthy/chilli_-_healthy_test_00165.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Chilli - Healthy/chilli_-_healthy_test_00165.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Chilli - Nutrition Deficiency/chilli_-_nutrition_deficiency_test_00206.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Chilli - Nutrition Deficiency/chilli_-_nutrition_deficiency_test_00206.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Chilli - Nutrition Deficiency/chilli_-_nutrition_deficiency_test_00227.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Chilli - Nutrition Deficiency/chilli_-_nutrition_deficiency_test_00227.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Chilli - White Spot/chilli_-_white_spot_test_00219.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Chilli - White Spot/chilli_-_white_spot_test_00219.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Citrus - Black spot/sourabh_b (254).png"
    dst_p = PROJECT_ROOT / "data/processed/test/Citrus - Black spot/sourabh_b (254).png"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Citrus - citrus algal leaf spot/2023_08_20_17_20_IMG_5090.JPG"
    dst_p = PROJECT_ROOT / "data/processed/test/Citrus - citrus algal leaf spot/2023_08_20_17_20_IMG_5090.JPG"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Citrus - citrus algal leaf spot/2023_08_21_16_36_IMG_7200.JPG"
    dst_p = PROJECT_ROOT / "data/processed/test/Citrus - citrus algal leaf spot/2023_08_21_16_36_IMG_7200.JPG"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Eggplant - Little Leaf/eggplant_little_leaf_test_00005.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Eggplant - Little Leaf/eggplant_little_leaf_test_00005.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Eggplant - Little Leaf/eggplant_little_leaf_test_00011.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Eggplant - Little Leaf/eggplant_little_leaf_test_00011.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Eggplant - Wilt/eggplant_wilt_test_00018.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Eggplant - Wilt/eggplant_wilt_test_00018.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Ginger - Bacterial Wilt/ginger_bacterial_wilt_test_00003.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Ginger - Bacterial Wilt/ginger_bacterial_wilt_test_00003.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Ginger - Bacterial Wilt/ginger_bacterial_wilt_test_00005.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Ginger - Bacterial Wilt/ginger_bacterial_wilt_test_00005.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Ginger - Bacterial Wilt/ginger_bacterial_wilt_test_00006.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Ginger - Bacterial Wilt/ginger_bacterial_wilt_test_00006.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Ginger - Bacterial Wilt/ginger_bacterial_wilt_test_00008.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Ginger - Bacterial Wilt/ginger_bacterial_wilt_test_00008.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Ginger - Bacterial Wilt/ginger_bacterial_wilt_test_00010.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Ginger - Bacterial Wilt/ginger_bacterial_wilt_test_00010.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Ginger - Bacterial Wilt/ginger_bacterial_wilt_test_00013.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Ginger - Bacterial Wilt/ginger_bacterial_wilt_test_00013.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Ginger - Bacterial Wilt/ginger_bacterial_wilt_test_00015.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Ginger - Bacterial Wilt/ginger_bacterial_wilt_test_00015.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Ginger - Dehydrated/ginger_dehydrated_test_00119.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Ginger - Dehydrated/ginger_dehydrated_test_00119.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Ginger - Dehydrated/ginger_dehydrated_test_00201.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Ginger - Dehydrated/ginger_dehydrated_test_00201.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Ginger - Healthy/ginger_healthy_test_00019.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Ginger - Healthy/ginger_healthy_test_00019.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Ginger - Healthy/ginger_healthy_test_00024.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Ginger - Healthy/ginger_healthy_test_00024.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Ginger - Healthy/ginger_healthy_test_00051.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Ginger - Healthy/ginger_healthy_test_00051.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Ginger - Healthy/ginger_healthy_test_00064.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Ginger - Healthy/ginger_healthy_test_00064.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Ginger - Healthy/ginger_healthy_test_00091.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Ginger - Healthy/ginger_healthy_test_00091.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Ginger - Leaf Blight/ginger_leaf_blight_test_00025.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Ginger - Leaf Blight/ginger_leaf_blight_test_00025.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Ginger - Leaf Blight/ginger_leaf_blight_test_00026.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Ginger - Leaf Blight/ginger_leaf_blight_test_00026.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Ginger - Leaf Blight/ginger_leaf_blight_test_00027.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Ginger - Leaf Blight/ginger_leaf_blight_test_00027.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Ginger - Leaf Blight/ginger_leaf_blight_test_00040.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Ginger - Leaf Blight/ginger_leaf_blight_test_00040.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Ginger - Leaf Blight/ginger_leaf_blight_test_00071.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Ginger - Leaf Blight/ginger_leaf_blight_test_00071.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Ginger - Leaf Blight/ginger_leaf_blight_test_00084.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Ginger - Leaf Blight/ginger_leaf_blight_test_00084.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Ginger - Leaf Blight/ginger_leaf_blight_test_00089.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Ginger - Leaf Blight/ginger_leaf_blight_test_00089.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Ginger - Leaf Blight/ginger_leaf_blight_test_00108.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Ginger - Leaf Blight/ginger_leaf_blight_test_00108.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Ginger - Leaf Blight/ginger_leaf_blight_test_00129.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Ginger - Leaf Blight/ginger_leaf_blight_test_00129.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Ginger - Leaf Blight/ginger_leaf_blight_test_00210.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Ginger - Leaf Blight/ginger_leaf_blight_test_00210.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Ginger - Leaf Blight/ginger_leaf_blight_test_00215.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Ginger - Leaf Blight/ginger_leaf_blight_test_00215.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Ginger - Pest Damage/ginger_pest_damage_test_00071.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Ginger - Pest Damage/ginger_pest_damage_test_00071.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Grape - grape downy mildew/grape_downy_mildew_test_00019.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Grape - grape downy mildew/grape_downy_mildew_test_00019.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Groundnut - Early leaf spot/img_00053029.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Groundnut - Early leaf spot/img_00053029.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Groundnut - Early leaf spot/img_00054770.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Groundnut - Early leaf spot/img_00054770.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Groundnut - Early leaf spot/img_00059303.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Groundnut - Early leaf spot/img_00059303.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Groundnut - Early leaf spot/img_00061926.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Groundnut - Early leaf spot/img_00061926.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Groundnut - Early leaf spot/img_00062475.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Groundnut - Early leaf spot/img_00062475.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Groundnut - Early rust/img_00051062.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Groundnut - Early rust/img_00051062.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Groundnut - Early rust/img_00052271.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Groundnut - Early rust/img_00052271.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Groundnut - Early rust/img_00054897.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Groundnut - Early rust/img_00054897.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Groundnut - Early rust/img_00057485.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Groundnut - Early rust/img_00057485.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Groundnut - Early rust/img_00059662.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Groundnut - Early rust/img_00059662.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Groundnut - Early rust/img_00060049.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Groundnut - Early rust/img_00060049.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Groundnut - Early rust/img_00063955.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Groundnut - Early rust/img_00063955.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Groundnut - Healthy/img_00045716.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Groundnut - Healthy/img_00045716.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Groundnut - Healthy/img_00048976.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Groundnut - Healthy/img_00048976.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Groundnut - Healthy/img_00063183.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Groundnut - Healthy/img_00063183.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Groundnut - Healthy/img_00064283.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Groundnut - Healthy/img_00064283.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Groundnut - Late leaf spot/img_00045556.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Groundnut - Late leaf spot/img_00045556.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Groundnut - Late leaf spot/img_00048512.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Groundnut - Late leaf spot/img_00048512.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Groundnut - Late leaf spot/img_00050794.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Groundnut - Late leaf spot/img_00050794.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Groundnut - Late leaf spot/img_00058490.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Groundnut - Late leaf spot/img_00058490.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Groundnut - Late leaf spot/img_00062379.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Groundnut - Late leaf spot/img_00062379.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Groundnut - Late leaf spot/img_00063105.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Groundnut - Late leaf spot/img_00063105.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Groundnut - Nutrition deficiency/img_00048330.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Groundnut - Nutrition deficiency/img_00048330.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Groundnut - Nutrition deficiency/img_00052795.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Groundnut - Nutrition deficiency/img_00052795.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Groundnut - Nutrition deficiency/img_00055517.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Groundnut - Nutrition deficiency/img_00055517.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Groundnut - Nutrition deficiency/img_00057918.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Groundnut - Nutrition deficiency/img_00057918.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Groundnut - Nutrition deficiency/img_00064961.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Groundnut - Nutrition deficiency/img_00064961.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Groundnut - Rust/img_00064573.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Groundnut - Rust/img_00064573.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Groundnut - Rust/img_00066129.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Groundnut - Rust/img_00066129.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Guava - Anthracnose/mendeley_guava_anthracnose_test_0020.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Anthracnose/mendeley_guava_anthracnose_test_0020.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Guava - Anthracnose/mendeley_guava_anthracnose_test_0023.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Anthracnose/mendeley_guava_anthracnose_test_0023.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Guava - Anthracnose/mendeley_guava_anthracnose_test_0028.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Anthracnose/mendeley_guava_anthracnose_test_0028.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Guava - Anthracnose/mendeley_guava_anthracnose_test_0050.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Anthracnose/mendeley_guava_anthracnose_test_0050.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Guava - Anthracnose/mendeley_guava_anthracnose_test_0062.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Anthracnose/mendeley_guava_anthracnose_test_0062.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Guava - Anthracnose/mendeley_guava_anthracnose_test_0067.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Anthracnose/mendeley_guava_anthracnose_test_0067.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Guava - Anthracnose/mendeley_guava_anthracnose_test_0079.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Anthracnose/mendeley_guava_anthracnose_test_0079.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Guava - Anthracnose/mendeley_guava_anthracnose_test_0080.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Anthracnose/mendeley_guava_anthracnose_test_0080.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Guava - Canker/mendeley_guava_canker_test_0006.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Canker/mendeley_guava_canker_test_0006.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Guava - Canker/mendeley_guava_canker_test_0010.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Canker/mendeley_guava_canker_test_0010.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Guava - Canker/mendeley_guava_canker_test_0020.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Canker/mendeley_guava_canker_test_0020.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Guava - Canker/mendeley_guava_canker_test_0030.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Canker/mendeley_guava_canker_test_0030.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Guava - Canker/mendeley_guava_canker_test_0033.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Canker/mendeley_guava_canker_test_0033.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Guava - Canker/mendeley_guava_canker_test_0036.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Canker/mendeley_guava_canker_test_0036.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Guava - Canker/mendeley_guava_canker_test_0040.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Canker/mendeley_guava_canker_test_0040.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Guava - Canker/mendeley_guava_canker_test_0051.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Canker/mendeley_guava_canker_test_0051.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Guava - Canker/mendeley_guava_canker_test_0059.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Canker/mendeley_guava_canker_test_0059.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Guava - Canker/mendeley_guava_canker_test_0062.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Canker/mendeley_guava_canker_test_0062.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Guava - Canker/mendeley_guava_canker_test_0079.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Canker/mendeley_guava_canker_test_0079.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Guava - Canker/mendeley_guava_canker_test_0080.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Canker/mendeley_guava_canker_test_0080.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Guava - Canker/mendeley_guava_canker_test_0087.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Canker/mendeley_guava_canker_test_0087.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Guava - Canker/mendeley_guava_canker_test_0090.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Canker/mendeley_guava_canker_test_0090.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Guava - Canker/mendeley_guava_canker_test_0094.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Canker/mendeley_guava_canker_test_0094.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Guava - Canker/mendeley_guava_canker_test_0095.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Canker/mendeley_guava_canker_test_0095.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Guava - Dot/mendeley_guava_dot_test_0002.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Dot/mendeley_guava_dot_test_0002.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Guava - Dot/mendeley_guava_dot_test_0006.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Dot/mendeley_guava_dot_test_0006.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Guava - Dot/mendeley_guava_dot_test_0013.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Dot/mendeley_guava_dot_test_0013.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Guava - Dot/mendeley_guava_dot_test_0015.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Dot/mendeley_guava_dot_test_0015.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Guava - Dot/mendeley_guava_dot_test_0016.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Dot/mendeley_guava_dot_test_0016.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Guava - Dot/mendeley_guava_dot_test_0017.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Dot/mendeley_guava_dot_test_0017.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Guava - Dot/mendeley_guava_dot_test_0023.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Dot/mendeley_guava_dot_test_0023.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Guava - Dot/mendeley_guava_dot_test_0024.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Dot/mendeley_guava_dot_test_0024.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Guava - Dot/mendeley_guava_dot_test_0027.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Dot/mendeley_guava_dot_test_0027.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Guava - Dot/mendeley_guava_dot_test_0029.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Dot/mendeley_guava_dot_test_0029.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Guava - Dot/mendeley_guava_dot_test_0030.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Dot/mendeley_guava_dot_test_0030.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Guava - Dot/mendeley_guava_dot_test_0038.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Dot/mendeley_guava_dot_test_0038.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Guava - Dot/mendeley_guava_dot_test_0039.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Dot/mendeley_guava_dot_test_0039.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Guava - Dot/mendeley_guava_dot_test_0041.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Dot/mendeley_guava_dot_test_0041.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Guava - Dot/mendeley_guava_dot_test_0042.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Dot/mendeley_guava_dot_test_0042.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Guava - Dot/mendeley_guava_dot_test_0046.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Dot/mendeley_guava_dot_test_0046.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Guava - Dot/mendeley_guava_dot_test_0049.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Dot/mendeley_guava_dot_test_0049.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Guava - Dot/mendeley_guava_dot_test_0050.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Dot/mendeley_guava_dot_test_0050.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Guava - Dot/mendeley_guava_dot_test_0051.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Dot/mendeley_guava_dot_test_0051.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Guava - Dot/mendeley_guava_dot_test_0054.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Dot/mendeley_guava_dot_test_0054.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Guava - Dot/mendeley_guava_dot_test_0058.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Dot/mendeley_guava_dot_test_0058.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Guava - Dot/mendeley_guava_dot_test_0063.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Dot/mendeley_guava_dot_test_0063.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Guava - Dot/mendeley_guava_dot_test_0067.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Dot/mendeley_guava_dot_test_0067.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Guava - Dot/mendeley_guava_dot_test_0078.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Dot/mendeley_guava_dot_test_0078.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Guava - Dot/mendeley_guava_dot_test_0084.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Dot/mendeley_guava_dot_test_0084.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Guava - Dot/test_0_9095.jpeg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Dot/test_0_9095.jpeg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Guava - Healthy/mendeley_guava_healthy_test_0001.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Healthy/mendeley_guava_healthy_test_0001.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Guava - Healthy/mendeley_guava_healthy_test_0012.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Healthy/mendeley_guava_healthy_test_0012.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Guava - Healthy/mendeley_guava_healthy_test_0014.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Healthy/mendeley_guava_healthy_test_0014.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Guava - Healthy/mendeley_guava_healthy_test_0015.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Healthy/mendeley_guava_healthy_test_0015.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Guava - Healthy/mendeley_guava_healthy_test_0017.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Healthy/mendeley_guava_healthy_test_0017.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Guava - Healthy/mendeley_guava_healthy_test_0028.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Healthy/mendeley_guava_healthy_test_0028.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Guava - Healthy/mendeley_guava_healthy_test_0030.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Healthy/mendeley_guava_healthy_test_0030.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Guava - Healthy/mendeley_guava_healthy_test_0033.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Healthy/mendeley_guava_healthy_test_0033.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Guava - Healthy/mendeley_guava_healthy_test_0034.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Healthy/mendeley_guava_healthy_test_0034.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Guava - Healthy/mendeley_guava_healthy_test_0036.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Healthy/mendeley_guava_healthy_test_0036.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Guava - Healthy/mendeley_guava_healthy_test_0045.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Healthy/mendeley_guava_healthy_test_0045.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Guava - Healthy/mendeley_guava_healthy_test_0046.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Healthy/mendeley_guava_healthy_test_0046.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Guava - Healthy/mendeley_guava_healthy_test_0053.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Healthy/mendeley_guava_healthy_test_0053.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Guava - Healthy/mendeley_guava_healthy_test_0054.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Healthy/mendeley_guava_healthy_test_0054.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Guava - Healthy/mendeley_guava_healthy_test_0055.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Healthy/mendeley_guava_healthy_test_0055.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Guava - Healthy/mendeley_guava_healthy_test_0059.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Healthy/mendeley_guava_healthy_test_0059.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Guava - Healthy/mendeley_guava_healthy_test_0061.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Healthy/mendeley_guava_healthy_test_0061.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Guava - Healthy/mendeley_guava_healthy_test_0069.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Healthy/mendeley_guava_healthy_test_0069.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Guava - Healthy/mendeley_guava_healthy_test_0071.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Healthy/mendeley_guava_healthy_test_0071.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Guava - Healthy/mendeley_guava_healthy_test_0073.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Healthy/mendeley_guava_healthy_test_0073.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Guava - Healthy/mendeley_guava_healthy_test_0074.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Healthy/mendeley_guava_healthy_test_0074.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Guava - Healthy/mendeley_guava_healthy_test_0075.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Healthy/mendeley_guava_healthy_test_0075.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Guava - Healthy/mendeley_guava_healthy_test_0076.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Healthy/mendeley_guava_healthy_test_0076.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Guava - Healthy/mendeley_guava_healthy_test_0079.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Healthy/mendeley_guava_healthy_test_0079.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Guava - Healthy/mendeley_guava_healthy_test_0082.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Healthy/mendeley_guava_healthy_test_0082.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Guava - Healthy/mendeley_guava_healthy_test_0086.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Healthy/mendeley_guava_healthy_test_0086.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Guava - Healthy/mendeley_guava_healthy_test_0090.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Healthy/mendeley_guava_healthy_test_0090.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Guava - Healthy/mendeley_guava_healthy_test_0093.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Healthy/mendeley_guava_healthy_test_0093.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Guava - Healthy/mendeley_guava_healthy_test_0094.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Healthy/mendeley_guava_healthy_test_0094.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Guava - Healthy/test_0_9338.jpeg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Healthy/test_0_9338.jpeg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Guava - Healthy/test_0_9353.jpeg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Healthy/test_0_9353.jpeg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Guava - Healthy/test_0_9390.jpeg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Healthy/test_0_9390.jpeg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Guava - Healthy/test_0_9582.jpeg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Healthy/test_0_9582.jpeg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Guava - Healthy/test_0_9692.jpeg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Healthy/test_0_9692.jpeg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Guava - Healthy/test_0_9765.jpeg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Healthy/test_0_9765.jpeg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Guava - Rust/mendeley_guava_rust_test_0002.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Rust/mendeley_guava_rust_test_0002.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Guava - Rust/mendeley_guava_rust_test_0009.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Rust/mendeley_guava_rust_test_0009.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Guava - Rust/mendeley_guava_rust_test_0010.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Rust/mendeley_guava_rust_test_0010.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Guava - Rust/mendeley_guava_rust_test_0011.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Rust/mendeley_guava_rust_test_0011.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Guava - Rust/mendeley_guava_rust_test_0012.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Rust/mendeley_guava_rust_test_0012.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Guava - Rust/mendeley_guava_rust_test_0014.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Rust/mendeley_guava_rust_test_0014.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Guava - Rust/mendeley_guava_rust_test_0018.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Rust/mendeley_guava_rust_test_0018.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Guava - Rust/mendeley_guava_rust_test_0019.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Rust/mendeley_guava_rust_test_0019.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Guava - Rust/mendeley_guava_rust_test_0020.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Rust/mendeley_guava_rust_test_0020.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Guava - Rust/mendeley_guava_rust_test_0022.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Rust/mendeley_guava_rust_test_0022.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Guava - Rust/mendeley_guava_rust_test_0025.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Rust/mendeley_guava_rust_test_0025.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Guava - Rust/mendeley_guava_rust_test_0029.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Rust/mendeley_guava_rust_test_0029.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Guava - Rust/mendeley_guava_rust_test_0032.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Rust/mendeley_guava_rust_test_0032.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Guava - Rust/mendeley_guava_rust_test_0033.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Rust/mendeley_guava_rust_test_0033.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Guava - Rust/mendeley_guava_rust_test_0035.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Rust/mendeley_guava_rust_test_0035.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Guava - Rust/mendeley_guava_rust_test_0037.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Rust/mendeley_guava_rust_test_0037.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Guava - Rust/mendeley_guava_rust_test_0039.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Rust/mendeley_guava_rust_test_0039.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Guava - Rust/mendeley_guava_rust_test_0041.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Rust/mendeley_guava_rust_test_0041.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Guava - Rust/mendeley_guava_rust_test_0042.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Rust/mendeley_guava_rust_test_0042.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Guava - Rust/mendeley_guava_rust_test_0044.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Rust/mendeley_guava_rust_test_0044.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Guava - Rust/mendeley_guava_rust_test_0049.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Rust/mendeley_guava_rust_test_0049.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Guava - Rust/mendeley_guava_rust_test_0050.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Rust/mendeley_guava_rust_test_0050.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Guava - Rust/mendeley_guava_rust_test_0051.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Rust/mendeley_guava_rust_test_0051.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Guava - Rust/mendeley_guava_rust_test_0059.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Rust/mendeley_guava_rust_test_0059.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Guava - Rust/mendeley_guava_rust_test_0061.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Rust/mendeley_guava_rust_test_0061.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Guava - Rust/mendeley_guava_rust_test_0062.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Rust/mendeley_guava_rust_test_0062.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Guava - Rust/mendeley_guava_rust_test_0063.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Rust/mendeley_guava_rust_test_0063.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Guava - Rust/mendeley_guava_rust_test_0064.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Rust/mendeley_guava_rust_test_0064.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Guava - Rust/mendeley_guava_rust_test_0065.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Rust/mendeley_guava_rust_test_0065.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Guava - Rust/mendeley_guava_rust_test_0066.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Rust/mendeley_guava_rust_test_0066.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Guava - Rust/mendeley_guava_rust_test_0067.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Rust/mendeley_guava_rust_test_0067.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Guava - Rust/mendeley_guava_rust_test_0068.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Rust/mendeley_guava_rust_test_0068.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Guava - Rust/mendeley_guava_rust_test_0069.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Rust/mendeley_guava_rust_test_0069.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Guava - Rust/mendeley_guava_rust_test_0073.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Rust/mendeley_guava_rust_test_0073.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Guava - Rust/mendeley_guava_rust_test_0077.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Rust/mendeley_guava_rust_test_0077.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Guava - Rust/mendeley_guava_rust_test_0081.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Rust/mendeley_guava_rust_test_0081.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Guava - Rust/mendeley_guava_rust_test_0082.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Rust/mendeley_guava_rust_test_0082.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Guava - Rust/mendeley_guava_rust_test_0087.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Rust/mendeley_guava_rust_test_0087.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Guava - Rust/mendeley_guava_rust_test_0092.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Rust/mendeley_guava_rust_test_0092.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Guava - Rust/mendeley_guava_rust_test_0093.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Rust/mendeley_guava_rust_test_0093.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Guava - Rust/mendeley_guava_rust_test_0094.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Rust/mendeley_guava_rust_test_0094.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Guava - Spiraling Whitefly/mendeley_guava_whitefly_test_0001.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Spiraling Whitefly/mendeley_guava_whitefly_test_0001.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Guava - Spiraling Whitefly/mendeley_guava_whitefly_test_0005.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Spiraling Whitefly/mendeley_guava_whitefly_test_0005.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Guava - Spiraling Whitefly/mendeley_guava_whitefly_test_0010.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Spiraling Whitefly/mendeley_guava_whitefly_test_0010.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Guava - Spiraling Whitefly/mendeley_guava_whitefly_test_0011.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Spiraling Whitefly/mendeley_guava_whitefly_test_0011.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Guava - Spiraling Whitefly/mendeley_guava_whitefly_test_0030.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Spiraling Whitefly/mendeley_guava_whitefly_test_0030.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Guava - Spiraling Whitefly/mendeley_guava_whitefly_test_0031.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Spiraling Whitefly/mendeley_guava_whitefly_test_0031.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Guava - Spiraling Whitefly/mendeley_guava_whitefly_test_0032.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Spiraling Whitefly/mendeley_guava_whitefly_test_0032.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Guava - Spiraling Whitefly/mendeley_guava_whitefly_test_0039.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Spiraling Whitefly/mendeley_guava_whitefly_test_0039.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Guava - Spiraling Whitefly/mendeley_guava_whitefly_test_0045.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Spiraling Whitefly/mendeley_guava_whitefly_test_0045.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Guava - Spiraling Whitefly/mendeley_guava_whitefly_test_0051.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Spiraling Whitefly/mendeley_guava_whitefly_test_0051.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Guava - Spiraling Whitefly/mendeley_guava_whitefly_test_0062.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Spiraling Whitefly/mendeley_guava_whitefly_test_0062.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Guava - Spiraling Whitefly/mendeley_guava_whitefly_test_0074.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Spiraling Whitefly/mendeley_guava_whitefly_test_0074.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Guava - Spiraling Whitefly/mendeley_guava_whitefly_test_0084.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Spiraling Whitefly/mendeley_guava_whitefly_test_0084.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Guava - Spiraling Whitefly/mendeley_guava_whitefly_test_0085.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Spiraling Whitefly/mendeley_guava_whitefly_test_0085.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Guava - Spiraling Whitefly/mendeley_guava_whitefly_test_0090.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Spiraling Whitefly/mendeley_guava_whitefly_test_0090.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Guava - Spiraling Whitefly/mendeley_guava_whitefly_test_0092.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Spiraling Whitefly/mendeley_guava_whitefly_test_0092.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Jamun - Bacterial Spot/jamun_bacterial_spot_test_0012.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Bacterial Spot/jamun_bacterial_spot_test_0012.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Jamun - Bacterial Spot/jamun_bacterial_spot_test_0022.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Bacterial Spot/jamun_bacterial_spot_test_0022.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Jamun - Bacterial Spot/jamun_bacterial_spot_test_0025.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Bacterial Spot/jamun_bacterial_spot_test_0025.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Jamun - Powdery Mildew/jamun_powdery_mildew_test_0018.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Powdery Mildew/jamun_powdery_mildew_test_0018.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Jamun - Powdery Mildew/jamun_powdery_mildew_test_0020.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Powdery Mildew/jamun_powdery_mildew_test_0020.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Mango - Anthracnose/20211011_170724 (Custom).jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Mango - Anthracnose/20211011_170724 (Custom).jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Mango - Bacterial Canker/IMG_20211106_143149 (Custom).jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Mango - Bacterial Canker/IMG_20211106_143149 (Custom).jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Mango - Die Back/20211129_164418 (Custom).jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Mango - Die Back/20211129_164418 (Custom).jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Mango - Die Back/20211129_164447 (Custom).jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Mango - Die Back/20211129_164447 (Custom).jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Mango - Die Back/20211129_164454 (Custom).jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Mango - Die Back/20211129_164454 (Custom).jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Mango - Healthy/20211231_162219 (Custom).jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Mango - Healthy/20211231_162219 (Custom).jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Mango - Healthy/20211231_162330 (Custom).jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Mango - Healthy/20211231_162330 (Custom).jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Mango - Healthy/20211231_162412 (Custom).jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Mango - Healthy/20211231_162412 (Custom).jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Paddy - Bacterial Leaf Blight/rice_lab_bacterial_val (64).jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Paddy - Bacterial Leaf Blight/rice_lab_bacterial_val (64).jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Paddy - Blast/rice_lab_leaf_blast_val (68).jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Paddy - Blast/rice_lab_leaf_blast_val (68).jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Paddy - Blast/rice_lab_leaf_blast_val (72).jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Paddy - Blast/rice_lab_leaf_blast_val (72).jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Paddy - Brown Spot/rice_lab_brown_val (75).jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Paddy - Brown Spot/rice_lab_brown_val (75).jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Paddy - Healthy/rice_lab_healthy_val (51).jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Paddy - Healthy/rice_lab_healthy_val (51).jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Paddy - Healthy/rice_lab_healthy_val (65).jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Paddy - Healthy/rice_lab_healthy_val (65).jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Paddy - Healthy/rice_lab_healthy_val (8).jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Paddy - Healthy/rice_lab_healthy_val (8).jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Peach - peach leaf curl/img_00039477.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Peach - peach leaf curl/img_00039477.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Plum - Healthy/694_lab.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Plum - Healthy/694_lab.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Plum - plum yellow leaf/587_lab.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Plum - plum yellow leaf/587_lab.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Plum - plum yellow leaf/7_lab.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Plum - plum yellow leaf/7_lab.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Plum - plum yellow leaf/81_lab.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Plum - plum yellow leaf/81_lab.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Plum - plum yellow leaf/83_lab.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Plum - plum yellow leaf/83_lab.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Plum - plum yellow leaf/98_lab.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Plum - plum yellow leaf/98_lab.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Potato - Healthy/img_00030143.JPG"
    dst_p = PROJECT_ROOT / "data/processed/test/Potato - Healthy/img_00030143.JPG"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Radish - Black leaf spot/img_00045461.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Radish - Black leaf spot/img_00045461.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Radish - Black leaf spot/img_00045656.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Radish - Black leaf spot/img_00045656.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Radish - Black leaf spot/img_00049837.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Radish - Black leaf spot/img_00049837.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Radish - Black leaf spot/img_00050845.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Radish - Black leaf spot/img_00050845.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Radish - Black leaf spot/img_00054229.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Radish - Black leaf spot/img_00054229.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Radish - Black leaf spot/img_00054272.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Radish - Black leaf spot/img_00054272.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Radish - Black leaf spot/img_00055167.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Radish - Black leaf spot/img_00055167.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Radish - Black leaf spot/img_00056233.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Radish - Black leaf spot/img_00056233.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Radish - Black leaf spot/img_00056436.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Radish - Black leaf spot/img_00056436.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Radish - Black leaf spot/img_00056665.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Radish - Black leaf spot/img_00056665.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Radish - Black leaf spot/img_00057668.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Radish - Black leaf spot/img_00057668.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Radish - Black leaf spot/img_00061770.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Radish - Black leaf spot/img_00061770.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Radish - Black leaf spot/img_00064808.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Radish - Black leaf spot/img_00064808.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Radish - Black leaf spot/img_00065142.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Radish - Black leaf spot/img_00065142.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Radish - Downey mildew/img_00046899.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Radish - Downey mildew/img_00046899.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Radish - Downey mildew/img_00049726.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Radish - Downey mildew/img_00049726.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Radish - Downey mildew/img_00051737.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Radish - Downey mildew/img_00051737.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Radish - Downey mildew/img_00052524.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Radish - Downey mildew/img_00052524.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Radish - Downey mildew/img_00055315.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Radish - Downey mildew/img_00055315.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Radish - Downey mildew/img_00056817.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Radish - Downey mildew/img_00056817.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Radish - Downey mildew/img_00059873.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Radish - Downey mildew/img_00059873.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Radish - Downey mildew/img_00063699.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Radish - Downey mildew/img_00063699.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Radish - Downey mildew/img_00064986.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Radish - Downey mildew/img_00064986.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Radish - Flea beetle/img_00046519.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Radish - Flea beetle/img_00046519.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Radish - Flea beetle/img_00048120.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Radish - Flea beetle/img_00048120.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Radish - Flea beetle/img_00048406.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Radish - Flea beetle/img_00048406.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Radish - Flea beetle/img_00049390.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Radish - Flea beetle/img_00049390.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Radish - Flea beetle/img_00054655.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Radish - Flea beetle/img_00054655.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Radish - Flea beetle/img_00055390.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Radish - Flea beetle/img_00055390.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Radish - Flea beetle/img_00055962.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Radish - Flea beetle/img_00055962.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Radish - Flea beetle/img_00056384.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Radish - Flea beetle/img_00056384.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Radish - Flea beetle/img_00057537.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Radish - Flea beetle/img_00057537.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Radish - Flea beetle/img_00058649.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Radish - Flea beetle/img_00058649.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Radish - Flea beetle/img_00058844.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Radish - Flea beetle/img_00058844.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Radish - Flea beetle/img_00059004.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Radish - Flea beetle/img_00059004.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Radish - Flea beetle/img_00063652.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Radish - Flea beetle/img_00063652.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Radish - Healthy/img_00047393.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Radish - Healthy/img_00047393.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Radish - Healthy/img_00048077.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Radish - Healthy/img_00048077.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Radish - Healthy/img_00052044.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Radish - Healthy/img_00052044.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Radish - Healthy/img_00052138.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Radish - Healthy/img_00052138.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Radish - Healthy/img_00055194.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Radish - Healthy/img_00055194.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Radish - Healthy/img_00055967.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Radish - Healthy/img_00055967.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Radish - Healthy/img_00056634.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Radish - Healthy/img_00056634.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Radish - Healthy/img_00057457.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Radish - Healthy/img_00057457.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Radish - Healthy/img_00057745.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Radish - Healthy/img_00057745.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Radish - Healthy/img_00059572.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Radish - Healthy/img_00059572.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Radish - Healthy/img_00065030.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Radish - Healthy/img_00065030.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Radish - Mosaic/img_00058440.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Radish - Mosaic/img_00058440.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Radish - Mosaic/img_00059120.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Radish - Mosaic/img_00059120.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Radish - Mosaic/img_00059573.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Radish - Mosaic/img_00059573.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Radish - Mosaic/img_00062310.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Radish - Mosaic/img_00062310.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Radish - Mosaic/img_00065125.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Radish - Mosaic/img_00065125.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Radish - Mosaic/img_00065162.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Radish - Mosaic/img_00065162.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Radish - Mosaic/img_00065300.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Radish - Mosaic/img_00065300.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Soybean - Frogeye Leaf Spot/img_00040510.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Soybean - Frogeye Leaf Spot/img_00040510.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Soybean - Healthy/scraped_kaggle_pv2_0ca2cd1f-bd70-49f5-9e1d-fb51958aee44___RS_HL 5014.JPG"
    dst_p = PROJECT_ROOT / "data/processed/test/Soybean - Healthy/scraped_kaggle_pv2_0ca2cd1f-bd70-49f5-9e1d-fb51958aee44___RS_HL 5014.JPG"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Soybean - Healthy/scraped_kaggle_pv2_11f78f5c-2acc-406f-a6d5-18059c551eda___RS_HL 4849.JPG"
    dst_p = PROJECT_ROOT / "data/processed/test/Soybean - Healthy/scraped_kaggle_pv2_11f78f5c-2acc-406f-a6d5-18059c551eda___RS_HL 4849.JPG"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Tomato - Bacterial Spot/img_00017296.JPG"
    dst_p = PROJECT_ROOT / "data/processed/test/Tomato - Bacterial Spot/img_00017296.JPG"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Tomato - Bacterial Spot/img_00019087.JPG"
    dst_p = PROJECT_ROOT / "data/processed/test/Tomato - Bacterial Spot/img_00019087.JPG"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Tomato - Healthy/img_00022732.JPG"
    dst_p = PROJECT_ROOT / "data/processed/test/Tomato - Healthy/img_00022732.JPG"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Tomato - Healthy/img_00023342.JPG"
    dst_p = PROJECT_ROOT / "data/processed/test/Tomato - Healthy/img_00023342.JPG"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Tomato - Healthy/img_00023416.JPG"
    dst_p = PROJECT_ROOT / "data/processed/test/Tomato - Healthy/img_00023416.JPG"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Tomato - Healthy/img_00023578.JPG"
    dst_p = PROJECT_ROOT / "data/processed/test/Tomato - Healthy/img_00023578.JPG"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Tomato - Spider Mites/img_00025235.JPG"
    dst_p = PROJECT_ROOT / "data/processed/test/Tomato - Spider Mites/img_00025235.JPG"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Tomato - tomato yellow leaf curl virus/Tomato - Yellow Leaf Curl Virus_img_00033469.JPG"
    dst_p = PROJECT_ROOT / "data/processed/test/Tomato - tomato yellow leaf curl virus/Tomato - Yellow Leaf Curl Virus_img_00033469.JPG"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/test/Tomato - tomato yellow leaf curl virus/Tomato - Yellow Leaf Curl Virus_img_00033727.JPG"
    dst_p = PROJECT_ROOT / "data/processed/test/Tomato - tomato yellow leaf curl virus/Tomato - Yellow Leaf Curl Virus_img_00033727.JPG"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/test/Tomato - tomato yellow leaf curl virus/Tomato - Yellow Leaf Curl Virus_img_00033846.JPG"
    dst_p = PROJECT_ROOT / "data/processed/test/Tomato - tomato yellow leaf curl virus/Tomato - Yellow Leaf Curl Virus_img_00033846.JPG"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Apple - apple alternaria leaf spot/plantcity_apple_apple_alternaria_leaf_spot_train_00185.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Apple - apple alternaria leaf spot/plantcity_apple_apple_alternaria_leaf_spot_train_00185.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Apple - apple alternaria leaf spot/plantcity_apple_apple_alternaria_leaf_spot_train_00213.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Apple - apple alternaria leaf spot/plantcity_apple_apple_alternaria_leaf_spot_train_00213.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Bell Pepper - Bacterial Spot/img_00016162.JPG"
    dst_p = PROJECT_ROOT / "data/processed/train/Bell Pepper - Bacterial Spot/img_00016162.JPG"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Bell Pepper - Healthy/img_00026981.JPG"
    dst_p = PROJECT_ROOT / "data/processed/train/Bell Pepper - Healthy/img_00026981.JPG"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Bell Pepper - Healthy/img_00026989.JPG"
    dst_p = PROJECT_ROOT / "data/processed/train/Bell Pepper - Healthy/img_00026989.JPG"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Bell Pepper - Healthy/img_00027557.JPG"
    dst_p = PROJECT_ROOT / "data/processed/train/Bell Pepper - Healthy/img_00027557.JPG"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Bell Pepper - Healthy/img_00027575.JPG"
    dst_p = PROJECT_ROOT / "data/processed/train/Bell Pepper - Healthy/img_00027575.JPG"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Bell Pepper - Healthy/img_00027577.JPG"
    dst_p = PROJECT_ROOT / "data/processed/train/Bell Pepper - Healthy/img_00027577.JPG"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Bell Pepper - bell pepper frogeye leaf spot/bell_pepper_frogeye_mendeley_train_00293.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Bell Pepper - bell pepper frogeye leaf spot/bell_pepper_frogeye_mendeley_train_00293.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Bell Pepper - bell pepper frogeye leaf spot/bell_pepper_frogeye_mendeley_train_00714.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Bell Pepper - bell pepper frogeye leaf spot/bell_pepper_frogeye_mendeley_train_00714.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Bell Pepper - bell pepper frogeye leaf spot/bell_pepper_frogeye_mendeley_train_01064.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Bell Pepper - bell pepper frogeye leaf spot/bell_pepper_frogeye_mendeley_train_01064.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Bell Pepper - bell pepper frogeye leaf spot/bell_pepper_frogeye_mendeley_train_01066.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Bell Pepper - bell pepper frogeye leaf spot/bell_pepper_frogeye_mendeley_train_01066.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Blackgram - Healthy/img_00000893.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Blackgram - Healthy/img_00000893.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Blueberry - Healthy/scraped_kaggle_pv2_04b13de1-c2bf-45ad-a04d-db4b7f7e6c7a___RS_HL 2534.JPG"
    dst_p = PROJECT_ROOT / "data/processed/train/Blueberry - Healthy/scraped_kaggle_pv2_04b13de1-c2bf-45ad-a04d-db4b7f7e6c7a___RS_HL 2534.JPG"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Cabbage - cabbage downy mildew/img_00036458.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Cabbage - cabbage downy mildew/img_00036458.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Cherry - Healthy/scraped_kaggle_pv2_34e05c4f-6742-442e-884e-ef3191eb923b___JR_HL 4049.JPG"
    dst_p = PROJECT_ROOT / "data/processed/train/Cherry - Healthy/scraped_kaggle_pv2_34e05c4f-6742-442e-884e-ef3191eb923b___JR_HL 4049.JPG"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Cherry - cherry brown spot/plantcity_cherry_cherry_brown_spot_train_00380.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Cherry - cherry brown spot/plantcity_cherry_cherry_brown_spot_train_00380.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Cherry - cherry leaf scorch/plantcity_cherry_cherry_leaf_scorch_train_00150.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Cherry - cherry leaf scorch/plantcity_cherry_cherry_leaf_scorch_train_00150.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Citrus - citrus algal leaf spot/2023_08_21_16_40_IMG_7360.JPG"
    dst_p = PROJECT_ROOT / "data/processed/train/Citrus - citrus algal leaf spot/2023_08_21_16_40_IMG_7360.JPG"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Citrus - citrus algal leaf spot/2023_08_21_16_40_IMG_7376.JPG"
    dst_p = PROJECT_ROOT / "data/processed/train/Citrus - citrus algal leaf spot/2023_08_21_16_40_IMG_7376.JPG"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Citrus - citrus greening disease/sourabh_g (45).png"
    dst_p = PROJECT_ROOT / "data/processed/train/Citrus - citrus greening disease/sourabh_g (45).png"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Citrus - citrus scab/2023_08_21_15_37_IMG_6045.JPG"
    dst_p = PROJECT_ROOT / "data/processed/train/Citrus - citrus scab/2023_08_21_15_37_IMG_6045.JPG"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Coffee - coffee leaf rust/scraped_coffee_rust_name291.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Coffee - coffee leaf rust/scraped_coffee_rust_name291.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Fig - fig brown spot/plantcity_fig_fig_brown_spot_train_00140.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Fig - fig brown spot/plantcity_fig_fig_brown_spot_train_00140.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Ginger - Bacterial Wilt/ginger_bacterial_wilt_train_00055.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Ginger - Bacterial Wilt/ginger_bacterial_wilt_train_00055.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Ginger - Bacterial Wilt/ginger_bacterial_wilt_train_00065.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Ginger - Bacterial Wilt/ginger_bacterial_wilt_train_00065.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Ginger - Bacterial Wilt/ginger_bacterial_wilt_train_00068.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Ginger - Bacterial Wilt/ginger_bacterial_wilt_train_00068.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Ginger - Bacterial Wilt/ginger_bacterial_wilt_train_00071.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Ginger - Bacterial Wilt/ginger_bacterial_wilt_train_00071.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Ginger - Bacterial Wilt/ginger_bacterial_wilt_train_00082.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Ginger - Bacterial Wilt/ginger_bacterial_wilt_train_00082.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Ginger - Bacterial Wilt/ginger_bacterial_wilt_train_00091.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Ginger - Bacterial Wilt/ginger_bacterial_wilt_train_00091.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Ginger - Bacterial Wilt/ginger_bacterial_wilt_train_00092.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Ginger - Bacterial Wilt/ginger_bacterial_wilt_train_00092.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Ginger - Bacterial Wilt/ginger_bacterial_wilt_train_00101.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Ginger - Bacterial Wilt/ginger_bacterial_wilt_train_00101.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Ginger - Bacterial Wilt/ginger_bacterial_wilt_train_00103.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Ginger - Bacterial Wilt/ginger_bacterial_wilt_train_00103.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Ginger - Bacterial Wilt/ginger_bacterial_wilt_train_00112.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Ginger - Bacterial Wilt/ginger_bacterial_wilt_train_00112.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Ginger - Bacterial Wilt/ginger_bacterial_wilt_train_00126.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Ginger - Bacterial Wilt/ginger_bacterial_wilt_train_00126.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Ginger - Dehydrated/ginger_dehydrated_train_00267.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Ginger - Dehydrated/ginger_dehydrated_train_00267.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Ginger - Dehydrated/ginger_dehydrated_train_00498.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Ginger - Dehydrated/ginger_dehydrated_train_00498.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Ginger - Dehydrated/ginger_dehydrated_train_00694.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Ginger - Dehydrated/ginger_dehydrated_train_00694.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Ginger - Dehydrated/ginger_dehydrated_train_00833.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Ginger - Dehydrated/ginger_dehydrated_train_00833.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Ginger - Dehydrated/ginger_dehydrated_train_00903.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Ginger - Dehydrated/ginger_dehydrated_train_00903.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Ginger - Dehydrated/ginger_dehydrated_train_01625.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Ginger - Dehydrated/ginger_dehydrated_train_01625.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Ginger - Healthy/ginger_healthy_train_00028.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Ginger - Healthy/ginger_healthy_train_00028.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Ginger - Healthy/ginger_healthy_train_00137.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Ginger - Healthy/ginger_healthy_train_00137.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Ginger - Healthy/ginger_healthy_train_00514.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Ginger - Healthy/ginger_healthy_train_00514.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Ginger - Healthy/ginger_healthy_train_00546.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Ginger - Healthy/ginger_healthy_train_00546.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Ginger - Healthy/ginger_healthy_train_00879.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Ginger - Healthy/ginger_healthy_train_00879.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Ginger - Leaf Blight/ginger_leaf_blight_train_00740.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Ginger - Leaf Blight/ginger_leaf_blight_train_00740.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Ginger - Leaf Blight/ginger_leaf_blight_train_01076.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Ginger - Leaf Blight/ginger_leaf_blight_train_01076.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Ginger - Leaf Blight/ginger_leaf_blight_train_01373.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Ginger - Leaf Blight/ginger_leaf_blight_train_01373.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Ginger - Leaf Blight/ginger_leaf_blight_train_01508.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Ginger - Leaf Blight/ginger_leaf_blight_train_01508.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Ginger - Leaf Blight/ginger_leaf_blight_train_01561.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Ginger - Leaf Blight/ginger_leaf_blight_train_01561.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Ginger - Leaf Blight/ginger_leaf_blight_train_01565.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Ginger - Leaf Blight/ginger_leaf_blight_train_01565.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Ginger - Leaf Blight/ginger_leaf_blight_train_01602.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Ginger - Leaf Blight/ginger_leaf_blight_train_01602.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Ginger - Leaf Blight/ginger_leaf_blight_train_01692.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Ginger - Leaf Blight/ginger_leaf_blight_train_01692.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Ginger - Pest Damage/ginger_pest_damage_train_00321.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Ginger - Pest Damage/ginger_pest_damage_train_00321.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Ginger - Pest Damage/ginger_pest_damage_train_00343.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Ginger - Pest Damage/ginger_pest_damage_train_00343.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Ginger - Pest Damage/ginger_pest_damage_train_00345.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Ginger - Pest Damage/ginger_pest_damage_train_00345.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Ginger - Pest Damage/ginger_pest_damage_train_00348.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Ginger - Pest Damage/ginger_pest_damage_train_00348.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Ginger - Pest Damage/ginger_pest_damage_train_00350.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Ginger - Pest Damage/ginger_pest_damage_train_00350.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Anthracnose/mendeley_guava_anthracnose_train_0019.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Anthracnose/mendeley_guava_anthracnose_train_0019.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Anthracnose/mendeley_guava_anthracnose_train_0056.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Anthracnose/mendeley_guava_anthracnose_train_0056.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Anthracnose/mendeley_guava_anthracnose_train_0074.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Anthracnose/mendeley_guava_anthracnose_train_0074.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Anthracnose/mendeley_guava_anthracnose_train_0090.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Anthracnose/mendeley_guava_anthracnose_train_0090.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Anthracnose/mendeley_guava_anthracnose_train_0101.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Anthracnose/mendeley_guava_anthracnose_train_0101.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Anthracnose/mendeley_guava_anthracnose_train_0103.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Anthracnose/mendeley_guava_anthracnose_train_0103.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Anthracnose/mendeley_guava_anthracnose_train_0140.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Anthracnose/mendeley_guava_anthracnose_train_0140.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Anthracnose/mendeley_guava_anthracnose_train_0141.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Anthracnose/mendeley_guava_anthracnose_train_0141.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Anthracnose/mendeley_guava_anthracnose_train_0158.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Anthracnose/mendeley_guava_anthracnose_train_0158.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Anthracnose/mendeley_guava_anthracnose_train_0164.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Anthracnose/mendeley_guava_anthracnose_train_0164.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Anthracnose/mendeley_guava_anthracnose_train_0170.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Anthracnose/mendeley_guava_anthracnose_train_0170.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Anthracnose/mendeley_guava_anthracnose_train_0173.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Anthracnose/mendeley_guava_anthracnose_train_0173.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Anthracnose/mendeley_guava_anthracnose_train_0177.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Anthracnose/mendeley_guava_anthracnose_train_0177.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Anthracnose/mendeley_guava_anthracnose_train_0215.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Anthracnose/mendeley_guava_anthracnose_train_0215.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Anthracnose/mendeley_guava_anthracnose_train_0242.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Anthracnose/mendeley_guava_anthracnose_train_0242.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Anthracnose/mendeley_guava_anthracnose_train_0259.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Anthracnose/mendeley_guava_anthracnose_train_0259.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Anthracnose/mendeley_guava_anthracnose_train_0261.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Anthracnose/mendeley_guava_anthracnose_train_0261.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Anthracnose/mendeley_guava_anthracnose_train_0278.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Anthracnose/mendeley_guava_anthracnose_train_0278.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Anthracnose/mendeley_guava_anthracnose_train_0282.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Anthracnose/mendeley_guava_anthracnose_train_0282.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Anthracnose/mendeley_guava_anthracnose_train_0306.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Anthracnose/mendeley_guava_anthracnose_train_0306.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Anthracnose/mendeley_guava_anthracnose_train_0309.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Anthracnose/mendeley_guava_anthracnose_train_0309.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Anthracnose/mendeley_guava_anthracnose_train_0361.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Anthracnose/mendeley_guava_anthracnose_train_0361.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Anthracnose/mendeley_guava_anthracnose_train_0396.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Anthracnose/mendeley_guava_anthracnose_train_0396.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Anthracnose/mendeley_guava_anthracnose_train_0410.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Anthracnose/mendeley_guava_anthracnose_train_0410.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Anthracnose/mendeley_guava_anthracnose_train_0417.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Anthracnose/mendeley_guava_anthracnose_train_0417.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Anthracnose/mendeley_guava_anthracnose_train_0471.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Anthracnose/mendeley_guava_anthracnose_train_0471.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Anthracnose/mendeley_guava_anthracnose_train_0479.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Anthracnose/mendeley_guava_anthracnose_train_0479.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Anthracnose/mendeley_guava_anthracnose_train_0485.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Anthracnose/mendeley_guava_anthracnose_train_0485.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Anthracnose/mendeley_guava_anthracnose_train_0488.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Anthracnose/mendeley_guava_anthracnose_train_0488.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Anthracnose/mendeley_guava_anthracnose_train_0505.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Anthracnose/mendeley_guava_anthracnose_train_0505.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Anthracnose/mendeley_guava_anthracnose_train_0521.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Anthracnose/mendeley_guava_anthracnose_train_0521.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Anthracnose/mendeley_guava_anthracnose_train_0524.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Anthracnose/mendeley_guava_anthracnose_train_0524.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Anthracnose/mendeley_guava_anthracnose_train_0528.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Anthracnose/mendeley_guava_anthracnose_train_0528.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Anthracnose/mendeley_guava_anthracnose_train_0535.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Anthracnose/mendeley_guava_anthracnose_train_0535.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Anthracnose/mendeley_guava_anthracnose_train_0537.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Anthracnose/mendeley_guava_anthracnose_train_0537.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Anthracnose/mendeley_guava_anthracnose_train_0603.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Anthracnose/mendeley_guava_anthracnose_train_0603.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Anthracnose/mendeley_guava_anthracnose_train_0609.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Anthracnose/mendeley_guava_anthracnose_train_0609.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Anthracnose/mendeley_guava_anthracnose_train_0626.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Anthracnose/mendeley_guava_anthracnose_train_0626.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Canker/mendeley_guava_canker_train_0006.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Canker/mendeley_guava_canker_train_0006.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Canker/mendeley_guava_canker_train_0011.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Canker/mendeley_guava_canker_train_0011.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Canker/mendeley_guava_canker_train_0020.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Canker/mendeley_guava_canker_train_0020.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Canker/mendeley_guava_canker_train_0028.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Canker/mendeley_guava_canker_train_0028.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Canker/mendeley_guava_canker_train_0040.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Canker/mendeley_guava_canker_train_0040.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Canker/mendeley_guava_canker_train_0052.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Canker/mendeley_guava_canker_train_0052.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Canker/mendeley_guava_canker_train_0073.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Canker/mendeley_guava_canker_train_0073.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Canker/mendeley_guava_canker_train_0099.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Canker/mendeley_guava_canker_train_0099.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Canker/mendeley_guava_canker_train_0110.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Canker/mendeley_guava_canker_train_0110.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Canker/mendeley_guava_canker_train_0144.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Canker/mendeley_guava_canker_train_0144.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Canker/mendeley_guava_canker_train_0156.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Canker/mendeley_guava_canker_train_0156.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Canker/mendeley_guava_canker_train_0177.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Canker/mendeley_guava_canker_train_0177.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Canker/mendeley_guava_canker_train_0185.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Canker/mendeley_guava_canker_train_0185.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Canker/mendeley_guava_canker_train_0208.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Canker/mendeley_guava_canker_train_0208.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Canker/mendeley_guava_canker_train_0219.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Canker/mendeley_guava_canker_train_0219.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Canker/mendeley_guava_canker_train_0228.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Canker/mendeley_guava_canker_train_0228.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Canker/mendeley_guava_canker_train_0229.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Canker/mendeley_guava_canker_train_0229.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Canker/mendeley_guava_canker_train_0232.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Canker/mendeley_guava_canker_train_0232.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Canker/mendeley_guava_canker_train_0243.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Canker/mendeley_guava_canker_train_0243.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Canker/mendeley_guava_canker_train_0274.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Canker/mendeley_guava_canker_train_0274.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Canker/mendeley_guava_canker_train_0315.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Canker/mendeley_guava_canker_train_0315.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Canker/mendeley_guava_canker_train_0320.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Canker/mendeley_guava_canker_train_0320.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Canker/mendeley_guava_canker_train_0342.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Canker/mendeley_guava_canker_train_0342.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Canker/mendeley_guava_canker_train_0374.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Canker/mendeley_guava_canker_train_0374.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Canker/mendeley_guava_canker_train_0393.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Canker/mendeley_guava_canker_train_0393.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Canker/mendeley_guava_canker_train_0395.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Canker/mendeley_guava_canker_train_0395.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Canker/mendeley_guava_canker_train_0420.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Canker/mendeley_guava_canker_train_0420.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Canker/mendeley_guava_canker_train_0456.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Canker/mendeley_guava_canker_train_0456.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Canker/mendeley_guava_canker_train_0479.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Canker/mendeley_guava_canker_train_0479.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Canker/mendeley_guava_canker_train_0496.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Canker/mendeley_guava_canker_train_0496.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Canker/mendeley_guava_canker_train_0499.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Canker/mendeley_guava_canker_train_0499.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Canker/mendeley_guava_canker_train_0533.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Canker/mendeley_guava_canker_train_0533.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Canker/mendeley_guava_canker_train_0546.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Canker/mendeley_guava_canker_train_0546.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Canker/mendeley_guava_canker_train_0549.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Canker/mendeley_guava_canker_train_0549.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Canker/mendeley_guava_canker_train_0561.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Canker/mendeley_guava_canker_train_0561.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Canker/mendeley_guava_canker_train_0567.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Canker/mendeley_guava_canker_train_0567.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Canker/mendeley_guava_canker_train_0569.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Canker/mendeley_guava_canker_train_0569.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Canker/mendeley_guava_canker_train_0579.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Canker/mendeley_guava_canker_train_0579.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Canker/mendeley_guava_canker_train_0596.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Canker/mendeley_guava_canker_train_0596.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Canker/mendeley_guava_canker_train_0599.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Canker/mendeley_guava_canker_train_0599.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Canker/mendeley_guava_canker_train_0606.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Canker/mendeley_guava_canker_train_0606.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Canker/mendeley_guava_canker_train_0632.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Canker/mendeley_guava_canker_train_0632.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Canker/mendeley_guava_canker_train_0637.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Canker/mendeley_guava_canker_train_0637.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Canker/mendeley_guava_canker_train_0657.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Canker/mendeley_guava_canker_train_0657.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Canker/mendeley_guava_canker_train_0661.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Canker/mendeley_guava_canker_train_0661.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Canker/mendeley_guava_canker_train_0669.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Canker/mendeley_guava_canker_train_0669.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Canker/mendeley_guava_canker_train_0681.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Canker/mendeley_guava_canker_train_0681.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Canker/mendeley_guava_canker_train_0686.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Canker/mendeley_guava_canker_train_0686.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Canker/mendeley_guava_canker_train_0688.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Canker/mendeley_guava_canker_train_0688.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Canker/mendeley_guava_canker_train_0689.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Canker/mendeley_guava_canker_train_0689.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Canker/mendeley_guava_canker_train_0692.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Canker/mendeley_guava_canker_train_0692.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Canker/mendeley_guava_canker_train_0708.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Canker/mendeley_guava_canker_train_0708.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Canker/mendeley_guava_canker_train_0712.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Canker/mendeley_guava_canker_train_0712.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Canker/mendeley_guava_canker_train_0715.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Canker/mendeley_guava_canker_train_0715.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Canker/mendeley_guava_canker_train_0727.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Canker/mendeley_guava_canker_train_0727.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Canker/mendeley_guava_canker_train_0739.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Canker/mendeley_guava_canker_train_0739.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Canker/mendeley_guava_canker_train_0743.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Canker/mendeley_guava_canker_train_0743.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Dot/mendeley_guava_dot_train_0007.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Dot/mendeley_guava_dot_train_0007.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Dot/mendeley_guava_dot_train_0009.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Dot/mendeley_guava_dot_train_0009.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Dot/mendeley_guava_dot_train_0022.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Dot/mendeley_guava_dot_train_0022.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Dot/mendeley_guava_dot_train_0037.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Dot/mendeley_guava_dot_train_0037.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Dot/mendeley_guava_dot_train_0041.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Dot/mendeley_guava_dot_train_0041.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Dot/mendeley_guava_dot_train_0046.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Dot/mendeley_guava_dot_train_0046.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Dot/mendeley_guava_dot_train_0060.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Dot/mendeley_guava_dot_train_0060.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Dot/mendeley_guava_dot_train_0062.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Dot/mendeley_guava_dot_train_0062.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Dot/mendeley_guava_dot_train_0065.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Dot/mendeley_guava_dot_train_0065.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Dot/mendeley_guava_dot_train_0075.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Dot/mendeley_guava_dot_train_0075.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Dot/mendeley_guava_dot_train_0085.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Dot/mendeley_guava_dot_train_0085.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Dot/mendeley_guava_dot_train_0094.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Dot/mendeley_guava_dot_train_0094.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Dot/mendeley_guava_dot_train_0095.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Dot/mendeley_guava_dot_train_0095.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Dot/mendeley_guava_dot_train_0100.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Dot/mendeley_guava_dot_train_0100.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Dot/mendeley_guava_dot_train_0110.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Dot/mendeley_guava_dot_train_0110.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Dot/mendeley_guava_dot_train_0117.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Dot/mendeley_guava_dot_train_0117.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Dot/mendeley_guava_dot_train_0118.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Dot/mendeley_guava_dot_train_0118.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Dot/mendeley_guava_dot_train_0121.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Dot/mendeley_guava_dot_train_0121.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Dot/mendeley_guava_dot_train_0124.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Dot/mendeley_guava_dot_train_0124.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Dot/mendeley_guava_dot_train_0128.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Dot/mendeley_guava_dot_train_0128.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Dot/mendeley_guava_dot_train_0129.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Dot/mendeley_guava_dot_train_0129.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Dot/mendeley_guava_dot_train_0131.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Dot/mendeley_guava_dot_train_0131.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Dot/mendeley_guava_dot_train_0133.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Dot/mendeley_guava_dot_train_0133.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Dot/mendeley_guava_dot_train_0137.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Dot/mendeley_guava_dot_train_0137.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Dot/mendeley_guava_dot_train_0145.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Dot/mendeley_guava_dot_train_0145.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Dot/mendeley_guava_dot_train_0149.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Dot/mendeley_guava_dot_train_0149.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Dot/mendeley_guava_dot_train_0170.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Dot/mendeley_guava_dot_train_0170.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Dot/mendeley_guava_dot_train_0173.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Dot/mendeley_guava_dot_train_0173.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Dot/mendeley_guava_dot_train_0180.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Dot/mendeley_guava_dot_train_0180.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Dot/mendeley_guava_dot_train_0183.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Dot/mendeley_guava_dot_train_0183.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Dot/mendeley_guava_dot_train_0185.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Dot/mendeley_guava_dot_train_0185.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Dot/mendeley_guava_dot_train_0193.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Dot/mendeley_guava_dot_train_0193.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Dot/mendeley_guava_dot_train_0194.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Dot/mendeley_guava_dot_train_0194.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Dot/mendeley_guava_dot_train_0205.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Dot/mendeley_guava_dot_train_0205.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Dot/mendeley_guava_dot_train_0208.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Dot/mendeley_guava_dot_train_0208.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Dot/mendeley_guava_dot_train_0210.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Dot/mendeley_guava_dot_train_0210.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Dot/mendeley_guava_dot_train_0211.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Dot/mendeley_guava_dot_train_0211.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Dot/mendeley_guava_dot_train_0218.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Dot/mendeley_guava_dot_train_0218.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Dot/mendeley_guava_dot_train_0221.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Dot/mendeley_guava_dot_train_0221.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Dot/mendeley_guava_dot_train_0234.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Dot/mendeley_guava_dot_train_0234.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Dot/mendeley_guava_dot_train_0240.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Dot/mendeley_guava_dot_train_0240.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Dot/mendeley_guava_dot_train_0253.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Dot/mendeley_guava_dot_train_0253.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Dot/mendeley_guava_dot_train_0255.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Dot/mendeley_guava_dot_train_0255.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Dot/mendeley_guava_dot_train_0262.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Dot/mendeley_guava_dot_train_0262.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Dot/mendeley_guava_dot_train_0269.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Dot/mendeley_guava_dot_train_0269.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Dot/mendeley_guava_dot_train_0271.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Dot/mendeley_guava_dot_train_0271.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Dot/mendeley_guava_dot_train_0286.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Dot/mendeley_guava_dot_train_0286.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Dot/mendeley_guava_dot_train_0289.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Dot/mendeley_guava_dot_train_0289.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Dot/mendeley_guava_dot_train_0293.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Dot/mendeley_guava_dot_train_0293.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Dot/mendeley_guava_dot_train_0294.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Dot/mendeley_guava_dot_train_0294.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Dot/mendeley_guava_dot_train_0295.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Dot/mendeley_guava_dot_train_0295.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Dot/mendeley_guava_dot_train_0299.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Dot/mendeley_guava_dot_train_0299.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Dot/mendeley_guava_dot_train_0304.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Dot/mendeley_guava_dot_train_0304.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Dot/mendeley_guava_dot_train_0311.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Dot/mendeley_guava_dot_train_0311.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Dot/mendeley_guava_dot_train_0313.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Dot/mendeley_guava_dot_train_0313.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Dot/mendeley_guava_dot_train_0319.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Dot/mendeley_guava_dot_train_0319.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Dot/mendeley_guava_dot_train_0342.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Dot/mendeley_guava_dot_train_0342.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Dot/mendeley_guava_dot_train_0356.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Dot/mendeley_guava_dot_train_0356.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Dot/mendeley_guava_dot_train_0357.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Dot/mendeley_guava_dot_train_0357.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Dot/mendeley_guava_dot_train_0370.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Dot/mendeley_guava_dot_train_0370.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Dot/mendeley_guava_dot_train_0374.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Dot/mendeley_guava_dot_train_0374.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Dot/mendeley_guava_dot_train_0383.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Dot/mendeley_guava_dot_train_0383.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Dot/mendeley_guava_dot_train_0391.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Dot/mendeley_guava_dot_train_0391.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Dot/mendeley_guava_dot_train_0403.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Dot/mendeley_guava_dot_train_0403.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Dot/mendeley_guava_dot_train_0405.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Dot/mendeley_guava_dot_train_0405.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Dot/mendeley_guava_dot_train_0410.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Dot/mendeley_guava_dot_train_0410.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Dot/mendeley_guava_dot_train_0411.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Dot/mendeley_guava_dot_train_0411.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Dot/mendeley_guava_dot_train_0413.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Dot/mendeley_guava_dot_train_0413.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Dot/mendeley_guava_dot_train_0421.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Dot/mendeley_guava_dot_train_0421.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Dot/mendeley_guava_dot_train_0429.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Dot/mendeley_guava_dot_train_0429.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Dot/mendeley_guava_dot_train_0436.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Dot/mendeley_guava_dot_train_0436.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Dot/mendeley_guava_dot_train_0437.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Dot/mendeley_guava_dot_train_0437.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Dot/mendeley_guava_dot_train_0444.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Dot/mendeley_guava_dot_train_0444.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Dot/mendeley_guava_dot_train_0460.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Dot/mendeley_guava_dot_train_0460.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Dot/mendeley_guava_dot_train_0469.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Dot/mendeley_guava_dot_train_0469.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Dot/mendeley_guava_dot_train_0481.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Dot/mendeley_guava_dot_train_0481.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Dot/mendeley_guava_dot_train_0508.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Dot/mendeley_guava_dot_train_0508.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Dot/mendeley_guava_dot_train_0527.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Dot/mendeley_guava_dot_train_0527.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Dot/mendeley_guava_dot_train_0528.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Dot/mendeley_guava_dot_train_0528.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Dot/mendeley_guava_dot_train_0545.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Dot/mendeley_guava_dot_train_0545.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Dot/mendeley_guava_dot_train_0560.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Dot/mendeley_guava_dot_train_0560.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Dot/mendeley_guava_dot_train_0566.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Dot/mendeley_guava_dot_train_0566.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Dot/mendeley_guava_dot_train_0567.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Dot/mendeley_guava_dot_train_0567.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Dot/mendeley_guava_dot_train_0568.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Dot/mendeley_guava_dot_train_0568.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Dot/mendeley_guava_dot_train_0574.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Dot/mendeley_guava_dot_train_0574.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Dot/mendeley_guava_dot_train_0576.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Dot/mendeley_guava_dot_train_0576.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Dot/mendeley_guava_dot_train_0581.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Dot/mendeley_guava_dot_train_0581.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Dot/mendeley_guava_dot_train_0585.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Dot/mendeley_guava_dot_train_0585.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Dot/mendeley_guava_dot_train_0598.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Dot/mendeley_guava_dot_train_0598.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Dot/mendeley_guava_dot_train_0609.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Dot/mendeley_guava_dot_train_0609.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Dot/mendeley_guava_dot_train_0610.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Dot/mendeley_guava_dot_train_0610.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Dot/mendeley_guava_dot_train_0615.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Dot/mendeley_guava_dot_train_0615.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Dot/mendeley_guava_dot_train_0619.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Dot/mendeley_guava_dot_train_0619.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Dot/mendeley_guava_dot_train_0621.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Dot/mendeley_guava_dot_train_0621.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Dot/mendeley_guava_dot_train_0645.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Dot/mendeley_guava_dot_train_0645.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Dot/mendeley_guava_dot_train_0647.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Dot/mendeley_guava_dot_train_0647.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Dot/mendeley_guava_dot_train_0649.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Dot/mendeley_guava_dot_train_0649.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Dot/mendeley_guava_dot_train_0651.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Dot/mendeley_guava_dot_train_0651.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Dot/mendeley_guava_dot_train_0652.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Dot/mendeley_guava_dot_train_0652.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Dot/mendeley_guava_dot_train_0653.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Dot/mendeley_guava_dot_train_0653.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Dot/mendeley_guava_dot_train_0654.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Dot/mendeley_guava_dot_train_0654.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Dot/mendeley_guava_dot_train_0669.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Dot/mendeley_guava_dot_train_0669.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Dot/mendeley_guava_dot_train_0670.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Dot/mendeley_guava_dot_train_0670.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Dot/mendeley_guava_dot_train_0690.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Dot/mendeley_guava_dot_train_0690.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Dot/mendeley_guava_dot_train_0692.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Dot/mendeley_guava_dot_train_0692.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Dot/mendeley_guava_dot_train_0697.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Dot/mendeley_guava_dot_train_0697.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Dot/mendeley_guava_dot_train_0698.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Dot/mendeley_guava_dot_train_0698.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Healthy/mendeley_guava_healthy_train_0003.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Healthy/mendeley_guava_healthy_train_0003.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Healthy/mendeley_guava_healthy_train_0005.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Healthy/mendeley_guava_healthy_train_0005.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Healthy/mendeley_guava_healthy_train_0014.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Healthy/mendeley_guava_healthy_train_0014.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Healthy/mendeley_guava_healthy_train_0033.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Healthy/mendeley_guava_healthy_train_0033.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Healthy/mendeley_guava_healthy_train_0043.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Healthy/mendeley_guava_healthy_train_0043.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Healthy/mendeley_guava_healthy_train_0055.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Healthy/mendeley_guava_healthy_train_0055.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Healthy/mendeley_guava_healthy_train_0060.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Healthy/mendeley_guava_healthy_train_0060.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Healthy/mendeley_guava_healthy_train_0063.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Healthy/mendeley_guava_healthy_train_0063.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Healthy/mendeley_guava_healthy_train_0064.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Healthy/mendeley_guava_healthy_train_0064.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Healthy/mendeley_guava_healthy_train_0082.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Healthy/mendeley_guava_healthy_train_0082.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Healthy/mendeley_guava_healthy_train_0101.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Healthy/mendeley_guava_healthy_train_0101.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Healthy/mendeley_guava_healthy_train_0115.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Healthy/mendeley_guava_healthy_train_0115.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Healthy/mendeley_guava_healthy_train_0135.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Healthy/mendeley_guava_healthy_train_0135.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Healthy/mendeley_guava_healthy_train_0147.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Healthy/mendeley_guava_healthy_train_0147.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Healthy/mendeley_guava_healthy_train_0154.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Healthy/mendeley_guava_healthy_train_0154.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Healthy/mendeley_guava_healthy_train_0192.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Healthy/mendeley_guava_healthy_train_0192.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Healthy/mendeley_guava_healthy_train_0199.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Healthy/mendeley_guava_healthy_train_0199.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Healthy/mendeley_guava_healthy_train_0203.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Healthy/mendeley_guava_healthy_train_0203.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Healthy/mendeley_guava_healthy_train_0205.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Healthy/mendeley_guava_healthy_train_0205.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Healthy/mendeley_guava_healthy_train_0212.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Healthy/mendeley_guava_healthy_train_0212.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Healthy/mendeley_guava_healthy_train_0219.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Healthy/mendeley_guava_healthy_train_0219.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Healthy/mendeley_guava_healthy_train_0221.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Healthy/mendeley_guava_healthy_train_0221.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Healthy/mendeley_guava_healthy_train_0233.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Healthy/mendeley_guava_healthy_train_0233.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Healthy/mendeley_guava_healthy_train_0237.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Healthy/mendeley_guava_healthy_train_0237.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Healthy/mendeley_guava_healthy_train_0247.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Healthy/mendeley_guava_healthy_train_0247.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Healthy/mendeley_guava_healthy_train_0259.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Healthy/mendeley_guava_healthy_train_0259.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Healthy/mendeley_guava_healthy_train_0260.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Healthy/mendeley_guava_healthy_train_0260.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Healthy/mendeley_guava_healthy_train_0274.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Healthy/mendeley_guava_healthy_train_0274.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Healthy/mendeley_guava_healthy_train_0282.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Healthy/mendeley_guava_healthy_train_0282.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Healthy/mendeley_guava_healthy_train_0295.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Healthy/mendeley_guava_healthy_train_0295.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Healthy/mendeley_guava_healthy_train_0299.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Healthy/mendeley_guava_healthy_train_0299.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Healthy/mendeley_guava_healthy_train_0308.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Healthy/mendeley_guava_healthy_train_0308.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Healthy/mendeley_guava_healthy_train_0318.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Healthy/mendeley_guava_healthy_train_0318.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Healthy/mendeley_guava_healthy_train_0322.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Healthy/mendeley_guava_healthy_train_0322.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Healthy/mendeley_guava_healthy_train_0327.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Healthy/mendeley_guava_healthy_train_0327.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Healthy/mendeley_guava_healthy_train_0334.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Healthy/mendeley_guava_healthy_train_0334.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Healthy/mendeley_guava_healthy_train_0349.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Healthy/mendeley_guava_healthy_train_0349.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Healthy/mendeley_guava_healthy_train_0369.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Healthy/mendeley_guava_healthy_train_0369.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Healthy/mendeley_guava_healthy_train_0397.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Healthy/mendeley_guava_healthy_train_0397.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Healthy/mendeley_guava_healthy_train_0399.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Healthy/mendeley_guava_healthy_train_0399.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Healthy/mendeley_guava_healthy_train_0426.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Healthy/mendeley_guava_healthy_train_0426.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Healthy/mendeley_guava_healthy_train_0437.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Healthy/mendeley_guava_healthy_train_0437.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Healthy/mendeley_guava_healthy_train_0452.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Healthy/mendeley_guava_healthy_train_0452.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Healthy/mendeley_guava_healthy_train_0485.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Healthy/mendeley_guava_healthy_train_0485.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Healthy/mendeley_guava_healthy_train_0486.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Healthy/mendeley_guava_healthy_train_0486.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Healthy/mendeley_guava_healthy_train_0487.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Healthy/mendeley_guava_healthy_train_0487.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Healthy/mendeley_guava_healthy_train_0490.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Healthy/mendeley_guava_healthy_train_0490.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Healthy/mendeley_guava_healthy_train_0495.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Healthy/mendeley_guava_healthy_train_0495.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Healthy/mendeley_guava_healthy_train_0500.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Healthy/mendeley_guava_healthy_train_0500.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Healthy/mendeley_guava_healthy_train_0540.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Healthy/mendeley_guava_healthy_train_0540.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Healthy/mendeley_guava_healthy_train_0543.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Healthy/mendeley_guava_healthy_train_0543.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Healthy/mendeley_guava_healthy_train_0545.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Healthy/mendeley_guava_healthy_train_0545.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Healthy/mendeley_guava_healthy_train_0555.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Healthy/mendeley_guava_healthy_train_0555.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Healthy/mendeley_guava_healthy_train_0560.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Healthy/mendeley_guava_healthy_train_0560.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Healthy/mendeley_guava_healthy_train_0563.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Healthy/mendeley_guava_healthy_train_0563.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Healthy/mendeley_guava_healthy_train_0578.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Healthy/mendeley_guava_healthy_train_0578.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Healthy/mendeley_guava_healthy_train_0583.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Healthy/mendeley_guava_healthy_train_0583.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Healthy/mendeley_guava_healthy_train_0598.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Healthy/mendeley_guava_healthy_train_0598.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Healthy/mendeley_guava_healthy_train_0599.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Healthy/mendeley_guava_healthy_train_0599.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Healthy/mendeley_guava_healthy_train_0602.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Healthy/mendeley_guava_healthy_train_0602.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Healthy/mendeley_guava_healthy_train_0605.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Healthy/mendeley_guava_healthy_train_0605.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Healthy/mendeley_guava_healthy_train_0606.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Healthy/mendeley_guava_healthy_train_0606.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Healthy/mendeley_guava_healthy_train_0613.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Healthy/mendeley_guava_healthy_train_0613.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Healthy/mendeley_guava_healthy_train_0638.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Healthy/mendeley_guava_healthy_train_0638.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Healthy/mendeley_guava_healthy_train_0640.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Healthy/mendeley_guava_healthy_train_0640.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Healthy/mendeley_guava_healthy_train_0649.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Healthy/mendeley_guava_healthy_train_0649.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Healthy/mendeley_guava_healthy_train_0667.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Healthy/mendeley_guava_healthy_train_0667.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Healthy/mendeley_guava_healthy_train_0674.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Healthy/mendeley_guava_healthy_train_0674.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Healthy/mendeley_guava_healthy_train_0682.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Healthy/mendeley_guava_healthy_train_0682.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Healthy/mendeley_guava_healthy_train_0694.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Healthy/mendeley_guava_healthy_train_0694.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Healthy/mendeley_guava_healthy_train_0698.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Healthy/mendeley_guava_healthy_train_0698.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Healthy/mendeley_guava_healthy_train_0716.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Healthy/mendeley_guava_healthy_train_0716.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Healthy/mendeley_guava_healthy_train_0717.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Healthy/mendeley_guava_healthy_train_0717.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Healthy/mendeley_guava_healthy_train_0724.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Healthy/mendeley_guava_healthy_train_0724.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Healthy/mendeley_guava_healthy_train_0743.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Healthy/mendeley_guava_healthy_train_0743.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Healthy/test_0_2206.jpeg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Healthy/test_0_2206.jpeg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Healthy/test_0_7988.jpeg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Healthy/test_0_7988.jpeg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Mummification/test_0_73.jpeg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Mummification/test_0_73.jpeg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Rust/mendeley_guava_rust_train_0011.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Rust/mendeley_guava_rust_train_0011.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Rust/mendeley_guava_rust_train_0031.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Rust/mendeley_guava_rust_train_0031.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Rust/mendeley_guava_rust_train_0036.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Rust/mendeley_guava_rust_train_0036.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Rust/mendeley_guava_rust_train_0037.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Rust/mendeley_guava_rust_train_0037.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Rust/mendeley_guava_rust_train_0050.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Rust/mendeley_guava_rust_train_0050.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Rust/mendeley_guava_rust_train_0060.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Rust/mendeley_guava_rust_train_0060.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Rust/mendeley_guava_rust_train_0065.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Rust/mendeley_guava_rust_train_0065.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Rust/mendeley_guava_rust_train_0066.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Rust/mendeley_guava_rust_train_0066.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Rust/mendeley_guava_rust_train_0077.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Rust/mendeley_guava_rust_train_0077.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Rust/mendeley_guava_rust_train_0078.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Rust/mendeley_guava_rust_train_0078.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Rust/mendeley_guava_rust_train_0107.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Rust/mendeley_guava_rust_train_0107.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Rust/mendeley_guava_rust_train_0113.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Rust/mendeley_guava_rust_train_0113.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Rust/mendeley_guava_rust_train_0122.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Rust/mendeley_guava_rust_train_0122.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Rust/mendeley_guava_rust_train_0124.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Rust/mendeley_guava_rust_train_0124.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Rust/mendeley_guava_rust_train_0126.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Rust/mendeley_guava_rust_train_0126.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Rust/mendeley_guava_rust_train_0139.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Rust/mendeley_guava_rust_train_0139.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Rust/mendeley_guava_rust_train_0157.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Rust/mendeley_guava_rust_train_0157.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Rust/mendeley_guava_rust_train_0159.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Rust/mendeley_guava_rust_train_0159.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Rust/mendeley_guava_rust_train_0170.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Rust/mendeley_guava_rust_train_0170.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Rust/mendeley_guava_rust_train_0174.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Rust/mendeley_guava_rust_train_0174.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Rust/mendeley_guava_rust_train_0175.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Rust/mendeley_guava_rust_train_0175.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Rust/mendeley_guava_rust_train_0187.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Rust/mendeley_guava_rust_train_0187.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Rust/mendeley_guava_rust_train_0196.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Rust/mendeley_guava_rust_train_0196.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Rust/mendeley_guava_rust_train_0200.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Rust/mendeley_guava_rust_train_0200.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Rust/mendeley_guava_rust_train_0209.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Rust/mendeley_guava_rust_train_0209.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Rust/mendeley_guava_rust_train_0214.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Rust/mendeley_guava_rust_train_0214.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Rust/mendeley_guava_rust_train_0222.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Rust/mendeley_guava_rust_train_0222.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Rust/mendeley_guava_rust_train_0226.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Rust/mendeley_guava_rust_train_0226.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Rust/mendeley_guava_rust_train_0256.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Rust/mendeley_guava_rust_train_0256.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Rust/mendeley_guava_rust_train_0257.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Rust/mendeley_guava_rust_train_0257.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Rust/mendeley_guava_rust_train_0259.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Rust/mendeley_guava_rust_train_0259.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Rust/mendeley_guava_rust_train_0260.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Rust/mendeley_guava_rust_train_0260.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Rust/mendeley_guava_rust_train_0264.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Rust/mendeley_guava_rust_train_0264.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Rust/mendeley_guava_rust_train_0290.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Rust/mendeley_guava_rust_train_0290.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Rust/mendeley_guava_rust_train_0342.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Rust/mendeley_guava_rust_train_0342.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Rust/mendeley_guava_rust_train_0361.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Rust/mendeley_guava_rust_train_0361.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Rust/mendeley_guava_rust_train_0368.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Rust/mendeley_guava_rust_train_0368.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Rust/mendeley_guava_rust_train_0369.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Rust/mendeley_guava_rust_train_0369.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Rust/mendeley_guava_rust_train_0370.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Rust/mendeley_guava_rust_train_0370.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Rust/mendeley_guava_rust_train_0373.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Rust/mendeley_guava_rust_train_0373.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Rust/mendeley_guava_rust_train_0378.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Rust/mendeley_guava_rust_train_0378.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Rust/mendeley_guava_rust_train_0379.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Rust/mendeley_guava_rust_train_0379.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Rust/mendeley_guava_rust_train_0392.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Rust/mendeley_guava_rust_train_0392.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Rust/mendeley_guava_rust_train_0406.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Rust/mendeley_guava_rust_train_0406.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Rust/mendeley_guava_rust_train_0431.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Rust/mendeley_guava_rust_train_0431.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Rust/mendeley_guava_rust_train_0454.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Rust/mendeley_guava_rust_train_0454.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Rust/mendeley_guava_rust_train_0463.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Rust/mendeley_guava_rust_train_0463.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Rust/mendeley_guava_rust_train_0478.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Rust/mendeley_guava_rust_train_0478.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Rust/mendeley_guava_rust_train_0481.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Rust/mendeley_guava_rust_train_0481.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Rust/mendeley_guava_rust_train_0489.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Rust/mendeley_guava_rust_train_0489.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Rust/mendeley_guava_rust_train_0518.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Rust/mendeley_guava_rust_train_0518.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Rust/mendeley_guava_rust_train_0527.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Rust/mendeley_guava_rust_train_0527.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Rust/mendeley_guava_rust_train_0530.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Rust/mendeley_guava_rust_train_0530.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Rust/mendeley_guava_rust_train_0572.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Rust/mendeley_guava_rust_train_0572.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Rust/mendeley_guava_rust_train_0577.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Rust/mendeley_guava_rust_train_0577.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Rust/mendeley_guava_rust_train_0579.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Rust/mendeley_guava_rust_train_0579.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Rust/mendeley_guava_rust_train_0580.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Rust/mendeley_guava_rust_train_0580.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Rust/mendeley_guava_rust_train_0588.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Rust/mendeley_guava_rust_train_0588.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Rust/mendeley_guava_rust_train_0589.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Rust/mendeley_guava_rust_train_0589.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Rust/mendeley_guava_rust_train_0611.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Rust/mendeley_guava_rust_train_0611.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Rust/mendeley_guava_rust_train_0625.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Rust/mendeley_guava_rust_train_0625.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Rust/mendeley_guava_rust_train_0626.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Rust/mendeley_guava_rust_train_0626.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Rust/mendeley_guava_rust_train_0631.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Rust/mendeley_guava_rust_train_0631.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Rust/mendeley_guava_rust_train_0647.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Rust/mendeley_guava_rust_train_0647.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Rust/mendeley_guava_rust_train_0650.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Rust/mendeley_guava_rust_train_0650.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Rust/mendeley_guava_rust_train_0672.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Rust/mendeley_guava_rust_train_0672.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Rust/mendeley_guava_rust_train_0690.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Rust/mendeley_guava_rust_train_0690.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Rust/mendeley_guava_rust_train_0699.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Rust/mendeley_guava_rust_train_0699.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Rust/mendeley_guava_rust_train_0707.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Rust/mendeley_guava_rust_train_0707.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Rust/mendeley_guava_rust_train_0732.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Rust/mendeley_guava_rust_train_0732.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Rust/mendeley_guava_rust_train_0737.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Rust/mendeley_guava_rust_train_0737.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Rust/mendeley_guava_rust_train_0746.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Rust/mendeley_guava_rust_train_0746.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Spiraling Whitefly/mendeley_guava_whitefly_train_0001.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Spiraling Whitefly/mendeley_guava_whitefly_train_0001.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Spiraling Whitefly/mendeley_guava_whitefly_train_0017.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Spiraling Whitefly/mendeley_guava_whitefly_train_0017.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Spiraling Whitefly/mendeley_guava_whitefly_train_0025.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Spiraling Whitefly/mendeley_guava_whitefly_train_0025.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Spiraling Whitefly/mendeley_guava_whitefly_train_0052.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Spiraling Whitefly/mendeley_guava_whitefly_train_0052.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Spiraling Whitefly/mendeley_guava_whitefly_train_0060.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Spiraling Whitefly/mendeley_guava_whitefly_train_0060.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Spiraling Whitefly/mendeley_guava_whitefly_train_0090.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Spiraling Whitefly/mendeley_guava_whitefly_train_0090.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Spiraling Whitefly/mendeley_guava_whitefly_train_0106.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Spiraling Whitefly/mendeley_guava_whitefly_train_0106.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Spiraling Whitefly/mendeley_guava_whitefly_train_0121.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Spiraling Whitefly/mendeley_guava_whitefly_train_0121.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Spiraling Whitefly/mendeley_guava_whitefly_train_0147.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Spiraling Whitefly/mendeley_guava_whitefly_train_0147.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Spiraling Whitefly/mendeley_guava_whitefly_train_0149.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Spiraling Whitefly/mendeley_guava_whitefly_train_0149.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Spiraling Whitefly/mendeley_guava_whitefly_train_0204.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Spiraling Whitefly/mendeley_guava_whitefly_train_0204.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Spiraling Whitefly/mendeley_guava_whitefly_train_0206.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Spiraling Whitefly/mendeley_guava_whitefly_train_0206.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Spiraling Whitefly/mendeley_guava_whitefly_train_0215.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Spiraling Whitefly/mendeley_guava_whitefly_train_0215.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Spiraling Whitefly/mendeley_guava_whitefly_train_0220.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Spiraling Whitefly/mendeley_guava_whitefly_train_0220.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Spiraling Whitefly/mendeley_guava_whitefly_train_0241.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Spiraling Whitefly/mendeley_guava_whitefly_train_0241.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Spiraling Whitefly/mendeley_guava_whitefly_train_0249.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Spiraling Whitefly/mendeley_guava_whitefly_train_0249.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Spiraling Whitefly/mendeley_guava_whitefly_train_0287.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Spiraling Whitefly/mendeley_guava_whitefly_train_0287.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Spiraling Whitefly/mendeley_guava_whitefly_train_0296.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Spiraling Whitefly/mendeley_guava_whitefly_train_0296.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Spiraling Whitefly/mendeley_guava_whitefly_train_0297.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Spiraling Whitefly/mendeley_guava_whitefly_train_0297.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Spiraling Whitefly/mendeley_guava_whitefly_train_0325.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Spiraling Whitefly/mendeley_guava_whitefly_train_0325.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Spiraling Whitefly/mendeley_guava_whitefly_train_0330.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Spiraling Whitefly/mendeley_guava_whitefly_train_0330.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Spiraling Whitefly/mendeley_guava_whitefly_train_0410.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Spiraling Whitefly/mendeley_guava_whitefly_train_0410.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Spiraling Whitefly/mendeley_guava_whitefly_train_0435.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Spiraling Whitefly/mendeley_guava_whitefly_train_0435.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Spiraling Whitefly/mendeley_guava_whitefly_train_0446.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Spiraling Whitefly/mendeley_guava_whitefly_train_0446.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Spiraling Whitefly/mendeley_guava_whitefly_train_0454.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Spiraling Whitefly/mendeley_guava_whitefly_train_0454.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Spiraling Whitefly/mendeley_guava_whitefly_train_0455.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Spiraling Whitefly/mendeley_guava_whitefly_train_0455.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Spiraling Whitefly/mendeley_guava_whitefly_train_0464.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Spiraling Whitefly/mendeley_guava_whitefly_train_0464.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Spiraling Whitefly/mendeley_guava_whitefly_train_0469.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Spiraling Whitefly/mendeley_guava_whitefly_train_0469.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Spiraling Whitefly/mendeley_guava_whitefly_train_0472.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Spiraling Whitefly/mendeley_guava_whitefly_train_0472.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Spiraling Whitefly/mendeley_guava_whitefly_train_0483.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Spiraling Whitefly/mendeley_guava_whitefly_train_0483.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Spiraling Whitefly/mendeley_guava_whitefly_train_0490.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Spiraling Whitefly/mendeley_guava_whitefly_train_0490.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Spiraling Whitefly/mendeley_guava_whitefly_train_0497.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Spiraling Whitefly/mendeley_guava_whitefly_train_0497.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Spiraling Whitefly/mendeley_guava_whitefly_train_0501.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Spiraling Whitefly/mendeley_guava_whitefly_train_0501.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Spiraling Whitefly/mendeley_guava_whitefly_train_0508.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Spiraling Whitefly/mendeley_guava_whitefly_train_0508.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Spiraling Whitefly/mendeley_guava_whitefly_train_0523.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Spiraling Whitefly/mendeley_guava_whitefly_train_0523.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Spiraling Whitefly/mendeley_guava_whitefly_train_0549.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Spiraling Whitefly/mendeley_guava_whitefly_train_0549.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Spiraling Whitefly/mendeley_guava_whitefly_train_0554.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Spiraling Whitefly/mendeley_guava_whitefly_train_0554.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Spiraling Whitefly/mendeley_guava_whitefly_train_0556.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Spiraling Whitefly/mendeley_guava_whitefly_train_0556.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Spiraling Whitefly/mendeley_guava_whitefly_train_0559.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Spiraling Whitefly/mendeley_guava_whitefly_train_0559.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Spiraling Whitefly/mendeley_guava_whitefly_train_0564.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Spiraling Whitefly/mendeley_guava_whitefly_train_0564.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Spiraling Whitefly/mendeley_guava_whitefly_train_0603.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Spiraling Whitefly/mendeley_guava_whitefly_train_0603.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Spiraling Whitefly/mendeley_guava_whitefly_train_0620.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Spiraling Whitefly/mendeley_guava_whitefly_train_0620.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Spiraling Whitefly/mendeley_guava_whitefly_train_0631.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Spiraling Whitefly/mendeley_guava_whitefly_train_0631.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Spiraling Whitefly/mendeley_guava_whitefly_train_0636.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Spiraling Whitefly/mendeley_guava_whitefly_train_0636.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Spiraling Whitefly/mendeley_guava_whitefly_train_0660.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Spiraling Whitefly/mendeley_guava_whitefly_train_0660.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Spiraling Whitefly/mendeley_guava_whitefly_train_0685.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Spiraling Whitefly/mendeley_guava_whitefly_train_0685.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Spiraling Whitefly/mendeley_guava_whitefly_train_0706.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Spiraling Whitefly/mendeley_guava_whitefly_train_0706.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Spiraling Whitefly/mendeley_guava_whitefly_train_0708.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Spiraling Whitefly/mendeley_guava_whitefly_train_0708.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Spiraling Whitefly/mendeley_guava_whitefly_train_0722.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Spiraling Whitefly/mendeley_guava_whitefly_train_0722.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Guava - Spiraling Whitefly/mendeley_guava_whitefly_train_0744.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Guava - Spiraling Whitefly/mendeley_guava_whitefly_train_0744.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Jamun - Bacterial Spot/jamun_bacterial_spot_train_0002.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Jamun - Bacterial Spot/jamun_bacterial_spot_train_0002.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Jamun - Bacterial Spot/jamun_bacterial_spot_train_0034.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Jamun - Bacterial Spot/jamun_bacterial_spot_train_0034.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Jamun - Bacterial Spot/jamun_bacterial_spot_train_0101.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Jamun - Bacterial Spot/jamun_bacterial_spot_train_0101.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Jamun - Bacterial Spot/jamun_bacterial_spot_train_0138.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Jamun - Bacterial Spot/jamun_bacterial_spot_train_0138.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Jamun - Bacterial Spot/jamun_bacterial_spot_train_0184.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Jamun - Bacterial Spot/jamun_bacterial_spot_train_0184.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Jamun - Bacterial Spot/jamun_bacterial_spot_train_0200.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Jamun - Bacterial Spot/jamun_bacterial_spot_train_0200.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Jamun - Bacterial Spot/jamun_bacterial_spot_train_0310.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Jamun - Bacterial Spot/jamun_bacterial_spot_train_0310.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Jamun - Brown Blight/jamun_brown_blight_train_0053.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Jamun - Brown Blight/jamun_brown_blight_train_0053.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Jamun - Brown Blight/jamun_brown_blight_train_0145.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Jamun - Brown Blight/jamun_brown_blight_train_0145.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Jamun - Brown Blight/jamun_brown_blight_train_0153.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Jamun - Brown Blight/jamun_brown_blight_train_0153.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Jamun - Brown Blight/jamun_brown_blight_train_0265.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Jamun - Brown Blight/jamun_brown_blight_train_0265.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Jamun - Powdery Mildew/jamun_powdery_mildew_train_0096.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Jamun - Powdery Mildew/jamun_powdery_mildew_train_0096.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Jamun - Powdery Mildew/jamun_powdery_mildew_train_0147.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Jamun - Powdery Mildew/jamun_powdery_mildew_train_0147.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Jamun - Powdery Mildew/jamun_powdery_mildew_train_0206.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Jamun - Powdery Mildew/jamun_powdery_mildew_train_0206.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Jamun - Powdery Mildew/jamun_powdery_mildew_train_0212.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Jamun - Powdery Mildew/jamun_powdery_mildew_train_0212.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Jamun - Powdery Mildew/jamun_powdery_mildew_train_0213.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Jamun - Powdery Mildew/jamun_powdery_mildew_train_0213.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Jamun - Powdery Mildew/jamun_powdery_mildew_train_0216.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Jamun - Powdery Mildew/jamun_powdery_mildew_train_0216.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Jamun - Powdery Mildew/jamun_powdery_mildew_train_0248.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Jamun - Powdery Mildew/jamun_powdery_mildew_train_0248.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Jamun - Powdery Mildew/jamun_powdery_mildew_train_0261.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Jamun - Powdery Mildew/jamun_powdery_mildew_train_0261.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Jamun - Powdery Mildew/jamun_powdery_mildew_train_0280.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Jamun - Powdery Mildew/jamun_powdery_mildew_train_0280.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Jamun - Powdery Mildew/jamun_powdery_mildew_train_0285.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Jamun - Powdery Mildew/jamun_powdery_mildew_train_0285.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Jamun - Powdery Mildew/jamun_powdery_mildew_train_0319.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Jamun - Powdery Mildew/jamun_powdery_mildew_train_0319.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Jamun - Sooty Mold/jamun_sooty_mold_train_0015.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Jamun - Sooty Mold/jamun_sooty_mold_train_0015.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Jamun - Sooty Mold/jamun_sooty_mold_train_0167.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Jamun - Sooty Mold/jamun_sooty_mold_train_0167.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Jamun - Sooty Mold/jamun_sooty_mold_train_0231.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Jamun - Sooty Mold/jamun_sooty_mold_train_0231.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Mango - Anthracnose/IMG_20211011_160602 (Custom).jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Mango - Anthracnose/IMG_20211011_160602 (Custom).jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Mango - Anthracnose/IMG_20211011_164346 (Custom).jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Mango - Anthracnose/IMG_20211011_164346 (Custom).jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Mango - Bacterial Canker/IMG_20211106_120928 (Custom).jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Mango - Bacterial Canker/IMG_20211106_120928 (Custom).jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Mango - Bacterial Canker/IMG_20211106_135747 (Custom).jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Mango - Bacterial Canker/IMG_20211106_135747 (Custom).jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Mango - Die Back/20211129_162005 (Custom).jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Mango - Die Back/20211129_162005 (Custom).jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Mango - Healthy/20211231_123105 (Custom).jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Mango - Healthy/20211231_123105 (Custom).jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Mango - Healthy/20211231_124442 (Custom).jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Mango - Healthy/20211231_124442 (Custom).jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Mango - Healthy/20211231_124834 (Custom).jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Mango - Healthy/20211231_124834 (Custom).jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Mango - Healthy/20211231_155455 (Custom).jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Mango - Healthy/20211231_155455 (Custom).jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Mango - Powdery Mildew/IMG_20211107_125219 (Custom).jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Mango - Powdery Mildew/IMG_20211107_125219 (Custom).jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Mango - Powdery Mildew/IMG_20211107_130143 (Custom).jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Mango - Powdery Mildew/IMG_20211107_130143 (Custom).jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Paddy - Bacterial Leaf Blight/rice_lab_bacterial_leaf_blight (163).jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Paddy - Bacterial Leaf Blight/rice_lab_bacterial_leaf_blight (163).jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Paddy - Blast/rice_lab_leaf_blast (121).jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Paddy - Blast/rice_lab_leaf_blast (121).jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Paddy - Blast/rice_lab_leaf_blast (123).jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Paddy - Blast/rice_lab_leaf_blast (123).jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Paddy - Blast/rice_lab_leaf_blast (132).jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Paddy - Blast/rice_lab_leaf_blast (132).jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Paddy - Blast/rice_lab_leaf_blast (139).jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Paddy - Blast/rice_lab_leaf_blast (139).jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Paddy - Blast/rice_lab_leaf_blast (303).jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Paddy - Blast/rice_lab_leaf_blast (303).jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Paddy - Blast/rice_lab_leaf_blast (305).jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Paddy - Blast/rice_lab_leaf_blast (305).jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Paddy - Healthy/rice_lab_healthy (147).jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Paddy - Healthy/rice_lab_healthy (147).jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Paddy - Healthy/rice_lab_healthy (53).jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Paddy - Healthy/rice_lab_healthy (53).jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Paddy - Leaf Scald/rice_lab_leaf_scald (118).jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Paddy - Leaf Scald/rice_lab_leaf_scald (118).jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Paddy - Leaf Scald/rice_lab_leaf_scald (147).jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Paddy - Leaf Scald/rice_lab_leaf_scald (147).jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Paddy - Leaf Scald/rice_lab_leaf_scald (206).jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Paddy - Leaf Scald/rice_lab_leaf_scald (206).jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Paddy - Leaf Scald/rice_lab_leaf_scald (260).jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Paddy - Leaf Scald/rice_lab_leaf_scald (260).jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Paddy - Leaf Scald/rice_lab_leaf_scald (261).jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Paddy - Leaf Scald/rice_lab_leaf_scald (261).jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Paddy - Leaf Scald/rice_lab_leaf_scald (323).jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Paddy - Leaf Scald/rice_lab_leaf_scald (323).jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Paddy - Leaf Scald/rice_lab_leaf_scald (325).jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Paddy - Leaf Scald/rice_lab_leaf_scald (325).jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Paddy - Leaf Scald/rice_lab_leaf_scald (331).jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Paddy - Leaf Scald/rice_lab_leaf_scald (331).jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Paddy - Leaf Scald/rice_lab_leaf_scald (55).jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Paddy - Leaf Scald/rice_lab_leaf_scald (55).jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Paddy - Leaf Scald/rice_lab_leaf_scald (62).jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Paddy - Leaf Scald/rice_lab_leaf_scald (62).jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Paddy - Narrow Brown Spot/rice_lab_narrow_brown (119).jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Paddy - Narrow Brown Spot/rice_lab_narrow_brown (119).jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Paddy - Narrow Brown Spot/rice_lab_narrow_brown (132).jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Paddy - Narrow Brown Spot/rice_lab_narrow_brown (132).jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Paddy - Narrow Brown Spot/rice_lab_narrow_brown (146).jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Paddy - Narrow Brown Spot/rice_lab_narrow_brown (146).jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Paddy - Narrow Brown Spot/rice_lab_narrow_brown (149).jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Paddy - Narrow Brown Spot/rice_lab_narrow_brown (149).jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Paddy - Narrow Brown Spot/rice_lab_narrow_brown (157).jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Paddy - Narrow Brown Spot/rice_lab_narrow_brown (157).jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Paddy - Narrow Brown Spot/rice_lab_narrow_brown (230).jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Paddy - Narrow Brown Spot/rice_lab_narrow_brown (230).jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Paddy - Narrow Brown Spot/rice_lab_narrow_brown (290).jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Paddy - Narrow Brown Spot/rice_lab_narrow_brown (290).jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Paddy - Narrow Brown Spot/rice_lab_narrow_brown (335).jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Paddy - Narrow Brown Spot/rice_lab_narrow_brown (335).jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Paddy - Narrow Brown Spot/rice_lab_narrow_brown (75).jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Paddy - Narrow Brown Spot/rice_lab_narrow_brown (75).jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Paddy - Narrow Brown Spot/rice_lab_narrow_brown (79).jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Paddy - Narrow Brown Spot/rice_lab_narrow_brown (79).jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Pear - Healthy/plantcity_pear_healthy_train_00021.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Pear - Healthy/plantcity_pear_healthy_train_00021.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Pear - Healthy/plantcity_pear_healthy_train_00240.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Pear - Healthy/plantcity_pear_healthy_train_00240.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Plum - Healthy/plum_healthy_ronokhasan_train_00020.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Plum - Healthy/plum_healthy_ronokhasan_train_00020.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Plum - plum insect hole/363_lab.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Plum - plum insect hole/363_lab.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Plum - plum insect hole/364_lab.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Plum - plum insect hole/364_lab.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Plum - plum insect hole/50_lab.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Plum - plum insect hole/50_lab.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Plum - plum insect hole/536_lab.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Plum - plum insect hole/536_lab.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Radish - Black leaf spot/img_00051248.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Radish - Black leaf spot/img_00051248.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Radish - Black leaf spot/img_00054057.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Radish - Black leaf spot/img_00054057.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Radish - Black leaf spot/img_00055721.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Radish - Black leaf spot/img_00055721.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Radish - Black leaf spot/img_00055876.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Radish - Black leaf spot/img_00055876.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Radish - Black leaf spot/img_00057446.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Radish - Black leaf spot/img_00057446.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Radish - Black leaf spot/img_00058964.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Radish - Black leaf spot/img_00058964.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Radish - Black leaf spot/img_00059182.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Radish - Black leaf spot/img_00059182.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Radish - Black leaf spot/img_00059813.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Radish - Black leaf spot/img_00059813.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Radish - Downey mildew/img_00045611.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Radish - Downey mildew/img_00045611.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Radish - Downey mildew/img_00045981.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Radish - Downey mildew/img_00045981.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Radish - Downey mildew/img_00048071.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Radish - Downey mildew/img_00048071.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Radish - Downey mildew/img_00059523.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Radish - Downey mildew/img_00059523.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Radish - Downey mildew/img_00062187.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Radish - Downey mildew/img_00062187.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Radish - Flea beetle/img_00047281.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Radish - Flea beetle/img_00047281.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Radish - Flea beetle/img_00050322.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Radish - Flea beetle/img_00050322.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Radish - Flea beetle/img_00051988.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Radish - Flea beetle/img_00051988.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Radish - Flea beetle/img_00053348.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Radish - Flea beetle/img_00053348.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Radish - Flea beetle/img_00053903.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Radish - Flea beetle/img_00053903.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Radish - Flea beetle/img_00054097.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Radish - Flea beetle/img_00054097.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Radish - Flea beetle/img_00061470.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Radish - Flea beetle/img_00061470.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Radish - Healthy/img_00046390.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Radish - Healthy/img_00046390.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Radish - Healthy/img_00046486.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Radish - Healthy/img_00046486.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Radish - Healthy/img_00047239.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Radish - Healthy/img_00047239.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Radish - Healthy/img_00049773.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Radish - Healthy/img_00049773.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Radish - Healthy/img_00050839.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Radish - Healthy/img_00050839.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Radish - Healthy/img_00055900.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Radish - Healthy/img_00055900.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Radish - Healthy/img_00056110.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Radish - Healthy/img_00056110.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Radish - Healthy/img_00062458.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Radish - Healthy/img_00062458.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Radish - Healthy/img_00064704.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Radish - Healthy/img_00064704.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Soybean - Healthy/scraped_kaggle_pv2_12b19357-38b6-4292-b9fc-a7be66faeaec___RS_HL 3648.JPG"
    dst_p = PROJECT_ROOT / "data/processed/train/Soybean - Healthy/scraped_kaggle_pv2_12b19357-38b6-4292-b9fc-a7be66faeaec___RS_HL 3648.JPG"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Soybean - Powdery Mildew/soybean_powdery_mildew_sivm_train_00009.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Soybean - Powdery Mildew/soybean_powdery_mildew_sivm_train_00009.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Soybean - Powdery Mildew/soybean_powdery_mildew_sivm_train_00037.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Soybean - Powdery Mildew/soybean_powdery_mildew_sivm_train_00037.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Soybean - Powdery Mildew/soybean_powdery_mildew_sivm_train_00061.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Soybean - Powdery Mildew/soybean_powdery_mildew_sivm_train_00061.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Soybean - Rust/img_00040632.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Soybean - Rust/img_00040632.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Tomato - Bacterial Spot/img_00017345.JPG"
    dst_p = PROJECT_ROOT / "data/processed/train/Tomato - Bacterial Spot/img_00017345.JPG"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Tomato - Bacterial Spot/img_00017600.JPG"
    dst_p = PROJECT_ROOT / "data/processed/train/Tomato - Bacterial Spot/img_00017600.JPG"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Tomato - Spider Mites/img_00026524.JPG"
    dst_p = PROJECT_ROOT / "data/processed/train/Tomato - Spider Mites/img_00026524.JPG"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/train/Zucchini - zucchini powdery mildew/img_00043069.jpg"
    dst_p = PROJECT_ROOT / "data/processed/train/Zucchini - zucchini powdery mildew/img_00043069.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Apple - Healthy/scraped_kaggle_pv2_3c047601-ed4d-4178-8bed-33a65e5f4b6d___RS_HL 6001.JPG"
    dst_p = PROJECT_ROOT / "data/processed/val/Apple - Healthy/scraped_kaggle_pv2_3c047601-ed4d-4178-8bed-33a65e5f4b6d___RS_HL 6001.JPG"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Banana - Pestalotiopsis/img_00066527.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Banana - Pestalotiopsis/img_00066527.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Bean - bean rust/img_00035813.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Bean - bean rust/img_00035813.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Bell Pepper - Healthy/img_00027266.JPG"
    dst_p = PROJECT_ROOT / "data/processed/val/Bell Pepper - Healthy/img_00027266.JPG"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Bell Pepper - Healthy/img_00027330.JPG"
    dst_p = PROJECT_ROOT / "data/processed/val/Bell Pepper - Healthy/img_00027330.JPG"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Bell Pepper - bell pepper frogeye leaf spot/bell_pepper_frogeye_mendeley_val_00008.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Bell Pepper - bell pepper frogeye leaf spot/bell_pepper_frogeye_mendeley_val_00008.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Bell Pepper - bell pepper frogeye leaf spot/bell_pepper_frogeye_mendeley_val_00009.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Bell Pepper - bell pepper frogeye leaf spot/bell_pepper_frogeye_mendeley_val_00009.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Bell Pepper - bell pepper frogeye leaf spot/bell_pepper_frogeye_mendeley_val_00012.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Bell Pepper - bell pepper frogeye leaf spot/bell_pepper_frogeye_mendeley_val_00012.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Bell Pepper - bell pepper frogeye leaf spot/bell_pepper_frogeye_mendeley_val_00013.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Bell Pepper - bell pepper frogeye leaf spot/bell_pepper_frogeye_mendeley_val_00013.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Bell Pepper - bell pepper frogeye leaf spot/bell_pepper_frogeye_mendeley_val_00019.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Bell Pepper - bell pepper frogeye leaf spot/bell_pepper_frogeye_mendeley_val_00019.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Bell Pepper - bell pepper frogeye leaf spot/bell_pepper_frogeye_mendeley_val_00030.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Bell Pepper - bell pepper frogeye leaf spot/bell_pepper_frogeye_mendeley_val_00030.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Bell Pepper - bell pepper frogeye leaf spot/bell_pepper_frogeye_mendeley_val_00036.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Bell Pepper - bell pepper frogeye leaf spot/bell_pepper_frogeye_mendeley_val_00036.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Bell Pepper - bell pepper frogeye leaf spot/bell_pepper_frogeye_mendeley_val_00038.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Bell Pepper - bell pepper frogeye leaf spot/bell_pepper_frogeye_mendeley_val_00038.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Bell Pepper - bell pepper frogeye leaf spot/bell_pepper_frogeye_mendeley_val_00044.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Bell Pepper - bell pepper frogeye leaf spot/bell_pepper_frogeye_mendeley_val_00044.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Bell Pepper - bell pepper frogeye leaf spot/bell_pepper_frogeye_mendeley_val_00045.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Bell Pepper - bell pepper frogeye leaf spot/bell_pepper_frogeye_mendeley_val_00045.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Bell Pepper - bell pepper frogeye leaf spot/bell_pepper_frogeye_mendeley_val_00048.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Bell Pepper - bell pepper frogeye leaf spot/bell_pepper_frogeye_mendeley_val_00048.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Bell Pepper - bell pepper frogeye leaf spot/bell_pepper_frogeye_mendeley_val_00049.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Bell Pepper - bell pepper frogeye leaf spot/bell_pepper_frogeye_mendeley_val_00049.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Bell Pepper - bell pepper frogeye leaf spot/bell_pepper_frogeye_mendeley_val_00055.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Bell Pepper - bell pepper frogeye leaf spot/bell_pepper_frogeye_mendeley_val_00055.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Bell Pepper - bell pepper frogeye leaf spot/bell_pepper_frogeye_mendeley_val_00059.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Bell Pepper - bell pepper frogeye leaf spot/bell_pepper_frogeye_mendeley_val_00059.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Bell Pepper - bell pepper frogeye leaf spot/bell_pepper_frogeye_mendeley_val_00060.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Bell Pepper - bell pepper frogeye leaf spot/bell_pepper_frogeye_mendeley_val_00060.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Bell Pepper - bell pepper frogeye leaf spot/bell_pepper_frogeye_mendeley_val_00065.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Bell Pepper - bell pepper frogeye leaf spot/bell_pepper_frogeye_mendeley_val_00065.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Bell Pepper - bell pepper frogeye leaf spot/bell_pepper_frogeye_mendeley_val_00071.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Bell Pepper - bell pepper frogeye leaf spot/bell_pepper_frogeye_mendeley_val_00071.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Bell Pepper - bell pepper frogeye leaf spot/bell_pepper_frogeye_mendeley_val_00078.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Bell Pepper - bell pepper frogeye leaf spot/bell_pepper_frogeye_mendeley_val_00078.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Bell Pepper - bell pepper frogeye leaf spot/bell_pepper_frogeye_mendeley_val_00079.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Bell Pepper - bell pepper frogeye leaf spot/bell_pepper_frogeye_mendeley_val_00079.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Bell Pepper - bell pepper frogeye leaf spot/bell_pepper_frogeye_mendeley_val_00086.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Bell Pepper - bell pepper frogeye leaf spot/bell_pepper_frogeye_mendeley_val_00086.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Bell Pepper - bell pepper frogeye leaf spot/bell_pepper_frogeye_mendeley_val_00099.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Bell Pepper - bell pepper frogeye leaf spot/bell_pepper_frogeye_mendeley_val_00099.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Bell Pepper - bell pepper frogeye leaf spot/bell_pepper_frogeye_mendeley_val_00113.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Bell Pepper - bell pepper frogeye leaf spot/bell_pepper_frogeye_mendeley_val_00113.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Bell Pepper - bell pepper frogeye leaf spot/bell_pepper_frogeye_mendeley_val_00125.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Bell Pepper - bell pepper frogeye leaf spot/bell_pepper_frogeye_mendeley_val_00125.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Bell Pepper - bell pepper frogeye leaf spot/bell_pepper_frogeye_mendeley_val_00127.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Bell Pepper - bell pepper frogeye leaf spot/bell_pepper_frogeye_mendeley_val_00127.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Blackgram - Healthy/img_00000981.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Blackgram - Healthy/img_00000981.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Blueberry - Healthy/scraped_kaggle_pv2_4e81dc73-7a2b-4398-8cb5-df2068ed6a57___RS_HL 2424.JPG"
    dst_p = PROJECT_ROOT / "data/processed/val/Blueberry - Healthy/scraped_kaggle_pv2_4e81dc73-7a2b-4398-8cb5-df2068ed6a57___RS_HL 2424.JPG"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Cauliflower - Downy mildew/img_00058902.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Cauliflower - Downy mildew/img_00058902.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Chilli - Healthy/chilli_-_healthy_val_00150.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Chilli - Healthy/chilli_-_healthy_val_00150.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Chilli - Leaf Curl Virus/chilli_-_leaf_curl_virus_val_00134.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Chilli - Leaf Curl Virus/chilli_-_leaf_curl_virus_val_00134.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Chilli - Leaf Curl Virus/chilli_-_leaf_curl_virus_val_00197.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Chilli - Leaf Curl Virus/chilli_-_leaf_curl_virus_val_00197.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Chilli - Nutrition Deficiency/chilli_-_nutrition_deficiency_val_00181.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Chilli - Nutrition Deficiency/chilli_-_nutrition_deficiency_val_00181.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Citrus - citrus greening disease/scraped_kaggle_pv2_00543c40-4cd3-413a-a152-5ceeffea98a0___UF.Citrus_HLB_Lab 0440.JPG"
    dst_p = PROJECT_ROOT / "data/processed/val/Citrus - citrus greening disease/scraped_kaggle_pv2_00543c40-4cd3-413a-a152-5ceeffea98a0___UF.Citrus_HLB_Lab 0440.JPG"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Citrus - citrus greening disease/sourabh_g (21).png"
    dst_p = PROJECT_ROOT / "data/processed/val/Citrus - citrus greening disease/sourabh_g (21).png"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Cucumber - cucumber powdery mildew/img_00038240.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Cucumber - cucumber powdery mildew/img_00038240.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Eggplant - Little Leaf/eggplant_little_leaf_val_00007.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Eggplant - Little Leaf/eggplant_little_leaf_val_00007.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Ginger - Bacterial Wilt/ginger_bacterial_wilt_val_00001.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Ginger - Bacterial Wilt/ginger_bacterial_wilt_val_00001.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Ginger - Bacterial Wilt/ginger_bacterial_wilt_val_00002.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Ginger - Bacterial Wilt/ginger_bacterial_wilt_val_00002.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Ginger - Bacterial Wilt/ginger_bacterial_wilt_val_00006.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Ginger - Bacterial Wilt/ginger_bacterial_wilt_val_00006.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Ginger - Bacterial Wilt/ginger_bacterial_wilt_val_00009.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Ginger - Bacterial Wilt/ginger_bacterial_wilt_val_00009.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Ginger - Bacterial Wilt/ginger_bacterial_wilt_val_00010.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Ginger - Bacterial Wilt/ginger_bacterial_wilt_val_00010.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Ginger - Bacterial Wilt/ginger_bacterial_wilt_val_00011.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Ginger - Bacterial Wilt/ginger_bacterial_wilt_val_00011.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Ginger - Dehydrated/ginger_dehydrated_val_00009.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Ginger - Dehydrated/ginger_dehydrated_val_00009.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Ginger - Dehydrated/ginger_dehydrated_val_00081.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Ginger - Dehydrated/ginger_dehydrated_val_00081.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Ginger - Dehydrated/ginger_dehydrated_val_00092.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Ginger - Dehydrated/ginger_dehydrated_val_00092.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Ginger - Dehydrated/ginger_dehydrated_val_00094.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Ginger - Dehydrated/ginger_dehydrated_val_00094.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Ginger - Dehydrated/ginger_dehydrated_val_00189.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Ginger - Dehydrated/ginger_dehydrated_val_00189.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Ginger - Dehydrated/ginger_dehydrated_val_00260.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Ginger - Dehydrated/ginger_dehydrated_val_00260.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Ginger - Healthy/ginger_healthy_val_00105.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Ginger - Healthy/ginger_healthy_val_00105.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Ginger - Leaf Blight/ginger_leaf_blight_val_00049.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Ginger - Leaf Blight/ginger_leaf_blight_val_00049.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Ginger - Leaf Blight/ginger_leaf_blight_val_00090.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Ginger - Leaf Blight/ginger_leaf_blight_val_00090.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Ginger - Leaf Blight/ginger_leaf_blight_val_00206.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Ginger - Leaf Blight/ginger_leaf_blight_val_00206.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Ginger - Leaf Blight/ginger_leaf_blight_val_00221.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Ginger - Leaf Blight/ginger_leaf_blight_val_00221.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Ginger - Pest Damage/ginger_pest_damage_val_00048.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Ginger - Pest Damage/ginger_pest_damage_val_00048.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Grape - Esca (Black Measles)/grape_esca_val_00038.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Grape - Esca (Black Measles)/grape_esca_val_00038.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Grape - Esca (Black Measles)/grape_esca_val_00174.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Grape - Esca (Black Measles)/grape_esca_val_00174.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Grape - grape bacterial rot/grape_bacterial_rot_val_00005.png"
    dst_p = PROJECT_ROOT / "data/processed/val/Grape - grape bacterial rot/grape_bacterial_rot_val_00005.png"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Groundnut - Early leaf spot/img_00064344.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Groundnut - Early leaf spot/img_00064344.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Groundnut - Early rust/img_00046807.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Groundnut - Early rust/img_00046807.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Groundnut - Early rust/img_00047406.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Groundnut - Early rust/img_00047406.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Groundnut - Early rust/img_00047818.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Groundnut - Early rust/img_00047818.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Groundnut - Early rust/img_00050242.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Groundnut - Early rust/img_00050242.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Groundnut - Early rust/img_00050571.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Groundnut - Early rust/img_00050571.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Groundnut - Early rust/img_00051704.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Groundnut - Early rust/img_00051704.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Groundnut - Early rust/img_00055404.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Groundnut - Early rust/img_00055404.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Groundnut - Early rust/img_00056070.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Groundnut - Early rust/img_00056070.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Groundnut - Early rust/img_00056535.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Groundnut - Early rust/img_00056535.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Groundnut - Early rust/img_00058518.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Groundnut - Early rust/img_00058518.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Groundnut - Early rust/img_00066661.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Groundnut - Early rust/img_00066661.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Groundnut - Healthy/img_00047384.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Groundnut - Healthy/img_00047384.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Groundnut - Healthy/img_00055221.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Groundnut - Healthy/img_00055221.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Groundnut - Late leaf spot/img_00047315.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Groundnut - Late leaf spot/img_00047315.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Groundnut - Late leaf spot/img_00055142.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Groundnut - Late leaf spot/img_00055142.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Groundnut - Late leaf spot/img_00055965.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Groundnut - Late leaf spot/img_00055965.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Groundnut - Late leaf spot/img_00061186.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Groundnut - Late leaf spot/img_00061186.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Groundnut - Late leaf spot/img_00065446.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Groundnut - Late leaf spot/img_00065446.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Groundnut - Nutrition deficiency/img_00048626.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Groundnut - Nutrition deficiency/img_00048626.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Groundnut - Nutrition deficiency/img_00050154.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Groundnut - Nutrition deficiency/img_00050154.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Groundnut - Nutrition deficiency/img_00055507.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Groundnut - Nutrition deficiency/img_00055507.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Groundnut - Nutrition deficiency/img_00065660.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Groundnut - Nutrition deficiency/img_00065660.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Groundnut - Rust/img_00045400.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Groundnut - Rust/img_00045400.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Groundnut - Rust/img_00045497.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Groundnut - Rust/img_00045497.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Groundnut - Rust/img_00052362.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Groundnut - Rust/img_00052362.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Groundnut - Rust/img_00054780.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Groundnut - Rust/img_00054780.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Groundnut - Rust/img_00055413.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Groundnut - Rust/img_00055413.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Groundnut - Rust/img_00061647.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Groundnut - Rust/img_00061647.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Groundnut - Rust/img_00061883.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Groundnut - Rust/img_00061883.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Groundnut - Rust/img_00065040.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Groundnut - Rust/img_00065040.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Anthracnose/mendeley_guava_anthracnose_val_0008.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Anthracnose/mendeley_guava_anthracnose_val_0008.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Anthracnose/mendeley_guava_anthracnose_val_0009.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Anthracnose/mendeley_guava_anthracnose_val_0009.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Anthracnose/mendeley_guava_anthracnose_val_0013.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Anthracnose/mendeley_guava_anthracnose_val_0013.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Anthracnose/mendeley_guava_anthracnose_val_0014.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Anthracnose/mendeley_guava_anthracnose_val_0014.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Anthracnose/mendeley_guava_anthracnose_val_0015.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Anthracnose/mendeley_guava_anthracnose_val_0015.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Anthracnose/mendeley_guava_anthracnose_val_0020.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Anthracnose/mendeley_guava_anthracnose_val_0020.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Guava - Anthracnose/mendeley_guava_anthracnose_val_0041.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Anthracnose/mendeley_guava_anthracnose_val_0041.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Anthracnose/mendeley_guava_anthracnose_val_0042.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Anthracnose/mendeley_guava_anthracnose_val_0042.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Anthracnose/mendeley_guava_anthracnose_val_0045.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Anthracnose/mendeley_guava_anthracnose_val_0045.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Anthracnose/mendeley_guava_anthracnose_val_0047.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Anthracnose/mendeley_guava_anthracnose_val_0047.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Anthracnose/mendeley_guava_anthracnose_val_0064.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Anthracnose/mendeley_guava_anthracnose_val_0064.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Anthracnose/mendeley_guava_anthracnose_val_0069.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Anthracnose/mendeley_guava_anthracnose_val_0069.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Anthracnose/mendeley_guava_anthracnose_val_0079.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Anthracnose/mendeley_guava_anthracnose_val_0079.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Canker/mendeley_guava_canker_val_0007.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Canker/mendeley_guava_canker_val_0007.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Canker/mendeley_guava_canker_val_0012.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Canker/mendeley_guava_canker_val_0012.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Canker/mendeley_guava_canker_val_0014.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Canker/mendeley_guava_canker_val_0014.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Canker/mendeley_guava_canker_val_0016.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Canker/mendeley_guava_canker_val_0016.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Canker/mendeley_guava_canker_val_0017.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Canker/mendeley_guava_canker_val_0017.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Canker/mendeley_guava_canker_val_0019.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Canker/mendeley_guava_canker_val_0019.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Canker/mendeley_guava_canker_val_0020.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Canker/mendeley_guava_canker_val_0020.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Canker/mendeley_guava_canker_val_0023.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Canker/mendeley_guava_canker_val_0023.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Canker/mendeley_guava_canker_val_0024.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Canker/mendeley_guava_canker_val_0024.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Guava - Canker/mendeley_guava_canker_val_0032.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Canker/mendeley_guava_canker_val_0032.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Canker/mendeley_guava_canker_val_0046.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Canker/mendeley_guava_canker_val_0046.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Canker/mendeley_guava_canker_val_0054.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Canker/mendeley_guava_canker_val_0054.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Canker/mendeley_guava_canker_val_0073.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Canker/mendeley_guava_canker_val_0073.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Canker/mendeley_guava_canker_val_0083.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Canker/mendeley_guava_canker_val_0083.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Canker/mendeley_guava_canker_val_0085.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Canker/mendeley_guava_canker_val_0085.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Canker/mendeley_guava_canker_val_0086.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Canker/mendeley_guava_canker_val_0086.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Canker/mendeley_guava_canker_val_0088.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Canker/mendeley_guava_canker_val_0088.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Dot/mendeley_guava_dot_val_0006.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Dot/mendeley_guava_dot_val_0006.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Dot/mendeley_guava_dot_val_0008.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Dot/mendeley_guava_dot_val_0008.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Guava - Dot/mendeley_guava_dot_val_0009.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Dot/mendeley_guava_dot_val_0009.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Dot/mendeley_guava_dot_val_0014.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Dot/mendeley_guava_dot_val_0014.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Dot/mendeley_guava_dot_val_0015.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Dot/mendeley_guava_dot_val_0015.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Dot/mendeley_guava_dot_val_0019.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Dot/mendeley_guava_dot_val_0019.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Dot/mendeley_guava_dot_val_0024.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Dot/mendeley_guava_dot_val_0024.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Dot/mendeley_guava_dot_val_0027.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Dot/mendeley_guava_dot_val_0027.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Dot/mendeley_guava_dot_val_0028.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Dot/mendeley_guava_dot_val_0028.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Guava - Dot/mendeley_guava_dot_val_0031.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Dot/mendeley_guava_dot_val_0031.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Dot/mendeley_guava_dot_val_0032.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Dot/mendeley_guava_dot_val_0032.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Dot/mendeley_guava_dot_val_0033.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Dot/mendeley_guava_dot_val_0033.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Dot/mendeley_guava_dot_val_0035.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Dot/mendeley_guava_dot_val_0035.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Dot/mendeley_guava_dot_val_0039.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Dot/mendeley_guava_dot_val_0039.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Dot/mendeley_guava_dot_val_0040.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Dot/mendeley_guava_dot_val_0040.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Dot/mendeley_guava_dot_val_0041.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Dot/mendeley_guava_dot_val_0041.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Dot/mendeley_guava_dot_val_0043.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Dot/mendeley_guava_dot_val_0043.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Guava - Dot/mendeley_guava_dot_val_0044.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Dot/mendeley_guava_dot_val_0044.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Dot/mendeley_guava_dot_val_0046.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Dot/mendeley_guava_dot_val_0046.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Dot/mendeley_guava_dot_val_0052.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Dot/mendeley_guava_dot_val_0052.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Dot/mendeley_guava_dot_val_0061.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Dot/mendeley_guava_dot_val_0061.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Guava - Dot/mendeley_guava_dot_val_0067.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Dot/mendeley_guava_dot_val_0067.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Guava - Dot/mendeley_guava_dot_val_0068.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Dot/mendeley_guava_dot_val_0068.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Dot/mendeley_guava_dot_val_0072.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Dot/mendeley_guava_dot_val_0072.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Dot/mendeley_guava_dot_val_0073.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Dot/mendeley_guava_dot_val_0073.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Guava - Dot/mendeley_guava_dot_val_0074.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Dot/mendeley_guava_dot_val_0074.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Dot/mendeley_guava_dot_val_0079.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Dot/mendeley_guava_dot_val_0079.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Dot/mendeley_guava_dot_val_0080.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Dot/mendeley_guava_dot_val_0080.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Dot/mendeley_guava_dot_val_0083.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Dot/mendeley_guava_dot_val_0083.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Dot/mendeley_guava_dot_val_0085.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Dot/mendeley_guava_dot_val_0085.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Healthy/mendeley_guava_healthy_val_0001.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Healthy/mendeley_guava_healthy_val_0001.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Healthy/mendeley_guava_healthy_val_0002.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Healthy/mendeley_guava_healthy_val_0002.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Healthy/mendeley_guava_healthy_val_0004.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Healthy/mendeley_guava_healthy_val_0004.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Healthy/mendeley_guava_healthy_val_0006.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Healthy/mendeley_guava_healthy_val_0006.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Healthy/mendeley_guava_healthy_val_0007.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Healthy/mendeley_guava_healthy_val_0007.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Healthy/mendeley_guava_healthy_val_0008.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Healthy/mendeley_guava_healthy_val_0008.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Healthy/mendeley_guava_healthy_val_0009.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Healthy/mendeley_guava_healthy_val_0009.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Healthy/mendeley_guava_healthy_val_0012.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Healthy/mendeley_guava_healthy_val_0012.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Guava - Healthy/mendeley_guava_healthy_val_0019.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Healthy/mendeley_guava_healthy_val_0019.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Healthy/mendeley_guava_healthy_val_0020.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Healthy/mendeley_guava_healthy_val_0020.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Healthy/mendeley_guava_healthy_val_0022.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Healthy/mendeley_guava_healthy_val_0022.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Healthy/mendeley_guava_healthy_val_0024.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Healthy/mendeley_guava_healthy_val_0024.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Healthy/mendeley_guava_healthy_val_0033.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Healthy/mendeley_guava_healthy_val_0033.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Healthy/mendeley_guava_healthy_val_0042.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Healthy/mendeley_guava_healthy_val_0042.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Healthy/mendeley_guava_healthy_val_0046.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Healthy/mendeley_guava_healthy_val_0046.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Guava - Healthy/mendeley_guava_healthy_val_0054.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Healthy/mendeley_guava_healthy_val_0054.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Healthy/mendeley_guava_healthy_val_0055.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Healthy/mendeley_guava_healthy_val_0055.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Healthy/mendeley_guava_healthy_val_0056.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Healthy/mendeley_guava_healthy_val_0056.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Healthy/mendeley_guava_healthy_val_0059.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Healthy/mendeley_guava_healthy_val_0059.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Guava - Healthy/mendeley_guava_healthy_val_0061.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Healthy/mendeley_guava_healthy_val_0061.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Healthy/mendeley_guava_healthy_val_0062.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Healthy/mendeley_guava_healthy_val_0062.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Healthy/mendeley_guava_healthy_val_0068.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Healthy/mendeley_guava_healthy_val_0068.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Healthy/mendeley_guava_healthy_val_0071.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Healthy/mendeley_guava_healthy_val_0071.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Healthy/mendeley_guava_healthy_val_0075.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Healthy/mendeley_guava_healthy_val_0075.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Healthy/mendeley_guava_healthy_val_0076.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Healthy/mendeley_guava_healthy_val_0076.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Healthy/mendeley_guava_healthy_val_0077.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Healthy/mendeley_guava_healthy_val_0077.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Healthy/mendeley_guava_healthy_val_0079.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Healthy/mendeley_guava_healthy_val_0079.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Healthy/mendeley_guava_healthy_val_0083.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Healthy/mendeley_guava_healthy_val_0083.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Healthy/mendeley_guava_healthy_val_0084.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Healthy/mendeley_guava_healthy_val_0084.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Healthy/mendeley_guava_healthy_val_0085.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Healthy/mendeley_guava_healthy_val_0085.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Healthy/mendeley_guava_healthy_val_0087.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Healthy/mendeley_guava_healthy_val_0087.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Healthy/mendeley_guava_healthy_val_0088.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Healthy/mendeley_guava_healthy_val_0088.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Healthy/mendeley_guava_healthy_val_0092.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Healthy/mendeley_guava_healthy_val_0092.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Guava - Healthy/test_0_8319.jpeg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Healthy/test_0_8319.jpeg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Healthy/test_0_8522.jpeg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Healthy/test_0_8522.jpeg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Guava - Healthy/test_0_8551.jpeg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Healthy/test_0_8551.jpeg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Guava - Healthy/test_0_8762.jpeg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Healthy/test_0_8762.jpeg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Healthy/test_0_8805.jpeg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Healthy/test_0_8805.jpeg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Guava - Healthy/test_0_9041.jpeg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Healthy/test_0_9041.jpeg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Guava - Mummification/test_0_8283.jpeg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Mummification/test_0_8283.jpeg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Rust/mendeley_guava_rust_val_0002.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Rust/mendeley_guava_rust_val_0002.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Rust/mendeley_guava_rust_val_0007.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Rust/mendeley_guava_rust_val_0007.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Rust/mendeley_guava_rust_val_0009.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Rust/mendeley_guava_rust_val_0009.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Rust/mendeley_guava_rust_val_0013.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Rust/mendeley_guava_rust_val_0013.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Rust/mendeley_guava_rust_val_0016.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Rust/mendeley_guava_rust_val_0016.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Rust/mendeley_guava_rust_val_0017.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Rust/mendeley_guava_rust_val_0017.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Rust/mendeley_guava_rust_val_0019.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Rust/mendeley_guava_rust_val_0019.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Rust/mendeley_guava_rust_val_0020.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Rust/mendeley_guava_rust_val_0020.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Guava - Rust/mendeley_guava_rust_val_0021.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Rust/mendeley_guava_rust_val_0021.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Rust/mendeley_guava_rust_val_0022.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Rust/mendeley_guava_rust_val_0022.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Rust/mendeley_guava_rust_val_0025.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Rust/mendeley_guava_rust_val_0025.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Rust/mendeley_guava_rust_val_0026.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Rust/mendeley_guava_rust_val_0026.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Rust/mendeley_guava_rust_val_0027.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Rust/mendeley_guava_rust_val_0027.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Rust/mendeley_guava_rust_val_0028.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Rust/mendeley_guava_rust_val_0028.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Rust/mendeley_guava_rust_val_0030.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Rust/mendeley_guava_rust_val_0030.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Guava - Rust/mendeley_guava_rust_val_0034.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Rust/mendeley_guava_rust_val_0034.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Rust/mendeley_guava_rust_val_0036.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Rust/mendeley_guava_rust_val_0036.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Rust/mendeley_guava_rust_val_0038.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Rust/mendeley_guava_rust_val_0038.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Rust/mendeley_guava_rust_val_0043.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Rust/mendeley_guava_rust_val_0043.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Rust/mendeley_guava_rust_val_0049.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Rust/mendeley_guava_rust_val_0049.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Rust/mendeley_guava_rust_val_0051.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Rust/mendeley_guava_rust_val_0051.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Rust/mendeley_guava_rust_val_0056.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Rust/mendeley_guava_rust_val_0056.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Rust/mendeley_guava_rust_val_0058.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Rust/mendeley_guava_rust_val_0058.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Rust/mendeley_guava_rust_val_0061.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Rust/mendeley_guava_rust_val_0061.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Guava - Rust/mendeley_guava_rust_val_0062.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Rust/mendeley_guava_rust_val_0062.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Rust/mendeley_guava_rust_val_0063.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Rust/mendeley_guava_rust_val_0063.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Rust/mendeley_guava_rust_val_0065.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Rust/mendeley_guava_rust_val_0065.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Rust/mendeley_guava_rust_val_0066.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Rust/mendeley_guava_rust_val_0066.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Rust/mendeley_guava_rust_val_0072.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Rust/mendeley_guava_rust_val_0072.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Rust/mendeley_guava_rust_val_0075.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Rust/mendeley_guava_rust_val_0075.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Rust/mendeley_guava_rust_val_0077.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Rust/mendeley_guava_rust_val_0077.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Guava - Rust/mendeley_guava_rust_val_0078.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Rust/mendeley_guava_rust_val_0078.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Rust/mendeley_guava_rust_val_0085.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Rust/mendeley_guava_rust_val_0085.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Rust/mendeley_guava_rust_val_0087.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Rust/mendeley_guava_rust_val_0087.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Rust/mendeley_guava_rust_val_0089.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Rust/mendeley_guava_rust_val_0089.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Rust/mendeley_guava_rust_val_0090.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Rust/mendeley_guava_rust_val_0090.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Rust/mendeley_guava_rust_val_0093.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Rust/mendeley_guava_rust_val_0093.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Spiraling Whitefly/mendeley_guava_whitefly_val_0004.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Spiraling Whitefly/mendeley_guava_whitefly_val_0004.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Spiraling Whitefly/mendeley_guava_whitefly_val_0009.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Spiraling Whitefly/mendeley_guava_whitefly_val_0009.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Guava - Spiraling Whitefly/mendeley_guava_whitefly_val_0011.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Spiraling Whitefly/mendeley_guava_whitefly_val_0011.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Spiraling Whitefly/mendeley_guava_whitefly_val_0022.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Spiraling Whitefly/mendeley_guava_whitefly_val_0022.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Spiraling Whitefly/mendeley_guava_whitefly_val_0036.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Spiraling Whitefly/mendeley_guava_whitefly_val_0036.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Spiraling Whitefly/mendeley_guava_whitefly_val_0038.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Spiraling Whitefly/mendeley_guava_whitefly_val_0038.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Guava - Spiraling Whitefly/mendeley_guava_whitefly_val_0044.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Spiraling Whitefly/mendeley_guava_whitefly_val_0044.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Spiraling Whitefly/mendeley_guava_whitefly_val_0047.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Spiraling Whitefly/mendeley_guava_whitefly_val_0047.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Spiraling Whitefly/mendeley_guava_whitefly_val_0049.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Spiraling Whitefly/mendeley_guava_whitefly_val_0049.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Spiraling Whitefly/mendeley_guava_whitefly_val_0051.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Spiraling Whitefly/mendeley_guava_whitefly_val_0051.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Spiraling Whitefly/mendeley_guava_whitefly_val_0055.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Spiraling Whitefly/mendeley_guava_whitefly_val_0055.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Spiraling Whitefly/mendeley_guava_whitefly_val_0059.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Spiraling Whitefly/mendeley_guava_whitefly_val_0059.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Spiraling Whitefly/mendeley_guava_whitefly_val_0063.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Spiraling Whitefly/mendeley_guava_whitefly_val_0063.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Spiraling Whitefly/mendeley_guava_whitefly_val_0065.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Spiraling Whitefly/mendeley_guava_whitefly_val_0065.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Spiraling Whitefly/mendeley_guava_whitefly_val_0067.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Spiraling Whitefly/mendeley_guava_whitefly_val_0067.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Spiraling Whitefly/mendeley_guava_whitefly_val_0078.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Spiraling Whitefly/mendeley_guava_whitefly_val_0078.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Spiraling Whitefly/mendeley_guava_whitefly_val_0087.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Spiraling Whitefly/mendeley_guava_whitefly_val_0087.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Spiraling Whitefly/mendeley_guava_whitefly_val_0089.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Spiraling Whitefly/mendeley_guava_whitefly_val_0089.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Guava - Spiraling Whitefly/mendeley_guava_whitefly_val_0090.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Guava - Spiraling Whitefly/mendeley_guava_whitefly_val_0090.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Jamun - Healthy/jamun_healthy_val_0009.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Jamun - Healthy/jamun_healthy_val_0009.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Jamun - Powdery Mildew/jamun_powdery_mildew_val_0021.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Jamun - Powdery Mildew/jamun_powdery_mildew_val_0021.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Jamun - Powdery Mildew/jamun_powdery_mildew_val_0033.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Jamun - Powdery Mildew/jamun_powdery_mildew_val_0033.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Jamun - Sooty Mold/jamun_sooty_mold_val_0003.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Jamun - Sooty Mold/jamun_sooty_mold_val_0003.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Jamun - Sooty Mold/jamun_sooty_mold_val_0036.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Jamun - Sooty Mold/jamun_sooty_mold_val_0036.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Jamun - Sooty Mold/jamun_sooty_mold_val_0038.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Jamun - Sooty Mold/jamun_sooty_mold_val_0038.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Mango - Anthracnose/IMG_20211011_164901 (Custom).jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Mango - Anthracnose/IMG_20211011_164901 (Custom).jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Mango - Healthy/20211231_161613 (Custom).jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Mango - Healthy/20211231_161613 (Custom).jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Mango - Sooty Mould/IMG_20211212_144846 (Custom).jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Mango - Sooty Mould/IMG_20211212_144846 (Custom).jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Paddy - Blast/rice_lab_leaf_blast_val (20).jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Paddy - Blast/rice_lab_leaf_blast_val (20).jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Paddy - Blast/rice_lab_leaf_blast_val (3).jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Paddy - Blast/rice_lab_leaf_blast_val (3).jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Paddy - Brown Spot/rice_lab_brown_val (12).jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Paddy - Brown Spot/rice_lab_brown_val (12).jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Paddy - Healthy/rice_lab_healthy_val (21).jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Paddy - Healthy/rice_lab_healthy_val (21).jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Paddy - Leaf Scald/rice_lab_leaf_scald (78).jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Paddy - Leaf Scald/rice_lab_leaf_scald (78).jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Paddy - Leaf Scald/rice_lab_leaf_scald (8).jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Paddy - Leaf Scald/rice_lab_leaf_scald (8).jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Paddy - Leaf Scald/rice_lab_leaf_scald_val (12).jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Paddy - Leaf Scald/rice_lab_leaf_scald_val (12).jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Paddy - Leaf Scald/rice_lab_leaf_scald_val (13).jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Paddy - Leaf Scald/rice_lab_leaf_scald_val (13).jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Paddy - Narrow Brown Spot/rice_lab_narrow_brown_val (19).jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Paddy - Narrow Brown Spot/rice_lab_narrow_brown_val (19).jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Paddy - Narrow Brown Spot/rice_lab_narrow_brown_val (38).jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Paddy - Narrow Brown Spot/rice_lab_narrow_brown_val (38).jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Pear - Healthy/plantcity_pear_healthy_val_00011.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Pear - Healthy/plantcity_pear_healthy_val_00011.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Pear - Healthy/plantcity_pear_healthy_val_00025.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Pear - Healthy/plantcity_pear_healthy_val_00025.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Pear - pear black spot/plantcity_pear_pear_black_spot_val_00023.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Pear - pear black spot/plantcity_pear_pear_black_spot_val_00023.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Plum - plum insect hole/575_lab.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Plum - plum insect hole/575_lab.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Plum - plum insect hole/582_lab.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Plum - plum insect hole/582_lab.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Plum - plum insect hole/600_lab.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Plum - plum insect hole/600_lab.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Plum - plum weevil/plum_weevil_val_00005.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Plum - plum weevil/plum_weevil_val_00005.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Plum - plum yellow leaf/531_lab.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Plum - plum yellow leaf/531_lab.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Plum - plum yellow leaf/53_lab.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Plum - plum yellow leaf/53_lab.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Plum - plum yellow leaf/577_lab.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Plum - plum yellow leaf/577_lab.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Potato - Early Blight/img_00014182.JPG"
    dst_p = PROJECT_ROOT / "data/processed/val/Potato - Early Blight/img_00014182.JPG"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Potato - Healthy/healthy (497)_kaggle.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Potato - Healthy/healthy (497)_kaggle.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Radish - Black leaf spot/img_00049137.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Radish - Black leaf spot/img_00049137.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Radish - Black leaf spot/img_00049552.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Radish - Black leaf spot/img_00049552.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Radish - Black leaf spot/img_00049760.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Radish - Black leaf spot/img_00049760.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Radish - Black leaf spot/img_00051954.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Radish - Black leaf spot/img_00051954.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Radish - Black leaf spot/img_00055979.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Radish - Black leaf spot/img_00055979.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Radish - Black leaf spot/img_00057030.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Radish - Black leaf spot/img_00057030.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Radish - Black leaf spot/img_00057193.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Radish - Black leaf spot/img_00057193.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Radish - Black leaf spot/img_00058309.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Radish - Black leaf spot/img_00058309.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Radish - Black leaf spot/img_00058907.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Radish - Black leaf spot/img_00058907.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Radish - Black leaf spot/img_00060599.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Radish - Black leaf spot/img_00060599.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Radish - Black leaf spot/img_00062305.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Radish - Black leaf spot/img_00062305.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Radish - Black leaf spot/img_00062349.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Radish - Black leaf spot/img_00062349.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Radish - Black leaf spot/img_00062787.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Radish - Black leaf spot/img_00062787.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Radish - Black leaf spot/img_00066102.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Radish - Black leaf spot/img_00066102.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Radish - Downey mildew/img_00046184.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Radish - Downey mildew/img_00046184.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Radish - Downey mildew/img_00052691.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Radish - Downey mildew/img_00052691.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Radish - Downey mildew/img_00057757.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Radish - Downey mildew/img_00057757.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Radish - Downey mildew/img_00058400.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Radish - Downey mildew/img_00058400.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Radish - Flea beetle/img_00045750.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Radish - Flea beetle/img_00045750.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Radish - Flea beetle/img_00045847.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Radish - Flea beetle/img_00045847.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Radish - Flea beetle/img_00047306.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Radish - Flea beetle/img_00047306.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Radish - Flea beetle/img_00048806.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Radish - Flea beetle/img_00048806.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Radish - Flea beetle/img_00050009.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Radish - Flea beetle/img_00050009.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Radish - Flea beetle/img_00050428.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Radish - Flea beetle/img_00050428.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Radish - Flea beetle/img_00052096.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Radish - Flea beetle/img_00052096.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Radish - Flea beetle/img_00059045.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Radish - Flea beetle/img_00059045.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Radish - Flea beetle/img_00059570.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Radish - Flea beetle/img_00059570.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Radish - Flea beetle/img_00062942.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Radish - Flea beetle/img_00062942.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Radish - Flea beetle/img_00063117.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Radish - Flea beetle/img_00063117.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Radish - Flea beetle/img_00066634.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Radish - Flea beetle/img_00066634.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Radish - Flea beetle/img_00066753.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Radish - Flea beetle/img_00066753.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Radish - Healthy/img_00046302.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Radish - Healthy/img_00046302.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Radish - Healthy/img_00047500.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Radish - Healthy/img_00047500.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Radish - Healthy/img_00047502.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Radish - Healthy/img_00047502.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Radish - Healthy/img_00048588.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Radish - Healthy/img_00048588.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Radish - Healthy/img_00049245.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Radish - Healthy/img_00049245.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Radish - Healthy/img_00050011.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Radish - Healthy/img_00050011.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Radish - Healthy/img_00050930.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Radish - Healthy/img_00050930.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Radish - Healthy/img_00052770.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Radish - Healthy/img_00052770.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Radish - Healthy/img_00052916.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Radish - Healthy/img_00052916.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Radish - Healthy/img_00053124.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Radish - Healthy/img_00053124.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Radish - Healthy/img_00054383.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Radish - Healthy/img_00054383.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Radish - Healthy/img_00056874.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Radish - Healthy/img_00056874.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Radish - Healthy/img_00058646.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Radish - Healthy/img_00058646.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Radish - Healthy/img_00059015.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Radish - Healthy/img_00059015.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Radish - Healthy/img_00060178.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Radish - Healthy/img_00060178.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Radish - Healthy/img_00061841.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Radish - Healthy/img_00061841.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Radish - Healthy/img_00063439.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Radish - Healthy/img_00063439.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Radish - Healthy/img_00065842.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Radish - Healthy/img_00065842.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Radish - Healthy/img_00066465.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Radish - Healthy/img_00066465.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Radish - Mosaic/img_00046250.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Radish - Mosaic/img_00046250.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Radish - Mosaic/img_00057521.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Radish - Mosaic/img_00057521.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Radish - Mosaic/img_00060792.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Radish - Mosaic/img_00060792.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Radish - Mosaic/img_00061558.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Radish - Mosaic/img_00061558.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Soybean - Bacterial Blight/soybean_bacterial_blight_sivm_val_00008.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Soybean - Bacterial Blight/soybean_bacterial_blight_sivm_val_00008.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Soybean - Healthy/scraped_kaggle_pv2_093efd97-3116-49c2-aa77-861d86957da6___RS_HL 5611 1.JPG"
    dst_p = PROJECT_ROOT / "data/processed/val/Soybean - Healthy/scraped_kaggle_pv2_093efd97-3116-49c2-aa77-861d86957da6___RS_HL 5611 1.JPG"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Soybean - Healthy/scraped_kaggle_pv2_1988b49c-e5f9-4239-abc6-3e9f6cbd8edb___RS_HL 5449.JPG"
    dst_p = PROJECT_ROOT / "data/processed/val/Soybean - Healthy/scraped_kaggle_pv2_1988b49c-e5f9-4239-abc6-3e9f6cbd8edb___RS_HL 5449.JPG"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Soybean - Powdery Mildew/soybean_powdery_mildew_sivm_val_00007.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Soybean - Powdery Mildew/soybean_powdery_mildew_sivm_val_00007.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Soybean - Powdery Mildew/soybean_powdery_mildew_sivm_val_00009.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Soybean - Powdery Mildew/soybean_powdery_mildew_sivm_val_00009.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Tomato - Bacterial Spot/img_00017299.JPG"
    dst_p = PROJECT_ROOT / "data/processed/val/Tomato - Bacterial Spot/img_00017299.JPG"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Tomato - Spider Mites/img_00026055.JPG"
    dst_p = PROJECT_ROOT / "data/processed/val/Tomato - Spider Mites/img_00026055.JPG"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Tomato - Target Spot/img_00031119.JPG"
    dst_p = PROJECT_ROOT / "data/processed/val/Tomato - Target Spot/img_00031119.JPG"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_cross_split_dups/val/Tomato - tomato leaf mold/Tomato - Leaf Mold_img_00016091.JPG"
    dst_p = PROJECT_ROOT / "data/processed/val/Tomato - tomato leaf mold/Tomato - Leaf Mold_img_00016091.JPG"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_label_conflict/val/Zucchini - Healthy/agrivision_zucchini_healthy_IMG_20241101_172157(1)_e949baa4.jpg"
    dst_p = PROJECT_ROOT / "data/processed/val/Zucchini - Healthy/agrivision_zucchini_healthy_IMG_20241101_172157(1)_e949baa4.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    print(f"Restored {restored} images.")

if __name__ == "__main__":
    restore()