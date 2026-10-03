# -*- coding: utf-8 -*-
"""Projektplanung: Arbeitspakete, Soll-Termine (Vorwaerts-/Rueckwaertsrechnung), Meilensteine.
Alle Soll-Termine werden aus Dauer und Vorgaengern berechnet. Ist-Daten gibt es bewusst nicht."""
import datetime as dt

START = dt.date(2026, 9, 10)
ENDE = dt.date(2026, 10, 8)
HEUTE = dt.date(2026, 10, 3)

# Arbeitstage (Mo-Fr) von START bis ENDE
WORKDAYS = [START + dt.timedelta(d) for d in range((ENDE - START).days + 1) if (START + dt.timedelta(d)).weekday() < 5]

# Y = Yasin, M = Mido, J = beide ("Y+M")
# (nr, name, dauer_AT, vorgaenger, verantwortlich)
AP = [
    (1, "Problemanalyse & Zielsetzung", 1, [], "Y+M"),
    (2, "Projektplanung erstellen", 2, [1], "Y+M"),
    (3, "BBiG & Berufsausbildungsvertrag recherchieren", 3, [1], "Y"),
    (4, "Eigenen Vertrag sichten & anonymisieren", 2, [1], "M"),
    (5, "Gliederung erstellen", 3, [3, 4], "Y+M"),
    (6, "Texte verfassen", 5, [5], "Y"),
    (7, "Praxisbeispiele & Grafiken erarbeiten", 4, [4, 5], "M"),
    (8, "Layout umsetzen", 4, [9, 10, 11], "Y+M"),
    (9, "Merkblatt erstellen", 2, [6], "Y"),
    (10, "Aufgaben & Erwartungshorizont erstellen", 3, [7], "M"),
    (11, "Quizfragen erstellen", 2, [6, 7], "Y+M"),
    (12, "Präsentation erstellen", 4, [10, 11], "Y+M"),
    (13, "Quiz als HTML-Datei erstellen", 3, [10, 11], "Y+M"),
    (14, "Druckmaterial erstellen", 2, [10], "Y+M"),
    (15, "Generalprobe (45 Minuten)", 1, [12, 13, 14], "Y+M"),
    (16, "Fachlicher Abgleich mit dem BBiG", 1, [8], "M"),
    (17, "Korrekturlesen & Probelesen", 2, [8], "M"),
    (18, "Projektbericht schreiben", 13, [2, 5], "Y+M"),
    (19, "Abgabe & Präsentation (08.10.)", 1, [15, 17, 18], "Y+M"),
]
NAME = {n: nm for n, nm, *_ in AP}

# Meilensteine: (Nr, Name, Termin = Ende der genannten Arbeitspakete)
MS_DEF = [
    (1, "Recherche abgeschlossen", [3, 4]),
    (2, "Gliederung steht", [5]),
    (3, "Texte und Beispiele fertig", [6, 7, 9, 10, 11]),
    (4, "Booklet fertig und geprüft", [16, 17]),
    (5, "Präsentation", [19]),
]

# ---- Vorwaertsrechnung (Finish-Start: Nachfolger beginnt am naechsten Arbeitstag)
def topo():
    done, order = set(), []
    while len(order) < len(AP):
        for row in AP:
            if row[0] not in done and all(p in done for p in row[3]):
                done.add(row[0]); order.append(row)
    return order
TOPO = topo()
ES, EF = {}, {}
for n, nm, d, pred, who in TOPO:
    s = max([EF[p] + 1 for p in pred], default=0)
    ES[n], EF[n] = s, s + d - 1
LAST = max(EF.values())
assert LAST == len(WORKDAYS) - 1, (LAST, len(WORKDAYS))

# ---- Rueckwaertsrechnung (kritischer Weg)
LF, LS = {}, {}
succ = {n: [m for m, _, _, pr, _ in AP if n in pr] for n, *_ in AP}
for n, nm, d, pred, who in reversed(TOPO):
    LF[n] = min([LS[m] - 1 for m in succ[n]], default=LAST)
    LS[n] = LF[n] - d + 1
SLACK = {n: LS[n] - ES[n] for n in ES}
CRIT = {n for n in SLACK if SLACK[n] == 0}

def start(n): return WORKDAYS[ES[n]]
def end(n): return WORKDAYS[EF[n]]
def fmt(d, year=False): return d.strftime("%d.%m.%Y" if year else "%d.%m.")
MS = [(k, nm, max(end(a) for a in aps)) for k, nm, aps in MS_DEF]

# ---- Projektstrukturplan (Baum): Teilaufgaben, verschachtelt moeglich
PSP = dict(
    root="Booklet-Projekt Ausbildungsvertrag",
    children=[
        dict(t="Planung", aps=[1, 2]),
        dict(t="Recherche & Konzeption", aps=[3, 4, 5]),
        dict(t="Booklet", aps=[6, 7, 8], sub=dict(t="Übungsteil", aps=[9, 10, 11])),
        dict(t="Präsentation & Praxisteil", aps=[12, 13, 14, 15]),
        dict(t="Qualitätssicherung", aps=[16, 17]),
        dict(ap=18),
        dict(ap=19),
    ],
)
OWNER_LONG = {"Y": "Yasin", "M": "Mido", "Y+M": "Yasin & Mido"}

if __name__ == "__main__":
    print("Arbeitstage:", len(WORKDAYS), fmt(WORKDAYS[0]), "-", fmt(WORKDAYS[-1]))
    for n, nm, d, pred, who in AP:
        print(f"{n:2} {nm:48} {d:2}AT {fmt(start(n))}-{fmt(end(n))} pred={pred} {who:3} slack={SLACK[n]} {'KRIT' if n in CRIT else ''}")
    for k, nm, t in MS: print("M", k, nm, fmt(t, True))
    assert sorted(a for c in PSP["children"] for a in ([c["ap"]] if "ap" in c else c["aps"] + (c["sub"]["aps"] if "sub" in c else []))) == list(range(1, 20))
