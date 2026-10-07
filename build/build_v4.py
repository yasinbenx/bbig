# -*- coding: utf-8 -*-
import os, sys, json, math
sys.path.insert(0, os.path.dirname(__file__))
from v4lib import *

D = json.loads(open(os.path.join(ROOT, "site/js/data.js"), encoding="utf-8").read().split("=", 1)[1].rstrip().rstrip(";"))
FAL, QZ, RG, FE = D["faelle"], D["quiz"], D["rg"], D["fehler"]
Y, M = "Yasin", "Mido"
GEN = ["lösung", "✓", "musterlösung", "[fehler"]          # nie auf einer Frage-Folie
PAIRS = []                                                  # (Frage-Nr, Antwort-Nr, Titel)


def link(q, a): PAIRS.append((q._meta["nr"], a._meta["nr"], q._meta["title"])); q._meta["pair"] = a._meta["nr"]


def bullets(s, x, y, w, items, size=28, gap=0.5, h=4.5):
    return text(s, x, y, w, h, [[("•  ", True, ACC)] + [(i, False, INK)] for i in items], size, space=gap)


# =============================================================== EINSTIEG (5:00)
s = new_slide("Einstieg", "Titel", "Titel", 20, Y, "Plenum", impuls="Begrüßen, Rollen klären: Wir übernehmen heute die Stunde. Fach GP, Thema Ausbildungsvertrag.",
              med="Beamer; Tafel/Flipchart vorbereiten (Spalten a–d für Vorwissen)", puffer="nicht streichbar", dark=True, ph_idx=0)
text(s, 1.0, 1.4, 11.5, 0.6, "UNTERRICHTSSTUNDE IM FACH GP", 24, True, ACC)
text(s, 1.0, 2.0, 11.5, 2.6, "Rechte und Pflichten aus dem Ausbildungsvertrag", 54, True, WHITE, name="Titel")
rect(s, 1.0, 4.8, 2.0, 0.08, ACC); text(s, 1.0, 5.05, 11, 0.8, "Yasin & Mido", 36, False, H("DCE3F2"))

s = frage_slide("Einstieg", "Szenario: Erster Arbeitstag", "Dein erster Arbeitstag: Was steht eigentlich in deinem Ausbildungsvertrag?", 70, Y,
                "Plenum · Zuruf, Handzeichen",
                impuls="Alltagsfall erzählen („Ihr bekommt euren Vertrag und sollt unterschreiben …“). 1. Handzeichen: Wer hat seinen Vertrag schon richtig gelesen? 2. Zuruf: Was glaubt ihr, was drinstehen muss? Stichworte an die Tafel, nicht bewerten.",
                erw="Gehalt/Vergütung, Urlaub, Probezeit, Arbeitszeit, Beginn/Dauer, Kündigung.",
                fehl="„Steht alles im Gesetz, Vertrag egal“ → Nachfrage: Was darf der Vertrag dann überhaupt regeln? · Schweigen → Partnergespräch 20 s, dann erneut fragen.",
                med="Tafel: Stichwortsammlung „Vertrag“", puffer="kürzbar auf 40 s (nur Handzeichen)", forbid=GEN + ["textform", "§ 11"])
text(s, 2.3, 4.7, 10.2, 0.9, "Handzeichen: Wer hat ihn schon richtig gelesen?", 28, False, MUTED)

s = new_slide("Einstieg", "Lernziele", "Lernziele", 30, M, "Plenum", impuls="Kurz vorlesen lassen? Nein: Wir nennen das Ziel mit eigenen Worten und sagen, dass wir am Ende zu diesen vier Punkten zurückkommen (Lernziele-Check).",
              med="Beamer", puffer="kürzbar auf 15 s")
titel(s, "Lernziele: Am Ende könnt ihr …")
for i, z in enumerate(["nennen, was in einen Ausbildungsvertrag gehört", "Vergütung, Urlaub und Arbeitszeit bestimmen", "Probezeit und Kündigung richtig anwenden", "Fälle mit der passenden Regel begründen"]):
    y = 1.8 + i * 1.25
    rect(s, 0.7, y, 11.9, 1.05, LIGHT); rect(s, 0.7, y, 0.12, 1.05, ACC)
    circle(s, 1.0, y + 0.15, 0.75, i + 1, 30); text(s, 2.0, y, 10.4, 1.05, z, 30, False, INK, anchor=MSO_ANCHOR.MIDDLE)

s = new_slide("Einstieg", "Ablauf", "Ablauf der Stunde", 25, M, "Plenum", impuls="Zeitleiste in einem Satz: erst zuhören und mitdenken, dann selbst üben am Handy, dann gemeinsam besprechen. Wer hat ein Handy mit? (Handzeichen); sonst zu zweit.",
              med="Beamer", puffer="kürzbar auf 10 s")
titel(s, "So läuft die Stunde")
steps = [("Einstieg", 5), ("Erklären (3 Blöcke)", 16), ("Üben", 12), ("Besprechen", 7), ("Abschluss", 5)]
x = 0.7
for nm, m in steps:
    w = m * 0.248
    r = rect(s, x, 2.6, w - 0.05, 1.2, ACC if nm == "Üben" else NAVY2)
    text(s, x, 2.6, w - 0.05, 1.2, f"{m}", 32, True, NAVY if nm == "Üben" else WHITE, PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE)
    k = [n for n, _ in steps].index(nm)
    text(s, x - 0.6, 3.95 + (k % 2) * 0.6, w + 1.2, 0.55, nm, 24, True, NAVY, PP_ALIGN.CENTER)
    x += w
text(s, 0.7, 5.5, 11.9, 0.8, "Zeit in Minuten · Handy bereithalten", 28, False, MUTED)

s = new_slide("Einstieg", "Auftrag Vorwissen", "Auftrag Vorwissen", 15, Y, "Plenum", impuls="Auftrag erklären: Vier Fragen, jede einzeln. Ihr antwortet frei, wir schreiben mit und lösen erst am Ende der Stunde auf.",
              med="Tafel/Flipchart: vier Spalten a bis d", puffer="nicht streichbar")
titel(s, "Was wisst ihr schon?")
for i, (t, sub) in enumerate([("Vier Fragen", "jede Frage einzeln"), ("Ihr antwortet frei", "Zuruf oder Handzeichen"), ("Wir schreiben mit", "Tafel/Flipchart, noch keine Auflösung")]):
    card(s, 0.7, 1.9 + i * 1.6, 11.9, 1.4, t, sub, 32, 28, LIGHT if i != 2 else ACC_L, NAVY2 if i != 2 else ACC)
badge(s, "Plenum")

VW = [("a", "Wie lange darf die Probezeit höchstens dauern?", ["vier monate", "4 monate"], "Vier Monate (§ 20 BBiG).", "„Sechs Monate“, „ein Jahr“ → notieren, nicht korrigieren.", Y),
      ("b", "Wie viele Urlaubstage stehen einem Azubi mindestens zu?", ["24 werktage", "27 werktage", "25 werktage"], "24 Werktage ab 18 Jahren, Jugendliche 25 bis 30 (§ 3 BUrlG, § 19 JArbSchG).", "„20 Tage“ (Arbeitstage) oder „30“ → notieren; Nachfrage: Hängt es vom Alter ab?", M),
      ("c", "Welche Kündigungsfrist gilt in der Probezeit?", ["keine frist", "ohne frist", "ohne kündigungsfrist"], "Keine Frist, aber schriftlich (§ 22 Abs. 1 und 3 BBiG).", "„Vier Wochen“, „zwei Wochen“ → notieren, nicht korrigieren.", Y),
      ("d", "Muss eine Kündigung schriftlich sein?", ["ja, die kündigung muss schriftlich"], "Ja, die Kündigung muss schriftlich erfolgen; die elektronische Form ist ausgeschlossen (§ 22 Abs. 3 BBiG).", "„E-Mail reicht“ → notieren; auf die Auflösung am Ende verweisen.", M)]
for k, q, fb, er, fe, spr in VW:
    s = frage_slide("Einstieg", f"Vorwissen {k}", q, 35, spr, "Plenum · Zuruf", forbid=GEN + fb,
                    impuls=f"Frage {k} stellen, zwei bis drei Zurufe sammeln, an der Tafel unter „{k}“ notieren. Nicht auflösen – die Auflösung kommt auf der Folie „Zurück zum Anfang“.",
                    erw=er, fehl=fe, med=f"Tafel: Spalte {k}", puffer="Vorwissen b–d bei Zeitnot nur als Handzeichen")
    text(s, 0.7, 5.3, 11.9, 0.7, f"Frage {k} von d", 28, True, AMBER)

# =============================================================== BLOCK 1 (5:30): Vertrag, Dauer, Zeit, Verguetung
s = erklaer_slide("Block 1", "Vertrag § 11", "Der Vertrag: sechs Pflichtangaben", 40, Y, para="§ 11 BBiG",
                  impuls="An die Tafelsammlung anknüpfen: Was habt ihr genannt – was davon steht hier? Die sechs Felder mündlich einordnen, Textform in eigenen Worten.",
                  erw="Schüler:innen erkennen ihre Zurufe wieder.", fehl="„Vertrag muss auf Papier unterschrieben sein“ → Textform seit 01.08.2024 (z. B. E-Mail); Papierform war vorher vorgeschrieben.",
                  med="Tafelsammlung abgleichen", puffer="nicht streichbar")
