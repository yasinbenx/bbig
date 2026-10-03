# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from html import escape as esc
from pdfkit import *
from data2 import *
OUT = os.path.join(os.path.dirname(__file__), "..", "output", "v2"); os.makedirs(OUT, exist_ok=True)
P = []
A = lambda t, extra="": f'<p style="{extra}">{esc(t)}</p>'

# 1 Cover
P.append(f"""<section class="page" style="background:{NAVY};color:#fff">
<div style="position:absolute;left:0;top:0;bottom:0;width:14mm;background:{ACCENT}"></div>
<div style="position:absolute;right:-10mm;top:22mm;font-size:300pt;line-height:1;font-weight:700;color:{NAVY2}">§</div>
<div style="position:absolute;left:34mm;right:24mm;top:108mm">
 <div style="color:{ACCENT};font-size:11pt;font-weight:700;letter-spacing:.14em;text-transform:uppercase;margin-bottom:6mm">Booklet</div>
 <div style="font-size:40pt;line-height:1.1;font-weight:700">Rechte und Pflichten aus dem Ausbildungsvertrag</div>
 <div style="width:30mm;height:1.6mm;background:{ACCENT};margin:9mm 0 8mm"></div>
 <div style="font-size:18pt;color:{ACCENT};font-weight:700">Prüfungsvorbereitung im Fach GP (Geschäftsprozesse)</div>
 <div style="font-size:14pt;margin-top:4mm;color:#DCE3F2">Kaufleute für Büromanagement · Stand Oktober 2026</div></div>
<div style="position:absolute;left:34mm;bottom:22mm;font-size:14pt">von Yasin &amp; Mido</div></section>""")

# 2 Einleitung
toc = [("Vertrag und Dauer", "3"), ("Ausbildungszeit und Vergütung", "4"), ("Urlaub und Probezeit", "5"), ("Kündigung", "6"), ("Pflichten von Azubi und Ausbildenden", "7"),
       ("Praxisbeispiele", "8"), ("Merkblatt", "9"), ("Aufgaben", "10"), ("Erwartungshorizont", "11"), ("Mini-Quiz und Quellen", "12"), ("Glossar", "13")]
tl = "".join(f'<div style="display:flex;gap:2mm;font-size:11pt;margin-bottom:1.6mm"><span style="color:{NAVY};font-weight:700">{esc(a)}</span><span style="flex:1;border-bottom:0.4mm dotted #9AA3B8;transform:translateY(-1mm)"></span><b>{b}</b></div>' for a, b in toc)
steps = ["Lies die Seiten 3 bis 8.", "Trenne das Merkblatt auf Seite 9 heraus.", "Löse die Aufgaben auf Seite 10 und vergleiche erst danach mit dem Erwartungshorizont auf Seite 11.", "Teste dich mit dem Mini-Quiz auf Seite 12."]
sl = "".join(f'<li style="margin-bottom:2.5mm">{esc(s)}</li>' for s in steps)
P.append(page("Einleitung", "Einleitung und „So nutzt du das Booklet“", f"""
<p class="lead">Jede Berufsausbildung beginnt mit einem Vertrag – und der regelt mehr, als viele denken. Dieses Booklet fasst zusammen, was im Berufsbildungsgesetz (BBiG) zu Beginn, Dauer, Arbeitszeit, Vergütung, Urlaub, Probezeit und Kündigung steht. Kurz, verständlich, mit echten Beispielen.</p>
<div style="margin:7mm 0;background:{NAVY};color:#fff;border-radius:3mm;padding:6mm 7mm;border-left:3mm solid {ACCENT}">
<div style="color:{ACCENT};font-size:10pt;font-weight:700;letter-spacing:.12em;text-transform:uppercase;margin-bottom:2mm">So wird geprüft</div>
<div style="font-size:13pt;line-height:1.5">Im IHK-Prüfungsbereich Wirtschafts- und Sozialkunde hast du 60 Minuten für fallbezogene Aufgaben; der Bereich zählt 10 % der Gesamtnote (<a style="color:{ACCENT}" href="{VERORDNUNG_URL}">Verordnung</a>). Genau solche Fälle übst du ab Seite 10.</div></div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:8mm;align-items:start">
<div style="background:{ACCENT_L};border-top:2mm solid {ACCENT};border-radius:0 0 3mm 3mm;padding:5mm 6mm 3mm"><div style="font-size:14pt;font-weight:700;color:{NAVY};margin-bottom:3mm">So nutzt du das Booklet:</div><ol style="margin-left:5mm;font-size:12pt;line-height:1.4">{sl}</ol></div>
<div><div style="font-size:10pt;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:{MUTED};margin-bottom:2mm">Inhalt</div>{tl}</div></div>""", 2))

