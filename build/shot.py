import sys
from playwright.sync_api import sync_playwright
def shot(html, png, w, h, scale=2, full=False):
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome", args=["--no-sandbox"])
        pg = b.new_page(viewport={"width": w, "height": h}, device_scale_factor=scale)
        pg.set_content(html); pg.wait_for_timeout(300)
        pg.screenshot(path=png, full_page=full)
        b.close()
if __name__ == "__main__":
    svg = open(sys.argv[1]).read()
    shot(f'<body style="margin:0;background:#fff">{svg}</body>', sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), 1)
