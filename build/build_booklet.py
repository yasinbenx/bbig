# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from html import escape as esc
from pdfkit import *
from data import *

P = []  # Seiten in Reihenfolge


def A(txt):  # Absatz
    return f"<p>{esc(txt)}</p>"


# ------------------------------------------------------------------ 1 Cover
P.append(f"""<section class="page" style="background:{NAVY};color:#fff">
<div style="position:absolute;left:0;top:0;bottom:0;width:14mm;background:{ACCENT}"></div>
<div style="position:absolute;right:-10mm;top:22mm;font-size:300pt;line-height:1;font-weight:700;color:{NAVY2};font-family:'Liberation Sans',Arial">§</div>
<div style="position:absolute;left:34mm;right:24mm;top:108mm">
  <div style="color:{ACCENT};font-size:11pt;font-weight:700;letter-spacing:.14em;text-transform:uppercase;margin-bottom:6mm">Prüfungsvorbereitung</div>
  <div style="font-size:40pt;line-height:1.1;font-weight:700">Rechte und Pflichten aus dem Ausbildungsvertrag</div>
  <div style="width:30mm;height:1.6mm;background:{ACCENT};margin:9mm 0 8mm"></div>
  <div style="font-size:18pt;color:{ACCENT};font-weight:700">Prüfungsvorbereitung Wirtschafts- und Sozialkunde</div>
  <div style="font-size:14pt;margin-top:4mm;color:#DCE3F2">Kaufleute für Büromanagement · Stand Oktober 2026</div>
</div>
<div style="position:absolute;left:34mm;bottom:22mm;font-size:14pt;color:#fff">von Yasin &amp; Mido</div>
</section>""")

# ------------------------------------------------------------------ 2 Inhalt
toc_main = [("Einleitung", "3"), ("Kapitel 1 bis 10", "4–13"), ("Merksätze", "14"), ("Merkblatt", "15"),
            ("Aufgaben", "16–18"), ("Erwartungshorizont", "19"), ("Quiz", "20–22"), ("Glossar", "23"), ("Quellen", "24")]
chap = [("1 Das Berufsbildungsgesetz (BBiG)", 4), ("2 Der Berufsausbildungsvertrag", 5), ("3 Beginn und Dauer der Ausbildung", 6),
        ("4 Tägliche Ausbildungszeit", 7), ("5 Ausbildungsvergütung", 8), ("6 Urlaub", 9), ("7 Probezeit", 10), ("8 Kündigung", 11),
        ("9 Pflichten von Azubi und Ausbildenden", 12), ("10 Praxisbeispiele", 13)]
toc = "".join(f'<div style="display:flex;align-items:baseline;gap:2mm;font-size:13pt;margin-bottom:2.2mm"><b style="color:{NAVY}">{esc(a)}</b><span style="flex:1;border-bottom:0.4mm dotted #9AA3B8;transform:translateY(-1mm)"></span><span style="font-weight:700">{b}</span></div>' for a, b in toc_main)
ch = "".join(f'<div style="display:flex;gap:2mm;font-size:10pt;color:{MUTED};margin-bottom:1mm"><span style="flex:1">Kapitel {esc(a)}</span><span>{b}</span></div>' for a, b in chap)
steps = ["Lies die Kapitel 1 bis 10.", "Trenne das Merkblatt auf Seite 15 heraus.",
         "Löse die Aufgaben und vergleiche erst danach mit dem Erwartungshorizont auf Seite 19.",
         "Teste mit den drei Quizrunden, ob alles sitzt."]
sl = "".join(f'<li style="margin-bottom:3mm">{esc(s)}</li>' for s in steps)
P.append(page("Orientierung", "Inhalt und Gebrauchsanleitung", f"""
<div style="display:grid;grid-template-columns:1.25fr 1fr;gap:9mm;align-items:start">
<div>{toc}<div style="margin:5mm 0 0 4mm;border-left:0.6mm solid {ACCENT};padding-left:4mm">{ch}</div></div>
<div style="background:{ACCENT_L};border-top:2mm solid {ACCENT};border-radius:0 0 3mm 3mm;padding:6mm 6mm 4mm">
<div style="font-size:15pt;font-weight:700;color:{NAVY};margin-bottom:4mm">So nutzt du das Booklet:</div>
<ol style="margin-left:5mm;font-size:12.5pt;line-height:1.45">{sl}</ol></div></div>""", 2))