# 3 Vertrag und Dauer
svg = f"""<svg viewBox="0 0 700 262" xmlns="http://www.w3.org/2000/svg" style="width:100%;font-family:'Liberation Sans',Arial">
<defs><marker id="ag" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0 0L8 4L0 8z" fill="#2E8B57"/></marker><marker id="ao" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0 0L8 4L0 8z" fill="#D9730D"/></marker></defs>
<text x="20" y="22" font-size="19" font-weight="700" fill="#2E8B57">Verkürzung</text><text x="20" y="44" font-size="15" fill="{INK}">auf gemeinsamen Antrag (§ 8 Abs. 1 BBiG)</text>
<path d="M545 70 L400 70" stroke="#2E8B57" stroke-width="6" marker-end="url(#ag)"/>
<rect x="40" y="90" width="520" height="32" rx="4" fill="{NAVY}"/><text x="300" y="112" text-anchor="middle" fill="#fff" font-size="16" font-weight="700">Ausbildungsdauer: meist 2 bis 3,5 Jahre</text>
<circle cx="40" cy="106" r="10" fill="{ACCENT}" stroke="{NAVY}" stroke-width="3"/><circle cx="560" cy="106" r="10" fill="{ACCENT}" stroke="{NAVY}" stroke-width="3"/>
<path d="M580 106 L685 106" stroke="#D9730D" stroke-width="6" marker-end="url(#ao)"/>
<text x="20" y="150" font-size="16" font-weight="700" fill="{NAVY}">Ausbildungsbeginn</text><text x="560" y="150" text-anchor="middle" font-size="16" font-weight="700" fill="{NAVY}">Prüfung</text>
<text x="560" y="170" text-anchor="middle" font-size="13" fill="{MUTED}">Ende mit Bekanntgabe (§ 21 Abs. 2 BBiG)</text>
<text x="20" y="205" font-size="19" font-weight="700" fill="#D9730D">Verlängerung</text>
<text x="20" y="228" font-size="15" fill="{INK}">nur in Ausnahmefällen auf Antrag des Azubis (§ 8 Abs. 2 BBiG) oder</text><text x="20" y="249" font-size="15" fill="{INK}">nach nicht bestandener Prüfung bis zu 1 Jahr (§ 21 Abs. 3 BBiG)</text></svg>"""
ic = [("calendar", "Beginn und Dauer"), ("clock", "Tägliche Ausbildungszeit"), ("euro", "Vergütung"), ("palm", "Urlaub"), ("hourglass", "Probezeit"), ("doc", "Kündigung")]
cells = "".join(f'<div style="display:flex;align-items:center;gap:2.5mm;border:0.4mm solid #D5D9E3;border-radius:2mm;padding:1.8mm 2.5mm">{icon(n, "8mm")}<div style="font-weight:700;color:{NAVY};font-size:9.5pt;line-height:1.2">{esc(t)}</div></div>' for n, t in ic)
P.append(page("Kapitel 1 bis 3", "Vertrag und Dauer", f"""
<div style="display:grid;grid-template-columns:1fr 1fr;gap:7mm"><div>
<h2 style="margin-top:0">Das BBiG</h2><p style="font-size:11pt">Das BBiG regelt bundesweit die betriebliche Berufsausbildung in Deutschland. Es legt fest, welche Rechte und Pflichten Auszubildende und Ausbildende haben – vom Vertragsschluss bis zur Abschlussprüfung.</p></div>
<div>{merk("Das BBiG ist die gesetzliche Grundlage jeder dualen Ausbildung.")}</div></div>
<h2 style="margin:3mm 0 2mm">Der Berufsausbildungsvertrag</h2><p style="font-size:11pt;margin-bottom:2mm">Nach § 11 BBiG muss der Ausbildungsvertrag unter anderem enthalten:</p>
<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:2.5mm;margin-bottom:3mm">{cells}</div>
<div class="info" style="margin:2mm 0 0;padding:3mm 5mm"><span class="lbl">Textform-Regel</span><span style="font-size:10.5pt">Seit dem 1. August 2024 darf der wesentliche Vertragsinhalt in Textform abgefasst werden, zum Beispiel per E-Mail; vorher war die Papierform vorgeschrieben (§ 11 BBiG).</span></div>
<h2 style="margin:3mm 0 1.5mm">Beginn und Dauer der Ausbildung</h2>
<p style="font-size:9.8pt;line-height:1.4;margin-bottom:2mm">Die Ausbildungsdauer richtet sich nach der jeweiligen Ausbildungsordnung, meist 2 bis 3,5 Jahre. Eine Verkürzung ist auf gemeinsamen Antrag von Azubi und Ausbildenden möglich (§ 8 Abs. 1 BBiG), nach der Praxis der IHK zum Beispiel um bis zu sechs Monate mit mittlerem Schulabschluss oder bis zu zwölf Monate mit Abitur. Eine Verlängerung gibt es nur in Ausnahmefällen auf Antrag des Azubis (§ 8 Abs. 2 BBiG) oder nach nicht bestandener Abschlussprüfung bis zur Wiederholungsprüfung, höchstens um ein Jahr (§ 21 Abs. 3 BBiG). Bei bestandener Prüfung endet die Ausbildung mit der Bekanntgabe des Ergebnisses (§ 21 Abs. 2 BBiG).</p>
<div style="border:0.4mm solid #D5D9E3;border-radius:3mm;padding:2mm 3mm 0;width:88%">{svg}</div>""", 3))

