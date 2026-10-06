# -*- coding: utf-8 -*-
"""Praesentation v3: ganze Unterrichtsstunde (45 Min.) im Fach GP in Lehrerrolle.
Inhalte: site/js/data.js (Aufgaben, Loesungen), booklet/merkblatt und Auftragstext. Keine Projektinhalte."""
import os, sys, json, math, re
sys.path.insert(0, os.path.dirname(__file__))
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
D = json.loads(open(os.path.join(ROOT, "site/js/data.js"), encoding="utf-8").read().split("=", 1)[1].rstrip().rstrip(";"))
QR = os.path.join(ROOT, "output/v2/qr/qr.png")
URL_KURZ = "yasinbenx.github.io/azubi-vertrag"
ICON = lambda n: os.path.join(os.path.dirname(__file__), "img", "icons", n + ".png")
L = ["A", "B", "C", "D"]

H = lambda s: RGBColor.from_string(s.lstrip("#"))
NAVY, NAVY2, ACC = H("14264B"), H("22386B"), H("F5A800")
ACC_L, BLUE_L, GREY_L, INK, MUTED, WHITE, LINE = H("FFF1CC"), H("E8EEF9"), H("EDEFF4"), H("1A2238"), H("5B6680"), H("FFFFFF"), H("BFC6D6")
GREEN, RED, ORANGE = H("2E8B57"), H("B3261E"), H("D9730D")

prs = Presentation(); prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
BLANK = prs.slide_layouts[6]
META = []      # (nr, titel, dauer_s, sprecher, hidden, sprech_woerter)

# ------------------------------------------------------------------ Bausteine
def rect(s, x, y, w, h, fill, line=None, shape=MSO_SHAPE.RECTANGLE, lw=1.2):
    r = s.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    r.fill.solid(); r.fill.fore_color.rgb = fill
    if line is None: r.line.fill.background()
    else: r.line.color.rgb = line; r.line.width = Pt(lw)
    r.shadow.inherit = False; return r

def text(s, x, y, w, h, t, size=24, bold=False, color=INK, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, font="Arial", shape=None, space=0.35):
    tb = shape or s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h)); tf = tb.text_frame
    tf.word_wrap = True; tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = Inches(0.1); tf.margin_top = tf.margin_bottom = Inches(0.05)
    for i, pt in enumerate(t if isinstance(t, list) else [t]):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph(); p.alignment = align
        if i: p.space_before = Pt(size * space)
        for rt, rb, rc in (pt if isinstance(pt, list) else [(pt, bold, color)]):
            r = p.add_run(); r.text = rt; r.font.size = Pt(size); r.font.bold = rb; r.font.color.rgb = rc; r.font.name = font
    return tb

def bullets(s, x, y, w, h, items, size=24, color=INK, gap=0.45):
    return text(s, x, y, w, h, [[("•  ", True, ACC)] + ([(i, False, color)] if isinstance(i, str) else i) for i in items], size, space=gap)

def words(t): return len(re.findall(r"\S+", t))
def mmss(sec): return f"{sec // 60}:{sec % 60:02d}"

def slide(title, kicker, sprecher, dauer, sprech, frage=None, erwartet=None, extra=None, hidden=False, dark=False, para=None):
    """dauer in Sekunden (None bei ausgeblendeten Reservefolien)"""
    assert words(sprech) <= 60, (title, words(sprech))
    s = prs.slides.add_slide(BLANK)
    if dark: rect(s, 0, 0, 13.333, 7.5, NAVY); rect(s, 0, 0, 0.35, 7.5, ACC)
    else:
        rect(s, 0, 0, 0.35, 7.5, ACC)
        if kicker: text(s, 0.7, 0.3, 11, 0.35, kicker.upper(), 13, True, H("B07A00"))
        if title: text(s, 0.7, 0.6, 12.2, 0.9, title, 32, True, NAVY)
    if para: text(s, 8.8, 7.0, 4.2, 0.4, para, 14, False, MUTED, PP_ALIGN.RIGHT)
    n = [f"SPRECHER: {sprecher}", f"DAUER: {mmss(dauer) if dauer is not None else 'Reserve (nicht in den 45 Minuten)'}", f"SPRECHTEXT: „{sprech}“"]
    if frage: n.append("MODERATIONSFRAGE AN DIE KLASSE: " + frage)
    if erwartet: n.append("ERWARTET: " + erwartet)
    if extra: n.append(extra)
    s.notes_slide.notes_text_frame.text = "\n".join(n)
    if hidden: s._element.set("show", "0")
    META.append((len(prs.slides), title or "Titel", dauer, sprecher, hidden, words(sprech)))
    return s

def card(s, x, y, w, h, head, body, hs=24, bs=24, fill=BLUE_L, bar=NAVY2):
    rect(s, x, y, w, h, fill); rect(s, x, y, 0.1, h, bar)
    if head: text(s, x + 0.25, y + 0.08, w - 0.4, 0.6, head, hs, True, NAVY)
    off = 0.15 + (hs * 0.032 if head else 0)
    text(s, x + 0.25, y + off, w - 0.4, h - off - 0.05, body, bs)

def table(s, data, x, y, w, colw, size=24, rowh=0.6, head=True, fills=None, bold_first=True):
    gt = s.shapes.add_table(len(data), len(data[0]), Inches(x), Inches(y), Inches(w), Inches(rowh * len(data))); t = gt.table
    pr = gt._element.graphic.graphicData.tbl.tblPr; pr.set("bandRow", "0"); pr.set("firstRow", "0")
    for j, cw in enumerate(colw): t.columns[j].width = Inches(cw)
    for i, row in enumerate(data):
        t.rows[i].height = Inches(rowh)
        for j, val in enumerate(row):
            c = t.cell(i, j); c.text = ""; c.margin_left = c.margin_right = Inches(0.12); c.margin_top = c.margin_bottom = Inches(0.04)
            c.vertical_anchor = MSO_ANCHOR.MIDDLE; c.text_frame.word_wrap = True
            r = c.text_frame.paragraphs[0].add_run(); r.text = val; r.font.name = "Arial"; r.font.size = Pt(size); c.fill.solid()
            if i == 0 and head: c.fill.fore_color.rgb = NAVY; r.font.color.rgb = WHITE; r.font.bold = True
            else:
                c.fill.fore_color.rgb = H("F6F8FC") if i % 2 == 0 else WHITE; r.font.color.rgb = INK
                if j == 0 and bold_first: r.font.bold = True; r.font.color.rgb = NAVY
                if fills and (i, j) in fills: c.fill.fore_color.rgb = fills[(i, j)]; r.font.color.rgb = WHITE; r.font.bold = True
    return t

def num_circle(s, x, y, d, n, size=22, fill=NAVY, fg=ACC):
    c = rect(s, x, y, d, d, fill, shape=MSO_SHAPE.OVAL)
    text(s, 0, 0, 0, 0, str(n), size, True, fg, PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE, shape=c)

