from __future__ import annotations

import argparse
import json
import os
import sys

from .env import load_env_local
from .extractor import extract_reservation


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Extract reservation info via Gemini URL context")
    parser.add_argument("--url", required=True, help="対象URL")
    parser.add_argument("--vendor", required=False, help="ベンダー名ヒント(任意)")
    args = parser.parse_args(argv)

    # Load from .env.local/.env first
    load_env_local()
    if not os.environ.get("GEMINI_API_KEY"):
        print("GEMINI_API_KEY が未設定です", file=sys.stderr)
        return 2

    data = extract_reservation(args.url, vendor_hint=args.vendor)
    print(json.dumps(data.model_dump(), ensure_ascii=False))
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
