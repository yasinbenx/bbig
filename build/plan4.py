# -*- coding: utf-8 -*-
"""Projektplanung v4: 5 Teilaufgaben, Arbeitspakete 1.1 ... 5.3, Soll-Termine (Mo-Fr, 10.09.-08.10.2026)."""
import datetime as dt
TITEL = "Rechte und Pflichten aus dem Ausbildungsvertrag"
UNTERTITEL = "Booklet und interaktive Unterrichtsstunde zur Prüfungsvorbereitung im Fach GP"
START, ENDE = dt.date(2026, 9, 10), dt.date(2026, 10, 8)
WORKDAYS = [START + dt.timedelta(d) for d in range((ENDE - START).days + 1) if (START + dt.timedelta(d)).weekday() < 5]
assert len(WORKDAYS) == 21
OWNER = {"Y": "Yasin", "M": "Mido", "YM": "Yasin & Mido"}
TA = {1: "Projektmanagement und Planung", 2: "Recherche", 3: "Booklet", 4: "Präsentation und Unterrichtsstunde (inkl. Website)", 5: "Abschluss und Evaluation"}
# (Nr, Name, Dauer AT, Vorgaenger, Verantwortlich, frueheste Startdatum oder None)
AP = [
 ("1.1", "Projektskizze und SMART-Ziele erstellen", 3, [], "YM", None),
 ("1.2", "Projektstrukturplan erstellen", 2, ["1.1"], "M", None),
 ("1.3", "Projektablaufplan erstellen", 2, ["1.2"], "M", None),
 ("2.1", "Gesetzliche Grundlagen recherchieren (BBiG, JArbSchG, BUrlG, ArbZG)", 4, ["1.1"], "Y", None),
 ("2.2", "Prüfungsrelevante Inhalte und Fallbeispiele auswählen", 2, ["2.1", "1.3"], "M", None),
 ("2.3", "Quellen und Zahlen prüfen (Stand Oktober 2026)", 2, ["2.2"], "YM", None),
 ("3.1", "Erklär-Themen schreiben", 3, ["2.3"], "Y", None),
 ("3.2", "Aufgaben mit Erwartungshorizont erstellen", 3, ["2.3"], "M", None),
 ("3.3", "Layout, Merkblatt und Korrekturlesen", 2, ["3.1", "3.2"], "M", None),
 ("4.1", "Unterrichtsstunde planen und Folien erstellen", 3, ["3.1", "3.2"], "Y", None),
 ("4.2", "Interaktive Website mit QR-Code", 2, ["3.2"], "M", dt.date(2026, 10, 2)),
 ("4.3", "Sprechskript schreiben", 2, ["4.1"], "Y", None),
 ("5.1", "Probelauf und Material prüfen", 1, ["3.3", "4.2", "4.3"], "YM", None),
 ("5.2", "Präsentation halten", 1, ["5.1"], "YM", None),
 ("5.3", "Evaluation, Reflexion und Projektbericht", None, ["5.2"], "YM", None),   # nach 08.10., Termin laut Lehrkraft
]
NAME = {n: nm for n, nm, *_ in AP}; DUR = {n: d for n, _, d, *_ in AP}; PRED = {n: p for n, _, _, p, *_ in AP}; WHO = {n: w for n, _, _, _, w, _ in AP}
wd_idx = lambda d: next(i for i, x in enumerate(WORKDAYS) if x >= d)
ES, EF = {}, {}
for n, nm, d, pred, who, sn in AP:
    if d is None: continue
    ES[n] = max([EF[p] + 1 for p in pred if p in EF] + ([wd_idx(sn)] if sn else []), default=0); EF[n] = ES[n] + d - 1
assert max(EF.values()) == 20
start = lambda n: WORKDAYS[ES[n]]; end = lambda n: WORKDAYS[EF[n]]
fmt = lambda d, y=False: d.strftime("%d.%m.%Y" if y else "%d.%m.")
# Spaetester Termin (Rueckwaertsrechnung) und Puffer
succ = {n: [m for m, _, _, pr, *_ in AP if n in pr and m in EF] for n in EF}
LS, LF = {}, {}
for n in reversed(list(EF)):
    LF[n] = min([LS[m] - 1 for m in succ[n]], default=20); LS[n] = LF[n] - DUR[n] + 1
SLACK = {n: LS[n] - ES[n] for n in EF}
CRIT = [n for n in EF if SLACK[n] == 0]
MS = [("M1", "Themenfreigabe (Projektskizze liegt vor)", end("1.1")), ("M2", "Recherche abgeschlossen", end("2.3")), ("M3", "Booklet fertig", end("3.3")),
      ("M4", "Präsentation fertig (Folien und Sprechskript)", max(end("4.1"), end("4.2"), end("4.3"))), ("M5", "Probelauf", end("5.1")), ("M6", "Präsentation am 08.10.2026", end("5.2"))]
assert MS[-1][2] == ENDE
def teil(n): return int(n.split(".")[0])
def weekrange(a, b): return sorted(n for n in EF if start(n) <= b and end(n) >= a)
WOCHEN = [("Woche 1", dt.date(2026, 9, 10), dt.date(2026, 9, 16)), ("Woche 2", dt.date(2026, 9, 17), dt.date(2026, 9, 23)), ("Woche 3", dt.date(2026, 9, 24), dt.date(2026, 9, 30)), ("Woche 4", dt.date(2026, 10, 1), dt.date(2026, 10, 8))]
def pred_txt(n): return ", ".join(PRED[n]) if PRED[n] else "–"
def dur_txt(n): return str(DUR[n]) if DUR[n] else "–"
def start_txt(n): return fmt(start(n), True) if n in ES else "nach 08.10.2026"
def end_txt(n): return fmt(end(n), True) if n in EF else "[laut Lehrkraft]"
if __name__ == "__main__":
    for n, nm, d, *_ in AP: print(n, nm[:48].ljust(48), dur_txt(n), start_txt(n), end_txt(n), pred_txt(n), OWNER[WHO[n]], SLACK.get(n))
    for m in MS: print(m[0], m[1], fmt(m[2], True))
    for w, a, b in WOCEN if False else WOCHEN: print(w, weekrange(a, b))
    # Ressourcencheck: keine Ueberlast pro Person
    for p in "YM":
        for i in range(21):
            act = [n for n in EF if ES[n] <= i <= EF[n] and p in WHO[n]]
            if len(act) > 1: print("Ueberlast", p, WORKDAYS[i], act)
