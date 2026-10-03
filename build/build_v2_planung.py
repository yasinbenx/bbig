# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import plan2
sys.modules["plan"] = plan2          # Zeichner nutzen jetzt die v2-Planung
from html import escape as esc
from plan2 import *
from psp_render import fit
from ablauf_render import gantt, netzplan, table_html
from render_pdf import render
from shot import shot
import build_planung_css as C

OUT = os.path.join(os.path.dirname(__file__), "..", "output", "v2"); os.makedirs(OUT, exist_ok=True)
IMG = os.path.join(os.path.dirname(__file__), "img"); T = lambda f: os.path.join(os.path.dirname(__file__), f)
RIGHT = "Booklet-Projekt<br>Yasin &amp; Mido"
page, doc = C.page, C.doc

# PSP (A4 quer)
svg, px, _ = fit(1070, 640, 6, 19, 30); print("PSP px", px)
h = doc(page("Projektplanung", "Projektstrukturplan", svg, RIGHT), "Projektstrukturplan"); open(T("v2_psp.html"), "w", encoding="utf-8").write(h)
render(T("v2_psp.html"), os.path.join(OUT, "projektstrukturplan.pdf"))
shot(h, os.path.join(OUT, "projektstrukturplan.png"), 1123, 794, 3.125)

# Ablaufplan (3 Seiten)
ms_rows = "".join(f'<tr><td class="c b">M{k}</td><td>{esc(nm)}</td><td class="c">{fmt(t, True)}</td></tr>' for k, nm, t in MS)
p1 = page("Projektablaufplan · Seite 1 von 3", "Tabelle der Arbeitspakete", '<style>table.pt td{padding:1.7mm 2.4mm}</style>' + table_html() +
          f'<table class="pt" style="margin-top:6mm;width:60%"><tr><th class="c" style="width:14mm">Nr.</th><th>Meilenstein (Soll)</th><th class="c" style="width:32mm">Termin</th></tr>{ms_rows}</table>'
          '<p class="note"><b>Soll</b> = geplante Termine, berechnet aus Dauer (Arbeitstage Mo–Fr) und Vorgängern; die Umsetzung beginnt am 01.10. <b>Ist</b> wird nach der Durchführung eingetragen. Kürzel in den Grafiken: Y = Yasin, M = Mido, Y+M = beide gemeinsam.</p>', RIGHT)
p2 = page("Projektablaufplan · Seite 2 von 3", "Netzplan", netzplan(1070, 625, 12, 112), RIGHT)
p3 = page("Projektablaufplan · Seite 3 von 3", "Gantt-Diagramm", gantt(1070, 640, 13, False, 0.38), RIGHT)
open(T("v2_ablauf.html"), "w", encoding="utf-8").write(doc(p1 + p2 + p3, "Projektablaufplan"))
render(T("v2_ablauf.html"), os.path.join(OUT, "projektablaufplan.pdf"))

# Bilder fuer die Folien
svg2, px2, _ = fit(1260, 600, 6, 20, 30); print("PSP Folie px", px2)
shot(f'<body style="margin:0;background:#fff">{svg2}</body>', os.path.join(IMG, "v2_psp_folie.png"), 1260, 600, 2)
g = gantt(1260, 600, 15.5, False, 0.40)
import re; gh = float(re.search(r'viewBox="0 0 1260 ([\d.]+)"', g).group(1))
shot(f'<body style="margin:0;background:#fff">{g}</body>', os.path.join(IMG, "v2_gantt_folie.png"), 1260, int(gh) + 1, 2)
print("Gantt Folie Hoehe", gh)