def qr_block(s, x, y, size, label=None):
    """QR-Code auf weissem Grund mit Rahmen; label = Text darunter (Kurz-URL)"""
    pad = size * 0.06
    rect(s, x, y, size + 2 * pad, size + 2 * pad, WHITE, LINE)
    s.shapes.add_picture(QR, Inches(x + pad), Inches(y + pad), width=Inches(size), height=Inches(size))

def url_bar(s, x, y, w, h=0.8, size=26):
    rect(s, x, y, w, h, NAVY); rect(s, x, y, 0.1, h, ACC)
    text(s, x + 0.2, y, w - 0.3, h, URL_KURZ, size, True, WHITE, anchor=MSO_ANCHOR.MIDDLE)

def answer_cards(s, answers, y0=2.5, h=1.0, size=26, cols=1, x0=0.7, w=11.9):
    cw = w / cols
    for i, a in enumerate(answers):
        col, row = i % cols, i // cols
        x, y = x0 + col * cw, y0 + row * (h + 0.2)
        rect(s, x, y, cw - (0.2 if cols > 1 else 0), h, WHITE, NAVY, MSO_SHAPE.ROUNDED_RECTANGLE, 2).adjustments[0] = 0.12
        num_circle(s, x + 0.2, y + (h - 0.7) / 2, 0.7, L[i], 24)
        text(s, x + 1.05, y, cw - 1.4, h, a, size, False, INK, anchor=MSO_ANCHOR.MIDDLE)

def blitz(nr, teil, sprecher, dauer, frage, answers, loesung, erwartet_txt):
    s = slide(f"Blitzfrage {nr} (Teil {teil})", "Erarbeitung", sprecher, dauer,
              f"Blitzfrage {nr}: {frage} Ihr habt zehn Sekunden. Antwortet mit Handzeichen oder ruft den Buchstaben.",
              f"{frage}", f"Lösung {loesung}: {erwartet_txt}", f"LÖSUNG (nur hier in den Notizen): {loesung}")
    rect(s, 0.7, 1.55, 11.9, 1.2, NAVY); rect(s, 0.7, 1.55, 0.1, 1.2, ACC)
    text(s, 0.95, 1.55, 11.5, 1.2, frage, 28, True, WHITE, anchor=MSO_ANCHOR.MIDDLE)
    answer_cards(s, answers, 3.0, 0.95, 26)
    return s

SERIF = "Times New Roman"
def excerpt(s, x, y, w, size, marks=False, numbers=False):
    """Vertragsauszug aus der Website (kopf + zeilen); marks: Fehlerzeilen rot, numbers: nummerierte Zeilen"""
    rect(s, x, y, w, 0.1, NAVY2)
    yy = y + 0.18
    kh = size * (4 * 0.0172 + 3 * 0.00625) + 0.2
    text(s, x + 0.1, yy, w - 0.2, kh, [[(D["kopf"][0], True, NAVY)]] + D["kopf"][1:], size, False, INK, font=SERIF)
    yy += kh + 0.06
    for i, z in enumerate(D["zeilen"]):
        extra = (1.5 if (marks and z["f"]) else 0) + (0.55 if numbers else 0)
        tw_ = w - 0.3 - extra
        cpl = int(tw_ / (size * 0.0066)); n = math.ceil(len(z["t"]) / cpl); h = max(n * size * 0.0172 + 0.1, 0.4 if numbers else 0)
        if marks and z["f"]: rect(s, x + 0.05, yy - 0.02, w - 0.1, h, H("FDE3E1"), RED)
        if numbers: num_circle(s, x + 0.12, yy + (h - 0.4) / 2, 0.4, i + 1, 14)
        text(s, x + 0.1 + (0.55 if numbers else 0), yy, tw_, h, z["t"], size, False, INK, font=SERIF)
        if marks and z["f"]:
            rect(s, x + w - 1.4, yy + (h - 0.3) / 2, 1.25, 0.3, RED); text(s, x + w - 1.4, yy + (h - 0.3) / 2, 1.25, 0.3, f"Fehler {z['f']}", 12, True, WHITE, PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE)
        yy += h + 0.04
    return yy

# =================================================================== PHASE 1: Einstieg und Vorwissen (4:00)
s = slide(None, None, "Yasin", 30,
          "Guten Tag zusammen! Wir sind Yasin und Mido und halten heute die Stunde zu den Rechten und Pflichten aus dem Ausbildungsvertrag. Wir erklären die wichtigsten Regeln, ihr übt sie am Handy, und wir besprechen die Ergebnisse gemeinsam.",
          extra="ZEITPLAN (intern): Phase 1 Einstieg und Vorwissen 4:00 · Phase 2 Erarbeitung 3 × 4:00 = 12:00 · Phase 3 Aufgaben erklären 3:00 · Phase 4 Übungsphase 13:00 · Phase 5 Besprechung 8:00 · Phase 6 Sicherung und Abschluss 5:00 = 45:00. Folien 28 bis 35 sind ausgeblendet (Reserve und Plan B).", dark=True)
text(s, 1.0, 1.2, 11.5, 0.5, "UNTERRICHTSSTUNDE IM FACH GP", 16, True, ACC)
text(s, 1.0, 1.8, 11.5, 2.3, "Rechte und Pflichten aus dem Ausbildungsvertrag", 48, True, WHITE)
rect(s, 1.0, 4.3, 2.0, 0.08, ACC)
text(s, 1.0, 4.55, 11, 0.7, "Yasin & Mido", 30, False, H("DCE3F2"))

s = slide("Was wisst ihr schon?", "Einstieg und Vorwissen", "Yasin", 120,
          "Bevor wir starten: Was wisst ihr schon? Meldet euch bitte: Wer hat seinen Ausbildungsvertrag schon richtig gelesen? Danach vier Fragen. Antwortet frei, wir schreiben an der Tafel mit und lösen noch nicht auf.",
          "Wer hat seinen Ausbildungsvertrag schon richtig gelesen? (Handzeichen) Dann Fragen a bis d, Antworten der Klasse an der Tafel mitschreiben, nicht auflösen.",
          "a) vier Monate · b) 24 Werktage ab 18 Jahren (jüngere haben mehr) · c) keine Frist · d) ja, schriftlich")
rect(s, 0.7, 1.55, 11.9, 1.1, NAVY); rect(s, 0.7, 1.55, 0.1, 1.1, ACC)
text(s, 0.95, 1.55, 9.3, 1.1, "Wer hat seinen Ausbildungsvertrag schon richtig gelesen?", 26, True, WHITE, anchor=MSO_ANCHOR.MIDDLE)
rect(s, 10.4, 1.8, 2.0, 0.6, ACC, shape=MSO_SHAPE.ROUNDED_RECTANGLE); text(s, 10.4, 1.8, 2.0, 0.6, "Handzeichen", 20, True, NAVY, PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE)
qs = ["Wie lange darf die Probezeit höchstens dauern?", "Wie viele Urlaubstage stehen einem Azubi mindestens zu?", "Welche Kündigungsfrist gilt in der Probezeit?", "Muss eine Kündigung schriftlich sein?"]
for i, q in enumerate(qs):
    col, row = i % 2, i // 2; x, y = 0.7 + col * 6.05, 2.95 + row * 1.9
    rect(s, x, y, 5.85, 1.7, BLUE_L); rect(s, x, y, 0.1, 1.7, NAVY2)
    num_circle(s, x + 0.25, y + 0.5, 0.7, "abcd"[i], 26)
    text(s, x + 1.15, y, 4.6, 1.7, q, 24, True, NAVY, anchor=MSO_ANCHOR.MIDDLE)

