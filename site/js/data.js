window.DATA = {
 "rg": [
  {
   "t": "Die Probezeit darf höchstens vier Monate dauern.",
   "ok": true,
   "b": "§ 20 BBiG"
  },
  {
   "t": "Die Probezeit darf sechs Monate dauern, wenn der Azubi zustimmt.",
   "ok": false,
   "b": "höchstens vier Monate (§ 20 BBiG)"
  },
  {
   "t": "In der Probezeit kann der Azubi jederzeit ohne Frist kündigen.",
   "ok": true,
   "b": "§ 22 Abs. 1 BBiG"
  },
  {
   "t": "Nach der Probezeit darf der Azubi mit vier Wochen Frist kündigen, wenn er den Beruf wechseln will.",
   "ok": true,
   "b": "§ 22 Abs. 2 BBiG"
  },
  {
   "t": "Eine Kündigung per E-Mail ist wirksam, wenn sie rechtzeitig ankommt.",
   "ok": false,
   "b": "Sie muss schriftlich erfolgen, die elektronische Form ist ausgeschlossen (§ 22 Abs. 3 BBiG)"
  },
  {
   "t": "Die Mindestausbildungsvergütung im 1. Jahr beträgt bei Beginn 2026 724 €.",
   "ok": true,
   "b": "§ 17 BBiG"
  },
  {
   "t": "Ein volljähriger Azubi hat mindestens 24 Werktage Urlaub.",
   "ok": true,
   "b": "§ 3 BUrlG"
  },
  {
   "t": "Werktage sind nur Montag bis Freitag.",
   "ok": false,
   "b": "Werktage sind alle Kalendertage außer Sonntagen und gesetzlichen Feiertagen"
  },
  {
   "t": "Jugendliche dürfen täglich bis zu 10 Stunden arbeiten.",
   "ok": false,
   "b": "höchstens 8 Stunden täglich und 40 pro Woche (§ 8 JArbSchG)"
  },
  {
   "t": "Der Betrieb muss den Azubi am Arbeitstag vor der schriftlichen Abschlussprüfung freistellen.",
   "ok": true,
   "b": "§ 15 BBiG"
  }
 ],
 "kopf": [
  "Berufsausbildungsvertrag (Auszug, fiktiv)",
  "Ausbildende: Muster GmbH (nicht tarifgebunden)",
  "Auszubildender: Jonas Muster, geboren am 20.11.2009",
  "Beruf: Kaufmann für Büromanagement"
 ],
 "zeilen": [
  {
   "t": "§ 1 Beginn und Dauer: Die Ausbildung beginnt am 01.09.2026 und dauert drei Jahre.",
   "f": null
  },
  {
   "t": "§ 2 Probezeit: Die Probezeit beträgt sechs Monate.",
   "f": 1
  },
  {
   "t": "§ 3 Vergütung: Die monatliche Ausbildungsvergütung beträgt im 1. Ausbildungsjahr 650 € brutto.",
   "f": 2
  },
  {
   "t": "§ 4 Ausbildungszeit: Die tägliche Ausbildungszeit beträgt 9 Stunden.",
   "f": 3
  },
  {
   "t": "§ 5 Urlaub: Der Urlaubsanspruch beträgt 20 Werktage pro Kalenderjahr.",
   "f": 4
  },
  {
   "t": "§ 6 Kündigung: Während der Probezeit kann das Ausbildungsverhältnis nur mit einer Frist von vier Wochen gekündigt werden.",
   "f": 5
  },
  {
   "t": "§ 7 Pflichten: Die Ausbildungsmittel stellt der Betrieb kostenlos zur Verfügung. Der Auszubildende führt einen Ausbildungsnachweis.",
   "f": null
  }
 ],
 "fehler": {
  "1": {
   "stelle": "§ 2 Probezeit",
   "regel": "höchstens vier Monate (§ 20 BBiG)"
  },
  "2": {
   "stelle": "§ 3 Vergütung",
   "regel": "mindestens 724 € im 1. Jahr (§ 17 BBiG)"
  },
  "3": {
   "stelle": "§ 4 Ausbildungszeit",
   "regel": "Jugendliche höchstens 8 Stunden täglich und 40 pro Woche (§ 8 JArbSchG)"
  },
  "4": {
   "stelle": "§ 5 Urlaub",
   "regel": "mindestens 24 Werktage, Jugendliche je nach Alter 25 bis 30 (§ 3 BUrlG, § 19 JArbSchG)"
  },
  "5": {
   "stelle": "§ 6 Kündigung",
   "regel": "in der Probezeit jederzeit ohne Frist, schriftlich (§ 22 Abs. 1 und 3 BBiG)"
  }
 },
 "faelle": [
  {
   "label": "Fall A (Probezeit und Kündigung)",
   "q": "Lena Berg beginnt am 01.09. bei der Muster GmbH eine Ausbildung zur Kauffrau für Büromanagement, vereinbart sind drei Monate Probezeit. Am 10.10. merkt sie, dass der Beruf nicht zu ihr passt. Welche Aussage ist richtig?",
   "a": [
    "Lena muss eine Kündigungsfrist von vier Wochen einhalten.",
    "Lena kann schriftlich und ohne Einhaltung einer Frist kündigen.",
    "Lena kann nur zum Monatsende kündigen.",
    "Lena braucht für die Kündigung die Zustimmung der IHK."
   ],
   "c": 1,
   "fb": "In der Probezeit ist die Kündigung jederzeit ohne Frist möglich, aber schriftlich (§ 22 Abs. 1 und 3 BBiG)."
  },
  {
   "label": "Fall B (Urlaub)",
   "q": "Tim Roth ist zu Beginn des Kalenderjahres 17 Jahre alt und arbeitet an fünf Tagen pro Woche. Wie viele Werktage Mindesturlaub stehen ihm nach dem Gesetz zu?",
   "a": [
    "20 Werktage",
    "24 Werktage",
    "25 Werktage",
    "30 Werktage"
   ],
   "c": 2,
   "fb": "Jugendliche unter 18 Jahren haben mindestens 25 Werktage (§ 19 JArbSchG), das entspricht 21 Arbeitstagen bei der Fünf-Tage-Woche."
  },
  {
   "label": "Fall C (Vergütung)",
   "q": "Die Muster GmbH ist nicht tarifgebunden und bietet Jonas für den Ausbildungsbeginn 2026 im ersten Jahr 690 € brutto an. Welche Aussage ist richtig?",
   "a": [
    "Zulässig, wenn Jonas zustimmt.",
    "Zulässig, weil die Vergütung frei vereinbart werden darf.",
    "Unzulässig, im ersten Ausbildungsjahr gelten 2026 mindestens 724 €.",
    "Unzulässig, erst ab dem zweiten Jahr gilt eine Mindestvergütung."
   ],
   "c": 2,
   "fb": "Die Mindestausbildungsvergütung nach § 17 BBiG darf nicht unterschritten werden."
  },
  {
   "label": "Reservefall D (tägliche Ausbildungszeit)",
   "q": "Nina Koch ist 17 Jahre alt und Auszubildende. Wegen Personalmangel soll sie täglich 9 Stunden arbeiten. Welche Aussage ist richtig?",
   "a": [
    "Zulässig, wenn die Mehrarbeit vergütet wird.",
    "Unzulässig, für Jugendliche gelten höchstens 8 Stunden täglich und 40 Stunden wöchentlich.",
    "Zulässig, bis zu 10 Stunden wie bei Erwachsenen.",
    "Zulässig, wenn die Eltern zustimmen."
   ],
   "c": 1,
   "fb": "§ 8 JArbSchG; ausnahmsweise sind 8,5 Stunden täglich erlaubt, wenn an anderen Tagen derselben Woche entsprechend weniger gearbeitet wird."
  },
  {
   "label": "Reservefall E (Beginn und Dauer)",
   "q": "Ben beginnt nach dem Abitur eine dreijährige Ausbildung und möchte sie verkürzen. Welche Aussage ist richtig?",
   "a": [
    "Ben beantragt die Verkürzung allein bei der Berufsschule.",
    "Ben und der Betrieb beantragen die Verkürzung gemeinsam bei der zuständigen Stelle.",
    "Die Ausbildung verkürzt sich wegen des Abiturs automatisch.",
    "Nur der Betrieb darf die Verkürzung bei der IHK beantragen."
   ],
   "c": 1,
   "fb": "§ 8 Abs. 1 BBiG; mit Abitur sind laut IHK bis zu zwölf Monate Verkürzung möglich."
  }
 ],
 "quiz": [
  {
   "q": "Eine Auszubildende ist zu Jahresbeginn 15 Jahre alt. Wie viele Werktage Mindesturlaub hat sie?",
   "a": [
    "24",
    "25",
    "27",
    "30"
   ],
   "c": 3,
   "fb": "§ 19 JArbSchG (unter 16 Jahren)"
  },
  {
   "q": "Ein Betrieb will eine Probezeit von sechs Monaten festlegen. Ist das zulässig?",
   "a": [
    "Ja, wenn der Azubi zustimmt",
    "Ja, in großen Betrieben",
    "Nein, höchstens vier Monate",
    "Nein, höchstens drei Monate"
   ],
   "c": 2,
   "fb": "§ 20 BBiG"
  },
  {
   "q": "Ein Azubi kündigt nach der Probezeit mündlich, weil er den Beruf wechseln will. Ist das wirksam?",
   "a": [
    "Ja, mit vier Wochen Frist",
    "Ja, ohne Frist",
    "Nein, die Kündigung muss schriftlich mit Angabe der Gründe erfolgen",
    "Nein, nur die IHK darf kündigen"
   ],
   "c": 2,
   "fb": "§ 22 Abs. 2 und 3 BBiG"
  },
  {
   "q": "Ein nicht tarifgebundener Betrieb zahlt im 2. Ausbildungsjahr (Beginn 2026) 800 €. Ist das zulässig?",
   "a": [
    "Ja, weil es mehr als im 1. Jahr ist",
    "Ja, wenn der Betrieb nicht tarifgebunden ist",
    "Nein, im 2. Jahr gelten mindestens 854 €",
    "Nein, im 2. Jahr gelten mindestens 977 €"
   ],
   "c": 2,
   "fb": "§ 17 BBiG"
  },
  {
   "q": "Ein volljähriger Azubi soll an einem Tag 10 Stunden arbeiten; im Durchschnitt von sechs Monaten bleibt es bei 8 Stunden. Ist das zulässig?",
   "a": [
    "Nein, höchstens 8 Stunden",
    "Ja, nach dem Arbeitszeitgesetz, wenn der Durchschnitt von 8 Stunden nicht überschritten wird",
    "Nein, nur mit Zustimmung der IHK",
    "Ja, dann sind sogar 12 Stunden erlaubt"
   ],
   "c": 1,
   "fb": "§ 3 ArbZG"
  }
 ],
 "experten": [
  {
   "t": "Probezeit",
   "kern": [
    "Ein bis vier Monate (§ 20 BBiG)",
    "Kündigung jederzeit ohne Frist, schriftlich (§ 22 Abs. 1 und 3 BBiG)"
   ],
   "frage": "Welche Kündigungsfrist gilt in der Probezeit?",
   "loesung": "Keine Frist, aber die Kündigung muss schriftlich erfolgen."
  },
  {
   "t": "Urlaub",
   "kern": [
    "Zu Jahresbeginn unter 16: 30, unter 17: 27, unter 18: 25, ab 18: 24 Werktage (§ 19 JArbSchG, § 3 BUrlG)",
    "Werktage sind alle Kalendertage außer Sonntagen und gesetzlichen Feiertagen."
   ],
   "frage": "Wie viele Werktage Mindesturlaub hat eine Auszubildende, die zu Jahresbeginn 16 Jahre alt ist?",
   "loesung": "27 Werktage."
  },
  {
   "t": "Vergütung",
   "kern": [
    "Bei Beginn 2026 mindestens 724 / 854 / 977 / 1.014 € im 1. bis 4. Jahr (§ 17 BBiG)"
   ],
   "frage": "Wie hoch ist die Mindestausbildungsvergütung im 3. Jahr bei Beginn 2026?",
   "loesung": "977 €."
  },
  {
   "t": "Kündigung",
   "kern": [
    "In der Probezeit ohne Frist.",
    "Danach fristlos aus wichtigem Grund (innerhalb von zwei Wochen nach Kenntnis) oder durch den Azubi mit vier Wochen Frist bei Berufswechsel oder Aufgabe der Ausbildung.",
    "Immer schriftlich, mit Gründen (§ 22 Abs. 2 bis 4 BBiG)."
   ],
   "frage": "Was muss ein Azubi beachten, der nach der Probezeit kündigen will, weil er den Beruf wechselt?",
   "loesung": "Vier Wochen Frist, schriftlich, mit Angabe der Gründe."
  }
 ],
 "merk": [
  {
   "thema": "Vertrag",
   "text": "Wesentlicher Inhalt in Textform (seit 01.08.2024), unter anderem Beginn, Dauer, tägliche Ausbildungszeit, Probezeit, Vergütung, Urlaub, Kündigung",
   "para": "§ 11 BBiG"
  },
  {
   "thema": "Dauer",
   "text": "Verkürzung auf gemeinsamen Antrag; Ende mit Bekanntgabe des Prüfungsergebnisses; Verlängerung nach Nichtbestehen höchstens um ein Jahr",
   "para": "§ 8, § 21 BBiG"
  },
  {
   "thema": "Ausbildungszeit",
   "text": "Jugendliche höchstens 8 Stunden täglich und 40 pro Woche; Volljährige 8 Stunden, bis 10 mit Ausgleich in sechs Monaten",
   "para": "§ 8 JArbSchG, § 3 ArbZG"
  },
  {
   "thema": "Vergütung",
   "text": "Mindestens 724 / 854 / 977 / 1.014 € (1.–4. Jahr, Beginn 2026)",
   "para": "§ 17 BBiG"
  },
  {
   "thema": "Urlaub",
   "text": "Zu Jahresbeginn unter 16: 30, unter 17: 27, unter 18: 25, ab 18: 24 Werktage",
   "para": "§ 19 JArbSchG, § 3 BUrlG"
  },
  {
   "thema": "Probezeit",
   "text": "Ein bis vier Monate; Kündigung jederzeit ohne Frist, schriftlich",
   "para": "§ 20, § 22 Abs. 1 BBiG"
  },
  {
   "thema": "Kündigung nach der Probezeit",
   "text": "Fristlos aus wichtigem Grund (innerhalb von zwei Wochen nach Kenntnis) oder durch den Azubi mit vier Wochen Frist bei Berufswechsel; immer schriftlich, mit Gründen",
   "para": "§ 22 Abs. 2 bis 4 BBiG"
  },
  {
   "thema": "Pflichten des Azubis",
   "text": "Lernen, sorgfältig arbeiten, Weisungen befolgen, Ordnung beachten, Geheimnisse wahren, Ausbildungsnachweis führen",
   "para": "§ 13 BBiG"
  },
  {
   "thema": "Pflichten der Ausbildenden",
   "text": "Ausbildungsziel vermitteln, Ausbildungsmittel kostenlos stellen, freistellen, Zeugnis ausstellen, Vergütung zahlen",
   "para": "§§ 14 bis 17 BBiG"
  }
 ],
 "quellen": [
  {
   "t": "BIBB – Mindestausbildungsvergütung 2026",
   "u": "https://www.bibb.de/de/199658.php"
  },
  {
   "t": "BBiG §§ 20–22 – Probezeit und Kündigung",
   "u": "https://www.buzer.de/gesetz/3118/b8613.htm"
  },
  {
   "t": "IHK – Urlaubsanspruch von Auszubildenden",
   "u": "https://www.ihk.de/bayreuth/hauptnavigation/service/ausbildung/rechtliches/bundesurlaubsgesetz-4447896"
  },
  {
   "t": "BBiG § 11 – Vertragsabfassung, Änderung vom 01.08.2024",
   "u": "https://www.buzer.de/gesetz/3118/al198348-0.htm"
  },
  {
   "t": "IHK München – Verkürzung und Verlängerung der Ausbildung",
   "u": "https://www.ihk-muenchen.de/ausbildung-fortbildung/ausbilden/ausbildungsverhaeltnis/verkuerzung-verlaengerung/"
  },
  {
   "t": "BBiG §§ 13 bis 17 – Pflichten",
   "u": "https://www.buzer.de/gesetz/3118/b8608.htm"
  },
  {
   "t": "IHK Erfurt – Höchstzulässige Ausbildungszeit",
   "u": "https://www.ihk.de/erfurt/bildung/ausbildungswiki/hoechstzulaessige-ausbildungszeit-4659100"
  },
  {
   "t": "Büromanagement-Prüfungsverordnung – Wirtschafts- und Sozialkunde",
   "u": "https://www.ihk.de/blueprint/servlet/resource/blob/4211038/080ed6789f3f23ed03a7002946d78600/vo-bueromanagement-aenderung-data.pdf"
  }
 ]
};
