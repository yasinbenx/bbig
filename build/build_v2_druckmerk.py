# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from html import escape as esc
from pdfkit import *
from data2 import MERKBLATT
from render_pdf import render
OUT = os.path.join(os.path.dirname(__file__), "..", "output", "v2")
mrows = "".join(f'<tr><td style="font-weight:700;color:{NAVY};width:27mm;padding:1.3mm 2mm">{esc(a)}</td><td style="padding:1.3mm 2mm">{esc(b)}</td><td style="font-weight:700;color:{NAVY};width:27mm;padding:1.3mm 2mm;border-left:0.3mm solid #D5D9E3">{esc(c)}</td></tr>' for a, b, c in MERKBLATT)
one = f'''<div style="height:143mm;padding:3mm 0 0"><div style="background:{NAVY};color:#fff;padding:2mm 4mm;font-weight:700;font-size:11pt;border-left:3mm solid {ACCENT}">Merkblatt: Das Wichtigste auf einer Seite <span style="font-weight:400;font-size:8.5pt;color:#DCE3F2">· Rechte und Pflichten aus dem Ausbildungsvertrag · Stand Oktober 2026</span></div>
<table class="t" style="font-size:8.8pt;line-height:1.28"><tr><th style="padding:1.3mm 2mm;font-size:8.8pt">Thema</th><th style="padding:1.3mm 2mm;font-size:8.8pt">Das müsst ihr wissen</th><th style="padding:1.3mm 2mm;font-size:8.8pt">Paragraf</th></tr>{mrows}</table>
<div style="display:flex;align-items:center;gap:4mm;margin-top:2.5mm;border:0.4mm solid {NAVY};border-radius:1.5mm;padding:1mm 3mm"><img src="{qr_uri()}" style="display:block;width:17mm;height:17mm;flex:none"><div><div style="font-weight:700;font-size:10.5pt;color:{NAVY}">Üben auf dem Handy</div><div style="font-size:9.5pt">{URL_KURZ}</div></div></div></div>'''
sec = f'<section class="page" style="padding:5mm 10mm 0"><div style="height:146mm;border-bottom:0.3mm dashed #666">{one}</div><div style="height:146mm;padding-top:1mm">{one}</div></section>'
p = os.path.join(os.path.dirname(__file__), "v2_druckmerk.html")
open(p, "w", encoding="utf-8").write(doc(sec, "Merkblatt zum Schneiden"))
render(p, os.path.join(OUT, "druck_merkblatt.pdf")); os.remove(p)
