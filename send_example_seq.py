"""Open post_seq: local .seq via ?data= (base64url) or remote file via ?url= (HTTPS)."""

from __future__ import annotations

import argparse
import base64
import json
import sys
import tempfile
import webbrowser
from pathlib import Path
from urllib.parse import quote

PAGE = "https://mrx-org.github.io/post_seq/"
# Windows browser launch breaks on very long command lines; use a tiny redirect HTML.
URL_OPEN_VIA_REDIRECT_HTML = 2048
# Hard limit for total address length (browser-dependent).
MAX_PAGE_URL_LEN = 1_500_000


def open_browser(url: str) -> None:
    if len(url) <= URL_OPEN_VIA_REDIRECT_HTML:
        webbrowser.open(url)
        return
    tmp = Path(tempfile.gettempdir()) / "post_seq_redirect.html"
    page = (
        "<!DOCTYPE html><meta charset=\"utf-8\"><title>post_seq</title>"
        "<script>location.replace("
        + json.dumps(url)
        + ");</script>"
    )
    tmp.write_text(page, encoding="utf-8")
    webbrowser.open(tmp.as_uri())


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "target",
        help='Path to a local .seq file, OR an https:// URL of a hosted .seq',
    )
    p.add_argument(
        "--print-only",
        action="store_true",
        help="print the post_seq URL only; do not open the browser",
    )
    args = p.parse_args()

    prefix = PAGE
    t = args.target.strip()
    if t.startswith("https://"):
        full = prefix + "?url=" + quote(t, safe="")
    else:
        path = Path(t).expanduser().resolve()
        if not path.is_file():
            print(f"Not a file: {path}", file=sys.stderr)
            return 1
        raw = path.read_bytes()
        b64 = base64.urlsafe_b64encode(raw).decode("ascii").rstrip("=")
        full = (
            prefix
            + "?data="
            + b64
            + "&name="
            + quote(path.name, safe="")
        )
        if len(full) > MAX_PAGE_URL_LEN:
            print(
                "Encoded URL would exceed the safe length for browsers.\n"
                "Host the file (e.g. GitHub raw) and use:\n"
                f'  python -u send_example_seq.py "https://…/file.seq"',
                file=sys.stderr,
            )
            return 1

    if args.print_only:
        print(full)
    else:
        open_browser(full)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
