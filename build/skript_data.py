# -*- coding: utf-8 -*-
"""Sprechskript v4: Inhalte je Folie (Nummer = Folie in praesentation_unterricht_v4.pptx)."""
# Felder: titel, text (Absaetze), klicks (Liste), frage (dict frage/sozial/erw/fehl/reakt), uebergang, streich
S = {}
S[1] = dict(titel="Titelfolie",
 text=["Guten Morgen zusammen! Wir sind Yasin und Mido, und wir halten heute die Stunde im Fach GP. Unser Thema: Rechte und Pflichten aus dem Ausbildungsvertrag."],
 klicks=[], frage=None, uebergang="Mido bleibt kurz still; Yasin geht direkt weiter zur nächsten Folie.", streich="Nein")
S[2] = dict(titel="Aufhänger, Lernziele und Ablauf",
 text=["Stellt euch vor: Es ist euer erster Arbeitstag. Ihr habt den Ausbildungsvertrag unterschrieben, aber ehrlich gesagt hat ihn kaum jemand richtig gelesen. Die Frage lautet also: Was steht eigentlich in diesem Vertrag?",
       "Ruft einfach mal rein, was euch einfällt. Wir schreiben mit. [Zurufe sammeln, 2–3 Stichworte an die Tafel.]",
       "Danke, das sind schon gute Punkte. Am Ende der Stunde könnt ihr drei Dinge: Erstens nennen, was in einen Ausbildungsvertrag gehört. Zweitens Vergütung, Urlaub, Arbeitszeit, Probezeit und Kündigung anwenden. Und drittens Fälle mit der passenden Regel begründen.",
       "Unser Ablauf: Zuerst prüfen wir kurz, was ihr schon wisst. Dann erklären wir die wichtigsten Regeln. Danach seid ihr dran und übt selbst. Anschließend besprechen wir die Lösungen, und zum Schluss gibt es ein kurzes Quiz."],
 klicks=[],
 frage=dict(frage="Dein erster Arbeitstag: Was steht eigentlich in deinem Ausbildungsvertrag?", sozial="Plenum · Zuruf",
  erw="Gehalt/Vergütung, Urlaub, Probezeit, Arbeitszeit, Beginn/Dauer, Kündigung.",
  fehl="Andere Stichworte (z. B. Kleiderordnung, Arbeitsort) nicht abwerten, einfach notieren.",
  reakt="Alles an die Tafel schreiben, nicht bewerten; ab Folie 4 wird abgeglichen."),
 uebergang="Dann prüfen wir jetzt, was ihr schon wisst – Mido übernimmt.", streich="Nein (Zuruf auf 30 s kürzbar)")
S[3] = dict(titel="Was wisst ihr schon?",
 text=["Bevor wir erklären, wollen wir wissen, wo ihr steht. Wir stellen vier Fragen. Ihr ruft die Antwort einfach rein, wir schreiben sie an die Tafel, und wir sagen noch nicht, was stimmt. Das klären wir später.",
       "Frage a: Wie lange darf die Probezeit höchstens dauern? [Antworten sammeln, in Spalte a notieren.]",
       "Frage b: Wie viele Urlaubstage stehen einem Azubi mindestens zu? [Spalte b.]",
       "Frage c: Welche Kündigungsfrist gilt in der Probezeit? [Spalte c.]",
       "Und Frage d: Muss eine Kündigung schriftlich sein? [Spalte d.]",
       "Vielen Dank. Wir lassen die Antworten bis später stehen."],
 klicks=[],
 frage=dict(frage="a) Wie lange darf die Probezeit höchstens dauern? b) Wie viele Urlaubstage stehen einem Azubi mindestens zu? c) Welche Kündigungsfrist gilt in der Probezeit? d) Muss eine Kündigung schriftlich sein?",
  sozial="Plenum · Zuruf, Tafel (Spalten a–d)",
  erw="a) vier Monate · b) 24 Werktage ab 18 Jahren (Jugendliche 25 bis 30) · c) keine Frist · d) ja, schriftlich.",
  fehl="sechs Monate; 20 Tage; vier Wochen; E-Mail genügt.",
  reakt="Notieren, nachfragen „Wie kommst du darauf?“, nicht korrigieren und nicht auflösen. Auflösung auf Folie 20."),
 uebergang="Jetzt erklärt Yasin, was im Vertrag stehen muss und was dazu gesetzlich gilt.", streich="Nein")
S[4] = dict(titel="Der Vertrag: sechs Pflichtangaben",
 text=["Was gehört in den Vertrag? Das regelt § 11 des Berufsbildungsgesetzes, kurz BBiG. Sechs Angaben sind Pflicht: Beginn und Dauer der Ausbildung, die tägliche Ausbildungszeit, die Probezeit, die Vergütung, der Urlaub und die Kündigungsvoraussetzungen.",
       "Schaut mal auf die Tafel: Vieles davon habt ihr vorhin selbst genannt.",
       "Noch ein Hinweis zur Form: Seit dem 1. August 2024 genügt die Textform, zum Beispiel per E-Mail. Vorher war Papierform nötig.",
       "[Optional, mündlich:] Was davon habt ihr genannt?"],
 klicks=[], frage=dict(frage="Was davon habt ihr genannt? (optional, mündlich)", sozial="Plenum · Zuruf", erw="Die Zurufe von Folie 2 mit den sechs Pflichtangaben abgleichen.", fehl="–", reakt="Kurz bestätigen, keine Diskussion."),
 uebergang="Die erste Pflichtangabe war Beginn und Dauer – dazu gleich mehr.", streich="Nein")
