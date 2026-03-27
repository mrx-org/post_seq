# post_seq

Static page for inspecting Pulseq `.seq` files in the browser.

**Public URL:** [https://mrx-org.github.io/post_seq/](https://mrx-org.github.io/post_seq/)

## GitHub Pages

[GitHub Pages](https://pages.github.com/) serves **static files only**. The site reads `.seq` files **locally in the browser** (JavaScript) for preview.

### Links (`?…` and `#…`)

Putting the full sequence text in a query string like `?data=…very long…` is **not a good idea**: browsers cap total URL length (often on the order of **1–2 MB** in practice), URLs are stored in history and server logs, and encoding increases size.

The page supports:

| Mechanism | Use case |
|-----------|----------|
| **`?url=https://…/file.seq`** | The app **GETs** that URL (must allow **CORS** from `https://mrx-org.github.io`). Good for **large** files hosted on GitHub raw, a CDN, etc. |
| **`#b64=…`** (base64url of UTF-8 bytes) | Embedded payload **without** sending it to the GitHub Pages server (fragment is client-only). Still limited by **maximum URL length** in the browser. |
| **`?seq=…`** | **Very short** snippets only (the page enforces a small limit). |

### Python helper

From the repo root (or this folder), open the public page with a local `.seq` embedded in `#b64=`:

```bash
python -u send_example_seq.py
```

Other file, or print the URL instead of opening the browser:

```bash
python -u send_example_seq.py --seq path/to/file.seq
python -u send_example_seq.py --no-browser
```

On Windows, long URLs are opened via a short temp redirect HTML file so the OS command line limit is not exceeded.

To open **mr0sim** (`index2.html`) with the same `#b64=` link, set the target page before running, for example:

```bash
set POST_SEQ_PAGE=https://mrx-org.github.io/post_seq/index2.html
python -u send_example_seq.py
```

(Adjust the URL to wherever `index2.html` is hosted.)

### Browser JavaScript → simulation API

If you add a backend that accepts uploads, you can POST from the page with [`fetch`](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API) and [`FormData`](https://developer.mozilla.org/en-US/docs/Web/API/FormData). The simulation server must send **CORS** headers allowing `https://mrx-org.github.io` if called from this origin.

---

## License

See the repository for license information.
