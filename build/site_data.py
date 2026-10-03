# -*- coding: utf-8 -*-
"""Erzeugt site/js/data.js aus den bestehenden Inhalten (data2.py) plus den Experten-Karten aus dem Auftrag."""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from data2 import *

EXPERTEN = [
    dict(t="Probezeit",
         kern=["Ein bis vier Monate (§ 20 BBiG)", "Kündigung jederzeit ohne Frist, schriftlich (§ 22 Abs. 1 und 3 BBiG)"],
         frage="Welche Kündigungsfrist gilt in der Probezeit?", loesung="Keine Frist, aber die Kündigung muss schriftlich erfolgen."),
    dict(t="Urlaub",
         kern=["Zu Jahresbeginn unter 16: 30, unter 17: 27, unter 18: 25, ab 18: 24 Werktage (§ 19 JArbSchG, § 3 BUrlG)",
               "Werktage sind alle Kalendertage außer Sonntagen und gesetzlichen Feiertagen."],
         frage="Wie viele Werktage Mindesturlaub hat eine Auszubildende, die zu Jahresbeginn 16 Jahre alt ist?", loesung="27 Werktage."),
    dict(t="Vergütung",
         kern=["Bei Beginn 2026 mindestens 724 / 854 / 977 / 1.014 € im 1. bis 4. Jahr (§ 17 BBiG)"],
         frage="Wie hoch ist die Mindestausbildungsvergütung im 3. Jahr bei Beginn 2026?", loesung="977 €."),
    dict(t="Kündigung",
         kern=["In der Probezeit ohne Frist.",
               "Danach fristlos aus wichtigem Grund (innerhalb von zwei Wochen nach Kenntnis) oder durch den Azubi mit vier Wochen Frist bei Berufswechsel oder Aufgabe der Ausbildung.",
               "Immer schriftlich, mit Gründen (§ 22 Abs. 2 bis 4 BBiG)."],
         frage="Was muss ein Azubi beachten, der nach der Probezeit kündigen will, weil er den Beruf wechselt?",
         loesung="Vier Wochen Frist, schriftlich, mit Angabe der Gründe."),
]

def build_data():
    d = dict(
        rg=[dict(t=t, ok=ok, b=b) for t, ok, b in RG],
        kopf=DET_KOPF,
        zeilen=[dict(t=t, f=f) for t, f in DET],
        fehler={str(n): dict(stelle=a, regel=b) for n, (a, b) in FEHLER.items()},
        faelle=[dict(label=("Reservefall " if f["reserve"] else "Fall ") + f["id"] + " (" + f["titel"] + ")", q=f["q"], a=f["a"], c=f["c"], fb=f["loesung"]) for f in FAELLE],
        quiz=[dict(q=a["q"], a=a["a"], c=a["c"], fb=a["fb"]) for a in ABSCHLUSS],
        experten=EXPERTEN,
        merk=[dict(thema=a, text=b, para=c) for a, b, c in MERKBLATT],
        quellen=[dict(t=t, u=u) for t, u in QUELLEN],
    )
    return "window.DATA = " + json.dumps(d, ensure_ascii=False, indent=1) + ";\n"