S[5] = dict(titel="Beginn und Dauer",
 text=["Beginn und Dauer: Die Ausbildung läuft von ihrem Beginn bis zur Prüfung. Sie endet mit der Bekanntgabe des Prüfungsergebnisses. Das steht in § 8 und § 21 BBiG.",
       "Die Dauer lässt sich ändern: Eine Verkürzung gibt es nur auf gemeinsamen Antrag von Azubi und Betrieb bei der zuständigen Stelle. Eine Verlängerung ist die Ausnahme: auf Antrag des Azubis oder nach nicht bestandener Prüfung, höchstens um ein Jahr.",
       "[Optional:] Wer beantragt die Verkürzung?"],
 klicks=[], frage=dict(frage="Wer beantragt die Verkürzung? (optional)", sozial="Plenum", erw="Azubi und Betrieb gemeinsam.", fehl="Nur der Betrieb / nur der Azubi.", reakt="Richtigstellen: gemeinsam, bei der zuständigen Stelle."),
 uebergang="Wie lange man am Tag arbeitet, ist die nächste Pflichtangabe.", streich="Nein (auf 50 s kürzbar)")
S[6] = dict(titel="Ausbildungszeit",
 text=["Zur täglichen Ausbildungszeit gibt es zwei Regeln. Für Jugendliche gilt § 8 des Jugendarbeitsschutzgesetzes: höchstens 8 Stunden täglich und 40 pro Woche, ausnahmsweise 8,5 Stunden, wenn es ausgeglichen wird.",
       "Für Volljährige gilt § 3 des Arbeitszeitgesetzes: grundsätzlich 8 Stunden täglich. Bis zu 10 Stunden sind möglich, wenn innerhalb von sechs Monaten ausgeglichen wird, und es sind höchstens 48 Stunden pro Woche.",
       "[Optional:] Wie viele Stunden dürfen Jugendliche täglich?"],
 klicks=[], frage=dict(frage="Wie viele Stunden dürfen Jugendliche täglich? (optional)", sozial="Plenum", erw="8 Stunden (ausnahmsweise 8,5).", fehl="9 oder 10 Stunden.", reakt="Auf die linke Spalte der Folie zeigen."),
 uebergang="Die nächste Zahl interessiert euch bestimmt am meisten: das Geld.", streich="Nein")
S[7] = dict(titel="Mindestausbildungsvergütung 2026",
 text=["Und jetzt das Geld. Nach § 17 BBiG gibt es eine Mindestausbildungsvergütung. Bei Beginn 2026 sind das im ersten Jahr 724 Euro, im zweiten 854 Euro, im dritten 977 Euro und im vierten 1.014 Euro.",
       "Diese Beträge dürfen nicht unterschritten werden, und sie werden jedes Jahr neu festgelegt.",
       "[Optional:] Wie hoch ist die Mindestvergütung im dritten Jahr?"],
 klicks=[], frage=dict(frage="Wie hoch ist die Mindestvergütung im 3. Jahr? (optional)", sozial="Plenum", erw="977 €.", fehl="854 € oder 1.014 € verwechselt.", reakt="Auf den Balken zeigen."),
 uebergang="Neben dem Geld zählt für viele die freie Zeit – dazu Mido.", streich="Nein")
S[8] = dict(titel="Urlaub nach Alter",
 text=["Beim Urlaub kommt es auf das Alter an. Nach § 19 des Jugendarbeitsschutzgesetzes und § 3 des Bundesurlaubsgesetzes gilt, jeweils gerechnet nach dem Alter zu Jahresbeginn: Unter 16 Jahren mindestens 30 Werktage, unter 17 mindestens 27, unter 18 mindestens 25 und ab 18 mindestens 24 Werktage.",
       "Wichtig ist das Wort Werktage: Das sind alle Kalendertage außer Sonntagen und gesetzlichen Feiertagen. 24 Werktage entsprechen 20 Arbeitstagen bei einer Fünf-Tage-Woche.",
       "[Optional:] Zählt der Samstag als Werktag? Ja."],
 klicks=[], frage=dict(frage="Zählt der Samstag als Werktag? (optional)", sozial="Plenum", erw="Ja.", fehl="Werktage = Montag bis Freitag.", reakt="Definition auf der Folie vorlesen."),
 uebergang="Jedes Ausbildungsverhältnis beginnt mit der Probezeit.", streich="Nein")
S[9] = dict(titel="Probezeit",
 text=["Jedes Ausbildungsverhältnis beginnt mit einer Probezeit. Nach § 20 BBiG dauert sie mindestens einen Monat und höchstens vier Monate.",
       "Schaut zur Tafel: Was stand dort bei Frage a? [Nicht auflösen, erst auf Folie 20.]",
       "[Optional:] Darf die Probezeit sechs Monate dauern? Nein."],
 klicks=[], frage=dict(frage="Darf die Probezeit sechs Monate dauern? (optional)", sozial="Plenum", erw="Nein, höchstens vier Monate.", fehl="Sechs Monate.", reakt="Auf die Monatsreihe zeigen."),
 uebergang="Was in der Probezeit gilt, wenn jemand kündigen will, zeigt Yasin im Entscheidungsbaum.", streich="Nein (auf 35 s kürzbar)")
