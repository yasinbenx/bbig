# -*- coding: utf-8 -*-
"""booklet_v4.pdf und merkblatt_v4.pdf: Aufbau folgt der Unterrichtspraesentation v4."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from html import escape as esc
from pdfkit import *
from data2 import *
from site_data import EXPERTEN
import render_pdf
OUT = os.path.join(os.path.dirname(__file__), "..", "output", "v4"); os.makedirs(OUT, exist_ok=True)
P = []
LOES1, LOES2 = 13, 14
FRAGEN = [("a", "Wie lange darf die Probezeit höchstens dauern?", "Vier Monate"),
          ("b", "Wie viele Urlaubstage stehen einem Azubi mindestens zu?", "24 Werktage ab 18 Jahren, Jugendliche 25 bis 30"),
          ("c", "Welche Kündigungsfrist gilt in der Probezeit?", "Keine Frist, aber schriftlich"),
          ("d", "Muss eine Kündigung schriftlich sein?", "Ja, die Kündigung muss schriftlich erfolgen (§ 22 Abs. 3 BBiG)")]
def lines(n, h="7mm"): return "".join(f'<div style="height:{h};border-bottom:0.3mm solid #BFC6D6"></div>' for _ in range(n))
def notes(n=4, label="Meine Notizen", h="7mm"):
    return f'<div style="margin-top:4mm"><div style="font-size:9pt;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:{MUTED}">{label}</div>{lines(n,h)}</div>'
def tag(t): return f'<span style="margin-left:auto;background:{ACCENT};color:{NAVY};font-weight:700;font-size:9pt;border-radius:1.2mm;padding:.4mm 2.2mm;white-space:nowrap">{esc(t)}</span>'
def thema(nr, titel, par, inner, mt="0"):
    return (f'<div style="border:0.4mm solid #D5D9E3;border-radius:2.5mm;margin-top:{mt};overflow:hidden"><div style="background:{NAVY};color:#fff;padding:1.8mm 4mm;display:flex;align-items:center;gap:3mm">'
            f'<span style="background:{ACCENT};color:{NAVY};font-weight:700;border-radius:50%;width:6.4mm;height:6.4mm;text-align:center;line-height:6.4mm;font-size:10pt">{nr}</span>'
            f'<span style="font-weight:700;font-size:12pt">{esc(titel)}</span>{tag(par)}</div><div style="padding:3mm 4.5mm;font-size:10.3pt;line-height:1.4">{inner}</div></div>')
def ul(xs, fs="10.3pt"): return f'<ul class="l" style="margin:0 0 0 4.5mm;font-size:{fs}">' + "".join(f'<li style="margin-bottom:.8mm">{x}</li>' for x in xs) + "</ul>"
def kv_row(items, cols=None):
    cols = cols or len(items)
    return f'<div style="display:grid;grid-template-columns:repeat({cols},1fr);gap:3mm">' + "".join(
        f'<div style="border-left:1.4mm solid {c};background:#F6F8FC;border-radius:0 2mm 2mm 0;padding:2mm 3.2mm"><div style="font-weight:700;color:{NAVY};font-size:10pt">{esc(h)}</div><div style="font-size:9.8pt">{t}</div></div>' for h, t, c in items) + "</div>"

# ---------------------------------------------------------------- 1 Cover
P.append(f"""<section class="page" style="background:{NAVY};color:#fff">
<div style="position:absolute;left:0;top:0;bottom:0;width:14mm;background:{ACCENT}"></div>
<div style="position:absolute;right:-10mm;top:22mm;font-size:300pt;line-height:1;font-weight:700;color:{NAVY2}">§</div>
<div style="position:absolute;left:34mm;right:24mm;top:100mm">
 <div style="color:{ACCENT};font-size:11pt;font-weight:700;letter-spacing:.14em;text-transform:uppercase;margin-bottom:6mm">Booklet zur Unterrichtsstunde</div>
 <div style="font-size:38pt;line-height:1.1;font-weight:700">Rechte und Pflichten aus dem Ausbildungsvertrag</div>
 <div style="width:30mm;height:1.6mm;background:{ACCENT};margin:9mm 0 8mm"></div>
 <div style="font-size:17pt;color:{ACCENT};font-weight:700">Prüfungsvorbereitung im Fach GP (Geschäftsprozesse)</div>
 <div style="font-size:14pt;margin-top:4mm;color:#DCE3F2">Kaufleute für Büromanagement · Stand Oktober 2026</div></div>