# ------------------------------------------------------------------ 3 Einleitung
P.append(page("Einleitung", "Einleitung", f"""
<div style="display:flex;gap:9mm;align-items:flex-start">{icon('contract', '34mm')}
<div class="lead" style="padding-top:2mm">{esc("Jede Berufsausbildung beginnt mit einem Vertrag – und der regelt mehr, als viele denken. Dieses Booklet fasst zusammen, was im Berufsbildungsgesetz (BBiG) zu Beginn, Dauer, Arbeitszeit, Vergütung, Urlaub, Probezeit und Kündigung steht. Kurz, verständlich, mit echten Beispielen.")}</div></div>
<div style="margin-top:14mm;background:{NAVY};color:#fff;border-radius:3mm;padding:7mm 8mm;border-left:3mm solid {ACCENT}">
<div style="color:{ACCENT};font-size:10pt;font-weight:700;letter-spacing:.12em;text-transform:uppercase;margin-bottom:2mm">So wird geprüft</div>
<div style="font-size:13.5pt;line-height:1.55">In Wirtschafts- und Sozialkunde hast du 60 Minuten für fallbezogene Aufgaben; der Bereich zählt 10 % der Gesamtnote (<a style="color:{ACCENT}" href="{VERORDNUNG_URL}">Verordnung</a>). Genau solche Fälle übst du ab Seite 16.</div></div>""", 3))

# ------------------------------------------------------------------ 4 Kapitel 1
P.append(page("Kapitel 1", "Das Berufsbildungsgesetz (BBiG)", f"""
<div style="display:flex;gap:9mm;align-items:flex-start"><div style="font-size:120pt;line-height:.9;font-weight:700;color:{NAVY};width:38mm;flex:none">§</div>
<div class="lead" style="padding-top:3mm">{esc("Das BBiG regelt bundesweit die betriebliche Berufsausbildung in Deutschland. Es legt fest, welche Rechte und Pflichten Auszubildende und Ausbildende haben – vom Vertragsschluss bis zur Abschlussprüfung.")}</div></div>
{merk("Das BBiG ist die gesetzliche Grundlage jeder dualen Ausbildung.", big=True)}""", 4))

# ------------------------------------------------------------------ 5 Kapitel 2
ic = [("calendar", "Beginn und Dauer der Ausbildung"), ("clock", "Tägliche Ausbildungszeit"), ("euro", "Höhe der Vergütung"),
      ("palm", "Dauer des Urlaubs"), ("hourglass", "Dauer der Probezeit"), ("doc", "Kündigungsbedingungen")]
cells = "".join(f'<div style="display:flex;align-items:center;gap:4mm;border:0.4mm solid #D5D9E3;border-radius:2.5mm;padding:3mm 4mm">{icon(n, "13mm")}<div style="font-weight:700;color:{NAVY};font-size:12pt;line-height:1.25">{esc(t)}</div></div>' for n, t in ic)
P.append(page("Kapitel 2", "Der Berufsausbildungsvertrag", f"""
{A("Nach § 11 BBiG muss der Ausbildungsvertrag unter anderem enthalten:")}
<div style="display:grid;grid-template-columns:1fr 1fr;gap:4mm;margin-bottom:6mm">{cells}</div>
{info(A("Seit dem 1. August 2024 darf der wesentliche Vertragsinhalt in Textform abgefasst werden, zum Beispiel per E-Mail; vorher war die Papierform vorgeschrieben (§ 11 BBiG)."), "Textform-Regel")}""", 5))

