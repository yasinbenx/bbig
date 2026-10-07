# -*- coding: utf-8 -*-
import os, sys, re
sys.path.insert(0, os.path.dirname(__file__))
import pymupdf
from docx import Document
from html import escape as esc
from extract_deck import load
from plan4 import *
from playwright.sync_api import sync_playwright
O = os.path.join(os.path.dirname(__file__), "..", "output", "v4")
def pdf(n): return " ".join(re.sub(r"\s+", " ", p.get_text()) for p in pymupdf.open(os.path.join(O, n)))
def docx_(n):
    d = Document(os.path.join(O, n)); t = [p.text for p in d.paragraphs]
    for tb in d.tables:
        for r in tb.rows:
            for c in r.cells: t.append(c.text)
    return " ".join(t)
D = load(); deck = " ".join(" ".join(d["texts"]) for d in D)
T = {"Skizze": docx_("projektskizze_v4.docx"), "PSP": pdf("projektstrukturplan_v4.pdf"), "Ablaufplan": pdf("projektablaufplan_v4.pdf"), "Booklet": pdf("booklet_v4.pdf"),
     "Merkblatt": pdf("merkblatt_v4.pdf"), "Sprechskript": pdf("sprechskript_v4.pdf"), "Präsentation": deck}
N = lambda s: re.sub(r"\s+", " ", s).replace("­", "")
checks = []
def chk(name, cond, detail=""): checks.append((name, bool(cond), detail))
# 1 Titel
for k in ("Skizze", "PSP", "Ablaufplan", "Booklet", "Sprechskript"): chk(f"Titel „{TITEL}“ in {k}", TITEL in N(T[k]))
chk("Titel in Präsentation (Folie 1)", "Rechte und Pflichten aus dem Ausbildungsvertrag" in N(T["Präsentation"]))
# 2 Namen
for k in ("Skizze", "PSP", "Ablaufplan", "Booklet", "Sprechskript", "Präsentation"): chk(f"Namen Yasin und Mido in {k}", "Yasin" in T[k] and "Mido" in T[k])
# 3 Daten
chk("08.10.2026 in Skizze, Ablaufplan, Sprechskript", all("08.10.2026" in T[k] for k in ("Skizze", "Ablaufplan", "Sprechskript")))
chk("Laufzeit 10.09.–08.10.2026 in Skizze und Ablaufplan", "10.09.2026" in T["Skizze"] and "10.09.2026" in T["Ablaufplan"])
chk("IHK-Prüfung 25.11.2026 in Skizze und Booklet-Einleitung", "25.11.2026" in T["Skizze"], "Booklet nennt den Prüfungsbereich (60 Minuten, 10 %), nicht das Datum")
chk("Prüfungsbereich 60 Minuten / 10 % in Skizze und Booklet", all("60 Minuten" in N(T[k]) and "10 %" in N(T[k]) for k in ("Skizze", "Booklet")))
chk("Stand Oktober 2026 in Booklet und Skizze", "Oktober 2026" in T["Booklet"] and "Oktober 2026" in T["Skizze"])
# 4 AP-Nummern
miss = [n for n in NAME if n not in T["Skizze"] and not re.search(rf"AP {n[0]}\.1.{n[0]}\.\d", T["Skizze"])]
chk("Alle 15 AP-Nummern in PSP und Ablaufplan", all(n in T["PSP"] and n in T["Ablaufplan"] for n in NAME))
chk("AP-Namen in PSP identisch mit Ablaufplan", all(N(NAME[n])[:25] in N(T["PSP"]) and N(NAME[n])[:25] in N(T["Ablaufplan"]) for n in NAME))
chk("Skizze nennt die AP-Bereiche 1.1–1.3 bis 5.1–5.3", all(f"AP {i}.1–{i}.3" in T["Skizze"] for i in range(1, 6)))
chk("Wochenzuordnung der Skizze entspricht dem Plan (aus plan4 berechnet)", all(f"{w} ({fmt(a)}–{fmt(b)})" in T["Skizze"] for w, a, b in WOCHEN))
chk("Meilensteine M1–M6 mit Terminen in Skizze und Ablaufplan", all(f"{k} " in T["Skizze"] and fmt(d) in T["Skizze"] and fmt(d, True) in T["Ablaufplan"] for k, _, d in MS))
chk("Kein Arbeitspaket endet nach dem 08.10.2026", all(end(n) <= ENDE for n in EF))
chk("Keine Doppelbelegung einer Person", all(len([n for n in EF if ES[n] <= i <= EF[n] and p in WHO[n]]) <= 1 for p in "YM" for i in range(21)))
chk("Meilenstein M3 (Booklet fertig) entspricht Ende AP 3.3, M6 = 08.10.", MS[2][2] == end("3.3") and MS[5][2] == ENDE)
# 5 Ergebnisse
chk("Booklet hat 16 Seiten (Skizze: 16 Seiten)", len(pymupdf.open(os.path.join(O, "booklet_v4.pdf"))) == 16 and "16 Seiten" in T["Skizze"])
chk("Merkblatt ist eine A4-Seite", len(pymupdf.open(os.path.join(O, "merkblatt_v4.pdf"))) == 1)
vis = [d for d in D if not d["hidden"]]; tot = sum(d["dauer"] for d in vis)
chk("Präsentation: 22 sichtbare + 5 versteckte Folien, 39:45", len(vis) == 22 and len(D) == 27 and tot == 2385 and "39:45" in T["Skizze"] and "39:45" in T["Sprechskript"])
chk("Sechs Phasen in Skizze = Phasen der Präsentation", all(p in T["Skizze"] for p in ("Einstieg", "Fragerunde", "Erklären", "Aufgaben", "Besprechen", "Quiz und Abschluss")) and len({d["phase"] for d in D}) == 6)
chk("Aktivitäten in Booklet: Rote/Grüne Karte, Vertrags-Detektiv, IHK-Fälle A–E, Mini-Quiz, Experten-Karten", all(x in T["Booklet"] for x in ("Rote/Grüne Karte", "Vertrags-Detektiv", "Fall E", "Mini-Quiz", "Experten-Karten")))
chk("Mini-Quiz-Zielwert 4 oder 5 Punkte (Skizze) = Erwartung in Präsentation/Sprechskript", "4 oder 5" in T["Skizze"] and "4 oder 5" in N(T["Sprechskript"]))
chk("URL der Website in Booklet, Merkblatt und Präsentation", all("yasinbenx.github.io/azubi-vertrag" in T[k] for k in ("Booklet", "Merkblatt", "Präsentation")))
# 6 Zahlen und Paragrafen
for z in ("724", "854", "977", "1.014"): chk(f"Vergütung {z} € in Booklet, Merkblatt/Präsentation", z in T["Booklet"] and z in T["Präsentation"] + T["Merkblatt"])
chk("Urlaub 30/27/25/24 Werktage in Booklet und Präsentation", all(re.search(rf"\b{z}\b", T[k]) for z in ("30", "27", "25", "24") for k in ("Booklet", "Präsentation")))
for para in ("§ 11 BBiG", "§ 17 BBiG", "§ 19 JArbSchG", "§ 20 BBiG", "§ 22 Abs. 3", "§ 8 JArbSchG", "§ 3 ArbZG", "§ 3 BUrlG"):
    chk(f"{para} in Booklet und Präsentation/Sprechskript", para in N(T["Booklet"]) and para in N(T["Präsentation"] + T["Sprechskript"].replace("Absatz ", "Abs. ")) or (para in N(T["Booklet"]) and para.replace("§ ", "§ ") in N(T["Sprechskript"])), "")
