# -*- coding: utf-8 -*-
"""Gemeinsames Design (CSS, Icons, Bausteine) fuer Booklet, Merkblatt und Druckmaterial."""
from html import escape as esc

NAVY = "#14264B"
NAVY2 = "#22386B"
ACCENT = "#F5A800"
ACCENT_L = "#FFF1CC"
BLUE_L = "#E8EEF9"
RED = "#B3261E"
RED_L = "#FCE9E7"
GREY_L = "#EDEFF4"
INK = "#1A2238"
MUTED = "#5B6680"

CSS = f"""
@page {{ size: A4; margin: 0; }}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
html {{ -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
body {{ font-family: 'Liberation Sans', Arial, Helvetica, sans-serif; color: {INK}; font-size: 12.5pt; line-height: 1.5; background: #fff; }}
a {{ color: {NAVY2}; }}
.page {{ width: 210mm; height: 297mm; position: relative; overflow: hidden; page-break-after: always; break-after: page; display: flex; flex-direction: column; background: #fff; }}
.page:last-child {{ page-break-after: auto; break-after: auto; }}
.head {{ background: {NAVY}; color: #fff; padding: 13mm 18mm 8mm 24mm; position: relative; flex: none; }}
.head::before {{ content: ''; position: absolute; left: 0; top: 0; bottom: 0; width: 6mm; background: {ACCENT}; }}
.kicker {{ color: {ACCENT}; font-size: 9.5pt; font-weight: 700; letter-spacing: .12em; text-transform: uppercase; }}
.head h1 {{ font-size: 23pt; line-height: 1.15; margin-top: 1.5mm; font-weight: 700; }}
.body {{ flex: 1; min-height: 0; overflow: hidden; padding: 11mm 18mm 0 24mm; }}
.foot {{ position: absolute; left: 24mm; right: 18mm; bottom: 8mm; display: flex; justify-content: space-between; font-size: 8.5pt; color: {MUTED}; border-top: 0.3mm solid #D5D9E3; padding-top: 2mm; }}
p {{ margin-bottom: 3.5mm; }}
.lead {{ font-size: 14pt; line-height: 1.55; }}
h2 {{ font-size: 13pt; color: {NAVY}; margin: 5mm 0 2.5mm; }}
.merk {{ background: {ACCENT_L}; border-left: 2mm solid {ACCENT}; border-radius: 0 2mm 2mm 0; padding: 4.5mm 6mm; margin: 5mm 0; }}
.merk .lbl, .info .lbl, .warn .lbl {{ font-size: 8.5pt; font-weight: 700; letter-spacing: .1em; text-transform: uppercase; color: #9A6A00; display: block; margin-bottom: 1mm; }}
.merk .txt {{ font-size: 13.5pt; font-weight: 700; color: {NAVY}; line-height: 1.4; }}
.merk.big .txt {{ font-size: 18pt; line-height: 1.35; }}
.info {{ background: {BLUE_L}; border-left: 2mm solid {NAVY2}; border-radius: 0 2mm 2mm 0; padding: 4.5mm 6mm; margin: 5mm 0; }}
.info .lbl {{ color: {NAVY2}; }}
.warn {{ background: {RED_L}; border-left: 2mm solid {RED}; border-radius: 0 2mm 2mm 0; padding: 4.5mm 6mm; margin: 5mm 0; }}
.warn .lbl {{ color: {RED}; }}
.warn .txt {{ font-weight: 700; color: #7A1812; font-size: 12.5pt; }}
.note {{ font-size: 9pt; color: {MUTED}; }}
table.t {{ width: 100%; border-collapse: collapse; font-size: 10.5pt; }}
table.t th {{ background: {NAVY}; color: #fff; text-align: left; padding: 2.4mm 3mm; font-size: 10pt; }}
table.t td {{ padding: 2.4mm 3mm; border-bottom: 0.3mm solid #D5D9E3; vertical-align: top; }}
table.t tr:nth-child(even) td {{ background: #F6F8FC; }}
table.t td.b {{ font-weight: 700; color: {NAVY}; }}
ul.l {{ margin: 0 0 3mm 5mm; }} ul.l li {{ margin-bottom: 1.5mm; }}
.two {{ display: grid; grid-template-columns: 1fr 1fr; gap: 6mm; }}
.col {{ border: 0.4mm solid #D5D9E3; border-radius: 2.5mm; overflow: hidden; background: #fff; }}
.col .ch {{ background: {NAVY}; color: #fff; padding: 3mm 5mm; font-weight: 700; font-size: 12pt; }}
.col .ch.acc {{ background: {ACCENT}; color: {NAVY}; }}
.col .cb {{ padding: 4mm 5mm; }}
.card {{ border: 0.4mm solid #D5D9E3; border-left: 2mm solid {NAVY}; border-radius: 0 2.5mm 2.5mm 0; padding: 4mm 5mm; margin-bottom: 5mm; background: #fff; }}
.card h3 {{ font-size: 12pt; color: {NAVY}; margin-bottom: 1.5mm; }}
.card h3 span {{ color: {ACCENT}; background: {NAVY}; border-radius: 1.2mm; padding: 0.4mm 2mm; margin-right: 2mm; font-size: 11pt; }}
.ans {{ display: flex; align-items: flex-start; gap: 3mm; border: 0.35mm solid #BFC6D6; border-radius: 1.8mm; padding: 1.8mm 3mm; margin-top: 1.8mm; font-size: 11pt; }}
.ans b {{ flex: none; width: 6.2mm; height: 6.2mm; border-radius: 50%; border: 0.4mm solid {NAVY}; color: {NAVY}; text-align: center; line-height: 5.6mm; font-size: 10pt; }}
.sol {{ background: {GREY_L}; color: #4A5368; border-radius: 1.8mm; padding: 1.6mm 3.5mm; margin-top: 2mm; font-size: 10pt; }}
.sol b {{ color: {NAVY}; }}
.num {{ display: inline-block; width: 7mm; height: 7mm; border-radius: 50%; background: {NAVY}; color: {ACCENT}; text-align: center; line-height: 7mm; font-weight: 700; margin-right: 2.5mm; font-size: 11pt; }}
.ic {{ width: 15mm; height: 15mm; flex: none; }}
"""


