# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from html import escape as esc
from docxlib import *
from plan4 import *
from playwright.sync_api import sync_playwright
OUTD = os.path.join(os.path.dirname(__file__), "..", "output", "v4")
# ================================================================= A) Checkliste (PDF)
box = '<span style="display:inline-block;width:3.6mm;height:3.6mm;border:.4mm solid #14264B;margin-right:2.2mm;vertical-align:-.5mm;flex:none"></span>'
def cl(items): return "".join(f'<div style="display:flex;margin-bottom:1.5mm">{box}<div>{x}</div></div>' for x in items)
def sec_(t, body): return f'<h2>{esc(t)}</h2>{body}'
NACH = [
 "<b>Skizze:</b> Klasse eintragen und Druckmenge/Drucker klären (Punkt 2 und 7, jeweils als [Platzhalter] markiert).",
 f"<b>Ablaufplan:</b> Termin für AP 5.3 (Evaluation, Reflexion, Projektbericht) bei der Lehrkraft erfragen und eintragen (steht als [laut Lehrkraft]).",
 "<b>Ist-Termine</b> der Arbeitspakete notieren (wann wurde wirklich gearbeitet?) für den Soll-Ist-Vergleich im Projektbericht.",
 "<b>Protokolle:</b> echte Besprechungen mit echtem Datum protokollieren. Die drei Beispielprotokolle sind nur Muster und dürfen nicht als echte Protokolle abgegeben werden.",
 "<b>Am 08.10.2026 notieren:</b> Handzeichen-Ergebnis des Mini-Quiz (5 / 4 / 3 / weniger) und die Stimmen aus dem Blitzlicht (Folie 22) für die Evaluation.",
 "<b>Projektbericht</b> schreiben (Gliederung: projektbericht_gliederung_v4); selbst auszufüllen: Soll-Ist-Vergleich, Probleme, Feedback der Klasse, Reflexion.",
 "<b>Anhang</b> zusammenstellen und ausdrucken (Anhangsverzeichnis in der Gliederung).",
 "<b>Website:</b> nur online lassen, wenn Lehrkraft und Klasse einverstanden sind; sie enthält keine personenbezogenen Daten. Wird sie offline genommen, QR-Code und Hinweise auf Folien 13, 14, 21 anpassen.",
 "<b>Offene Frage:</b> Verlangt die Lehrkraft Skizze, PSP und Ablaufplan als Folien in der Präsentation? Die finale Präsentation enthält sie nicht (bewusst nicht verändert).",
]
DRUCK = [("merkblatt_v4.pdf", "1 Seite A4", "für alle in der Klasse: [Klassenstärke] + Reserve"),
         ("booklet_v4.pdf", "16 Seiten A4, Farbe, doppelseitig", "optional: 1 Exemplar Lehrkraft + [Anzahl]; Rest digital über QR/Website"),
         ("sprechskript_v4.pdf", "21 Seiten, nur für uns", "2 Exemplare (je Person eines); Plan-B-Seiten optional"),
         ("projektskizze_v4.pdf, projektstrukturplan_v4.pdf, projektablaufplan_v4.pdf", "Abgabe an die Lehrkraft", "je 1 Exemplar (PSP/Ablaufplan querformat)"),
         ("leere Zettel A–D", "Plan B (Folie 26)", "ein paar Blätter bereithalten, nicht vorher ausdrucken")]
PROBE = ["<b>Beamer/Laptop:</b> Datei praesentation_unterricht_v4.pptx im Präsentationsmodus öffnen, Auflösung und Ton prüfen; Ladegerät dabei.",
 "<b>Animationsreihenfolge:</b> Folie 14 (Countdown startet automatisch, 12 Segmente), Folie 16 (5 Klicks), Folien 17–19 (je 2 Klicks), Folie 20 (4 Klicks) einmal komplett durchklicken.",
 "<b>Klicker/Pfeiltaste</b> getestet; Zurück-Taste ausprobiert.",
 "<b>WLAN und Handys:</b> Empfang im Raum prüfen; Website öffnet sich mit dem Handy.",
 "<b>QR-Code:</b> mit zwei Handys vom Beamer und vom Merkblatt scannen; Adresse yasinbenx.github.io/azubi-vertrag öffnet sich.",
 "<b>Website erreichbar:</b> Rote/Grüne Karte, Vertrags-Detektiv, Fälle A–E, Mini-Quiz laden und funktionieren.",
 "<b>Stoppuhr</b> bereit (Arbeitsphase 12 Minuten, Quiz ca. 3 Minuten); Zeit ansagen nach 3, 8 und 12 Minuten.",
 "<b>Plan B:</b> versteckte Folien 23–27 gefunden und angesprungen (Folie anwählen); Zettel liegen bereit.",
 "<b>Tafel/Flipchart:</b> vier Spalten a–d beschriftet (Folien 3 und 20), Stifte funktionieren.",
 "<b>Wer sagt was:</b> Sprecherwechsel laut Sprechskript durchgehen (Yasin 15 Folien, Mido 7); Zeit mit Stoppuhr mitlaufen lassen (Ziel 39:45, Puffer bis 45:00).",
 "<b>Merkblätter</b> ausgedruckt und vorsortiert; Sprechskript in Papierform dabei."]
