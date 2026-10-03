# -*- coding: utf-8 -*-
import os, sys, shutil
sys.path.insert(0, os.path.dirname(__file__))
from html import escape as esc
from plan import *
from psp_render import fit
from ablauf_render import gantt, netzplan, table_html
from render_pdf import render
from shot import shot

OUT = os.path.join(os.path.dirname(__file__), "..", "output", "projektplanung")
os.makedirs(OUT, exist_ok=True)
NAVY, NAVY2, ACC = "#14264B", "#22386B", "#F5A800"

CSS = f"""
@page {{ size: A4 landscape; margin: 0; }}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
html {{ -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
body {{ font-family: 'Liberation Sans', Arial, sans-serif; color: #1A2238; font-size: 11pt; background: #fff; }}
.page {{ width: 297mm; height: 210mm; position: relative; overflow: hidden; page-break-after: always; break-after: page; display: flex; flex-direction: column; }}
.page:last-child {{ page-break-after: auto; break-after: auto; }}
.head {{ background: {NAVY}; color: #fff; padding: 7mm 14mm 5mm 20mm; position: relative; flex: none; display: flex; justify-content: space-between; align-items: flex-end; }}
.head::before {{ content: ''; position: absolute; left: 0; top: 0; bottom: 0; width: 5mm; background: {ACC}; }}
.kicker {{ color: {ACC}; font-size: 9pt; font-weight: 700; letter-spacing: .12em; text-transform: uppercase; }}
.head h1 {{ font-size: 21pt; line-height: 1.1; margin-top: 1mm; }}
.head .r {{ font-size: 10pt; color: #DCE3F2; text-align: right; }}
.body {{ flex: 1; min-height: 0; overflow: hidden; padding: 4mm 7mm 0 12mm; }}
.foot {{ position: absolute; left: 12mm; right: 7mm; bottom: 4mm; display: flex; justify-content: space-between; font-size: 8pt; color: #5B6680; border-top: 0.3mm solid #D5D9E3; padding-top: 1.5mm; }}
table.pt {{ width: 100%; border-collapse: collapse; font-size: 9.6pt; }}
table.pt th {{ background: {NAVY}; color: #fff; padding: 1.9mm 2.4mm; text-align: left; font-size: 9pt; line-height: 1.15; }}
table.pt th span {{ font-weight: 400; font-size: 7.5pt; color: #DCE3F2; }}
table.pt td {{ padding: 1.55mm 2.4mm; border-bottom: 0.3mm solid #D5D9E3; }}
table.pt tr:nth-child(even) td {{ background: #F6F8FC; }}
.c {{ text-align: center; }} .b {{ font-weight: 700; color: {NAVY}; }} .ist {{ color: #8A93A8; }}
.note {{ font-size: 8.8pt; color: #5B6680; margin-top: 2.5mm; line-height: 1.4; }}
svg {{ display: block; width: 100%; height: auto; }}
"""

def page(kicker, title, body, right=""):
    return (f'<section class="page"><div class="head"><div><div class="kicker">{esc(kicker)}</div><h1>{esc(title)}</h1></div><div class="r">{right}</div></div>'
            f'<div class="body">{body}</div><div class="foot"><span>Yasin &amp; Mido · Rechte und Pflichten aus dem Ausbildungsvertrag</span><span>Planung (Soll) · 10.09.–08.10.2026</span></div></section>')

def doc(pages, title): return f'<!doctype html><html lang="de"><head><meta charset="utf-8"><title>{esc(title)}</title><style>{CSS}</style></head><body>{pages}</body></html>'

RIGHT = "Booklet-Projekt<br>Yasin &amp; Mido"
T = lambda f: os.path.join(os.path.dirname(__file__), f)

# ---------------------------------------------------------------- PSP (A4 quer)
svg, px, my = fit(1070, 640, 6, 15.5, 30)
print("PSP A4 px", px)
psp_html = doc(page("Projektplanung", "Projektstrukturplan", svg, RIGHT), "Projektstrukturplan")
open(T("psp.html"), "w", encoding="utf-8").write(psp_html)
render(T("psp.html"), os.path.join(OUT, "projektstrukturplan.pdf"))
shot(psp_html.replace("<style>", "<style>html,body{margin:0}"), os.path.join(OUT, "projektstrukturplan.png"), 1123, 794, 3.125)

# ---------------------------------------------------------------- Ablaufplan (3 Seiten)
p1 = page("Projektablaufplan · Seite 1 von 3", "Tabelle der Arbeitspakete", table_html() +
          f'<p class="note"><b>Soll</b> = geplante Termine, berechnet aus Dauer (Arbeitstage Mo–Fr) und Vorgängern. Dauer ist die Zeitspanne vom Start bis zum Ende, die Pakete laufen neben Schule und Ausbildung. <b>Ist</b> wird nach der Durchführung eingetragen. Kürzel in den Grafiken: Y = Yasin, M = Mido, Y+M = beide gemeinsam.</p>', RIGHT)
p2 = page("Projektablaufplan · Seite 2 von 3", "Netzplan", netzplan(1070, 620, 10.5), RIGHT)
p3 = page("Projektablaufplan · Seite 3 von 3", "Gantt-Diagramm", gantt(1070, 630, 11.5), RIGHT)
open(T("ablauf.html"), "w", encoding="utf-8").write(doc(p1 + p2 + p3, "Projektablaufplan"))
render(T("ablauf.html"), os.path.join(OUT, "projektablaufplan.pdf"))

# ---------------------------------------------------------------- Bilder fuer die Folien
IMG = os.path.join(os.path.dirname(__file__), "img"); os.makedirs(IMG, exist_ok=True)
svg2, px2, _ = fit(1260, 600, 6, 16, 30)
print("PSP Folie px", px2)
shot(f'<body style="margin:0;background:#fff">{svg2}</body>', os.path.join(IMG, "psp_folie.png"), 1260, 600, 2)
shot(f'<body style="margin:0;background:#fff">{gantt(1260, 600, 14.5, True, 0.37)}</body>', os.path.join(IMG, "gantt_folie.png"), 1260, 600, 2)
print("fertig")