s = slide("Lernziele", "Einstieg und Vorwissen", "Yasin", 45,
          "Das sind unsere Lernziele für heute. Am Ende könnt ihr nennen, was in einen Ausbildungsvertrag gehört, Vergütung, Urlaub und Arbeitszeit bestimmen, Probezeit und Kündigung richtig anwenden und Fälle mit der passenden Regel begründen.",
          "Welches Ziel ist euch am wichtigsten? (Meinungsabfrage, keine Wertung)", "Freie Antworten der Klasse")
text(s, 0.7, 1.55, 11.9, 0.7, "Am Ende könnt ihr:", 28, True, NAVY)
ziele = ["nennen, was in einen Ausbildungsvertrag gehört", "Vergütung, Urlaub und Arbeitszeit bestimmen", "Probezeit und Kündigung richtig anwenden", "Fälle mit der passenden Regel begründen"]
for i, z in enumerate(ziele):
    y = 2.4 + i * 1.12
    rect(s, 0.7, y, 11.9, 0.95, BLUE_L); rect(s, 0.7, y, 0.1, 0.95, NAVY2)
    num_circle(s, 1.0, y + 0.12, 0.7, i + 1, 26)
    text(s, 1.95, y, 10.5, 0.95, z, 28, False, INK, anchor=MSO_ANCHOR.MIDDLE)

s = slide("Ablauf der Stunde", "Einstieg und Vorwissen", "Yasin", 45,
          "So läuft die Stunde: erst euer Vorwissen, dann zwölf Minuten Erklären in drei Teilen, drei Minuten Aufgaben erklären, dreizehn Minuten Üben am Handy, acht Minuten gemeinsame Besprechung und zum Schluss Quiz und Abschluss.",
          "Wer hat sein Handy dabei? (Handzeichen)", "Wer kein Handy hat, schaut zu zweit mit (Plan B: Beamer-Folien 29 bis 35)")
ablauf = [("Vorwissen", 4), ("Erklären", 12), ("Aufgaben erklären", 3), ("Üben", 13), ("Besprechen", 8), ("Quiz und Abschluss", 5)]
for i, (nm, m) in enumerate(ablauf):
    y = 1.6 + i * 0.88
    text(s, 0.7, y, 4.4, 0.75, nm, 26, True, NAVY, anchor=MSO_ANCHOR.MIDDLE)
    rect(s, 5.2, y + 0.05, m * 0.55, 0.65, ACC if nm == "Üben" else NAVY2)
    text(s, 5.2, y + 0.05, max(m * 0.55, 1.4), 0.65, f"{m} Min.", 22, True, NAVY if nm == "Üben" else WHITE, PP_ALIGN.CENTER if m * 0.55 > 1.4 else PP_ALIGN.LEFT, MSO_ANCHOR.MIDDLE)

# =================================================================== PHASE 2: Erarbeitung (3 x 4:00)
# ---- Teil 1 (Yasin)
s = slide("Der Ausbildungsvertrag (Teil 1)", "Erarbeitung", "Yasin", 75,
          "Ein Ausbildungsvertrag muss nach § 11 BBiG bestimmte Angaben enthalten: Beginn und Dauer, tägliche Ausbildungszeit, Probezeit, Vergütung, Urlaub und die Kündigungsvoraussetzungen. Seit dem 1. August 2024 genügt dafür die Textform, zum Beispiel per E-Mail.",
          "Welche sechs Angaben gehören in den Vertrag?", "Beginn und Dauer, tägliche Ausbildungszeit, Probezeit, Vergütung, Urlaub, Kündigungsvoraussetzungen", para="§ 11 BBiG")
pf = [("calendar", "Beginn und Dauer"), ("clock", "tägliche Ausbildungszeit"), ("hourglass", "Probezeit"), ("euro", "Vergütung"), ("palm", "Urlaub"), ("doc", "Kündigungsvoraussetzungen")]
for i, (ic, t) in enumerate(pf):
    col, row = i % 2, i // 2; x, y = 0.7 + col * 6.05, 1.55 + row * 1.2
    rect(s, x, y, 5.85, 1.05, WHITE, LINE)
    s.shapes.add_picture(ICON(ic), Inches(x + 0.15), Inches(y + 0.1), width=Inches(0.85), height=Inches(0.85))
    text(s, x + 1.15, y, 4.65, 1.05, t, 21, True, NAVY, anchor=MSO_ANCHOR.MIDDLE)
rect(s, 0.7, 5.3, 11.9, 1.5, BLUE_L); rect(s, 0.7, 5.3, 0.1, 1.5, NAVY2)
text(s, 0.95, 5.3, 11.5, 1.5, [[("Textform: ", True, NAVY), ("Seit 01.08.2024 genügt für den Vertragsinhalt die Textform (zum Beispiel per E-Mail); vorher war die Papierform vorgeschrieben.", False, INK)]], 24, anchor=MSO_ANCHOR.MIDDLE)

s = slide("Beginn und Dauer (Teil 1)", "Erarbeitung", "Yasin", 60,
          "Zu Beginn und Dauer: Eine Verkürzung beantragen Azubi und Betrieb gemeinsam bei der zuständigen Stelle. Eine Verlängerung gibt es nur in Ausnahmefällen auf Antrag des Azubis oder nach nicht bestandener Prüfung, höchstens um ein Jahr. Die Ausbildung endet mit der Bekanntgabe des Prüfungsergebnisses.",
          "Wer beantragt eine Verkürzung?", "Azubi und Betrieb gemeinsam bei der zuständigen Stelle", para="§ 8, § 21 BBiG")
rect(s, 1.2, 2.0, 9.4, 0.5, NAVY); text(s, 1.2, 2.0, 9.4, 0.5, "Ausbildungsdauer", 22, True, WHITE, PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE)
for xx in (1.2, 10.6): rect(s, xx - 0.2, 1.95, 0.6, 0.6, ACC, NAVY, MSO_SHAPE.OVAL, 3)
text(s, 0.7, 2.65, 2.6, 0.6, "Beginn", 24, True, NAVY)
text(s, 8.7, 2.65, 4.2, 0.6, "Prüfung", 24, True, NAVY, PP_ALIGN.RIGHT)
text(s, 7.2, 3.1, 5.7, 0.7, "Ende mit Bekanntgabe des Prüfungsergebnisses", 20, False, INK, PP_ALIGN.RIGHT)
card(s, 0.7, 3.7, 5.85, 3.2, "Verkürzung", "auf gemeinsamen Antrag von Azubi und Betrieb bei der zuständigen Stelle", 26, 24, H("E3F3EA"), GREEN)
card(s, 6.75, 3.7, 5.85, 3.2, "Verlängerung", "nur in Ausnahmefällen auf Antrag des Azubis oder nach nicht bestandener Prüfung bis zur Wiederholungsprüfung, höchstens um ein Jahr", 26, 24, H("FCEBDD"), ORANGE)

