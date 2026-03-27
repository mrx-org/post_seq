"""Open post_seq with ?url=<percent-encoded HTTPS URL> pointing to a .seq file."""

from __future__ import annotations

import argparse
import sys
import webbrowser
from urllib.parse import quote

PAGE = "https://mrx-org.github.io/post_seq/"


def page_url_for_seq_url(seq_https_url: str) -> str:
    return PAGE.rstrip("/") + "/?url=" + quote(seq_https_url.strip(), safe="")


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "seq_url",
        help='HTTPS URL of the .seq file (e.g. "https://raw.githubusercontent.com/.../file.seq")',
    )
    p.add_argument(
        "--print-only",
        action="store_true",
        help="print the post_seq URL only; do not open the browser",
    )
    args = p.parse_args()

    u = args.seq_url.strip()
    if not u.startswith("https://"):
        print("Error: URL must start with https://", file=sys.stderr)
        return 1

    full = page_url_for_seq_url(u)
    if args.print_only:
        print(full)
    else:
        webbrowser.open(full)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