OFFEN = ["Klasse (Skizze, Punkt 2) und Druckmengen (Punkt 7) sind noch Platzhalter.",
 "Termin für AP 5.3 und Abgabetermin Projektbericht stehen bei der Lehrkraft.",
 "Bewertungsbogen (19 Kriterien × 4 Punkte) lag mir nicht im Wortlaut vor; die Berichtsgliederung nutzt die bekannten Kriterien als Hinweise. Bitte mit dem Bogen abgleichen.",
 "Ist-Termine, Probleme, Feedback und Reflexion können nur ihr beschreiben."]
html_a = f"""<!doctype html><html lang="de"><head><meta charset="utf-8"><style>
@page{{size:A4;margin:13mm 15mm 14mm 17mm}} body{{font-family:'Liberation Sans',Arial,sans-serif;font-size:9.8pt;color:#1A2238;line-height:1.4}}
h1{{font-size:20pt;color:#14264B}} .bar{{width:24mm;height:1.5mm;background:#F5A800;margin:1.5mm 0 3mm}} h2{{font-size:12.5pt;color:#14264B;margin:4.5mm 0 2mm;border-bottom:.4mm solid #F5A800;padding-bottom:.6mm}}
table{{border-collapse:collapse;width:100%}} th{{background:#14264B;color:#fff;text-align:left;padding:1.3mm 2mm;font-size:9pt}} td{{padding:1.2mm 2mm;border-bottom:.25mm solid #D5D9E3;vertical-align:top;font-size:9.2pt}} .pb{{break-before:page}} li{{margin:0 0 1.2mm 4mm}}</style></head><body>
<h1>Nacharbeiten und Checklisten</h1><div class="bar"></div><p style="color:#5B6680;margin-bottom:1mm">Rechte und Pflichten aus dem Ausbildungsvertrag · Yasin &amp; Mido · Präsentation 08.10.2026</p>
{sec_("1 Das müssen nur wir erledigen", cl(NACH))}
{sec_("2 Druckliste", "<table><tr><th>Datei</th><th>Format</th><th>Menge / Hinweis</th></tr>" + "".join(f"<tr><td><b>{esc(a)}</b></td><td>{esc(b)}</td><td>{esc(c)}</td></tr>" for a, b, c in DRUCK) + "</table>")}
<div class="pb"></div>{sec_("3 Probelauf-Checkliste (heute Abend, 07.10.2026)", cl(PROBE))}
{sec_("4 Offene Punkte", "<ul>" + "".join(f"<li>{esc(x)}</li>" for x in OFFEN) + "</ul>")}
</body></html>"""
hp = os.path.join(OUTD, "_c.html"); open(hp, "w", encoding="utf-8").write(html_a)
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome", args=["--no-sandbox"]); pg = b.new_page(); pg.goto("file://" + os.path.abspath(hp))
    pg.pdf(path=os.path.join(OUTD, "nacharbeiten_checkliste.pdf"), prefer_css_page_size=True, print_background=True); b.close()
os.remove(hp)

# ================================================================= B) Protokoll-Vorlage
doc, sec = new_doc(); sec.top_margin = Cm(1.3); sec.bottom_margin = Cm(1.4)
def kv(rows):
    t = doc.add_table(rows=len(rows), cols=2)
    for i, (k, v, h) in enumerate(rows):
        a, b = t.rows[i].cells; shade(a, "E8EEF9")
        for c in (a, b): cell_margins(c, 70, 70, 100, 100); cell_borders(c, top=(4, "BFC6D6"), bottom=(4, "BFC6D6"), left=(4, "BFC6D6"), right=(4, "BFC6D6"))
        a.paragraphs[0].paragraph_format.space_after = Pt(0); run(a.paragraphs[0], k, 9.5, True, NAVY)
        first = True
        for line in (v if isinstance(v, list) else [v]):
            q = b.paragraphs[0] if first else b.add_paragraph(); first = False; q.paragraph_format.space_after = Pt(1); run(q, line, 9.5)
        if h:
            trPr = t.rows[i]._tr.get_or_add_trPr(); he = OxmlElement("w:trHeight"); he.set(qn("w:val"), str(int(h * 567))); he.set(qn("w:hRule"), "atLeast"); trPr.append(he)
    fix_widths(t, [4.2, 12.8]); return t
