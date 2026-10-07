# -*- coding: utf-8 -*-
"""Praesentation v4 (schlank): 6 Phasen, 22 sichtbare + 5 ausgeblendete Folien. Inhalte aus site/js/data.js."""
import os, sys, json, math
sys.path.insert(0, os.path.dirname(__file__))
import v4lib
from v4lib import *
from PIL import ImageFont

v4lib.PHASES[:] = ["Einstieg", "Fragerunde", "Erklären", "Aufgaben", "Besprechen", "Quiz & Abschluss"]
v4lib.PH_W = [1, 1.1, 1, 1.05, 1.15, 1.7]
PH = v4lib.PHASES
D = json.loads(open(os.path.join(ROOT, "site/js/data.js"), encoding="utf-8").read().split("=", 1)[1].rstrip().rstrip(";"))
FAL, QZ, RG, FE = D["faelle"], D["quiz"], D["rg"], D["fehler"]
Y, M = "Yasin", "Mido"
GEN = ["lösung", "✓", "musterlösung", "[fehler", "begründung"]
FP = {False: "/usr/share/fonts/truetype/crosextra/Carlito-Regular.ttf", True: "/usr/share/fonts/truetype/crosextra/Carlito-Bold.ttf"}
SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
_f = {}


def nlines(t, size, width_in, bold=False, serif=False):
    key = (serif, bold, size)
    if key not in _f: _f[key] = ImageFont.truetype(SERIF if serif else FP[bold], int(size * 8))
    f = _f[key]; maxw = (width_in - 0.2) * 72 * 8; n, cur = 1, ""
    for w in t.split(" "):
        c = (cur + " " + w).strip()
        if f.getlength(c) <= maxw or not cur: cur = c
        else: n += 1; cur = w
    return n


hgt = lambda n, size: n * size * 1.2 / 72 + 0.14
PAIRS = []


def mk(phase, kind, title, dauer, spr, sozial, stich="", erw="", hint="", hidden=False, forbid=None, dark=False, anim_note="", label=None):
    s = new_slide(phase, kind, title, dauer, spr, sozial, impuls=stich, erw=erw, puffer=hint, hidden=hidden, forbid=forbid, dark=dark, anim_note=anim_note, label=label)
    return s


def lines(items, size=28):
    return text  # (platzhalter, nicht benutzt)


def bl(s, x, y, w, items, size=28, gap=0.35, h=4.0):
    return text(s, x, y, w, h, [[("•  ", True, ACC)] + [(i, False, INK)] for i in items], size, space=gap)


# =============================================================== 1 EINSTIEG
s = mk("Einstieg", "Titel", "Titel", 15, Y, "Plenum", "Begrüßen, Rollen klären: Wir halten heute die Stunde (Fach GP).", hint="nicht streichbar", dark=True)
text(s, 1.0, 1.4, 11.5, 0.6, "UNTERRICHTSSTUNDE IM FACH GP", 24, True, ACC)
text(s, 1.0, 2.0, 11.5, 2.6, "Rechte und Pflichten aus dem Ausbildungsvertrag", 54, True, WHITE, name="Titel")
rect(s, 1.0, 4.8, 2.0, 0.08, ACC); text(s, 1.0, 5.05, 11, 0.8, "Yasin & Mido", 36, False, H("DCE3F2"))

s = mk("Einstieg", "Frage", "Aufhänger und Lernziele", 105, Y, "Plenum · Zuruf",
       "Szenario kurz erzählen, 2–3 Zurufe sammeln (Stichworte an die Tafel). Lernziele in eigenen Worten nennen; Ablaufstreifen zeigen: erst Vorwissen, dann Erklären, Üben, Besprechen.",
       "Gehalt/Vergütung, Urlaub, Probezeit, Arbeitszeit, Beginn/Dauer, Kündigung.", "nicht streichbar (Zuruf auf 30 s kürzbar)", forbid=GEN + ["textform", "§", "vier monate"])
pic(s, IC("question"), 0.6, 0.7, 1.0, alt="Fragezeichen-Symbol")
text(s, 1.8, 0.62, 11.0, 1.25, "Dein erster Arbeitstag: Was steht eigentlich in deinem Ausbildungsvertrag?", 34, True, NAVY, anchor=MSO_ANCHOR.MIDDLE, name="Frage")
text(s, 0.7, 1.95, 11.9, 0.5, "Am Ende der Stunde könnt ihr …", 28, True, AMBER)
for i, z in enumerate(["nennen, was in einen Ausbildungsvertrag gehört", "Vergütung, Urlaub, Arbeitszeit, Probezeit und Kündigung anwenden", "Fälle mit der passenden Regel begründen"]):
    y = 2.5 + i * 1.0; rect(s, 0.7, y, 11.9, 0.92, LIGHT); rect(s, 0.7, y, 0.12, 0.92, ACC)
    circle(s, 1.0, y + 0.15, 0.62, i + 1, 24); text(s, 1.85, y, 10.6, 0.92, z, 28, False, INK, anchor=MSO_ANCHOR.MIDDLE)
strip = [("Einstieg", "2"), ("Fragerunde", "3"), ("Erklären", "12"), ("Aufgaben", "13"), ("Besprechen", "7"), ("Quiz &\nAbschluss", "5")]
for i, (nm, mi) in enumerate(strip):
    x = 0.7 + i * 1.99; rect(s, x, 5.5, 1.9, 1.35, NAVY if i != 3 else ACC)
    text(s, x, 5.5, 1.9, 0.5, mi + " Min.", 28, True, WHITE if i != 3 else NAVY, PP_ALIGN.CENTER)
    t = text(s, x, 5.98, 1.9, 0.85, nm.split("\n"), 24, False, WHITE if i != 3 else NAVY, PP_ALIGN.CENTER, space=0)

