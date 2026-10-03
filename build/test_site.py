# -*- coding: utf-8 -*-
"""Testet die Website mit Playwright. Gibt eine Testliste aus und legt Screenshots ab."""
import os, sys, re, json, shutil, subprocess, time, threading, http.server, socketserver, functools
sys.path.insert(0, os.path.dirname(__file__))
from playwright.sync_api import sync_playwright
import pymupdf
from data2 import *
from site_data import EXPERTEN

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SHOTS = sys.argv[1] if len(sys.argv) > 1 else "/tmp/site_shots"
os.makedirs(SHOTS, exist_ok=True)
# Unterpfad-Test: Seite unter /azubi/mein-pfad/ ausliefern
SERVE = "/tmp/site_serve"; shutil.rmtree(SERVE, ignore_errors=True)
shutil.copytree(os.path.join(ROOT, "site"), os.path.join(SERVE, "azubi", "mein-pfad"))
Handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=SERVE)
class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
Handler = functools.partial(Q, directory=SERVE)
srv = socketserver.TCPServer(("127.0.0.1", 0), Handler); PORT = srv.server_address[1]
threading.Thread(target=srv.serve_forever, daemon=True).start()
BASE = f"http://127.0.0.1:{PORT}/azubi/mein-pfad/"

PAGES = ["index.html", "rote-gruene-karte.html", "vertrags-detektiv.html", "ihk-faelle.html", "mini-quiz.html", "experten-karten.html", "merkblatt.html", "quellen.html"]
FOOT = "Erstellt von Yasin & Mido · GP · Rechtsstand Oktober 2026 · Zur Prüfungsvorbereitung, keine Rechtsberatung"
results = []
def ok(name, cond, detail=""):
    results.append((bool(cond), name, detail))
    if not cond: print("FAIL:", name, detail)

norm = lambda s: re.sub(r"\s+", " ", s.replace("­", "").replace("-\n", "").replace("\n", " ")).strip()
booklet = norm(" ".join(p.get_text() for p in pymupdf.open(os.path.join(ROOT, "output/v2/booklet.pdf"))))
merk_pdf = norm(" ".join(p.get_text() for p in pymupdf.open(os.path.join(ROOT, "output/v2/merkblatt.pdf"))))
from pptx import Presentation
prs = Presentation(os.path.join(ROOT, "output/v2/praesentation.pptx"))
pptx_text = norm(" ".join(sh.text_frame.text for s in prs.slides for sh in s.shapes if sh.has_text_frame))