import base64, os as _os
URL_QR = "https://yasinbenx.github.io/azubi-vertrag/"
URL_KURZ = "yasinbenx.github.io/azubi-vertrag"
def qr_uri():
    p = _os.path.join(_os.path.dirname(__file__), "..", "output", "v2", "qr", "qr.svg")
    return "data:image/svg+xml;base64," + base64.b64encode(open(p, "rb").read()).decode()

def doc(pages_html, title):
    return f"""<!doctype html><html lang="de"><head><meta charset="utf-8"><title>{esc(title)}</title>
<style>{CSS}</style></head><body>{pages_html}</body></html>"""


def page(kicker, title, body, num=None, foot=True, qr_head=False):
    f = ""
    qh = ""
    if qr_head:
        qh = (f'<div style="position:absolute;right:12mm;top:3mm;display:flex;align-items:center;gap:3mm">'
              f'<div style="text-align:right;line-height:1.25"><div style="color:{ACCENT};font-weight:700;font-size:10pt">Interaktiv üben</div><div style="color:#DCE3F2;font-size:7.5pt">{URL_KURZ}</div></div>'
              f'<div style="background:#fff;padding:0.8mm;border-radius:1.2mm"><img src="{qr_uri()}" style="display:block;width:22mm;height:22mm"></div></div>')
    if foot:
        f = f'<div class="foot"><span>Rechte und Pflichten aus dem Ausbildungsvertrag · Stand Oktober 2026</span><span>{num}</span></div>' if num else \
            '<div class="foot"><span>Rechte und Pflichten aus dem Ausbildungsvertrag · Stand Oktober 2026</span><span></span></div>'
    return f"""<section class="page"><div class="head"><div class="kicker">{esc(kicker)}</div><h1>{esc(title)}</h1>{qh}</div>
<div class="body">{body}</div>{f}</section>"""


def merk(text, label="Merksatz", big=False):
    return f'<div class="merk{" big" if big else ""}"><span class="lbl">{esc(label)}</span><div class="txt">{esc(text)}</div></div>'


def info(inner, label="Wichtig"):
    return f'<div class="info"><span class="lbl">{esc(label)}</span>{inner}</div>'