# 4 Ausbildungszeit und Verguetung
def big(num, unit, sub, head, acc=False):
    return f'<div class="col"><div class="ch{" acc" if acc else ""}" style="padding:2mm 4mm;font-size:11pt">{head}</div><div class="cb" style="text-align:center;padding:4mm 4mm"><div style="font-size:30pt;font-weight:700;color:{NAVY};line-height:1">{num}</div><div style="font-size:11.5pt;font-weight:700;color:{NAVY};margin-bottom:2mm">{unit}</div><div style="font-size:9.5pt">{sub}</div></div></div>'
rows = "".join(f'<tr><td class="b" style="padding:2mm 4mm">{j}</td><td style="font-weight:700;padding:2mm 4mm">{v:,} €</td></tr>'.replace(",", ".") for j, v in VERGUETUNG)
bars = ""
for j, v in VERGUETUNG:
    bars += f'<div style="display:flex;align-items:center;gap:3mm;margin-bottom:1.8mm"><div style="width:15mm;font-weight:700;color:{NAVY};font-size:10pt">{j}</div><div style="flex:1;background:#EEF1F7;border-radius:1.5mm"><div style="width:{v/1014*100:.1f}%;background:{NAVY if j!="4. Jahr" else ACCENT};height:7mm;border-radius:1.5mm;display:flex;align-items:center;justify-content:flex-end;padding-right:3mm;color:{"#fff" if j!="4. Jahr" else NAVY};font-weight:700;font-size:10pt">{f"{v:,}".replace(",", ".")} €</div></div></div>'