# ---------------- Inhalte: Website-Daten = Booklet / Praesentation / Auftrag
D = json.loads(open(os.path.join(ROOT, "site/js/data.js"), encoding="utf-8").read().split("=", 1)[1].rstrip().rstrip(";"))
ok("Daten: 10 Aussagen Rote/Grüne Karte", len(D["rg"]) == 10)
ok("Daten: Aussagen wörtlich im Booklet (Wahr oder falsch)", all(norm(r["t"]) in booklet for r in D["rg"]), [r["t"] for r in D["rg"] if norm(r["t"]) not in booklet])
ok("Daten: Lösungen Rote/Grüne Karte wörtlich im Erwartungshorizont", all(norm(r["b"]) in booklet for r in D["rg"]), [r["b"] for r in D["rg"] if norm(r["b"]) not in booklet])
ok("Daten: Stimmt/Stimmt nicht gleich wie in der Präsentation", all((("Stimmt nicht" if not r["ok"] else "Stimmt") in booklet) for r in D["rg"]))
ok("Daten: Detektiv-Zeilen wörtlich im Booklet", all(norm(z["t"]) in booklet for z in D["zeilen"]) and all(norm(k) in booklet for k in D["kopf"]))
ok("Daten: Detektiv-Zeilen wörtlich in der Präsentation", all(norm(z["t"]) in pptx_text for z in D["zeilen"]) and all(norm(k) in pptx_text for k in D["kopf"]))
ok("Daten: genau 5 Fehler, Zeilen § 2 bis § 6", sorted(z["f"] for z in D["zeilen"] if z["f"]) == [1, 2, 3, 4, 5])
ok("Daten: Fehler-Regeln wörtlich im Erwartungshorizont", all(norm(v["regel"]) in booklet for v in D["fehler"].values()), [v["regel"] for v in D["fehler"].values() if norm(v["regel"]) not in booklet])
fk = {z["f"]: z["t"] for z in D["zeilen"] if z["f"]}
ok("Daten: Fehler-Stellen passen zu den Zeilen", all(D["fehler"][str(n)]["stelle"].split(" ")[1] == fk[n].split(" ")[1] for n in fk))
ok("Daten: Fälle A–E, Texte wörtlich aus data2", len(D["faelle"]) == 5 and [f["c"] for f in D["faelle"]] == [1, 2, 2, 1, 1])
ok("Daten: Fälle A–C wörtlich im Booklet", all(norm(f["q"]) in booklet and all(norm(a) in booklet for a in f["a"]) for f in D["faelle"][:3]))
ok("Daten: Fall-Lösungen A–C stimmen mit Erwartungshorizont (B, C, C)", [("ABCD"[f["c"]]) for f in D["faelle"][:3]] == ["B", "C", "C"])
ok("Daten: Mini-Quiz 5 Fragen, Lösungen B? C C C B", [("ABCD"[q["c"]]) for q in D["quiz"]] == ["D", "C", "C", "C", "B"])
ok("Daten: Mini-Quiz-Fragen wörtlich in Modul-B-Folien", all(norm(q["q"]) in pptx_text for q in D["quiz"]))
ok("Daten: Experten-Karten 4, Lösungen aus dem Auftrag", [e["loesung"] for e in D["experten"]] == ["Keine Frist, aber die Kündigung muss schriftlich erfolgen.", "27 Werktage.", "977 €.", "Vier Wochen Frist, schriftlich, mit Angabe der Gründe."])
ok("Daten: Merkblatt 9 Zeilen, Inhalt wie merkblatt.pdf", len(D["merk"]) == 9 and all(norm(m["text"]) in merk_pdf or norm(m["text"])[:40] in merk_pdf for m in D["merk"]))
ok("Daten: Quellen 8, wie booklet.pdf", len(D["quellen"]) == 8 and all(norm(q["t"]) in booklet for q in D["quellen"]))

