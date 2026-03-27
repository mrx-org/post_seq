"""Open the post_seq / mr0sim page with a .seq file embedded in the URL (#b64=…)."""

from __future__ import annotations

import argparse
import base64
import json
import os
import sys
import tempfile
import webbrowser
from pathlib import Path

# Browsers limit total URL length; stay under a conservative cap for #b64= links.
MAX_LINK_CHARS = 1_500_000
# Windows fails opening very long URLs via webbrowser (command-line limits).
# Above this, open a tiny temp .html that redirects with location.replace(safe JS string).
URL_OPEN_VIA_REDIRECT_HTML = 2048

ROOT = Path(__file__).resolve().parent
DEFAULT_SEQ = ROOT / "example.seq"
# Default: post_seq. Set POST_SEQ_PAGE to your mr0sim URL, e.g. …/index2.html on GitHub Pages.
PAGE_URL = os.environ.get("POST_SEQ_PAGE", "https://mrx-org.github.io/post_seq/").rstrip("/") + "/"


def open_browser_to_url(url: str) -> None:
    """Open URL in default browser; avoid passing huge strings to the OS on Windows."""
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
        "--seq",
        type=Path,
        default=DEFAULT_SEQ,
        help=f"path to .seq file (default: {DEFAULT_SEQ.name})",
    )
    p.add_argument(
        "--no-browser",
        action="store_true",
        help="print the URL instead of opening the browser",
    )
    args = p.parse_args()

    path = args.seq.resolve()
    if not path.is_file():
        print(f"Not found: {path}", file=sys.stderr)
        return 1

    data = path.read_bytes()
    b64 = base64.urlsafe_b64encode(data).decode("ascii").rstrip("=")
    link = f"{PAGE_URL.rstrip('/')}/#b64={b64}"
    if len(link) > MAX_LINK_CHARS:
        print(
            f"URL would be {len(link)} characters (limit ~{MAX_LINK_CHARS}). "
            "Host the .seq file and open the page with ?url=…, or use the file picker.",
            file=sys.stderr,
        )
        return 1

    if args.no_browser:
        print(link)
    else:
        open_browser_to_url(link)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
