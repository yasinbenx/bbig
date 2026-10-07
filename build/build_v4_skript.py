# -*- coding: utf-8 -*-
import os, sys, re, subprocess
sys.path.insert(0, os.path.dirname(__file__))
from html import escape as esc
from extract_deck import load
from skript_data import S
from playwright.sync_api import sync_playwright
OUT = os.path.join(os.path.dirname(__file__), "..", "output", "v4")
os.makedirs(OUT, exist_ok=True)
D = load()
PH = ["Einstieg", "Fragerunde", "Erklären", "Aufgaben", "Besprechen", "Quiz & Abschluss"]
def mmss(s): return f"{s//60}:{s%60:02d}"
vis = [d for d in D if not d["hidden"]]
ph_sum = {p: sum(d["dauer"] for d in vis if d["phase"] == p) for p in PH}
total = sum(ph_sum.values())
by_spr = {}
for d in vis: by_spr.setdefault(d["spr"], []).append(d)
HINWEISE = [
 ("Rollen", [f"Es spricht immer die Person, die im Skript bei der Folie steht (Yasin {len(by_spr['Yasin'])} sichtbare Folien, Mido {len(by_spr['Mido'])}). Die andere Person ist dann Co-Moderation: Tafel beschriften, Stoppuhr, Technik, Zurufe sammeln.",
   "Geklickt wird von der sprechenden Person, ein Klick pro Hinweis „Klick n“ im Skript. Den Klicker oder die Pfeiltaste vorher gemeinsam testen.",
   "Folienwechsel mit dem Übergangssatz ankündigen; bei Sprecherwechsel kurz zum Partner schauen."]),
 ("Material und Raum", ["Laptop mit Beamer und die Datei praesentation_unterricht_v4.pptx im Präsentationsmodus (versteckte Folien 23–27 bleiben unsichtbar, bis sie bewusst angesprungen werden).",
   "Merkblatt ausgedruckt für alle, Stoppuhr, Tafel oder Flipchart mit vier Spalten a–d vorbereiten (für Folie 3 und Folie 20).",
   "Handy-Empfang oder WLAN im Raum vorher prüfen; QR-Code und Adresse der Website einmal testen. Papier für Plan B (A–D-Zettel) bereithalten.",
   "Den QR-Code auf Folie 13 etwa 20 Sekunden stehen lassen."]),
 ("Stille aushalten", ["Nach jeder Frage 5 bis 7 Sekunden warten, bevor jemand nachhilft. Stille heißt: Die Klasse denkt.",
   "Während der Arbeitsphase (Folie 14) und des Mini-Quiz (Folie 21) wird nicht gesprochen und nicht geklickt; Yasin geht durch die Reihen.",
   "Zahlen bei Handzeichen aufschreiben, nicht kommentieren."]),
 ("Falsche Antworten", ["Nie bloßstellen: erst nachfragen „Wie kommst du darauf?“, dann die Regel mit Paragraf nennen.",
   "In der Fragerunde (Folie 3) wird noch nichts korrigiert; die Auflösung kommt erst auf Folie 20.",
   "Bei Handzeichen-Fällen eine Begründung erfragen, bevor der Klick die Lösung zeigt.",
   "Wenn niemand antwortet: die Frage anders formulieren oder eine Antwortoption vorlesen."]),
 ("Zeit", [f"Geplant sind {mmss(total)} Minuten; bis 45 Minuten bleibt Puffer. Bei Zeitnot zuerst Fall B und Fall C streichen (Folien 18, 19), dann die Arbeitsphase auf 9 Minuten kürzen.",
   "Die Zeiten im Skript sind Richtwerte. Der Sprechtext füllt je Folie nur etwa 60–80 % der Zeit; der Rest ist für Pausen, Zeigen auf der Folie und Rückfragen.",
   "Die versteckten Folien 23–27 (Plan B) sind nicht in den Zeiten enthalten und nur bei Ausfall von Internet oder Handys zu zeigen."]),
]

