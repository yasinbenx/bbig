# -*- coding: utf-8 -*-
"""Projektstrukturplan als SVG (Baum: Wurzel, Teilaufgaben, Arbeitspakete, rechtwinklige Linien mit Pfeilen)."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from html import escape as esc
from PIL import ImageFont
from plan import *

NAVY, NAVY2, ACC = "#14264B", "#22386B", "#F5A800"
LINE = "#8E97AC"
TA_FILL, TA_LINE = "#CFE0F7", "#22386B"
AP_FILL, AP_LINE = "#FFF3C4", "#F5A800"
FR = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
FB = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
_fc = {}
def font(bold, px):
    k = (bold, round(px * 4))
    if k not in _fc: _fc[k] = ImageFont.truetype(FB if bold else FR, int(round(px * 4)))
    return _fc[k]
def tw(t, px, bold=False): return font(bold, px).getlength(t) / 4

HY = {"Berufsausbildungsvertrag": ["Berufs-", "ausbildungs-", "vertrag"], "Erwartungshorizont": ["Erwartungs-", "horizont"],
      "Qualitätssicherung": ["Qualitäts-", "sicherung"], "Problemanalyse": ["Problem-", "analyse"],
      "Praxisbeispiele": ["Praxis-", "beispiele"], "Projektbericht": ["Projekt-", "bericht"], "Projektplanung": ["Projekt-", "planung"],
      "Übungsteil": ["Übungs-", "teil"], "Generalprobe": ["General-", "probe"], "Korrekturlesen": ["Korrektur-", "lesen"],
      "Booklet-Projekt": ["Booklet-", "Projekt"], "Ausbildungsvertrag": ["Ausbildungs-", "vertrag"], "Präsentation": ["Präsen-", "tation"],
      "Druckmaterial": ["Druck-", "material"], "Abgleich": ["Ab-", "gleich"]}

def wrap(text, px, maxw, bold=False):
    toks = []                         # (text, glue_to_previous)
    for w in text.split(" "):
        if tw(w, px, bold) > maxw and w in HY:
            parts = HY[w]
            toks += [(parts[0], False)] + [(p, True) for p in parts[1:]]
        else:
            toks.append((w, False))
    lines, cur = [], ""
    for t, glue in toks:
        cand = cur + t if glue else (cur + " " + t).strip()
        if tw(cand, px, bold) <= maxw or not cur: cur = cand
        else: lines.append(cur); cur = t
    lines.append(cur)
    assert all(tw(l, px, bold) <= maxw + 0.5 for l in lines), ("Wort zu breit", lines, maxw)
    return lines

def chip(x, y, who, px):
    """kleines Kuerzel (Y / M / Y+M) mit rechter oberer Ecke bei x,y"""
    w = {"Y": 0.0, "M": 0.0, "Y+M": 0.0}
    t = who
    cw = tw(t, px * 0.82, True) + px * 0.9
    ch = px * 1.15
    return (f'<rect x="{x-cw:.1f}" y="{y:.1f}" width="{cw:.1f}" height="{ch:.1f}" rx="{ch/2:.1f}" fill="{NAVY}"/>'
            f'<text x="{x-cw/2:.1f}" y="{y+ch*0.74:.1f}" text-anchor="middle" font-size="{px*0.82:.1f}" font-weight="700" fill="#fff">{esc(t)}</text>')

def build(W, H, top=10, px=12.5, bottom=34, title_band=0):
    """liefert (svg, ok)"""
    mx, g = 26, 14
    weights = [0.95, 1.3, 1.55, 1.25, 1.0, 0.95, 0.95]
    avail = W - 2 * mx - 6 * g
    cw = [avail * w / sum(weights) for w in weights]
    cx = [mx + sum(cw[:i]) + g * i for i in range(7)]
    lh = px * 1.2
    ind1, ind2 = 24, 52
    def ap_box(n, x, w, y):
        lines = wrap(NAME[n], px, w - 14)
        h = 8 + px * 1.25 + len(lines) * lh + 5
        return dict(n=n, x=x, y=y, w=w, h=h, lines=lines)
    out, boxes = [], []
    # Wurzel
    rw, rh = min(330, W * 0.3), px * 2.9
    rx = (W - rw) / 2
    ry = top
    root_lines = wrap(PSP["root"], px * 1.15, rw - 20, True)
    bus_y = ry + rh + 22
    yc = bus_y + 22
    taH = px * 3.0
    items = []   # (draw ops)
    ops = []
    arrow = lambda x1, y1, x2, y2: f'<path d="M{x1:.1f} {y1:.1f} L{x2:.1f} {y2:.1f}" stroke="{LINE}" stroke-width="1.7" fill="none" marker-end="url(#ar)"/>'
    pline = lambda pts: f'<path d="M{pts}" stroke="{LINE}" stroke-width="1.7" fill="none"/>'
    maxy = 0
    centers = []
    for i, c in enumerate(PSP["children"]):
        x, w = cx[i], cw[i]
        centers.append(x + w / 2)
        if "ap" in c:      # direkt angehaengtes Arbeitspaket
            b = ap_box(c["ap"], x, w, yc)
            b["h"] = max(b["h"], taH)
            boxes.append(("ap", b)); maxy = max(maxy, b["y"] + b["h"])
            continue
        tl = wrap(c["t"], px * 1.1, w - 14, True)
        ops.append(("ta", dict(x=x, y=yc, w=w, h=taH, lines=tl, big=True)))
        xl = x + 12
        y = yc + taH + 14
        stack_end = yc + taH
        for n in c["aps"]:
            b = ap_box(n, x + ind1, w - ind1, y)
            ops.append(("line_to", (xl, b["y"] + b["h"] / 2, b["x"])))
            boxes.append(("ap", b)); y += b["h"] + 9; stack_end = b["y"] + b["h"] / 2
        ops.append(("vline", (xl, yc + taH, stack_end)))
        if "sub" in c:
            sub = c["sub"]
            sx, sw = x + ind1, w - ind1
            stl = wrap(sub["t"], px * 1.05, sw - 14, True)
            sh = px * 2.4
            ops.append(("ta", dict(x=sx, y=y, w=sw, h=sh, lines=stl, big=False)))
            ops.append(("line_to", (xl, y + sh / 2, sx)))
            stack_end = y + sh / 2
            ops.append(("vline", (xl, yc + taH, stack_end)))   # Hauptlinie bis zur Unteraufgabe
            xl2 = sx + 14
            y2 = y + sh + 14
            se2 = y + sh
            for n in sub["aps"]:
                b = ap_box(n, x + ind2, w - ind2, y2)
                ops.append(("line_to", (xl2, b["y"] + b["h"] / 2, b["x"])))
                boxes.append(("ap", b)); y2 += b["h"] + 9; se2 = b["y"] + b["h"] / 2
            ops.append(("vline", (xl2, y + sh, se2)))
            y = y2
        maxy = max(maxy, y - 9)
    ok = maxy <= H - bottom
    # ---------- SVG zusammensetzen
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="Liberation Sans, Arial, sans-serif">',
         f'<defs><marker id="ar" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto" markerUnits="userSpaceOnUse"><path d="M0 0 L9 4.5 L0 9 z" fill="{LINE}"/></marker></defs>']
    # Wurzel + Bus
    s.append(f'<rect x="{rx:.1f}" y="{ry}" width="{rw:.1f}" height="{rh:.1f}" rx="3" fill="{NAVY}"/>')
    ly0 = ry + rh / 2 - (len(root_lines) - 1) * lh * 0.55 + px * 0.38
    for k, l in enumerate(root_lines):
        s.append(f'<text x="{W/2:.1f}" y="{ly0 + k * lh * 1.1:.1f}" text-anchor="middle" font-size="{px*1.15:.1f}" font-weight="700" fill="#fff">{esc(l)}</text>')
    s.append(pline(f"{W/2:.1f} {ry+rh:.1f} L{W/2:.1f} {bus_y}"))
    s.append(pline(f"{min(centers):.1f} {bus_y} L{max(centers):.1f} {bus_y}"))
    for cxm in centers: s.append(arrow(cxm, bus_y, cxm, yc - 1))
    for kind, d in ops:
        if kind == "vline": s.append(pline(f"{d[0]:.1f} {d[1]:.1f} L{d[0]:.1f} {d[2]:.1f}"))
        elif kind == "line_to": s.append(arrow(d[0], d[1], d[2] - 1, d[1]))
    for kind, d in ops:
        if kind == "ta":
            s.append(f'<rect x="{d["x"]:.1f}" y="{d["y"]:.1f}" width="{d["w"]:.1f}" height="{d["h"]:.1f}" rx="3" fill="{TA_FILL}" stroke="{TA_LINE}" stroke-width="1.4"/>')
            fs = px * (1.1 if d["big"] else 1.05)
            y0 = d["y"] + d["h"] / 2 - (len(d["lines"]) - 1) * lh * 0.55 + fs * 0.36
            for k, l in enumerate(d["lines"]):
                s.append(f'<text x="{d["x"]+d["w"]/2:.1f}" y="{y0 + k * lh * 1.1:.1f}" text-anchor="middle" font-size="{fs:.1f}" font-weight="700" fill="{NAVY}">{esc(l)}</text>')
    for _, b in boxes:
        who = next(w for n, nm, d, pr, w in AP if n == b["n"])
        s.append(f'<rect x="{b["x"]:.1f}" y="{b["y"]:.1f}" width="{b["w"]:.1f}" height="{b["h"]:.1f}" rx="3" fill="{AP_FILL}" stroke="{AP_LINE}" stroke-width="1.6"/>')
        s.append(f'<text x="{b["x"]+7:.1f}" y="{b["y"]+px*1.05+3:.1f}" font-size="{px*0.9:.1f}" font-weight="700" fill="#9A6A00">AP {b["n"]}</text>')
        s.append(chip(b["x"] + b["w"] - 5, b["y"] + 4, who, px * 0.9))
        for k, l in enumerate(b["lines"]):
            s.append(f'<text x="{b["x"]+7:.1f}" y="{b["y"]+px*1.25+8+px*0.9+k*lh:.1f}" font-size="{px:.1f}" fill="{INK}">{esc(l)}</text>')
    # Legende
    ly = H - 14
    lx = mx
    s.append(f'<rect x="{lx}" y="{ly-11}" width="16" height="11" rx="2" fill="{TA_FILL}" stroke="{TA_LINE}" stroke-width="1.2"/><text x="{lx+22}" y="{ly}" font-size="{px*0.95:.1f}" fill="{MUTED}">Teilaufgabe</text>')
    lx += 22 + tw("Teilaufgabe", px * 0.95) + 22
    s.append(f'<rect x="{lx}" y="{ly-11}" width="16" height="11" rx="2" fill="{AP_FILL}" stroke="{AP_LINE}" stroke-width="1.4"/><text x="{lx+22}" y="{ly}" font-size="{px*0.95:.1f}" fill="{MUTED}">Arbeitspaket (AP)</text>')
    lx += 22 + tw("Arbeitspaket (AP)", px * 0.95) + 26
    s.append(f'<text x="{lx}" y="{ly}" font-size="{px*0.95:.1f}" fill="{MUTED}">Verantwortlich: Y = Yasin · M = Mido · Y+M = beide gemeinsam</text>')
    s.append("</svg>")
    return "\n".join(s), ok, maxy

INK, MUTED = "#1A2238", "#5B6680"

def fit(W, H, top=10, start_px=14.0, bottom=34):
    px = start_px
    while px > 8:
        try:
            svg, ok, my = build(W, H, top, px, bottom)
        except AssertionError:
            px -= 0.25; continue
        if ok: return svg, px, my
        px -= 0.25
    raise RuntimeError("PSP passt nicht")

if __name__ == "__main__":
    svg, px, my = fit(1075, 590, 8, 13.5, 30)
    print("px", px, "maxy", my)
    open("/tmp/psp_test.svg", "w").write(svg)
