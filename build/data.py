# -*- coding: utf-8 -*-
"""Gemeinsame Inhaltsbasis. Alle Fakten stammen ausschliesslich aus dem Skript."""

NAVY = "#14264B"
ACCENT = "#F5A800"

# ---------------------------------------------------------------- Station 1
WISSENS_CHECK = [
    dict(q="Wie lang darf die Probezeit höchstens sein?",
         a=["2 Monate", "3 Monate", "4 Monate", "6 Monate"], c=2,
         fb="§ 20 BBiG: ein bis vier Monate"),
    dict(q="Wie hoch ist die Mindestausbildungsvergütung im 1. Ausbildungsjahr bei Ausbildungsbeginn 2026?",
         a=["650 €", "724 €", "854 €", "1.014 €"], c=1, fb="§ 17 BBiG"),
    dict(q="Ein Azubi kündigt während der Probezeit. Welche Frist gilt?",
         a=["4 Wochen", "2 Wochen", "keine Frist", "Monatsende"], c=2,
         fb="§ 22 Abs. 1 BBiG"),
]

# ---------------------------------------------------------------- Station 2
# (Nr, Situation, Buchstabe der Regelung laut Booklet-Aufgabe 1)
PAARE = [
    (1, "Eine volljährige Auszubildende will wissen, wie viele Werktage Urlaub ihr mindestens zustehen.", "E"),
    (2, "Ein Azubi ist zu Jahresbeginn 16 Jahre alt und fragt nach seinem Mindesturlaub.", "C"),
    (3, "Eine Auszubildende will in der Probezeit kündigen.", "G"),
    (4, "Ein Azubi will nach der Probezeit den Beruf wechseln.", "B"),
    (5, "Ein Betrieb will nach der Probezeit wegen einer schweren Pflichtverletzung kündigen.", "H"),
    (6, "Ein nicht tarifgebundener Betrieb bietet im 1. Jahr (Beginn 2026) 600 € an.", "A"),
    (7, "Eine Auszubildende erzählt in sozialen Netzwerken interne Geschäftszahlen.", "F"),
    (8, "Es ist der Arbeitstag vor der schriftlichen Abschlussprüfung.", "D"),
]
REGELUNGEN = {  # Buchstabe -> Regelung (Reihenfolge A..H wie im Booklet)
    "A": "Unzulässig: mindestens 724 € (§ 17 BBiG)",
    "B": "Kündigung mit vier Wochen Frist, schriftlich und mit Gründen (§ 22 Abs. 2 und 3 BBiG)",
    "C": "Mindestens 27 Werktage (§ 19 JArbSchG)",
    "D": "Der Betrieb muss den Azubi freistellen (§ 15 BBiG)",
    "E": "Mindestens 24 Werktage (§ 3 BUrlG)",
    "F": "Verstoß gegen die Pflicht zur Verschwiegenheit (§ 13 BBiG)",
    "G": "Jederzeit ohne Frist, aber schriftlich (§ 22 Abs. 1 und 3 BBiG)",
    "H": "Nur fristlos aus wichtigem Grund, schriftlich mit Gründen, innerhalb von zwei Wochen nach Kenntnis (§ 22 Abs. 2 bis 4 BBiG)",
}
LOESUNGSSCHLUESSEL = "1 → E · 2 → C · 3 → G · 4 → B · 5 → H · 6 → A · 7 → F · 8 → D"