# =============================================================== 2 FRAGERUNDE
s = mk("Fragerunde", "Frage", "Was wisst ihr schon?", 150, M, "Plenum · Zuruf, Tafel",
       "Vier Fragen nacheinander stellen, Antworten frei zurufen lassen, an der Tafel in Spalten a–d notieren, NICHT auflösen. Auflösung auf Folie 20.",
       "a) vier Monate · b) 24 Werktage ab 18 Jahren (Jugendliche 25 bis 30) · c) keine Frist · d) ja, schriftlich. Typische Fehlvorstellungen: sechs Monate; 20 Tage; vier Wochen; E-Mail genügt. Reaktion: notieren, nachfragen „Wie kommst du darauf?“, nicht korrigieren.",
       "nicht streichbar", forbid=GEN + ["vier monate", "4 monate", "24 werktage", "25 bis 30", "keine frist", "ohne frist", "§", "antwort"])
text(s, 0.6, 0.6, 12.2, 0.95, "Was wisst ihr schon?", 40, True, NAVY, anchor=MSO_ANCHOR.MIDDLE, name="Titel"); rect(s, 0.7, 1.5, 1.6, 0.07, ACC)
VW = ["Wie lange darf die Probezeit höchstens dauern?", "Wie viele Urlaubstage stehen einem Azubi mindestens zu?", "Welche Kündigungsfrist gilt in der Probezeit?", "Muss eine Kündigung schriftlich sein?"]
for i, q in enumerate(VW):
    col, row = i % 2, i // 2; x, y = 0.7 + col * 6.05, 1.85 + row * 2.45
    rect(s, x, y, 5.85, 2.25, LIGHT); rect(s, x, y, 0.12, 2.25, ACC)
    circle(s, x + 0.3, y + 0.25, 0.75, "abcd"[i], 28); text(s, x + 0.35, y + 1.0, 5.4, 1.2, q, 28, True, NAVY, anchor=MSO_ANCHOR.MIDDLE, name=f"Frage_{'abcd'[i]}")
badge(s, "Zuruf · Tafel")

# =============================================================== 3 ERKLAEREN (9 Folien)
def erkl(title, dauer, spr, para, stich, hint, rb=None):
    s = mk("Erklären", "Erklärfolie", title, dauer, spr, "Plenum · Zuhören", stich, hint=hint)
    titel(s, title); para_corner(s, para); return s