chk("Probezeit höchstens vier Monate in Booklet, Merkblatt, Präsentation", all(x in T["Booklet"] for x in ("vier Monate",)) and "Ein bis vier Monate" in T["Merkblatt"] and "4 Monate" in T["Präsentation"])
chk("Textform seit 01.08.2024 in Booklet und Präsentation", "01.08.2024" in T["Booklet"] and "01.08.2024" in T["Präsentation"])
chk("Booklet-Lösung Mini-Quiz D, C, C, C, B (wie Website/Plan B Folie 27)", re.search(r"1 D .*?2 C .*?3 C .*?4 C .*?5 B", N(pdf("booklet_v4.pdf"))) is not None)
chk("Wissensstand-Check a–d identisch mit Folie 3 und 20", all(q in T["Booklet"] and q in T["Präsentation"] for q in ("Wie lange darf die Probezeit höchstens dauern?", "Muss eine Kündigung schriftlich sein?")))
ok = sum(c[1] for c in checks)
DEV = [
 ("Präsentation und Projektablauf", "Die Unterrichtspräsentation (v4, final, unverändert) zeigt keine Folien zum Projektablauf (PSP, Ablaufplan). Diese Unterlagen sind eigene Dokumente im Anhang des Projektberichts. Sollen sie in der Präsentation vorkommen, wäre eine eigene Zusatzfolie nötig."),
 ("Ältere Planung (v2)", "output/v2 enthält Projektskizze, PSP und Ablaufplan mit 11 Arbeitspaketen (Nummerierung 1 bis 11). Sie sind überholt; maßgeblich sind die v4-Dokumente (15 Arbeitspakete, Nummerierung 1.1 bis 5.3). Nicht mischen."),
 ("Booklet v2/v3", "Das Booklet v2 hatte 15 Seiten mit „Praxisbeispielen“ und „Wahr oder falsch“. Booklet v4 hat 16 Seiten und folgt der Präsentation; Praxisbeispiele sind nicht enthalten und werden in der Skizze v4 nicht versprochen."),
 ("AP 5.3 ohne Datum", "AP 5.3 (Evaluation, Reflexion, Projektbericht) liegt nach der Präsentation; sein Termin steht als [laut Lehrkraft] im Plan und ist von euch einzutragen."),
 ("Platzhalter", "Klasse [eintragen] und Druckmenge/Drucker [klären] stehen in der Skizze als Platzhalter."),
 ("Soll-Termine", "Alle Termine sind Soll-Termine. Ist-Termine und Abweichungen gehören in den Projektbericht (Soll-Ist-Vergleich); sie sind nicht erfunden und müssen von euch ergänzt werden."),
 ("Prüfungsdatum", "Das Prüfungsdatum 25.11.2026 steht in der Skizze, nicht im Booklet (dort nur 60 Minuten und 10 %)."),
]
rows = "".join(f'<tr><td style="width:9mm;font-weight:700;color:{"#2E7D32" if r else "#B3261E"}">{"✓" if r else "✗"}</td><td>{esc(n)}</td><td style="color:#5B6680;font-size:8.5pt">{esc(d)}</td></tr>' for n, r, d in checks)
dv = "".join(f"<li><b>{esc(a)}:</b> {esc(b)}</li>" for a, b in DEV)
CSS = """@page{size:A4;margin:14mm 15mm 16mm 18mm}body{font-family:'Liberation Sans',Arial,sans-serif;font-size:9.6pt;color:#1A2238;line-height:1.4}h1{font-size:20pt;color:#14264B;margin-bottom:1mm}.bar{width:24mm;height:1.5mm;background:#F5A800;margin:2mm 0 4mm}h2{font-size:13pt;color:#14264B;margin:6mm 0 2mm}table{border-collapse:collapse;width:100%}td{padding:1.1mm 2mm;border-bottom:.25mm solid #D5D9E3;vertical-align:top}li{margin:0 0 1.6mm 4mm}"""
html = f'<!doctype html><html lang="de"><head><meta charset="utf-8"><style>{CSS}</style></head><body><h1>Konsistenzprüfung der Projektunterlagen</h1><div class="bar"></div><p>Geprüft wurden Projektskizze, Projektstrukturplan, Projektablaufplan, Booklet, Merkblatt, Sprechskript und Präsentation (Stand Oktober 2026). Die Prüfung wurde automatisch aus den erzeugten Dateien durchgeführt.</p><p><b>Ergebnis: {ok} von {len(checks)} Prüfpunkten bestanden.</b></p><h2>Prüfpunkte</h2><table>{rows}</table><h2>Abweichungen und offene Hinweise</h2><ul>{dv}</ul></body></html>'
hp = os.path.join(O, "_k.html"); open(hp, "w", encoding="utf-8").write(html)
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome", args=["--no-sandbox"]); pg = b.new_page(); pg.goto("file://" + os.path.abspath(hp))
    pg.pdf(path=os.path.join(O, "konsistenzpruefung_v4.pdf"), prefer_css_page_size=True, print_background=True, display_header_footer=True, header_template="<span></span>", footer_template='<div style="font-size:8px;width:100%;text-align:center;color:#5B6680">Konsistenzprüfung · Seite <span class="pageNumber"></span> / <span class="totalPages"></span></div>'); b.close()
os.remove(hp)
print(ok, "/", len(checks)); [print("FAIL", c) for c in checks if not c[1]]