P.append(page("Kapitel 4 und 5", "Ausbildungszeit und Vergütung", f"""
<h2 style="margin-top:0">Tägliche Ausbildungszeit</h2>
<div class="two" style="margin-bottom:3mm">
{big("8", "Stunden täglich", "höchstens 40 Stunden wöchentlich; ausnahmsweise 8,5 Stunden täglich, wenn in derselben Woche ausgeglichen wird (§ 8 JArbSchG)", "Jugendliche")}
{big("bis 10", "Stunden mit Ausgleich", "grundsätzlich höchstens 8 Stunden täglich; im Durchschnitt von sechs Monaten dürfen 8 Stunden nicht überschritten werden, höchstens aber 48 Stunden pro Woche (§ 3 ArbZG)", "Volljährige", True)}</div>
<p style="font-size:10.5pt">Für minderjährige Azubis gilt das Jugendarbeitsschutzgesetz, für volljährige Azubis das Arbeitszeitgesetz.</p>
<h2>Ausbildungsvergütung</h2>
<p style="font-size:11pt">Seit 2020 gilt eine gesetzliche Mindestausbildungsvergütung nach § 17 BBiG. Für Ausbildungsverträge, die 2026 beginnen:</p>
<div style="display:grid;grid-template-columns:1fr 1.25fr;gap:7mm;align-items:center;margin:2mm 0">
<table class="t"><tr><th style="font-size:10pt">Ausbildungsjahr</th><th style="font-size:10pt">Mindestvergütung</th></tr>{rows}</table><div>{bars}</div></div>
{merk("Die Vergütung steigt jedes Jahr – und darf diese Mindestbeträge nicht unterschreiten.")}""", 4))

# 5 Urlaub und Probezeit
palm = icon("palm", "9mm")
urows = "".join(f'<tr><td style="width:14mm;padding:1.8mm 3mm">{palm}</td><td style="font-size:11.5pt;padding:1.8mm 3mm">{esc(a)}</td><td style="font-size:11.5pt;font-weight:700;color:{NAVY};padding:1.8mm 3mm">{esc(b)}</td></tr>' for a, b in URLAUB)
seg = "".join(f'<div style="flex:1;background:{NAVY if i<3 else ACCENT};color:{"#fff" if i<3 else NAVY};text-align:center;padding:3mm 0;font-weight:700;font-size:11.5pt;border-right:0.8mm solid #fff">{i+1}. Monat</div>' for i in range(4))
P.append(page("Kapitel 6 und 7", "Urlaub und Probezeit", f"""
<h2 style="margin-top:0">Urlaub</h2>
<table class="t"><tr><th></th><th style="font-size:10pt">Status</th><th style="font-size:10pt">Urlaubsanspruch</th></tr>{urows}</table>
<p class="note" style="margin-top:3mm">Grundlage: § 19 Jugendarbeitsschutzgesetz (Minderjährige), § 3 Bundesurlaubsgesetz (Volljährige).</p>
<h2 style="margin-top:8mm">Probezeit</h2>
<p style="font-size:11.5pt">Jedes Berufsausbildungsverhältnis beginnt mit einer Probezeit (§ 20 BBiG) von mindestens einem, höchstens vier Monaten.</p>
<div style="margin:5mm 0 1mm;display:flex;border-radius:2mm;overflow:hidden">{seg}</div>
<div style="display:flex;justify-content:space-between;font-size:10pt;color:{MUTED};margin-bottom:4mm"><span>mindestens 1 Monat</span><span>höchstens 4 Monate</span></div>
{merk("Keine Probezeit, keine Ausbildung – sie ist gesetzlich Pflicht.", big=True)}""", 5))

# 6 Kuendigung
P.append(page("Kapitel 8", "Kündigung", f"""
<div class="two" style="margin-bottom:6mm">
<div class="col"><div class="ch">In der Probezeit</div><div class="cb" style="font-size:12.5pt">Während der Probezeit kann jede Seite jederzeit ohne Kündigungsfrist kündigen (§ 22 Abs. 1 BBiG).</div></div>
<div class="col"><div class="ch acc">Nach der Probezeit</div><div class="cb" style="font-size:12.5pt">Nach der Probezeit ist eine Kündigung nur noch möglich:<ul class="l" style="margin-top:2mm"><li>fristlos aus wichtigem Grund (beide Seiten), oder</li><li>durch den Azubi selbst mit vierwöchiger Frist, wenn er die Ausbildung aufgeben oder sich für eine andere Berufstätigkeit ausbilden lassen will.</li></ul></div></div></div>
{warn("Jede Kündigung muss schriftlich erfolgen; eine elektronische Form ist ausgeschlossen (§ 22 Abs. 3 BBiG).", "Schriftform")}""", 6))

