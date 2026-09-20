#!/usr/bin/env python3
"""Construye el EPUB 3 de «La escribana de los dioses» desde 03-manuscrito/.
Uso: python3 build_epub.py  (desde cualquier directorio)
Salida: libros/libro-01/ebook/la-escribana-de-los-dioses.epub
"""
import re, zipfile, html, uuid, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]          # libros/libro-01
MS = ROOT / "03-manuscrito"
OUT = Path(__file__).resolve().parent / "la-escribana-de-los-dioses.epub"

TITLE = "La escribana de los dioses"
SERIES = "Los cuadernos de la escribana"
SERIES_POS = "1"
AUTHOR = "Albertoni"              # seudónimo de Nico (D-024, RATIFICADA)
LANG = "es-MX"
BOOK_ID = "urn:uuid:" + str(uuid.uuid5(uuid.NAMESPACE_URL, "unicostudios.mx/la-escribana-de-los-dioses"))

CSS = """
@charset "utf-8";
body { font-family: serif; line-height: 1.55; margin: 0 4%; }
h1.chap { font-size: 1.35em; font-weight: normal; text-align: left;
  margin: 2.5em 0 1.6em 0; page-break-before: always; }
h1.chap .num { display: block; font-size: .8em; letter-spacing: .12em;
  color: #666; margin-bottom: .35em; }
p { margin: 0; text-indent: 1.35em; }
p.first { text-indent: 0; }
hr.sep { border: none; text-align: center; margin: 1.4em 0; }
hr.sep:after { content: "—"; color: #888; }
.titlepage { text-align: center; margin-top: 18%; }
.titlepage .series { font-size: .8em; letter-spacing: .25em; color: #666; }
.titlepage h1 { font-size: 1.9em; font-weight: normal; margin: 1.2em 0 .4em 0; }
.titlepage .author { margin-top: 3em; font-size: .95em; letter-spacing: .1em; }
.blankpage { page-break-before: always; page-break-after: always; }
"""

def md_inline(s: str) -> str:
    s = html.escape(s, quote=False)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"\*(.+?)\*", r"<em>\1</em>", s)
    return s

def chapter_xhtml(num: int, title: str, body_lines: list[str]) -> str:
    out, first = [], True
    for ln in body_lines:
        t = ln.strip()
        if not t:
            continue
        if t == "—":
            out.append('<hr class="sep"/>')
            first = True
            continue
        cls = ' class="first"' if first else ""
        out.append(f"<p{cls}>{md_inline(t)}</p>")
        first = False
    body = "\n".join(out)
    return f"""<?xml version="1.0" encoding="utf-8"?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="{LANG}">
<head><title>{html.escape(title)}</title><link rel="stylesheet" type="text/css" href="style.css"/></head>
<body><section epub:type="chapter">
<h1 class="chap"><span class="num">{num}</span>{md_inline(title)}</h1>
{body}
</section></body></html>"""

def simple_page(title: str, inner: str) -> str:
    return f"""<?xml version="1.0" encoding="utf-8"?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="{LANG}">
<head><title>{html.escape(title)}</title><link rel="stylesheet" type="text/css" href="style.css"/></head>
<body>{inner}</body></html>"""

# --- leer manuscrito ---
chapters = []
for i in range(1, 41):
    p = MS / f"cap-{i:02d}.md"
    lines = p.read_text(encoding="utf-8").splitlines()
    m = re.match(r"#\s*\d+\.\s*(.+)", lines[0])
    title = m.group(1).strip() if m else f"Capítulo {i}"
    chapters.append((i, title, lines[1:]))

# --- páginas ---
titlepage = simple_page(TITLE, f"""
<div class="titlepage">
<p class="series">LOS CUADERNOS DE LA ESCRIBANA · CUADERNO I</p>
<h1>{html.escape(TITLE)}</h1>
<p class="author">{html.escape(AUTHOR)}</p>
</div>""")
blankpage = simple_page(" ", '<div class="blankpage">&#160;</div>')