# ---- Abgleich mit der pptx ----
dev = []
for d in D:
    s = S[d["nr"]]; txt = " ".join(d["texts"]) + " " + d["notes"]
    paras = set(re.findall(r"§§? ?\d+[a-z]?(?:[–-]\d+)?", " ".join(s["text"])))
    for p in sorted(paras):
        num = re.search(r"\d+", p).group()
        if num not in txt: dev.append(f"Folie {d['nr']}: {p} im Skript, aber nicht auf Folie/Notiz")
    nclicks = len(d["clicks"])
    sc = sum(1 for k in s["klicks"] if k.startswith("Klick"))
    if nclicks != sc: dev.append(f"Folie {d['nr']}: {sc} Klickhinweise im Skript, {nclicks} Klicks in der Folie")
    if d["nr"] == 14 and len(d["auto"]) != 12: dev.append("Folie 14: Countdown nicht 12 Segmente")
    for z in re.findall(r"\b\d{1,2}(?:\.\d{3})? ?(?:Euro|Monate|Werktage|Stunden)", " ".join(s["text"])): pass
print("Abweichungen automatisch:", dev or "keine")
# bewusste, dokumentierte Abweichungen/Hinweise
NOTES_DEV = [
 "Folie 5, 9, 11, 20, 22: In der pptx-Notiz steht „nicht streichbar“ bzw. „kürzbar auf …“. Das Skript übernimmt das („Nein, aber auf … kürzbar“). Streichbar sind nur Folie 18 und 19 (und die Arbeitsphase teilweise).",
 "Folie 12: Notiz sagt „nicht streichbar“; das Skript empfiehlt nur bei äußerster Zeitnot, die Spalten ohne Aufzählung zu nennen. Das ist ein Hinweis, keine Änderung der Folie.",
 "Folie 1: Die pptx-Notiz nennt „Begrüßen, Rollen klären“; das Skript fasst das in einem Satz zusammen.",
 "Folie 17: Die Folie fragt „Welche Aussage ist richtig?“; das Skript liest zusätzlich die Antworten A–D vor. Das ist Sprechtext, die Folie bleibt unverändert.",
 "Folie 23–27: Die Notiz gibt als Dauer „Reserve (nicht in den 45 Minuten)“ an; das Skript führt dafür keine Minutenzahl und rechnet sie nicht in die Gesamtzeit ein.",
 "Bei Folie 16 steht in der pptx-Notiz der Hinweis auf das Geburtsdatum (20.11.2009); das Skript nennt ihn bei Fehler 3 (Klick 3). Der Auszug nennt als Ausbildungsbeginn 01.09.2026, bei dem Jonas 16 Jahre alt ist.",
]
if not dev: dev_text = "Automatischer Abgleich: Alle Paragrafen im Skript kommen auf der jeweiligen Folie oder in ihrer Notiz vor; Klickanzahl (Folie 14: 12 Countdown-Segmente automatisch; 16: 5 Klicks; 17–19: je 2; 20: 4) und Dauern stimmen mit der pptx überein."
else: dev_text = "Automatischer Abgleich fand: " + "; ".join(dev)