def tasks(rows, n=4):
    t = doc.add_table(rows=1 + max(n, len(rows)), cols=3)
    for j, h in enumerate(("Wer", "Was", "Bis wann")):
        c = t.rows[0].cells[j]; shade(c, NAVY); cell_margins(c, 50, 50, 100, 100); c.paragraphs[0].paragraph_format.space_after = Pt(0); run(c.paragraphs[0], h, 9.5, True, "FFFFFF")
    for i in range(1, len(t.rows)):
        for j, c in enumerate(t.rows[i].cells):
            cell_margins(c, 80, 80, 100, 100); cell_borders(c, bottom=(4, "BFC6D6"), left=(4, "BFC6D6"), right=(4, "BFC6D6")); c.paragraphs[0].paragraph_format.space_after = Pt(0)
            if i - 1 < len(rows): run(c.paragraphs[0], rows[i - 1][j], 9.5)
    fix_widths(t, [3.2, 10.6, 3.2])
def protokoll(titel, sub, daten, punkte, ergebnisse, tasks_, offen, naechst, example=False):
    para(doc, ("BEISPIEL · " if example else "") + "PROTOKOLL", 9, True, "B07800", after=0)
    para(doc, titel, 18, True, NAVY, after=1); para(doc, sub, 9.5, color="5B6680", after=5)
    kv(daten); para(doc, "", after=2)
    kv([("Besprochene Punkte", punkte, 3.4), ("Ergebnisse / Beschlüsse", ergebnisse, 3.0)])
    para(doc, "Aufgaben", 11, True, NAVY, before=6, after=3); tasks(tasks_)
    para(doc, "", after=2); kv([("Offene Punkte", offen, 1.6), ("Nächster Termin", naechst, None), ("Protokollführer", "[Name]" if example else "", None)])
    if example: para(doc, "Hinweis: Muster mit [Platzhaltern]. Datum, Teilnehmer und Inhalte sind selbst einzutragen; Fristen entsprechen dem Soll-Plan und sind keine Ist-Angaben.", 8.5, color="5B6680", before=6)
sub = "Rechte und Pflichten aus dem Ausbildungsvertrag · Yasin & Mido"
protokoll("Protokoll (Vorlage)", sub, [("Projekt", "Rechte und Pflichten aus dem Ausbildungsvertrag", None), ("Datum", "", None), ("Uhrzeit", "", None), ("Ort / Form", "", None), ("Teilnehmer", "", None), ("Thema", "", None)], "", "", [], "", "", False)
doc.add_page_break()
pk = lambda d: ("[Datum]", "[Uhrzeit]", "[Ort / Form]")
protokoll("Protokoll 1: Themenstart und Projektskizze", sub,
 [("Projekt", "Rechte und Pflichten aus dem Ausbildungsvertrag", None), ("Datum", "[Datum]", None), ("Uhrzeit", "[Uhrzeit]", None), ("Ort / Form", "[Ort / Form]", None), ("Teilnehmer", "Yasin, Mido [weitere Teilnehmer eintragen]", None), ("Thema", "Themenfestlegung, Projektskizze und SMART-Ziele (AP 1.1)", None)],
 ["Thema und Zielgruppe: [Ergebnis der Absprache eintragen]", "Projektskizze mit den sieben Punkten und zwei SMART-Zielen", "Rollenverteilung Yasin / Mido"],
 ["[Beschluss zum Thema]", "[Beschluss zur Aufgabenverteilung]", "Projektskizze wird zur Themenfreigabe vorgelegt (Meilenstein M1)"],
 [("Yasin & Mido", "Projektskizze und SMART-Ziele fertigstellen (AP 1.1)", f"[Datum] (Plan: {fmt(end('1.1'), True)})"), ("Mido", "Projektstrukturplan vorbereiten (AP 1.2)", "[Datum]")],
 "[offene Punkte]", "[Datum]", True)