# 7 Pflichten
az = ["sich bemühen, die berufliche Handlungsfähigkeit zu erwerben", "aufgetragene Aufgaben sorgfältig ausführen", "Weisungen befolgen und die Ordnung der Ausbildungsstätte beachten", "Werkzeug und Einrichtungen pfleglich behandeln", "über Betriebs- und Geschäftsgeheimnisse Stillschweigen wahren", "einen Ausbildungsnachweis (Berichtsheft) führen"]
ab = ["das Ausbildungsziel planmäßig vermitteln und selbst ausbilden oder einen Ausbilder beauftragen", "Ausbildungsmittel kostenlos zur Verfügung stellen", "Azubis zum Berufsschulbesuch und zum Führen des Ausbildungsnachweises anhalten und diesen regelmäßig durchsehen", "Azubis charakterlich fördern und nicht gefährden", "für Berufsschule und Prüfungen freistellen (§ 15), auch am Arbeitstag vor der schriftlichen Abschlussprüfung", "bei Ende der Ausbildung ein schriftliches Zeugnis ausstellen (§ 16)", "eine angemessene Vergütung zahlen (§ 17)"]
li = lambda xs: "<ul class='l' style='font-size:11pt'>" + "".join(f"<li>{esc(x)}</li>" for x in xs) + "</ul>"
P.append(page("Kapitel 9", "Pflichten von Azubi und Ausbildenden", f"""
{A("Neben dem Vertrag regelt das BBiG, was beide Seiten tun müssen.")}
<div class="two"><div class="col"><div class="ch">Pflichten der Auszubildenden<br><span style="font-size:9.5pt;font-weight:400">§ 13 BBiG</span></div><div class="cb">{li(az)}</div></div>
<div class="col"><div class="ch acc">Pflichten der Ausbildenden<br><span style="font-size:9.5pt;font-weight:400">§§ 14 bis 17 BBiG</span></div><div class="cb">{li(ab)}</div></div></div>
<div style="margin-top:7mm;background:{NAVY};color:#fff;border-radius:2.5mm;padding:5mm 7mm;border-left:3mm solid {ACCENT}"><span style="color:{ACCENT};font-size:9pt;font-weight:700;letter-spacing:.1em;text-transform:uppercase">Merksatz</span><div style="font-size:14pt;font-weight:700;margin-top:1mm">Der Betrieb bildet aus und zahlt, der Azubi lernt, folgt und schweigt über Betriebsgeheimnisse.</div></div>""", 7))

# 8 Praxisbeispiele (leerer Rahmen)
rows8 = "".join(f"""<div style="display:grid;grid-template-columns:1.15fr 1fr;gap:6mm;margin-bottom:6mm;height:63mm"><div style="border:0.5mm dashed #9AA3B8;border-radius:2.5mm;position:relative;background:#FBFCFE"><span style="position:absolute;left:4mm;top:3mm;font-size:9pt;color:{MUTED}">Vertragsauszug {i} (anonymisiert)</span></div><div style="border:0.5mm solid #D5D9E3;border-radius:2.5mm;position:relative"><span style="position:absolute;left:4mm;top:3mm;font-size:9pt;color:{MUTED}">Erklärung zu Auszug {i}</span></div></div>""" for i in (1, 2, 3))
P.append(page("Kapitel 10", "Praxisbeispiele aus dem eigenen Ausbildungsverhältnis", rows8, 8))

# 9 Merkblatt
P.append(merkblatt_page(9))