S[10] = dict(titel="Kündigung: Entscheidungsbaum",
 text=["Die Kündigung ist der Teil, bei dem die meisten Fehler passieren. Wir gehen den Baum von oben nach unten durch. § 22 Absatz 1 und 2 BBiG.",
       "Erste Frage: Wann wird gekündigt? In der Probezeit kann jederzeit ohne Frist gekündigt werden, und zwar von beiden Seiten.",
       "Nach der Probezeit ist es strenger: Der Betrieb kann nur fristlos aus einem wichtigen Grund kündigen. Der Azubi kann mit vier Wochen Frist kündigen, aber nur, wenn er die Ausbildung aufgibt oder den Beruf wechseln will.",
       "[Optional:] Welche Frist hat der Azubi nach der Probezeit? Vier Wochen."],
 klicks=[], frage=dict(frage="Welche Frist hat der Azubi nach der Probezeit? (optional)", sozial="Plenum", erw="Vier Wochen (bei Aufgabe der Ausbildung oder Berufswechsel).", fehl="Keine Frist; Monatsende.", reakt="Auf den rechten Ast des Baums zeigen."),
 uebergang="Dazu kommt, wie gekündigt werden muss – Form und Frist.", streich="Nein")
S[11] = dict(titel="Kündigung: Form und Frist",
 text=["Drei Karten, drei Sätze, § 22 Absatz 3 und 4 BBiG. Erstens: Eine Kündigung ist immer schriftlich, eine E-Mail ist ausgeschlossen. Zweitens: Nach der Probezeit muss sie mit Gründen erfolgen. Drittens: Eine Kündigung aus wichtigem Grund ist nur innerhalb von zwei Wochen möglich, nachdem man die Gründe kennt.",
       "[Optional:] Reicht eine E-Mail? Nein."],
 klicks=[], frage=dict(frage="Reicht eine E-Mail? (optional)", sozial="Plenum", erw="Nein, schriftlich; E-Mail ist ausgeschlossen.", fehl="E-Mail genügt (Verwechslung mit der Textform des Vertrags).", reakt="Unterschied betonen: Vertrag Textform, Kündigung schriftlich."),
 uebergang="Zuletzt: Wer muss eigentlich was tun?", streich="Nein (auf 45 s kürzbar)")
S[12] = dict(titel="Pflichten von Azubi und Ausbildenden",
 text=["Zum Schluss die Pflichten, §§ 13 bis 17 BBiG. Azubis müssen lernen, sorgfältig arbeiten, Weisungen befolgen, die Ordnung beachten, Geheimnisse wahren und den Ausbildungsnachweis führen.",
       "Ausbildende müssen das Ausbildungsziel vermitteln, die Ausbildungsmittel kostenlos stellen, für Berufsschule und Prüfungen freistellen, ein Zeugnis ausstellen und die Vergütung zahlen.",
       "[Optional:] Wer stellt die Ausbildungsmittel? Der Betrieb, kostenlos."],
 klicks=[], frage=dict(frage="Wer stellt die Ausbildungsmittel? (optional)", sozial="Plenum", erw="Der Betrieb, kostenlos.", fehl="Der Azubi.", reakt="Auf die rechte Spalte zeigen."),
 uebergang="Jetzt habt ihr alles gehört – jetzt seid ihr dran. Mido erklärt den Auftrag.", streich="Nein (nur bei äußerster Zeitnot nur die Überschriften nennen)")
S[13] = dict(titel="Jetzt seid ihr dran (Aufgabenüberblick)",
 text=["Jetzt seid ihr dran. Öffnet bitte die Seite über den QR-Code oder die Adresse unten. [QR-Code 20 Sekunden stehen lassen.]",
       "Es gibt drei Aufgaben, die Reihenfolge ist frei: Erstens die Rote/Grüne Karte, allein, drei Minuten. Zweitens der Vertrags-Detektiv, zu zweit, fünf Minuten. Drittens die IHK-Fälle A bis C, zu zweit, vier Minuten. Als Hilfsmittel habt ihr das Merkblatt.",
       "Wer schnell fertig ist, findet auf der Website Reserve. Wer kein Handy hat, schaut mit einer Partnerin oder einem Partner mit.",
       "Handzeichen: Wer ist auf der Seite?"],
 klicks=[], frage=dict(frage="Wer ist auf der Seite? (Handzeichen)", sozial="Plenum · Handzeichen", erw="Fast alle zeigen auf.", fehl="Seite lädt nicht / kein Handy.", reakt="Zu zweit mitschauen lassen; bei Totalausfall Plan B (Folien 23–27)."),
 uebergang="Dann geht es los: Yasin startet die Zeit.", streich="Nein")
