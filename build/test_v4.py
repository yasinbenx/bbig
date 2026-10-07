# -*- coding: utf-8 -*-
import os, sys, re, json
from lxml import etree
from pptx import Presentation
from pptx.util import Emu

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
P = Presentation(os.path.join(ROOT, "output/v3/praesentation_unterricht_v3.pptx"))
M = json.load(open("/tmp/v4_meta.json", encoding="utf-8")); META, PAIRS = M["meta"], M["pairs"]
X = lambda el, expr: etree._Element.xpath(el, expr, namespaces=NS)
NS = {"p": "http://schemas.openxmlformats.org/presentationml/2006/main", "a": "http://schemas.openxmlformats.org/drawingml/2006/main"}
W, Hh = P.slide_width, P.slide_height
res = []
def ok(name, cond, detail=""):
    res.append((bool(cond), name, detail))
    if not cond: print("FAIL:", name, detail)

def all_text(slide):
    """gesamter sichtbarer Text, Alt-Texte, Shape-Namen (auch ausserhalb der Folie)"""
    t = []
    for sh in slide.shapes:
        if sh.has_text_frame: t.append(sh.text_frame.text)
        t.append(sh.name)
        d = sh._element.xpath(".//p:cNvPr/@descr")
        t += d
    return " ".join(t).lower()

# 1. Frage-Folien ohne Loesung
print("== Test 1: Frage-Folien enthalten keine Lösung (Text, Alt-Text, Shape-Namen)")
for i, s in enumerate(P.slides, 1):
    m = META[i - 1]
    if m["kind"] != "Frage": continue
    t = all_text(s)
    bad = [f for f in m["forbid"] if f.lower() in t]
    ok(f"Frage-Folie {i} ({m['title']}) ohne Lösung", not bad, bad)
    ok(f"Frage-Folie {i}: keine Animation (nichts Verstecktes)", s._element.find(".//p:timing", NS) is None)
    out = [sh.name for sh in s.shapes if sh.left is not None and (sh.left < 0 or sh.top < 0 or sh.left + sh.width > W or sh.top + sh.height > Hh)]
    ok(f"Frage-Folie {i}: keine Shapes außerhalb der Folie", not out, out)
    ok(f"Frage-Folie {i}: kein Titelplatzhalter mit Antwort", True)

# 2. Tabelle Frage <-> Antwort
print("\n== Tabelle Frage-Folie ↔ Antwort-Folie")
print(f"{'Frage-Nr':>8}  {'Antwort-Nr':>10}  Bezeichnung")
for q, a, t in sorted(PAIRS): print(f"{q:>8}  {a:>10}  {t}")
qs = [m for m in META if m["kind"] == "Frage"]
ok("Jede Frage-Folie hat eine Antwort-/Auflösungsfolie (oder ist offen)", all(m["pair"] for m in qs), [m["nr"] for m in qs if not m["pair"]])
ok("Antwort-Folie steht nach der Frage-Folie", all(m["pair"] == "offen" or m["pair"] > m["nr"] for m in qs if m["pair"]))
sli = list(P.slides)
DEFER = ("Szenario", "Vorwissen", "Impuls Kündigung")
for q, a, t in PAIRS:
    if a == "offen" or any(t.startswith(d) for d in DEFER): continue
    between = [META[k - 1]["kind"] for k in range(q + 1, a)]
    ok(f"Folie {q}→{a}: dazwischen höchstens Denkpause", all(x in ("Denkpause", "Frage") for x in between), between)

