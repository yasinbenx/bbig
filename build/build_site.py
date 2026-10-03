# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from html import escape as esc
from site_data import build_data

SITE = os.path.join(os.path.dirname(__file__), "..", "site")
for d in ("css", "js"): os.makedirs(os.path.join(SITE, d), exist_ok=True)
FOOT = "Erstellt von Yasin &amp; Mido · GP · Rechtsstand Oktober 2026 · Zur Prüfungsvorbereitung, keine Rechtsberatung"
PAGES = [("rote-gruene-karte.html", "rg", "Rote/Grüne Karte", "10 Aussagen: stimmt oder stimmt nicht?"),
         ("vertrags-detektiv.html", "det", "Vertrags-Detektiv", "5 Fehler im Vertragsauszug finden"),
         ("ihk-faelle.html", "faelle", "IHK-Fälle", "Fälle A bis E wie in der Prüfung"),
         ("mini-quiz.html", "quiz", "Mini-Quiz", "5 Fragen zum Abschluss"),
         ("experten-karten.html", "experten", "Experten-Karten", "4 Themenkarten mit Frage an die Klasse"),
         ("merkblatt.html", "merk", "Merkblatt", "Das Wichtigste auf einer Seite, zum Drucken"),
         ("quellen.html", "quellen", "Quellen", "Quellenverzeichnis, Stand Oktober 2026")]
TITLE = "Rechte und Pflichten aus dem Ausbildungsvertrag"

def page(file, key, title, body):
    cur = ' aria-current="page"'
    nav = "".join(f'<a href="{f}"{cur if f == file else ""}>{esc(t)}</a>' for f, _, t, _ in PAGES)
    home = file == "index.html"
    return f"""<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<meta name="description" content="Übungsseite zu den Rechten und Pflichten aus dem Ausbildungsvertrag. Keine Anmeldung, keine Datenübertragung.">
<title>{esc(title) + ("" if home else " · Ausbildungsvertrag")}</title>
<link rel="icon" href="data:,">
<link rel="stylesheet" href="css/style.css">
</head>
<body data-page="{key}">
<a class="skip" href="#inhalt">Zum Inhalt springen</a>
<header class="top">
 <div class="bar">
  <a class="brand" href="index.html" aria-label="Zur Startseite"><span class="sym" aria-hidden="true">§</span> Ausbildungsvertrag</a>
  <details class="menu"><summary>Menü</summary><nav aria-label="Seiten">
   <a href="index.html"{cur if home else ""}>Start</a>{nav}</nav></details>
 </div>
</header>
<main id="inhalt" tabindex="-1">
{body}
</main>
<footer class="foot"><p>{FOOT}</p></footer>
<script src="js/data.js"></script>
<script src="js/app.js"></script>
</body>
</html>
"""

tiles = "".join(f'<li><a class="tile" href="{f}" data-tile="{k}"><span class="tt">{esc(t)}</span><span class="td">{esc(d)}</span><span class="ts" aria-live="polite"></span></a></li>' for f, k, t, d in PAGES)
home_body = f"""<section class="hero">
<h1>{esc(TITLE)}</h1>
<p class="lead">Übt den Ausbildungsvertrag in 15 Minuten, ohne Anmeldung.</p>
</section>
<ul class="tiles">{tiles}</ul>
<p class="note" id="datenhinweis"><strong>Es werden keine Daten gespeichert oder gesendet.</strong> Nur dein Fortschritt bleibt lokal auf deinem Gerät. Mit „Zurücksetzen“ löschst du ihn.</p>
<p><button class="btn ghost" id="reset" type="button">Zurücksetzen</button></p>"""
open(os.path.join(SITE, "index.html"), "w", encoding="utf-8").write(page("index.html", "home", TITLE, home_body))

bodies = {
 "rg": '<h1>Rote/Grüne Karte</h1><p class="lead">Stimmt die Aussage oder stimmt sie nicht?</p><div id="app" aria-live="off"></div>',
 "det": '<h1>Vertrags-Detektiv</h1><p class="lead">Im Vertragsauszug stecken 5 Fehler. Tippe bis zu 5 Zeilen an, die du für fehlerhaft hältst, und tippe dann auf „Prüfen“.</p><div id="app"></div>',
 "faelle": '<h1>IHK-Fälle</h1><p class="lead">Wähle A bis D. Danach siehst du die Lösung mit Begründung.</p><div id="app"></div>',
 "quiz": '<h1>Mini-Quiz</h1><p class="lead">Fünf Fragen zum Abschluss.</p><div id="app"></div>',
 "experten": '<h1>Experten-Karten</h1><p class="lead">Vier Themen. Lies die Kernpunkte und beantworte die Frage an die Klasse. Die Lösung deckst du per Tippen auf.</p><div id="app"></div>',
 "merk": '<h1>Merkblatt: Das Wichtigste auf einer Seite</h1><p class="noprint"><button class="btn" id="print" type="button">Drucken</button></p><div id="app"></div>',
 "quellen": '<h1>Quellenverzeichnis</h1><p class="lead">Rechtsstand: Oktober 2026</p><div id="app"></div>',
}
for f, k, t, d in PAGES:
    open(os.path.join(SITE, f), "w", encoding="utf-8").write(page(f, k, t, bodies[k] + '<noscript><p class="note">Diese Seite braucht JavaScript. Bei Problemen helfen die Folien im Unterricht.</p></noscript>'))
open(os.path.join(SITE, "js", "data.js"), "w", encoding="utf-8").write(build_data())
print("Seiten:", len(PAGES) + 1)
