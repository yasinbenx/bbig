# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from html import escape as esc
from pdfkit import *
from data import *

COL = {"A": ("#D62839", "#fff"), "B": ("#1F6FD1", "#fff"), "C": ("#F7C600", NAVY), "D": ("#2E9E4F", "#fff")}
P = []
# Antwortkarten A-D (1 Satz je Seite, 2x2, Schnittlinien)
cards = "".join(f'<div style="background:{COL[L][0]};color:{COL[L][1]};display:flex;align-items:center;justify-content:center;font-size:150pt;font-weight:700;border:0.3mm dashed #666">{L}</div>' for L in "ABCD")
P.append(page("Druckmaterial", "Antwortkarten A bis D", f'<p class="note" style="margin-bottom:4mm">Pro Person ein Satz. Ausdrucken (farbig) und an den gestrichelten Linien ausschneiden.</p><div style="display:grid;grid-template-columns:1fr 1fr;grid-template-rows:1fr 1fr;gap:0;height:215mm">{cards}</div>', foot=False))

# Kartenset Station 2
def kset(title, items, sit):
    cs = ""
    for lab, txt in items:
        bg = NAVY if sit else ACCENT_L
        fg = "#fff" if sit else NAVY
        tag = f'<div style="font-size:9pt;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:{ACCENT if sit else "#9A6A00"};margin-bottom:2mm">{"Situation" if sit else "Regelung"} {lab}</div>'
        cs += f'<div style="background:{bg};color:{fg};border:0.3mm dashed #666;padding:6mm;display:flex;flex-direction:column;justify-content:center"><div>{tag}<div style="font-size:13pt;font-weight:700;line-height:1.35">{esc(txt)}</div></div></div>'
    return page("Station 2 · Situationen zuordnen", title, f'<p class="note" style="margin-bottom:4mm">Pro Zweierteam ein Set (8 Situations- und 8 Regelungskarten). Ausdrucken, schneiden und gemischt ausgeben.</p><div style="display:grid;grid-template-columns:1fr 1fr;grid-template-rows:repeat(4,1fr);height:214mm">{cs}</div>', foot=False)
P.append(kset("Situationskarten", [(str(n), t) for n, t, _ in PAARE], True))
P.append(kset("Regelungskarten", [(k, v) for k, v in REGELUNGEN.items()], False))

# Arbeitsblatt
def fall(f):
    ans = "".join(f'<div class="ans" style="margin-top:1mm;padding:1mm 3mm;font-size:10pt"><b>{L}</b><span>{esc(t)}</span></div>' for L, t in zip("ABCD", f["a"]))
    return f'<div class="card" style="padding:2.5mm 5mm;margin-bottom:3.5mm"><h3><span>{f["id"]}</span>{"Reservefall" if f["reserve"] else "Fall"} {f["id"]} ({esc(f["titel"])})</h3><div style="margin-bottom:1mm;font-size:10pt">{esc(f["q"])}</div>{ans}<div style="margin-top:2mm;font-size:9.5pt;color:{MUTED}">Begründung mit Regel (Paragraf): <span style="display:inline-block;border-bottom:0.3mm solid #8E97AC;width:100mm"></span></div></div>'
head = f'<div style="display:flex;gap:8mm;font-size:10.5pt;margin-bottom:4mm"><span>Gruppe: <span style="display:inline-block;border-bottom:0.3mm solid #8E97AC;width:60mm"></span></span><span>Gewählte Antwort: A B C D</span></div>'
P.append(page("Station 4 · IHK-Fälle", "Arbeitsblatt: Fälle A bis C", head + "".join(fall(f) for f in FAELLE[:3]), foot=False))
P.append(page("Station 4 · IHK-Fälle", "Arbeitsblatt: Reservefälle D und E", head + "".join(fall(f) for f in FAELLE[3:]), foot=False))
html = doc("".join(P), "Druckmaterial")
open(os.path.join(os.path.dirname(__file__), "druck.html"), "w", encoding="utf-8").write(html)