CSS = """
@page { size: A4; margin: 15mm 15mm 17mm 18mm; }
*{box-sizing:border-box} body{font-family:'Liberation Sans',Arial,sans-serif;color:#1A2238;font-size:10.5pt;line-height:1.45}
h1{font-size:22pt;color:#14264B;margin:0 0 2mm} .sub{color:#5B6680;margin-bottom:6mm}
.bar{height:2mm;background:#F5A800;width:30mm;margin:3mm 0 5mm}
.entry{border:.3mm solid #C9CFDD;border-radius:2mm;margin:0 0 5mm;break-inside:avoid-page;overflow:hidden}
.eh{background:#14264B;color:#fff;padding:2.2mm 4mm;display:flex;gap:3mm;align-items:baseline}
.eh .n{background:#F5A800;color:#14264B;font-weight:700;border-radius:1.2mm;padding:0 2mm}
.eh .t{font-weight:700;font-size:11.5pt;flex:1}
.eh .m{font-size:9pt;color:#DCE3F2}
.meta{background:#F6F8FC;padding:1.6mm 4mm;font-size:9pt;color:#44506A;display:flex;flex-wrap:wrap;gap:1mm 5mm;border-bottom:.3mm solid #E3E7F0}
.hid{background:#FFF1CC;color:#7A5200;font-weight:700;padding:0 1.5mm;border-radius:1mm}
.eb{padding:3mm 4mm}
.lbl{font-size:8pt;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:#9A6A00;margin:2mm 0 .5mm}
.eb p{margin:0 0 2mm}
.say p{font-size:10.8pt}
.clk{background:#E8EEF9;border-left:1.2mm solid #22386B;padding:1.2mm 3mm;margin:1mm 0;font-size:9.5pt}
.q{background:#FFF9E8;border-left:1.2mm solid #F5A800;padding:2mm 3mm;margin-top:2mm;font-size:9.5pt}
.q b{color:#14264B}
.ue{font-style:italic;color:#44506A;margin-top:2mm;font-size:9.8pt}
table{width:100%;border-collapse:collapse;margin:3mm 0}th{background:#14264B;color:#fff;text-align:left;padding:2mm 3mm}td{padding:2mm 3mm;border-bottom:.3mm solid #D5D9E3}
td.r,th.r{text-align:right} tr.tot td{font-weight:700;background:#FFF1CC}
h2{color:#14264B;font-size:14pt;margin:5mm 0 2mm} ul{margin:0 0 3mm 5mm} li{margin-bottom:1.3mm}
.pb{break-before:page}
"""
def entry_html(d):
    s = S[d["nr"]]
    dur = mmss(d["dauer"]) + " Min." if d["dauer"] else "Reserve (nicht in den 39:45)"
    h = f'<div class="entry"><div class="eh"><span class="n">{d["nr"]}</span><span class="t">{esc(s["titel"])}</span><span class="m">{esc(d["phase"])} · {esc(d["spr"])} · {dur}</span></div>'
    meta = [f"Sprecher: <b>{esc(d['spr'])}</b>", f"Sozialform: {esc(d['sozial'])}", f"Streichbar: <b>{esc(s['streich'])}</b>"]
    if d["hidden"]: meta.insert(0, '<span class="hid">VERSTECKTE FOLIE · Plan B</span>')
    h += '<div class="meta">' + " · ".join(meta) + "</div><div class='eb'>"
    h += '<div class="lbl">Sprechtext</div><div class="say">' + "".join(f"<p>{esc(t)}</p>" for t in s["text"]) + "</div>"
    if s["klicks"]:
        h += '<div class="lbl">Klickhinweise</div>' + "".join(f'<div class="clk">{esc(k)}</div>' for k in s["klicks"])
    if s.get("extra"): h += f'<div class="lbl">Merken</div><p>{esc(s["extra"])}</p>'
    if s["frage"]:
        f = s["frage"]
        h += f'<div class="q"><div class="lbl" style="margin-top:0">Frage an die Klasse</div><b>{esc(f["frage"])}</b><br>Sozialform: {esc(f["sozial"])}<br><b>Erwartete Antworten:</b> {esc(f["erw"])}<br><b>Typische Fehlvorstellungen:</b> {esc(f["fehl"])}<br><b>Reaktion:</b> {esc(f["reakt"])}</div>'
    h += f'<div class="ue"><b>Überleitung:</b> {esc(s["uebergang"])}</div></div></div>'
    return h
body = '<h1>Sprechskript zur Unterrichtsstunde</h1><div class="bar"></div><div class="sub">„Rechte und Pflichten aus dem Ausbildungsvertrag“ · Fach GP · Yasin &amp; Mido · Präsentation 08.10.2026<br>Zu praesentation_unterricht_v4.pptx: 27 Folien (22 sichtbar, 5 versteckt). Nur für uns, nicht zum Verteilen. Text in eckigen Klammern ist Regieanweisung, nicht Sprechtext.</div>'
for d in D:
    if d["nr"] == 23: body += '<div class="pb"></div><h2>Versteckte Folien (Plan B, nur bei Ausfall von Internet oder Handys)</h2>'
    body += entry_html(d)
