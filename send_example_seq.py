"""POST example.seq as multipart form field "file" (same contract as README)."""

from __future__ import annotations

import argparse
import base64
import json
import os
import sys
import tempfile
import webbrowser
from pathlib import Path

import requests

# Browsers limit total URL length; stay under a conservative cap for #b64= links.
MAX_LINK_CHARS = 1_500_000
# Windows fails opening very long URLs via webbrowser (command-line limits; "path too long").
# Above this, open a tiny temp .html that redirects with location.replace(safe JS string).
URL_OPEN_VIA_REDIRECT_HTML = 2048

ROOT = Path(__file__).resolve().parent
DEFAULT_SEQ = ROOT / "example.seq"
PAGE_URL = "https://mrx-org.github.io/post_seq/"


def open_browser_to_url(url: str) -> None:
    """Open URL in default browser; avoid passing huge strings to the OS on Windows."""
    if len(url) <= URL_OPEN_VIA_REDIRECT_HTML:
        webbrowser.open(url)
        return
    tmp = Path(tempfile.gettempdir()) / "post_seq_redirect.html"
    # json.dumps is safe for embedding as a JS string literal.
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
        "--url",
        default=os.environ.get("POST_SEQ_URL", PAGE_URL),
        help=f"POST target (default: {PAGE_URL}; env POST_SEQ_URL overrides)",
    )
    p.add_argument(
        "--seq",
        type=Path,
        default=DEFAULT_SEQ,
        help=f"path to .seq file (default: {DEFAULT_SEQ.name})",
    )
    p.add_argument("--timeout", type=float, default=120.0)
    p.add_argument(
        "--no-browser",
        action="store_true",
        help="do not open the post_seq page in the default browser",
    )
    p.add_argument(
        "--open-link",
        action="store_true",
        help="open page with #b64=… (UTF-8 bytes, base64url); no POST. Fails if URL too long.",
    )
    args = p.parse_args()

    path = args.seq.resolve()
    if not path.is_file():
        print(f"Not found: {path}", file=sys.stderr)
        return 1

    if args.open_link:
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
    if not r.ok and args.url.rstrip("/") == PAGE_URL.rstrip("/"):
        print(
            "(GitHub Pages is static and often returns 405 for POST; "
            "use the opened page to load the .seq file locally.)",
            file=sys.stderr,
        )

    if not args.no_browser:
        open_browser_to_url(PAGE_URL)

    return 0 if r.ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
