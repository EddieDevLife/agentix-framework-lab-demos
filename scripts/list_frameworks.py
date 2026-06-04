from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "shared"))

from agentix_framework_demos import list_frameworks


if __name__ == "__main__":
    print(json.dumps(list_frameworks(), indent=2, ensure_ascii=False))