s = slide("Pflichten (Teil 1)", "Erarbeitung", "Yasin", 75,
          "Beide Seiten haben Pflichten. Azubis lernen, arbeiten sorgfältig, befolgen Weisungen, wahren Geheimnisse und führen den Ausbildungsnachweis. Der Betrieb vermittelt das Ausbildungsziel, stellt Ausbildungsmittel kostenlos, gibt für Berufsschule und Prüfungen frei, stellt ein Zeugnis aus und zahlt die Vergütung.",
          "Wer stellt die Ausbildungsmittel zur Verfügung, und was kostet das den Azubi?", "Der Betrieb, kostenlos (§ 14 BBiG)", para="§§ 13–17 BBiG")
rect(s, 0.7, 1.55, 5.85, 0.7, NAVY); text(s, 0.9, 1.55, 5.5, 0.7, "Azubis (§ 13)", 26, True, WHITE, anchor=MSO_ANCHOR.MIDDLE)
rect(s, 6.75, 1.55, 5.85, 0.7, ACC); text(s, 6.95, 1.55, 5.5, 0.7, "Ausbildende (§§ 14–17)", 26, True, NAVY, anchor=MSO_ANCHOR.MIDDLE)
bullets(s, 0.7, 2.4, 5.85, 4.4, ["lernen", "sorgfältig arbeiten", "Weisungen befolgen und Ordnung beachten", "Geheimnisse wahren", "Ausbildungsnachweis führen"], 24)
bullets(s, 6.75, 2.4, 5.85, 4.4, ["Ausbildungsziel vermitteln", "Ausbildungsmittel kostenlos stellen", "für Berufsschule und Prüfungen freistellen", "Zeugnis ausstellen", "Vergütung zahlen"], 24)

blitz(1, 1, "Yasin", 30, "Welche Form genügt seit dem 01.08.2024 für den Vertragsinhalt?",
      ["Nur Papier mit Unterschrift", "Textform, zum Beispiel E-Mail", "Mündlich reicht"], "B", "Textform (§ 11 BBiG)")

# ---- Teil 2 (Mido)
s = slide("Ausbildungszeit (Teil 2)", "Erarbeitung", "Mido", 75,
          "Für Jugendliche gilt das Jugendarbeitsschutzgesetz: höchstens 8 Stunden täglich und 40 pro Woche, ausnahmsweise 8,5 Stunden täglich bei Ausgleich. Volljährige arbeiten 8 Stunden täglich, bis zu 10 Stunden mit Ausgleich innerhalb von sechs Monaten, höchstens 48 Stunden pro Woche.",
          "Wie viele Stunden dürfen Jugendliche täglich höchstens arbeiten?", "8 Stunden täglich (ausnahmsweise 8,5 Stunden bei Ausgleich)", para="§ 8 JArbSchG · § 3 ArbZG")
rect(s, 0.7, 1.55, 5.85, 0.7, NAVY); text(s, 0.9, 1.55, 5.5, 0.7, "Jugendliche", 26, True, WHITE, anchor=MSO_ANCHOR.MIDDLE)
rect(s, 6.75, 1.55, 5.85, 0.7, ACC); text(s, 6.95, 1.55, 5.5, 0.7, "Volljährige", 26, True, NAVY, anchor=MSO_ANCHOR.MIDDLE)
bullets(s, 0.7, 2.5, 5.85, 4.3, ["höchstens 8 Stunden täglich", "höchstens 40 Stunden pro Woche", "ausnahmsweise 8,5 Stunden täglich bei Ausgleich"], 24)
bullets(s, 6.75, 2.5, 5.85, 4.3, ["8 Stunden täglich", "bis 10 Stunden mit Ausgleich innerhalb von sechs Monaten", "höchstens 48 Stunden pro Woche"], 24)

s = slide("Vergütung (Teil 2)", "Erarbeitung", "Mido", 60,
          "Seit 2020 gibt es eine gesetzliche Mindestausbildungsvergütung. Bei Beginn 2026 sind es 724, 854, 977 und 1.014 Euro im ersten bis vierten Jahr. Die Beträge dürfen nicht unterschritten werden und werden jedes Jahr neu festgelegt.",
          "Wie hoch ist die Mindestvergütung im 2. Jahr bei Beginn 2026?", "854 €", para="§ 17 BBiG")
text(s, 0.7, 1.5, 11.9, 0.6, "Mindestausbildungsvergütung bei Beginn 2026", 26, True, NAVY)
table(s, [["Ausbildungsjahr", "Mindestvergütung"], ["1. Jahr", "724 €"], ["2. Jahr", "854 €"], ["3. Jahr", "977 €"], ["4. Jahr", "1.014 €"]], 0.7, 2.2, 11.9, [5.9, 6.0], 28, 0.72)
text(s, 0.7, 6.0, 11.9, 0.9, "Darf nicht unterschritten werden und wird jedes Jahr neu festgelegt.", 24, False, INK)

s = slide("Urlaub (Teil 2)", "Erarbeitung", "Mido", 75,
          "Der Mindesturlaub hängt vom Alter zu Jahresbeginn ab: unter 16 sind es 30, unter 17 sind es 27, unter 18 sind es 25 und ab 18 sind es 24 Werktage. Werktage sind alle Kalendertage außer Sonntagen und gesetzlichen Feiertagen.",
          "Zählt der Samstag als Werktag?", "Ja, Werktage sind alle Kalendertage außer Sonntagen und gesetzlichen Feiertagen", para="§ 19 JArbSchG · § 3 BUrlG")
table(s, [["Alter zu Jahresbeginn", "Werktage"], ["unter 16", "30"], ["unter 17", "27"], ["unter 18", "25"], ["ab 18", "24"]], 0.7, 1.6, 6.3, [3.9, 2.4], 26, 0.85)
rect(s, 7.3, 1.6, 5.3, 4.25, ACC_L); rect(s, 7.3, 1.6, 0.1, 4.25, ACC)
text(s, 7.5, 1.7, 5.0, 4.1, [[("Werktage", True, NAVY)], "sind alle Kalendertage außer Sonntagen und gesetzlichen Feiertagen.", "24 Werktage entsprechen 20 Arbeitstagen bei der Fünf-Tage-Woche."], 24)

blitz(2, 2, "Mido", 30, "24 Werktage Urlaub: Wie viele Arbeitstage sind das bei einer Fünf-Tage-Woche?",
      ["18", "20", "24", "28"], "B", "20 Arbeitstage (§ 3 BUrlG)")

