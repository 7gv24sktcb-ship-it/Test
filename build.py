#!/usr/bin/env python3
"""Build TDK Release Bench from bench.template.html.

Two targets share one template and one script bundle:

  local     dist/tdk-release-bench/index.html — a complete, standalone HTML
            document with the web fonts embedded as data URIs. Runs from
            file:// or any static web server, with no network access at all.

  artifact  tdk-release-bench.html — the body fragment the Claude Artifact
            host wraps in its own document skeleton; fonts come from Google
            Fonts, the one external host its CSP admits.

pdfjs-dist 4.10.38 ships ESM only. Both bundles end in a single `export{...}`
statement, which we rewrite into a globalThis assignment so the modules can be
inlined in the page. Setting globalThis.pdfjsWorker makes pdf.js take its
main-thread ("fake worker") path, so the page needs no Worker, no blob URL,
and no network — all of which the Artifact CSP would block.
"""
import argparse, pathlib, re, shutil, zipfile

ROOT = pathlib.Path(__file__).parent
VENDOR = ROOT / "vendor"
DIST = ROOT / "dist"

EXPORT_TAIL = re.compile(r"export\{([^{}]*)\};?\s*$")

GOOGLE_FONTS = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
    '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
    "family=Archivo:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500"
    '&family=Source+Serif+4:opsz,wght@8..60,400&display=swap">'
)

LOCAL_HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
  :root{color-scheme:light dark}
  img{max-width:100%}
  [hidden]{display:none !important}
</style>
"""


def to_global(src: str, global_name: str, only: set) -> str:
    m = EXPORT_TAIL.search(src)
    if not m:
        raise SystemExit(f"no trailing export statement found for {global_name}")
    pairs = []
    for part in m.group(1).split(","):
        local, _, exported = part.partition(" as ")
        local, exported = local.strip(), (exported.strip() or local.strip())
        if exported in only:
            pairs.append(f"{exported}:{local}")
    missing = only - {p.split(":")[0] for p in pairs}
    if missing:
        raise SystemExit(f"{global_name} is missing exports: {sorted(missing)}")
    return src[: m.start()] + f"globalThis.{global_name}={{{','.join(pairs)}}};\n"


def pdfjs_block() -> str:
    worker = to_global(
        (VENDOR / "pdf.worker.min.mjs").read_text(encoding="utf-8"),
        "pdfjsWorker",
        {"WorkerMessageHandler"},
    )
    main = to_global(
        (VENDOR / "pdf.min.mjs").read_text(encoding="utf-8"),
        "pdfjsLib",
        {"getDocument", "GlobalWorkerOptions", "PDFWorker", "version"},
    )
    for name, src in (("pdf.worker.min.mjs", worker), ("pdf.min.mjs", main)):
        if "</script" in src:
            raise SystemExit(f"{name} contains a script-closing sequence")
    return (
        "<!-- pdfjs-dist 4.10.38 (Apache-2.0), inlined and rewired to run on the main thread -->\n"
        f'<script type="module">{worker}</script>\n'
        f'<script type="module">{main}</script>'
    )


LOCAL_ONLY = re.compile(r"[ \t]*<!--LOCAL_ONLY-->.*?<!--/LOCAL_ONLY-->\n?", re.S)


def render(target: str) -> str:
    html = (ROOT / "bench.template.html").read_text(encoding="utf-8")
    # Drafting through the Claude API only exists in the local build: the
    # Artifact CSP blocks requests to api.anthropic.com, so the card and its
    # output tab would be dead controls there.
    if target != "local":
        html = LOCAL_ONLY.sub("", html)
    else:
        html = html.replace("<!--LOCAL_ONLY-->", "").replace("<!--/LOCAL_ONLY-->", "")
    if target == "local":
        fonts = "<style>\n" + (VENDOR / "fonts-embedded.css").read_text(encoding="utf-8") + "\n</style>"
        marks = {"DOC_OPEN": LOCAL_HEAD, "FONTS": fonts,
                 "BODY_OPEN": "</head>\n<body>", "DOC_CLOSE": "</body>\n</html>"}
    else:
        marks = {"DOC_OPEN": "", "FONTS": GOOGLE_FONTS, "BODY_OPEN": "", "DOC_CLOSE": ""}
    marks["PDFJS"] = pdfjs_block()
    for key, value in marks.items():
        token = f"<!--{key}-->"
        if token not in html:
            raise SystemExit(f"template is missing the {token} marker")
        html = html.replace(token, value)
    return html


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--target", choices=["local", "artifact", "both"], default="both")
    args = ap.parse_args()

    if args.target in ("artifact", "both"):
        out = ROOT / "tdk-release-bench.html"
        out.write_text(render("artifact"), encoding="utf-8")
        print(f"artifact  {out.relative_to(ROOT)} — {out.stat().st_size:,} bytes")

    if args.target in ("local", "both"):
        folder = DIST / "tdk-release-bench"
        if folder.exists():
            shutil.rmtree(folder)
        folder.mkdir(parents=True)
        (folder / "index.html").write_text(render("local"), encoding="utf-8")
        shutil.copy(ROOT / "README-local.txt", folder / "README.txt")
        archive = DIST / "tdk-release-bench.zip"
        with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
            for f in sorted(folder.rglob("*")):
                z.write(f, f.relative_to(DIST))
        print(f"local     {(folder / 'index.html').relative_to(ROOT)} — "
              f"{(folder / 'index.html').stat().st_size:,} bytes")
        print(f"archive   {archive.relative_to(ROOT)} — {archive.stat().st_size:,} bytes")


if __name__ == "__main__":
    main()