# ------------------------------------------------------------------ 6 Kapitel 3 (Zeitstrahl)
svg = f"""<svg viewBox="0 0 700 380" xmlns="http://www.w3.org/2000/svg" style="width:100%;font-family:'Liberation Sans',Arial">
<defs><marker id="ag" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0 0L8 4L0 8z" fill="#2E8B57"/></marker>
<marker id="ao" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0 0L8 4L0 8z" fill="#D9730D"/></marker></defs>
<text x="20" y="28" font-size="22" font-weight="700" fill="#2E8B57">Verkürzung</text>
<text x="20" y="54" font-size="16" fill="{INK}">auf gemeinsamen Antrag (§ 8 Abs. 1 BBiG),</text>
<text x="20" y="76" font-size="16" fill="{INK}">nach IHK-Praxis bis zu 6 Monate mit mittlerem</text>
<text x="20" y="98" font-size="16" fill="{INK}">Schulabschluss, bis zu 12 Monate mit Abitur</text>
<path d="M545 150 L400 150" stroke="#2E8B57" stroke-width="6" marker-end="url(#ag)"/>
<rect x="40" y="170" width="520" height="34" rx="4" fill="{NAVY}"/>
<text x="300" y="193" text-anchor="middle" fill="#fff" font-size="16" font-weight="700">Ausbildungsdauer: meist 2 bis 3,5 Jahre</text>
<circle cx="40" cy="187" r="10" fill="{ACCENT}" stroke="{NAVY}" stroke-width="3"/><circle cx="560" cy="187" r="10" fill="{ACCENT}" stroke="{NAVY}" stroke-width="3"/>
<path d="M580 187 L685 187" stroke="#D9730D" stroke-width="6" marker-end="url(#ao)"/>
<text x="20" y="232" font-size="17" font-weight="700" fill="{NAVY}">Ausbildungsbeginn</text>
<text x="560" y="232" text-anchor="middle" font-size="17" font-weight="700" fill="{NAVY}">Prüfung</text>
<text x="560" y="254" text-anchor="middle" font-size="14" fill="{MUTED}">Ende mit Bekanntgabe des</text>
<text x="560" y="272" text-anchor="middle" font-size="14" fill="{MUTED}">Ergebnisses (§ 21 Abs. 2 BBiG)</text>
<text x="20" y="318" font-size="22" font-weight="700" fill="#D9730D">Verlängerung</text>
<text x="20" y="344" font-size="16" fill="{INK}">nur in Ausnahmefällen auf Antrag des Azubis (§ 8 Abs. 2 BBiG) oder nach nicht</text>
<text x="20" y="366" font-size="16" fill="{INK}">bestandener Prüfung bis zu 1 Jahr, bis zur Wiederholungsprüfung (§ 21 Abs. 3 BBiG)</text>
</svg>"""
P.append(page("Kapitel 3", "Beginn und Dauer der Ausbildung", f"""
{A("Die Ausbildungsdauer richtet sich nach der jeweiligen Ausbildungsordnung, meist 2 bis 3,5 Jahre. Eine Verkürzung ist auf gemeinsamen Antrag von Azubi und Ausbildenden möglich (§ 8 Abs. 1 BBiG), nach der Praxis der IHK zum Beispiel um bis zu sechs Monate mit mittlerem Schulabschluss oder bis zu zwölf Monate mit Abitur. Eine Verlängerung gibt es nur in Ausnahmefällen auf Antrag des Azubis (§ 8 Abs. 2 BBiG) oder nach nicht bestandener Abschlussprüfung bis zur Wiederholungsprüfung, höchstens um ein Jahr (§ 21 Abs. 3 BBiG). Bei bestandener Prüfung endet die Ausbildung mit der Bekanntgabe des Ergebnisses (§ 21 Abs. 2 BBiG).")}
<div style="margin-top:6mm;border:0.4mm solid #D5D9E3;border-radius:3mm;padding:5mm 3mm 2mm">{svg}</div>""", 6))

# ------------------------------------------------------------------ 7 Kapitel 4
def big(num, unit, sub, head, acc=False):
    return f"""<div class="col"><div class="ch{' acc' if acc else ''}">{head}</div><div class="cb" style="text-align:center;padding:7mm 5mm">
<div style="font-size:46pt;font-weight:700;color:{NAVY};line-height:1">{num}</div><div style="font-size:14pt;font-weight:700;color:{NAVY};margin-bottom:4mm">{unit}</div>
<div style="font-size:11pt;color:{INK}">{sub}</div></div></div>"""