# 10 Aufgaben
def fall_c(f):
    ans = "".join(f'<div style="display:flex;gap:1.6mm;margin-top:0.6mm;font-size:8.4pt;line-height:1.22"><b style="flex:none;width:4.2mm;height:4.2mm;border-radius:50%;border:0.35mm solid {NAVY};color:{NAVY};text-align:center;line-height:3.6mm;font-size:7.6pt">{L}</b><span>{esc(t)}</span></div>' for L, t in zip("ABCD", f["a"]))
    return f'<div style="border-left:1.6mm solid {NAVY};background:#F9FAFD;padding:1.6mm 2.6mm;margin-bottom:2mm"><div style="font-weight:700;color:{NAVY};font-size:9.2pt;margin-bottom:0.6mm"><span style="background:{NAVY};color:{ACCENT};border-radius:1mm;padding:0 1.4mm;margin-right:1.4mm">{f["id"]}</span>Fall {f["id"]} ({esc(f["titel"])})</div><div style="font-size:8.4pt;line-height:1.25">{esc(f["q"])}</div>{ans}</div>'
det = "".join(f'<div style="margin-bottom:0.6mm">{esc(t)}</div>' for t, _ in DET)
kopf = "".join(f'<div style="{"font-weight:700;color:"+NAVY+";margin-bottom:0.6mm" if i==0 else ""}">{esc(t)}</div>' for i, t in enumerate(DET_KOPF))
wf = "".join(f'<div style="display:grid;grid-template-columns:4mm 1fr 8mm 8mm;gap:1.2mm;padding:1.1mm 0;border-bottom:0.25mm solid #D5D9E3;align-items:start"><b style="color:{NAVY};font-size:8.6pt">{i+1}</b><div style="font-size:8.3pt;line-height:1.22">{esc(t)}</div><div style="text-align:center;font-size:10pt;line-height:1">☐</div><div style="text-align:center;font-size:10pt;line-height:1">☐</div></div>' for i, (t, _, _) in enumerate(RG))
wfh = f'<div style="display:grid;grid-template-columns:4mm 1fr 8mm 8mm;gap:1.2mm;font-size:6.8pt;color:{MUTED};text-align:center;line-height:1.1;margin-bottom:0.8mm"><span></span><span></span><span>stimmt</span><span>stimmt nicht</span></div>'
P.append(page("Aufgaben", "Aufgaben", f"""
<div style="margin-top:-5mm">
<div style="font-size:9.4pt;margin-bottom:1.2mm"><b style="color:{NAVY}">Aufgabe 1 · Vertrags-Detektiv:</b> Im Auszug stecken 5 Fehler. Finde sie und begründe sie mit der passenden Regel.</div>
<div style="background:#F6F8FC;border:0.4mm solid #BFC6D6;border-radius:2mm;padding:2mm 4mm;font-family:'Liberation Serif',serif;font-size:9.3pt;line-height:1.25">{kopf}<div style="border-top:0.3mm solid #BFC6D6;margin:1.2mm 0"></div>{det}</div>
<div style="display:grid;grid-template-columns:101mm 1fr;gap:5mm;margin-top:2.6mm;align-items:start">
<div><div style="font-weight:700;color:{NAVY};font-size:9.6pt;margin-bottom:1.2mm">Aufgabe 2 · IHK-Fälle A bis C <span style="font-weight:400;color:{MUTED}">(wähle A–D, begründe mit einer Regel)</span></div>{"".join(fall_c(f) for f in FAELLE_ABC)}</div>
<div><div style="font-weight:700;color:{NAVY};font-size:9.6pt;margin-bottom:1mm">Aufgabe 3 · Wahr oder falsch</div>{wfh}{wf}</div></div></div>""", P_AUFG))