pf = [("calendar", "Beginn und Dauer"), ("clock", "tägliche Ausbildungszeit"), ("hourglass", "Probezeit"), ("euro", "Vergütung"), ("palm", "Urlaub"), ("doc", "Kündigung")]
for i, (ic, t) in enumerate(pf):
    x, y = 0.7 + (i % 3) * 4.05, 1.8 + (i // 3) * 1.45
    rect(s, x, y, 3.85, 1.25, WHITE, LINE, lw=2); pic(s, IC(ic), x + 0.15, y + 0.15, 0.95, alt=f"Symbol {t}")
    text(s, x + 1.15, y, 2.7, 1.25, t, 26, True, NAVY, anchor=MSO_ANCHOR.MIDDLE)
rect(s, 0.7, 4.85, 11.9, 1.85, ACC_L); rect(s, 0.7, 4.85, 0.12, 1.85, ACC)
text(s, 1.0, 4.85, 11.5, 1.85, [[("Textform genügt ", True, NAVY), ("(seit 01.08.2024), zum Beispiel per E-Mail.", False, INK)], [("Vorher: ", True, NAVY), ("Papierform.", False, INK)]], 32, anchor=MSO_ANCHOR.MIDDLE)

q = frage_slide("Block 1", "Lückensatz Textform", "Ergänzt den Satz auf eurem Arbeitsblatt:\n„Seit dem ① genügt für den Vertragsinhalt die ② . Vorher war die ③ vorgeschrieben.“", 30, Y,
                "Einzelarbeit · Mitschreiben", size=34, forbid=GEN + ["01.08.2024", "textform", "papierform", "e-mail"],
                impuls="Lückensatz: 20 Sekunden still ausfüllen (Arbeitsblatt oder Heft), dann eine Person nennen lassen, ohne zu bewerten.",
                erw="① 01.08.2024 · ② Textform · ③ Papierform", fehl="„1. Januar“, „E-Mail“ statt Textform → beide Begriffe zeigen, Textform = lesbare Erklärung, z. B. E-Mail.",
                med="Arbeitsblatt Tafelbild (optional)", puffer="streichbar (Lückensatz Block 1)")
a = antwort_slide("Block 1", "Antwort Lückensatz", "So steht es im Gesetz (§ 11 BBiG)", 20, Y, "Plenum · Abgleichen", pair=q,
                  impuls="Antworten per Klick aufdecken, Klasse korrigiert ihr Blatt selbst.", anim_note="Klick 1: ① 01.08.2024 · Klick 2: ② Textform · Klick 3: ③ Papierform", puffer="streichbar zusammen mit der Frage")
text(s=a, x=0.9, y=1.8, w=11.5, h=1.7, t="Seit dem ① genügt für den Vertragsinhalt die ② . Vorher war die ③ vorgeschrieben.", size=34, color=INK)
chips = []
for i, t in enumerate(["① 01.08.2024", "② Textform", "③ Papierform"]):
    r = rect(a, 0.9 + i * 4.0, 4.0, 3.7, 1.4, ACC_L, ACC, MSO_SHAPE.ROUNDED_RECTANGLE, 3, name=f"Antwort_{i+1}"); text(a, 0, 0, 0, 0, t, 32, True, NAVY, PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE, shape=r); chips.append(r)
para_corner(a, "§ 11 BBiG"); animate(a, groups=[[c] for c in chips]); link(q, a)

s = erklaer_slide("Block 1", "Beginn und Dauer", "Beginn und Dauer: Zeitstrahl", 40, Y, para="§ 8, § 21 BBiG",
                  impuls="Zeitstrahl am Beamer mündlich durchgehen: Beginn → Prüfung → Ende. Frage in die Runde: Wer kann den Zeitstrahl verkürzen? (Antwort steht auf den Karten).",
                  erw="Azubi und Betrieb gemeinsam, zuständige Stelle.", fehl="„Betrieb kann allein kürzen“ → gemeinsamer Antrag nötig.", puffer="kürzbar auf 25 s")
rect(s, 1.2, 1.95, 10.9, 0.55, NAVY); text(s, 1.2, 1.95, 10.9, 0.55, "Ausbildungsdauer", 28, True, WHITE, PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE)
for xx in (1.0, 11.9): rect(s, xx, 1.9, 0.65, 0.65, ACC, NAVY, MSO_SHAPE.OVAL, 3)
text(s, 0.6, 2.6, 3, 0.5, "Beginn", 28, True, NAVY); text(s, 7.6, 2.6, 5.2, 0.5, "Prüfung", 28, True, NAVY, PP_ALIGN.RIGHT)
text(s, 6.2, 3.1, 6.6, 0.5, "Ende mit Bekanntgabe des Ergebnisses", 24, False, MUTED, PP_ALIGN.RIGHT)
card(s, 0.7, 3.75, 5.85, 3.0, "Verkürzung", "auf gemeinsamen Antrag von Azubi und Betrieb bei der zuständigen Stelle", 32, 28, GREEN_L, GREEN)
card(s, 6.75, 3.75, 5.85, 3.0, "Verlängerung", "nur in Ausnahmefällen auf Antrag des Azubis oder nach nicht bestandener Prüfung, höchstens um ein Jahr", 32, 28, ORANGE_L, ORANGE)

s = erklaer_slide("Block 1", "Ausbildungszeit", "Ausbildungszeit: Jugendliche und Volljährige", 45, Y, para="§ 8 JArbSchG · § 3 ArbZG",
                  impuls="Vergleich an der Tafel nachzeichnen: links Jugendliche (JArbSchG), rechts Volljährige (ArbZG). Ausgleich in sechs Monaten erklären.",
                  erw="–", fehl="„Jugendliche dürfen auch 10 Stunden“ → nur Volljährige, und nur mit Ausgleich.", med="Tafel: zwei Spalten", puffer="nicht streichbar")
for i, (hd, big, sub, lines, col) in enumerate([("Jugendliche", "8", "Stunden täglich", ["höchstens 40 pro Woche", "ausnahmsweise 8,5 bei Ausgleich"], NAVY), ("Volljährige", "8", "Stunden täglich", ["bis 10 mit Ausgleich (6 Monate)", "höchstens 48 pro Woche"], ACC)]):
    x = 0.7 + i * 6.05
    rect(s, x, 1.85, 5.85, 0.75, col); text(s, x + 0.2, 1.85, 5.5, 0.75, hd, 32, True, WHITE if i == 0 else NAVY, anchor=MSO_ANCHOR.MIDDLE)
    rect(s, x, 2.6, 5.85, 4.15, LIGHT)
    text(s, x, 2.7, 5.85, 1.3, big, 80, True, NAVY, PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE); text(s, x, 3.95, 5.85, 0.6, sub, 28, True, NAVY, PP_ALIGN.CENTER)
    text(s, x + 0.2, 4.7, 5.5, 2.0, [[("• ", True, ACC), (l, False, INK)] for l in lines], 28, space=0.4)

q = frage_slide("Block 1", "Verständnis Ausbildungszeit", "Wie viele Stunden dürfen Jugendliche täglich höchstens arbeiten – und wie viele pro Woche?", 25, Y,
                "Partnergespräch · Zuruf", forbid=GEN + ["8 stunden", "40 stunden", "8,5", "§ 8"],
                impuls="Eine Minute Murmelphase, dann zwei Antworten einsammeln.", erw="8 Stunden täglich, 40 pro Woche; ausnahmsweise 8,5 bei Ausgleich (§ 8 JArbSchG).",
                fehl="„10 Stunden“ (Volljährigen-Regel) → Unterschied Jugendliche/Volljährige noch einmal zeigen.", puffer="streichbar")
a = antwort_slide("Block 1", "Antwort Ausbildungszeit", "8 Stunden täglich, 40 pro Woche", 25, Y, pair=q, impuls="Aufdecken, dann Rückbezug auf den Vergleich.", anim_note="Klick 1: Antwortkasten", puffer="streichbar")
r = rect(a, 0.9, 1.9, 11.5, 2.6, ACC_L, ACC, MSO_SHAPE.ROUNDED_RECTANGLE, 3, name="Antwort_1")
text(a, 0, 0, 0, 0, [[("8 Stunden täglich, 40 pro Woche", True, NAVY)], [("Ausnahmsweise 8,5 Stunden täglich bei Ausgleich.", False, INK)]], 32, shape=r, anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
para_corner(a, "§ 8 JArbSchG"); animate(a, groups=[[r]]); link(q, a)

q = frage_slide("Block 1", "Rätsel Vergütung", "Wie hoch ist die gesetzliche Mindestausbildungsvergütung im 1. Ausbildungsjahr bei Beginn 2026?", 45, Y,
                "Murmelphase · Schätzen", forbid=GEN + ["724", "854", "977", "1.014"],
                impuls="Aufdeck-Rätsel: Schätzen lassen (Zuruf-Spanne an die Tafel). 30 Sekunden Murmelphase. Danach Denkpause und Auflösung.",
                erw="724 € (§ 17 BBiG).", fehl="Tarifvertrag/„Je nach Betrieb“ → es gibt eine gesetzliche Untergrenze. · Zu hohe Schätzungen (1.000 €) ausdrücklich würdigen.",
                med="Tafel: Schätzspanne", puffer="Murmelphase auf 15 s kürzen")
dk = denk_slide("Block 1", 15, Y, impuls="Schätzungen stehen an der Tafel; erst jetzt auflösen.")
a = antwort_slide("Block 1", "Antwort Vergütung", "Mindestausbildungsvergütung 2026", 45, Y, pair=q, impuls="Balken per Klick aufdecken: Jahr für Jahr. Frage: Wer lag richtig? Hinweis: wird jedes Jahr neu festgelegt, darf nicht unterschritten werden.",
                  erw="–", fehl="„Das ist mein Nettogehalt“ → es ist brutto, Untergrenze.", anim_note="Klick 1–4: 1.–4. Jahr (Balken und Betrag)", puffer="nicht streichbar")
bars = []
for i, (j, v) in enumerate([("1. Jahr", 724), ("2. Jahr", 854), ("3. Jahr", 977), ("4. Jahr", 1014)]):
    y = 1.75 + i * 1.08
    g1 = text(a, 0.9, y, 1.6, 0.9, j, 28, True, NAVY, anchor=MSO_ANCHOR.MIDDLE, name=f"Jahr_{i+1}")
    b = rect(a, 2.6, y, 9.4 * v / 1014, 0.9, ACC if i == 0 else NAVY2, name=f"Balken_{i+1}")
    text(a, 0, 0, 0, 0, f"{v:,} €".replace(",", "."), 30, True, NAVY if i == 0 else WHITE, PP_ALIGN.RIGHT, MSO_ANCHOR.MIDDLE, shape=b)
    bars.append([g1, b])
text(a, 0.9, 6.1, 9.5, 0.5, "Darf nicht unterschritten werden · wird jedes Jahr neu festgelegt", 24, False, MUTED)
para_corner(a, "§ 17 BBiG"); animate(a, groups=bars); link(q, a)

# =============================================================== BLOCK 2 (5:30): Urlaub, Probezeit
q = frage_slide("Block 2", "Aufstellen Werktag", "Stimmt oder stimmt nicht?\nDer Samstag zählt als Werktag.", 30, M, "Aufstellen im Raum · stimmt / stimmt nicht",
                size=44, forbid=GEN + ["sonntag", "feiertag", "kalendertage"],
                impuls="Aufstellen: Wer meint „stimmt“, steht rechts; „stimmt nicht“ links. Eine Person pro Seite begründen lassen, dann weiter.",
                erw="Stimmt: Werktage sind alle Kalendertage außer Sonntagen und gesetzlichen Feiertagen.",
                fehl="„Werktage = Montag bis Freitag“ → das sind Arbeitstage; Samstag zählt als Werktag.", med="Raum: rechts/links markieren (Zettel „Stimmt“ / „Stimmt nicht“)",
                puffer="als Handzeichen kürzen (−15 s)")
a = antwort_slide("Block 2", "Antwort Werktag", "Stimmt: Der Samstag ist ein Werktag", 35, M, pair=q, impuls="Aufdecken, danach: 24 Werktage entsprechen 20 Arbeitstagen bei der Fünf-Tage-Woche – an der Tafel zeigen.",
                  erw="–", fehl="Verwechslung Werktag/Arbeitstag → Wochenkalender anzeichnen (Mo–Sa = 6 Werktage).", anim_note="Klick 1: Definition · Klick 2: Arbeitstage-Hinweis", puffer="nicht streichbar")
r1 = rect(a, 0.9, 1.8, 11.5, 2.0, ACC_L, ACC, MSO_SHAPE.ROUNDED_RECTANGLE, 3, name="Antwort_1")
text(a, 0, 0, 0, 0, "Werktage sind alle Kalendertage außer Sonntagen und gesetzlichen Feiertagen.", 32, True, NAVY, shape=r1, anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
r2 = rect(a, 0.9, 4.1, 11.5, 1.8, LIGHT, NAVY2, MSO_SHAPE.ROUNDED_RECTANGLE, 3, name="Antwort_2")
text(a, 0, 0, 0, 0, "24 Werktage entsprechen 20 Arbeitstagen bei der Fünf-Tage-Woche.", 32, False, INK, shape=r2, anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
para_corner(a, "§ 3 BUrlG"); animate(a, groups=[[r1], [r2]]); link(q, a)

s = erklaer_slide("Block 2", "Urlaub nach Alter", "Mindesturlaub nach Alter", 55, M, para="§ 19 JArbSchG · § 3 BUrlG",
                  impuls="Balken Stufe für Stufe aufdecken: Alter zu Jahresbeginn entscheidet. Wir fragen beim Aufdecken: Wer gehört zu welcher Zeile?",
                  erw="–", fehl="„Urlaub zählt in Arbeitstagen“ → hier Werktage.", anim_note="Klick 1–4: unter 16 / unter 17 / unter 18 / ab 18", med="Tafel: Alterstreppe", puffer="nicht streichbar")
rows = []
for i, (lab, v) in enumerate([("unter 16", 30), ("unter 17", 27), ("unter 18", 25), ("ab 18", 24)]):
    y = 1.9 + i * 1.2
    t1 = text(s, 0.9, y, 2.6, 0.95, lab, 30, True, NAVY, anchor=MSO_ANCHOR.MIDDLE, name=f"Alter_{i+1}")
    b = rect(s, 3.6, y, 8.6 * v / 30, 0.95, ACC if i == 3 else NAVY2, name=f"Urlaub_{i+1}")
    text(s, 0, 0, 0, 0, f"{v} Werktage", 30, True, NAVY if i == 3 else WHITE, PP_ALIGN.RIGHT, MSO_ANCHOR.MIDDLE, shape=b); rows.append([t1, b])
text(s, 0.9, 6.55, 8, 0.5, "Alter zu Jahresbeginn", 24, False, MUTED)
animate(s, groups=rows)

q = frage_slide("Block 2", "TPS Urlaub 16 Jahre", "Wie viele Werktage Mindesturlaub hat eine Auszubildende, die zu Jahresbeginn 16 Jahre alt ist?", 35, M, "Think-Pair-Share",
                forbid=GEN + ["27", "§ 19"], impuls="Think: still überlegen. Pair: Partner:in. Share: zwei Antworten. Auf die Alterstreppe verweisen, nicht auf die Zahl.",
                erw="27 Werktage (§ 19 JArbSchG).", fehl="„30“ (unter 16) oder „24“ → Frage nach der Altersgrenze: 16 ist nicht unter 16, aber unter 17.", puffer="als Zuruf kürzen")
dk = denk_slide("Block 2", 15, M)
a = antwort_slide("Block 2", "Antwort Urlaub 16", "27 Werktage", 20, M, pair=q, impuls="Aufdecken; wer hatte 27? Wer hat sich bei 30 vertan – warum?", anim_note="Klick 1: Antwort", puffer="nicht streichbar")
r = rect(a, 0.9, 1.9, 11.5, 2.8, ACC_L, ACC, MSO_SHAPE.ROUNDED_RECTANGLE, 3, name="Antwort_1")
text(a, 0, 0, 0, 0, [[("27 Werktage", True, NAVY)], [("unter 17 Jahre zu Jahresbeginn", False, INK)]], 44, shape=r, anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
para_corner(a, "§ 19 JArbSchG"); animate(a, groups=[[r]]); link(q, a)

s = erklaer_slide("Block 2", "Probezeit", "Probezeit: ein bis vier Monate", 55, M, para="§ 20 BBiG",
                  impuls="Rückgriff auf die Tafel (Vorwissen a): Welche Schätzungen waren dabei? Monate per Klick aufdecken, bei Monat 4 stoppen.",
                  erw="–", fehl="„Probezeit = immer 3 oder 6 Monate“ → mindestens 1, höchstens 4 Monate.", anim_note="Klick 1–4: 1. bis 4. Monat", med="Tafel: Vorwissen a abgleichen", puffer="nicht streichbar")
text(s, 0.7, 1.8, 11.9, 1.2, "Jedes Ausbildungsverhältnis beginnt mit einer Probezeit.", 32, True, NAVY)
segs = []
for i in range(4):
    r = rect(s, 0.7 + i * 3.0, 3.4, 2.9, 1.5, ACC if i == 3 else NAVY2, name=f"Monat_{i+1}"); text(s, 0, 0, 0, 0, f"{i+1}. Monat", 32, True, NAVY if i == 3 else WHITE, PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE, shape=r); segs.append(r)
text(s, 0.7, 5.1, 5, 0.6, "mindestens 1 Monat", 28, False, MUTED); text(s, 7.6, 5.1, 5.0, 0.6, "höchstens 4 Monate", 28, True, NAVY, PP_ALIGN.RIGHT)
animate(s, groups=[[x] for x in segs])

q = frage_slide("Block 2", "Aufstellen Probezeit 6 Monate", "Stimmt oder stimmt nicht?\nDie Probezeit darf sechs Monate dauern, wenn der Azubi zustimmt.", 25, M, "Aufstellen · stimmt / stimmt nicht",
                size=38, forbid=GEN + ["höchstens vier", "§ 20", "4 monate"], impuls="Schnell aufstellen lassen; zwei Begründungen.",
                erw="Stimmt nicht: höchstens vier Monate (§ 20 BBiG).", fehl="„Mit Zustimmung geht mehr“ → Gesetz lässt auch mit Zustimmung nicht mehr zu.", puffer="streichbar")
a = antwort_slide("Block 2", "Antwort Probezeit 6", "Stimmt nicht: höchstens vier Monate", 20, M, pair=q, impuls="Aufdecken, auf die Monatsreihe zeigen.", anim_note="Klick 1: Antwort", puffer="streichbar")
r = rect(a, 0.9, 1.9, 11.5, 2.4, ACC_L, ACC, MSO_SHAPE.ROUNDED_RECTANGLE, 3, name="Antwort_1")
text(a, 0, 0, 0, 0, "Höchstens vier Monate, auch mit Zustimmung des Azubis.", 36, True, NAVY, shape=r, anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
para_corner(a, "§ 20 BBiG"); animate(a, groups=[[r]]); link(q, a)

s = new_slide("Block 2", "Ampelkarte", "Ampelkarte Block 2", 40, M, "Einzelarbeit · Ampelkarte hochhalten",
              impuls="Ampelkarte: Grün = kann ich erklären, Gelb = unsicher, Rot = verstehe ich nicht. Bei vielen Gelb/Rot: Alterstreppe oder Monatsreihe nochmal zeigen.",
              erw="Mehrheit Grün oder Gelb.", fehl="Wenig Rückmeldung → eine Person nach der Zahl fragen (27, 24).", med="Ampelkarten (grün/gelb/rot) oder Zettel", puffer="streichbar (−40 s)")
titel(s, "Ampelkarte: Urlaub und Probezeit")
for i, (c, t, col) in enumerate([("Grün", "kann ich erklären", GREEN), ("Gelb", "bin unsicher", H("F5A623")), ("Rot", "verstehe ich noch nicht", RED)]):
    y = 1.9 + i * 1.5
    rect(s, 0.7, y, 11.9, 1.3, LIGHT); circle(s, 1.0, y + 0.15, 1.0, "", 24, col); text(s, 2.4, y, 10.0, 1.3, [[(c + ": ", True, NAVY), (t, False, INK)]], 34, anchor=MSO_ANCHOR.MIDDLE)
badge(s, "Ampelkarte hoch")

# =============================================================== BLOCK 3 (5:00): Kuendigung, Pflichten
q = frage_slide("Block 3", "Impuls Kündigung", "Ein Azubi merkt in der Probezeit: Der Beruf passt nicht zu ihm. Was darf er tun?", 30, Y, "Murmelphase · Vermutungen sammeln",
                forbid=GEN + ["ohne frist", "ohne kündigungsfrist", "vier wochen", "§ 22"], impuls="Murmelphase 30 s; Vermutungen an die Tafel (Spalte Kündigung). Keine Wertung.",
                erw="Kündigen, jederzeit, vermutlich schriftlich.", fehl="„Man muss durchhalten“ / „vier Wochen Frist“ → notieren, später prüfen.", med="Tafel: Vermutungen Kündigung", puffer="nicht streichbar")
dk = denk_slide("Block 3", 20, Y, impuls="Vermutungen stehen an der Tafel; Auflösung folgt im Entscheidungsbaum.")
s = erklaer_slide("Block 3", "Entscheidungsbaum Kündigung", "Kündigung: Entscheidungsbaum", 60, Y, para="§ 22 Abs. 1 und 2 BBiG",
                  impuls="Baum Schritt für Schritt aufdecken (3 Klicks): erst Probezeit, dann nach der Probezeit zwei Wege. Immer wieder an die Vermutungen der Tafel anknüpfen.",
                  erw="–", fehl="„Auch nach der Probezeit jederzeit ohne Grund“ → nur fristlos aus wichtigem Grund oder 4 Wochen bei Aufgabe/Berufswechsel.",
                  anim_note="Klick 1: Probezeit → ohne Frist · Klick 2: nach Probezeit → wichtiger Grund · Klick 3: Azubi → vier Wochen", med="Tafel: Baum abzeichnen", puffer="nicht streichbar")
root = rect(s, 4.4, 1.75, 4.5, 0.85, NAVY, name="Baum_Wurzel"); text(s, 0, 0, 0, 0, "Kündigung durch …?", 28, True, WHITE, PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE, shape=root)
ln = lambda x, y, w, h, n: rect(s, x, y, w, h, MUTED, name=n)
l0 = ln(6.6, 2.6, 0.08, 0.2, "Linie_Stamm"); l1 = ln(2.5, 2.8, 4.18, 0.08, "Linie_Quer")
l2 = ln(2.5, 2.8, 0.08, 0.2, "Linie_Probezeit"); l3 = ln(6.6, 2.8, 0.08, 0.2, "Linie_Nach")
b1 = rect(s, 0.7, 3.0, 3.7, 0.8, NAVY2, name="Baum_Probezeit"); text(s, 0, 0, 0, 0, "in der Probezeit", 28, True, WHITE, PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE, shape=b1)
b2 = rect(s, 4.9, 3.0, 3.7, 0.8, NAVY2, name="Baum_Nach"); text(s, 0, 0, 0, 0, "nach der Probezeit", 28, True, WHITE, PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE, shape=b2)
k1 = ln(2.5, 3.8, 0.08, 0.5, "Linie_Ergebnis_1"); k2 = ln(6.6, 3.8, 0.08, 0.5, "Linie_Ergebnis_2"); k3 = ln(8.6, 3.36, 0.3, 0.08, "Linie_Ergebnis_3")
r1 = rect(s, 0.7, 4.3, 3.7, 2.3, GREEN_L, GREEN, lw=3, name="Ergebnis_1"); text(s, 0, 0, 0, 0, [[("jederzeit ohne Frist", True, NAVY)], "von beiden Seiten"], 28, shape=r1, anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
r2 = rect(s, 4.9, 4.3, 3.7, 2.3, ORANGE_L, ORANGE, lw=3, name="Ergebnis_2"); text(s, 0, 0, 0, 0, [[("fristlos aus wichtigem Grund", True, NAVY)], "beide Seiten"], 28, shape=r2, anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
r3 = rect(s, 8.9, 2.75, 3.7, 3.85, ACC_L, ACC, lw=3, name="Ergebnis_3"); text(s, 0, 0, 0, 0, [[("Azubi: vier Wochen Frist", True, NAVY)], "bei Aufgabe der Ausbildung oder Berufswechsel"], 28, shape=r3, anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
animate(s, groups=[[l0, l1, l2, b1, k1, r1], [l3, b2, k2, r2], [k3, r3]])

s = erklaer_slide("Block 3", "Form der Kündigung", "Form und Frist der Kündigung", 35, Y, para="§ 22 Abs. 3 und 4 BBiG",
                  impuls="Drei Karten, jede in einem Satz: schriftlich (E-Mail reicht nicht), nach der Probezeit mit Gründen, wichtiger Grund nur innerhalb von zwei Wochen nach Kenntnis.",
                  erw="–", fehl="„E-Mail genügt“ → die elektronische Form ist ausgeschlossen.", med="Tafel: Schlagwörter schriftlich / Gründe / 2 Wochen", puffer="kürzbar auf 20 s")
for i, (ic, h, b) in enumerate([("doc", "Immer schriftlich", "E-Mail ist ausgeschlossen"), ("bulb", "Mit Gründen", "nach der Probezeit"), ("clock", "Zwei Wochen", "nach Kenntnis der Gründe")]):
    x = 0.7 + i * 4.05
    rect(s, x, 1.9, 3.85, 4.7, LIGHT); rect(s, x, 1.9, 3.85, 0.12, ACC if i == 0 else NAVY2)
    pic(s, IC(ic), x + 1.3, 2.2, 1.25, alt=f"Symbol {h}"); text(s, x + 0.1, 3.7, 3.65, 0.8, h, 32, True, NAVY, PP_ALIGN.CENTER)
    text(s, x + 0.1, 4.6, 3.65, 1.8, b, 28, False, INK, PP_ALIGN.CENTER)

q = frage_slide("Block 3", "Aufstellen E-Mail", "Stimmt oder stimmt nicht?\nEine Kündigung per E-Mail ist wirksam, wenn sie rechtzeitig ankommt.", 25, Y, "Aufstellen · stimmt / stimmt nicht",
                size=38, forbid=GEN + ["§ 22", "elektronische form", "ausgeschlossen"], impuls="Aufstellen; eine Begründung je Seite.",
                erw="Stimmt nicht: Die Kündigung muss schriftlich erfolgen; die elektronische Form ist ausgeschlossen (§ 22 Abs. 3 BBiG).", fehl="„Rechtzeitig reicht“ → Form ist Wirksamkeitsvoraussetzung.", puffer="streichbar")
a = antwort_slide("Block 3", "Antwort E-Mail", "Stimmt nicht: schriftlich", 20, Y, pair=q, impuls="Aufdecken und auf die „Immer schriftlich“-Karte zurückverweisen.", anim_note="Klick 1: Antwort", puffer="streichbar")
r = rect(a, 0.9, 1.9, 11.5, 2.6, ACC_L, ACC, MSO_SHAPE.ROUNDED_RECTANGLE, 3, name="Antwort_1")
text(a, 0, 0, 0, 0, "Sie muss schriftlich erfolgen, die elektronische Form ist ausgeschlossen.", 34, True, NAVY, shape=r, anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
para_corner(a, "§ 22 Abs. 3 BBiG"); animate(a, groups=[[r]]); link(q, a)

q = frage_slide("Block 3", "Frist wichtiger Grund", "Wann muss eine Kündigung aus wichtigem Grund ausgesprochen werden?", 25, Y, "Plenum · Abstimmung A–D",
                options=["Innerhalb von vier Wochen nach Kenntnis", "Innerhalb von zwei Wochen nach Kenntnis", "Immer zum Monatsende", "Jederzeit"], size=36, opt_size=26, forbid=GEN + ["§ 22"],
                impuls="Abstimmung per Handzeichen, Verteilung an die Tafel (A–D).", erw="B: innerhalb von zwei Wochen nach Kenntnis (§ 22 Abs. 4 BBiG).",
                fehl="A (vier Wochen) → Verwechslung mit der Frist des Azubis; D → Frist gilt ab Kenntnis.", puffer="streichbar")
a = antwort_slide("Block 3", "Antwort Frist", "Antwort B: zwei Wochen nach Kenntnis", 20, Y, pair=q, impuls="Aufdecken; Abgrenzung: Vier Wochen gelten nur für die Kündigung durch den Azubi bei Aufgabe oder Berufswechsel.", anim_note="Klick 1: Antwort B", puffer="streichbar")
r = rect(a, 0.9, 1.9, 11.5, 2.6, ACC_L, ACC, MSO_SHAPE.ROUNDED_RECTANGLE, 3, name="Antwort_1")
text(a, 0, 0, 0, 0, [[("B", True, NAVY)], "Innerhalb von zwei Wochen, nachdem die Gründe bekannt wurden."], 34, shape=r, anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
para_corner(a, "§ 22 Abs. 4 BBiG"); animate(a, groups=[[r]]); link(q, a)

q = frage_slide("Block 3", "Zuruf Ausbildungsmittel", "Wer muss die Ausbildungsmittel stellen – und was darf das den Azubi kosten?", 25, Y, "Zuruf",
                forbid=GEN + ["kostenlos", "§ 14", "betrieb muss"], impuls="Zuruf; kurz sammeln, dann auflösen.", erw="Der Betrieb (Ausbildende), kostenlos (§ 14 BBiG).", fehl="„Azubi kauft Werkzeug selbst“ → Betrieb stellt kostenlos.", puffer="streichbar")
a = antwort_slide("Block 3", "Pflichten", "Pflichten: Azubi und Ausbildende", 40, Y, pair=q, impuls="Spalten per Klick aufdecken; bei Ausbildende „Ausbildungsmittel kostenlos“ als Antwort auf die Frage markieren.",
                  fehl="–", anim_note="Klick 1: Spalte Azubi · Klick 2: Spalte Ausbildende", puffer="nicht streichbar")
cA = []; cB = []
hA = rect(a, 0.7, 1.75, 5.85, 0.8, NAVY, name="Azubi_Kopf"); text(a, 0, 0, 0, 0, "Azubi (§ 13)", 32, True, WHITE, shape=hA, anchor=MSO_ANCHOR.MIDDLE)
tA = bullets(a, 0.7, 2.7, 5.85, ["lernen, sorgfältig arbeiten", "Weisungen befolgen, Ordnung beachten", "Geheimnisse wahren", "Ausbildungsnachweis führen"], 28, 0.35); tA.name = "Azubi_Liste"
hB = rect(a, 6.75, 1.75, 5.85, 0.8, ACC, name="Ausbildende_Kopf"); text(a, 0, 0, 0, 0, "Ausbildende (§§ 14–17)", 32, True, NAVY, shape=hB, anchor=MSO_ANCHOR.MIDDLE)
tB = bullets(a, 6.75, 2.7, 5.85, ["Ausbildungsziel vermitteln", "Ausbildungsmittel kostenlos stellen", "freistellen (Schule, Prüfungen)", "Zeugnis ausstellen, Vergütung zahlen"], 28, 0.35); tB.name = "Ausbildende_Liste"
animate(a, groups=[[hA, tA], [hB, tB]]); link(q, a)

# =============================================================== UEBEN (12:00)
s = new_slide("Üben", "Arbeitsauftrag Überblick", "Die Aufgaben im Überblick", 45, M, "Plenum · Auftrag erklären",
              impuls="Auftrag in eigenen Worten: Seite öffnen (QR), drei Aufgaben, Reihenfolge frei. Wer kein Handy hat, schaut zu zweit mit; Plan B: Beamer-Folien (ausgeblendet). Nach dem Erklären QR-Code 20 Sekunden stehen lassen.",
              erw="Handzeichen: Wer hat die Seite offen?", fehl="Seite lädt nicht → Plan B Folien zeigen, WLAN klären.", med="QR-Code, Beamer, Handys; Merkblatt auf dem Tisch", puffer="nicht streichbar")
titel(s, "Jetzt seid ihr dran")
qr_block(s, 0.7, 1.75, 4.6, "QR-Code zur Übungsseite der Klasse")
rect(s, 5.9, 1.75, 6.7, 0.85, NAVY); rect(s, 5.9, 1.75, 0.12, 0.85, ACC); text(s, 6.15, 1.75, 6.4, 0.85, URL_KURZ, 28, True, WHITE, anchor=MSO_ANCHOR.MIDDLE, name="URL")
for i, (t, b) in enumerate([("1  Rote/Grüne Karte", "allein"), ("2  Vertrags-Detektiv", "zu zweit"), ("3  IHK-Fälle A bis C", "in Gruppen")]):
    y = 2.85 + i * 1.12; rect(s, 5.9, y, 6.7, 1.0, LIGHT); rect(s, 5.9, y, 0.12, 1.0, NAVY2)
    text(s, 6.15, y, 4.4, 1.0, t, 28, True, NAVY, anchor=MSO_ANCHOR.MIDDLE); text(s, 10.4, y, 2.15, 1.0, b, 28, False, INK, PP_ALIGN.RIGHT, MSO_ANCHOR.MIDDLE)
rect(s, 5.9, 6.2, 6.7, 0.65, ACC_L); text(s, 6.15, 6.2, 6.4, 0.65, "Kein Handy? Schaut zu zweit mit.", 28, True, NAVY, anchor=MSO_ANCHOR.MIDDLE)

def auftrag(nr, titel_t, spr, dauer, sozial, zeit, hilfs, auftrag_t, fertig, impuls, erw="", fehl=""):
    s = new_slide("Üben", "Arbeitsauftrag", f"Aufgabe {nr}", dauer, spr, sozial, impuls=impuls, erw=erw, fehl=fehl, med="Merkblatt, Handy/Website", puffer="nicht streichbar")
    titel(s, f"Aufgabe {nr}: {titel_t}")
    text(s, 0.7, 1.85, 11.9, 1.9, auftrag_t, 30, False, INK)
    for i, (k, v, col, fg) in enumerate([("Sozialform", sozial.split(" · ")[0], NAVY, WHITE), ("Zeit", zeit, ACC, NAVY), ("Hilfsmittel", hilfs, NAVY2, WHITE)]):
        x = 0.7 + i * 4.05; rect(s, x, 3.85, 3.85, 1.7, col, shape=MSO_SHAPE.ROUNDED_RECTANGLE).adjustments[0] = 0.1
        text(s, x, 3.9, 3.85, 0.5, k, 24, True, fg, PP_ALIGN.CENTER); text(s, x, 4.4, 3.85, 1.1, v, 32, True, fg, PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE)
    rect(s, 0.7, 5.75, 11.9, 1.0, ACC_L); rect(s, 0.7, 5.75, 0.12, 1.0, ACC)
    text(s, 1.0, 5.75, 11.5, 1.0, [[("Fertig? ", True, NAVY), (fertig, False, INK)]], 26, anchor=MSO_ANCHOR.MIDDLE)
    return s
auftrag(1, "Rote/Grüne Karte", Y, 20, "Einzelarbeit", "3 Minuten", "Merkblatt", "10 Aussagen, eine pro Bildschirm: „Stimmt“ oder „Stimmt nicht“ tippen, danach die Lösung lesen.", "Aufgabe 2 beginnen.",
        "Kurz: Schnell-Check, Ergebnis wird nicht abgefragt.")
auftrag(2, "Vertrags-Detektiv", M, 25, "Partnerarbeit", "5 Minuten", "Merkblatt, Notizen", "Lest den Vertragsauszug. Tippt bis zu 5 Zeilen mit Fehlern an, prüft und begründet jeden Fehler mit der passenden Regel.", "Aufgabe 3 oder die Reserve (Fälle D, E, Experten-Karten).",
        "Ergebnissicherung: Zeilennummer + Regel + Paragraf notieren; wird gleich besprochen.", erw="Fehler in § 2 bis § 6.", fehl="Zeile 1 oder 7 als Fehler markiert → in der Besprechung erklären.")
auftrag(3, "IHK-Fälle A bis C", Y, 25, "Gruppenarbeit", "4 Minuten", "Merkblatt", "Fall lesen, Antwort A bis D wählen und mit einer Regel begründen. Merkt euch eine Frage für die Besprechung.", "Fälle D und E oder Experten-Karten auf der Website.",
        "Ergebnissicherung: Buchstabe + Regel pro Fall im Heft notieren.", erw="Fall A–C siehe Besprechung.")

s = new_slide("Üben", "Arbeitsphase", "Arbeitsphase", 605, M, "Einzel-, Partner-, Gruppenarbeit", impuls="Wir gehen durch die Reihen, helfen und merken uns typische Fehler. Zeit ansagen nach 3, 8 und 10 Minuten. Fertig? Reserve D/E, Experten-Karten.",
              erw="Typische Fehler notieren: Probezeit 6 Monate, 650 €, 9 Stunden, 20 Werktage, vier Wochen in der Probezeit.", fehl="Frust bei Technik → zu zweit mitschauen, Plan B.", med="QR-Code; Countdown-Folie laufen lassen", puffer="Arbeitsphase auf 8 Minuten verkürzbar", anim_note="Countdown-Balken läuft automatisch beim Folienwechsel (10 Segmente à 1 Minute)", ph_idx=4)
titel(s, "Arbeitsphase")
qr_block(s, 0.7, 1.7, 3.9, "QR-Code zur Übungsseite der Klasse")
rect(s, 5.2, 1.7, 7.4, 0.85, NAVY); text(s, 5.45, 1.7, 7.1, 0.85, URL_KURZ, 28, True, WHITE, anchor=MSO_ANCHOR.MIDDLE)
text(s, 5.2, 2.7, 7.4, 0.8, "Countdown", 28, False, MUTED)
text(s, 5.2, 3.2, 7.4, 1.4, "10 Min.", 72, True, NAVY, name="Countdown_Zeit")
segs = []
for i in range(10): segs.append(rect(s, 5.25 + i * 0.735, 4.65, 0.68, 0.5, ACC, name=f"Countdown_{i+1}"))
text(s, 5.2, 5.3, 7.4, 0.6, "Jedes Segment = 1 Minute", 24, False, MUTED)
rect(s, 5.2, 6.0, 7.4, 0.8, ACC_L); text(s, 5.45, 6.0, 7.1, 0.8, "Fertig? Reserve auf der Website", 28, True, NAVY, anchor=MSO_ANCHOR.MIDDLE)
animate(s, auto=segs, step_ms=60000)

# =============================================================== BESPRECHEN (7:00)
s = new_slide("Besprechen", "Auftrag Besprechung", "Wir besprechen gemeinsam", 30, Y, "Plenum", impuls="Überleitung: Handys weg oder zur Seite. Erst Vertrags-Detektiv (Fehler nennen lassen), dann drei Fälle (abstimmen, begründen). Typische Fehler aus der Arbeitsphase aufgreifen.",
              erw="–", fehl="Schüler:innen reden weiter am Handy → kurze Ansage, Blickkontakt.", med="Beamer", puffer="kürzbar auf 15 s")
titel(s, "Wir besprechen gemeinsam")
for i, (n, t) in enumerate([(1, "Vertrags-Detektiv: Wer findet die Fehler?"), (2, "IHK-Fälle A bis C: abstimmen und begründen")]):
    y = 2.0 + i * 1.6; rect(s, 0.7, y, 11.9, 1.35, LIGHT); rect(s, 0.7, y, 0.12, 1.35, ACC); circle(s, 1.0, y + 0.3, 0.75, n, 30); text(s, 2.1, y, 10.3, 1.35, t, 32, False, INK, anchor=MSO_ANCHOR.MIDDLE)
badge(s, "Plenum")

def excerpt(s, x, y, w, size):
    """Vertragsauszug (Dokumentansicht, Originaltext aus der Website, Ausnahme von der 24-pt-Regel)"""
    rect(s, x, y, w, 5.6, H("F6F8FC"), LINE, name="Vertragsauszug"); rect(s, x, y, w, 0.1, NAVY2)
    lines = D["kopf"]
    text(s, x + 0.1, y + 0.15, w - 0.2, 1.5, [[(lines[0], True, NAVY)]] + lines[1:], size, False, INK, font="Times New Roman", space=0.1, name="Vertragskopf")
    yy = y + 1.35
    for i, z in enumerate(D["zeilen"]):
        cpl = int((w - 1.0) / (size * 0.0078)); n = max(1, math.ceil(len(z["t"]) / cpl)); hh = n * size * 0.0172 + 0.14
        circle(s, x + 0.15, yy + (hh - 0.36) / 2, 0.36, i + 1, 18, NAVY, WHITE, name=f"Zeilennummer_{i+1}")
        text(s, x + 0.65, yy, w - 0.8, hh, z["t"], size, False, INK, font="Times New Roman", name=f"Zeile_{i+1}")
        yy += hh + 0.04

s = new_slide("Besprechen", "Detektiv Mitlesen", "Vertrags-Detektiv: Zum Mitlesen", 30, Y, "Plenum · Fehler nennen lassen",
              impuls="Auszug ohne jede Markierung zeigen. Klasse nennt Zeilennummern, die sie für fehlerhaft hält; noch nicht bestätigen. Sammeln: Welche Zeilen wurden am häufigsten genannt?",
              erw="Zeilen 2, 3, 4, 5, 6.", fehl="Zeile 1 oder 7 genannt → noch nicht korrigieren; in der Auflösung begründen.", med="Tafel: Zeilennummern mit Strichliste",
              puffer="nicht streichbar", forbid=GEN + ["bbig", "jarbschg", "burlg", "regel", "fehler"])
text(s, 0.6, 0.55, 12.2, 0.6, "Vertragsauszug – welche Zeilen enthalten einen Fehler?", 28, True, AMBER, name="Auftrag")
excerpt(s, 0.7, 1.2, 11.9, 17)
badge(s, "Fehler nennen")
mit = s

# Auflösung in drei Schritt-Folien (2 + 2 + 1 Fehler), je Fehler ein Klick
fz = [(i, z) for i, z in enumerate(D["zeilen"]) if z["f"]]
chunks = [(fz[0:2], 60), (fz[2:4], 60), (fz[4:5], 30)]
for ci, (ch, dur) in enumerate(chunks):
    s = antwort_slide("Besprechen", f"Detektiv Auflösung {ci+1}", f"Auflösung Vertrags-Detektiv ({ci+1} von 3)", dur, Y if ci != 1 else M, "Plenum · Gruppen berichten", pair=mit if ci == 0 else None,
                      impuls="Pro Klick ein Fehler: Wer hat ihn gefunden? Welche Regel? Dann Regel auf der Folie zeigen. " + ("Bei Fehler 3: Der Azubi ist bei Beginn 16 Jahre alt (geboren 20.11.2009). " if any(z["f"] == 3 for _, z in ch) else "") + ("Zeilen 1 und 7 sind korrekt." if ci == 2 else ""),
                      erw=" · ".join(f"Fehler {z['f']}: {FE[str(z['f'])]['regel']}" for _, z in ch),
                      fehl="Zeile 7 als Fehler markiert → Ausbildungsmittel kostenlos ist korrekt (§ 14 BBiG). Zeile 1 korrekt (drei Jahre, Beginn 01.09.2026).",
                      anim_note="; ".join(f"Klick {k+1}: Fehler {z['f']} (Fehlerzeile + Regel mit Paragraf)" for k, (_, z) in enumerate(ch)), puffer="Folie 3 von 3 streichbar (−30 s)" if ci == 2 else "kürzbar")
    groups = []
    for k, (i, z) in enumerate(ch):
        y0 = 1.8 + k * 2.55
        fe = FE[str(z["f"])]
        c1 = rect(s, 0.8, y0, 11.7, 1.2, H("FDE3E1"), RED, lw=3, name=f"Fehlerzeile_{z['f']}")
        text(s, 0, 0, 0, 0, [[(f"Fehler {z['f']}  ", True, RED), (z["t"], False, INK)]], 24, shape=c1, anchor=MSO_ANCHOR.MIDDLE, font="Times New Roman")
        c2 = rect(s, 0.8, y0 + 1.3, 11.7, 1.0, ACC_L, ACC, lw=3, name=f"Regel_Fehler_{z['f']}")
        text(s, 0, 0, 0, 0, [[("Regel: ", True, AMBER), (fe["regel"], True, NAVY)]], 28, shape=c2, anchor=MSO_ANCHOR.MIDDLE)
        groups.append([c1, c2])
    animate(s, groups=groups)
    if ci == 0: PAIRS.append((mit._meta["nr"], s._meta["nr"], mit._meta["title"])); mit._meta["pair"] = s._meta["nr"]

def fall_loesung(i, hidden=False, phase="Besprechen", dauer=40, spr=Y, q=None):
    f = FAL[i]
    a = antwort_slide(phase, f"Antwort {f['label'].split(' (')[0]}", f"{f['label'].split(' (')[0]}: Lösung {'ABCD'[f['c']]}", dauer, spr, "Plenum · Begründung nennen lassen", pair=q, hidden=hidden,
                      impuls="Abstimmung vergleichen: Wer hatte " + "ABCD"[f["c"]] + "? Eine Begründung mit Regel erfragen, dann Lösung aufdecken. Abweichende Antworten kurz erklären.",
                      erw=f"{'ABCD'[f['c']]}: {f['fb']}", fehl="Wahl einer anderen Antwort → Nachfrage: Welche Regel hat euch geleitet? Dann die Paragrafen-Karte zeigen.",
                      anim_note="Klick 1: Lösung (Buchstabe + Antworttext) · Klick 2: Begründung mit Paragraf", puffer="auf 25 s kürzbar")
    r1 = rect(a, 0.9, 1.9, 11.5, 1.8, ACC_L, ACC, MSO_SHAPE.ROUNDED_RECTANGLE, 3, name="Loesung")
    text(a, 0, 0, 0, 0, [[(f"{'ABCD'[f['c']]}  ", True, NAVY), (f["a"][f["c"]], True, NAVY)]], 30, shape=r1, anchor=MSO_ANCHOR.MIDDLE)
    r2 = rect(a, 0.9, 4.0, 11.5, 2.5, LIGHT, NAVY2, MSO_SHAPE.ROUNDED_RECTANGLE, 2, name="Begruendung")
    text(a, 0, 0, 0, 0, [[("Begründung: ", True, NAVY), (f["fb"], False, INK)]], 28, shape=r2, anchor=MSO_ANCHOR.MIDDLE)
    animate(a, groups=[[r1], [r2]]); return a
for i in range(3):
    q = fall_frage_slide("Besprechen", f"Fall {'ABC'[i]}", FAL[i], 30, Y if i % 2 == 0 else M, forbid=GEN + ["§"],
                         impuls=f"Fall in 20 Sekunden still lesen lassen, dann Abstimmung A–D per Handzeichen; Verteilung an der Tafel notieren. Eine Begründung mit Regel erfragen, noch nicht bewerten.",
                         erw=f"{'ABCD'[FAL[i]['c']]}: {FAL[i]['fb']}", fehl="Streuung der Stimmen ist normal → erst Lösung aufdecken, dann die Regel erklären.", med="Tafel: Strichliste A–D", puffer="Fall C bei Zeitnot nur Lösung (−30 s)")
    fall_loesung(i, q=q, spr=Y if i % 2 == 0 else M)
    PAIRS.append((q._meta["nr"], len(prs.slides), q._meta["title"])); q._meta["pair"] = len(prs.slides)

# =============================================================== ABSCHLUSS (5:00)
s = new_slide("Abschluss", "Merksatz", "Fünf Kernzahlen", 40, M, "Plenum · Tafelbild", impuls="Fünf Kacheln im Schnelldurchgang; nicht vorlesen, sondern abfragen: „Welche Zahl gehört zu welcher Regel?“ (Kacheln zeigen nur die Zahl, Regel mündlich).",
              erw="Probezeit 4 Monate, 724 €, 24 Werktage, schriftlich, 8 Stunden.", fehl="Zahl wird einer falschen Regel zugeordnet → Merkblatt zeigen.", med="Merkblatt (ausgeteilt)", puffer="kürzbar auf 25 s")
titel(s, "Merke dir diese fünf")
for i, (big, small, para) in enumerate([("4 Monate", "Probezeit, höchstens", "§ 20 BBiG"), ("724 €", "im 1. Jahr, Beginn 2026", "§ 17 BBiG"), ("24", "Werktage Urlaub ab 18", "§ 3 BUrlG"), ("schriftlich", "Kündigung, nie E-Mail", "§ 22 BBiG"), ("8 h", "täglich, Jugendliche", "§ 8 JArbSchG")]):
    col, row = i % 3, i // 3; x, y = 0.7 + col * 4.05, 1.85 + row * 2.55
    rect(s, x, y, 3.85, 2.35, ACC_L if i % 2 == 0 else LIGHT); rect(s, x, y, 3.85, 0.12, ACC if i % 2 == 0 else NAVY2)
    text(s, x, y + 0.2, 3.85, 1.0, big, 48, True, NAVY, PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE); text(s, x + 0.05, y + 1.25, 3.75, 0.5, small, 24, False, INK, PP_ALIGN.CENTER)
    text(s, x, y + 1.85, 3.85, 0.4, para, 24, True, AMBER, PP_ALIGN.CENTER)

s = new_slide("Abschluss", "Mini-Quiz", "Mini-Quiz", 120, M, "Einzelarbeit · Handy (Plan B: Handzeichen/Zettel)", impuls="Auftrag: fünf Fragen auf der Seite „Mini-Quiz“, allein, zwei Minuten. Danach Handzeichen: Wer hat 5, 4, 3 oder weniger? Zahlen notieren (für unsere Auswertung). Bei Zeitnot nur Fragen 1 bis 3.",
              erw="Mehrheit 4 oder 5.", fehl="Kein Handy → Plan B (ausgeblendete Folien) oder zu zweit.", med="QR-Code; Zettel/Stift für Plan B", puffer="auf 90 s kürzbar (Fragen 1–3)")
titel(s, "Mini-Quiz: Zeig, was du kannst")
qr_block(s, 0.7, 1.75, 4.3, "QR-Code zur Übungsseite der Klasse")
bullets(s, 5.6, 1.85, 7.0, ["5 Fragen", "allein", "ca. 2 Minuten"], 36, 0.7)
text(s, 5.6, 5.0, 7.0, 0.8, URL_KURZ, 28, True, NAVY); text(s, 5.6, 5.8, 7.0, 0.8, "Danach: Handzeichen 5 · 4 · 3 oder weniger", 28, False, MUTED)

s = antwort_slide("Abschluss", "Zurück zum Anfang", "Zurück zum Anfang", 45, Y, "Plenum · Vergleich mit der Tafel", impuls="Jede Frage per Klick auflösen und mit den Tafelnotizen vergleichen: Was war richtig? Was war neu? Frage an alle: Was war neu für euch?",
                  erw="a Vier Monate · b 24 Werktage ab 18 Jahren, Jugendliche 25 bis 30 · c Keine Frist, aber schriftlich · d Ja, schriftlich.", fehl="Tafelantworten falsch → nicht bloßstellen, Lernzuwachs betonen.",
                  anim_note="Klick 1–4: Antwort a bis d", med="Tafel: Vorwissen a–d", puffer="auf 30 s kürzbar (nur a und c)")
rows = []
for i, (k, q_, _, ans, _, _) in enumerate(VW):
    y = 1.8 + i * 1.2; rect(s, 0.8, y, 11.8, 1.05, LIGHT); circle(s, 0.95, y + 0.17, 0.7, k, 28)
    text(s, 1.85, y, 5.0, 1.05, q_, 24, True, NAVY, anchor=MSO_ANCHOR.MIDDLE)
    r = rect(s, 7.0, y + 0.07, 5.5, 0.9, ACC_L, ACC, lw=2.5, name=f"Antwort_{k}")
    short = {"a": "Vier Monate", "b": "24 Werktage ab 18, Jugendliche 25 bis 30", "c": "Keine Frist, aber schriftlich", "d": "Ja, schriftlich (§ 22 Abs. 3 BBiG)"}[k]
    text(s, 0, 0, 0, 0, short, 24, True, NAVY, shape=r, anchor=MSO_ANCHOR.MIDDLE); rows.append([r])
animate(s, groups=rows)

s = new_slide("Abschluss", "Lernziele-Check", "Lernziele-Check", 25, Y, "Einzelarbeit · Ampelkarte", impuls="Ampelkarte zu jedem der vier Lernziele: Grün/Gelb/Rot. Ziele einzeln aufrufen, Kärtchen hochhalten lassen; Rot/Gelb notieren für die Website-Übung.",
              erw="Überwiegend Grün/Gelb.", fehl="Viele Rot → Hinweis auf Merkblatt und Website zum Weiterüben.", med="Ampelkarten", puffer="auf 15 s kürzbar")
titel(s, "Was könnt ihr jetzt? (Ampelkarte)")
for i, z in enumerate(["nennen, was in einen Ausbildungsvertrag gehört", "Vergütung, Urlaub und Arbeitszeit bestimmen", "Probezeit und Kündigung richtig anwenden", "Fälle mit der passenden Regel begründen"]):
    y = 1.8 + i * 1.25; rect(s, 0.7, y, 11.9, 1.05, LIGHT); rect(s, 0.7, y, 0.12, 1.05, ACC); circle(s, 1.0, y + 0.15, 0.75, i + 1, 30); text(s, 2.0, y, 10.4, 1.05, z, 30, False, INK, anchor=MSO_ANCHOR.MIDDLE)

q = frage_slide("Abschluss", "Blitzlicht", "Blitzlicht: Was nehme ich aus dieser Stunde mit – und was fehlt mir noch?", 40, M, "Plenum · Blitzlicht (ein Satz)",
                impuls="Offene Frage; jede:r sagt einen Satz oder eine Person pro Reihe. Rückmeldungen mitschreiben (für unsere Auswertung).", erw="Offene Antworten, z. B. Zahlen, Fristen, Website.",
                fehl="Schweigen → Partnergespräch 15 s, dann Reihe für Reihe.", med="Notizzettel", puffer="auf 20 s kürzbar (drei Stimmen)", forbid=GEN)

s = new_slide("Abschluss", "Dank", "Danke", 30, Y, "Plenum", impuls="Danken, Merkblatt und Website nennen: Üben geht jederzeit weiter. Fragen? Danach Aufräumen.",
              med="QR-Code, Merkblatt", puffer="nicht streichbar", dark=True, ph_idx=6)
text(s, 1.0, 0.9, 11, 0.6, "VIELEN DANK!", 24, True, ACC)
text(s, 1.0, 1.6, 7.2, 2.0, "Danke fürs Mitmachen!", 54, True, WHITE)
bullets_x = [("Merkblatt", "mitnehmen"), ("Website", URL_KURZ)]
for i, (a_, b_) in enumerate(bullets_x):
    text(s, 1.0, 3.9 + i * 1.1, 7.2, 1.0, [[(a_ + ": ", True, ACC), (b_, False, WHITE)]], 30)
qr_block(s, 8.9, 1.5, 3.6, "QR-Code zur Übungsseite der Klasse")
text(s, 8.7, 5.5, 4.0, 0.8, "Weiter üben", 28, True, ACC, PP_ALIGN.CENTER)

# =============================================================== AUSGEBLENDET: Reserve und Plan B
s = new_slide("Üben", "Reserve", "Reserve: Schnell fertig?", None, M, "Partnerarbeit", impuls="Nur zeigen, wenn jemand schneller fertig ist. Experten-Karten: Thema wählen, Partner:in in einer Minute erklären, dann Frage lösen. Oder Fälle D und E.",
              erw="–", med="Website", puffer="Reserve – nicht Teil der 45 Minuten", hidden=True, ph_idx=4)
titel(s, "Reserve: Schnell fertig?")
for i, t in enumerate(["Experten-Karten auf der Website öffnen", "Thema wählen und der Partnerin / dem Partner in einer Minute erklären", "Frage lösen", "Oder: Fälle D und E bearbeiten"]):
    y = 1.8 + i * 1.2; circle(s, 0.9, y + 0.1, 0.8, i + 1, 30); text(s, 2.0, y, 10.5, 1.0, t, 30, False, INK, anchor=MSO_ANCHOR.MIDDLE)
text(s, 0.7, 6.6, 11, 0.5, URL_KURZ, 24, True, NAVY)
for i in (3, 4):
    q = fall_frage_slide("Besprechen", f"Reserve {FAL[i]['label'].split(' (')[0]}", FAL[i], None, Y, hidden=True, forbid=GEN + ["§"], impuls="Nur wenn bearbeitet oder Zeit übrig. Abstimmung A–D, dann Lösung.",
                         erw=f"{'ABCD'[FAL[i]['c']]}: {FAL[i]['fb']}", puffer="Reserve")
    a = fall_loesung(i, hidden=True, dauer=None, q=q); PAIRS.append((q._meta["nr"], a._meta["nr"], q._meta["title"])); q._meta["pair"] = a._meta["nr"]

# Plan B Rote/Gruene Karte (24 pt, je 5 Aussagen)
def planb_rg(part, loes):
    sl = RG[(part - 1) * 5: part * 5]
    kind = "Antwort" if loes else "Frage"
    s = new_slide("Üben", kind, f"Plan B Rote/Grüne Karte {'Lösungen' if loes else 'Aussagen'} {part}", None, Y if part == 1 else M, "Plenum · Daumen hoch / Daumen runter",
                  impuls=("Lösungen vorlesen lassen, Begründung mit Paragraf nennen." if loes else "Aussage vorlesen, Daumen hoch = stimmt, Daumen runter = stimmt nicht; auf „drei“ gleichzeitig."),
                  erw="Lösung siehe Folie nach der Abstimmung." if not loes else "–", med="Plan B ohne Handy/Internet", puffer="nur bei Ausfall", hidden=True,
                  forbid=None if loes else GEN + ["§", "stimmt nicht –"], ph_idx=4)
    rect(s, 0.45, 0.62, 12.43, 6.2, None, ACC, lw=6) if loes else None
    text(s, 0.7, 0.6, 11.2, 0.85, f"Plan B: {'Lösungen' if loes else 'Aussagen'} {(part-1)*5+1}–{part*5}", 40, True, NAVY, name="Titel", anchor=MSO_ANCHOR.MIDDLE)
    for i, r in enumerate(sl):
        y = 1.6 + i * 1.04; rect(s, 0.7, y, 11.9, 0.95, LIGHT)
        circle(s, 0.8, y + 0.1, 0.75, (part - 1) * 5 + i + 1, 24)
        if loes:
            text(s, 1.75, y, 10.8, 0.95, [[("✓ Stimmt – " if r["ok"] else "✗ Stimmt nicht – ", True, GREEN if r["ok"] else RED), (r["b"], False, INK)]], 24, anchor=MSO_ANCHOR.MIDDLE)
        else:
            text(s, 1.75, y, 10.8, 0.95, r["t"], 24, True, NAVY, anchor=MSO_ANCHOR.MIDDLE, name=f"Aussage_{(part-1)*5+i+1}")
    return s
for part in (1, 2):
    q = planb_rg(part, False); a = planb_rg(part, True); PAIRS.append((q._meta["nr"], a._meta["nr"], q._meta["title"])); q._meta["pair"] = a._meta["nr"]

# Plan B Mini-Quiz
for i, qq in enumerate(QZ):
    q = frage_slide("Abschluss", f"Plan B Quiz {i+1}", qq["q"], None, M if i % 2 == 0 else Y, "Einzelarbeit · A–D auf Zettel", options=qq["a"], size=30, opt_size=24, hidden=True, forbid=GEN + ["§"],
                    impuls="Plan B ohne Handy: Frage zeigen, A–D auf Zettel notieren; Lösung folgt auf der Lösungsfolie.", erw=f"{'ABCD'[qq['c']]}: {qq['a'][qq['c']]} ({qq['fb']})", puffer="nur bei Ausfall")
    q._meta["title"] = f"Plan B Mini-Quiz Frage {i+1}"
a = antwort_slide("Abschluss", "Plan B Quiz Lösungen", "Plan B: Mini-Quiz Lösungen", None, Y, "Plenum · Zählen mit Handzeichen", hidden=True, impuls="Lösungen mit Regel; Handzeichen: Wer hat 5, 4, 3 oder weniger richtig?", puffer="nur bei Ausfall")
for i, qq in enumerate(QZ):
    y = 1.6 + i * 1.05; rect(a, 0.7, y, 11.9, 0.95, LIGHT); circle(a, 0.8, y + 0.1, 0.75, i + 1, 24)
    text(a, 1.75, y, 10.8, 0.95, [[(f"{'ABCD'[qq['c']]}  ", True, NAVY), (qq["a"][qq["c"]], False, INK), (f"  ({qq['fb']})", False, AMBER)]], 24, anchor=MSO_ANCHOR.MIDDLE)
for m in META:
    if m["title"].startswith("Plan B Mini-Quiz Frage"): m["pair"] = a._meta["nr"]; PAIRS.append((m["nr"], a._meta["nr"], m["title"]))

def find(title): return next(m for m in META if m["title"] == title)
for m in META:
    if m["title"].startswith("Vorwissen ") and m["kind"] == "Frage":
        m["pair"] = find("Zurück zum Anfang")["nr"]; PAIRS.append((m["nr"], m["pair"], m["title"]))
sz = find("Szenario: Erster Arbeitstag"); sz["pair"] = find("Der Vertrag: sechs Pflichtangaben")["nr"]; PAIRS.append((sz["nr"], sz["pair"], sz["title"]))
ik = find("Impuls Kündigung"); ik["pair"] = find("Kündigung: Entscheidungsbaum")["nr"]; PAIRS.append((ik["nr"], ik["pair"], ik["title"]))
find("Blitzlicht")["pair"] = "offen"; PAIRS.append((find("Blitzlicht")["nr"], "offen", "Blitzlicht (offene Frage)"))
out_dir = os.path.join(ROOT, "output/v3"); os.makedirs(out_dir, exist_ok=True)
prs.save(os.path.join(out_dir, "praesentation_unterricht_v3.pptx"))
json.dump(dict(meta=META, pairs=PAIRS), open("/tmp/v4_meta.json", "w"), ensure_ascii=False)
vis = [m for m in META if not m["hidden"]]
print("Folien", len(META), "sichtbar", len(vis), "ausgeblendet", len(META) - len(vis))
tot = {}
for m in vis: tot[m["phase"]] = tot.get(m["phase"], 0) + m["dauer"]
print({k: mmss(v) for k, v in tot.items()}, "Summe", mmss(sum(tot.values())))
for k, v in tot.items():
    if v != PH_TARGET[k]: print("ABWEICHUNG", k, mmss(v), "Soll", mmss(PH_TARGET[k]))