doc.add_page_break()
protokoll("Protokoll 2: Planung und Recherche", sub,
 [("Projekt", "Rechte und Pflichten aus dem Ausbildungsvertrag", None), ("Datum", "[Datum]", None), ("Uhrzeit", "[Uhrzeit]", None), ("Ort / Form", "[Ort / Form]", None), ("Teilnehmer", "Yasin, Mido", None), ("Thema", "Projektstrukturplan, Projektablaufplan, Recherche (AP 1.2, 1.3, 2.1)", None)],
 ["Projektstrukturplan mit fünf Teilaufgaben (AP 1.2)", "Projektablaufplan mit Terminen und Meilensteinen (AP 1.3)", "Aufteilung der Recherche zu BBiG, JArbSchG, BUrlG, ArbZG (AP 2.1)"],
 ["[Beschluss zum Plan]", "[Beschluss zur Recherche-Aufteilung]"],
 [("Mido", "Projektstrukturplan und Projektablaufplan fertigstellen (AP 1.2, 1.3)", f"[Datum] (Plan: {fmt(end('1.3'), True)})"), ("Yasin", "Gesetzliche Grundlagen recherchieren (AP 2.1)", f"[Datum] (Plan: {fmt(end('2.1'), True)})")],
 "[offene Punkte]", "[Datum]", True)
doc.add_page_break()
protokoll("Protokoll 3: Abschluss und Probelauf", sub,
 [("Projekt", "Rechte und Pflichten aus dem Ausbildungsvertrag", None), ("Datum", "[Datum]", None), ("Uhrzeit", "[Uhrzeit]", None), ("Ort / Form", "[Ort / Form]", None), ("Teilnehmer", "Yasin, Mido", None), ("Thema", "Probelauf der Präsentation, Material, Ablauf am 08.10.2026 (AP 5.1, 5.2)", None)],
 ["Probelauf mit Sprechskript und Stoppuhr", "Technik (Beamer, QR-Code, Website) und Plan B", "Material: Merkblatt gedruckt, Zettel für Plan B"],
 ["[Ergebnis des Probelaufs, zum Beispiel Gesamtdauer]", "[Beschluss zu Anpassungen]"],
 [("Yasin & Mido", "Letzte Korrekturen und Materialcheck (AP 5.1)", f"[Datum] (Plan: {fmt(end('5.1'), True)})"), ("Yasin & Mido", "Präsentation halten (AP 5.2)", f"[Datum] (Plan: {fmt(end('5.2'), True)})"), ("Yasin & Mido", "Evaluation und Projektbericht (AP 5.3)", "[laut Lehrkraft]")],
 "[offene Punkte]", "[Datum]", True)
footer(sec, "Protokoll · Yasin & Mido")
path = os.path.join(OUTD, "protokoll_vorlage_v4.docx"); doc.save(path); print("Protokoll Seiten", to_pdf(path))

