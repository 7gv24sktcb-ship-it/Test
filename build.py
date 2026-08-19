#!/usr/bin/env python3
"""Build tdk-release-bench.html by inlining pdf.js into bench.template.html.

pdfjs-dist 4.10.38 ships ESM only. Both bundles end in a single `export{...}`
statement; we rewrite that into a globalThis assignment so the modules can be
inlined directly in the page. Setting globalThis.pdfjsWorker makes pdf.js take
its main-thread ("fake worker") path, so the page needs no Worker, no blob URL,
and no network — all of which the Artifact CSP would block.
"""
import re, pathlib

ROOT = pathlib.Path(__file__).parent
VENDOR = ROOT / "vendor"

EXPORT_TAIL = re.compile(r"export\{([^{}]*)\};?\s*$")

def to_global(src: str, global_name: str, only=None) -> str:
    m = EXPORT_TAIL.search(src)
    if not m:
        raise SystemExit(f"no trailing export statement found for {global_name}")
    pairs = []
    for part in m.group(1).split(","):
        local, _, exported = part.partition(" as ")
        local, exported = local.strip(), (exported.strip() or local.strip())
        if only and exported not in only:
            continue
        pairs.append(f"{exported}:{local}")
    if only:
        missing = set(only) - {p.split(":")[0] for p in pairs}
        if missing:
            raise SystemExit(f"{global_name} is missing exports: {sorted(missing)}")
    return src[: m.start()] + f"globalThis.{global_name}={{{','.join(pairs)}}};\n"

worker = to_global(
    (VENDOR / "pdf.worker.min.mjs").read_text(encoding="utf-8"),
    "pdfjsWorker",
    only={"WorkerMessageHandler"},
)
main = to_global(
    (VENDOR / "pdf.min.mjs").read_text(encoding="utf-8"),
    "pdfjsLib",
    only={"getDocument", "GlobalWorkerOptions", "PDFWorker", "version"},
)

for name, src in (("pdf.worker.min.mjs", worker), ("pdf.min.mjs", main)):
    if "</script" in src:
        raise SystemExit(f"{name} contains a script-closing sequence")

block = (
    "<!-- pdfjs-dist 4.10.38 (Apache-2.0), inlined and rewired to run on the main thread -->\n"
    f'<script type="module">{worker}</script>\n'
    f'<script type="module">{main}</script>'
)

template = (ROOT / "bench.template.html").read_text(encoding="utf-8")
if "<!--PDFJS-->" not in template:
    raise SystemExit("template is missing the <!--PDFJS--> marker")
out = template.replace("<!--PDFJS-->", block)
(ROOT / "tdk-release-bench.html").write_text(out, encoding="utf-8")
print(f"wrote tdk-release-bench.html — {len(out.encode('utf-8')):,} bytes")