P.append(page("Kapitel 4", "Tägliche Ausbildungszeit", f"""
<div class="two" style="margin-bottom:7mm">
{big("8", "Stunden täglich", "höchstens 40 Stunden wöchentlich; ausnahmsweise 8,5 Stunden täglich, wenn in derselben Woche ausgeglichen wird (§ 8 JArbSchG)", "Jugendliche")}
{big("bis 10", "Stunden mit Ausgleich", "grundsätzlich höchstens 8 Stunden täglich; im Durchschnitt von sechs Monaten dürfen 8 Stunden nicht überschritten werden, höchstens aber 48 Stunden pro Woche (§ 3 ArbZG)", "Volljährige", True)}
</div>
{A("Für minderjährige Azubis gilt das Jugendarbeitsschutzgesetz: höchstens 8 Stunden täglich und 40 Stunden wöchentlich, ausnahmsweise 8,5 Stunden täglich, wenn in derselben Woche ausgeglichen wird (§ 8 JArbSchG). Für volljährige Azubis gilt das Arbeitszeitgesetz: grundsätzlich höchstens 8 Stunden täglich; bis zu 10 Stunden sind erlaubt, wenn im Durchschnitt von sechs Monaten 8 Stunden nicht überschritten werden, höchstens aber 48 Stunden pro Woche (§ 3 ArbZG).")}""", 7))

# ------------------------------------------------------------------ 8 Kapitel 5
rows = "".join(f'<tr><td class="b" style="font-size:13pt;padding:3.4mm 5mm">{j}</td><td style="font-size:13pt;font-weight:700;padding:3.4mm 5mm">{v:,} €'.replace(",", ".") + "</td></tr>" for j, v in VERGUETUNG)
bars = ""
for j, v in VERGUETUNG:
    w = round(v / 1014 * 100, 1)
    bars += f'<div style="display:flex;align-items:center;gap:3mm;margin-bottom:2.5mm"><div style="width:16mm;font-weight:700;color:{NAVY};font-size:11pt">{j}</div><div style="flex:1;background:#EEF1F7;border-radius:1.5mm"><div style="width:{w}%;background:{NAVY if j!="4. Jahr" else ACCENT};height:9mm;border-radius:1.5mm;display:flex;align-items:center;justify-content:flex-end;padding-right:3mm;color:{"#fff" if j!="4. Jahr" else NAVY};font-weight:700;font-size:11pt">{f"{v:,}".replace(",", ".")} €</div></div></div>'
P.append(page("Kapitel 5", "Ausbildungsvergütung", f"""
{A("Seit 2020 gilt eine gesetzliche Mindestausbildungsvergütung nach § 17 BBiG. Für Ausbildungsverträge, die 2026 beginnen:")}
<table class="t" style="margin:2mm 0 7mm"><tr><th style="font-size:11pt">Ausbildungsjahr</th><th style="font-size:11pt">Mindestvergütung</th></tr>{rows}</table>
{bars}
{merk("Die Vergütung steigt jedes Jahr – und darf diese Mindestbeträge nicht unterschreiten.")}""", 8))

# ------------------------------------------------------------------ 9 Kapitel 6
palm = icon("palm", "11mm")
urows = "".join(f'<tr><td style="width:18mm;padding:2.5mm 4mm">{palm}</td><td style="font-size:13pt;padding:2.5mm 4mm">{esc(a)}</td><td style="font-size:13pt;font-weight:700;color:{NAVY};padding:2.5mm 4mm">{esc(b)}</td></tr>' for a, b in URLAUB)
P.append(page("Kapitel 6", "Urlaub", f"""
<table class="t"><tr><th></th><th style="font-size:11pt">Status</th><th style="font-size:11pt">Urlaubsanspruch</th></tr>{urows}</table>
<p class="note" style="margin-top:5mm">Grundlage: § 19 Jugendarbeitsschutzgesetz (Minderjährige), § 3 Bundesurlaubsgesetz (Volljährige).</p>""", 9))

