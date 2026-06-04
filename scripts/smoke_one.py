from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "shared"))

from agentix_framework_demos.runtime import run_demo


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("framework_id")
    parser.add_argument("--input", dest="user_input")
    parser.add_argument("--model")
    args = parser.parse_args()
    print(json.dumps(run_demo(args.framework_id, args.user_input, args.model), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
