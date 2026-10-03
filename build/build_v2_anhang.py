# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import pymupdf
from render_pdf import render
OUT = os.path.join(os.path.dirname(__file__), "..", "output", "v2")
NAVY, NAVY2, ACC = "#14264B", "#22386B", "#F5A800"

html = f"""<!doctype html><html lang="de"><head><meta charset="utf-8"><title>Anhang</title><style>
@page {{ size: A4; margin: 0 }} * {{ box-sizing: border-box; margin: 0; padding: 0 }}
html {{ -webkit-print-color-adjust: exact; print-color-adjust: exact }}
body {{ font-family: 'Liberation Sans', Arial, sans-serif; }}
.page {{ width: 210mm; height: 297mm; background: {NAVY}; color: #fff; position: relative; overflow: hidden }}
.bar {{ position: absolute; left: 0; top: 0; bottom: 0; width: 14mm; background: {ACC} }}
.sym {{ position: absolute; right: -10mm; top: 22mm; font-size: 300pt; line-height: 1; font-weight: 700; color: {NAVY2} }}
.main {{ position: absolute; left: 34mm; right: 24mm; top: 95mm }}
.k {{ color: {ACC}; font-size: 11pt; font-weight: 700; letter-spacing: .14em; text-transform: uppercase; margin-bottom: 6mm }}
h1 {{ font-size: 54pt; line-height: 1.05 }} .ln {{ width: 30mm; height: 1.6mm; background: {ACC}; margin: 9mm 0 7mm }}
.sub {{ font-size: 15pt; color: {ACC}; font-weight: 700 }} .sub2 {{ font-size: 12pt; color: #DCE3F2; margin-top: 3mm }}
.toc {{ position: absolute; left: 34mm; right: 24mm; top: 178mm; font-size: 13pt }}
.toc div {{ display: flex; gap: 3mm; align-items: baseline; margin-bottom: 3mm }}
.toc .d {{ flex: 1; border-bottom: .4mm dotted #6B7BA3; transform: translateY(-1mm) }} .toc b {{ color: {ACC} }}
.by {{ position: absolute; left: 34mm; bottom: 20mm; font-size: 12pt }}
</style></head><body><section class="page"><div class="bar"></div><div class="sym">§</div>
<div class="main"><div class="k">Projektbericht</div><h1>Anhang</h1><div class="ln"></div>
<div class="sub">Projektplanung: Rechte und Pflichten aus dem Ausbildungsvertrag</div><div class="sub2">Booklet-Projekt · Präsentation am 08.10.2026</div></div>
<div class="toc"><div><span>Protokoll-Vorlage</span><span class="d"></span><b>Seite 2</b></div><div><span>Projektskizze</span><span class="d"></span><b>Seite 3</b></div><div><span>Projektstrukturplan</span><span class="d"></span><b>Seite 5</b></div><div><span>Projektablaufplan (Tabelle, Netzplan, Gantt-Diagramm)</span><span class="d"></span><b>Seite 6</b></div></div>
<div class="by">Yasin &amp; Mido</div></section></body></html>"""
hp = os.path.join(os.path.dirname(__file__), "v2_anhang_deckblatt.html")
open(hp, "w", encoding="utf-8").write(html)
cover = os.path.join("/tmp", "v2_anhang_cover.pdf"); render(hp, cover)

out = pymupdf.open(cover)
for f in ("protokoll_vorlage", "projektskizze", "projektstrukturplan", "projektablaufplan"):
    out.insert_pdf(pymupdf.open(os.path.join(OUT, f + ".pdf")))
n = len(out)
for i, pg in enumerate(out):
    if i == 0: continue
    r = pg.rect
    land = r.width > r.height
    txt = f"Anhang · Seite {i+1} von {n}"
    col = (0.86, 0.89, 0.95) if land else (0.36, 0.40, 0.50)
    y = 20 if land else 24
    pg.insert_textbox(pymupdf.Rect(r.width - 260, y - 9, r.width - 28, y + 6), txt, fontsize=8.5, fontname="helv", color=col, align=pymupdf.TEXT_ALIGN_RIGHT)
out.save(os.path.join(OUT, "anhang_projektplanung.pdf"))
print("Anhang Seiten:", n, [ (round(p.rect.width), round(p.rect.height)) for p in out])