S[14] = dict(titel="Arbeitsphase",
 text=["Zwölf Minuten, los geht’s. Der Balken läuft von selbst.",
       "[Während der Arbeit durch die Reihen gehen, helfen, typische Fehler merken. Zeit ansagen:]",
       "Nach 3 Minuten: „Drei Minuten sind um. Wer die Rote/Grüne Karte hat, kann zum Vertrags-Detektiv wechseln.“",
       "Nach 8 Minuten: „Acht Minuten sind um, noch vier. Jetzt sind die IHK-Fälle dran.“",
       "Nach 12 Minuten: „Die Zeit ist um. Bitte Handys kurz zur Seite, wir besprechen jetzt gemeinsam.“"],
 klicks=["Beim Folienwechsel startet der Countdown automatisch: 12 Segmente, je 60 Sekunden."],
 frage=None, extra="Typische Fehler für die Besprechung notieren: Probezeit 6 Monate, 650 €, 9 Stunden, 20 Werktage, vier Wochen in der Probezeit.",
 uebergang="Mido bleibt nah am Beamer; Yasin leitet zum Vertragsauszug über.", streich="Teilweise: Arbeitsphase auf 9 Minuten kürzbar (−3 Min.)")
S[15] = dict(titel="Vertragsauszug: Welche Zeilen enthalten einen Fehler?",
 text=["Schauen wir uns den Vertragsauszug aus dem Detektiv an. Er stammt von einem fiktiven Betrieb. Der Azubi ist Jonas Muster, geboren am 20.11.2009, Ausbildungsbeginn 01.09.2026.",
       "Welche Zeilen enthalten einen Fehler? Nennt die Nummern. [Strichliste an der Tafel.] Ich bestätige noch nichts, das machen wir gleich Zeile für Zeile."],
 klicks=[], frage=dict(frage="Welche Zeilen enthalten einen Fehler?", sozial="Plenum · Zuruf, Strichliste", erw="Zeilen 2, 3, 4, 5, 6.", fehl="Zeile 1 oder 7 wird genannt.", reakt="Nicht bestätigen; in der Auflösung begründen."),
 uebergang="Die Auflösung macht Mido mit euch, Fehler für Fehler.", streich="Nein")
S[16] = dict(titel="Auflösung: die 5 Fehler",
 text=["Wir gehen jetzt Zeile für Zeile durch. Pro Klick ein Fehler. Bei jedem fragen wir: Wer hat ihn gefunden, und welche Regel steckt dahinter?",
       "[Klick 1] Zeile 2: Probezeit sechs Monate. Regel: höchstens vier Monate, § 20 BBiG.",
       "[Klick 2] Zeile 3: 650 Euro im ersten Jahr. Regel: mindestens 724 Euro, § 17 BBiG.",
       "[Klick 3] Zeile 4: 9 Stunden täglich. Jonas ist bei Beginn 16 Jahre alt (geboren 20.11.2009), also gilt: Jugendliche höchstens 8 Stunden täglich und 40 pro Woche, § 8 JArbSchG.",
       "[Klick 4] Zeile 5: 20 Werktage Urlaub. Regel: mindestens 24 Werktage, bei Jugendlichen je nach Alter 25 bis 30, § 3 BUrlG und § 19 JArbSchG.",
       "[Klick 5] Zeile 6: vier Wochen Frist in der Probezeit. Regel: in der Probezeit jederzeit ohne Frist, schriftlich, § 22 Absatz 1 und 3 BBiG.",
       "Die Zeilen 1 und 7 sind korrekt."],
 klicks=["Klick 1: Fehler 1 (Zeile § 2, Probezeit) erscheint, mit Regel", "Klick 2: Fehler 2 (§ 3, Vergütung)", "Klick 3: Fehler 3 (§ 4, Ausbildungszeit)", "Klick 4: Fehler 4 (§ 5, Urlaub)", "Klick 5: Fehler 5 (§ 6, Kündigung)"],
 frage=dict(frage="Wer hat diesen Fehler gefunden? Welche Regel steckt dahinter? (pro Klick)", sozial="Plenum · Gruppen berichten",
  erw="1: höchstens vier Monate (§ 20 BBiG) · 2: mindestens 724 € im 1. Jahr (§ 17 BBiG) · 3: Jugendliche höchstens 8 Stunden täglich und 40 pro Woche (§ 8 JArbSchG) · 4: mindestens 24 Werktage, Jugendliche 25 bis 30 (§ 3 BUrlG, § 19 JArbSchG) · 5: in der Probezeit jederzeit ohne Frist, schriftlich (§ 22 Abs. 1 und 3 BBiG).",
  fehl="Fehler 3: Alter nicht beachtet; Zeile 1 oder 7 für fehlerhaft gehalten.", reakt="Gruppe zuerst berichten lassen, dann Klick; bei Fehler 3 Geburtsdatum nennen."),
 uebergang="Jetzt wenden wir die Regeln auf Fälle an – wie in der IHK-Prüfung. Yasin liest Fall A.", streich="Nein (Fehler 3–5 kürzbar)")
def fall(nr, titel, text, frage, sozial, erw, fehl, reakt, uebergang, streich, spr_hint=""):
    S[nr] = dict(titel=titel, text=text, klicks=["Klick 1: Lösung wird markiert (grüner Rahmen + Haken)", "Klick 2: Begründung mit Paragraf erscheint"],
     frage=dict(frage=frage, sozial=sozial, erw=erw, fehl=fehl, reakt=reakt), uebergang=uebergang, streich=streich)
