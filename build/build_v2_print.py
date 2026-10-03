# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from html import escape as esc
from pdfkit import *
from data2 import *
from render_pdf import render
OUT = os.path.join(os.path.dirname(__file__), "..", "output", "v2")
G, R = ("#2E9E4F", "#fff"), ("#D62839", "#fff")
P = []

# 1 Rote und gruene Karten (je 4 pro Seite)
def card(label, col):
    return f'<div style="background:{col[0]};color:{col[1]};border:0.3mm dashed #666;display:flex;align-items:center;justify-content:center;font-size:30pt;font-weight:700;text-align:center;line-height:1.1">{label}</div>'
cs = "".join(card("Stimmt", G) + card("Stimmt nicht", R) for _ in range(4))
P.append(page("Druckmaterial", "Rote und grüne Karten", f'<p class="note" style="margin-bottom:3mm">Pro Person je eine grüne („Stimmt“) und eine rote Karte („Stimmt nicht“). Farbig ausdrucken und an den gestrichelten Linien ausschneiden.</p><div style="display:grid;grid-template-columns:1fr 1fr;grid-template-rows:repeat(4,1fr);height:218mm">{cs}</div>', foot=False))

# 2 Arbeitsblatt Vertrags-Detektiv
kopf = "".join(f'<div style="{"font-weight:700;color:"+NAVY+";margin-bottom:1mm" if i==0 else ""}">{esc(t)}</div>' for i, t in enumerate(DET_KOPF))
det = "".join(f'<div style="margin-bottom:1.2mm">{esc(t)}</div>' for t, _ in DET)
rows = "".join(f'<tr><td class="b" style="text-align:center;width:11mm;height:16mm">{i}</td><td style="width:40mm"></td><td style="width:55mm"></td><td></td></tr>' for i in range(1, 6))
P.append(page("Aktivität 2", "Arbeitsblatt Vertrags-Detektiv", f"""
<div style="display:flex;gap:10mm;font-size:10.5pt;margin-bottom:4mm"><span>Name: <span style="display:inline-block;border-bottom:0.3mm solid #8E97AC;width:70mm"></span></span><span>Gruppe: <span style="display:inline-block;border-bottom:0.3mm solid #8E97AC;width:40mm"></span></span></div>
<p style="font-size:11pt;margin-bottom:3mm">Im Vertragsauszug stecken <b>5 Fehler</b>. Finde sie und begründe sie mit der passenden Regel.</p>
<div style="background:#F6F8FC;border:0.4mm solid #BFC6D6;border-radius:2mm;padding:4mm 6mm;font-family:'Liberation Serif',serif;font-size:11pt;line-height:1.35">{kopf}<div style="border-top:0.3mm solid #BFC6D6;margin:2mm 0"></div>{det}</div>
<table class="t" style="margin-top:7mm;font-size:10pt"><tr><th style="text-align:center">Fehler</th><th>Fehler (Stelle im Vertrag)</th><th>Regel (Paragraf)</th><th>Begründung</th></tr>{rows}</table>""", foot=False))

# 3 Merkblatt zweimal pro Seite
mrows = "".join(f'<tr><td style="font-weight:700;color:{NAVY};width:27mm;padding:1.5mm 2mm">{esc(a)}</td><td style="padding:1.5mm 2mm">{esc(b)}</td><td style="font-weight:700;color:{NAVY};width:27mm;padding:1.5mm 2mm;border-left:0.3mm solid #D5D9E3">{esc(c)}</td></tr>' for a, b, c in MERKBLATT)
one = f'<div style="height:140mm;padding:4mm 0 0"><div style="background:{NAVY};color:#fff;padding:2mm 4mm;font-weight:700;font-size:11pt;border-left:3mm solid {ACCENT}">Merkblatt: Das Wichtigste auf einer Seite <span style="font-weight:400;font-size:8.5pt;color:#DCE3F2">· Rechte und Pflichten aus dem Ausbildungsvertrag · Stand Oktober 2026</span></div><table class="t" style="font-size:9.4pt;line-height:1.3"><tr><th style="padding:1.5mm 2mm;font-size:9.4pt">Thema</th><th style="padding:1.5mm 2mm;font-size:9.4pt">Das müsst ihr wissen</th><th style="padding:1.5mm 2mm;font-size:9.4pt">Paragraf</th></tr>{mrows}</table></div>'
P.append(f'<section class="page" style="padding:6mm 10mm 0"><div style="height:145mm;border-bottom:0.3mm dashed #666">{one}</div><div style="height:145mm">{one}</div></section>')

open(os.path.join(os.path.dirname(__file__), "v2_druck.html"), "w", encoding="utf-8").write(doc("".join(P), "Druckmaterial"))
render(os.path.join(os.path.dirname(__file__), "v2_druck.html"), os.path.join(OUT, "druckmaterial.pdf"))
