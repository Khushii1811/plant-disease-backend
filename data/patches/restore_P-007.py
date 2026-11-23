"""Restore script for Patch P-007."""
import shutil
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

def restore():
    restored = 0
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Ginger - Bacterial Wilt/ginger_bacterial_wilt_train_00078.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Ginger - Bacterial Wilt/ginger_bacterial_wilt_train_00078.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Ginger - Bacterial Wilt/ginger_bacterial_wilt_train_00084.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Ginger - Bacterial Wilt/ginger_bacterial_wilt_train_00084.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Ginger - Bacterial Wilt/ginger_bacterial_wilt_train_00123.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Ginger - Bacterial Wilt/ginger_bacterial_wilt_train_00123.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Grape - Esca (Black Measles)/grape_esca_train_00491.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Grape - Esca (Black Measles)/grape_esca_train_00491.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Guava - Insect Damage/mendeley_guava_anthracnose_train_0067.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Insect Damage/mendeley_guava_anthracnose_train_0067.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Guava - Insect Damage/mendeley_guava_anthracnose_train_0071.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Insect Damage/mendeley_guava_anthracnose_train_0071.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Guava - Insect Damage/mendeley_guava_anthracnose_train_0080.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Insect Damage/mendeley_guava_anthracnose_train_0080.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Guava - Insect Damage/mendeley_guava_anthracnose_train_0087.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Insect Damage/mendeley_guava_anthracnose_train_0087.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Guava - Insect Damage/mendeley_guava_anthracnose_train_0105.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Insect Damage/mendeley_guava_anthracnose_train_0105.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Guava - Insect Damage/mendeley_guava_anthracnose_train_0233.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Insect Damage/mendeley_guava_anthracnose_train_0233.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Guava - Insect Damage/mendeley_guava_anthracnose_train_0265.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Insect Damage/mendeley_guava_anthracnose_train_0265.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Guava - Insect Damage/mendeley_guava_anthracnose_train_0271.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Insect Damage/mendeley_guava_anthracnose_train_0271.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Guava - Insect Damage/mendeley_guava_anthracnose_train_0305.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Insect Damage/mendeley_guava_anthracnose_train_0305.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Guava - Insect Damage/mendeley_guava_anthracnose_train_0312.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Insect Damage/mendeley_guava_anthracnose_train_0312.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Guava - Insect Damage/mendeley_guava_anthracnose_train_0366.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Insect Damage/mendeley_guava_anthracnose_train_0366.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Guava - Insect Damage/mendeley_guava_anthracnose_train_0385.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Insect Damage/mendeley_guava_anthracnose_train_0385.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Guava - Insect Damage/mendeley_guava_anthracnose_train_0387.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Insect Damage/mendeley_guava_anthracnose_train_0387.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Guava - Insect Damage/mendeley_guava_anthracnose_train_0438.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Insect Damage/mendeley_guava_anthracnose_train_0438.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Guava - Insect Damage/mendeley_guava_anthracnose_train_0478.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Insect Damage/mendeley_guava_anthracnose_train_0478.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Guava - Insect Damage/mendeley_guava_anthracnose_train_0481.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Insect Damage/mendeley_guava_anthracnose_train_0481.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Guava - Insect Damage/mendeley_guava_anthracnose_train_0491.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Insect Damage/mendeley_guava_anthracnose_train_0491.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Guava - Insect Damage/mendeley_guava_anthracnose_train_0498.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Insect Damage/mendeley_guava_anthracnose_train_0498.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Guava - Insect Damage/mendeley_guava_anthracnose_train_0573.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Insect Damage/mendeley_guava_anthracnose_train_0573.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Guava - Insect Damage/mendeley_guava_anthracnose_train_0574.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Insect Damage/mendeley_guava_anthracnose_train_0574.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Guava - Insect Damage/mendeley_guava_anthracnose_train_0577.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Insect Damage/mendeley_guava_anthracnose_train_0577.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Guava - Insect Damage/mendeley_guava_anthracnose_train_0578.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Insect Damage/mendeley_guava_anthracnose_train_0578.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Guava - Insect Damage/mendeley_guava_anthracnose_train_0579.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Insect Damage/mendeley_guava_anthracnose_train_0579.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Guava - Insect Damage/mendeley_guava_anthracnose_train_0630.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Insect Damage/mendeley_guava_anthracnose_train_0630.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Guava - Spiraling Whitefly/mendeley_guava_whitefly_test_0077.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Guava - Spiraling Whitefly/mendeley_guava_whitefly_test_0077.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Jamun - Bacterial Spot/jamun_bacterial_spot_train_0022.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Bacterial Spot/jamun_bacterial_spot_train_0022.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Jamun - Bacterial Spot/jamun_bacterial_spot_train_0023.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Bacterial Spot/jamun_bacterial_spot_train_0023.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Jamun - Bacterial Spot/jamun_bacterial_spot_train_0051.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Bacterial Spot/jamun_bacterial_spot_train_0051.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Jamun - Bacterial Spot/jamun_bacterial_spot_train_0053.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Bacterial Spot/jamun_bacterial_spot_train_0053.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Jamun - Bacterial Spot/jamun_bacterial_spot_train_0057.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Bacterial Spot/jamun_bacterial_spot_train_0057.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Jamun - Bacterial Spot/jamun_bacterial_spot_train_0061.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Bacterial Spot/jamun_bacterial_spot_train_0061.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Jamun - Bacterial Spot/jamun_bacterial_spot_train_0074.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Bacterial Spot/jamun_bacterial_spot_train_0074.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Jamun - Bacterial Spot/jamun_bacterial_spot_train_0090.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Bacterial Spot/jamun_bacterial_spot_train_0090.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Jamun - Bacterial Spot/jamun_bacterial_spot_train_0103.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Bacterial Spot/jamun_bacterial_spot_train_0103.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Jamun - Bacterial Spot/jamun_bacterial_spot_train_0106.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Bacterial Spot/jamun_bacterial_spot_train_0106.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Jamun - Bacterial Spot/jamun_bacterial_spot_train_0110.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Bacterial Spot/jamun_bacterial_spot_train_0110.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Jamun - Bacterial Spot/jamun_bacterial_spot_train_0125.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Bacterial Spot/jamun_bacterial_spot_train_0125.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Jamun - Bacterial Spot/jamun_bacterial_spot_train_0134.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Bacterial Spot/jamun_bacterial_spot_train_0134.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Jamun - Bacterial Spot/jamun_bacterial_spot_train_0154.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Bacterial Spot/jamun_bacterial_spot_train_0154.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Jamun - Bacterial Spot/jamun_bacterial_spot_train_0156.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Bacterial Spot/jamun_bacterial_spot_train_0156.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Jamun - Bacterial Spot/jamun_bacterial_spot_train_0165.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Bacterial Spot/jamun_bacterial_spot_train_0165.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Jamun - Bacterial Spot/jamun_bacterial_spot_train_0174.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Bacterial Spot/jamun_bacterial_spot_train_0174.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Jamun - Bacterial Spot/jamun_bacterial_spot_train_0179.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Bacterial Spot/jamun_bacterial_spot_train_0179.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Jamun - Bacterial Spot/jamun_bacterial_spot_train_0193.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Bacterial Spot/jamun_bacterial_spot_train_0193.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Jamun - Bacterial Spot/jamun_bacterial_spot_train_0194.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Bacterial Spot/jamun_bacterial_spot_train_0194.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Jamun - Bacterial Spot/jamun_bacterial_spot_train_0195.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Bacterial Spot/jamun_bacterial_spot_train_0195.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Jamun - Bacterial Spot/jamun_bacterial_spot_train_0197.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Bacterial Spot/jamun_bacterial_spot_train_0197.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Jamun - Bacterial Spot/jamun_bacterial_spot_train_0221.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Bacterial Spot/jamun_bacterial_spot_train_0221.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Jamun - Bacterial Spot/jamun_bacterial_spot_train_0242.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Bacterial Spot/jamun_bacterial_spot_train_0242.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Jamun - Bacterial Spot/jamun_bacterial_spot_train_0259.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Bacterial Spot/jamun_bacterial_spot_train_0259.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Jamun - Bacterial Spot/jamun_bacterial_spot_train_0264.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Bacterial Spot/jamun_bacterial_spot_train_0264.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Jamun - Bacterial Spot/jamun_bacterial_spot_train_0277.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Bacterial Spot/jamun_bacterial_spot_train_0277.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Jamun - Bacterial Spot/jamun_bacterial_spot_train_0283.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Bacterial Spot/jamun_bacterial_spot_train_0283.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Jamun - Bacterial Spot/jamun_bacterial_spot_train_0300.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Bacterial Spot/jamun_bacterial_spot_train_0300.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Jamun - Bacterial Spot/jamun_bacterial_spot_train_0320.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Bacterial Spot/jamun_bacterial_spot_train_0320.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Jamun - Brown Blight/jamun_brown_blight_train_0021.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Brown Blight/jamun_brown_blight_train_0021.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Jamun - Brown Blight/jamun_brown_blight_train_0049.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Brown Blight/jamun_brown_blight_train_0049.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Jamun - Brown Blight/jamun_brown_blight_train_0051.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Brown Blight/jamun_brown_blight_train_0051.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Jamun - Brown Blight/jamun_brown_blight_train_0056.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Brown Blight/jamun_brown_blight_train_0056.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Jamun - Brown Blight/jamun_brown_blight_train_0060.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Brown Blight/jamun_brown_blight_train_0060.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Jamun - Brown Blight/jamun_brown_blight_train_0089.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Brown Blight/jamun_brown_blight_train_0089.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Jamun - Brown Blight/jamun_brown_blight_train_0101.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Brown Blight/jamun_brown_blight_train_0101.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Jamun - Brown Blight/jamun_brown_blight_train_0108.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Brown Blight/jamun_brown_blight_train_0108.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Jamun - Brown Blight/jamun_brown_blight_train_0132.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Brown Blight/jamun_brown_blight_train_0132.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Jamun - Brown Blight/jamun_brown_blight_train_0152.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Brown Blight/jamun_brown_blight_train_0152.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Jamun - Brown Blight/jamun_brown_blight_train_0155.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Brown Blight/jamun_brown_blight_train_0155.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Jamun - Brown Blight/jamun_brown_blight_train_0164.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Brown Blight/jamun_brown_blight_train_0164.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Jamun - Brown Blight/jamun_brown_blight_train_0173.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Brown Blight/jamun_brown_blight_train_0173.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Jamun - Brown Blight/jamun_brown_blight_train_0178.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Brown Blight/jamun_brown_blight_train_0178.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Jamun - Brown Blight/jamun_brown_blight_train_0191.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Brown Blight/jamun_brown_blight_train_0191.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Jamun - Brown Blight/jamun_brown_blight_train_0192.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Brown Blight/jamun_brown_blight_train_0192.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Jamun - Brown Blight/jamun_brown_blight_train_0193.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Brown Blight/jamun_brown_blight_train_0193.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Jamun - Brown Blight/jamun_brown_blight_train_0195.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Brown Blight/jamun_brown_blight_train_0195.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Jamun - Brown Blight/jamun_brown_blight_train_0218.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Brown Blight/jamun_brown_blight_train_0218.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Jamun - Brown Blight/jamun_brown_blight_train_0239.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Brown Blight/jamun_brown_blight_train_0239.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Jamun - Brown Blight/jamun_brown_blight_train_0247.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Brown Blight/jamun_brown_blight_train_0247.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Jamun - Brown Blight/jamun_brown_blight_train_0256.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Brown Blight/jamun_brown_blight_train_0256.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Jamun - Brown Blight/jamun_brown_blight_train_0261.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Brown Blight/jamun_brown_blight_train_0261.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Jamun - Brown Blight/jamun_brown_blight_train_0275.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Brown Blight/jamun_brown_blight_train_0275.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Jamun - Brown Blight/jamun_brown_blight_train_0281.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Brown Blight/jamun_brown_blight_train_0281.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Jamun - Brown Blight/jamun_brown_blight_train_0298.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Brown Blight/jamun_brown_blight_train_0298.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Jamun - Brown Blight/jamun_brown_blight_train_0319.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Brown Blight/jamun_brown_blight_train_0319.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Jamun - Brown Blight/jamun_brown_blight_train_0320.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Brown Blight/jamun_brown_blight_train_0320.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Jamun - Healthy/jamun_healthy_train_0002.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Healthy/jamun_healthy_train_0002.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Jamun - Healthy/jamun_healthy_train_0015.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Healthy/jamun_healthy_train_0015.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Jamun - Healthy/jamun_healthy_train_0021.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Healthy/jamun_healthy_train_0021.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Jamun - Healthy/jamun_healthy_train_0053.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Healthy/jamun_healthy_train_0053.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Jamun - Healthy/jamun_healthy_train_0072.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Healthy/jamun_healthy_train_0072.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Jamun - Healthy/jamun_healthy_train_0093.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Healthy/jamun_healthy_train_0093.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Jamun - Healthy/jamun_healthy_train_0100.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Healthy/jamun_healthy_train_0100.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Jamun - Healthy/jamun_healthy_train_0103.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Healthy/jamun_healthy_train_0103.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Jamun - Healthy/jamun_healthy_train_0104.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Healthy/jamun_healthy_train_0104.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Jamun - Healthy/jamun_healthy_train_0107.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Healthy/jamun_healthy_train_0107.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Jamun - Healthy/jamun_healthy_train_0117.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Healthy/jamun_healthy_train_0117.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Jamun - Healthy/jamun_healthy_train_0122.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Healthy/jamun_healthy_train_0122.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Jamun - Healthy/jamun_healthy_train_0131.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Healthy/jamun_healthy_train_0131.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Jamun - Healthy/jamun_healthy_train_0152.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Healthy/jamun_healthy_train_0152.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Jamun - Healthy/jamun_healthy_train_0203.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Healthy/jamun_healthy_train_0203.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Jamun - Healthy/jamun_healthy_train_0208.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Healthy/jamun_healthy_train_0208.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Jamun - Powdery Mildew/jamun_powdery_mildew_train_0017.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Powdery Mildew/jamun_powdery_mildew_train_0017.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Jamun - Powdery Mildew/jamun_powdery_mildew_train_0045.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Powdery Mildew/jamun_powdery_mildew_train_0045.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Jamun - Powdery Mildew/jamun_powdery_mildew_train_0047.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Powdery Mildew/jamun_powdery_mildew_train_0047.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Jamun - Powdery Mildew/jamun_powdery_mildew_train_0051.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Powdery Mildew/jamun_powdery_mildew_train_0051.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Jamun - Powdery Mildew/jamun_powdery_mildew_train_0068.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Powdery Mildew/jamun_powdery_mildew_train_0068.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Jamun - Powdery Mildew/jamun_powdery_mildew_train_0084.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Powdery Mildew/jamun_powdery_mildew_train_0084.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Jamun - Powdery Mildew/jamun_powdery_mildew_train_0097.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Powdery Mildew/jamun_powdery_mildew_train_0097.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Jamun - Powdery Mildew/jamun_powdery_mildew_train_0100.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Powdery Mildew/jamun_powdery_mildew_train_0100.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Jamun - Powdery Mildew/jamun_powdery_mildew_train_0119.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Powdery Mildew/jamun_powdery_mildew_train_0119.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Jamun - Powdery Mildew/jamun_powdery_mildew_train_0150.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Powdery Mildew/jamun_powdery_mildew_train_0150.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Jamun - Powdery Mildew/jamun_powdery_mildew_train_0168.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Powdery Mildew/jamun_powdery_mildew_train_0168.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Jamun - Powdery Mildew/jamun_powdery_mildew_train_0187.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Powdery Mildew/jamun_powdery_mildew_train_0187.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Jamun - Powdery Mildew/jamun_powdery_mildew_train_0188.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Powdery Mildew/jamun_powdery_mildew_train_0188.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Jamun - Powdery Mildew/jamun_powdery_mildew_train_0217.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Powdery Mildew/jamun_powdery_mildew_train_0217.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Jamun - Powdery Mildew/jamun_powdery_mildew_train_0238.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Powdery Mildew/jamun_powdery_mildew_train_0238.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Jamun - Powdery Mildew/jamun_powdery_mildew_train_0246.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Powdery Mildew/jamun_powdery_mildew_train_0246.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Jamun - Powdery Mildew/jamun_powdery_mildew_train_0256.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Powdery Mildew/jamun_powdery_mildew_train_0256.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Jamun - Powdery Mildew/jamun_powdery_mildew_train_0262.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Powdery Mildew/jamun_powdery_mildew_train_0262.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Jamun - Powdery Mildew/jamun_powdery_mildew_train_0275.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Powdery Mildew/jamun_powdery_mildew_train_0275.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Jamun - Powdery Mildew/jamun_powdery_mildew_train_0282.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Powdery Mildew/jamun_powdery_mildew_train_0282.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Jamun - Powdery Mildew/jamun_powdery_mildew_train_0300.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Powdery Mildew/jamun_powdery_mildew_train_0300.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Jamun - Sooty Mold/jamun_sooty_mold_train_0010.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Sooty Mold/jamun_sooty_mold_train_0010.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Jamun - Sooty Mold/jamun_sooty_mold_train_0039.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Sooty Mold/jamun_sooty_mold_train_0039.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Jamun - Sooty Mold/jamun_sooty_mold_train_0041.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Sooty Mold/jamun_sooty_mold_train_0041.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Jamun - Sooty Mold/jamun_sooty_mold_train_0045.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Sooty Mold/jamun_sooty_mold_train_0045.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Jamun - Sooty Mold/jamun_sooty_mold_train_0090.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Sooty Mold/jamun_sooty_mold_train_0090.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Jamun - Sooty Mold/jamun_sooty_mold_train_0112.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Sooty Mold/jamun_sooty_mold_train_0112.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Jamun - Sooty Mold/jamun_sooty_mold_train_0140.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Sooty Mold/jamun_sooty_mold_train_0140.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Jamun - Sooty Mold/jamun_sooty_mold_train_0142.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Sooty Mold/jamun_sooty_mold_train_0142.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Jamun - Sooty Mold/jamun_sooty_mold_train_0179.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Sooty Mold/jamun_sooty_mold_train_0179.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Jamun - Sooty Mold/jamun_sooty_mold_train_0180.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Sooty Mold/jamun_sooty_mold_train_0180.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Jamun - Sooty Mold/jamun_sooty_mold_train_0181.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Sooty Mold/jamun_sooty_mold_train_0181.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Jamun - Sooty Mold/jamun_sooty_mold_train_0183.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Sooty Mold/jamun_sooty_mold_train_0183.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Jamun - Sooty Mold/jamun_sooty_mold_train_0227.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Sooty Mold/jamun_sooty_mold_train_0227.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Jamun - Sooty Mold/jamun_sooty_mold_train_0236.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Sooty Mold/jamun_sooty_mold_train_0236.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Jamun - Sooty Mold/jamun_sooty_mold_train_0245.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Sooty Mold/jamun_sooty_mold_train_0245.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Jamun - Sooty Mold/jamun_sooty_mold_train_0250.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Sooty Mold/jamun_sooty_mold_train_0250.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Jamun - Sooty Mold/jamun_sooty_mold_train_0263.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Sooty Mold/jamun_sooty_mold_train_0263.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Jamun - Sooty Mold/jamun_sooty_mold_train_0269.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Sooty Mold/jamun_sooty_mold_train_0269.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Jamun - Sooty Mold/jamun_sooty_mold_train_0286.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Sooty Mold/jamun_sooty_mold_train_0286.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Jamun - Sooty Mold/jamun_sooty_mold_train_0306.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Jamun - Sooty Mold/jamun_sooty_mold_train_0306.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Paddy - Blast/rice_lab_leaf_blast (148).jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Paddy - Blast/rice_lab_leaf_blast (148).jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Paddy - Blast/rice_lab_leaf_blast (150).jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Paddy - Blast/rice_lab_leaf_blast (150).jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Paddy - Blast/rice_lab_leaf_blast (159).jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Paddy - Blast/rice_lab_leaf_blast (159).jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Paddy - Blast/rice_lab_leaf_blast (199).jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Paddy - Blast/rice_lab_leaf_blast (199).jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Paddy - Blast/rice_lab_leaf_blast (218).jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Paddy - Blast/rice_lab_leaf_blast (218).jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Paddy - Blast/rice_lab_leaf_blast (308).jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Paddy - Blast/rice_lab_leaf_blast (308).jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Paddy - Blast/rice_lab_leaf_blast (342).jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Paddy - Blast/rice_lab_leaf_blast (342).jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Paddy - Brown Spot/rice_lab_brown_spot (248).jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Paddy - Brown Spot/rice_lab_brown_spot (248).jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Paddy - Brown Spot/rice_lab_brown_spot (264).jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Paddy - Brown Spot/rice_lab_brown_spot (264).jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Paddy - Brown Spot/rice_lab_brown_spot (305).jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Paddy - Brown Spot/rice_lab_brown_spot (305).jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Paddy - Brown Spot/rice_lab_brown_spot (331).jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Paddy - Brown Spot/rice_lab_brown_spot (331).jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Paddy - Leaf Scald/rice_lab_leaf_scald (12).jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Paddy - Leaf Scald/rice_lab_leaf_scald (12).jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Paddy - Leaf Scald/rice_lab_leaf_scald (148).jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Paddy - Leaf Scald/rice_lab_leaf_scald (148).jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Paddy - Leaf Scald/rice_lab_leaf_scald (158).jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Paddy - Leaf Scald/rice_lab_leaf_scald (158).jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Paddy - Leaf Scald/rice_lab_leaf_scald (170).jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Paddy - Leaf Scald/rice_lab_leaf_scald (170).jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Paddy - Leaf Scald/rice_lab_leaf_scald (205).jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Paddy - Leaf Scald/rice_lab_leaf_scald (205).jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Paddy - Leaf Scald/rice_lab_leaf_scald (235).jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Paddy - Leaf Scald/rice_lab_leaf_scald (235).jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Paddy - Leaf Scald/rice_lab_leaf_scald (254).jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Paddy - Leaf Scald/rice_lab_leaf_scald (254).jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Paddy - Leaf Scald/rice_lab_leaf_scald (281).jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Paddy - Leaf Scald/rice_lab_leaf_scald (281).jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Paddy - Leaf Scald/rice_lab_leaf_scald (344).jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Paddy - Leaf Scald/rice_lab_leaf_scald (344).jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Paddy - Leaf Scald/rice_lab_leaf_scald (49).jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Paddy - Leaf Scald/rice_lab_leaf_scald (49).jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Paddy - Leaf Scald/rice_lab_leaf_scald (7).jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Paddy - Leaf Scald/rice_lab_leaf_scald (7).jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Paddy - Narrow Brown Spot/rice_lab_narrow_brown (159).jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Paddy - Narrow Brown Spot/rice_lab_narrow_brown (159).jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Paddy - Narrow Brown Spot/rice_lab_narrow_brown (186).jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Paddy - Narrow Brown Spot/rice_lab_narrow_brown (186).jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Paddy - Narrow Brown Spot/rice_lab_narrow_brown (216).jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Paddy - Narrow Brown Spot/rice_lab_narrow_brown (216).jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Paddy - Narrow Brown Spot/rice_lab_narrow_brown (262).jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Paddy - Narrow Brown Spot/rice_lab_narrow_brown (262).jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Paddy - Narrow Brown Spot/rice_lab_narrow_brown (286).jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Paddy - Narrow Brown Spot/rice_lab_narrow_brown (286).jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Paddy - Narrow Brown Spot/rice_lab_narrow_brown (308).jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Paddy - Narrow Brown Spot/rice_lab_narrow_brown (308).jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Paddy - Narrow Brown Spot/rice_lab_narrow_brown (328).jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Paddy - Narrow Brown Spot/rice_lab_narrow_brown (328).jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Paddy - Narrow Brown Spot/rice_lab_narrow_brown (348).jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Paddy - Narrow Brown Spot/rice_lab_narrow_brown (348).jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Paddy - Narrow Brown Spot/rice_lab_narrow_brown (37).jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Paddy - Narrow Brown Spot/rice_lab_narrow_brown (37).jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Paddy - Narrow Brown Spot/rice_lab_narrow_brown (54).jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Paddy - Narrow Brown Spot/rice_lab_narrow_brown (54).jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Soybean - Powdery Mildew/soybean_powdery_mildew_sivm_train_00012.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Soybean - Powdery Mildew/soybean_powdery_mildew_sivm_train_00012.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Soybean - Powdery Mildew/soybean_powdery_mildew_sivm_train_00044.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Soybean - Powdery Mildew/soybean_powdery_mildew_sivm_train_00044.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Soybean - Powdery Mildew/soybean_powdery_mildew_sivm_train_00068.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Soybean - Powdery Mildew/soybean_powdery_mildew_sivm_train_00068.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Soybean - Powdery Mildew/soybean_powdery_mildew_sivm_train_00076.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Soybean - Powdery Mildew/soybean_powdery_mildew_sivm_train_00076.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    q_p = PROJECT_ROOT / "data/raw/quarantine_test_leakage_twins/test/Soybean - Powdery Mildew/soybean_powdery_mildew_sivm_train_00096.jpg"
    dst_p = PROJECT_ROOT / "data/processed/test/Soybean - Powdery Mildew/soybean_powdery_mildew_sivm_train_00096.jpg"
    if q_p.exists():
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(q_p), str(dst_p))
        restored += 1
    print(f"Restored {restored} images.")

if __name__ == "__main__":
    restore()