# ---------------------------------------------------------------- Station 3
MILLIONAER = [
    dict(stufe="50 €", q="Wie viele Monate dauert die Probezeit mindestens?",
         a=["1", "2", "3", "4"], c=0, fb="§ 20 BBiG"),
    dict(stufe="100 €", q="Wer fasst den wesentlichen Inhalt des Ausbildungsvertrags in Textform ab?",
         a=["Berufsschule", "IHK", "Ausbildende", "Azubi"], c=2, fb="§ 11 BBiG"),
    dict(stufe="200 €", q="Welche Pflicht hat der Ausbildende?",
         a=["Ausbildungsmittel kostenlos stellen", "Ausbildungsnachweis führen",
            "Weisungen befolgen", "Betriebsgeheimnisse wahren"], c=0,
         fb="§ 14 BBiG; B bis D sind Pflichten des Azubis (§ 13 BBiG)"),
    dict(stufe="500 €", q="Wie viele Werktage Mindesturlaub hat ein volljähriger Azubi?",
         a=["20", "24", "25", "30"], c=1,
         fb="§ 3 BUrlG (20 Arbeitstage bei Fünf-Tage-Woche)"),
    dict(stufe="1.000 €", q="Welche Kündigungsfrist hat der Azubi nach der Probezeit bei Berufswechsel?",
         a=["keine", "2 Wochen", "4 Wochen", "3 Monate"], c=2, fb="§ 22 Abs. 2 BBiG"),
    dict(stufe="5.000 €", q="Wie hoch ist die Mindestausbildungsvergütung im 3. Ausbildungsjahr (Beginn 2026)?",
         a=["724 €", "854 €", "977 €", "1.014 €"], c=2, fb="§ 17 BBiG"),
    dict(stufe="1 Million €", q="Eine Kündigung aus wichtigem Grund nach der Probezeit ist unwirksam, wenn …",
         a=["die Gründe länger als zwei Wochen bekannt sind", "der Azubi nicht zustimmt",
            "sie nicht zum Monatsende wirkt", "kein Zeuge dabei war"], c=0,
         fb="§ 22 Abs. 4 BBiG"),
]

