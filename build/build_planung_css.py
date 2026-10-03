import os
from html import escape as esc
NAVY, NAVY2, ACC = "#14264B", "#22386B", "#F5A800"
CSS = f"""
@page {{ size: A4 landscape; margin: 0; }}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
html {{ -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
body {{ font-family: 'Liberation Sans', Arial, sans-serif; color: #1A2238; font-size: 11pt; background: #fff; }}
.page {{ width: 297mm; height: 210mm; position: relative; overflow: hidden; page-break-after: always; break-after: page; display: flex; flex-direction: column; }}
.page:last-child {{ page-break-after: auto; break-after: auto; }}
.head {{ background: {NAVY}; color: #fff; padding: 7mm 14mm 5mm 20mm; position: relative; flex: none; display: flex; justify-content: space-between; align-items: flex-end; }}
.head::before {{ content: ''; position: absolute; left: 0; top: 0; bottom: 0; width: 5mm; background: {ACC}; }}
.kicker {{ color: {ACC}; font-size: 9pt; font-weight: 700; letter-spacing: .12em; text-transform: uppercase; }}
.head h1 {{ font-size: 21pt; line-height: 1.1; margin-top: 1mm; }}
.head .r {{ font-size: 10pt; color: #DCE3F2; text-align: right; }}
.body {{ flex: 1; min-height: 0; overflow: hidden; padding: 4mm 7mm 0 12mm; }}
.foot {{ position: absolute; left: 12mm; right: 7mm; bottom: 4mm; display: flex; justify-content: space-between; font-size: 8pt; color: #5B6680; border-top: 0.3mm solid #D5D9E3; padding-top: 1.5mm; }}
table.pt {{ width: 100%; border-collapse: collapse; font-size: 10.4pt; }}
table.pt th {{ background: {NAVY}; color: #fff; padding: 1.9mm 2.4mm; text-align: left; font-size: 9pt; line-height: 1.15; }}
table.pt th span {{ font-weight: 400; font-size: 7.5pt; color: #DCE3F2; }}
table.pt td {{ padding: 2.3mm 2.4mm; border-bottom: 0.3mm solid #D5D9E3; }}
table.pt tr:nth-child(even) td {{ background: #F6F8FC; }}
.c {{ text-align: center; }} .b {{ font-weight: 700; color: {NAVY}; }} .ist {{ color: #8A93A8; }}
.note {{ font-size: 8.8pt; color: #5B6680; margin-top: 2.5mm; line-height: 1.4; }}
svg {{ display: block; width: 100%; height: auto; }}
"""

def page(kicker, title, body, right=""):
    return (f'<section class="page"><div class="head"><div><div class="kicker">{esc(kicker)}</div><h1>{esc(title)}</h1></div><div class="r">{right}</div></div>'
            f'<div class="body">{body}</div><div class="foot"><span>Yasin &amp; Mido · Rechte und Pflichten aus dem Ausbildungsvertrag</span><span>Planung (Soll) · 10.09.–08.10.2026</span></div></section>')

def doc(pages, title): return f'<!doctype html><html lang="de"><head><meta charset="utf-8"><title>{esc(title)}</title><style>{CSS}</style></head><body>{pages}</body></html>'