def warn(text, label="Achtung"):
    return f'<div class="warn"><span class="lbl">{esc(label)}</span><div class="txt">{esc(text)}</div></div>'


# ---------------------------------------------------------------- Icons (selbst gezeichnet, 48x48)
def icon(name, size="15mm", color=NAVY, acc=ACCENT):
    s = f'fill="none" stroke="{color}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"'
    paths = {
        "calendar": f'<rect x="6" y="10" width="36" height="32" rx="4" {s}/><path d="M6 20h36M16 5v9M32 5v9" {s}/><rect x="13" y="26" width="7" height="6" fill="{acc}"/><rect x="26" y="26" width="7" height="6" fill="{acc}"/>',
        "clock": f'<circle cx="24" cy="24" r="18" {s}/><path d="M24 12v13l9 5" {s} stroke="{acc}"/>',
        "euro": f'<circle cx="24" cy="24" r="18" {s}/><text x="24" y="32" text-anchor="middle" font-size="24" font-weight="700" font-family="Liberation Sans, Arial" fill="{acc}">€</text>',
        "palm": f'<path d="M23 43c0-9 1-17 3-26" {s}/><path d="M26 17c-5-7-13-7-19-2M26 17c-2-8 5-12 12-9M26 17c6-5 13-3 16 4M26 17c5 3 8 8 8 13M26 17c-7 0-12 4-14 10" {s} stroke="{acc}"/><path d="M12 43h24" {s}/>',
        "hourglass": f'<path d="M12 6h24M12 42h24M14 6c0 10 10 12 10 18S14 32 14 42M34 6c0 10-10 12-10 18s10 8 10 18" {s}/><path d="M18 38c3-3 9-3 12 0z" fill="{acc}" stroke="none"/>',
        "doc": f'<path d="M12 5h18l8 8v30H12z" {s}/><path d="M30 5v8h8M18 22h14M18 29h14M18 36h9" {s} stroke="{acc}"/>',
        "contract": f'<path d="M9 5h20l7 7v31H9z" {s}/><path d="M15 20h14M15 27h10" {s}/><path d="M26 41l14-14 5 5-14 14-7 2z" fill="{acc}" stroke="{color}" stroke-width="2.5" stroke-linejoin="round"/>',
        "para": f'<text x="24" y="38" text-anchor="middle" font-size="44" font-weight="700" font-family="Liberation Sans, Arial" fill="{color}">§</text>',
    }
    return f'<svg class="ic" style="width:{size};height:{size}" viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg">{paths[name]}</svg>'


def merkblatt_page(num=None, standalone=False, qr=True):
    from data import MERKBLATT
    rows = "".join(f'<tr><td class="b">{esc(a)}</td><td>{esc(b)}</td><td class="p">{esc(c)}</td></tr>' for a, b, c in MERKBLATT)
    css = """<style>
    .mb table.t { font-size: 11pt; } .mb table.t th { background:#14264B; color:#fff; font-size:11pt; letter-spacing:.02em; border-bottom: 1.2mm solid #F5A800; }
    .mb table.t td { padding: 1.5mm 3.5mm; } .mb table.t td.b { width: 34mm; font-size: 11pt; } .mb table.t td.p { width: 33mm; font-weight: 700; color:#14264B; border-left: 0.3mm solid #D5D9E3; }
    .mb table.t tr td { border-bottom: 0.3mm solid #8E97AC; }
    </style>"""
    strip = ""
    if qr:
        strip = (f'<div style="display:flex;align-items:center;gap:5mm;margin-top:3.5mm;border:0.5mm solid {NAVY};border-radius:2mm;padding:1.5mm 4mm;background:#fff">'
                 f'<img src="{qr_uri()}" style="display:block;width:20mm;height:20mm;flex:none">'
                 f'<div><div style="font-weight:700;font-size:13pt;color:{NAVY}">Üben auf dem Handy</div><div style="font-size:11pt">{URL_KURZ}</div></div></div>')
    body = css + f'<div class="mb"><table class="t"><tr><th>Thema</th><th>Das müsst ihr wissen</th><th>Paragraf</th></tr>{rows}</table>{strip}</div>'
    return page("Zum Herausnehmen", "Merkblatt: Das Wichtigste auf einer Seite", body, num=num)