# ================================================================= C) Projektbericht-Gliederung + Anhangsverzeichnis
doc, sec = new_doc(); sec.top_margin = Cm(1.0); sec.bottom_margin = Cm(1.2)
para(doc, "PROJEKTBERICHT", 9, True, "B07800", after=0)
para(doc, "Gliederung mit Stichwort-Hinweisen", 18, True, NAVY, after=1)
para(doc, f"{TITEL} · Yasin & Mido. Bewertungsbogen: 19 Kriterien × 4 Punkte (der Wortlaut lag nicht vor; Hinweise folgen den bekannten Kriterien: Aufgabenstellung verständlich, Einbettung in den Gesamtzusammenhang, Arbeitsschritte aus der Skizze abgeleitet, Vorgehensweise grafisch aufbereitet, Rechtschreibung, einheitliches Layout). Orange markiert = selbst auszufüllen.", 9.2, color="5B6680", after=6)
GL = [
 ("1", "Ausgangsbeschreibung und Aufgabenstellung", [
   ("Ausgangslage: Prüfung 25.11.2026, Wirtschafts- und Sozialkunde, Mitschüler vorbereiten", False),
   ("Aufgabe: Booklet, Unterrichtsstunde, Website (Projektskizze, Punkt 3)", False),
   ("Einbettung in den Gesamtzusammenhang: Fach GP, Berufsbild, Ausbildungsvertrag im Alltag", False),
   ("SMART-Ziele aus der Skizze (Ziel 1 Booklet, Ziel 2 Unterrichtsstunde)", False)]),
 ("2", "Planung", [
   ("Projektskizze (Kurzfassung der sieben Punkte)", False),
   ("Projektstrukturplan: fünf Teilaufgaben, 15 Arbeitspakete (Grafik einfügen)", False),
   ("Projektablaufplan: Tabelle, Gantt, Meilensteine M1–M6, kritischer Weg", False),
   ("Vorgehensmodell Wasserfall; Ableitung der Arbeitsschritte aus der Skizze", False),
   ("Ressourcen: Yasin, Mido, Zeit 21 Arbeitstage, keine Kosten (Druck: [Menge])", False)]),
 ("3", "Durchführung", [
   ("Recherche (AP 2.1–2.3): Quellen und Stand Oktober 2026", False),
   ("Booklet (AP 3.1–3.3): 16 Seiten, Merkblatt, Aufgaben mit Erwartungshorizont", False),
   ("Präsentation und Website (AP 4.1–4.3): 22 sichtbare + 5 versteckte Folien, Sprechskript", False),
   ("Probelauf und Präsentation am 08.10.2026 (AP 5.1, 5.2)", False),
   ("Tatsächlicher Ablauf je Arbeitspaket: [selbst beschreiben]", True)]),
 ("4", "Evaluation", [
   ("Soll-Ist-Vergleich der Termine und Ergebnisse: [selbst ausfüllen]", True),
   ("Aufgetretene Probleme und wie sie gelöst wurden: [selbst ausfüllen]", True),
   ("Feedback der Klasse (Mini-Quiz-Ergebnis per Handzeichen, Blitzlicht, Rückmeldungen): [selbst ausfüllen]", True),
   ("Zielerreichung der SMART-Ziele (messbare Werte prüfen): [selbst ausfüllen]", True),
   ("Reflexion: Was lief gut, was würden wir anders machen, was haben wir gelernt: [selbst ausfüllen]", True)]),
 ("5", "Anhang", [("Anhangsverzeichnis siehe unten", False)]),
]
for nr, titel, pts in GL:
    para(doc, f"{nr}  {titel}", 12.5, True, NAVY, before=5, after=1)
    for txt_, me in pts:
        p = para(doc, "", after=1.5); p.paragraph_format.left_indent = Cm(0.5)
        run(p, "• ", 10); run(p, txt_, 10, me, "B07800" if me else "1A2238")
para(doc, "Anhangsverzeichnis", 14, True, NAVY, before=6, after=2)
AN = [("A1", "Projektskizze", "projektskizze_v4.pdf"), ("A2", "Projektstrukturplan (Grafik und Arbeitspaketliste)", "projektstrukturplan_v4.pdf"), ("A3", "Projektablaufplan (Tabelle, Gantt, Meilensteine)", "projektablaufplan_v4.pdf / .xlsx"),
      ("A4", "Booklet und Merkblatt", "booklet_v4.pdf, merkblatt_v4.pdf"), ("A5", "Präsentation (Folienübersicht) und Sprechskript", "praesentation_unterricht_v4.pptx, sprechskript_v4.pdf"),
      ("A6", "Protokolle (echte Protokolle der Besprechungen)", "[selbst erstellen mit protokoll_vorlage_v4.docx]"), ("A7", "Website und QR-Code", "yasinbenx.github.io/azubi-vertrag"),
      ("A8", "Feedback der Klasse (Quizergebnis, Blitzlicht)", "[selbst ergänzen]"), ("A9", "Quellenverzeichnis", "siehe Booklet Seite 16")]
t = doc.add_table(rows=1, cols=3)
for c, h in zip(t.rows[0].cells, ("Nr.", "Anlage", "Datei / Hinweis")):
    shade(c, NAVY); cell_margins(c, 50, 50, 100, 100); c.paragraphs[0].paragraph_format.space_after = Pt(0); run(c.paragraphs[0], h, 9.5, True, "FFFFFF")
for a, b, c_ in AN:
    r = t.add_row()
    for c, v in zip(r.cells, (a, b, c_)):
        cell_margins(c, 50, 50, 100, 100); cell_borders(c, bottom=(4, "BFC6D6")); c.paragraphs[0].paragraph_format.space_after = Pt(0)
        run(c.paragraphs[0], v, 9.5, v == a, "B07800" if "[selbst" in v else "1A2238")
fix_widths(t, [1.4, 8.4, 7.2])
footer(sec, "Projektbericht-Gliederung · Yasin & Mido")
path = os.path.join(OUTD, "projektbericht_gliederung_v4.docx"); doc.save(path); print("Bericht Seiten", to_pdf(path))