s = erkl("Der Vertrag: sechs Pflichtangaben", 90, Y, "§ 11 BBiG", "Frei erklären: was gehört in den Vertrag, Tafelsammlung abgleichen. Textform kurz einordnen (E-Mail genügt, vorher Papier). Optionale Rückfrage (nur mündlich): Was davon habt ihr genannt?", "nicht streichbar")
for i, (ic, t) in enumerate([("calendar", "Beginn und Dauer"), ("clock", "tägliche Ausbildungszeit"), ("hourglass", "Probezeit"), ("euro", "Vergütung"), ("palm", "Urlaub"), ("doc", "Kündigung")]):
    x, y = 0.7 + (i % 2) * 6.05, 1.75 + (i // 2) * 1.05
    rect(s, x, y, 5.85, 0.93, WHITE, LINE, lw=2); pic(s, IC(ic), x + 0.12, y + 0.1, 0.72, alt=f"Symbol {t}"); text(s, x + 1.0, y, 4.8, 0.93, t, 28, True, NAVY, anchor=MSO_ANCHOR.MIDDLE)
rect(s, 0.7, 5.05, 11.9, 1.75, ACC_L); rect(s, 0.7, 5.05, 0.12, 1.75, ACC)
text(s, 1.0, 5.05, 11.5, 1.75, [[("Textform genügt ", True, NAVY), ("(seit 01.08.2024), zum Beispiel per E-Mail.", False, INK)], [("Vorher: ", True, NAVY), ("Papierform.", False, INK)]], 30, anchor=MSO_ANCHOR.MIDDLE)

s = erkl("Beginn und Dauer", 70, Y, "§ 8, § 21 BBiG", "Zeitstrahl durchgehen: Beginn → Prüfung. Verkürzung nur gemeinsam; Verlängerung Ausnahme. Optionale Rückfrage: Wer beantragt die Verkürzung?", "streichbar: nein (kürzbar auf 50 s)")
rect(s, 1.2, 1.9, 10.9, 0.55, NAVY); text(s, 1.2, 1.9, 10.9, 0.55, "Ausbildungsdauer", 28, True, WHITE, PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE)
for xx in (1.0, 11.9): rect(s, xx, 1.85, 0.65, 0.65, ACC, NAVY, MSO_SHAPE.OVAL, 3)
text(s, 0.6, 2.55, 3, 0.5, "Beginn", 28, True, NAVY); text(s, 7.6, 2.55, 5.2, 0.5, "Prüfung", 28, True, NAVY, PP_ALIGN.RIGHT)
text(s, 4.6, 3.05, 8.2, 0.5, "Ende mit Bekanntgabe des Ergebnisses", 24, False, MUTED, PP_ALIGN.RIGHT)
card(s, 0.7, 3.7, 5.85, 3.15, "Verkürzung", "auf gemeinsamen Antrag von Azubi und Betrieb bei der zuständigen Stelle", 32, 28, GREEN_L, GREEN)
card(s, 6.75, 3.7, 5.85, 3.15, "Verlängerung", "nur in Ausnahmefällen auf Antrag des Azubis oder nach nicht bestandener Prüfung, höchstens um ein Jahr", 32, 28, ORANGE_L, ORANGE)

s = erkl("Ausbildungszeit", 70, Y, "§ 8 JArbSchG · § 3 ArbZG", "Vergleich links/rechts erklären, Ausgleich in sechs Monaten kurz. Optionale Rückfrage: Wie viele Stunden dürfen Jugendliche täglich?", "nicht streichbar")
for i, (hd, lines_, col) in enumerate([("Jugendliche", ["8 Stunden täglich", "höchstens 40 pro Woche", "ausnahmsweise 8,5 bei Ausgleich"], NAVY), ("Volljährige", ["8 Stunden täglich", "bis 10 mit Ausgleich (6 Monate)", "höchstens 48 pro Woche"], ACC)]):
    x = 0.7 + i * 6.05; rect(s, x, 1.75, 5.85, 0.8, col); text(s, x + 0.2, 1.75, 5.5, 0.8, hd, 32, True, WHITE if i == 0 else NAVY, anchor=MSO_ANCHOR.MIDDLE)
    rect(s, x, 2.55, 5.85, 4.25, LIGHT); text(s, x + 0.2, 2.75, 5.5, 3.9, [[("• ", True, ACC), (l, j == 0, NAVY if j == 0 else INK)] for j, l in enumerate(lines_)], 30, space=0.5)

s = erkl("Mindestausbildungsvergütung 2026", 70, Y, "§ 17 BBiG", "Balken erklären: Beginn 2026, steigt mit dem Ausbildungsjahr. Darf nicht unterschritten werden, wird jedes Jahr neu festgelegt. Optionale Rückfrage: Wie hoch im 3. Jahr?", "streichbar: nein")
for i, (j, v) in enumerate([("1. Jahr", 724), ("2. Jahr", 854), ("3. Jahr", 977), ("4. Jahr", 1014)]):
    y = 1.8 + i * 1.12; text(s, 0.7, y, 1.8, 0.9, j, 30, True, NAVY, anchor=MSO_ANCHOR.MIDDLE)
    b = rect(s, 2.6, y, 9.6 * v / 1014, 0.9, ACC if i == 0 else NAVY2); text(s, 0, 0, 0, 0, f"{v:,} €".replace(",", "."), 32, True, NAVY if i == 0 else WHITE, PP_ALIGN.RIGHT, MSO_ANCHOR.MIDDLE, shape=b)
text(s, 0.7, 6.3, 11.9, 0.6, "Darf nicht unterschritten werden · wird jedes Jahr neu festgelegt", 28, False, MUTED)

s = erkl("Urlaub nach Alter", 95, M, "§ 19 JArbSchG · § 3 BUrlG", "Alterstreppe erklären (Alter zu Jahresbeginn), dann Werktage-Hinweis; 24 Werktage = 20 Arbeitstage. Optionale Rückfrage: Zählt der Samstag als Werktag? (ja)", "streichbar: nein")
for i, (lab, v) in enumerate([("unter 16", 30), ("unter 17", 27), ("unter 18", 25), ("ab 18", 24)]):
    y = 1.7 + i * 0.95; text(s, 0.7, y, 2.4, 0.8, lab, 30, True, NAVY, anchor=MSO_ANCHOR.MIDDLE)
    b = rect(s, 3.2, y, 9.0 * v / 30, 0.8, ACC if i == 3 else NAVY2); text(s, 0, 0, 0, 0, f"{v} Werktage", 30, True, NAVY if i == 3 else WHITE, PP_ALIGN.RIGHT, MSO_ANCHOR.MIDDLE, shape=b)
rect(s, 0.7, 5.6, 11.9, 1.25, ACC_L); rect(s, 0.7, 5.6, 0.12, 1.25, ACC)
text(s, 1.0, 5.6, 11.5, 1.25, [[("Werktage: ", True, NAVY), ("alle Kalendertage außer Sonntagen und gesetzlichen Feiertagen. 24 Werktage = 20 Arbeitstage bei der Fünf-Tage-Woche.", False, INK)]], 28, anchor=MSO_ANCHOR.MIDDLE)

s = erkl("Probezeit", 50, M, "§ 20 BBiG", "Monatsreihe zeigen: mindestens 1, höchstens 4 Monate; mit Vorwissen a von der Tafel vergleichen (nicht auflösen, erst Folie 20). Optionale Rückfrage: Darf sie sechs Monate dauern? (nein)", "streichbar: nein (kürzbar auf 35 s)")
text(s, 0.7, 1.8, 11.9, 1.2, "Jedes Ausbildungsverhältnis beginnt mit einer Probezeit.", 32, True, NAVY)
for i in range(4):
    r = rect(s, 0.7 + i * 3.0, 3.3, 2.9, 1.5, ACC if i == 3 else NAVY2); text(s, 0, 0, 0, 0, f"{i+1}. Monat", 32, True, NAVY if i == 3 else WHITE, PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE, shape=r)
text(s, 0.7, 5.0, 5, 0.6, "mindestens 1 Monat", 28, False, MUTED); text(s, 7.6, 5.0, 5.0, 0.6, "höchstens 4 Monate", 28, True, NAVY, PP_ALIGN.RIGHT)

s = erkl("Kündigung: Entscheidungsbaum", 105, Y, "§ 22 Abs. 1 und 2 BBiG", "Baum von oben nach unten erklären: Probezeit → jederzeit ohne Frist; danach nur fristlos aus wichtigem Grund oder durch den Azubi mit vier Wochen Frist (Aufgabe/Berufswechsel). Optionale Rückfrage: Welche Frist hat der Azubi nach der Probezeit?", "streichbar: nein")
root = rect(s, 4.4, 1.7, 4.5, 0.85, NAVY); text(s, 0, 0, 0, 0, "Kündigung durch …?", 28, True, WHITE, PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE, shape=root)
ln = lambda x, y, w, h: rect(s, x, y, w, h, MUTED)
ln(6.6, 2.55, 0.08, 0.25); ln(2.5, 2.8, 4.18, 0.08); ln(2.5, 2.8, 0.08, 0.25); ln(6.6, 2.8, 0.08, 0.25)
b1 = rect(s, 0.7, 3.05, 3.7, 0.8, NAVY2); text(s, 0, 0, 0, 0, "in der Probezeit", 28, True, WHITE, PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE, shape=b1)
b2 = rect(s, 4.9, 3.05, 3.7, 0.8, NAVY2); text(s, 0, 0, 0, 0, "nach der Probezeit", 28, True, WHITE, PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE, shape=b2)
ln(2.5, 3.85, 0.08, 0.45); ln(6.6, 3.85, 0.08, 0.45); ln(8.6, 3.4, 0.3, 0.08)
r1 = rect(s, 0.7, 4.3, 3.7, 2.5, GREEN_L, GREEN, lw=3); text(s, 0, 0, 0, 0, [[("jederzeit ohne Frist", True, NAVY)], "von beiden Seiten"], 28, shape=r1, anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
r2 = rect(s, 4.9, 4.3, 3.7, 2.5, ORANGE_L, ORANGE, lw=3); text(s, 0, 0, 0, 0, [[("fristlos aus wichtigem Grund", True, NAVY)], "beide Seiten"], 28, shape=r2, anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
r3 = rect(s, 8.9, 2.75, 3.7, 4.05, ACC_L, ACC, lw=3); text(s, 0, 0, 0, 0, [[("Azubi: vier Wochen Frist", True, NAVY)], "bei Aufgabe der Ausbildung oder Berufswechsel"], 28, shape=r3, anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)

s = erkl("Kündigung: Form und Frist", 60, Y, "§ 22 Abs. 3 und 4 BBiG", "Drei Karten, je ein Satz: schriftlich (E-Mail ausgeschlossen), nach der Probezeit mit Gründen, wichtiger Grund nur innerhalb von zwei Wochen nach Kenntnis. Optionale Rückfrage: Reicht eine E-Mail? (nein)", "streichbar: nein (kürzbar auf 45 s)")
for i, (ic, h, b) in enumerate([("doc", "Immer schriftlich", "E-Mail ist ausgeschlossen"), ("bulb", "Mit Gründen", "nach der Probezeit"), ("clock", "Zwei Wochen", "nach Kenntnis der Gründe")]):
    x = 0.7 + i * 4.05; rect(s, x, 1.8, 3.85, 5.0, LIGHT); rect(s, x, 1.8, 3.85, 0.12, ACC if i == 0 else NAVY2)
    pic(s, IC(ic), x + 1.3, 2.15, 1.25, alt=f"Symbol {h}"); text(s, x + 0.1, 3.65, 3.65, 0.8, h, 32, True, NAVY, PP_ALIGN.CENTER); text(s, x + 0.15, 4.55, 3.55, 1.9, b, 28, False, INK, PP_ALIGN.CENTER)

s = erkl("Pflichten von Azubi und Ausbildenden", 80, Y, "§§ 13–17 BBiG", "Zwei Spalten erklären. Vollständig: Azubi lernen, sorgfältig arbeiten, Weisungen befolgen, Ordnung beachten, Geheimnisse wahren, Ausbildungsnachweis führen; Ausbildende Ausbildungsziel vermitteln, Ausbildungsmittel kostenlos stellen, für Berufsschule und Prüfungen freistellen, Zeugnis ausstellen, Vergütung zahlen. Optionale Rückfrage: Wer stellt die Ausbildungsmittel? (Betrieb, kostenlos)", "streichbar: nein")
rect(s, 0.7, 1.75, 5.85, 0.8, NAVY); text(s, 0.9, 1.75, 5.5, 0.8, "Azubis (§ 13)", 32, True, WHITE, anchor=MSO_ANCHOR.MIDDLE)
rect(s, 6.75, 1.75, 5.85, 0.8, ACC); text(s, 6.95, 1.75, 5.5, 0.8, "Ausbildende (§§ 14–17)", 32, True, NAVY, anchor=MSO_ANCHOR.MIDDLE)
bl(s, 0.7, 2.75, 5.85, ["lernen", "sorgfältig arbeiten", "Weisungen befolgen", "Geheimnisse wahren", "Ausbildungsnachweis führen"], 28, 0.45, 4.0)
bl(s, 6.75, 2.75, 5.85, ["Ziel vermitteln", "Mittel kostenlos stellen", "freistellen (Schule, Prüfung)", "Zeugnis ausstellen", "Vergütung zahlen"], 28, 0.45, 4.0)

# =============================================================== 4 AUFGABEN
s = mk("Aufgaben", "Auftrag", "Aufgabenüberblick", 45, M, "Plenum · Auftrag erklären",
       "Seite per QR öffnen (QR-Code 20 Sekunden stehen lassen), drei Aufgaben, Reihenfolge frei. Wer kein Handy hat, schaut zu zweit mit. Handzeichen: Wer ist drauf?", "Hilfsmittel: Merkblatt. Fertig? Reserve auf der Website (Fälle D, E, Experten-Karten).", "streichbar: nein")
text(s, 0.6, 0.58, 12.2, 0.95, "Jetzt seid ihr dran", 40, True, NAVY, anchor=MSO_ANCHOR.MIDDLE, name="Titel"); rect(s, 0.7, 1.5, 1.6, 0.07, ACC)
qr_block(s, 0.7, 1.75, 3.7, "QR-Code zur Übungsseite der Klasse"); text(s, 0.55, 5.9, 4.5, 0.9, URL_KURZ, 24, True, NAVY, name="URL")
for i, (t, so, ze) in enumerate([("1  Rote/Grüne Karte", "allein", "3 Min."), ("2  Vertrags-Detektiv", "zu zweit", "5 Min."), ("3  IHK-Fälle A–C", "zu zweit", "4 Min.")]):
    y = 1.75 + i * 1.12; rect(s, 5.2, y, 7.4, 1.0, LIGHT); rect(s, 5.2, y, 0.12, 1.0, NAVY2)
    text(s, 5.45, y, 3.7, 1.0, t, 28, True, NAVY, anchor=MSO_ANCHOR.MIDDLE)
    for k, (lbl, col, fg) in enumerate([(so, NAVY, WHITE), (ze, ACC, NAVY)]):
        rect(s, 9.15 + k * 1.75, y + 0.27, 1.65, 0.46, col, shape=MSO_SHAPE.ROUNDED_RECTANGLE).adjustments[0] = 0.4; text(s, 9.15 + k * 1.75, y + 0.27, 1.65, 0.46, lbl, 24, True, fg, PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE)
text(s, 5.2, 5.15, 7.4, 0.6, [[("Hilfsmittel: ", True, NAVY), ("Merkblatt", False, INK)]], 28)
rect(s, 5.2, 5.75, 7.4, 1.1, ACC_L); rect(s, 5.2, 5.75, 0.12, 1.1, ACC)
text(s, 5.45, 5.75, 7.1, 1.1, [[("Schnell fertig? ", True, NAVY), ("Reserve auf der Website.", False, INK)], [("Kein Handy? ", True, NAVY), ("Schaut zu zweit mit.", False, INK)]], 28, anchor=MSO_ANCHOR.MIDDLE, space=0.1)

s = mk("Aufgaben", "Arbeitsphase", "Arbeitsphase", 720, Y, "Allein / zu zweit",
       "Countdown läuft automatisch (12 Segmente, eines je Minute). Durch die Reihen gehen, helfen, typische Fehler merken. Zeit ansagen nach 3, 8 und 12 Minuten.",
       "Typische Fehler für die Besprechung notieren (Probezeit 6 Monate, 650 €, 9 Stunden, 20 Werktage, vier Wochen in der Probezeit).", "streichbar: Arbeitsphase auf 9 Minuten kürzbar (−3 Min.)",
       anim_note="Countdown-Balken läuft automatisch beim Folienwechsel: Segment 1–12, je 60 Sekunden")
text(s, 0.6, 0.58, 12.2, 0.95, "Arbeitsphase", 40, True, NAVY, anchor=MSO_ANCHOR.MIDDLE, name="Titel"); rect(s, 0.7, 1.5, 1.6, 0.07, ACC)
qr_block(s, 0.7, 1.75, 3.9, "QR-Code zur Übungsseite der Klasse"); text(s, 0.55, 6.15, 4.6, 0.7, URL_KURZ, 24, True, NAVY)
text(s, 5.4, 1.7, 7.2, 0.6, "Countdown", 28, False, MUTED); text(s, 5.4, 2.2, 7.2, 1.5, "12 Min.", 80, True, NAVY, name="Countdown_Zeit")
segs = [rect(s, 5.45 + i * 0.6, 3.85, 0.55, 0.6, ACC, name=f"Countdown_{i+1}") for i in range(12)]
text(s, 5.4, 4.5, 7.2, 0.6, "Jedes Segment = 1 Minute", 24, False, MUTED)
for i, t in enumerate(["Rote/Grüne Karte · 3 Min.", "Vertrags-Detektiv · 5 Min.", "IHK-Fälle A–C · 4 Min."]):
    circle(s, 5.45, 5.15 + i * 0.58, 0.45, i + 1, 22); text(s, 6.1, 5.1 + i * 0.58, 6.5, 0.55, t, 28, False, INK, anchor=MSO_ANCHOR.MIDDLE)
animate(s, auto=segs, step_ms=60000)

# =============================================================== 5 BESPRECHEN
def excerpt(s, x, y, w, size, h):
    rect(s, x, y, w, h, H("F6F8FC"), LINE, name="Vertragsauszug"); rect(s, x, y, w, 0.1, NAVY2)
    text(s, x + 0.1, y + 0.15, w - 0.2, 1.4, [[(D["kopf"][0], True, NAVY)]] + D["kopf"][1:], size, False, INK, font="Times New Roman", space=0.1, name="Vertragskopf")
    yy = y + 0.2 + hgt(4, size) + 0.05
    for i, z in enumerate(D["zeilen"]):
        n = nlines(z["t"], size, w - 0.8, serif=True); hh = hgt(n, size)
        circle(s, x + 0.15, yy + (hh - 0.36) / 2, 0.36, i + 1, 18, NAVY, WHITE, name=f"Zeilennummer_{i+1}")
        text(s, x + 0.65, yy, w - 0.8, hh, z["t"], size, False, INK, font="Times New Roman", name=f"Zeile_{i+1}"); yy += hh + 0.03
    return yy


s = mk("Besprechen", "Frage", "Vertragsauszug", 45, Y, "Plenum · Zuruf",
       "Auszug ohne Markierung zeigen, Klasse nennt Zeilennummern, Strichliste an der Tafel. Noch nicht bestätigen. Dann Klick-Folge auf Folie 16.",
       "Zeilen 2, 3, 4, 5, 6 enthalten Fehler. Fehlvorstellung: Zeile 1 oder 7 genannt → in der Auflösung begründen.", "nicht streichbar",
       forbid=GEN + ["bbig", "jarbschg", "burlg", "regel:", "fehler 1", "fehler 2", "fehler 3", "fehler 4", "fehler 5"])
text(s, 0.6, 0.55, 12.2, 0.7, "Welche Zeilen enthalten einen Fehler?", 36, True, NAVY, anchor=MSO_ANCHOR.MIDDLE, name="Frage")
yy = excerpt(s, 0.7, 1.3, 11.9, 18, 5.45); badge(s, "Zuruf: Zeilennummern")
mit = s

# Aufloesung Detektiv: ALLE 5 Fehler auf einer Folie, je Klick eine Zeile + Regel
s = antwort_slide("Besprechen", "Detektiv Auflösung", "Auflösung: die 5 Fehler", 135, M, "Plenum · Gruppen berichten", pair=mit,
                  impuls="Pro Klick ein Fehler: Wer hat ihn gefunden? Welche Regel? Fehler 3: Der Azubi ist bei Beginn 16 Jahre alt (geboren 20.11.2009). Zeilen 1 und 7 sind korrekt.",
                  erw="Fehler 1: höchstens vier Monate (§ 20 BBiG) · 2: mindestens 724 € im 1. Jahr (§ 17 BBiG) · 3: Jugendliche höchstens 8 Stunden täglich und 40 pro Woche (§ 8 JArbSchG) · 4: mindestens 24 Werktage, Jugendliche 25 bis 30 (§ 3 BUrlG, § 19 JArbSchG) · 5: in der Probezeit jederzeit ohne Frist, schriftlich (§ 22 Abs. 1 und 3 BBiG)",
                  puffer="streichbar: nein (Fehler 3–5 kürzbar)", anim_note="Klick 1–5: Fehler 1 bis 5 (Fehlerzeile rot markiert + Regel mit Paragraf), Reihenfolge § 2, § 3, § 4, § 5, § 6")
fz = [(i, z) for i, z in enumerate(D["zeilen"]) if z["f"]]
for ls, rs in ((18, 22), (17, 22), (16, 20), (15, 20), (14, 18)):
    rows = []
    for i, z in fz:
        L = hgt(nlines(f"Fehler {z['f']}  " + z["t"], ls, 5.7, serif=True), ls); R = hgt(nlines("Regel: " + FE[str(z["f"])]["regel"], rs, 6.1, True), rs)
        rows.append(max(L, R))
    if sum(rows) + 0.1 * 4 <= 5.25: break
y0 = 1.58; groups = []
for (i, z), rh in zip(fz, rows):
    c1 = rect(s, 0.8, y0, 5.7, rh, H("FDE3E1"), RED, lw=3, name=f"Reveal_Fehlerzeile_{z['f']}")
    text(s, 0, 0, 0, 0, [[(f"Fehler {z['f']}  ", True, RED), (z["t"], False, INK)]], ls, shape=c1, anchor=MSO_ANCHOR.MIDDLE, font="Times New Roman")
    c2 = rect(s, 6.6, y0, 6.0, rh, ACC_L, ACC, lw=3, name=f"Reveal_Regel_{z['f']}")
    text(s, 0, 0, 0, 0, [[("Regel: ", True, AMBER), (FE[str(z["f"])]["regel"], True, NAVY)]], rs, shape=c2, anchor=MSO_ANCHOR.MIDDLE)
    groups.append([c1, c2]); y0 += rh + 0.1
animate(s, groups=groups)
PAIRS.append((mit._meta["nr"], s._meta["nr"], "Vertragsauszug"))
print("Auflösung Schrift:", ls, rs, "Höhe", round(sum(rows) + 0.4, 2))

# Faelle A-C
def fall_slide(i, dauer, spr, hint):
    f = FAL[i]; nm = f["label"].split(" (")[0]
    s = mk("Besprechen", "Fall", f["label"], dauer, spr, "Plenum · Abstimmung A–D per Handzeichen",
           "Fall lesen lassen, Abstimmung A–D per Handzeichen (Verteilung an der Tafel), eine Begründung mit Regel erfragen, dann Klick 1 (Lösung) und Klick 2 (Begründung).",
           f"{'ABCD'[f['c']]}: {f['fb']}", hint, forbid=GEN + ["§"], anim_note="Klick 1: Lösung markieren (grüner Rahmen + Haken) · Klick 2: Begründung mit Paragraf")
    for fs in (24, 23, 22):
        n0 = nlines(f["label"] + " " + f["q"], fs, 11.7); h0 = hgt(n0 + 0, fs) + 0.3
        oh = [max(hgt(nlines(a, fs, 10.6), fs), 0.62) for a in f["a"]]; bg = hgt(nlines("Begründung: " + f["fb"], fs + 2, 11.7), fs + 2) + 0.05
        if 0.62 + h0 + 0.1 + sum(oh) + 0.08 * 4 + 0.1 + bg <= 6.82: break
    y = 0.62; rect(s, 0.7, y, 11.9, h0, LIGHT); rect(s, 0.7, y, 0.12, h0, ACC)
    text(s, 0.95, y, 11.5, h0, [[(f["label"] + "  ", True, AMBER), (f["q"], True, NAVY)]], fs, anchor=MSO_ANCHOR.MIDDLE, name="Fall"); y += h0 + 0.1
    ys = []
    for k, a in enumerate(f["a"]):
        rect(s, 0.7, y, 11.9, oh[k], WHITE, NAVY, MSO_SHAPE.ROUNDED_RECTANGLE, 2).adjustments[0] = 0.15
        circle(s, 0.82, y + (oh[k] - 0.5) / 2, 0.5, "ABCD"[k], 22); text(s, 1.55, y, 10.95, oh[k], a, fs, False, INK, anchor=MSO_ANCHOR.MIDDLE, name=f"Option_{'ABCD'[k]}")
        ys.append(y); y += oh[k] + 0.08
    c = f["c"]
    hl = rect(s, 0.65, ys[c] - 0.04, 12.0, oh[c] + 0.08, None, GREEN, MSO_SHAPE.ROUNDED_RECTANGLE, 5, name="Reveal_Markierung"); hl.adjustments[0] = 0.15
    tk = rect(s, 11.2, ys[c] + (oh[c] - 0.5) / 2, 1.3, 0.5, GREEN, shape=MSO_SHAPE.ROUNDED_RECTANGLE, name="Reveal_Haken"); text(s, 0, 0, 0, 0, "✓ " + "ABCD"[c], 24, True, WHITE, PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE, shape=tk)
    y += 0.02; r = rect(s, 0.7, y, 11.9, bg, GREEN_L, GREEN, lw=3, name="Reveal_Begruendung")
    text(s, 0, 0, 0, 0, [[("Begründung: ", True, GREEN), (f["fb"], False, INK)]], fs + 2, shape=r, anchor=MSO_ANCHOR.MIDDLE)
    animate(s, groups=[[hl, tk], [r]]); badge(s, "Abstimmung A–D")
    return s, fs
sA, f1 = fall_slide(0, 70, Y, "streichbar: nein"); sB, f2 = fall_slide(1, 70, M, "streichbar: ja (Fall B bei Zeitnot)"); sC, f3 = fall_slide(2, 70, Y, "streichbar: ja (Fall C bei Zeitnot)")
print("Fall-Schrift:", f1, f2, f3)

# =============================================================== 6 QUIZ & ABSCHLUSS
s = antwort_slide("Quiz & Abschluss", "Zurück zum Anfang", "Zurück zum Anfang", 75, Y, "Plenum · Vergleich mit der Tafel",
                  impuls="Pro Klick eine Antwort, mit den Tafelnotizen vergleichen. Dann Frage an die Klasse: „Was war neu für euch?“",
                  erw="a Vier Monate · b 24 Werktage ab 18 Jahren, Jugendliche 25 bis 30 · c Keine Frist, aber schriftlich · d Ja, die Kündigung muss schriftlich erfolgen (§ 22 Abs. 3 BBiG). Freie Antworten zu „Was war neu?“",
                  puffer="streichbar: nein (kürzbar auf 50 s)", anim_note="Klick 1–4: Antwort a, b, c, d")
ans = {"a": "Vier Monate", "b": "24 Werktage ab 18 Jahren, Jugendliche 25 bis 30", "c": "Keine Frist, aber schriftlich", "d": "Ja, die Kündigung muss schriftlich erfolgen"}
groups = []
for i, q in enumerate(VW):
    k = "abcd"[i]; y = 1.6 + i * 1.12; rect(s, 0.8, y, 11.8, 1.0, LIGHT); circle(s, 0.95, y + 0.14, 0.72, k, 28)
    text(s, 1.85, y, 5.0, 1.0, q, 24, True, NAVY, anchor=MSO_ANCHOR.MIDDLE)
    r = rect(s, 6.95, y + 0.06, 5.55, 0.88, ACC_L, ACC, lw=2.5, name=f"Reveal_Antwort_{k}")
    text(s, 0, 0, 0, 0, ans[k], 26 if k in "ad" else 28, True, NAVY, shape=r, anchor=MSO_ANCHOR.MIDDLE); groups.append([r])
rect(s, 0.8, 6.1, 11.8, 0.7, ACC_L); text(s, 1.0, 6.1, 11.4, 0.7, "Was war neu für euch?", 30, True, NAVY, anchor=MSO_ANCHOR.MIDDLE)
animate(s, groups=groups)

s = mk("Quiz & Abschluss", "Quiz", "Mini-Quiz", 150, M, "Einzelarbeit · Handy",
       "Mini-Quiz auf der Website (5 Fragen), allein, ca. 3 Minuten, währenddessen kein Foliensprung. Danach Handzeichen: 5, 4, 3 oder weniger richtig? Zahlen notieren.",
       "Mehrheit 4 oder 5 richtig.", "streichbar: nein (Fragen 1–3 genügen bei Zeitnot)")
text(s, 0.6, 0.58, 12.2, 0.95, "Mini-Quiz: Zeig, was du kannst", 40, True, NAVY, anchor=MSO_ANCHOR.MIDDLE, name="Titel"); rect(s, 0.7, 1.5, 1.6, 0.07, ACC)
qr_block(s, 0.7, 1.75, 4.3, "QR-Code zur Übungsseite der Klasse")
bl(s, 5.7, 1.85, 7.0, ["5 Fragen auf der Website", "allein", "ca. 3 Minuten"], 36, 0.6, 3.0)
text(s, 5.7, 4.5, 7.0, 0.7, URL_KURZ, 28, True, NAVY); rect(s, 5.7, 5.4, 6.9, 1.2, ACC_L); rect(s, 5.7, 5.4, 0.12, 1.2, ACC)
text(s, 5.95, 5.4, 6.6, 1.2, "Danach: Handzeichen 5 · 4 · 3 · weniger richtig", 28, True, NAVY, anchor=MSO_ANCHOR.MIDDLE)

s = mk("Quiz & Abschluss", "Frage", "Merksatz und Abschluss", 45, Y, "Plenum · Blitzlicht",
       "Fünf Kernzahlen im Schnelldurchgang, Merkblatt zeigen (ausgeteilt). Blitzlicht: eine offene Frage, ein Satz pro Person oder Reihe. Danken, Website nennen.",
       "Offene Antworten (z. B. Zahlen, Fristen, Website).", "streichbar: nein (Blitzlicht auf drei Stimmen kürzbar)", forbid=GEN)
text(s, 0.6, 0.55, 12.2, 0.8, "Merke dir diese fünf", 40, True, NAVY, anchor=MSO_ANCHOR.MIDDLE, name="Titel"); rect(s, 0.7, 1.35, 1.6, 0.07, ACC)
for i, (big, small, para) in enumerate([("4 Monate", "Probezeit, höchstens", "§ 20 BBiG"), ("724 €", "im 1. Jahr, Beginn 2026", "§ 17 BBiG"), ("24", "Werktage Urlaub ab 18", "§ 3 BUrlG"), ("schriftlich", "Kündigung, nie E-Mail", "§ 22 BBiG"), ("8 h", "täglich, Jugendliche", "§ 8 JArbSchG")]):
    col, row = i % 3, i // 3; x, y = 0.7 + col * 4.05, 1.6 + row * 1.95
    rect(s, x, y, 3.85, 1.8, ACC_L if i % 2 == 0 else LIGHT); rect(s, x, y, 3.85, 0.1, ACC if i % 2 == 0 else NAVY2)
    text(s, x, y + 0.12, 3.85, 0.8, big, 40, True, NAVY, PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE); text(s, x + 0.05, y + 0.95, 3.75, 0.4, small, 24, False, INK, PP_ALIGN.CENTER); text(s, x, y + 1.35, 3.85, 0.4, para, 24, True, AMBER, PP_ALIGN.CENTER)
rect(s, 8.8, 3.55, 3.85, 1.8, NAVY); text(s, 8.8, 3.55, 3.85, 1.8, [[("Merkblatt", True, ACC)], [("zum Mitnehmen", False, WHITE)]], 32, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
rect(s, 0.7, 5.5, 8.0, 1.35, ACC_L); rect(s, 0.7, 5.5, 0.12, 1.35, ACC)
text(s, 0.95, 5.5, 7.7, 1.35, [[("Blitzlicht: ", True, NAVY), ("Was nehme ich aus dieser Stunde mit – und was fehlt mir noch?", False, INK)]], 28, anchor=MSO_ANCHOR.MIDDLE)
rect(s, 8.9, 5.5, 3.75, 1.35, WHITE, LINE); pic(s, QR, 9.0, 5.58, 1.2, 1.2, "QR-Code zur Übungsseite der Klasse")
text(s, 10.25, 5.5, 2.4, 1.35, [[("Danke!", True, NAVY)], [("Weiter üben", False, INK)]], 24, anchor=MSO_ANCHOR.MIDDLE, space=0.1)

# =============================================================== AUSGEBLENDET (Plan B, 5 Folien)
PLB = "NUR ANZEIGEN, wenn Internet oder Handys ausfallen."
s = mk("Aufgaben", "Frage", "Plan B: Rote/Grüne Karte (Aussagen)", None, Y, "Plenum · Daumen hoch/runter", "Aussage für Aussage vorlesen; Daumen hoch = stimmt, Daumen runter = stimmt nicht; auf „drei“ gleichzeitig. Dann Lösungsfolie.", "Lösungen auf der nächsten Folie.", PLB, hidden=True, forbid=GEN + ["§", "stimmt nicht –"])
text(s, 0.6, 0.58, 12.2, 0.8, "Plan B: Stimmt oder stimmt nicht?", 36, True, NAVY, anchor=MSO_ANCHOR.MIDDLE, name="Titel")
for i, r in enumerate(RG):
    y = 1.4 + i * 0.55; rect(s, 0.7, y, 11.9, 0.5, LIGHT); text(s, 0.75, y, 0.6, 0.5, str(i + 1), 20, True, NAVY, PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE); text(s, 1.4, y, 11.1, 0.5, r["t"], 18, True, NAVY, anchor=MSO_ANCHOR.MIDDLE, name=f"Aussage_{i+1}")
text(s, 0.7, 6.95, 11.9, 0.45, "Daumen hoch = Stimmt · Daumen runter = Stimmt nicht", 24, True, NAVY)
q1 = s
s = antwort_slide("Aufgaben", "Plan B RG Lösungen", "Plan B: Lösungen", None, M, "Plenum", pair=q1, hidden=True, impuls="Lösungen mit Paragraf vorlesen lassen.", puffer=PLB)
for i, r in enumerate(RG):
    y = 1.4 + i * 0.55; rect(s, 0.7, y, 11.9, 0.5, LIGHT); text(s, 0.75, y, 0.6, 0.5, str(i + 1), 20, True, NAVY, PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE)
    text(s, 1.4, y, 11.1, 0.5, [[("✓ Stimmt – " if r["ok"] else "✗ Stimmt nicht – ", True, GREEN if r["ok"] else RED), (r["b"], False, INK)]], 18, anchor=MSO_ANCHOR.MIDDLE)
PAIRS.append((q1._meta["nr"], s._meta["nr"], "Plan B Rote/Grüne Karte"))
s = mk("Besprechen", "Frage", "Plan B: Vertrags-Detektiv", None, Y, "Plenum · Zuruf", "Auszug zeigen, Zeilennummern nennen lassen; Auflösung mündlich mit der Fehlerliste aus den Notizen von Folie 16.", "Zeilen 2–6.", PLB, hidden=True,
       forbid=GEN + ["bbig", "jarbschg", "burlg", "regel:", "fehler 1", "fehler 2", "fehler 3", "fehler 4", "fehler 5"])
text(s, 0.6, 0.55, 12.2, 0.7, "Plan B: Welche Zeilen enthalten einen Fehler?", 36, True, NAVY, anchor=MSO_ANCHOR.MIDDLE, name="Frage")
excerpt(s, 0.7, 1.3, 11.9, 18, 5.45)
q2 = s
s = mk("Quiz & Abschluss", "Frage", "Plan B: Mini-Quiz Fragen", None, M, "Einzelarbeit · A–D auf Zettel", "Fünf Fragen zeigen, A–D auf Zettel notieren, danach Lösungsfolie; Handzeichen 5/4/3/weniger.", "Lösungen auf der nächsten Folie.", PLB, hidden=True, forbid=GEN + ["§"])
text(s, 0.6, 0.55, 12.2, 0.7, "Plan B: Mini-Quiz", 36, True, NAVY, anchor=MSO_ANCHOR.MIDDLE, name="Titel")
for i, q in enumerate(QZ):
    y = 1.3 + i * 1.12; rect(s, 0.7, y, 11.9, 1.05, LIGHT); rect(s, 0.7, y, 0.1, 1.05, NAVY2)
    text(s, 0.9, y, 11.6, 1.05, [[(f"{i+1}  ", True, AMBER), (q["q"], True, NAVY)], "   ·   ".join(f"{'ABCD'[j]} {a}" for j, a in enumerate(q["a"]))], 17, anchor=MSO_ANCHOR.MIDDLE, space=0.1, name=f"Quizfrage_{i+1}")
q3 = s
s = antwort_slide("Quiz & Abschluss", "Plan B Quiz Lösungen", "Plan B: Quiz-Lösungen", None, Y, "Plenum", pair=q3, hidden=True, impuls="Lösungen mit Regel; Handzeichen 5/4/3/weniger.", puffer=PLB)
for i, q in enumerate(QZ):
    y = 1.6 + i * 1.02; rect(s, 0.7, y, 11.9, 0.92, LIGHT)
    text(s, 0.9, y, 11.6, 0.92, [[(f"{i+1}  {'ABCD'[q['c']]}  ", True, NAVY), (q["a"][q["c"]], False, INK), (f"  ({q['fb']})", False, AMBER)]], 22, anchor=MSO_ANCHOR.MIDDLE)
PAIRS.append((q3._meta["nr"], s._meta["nr"], "Plan B Mini-Quiz"))
# Reihenfolge: ausgeblendete Folien liegen schon am Ende; Plan-B-Detektiv hat keine Antwortfolie (Auflösung = Folie 16)
q2._meta["pair"] = mit._meta["nr"] + 1

# Frage-Paare (Vorwissen, Szenario -> Folie 20)
def find(t): return next(m for m in META if m["title"] == t)
for t, tgt in (("Aufhänger und Lernziele", "Zurück zum Anfang"), ("Was wisst ihr schon?", "Zurück zum Anfang")):
    m = find(t); m["pair"] = find(tgt)["nr"]; PAIRS.append((m["nr"], m["pair"], t))
find("Merksatz und Abschluss")["pair"] = "offen"; PAIRS.append((find("Merksatz und Abschluss")["nr"], "offen", "Merksatz/Blitzlicht (offene Frage)"))
PAIRS.append((q2._meta["nr"], q2._meta["pair"], "Plan B Vertrags-Detektiv"))

out_dir = os.path.join(ROOT, "output/v3"); os.makedirs(out_dir, exist_ok=True)
prs.save(os.path.join(out_dir, "praesentation_unterricht_v4.pptx"))
json.dump(dict(meta=META, pairs=PAIRS), open("/tmp/v5_meta.json", "w"), ensure_ascii=False)
vis = [m for m in META if not m["hidden"]]; tot = sum(m["dauer"] for m in vis)
ph = {}
for m in vis: ph[m["phase"]] = ph.get(m["phase"], 0) + m["dauer"]
print("Folien", len(META), "sichtbar", len(vis), "ausgeblendet", len(META) - len(vis))
print({k: mmss(v) for k, v in ph.items()}, "Summe", mmss(tot))
