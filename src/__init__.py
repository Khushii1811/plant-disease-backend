"""src — Top-level package namespace for plant-disease-backend source modules."""

import sys
from pathlib import Path

# Ensure the project root (parent of this src/ directory) is on sys.path so
# that `import config` works from any src.* module regardless of how it is
# invoked (e.g. `python -m src.models.train_convnext` or imported by
# serving/inference.py which already injects the root itself).
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))