# ---------------------------------------------------------------- Station 4
FAELLE = [
    dict(id="A", titel="Probezeit und Kündigung", reserve=False,
         q="Lena Berg beginnt am 01.09. bei der Muster GmbH eine Ausbildung zur Kauffrau für Büromanagement, vereinbart sind drei Monate Probezeit. Am 10.10. merkt sie, dass der Beruf nicht zu ihr passt. Welche Aussage ist richtig?",
         a=["Lena muss eine Kündigungsfrist von vier Wochen einhalten.",
            "Lena kann schriftlich und ohne Einhaltung einer Frist kündigen.",
            "Lena kann nur zum Monatsende kündigen.",
            "Lena braucht für die Kündigung die Zustimmung der IHK."],
         c=1, loesung="In der Probezeit ist die Kündigung jederzeit ohne Frist möglich, aber schriftlich (§ 22 Abs. 1 und 3 BBiG).",
         para="§ 22 Abs. 1 und 3 BBiG",
         begr="In der Probezeit jederzeit ohne Frist, aber schriftlich."),
    dict(id="B", titel="Urlaub", reserve=False,
         q="Tim Roth ist zu Beginn des Kalenderjahres 17 Jahre alt und arbeitet an fünf Tagen pro Woche. Wie viele Werktage Mindesturlaub stehen ihm nach dem Gesetz zu?",
         a=["20 Werktage", "24 Werktage", "25 Werktage", "30 Werktage"],
         c=2, loesung="Jugendliche unter 18 Jahren haben mindestens 25 Werktage (§ 19 JArbSchG), das entspricht 21 Arbeitstagen bei der Fünf-Tage-Woche.",
         para="§ 19 JArbSchG",
         begr="Jugendliche unter 18 Jahren haben mindestens 25 Werktage, das sind 21 Arbeitstage bei der Fünf-Tage-Woche."),
    dict(id="C", titel="Vergütung", reserve=False,
         q="Die Muster GmbH ist nicht tarifgebunden und bietet Jonas für den Ausbildungsbeginn 2026 im ersten Jahr 690 € brutto an. Welche Aussage ist richtig?",
         a=["Zulässig, wenn Jonas zustimmt.",
            "Zulässig, weil die Vergütung frei vereinbart werden darf.",
            "Unzulässig, im ersten Ausbildungsjahr gelten 2026 mindestens 724 €.",
            "Unzulässig, erst ab dem zweiten Jahr gilt eine Mindestvergütung."],
         c=2, loesung="Die Mindestausbildungsvergütung nach § 17 BBiG darf nicht unterschritten werden.",
         para="§ 17 BBiG",
         begr="Die Mindestausbildungsvergütung darf nicht unterschritten werden, im 1. Jahr 2026 sind es 724 €."),
    dict(id="D", titel="tägliche Ausbildungszeit", reserve=True,
         q="Nina Koch ist 17 Jahre alt und Auszubildende. Wegen Personalmangel soll sie täglich 9 Stunden arbeiten. Welche Aussage ist richtig?",
         a=["Zulässig, wenn die Mehrarbeit vergütet wird.",
            "Unzulässig, für Jugendliche gelten höchstens 8 Stunden täglich und 40 Stunden wöchentlich.",
            "Zulässig, bis zu 10 Stunden wie bei Erwachsenen.",
            "Zulässig, wenn die Eltern zustimmen."],
         c=1, loesung="§ 8 JArbSchG; ausnahmsweise sind 8,5 Stunden täglich erlaubt, wenn an anderen Tagen derselben Woche entsprechend weniger gearbeitet wird.",
         para="§ 8 JArbSchG",
         begr="Jugendliche höchstens 8 Stunden täglich und 40 pro Woche, ausnahmsweise 8,5 Stunden täglich bei Ausgleich in derselben Woche."),
    dict(id="E", titel="Beginn und Dauer", reserve=True,
         q="Ben beginnt nach dem Abitur eine dreijährige Ausbildung und möchte sie verkürzen. Welche Aussage ist richtig?",
         a=["Ben beantragt die Verkürzung allein bei der Berufsschule.",
            "Ben und der Betrieb beantragen die Verkürzung gemeinsam bei der zuständigen Stelle.",
            "Die Ausbildung verkürzt sich wegen des Abiturs automatisch.",
            "Nur der Betrieb darf die Verkürzung bei der IHK beantragen."],
         c=1, loesung="§ 8 Abs. 1 BBiG; mit Abitur sind laut IHK bis zu zwölf Monate Verkürzung möglich.",
         para="§ 8 Abs. 1 BBiG",
         begr="Verkürzung auf gemeinsamen Antrag von Azubi und Betrieb bei der zuständigen Stelle."),
]

# ---------------------------------------------------------------- Station 5
ABSCHLUSS = [
    dict(q="Eine Auszubildende ist zu Jahresbeginn 15 Jahre alt. Wie viele Werktage Mindesturlaub hat sie?",
         a=["24", "25", "27", "30"], c=3, fb="§ 19 JArbSchG (unter 16 Jahren)"),
    dict(q="Ein Betrieb will eine Probezeit von sechs Monaten festlegen. Ist das zulässig?",
         a=["Ja, wenn der Azubi zustimmt", "Ja, in großen Betrieben",
            "Nein, höchstens vier Monate", "Nein, höchstens drei Monate"], c=2, fb="§ 20 BBiG"),
    dict(q="Ein Azubi kündigt nach der Probezeit mündlich, weil er den Beruf wechseln will. Ist das wirksam?",
         a=["Ja, mit vier Wochen Frist", "Ja, ohne Frist",
            "Nein, die Kündigung muss schriftlich mit Angabe der Gründe erfolgen",
            "Nein, nur die IHK darf kündigen"], c=2, fb="§ 22 Abs. 2 und 3 BBiG"),
    dict(q="Ein nicht tarifgebundener Betrieb zahlt im 2. Ausbildungsjahr (Beginn 2026) 800 €. Ist das zulässig?",
         a=["Ja, weil es mehr als im 1. Jahr ist", "Ja, wenn der Betrieb nicht tarifgebunden ist",
            "Nein, im 2. Jahr gelten mindestens 854 €", "Nein, im 2. Jahr gelten mindestens 977 €"],
         c=2, fb="§ 17 BBiG"),
    dict(q="Ein volljähriger Azubi soll an einem Tag 10 Stunden arbeiten; im Durchschnitt von sechs Monaten bleibt es bei 8 Stunden. Ist das zulässig?",
         a=["Nein, höchstens 8 Stunden",
            "Ja, nach dem Arbeitszeitgesetz, wenn der Durchschnitt von 8 Stunden nicht überschritten wird",
            "Nein, nur mit Zustimmung der IHK", "Ja, dann sind sogar 12 Stunden erlaubt"],
         c=1, fb="§ 3 ArbZG"),
]

