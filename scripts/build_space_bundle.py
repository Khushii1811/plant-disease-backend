"""
Build clean Hugging Face Space deployment bundle.
Copies ONLY runtime files into deploy/space/ without git history.
"""

import os
import shutil
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BACKEND_DIR.parent / "plant-disease-frontend"
DEPLOY_DIR = BACKEND_DIR / "deploy" / "space"


def copy_file(src: Path, dst: Path):
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def copy_tree_filtered(src_dir: Path, dst_dir: Path, ignore_patterns=None):
    if ignore_patterns is None:
        ignore_patterns = shutil.ignore_patterns(
            "__pycache__", "*.pyc", "*.pyo", ".pytest_cache", ".git"
        )
    shutil.copytree(src_dir, dst_dir, ignore=ignore_patterns, dirs_exist_ok=True)


def format_size(bytes_val: int) -> str:
    if bytes_val >= 1024 * 1024:
        return f"{bytes_val / (1024 * 1024):.2f} MB"
    if bytes_val >= 1024:
        return f"{bytes_val / 1024:.2f} KB"
    return f"{bytes_val} B"


def main():
    print(f"Building Hugging Face Space bundle in: {DEPLOY_DIR}")

    if DEPLOY_DIR.exists():
        print(f"Cleaning previous bundle directory: {DEPLOY_DIR}")
        shutil.rmtree(DEPLOY_DIR)

    DEPLOY_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Root configuration & Docker files
    copy_file(BACKEND_DIR / "Dockerfile", DEPLOY_DIR / "Dockerfile")
    copy_file(BACKEND_DIR / "requirements.txt", DEPLOY_DIR / "requirements.txt")
    copy_file(BACKEND_DIR / "config.py", DEPLOY_DIR / "config.py")
    copy_file(BACKEND_DIR / "LICENSE", DEPLOY_DIR / "LICENSE")

    # Write .gitignore for Space repository to prevent bytecode caching
    (DEPLOY_DIR / ".gitignore").write_text("__pycache__/\n*.py[cod]\n*$py.class\n.pytest_cache/\n", encoding="utf-8")

    # 2. Hugging Face Space README.md with YAML header
    readme_src = BACKEND_DIR / "hf_space" / "README.md"
    if not readme_src.exists():
        raise FileNotFoundError(f"Missing HF Space README at {readme_src}")
    copy_file(readme_src, DEPLOY_DIR / "README.md")

    # 3. Serving modules
    copy_tree_filtered(BACKEND_DIR / "serving", DEPLOY_DIR / "serving")

    # 4. Runtime src modules
    copy_file(BACKEND_DIR / "src" / "__init__.py", DEPLOY_DIR / "src" / "__init__.py")
    copy_tree_filtered(BACKEND_DIR / "src" / "models", DEPLOY_DIR / "src" / "models")
    copy_tree_filtered(BACKEND_DIR / "src" / "data", DEPLOY_DIR / "src" / "data")

    # 5. Production model bundle (models/v1/)
    copy_tree_filtered(BACKEND_DIR / "models" / "v1", DEPLOY_DIR / "models" / "v1")

    # 6. Frontend static files into deploy/space/static/
    static_dst = DEPLOY_DIR / "static"
    static_dst.mkdir(parents=True, exist_ok=True)

    frontend_files = [
        "index.html",
        "wiki.html",
        "credits.html",
        "app.js",
        "style.css",
        "cropper.min.css",
        "cropper.min.js",
        "html2canvas.min.js",
        "jspdf.umd.min.js",
        "treatments.json",
        "wiki_data.json",
        "hero-bg.jpg",
        "favicon.ico",
    ]
    for fname in frontend_files:
        src_path = FRONTEND_DIR / fname
        if src_path.exists():
            copy_file(src_path, static_dst / fname)
        else:
            print(f"[WARNING] Frontend file missing: {src_path}")

    assets_src = FRONTEND_DIR / "assets"
    if assets_src.exists():
        copy_tree_filtered(assets_src, static_dst / "assets")

    # 7. Audit all bundle files
    print("\n" + "=" * 80)
    print("DEPLOYMENT BUNDLE AUDIT")
    print("=" * 80)

    total_bytes = 0
    file_count = 0
    large_files = []

    all_files = sorted(DEPLOY_DIR.rglob("*"))

    print(f"{'Relative Path':<55} | {'Size':>12}")
    print("-" * 70)

    for p in all_files:
        if p.is_file():
            file_count += 1
            sz = p.stat().st_size
            total_bytes += sz
            rel_p = p.relative_to(DEPLOY_DIR).as_posix()
            if sz > 10 * 1024 * 1024:
                large_files.append((rel_p, sz))
                print(f"{rel_p:<55} | {format_size(sz):>12}  [LFS REQUIRED]")
            elif not rel_p.startswith("static/assets/wiki_samples/"):
                print(f"{rel_p:<55} | {format_size(sz):>12}")

    wiki_samples_dir = static_dst / "assets" / "wiki_samples"
    if wiki_samples_dir.exists():
        wiki_files = list(wiki_samples_dir.glob("*"))
        wiki_size = sum(f.stat().st_size for f in wiki_files if f.is_file())
        print(
            f"{'static/assets/wiki_samples/* (' + str(len(wiki_files)) + ' files)':<55} | {format_size(wiki_size):>12}"
        )

    print("-" * 70)
    print(f"Total Files: {file_count}")
    print(f"Total Bundle Size: {format_size(total_bytes)} ({total_bytes:,} bytes)")
    print("=" * 80)

    if large_files:
        print("\n[NOTE] Files > 10 MB requiring Git LFS on Hugging Face Spaces:")
        for lf, sz in large_files:
            print(f"  - {lf}: {format_size(sz)}")

    print(f"\nClean bundle successfully created at: {DEPLOY_DIR}")


if __name__ == "__main__":
    main()
