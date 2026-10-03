# Übungsseite: Rechte und Pflichten aus dem Ausbildungsvertrag

Kleine Website für die Unterrichtsstunde (Fach GP, Yasin & Mido). Die Klasse öffnet sie per QR-Code auf dem Handy und übt dort:
Rote/Grüne Karte, Vertrags-Detektiv, IHK-Fälle, Mini-Quiz, Experten-Karten, Merkblatt (mit Druckansicht) und Quellen.

- Reines HTML, CSS und JavaScript. Kein Server, kein Build-Schritt, keine externen Anfragen (keine CDN, keine Web-Fonts, keine Tracker).
- Keine Anmeldung, keine Cookies. Es werden keine Namen oder Ergebnisse gesendet. Der Fortschritt bleibt nur lokal im Browser (localStorage) und lässt sich auf der Startseite mit „Zurücksetzen“ löschen.
- Alle Pfade sind relativ. Die Seite läuft deshalb auch unter einem Unterpfad (zum Beispiel `https://name.github.io/azubi-vertrag/`).
- Gesamtgröße ca. 50 KB.

## Erwartete Adresse und QR-Code

Der QR-Code in Präsentation, Booklet und Merkblatt zeigt auf **https://yasinbenx.github.io/azubi-vertrag/**.
Lege das Repository deshalb genau mit dem Namen `azubi-vertrag` an (Konto `yasinbenx`). Weicht die Adresse ab, muss der QR-Code neu erzeugt werden.

## Ordner

| Datei | Inhalt |
|---|---|
| `index.html` | Startseite mit Kacheln |
| `rote-gruene-karte.html`, `vertrags-detektiv.html`, `ihk-faelle.html`, `mini-quiz.html`, `experten-karten.html`, `merkblatt.html`, `quellen.html` | die Seiten |
| `css/style.css` | Gestaltung (Navy und gelb-oranger Akzent, Systemschriften, Druckstil fürs Merkblatt) |
| `js/data.js` | alle Inhalte (Aussagen, Vertragsauszug, Fälle, Quiz, Experten-Karten, Merkblatt, Quellen) |
| `js/app.js` | Programmlogik |

Inhalte ändern: Texte stehen in `js/data.js`. Wichtig: Dieselben Texte stehen auch in Booklet und Präsentation. Ändert sie überall gleich.

## Lokal testen

```
cd site
python3 -m http.server 8000
```

Dann `http://localhost:8000` im Browser öffnen. Die Dateien lassen sich auch direkt per Doppelklick auf `index.html` öffnen.

## Veröffentlichen (kostenlos)

Es werden keine Zugangsdaten im Projekt gespeichert. Du meldest dich nur auf der Website des Anbieters an. Die Bezeichnungen der Menüs können dort leicht abweichen.

### Variante A: GitHub Pages (empfohlen, mit GitHub-Konto)

Das kostenlose GitHub Pages braucht ein **öffentliches** Repository. Lege deshalb ein **neues** Repository nur für diese Seite an, damit andere Projektdateien nicht öffentlich werden.

1. Auf github.com einloggen. Oben rechts **+ → New repository**.
2. Name eingeben, zum Beispiel `azubi-vertrag` (kurz, Kleinbuchstaben, ohne Sonderzeichen). Sichtbarkeit **Public**. **Create repository**.
3. Auf der Repository-Seite **uploading an existing file** wählen und **den Inhalt** des Ordners `site/` hineinziehen (also `index.html`, die anderen `.html`-Dateien, `css/`, `js/` und `README.md`, nicht den Ordner `site` selbst). Unten **Commit changes**.
4. **Settings → Pages**. Bei **Build and deployment** als Source **Deploy from a branch** wählen, Branch `main`, Ordner `/ (root)`, **Save**.
5. Nach ein bis zwei Minuten steht oben auf der Pages-Einstellung die Adresse: `https://DEIN-BENUTZERNAME.github.io/azubi-vertrag/`. Diese Adresse ist die endgültige URL für den QR-Code.

Hinweis: Bei GitHub Pages steht dein GitHub-Benutzername in der Adresse.

### Variante B: Netlify (ohne Git, per Ziehen und Ablegen)

1. Auf netlify.com ein kostenloses Konto anlegen.
2. **Add new site → Deploy manually** und den Ordner `site/` ins Feld ziehen.
3. Unter **Site configuration → Change site name** einen kurzen Namen wie `azubi-vertrag` wählen. Die Adresse lautet dann `https://azubi-vertrag.netlify.app` (falls der Name frei ist).

### Variante C: Cloudflare Pages

1. Auf cloudflare.com ein kostenloses Konto anlegen.
2. **Workers & Pages → Create → Pages → Upload assets**, Projektnamen wählen (zum Beispiel `azubi-vertrag`), den Ordner `site/` hochladen, **Deploy**.
3. Die Adresse lautet `https://azubi-vertrag.pages.dev` (falls der Name frei ist).

## Erneut veröffentlichen (nach Änderungen)

- **GitHub Pages:** Im Repository die geänderte Datei öffnen (zum Beispiel `js/data.js`), Stift-Symbol **Edit**, ändern, **Commit changes**. Oder **Add file → Upload files** und die neue Datei hochladen, die alte wird ersetzt. Nach ein bis zwei Minuten ist die neue Version online. Die Adresse bleibt gleich.
- **Netlify:** Im Projekt **Deploys** öffnen und den aktualisierten Ordner `site/` erneut in das Feld **Drag and drop** ziehen.
- **Cloudflare Pages:** Im Projekt **Create deployment** wählen und den Ordner erneut hochladen.

Nach jeder Änderung die Seite auf dem Handy öffnen und die Aktivitäten einmal durchklicken. Wenn die Adresse gleich bleibt, muss der QR-Code nicht neu erstellt werden.

## Datenschutz

Es gibt keinen Server und keine Datenübertragung. Beim Öffnen der Seite lädt der Browser nur die Dateien dieser Seite. Die Links auf der Seite „Quellen“ führen auf externe Webseiten und werden nur beim Antippen geöffnet.
