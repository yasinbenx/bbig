# -*- coding: utf-8 -*-
import os, sys, json
from html import escape as esc
from playwright.sync_api import sync_playwright
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
M = json.load(open("/tmp/v4_meta.json", encoding="utf-8")); META = M["meta"]
NAVY, ACC = "#1F2A44", "#F5A623"
mm = lambda s: f"{s//60}:{s%60:02d}" if s is not None else "Reserve"
CSS = f"""@page {{ size: A4 landscape; margin: 10mm 10mm 12mm 10mm }}
* {{ box-sizing: border-box }} html {{ -webkit-print-color-adjust: exact; print-color-adjust: exact }}
body {{ font-family: Carlito, Calibri, 'Liberation Sans', Arial, sans-serif; font-size: 8.4pt; line-height: 1.28; color: #1a2238 }}
h1 {{ font-size: 20pt; color: #fff; background: {NAVY}; padding: 5mm 8mm; border-left: 4mm solid {ACC}; margin-bottom: 4mm }}
h2 {{ font-size: 12.5pt; color: {NAVY}; margin: 4mm 0 1.5mm; border-bottom: 0.6mm solid {ACC}; padding-bottom: 0.5mm }}
.grid {{ display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 4mm }} .box {{ border: 0.3mm solid #b8c0d0; border-radius: 1.5mm; padding: 2.5mm 3mm }} .box h3 {{ font-size: 9.5pt; color: {NAVY}; margin-bottom: 1mm }}
.box ul {{ margin-left: 4mm }} .box li {{ margin-bottom: 0.7mm }}
table {{ width: 100%; border-collapse: collapse; table-layout: fixed; font-size: 7.4pt }}
th {{ background: {NAVY}; color: #fff; text-align: left; padding: 1.3mm 1.5mm; font-size: 7.4pt }}
td {{ border-bottom: 0.25mm solid #c9cfdc; padding: 1.2mm 1.5mm; vertical-align: top; overflow-wrap: anywhere }}
tr {{ page-break-inside: avoid }} tr.ph td {{ background: {ACC}; color: {NAVY}; font-weight: 700; font-size: 8.4pt }}
tr.f td:first-child {{ border-left: 1mm solid {ACC} }} tr.a td:first-child {{ border-left: 1mm solid #1e7b4f }}
.mut {{ color: #4a5568 }}"""
rows = ""; cur = None
def row(m):
    cls = "f" if m["kind"] == "Frage" else "a" if m["kind"] == "Antwort" else ""
    return (f'<tr class="{cls}"><td><b>{m["nr"]}</b></td><td>{esc(m["phase"])}<br>{mm(m["dauer"])}</td><td><b>{esc(m["spr"])}</b><br>{esc(m["sozial"])}</td>'
            f'<td><b>{esc(m["title"])}</b> <span class="mut">({esc(m["kind"])})</span><br>{esc(m["impuls"]) or "–"}</td><td>{esc(m["erw"]) or "–"}</td><td>{esc(m["fehl"]) or "–"}</td><td>{esc(m["med"]) or "–"}</td><td>{esc(m["puffer"]) or "–"}</td></tr>')
head = '<tr><th style="width:6mm">Nr.</th><th style="width:16mm">Phase · Zeit</th><th style="width:25mm">Sprecher · Sozialform</th><th style="width:62mm">Folie · Impuls / Moderation (frei)</th><th style="width:46mm">Erwartete Antworten</th><th style="width:50mm">Fehlvorstellungen &amp; Reaktion</th><th style="width:22mm">Medien / Tafel</th><th style="width:30mm">Zeitpuffer / Streichen</th></tr>'
body = ""
for m in [x for x in META if not x["hidden"]]:
    if m["phase"] != cur:
        cur = m["phase"]; tot = sum(x["dauer"] for x in META if not x["hidden"] and x["phase"] == cur)
        body += f'<tr class="ph"><td colspan="8">{esc(cur)} · {mm(tot)} Min.</td></tr>'
    body += row(m)