fall(17, "Fall A (Probezeit und Kündigung)",
 ["Fall A: Lena Berg beginnt am 1. September bei der Muster GmbH eine Ausbildung zur Kauffrau für Büromanagement, vereinbart sind drei Monate Probezeit. Am 10. Oktober merkt sie, dass der Beruf nicht zu ihr passt. Welche Aussage ist richtig? [Antworten A bis D vorlesen.]",
  "Abstimmung per Handzeichen: Wer sagt A? B? C? D? [Verteilung an die Tafel.] Wer begründet seine Wahl mit einer Regel?",
  "[Klick 1] Richtig ist B. [Klick 2] In der Probezeit ist die Kündigung jederzeit ohne Frist möglich, aber schriftlich, § 22 Absatz 1 und 3 BBiG."],
 "Welche Aussage ist richtig, A, B, C oder D?", "Plenum · Abstimmung per Handzeichen", "B: In der Probezeit ist die Kündigung jederzeit ohne Frist möglich, aber schriftlich (§ 22 Abs. 1 und 3 BBiG).",
 "A (vier Wochen Frist), C (nur zum Monatsende), D (Zustimmung der IHK).", "Eine Begründung erfragen, Fehlvorstellung nicht bloßstellen, Regel nennen.",
 "Mido liest Fall B.", "Nein")
fall(18, "Fall B (Urlaub)",
 ["Fall B: Tim Roth ist zu Beginn des Kalenderjahres 17 Jahre alt und arbeitet an fünf Tagen pro Woche. Wie viele Werktage Mindesturlaub stehen ihm nach dem Gesetz zu? [Antworten A bis D vorlesen.]",
  "Handzeichen: A, B, C oder D? [Verteilung an die Tafel, eine Begründung erfragen.]",
  "[Klick 1] Richtig ist C: 25 Werktage. [Klick 2] Jugendliche unter 18 Jahren haben mindestens 25 Werktage, § 19 JArbSchG. Das entspricht 21 Arbeitstagen bei der Fünf-Tage-Woche."],
 "Wie viele Werktage Mindesturlaub stehen Tim zu: A, B, C oder D?", "Plenum · Abstimmung per Handzeichen", "C: Jugendliche unter 18 Jahren haben mindestens 25 Werktage (§ 19 JArbSchG), das entspricht 21 Arbeitstagen bei der Fünf-Tage-Woche.",
 "A (20 Werktage), B (24 Werktage: Alter nicht beachtet), D (30 Werktage).", "Alter zu Jahresbeginn betonen, Alterstreppe von Folie 8 zeigen.",
 "Yasin liest Fall C.", "Ja (bei Zeitnot streichen; dann direkt zu Fall C oder Folie 20)")
fall(19, "Fall C (Vergütung)",
 ["Fall C: Die Muster GmbH ist nicht tarifgebunden und bietet Jonas für den Ausbildungsbeginn 2026 im ersten Jahr 690 Euro brutto an. Welche Aussage ist richtig? [Antworten A bis D vorlesen.]",
  "Handzeichen: A, B, C oder D? [Verteilung an die Tafel, eine Begründung erfragen.]",
  "[Klick 1] Richtig ist C. [Klick 2] Die Mindestausbildungsvergütung nach § 17 BBiG darf nicht unterschritten werden; im ersten Jahr sind es 2026 mindestens 724 Euro."],
 "Welche Aussage ist richtig, A, B, C oder D?", "Plenum · Abstimmung per Handzeichen", "C: Die Mindestausbildungsvergütung nach § 17 BBiG darf nicht unterschritten werden (im 1. Jahr 2026 mindestens 724 €).",
 "A (zulässig, wenn Jonas zustimmt), B (frei vereinbar), D (erst ab dem 2. Jahr).", "Hinweis: Zustimmung des Azubis heilt eine Unterschreitung nicht.",
 "Jetzt schließen wir den Kreis zum Anfang – Yasin geht zurück zu unseren vier Fragen.", "Ja (bei Zeitnot streichen)")
S[20] = dict(titel="Zurück zum Anfang",
 text=["Zurück zum Anfang: Das waren unsere vier Fragen. Schaut auf die Tafel, was ihr vorhin gesagt habt, und vergleicht.",
       "[Klick 1] a: Vier Monate. [Klick 2] b: 24 Werktage ab 18 Jahren, Jugendliche 25 bis 30. [Klick 3] c: Keine Frist, aber schriftlich. [Klick 4] d: Ja, die Kündigung muss schriftlich erfolgen, § 22 Absatz 3 BBiG.",
       "Jetzt noch eine Frage an euch: Was war neu für euch?"],
 klicks=["Klick 1: Antwort a", "Klick 2: Antwort b", "Klick 3: Antwort c", "Klick 4: Antwort d"],
 frage=dict(frage="Was war neu für euch?", sozial="Plenum · offen", erw="Freie Antworten (z. B. Alterstreppe beim Urlaub, keine Frist in der Probezeit).", fehl="–", reakt="Zwei bis drei Stimmen sammeln, danke sagen."),
 uebergang="Zum Abschluss testet Mido, was bei euch hängen geblieben ist.", streich="Nein (auf 50 s kürzbar)")