rows = "".join(f"<tr><td>{p}</td><td class='r'>{mmss(ph_sum[p])}</td><td>{', '.join(str(d['nr']) for d in vis if d['phase']==p)}</td></tr>" for p in PH)
body += f'<div class="pb"></div><h2>Zeitübersicht</h2><table><tr><th>Phase</th><th class="r">Dauer (Min.)</th><th>Folien</th></tr>{rows}<tr class="tot"><td>Gesamt (sichtbare Folien 1–22)</td><td class="r">{mmss(total)}</td><td>Puffer bis 45:00: {mmss(2700-total)}</td></tr></table>'
spr_rows = "".join(f"<tr><td>{k}</td><td class='r'>{len(v)}</td><td class='r'>{mmss(sum(d['dauer'] for d in v))}</td></tr>" for k, v in by_spr.items())
body += f'<table><tr><th>Sprecher</th><th class="r">Folien (sichtbar)</th><th class="r">Zeit (Min.)</th></tr>{spr_rows}</table>'
body += '<p>Streichbar bei Zeitnot: Folie 18 (Fall B) und 19 (Fall C) je 1:10; Arbeitsphase auf 9 Minuten kürzbar (−3:00). Kürzbar: Folie 5 auf 50 s, 9 auf 35 s, 11 auf 45 s, 20 auf 50 s.</p>'
body += '<div class="pb"></div><h1 style="font-size:20pt">Hinweise für uns</h1><div class="bar"></div>'
for t, items in HINWEISE: body += f"<h2>{t}</h2><ul>" + "".join(f"<li>{esc(i)}</li>" for i in items) + "</ul>"
body += f'<div class="pb"></div><h1 style="font-size:20pt">Abgleich mit der Präsentation</h1><div class="bar"></div><p>{esc(dev_text)}</p><h2>Bewusste Abweichungen und Hinweise</h2><ul>' + "".join(f"<li>{esc(x)}</li>" for x in NOTES_DEV) + "</ul>"
html = f'<!doctype html><html lang="de"><head><meta charset="utf-8"><title>Sprechskript v4</title><style>{CSS}</style></head><body>{body}</body></html>'
hp = os.path.join(OUT, "_skript.html"); open(hp, "w", encoding="utf-8").write(html)
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome", args=["--no-sandbox"]); pg = b.new_page()
    pg.goto("file://" + os.path.abspath(hp)); pg.wait_for_timeout(300)
    pg.pdf(path=os.path.join(OUT, "sprechskript_v4.pdf"), prefer_css_page_size=True, print_background=True, display_header_footer=True,
           header_template="<span></span>", footer_template='<div style="font-size:8px;width:100%;padding:0 18mm;color:#5B6680;display:flex;justify-content:space-between"><span>Sprechskript v4 · Yasin &amp; Mido · nur für uns</span><span>Seite <span class="pageNumber"></span> / <span class="totalPages"></span></span></div>')
    b.close()
os.remove(hp)

