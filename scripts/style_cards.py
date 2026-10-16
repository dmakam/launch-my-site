#!/usr/bin/env python3
"""Render visual style samples so a non-technical person can pick a look by pointing.

Each sample is a small, real homepage hero using THEIR business name, tagline and
main button, in one of several distinct styles. Output: one PNG per style plus a
single side-by-side sheet (style-cards.png) to send in chat, and the HTML files.

Usage:
  python scripts/style_cards.py --name "Northside Heating & Air" --tagline "Honest HVAC, done right" \
      --cta "Call (555) 010-0100" --out style-cards/ [--styles clean,bold,warm,classic]
      [--industry "heating & cooling"]

Needs: pip install playwright && playwright install chromium
"""
import argparse, asyncio, html, os

STYLES = {
    "clean": {
        "label": "Clean & bright",
        "note": "Light, airy, lots of white space. Feels calm and trustworthy.",
        "font": "Plus+Jakarta+Sans:wght@500;800", "family": "'Plus Jakarta Sans'",
        "css": """body{background:linear-gradient(160deg,#f4faff,#e3f1ff)}
.h{color:#0b1b33}.t{color:#4a5b75}.btn{background:linear-gradient(135deg,#38a9ff,#0a5bd8);color:#fff;border-radius:999px;box-shadow:0 10px 26px rgba(10,91,216,.3)}
.orb{background:radial-gradient(circle,rgba(56,169,255,.45),transparent 65%)}.bar{background:#fff;border-bottom:1px solid #dbe9f8;color:#0b1b33}""",
    },
    "bold": {
        "label": "Bold & dark",
        "note": "Dark background, big type, bright accents. Stands out from competitors.",
        "font": "Archivo:wght@500;900", "family": "Archivo",
        "css": """body{background:#060c1a}
.h{color:#fff;letter-spacing:-.04em}.t{color:#9aabcb}.btn{background:linear-gradient(135deg,#ffb04a,#ff7a2f);color:#1a0b00;border-radius:12px;box-shadow:0 12px 32px rgba(255,122,47,.35)}
.orb{background:radial-gradient(circle,rgba(46,197,255,.5),transparent 60%)}.bar{background:rgba(255,255,255,.04);border-bottom:1px solid rgba(255,255,255,.08);color:#fff}""",
    },
    "warm": {
        "label": "Warm & local",
        "note": "Earthy colours, friendly type. Feels like a family business next door.",
        "font": "Fraunces:wght@500;800", "family": "Fraunces",
        "css": """body{background:linear-gradient(170deg,#fbf3e8,#f4e2cc)}
.h{color:#3b2414}.t{color:#7a5a43}.btn{background:#c2562b;color:#fff;border-radius:10px;box-shadow:0 10px 24px rgba(194,86,43,.3)}
.orb{background:radial-gradient(circle,rgba(230,160,90,.45),transparent 65%)}.bar{background:#fffaf3;border-bottom:1px solid #ead7bf;color:#3b2414}""",
    },
    "classic": {
        "label": "Classic & formal",
        "note": "Navy and gold, traditional serif. Feels established and professional.",
        "font": "Playfair+Display:wght@600;800", "family": "'Playfair Display'",
        "css": """body{background:linear-gradient(180deg,#0f2340,#152d52)}
.h{color:#fff}.t{color:#c9d3e3}.btn{background:#d4a64a;color:#13233d;border-radius:4px;box-shadow:0 10px 24px rgba(0,0,0,.3)}
.orb{background:radial-gradient(circle,rgba(212,166,74,.3),transparent 65%)}.bar{background:#0b1a31;border-bottom:1px solid rgba(212,166,74,.35);color:#fff}""",
    },
}

