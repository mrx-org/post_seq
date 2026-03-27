# post_seq

Static GitHub Pages app: open a Pulseq **`.seq`** file by passing a **single query parameter** — the **HTTPS URL of the file**, as a **percent-encoded** string.

**Public URL:** [https://mrx-org.github.io/post_seq/](https://mrx-org.github.io/post_seq/)

## How it works

1. Host your `.seq` somewhere **public over HTTPS** (see below).
2. Build a link to this site with **`?url=`** set to that address, **URL-encoded** (so `https://` becomes `https%3A%2F%2F`, etc.).
3. Open the link. The page **`fetch`es** the file in the browser and shows the text. Nothing is uploaded to GitHub Pages.

Example shape:

```text
https://mrx-org.github.io/post_seq/?url=https%3A%2F%2Fraw.githubusercontent.com%2FUSER%2FREPO%2Fmain%2Fpath%2Ffile.seq
```

### Requirements

- **HTTPS** for the file URL (mixed content rules).
- **CORS**: the file host must allow **`GET`** from **`https://mrx-org.github.io`** (many **GitHub raw** / **Gist raw** URLs work).

### Helper script (optional)

From the repo root, open the page with a correctly encoded `?url=` (stdlib only):

```bash
python -u send_example_seq.py "https://raw.githubusercontent.com/USER/REPO/REF/path/file.seq"
```

Print the final URL without opening a browser:

```bash
python -u send_example_seq.py --print-only "https://…/file.seq"
```

### Build `?url=` yourself

**JavaScript** (e.g. browser console):

```javascript
const fileUrl = "https://raw.githubusercontent.com/USER/REPO/REF/path/file.seq";
const page = "https://mrx-org.github.io/post_seq/?url=" + encodeURIComponent(fileUrl);
console.log(page);
```

**Python:**

```python
from urllib.parse import quote

file_url = "https://raw.githubusercontent.com/USER/REPO/REF/path/file.seq"
page = "https://mrx-org.github.io/post_seq/?url=" + quote(file_url, safe="")
print(page)
```

### Hosting the `.seq` file

| Option | Notes |
|--------|--------|
| **GitHub** (public repo → **Raw**) | `https://raw.githubusercontent.com/...` |
| **GitHub Gist** (public → **Raw**) | `https://gist.githubusercontent.com/.../raw/...` |
| Other HTTPS + CORS | Must allow browser `fetch` from `https://mrx-org.github.io`. |

### Test

1. Confirm the **raw** file URL opens in a browser tab and shows the sequence text.
2. On [post_seq](https://mrx-org.github.io/post_seq/), open the console and run  
   `fetch("YOUR_RAW_URL", { mode: "cors" }).then(r => r.text()).then(console.log)`  
   If that succeeds, **`?url=`** will work.

---

## License

See the repository for license information.