S[21] = dict(titel="Mini-Quiz: Zeig, was du kannst",
 text=["Jetzt testet ihr euch selbst: Das Mini-Quiz auf der Website. Fünf Fragen, allein, etwa drei Minuten. Die Seite ist dieselbe wie vorhin.",
       "[Während des Quiz nicht sprechen, kein Foliensprung. Nach ca. 3 Minuten:]",
       "Zeit ist um. Handzeichen: Wer hat 5 richtig? 4? 3? Weniger? [Zahlen notieren.]"],
 klicks=[], frage=dict(frage="Wer hat 5, 4, 3 oder weniger Fragen richtig?", sozial="Einzelarbeit · Handy, danach Handzeichen", erw="Mehrheit 4 oder 5 richtig.", fehl="Seite lädt nicht → Plan B (Folien 26 und 27).", reakt="Zahlen notieren; bei vielen 3 oder weniger auf das Merkblatt verweisen."),
 uebergang="Mit den fünf wichtigsten Zahlen schließt Yasin ab.", streich="Nein (Fragen 1–3 genügen bei Zeitnot)")
S[22] = dict(titel="Merksatz und Abschluss",
 text=["Merkt euch diese fünf: Vier Monate Probezeit höchstens, § 20 BBiG. 724 Euro im ersten Jahr bei Beginn 2026, § 17 BBiG. 24 Werktage Urlaub ab 18, § 3 BUrlG. Kündigung immer schriftlich, nie per E-Mail, § 22 BBiG. Und 8 Stunden täglich für Jugendliche, § 8 JArbSchG.",
       "Das alles steht auf dem Merkblatt zum Mitnehmen.",
       "Zum Abschluss ein Blitzlicht: Was nehme ich aus dieser Stunde mit, und was fehlt mir noch? Ein Satz pro Person oder Reihe.",
       "Vielen Dank fürs Mitmachen! Zum Weiterüben findet ihr alles auf der Website."],
 klicks=[], frage=dict(frage="Was nehme ich aus dieser Stunde mit – und was fehlt mir noch?", sozial="Plenum · Blitzlicht", erw="Offene Antworten (Zahlen, Fristen, Website).", fehl="–", reakt="Nicht kommentieren, nur danken; bei „fehlt mir noch“ auf Booklet/Website verweisen."),
 uebergang="Ende der Stunde.", streich="Nein (Blitzlicht auf drei Stimmen kürzbar)")
S[23] = dict(titel="Plan B: Stimmt oder stimmt nicht?",
 text=["Falls Internet oder Handys ausfallen, machen wir die Übung ohne Handy: Ich lese zehn Aussagen vor. Daumen hoch heißt stimmt, Daumen runter heißt stimmt nicht. Bei „drei“ zeigen alle gleichzeitig.",
       "[Aussage 1 bis 10 vorlesen, jeweils kurz warten; dann Lösungsfolie 24.]"],
 klicks=[], frage=dict(frage="Zehn Aussagen: Stimmt oder stimmt nicht?", sozial="Plenum · Daumen hoch/runter", erw="Lösungen auf Folie 24.", fehl="Aussagen 2, 5, 8, 9 häufig falsch eingeschätzt.", reakt="Auf „drei“ gleichzeitig zeigen lassen."),
 uebergang="Mido zeigt die Lösungen.", streich="Ja (nur bei Ausfall zeigen)")
S[24] = dict(titel="Plan B: Lösungen",
 text=["Hier die Lösungen. 1 stimmt, § 20 BBiG. 2 stimmt nicht, höchstens vier Monate. 3 stimmt, § 22 Absatz 1. 4 stimmt, § 22 Absatz 2. 5 stimmt nicht: Die Kündigung muss schriftlich erfolgen, die elektronische Form ist ausgeschlossen, § 22 Absatz 3. 6 stimmt, § 17 BBiG. 7 stimmt, § 3 BUrlG. 8 stimmt nicht: Werktage sind alle Kalendertage außer Sonntagen und gesetzlichen Feiertagen. 9 stimmt nicht: höchstens 8 Stunden täglich und 40 pro Woche, § 8 JArbSchG. 10 stimmt, § 15 BBiG."],
 klicks=[], frage=None, uebergang="Danach weiter mit dem Plan-B-Auszug (Folie 25) oder Quiz (26).", streich="Ja (nur bei Ausfall zeigen)")
S[25] = dict(titel="Plan B: Welche Zeilen enthalten einen Fehler?",
 text=["Ohne Handy lösen wir den Vertragsauszug gemeinsam: Welche Zeilen enthalten einen Fehler? Nennt die Nummern. [Zeilennummern sammeln.]",
       "Die Auflösung mache ich mündlich mit der Fehlerliste von Folie 16: Zeile 2 bis 6 sind fehlerhaft."],
 klicks=[], frage=dict(frage="Welche Zeilen enthalten einen Fehler?", sozial="Plenum · Zuruf", erw="Zeilen 2–6.", fehl="Zeile 1 oder 7 genannt.", reakt="Auflösung mündlich mit der Fehlerliste aus den Notizen von Folie 16."),
 uebergang="Mido stellt das Mini-Quiz auf Papier.", streich="Ja (nur bei Ausfall zeigen)")