# ------------------------------------------------------------------ 10 Kapitel 7
seg = "".join(f'<div style="flex:1;background:{NAVY if i<3 else ACCENT};color:{"#fff" if i<3 else NAVY};text-align:center;padding:4mm 0;font-weight:700;font-size:13pt;border-right:0.8mm solid #fff">{i+1}. Monat</div>' for i in range(4))
P.append(page("Kapitel 7", "Probezeit", f"""
{A("Jedes Berufsausbildungsverhältnis beginnt mit einer Probezeit (§ 20 BBiG) von mindestens einem, höchstens vier Monaten.")}
<div style="margin:8mm 0 1mm;display:flex;border-radius:2mm;overflow:hidden">{seg}</div>
<div style="display:flex;justify-content:space-between;font-size:10.5pt;color:{MUTED};margin-bottom:8mm"><span>mindestens 1 Monat</span><span>höchstens 4 Monate</span></div>
{merk("Keine Probezeit, keine Ausbildung – sie ist gesetzlich Pflicht.", big=True)}""", 10))

# ------------------------------------------------------------------ 11 Kapitel 8
P.append(page("Kapitel 8", "Kündigung", f"""
<div class="two" style="margin-bottom:6mm">
<div class="col"><div class="ch">In der Probezeit</div><div class="cb" style="font-size:12.5pt">{esc("Während der Probezeit kann jede Seite jederzeit ohne Kündigungsfrist kündigen (§ 22 Abs. 1 BBiG).")}</div></div>
<div class="col"><div class="ch acc">Nach der Probezeit</div><div class="cb" style="font-size:12.5pt">{esc("Nach der Probezeit ist eine Kündigung nur noch möglich:")}
<ul class="l" style="margin-top:2mm"><li>fristlos aus wichtigem Grund (beide Seiten), oder</li><li>durch den Azubi selbst mit vierwöchiger Frist, wenn er die Ausbildung aufgeben oder sich für eine andere Berufstätigkeit ausbilden lassen will.</li></ul></div></div></div>
{warn("Jede Kündigung muss schriftlich erfolgen; eine elektronische Form ist ausgeschlossen (§ 22 Abs. 3 BBiG).", "Schriftform")}""", 11))

# ------------------------------------------------------------------ 12 Kapitel 9
az = ["sich bemühen, die berufliche Handlungsfähigkeit zu erwerben", "aufgetragene Aufgaben sorgfältig ausführen",
      "Weisungen befolgen und die Ordnung der Ausbildungsstätte beachten", "Werkzeug und Einrichtungen pfleglich behandeln",
      "über Betriebs- und Geschäftsgeheimnisse Stillschweigen wahren", "einen Ausbildungsnachweis (Berichtsheft) führen"]
ab = ["das Ausbildungsziel planmäßig vermitteln und selbst ausbilden oder einen Ausbilder beauftragen", "Ausbildungsmittel kostenlos zur Verfügung stellen",
      "Azubis zum Berufsschulbesuch und zum Führen des Ausbildungsnachweises anhalten und diesen regelmäßig durchsehen",
      "Azubis charakterlich fördern und nicht gefährden", "für Berufsschule und Prüfungen freistellen (§ 15), auch am Arbeitstag vor der schriftlichen Abschlussprüfung",
      "bei Ende der Ausbildung ein schriftliches Zeugnis ausstellen (§ 16)", "eine angemessene Vergütung zahlen (§ 17)"]
li = lambda xs: "<ul class='l' style='font-size:11pt'>" + "".join(f"<li>{esc(x)}</li>" for x in xs) + "</ul>"
P.append(page("Kapitel 9", "Pflichten von Azubi und Ausbildenden", f"""
{A("Neben dem Vertrag regelt das BBiG, was beide Seiten tun müssen.")}
<div class="two"><div class="col"><div class="ch">Pflichten der Auszubildenden<br><span style="font-size:9.5pt;font-weight:400">§ 13 BBiG</span></div><div class="cb">{li(az)}</div></div>
<div class="col"><div class="ch acc">Pflichten der Ausbildenden<br><span style="font-size:9.5pt;font-weight:400">§§ 14 bis 17 BBiG</span></div><div class="cb">{li(ab)}</div></div></div>
<div style="margin-top:7mm;background:{NAVY};color:#fff;border-radius:2.5mm;padding:5mm 7mm;border-left:3mm solid {ACCENT}"><span style="color:{ACCENT};font-size:9pt;font-weight:700;letter-spacing:.1em;text-transform:uppercase">Merksatz</span>
<div style="font-size:14pt;font-weight:700;margin-top:1mm">Der Betrieb bildet aus und zahlt, der Azubi lernt, folgt und schweigt über Betriebsgeheimnisse.</div></div>""", 12))

