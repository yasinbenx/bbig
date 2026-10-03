# -*- coding: utf-8 -*-
"""Projektablaufplan: Gantt-Diagramm und Netzplan als SVG, Tabelle als HTML."""
import os, sys, datetime as dt
sys.path.insert(0, os.path.dirname(__file__))
from html import escape as esc
from plan import *
from psp_render import wrap, tw, NAVY, NAVY2, ACC, LINE, INK, MUTED, AP_FILL, AP_LINE

RED = "#C62828"
WK = "MDMDFSS"   # Wochentags-Initialen Mo..So

def chip_svg(xr, y, who, px, h=None):
    t = who; fs = px * 0.8
    cw = tw(t, fs, True) + px * 0.8; ch = h or px * 1.1
    return (f'<rect x="{xr-cw:.1f}" y="{y:.1f}" width="{cw:.1f}" height="{ch:.1f}" rx="{ch/2:.1f}" fill="{NAVY}"/>'
            f'<text x="{xr-cw/2:.1f}" y="{y+ch*0.73:.1f}" text-anchor="middle" font-size="{fs:.1f}" font-weight="700" fill="#fff">{esc(t)}</text>'), cw

def gantt(W, H, px=11.5, heute=True, lw=0.33):
    global_H = H
    days = [START + dt.timedelta(i) for i in range((ENDE - START).days + 1)]
    nd = len(days)
    LW = W * lw
    x0 = LW + 8
    dw = (W - 6 - x0) / nd
    top = 18 if heute else 4
    hdr = [17, 15, 16, 12]                    # Monat, KW, Tag, Wochentag
    y_body = top + sum(hdr)
    ms_h = 46
    leg_h = 34
    rh = min((H - y_body - ms_h - leg_h) / len(AP), 46 if len(AP) <= 12 else 38)
    H = y_body + rh * len(AP) + ms_h + leg_h
    dx = lambda d: x0 + (d - START).days * dw
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="Liberation Sans, Arial, sans-serif">']
    chart_bottom = y_body + rh * len(AP)
    # Wochenenden + Zebra
    for d in days:
        if d.weekday() >= 5:
            s.append(f'<rect x="{dx(d):.1f}" y="{top+hdr[0]+hdr[1]}" width="{dw:.1f}" height="{chart_bottom-(top+hdr[0]+hdr[1]):.1f}" fill="#E9ECF3"/>')
    for i in range(len(AP)):
        if i % 2 == 0:
            s.append(f'<rect x="4" y="{y_body+i*rh:.1f}" width="{LW:.1f}" height="{rh:.1f}" fill="#F6F8FC"/>')
    # Kopf: Monate
    def span(a, b, y, h, label, fill, fg, bold=True, fs=px):
        s.append(f'<rect x="{dx(a):.1f}" y="{y}" width="{(b-a).days*dw+dw-1:.1f}" height="{h-1}" fill="{fill}"/>')
        s.append(f'<text x="{dx(a)+((b-a).days*dw+dw)/2:.1f}" y="{y+h*0.72:.1f}" text-anchor="middle" font-size="{fs:.1f}" font-weight="{700 if bold else 400}" fill="{fg}">{esc(label)}</text>')
    span(START, dt.date(2026, 9, 30), top, hdr[0], "September 2026", NAVY, "#fff")
    span(dt.date(2026, 10, 1), ENDE, top, hdr[0], "Oktober 2026", NAVY2, "#fff")
    # KW
    cur = START
    while cur <= ENDE:
        wend = min(ENDE, cur + dt.timedelta(6 - cur.weekday()))
        span(cur, wend, top + hdr[0], hdr[1], f"KW {cur.isocalendar()[1]}", "#CFE0F7", NAVY, True, px * 0.92)
        cur = wend + dt.timedelta(1)
    for d in days:
        wk = d.weekday() >= 5
        s.append(f'<text x="{dx(d)+dw/2:.1f}" y="{top+hdr[0]+hdr[1]+hdr[2]*0.78:.1f}" text-anchor="middle" font-size="{px*0.9:.1f}" font-weight="700" fill="{MUTED if wk else NAVY}">{d.day}</text>')
        s.append(f'<text x="{dx(d)+dw/2:.1f}" y="{top+hdr[0]+hdr[1]+hdr[2]+hdr[3]*0.8:.1f}" text-anchor="middle" font-size="{px*0.78:.1f}" fill="{MUTED}">{WK[d.weekday()]}</text>')
    s.append(f'<text x="8" y="{top+sum(hdr)-4}" font-size="{px:.1f}" font-weight="700" fill="{NAVY}">Arbeitspaket (Soll-Plan)</text>')
    # senkrechte Tagesgitter
    for i in range(nd + 1):
        s.append(f'<line x1="{x0+i*dw:.1f}" y1="{top+hdr[0]+hdr[1]+hdr[2]+hdr[3]}" x2="{x0+i*dw:.1f}" y2="{chart_bottom:.1f}" stroke="#DDE1EA" stroke-width="0.6"/>')
    # Zeilen
    for i, (n, nm, d, pred, who) in enumerate(AP):
        y = y_body + i * rh
        chip, cw = chip_svg(LW - 2, y + rh / 2 - px * 0.55, who, px)
        s.append(chip)
        s.append(f'<text x="8" y="{y+rh/2+px*0.36:.1f}" font-size="{px*0.95:.1f}" font-weight="700" fill="#9A6A00">AP {n}</text>')
        tx = 8 + tw("AP 19", px * 0.95, True) + 6
        avail = LW - 4 - tx - cw - 6
        lines = wrap(nm, px, avail)
        fs = px
        if len(lines) > 1:
            fs = px * 0.88; lines = wrap(nm, fs, avail)
        for k, l in enumerate(lines):
            yy = y + rh / 2 + fs * 0.36 - (len(lines) - 1) * fs * 0.6 + k * fs * 1.2
            s.append(f'<text x="{tx:.1f}" y="{yy:.1f}" font-size="{fs:.1f}" fill="{INK}">{esc(l)}</text>')
        bx = dx(start(n)) + 1.5
        bw = (end(n) - start(n)).days * dw + dw - 3
        bh = rh * 0.6
        s.append(f'<rect x="{bx:.1f}" y="{y+(rh-bh)/2:.1f}" width="{bw:.1f}" height="{bh:.1f}" rx="3.5" fill="{NAVY2}"/>')
        lab = f"{d} AT"
        if tw(lab, px * 0.85, True) + 8 < bw:
            s.append(f'<text x="{bx+bw/2:.1f}" y="{y+rh/2+px*0.3:.1f}" text-anchor="middle" font-size="{px*0.85:.1f}" font-weight="700" fill="#fff">{lab}</text>')
    s.append(f'<line x1="4" y1="{chart_bottom:.1f}" x2="{W-6}" y2="{chart_bottom:.1f}" stroke="{NAVY}" stroke-width="1.2"/>')
    # Meilensteine (Raute) + Hilfslinien
    my = chart_bottom + 17
    s.append(f'<text x="8" y="{my+4:.1f}" font-size="{px:.1f}" font-weight="700" fill="{NAVY}">Meilensteine (Soll)</text>')
    for k, nm, t in MS:
        cx = dx(t) + dw / 2
        s.append(f'<line x1="{cx:.1f}" y1="{y_body}" x2="{cx:.1f}" y2="{my-10:.1f}" stroke="{ACC}" stroke-width="1.2" stroke-dasharray="2 3" opacity="0.9"/>')
        s.append(f'<path d="M{cx:.1f} {my-10:.1f} L{cx+10:.1f} {my:.1f} L{cx:.1f} {my+10:.1f} L{cx-10:.1f} {my:.1f} z" fill="{ACC}" stroke="{NAVY}" stroke-width="1.2"/>')
        s.append(f'<text x="{cx:.1f}" y="{my+px*0.33:.1f}" text-anchor="middle" font-size="{px*0.95:.1f}" font-weight="800" fill="{NAVY}">{k}</text>')
    # Legende der Meilensteine
    lx = 8; ly = my + 30
    for k, nm, t in MS:
        txt = f"M{k} {nm} ({fmt(t)})"
        if lx + 14 + tw(txt, px * 0.88) > W - 8: lx = 8; ly += 16
        s.append(f'<path d="M{lx+5} {ly-9} l5 5 l-5 5 l-5 -5 z" fill="{ACC}" stroke="{NAVY}" stroke-width="1"/>')
        s.append(f'<text x="{lx+14}" y="{ly}" font-size="{px*0.88:.1f}" fill="{INK}">{esc(txt)}</text>')
        lx += 14 + tw(txt, px * 0.88) + 18
    if heute:
        hx = dx(HEUTE) + dw / 2
        s.append(f'<line x1="{hx:.1f}" y1="{top+hdr[0]-2}" x2="{hx:.1f}" y2="{chart_bottom:.1f}" stroke="{RED}" stroke-width="2" stroke-dasharray="6 4"/>')
        lab = "Heute 03.10."
        lw = tw(lab, px * 0.85, True) + 10
        s.append(f'<rect x="{hx-lw/2:.1f}" y="0" width="{lw:.1f}" height="{top-2}" rx="3" fill="{RED}"/><text x="{hx:.1f}" y="{(top-2)*0.76:.1f}" text-anchor="middle" font-size="{px*0.85:.1f}" font-weight="700" fill="#fff">{lab}</text>')
    s.append("</svg>")
    return "\n".join(s)