S[26] = dict(titel="Plan B: Mini-Quiz",
 text=["Das Mini-Quiz ohne Handy: Fünf Fragen, ihr notiert A bis D auf einem Zettel. Ich lese jede Frage vor und lasse sie stehen. [Fragen vorlesen, nach der letzten Frage ca. 3 Minuten warten.]",
       "Danach zeigen wir die Lösungen und machen die Handzeichen: 5, 4, 3 oder weniger richtig?"],
 klicks=[], frage=dict(frage="Fünf Quizfragen, Antwort A–D auf Zettel", sozial="Einzelarbeit · A–D auf Zettel", erw="Lösungen auf Folie 27.", fehl="–", reakt="Danach Handzeichen 5/4/3/weniger."),
 uebergang="Yasin zeigt die Lösungen.", streich="Ja (nur bei Ausfall zeigen)")
S[27] = dict(titel="Plan B: Quiz-Lösungen",
 text=["Die Lösungen: Frage 1 D, 30 Werktage, § 19 JArbSchG. Frage 2 C, höchstens vier Monate, § 20 BBiG. Frage 3 C, die Kündigung muss schriftlich mit Angabe der Gründe erfolgen, § 22 Absatz 2 und 3 BBiG. Frage 4 C, im zweiten Jahr gelten mindestens 854 Euro, § 17 BBiG. Frage 5 B, ja, nach dem Arbeitszeitgesetz, wenn der Durchschnitt von 8 Stunden nicht überschritten wird, § 3 ArbZG.",
       "Handzeichen: 5, 4, 3 oder weniger richtig? [Zahlen notieren.]"],
 klicks=[], frage=None, uebergang="Weiter mit Folie 22 (Merksatz und Abschluss).", streich="Ja (nur bei Ausfall zeigen)")

# --- Feinabstimmung der Sprechtexte auf die Foliendauer (ca. 120-130 Woerter/Min. reines Sprechen) ---
S[4]["text"] = ["Was gehört eigentlich in einen Ausbildungsvertrag? Das ist nicht dem Zufall überlassen, sondern gesetzlich geregelt: in § 11 des Berufsbildungsgesetzes, kurz BBiG. Dort stehen sechs Pflichtangaben, die im Vertrag auftauchen müssen.",
 "Erstens Beginn und Dauer der Ausbildung. Zweitens die tägliche Ausbildungszeit. Drittens die Probezeit. Viertens die Vergütung. Fünftens der Urlaub. Und sechstens die Voraussetzungen, unter denen der Vertrag gekündigt werden kann.",
 "Schaut mal zur Tafel: Vieles davon habt ihr vorhin selbst zugerufen. Und genau diese sechs Punkte schauen wir uns gleich einzeln an.",
 "Noch ein kurzer Hinweis zur Form: Seit dem 1. August 2024 genügt für den Vertrag die Textform, zum Beispiel per E-Mail. Vorher war Papierform nötig.",
 "[Optional, nur mündlich:] Was davon habt ihr genannt?"]
S[5]["text"] = ["Fangen wir mit Beginn und Dauer an. Das regeln § 8 und § 21 BBiG. Die Ausbildung beginnt zum vereinbarten Datum und läuft bis zur Prüfung. Sie endet mit der Bekanntgabe des Prüfungsergebnisses. Der Zeitstrahl auf der Folie zeigt das: vom Beginn bis zur Prüfung.",
 "Die Dauer kann sich aber ändern. Eine Verkürzung gibt es nur auf gemeinsamen Antrag von Azubi und Betrieb bei der zuständigen Stelle. Allein kann also keiner von beiden verkürzen.",
 "Eine Verlängerung ist die Ausnahme: Sie ist möglich auf Antrag des Azubis oder nach nicht bestandener Prüfung, und zwar höchstens um ein Jahr.",
 "[Optional:] Wer beantragt die Verkürzung?"]
S[6]["text"] = ["Als Nächstes die tägliche Ausbildungszeit. Hier gibt es zwei Regeln, je nachdem, ob jemand jugendlich oder volljährig ist. Links seht ihr die Jugendlichen, rechts die Volljährigen.",
 "Für Jugendliche gilt § 8 des Jugendarbeitsschutzgesetzes: höchstens 8 Stunden täglich und höchstens 40 Stunden pro Woche. Ausnahmsweise sind 8,5 Stunden am Tag erlaubt, wenn das ausgeglichen wird.",
 "Für Volljährige gilt § 3 des Arbeitszeitgesetzes: Grundsätzlich sind es ebenfalls 8 Stunden täglich. Bis zu 10 Stunden sind möglich, wenn innerhalb von sechs Monaten ausgeglichen wird, und die Woche darf höchstens 48 Stunden haben.",
 "[Optional:] Wie viele Stunden dürfen Jugendliche täglich?"]