# ------------------------------------------------------------------ 13 Kapitel 10 (leerer Rahmen fuer Vertragsauszuege)
rows13 = ""
for i in range(1, 4):
    rows13 += f"""<div style="display:grid;grid-template-columns:1.15fr 1fr;gap:6mm;margin-bottom:6mm;height:63mm">
<div style="border:0.5mm dashed #9AA3B8;border-radius:2.5mm;position:relative;background:#FBFCFE"><span style="position:absolute;left:4mm;top:3mm;font-size:9pt;color:{MUTED};letter-spacing:.04em">Vertragsauszug {i} (anonymisiert)</span></div>
<div style="border:0.5mm solid #D5D9E3;border-radius:2.5mm;position:relative"><span style="position:absolute;left:4mm;top:3mm;font-size:9pt;color:{MUTED};letter-spacing:.04em">Erklärung zu Auszug {i}</span></div></div>"""
P.append(page("Kapitel 10", "Praxisbeispiele aus dem eigenen Ausbildungsverhältnis", rows13, 13))

# ------------------------------------------------------------------ 14 Merksaetze
ms = ["Der Vertragsinhalt wird in Textform abgefasst (seit 01.08.2024), eine Kündigung braucht weiterhin die Schriftform.",
      "Die Mindestausbildungsvergütung darf nie unterschritten werden.",
      "In der Probezeit kann fristlos gekündigt werden – danach nur noch aus wichtigem Grund."]
cards = "".join(f'<div style="background:{ACCENT_L};border-top:3mm solid {ACCENT};border-radius:0 0 3mm 3mm;padding:7mm 4mm;display:flex;flex-direction:column;gap:6mm"><div style="width:11mm;height:11mm;border-radius:50%;background:{NAVY};color:{ACCENT};font-weight:700;font-size:15pt;text-align:center;line-height:11mm">{i+1}</div><div style="font-size:12.5pt;font-weight:700;color:{NAVY};line-height:1.4">{esc(t).replace("Mindestausbildungsvergütung","Mindest&shy;ausbildungs&shy;vergütung")}</div></div>' for i, t in enumerate(ms))
P.append(page("Zum Schluss", "Merksätze zum Schluss", f'<div style="display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:5mm;margin-top:14mm;height:95mm">{cards}</div>', 14))

# ------------------------------------------------------------------ 15 Merkblatt
P.append(merkblatt_page(15))

# ------------------------------------------------------------------ 16 Aufgabe 1
sit = "".join(f'<tr><td class="b">{n}</td><td>{esc(t)}</td></tr>' for n, t, _ in PAARE)
reg = "".join(f'<tr><td class="b">{k}</td><td>{esc(v)}</td></tr>' for k, v in REGELUNGEN.items())
nums = "".join(f'<td style="text-align:center;font-weight:700;color:{NAVY};background:{BLUE_L};border:0.4mm solid #BFC6D6;padding:2mm">{n}</td>' for n in range(1, 9))
blank = "".join('<td style="border:0.4mm solid #BFC6D6;height:12mm"></td>' for _ in range(8))
P.append(page("Aufgabe 1", "Situationen zuordnen", f"""
{A("Ordne jeder Situation die passende Regelung zu. Die Lösung steht auf Seite 19.")}
<div style="display:grid;grid-template-columns:1fr 1fr;gap:5mm;font-size:9.5pt">
<table class="t" style="font-size:9.5pt"><tr><th style="width:9mm">Nr.</th><th>Situation</th></tr>{sit}</table>
<table class="t" style="font-size:9.5pt"><tr><th style="width:9mm">Buchst.</th><th>Regelung</th></tr>{reg}</table></div>
<div style="margin-top:7mm;font-weight:700;color:{NAVY};font-size:11pt;margin-bottom:1.5mm">Meine Lösung (Buchstabe eintragen):</div>
<table style="width:100%;border-collapse:collapse"><tr>{nums}</tr><tr>{blank}</tr></table>""", 16))

