# -*- coding: utf-8 -*-
"""Projektplanung v2 (schlank, 10 Arbeitspakete). Gleiche Schnittstelle wie plan.py.
Soll-Termine werden aus Dauer, Vorgaengern und fruehestem Start (SNET) berechnet. Keine Ist-Daten."""
import datetime as dt

START = dt.date(2026, 9, 10)
ENDE = dt.date(2026, 10, 8)
HEUTE = dt.date(2026, 10, 3)
OKT = dt.date(2026, 10, 1)       # Umsetzung im Oktober

WORKDAYS = [START + dt.timedelta(d) for d in range((ENDE - START).days + 1) if (START + dt.timedelta(d)).weekday() < 5]

# (nr, name, dauer_AT, vorgaenger, verantwortlich, fruehester Start oder None)
AP = [
    (1, "Projektskizze und Ziele erstellen", 5, [], "Y+M", None),
    (2, "Projektstrukturplan erstellen", 4, [1], "Y+M", None),
    (3, "Projektablaufplan erstellen", 4, [2], "Y+M", None),
    (4, "Praxisbeispiele sammeln und anonymisieren", 8, [1], "M", None),
    (5, "Booklet mit Kapiteln, Merkblatt und Mini-Quiz erstellen", 4, [3, 4], "Y+M", OKT),
    (6, "Aufgaben mit Erwartungshorizont erstellen", 2, [3, 4], "Y+M", OKT),
    (7, "Präsentation erstellen", 2, [6], "Y+M", None),
    (8, "Material, Korrekturlesen und Probelauf", 1, [5, 7], "Y+M", None),
    (9, "Projektbericht schreiben", 5, [3], "Y+M", OKT),
    (10, "Präsentation halten (08.10.)", 1, [8, 9], "Y+M", None),
]
AP4 = [(n, nm, d, pr, w) for n, nm, d, pr, w, _ in AP]     # kompatibel zu plan.py
NAME = {n: nm for n, nm, *_ in AP}
SNET = {n: s for n, _, _, _, _, s in AP}
_wd_index = lambda d: next(i for i, x in enumerate(WORKDAYS) if x >= d)

def _topo():
    done, order = set(), []
    while len(order) < len(AP):
        for row in AP:
            if row[0] not in done and all(p in done for p in row[3]):
                done.add(row[0]); order.append(row)
    return order
TOPO = _topo()
ES, EF = {}, {}
for n, nm, d, pred, who, sn in TOPO:
    s = max([EF[p] + 1 for p in pred] + ([_wd_index(sn)] if sn else []), default=0)
    ES[n], EF[n] = s, s + d - 1
LAST = max(EF.values())
assert LAST == len(WORKDAYS) - 1, (LAST, len(WORKDAYS))
succ = {n: [m for m, _, _, pr, _, _ in AP if n in pr] for n, *_ in AP}
LS, LF = {}, {}
for n, nm, d, pred, who, sn in reversed(TOPO):
    LF[n] = min([LS[m] - 1 for m in succ[n]], default=LAST); LS[n] = LF[n] - d + 1
SLACK = {n: LS[n] - ES[n] for n in ES}
CRIT = {n for n in SLACK if SLACK[n] == 0}

def start(n): return WORKDAYS[ES[n]]
def end(n): return WORKDAYS[EF[n]]
def fmt(d, year=False): return d.strftime("%d.%m.%Y" if year else "%d.%m.")

AP_PUBLIC = AP4
AP = AP4        # die Zeichner erwarten (nr, name, dauer, vorgaenger, wer)

MS_DEF = [
    (1, "Projektskizze und Ziele fertig", [1]),
    (2, "Planung und Praxisbeispiele fertig", [3, 4]),
    (3, "Booklet und Aufgaben fertig", [5, 6]),
    (4, "Präsentation und Material fertig", [8]),
    (5, "Präsentation gehalten", [10]),
]
MS = [(k, nm, max(end(a) for a in aps)) for k, nm, aps in MS_DEF]

PSP = dict(
    root="Booklet-Projekt",
    children=[
        dict(t="Vorbereitung", aps=[1], sub=dict(t="Planung", aps=[2, 3])),
        dict(ap=4),
        dict(t="Booklet und Aufgaben", aps=[5, 6]),
        dict(t="Präsentation und Abschluss", aps=[7, 8, 9, 10]),
    ],
)
OWNER_LONG = {"Y": "Yasin", "M": "Mido", "Y+M": "Yasin & Mido"}

# Netzplan-Positionen (Ebene, Zeile): AP5, AP6, AP9 laufen parallel
POS_NET = {1: (0, 1), 2: (1, 0), 4: (1, 2), 3: (2, 0), 9: (3, 0), 5: (3, 1), 6: (3, 2), 7: (4, 2), 8: (5, 1), 10: (6, 1)}

if __name__ == "__main__":
    for n, nm, d, pred, who in AP:
        print(f"{n:2} {nm:56} {d:2}AT {fmt(start(n))}-{fmt(end(n))} pred={pred} {who:3} slack={SLACK[n]}")
    for k, nm, t in MS: print("M", k, nm, fmt(t, True))