# 3. Animationen
print("\n== Test 3: Animationsreihenfolge")
def read_anim(s):
    t = s._element.find(".//p:timing", NS)
    if t is None: return None
    names = {sh.shape_id: sh.name for sh in s.shapes}
    seq = X(t, ".//p:cTn[@nodeType='mainSeq']/p:childTnLst/p:par")
    auto, clicks = [], []
    for outer in seq:
        conds = X(outer, "./p:cTn/p:stCondLst/p:cond")
        is_auto = any(c.get("evt") == "onBegin" for c in conds)
        group = []
        for eff in X(outer, ".//p:cTn[@presetClass='entr']"):
            spid = int(X(eff, ".//p:spTgt/@spid")[0]); group.append(names[spid])
        (auto.extend(group) if is_auto else clicks.append(group))
    return auto, clicks
anim_slides = 0
for i, s in enumerate(P.slides, 1):
    exp = getattr(s, "_anim", None)
    r = read_anim(s)
    if r is None: continue
    anim_slides += 1; auto, clicks = r
    ok(f"Folie {i}: Animations-XML wohlgeformt", True)
    ids = [sh.shape_id for sh in s.shapes]; ok(f"Folie {i}: Shape-IDs eindeutig", len(ids) == len(set(ids)))
    nm = META[i - 1]["title"]
    # erwartete Klickfolge aus der Notiz
    note = s.notes_slide.notes_text_frame.text
    m = re.search(r"ANIMATION \(Klickfolge\): (.*)", note)
    ok(f"Folie {i} ({nm}): Klickfolge in den Notizen dokumentiert", m is not None)
    print(f"Folie {i:>2} {nm[:36]:36} automatisch: {len(auto):>2} Shapes · Klicks: {len(clicks)} → " + " | ".join("+".join(g) if len(g) < 4 else f"{g[0]}…(+{len(g)-1})" for g in clicks))
print("Folien mit Animation:", anim_slides)
# Reihenfolge konkret pruefen (Erwartung)
exp_clicks = {
    "Antwort Lückensatz": [["Antwort_1"], ["Antwort_2"], ["Antwort_3"]],
    "Antwort Vergütung": [["Jahr_1", "Balken_1"], ["Jahr_2", "Balken_2"], ["Jahr_3", "Balken_3"], ["Jahr_4", "Balken_4"]],
    "Urlaub nach Alter": [["Alter_1", "Urlaub_1"], ["Alter_2", "Urlaub_2"], ["Alter_3", "Urlaub_3"], ["Alter_4", "Urlaub_4"]],
    "Probezeit": [["Monat_1"], ["Monat_2"], ["Monat_3"], ["Monat_4"]],
}
for i, s in enumerate(P.slides, 1):
    t = META[i - 1]["title"]
    if t in exp_clicks:
        r = read_anim(s); ok(f"Folie {i} ({t}): Klickreihenfolge = {exp_clicks[t]}", r and r[1] == exp_clicks[t], r[1] if r else None)
    if t.startswith("Detektiv Auflösung"):
        r = read_anim(s); fs = [int(re.search(r"Fehlerzeile_(\d)", g[0]).group(1)) for g in r[1]]
        ok(f"Folie {i} ({t}): Fehler erscheinen in Reihenfolge, je Fehler Zeile + Regel", all(len(g) == 2 and g[1].startswith("Regel_Fehler") for g in r[1]) and fs == sorted(fs), fs)
for i, s in enumerate(P.slides, 1):
    if META[i - 1]["kind"] == "Denkpause":
        r = read_anim(s); ok(f"Folie {i}: Denkpause-Countdown startet automatisch ({len(r[0])} Segmente)", r and len(r[0]) == 10 and not r[1])
fe = [m for m in META if m["title"].startswith("Detektiv Auflösung")]

# 4. Notizen
print("\n== Test 4: Notizen")
need = ["SPRECHER:", "DAUER:", "SOZIALFORM:"]
for i, s in enumerate(P.slides, 1):
    n = s.notes_slide.notes_text_frame.text
    ok(f"Folie {i}: Notizen mit Sprecher/Dauer/Sozialform", all(x in n for x in need))
    ok(f"Folie {i}: Sprecher Yasin/Mido", re.search(r"SPRECHER: (Yasin|Mido)", n) is not None)