# 11 Erwartungshorizont
t_det = "".join(f'<tr><td class="b" style="text-align:center">{n}</td><td>{esc(a)}</td><td>{esc(b)}</td><td style="text-align:center;white-space:nowrap">2 (1 + 1)</td></tr>' for n, (a, b) in FEHLER.items())
t_f = "".join(f'<tr><td class="b" style="text-align:center">{f["id"]}</td><td class="b" style="text-align:center">{"ABCD"[f["c"]]}</td><td>{esc(f["begr"])} ({esc(f["para"])})</td><td style="text-align:center;white-space:nowrap">2 (1 + 1)</td></tr>' for f in FAELLE_ABC)
t_w = "".join(f'<tr><td class="b" style="text-align:center">{i+1}</td><td class="b" style="white-space:nowrap">{"Stimmt" if ok else "Stimmt nicht"}</td><td>{esc(b)}</td><td style="text-align:center">1</td></tr>' for i, (_, ok, b) in enumerate(RG))
sm = "font-size:8.6pt"
P.append(page("Lösungen", "Erwartungshorizont", f"""<style>.eh table.t td{{padding:1mm 2.2mm}} .eh table.t th{{padding:1.3mm 2.2mm}}</style><div class="eh">
<div style="font-size:10pt;margin-bottom:1.5mm"><b style="color:{NAVY}">Aufgabe 1 · Vertrags-Detektiv</b> (je Fehler 1 Punkt fürs Finden und 1 Punkt für die Begründung, höchstens 10)</div>
<table class="t" style="{sm}"><tr><th style="width:11mm">Fehler</th><th style="width:34mm">Stelle</th><th>Lösung mit Regel</th><th style="width:20mm">Punkte</th></tr>{t_det}</table>
<div style="font-size:10pt;margin:3.5mm 0 1.5mm"><b style="color:{NAVY}">Aufgabe 2 · IHK-Fälle</b> (je Fall 2 Punkte)</div>
<table class="t" style="{sm}"><tr><th style="width:11mm">Fall</th><th style="width:15mm">Lösung</th><th>Begründung mit Regel</th><th style="width:20mm">Punkte</th></tr>{t_f}</table>
<div style="font-size:10pt;margin:3.5mm 0 1.5mm"><b style="color:{NAVY}">Aufgabe 3 · Wahr oder falsch</b> (je Aussage 1 Punkt)</div>
<table class="t" style="{sm}"><tr><th style="width:11mm">Nr.</th><th style="width:24mm">Lösung</th><th>Begründung mit Paragraf</th><th style="width:20mm">Punkte</th></tr>{t_w}</table>
<div style="margin-top:3mm;background:{ACCENT_L};border-left:2mm solid {ACCENT};padding:2.5mm 4mm;font-size:10pt"><b style="color:{NAVY}">Gesamt: höchstens 26 Punkte</b> (Detektiv höchstens 10 + Fälle 3 × 2 + Wahr oder falsch 10 × 1).</div></div>""", P_EH))

# 12 Mini-Quiz + Quellen
def qcard(i, text, sol):
    return f'<div class="card" style="margin-bottom:3mm;padding:2.4mm 5mm"><div style="display:flex;gap:3mm"><span class="num" style="flex:none">{i}</span><div style="font-size:11pt;font-weight:700;color:{NAVY}">{esc(text)}</div></div><div class="sol" style="padding:1.4mm 3.5mm;margin-top:1.5mm"><b>Lösung:</b> {esc(sol)}</div></div>'
q = "".join(f'<li style="margin-bottom:1.2mm"><a href="{u}" style="color:{NAVY2}">{esc(t)}</a></li>' for t, u in QUELLEN)
P.append(page("Quiz", "Mini-Quiz und Quellenverzeichnis", A("Ordne die Situation der passenden Regelung zu. Die Lösung steht jeweils dahinter.", "font-size:10.5pt") + "".join(qcard(i + 1, a, b) for i, (a, b) in enumerate(SELBSTTEST)) +
              f'<div style="font-size:9pt;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:{MUTED};margin:4mm 0 1.5mm">Quellenverzeichnis</div><ul style="list-style:none;font-size:7.8pt;line-height:1.3">{q}</ul>', P_QUIZ))

# 13 Glossar
gl = "".join(f'<div style="display:grid;grid-template-columns:58mm 1fr;gap:5mm;padding:3.2mm 0;border-bottom:0.3mm solid #D5D9E3"><b style="color:{NAVY};font-size:12pt">{esc(t)}</b><span style="font-size:11.5pt">{esc(d)}</span></div>' for t, d in GLOSSAR)
P.append(page("Nachschlagen", "Glossar", gl, 13))

assert len(P) == 13, len(P)
open(os.path.join(os.path.dirname(__file__), "v2_booklet.html"), "w", encoding="utf-8").write(doc("".join(P), "Rechte und Pflichten aus dem Ausbildungsvertrag"))