# ---------------------------------------------------------------- Selbsttest (Booklet S. 20)
SELBSTTEST = [
    ("Eine Auszubildende fragt, wie lang die Probezeit höchstens sein darf.",
     "mindestens ein, höchstens vier Monate (§ 20 BBiG)."),
    ("Ein Azubi will in der Probezeit kündigen.",
     "jederzeit ohne Kündigungsfrist, aber schriftlich (§ 22 Abs. 1 und 3 BBiG)."),
    ("Eine Auszubildende will nach der Probezeit die Ausbildung aufgeben.",
     "Kündigung mit vier Wochen Frist, schriftlich und mit Angabe der Gründe (§ 22 Abs. 2 und 3 BBiG)."),
    ("Ein nicht tarifgebundener Betrieb zahlt im ersten Ausbildungsjahr (Beginn 2026) 650 € brutto.",
     "nicht zulässig, die Mindestausbildungsvergütung beträgt 724 € (§ 17 BBiG)."),
    ("Mara ist zu Jahresbeginn 16 Jahre alt. Wie viele Werktage Urlaub stehen ihr mindestens zu?",
     "27 Werktage (§ 19 JArbSchG)."),
]

# ---------------------------------------------------------------- Merkblatt
MERKBLATT = [
    ("Vertrag", "Wesentlicher Inhalt in Textform (seit 01.08.2024), unter anderem Beginn, Dauer, tägliche Ausbildungszeit, Probezeit, Vergütung, Urlaub, Kündigung", "§ 11 BBiG"),
    ("Dauer", "Verkürzung auf gemeinsamen Antrag; Ende mit Bekanntgabe des Prüfungsergebnisses; Verlängerung nach Nichtbestehen höchstens um ein Jahr", "§ 8, § 21 BBiG"),
    ("Ausbildungszeit", "Jugendliche höchstens 8 Stunden täglich und 40 pro Woche; Volljährige 8 Stunden, bis 10 mit Ausgleich in sechs Monaten", "§ 8 JArbSchG, § 3 ArbZG"),
    ("Vergütung", "Mindestens 724 / 854 / 977 / 1.014 € (1.–4. Jahr, Beginn 2026)", "§ 17 BBiG"),
    ("Urlaub", "Zu Jahresbeginn unter 16: 30, unter 17: 27, unter 18: 25, ab 18: 24 Werktage", "§ 19 JArbSchG, § 3 BUrlG"),
    ("Probezeit", "Ein bis vier Monate; Kündigung jederzeit ohne Frist, schriftlich", "§ 20, § 22 Abs. 1 BBiG"),
    ("Kündigung nach der Probezeit", "Fristlos aus wichtigem Grund (innerhalb von zwei Wochen nach Kenntnis) oder durch den Azubi mit vier Wochen Frist bei Berufswechsel; immer schriftlich, mit Gründen", "§ 22 Abs. 2 bis 4 BBiG"),
    ("Pflichten des Azubis", "Lernen, sorgfältig arbeiten, Weisungen befolgen, Ordnung beachten, Geheimnisse wahren, Ausbildungsnachweis führen", "§ 13 BBiG"),
    ("Pflichten der Ausbildenden", "Ausbildungsziel vermitteln, Ausbildungsmittel kostenlos stellen, freistellen, Zeugnis ausstellen, Vergütung zahlen", "§§ 14 bis 17 BBiG"),
]