# ------------------------------------------------------------------ 17/18 Faelle
def fall_card(f):
    ans = "".join(f'<div class="ans" style="margin-top:1.2mm;padding:1.2mm 3mm;font-size:10.5pt"><b>{L}</b><span>{esc(t)}</span></div>' for L, t in zip("ABCD", f["a"]))
    kind = "Reservefall" if f["reserve"] else "Fall"
    return f'<div class="card" style="margin-bottom:4mm;padding:3mm 5mm"><h3><span>{f["id"]}</span>{kind} {f["id"]} ({esc(f["titel"])})</h3><div style="margin-bottom:1mm;font-size:10.5pt">{esc(f["q"])}</div>{ans}</div>'

P.append(page("Aufgabe 2", "IHK-Fälle A bis C", A("Wähle A–D und begründe mit einer Regel. Die Lösung steht auf Seite 19.") + "".join(fall_card(f) for f in FAELLE[:3]), 17))
P.append(page("Aufgabe 3", "Reservefälle D und E", A("Wähle A–D und begründe mit einer Regel. Die Lösung steht auf Seite 19.") + "".join(fall_card(f) for f in FAELLE[3:]), 18))

# ------------------------------------------------------------------ 19 Erwartungshorizont
erows = "".join(f'<tr><td class="b" style="text-align:center">{f["id"]}</td><td class="b" style="text-align:center">{"ABCD"[f["c"]]}</td><td>{esc(f["begr"])} ({esc(f["para"])})</td><td style="text-align:center;font-weight:700;white-space:nowrap">2 (1 + 1)</td></tr>' for f in FAELLE)
P.append(page("Lösungen", "Erwartungshorizont", f"""
<div style="background:{ACCENT_L};border-left:2mm solid {ACCENT};padding:4mm 5mm;border-radius:0 2mm 2mm 0;font-size:11.5pt"><b style="color:{NAVY}">Aufgabe 1, Lösungsschlüssel:</b> {esc(LOESUNGSSCHLUESSEL)} (1 Punkt je Treffer, höchstens 8 Punkte).</div>
<table class="t" style="margin-top:6mm"><tr><th>Fall</th><th>Lösung</th><th>Begründung mit Regel</th><th>Punkte</th></tr>{erows}</table>
<p style="margin-top:6mm"><b>Gesamt:</b> höchstens 18 Punkte (8 + 5 × 2). Bei den Fällen gibt es 1 Punkt für die richtige Antwort und 1 Punkt für die Begründung mit der passenden Regel.</p>""", 19))

# ------------------------------------------------------------------ 20 Quiz 1
def qcard(i, text, sol_html, extra=""):
    return f'<div class="card" style="margin-bottom:2.6mm;padding:2.2mm 5mm"><div style="display:flex;gap:3mm"><span class="num" style="flex:none">{i}</span><div style="font-size:12pt;font-weight:700;color:{NAVY}">{esc(text)}</div></div>{extra}<div class="sol"><b>Lösung:</b> {sol_html}</div></div>'

P.append(page("Quiz 1", "Selbsttest", A("Ordne die Situation der passenden Regelung zu. Die Lösung steht jeweils dahinter.") + "".join(qcard(i + 1, q, esc(s)) for i, (q, s) in enumerate(SELBSTTEST)), 20))