# ---- DOCX ----
sys.path.insert(0, os.path.dirname(__file__))
from docxlib import shade, cell_margins, cell_borders, fix_widths, run, para, new_doc, footer
from docx.shared import Pt, Cm
doc, sec = new_doc()
para(doc, "SPRECHSKRIPT · FACH GP", 9, True, "F5A800")
para(doc, "Sprechskript zur Unterrichtsstunde", 22, True, "14264B", after=2)
para(doc, "„Rechte und Pflichten aus dem Ausbildungsvertrag“ · Yasin & Mido · Präsentation 08.10.2026. Zu praesentation_unterricht_v4.pptx (27 Folien, davon 5 versteckt). Eckige Klammern = Regieanweisung.", 9.5, color="5B6680", after=8)
def lab(c, t): para(c, t.upper(), 7.5, True, "9A6A00", after=1, before=3)
for d in D:
    s = S[d["nr"]]
    if d["nr"] == 23: para(doc, "Versteckte Folien (Plan B, nur bei Ausfall von Internet oder Handys)", 13, True, "14264B", before=10, after=4)
    t = doc.add_table(rows=3, cols=1); fix_widths(t, [17])
    dur = mmss(d["dauer"]) + " Min." if d["dauer"] else "Reserve (nicht in den 39:45)"
    c0, c1, c2 = t.rows[0].cells[0], t.rows[1].cells[0], t.rows[2].cells[0]
    shade(c0, "14264B"); shade(c1, "F6F8FC")
    for c in (c0, c1, c2):
        cell_margins(c, 70, 70, 140, 140); cell_borders(c, top=(4, "C9CFDD"), bottom=(4, "C9CFDD"), left=(4, "C9CFDD"), right=(4, "C9CFDD"))
    p = c0.paragraphs[0]; run(p, f"Folie {d['nr']}  ", 11, True, "F5A800"); run(p, s["titel"], 11, True, "FFFFFF"); run(p, f"   {d['phase']} · {d['spr']} · {dur}", 8.5, False, "DCE3F2")
    p = c1.paragraphs[0]; run(p, ("VERSTECKTE FOLIE (Plan B) · " if d["hidden"] else "") + f"Sprecher: {d['spr']} · Sozialform: {d['sozial']} · Streichbar: {s['streich']}", 8.5, False, "44506A")
    c2.paragraphs[0].paragraph_format.space_after = Pt(0)
    lab(c2, "Sprechtext")
    for tx in s["text"]: para(c2, tx, 10.5, after=3)
    if s["klicks"]:
        lab(c2, "Klickhinweise")
        for k in s["klicks"]: para(c2, "▸ " + k, 9.5, color="22386B", after=1)
    if s.get("extra"): lab(c2, "Merken"); para(c2, s["extra"], 9.5)
    if s["frage"]:
        f = s["frage"]; lab(c2, "Frage an die Klasse")
        para(c2, f["frage"], 10, True, "14264B", after=1)
        for k, v in (("Sozialform", f["sozial"]), ("Erwartete Antworten", f["erw"]), ("Typische Fehlvorstellungen", f["fehl"]), ("Reaktion", f["reakt"])):
            p = para(c2, "", after=1); run(p, k + ": ", 9.5, True); run(p, v, 9.5)
    p = para(c2, "", after=2, before=3); run(p, "Überleitung: ", 9.5, True, "44506A"); run(p, s["uebergang"], 9.5, False, "44506A", italic=True)
    para(doc, "", 4, after=4)
doc.add_page_break()
para(doc, "Zeitübersicht", 16, True, "14264B", after=4)
t = doc.add_table(rows=1, cols=3); fix_widths(t, [6, 3, 8])
for c, h in zip(t.rows[0].cells, ("Phase", "Dauer (Min.)", "Folien")): shade(c, "14264B"); run(c.paragraphs[0], h, 10, True, "FFFFFF")
for p_ in PH + ["Gesamt"]:
    r = t.add_row(); vals = (p_, mmss(ph_sum[p_]) if p_ != "Gesamt" else mmss(total), ", ".join(str(d["nr"]) for d in vis if d["phase"] == p_) if p_ != "Gesamt" else f"Puffer bis 45:00: {mmss(2700-total)}")
    for c, v in zip(r.cells, vals):
        run(c.paragraphs[0], v, 10, p_ == "Gesamt")
        if p_ == "Gesamt": shade(c, "FFF1CC")
fix_widths(t, [6, 3, 8])
para(doc, "", after=4)
for k, v in by_spr.items(): para(doc, f"{k}: {len(v)} sichtbare Folien, {mmss(sum(d['dauer'] for d in v))} Min.", 10, after=1)
para(doc, "Streichbar bei Zeitnot: Folie 18 und 19 (je 1:10); Arbeitsphase auf 9 Min. kürzbar (−3:00). Kürzbar: Folie 5 auf 50 s, 9 auf 35 s, 11 auf 45 s, 20 auf 50 s.", 10, before=6)
doc.add_page_break()
para(doc, "Hinweise für uns", 18, True, "14264B", after=4)
for tt, items in HINWEISE:
    para(doc, tt, 12, True, "14264B", before=6, after=2)
    for i in items: para(doc, "• " + i, 10, after=2)
doc.add_page_break()
para(doc, "Abgleich mit der Präsentation", 18, True, "14264B", after=4)
para(doc, dev_text, 10, after=6)
para(doc, "Bewusste Abweichungen und Hinweise", 12, True, "14264B", after=2)
for x in NOTES_DEV: para(doc, "• " + x, 10, after=2)
footer(doc.sections[0], "Sprechskript v4 · Yasin & Mido · nur für uns")
doc.save(os.path.join(OUT, "sprechskript_v4.docx"))
print("ok", total, ph_sum)