rb = ""
for m in [x for x in META if x["hidden"]]: rb += row(m)
html = f"""<!doctype html><html lang="de"><head><meta charset="utf-8"><title>Moderationsleitfaden</title><style>{CSS}</style></head><body>
<h1>Moderationsleitfaden: Rechte und Pflichten aus dem Ausbildungsvertrag (GP)</h1>
<p class="mut" style="margin-bottom:2mm">Unterrichtsstunde 45 Minuten · Yasin &amp; Mido · Rechtsstand Oktober 2026 · Drehbuch zu <b>praesentation_unterricht_v3.pptx</b> ({len([m for m in META if not m['hidden']])} sichtbare, {len([m for m in META if m['hidden']])} ausgeblendete Folien). Die Folien tragen dieselben Angaben in den Notizen.</p>
<div class="grid">
<div class="box"><h3>Raumorganisation</h3><ul><li>Beamer + Tafel/Flipchart (Spalten a–d für Vorwissen, Stichwortsammlungen)</li><li>Stühle so, dass Partner:innen zusammensitzen (Think-Pair-Share, Partnerarbeit)</li><li>Freie Fläche für „Aufstellen“: rechts „Stimmt“, links „Stimmt nicht“</li><li>WLAN/Handys vorab testen, QR-Code von hinten lesbar?</li></ul></div>
<div class="box"><h3>Materialliste</h3><ul><li>Merkblatt (ausgeteilt, ein Exemplar je Person)</li><li>Arbeitsblatt „Tafelbild“ (optional, 1 Seite) · Zettel und Stifte</li><li>Ampelkarten (grün/gelb/rot) oder farbige Zettel</li><li>Zettel „Stimmt“ / „Stimmt nicht“ für das Aufstellen</li><li>QR-Code (Folien 40, 44, 57, 61), Plan-B-Folien (ausgeblendet)</li><li>Stoppuhr als Reserve zum Countdown</li></ul></div>
<div class="box"><h3>Rollenverteilung</h3><ul><li><b>Yasin:</b> Einstieg, Block 1, Block 3, Teile der Besprechung</li><li><b>Mido:</b> Lernziele/Ablauf, Block 2, Aufgaben erklären, Abschluss</li><li>Wer nicht spricht, schreibt an der Tafel mit, hält Zeit und beobachtet die Klasse</li><li>Arbeitsphase: Yasin links, Mido rechts durch die Reihen</li></ul></div>
<div class="box"><h3>Bei Zeitnot streichen (Reihenfolge)</h3><ul><li>1. Lückensatz Block 1 (Folien 11–12, −50 s)</li><li>2. Verständnis Ausbildungszeit (15–16, −50 s)</li><li>3. Probezeit 6 Monate (27–28, −45 s)</li><li>4. Ampelkarte Block 2 (29, −40 s)</li><li>5. Arbeitsphase auf 8 Minuten (−2 Min.)</li><li>6. Fall C nur Lösung (−30 s), Mini-Quiz Fragen 1–3 (−30 s)</li><li>Nicht streichen: Vorwissen, Entscheidungsbaum, Detektiv-Auflösung, Merksatz</li></ul></div>
<div class="box"><h3>Umgang mit Schweigen</h3><ul><li>Denkpause (Folie mit Countdown) + Partnergespräch 20 Sekunden</li><li>Frage umformulieren, kleineren Schritt fragen („Was glaubt ihr, ungefähr?“)</li><li>Zuruf statt Meldung erlauben; erste Antwort würdigen, nicht bewerten</li><li>Nie sofort die Lösung nennen</li></ul></div>
<div class="box"><h3>Umgang mit falschen Antworten</h3><ul><li>Sammeln, an der Tafel notieren, nicht sofort korrigieren</li><li>Nachfrage: „Wie kommst du darauf?“ – oft steckt eine richtige Regel (z. B. Arbeitstage statt Werktage)</li><li>Erst bei der Antwort-Folie auflösen, dann Regel + Paragraf nennen</li><li>Fehler als Lernchance: Lernzuwachs am Ende zeigen („Zurück zum Anfang“)</li></ul></div>
</div>
<h2 style="page-break-before:always">Ablauf Folie für Folie (sichtbare Folien, 45:00)</h2>
<table>{head}{body}</table>
<h2>Reserve- und Plan-B-Folien (ausgeblendet, nicht in den 45 Minuten)</h2>
<p class="mut" style="margin-bottom:1.5mm">Nur einblenden, wenn Internet oder Handys ausfallen oder jemand schneller fertig ist: Rechtsklick auf die Folie → „Folie einblenden“. Gleiche Struktur: Frage ohne Lösung → Lösungsfolie.</p>
<table>{head}{rb}</table>
</body></html>"""
out = os.path.join(ROOT, "output/v3"); os.makedirs(out, exist_ok=True)
open("/tmp/leitfaden.html", "w", encoding="utf-8").write(html)

