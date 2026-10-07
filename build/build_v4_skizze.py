# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from docxlib import *
from plan4 import *
import docxlib
OUTD = os.path.join(os.path.dirname(__file__), "..", "output", "v4")
doc, sec = new_doc(); sec.top_margin = Cm(1.4); sec.bottom_margin = Cm(1.4)
para(doc, "PROJEKTSKIZZE", 9, True, "B07800", after=0)
para(doc, "Rechte und Pflichten aus dem Ausbildungsvertrag", 18, True, NAVY, after=1)
para(doc, "Fach GP (Geschäftsprozesse) · Kaufleute für Büromanagement · Präsentation am 08.10.2026", 9.5, color="5B6680", after=5)
def row(t, nr, label, build, widths=(0.9, 4.1, 12)):
    r = t.add_row(); a, b, c = r.cells
    for x in (a, b, c): cell_margins(x, 60, 60, 90, 90); cell_borders(x, bottom=(4, "BFC6D6"), top=(4, "BFC6D6"))
    shade(a, "14264B"); shade(b, "E8EEF9")
    run(a.paragraphs[0], str(nr), 10, True, "FFFFFF"); a.paragraphs[0].paragraph_format.space_after = Pt(0)
    run(b.paragraphs[0], label, 9.5, True, NAVY); b.paragraphs[0].paragraph_format.space_after = Pt(0)
    build(c)
t = doc.add_table(rows=0, cols=3)
def txt(s, bold_lead=None):
    def f(c):
        p = c.paragraphs[0]; p.paragraph_format.space_after = Pt(0)
        if bold_lead: run(p, bold_lead + " ", 9.5, True)
        run(p, s, 9.5)
    return f
def bullets(items):
    def f(c):
        first = True
        for lead, s in items:
            p = c.paragraphs[0] if first else c.add_paragraph(); first = False
            p.paragraph_format.space_after = Pt(1.5); run(p, "• ", 9.5); run(p, lead + " ", 9.5, True); run(p, s, 9.5)
    return f
row(t, 1, "Arbeitstitel", txt(f"{TITEL} – {UNTERTITEL}"))
row(t, 2, "Einreicher / Ansprechpartner", txt("Yasin & Mido · Betreuende Lehrkraft: Frau Schorr-Fischer · Klasse: [eintragen]"))
row(t, 3, "Projektziel / Projektidee", txt("Wir erstellen ein Booklet, eine interaktive Unterrichtsstunde (Präsentation) und eine kleine Website zum Thema „Rechte und Pflichten aus dem Ausbildungsvertrag“, um Mitschüler auf die schriftliche IHK-Abschlussprüfung am 25.11.2026 im Prüfungsbereich Wirtschafts- und Sozialkunde vorzubereiten. Inhaltlich geht es um Vertrag, Beginn und Dauer, tägliche Ausbildungszeit, Vergütung, Urlaub, Probezeit, Kündigung sowie die Pflichten von Azubi und Ausbildenden. Gesetzesstand: Oktober 2026."))
row(t, 4, "Verwertbarkeit / Nutzen", bullets([("Mitschüler:", "Kompaktes Lernmaterial mit Aufgaben und Lösungen in einfacher Sprache statt Gesetzesdeutsch; Merkblatt zum Mitnehmen."),
    ("Prüfungsnah:", "Der Prüfungsbereich dauert 60 Minuten und zählt 10 % der Gesamtnote; die Aufgaben (IHK-Fälle, Mini-Quiz) üben genau solche Fälle."),
    ("Wir selbst:", "Wir wenden die Methoden des Projektmanagements praktisch an und lernen die Regeln sicher anzuwenden.")]))
row(t, 5, "Umsetzung", bullets([("1 Projektmanagement und Planung:", "Skizze, Projektstrukturplan, Projektablaufplan (AP 1.1–1.3)"),
    ("2 Recherche:", "gesetzliche Grundlagen, Inhalte und Fälle, Quellen prüfen (AP 2.1–2.3)"),
    ("3 Booklet:", "Erklär-Themen, Aufgaben mit Erwartungshorizont, Layout und Merkblatt (AP 3.1–3.3)"),
    ("4 Präsentation und Unterrichtsstunde:", "Folien, Website mit QR-Code, Sprechskript (AP 4.1–4.3)"),
    ("5 Abschluss und Evaluation:", "Probelauf, Präsentation halten, Evaluation und Projektbericht (AP 5.1–5.3)"),
    ("Vorgehen:", "Wasserfallmodell; Arbeitsverteilung siehe Projektstrukturplan und Projektablaufplan (Anhang).")]))