# ---- Teil 3 (Yasin)
s = slide("Probezeit (Teil 3)", "Erarbeitung", "Yasin", 45,
          "Jedes Ausbildungsverhältnis beginnt mit einer Probezeit nach § 20 BBiG. Sie dauert mindestens einen und höchstens vier Monate.",
          "Darf die Probezeit sechs Monate dauern, wenn der Azubi zustimmt?", "Nein, höchstens vier Monate (§ 20 BBiG)", para="§ 20 BBiG")
text(s, 0.7, 1.7, 11.9, 1.5, "Jedes Ausbildungsverhältnis beginnt mit einer Probezeit von mindestens einem und höchstens vier Monaten.", 30, True, NAVY)
for i in range(4):
    rect(s, 0.7 + i * 3.0, 3.8, 2.9, 1.1, NAVY2 if i < 3 else ACC)
    text(s, 0.7 + i * 3.0, 3.8, 2.9, 1.1, f"{i+1}. Monat", 26, True, WHITE if i < 3 else NAVY, PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE)
text(s, 0.7, 5.05, 5.0, 0.6, "mindestens 1 Monat", 24, False, MUTED)
text(s, 7.6, 5.05, 5.0, 0.6, "höchstens 4 Monate", 24, False, MUTED, PP_ALIGN.RIGHT)

s = slide("Kündigung (Teil 3)", "Erarbeitung", "Yasin", 75,
          "In der Probezeit können beide Seiten jederzeit ohne Frist kündigen. Nach der Probezeit geht es nur noch fristlos aus wichtigem Grund, für beide Seiten, oder durch den Azubi mit vier Wochen Frist, wenn er die Ausbildung aufgibt oder den Beruf wechseln will.",
          "Welche Frist hat der Azubi nach der Probezeit bei Berufswechsel?", "Vier Wochen", para="§ 22 Abs. 1 und 2 BBiG")
rect(s, 0.7, 1.55, 5.85, 0.7, NAVY); text(s, 0.9, 1.55, 5.5, 0.7, "In der Probezeit", 26, True, WHITE, anchor=MSO_ANCHOR.MIDDLE)
rect(s, 6.75, 1.55, 5.85, 0.7, ACC); text(s, 6.95, 1.55, 5.5, 0.7, "Nach der Probezeit", 26, True, NAVY, anchor=MSO_ANCHOR.MIDDLE)
bullets(s, 0.7, 2.5, 5.85, 4.3, ["jederzeit ohne Frist", "von beiden Seiten"], 26)
bullets(s, 6.75, 2.5, 5.85, 4.3, ["fristlos aus wichtigem Grund (beide Seiten)", "oder durch den Azubi mit vier Wochen Frist, wenn er die Ausbildung aufgibt oder den Beruf wechseln will"], 24)

s = slide("Form und Fristen der Kündigung (Teil 3)", "Erarbeitung", "Yasin", 75,
          "Jede Kündigung muss schriftlich erfolgen, die elektronische Form ist ausgeschlossen. Nach der Probezeit braucht sie die Angabe der Gründe. Eine Kündigung aus wichtigem Grund ist nur innerhalb von zwei Wochen möglich, nachdem die Gründe bekannt wurden.",
          "Ist eine Kündigung per E-Mail wirksam?", "Nein, sie muss schriftlich erfolgen, die elektronische Form ist ausgeschlossen", para="§ 22 Abs. 3 und 4 BBiG")
for i, (h, b) in enumerate([("Immer schriftlich", "Die elektronische Form ist ausgeschlossen."), ("Mit Gründen", "Nach der Probezeit mit Angabe der Gründe."),
                            ("Innerhalb von zwei Wochen", "Eine Kündigung aus wichtigem Grund nur innerhalb von zwei Wochen, nachdem die Gründe bekannt wurden.")]):
    card(s, 0.7, [1.5, 3.05, 4.6][i], 11.9, [1.4, 1.4, 2.2][i], h, b, 26, 24, ACC_L if i == 0 else BLUE_L, ACC if i == 0 else NAVY2)

blitz(3, 3, "Yasin", 45, "Wann muss eine Kündigung aus wichtigem Grund ausgesprochen werden?",
      ["Innerhalb von vier Wochen nach Kenntnis", "Innerhalb von zwei Wochen nach Kenntnis", "Immer zum Monatsende", "Jederzeit"], "B", "Innerhalb von zwei Wochen nach Kenntnis (§ 22 Abs. 4 BBiG)")

# =================================================================== PHASE 3: Aufgaben erklaeren (3:00)
s = slide("Die Aufgaben im Überblick", "Aufgaben erklären", "Yasin", 60,
          "Jetzt seid ihr dran. Scannt den QR-Code und öffnet die Seite. Ihr bearbeitet drei Aufgaben: Rote/Grüne Karte allein, Vertrags-Detektiv und IHK-Fälle zu zweit. Wer schnell fertig ist, nimmt die Fälle D und E oder die Experten-Karten.",
          "Wer hat die Seite geöffnet? (Handzeichen)", "Mehrheit meldet sich; sonst QR-Code erneut zeigen", "HINWEIS (intern): QR-Code 20 Sekunden stehen lassen. Kein Handy? Zu zweit mitschauen, Plan B: Folien 29 bis 35.")
rect(s, 0.7, 1.45, 5.0, 5.0, WHITE, LINE); s.shapes.add_picture(QR, Inches(0.85), Inches(1.6), width=Inches(4.7), height=Inches(4.7))
url_bar(s, 6.0, 1.45, 6.6, 0.8, 26)
table(s, [["Aufgabe", "Arbeitsform", "Zeit"], ["1 Rote/Grüne Karte", "allein", "3 Min."], ["2 Vertrags-Detektiv", "zu zweit", "5 Min."], ["3 IHK-Fälle A bis C", "zu zweit", "5 Min."]], 6.0, 2.45, 6.6, [3.2, 2.0, 1.4], 22, 0.62)
text(s, 6.0, 5.0, 6.6, 0.95, [[("Schnell fertig? ", True, NAVY), ("Fälle D und E und Experten-Karten auf der Website.", False, INK)]], 24)
rect(s, 6.0, 6.05, 6.6, 0.75, ACC_L); rect(s, 6.0, 6.05, 0.1, 0.75, ACC)
text(s, 6.2, 6.05, 6.3, 0.75, "Kein Handy? Schaut zu zweit mit.", 24, True, NAVY, anchor=MSO_ANCHOR.MIDDLE)

