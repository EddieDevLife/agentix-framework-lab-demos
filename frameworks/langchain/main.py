from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "shared"))

from agentix_framework_demos.runtime import print_result, run_demo


if __name__ == "__main__":
    print_result(run_demo("langchain"))