wk = "; ".join(f"{w} ({fmt(a)}–{fmt(b)}): AP " + ", ".join(weekrange(a, b)) for w, a, b in WOCHEN)
ms = " · ".join(f"{k} {nm} ({fmt(d)})" for k, nm, d in MS)
row(t, 6, "Laufzeit", txt(f"10.09.2026 bis 08.10.2026 (4 Wochen, 21 Arbeitstage Montag bis Freitag). {wk}. Meilensteine: {ms}."))
row(t, 7, "Finanzierung", txt("Es entstehen keine nennenswerten Kosten. Benötigt werden Computer, Beamer der Schule und kostenloser Webspace (GitHub Pages) für die Website. Druck von Merkblatt (und gegebenenfalls Booklet): [Anzahl und Drucker klären]."))
fix_widths(t, [0.9, 4.1, 12])
p = para(doc, "SMART-Ziele", 13, True, NAVY, before=8, after=3); p.paragraph_format.keep_with_next = True
t2 = doc.add_table(rows=1, cols=3)
for c, h in zip(t2.rows[0].cells, ("Kriterium", "Ziel 1 – Booklet und Merkblatt", "Ziel 2 – Unterrichtsstunde")):
    shade(c, "14264B"); cell_margins(c, 50, 50, 90, 90); c.paragraphs[0].paragraph_format.space_after = Pt(0); run(c.paragraphs[0], h, 9.5, True, "FFFFFF")
SM = [("S – spezifisch", "Wir erstellen ein Booklet zu den Rechten und Pflichten aus dem Ausbildungsvertrag mit neun Erklär-Themen, Aufgaben (Rote/Grüne Karte, Vertrags-Detektiv, IHK-Fälle A–E, Mini-Quiz) mit Erwartungshorizont, Glossar und einem einseitigen Merkblatt.",
       "Wir halten eine interaktive Unterrichtsstunde im Fach GP mit sechs Phasen (Einstieg, Fragerunde, Erklären, Aufgaben, Besprechen, Quiz und Abschluss)."),
      ("M – messbar", "16 Seiten (Booklet) plus 1 Seite Merkblatt; alle Zahlen und Paragrafen sind gegen die Quellen geprüft.",
       "Die Stunde dauert höchstens 45 Minuten (geplant 39:45); im Mini-Quiz erreicht die Mehrheit der Klasse 4 oder 5 von 5 Punkten (Handzeichen)."),
      ("A – attraktiv", "Die Mitschüler erhalten Übungsmaterial mit Lösungen für die IHK-Prüfung am 25.11.2026.",
       "Die Klasse lernt durch Mitmachen (Handzeichen, Gruppenaufgaben, Handy-Quiz) statt durch reines Zuhören."),
      ("R – realistisch", "Zwei Personen, 21 Arbeitstage, Inhalte aus Gesetzestexten und bekannten Quellen; Arbeitspakete 3.1–3.3 sind mit 2–3 Arbeitstagen je Paket geplant.",
       "Die Stunde ist auf die vorhandene Unterrichtszeit zugeschnitten; Plan B (Papier) steht bereit, falls Internet oder Handys ausfallen."),
      ("T – terminiert", "Booklet fertig am 01.10.2026 (Meilenstein M3).", "Präsentation am 08.10.2026 (Meilenstein M6); Probelauf am 07.10.2026.")]
for k, a, b in SM:
    r = t2.add_row()
    for c, v, bd in zip(r.cells, (k, a, b), (True, False, False)):
        cell_margins(c, 50, 50, 90, 90); cell_borders(c, bottom=(4, "BFC6D6")); c.paragraphs[0].paragraph_format.space_after = Pt(0); run(c.paragraphs[0], v, 9, bd, NAVY if bd else "1A2238")
    shade(r.cells[0], "E8EEF9")
fix_widths(t2, [2.7, 7.2, 7.1])
footer(sec, "Projektskizze · Yasin & Mido")
path = os.path.join(OUTD, "projektskizze_v4.docx"); doc.save(path); print("Seiten", to_pdf(path))