TEMPLATE = """<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family={font}&family=Inter:wght@400;600&display=swap" rel="stylesheet">
<style>*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:720px;height:460px;overflow:hidden;font-family:Inter,system-ui,sans-serif;position:relative}}
.bar{{height:56px;display:flex;align-items:center;justify-content:space-between;padding:0 32px;font-family:{family},serif;font-weight:800;font-size:19px}}
.bar span{{font-family:Inter;font-weight:600;font-size:13px;opacity:.75}}
.orb{{position:absolute;width:420px;height:420px;border-radius:50%;right:-120px;top:-60px}}
.hero{{position:relative;padding:58px 32px 0}}
.k{{font-size:12px;font-weight:600;letter-spacing:.14em;text-transform:uppercase;opacity:.7;margin-bottom:14px}}
.h{{font-family:{family},serif;font-weight:800;font-size:48px;line-height:1.02;max-width:560px}}
.t{{font-size:16px;line-height:1.55;margin-top:16px;max-width:470px}}
.btn{{display:inline-block;margin-top:26px;padding:15px 26px;font-weight:600;font-size:15px}}
{css}</style></head><body>
<div class="bar">{name}<span>Services&nbsp;&nbsp;·&nbsp;&nbsp;About&nbsp;&nbsp;·&nbsp;&nbsp;Contact</span></div>
<div class="orb"></div>
<div class="hero"><div class="k t">{industry}</div><div class="h">{tagline}</div>
<p class="t">This is a style sample. Your real words and photos go in later.</p>
<span class="btn">{cta}</span></div></body></html>"""

SHEET = """<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@500;700&display=swap" rel="stylesheet">
<style>*{{margin:0;padding:0;box-sizing:border-box}}body{{font-family:Inter,sans-serif;background:#f3f4f7;padding:36px;width:{w}px}}
.g{{display:grid;grid-template-columns:repeat(2,1fr);gap:28px}}.c{{background:#fff;border-radius:18px;overflow:hidden;box-shadow:0 8px 24px rgba(0,0,0,.08)}}
.c img{{display:block;width:100%}}.m{{padding:16px 20px}}.m b{{font-size:18px}}.m b i{{font-style:normal;color:#888;margin-right:8px}}.m p{{color:#555;font-size:14px;margin-top:4px}}</style></head>
<body><div class="g">{cards}</div></body></html>"""


async def render(args):
    from playwright.async_api import async_playwright
    os.makedirs(args.out, exist_ok=True)
    keys = [k.strip() for k in args.styles.split(",") if k.strip() in STYLES]
    esc = lambda s: html.escape(s)
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 720, "height": 460}, device_scale_factor=2)
        cards = []
        for i, k in enumerate(keys, 1):
            s = STYLES[k]
            path = os.path.abspath(os.path.join(args.out, f"style-{k}.html"))
            with open(path, "w") as f:
                f.write(TEMPLATE.format(font=s["font"], family=s["family"], css=s["css"],
                        name=esc(args.name), tagline=esc(args.tagline), cta=esc(args.cta),
                        industry=esc(args.industry or "")))
            await pg.goto("file://" + path, wait_until="networkidle")
            png = os.path.join(args.out, f"style-{k}.png")
            await pg.screenshot(path=png)
            cards.append(f'<div class="c"><img src="file://{os.path.abspath(png)}"><div class="m"><b><i>{i}</i>{s["label"]}</b><p>{s["note"]}</p></div></div>')
            print("rendered", png)
        sheet = os.path.abspath(os.path.join(args.out, "sheet.html"))
        with open(sheet, "w") as f:
            f.write(SHEET.format(w=1560, cards="".join(cards)))
        sp = await b.new_page(viewport={"width": 1560, "height": 800})
        await sp.goto("file://" + sheet, wait_until="networkidle")
        await sp.screenshot(path=os.path.join(args.out, "style-cards.png"), full_page=True)
        print("sheet", os.path.join(args.out, "style-cards.png"))
        await b.close()


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", required=True)
    ap.add_argument("--tagline", required=True, help="Short headline in their words")
    ap.add_argument("--cta", required=True, help="Main button text, e.g. 'Call 555-0100'")
    ap.add_argument("--industry", default="")
    ap.add_argument("--styles", default="clean,bold,warm,classic")
    ap.add_argument("--out", default="style-cards")
    asyncio.run(render(ap.parse_args()))
