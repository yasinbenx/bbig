# -*- coding: utf-8 -*-
import os, sys, math
sys.path.insert(0, os.path.dirname(__file__))
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from data2 import *

H = lambda s: RGBColor.from_string(s.lstrip("#"))
NAVY, NAVY2, ACC = H("14264B"), H("22386B"), H("F5A800")
ACC_L, BLUE_L, GREY_L, INK, MUTED, WHITE = H("FFF1CC"), H("E8EEF9"), H("EDEFF4"), H("1A2238"), H("5B6680"), H("FFFFFF")
GREEN, RED = H("2E9E4F"), H("D62839")
IMG = os.path.join(os.path.dirname(__file__), "img")
QR = os.path.join(os.path.dirname(__file__), "..", "output", "v2", "qr", "qr.png")
URL_KURZ = "yasinbenx.github.io/azubi-vertrag"
prs = Presentation(); prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
BLANK = prs.slide_layouts[6]

def rect(s, x, y, w, h, fill, line=None, shape=MSO_SHAPE.RECTANGLE):
    r = s.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    r.fill.solid(); r.fill.fore_color.rgb = fill
    if line is None: r.line.fill.background()
    else: r.line.color.rgb = line; r.line.width = Pt(1.2)
    r.shadow.inherit = False; return r

def text(s, x, y, w, h, t, size=20, bold=False, color=INK, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, shape=None, font="Arial"):
    tb = shape or s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h)); tf = tb.text_frame
    tf.word_wrap = True; tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = Inches(0.1); tf.margin_top = tf.margin_bottom = Inches(0.05)
    for i, pt in enumerate(t if isinstance(t, list) else [t]):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph(); p.alignment = align
        if i: p.space_before = Pt(size * 0.45)
        for rt, rb, rc in (pt if isinstance(pt, list) else [(pt, bold, color)]):
            r = p.add_run(); r.text = rt; r.font.size = Pt(size); r.font.bold = rb; r.font.color.rgb = rc; r.font.name = font
    return tb

def slide(title=None, kicker=None, notes="", dark=False, hidden=False):
    s = prs.slides.add_slide(BLANK)
    if dark: rect(s, 0, 0, 13.333, 7.5, NAVY); rect(s, 0, 0, 0.35, 7.5, ACC)
    else:
        rect(s, 0, 0, 0.35, 7.5, ACC)
        if kicker: text(s, 0.7, 0.3, 11, 0.35, kicker.upper(), 13, True, H("B07A00"))
        if title: text(s, 0.7, 0.6, 12, 0.9, title, 32, True, NAVY)
    s.notes_slide.notes_text_frame.text = notes
    if hidden: s._element.set("show", "0")
    return s

def card(s, x, y, w, h, head, body, hs=20, bs=19, fill=BLUE_L, bar=NAVY2):
    rect(s, x, y, w, h, fill); rect(s, x, y, 0.1, h, bar)
    text(s, x + 0.25, y + 0.08, w - 0.4, 0.5, head, hs, True, NAVY)
    off = 0.12 + hs * 0.026
    text(s, x + 0.25, y + off, w - 0.4, h - off - 0.05, body, bs)

def table(s, data, x, y, w, colw, size=16, rowh=0.5, fills=None):
    gt = s.shapes.add_table(len(data), len(data[0]), Inches(x), Inches(y), Inches(w), Inches(rowh * len(data))); t = gt.table
    pr = gt._element.graphic.graphicData.tbl.tblPr; pr.set("bandRow", "0"); pr.set("firstRow", "0")
    for j, cw in enumerate(colw): t.columns[j].width = Inches(cw)
    for i, row in enumerate(data):
        t.rows[i].height = Inches(rowh)
        for j, val in enumerate(row):
            c = t.cell(i, j); c.text = ""; c.margin_left = c.margin_right = Inches(0.1); c.margin_top = c.margin_bottom = Inches(0.03)
            c.vertical_anchor = MSO_ANCHOR.MIDDLE; c.text_frame.word_wrap = True
            r = c.text_frame.paragraphs[0].add_run(); r.text = val; r.font.name = "Arial"; r.font.size = Pt(size); c.fill.solid()
            if i == 0: c.fill.fore_color.rgb = NAVY; r.font.color.rgb = WHITE; r.font.bold = True
            else:
                c.fill.fore_color.rgb = H("F6F8FC") if i % 2 == 0 else WHITE; r.font.color.rgb = INK
                if j == 0: r.font.bold = True; r.font.color.rgb = NAVY
                if fills and (i, j) in fills:
                    c.fill.fore_color.rgb = fills[(i, j)][0]; r.font.color.rgb = WHITE; r.font.bold = True
    return t