S[7]["text"] = ["Jetzt kommt das Thema, das euch wahrscheinlich am meisten interessiert: das Geld. Nach § 17 BBiG gibt es eine Mindestausbildungsvergütung, also einen Betrag, den kein Betrieb unterschreiten darf.",
 "Die Zahlen gelten für Beginn 2026 und steigen mit dem Ausbildungsjahr: Im ersten Jahr sind es 724 Euro, im zweiten 854 Euro, im dritten 977 Euro und im vierten Jahr 1.014 Euro. Schaut euch die Balken an: Sie werden von Jahr zu Jahr höher.",
 "Wichtig: Diese Beträge dürfen nicht unterschritten werden, und sie werden jedes Jahr neu festgelegt. Wer später anfängt, muss also wieder nachschauen.",
 "[Optional:] Wie hoch ist die Mindestvergütung im dritten Jahr?"]
S[8]["text"] = ["Beim Urlaub kommt es auf das Alter an, und zwar auf das Alter zu Beginn des Kalenderjahres. Die Grundlage sind § 19 des Jugendarbeitsschutzgesetzes und § 3 des Bundesurlaubsgesetzes.",
 "Die Alterstreppe auf der Folie: Wer unter 16 ist, hat mindestens 30 Werktage Urlaub. Unter 17 sind es mindestens 27 Werktage. Unter 18 mindestens 25 Werktage. Und ab 18 mindestens 24 Werktage.",
 "Wichtig ist das Wort Werktage. Werktage sind alle Kalendertage außer Sonntagen und gesetzlichen Feiertagen, der Samstag zählt also mit. Deshalb entsprechen 24 Werktage bei einer Fünf-Tage-Woche 20 Arbeitstagen. Das ist eine häufige Verwechslung.",
 "[Optional:] Zählt der Samstag als Werktag? Ja."]
S[9]["text"] = ["Jedes Ausbildungsverhältnis beginnt mit einer Probezeit. Nach § 20 BBiG dauert sie mindestens einen Monat und höchstens vier Monate. Auf der Folie seht ihr die Monatsreihe: erster, zweiter, dritter, vierter Monat.",
 "Vergleicht kurz mit der Tafel: Was habt ihr bei Frage a gesagt? Wir lösen das noch nicht auf, das machen wir am Ende.",
 "[Optional:] Darf die Probezeit sechs Monate dauern? Nein."]
S[10]["text"] = ["Jetzt zur Kündigung. Hier passieren die meisten Fehler, deshalb haben wir einen Entscheidungsbaum gemacht. Die Grundlage ist § 22 Absatz 1 und 2 BBiG. Wir gehen ihn von oben nach unten durch.",
 "Die erste Frage lautet: Wer kündigt, und wann? Wenn es in der Probezeit passiert, geht es jederzeit ohne Frist, und zwar von beiden Seiten.",
 "Nach der Probezeit ist es deutlich strenger. Der Betrieb kann dann nur noch fristlos aus einem wichtigen Grund kündigen. Der Azubi dagegen kann mit vier Wochen Frist kündigen, aber nur, wenn er die Ausbildung aufgibt oder den Beruf wechseln will.",
 "Merkt euch den Unterschied: In der Probezeit keine Frist, danach nur aus wichtigem Grund oder durch den Azubi mit vier Wochen Frist.",
 "[Optional:] Welche Frist hat der Azubi nach der Probezeit? Vier Wochen."]
S[11]["text"] = ["Dazu kommen die Regeln zu Form und Frist, § 22 Absatz 3 und 4 BBiG. Auf der Folie sind es drei Karten, jeweils ein Satz.",
 "Erstens: Eine Kündigung ist immer schriftlich. Eine E-Mail ist ausgeschlossen. Zweitens: Nach der Probezeit muss die Kündigung mit Gründen erfolgen. Drittens: Eine Kündigung aus wichtigem Grund ist nur innerhalb von zwei Wochen möglich, nachdem man die Gründe kennt.",
 "[Optional:] Reicht eine E-Mail? Nein."]
S[12]["text"] = ["Zum Schluss der Erklärung: wer was tun muss, in den §§ 13 bis 17 BBiG. Die Folie hat zwei Spalten.",
 "Links die Azubis, § 13: Sie müssen lernen, sorgfältig arbeiten, Weisungen befolgen, die Ordnung beachten, Geheimnisse wahren und den Ausbildungsnachweis führen.",
 "Rechts die Ausbildenden, §§ 14 bis 17: Sie müssen das Ausbildungsziel vermitteln, die Ausbildungsmittel kostenlos stellen, für Berufsschule und Prüfungen freistellen, ein Zeugnis ausstellen und die Vergütung zahlen.",
 "[Optional:] Wer stellt die Ausbildungsmittel? Der Betrieb, kostenlos."]
S[22]["text"] = ["Merkt euch diese fünf Zahlen: Vier Monate Probezeit höchstens, § 20 BBiG. 724 Euro im ersten Jahr bei Beginn 2026, § 17 BBiG. 24 Werktage Urlaub ab 18, § 3 BUrlG. Kündigung immer schriftlich, nie per E-Mail, § 22 BBiG. Und 8 Stunden täglich für Jugendliche, § 8 JArbSchG.",
 "Das steht alles auf dem Merkblatt zum Mitnehmen.",
 "Blitzlicht, ein Satz pro Person: Was nehme ich mit, und was fehlt mir noch? [Drei Stimmen.] Danke fürs Mitmachen!"]