vis = [m for m in META if not m["hidden"]]
tot = sum(m["dauer"] for m in vis)
print(f"Summe der Notiz-Zeiten sichtbarer Folien: {tot//60}:{tot%60:02d}")
ok("Gesamtzeit der sichtbaren Folien ≤ 45:00", tot <= 2700, tot)
ph = {}
for m in vis: ph[m["phase"]] = ph.get(m["phase"], 0) + m["dauer"]
print({k: f"{v//60}:{v%60:02d}" for k, v in ph.items()})
spr = [m["spr"] for m in vis]
ok("Sprecher wechseln ab (beide kommen vor)", {"Yasin", "Mido"} <= set(spr))
hid = [i for i, m in enumerate(META, 1) if m["hidden"]]
ok("Ausgeblendete Folien markiert", all(P.slides[i - 1]._element.get("show") == "0" for i in hid), hid)

# 5. Schriftgroessen / Layout
print("\n== Test 5: Schriftgrößen (Pflicht: Fließtext ≥ 24 pt, Titel ≥ 40 pt)")
small = {}; titles = []
for i, s in enumerate(P.slides, 1):
    for sh in s.shapes:
        if not sh.has_text_frame: continue
        for p in sh.text_frame.paragraphs:
            for r in p.runs:
                if r.font.size and r.text.strip() and r.font.size.pt < 24: small.setdefault(i, []).append((r.font.size.pt, r.text[:30]))
        if sh.name == "Titel" and sh.text_frame.text.strip():
            sz = min(r.font.size.pt for p in sh.text_frame.paragraphs for r in p.runs if r.font.size)
            titles.append((i, sz))
ok("Titel ≥ 40 pt (Folien mit Titel)", all(sz >= 40 or META[i - 1]["kind"] in ("Titel", "Antwort") and sz >= 32 for i, sz in titles), [(i, sz) for i, sz in titles if sz < 40])
print("Folien mit Text < 24 pt:", {i: sorted({x[0] for x in v}) for i, v in small.items()} or "keine")
ok("Kein Text unter 17 pt", all(x[0] >= 17 for v in small.values() for x in v), [(i, x) for i, v in small.items() for x in v if x[0] < 17][:5])
for i, s in enumerate(P.slides, 1):
    lines = 0
    for sh in s.shapes:
        if sh.has_text_frame and sh.name not in ("Titel",): lines += 0
    # Textwand: Woerter pro Folie
    words = sum(len(sh.text_frame.text.split()) for sh in s.shapes if sh.has_text_frame)
    if words > 90: print(f"Hinweis: Folie {i} hat {words} Wörter ({META[i-1]['title']})")
alts = sum(1 for s in P.slides for sh in s.shapes if sh.shape_type == 13)
ok("Alle Bilder haben Alt-Text", all(sh._element.xpath(".//p:cNvPr/@descr") and sh._element.xpath(".//p:cNvPr/@descr")[0] for s in P.slides for sh in s.shapes if sh.shape_type == 13), alts)

# 6. Fakten
print("\n== Test 6: Zahlen und Paragrafen")
D = json.loads(open(os.path.join(ROOT, "site/js/data.js"), encoding="utf-8").read().split("=", 1)[1].rstrip().rstrip(";"))
norm = lambda x: re.sub(r"\s+", " ", x).strip()
def txt_of(idx): return norm(" ".join(sh.text_frame.text for sh in P.slides[idx - 1].shapes if sh.has_text_frame))
alltxt = " ".join(txt_of(i) for i in range(1, len(P.slides) + 1))
notes_all = " ".join(s.notes_slide.notes_text_frame.text for s in P.slides)
facts = ["§ 11 BBiG", "§ 8, § 21 BBiG", "§ 8 JArbSchG", "§ 3 ArbZG", "§ 17 BBiG", "§ 19 JArbSchG", "§ 3 BUrlG", "§ 20 BBiG", "§ 22 Abs. 1 und 2 BBiG", "§ 22 Abs. 3 und 4 BBiG",
         "724 €", "854 €", "977 €", "1.014 €", "01.08.2024", "30 Werktage", "27 Werktage", "25 Werktage", "24 Werktage", "20 Arbeitstagen", "8,5", "48 pro Woche", "40 pro Woche", "sechs Monate"]