def aufgabe(nr, titel, sprecher, dauer, sprech, bl, chips, frage=None, erwartet=None):
    s = slide(f"Aufgabe {nr} – {titel}", "Aufgaben erklären", sprecher, dauer, sprech, frage, erwartet)
    bullets(s, 0.7, 1.7, 8.2, 5.0, bl, 26, gap=0.6)
    for i, (k, v) in enumerate(chips):
        y = 1.8 + i * 1.5
        rect(s, 9.4, y, 3.2, 1.3, ACC_L if i else NAVY);
        text(s, 9.4, y + 0.08, 3.2, 0.45, k.upper(), 13, True, H("B07A00") if i else ACC, PP_ALIGN.CENTER)
        text(s, 9.4, y + 0.5, 3.2, 0.7, v, 28, True, NAVY if i else WHITE, PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE)
    return s
aufgabe(1, "Rote/Grüne Karte", "Mido", 30,
        "Aufgabe 1: Rote/Grüne Karte. Zehn Aussagen, eine pro Bildschirm. Tippt Stimmt oder Stimmt nicht und lest danach die Lösung. Das ist euer Schnell-Check, drei Minuten.",
        ["10 Aussagen, eine pro Bildschirm", "„Stimmt“ oder „Stimmt nicht“ tippen", "danach die Lösung lesen", "Ziel: Schnell-Check"], [("Arbeitsform", "allein"), ("Zeit", "3 Minuten")])
aufgabe(2, "Vertrags-Detektiv", "Yasin", 45,
        "Aufgabe 2: Vertrags-Detektiv. Lest den Vertragsauszug und tippt bis zu fünf Zeilen mit Fehlern an. Dann prüft ihr und begründet jeden Fehler mit der passenden Regel. Notizen und Merkblatt dürft ihr nutzen. Fünf Minuten, zu zweit.",
        ["Lest den Vertragsauszug", "Tippt die Zeilen mit Fehlern an (bis zu 5)", "Prüft und begründet jeden Fehler mit der passenden Regel", "Hilfsmittel: Notizen, Merkblatt"], [("Arbeitsform", "zu zweit"), ("Zeit", "5 Minuten")],
        "Wo findet ihr die passende Regel schnell?", "Im Merkblatt, Spalte „Paragraf“")
aufgabe(3, "IHK-Fälle A bis C", "Mido", 45,
        "Aufgabe 3: IHK-Fälle A bis C. Lest den Fall, wählt Antwort A bis D und begründet sie mit einer Regel. Fünf Minuten, zu zweit. Merkt euch eine Frage für die Besprechung.",
        ["Fall lesen", "Antwort A bis D wählen", "Antwort mit einer Regel begründen", "Merkt euch eine Frage für die Besprechung"], [("Arbeitsform", "zu zweit"), ("Zeit", "5 Minuten")],
        "Worauf achtet ihr bei der Begründung?", "Passende Regel mit Paragraf nennen")

# =================================================================== PHASE 4: Uebungsphase (13:00)
s = slide("Arbeitsphase", "Übungsphase", "Yasin und Mido", 780,
          "Los geht's, ihr habt dreizehn Minuten. Wir gehen durch die Reihen und helfen. Nach drei, acht und dreizehn Minuten sagen wir die Zeit an. Fertig? Dann nehmt die Reserve auf der Website.",
          "(beim Gehen) Welche Regel hilft euch hier?", "Passenden Paragrafen im Merkblatt finden",
          "HINWEIS (intern): Wir gehen durch die Klasse, helfen und merken uns typische Fehler für die Besprechung. Zeit ansagen nach Minute 3, 8 und 13. Schnell fertig: Fälle D und E, Experten-Karten.")
rect(s, 0.7, 1.45, 4.5, 4.5, WHITE, LINE); s.shapes.add_picture(QR, Inches(0.85), Inches(1.6), width=Inches(4.2), height=Inches(4.2))
url_bar(s, 5.5, 1.45, 7.1, 0.8, 26)
for i, (m, t) in enumerate([(3, "Aufgabe 1 · Rote/Grüne Karte"), (8, "Aufgabe 2 · Vertrags-Detektiv"), (13, "Aufgabe 3 · IHK-Fälle A bis C")]):
    y = 2.5 + i * 0.9
    rect(s, 5.5, y + 0.1, 0.55, 0.55, WHITE, NAVY, lw=3); text(s, 6.2, y, 6.4, 0.75, [[(f"Minute {m}: ", True, NAVY), (t, False, INK)]], 24, anchor=MSO_ANCHOR.MIDDLE)
rect(s, 5.5, 5.3, 7.1, 0.65, ACC_L); rect(s, 5.5, 5.3, 0.1, 0.65, ACC)
text(s, 5.7, 5.3, 6.8, 0.65, "Fertig? Reserve auf der Website", 24, True, NAVY, anchor=MSO_ANCHOR.MIDDLE)
x0, x1 = 0.9, 12.4
rect(s, x0, 6.55, x1 - x0, 0.12, NAVY2)
for m in (0, 3, 8, 13):
    xx = x0 + m * (x1 - x0) / 13
    rect(s, xx - 0.03, 6.4, 0.06, 0.42, ACC if m else NAVY)
    text(s, xx - 0.6, 6.85, 1.2, 0.4, f"{m} Min." if m else "Start", 16, True, NAVY, PP_ALIGN.CENTER)

# =================================================================== PHASE 5: Gemeinsame Besprechung (8:00)
FE = D["fehler"]
s = slide("Besprechung: Vertrags-Detektiv", "Gemeinsame Besprechung", "Yasin", 240,
          "Wir besprechen den Vertrags-Detektiv. Die Zeilen 1 und 7 sind korrekt, in fünf Zeilen steckt ein Fehler. Fehler 1: Die Probezeit darf höchstens vier Monate dauern. Wer hat welchen Fehler gefunden, und mit welcher Regel?",
          "Wer hat Fehler 1 gefunden? Welche Regel? Dann Fehler 2 bis 5 reihum abfragen.",
          "Fehler 1: höchstens vier Monate (§ 20 BBiG) · Fehler 2: mindestens 724 € im 1. Jahr (§ 17 BBiG) · Fehler 3: Jugendliche höchstens 8 Stunden täglich und 40 pro Woche (§ 8 JArbSchG) · Fehler 4: mindestens 24 Werktage, Jugendliche 25 bis 30 (§ 3 BUrlG, § 19 JArbSchG) · Fehler 5: in der Probezeit jederzeit ohne Frist, schriftlich (§ 22 Abs. 1 und 3 BBiG)")
rect(s, 0.7, 1.45, 7.7, 5.1, H("F6F8FC"), LINE); excerpt(s, 0.75, 1.5, 7.6, 11.5, marks=True)
text(s, 0.7, 6.6, 7.7, 0.45, "Zeilen 1 und 7 sind korrekt.", 16, True, MUTED)
for n in range(1, 6):
    fe = FE[str(n)]; y = 1.45 + (n - 1) * 1.04
    rect(s, 8.6, y, 4.0, 0.96, ACC_L); rect(s, 8.6, y, 0.1, 0.96, RED)
    body = [[(f"Fehler {n} · {fe['stelle']}", True, NAVY)], fe["regel"]]
    if n == 3: body.append("(Der Azubi ist bei Beginn 16 Jahre alt.)")
    text(s, 8.78, y, 3.8, 0.96, body, 12, anchor=MSO_ANCHOR.MIDDLE, space=0.1)