# ---------------------------------------------------------------- Glossar
GLOSSAR = [
    ("Ausbildende", "wer andere zur Berufsausbildung einstellt, meist der Betrieb; Vertragspartner des Azubis."),
    ("Auszubildende (Azubi)", "Person, die im Betrieb und in der Berufsschule ausgebildet wird."),
    ("Probezeit", "Beginn jeder Ausbildung, ein bis vier Monate (§ 20 BBiG)."),
    ("Werktag", "jeder Kalendertag außer Sonntagen und gesetzlichen Feiertagen, also auch der Samstag."),
    ("Mindestausbildungsvergütung", "gesetzliche Untergrenze der Vergütung nach § 17 BBiG, die jedes Jahr angepasst wird."),
    ("Kündigung aus wichtigem Grund", "fristlose Kündigung nach der Probezeit; sie ist unwirksam, wenn die Gründe länger als zwei Wochen bekannt sind (§ 22 Abs. 4 BBiG)."),
    ("Textform", "lesbare Erklärung auf einem dauerhaften Datenträger, zum Beispiel per E-Mail (§ 126b BGB)."),
]

# ---------------------------------------------------------------- Quellen (Links aus dem Skript)
QUELLEN = [
    ("BIBB – Mindestausbildungsvergütung 2026", "https://www.bibb.de/de/199658.php"),
    ("BBiG §§ 20–22 – Probezeit und Kündigung", "https://www.buzer.de/gesetz/3118/b8613.htm"),
    ("IHK – Urlaubsanspruch von Auszubildenden", "https://www.ihk.de/bayreuth/hauptnavigation/service/ausbildung/rechtliches/bundesurlaubsgesetz-4447896"),
    ("BBiG § 11 – Vertragsabfassung, Änderung vom 01.08.2024", "https://www.buzer.de/gesetz/3118/al198348-0.htm"),
    ("IHK München – Verkürzung und Verlängerung der Ausbildung", "https://www.ihk-muenchen.de/ausbildung-fortbildung/ausbilden/ausbildungsverhaeltnis/verkuerzung-verlaengerung/"),
    ("BBiG §§ 13 bis 17 – Pflichten", "https://www.buzer.de/gesetz/3118/b8608.htm"),
    ("IHK Erfurt – Höchstzulässige Ausbildungszeit", "https://www.ihk.de/erfurt/bildung/ausbildungswiki/hoechstzulaessige-ausbildungszeit-4659100"),
    ("Büromanagement-Prüfungsverordnung – Wirtschafts- und Sozialkunde", "https://www.ihk.de/blueprint/servlet/resource/blob/4211038/080ed6789f3f23ed03a7002946d78600/vo-bueromanagement-aenderung-data.pdf"),
]
VERORDNUNG_URL = QUELLEN[-1][1]
IHK_INFO_URL = "https://www.ihk.de/blueprint/servlet/resource/blob/2727156/6f6f7c34adafa8f28d61d7d53fbcfca6/informationen-zur-abschlusspruefung-bueromanagement-bf-data.pdf"

URLAUB = [
    ("Unter 16 Jahre (Jahresbeginn)", "mind. 30 Werktage"),
    ("Unter 17 Jahre (Jahresbeginn)", "mind. 27 Werktage"),
    ("Unter 18 Jahre (Jahresbeginn)", "mind. 25 Werktage"),
    ("Volljährig", "mind. 24 Werktage"),
]
VERGUETUNG = [("1. Jahr", 724), ("2. Jahr", 854), ("3. Jahr", 977), ("4. Jahr", 1014)]