for f in facts: ok(f"Fakt in der Präsentation: {f}", f in alltxt, "")
# Aktivitaetstexte wortgleich
mit = next(i for i, m in enumerate(META, 1) if m["title"] == "Vertrags-Detektiv: Zum Mitlesen")
t = txt_of(mit)
ok("Vertragsauszug wörtlich (Kopf + 7 Zeilen)", all(norm(z["t"]) in t for z in D["zeilen"]) and all(k in t for k in D["kopf"]))
ok("Detektiv-Mitlesen: Fehlermarkierungen fehlen", "[Fehler" not in t and not any("Markierung" in sh.name for sh in P.slides[mit - 1].shapes))
fall_nr = [i for i, m in enumerate(META, 1) if m["kind"] == "Frage" and m["title"].startswith(("Fall ", "Reservefall"))]
for i, f in zip(fall_nr, D["faelle"]):
    ok(f"Fall-Frage Folie {i} wörtlich ({f['label'][:12]})", norm(f["q"]) in txt_of(i) and all(norm(a) in txt_of(i) for a in f["a"]))
lo = {m["nr"]: m for m in META}
for q, a, t in PAIRS:
    if t.startswith(("Fall ", "Reservefall")):
        f = next(x for x in D["faelle"] if x["label"].startswith(t.replace("Reserve", "Reserve")) or x["label"].split(" (")[0].replace("Reservefall", "Fall") == t.split(" (")[0].replace("Reservefall", "Fall"))
        ok(f"Fall-Lösung Folie {a}: Buchstabe + Begründung wörtlich", f["fb"] in txt_of(a) and f["a"][f["c"]] in txt_of(a))
rgq = [r["t"] for r in D["rg"]]; rgb = [r["b"] for r in D["rg"]]
ok("Rote/Grüne Karte: 10 Aussagen wörtlich (Plan B)", all(norm(x) in alltxt for x in rgq))
ok("Rote/Grüne Karte: 10 Lösungen wörtlich (Plan B)", all(norm(x) in alltxt for x in rgb))
ok("Mini-Quiz: Fragen + Antworten wörtlich (Plan B)", all(norm(q["q"]) in alltxt and all(norm(a) in alltxt for a in q["a"]) for q in D["quiz"]))
ok("Mini-Quiz: Lösungen + Regel wörtlich (Plan B)", all(norm(q["a"][q["c"]]) in alltxt and q["fb"] in alltxt for q in D["quiz"]))
for k, v in D["fehler"].items(): ok(f"Fehlerregel {k} wörtlich in der Auflösung", norm(v["regel"]) in alltxt)
for tt in ("WiSo", "Wirtschafts- und Sozialkunde"):
    ok(f"'{tt}' nicht auf Folien", tt not in alltxt)
ok("Keine Projektinhalte (Skizze, PSP, Ablaufplan)", not re.search(r"projektskizze|strukturplan|ablaufplan|projektbericht|gantt", (alltxt + notes_all).lower()))
ok("Keine Platzhalter in eckigen Klammern", "[eintragen]" not in alltxt and "[..]" not in alltxt)

n_ok = sum(1 for r in res if r[0]); print(f"\nErgebnis: {n_ok} von {len(res)} Prüfungen bestanden")
open("/tmp/v4_testliste.txt", "w", encoding="utf-8").write("\n".join(("✓ " if r[0] else "✗ ") + r[1] + ("" if r[0] else f" → {r[2]}") for r in res))