<div style="position:absolute;left:34mm;bottom:22mm;font-size:14pt">von Yasin &amp; Mido</div>
<div style="position:absolute;right:20mm;bottom:18mm;background:#fff;padding:2mm;border-radius:2mm"><img src="{qr_uri()}" style="display:block;width:28mm;height:28mm"></div>
<div style="position:absolute;right:20mm;bottom:50mm;text-align:right;font-size:9pt;color:#DCE3F2;width:60mm"><b style="color:{ACCENT}">Interaktiv üben</b><br>{URL_KURZ}</div></section>""")

# ---------------------------------------------------------------- 2 Einleitung
steps = ["Einstieg und Wissensstand-Check auf Seite 3 bearbeiten.", "Die neun Themen auf den Seiten 4 bis 7 lesen.", "Aufgaben auf den Seiten 8 bis 11 lösen, erst danach die Lösungen auf den Seiten 13 und 14 ansehen.", "Mit dem Mini-Quiz auf Seite 12 testen, wo du stehst.", "Merkblatt (Seite 15) heraustrennen und mitnehmen."]
toc = [("Einstieg und Wissensstand-Check", "3"), ("Erklär-Themen 1 bis 9", "4–7"), ("Rote/Grüne Karte", "8"), ("Vertrags-Detektiv", "9"), ("IHK-Fälle A bis E", "10–11"), ("Experten-Karten", "11"), ("Mini-Quiz", "12"), ("Lösungen und Erwartungshorizont", "13–14"), ("Merkblatt", "15"), ("Glossar und Quellen", "16")]
tl = "".join(f'<div style="display:flex;gap:2mm;font-size:11pt;margin-bottom:1.8mm"><span style="color:{NAVY};font-weight:700">{esc(a)}</span><span style="flex:1;border-bottom:0.4mm dotted #9AA3B8;transform:translateY(-1mm)"></span><b>{b}</b></div>' for a, b in toc)
sl = "".join(f'<li style="margin-bottom:2.2mm">{esc(s)}</li>' for s in steps)
P.append(page("Einleitung", "Einleitung und „So nutzt du das Booklet“", f"""
<p class="lead">Jede Berufsausbildung beginnt mit einem Vertrag. Dieses Booklet folgt dem Ablauf unserer Unterrichtsstunde: erst Einstieg und Vorwissen, dann die Regeln zu Vertrag, Dauer, Arbeitszeit, Vergütung, Urlaub, Probezeit und Kündigung, danach Aufgaben und ein Mini-Quiz. So kannst du alles zu Hause noch einmal nacharbeiten.</p>
<div style="margin:6mm 0;background:{NAVY};color:#fff;border-radius:3mm;padding:5mm 7mm;border-left:3mm solid {ACCENT}">
<div style="color:{ACCENT};font-size:10pt;font-weight:700;letter-spacing:.12em;text-transform:uppercase;margin-bottom:2mm">So wird geprüft</div>
<div style="font-size:12.5pt;line-height:1.5">Im IHK-Prüfungsbereich Wirtschafts- und Sozialkunde hast du 60 Minuten für fallbezogene Aufgaben; der Bereich zählt 10 % der Gesamtnote (<a style="color:{ACCENT}" href="{VERORDNUNG_URL}">Verordnung</a>). Genau solche Fälle übst du in den Aufgaben.</div></div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:8mm;align-items:start">
<div style="background:{ACCENT_L};border-top:2mm solid {ACCENT};border-radius:0 0 3mm 3mm;padding:5mm 6mm 3mm"><div style="font-size:14pt;font-weight:700;color:{NAVY};margin-bottom:3mm">So nutzt du das Booklet:</div><ol style="margin-left:5mm;font-size:11.5pt;line-height:1.4">{sl}</ol></div>
<div><div style="font-size:10pt;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:{MUTED};margin-bottom:2mm">Inhalt</div>{tl}</div></div>
<div style="display:flex;align-items:center;gap:6mm;margin-top:8mm;border:0.5mm solid {NAVY};border-radius:2.5mm;padding:3mm 5mm"><img src="{qr_uri()}" style="width:26mm;height:26mm"><div><div style="font-weight:700;font-size:13pt;color:{NAVY}">Üben auf dem Handy</div><div style="font-size:11pt">Rote/Grüne Karte, Vertrags-Detektiv, IHK-Fälle und Mini-Quiz auch auf unserer Website: <b>{URL_KURZ}</b></div></div></div>""", 2))

# ---------------------------------------------------------------- 3 Einstieg + Wissensstand-Check
fr = "".join(f'<div style="display:flex;gap:3mm;margin-bottom:3.2mm"><span class="num" style="flex:none;margin-top:.5mm">{a}</span><div style="flex:1"><div style="font-weight:700;color:{NAVY};font-size:11.3pt">{esc(q)}</div><div style="height:7.5mm;border-bottom:0.3mm solid #BFC6D6"></div></div></div>' for a, q, _ in FRAGEN)
goals = ["nennen, was in einen Ausbildungsvertrag gehört", "Vergütung, Urlaub, Arbeitszeit, Probezeit und Kündigung anwenden", "Fälle mit der passenden Regel begründen"]
gl_ = "".join(f'<div style="display:flex;gap:3mm;align-items:center;margin-bottom:2mm"><span class="num" style="flex:none">{i+1}</span><span style="font-size:11.3pt">{esc(g)}</span></div>' for i, g in enumerate(goals))
P.append(page("Einstieg und Fragerunde", "Wissensstand-Check", f"""
<div style="background:{ACCENT_L};border-left:2mm solid {ACCENT};border-radius:0 2mm 2mm 0;padding:4mm 6mm;margin-bottom:5mm"><span style="font-size:8.5pt;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:#9A6A00">Einstieg</span><div style="font-size:13.5pt;font-weight:700;color:{NAVY};line-height:1.35">Dein erster Arbeitstag: Was steht eigentlich in deinem Ausbildungsvertrag?</div></div>
<div style="font-size:10pt;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:{MUTED};margin-bottom:1mm">Meine Stichworte</div>{lines(3)}
<h2 style="margin-top:6mm">Am Ende der Stunde kannst du …</h2>{gl_}
<h2 style="margin-top:6mm">Was wisst ihr schon? Vier Fragen, bevor du weiterliest</h2>
<p class="note" style="margin-bottom:3mm">Schreibe deine Antwort auf, ohne nachzuschauen. Die Auflösung steht auf Seite {LOES1}.</p>{fr}""", 3))

# ---------------------------------------------------------------- 4 Themen 1-3
pflicht = [("calendar", "Beginn und Dauer"), ("clock", "Tägliche Ausbildungszeit"), ("hourglass", "Probezeit"), ("euro", "Vergütung"), ("palm", "Urlaub"), ("doc", "Kündigung")]
cells = "".join(f'<div style="display:flex;align-items:center;gap:2.5mm;border:0.4mm solid #D5D9E3;border-radius:2mm;padding:1.6mm 2.5mm;background:#fff">{icon(n, "8mm")}<div style="font-weight:700;color:{NAVY};font-size:9.5pt;line-height:1.2">{esc(t)}</div></div>' for n, t in pflicht)
t1 = f'<p style="margin-bottom:2mm">Der Ausbildungsvertrag muss sechs Pflichtangaben enthalten:</p><div style="display:grid;grid-template-columns:repeat(3,1fr);gap:2.5mm;margin-bottom:2.5mm">{cells}</div><div style="background:{BLUE_L};border-left:1.6mm solid {NAVY2};padding:2mm 3.5mm;border-radius:0 2mm 2mm 0;font-size:10pt"><b style="color:{NAVY2}">Textform:</b> Seit dem 01.08.2024 genügt die Textform, zum Beispiel per E-Mail. Vorher war Papierform nötig.</div>'
t2 = kv_row([("Ausbildungsdauer", "Von Beginn bis zur Prüfung. Ende mit Bekanntgabe des Prüfungsergebnisses.", NAVY),
             ("Verkürzung", "Auf gemeinsamen Antrag von Azubi und Betrieb bei der zuständigen Stelle.", "#2E8B57"),
             ("Verlängerung", "Nur in Ausnahmefällen auf Antrag des Azubis oder nach nicht bestandener Prüfung, höchstens um ein Jahr.", "#D9730D")])
def big(num, sub, head, acc=False):
    return f'<div class="col"><div class="ch{" acc" if acc else ""}" style="padding:1.6mm 4mm;font-size:10.5pt">{head}</div><div class="cb" style="padding:2.4mm 4mm"><div style="font-size:21pt;font-weight:700;color:{NAVY};line-height:1.05">{num}</div><div style="font-size:9.8pt;margin-top:1mm">{sub}</div></div></div>'
t3 = ('<div class="two" style="gap:4mm">' + big("8 Stunden täglich", "höchstens 40 pro Woche; ausnahmsweise 8,5 Stunden bei Ausgleich", "Jugendliche") +
      big("8 Stunden täglich", "bis 10 mit Ausgleich (6 Monate); höchstens 48 pro Woche", "Volljährige", True) + "</div>")
P.append(page("Erklär-Themen 1 bis 3", "Vertrag, Dauer und Ausbildungszeit", thema(1, "Der Vertrag: sechs Pflichtangaben", "§ 11 BBiG", t1) + thema(2, "Beginn und Dauer", "§ 8, § 21 BBiG", t2, "5mm") + thema(3, "Ausbildungszeit", "§ 8 JArbSchG · § 3 ArbZG", t3, "5mm") + notes(3, "Meine Notizen", "6.5mm"), 4))

# ---------------------------------------------------------------- 5 Themen 4-6
bars = "".join(f'<div style="display:flex;align-items:center;gap:3mm;margin-bottom:1.6mm"><div style="width:15mm;font-weight:700;color:{NAVY};font-size:10pt">{j}</div><div style="flex:1;background:#EEF1F7;border-radius:1.5mm"><div style="width:{v/1014*100:.1f}%;background:{NAVY if i<3 else ACCENT};color:{"#fff" if i<3 else NAVY};padding:.8mm 3mm;border-radius:1.5mm;font-weight:700;font-size:10.5pt">{f"{v:,}".replace(",", ".")} €</div></div></div>' for i, (j, v) in enumerate(VERGUETUNG))
t4 = f'<p style="margin-bottom:2mm">Mindestausbildungsvergütung bei Beginn 2026. Sie darf nicht unterschritten werden und wird jedes Jahr neu festgelegt.</p>{bars}'
ur = "".join(f'<div style="flex:1;text-align:center;background:{NAVY if i<3 else ACCENT};color:{"#fff" if i<3 else NAVY};border-right:.8mm solid #fff;padding:2mm 1mm"><div style="font-size:9pt">{esc(a)}</div><div style="font-weight:700;font-size:15pt;line-height:1.1">{b}</div><div style="font-size:9pt">Werktage</div></div>' for i, (a, b) in enumerate([("unter 16", 30), ("unter 17", 27), ("unter 18", 25), ("ab 18", 24)]))
t5 = f'<div style="display:flex;border-radius:2mm;overflow:hidden;margin-bottom:2mm">{ur}</div><p style="font-size:9.8pt">Das Alter zählt zu Beginn des Kalenderjahres. <b>Werktage</b> sind alle Kalendertage außer Sonntagen und gesetzlichen Feiertagen. 24 Werktage entsprechen 20 Arbeitstagen bei der Fünf-Tage-Woche.</p>'
seg = "".join(f'<div style="flex:1;background:{NAVY if i<3 else ACCENT};color:{"#fff" if i<3 else NAVY};text-align:center;padding:2mm 0;font-weight:700;font-size:10.5pt;border-right:0.8mm solid #fff">{i+1}. Monat</div>' for i in range(4))
t6 = f'<p style="margin-bottom:2mm">Jedes Ausbildungsverhältnis beginnt mit einer Probezeit.</p><div style="display:flex;border-radius:2mm;overflow:hidden">{seg}</div><div style="display:flex;justify-content:space-between;font-size:9.5pt;color:{MUTED};margin-top:1mm"><span>mindestens 1 Monat</span><span>höchstens 4 Monate</span></div>'
P.append(page("Erklär-Themen 4 bis 6", "Vergütung, Urlaub und Probezeit", thema(4, "Mindestausbildungsvergütung 2026", "§ 17 BBiG", t4) + thema(5, "Urlaub nach Alter", "§ 19 JArbSchG · § 3 BUrlG", t5, "5mm") + thema(6, "Probezeit", "§ 20 BBiG", t6, "5mm") + notes(3, "Meine Notizen", "6.5mm"), 5))

# ---------------------------------------------------------------- 6 Themen 7-8
def node(t, fill, col="#fff", w="auto", sub=""):
    return f'<div style="background:{fill};color:{col};border-radius:2mm;padding:2mm 3mm;text-align:center;font-weight:700;font-size:10.3pt;width:{w}">{esc(t)}' + (f'<div style="font-weight:400;font-size:9pt">{esc(sub)}</div>' if sub else "") + "</div>"
arrow = f'<div style="text-align:center;color:{ACCENT};font-size:14pt;line-height:1">▼</div>'
tree = f"""<div style="display:flex;flex-direction:column;align-items:center">{node("Kündigung durch …?", NAVY, w="60mm")}{arrow}</div>
<div style="display:grid;grid-template-columns:1fr 1.7fr;gap:5mm;align-items:start">
<div>{node("in der Probezeit", NAVY2)}{arrow}{node("jederzeit ohne Frist", ACCENT_L, NAVY, sub="von beiden Seiten")}</div>
<div>{node("nach der Probezeit", NAVY2)}{arrow}<div style="display:grid;grid-template-columns:1fr 1fr;gap:3mm">{node("fristlos aus wichtigem Grund", ACCENT_L, NAVY, sub="beide Seiten")}{node("Azubi: vier Wochen Frist", ACCENT_L, NAVY, sub="bei Aufgabe der Ausbildung oder Berufswechsel")}</div></div></div>"""
t7 = tree
cards = kv_row([("Immer schriftlich", "E-Mail ist ausgeschlossen", RED), ("Mit Gründen", "nach der Probezeit", NAVY), ("Zwei Wochen", "nach Kenntnis der Gründe (wichtiger Grund)", ACCENT)])
t8 = cards
P.append(page("Erklär-Themen 7 und 8", "Kündigung", thema(7, "Kündigung: Entscheidungsbaum", "§ 22 Abs. 1 und 2 BBiG", t7) + thema(8, "Kündigung: Form und Frist", "§ 22 Abs. 3 und 4 BBiG", t8, "6mm") + f'<div style="margin-top:6mm">{warn("Jede Kündigung muss schriftlich erfolgen; E-Mail oder elektronische Form sind ausgeschlossen (§ 22 Abs. 3 BBiG).", "Schriftform")}</div>' + notes(4, "Meine Notizen", "6.5mm"), 6))

# ---------------------------------------------------------------- 7 Thema 9 + Kernzahlen
az = ["lernen", "sorgfältig arbeiten", "Weisungen befolgen", "Ordnung beachten", "Geheimnisse wahren", "Ausbildungsnachweis führen"]
ab = ["Ausbildungsziel vermitteln", "Ausbildungsmittel kostenlos stellen", "für Berufsschule und Prüfungen freistellen", "Zeugnis ausstellen", "Vergütung zahlen"]
t9 = f'<div class="two" style="gap:4mm"><div class="col"><div class="ch" style="padding:1.6mm 4mm;font-size:10.5pt">Azubis (§ 13 BBiG)</div><div class="cb" style="padding:2.5mm 4mm">{ul(az, "10.5pt")}</div></div><div class="col"><div class="ch acc" style="padding:1.6mm 4mm;font-size:10.5pt">Ausbildende (§§ 14–17 BBiG)</div><div class="cb" style="padding:2.5mm 4mm">{ul(ab, "10.5pt")}</div></div></div>'
five = [("4 Monate", "Probezeit, höchstens", "§ 20 BBiG"), ("724 €", "im 1. Jahr, Beginn 2026", "§ 17 BBiG"), ("24", "Werktage Urlaub ab 18", "§ 3 BUrlG"), ("schriftlich", "Kündigung, nie E-Mail", "§ 22 BBiG"), ("8 h", "täglich, Jugendliche", "§ 8 JArbSchG")]
fv = "".join(f'<div style="flex:1;background:{NAVY};color:#fff;border-radius:2mm;padding:3mm 2mm;text-align:center"><div style="color:{ACCENT};font-weight:700;font-size:15pt;line-height:1.1">{a}</div><div style="font-size:8.6pt;margin-top:1mm">{b}</div><div style="font-size:8.2pt;color:#DCE3F2;margin-top:1mm">{c}</div></div>' for a, b, c in five)
P.append(page("Erklär-Thema 9", "Pflichten und die fünf wichtigsten Zahlen", thema(9, "Pflichten von Azubi und Ausbildenden", "§§ 13–17 BBiG", t9) +
  f'<h2 style="margin-top:8mm">Merke dir diese fünf</h2><div style="display:flex;gap:2.5mm">{fv}</div>' + merk("Probezeit höchstens vier Monate, im 1. Jahr mindestens 724 €, 24 Werktage ab 18 Jahren, Kündigung immer schriftlich, Jugendliche höchstens 8 Stunden täglich.", "Merksatz") + notes(5, "Meine Notizen", "7mm"), 7))

# ---------------------------------------------------------------- 8 Rote/Gruene Karte
rg = "".join(f'<div style="display:grid;grid-template-columns:7mm 1fr 20mm 30mm;gap:3mm;padding:2.1mm 0;border-bottom:0.3mm solid #D5D9E3;align-items:center"><b style="color:{NAVY};font-size:11.5pt">{i+1}</b><div style="font-size:10.8pt;line-height:1.3">{esc(t)}</div><div style="font-size:9.5pt;white-space:nowrap"><span style="display:inline-block;width:4mm;height:4mm;border:.4mm solid #2E8B57;vertical-align:middle;margin-right:1mm"></span>stimmt</div><div style="font-size:9.5pt;white-space:nowrap"><span style="display:inline-block;width:4mm;height:4mm;border:.4mm solid {RED};vertical-align:middle;margin-right:1mm"></span>stimmt nicht</div></div>' for i, (t, _, _) in enumerate(RG))
P.append(page("Aufgabe 1 · allein · 3 Min.", "Rote/Grüne Karte", f'<p style="font-size:11pt;margin-bottom:2mm">Kreuze an, ob die Aussage stimmt (grün) oder nicht stimmt (rot). Hilfsmittel: Merkblatt auf Seite 15. Lösung auf Seite {LOES1}.</p>{rg}{notes(2, "Notizen", "7mm")}', 8, qr_head=True))

# ---------------------------------------------------------------- 9 Vertrags-Detektiv
det = "".join(f'<div style="margin-bottom:1.6mm"><b style="color:{NAVY}">{i+1}</b>&nbsp; {esc(t)}</div>' for i, (t, _) in enumerate(DET))
kopf = "".join(f'<div style="{"font-weight:700;color:"+NAVY+";margin-bottom:1mm" if i==0 else ""}">{esc(t)}</div>' for i, t in enumerate(DET_KOPF))
rows_det = "".join(f'<tr><td class="b" style="text-align:center;width:14mm;height:13mm">{i}</td><td style="width:42mm"></td><td style="width:58mm"></td><td></td></tr>' for i in range(1, 6))
P.append(page("Aufgabe 2 · zu zweit · 5 Min.", "Vertrags-Detektiv", f"""
<p style="font-size:12pt;margin-bottom:3mm">Im Vertragsauszug stecken <b>5 Fehler</b>. Finde sie und begründe sie mit der passenden Regel. Lösung auf Seite {LOES1}.</p>
<div style="background:#F6F8FC;border:0.4mm solid #BFC6D6;border-radius:2mm;padding:4mm 6mm;font-family:'Liberation Serif',serif;font-size:12pt;line-height:1.35">{kopf}<div style="border-top:0.3mm solid #BFC6D6;margin:2mm 0"></div>{det}</div>
<div style="font-weight:700;color:{NAVY};font-size:11pt;margin:7mm 0 2mm">Meine Lösung (Zeilennummer nennen: welche Zeilen enthalten einen Fehler?)</div>
<table class="t" style="font-size:10pt"><tr><th style="text-align:center">Fehler</th><th>Stelle im Vertrag</th><th>Regel (Paragraf)</th><th>Begründung</th></tr>{rows_det}</table>""", 9, qr_head=True))

# ---------------------------------------------------------------- 10-11 Faelle, Experten
def fall_c(f, reserve=False):
    pad = ("0.7mm 3mm", "9.4pt", "1mm") if reserve else ("1.1mm 3mm", "10pt", "1.2mm")
    ans = "".join(f'<div class="ans" style="margin-top:{pad[2]};padding:{pad[0]};font-size:{pad[1]}"><b>{L}</b><span>{esc(t)}</span></div>' for L, t in zip("ABCD", f["a"]))
    wrap = ('<div style="display:grid;grid-template-columns:1fr 1fr;gap:1mm 3mm">' + ans + "</div>") if reserve else ans
    res = f'<span style="background:{ACCENT_L};color:#9A6A00;font-size:8.5pt;font-weight:700;border-radius:1mm;padding:.3mm 2mm;margin-left:2mm">Reserve</span>' if reserve else ""
    return f'<div class="card" style="margin-bottom:{"2.6mm" if reserve else "3.5mm"};padding:{"2mm 5mm" if reserve else "2.8mm 5mm"}"><h3><span>{f["id"]}</span>Fall {f["id"]} ({esc(f["titel"])}){res}</h3><div style="margin-bottom:1mm;font-size:{"9.8pt" if reserve else "10.5pt"}">{esc(f["q"])}</div>{wrap}</div>'
FDE = [f for f in FAELLE if f["id"] in "DE"]
P.append(page("Aufgabe 3 · zu zweit · 4 Min.", "IHK-Fälle A bis C", f'<p style="font-size:11pt;margin-bottom:3mm">Wähle A–D und begründe mit einer Regel. Lösung auf Seite {LOES2}.</p>' + "".join(fall_c(f) for f in FAELLE_ABC) + "", 10, qr_head=True))
exp = "".join(f'<div style="border:0.4mm solid #D5D9E3;border-top:1.6mm solid {ACCENT};border-radius:0 0 2mm 2mm;padding:1.6mm 3.2mm"><div style="font-weight:700;color:{NAVY};font-size:10.5pt;margin-bottom:.5mm">{esc(e["t"])}</div>{ul(e["kern"], "8.9pt")}<div style="font-size:9.2pt;margin-top:1mm"><b>Frage:</b> {esc(e["frage"])}</div></div>' for e in EXPERTEN)
P.append(page("Reserve für Schnelle", "Fälle D, E und Experten", '<div style="margin-top:-6mm">' + "".join(fall_c(f, True) for f in FDE) + f'<h2 style="margin:0 0 1.5mm">Experten-Karten <span style="font-size:9.5pt;font-weight:400;color:#5B6680">· Schnell fertig? Hier gibt es mehr zu üben. Lösungen auf Seite {LOES2}.</span></h2><div style="display:grid;grid-template-columns:1fr 1fr;gap:3mm;align-items:start">{exp}</div></div>', 11, qr_head=True))

# ---------------------------------------------------------------- 12 Mini-Quiz
def qcard(i, f):
    ans = "".join(f'<div class="ans" style="margin-top:0;padding:.9mm 2.5mm;font-size:9.4pt"><b>{L}</b><span>{esc(t)}</span></div>' for L, t in zip("ABCD", f["a"]))
    return f'<div class="card" style="margin-bottom:3mm;padding:2.2mm 5mm"><div style="display:flex;gap:3mm;margin-bottom:1.2mm"><span class="num" style="flex:none">{i}</span><div style="font-size:10.6pt;font-weight:700;color:{NAVY}">{esc(f["q"])}</div></div><div style="display:grid;grid-template-columns:1fr 1fr;gap:1.4mm 3mm">{ans}</div></div>'
P.append(page("Mini-Quiz · allein · ca. 3 Min.", "Zeig, was du kannst", f'<p style="font-size:10.5pt;margin-bottom:2.5mm">Kreuze pro Frage eine Antwort an. Lösung auf Seite {LOES2}. Handzeichen im Unterricht: 5, 4, 3 oder weniger richtig.</p>' + "".join(qcard(i + 1, f) for i, f in enumerate(ABSCHLUSS)), 12, qr_head=True))

# ---------------------------------------------------------------- 13-14 Loesungen
sm = "font-size:8.9pt"
t_ws = "".join(f'<tr><td class="b" style="text-align:center">{a}</td><td>{esc(q)}</td><td>{esc(l)}</td></tr>' for a, q, l in FRAGEN)
t_rg = "".join(f'<tr><td class="b" style="text-align:center">{i+1}</td><td class="b" style="white-space:nowrap;color:{"#2E8B57" if ok else RED}">{"Stimmt" if ok else "Stimmt nicht"}</td><td>{esc(b)}</td></tr>' for i, (_, ok, b) in enumerate(RG))
t_det = "".join(f'<tr><td class="b" style="text-align:center">{n}</td><td>{esc(a)}</td><td>{esc(b)}</td><td style="text-align:center;white-space:nowrap">2 (1 + 1)</td></tr>' for n, (a, b) in FEHLER.items())
P.append(page("Lösungen 1 von 2", "Lösungen: Check, Karte, Detektiv", f"""<style>.eh table.t td{{padding:1.1mm 2.2mm}} .eh table.t th{{padding:1.3mm 2.2mm}}</style><div class="eh">
<div style="font-size:10pt;margin-bottom:1.5mm"><b style="color:{NAVY}">Wissensstand-Check (Seite 3)</b></div>
<table class="t" style="{sm}"><tr><th style="width:11mm">Frage</th><th>Frage</th><th>Antwort</th></tr>{t_ws}</table>
<div style="font-size:10pt;margin:4mm 0 1.5mm"><b style="color:{NAVY}">Aufgabe 1 · Rote/Grüne Karte</b> (je Aussage 1 Punkt, höchstens 10)</div>
<table class="t" style="{sm}"><tr><th style="width:11mm">Nr.</th><th style="width:24mm">Lösung</th><th>Begründung mit Paragraf</th></tr>{t_rg}</table>
<div style="font-size:10pt;margin:4mm 0 1.5mm"><b style="color:{NAVY}">Aufgabe 2 · Vertrags-Detektiv</b> (je Fehler 1 Punkt fürs Finden, 1 Punkt für die Begründung; höchstens 10). Zeilen 1 und 7 sind korrekt.</div>
<table class="t" style="{sm}"><tr><th style="width:11mm">Fehler</th><th style="width:34mm">Stelle</th><th>Lösung mit Regel</th><th style="width:20mm">Punkte</th></tr>{t_det}</table></div>""", LOES1))
t_f = "".join(f'<tr><td class="b" style="text-align:center">{f["id"]}{"*" if f["reserve"] else ""}</td><td class="b" style="text-align:center">{"ABCD"[f["c"]]}</td><td>{esc(f["begr"])} ({esc(f["para"])})</td><td style="text-align:center;white-space:nowrap">{"–" if f["reserve"] else "2 (1 + 1)"}</td></tr>' for f in FAELLE)
t_e = "".join(f'<tr><td class="b" style="white-space:nowrap">{esc(e["t"])}</td><td>{esc(e["loesung"])}</td></tr>' for e in EXPERTEN)
t_q = "".join(f'<tr><td class="b" style="text-align:center">{i+1}</td><td class="b" style="text-align:center">{"ABCD"[f["c"]]}</td><td>{esc(f["a"][f["c"]])} ({esc(f["fb"])})</td></tr>' for i, f in enumerate(ABSCHLUSS))
P.append(page("Lösungen 2 von 2", "Lösungen: Fälle, Experten, Quiz", f"""<style>.eh table.t td{{padding:1.1mm 2.2mm}} .eh table.t th{{padding:1.3mm 2.2mm}}</style><div class="eh">
<div style="font-size:10pt;margin-bottom:1.5mm"><b style="color:{NAVY}">Aufgabe 3 · IHK-Fälle</b> (A bis C je 2 Punkte; * Reserve, ohne Punkte)</div>
<table class="t" style="{sm}"><tr><th style="width:11mm">Fall</th><th style="width:15mm">Lösung</th><th>Begründung mit Regel</th><th style="width:20mm">Punkte</th></tr>{t_f}</table>
<div style="font-size:10pt;margin:4mm 0 1.5mm"><b style="color:{NAVY}">Experten-Karten</b></div>
<table class="t" style="{sm}"><tr><th style="width:24mm">Karte</th><th>Lösung</th></tr>{t_e}</table>
<div style="font-size:10pt;margin:4mm 0 1.5mm"><b style="color:{NAVY}">Mini-Quiz</b> (je Frage 1 Punkt; im Unterricht Handzeichen 5, 4, 3 oder weniger)</div>
<table class="t" style="{sm}"><tr><th style="width:11mm">Nr.</th><th style="width:15mm">Lösung</th><th>Antwort und Regel</th></tr>{t_q}</table>
<div style="margin-top:4mm;background:{ACCENT_L};border-left:2mm solid {ACCENT};padding:2.5mm 4mm;font-size:10pt"><b style="color:{NAVY}">Punkte Aufgaben 1 bis 3: höchstens 26</b> (Karte 10 + Detektiv 10 + Fälle A bis C 3 × 2). Dazu Mini-Quiz höchstens 5.</div></div>""", LOES2))

# ---------------------------------------------------------------- 15 Merkblatt, 16 Glossar + Quellen
P.append(merkblatt_page(15))
gl = "".join(f'<div style="display:grid;grid-template-columns:64mm 1fr;gap:4mm;padding:2mm 0;border-bottom:0.3mm solid #D5D9E3"><b style="color:{NAVY};font-size:10.5pt">{esc(t)}</b><span style="font-size:10pt">{esc(d)}</span></div>' for t, d in GLOSSAR)
q = "".join(f'<li style="margin-bottom:1.1mm"><a href="{u}" style="color:{NAVY2}">{esc(t)}</a></li>' for t, u in QUELLEN)
P.append(page("Nachschlagen", "Glossar und Quellen", gl + f'<div style="font-size:9pt;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:{MUTED};margin:6mm 0 1.5mm">Quellenverzeichnis</div><ul style="list-style:none;font-size:8.2pt;line-height:1.3">{q}</ul>'
  f'<div style="display:flex;align-items:center;gap:6mm;margin-top:6mm;border:0.5mm solid {NAVY};border-radius:2.5mm;padding:3mm 5mm"><img src="{qr_uri()}" style="width:24mm;height:24mm"><div><div style="font-weight:700;font-size:12pt;color:{NAVY}">Weiter üben</div><div style="font-size:10.5pt">{URL_KURZ}</div><div class="note">Rechte und Pflichten aus dem Ausbildungsvertrag · Yasin &amp; Mido · Fach GP · Stand Oktober 2026</div></div></div>', 16))

assert len(P) == 16, len(P)
hp = os.path.join(OUT, "_booklet.html"); open(hp, "w", encoding="utf-8").write(doc("".join(P), "Rechte und Pflichten aus dem Ausbildungsvertrag"))
render_pdf.render(hp, os.path.join(OUT, "booklet_v4.pdf")); os.remove(hp)
# Merkblatt: eine Seite
hp = os.path.join(OUT, "_merk.html"); open(hp, "w", encoding="utf-8").write(doc(merkblatt_page(None), "Merkblatt"))
render_pdf.render(hp, os.path.join(OUT, "merkblatt_v4.pdf")); os.remove(hp)
print("ok")
