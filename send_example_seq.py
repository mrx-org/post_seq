"""POST example.seq as multipart form field "file" (same contract as README)."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent
DEFAULT_SEQ = ROOT / "example.seq"


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--url",
        default=os.environ.get(
            "POST_SEQ_URL",
            "https://httpbin.org/post",
        ),
        help="POST target (env POST_SEQ_URL overrides default)",
    )
    p.add_argument(
        "--seq",
        type=Path,
        default=DEFAULT_SEQ,
        help=f"path to .seq file (default: {DEFAULT_SEQ.name})",
    )
    p.add_argument("--timeout", type=float, default=120.0)
    args = p.parse_args()

    path = args.seq.resolve()
    if not path.is_file():
        print(f"Not found: {path}", file=sys.stderr)
        return 1

    with path.open("rb") as f:
        r = requests.post(
            args.url,
            files={
                "file": (
                    path.name,
                    f,
                    "application/octet-stream",
                )
            },
            timeout=args.timeout,
        )

    print(r.status_code)
    text = r.text
    if len(text) > 4000:
        print(text[:4000] + "\n… [truncated]")
    else:
        print(text)
    return 0 if r.ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
