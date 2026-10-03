# -*- coding: utf-8 -*-
"""Aktivitaetsinhalte v2 (fest vorgegeben) + gemeinsame Daten aus data.py."""
from data import *

# Rote/Gruene Karte: (Aussage, stimmt?, Begruendung/Paragraf)
RG = [
    ("Die Probezeit darf höchstens vier Monate dauern.", True, "§ 20 BBiG"),
    ("Die Probezeit darf sechs Monate dauern, wenn der Azubi zustimmt.", False, "höchstens vier Monate (§ 20 BBiG)"),
    ("In der Probezeit kann der Azubi jederzeit ohne Frist kündigen.", True, "§ 22 Abs. 1 BBiG"),
    ("Nach der Probezeit darf der Azubi mit vier Wochen Frist kündigen, wenn er den Beruf wechseln will.", True, "§ 22 Abs. 2 BBiG"),
    ("Eine Kündigung per E-Mail ist wirksam, wenn sie rechtzeitig ankommt.", False, "Sie muss schriftlich erfolgen, die elektronische Form ist ausgeschlossen (§ 22 Abs. 3 BBiG)"),
    ("Die Mindestausbildungsvergütung im 1. Jahr beträgt bei Beginn 2026 724 €.", True, "§ 17 BBiG"),
    ("Ein volljähriger Azubi hat mindestens 24 Werktage Urlaub.", True, "§ 3 BUrlG"),
    ("Werktage sind nur Montag bis Freitag.", False, "Werktage sind alle Kalendertage außer Sonntagen und gesetzlichen Feiertagen"),
    ("Jugendliche dürfen täglich bis zu 10 Stunden arbeiten.", False, "höchstens 8 Stunden täglich und 40 pro Woche (§ 8 JArbSchG)"),
    ("Der Betrieb muss den Azubi am Arbeitstag vor der schriftlichen Abschlussprüfung freistellen.", True, "§ 15 BBiG"),
]

# Vertrags-Detektiv: Auszug (fiktiv). Zeilen: (Text, Fehlernummer oder None)
DET_KOPF = [
    "Berufsausbildungsvertrag (Auszug, fiktiv)",
    "Ausbildende: Muster GmbH (nicht tarifgebunden)",
    "Auszubildender: Jonas Muster, geboren am 20.11.2009",
    "Beruf: Kaufmann für Büromanagement",
]
DET = [
    ("§ 1 Beginn und Dauer: Die Ausbildung beginnt am 01.09.2026 und dauert drei Jahre.", None),
    ("§ 2 Probezeit: Die Probezeit beträgt sechs Monate.", 1),
    ("§ 3 Vergütung: Die monatliche Ausbildungsvergütung beträgt im 1. Ausbildungsjahr 650 € brutto.", 2),
    ("§ 4 Ausbildungszeit: Die tägliche Ausbildungszeit beträgt 9 Stunden.", 3),
    ("§ 5 Urlaub: Der Urlaubsanspruch beträgt 20 Werktage pro Kalenderjahr.", 4),
    ("§ 6 Kündigung: Während der Probezeit kann das Ausbildungsverhältnis nur mit einer Frist von vier Wochen gekündigt werden.", 5),
    ("§ 7 Pflichten: Die Ausbildungsmittel stellt der Betrieb kostenlos zur Verfügung. Der Auszubildende führt einen Ausbildungsnachweis.", None),
]
FEHLER = {
    1: ("§ 2 Probezeit", "höchstens vier Monate (§ 20 BBiG)"),
    2: ("§ 3 Vergütung", "mindestens 724 € im 1. Jahr (§ 17 BBiG)"),
    3: ("§ 4 Ausbildungszeit", "Jugendliche höchstens 8 Stunden täglich und 40 pro Woche (§ 8 JArbSchG)"),
    4: ("§ 5 Urlaub", "mindestens 24 Werktage, Jugendliche je nach Alter 25 bis 30 (§ 3 BUrlG, § 19 JArbSchG)"),
    5: ("§ 6 Kündigung", "in der Probezeit jederzeit ohne Frist, schriftlich (§ 22 Abs. 1 und 3 BBiG)"),
}
FAELLE_ABC = [f for f in FAELLE if f["id"] in "ABC"]
LEHRKRAFT = "Frau Schorr-Fischer"

# Aufgabenplan Seitenzahlen (Booklet v2, 13 Seiten)
P_AUFG, P_EH, P_QUIZ, P_MERK = 10, 11, 12, 9