FAL = D["faelle"]
def faelle_besprechung(idx, titel, sprecher, dauer, sprech, frage, erwartet, hidden_note=None):
    s = slide(titel, "Gemeinsame Besprechung", sprecher, dauer, sprech, frage, erwartet, hidden_note)
    rows = [["Fall", "Lösung", "Begründung"]]
    for i in idx: rows.append([FAL[i]["label"].split(" (")[0].replace("Reservefall", "Fall"), L[FAL[i]["c"]], FAL[i]["fb"]])
    table(s, rows, 0.7, 1.6, 11.9, [2.0, 1.5, 8.4], 20, 1.25 if len(idx) == 3 else 1.4)
    return s
faelle_besprechung([0, 1, 2], "Besprechung: IHK-Fälle A bis C", "Mido", 150,
                   "Jetzt die IHK-Fälle A bis C. Für Fall A war die richtige Antwort B: In der Probezeit ist die Kündigung jederzeit ohne Frist möglich, aber schriftlich. Bei Fall B und Fall C war es jeweils C. Wie habt ihr begründet?",
                   "Welche Antwort habt ihr gewählt, und mit welcher Regel?", "A: B (§ 22 Abs. 1 und 3 BBiG) · B: C, 25 Werktage (§ 19 JArbSchG) · C: C, mindestens 724 € (§ 17 BBiG)")
faelle_besprechung([3, 4], "Besprechung: IHK-Fälle D und E", "Yasin", 90,
                   "Nur wenn ihr sie bearbeitet habt: Fall D und Fall E. Bei beiden war die richtige Antwort B. Fall D: Jugendliche arbeiten höchstens 8 Stunden täglich. Fall E: Die Verkürzung beantragen Azubi und Betrieb gemeinsam bei der zuständigen Stelle.",
                   "Wer hat Fall D oder E bearbeitet? Welche Regel gilt?", "D: B (§ 8 JArbSchG) · E: B (§ 8 Abs. 1 BBiG)",
                   "HINWEIS (intern): Nur wenn bearbeitet. Sonst die 1:30 auf Folie 22 und 23 verteilen.")

# =================================================================== PHASE 6: Sicherung und Abschluss (5:00)
s = slide("Mini-Quiz: Zeig, was du kannst", "Sicherung und Abschluss", "Mido", 180,
          "Zum Abschluss das Mini-Quiz: fünf Fragen auf der Website, allein, drei Minuten. Zeigt, was ihr könnt! Danach Handzeichen: Wer hat fünf, vier, drei oder weniger richtig?",
          "Wer hat 5, 4, 3 oder weniger richtig? (Handzeichen)", "Zahlen aufschreiben (für den Projektbericht)", "HINWEIS (intern): Handzeichen-Zahlen notieren.")
bullets(s, 0.7, 1.8, 7.9, 4.6, ["5 Fragen auf der Website", "allein", "3 Minuten"], 30, gap=0.8)
rect(s, 8.9, 1.6, 3.9, 3.9, WHITE, LINE); s.shapes.add_picture(QR, Inches(9.05), Inches(1.75), width=Inches(3.6), height=Inches(3.6))
text(s, 8.7, 5.65, 4.3, 0.6, URL_KURZ, 18, True, NAVY, PP_ALIGN.CENTER)

s = slide("Zurück zum Vorwissen", "Sicherung und Abschluss", "Yasin", 60,
          "Zurück zu unseren Anfangsfragen: Die Probezeit dauert höchstens vier Monate, der Mindesturlaub beträgt ab 18 Jahren 24 Werktage, für Jugendliche 25 bis 30. In der Probezeit gilt keine Frist, aber schriftlich. Ja, jede Kündigung muss schriftlich erfolgen.",
          "Was war neu für euch?", "Freie Antworten der Klasse (mit den Anfangsantworten an der Tafel vergleichen)")
table(s, [["Frage", "Antwort"], ["a) Probezeit höchstens?", "Vier Monate"], ["b) Urlaub mindestens?", "24 Werktage ab 18 Jahren, Jugendliche 25 bis 30"], ["c) Kündigungsfrist in der Probezeit?", "Keine Frist, aber schriftlich"], ["d) Kündigung schriftlich?", "Ja, die Kündigung muss schriftlich erfolgen"]],
      0.7, 1.55, 11.9, [4.9, 7.0], 24, 0.85)
rect(s, 0.7, 6.1, 11.9, 0.8, ACC_L); rect(s, 0.7, 6.1, 0.1, 0.8, ACC)
text(s, 0.95, 6.1, 11.5, 0.8, "Was war neu für euch?", 28, True, NAVY, anchor=MSO_ANCHOR.MIDDLE)

s = slide("Merkblatt und Feedback", "Sicherung und Abschluss", "Mido", 60,
          "Das Merkblatt habt ihr ausgeteilt bekommen, über den QR-Code übt ihr weiter. Zwei Fragen an euch: Was war hilfreich? Was fehlt euch noch? Vielen Dank fürs Mitmachen!",
          "Was war hilfreich? Was fehlt euch noch?", "Freie Antworten; Rückmeldungen notieren", "HINWEIS (intern): Feedback der Klasse in einem Satz festhalten (für den Projektbericht).")
card(s, 0.7, 1.55, 7.6, 1.4, "Merkblatt", "Das Wichtigste auf einer Seite – ausgeteilt.", 26, 24, ACC_L, ACC)
for i, q in enumerate(["Was war hilfreich?", "Was fehlt euch noch?"]):
    card(s, 0.7, 3.2 + i * 1.5, 7.6, 1.3, None, [[(q, True, NAVY)]], 24, 30)
text(s, 0.7, 6.2, 7.6, 0.9, "Vielen Dank!", 40, True, ACC)
rect(s, 9.0, 1.7, 3.6, 3.6, WHITE, LINE); s.shapes.add_picture(QR, Inches(9.12), Inches(1.82), width=Inches(3.36), height=Inches(3.36))
text(s, 8.8, 5.45, 4.0, 0.9, [[("Weiter üben", True, NAVY)], [(URL_KURZ, False, INK)]], 18, align=PP_ALIGN.CENTER)

# =================================================================== ausgeblendet: Reserve und Plan B
s = slide("Reserve: Schnell fertig?", "Reserve · ausgeblendet", "Mido", None,
          "Schnell fertig? Dann nehmt auf der Website die Experten-Karten: Thema wählen, dem Partner in einer Minute erklären und die Frage lösen. Oder bearbeitet die Fälle D und E.",
          "Welches Thema habt ihr gewählt, und was war die Frage?", "Karten: Probezeit, Urlaub, Vergütung, Kündigung", "NUR ANZEIGEN, wenn jemand schneller fertig ist.", hidden=True)