def qr_small(s, label="Am Handy üben"):
    """kleiner QR-Code unten rechts auf weissem Grund, daneben Kurz-URL"""
    rect(s, 11.85, 6.3, 1.1, 1.1, WHITE, H("BFC6D6"))
    s.shapes.add_picture(QR, Inches(11.9), Inches(6.35), width=Inches(1.0), height=Inches(1.0))
    text(s, 7.9, 6.54, 3.9, 0.7, [[(label, True, NAVY)], [(URL_KURZ, False, INK)]], 14, align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE)

def fallback_note(s, t):
    text(s, 0.7, 6.4, 7.0, 1.0, t, 14, False, MUTED, anchor=MSO_ANCHOR.MIDDLE)

# ===================================================================== 1 Titel
s = slide(dark=True, notes=(
    "Yasin (0:30): „Guten Tag zusammen, wir sind Yasin und Mido. Wir zeigen euch kurz unser Projekt zu den Rechten und Pflichten aus dem Ausbildungsvertrag – und danach macht ihr selbst mit: Rote/Grüne Karte und Vertrags-Detektiv.“\n\n"
    "ZEITPLAN (intern): Kern ca. 28 Minuten = Projekt 2 · Durchführung 4 · Booklet 2 · Jetzt seid ihr dran 1 · Rote/Grüne Karte 5 · Vertrags-Detektiv 8 · Merkblatt, Evaluation und Fragen 6. "
    "Mit Modul A Experten-Runde (10 Minuten) und Modul B Abschluss-Mini-Quiz (6 Minuten) ca. 44 Minuten. "
    "Die vier ausgeblendeten Zusatzfolien (14 bis 17) liegen direkt nach der Lösung zum Vertrags-Detektiv: Folie einblenden und abspielen.\n"
    "PLAN B (intern): Fallen Internet oder Handys aus, laufen die Aktivitäten über die Folien: Rote/Grüne Karte mit Daumen hoch (stimmt) und Daumen runter (stimmt nicht), Vertrags-Detektiv direkt auf der Folie."))
