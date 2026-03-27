# post_seq

Static page for inspecting Pulseq `.seq` files in the browser, plus examples for sending a `.seq` file with **HTTP POST** (multipart form).

**Public URL:** [https://mrx-org.github.io/post_seq/](https://mrx-org.github.io/post_seq/)

## GitHub Pages and POST

[GitHub Pages](https://pages.github.com/) serves **static files only**. It does **not** run server code, so it cannot accept `POST` bodies or store uploaded files. The site reads `.seq` files **locally in the browser** (JavaScript) for preview.

The Python and MATLAB snippets below use the intended API: **`POST`** with multipart field name **`file`**. Use them against any HTTP server you control that implements the same contract (for example a small Flask or FastAPI app, or a serverless function). You can keep the same URL path after you add such a backend, or point the scripts to your server’s URL.

### Links (`?…` and `#…`)

Putting the full sequence text in a query string like `?data=…very long…` is **not a good idea**: browsers cap total URL length (often on the order of **1–2 MB** in practice, and much less in older stacks), URLs are stored in history and server logs, and encoding increases size.

The page supports:

| Mechanism | Use case |
|-----------|----------|
| **`?url=https://…/file.seq`** | The app **GETs** that URL (must allow **CORS** from `https://mrx-org.github.io`). Good for **large** files hosted on GitHub raw, a CDN, etc. |
| **`#b64=…`** (base64url of UTF-8 bytes) | Embedded payload **without** sending it to the GitHub Pages server (fragment is client-only). Still limited by **maximum URL length** in the browser—fine for small/medium files, not for arbitrary multi‑MB files. |
| **`?seq=…`** | **Very short** snippets only (the page enforces a small limit). |

Use **`send_example_seq.py --open-link`** to open the site with a `#b64=` link when the file is small enough; otherwise host the `.seq` and open `?url=…`.

### Browser JavaScript → simulation API

Yes. The GitHub Pages site only **hosts** the HTML/JS; your script runs in the visitor’s browser. After the user picks a `.seq` file, JavaScript holds a [`File`](https://developer.mozilla.org/en-US/docs/Web/API/File) object. You can forward it to your simulation backend with [`fetch`](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API) and [`FormData`](https://developer.mozilla.org/en-US/docs/Web/API/FormData), for example:

```javascript
const simulationUrl = "https://your-simulation-api.example.com/run"; // your API

async function sendSeq(file) {
  const body = new FormData();
  body.append("file", file, file.name);
  const res = await fetch(simulationUrl, { method: "POST", body, mode: "cors" });
  if (!res.ok) throw new Error(await res.text());
  return res.json(); // or res.text(), depending on your API
}
```

The simulation server must respond with [**CORS**](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CORS) headers that allow the GitHub Pages origin, e.g. `Access-Control-Allow-Origin: https://mrx-org.github.io` (or a specific path if you use a project Pages URL). Without that, the browser will block the response. Secrets (API keys) should live on the server or use a short-lived token flow, not hard-coded in public static JS.

---

## Python (`requests`)

Install [requests](https://requests.readthedocs.io/) if needed (`pip install requests`).

```python
import requests

url = "https://mrx-org.github.io/post_seq/"
path = "my_sequence.seq"

with open(path, "rb") as f:
    r = requests.post(
        url,
        files={
            "file": (
                path,
                f,
                "application/octet-stream",
            )
        },
        timeout=60,
    )

print(r.status_code)
print(r.text[:500] if r.text else "")
```

On pure GitHub Pages, `POST` to this URL typically returns **405 Method Not Allowed**. Point `url` at your own upload endpoint that accepts `multipart/form-data` with field **`file`**.

---

## MATLAB

### Option A: `curl` (simplest; available on Windows 10+ and most systems)

```matlab
url = 'https://mrx-org.github.io/post_seq/';
seqFile = 'my_sequence.seq';

cmd = sprintf('curl -sS -w "\nHTTP_CODE:%%{http_code}" -X POST -F "file=@%s" "%s"', seqFile, url);
[status, result] = system(cmd);
disp(result);
```

Adjust `seqFile` to a full path if the file is not on the MATLAB path.

### Option B: `matlab.net.http` (R2016b+; multipart without `curl`)

```matlab
import matlab.net.*
import matlab.net.http.*
import matlab.net.http.io.*

url = 'https://mrx-org.github.io/post_seq/';
seqFile = 'my_sequence.seq';

provider = FileProvider(seqFile, 'file', 'application/octet-stream');
body = MultipartFormProvider(provider);
req = RequestMessage('post', [], body);
uri = URI(url);
resp = req.send(uri);

disp(resp.StatusCode);
if ~isempty(resp.Body.Data)
    disp(char(resp.Body.Data));
end
```

Field name **`file`** must match what your server expects (same as the Python example).

---

## API summary

| Item        | Value |
|------------|--------|
| Method     | `POST` |
| Body       | `multipart/form-data` |
| File field | `file` |

---

## License

See the repository for license information.
