# -*- coding: utf-8 -*-
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from data import *

modes = {
 "check": dict(name="Wissens-Check", sub="Station 1 · 3 Blitzfragen", items=[dict(q=x["q"], a=x["a"], c=x["c"], fb=x["fb"]) for x in WISSENS_CHECK]),
 "million": dict(name="Azubi-Millionär", sub="Station 3 · 7 Fragen · 50:50-Joker", items=[dict(q=x["q"], a=x["a"], c=x["c"], fb=x["fb"], stufe=x["stufe"]) for x in MILLIONAER]),
 "faelle": dict(name="IHK-Fälle", sub="Station 4 · Fälle A bis E", items=[dict(q=x["q"], a=x["a"], c=x["c"], fb=x["loesung"], label=("Reservefall " if x["reserve"] else "Fall ") + x["id"] + " · " + x["titel"]) for x in FAELLE]),
 "abschluss": dict(name="Abschluss-Quiz", sub="Station 5 · 5 neue Situationen", items=[dict(q=x["q"], a=x["a"], c=x["c"], fb=x["fb"]) for x in ABSCHLUSS]),
}
html = open(os.path.join(os.path.dirname(__file__), "quiz_template.html"), encoding="utf-8").read()
html = html.replace("/*DATA*/", "const MODES = " + json.dumps(modes, ensure_ascii=False) + ";")
open(os.path.join(os.path.dirname(__file__), "..", "output", "quiz.html"), "w", encoding="utf-8").write(html)
print(len(html), "Bytes")