COVER = Path(__file__).resolve().parent / "portada" / "portada.png"

manifest, spine, navlist, files = [], [], [], []

def add(fname, title_for_nav, content, in_nav=True, props=""):
    files.append((f"OEBPS/{fname}", content))
    mid = fname.replace(".", "_")
    prop = f' properties="{props}"' if props else ""
    manifest.append(f'<item id="{mid}" href="{fname}" media-type="application/xhtml+xml"{prop}/>')
    spine.append(f'<itemref idref="{mid}"/>')
    if in_nav:
        navlist.append(f'<li><a href="{fname}">{html.escape(title_for_nav)}</a></li>')

if COVER.exists():
    coverpage = f"""<?xml version="1.0" encoding="utf-8"?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="{LANG}">
<head><title>{html.escape(TITLE)}</title><style>body{{margin:0;padding:0;}} img{{width:100%;height:auto;}}</style></head>
<body epub:type="cover"><img src="cover.png" alt="{html.escape(TITLE)}"/></body></html>"""
    files.append(("OEBPS/cover.xhtml", coverpage))
    manifest.append('<item id="coverpage" href="cover.xhtml" media-type="application/xhtml+xml"/>')
    manifest.append('<item id="coverimg" href="cover.png" media-type="image/png" properties="cover-image"/>')
    spine.append('<itemref idref="coverpage"/>')

add("titlepage.xhtml", "Portada", titlepage)
for i, title, body in chapters:
    add(f"cap{i:02d}.xhtml", f"{i}. {title}", chapter_xhtml(i, title, body))
    if i == 11:   # la página en blanco, entre los capítulos que le corresponden
        add("blank.xhtml", "", blankpage, in_nav=False)

nav = f"""<?xml version="1.0" encoding="utf-8"?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="{LANG}">
<head><title>Índice</title><link rel="stylesheet" type="text/css" href="style.css"/></head>
<body><nav epub:type="toc"><h1>Índice</h1><ol>
{chr(10).join(navlist)}
</ol></nav></body></html>"""

now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
opf = f"""<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="bookid" xml:lang="{LANG}">
<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
<dc:identifier id="bookid">{BOOK_ID}</dc:identifier>
<dc:title id="t1">{html.escape(TITLE)}</dc:title>
<dc:language>{LANG}</dc:language>
<dc:creator id="aut">{html.escape(AUTHOR)}</dc:creator>
<meta property="dcterms:modified">{now}</meta>
<meta property="belongs-to-collection" id="c01">{html.escape(SERIES)}</meta>
<meta refines="#c01" property="collection-type">series</meta>
<meta refines="#c01" property="group-position">{SERIES_POS}</meta>
</metadata>
<manifest>
<item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>
<item id="css" href="style.css" media-type="text/css"/>
{chr(10).join(manifest)}
</manifest>
<spine>
{chr(10).join(spine)}
</spine>
</package>"""

container = """<?xml version="1.0" encoding="utf-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
<rootfiles><rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/></rootfiles>
</container>"""

with zipfile.ZipFile(OUT, "w") as z:
    z.writestr("mimetype", "application/epub+zip", compress_type=zipfile.ZIP_STORED)
    z.writestr("META-INF/container.xml", container, compress_type=zipfile.ZIP_DEFLATED)
    z.writestr("OEBPS/content.opf", opf, compress_type=zipfile.ZIP_DEFLATED)
    z.writestr("OEBPS/nav.xhtml", nav, compress_type=zipfile.ZIP_DEFLATED)
    z.writestr("OEBPS/style.css", CSS, compress_type=zipfile.ZIP_DEFLATED)
    for path, content in files:
        z.writestr(path, content, compress_type=zipfile.ZIP_DEFLATED)
    if COVER.exists():
        z.write(COVER, "OEBPS/cover.png", compress_type=zipfile.ZIP_DEFLATED)

print(f"OK: {OUT} ({OUT.stat().st_size/1024:.0f} KB), {len(chapters)} capítulos")
