# -*- coding: utf-8 -*-
import os, sys, segno, cv2, numpy as np
from PIL import Image
URL = "https://yasinbenx.github.io/azubi-vertrag/"
OUT = os.path.join(os.path.dirname(__file__), "..", "output", "v2", "qr")
os.makedirs(OUT, exist_ok=True)
qr = segno.make(URL, error="q", micro=False, boost_error=False)       # Fehlerkorrektur Q
BORDER = 4                                                              # Ruhezone: 4 Module
mods = qr.symbol_size(border=BORDER)[0]
scale = -(-1000 // mods)                                                # ganzzahlige Skalierung, mind. 1000 px
qr.save(os.path.join(OUT, "qr.png"), scale=scale, border=BORDER, dark="black", light="white")
im = Image.open(os.path.join(OUT, "qr.png")).convert("RGB"); assert im.width >= 1000 and im.width == im.height, im.size
qr.save(os.path.join(OUT, "qr.svg"), scale=10, border=BORDER, dark="black", light="white", xmldecl=True, svgns=True)
# klein (~300 px): ganzzahlig skaliert, damit alle Module gleich gross und scharf bleiben
s2 = max(1, round(300 / mods))
qr.save(os.path.join(OUT, "qr_klein.png"), scale=s2, border=BORDER, dark="black", light="white")
open(os.path.join(OUT, "url_text.txt"), "w", encoding="utf-8").write(URL + "\n")
print("Version", qr.version, "Fehlerkorrektur", qr.error, "Module", mods, "px gross:", Image.open(os.path.join(OUT, "qr.png")).size, "klein:", Image.open(os.path.join(OUT, "qr_klein.png")).size)

def decode_cv(path):
    img = cv2.imread(path); d = cv2.QRCodeDetector(); val, pts, _ = d.detectAndDecode(img); return val
def decode_all(path):
    out = {"opencv": decode_cv(path)}
    try:
        from pyzbar import pyzbar
        out["zbar"] = ",".join(o.data.decode() for o in pyzbar.decode(Image.open(path)))
    except Exception as e: out["zbar"] = None
    return out
if __name__ == "__main__":
    for f in ("qr.png", "qr_klein.png"):
        r = decode_all(os.path.join(OUT, f)); print(f, r, "OK" if all(v == URL for v in r.values() if v is not None) else "FEHLER")
    # SVG: rendern und dekodieren
    import subprocess
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome", args=["--no-sandbox"]); pg = b.new_page(viewport={"width": 800, "height": 800})
        pg.goto("file://" + os.path.abspath(os.path.join(OUT, "qr.svg"))); pg.screenshot(path="/tmp/qr_svg.png"); b.close()
    print("qr.svg", decode_all("/tmp/qr_svg.png"))