arb = f"""<!doctype html><html lang="de"><head><meta charset="utf-8"><title>Tafelbild / Arbeitsblatt</title><style>
@page {{ size: A4; margin: 0 }} * {{ box-sizing: border-box; margin: 0; padding: 0 }} html {{ -webkit-print-color-adjust: exact; print-color-adjust: exact }}
body {{ font-family: Carlito, Calibri, 'Liberation Sans', Arial, sans-serif; font-size: 12.5pt; line-height: 1.5; color: #1a2238; width: 210mm; height: 297mm; position: relative }}
.head {{ background: {NAVY}; color: #fff; padding: 11mm 16mm 7mm 22mm; position: relative }} .head::before {{ content:''; position:absolute; left:0; top:0; bottom:0; width:6mm; background:{ACC} }}
.k {{ color: {ACC}; font-weight: 700; letter-spacing: .12em; font-size: 9.5pt; text-transform: uppercase }} h1 {{ font-size: 22pt; margin-top: 1mm }}
.body {{ padding: 8mm 16mm 0 22mm }} p.t {{ margin-bottom: 4.5mm }} .l {{ display: inline-block; border-bottom: 0.3mm solid #1a2238; min-width: 28mm; height: 5.5mm; vertical-align: bottom }} .l.w {{ min-width: 55mm }}
h2 {{ font-size: 13pt; color: {NAVY}; margin: 5mm 0 2mm }} .n {{ display:inline-block; width: 7mm; height: 7mm; border-radius: 50%; background: {NAVY}; color: {ACC}; text-align: center; font-weight: 700; margin-right: 2mm; line-height: 7mm; font-size: 11pt }}
.tree {{ border: 0.4mm solid #b8c0d0; border-radius: 2mm; padding: 4mm; height: 62mm; margin-top: 2mm; position: relative }} .tree span {{ position:absolute; font-size: 9pt; color:#4a5568 }}
.foot {{ position: absolute; left: 22mm; right: 16mm; bottom: 8mm; font-size: 9pt; color: #4a5568; border-top: 0.3mm solid #d5d9e3; padding-top: 2mm }}
</style></head><body><div class="head"><div class="k">Arbeitsblatt zum Mitschreiben · Fach GP</div><h1>Tafelbild: Rechte und Pflichten aus dem Ausbildungsvertrag</h1></div>
<div class="body"><h2>Ergänze die Lücken (Lösungen im Unterricht)</h2>
<p class="t"><span class="n">1</span>Seit dem <span class="l"></span> genügt für den Vertragsinhalt die <span class="l"></span>. Vorher war die <span class="l"></span> vorgeschrieben. <span style="color:#4a5568">(§ 11 BBiG)</span></p>
<p class="t"><span class="n">2</span>Die Probezeit dauert mindestens <span class="l" style="min-width:18mm"></span> und höchstens <span class="l" style="min-width:18mm"></span> Monate. <span style="color:#4a5568">(§ 20 BBiG)</span></p>
<p class="t"><span class="n">3</span>Mindestausbildungsvergütung im 1. Jahr bei Beginn 2026: <span class="l"></span> €. <span style="color:#4a5568">(§ 17 BBiG)</span></p>
<p class="t"><span class="n">4</span>Mindesturlaub ab 18 Jahren: <span class="l" style="min-width:18mm"></span> Werktage; unter 17 Jahren (Jahresbeginn): <span class="l" style="min-width:18mm"></span> Werktage. <span style="color:#4a5568">(§ 3 BUrlG, § 19 JArbSchG)</span></p>
<p class="t"><span class="n">5</span>Jugendliche arbeiten höchstens <span class="l" style="min-width:16mm"></span> Stunden täglich und <span class="l" style="min-width:16mm"></span> pro Woche. <span style="color:#4a5568">(§ 8 JArbSchG)</span></p>
<p class="t"><span class="n">6</span>Kündigung in der Probezeit: <span class="l w"></span>; sie muss immer <span class="l"></span> erfolgen. <span style="color:#4a5568">(§ 22 BBiG)</span></p>
<h2>Entscheidungsbaum Kündigung (aus der Stunde ergänzen)</h2>
<div class="tree"><span style="left:42%;top:3mm">Kündigung durch …?</span><span style="left:8%;top:22mm">in der Probezeit → ______________________</span><span style="left:52%;top:22mm">nach der Probezeit → ______________________</span><span style="left:8%;top:40mm">______________________________</span><span style="left:52%;top:40mm">Azubi: __________________________</span></div>
<h2>Meine Notizen</h2><div style="border:0.3mm solid #b8c0d0; border-radius:2mm; height:30mm"></div></div>
<div class="foot">Yasin &amp; Mido · Rechtsstand Oktober 2026 · Zur Prüfungsvorbereitung, keine Rechtsberatung</div></body></html>"""
open("/tmp/arbeitsblatt.html", "w", encoding="utf-8").write(arb)
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome", args=["--no-sandbox"]); pg = b.new_page()
    pg.goto("file:///tmp/leitfaden.html"); pg.wait_for_timeout(300); pg.pdf(path=os.path.join(out, "moderationsleitfaden.pdf"), prefer_css_page_size=True, print_background=True)
    pg.goto("file:///tmp/arbeitsblatt.html"); pg.wait_for_timeout(300); pg.pdf(path=os.path.join(out, "tafelbild_arbeitsblatt.pdf"), prefer_css_page_size=True, print_background=True)
    b.close()
import pymupdf
for f in ("moderationsleitfaden", "tafelbild_arbeitsblatt"):
    d = pymupdf.open(os.path.join(out, f + ".pdf")); print(f, len(d), "Seiten")
    for i, pgx in enumerate(d):
        if i < 3 or f.startswith("tafel"): pgx.get_pixmap(dpi=60).save(f"/tmp/claude-0/-home-user-bbig/039a734c-67c7-5163-9323-eb0bfa939268/scratchpad/{f}_{i+1}.png")
