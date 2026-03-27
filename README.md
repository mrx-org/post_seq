# post_seq

Static GitHub Pages app (**mr0sim**): load a Pulseq **`.seq`** from the URL query string (**`?data=`** — base64url of the file bytes, optional **`&name=`**), or fetch a hosted file with **`?url=`**. When present, that sequence is the **default input** for “Run pipeline”; a banner explains that on the page.

**Public URL:** [https://mrx-org.github.io/post_seq/](https://mrx-org.github.io/post_seq/) (served as **`index.html`**)

Nothing is uploaded to GitHub Pages; the app runs in the browser.

### Local file → open in the browser (URL carries the content)

From the repo directory, pass a **path** to your `.seq` file:

```bash
python -u send_example_seq.py path/to/my_sequence.seq
```

The script reads the file, builds `?data=<base64url>&name=...`, and opens the site. If the full URL is very long (large files), it uses a short **temporary HTML redirect** on Windows so the browser still opens.

Print the link without opening the browser:

```bash
python -u send_example_seq.py --print-only my_sequence.seq
```

If the encoded URL exceeds a safe length, the script exits with an error (file too large to embed in a URL).

---

## License

See the repository for license information.