# ------------------------------------------------------------------ 21 Quiz 2
mrows = ""
for k, m in enumerate(MILLIONAER):
    ans = "".join(f'<div style="display:flex;gap:2mm"><b style="color:{NAVY}">{L}</b><span>{esc(t)}</span></div>' for L, t in zip("ABCD", m["a"]))
    mrows += f"""<div style="display:grid;grid-template-columns:25mm 1fr 36mm;gap:4mm;border-bottom:0.3mm solid #D5D9E3;padding:2.6mm 0;align-items:center">
<div style="background:{NAVY if k<6 else ACCENT};color:{'#fff' if k<6 else NAVY};border-radius:1.8mm;text-align:center;font-weight:700;padding:2mm 0;font-size:{11 if k<6 else 10.5}pt;margin-left:{k*0.8}mm">{esc(m['stufe'])}</div>
<div><div style="font-weight:700;font-size:10.5pt;color:{NAVY};margin-bottom:1mm">{esc(m['q'])}</div><div style="display:grid;grid-template-columns:1fr 1fr;gap:0 4mm;font-size:9.5pt">{ans}</div></div>
<div style="font-size:8pt;color:#7B8498;background:{GREY_L};border-radius:1.5mm;padding:1.6mm 2mm"><b>Lösung:</b> {"ABCD"[m['c']]} – {esc(m['fb'])}</div></div>"""
P.append(page("Quiz 2", "Wer wird Azubi-Millionär?", f'<div style="display:grid;grid-template-columns:25mm 1fr 36mm;gap:4mm;font-size:8.5pt;font-weight:700;color:{MUTED};letter-spacing:.06em;text-transform:uppercase;margin-bottom:1mm"><span>Gewinnstufe</span><span>Frage und Antworten</span><span>Lösung</span></div>' + mrows, 21))

# ------------------------------------------------------------------ 22 Quiz 3
def qcard3(i, a):
    ans = "".join(f'<div style="display:flex;gap:2mm;font-size:9.5pt;line-height:1.35"><b style="color:{NAVY}">{L}</b><span>{esc(t)}</span></div>' for L, t in zip("ABCD", a["a"]))
    ex = f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:0.4mm 6mm;margin:1mm 0 0 10mm">{ans}</div>'
    return qcard(i, a["q"], f'{"ABCD"[a["c"]]} – {esc(a["fb"])}', ex)
P.append(page("Quiz 3", "Abschluss-Quiz", "".join(qcard3(i + 1, a) for i, a in enumerate(ABSCHLUSS)), 22))

# ------------------------------------------------------------------ 23 Glossar
gl = "".join(f'<div style="display:grid;grid-template-columns:58mm 1fr;gap:5mm;padding:3.2mm 0;border-bottom:0.3mm solid #D5D9E3"><b style="color:{NAVY};font-size:12pt">{esc(t)}</b><span style="font-size:11.5pt">{esc(d)}</span></div>' for t, d in GLOSSAR)
P.append(page("Nachschlagen", "Glossar", gl, 23))

# ------------------------------------------------------------------ 24 Quellen
q = "".join(f'<li style="margin-bottom:3.5mm"><a href="{u}" style="color:{NAVY2}">{esc(t)}</a><br><span class="note" style="word-break:break-all">{esc(u)}</span></li>' for t, u in QUELLEN)
P.append(page("Belege", "Quellenverzeichnis", f'<ul style="list-style:none;font-size:10.5pt">{q}</ul>', 24))

# ------------------------------------------------------------------ 25 Rueckseite
P.append(f"""<section class="page" style="background:{NAVY};color:#fff;align-items:center;justify-content:center;text-align:center">
<div style="position:absolute;left:0;top:0;bottom:0;width:14mm;background:{ACCENT}"></div>
<div style="max-width:120mm"><div style="font-size:60pt;font-weight:700;color:{ACCENT};line-height:1;margin-bottom:10mm">§</div>
<p style="font-size:13.5pt;line-height:1.6">Erstellt von Yasin &amp; Mido im Rahmen des Projekts im Themenschwerpunkt Verkürzer.</p>
<p style="font-size:12pt;line-height:1.6;color:#DCE3F2">Rechtsstand: Oktober 2026. Die Praxisbeispiele stammen aus einem anonymisierten Ausbildungsvertrag. Das Booklet dient der Prüfungsvorbereitung und ersetzt keine Rechtsberatung.</p></div>
</section>""")

assert len(P) == 25, len(P)
html = doc("".join(P), "Rechte und Pflichten aus dem Ausbildungsvertrag")
open(os.path.join(os.path.dirname(__file__), "booklet.html"), "w", encoding="utf-8").write(html)

mb = doc(merkblatt_page(None), "Merkblatt")
open(os.path.join(os.path.dirname(__file__), "merkblatt.html"), "w", encoding="utf-8").write(mb)