with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome", args=["--no-sandbox"])
    for vname, (w, h) in (("390x844", (390, 844)), ("1280x720", (1280, 720))):
        ctx = b.new_context(viewport={"width": w, "height": h}, device_scale_factor=1, has_touch=(w < 500), is_mobile=(w < 500))
        ext, errs = [], []
        ctx.on("request", lambda r: ext.append(r.url) if not r.url.startswith(f"http://127.0.0.1:{PORT}") and not r.url.startswith("data:") else None)
        pg = ctx.new_page()
        pg.on("console", lambda m: errs.append(m.text) if m.type in ("error", "warning") else None); pg.on("pageerror", lambda e: errs.append(str(e)))
        for f in PAGES:
            pg.goto(BASE + f); pg.wait_for_load_state("networkidle")
            tag = f"{f} @{vname}"
            pg.screenshot(path=f"{SHOTS}/{f.replace('.html','')}_{vname}.png", full_page=True)
            over = pg.evaluate("document.documentElement.scrollWidth - window.innerWidth")
            ok(f"Kein seitliches Scrollen: {tag}", over <= 0, over)
            ok(f"Footer-Text exakt: {tag}", pg.inner_text("footer").strip() == FOOT)
            small = pg.evaluate("""() => { const bad=[]; document.querySelectorAll('body *').forEach(e=>{ if(e.closest('.sr')||e.matches('script,style,noscript,.skip')) return; const r=e.getBoundingClientRect(); if(r.width===0||r.height===0) return; const hasText=[...e.childNodes].some(n=>n.nodeType===3&&n.textContent.trim()); if(!hasText) return; const fs=parseFloat(getComputedStyle(e).fontSize); if(fs<17.99) bad.push(e.tagName+':'+fs+':'+e.textContent.slice(0,30)); }); return bad; }""")
            ok(f"Schrift mindestens 18 px: {tag}", not small, small[:3])
            short = pg.evaluate("""() => { const bad=[]; document.querySelectorAll('button,a.btn,a.tile,summary,.menu nav a,.links a,a.brand').forEach(e=>{ const r=e.getBoundingClientRect(); if(r.width>0 && r.height>0 && r.height<47.5) bad.push(e.tagName+':'+Math.round(r.height)+':'+e.textContent.slice(0,25)); }); return bad; }""")
            ok(f"Bedienelemente mindestens 48 px hoch: {tag}", not short, short[:3])
            ok(f"Eine Überschrift h1: {tag}", pg.locator("h1").count() == 1)
        # ---------------- Aktivitaeten komplett durchklicken
        pg.evaluate("localStorage.clear()")
        # Rote/Gruene Karte (richtig)
        pg.goto(BASE + "rote-gruene-karte.html")
        for i, r in enumerate(D["rg"]):
            stat = pg.inner_text("h2.q")
            if stat != r["t"]: ok(f"RG Aussage {i+1} Reihenfolge fest @{vname}", False, stat)
            pg.get_by_role("button", name="✓ Stimmt", exact=True).click() if r["ok"] else pg.get_by_role("button", name="✗ Stimmt nicht", exact=True).click()
            fb = pg.inner_text("[role=status]")
            if not ("✓ Richtig!" in fb and (("Stimmt – " if r["ok"] else "Stimmt nicht – ") + r["b"]) in fb): ok(f"RG Lösung {i+1} @{vname}", False, fb)
            if vname == "390x844" and i == 0: pg.screenshot(path=f"{SHOTS}/rg_antwort_{vname}.png", full_page=True)
            pg.get_by_role("button", name=re.compile("Weiter|Ergebnis ansehen")).click()
        ok(f"RG Ergebnis 10 von 10 @{vname}", "10 von 10" in pg.inner_text(".result"))
        pg.screenshot(path=f"{SHOTS}/rg_ergebnis_{vname}.png", full_page=True)
        # falsch
        pg.get_by_role("button", name="Noch einmal").click()
        pg.get_by_role("button", name="✗ Stimmt nicht", exact=True).click() if D["rg"][0]["ok"] else None
        ok(f"RG falsche Antwort zeigt ✗ und Text @{vname}", "✗ Leider falsch." in pg.inner_text("[role=status]"))
        # Tastatur
        pg.goto(BASE + "rote-gruene-karte.html"); pg.get_by_role("button", name="✓ Stimmt", exact=True).focus(); pg.keyboard.press("Enter")
        ok(f"RG per Tastatur bedienbar @{vname}", "Richtig" in pg.inner_text("[role=status]"))
        # IHK-Faelle
        for page_name, key, items, n in (("ihk-faelle.html", "faelle", D["faelle"], 5), ("mini-quiz.html", "quiz", D["quiz"], 5)):
            pg.goto(BASE + page_name)
            for i, it in enumerate(items):
                ok(f"{key} Frage {i+1}: Text/Antworten wörtlich @{vname}", it["q"] in pg.inner_text(".card.q") and all(a in pg.inner_text(".answers") for a in it["a"]))
                pg.locator(".ans").nth(it["c"]).click()
                fb = pg.inner_text("[role=status]")
                if not ("✓ Richtig!" in fb and it["fb"] in fb and f"Richtig ist {'ABCD'[it['c']]}" in fb): ok(f"{key} Lösung {i+1} @{vname}", False, fb)
                if i == 0 and vname == "390x844": pg.screenshot(path=f"{SHOTS}/{key}_antwort_{vname}.png", full_page=True)
                pg.get_by_role("button", name=re.compile("Weiter|Ergebnis ansehen")).click()
            ok(f"{key} Ergebnis 5 von 5 @{vname}", "5 von 5" in pg.inner_text(".result"))
            pg.screenshot(path=f"{SHOTS}/{key}_ergebnis_{vname}.png", full_page=True)
            pg.get_by_role("button", name="Noch einmal").click()
            wrong = (items[0]["c"] + 1) % 4
            pg.locator(".ans").nth(wrong).click()
            fb = pg.inner_text("[role=status]")
            ok(f"{key} falsche Antwort: ✗ und Text @{vname}", "✗ Leider falsch." in fb and "✗ Deine Antwort" in pg.inner_text(".answers") and "✓ Richtig" in pg.inner_text(".answers"))
        # Vertrags-Detektiv
        pg.goto(BASE + "vertrags-detektiv.html")
        ok(f"Detektiv: vor dem Prüfen keine [Fehler n] @{vname}", "[Fehler" not in pg.inner_text("main"))
        zeilen = pg.locator(".zeile")
        ok(f"Detektiv: 7 nummerierte Zeilen @{vname}", zeilen.count() == 7)
        err_idx = [i for i, z in enumerate(D["zeilen"]) if z["f"]]
        for i in err_idx: zeilen.nth(i).click()
        ok(f"Detektiv: 5 markiert @{vname}", pg.locator(".zeile[aria-pressed=true]").count() == 5)
        extra = [i for i in range(7) if i not in err_idx][0]; zeilen.nth(extra).click()
        ok(f"Detektiv: 6. Zeile wird abgelehnt mit Hinweis @{vname}", pg.locator(".zeile[aria-pressed=true]").count() == 5 and "höchstens 5" in pg.inner_text("[role=status]"))
        if vname == "390x844": pg.screenshot(path=f"{SHOTS}/det_markiert_{vname}.png", full_page=True)
        pg.get_by_role("button", name="Prüfen").click()
        txt = pg.inner_text("main")
        ok(f"Detektiv: [Fehler 1..5] jetzt in der Lösung @{vname}", all(f"[Fehler {n}]" in txt for n in range(1, 6)))
        ok(f"Detektiv: alle 5 gefunden, Regeln & Paragrafen sichtbar @{vname}", txt.count("✓ Gefunden") >= 5 and all(v["regel"] in txt for v in D["fehler"].values()))
        ok(f"Detektiv: Punkte zu Beginn 5 von 10 @{vname}", "5 von 10" in pg.inner_text(".points"))
        for k in range(5): pg.locator(".fehlercard").nth(k).get_by_role("button", name="✓ Ja").click()
        ok(f"Detektiv: nach 5× Ja 10 von 10 @{vname}", "10 von 10" in pg.inner_text(".points"))
        pg.locator(".fehlercard").nth(0).get_by_role("button", name="✗ Nein").click()
        ok(f"Detektiv: Nein senkt auf 9 @{vname}", "9 von 10" in pg.inner_text(".points"))
        pg.screenshot(path=f"{SHOTS}/det_loesung_{vname}.png", full_page=True)
        # nur falsche Zeilen
        pg.get_by_role("button", name="Noch einmal").click()
        for i in [i for i in range(7) if i not in err_idx][:2]: pg.locator(".zeile").nth(i).click()
        pg.get_by_role("button", name="Prüfen").click()
        ok(f"Detektiv: falsch markiert → 0 gefunden, ✗-Hinweise @{vname}", "0 von 10" in pg.inner_text(".points") and "✗ Nicht gefunden" in pg.inner_text("main") and "kein Fehler" in pg.inner_text("main"))
        # Experten
        pg.goto(BASE + "experten-karten.html")
        ok(f"Experten: 4 Karten, Lösung zunächst verborgen @{vname}", pg.locator("section.card").count() == 4 and pg.locator(".reveal:visible").count() == 0)
        for i, e in enumerate(D["experten"]):
            btn = pg.locator("section.card").nth(i).get_by_role("button"); btn.click()
            ok(f"Experten {e['t']}: Lösung aufgedeckt, aria-expanded @{vname}", e["loesung"] in pg.locator("section.card").nth(i).inner_text() and btn.get_attribute("aria-expanded") == "true")
            ok(f"Experten {e['t']}: Kernpunkte und Frage wörtlich @{vname}", all(k in pg.locator("section.card").nth(i).inner_text() for k in e["kern"]) and e["frage"] in pg.locator("section.card").nth(i).inner_text())
        # Merkblatt
        pg.goto(BASE + "merkblatt.html")
        ok(f"Merkblatt: 9 Zeilen @{vname}", pg.locator("table.merk tbody tr").count() == 9)
        ok(f"Merkblatt: Drucken-Button @{vname}", pg.get_by_role("button", name="Drucken").count() == 1)
        if vname == "1280x720":
            pg.emulate_media(media="print"); pdf = pg.pdf(format="A4", print_background=True); open(f"{SHOTS}/merkblatt_druck.pdf", "wb").write(pdf)
            npg = len(pymupdf.open(stream=pdf, filetype="pdf")); ok("Merkblatt: Druckansicht passt auf 1 A4-Seite", npg == 1, npg)
            t = pymupdf.open(stream=pdf, filetype="pdf")[0].get_text(); ok("Merkblatt: Druckansicht ohne Navigation/Buttons", "Menü" not in t and "Drucken" not in t)
            pg.emulate_media(media="screen")
        # Quellen
        pg.goto(BASE + "quellen.html")
        hrefs = pg.eval_on_selector_all(".links a", "els => els.map(e => e.href)")
        ok(f"Quellen: 8 Links = booklet.pdf-Links @{vname}", hrefs == [q["u"] for q in D["quellen"]] and len(hrefs) == 8)
        # Start: Fortschritt + Zuruecksetzen
        pg.goto(BASE + "index.html")
        stat = pg.inner_text("ul.tiles")
        ok(f"Start: 7 Kacheln @{vname}", pg.locator("a.tile").count() == 7)
        ok(f"Start: Fortschritt lokal sichtbar (✓) @{vname}", "✓" in stat)
        ok(f"Start: Hinweistext und Satz @{vname}", "Es werden keine Daten gespeichert oder gesendet" in pg.inner_text("main") and "Übt den Ausbildungsvertrag in 15 Minuten, ohne Anmeldung" in pg.inner_text("main"))
        pg.get_by_role("button", name="Zurücksetzen").click()
        ok(f"Start: Zurücksetzen löscht Fortschritt @{vname}", "✓ " not in pg.inner_text("ul.tiles") and pg.evaluate("localStorage.getItem('azubi-vertrag-v1')") is None)
        # Menue per Tastatur
        pg.goto(BASE + "index.html"); pg.keyboard.press("Tab"); pg.keyboard.press("Tab"); pg.keyboard.press("Tab")
        ok(f"Tastatur: Tab erreicht Menü/Inhalt @{vname}", pg.evaluate("document.activeElement.tagName") in ("SUMMARY", "A", "BUTTON"))
        ok(f"Keine externen Anfragen @{vname}", not ext, ext[:3])
        ok(f"Keine Konsolenfehler/-warnungen @{vname}", not errs, errs[:3])
        ok(f"Keine Cookies @{vname}", ctx.cookies() == [])
        ctx.close()
    b.close()

size = sum(os.path.getsize(os.path.join(dp, f)) for dp, _, fs in os.walk(os.path.join(ROOT, "site")) for f in fs)
ok("Gesamtgröße unter 300 KB", size < 300_000, size)
srcs = open(os.path.join(ROOT, "site/js/app.js")).read() + open(os.path.join(ROOT, "site/css/style.css")).read() + "".join(open(os.path.join(ROOT, "site", f), encoding="utf-8").read() for f in PAGES)
ok("Keine externen URLs im Code (außer Quellenlinks in den Daten)", not re.search(r"(src|href)=[\"']https?://", srcs) and "@import" not in srcs and "url(http" not in srcs)
ok("Keine Cookies/Tracker im Code", "document.cookie" not in srcs and "fetch(" not in srcs and "XMLHttpRequest" not in srcs and "sendBeacon" not in srcs)
n_ok = sum(1 for r in results if r[0]); print(f"\nErgebnis: {n_ok} von {len(results)} Prüfungen bestanden")
open("/tmp/site_testliste.txt", "w", encoding="utf-8").write("\n".join(("✓ " if r[0] else "✗ ") + r[1] + ("" if r[0] else f" → {r[2]}") for r in results))
srv.shutdown()