_POS_OLD = {1: (0, 2), 2: (1, 0), 3: (1, 2), 4: (1, 3), 5: (2, 2), 18: (3, 0), 6: (3, 2), 7: (3, 3), 9: (4, 1), 11: (4, 2), 10: (4, 3),
       8: (5, 1), 12: (5, 2), 13: (5, 3), 14: (5, 4), 16: (6, 1), 17: (6, 2), 15: (6, 3), 19: (7, 2)}
POS = globals().get('POS_NET') or _POS_OLD

def netzplan(W, H, px=10.5, bhmax=86):
    nl, nr = max(l for l, r in POS.values()) + 1, max(r for l, r in POS.values()) + 1
    m = 6
    pitch = (W - 2 * m) / nl
    bw = pitch * 0.78
    gap = pitch - bw
    top = 6
    bh = min(bhmax, (H - 2 * top - 34) / nr * 0.78)
    rp = (H - top - 34 - bh) / (nr - 1)
    X = lambda L: m + L * pitch
    Y = lambda r: top + r * rp
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="Liberation Sans, Arial, sans-serif">',
         f'<defs><marker id="na" markerWidth="8" markerHeight="8" refX="6.5" refY="4" orient="auto" markerUnits="userSpaceOnUse"><path d="M0 0 L8 4 L0 8 z" fill="{LINE}"/></marker></defs>']
    # Kanten
    drawn = set()
    for n, nm, d, pred, who in AP:
        Lt, rt = POS[n]
        xc = X(Lt) - gap / 2 + (rt - 2) * 4.2
        yt = Y(rt) + bh / 2
        for p in pred:
            Ls, rs = POS[p]
            xs = X(Ls) + bw
            ys = Y(rs) + bh / 2
            if abs(ys - yt) < 0.1:
                s.append(f'<path d="M{xs:.1f} {ys:.1f} L{X(Lt)-1:.1f} {yt:.1f}" stroke="{LINE}" stroke-width="1.5" fill="none" marker-end="url(#na)"/>')
            else:
                s.append(f'<path d="M{xs:.1f} {ys:.1f} L{xc:.1f} {ys:.1f} L{xc:.1f} {yt:.1f} L{X(Lt)-1:.1f} {yt:.1f}" stroke="{LINE}" stroke-width="1.5" fill="none" marker-end="url(#na)" stroke-linejoin="round"/>')
    # Knoten
    for n, nm, d, pred, who in AP:
        L, r = POS[n]
        x, y = X(L), Y(r)
        hh = 15
        s.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{bw:.1f}" height="{bh:.1f}" rx="3" fill="{AP_FILL}" stroke="{AP_LINE}" stroke-width="1.6"/>')
        s.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{bw:.1f}" height="{hh}" rx="3" fill="{NAVY}"/><rect x="{x:.1f}" y="{y+hh-4}" width="{bw:.1f}" height="4" fill="{NAVY}"/>')
        s.append(f'<text x="{x+6:.1f}" y="{y+11:.1f}" font-size="{px:.1f}" font-weight="700" fill="{ACC}">AP {n}</text>')
        s.append(f'<text x="{x+bw/2+4:.1f}" y="{y+11:.1f}" text-anchor="middle" font-size="{px*0.95:.1f}" font-weight="700" fill="#fff">{d} AT</text>')
        s.append(f'<text x="{x+bw-6:.1f}" y="{y+11:.1f}" text-anchor="end" font-size="{px*0.95:.1f}" font-weight="700" fill="#fff">{esc(who)}</text>')
        fs = px
        lines = wrap(nm, fs, bw - 12)
        while len(lines) * fs * 1.18 > bh - hh - 18 and fs > 7.5:
            fs -= 0.25; lines = wrap(nm, fs, bw - 12)
        area_top, area_h = y + hh, bh - hh - 15
        y0 = area_top + area_h / 2 - (len(lines) - 1) * fs * 0.59 + fs * 0.35
        for k, l in enumerate(lines):
            s.append(f'<text x="{x+bw/2:.1f}" y="{y0+k*fs*1.18:.1f}" text-anchor="middle" font-size="{fs:.1f}" fill="{INK}">{esc(l)}</text>')
        s.append(f'<line x1="{x:.1f}" y1="{y+bh-15:.1f}" x2="{x+bw:.1f}" y2="{y+bh-15:.1f}" stroke="{AP_LINE}" stroke-width="1"/>')
        s.append(f'<text x="{x+6:.1f}" y="{y+bh-4.5:.1f}" font-size="{px*0.95:.1f}" font-weight="700" fill="{NAVY}">{fmt(start(n))}</text>')
        s.append(f'<text x="{x+bw-6:.1f}" y="{y+bh-4.5:.1f}" text-anchor="end" font-size="{px*0.95:.1f}" font-weight="700" fill="{NAVY}">{fmt(end(n))}</text>')
    # Legende
    s.append(f'<text x="{m}" y="{H-19}" font-size="{px:.1f}" fill="{MUTED}">Kästchen: oben Nummer · Dauer in Arbeitstagen (AT) · Verantwortliche (Y = Yasin, M = Mido, Y+M = beide) | Mitte Bezeichnung | unten Start und Ende (Soll).</text>')
    s.append(f'<text x="{m}" y="{H-6}" font-size="{px:.1f}" fill="{MUTED}">Pfeile zeigen Abhängigkeiten: Der Nachfolger beginnt am nächsten Arbeitstag nach dem Vorgänger. Parallele Arbeitspakete stehen untereinander.</text>')
    s.append("</svg>")
    return "\n".join(s)


def table_html():
    rows = ""
    for n, nm, d, pred, who in AP:
        rows += (f'<tr><td class="c b">{n}</td><td>{esc(nm)}</td><td class="c">{d}</td><td class="c">{fmt(start(n), True)}</td><td class="c">{fmt(end(n), True)}</td>'
                 f'<td class="c">{", ".join(map(str, pred)) or "–"}</td><td class="c">{esc(OWNER_LONG[who])}</td><td class="c ist">[eintragen]</td></tr>')
    return ('<table class="pt"><tr><th class="c">Nr.</th><th>Arbeitspaket</th><th class="c">Dauer<br><span>(Arbeitstage)</span></th><th class="c">Start<br><span>(Soll)</span></th><th class="c">Ende<br><span>(Soll)</span></th>'
            '<th class="c">Vorgänger</th><th class="c">Verantwortlich</th><th class="c">Ist</th></tr>' + rows + '</table>')

if __name__ == "__main__":
    open("/tmp/g.svg", "w").write(gantt(1070, 600))
    open("/tmp/n.svg", "w").write(netzplan(1070, 600))