text(s, 1.0, 1.1, 11.5, 0.5, "PROJEKT IM FACH GP (GESCHÄFTSPROZESSE)", 16, True, ACC)
text(s, 1.0, 1.7, 11.5, 2.2, "Rechte und Pflichten aus dem Ausbildungsvertrag", 48, True, WHITE)
text(s, 1.0, 3.95, 11, 0.5, "Yasin & Mido · Kaufleute für Büromanagement", 24, False, H("DCE3F2"))
for i, t in enumerate(["Projekt", "Booklet", "Mitmachen"]):
    x = 1.0 + i * 3.9; rect(s, x, 5.2, 3.6, 1.1, NAVY2); rect(s, x, 5.2, 3.6, 0.08, ACC)
    text(s, x, 5.35, 3.6, 0.9, [[(f"{i+1}  ", True, ACC), (t, True, WHITE)]], 24, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

# ===================================================================== 2 Projekt in Kuerze
s = slide("Unser Projekt in Kürze", "Aufgabe, Problem, Ziel",
          "Yasin (1:00): „Unsere Aufgabe: ein Booklet zur Prüfungsvorbereitung im Fach GP, zum Ausbildungsvertrag. Dazu gab es bisher kein kompaktes Lernmaterial mit Aufgaben und Lösungen. Unser Ziel: Am 25. November sollt ihr die Regeln zu Beginn und Dauer, Arbeitszeit, Vergütung, Urlaub, Probezeit und Kündigung sicher anwenden können.“")
for i, (h, b) in enumerate([("Aufgabe", "Ein Booklet zur Prüfungsvorbereitung im Fach GP zum Thema Ausbildungsvertrag."),
                            ("Problem", "Bisher gab es dazu kein kompaktes Lernmaterial mit Aufgaben und Lösungen."),
                            ("Ziel", "Beginn und Dauer, Arbeitszeit, Vergütung, Urlaub, Probezeit und Kündigung sicher anwenden können.")]):
    card(s, 0.7, 1.7 + i * 1.7, 8.6, 1.55, h, b, 22, 20)
rect(s, 9.7, 1.7, 3.1, 4.95, NAVY); rect(s, 9.7, 1.7, 3.1, 0.1, ACC)
text(s, 9.7, 2.3, 3.1, 0.5, "IHK-PRÜFUNG", 18, True, ACC, PP_ALIGN.CENTER)
text(s, 9.7, 2.9, 3.1, 1.3, "25.11.", 54, True, WHITE, PP_ALIGN.CENTER)
text(s, 9.7, 4.4, 3.1, 1.4, "schriftliche Abschlussprüfung", 18, False, H("DCE3F2"), PP_ALIGN.CENTER)

# ===================================================================== 3 Projektskizze
s = slide("Projektskizze auf einen Blick", "Ziel, Zielgruppe, Laufzeit",
          "Mido (1:00): „Unsere Projektskizze auf einen Blick: Zielgruppe seid ihr, Laufzeit vom 10. September bis 8. Oktober. Dazu zwei SMART-Ziele: Erstens Wissen über den Ausbildungsvertrag, zweitens Anwendung – im Vertrags-Detektiv sollt ihr mindestens vier von fünf Fehlern finden.“")
card(s, 0.7, 1.65, 4.0, 1.75, "Ziel", "Booklet und interaktive Stunde zur Prüfungsvorbereitung", 20, 19)
card(s, 4.9, 1.65, 4.0, 1.75, "Zielgruppe", "Mitschüler vor der Abschlussprüfung am 25.11.", 20, 19)
card(s, 9.1, 1.65, 3.55, 1.75, "Laufzeit", "10.09. – 08.10.2026", 20, 22, ACC_L, ACC)
card(s, 0.7, 3.65, 5.95, 3.4, "SMART-Ziel 1 · Wissen", "Bis 08.10. die sechs Prüfungspunkte kennen und zu jedem ein Beispiel erklären können.", 22, 22)
card(s, 6.85, 3.65, 5.8, 3.4, "SMART-Ziel 2 · Anwendung", "Bis 08.10. finden Mitschüler im Vertrags-Detektiv mindestens 4 von 5 Fehlern und begründen sie mit der passenden Regel.", 22, 22, ACC_L, ACC)

# ===================================================================== 4 PSP / 5 Gantt
s = slide("Projektstrukturplan", "Durchführung",
          "Yasin (1:00): „Der Projektstrukturplan zeigt alle Aufgaben: Vorbereitung mit Planung, die Praxisbeispiele, Booklet und Aufgaben sowie Präsentation und Abschluss – zusammen elf Arbeitspakete, jeweils mit Verantwortlichen: Yasin, Mido oder wir beide.“")
s.shapes.add_picture(os.path.join(IMG, "v2_psp_folie.png"), Inches(0.75), Inches(1.45), width=Inches(12.1))
s = slide("Projektablaufplan (Soll)", "Durchführung",
          "Mido (1:00): „Der Projektablaufplan zeigt den Soll-Plan vom 10. September bis 8. Oktober: Vorbereitung im September, Umsetzung im Oktober. Fünf Meilensteine sichern den Plan, der letzte ist die Präsentation am 8. Oktober.“")
s.shapes.add_picture(os.path.join(IMG, "v2_gantt_folie.png"), Inches(0.75), Inches(1.45), width=Inches(12.1))

# ===================================================================== 6 Durchfuehrung
s = slide("Durchführung", "Vorgehen, Aufgaben, Rahmen",
          "Yasin (1:00): „Vorbereitung im September, Umsetzung im Oktober. Recherche und Texte bei mir, Vertragssichtung, Praxisbeispiele, Grafiken und Korrekturlesen bei Mido, Gliederung, Layout und Präsentation gemeinsam.“\n"
          "Mido (1:00): „Rahmen: zwei Personen, Abgabe am 8. Oktober, keine nennenswerten Kosten. Probleme und Anpassungen sowie Absprachen: [eintragen].“")
card(s, 0.7, 1.65, 5.95, 2.45, "Vorgehen", ["Vorbereitung im September", "Umsetzung im Oktober", "Präsentation am 08.10."], 22, 20)
card(s, 6.85, 1.65, 5.8, 2.45, "Aufgabenverteilung", [[("Yasin: ", True, NAVY), ("Recherche, Texte", False, INK)], [("Mido: ", True, NAVY), ("Vertragssichtung, Praxisbeispiele, Grafiken, Korrekturlesen", False, INK)], [("Gemeinsam: ", True, NAVY), ("Gliederung, Layout, Präsentation", False, INK)]], 22, 17)
card(s, 0.7, 4.3, 5.95, 2.75, "Probleme und Anpassungen", "[eintragen]", 22, 24, ACC_L, ACC)
card(s, 6.85, 4.3, 5.8, 2.75, "Rahmenbedingungen und Absprachen", [[("Rahmen: ", True, NAVY), ("2 Personen, feste Abgabe 08.10., keine nennenswerten Kosten, Vertragsauszüge nur anonymisiert", False, INK)], [("Absprachen: ", True, NAVY), ("[eintragen]", False, INK)]], 19, 17, ACC_L, ACC)

# ===================================================================== 7 Booklet
s = slide("Das Booklet im Überblick", "15 Seiten, fünf Bausteine",
          "Mido (2:00): „Unser Booklet hat 15 Seiten: kurze Kapitel entlang der Prüfungsthemen, ein Merkblatt auf einer Seite, Aufgaben mit Erwartungshorizont – also Lösung, Paragraf und Begründung – und ein Mini-Quiz. Dazu kommen Glossar und Quellenverzeichnis. Ihr bekommt es nach den Aktivitäten.“")
s.shapes.add_picture(os.path.join(IMG, "v2_b1.png"), Inches(9.5), Inches(1.5), height=Inches(5.3))
for i, (h, b) in enumerate([("Kapitel", "kurze Kapitel entlang der Prüfungsthemen"), ("Merkblatt", "das Wichtigste auf einer Seite"), ("Aufgaben", "Vertrags-Detektiv, IHK-Fälle, Wahr oder falsch"),
                            ("Erwartungshorizont", "Lösung, Paragraf, Begründung, Punkte"), ("Quiz", "Mini-Quiz zum Selbsttesten")]):
    y = 1.6 + i * 1.05
    rect(s, 0.7, y, 0.8, 0.85, NAVY); text(s, 0.7, y, 0.8, 0.85, str(i + 1), 28, True, ACC, PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE)
    rect(s, 1.5, y, 7.6, 0.85, BLUE_L); text(s, 1.65, y, 7.4, 0.85, [[(h + ": ", True, NAVY), (b, False, INK)]], 19, anchor=MSO_ANCHOR.MIDDLE)
text(s, 0.7, 6.9, 8.4, 0.4, "Dazu: Glossar und Quellenverzeichnis", 16, False, MUTED)

# ===================================================================== neue Folie: Jetzt seid ihr dran
s = slide("Jetzt seid ihr dran", "Mitmachen am Handy",
          "Yasin (0:30): „Jetzt seid ihr dran: Scannt den QR-Code und öffnet die Seite auf dem Handy.“\n"
          "Mido (0:30): „Wählt eine Aktivität und klickt sie in fünf Minuten durch. Kein Handy? Schaut zu zweit mit.“\n"
          "HINWEIS (intern): QR-Code 20 Sekunden stehen lassen.")
rect(s, 0.7, 1.5, 5.4, 5.4, WHITE, H("BFC6D6"))
s.shapes.add_picture(QR, Inches(0.85), Inches(1.65), width=Inches(5.1), height=Inches(5.1))
rect(s, 6.5, 1.6, 6.3, 1.2, NAVY); rect(s, 6.5, 1.6, 0.1, 1.2, ACC)
text(s, 6.7, 1.6, 6.0, 1.2, URL_KURZ, 24, True, WHITE, anchor=MSO_ANCHOR.MIDDLE)
for i, t in enumerate(["QR-Code scannen", "Aktivität wählen", "in 5 Minuten durchklicken"]):
    y = 3.05 + i * 0.95
    rect(s, 6.5, y + 0.05, 0.7, 0.7, NAVY, shape=MSO_SHAPE.OVAL)
    text(s, 0, 0, 0, 0, str(i + 1), 24, True, ACC, PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE, shape=s.shapes[-1])
    text(s, 7.35, y, 5.5, 0.85, t, 26, False, INK, anchor=MSO_ANCHOR.MIDDLE)
rect(s, 6.5, 6.05, 6.3, 0.85, ACC_L); rect(s, 6.5, 6.05, 0.1, 0.85, ACC)
text(s, 6.7, 6.05, 6.0, 0.85, "Kein Handy? Schaut zu zweit mit.", 24, True, NAVY, anchor=MSO_ANCHOR.MIDDLE)

# ===================================================================== 8-9 Rote/Gruene Karte
rules = [[("Am Handy: ", True, NAVY), ("Rote/Grüne Karte öffnen und „Stimmt“ oder „Stimmt nicht“ antippen", False, INK)],
         [("Ohne Handy: ", True, NAVY), ("Daumen hoch = stimmt, Daumen runter = stimmt nicht", False, INK)],
         "Auf „drei“ zeigen alle gleichzeitig"]
def rg_slide(part, items, start, notes):
    s = slide(f"Rote/Grüne Karte ({part} von 2)", "Aktivität 1", notes)
    if part == 1:
        rect(s, 0.7, 1.7, 3.7, 4.55, BLUE_L); rect(s, 0.7, 1.7, 3.7, 0.1, ACC)
        text(s, 0.85, 1.85, 3.4, 0.5, "Regeln", 22, True, NAVY)
        text(s, 0.85, 2.4, 3.4, 3.8, rules, 17)
        x0, w0 = 4.7, 8.1
    else: x0, w0 = 0.7, 12.1
    for i, (t, _, _) in enumerate(items):
        y = 1.7 + i * 0.94
        rect(s, x0, y, 0.75, 0.8, NAVY); text(s, x0, y, 0.75, 0.8, str(start + i), 26, True, ACC, PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE)
        rect(s, x0 + 0.75, y, w0 - 0.75, 0.8, GREY_L); text(s, x0 + 0.9, y, w0 - 1.0, 0.8, t, 19 if part == 1 else 22, True, NAVY, anchor=MSO_ANCHOR.MIDDLE)
    fallback_note(s, "Die Aktivität läuft am Handy über die Website. Diese Folie ist der Ersatz am Beamer, falls Internet oder Handys ausfallen.")
    qr_small(s, "Am Handy: Rote/Grüne Karte")
rg_slide(1, RG[:5], 1, "Yasin (2:00): „Aktivität 1: Rote/Grüne Karte. Scannt den QR-Code und öffnet die Rote/Grüne Karte am Handy: Stimmt oder Stimmt nicht antippen. Ohne Handy: Daumen hoch heißt stimmt, Daumen runter heißt stimmt nicht – auf ‚drei‘ zeigen alle gleichzeitig. Fünf Aussagen jetzt, fünf auf der nächsten Folie.“")
rg_slide(2, RG[5:], 6, "Mido (2:00): „Noch fünf Aussagen, gleiche Regel: am Handy antippen oder Daumen zeigen, auf ‚drei‘ alle gleichzeitig. Danach lösen wir gemeinsam auf.“")

# ===================================================================== 10 Loesung RG
s = slide("Lösung: Rote/Grüne Karte", "Aktivität 1",
          "Yasin und Mido (1:00): „Wir gehen die zehn Aussagen durch und nennen jeweils den Paragrafen. Wo lag die Klasse falsch? Dort erklären wir die Regel kurz.“")
rows = [["Nr.", "Karte", "Begründung"]]; fills = {}
for i, (t, ok, b) in enumerate(RG):
    rows.append([str(i + 1), "Stimmt" if ok else "Stimmt nicht", b]); fills[(i + 1, 1)] = (GREEN if ok else RED, 0, 0)
table(s, rows, 0.7, 1.5, 12.0, [0.9, 2.5, 8.6], 15, 0.5, fills)

# ===================================================================== 11-12 Vertrags-Detektiv
SERIF = "Times New Roman"
def excerpt(s, x, y, w, size, marks=False):
    rect(s, x, y, w, 0.1, NAVY2)
    yy = y + 0.18
    kopf_h = size * (4 * 0.0172 + 3 * 0.00625) + 0.2
    text(s, x + 0.1, yy, w - 0.2, kopf_h, [[(DET_KOPF[0], True, NAVY)]] + DET_KOPF[1:], size, False, INK, font=SERIF)
    yy += kopf_h + 0.06
    for t, f in DET:
        tw_ = w - 0.3 - (1.5 if (marks and f) else 0)
        cpl = int(tw_ / (size * 0.0066))
        n = math.ceil(len(t) / cpl); h = n * size * 0.0172 + 0.1
        if marks and f: rect(s, x + 0.05, yy - 0.02, w - 0.1, h, H("FDE3E1"), RED)
        text(s, x + 0.1, yy, tw_, h, t, size, False, INK, font=SERIF)
        if marks and f:
            rect(s, x + w - 1.4, yy + (h - 0.3) / 2, 1.25, 0.3, RED); text(s, x + w - 1.4, yy + (h - 0.3) / 2, 1.25, 0.3, f"Fehler {f}", 12, True, WHITE, PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE)
        yy += h + 0.03
    return yy
s = slide("Vertrags-Detektiv: 5 Fehler", "Aktivität 2",
          "Mido (5:00): „Aktivität 2: Vertrags-Detektiv. Öffnet am Handy den Vertrags-Detektiv, tippt die Zeilen an, die ihr für fehlerhaft haltet, und prüft. Ohne Handy sucht ihr die fünf Fehler hier auf der Folie. Ihr habt fünf Minuten.“")
rect(s, 0.7, 1.5, 12.0, 4.8, H("F6F8FC"), H("BFC6D6")); excerpt(s, 0.8, 1.55, 11.8, 15)
fallback_note(s, "Die Aktivität läuft am Handy über die Website. Diese Folie ist der Ersatz am Beamer, falls Internet oder Handys ausfallen.")
qr_small(s, "Am Handy: Vertrags-Detektiv")
s = slide("Lösung: Vertrags-Detektiv", "Aktivität 2",
          "Yasin (3:00): „Wir gehen die fünf Fehler durch, jeweils mit Paragraf. Für jeden Fehler gibt es einen Punkt fürs Finden und einen für die Begründung, höchstens zehn Punkte. Wie viele habt ihr gefunden?“")
rect(s, 0.7, 1.55, 7.7, 5.6, H("F6F8FC"), H("BFC6D6")); excerpt(s, 0.75, 1.6, 7.6, 13, True)
for n, (stelle, regel) in FEHLER.items():
    y = 1.55 + (n - 1) * 1.12
    rect(s, 8.6, y, 4.1, 1.0, ACC_L); rect(s, 8.6, y, 0.1, 1.0, RED)
    text(s, 8.8, y + 0.02, 3.85, 0.95, [[(f"Fehler {n} · {stelle}: ", True, NAVY)], regel], 13, anchor=MSO_ANCHOR.MIDDLE)

# ===================================================================== 13-16 ausgeblendete Zusatzfolien
s = slide("Modul A: Experten-Runde (10 Minuten)", "Zusatzfolie · ausgeblendet",
          "Yasin (2:00): „Experten-Runde: Jede Gruppe bekommt ein Thema und erklärt es in zwei Minuten mit dem Merkblatt. Danach stellt sie der Klasse eine Frage.“", hidden=True)
for i, t in enumerate(["Vier Gruppen, vier Themen: Probezeit, Urlaub, Vergütung, Kündigung", "Vorbereiten mit dem Merkblatt", "Jede Gruppe erklärt ihr Thema in 2 Minuten", "Danach stellt sie der Klasse eine Frage"]):
    y = 1.8 + i * 1.2; rect(s, 0.8, y + 0.05, 0.6, 0.6, NAVY, shape=MSO_SHAPE.OVAL)
    text(s, 0, 0, 0, 0, str(i + 1), 22, True, ACC, PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE, shape=s.shapes[-1]); text(s, 1.65, y - 0.05, 10.8, 1.0, t, 26, anchor=MSO_ANCHOR.MIDDLE)
s = slide("Modul A: Die vier Themen", "Zusatzfolie · ausgeblendet",
          "Mido (1:00): „Hier sind die vier Themen mit den passenden Zeilen aus dem Merkblatt. Jede Gruppe zieht eins und bereitet sich vor.“", hidden=True)
mb = {a: (b, c) for a, b, c in MERKBLATT}
for i, (h, key) in enumerate([("Probezeit", "Probezeit"), ("Urlaub", "Urlaub"), ("Vergütung", "Vergütung"), ("Kündigung", "Kündigung nach der Probezeit")]):
    b, c = mb[key]
    card(s, 0.7 + (i % 2) * 6.15, 1.65 + (i // 2) * 2.7, 5.95, 2.5, f"{h} · {c}", b, 20, 17, [BLUE_L, ACC_L][(i + i // 2) % 2], [NAVY2, ACC][(i + i // 2) % 2])
def abschluss_slide(title, loes):
    s = slide(title, "Modul B: Abschluss-Mini-Quiz (6 Minuten)" if not loes else "Modul B: Lösung", 
              "Yasin (4:00): „Abschluss-Mini-Quiz: fünf neue Situationen. Öffnet am Handy die Seite Mini-Quiz und klickt die Fragen durch. Ohne Handy notiert ihr A bis D auf einem Zettel; die Fragen stehen auf dieser Folie.“" if not loes else
              "Mido (2:00): „Hier die Lösungen mit Paragraf. Wir zählen aus, wie viele richtig waren.“", hidden=True)
    if not loes:
        for i, a in enumerate(ABSCHLUSS):
            col, row = (0, i) if i < 3 else (1, i - 3); x = 0.7 + col * 6.2; y = 1.55 + row * 1.8
            if col == 1: y = 1.55 + row * 2.3
            h = 1.65 if col == 0 else 2.15
            rect(s, x, y, 6.0, h, BLUE_L); rect(s, x, y, 0.1, h, NAVY2)
            ans = "  ·  ".join(f"{L} {t}" for L, t in zip("ABCD", a["a"]))
            text(s, x + 0.2, y + 0.03, 5.7, h - 0.05, [[(f"{i+1}  ", True, ACC), (a["q"], True, NAVY)], ans], 12.5)
        qr_small(s, "Am Handy: Mini-Quiz")
    else:
        table(s, [["Nr.", "Lösung", "Paragraf"]] + [[str(i + 1), f'{"ABCD"[a["c"]]} – {a["a"][a["c"]]}', a["fb"]] for i, a in enumerate(ABSCHLUSS)], 0.7, 1.6, 12.0, [0.9, 7.6, 3.5], 17, 0.85)
abschluss_slide("Fünf neue Situationen", False); abschluss_slide("Lösung: Abschluss-Mini-Quiz", True)

# ===================================================================== 17 Merkblatt und Zusammenfassung
s = slide("Merkblatt und Zusammenfassung", "Das Wichtigste auf einer Seite",
          "Mido (2:00): „Zum Mitnehmen: das Merkblatt. Kernregeln: Probezeit ein bis vier Monate, Mindestausbildungsvergütung 2026 724, 854, 977 und 1.014 Euro, Mindesturlaub 24 Werktage, Kündigung immer schriftlich, Jugendliche höchstens 8 Stunden täglich, Vertragsinhalt seit August 2024 in Textform.“")
rules6 = [("Probezeit", "ein bis vier Monate"), ("Vergütung 2026", "724 / 854 / 977 / 1.014 €"), ("Urlaub", "ab 18 Jahren 24 Werktage, darunter 25, 27 oder 30"),
          ("Kündigung", "Probezeit: jederzeit ohne Frist. Danach fristlos aus wichtigem Grund oder durch den Azubi mit 4 Wochen Frist beim Berufswechsel – immer schriftlich"),
          ("Jugendliche", "höchstens 8 Stunden täglich"), ("Vertrag", "seit August 2024 in Textform")]
for i, (h, b) in enumerate(rules6):
    card(s, 0.7 + (i % 3) * 4.1, 1.7 + (i // 3) * 2.8, 3.85, 2.6, h, b, 22, 17 if i == 3 else 20, ACC_L if i % 2 == 0 else BLUE_L, ACC if i % 2 == 0 else NAVY2)

# ===================================================================== 18 Evaluation und Reflexion
s = slide("Evaluation und Reflexion", "Ziel erreicht?",
          "Yasin und Mido (2:00): „Hat das Projekt sein Ziel erreicht? Im Vertrags-Detektiv fanden [Anzahl] von [Anzahl] Mitschülern mindestens 4 von 5 Fehlern (Handzeichen). Verbesserungen: Booklet jährlich aktualisieren, Probelesen früher einplanen, [eigener Vorschlag]. Reflexion: Gut lief [..], schwierig war [..], beim nächsten Mal [..].“")
card(s, 0.7, 1.65, 5.95, 2.3, "Ergebnis Vertrags-Detektiv", [[("[eintragen]", True, NAVY), (" von 5 Fehlern gefunden", False, INK)], [("[Anzahl]", True, NAVY), (" von ", False, INK), ("[Anzahl]", True, NAVY), (" Mitschülern fanden im Vertrags-Detektiv mindestens 4 von 5 Fehlern", False, INK)], [("(Zahlen per Handzeichen ermitteln)", False, MUTED)]], 20, 18, ACC_L, ACC)
rect(s, 0.7, 4.15, 5.95, 2.9, BLUE_L); rect(s, 0.7, 4.15, 0.1, 2.9, NAVY2)
text(s, 0.95, 4.2, 5.6, 0.5, "Verbesserungsvorschläge", 20, True, NAVY)
text(s, 0.95, 4.7, 5.6, 2.3, ["1  Booklet jährlich aktualisieren (die Mindestausbildungsvergütung wird jedes Jahr neu festgelegt)", "2  Probelesen durch Mitschüler früher einplanen", "3  [eigener Vorschlag]"], 16)
card(s, 6.85, 1.65, 5.8, 2.7, "Reflexion", [[("Gut lief: ", True, NAVY), ("[..]", False, INK)], [("Schwierig war: ", True, NAVY), ("[..]", False, INK)], [("Beim nächsten Mal: ", True, NAVY), ("[..]", False, INK)]], 20, 20)
card(s, 6.85, 4.55, 5.8, 2.5, "Feedback der Klasse", "[eintragen]", 20, 24, GREY_L, MUTED)

# ===================================================================== 19 Danke und Fragen
s = slide(dark=True, notes="Yasin und Mido (2:00): „Vielen Dank fürs Mitmachen! Zwei Fragen an euch: Was war am Booklet am hilfreichsten, und was fehlt euch noch? Und habt ihr Fragen zum Ausbildungsvertrag oder zu unserem Projekt?“")
text(s, 1.0, 1.0, 11, 0.5, "FRAGEN & KLASSENFEEDBACK", 16, True, ACC)
text(s, 1.0, 1.7, 11.3, 1.2, "Was war am Booklet am hilfreichsten, und was fehlt euch noch?", 34, True, WHITE)
text(s, 1.0, 3.5, 11.3, 1.2, "Habt ihr Fragen zum Ausbildungsvertrag oder zu unserem Projekt?", 34, True, WHITE)
rect(s, 1.0, 5.4, 2.0, 0.08, ACC); text(s, 1.0, 5.6, 11, 1.0, "Vielen Dank!", 44, True, ACC)

out = os.path.join(os.path.dirname(__file__), "..", "output", "v2", "praesentation.pptx"); prs.save(out)
vis = sum(1 for s_ in prs.slides if s_._element.get("show") != "0")
print("Folien gesamt", len(prs.slides), "sichtbar", vis)
for i, s_ in enumerate(prs.slides):
    n = s_.notes_slide.notes_text_frame.text
    sp = n.split("ZEITPLAN")[0]
    print(i + 1, "ausgeblendet" if s_._element.get("show") == "0" else "", len(sp.split()), "Woerter")