for i, t in enumerate(["Experten-Karten auf der Website öffnen", "Thema wählen und dem Partner in einer Minute erklären", "Frage lösen", "Oder: Fälle D und E bearbeiten"]):
    y = 1.7 + i * 1.3; num_circle(s, 0.9, y + 0.1, 0.8, i + 1, 26)
    text(s, 2.0, y, 10.5, 1.0, t, 28, False, INK, anchor=MSO_ANCHOR.MIDDLE)
text(s, 0.7, 6.9, 12, 0.45, URL_KURZ, 18, True, NAVY)

PLANB = "NUR ANZEIGEN, wenn Internet oder Handys ausfallen."
s = slide("Plan B: Rote/Grüne Karte – Aussagen", "Plan B · ausgeblendet", "Yasin", None,
          "Plan B ohne Handy: Wir lesen die Aussagen nacheinander vor. Daumen hoch heißt Stimmt, Daumen runter heißt Stimmt nicht. Auf drei zeigen alle gleichzeitig. Danach lösen wir auf.",
          "Stimmt die Aussage? (Daumen hoch oder runter)", "Lösungen auf der nächsten Folie", PLANB, hidden=True)
table(s, [["Nr.", "Aussage"]] + [[str(i + 1), r["t"]] for i, r in enumerate(D["rg"])], 0.7, 1.45, 11.9, [0.9, 11.0], 16, 0.47)
text(s, 0.7, 6.55, 11.9, 0.5, "Daumen hoch = Stimmt · Daumen runter = Stimmt nicht", 20, True, NAVY)

s = slide("Plan B: Rote/Grüne Karte – Lösungen", "Plan B · ausgeblendet", "Mido", None,
          "Hier die Lösungen mit Paragraf. Bei jeder falschen Abstimmung erklären wir die Regel kurz.",
          "Bei welcher Aussage lag die Klasse falsch? Warum?", "Begründung mit Paragraf von der Folie nennen", PLANB, hidden=True)
rows = [["Nr.", "Lösung", "Begründung"]]; fills = {}
for i, r in enumerate(D["rg"]):
    rows.append([str(i + 1), "✓ Stimmt" if r["ok"] else "✗ Stimmt nicht", r["b"]]); fills[(i + 1, 1)] = GREEN if r["ok"] else RED
table(s, rows, 0.7, 1.45, 11.9, [0.9, 2.4, 8.6], 15, 0.5, fills=fills)

s = slide("Plan B: Vertrags-Detektiv", "Plan B · ausgeblendet", "Yasin", None,
          "Plan B ohne Handy: Lest den Vertragsauszug auf der Folie. In fünf Zeilen steckt ein Fehler. Notiert die Zeilennummern und die passende Regel, wir besprechen sie danach.",
          "In welchen Zeilen steckt ein Fehler?", "Zeilen 2 bis 6 (Lösung: Folie 22)", PLANB, hidden=True)
rect(s, 0.7, 1.45, 11.9, 5.4, H("F6F8FC"), LINE); excerpt(s, 0.8, 1.5, 11.7, 15, numbers=True)

def fall_cols(s, idxs, size, x0=0.7, w=11.9, y0=1.5, h=5.4):
    cw = w / len(idxs)
    for k, i in enumerate(idxs):
        f = FAL[i]; x = x0 + k * cw
        rect(s, x, y0, cw - 0.15, h, BLUE_L); rect(s, x, y0, 0.08, h, NAVY2)
        body = [[(f["label"], True, NAVY)], f["q"]] + [[(f"{L[j]}  ", True, NAVY2), (a, False, INK)] for j, a in enumerate(f["a"])]
        text(s, x + 0.18, y0 + 0.05, cw - 0.45, h - 0.1, body, size, space=0.35)
s = slide("Plan B: IHK-Fälle A bis C", "Plan B · ausgeblendet", "Mido", None,
          "Plan B ohne Handy: Lest die Fälle A bis C. Wählt Antwort A bis D und begründet mit einer Regel. Wir besprechen die Lösungen danach auf Folie 23.",
          "Welche Antwort wählt ihr, und mit welcher Regel?", "Lösungen: A B, B C, C C (Folie 23)", PLANB, hidden=True)
fall_cols(s, [0, 1, 2], 13)
s = slide("Plan B: IHK-Fälle D und E", "Plan B · ausgeblendet", "Yasin", None,
          "Plan B ohne Handy: Lest die Fälle D und E, wählt Antwort A bis D und begründet mit einer Regel. Die Lösungen besprechen wir auf Folie 24.",
          "Welche Antwort wählt ihr, und mit welcher Regel?", "Lösungen: D B, E B (Folie 24)", PLANB, hidden=True)
fall_cols(s, [3, 4], 17)

QZ = D["quiz"]
s = slide("Plan B: Mini-Quiz – Fragen", "Plan B · ausgeblendet", "Mido", None,
          "Plan B ohne Handy: Fünf Fragen, antwortet mit A bis D auf einem Zettel. Danach lösen wir auf und zählen mit Handzeichen, wer fünf, vier, drei oder weniger richtig hat.",
          "Wer hat 5, 4, 3 oder weniger richtig? (Handzeichen)", "Zahlen aufschreiben (für den Projektbericht)", PLANB, hidden=True)
for i, q in enumerate(QZ):
    col = 0 if i < 3 else 1; row = i if i < 3 else i - 3
    x = 0.7 + col * 6.05; hh = 1.7 if col == 0 else 2.5; y = 1.45 + (row * 1.85 if col == 0 else row * 2.65)
    rect(s, x, y, 5.85, hh, BLUE_L); rect(s, x, y, 0.08, hh, NAVY2)
    text(s, x + 0.15, y + 0.03, 5.6, hh - 0.05, [[(f"{i+1}  ", True, NAVY2), (q["q"], True, NAVY)], "  ·  ".join(f"{L[j]} {a}" for j, a in enumerate(q["a"]))], 12.5, space=0.2)
s = slide("Plan B: Mini-Quiz – Lösungen", "Plan B · ausgeblendet", "Yasin", None,
          "Hier die Lösungen mit Paragraf. Zählt eure richtigen Antworten.",
          "Wo hattet ihr eine andere Antwort? Warum?", "Regel von der Folie nennen", PLANB, hidden=True)
table(s, [["Nr.", "Lösung", "Regel"]] + [[str(i + 1), f"{L[q['c']]} – {q['a'][q['c']]}", q["fb"]] for i, q in enumerate(QZ)], 0.7, 1.55, 11.9, [0.9, 7.6, 3.4], 18, 0.9)

# =================================================================== Reihenfolge: sichtbare Folien zuerst, ausgeblendete am Ende (sind bereits so angelegt)
out = os.path.join(ROOT, "output/v2/praesentation.pptx")
prs.save(out)
vis = [m for m in META if not m[4]]
print("Folien", len(META), "sichtbar", len(vis), "ausgeblendet", len(META) - len(vis))
tot = sum(m[2] for m in vis); print("Summe Dauer", mmss(tot))
json.dump(META, open("/tmp/v3_meta.json", "w"), ensure_ascii=False)
