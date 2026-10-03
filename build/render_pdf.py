# -*- coding: utf-8 -*-
"""HTML -> PDF per Chromium (Playwright) plus Ueberlauf-Pruefung je Seite."""
import sys, os, asyncio
from playwright.sync_api import sync_playwright

def render(html_path, pdf_path):
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome", args=["--no-sandbox"])
        pg = b.new_page()
        pg.goto("file://" + os.path.abspath(html_path))
        pg.wait_for_timeout(400)
        bad = pg.evaluate("""() => [...document.querySelectorAll('.page')].map((s,i)=>{
            const body = s.querySelector('.body'); if(!body) return null;
            const over = body.scrollHeight - body.clientHeight;
            // lowest content bottom vs footer
            const foot = s.querySelector('.foot'); const fb = foot ? foot.getBoundingClientRect().top : s.getBoundingClientRect().bottom;
            let maxb = 0; body.querySelectorAll('*').forEach(e=>{const r=e.getBoundingClientRect(); if(r.height>0) maxb=Math.max(maxb,r.bottom);});
            const sb = s.getBoundingClientRect();
            return {page:i+1, over, gapToFooter: Math.round((fb-maxb)*0.2646*10)/10};
        })""")
        for r in bad:
            if r and (r["over"] > 1 or r["gapToFooter"] < 3):
                print("WARN overflow/tight:", r)
        pg.pdf(path=pdf_path, prefer_css_page_size=True, print_background=True)
        b.close()

if __name__ == "__main__":
    render(sys.argv[1], sys.argv[2])
