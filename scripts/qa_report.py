#!/usr/bin/env python3
"""
QA report for a site, before or after it goes live. Produces a pass/warn/fail report the owner can read.

    python qa_report.py site/                      # a local folder (served on a temporary local port)
    python qa_report.py https://mariasbakery.com   # a live site
    options: --out qa/  --widths 390,768,1440  --max-pages 30  --expect-phone "555-0100"

It follows internal links from the homepage and, for every page:
  loads without errors (desktop, tablet, phone) · no sideways scrolling · images load and have descriptions
  internal links and #anchors resolve · external links open safely · page title and description present
  one main heading · language set · share preview tags with an absolute image · favicon
  tap targets big enough on phones · tiny text on phones · placeholder text left behind
  forms that don't send anywhere · page weight and load time
Site-wide: sitemap.xml, robots.txt, 404 page, business details (structured data), phone number consistency.

Writes <out>/qa-report.md, <out>/qa-report.json and screenshots in <out>/shots/.
Exit code: 0 = no failures (warnings allowed), 1 = at least one failure.
Needs: pip install playwright requests && playwright install chromium
"""
import argparse
import functools
import http.server
import json
import pathlib
import re
import socketserver
import sys
import threading
import time
from urllib.parse import urljoin, urlparse, urldefrag

try:
    import requests
    from playwright.sync_api import sync_playwright
except ImportError:
    sys.exit("Missing dependencies: pip install playwright requests && playwright install chromium")

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36"
GENERIC_TYPES = {"WebSite", "WebPage", "BreadcrumbList", "Article", "BlogPosting", "ImageObject", "FAQPage", "SiteNavigationElement", "SearchAction", "Person", "VideoObject", "ItemList"}
PLACEHOLDER = re.compile(r"lorem ipsum|\bTODO\b|\bTBD\b|placeholder text|your (business|company) name here|example\.com|\[insert|xx+x", re.I)

PAGE_JS = r"""
() => {
  const q = s => document.querySelector(s);
  const meta = n => (q(`meta[name="${n}"]`) || q(`meta[property="${n}"]`) || {}).content || "";
  const imgs = [...document.images].map(i => ({src: i.currentSrc || i.src, ok: i.complete && i.naturalWidth > 0,
      alt: i.hasAttribute('alt'), decorative: i.getAttribute('alt') === '' }));
  const links = [...document.querySelectorAll('a[href]')].map(a => ({href: a.getAttribute('href'), abs: a.href,
      target: a.target, rel: a.rel, text: (a.innerText || a.getAttribute('aria-label') || '').trim().slice(0, 60)}));
  const forms = [...document.forms].map(f => ({action: f.getAttribute('action') || '', method: (f.method || 'get').toLowerCase(),
      handled: !!f.getAttribute('data-handled') || !!f.onsubmit}));
  const ids = [...document.querySelectorAll('[id]')].map(e => e.id);
  const ld = [...document.querySelectorAll('script[type="application/ld+json"]')].map(s => s.textContent);
  const nav = performance.getEntriesByType('navigation')[0] || {};
  const res = performance.getEntriesByType('resource');
  const bytes = (nav.transferSize || nav.encodedBodySize || 0) + res.reduce((s, r) => s + (r.transferSize || r.encodedBodySize || 0), 0);
  return {
    title: document.title || '', description: meta('description'), lang: document.documentElement.lang || '',
    viewport: meta('viewport'), h1: document.querySelectorAll('h1').length,
    og: {title: meta('og:title'), description: meta('og:description'), image: meta('og:image'), url: meta('og:url')},
    twitter: meta('twitter:card'), favicon: !!q('link[rel~="icon"]'),
    imgs, links, forms, ids, ld, text: document.body ? document.body.innerText : '',
    bytes, loadMs: Math.round((nav.loadEventEnd || nav.duration || 0)),
  };
}
"""

MOBILE_JS = r"""
() => {
  const vw = document.documentElement.clientWidth;
  const over = document.documentElement.scrollWidth > vw + 1;
  const culprits = over ? [...document.querySelectorAll('body *')].filter(e => {
      const r = e.getBoundingClientRect(); return r.right > vw + 1 && r.width > 0; }).slice(0, 3)
      .map(e => e.tagName.toLowerCase() + (e.className && typeof e.className === 'string' ? '.' + e.className.split(' ')[0] : '')) : [];
  const small = [...document.querySelectorAll('a, button, input, select, textarea')].filter(e => {
      const r = e.getBoundingClientRect(); const st = getComputedStyle(e);
      return r.width > 0 && r.height > 0 && st.visibility !== 'hidden' && (r.height < 32 || r.width < 32) &&
             !e.closest('p, li, td, figcaption'); }).length;
  const tiny = [...document.querySelectorAll('p, li, a, span, td, label')].filter(e => {
      const st = getComputedStyle(e); return e.innerText && e.innerText.trim().length > 3 && parseFloat(st.fontSize) < 12 &&
             e.getBoundingClientRect().width > 0; }).length;
  return {over, culprits, small, tiny};
}
"""


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass


def serve(folder):
    handler = functools.partial(Quiet, directory=str(folder))
    httpd = socketserver.TCPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd, f"http://127.0.0.1:{httpd.server_address[1]}/"


class Report:
    def __init__(self):
        self.items = []  # (level, page, check, detail)

    def add(self, level, page, check, detail=""):
        self.items.append({"level": level, "page": page, "check": check, "detail": detail})

    def count(self, level):
        return sum(1 for i in self.items if i["level"] == level)


def norm(u):
    u, _ = urldefrag(u)
    return u[:-len("index.html")] if u.endswith("/index.html") else u


def head_ok(url, cache):
    if url in cache:
        return cache[url]
    try:
        r = requests.head(url, headers={"User-Agent": UA}, timeout=15, allow_redirects=True)
        if r.status_code in (405, 403):
            r = requests.get(url, headers={"User-Agent": UA}, timeout=15, stream=True)
        cache[url] = r.status_code
    except Exception as e:
        cache[url] = str(e)[:60]
    return cache[url]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("target", help="local site folder or https:// URL")
    ap.add_argument("--out", default="qa")
    ap.add_argument("--widths", default="390,768,1440")
    ap.add_argument("--max-pages", type=int, default=30)
    ap.add_argument("--expect-phone", default="", help="the business phone number; flags pages that show a different one")
    ap.add_argument("--check-external", action="store_true", help="also request every external link (slower)")
    a = ap.parse_args()

    out = pathlib.Path(a.out); (out / "shots").mkdir(parents=True, exist_ok=True)
    widths = [int(w) for w in a.widths.split(",")]
    local = not re.match(r"https?://", a.target)
    httpd = None
    if local:
        folder = pathlib.Path(a.target).resolve()
        if not (folder / "index.html").exists():
            sys.exit(f"No index.html in {folder}")
        httpd, base = serve(folder)
    else:
        base = a.target.rstrip("/") + "/"
    host = urlparse(base).netloc
    R = Report()
    status_cache = {}
    pages, queue, seen, broken = {}, [base], set(), set()

    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context(user_agent=UA)
        while queue and len(seen) < a.max_pages:
            url = norm(queue.pop(0))
            if url in seen:
                continue
            seen.add(url)
            name = urlparse(url).path or "/"
            pg = ctx.new_page()
            errors = []
            pg.on("pageerror", lambda e: errors.append(str(e)[:120]))
            pg.on("console", lambda m: errors.append(m.text[:120]) if m.type == "error" and not m.text.startswith("Failed to load resource") else None)
            t0 = time.time()
            try:
                resp = pg.goto(url, wait_until="networkidle", timeout=45000)
            except Exception as e:
                R.add("fail", name, "Page loads", str(e)[:120]); pg.close(); continue
            if not resp or resp.status >= 400:
                if url not in broken:
                    R.add("fail", name, "Page loads", f"HTTP {resp.status if resp else '?'}")
                pg.close(); continue
            pg.wait_for_timeout(600)
            info = pg.evaluate(PAGE_JS)
            info["seconds"] = round(time.time() - t0, 1)
            pages[name] = info

            # discover internal pages
            for l in info["links"]:
                u = norm(l["abs"])
                pu = urlparse(u)
                if pu.scheme in ("http", "https") and pu.netloc == host and not re.search(r"\.(pdf|zip|jpg|png|webp|mp4|svg)$", pu.path, re.I):
                    if u not in seen and u not in queue:
                        queue.append(u)

            # --- page checks
            if errors:
                R.add("fail", name, "No script errors", "; ".join(dict.fromkeys(errors))[:200])
            t = info["title"].strip()
            if not t:
                R.add("fail", name, "Page title", "missing")
            elif not (10 <= len(t) <= 65):
                R.add("warn", name, "Page title length", f"{len(t)} characters (aim for 10–65): {t[:70]}")
            d = info["description"].strip()
            if not d:
                R.add("fail", name, "Search description", "missing meta description")
            elif not (50 <= len(d) <= 160):
                R.add("warn", name, "Search description length", f"{len(d)} characters (aim for 50–160)")
            if info["h1"] != 1:
                R.add("warn", name, "One main heading", f"{info['h1']} main headings (should be exactly 1)")
            if not info["lang"]:
                R.add("warn", name, "Language set", "the page doesn't say which language it's in (helps screen readers and search)")
            if "width=device-width" not in info["viewport"]:
                R.add("fail", name, "Phone layout", "page isn't set up to fit phone screens (missing viewport setting)")
            og = info["og"]
            missing = [k for k in ("title", "description", "image") if not og[k]]
            if missing:
                R.add("fail", name, "Share preview", "when shared in chats or social posts, the preview has no " + ", no ".join({"title": "title", "description": "description", "image": "picture"}[m] for m in missing))
            elif not og["image"].startswith("https://") and not local:
                R.add("fail", name, "Share preview", "the share picture needs a full https:// address")
            elif not og["image"].startswith("http"):
                R.add("warn", name, "Share preview", "the share picture should use a full https:// address on the live domain")
            if info["twitter"] != "summary_large_image":
                R.add("warn", name, "Share preview", "large share picture not enabled for X/Twitter")
            if not info["favicon"]:
                R.add("warn", name, "Browser tab icon", "no small icon for browser tabs and bookmarks")
            for im in info["imgs"]:
                if not im["ok"]:
                    R.add("fail", name, "Images load", im["src"][-80:])
                elif not im["alt"]:
                    R.add("warn", name, "Image descriptions", f"no description for screen readers and search: {im['src'][-60:]}")
            for l in info["links"]:
                h = l["href"]
                if h.startswith("#") and len(h) > 1 and h[1:] not in info["ids"]:
                    R.add("fail", name, "Links", f"#{h[1:]} doesn't exist on the page")
                elif h.startswith(("tel:", "mailto:", "sms:")):
                    continue
                elif h.startswith(("http://", "https://", "/")) or not h.startswith(("#", "javascript:")):
                    pu = urlparse(l["abs"])
                    if pu.netloc == host:
                        st = head_ok(urldefrag(l["abs"])[0], status_cache)
                        if st != 200:
                            R.add("fail", name, "Links", f"{h} → {st}")
                            broken.add(norm(l["abs"]))
                    elif pu.scheme in ("http", "https"):
                        if l["target"] == "_blank" and "noopener" not in l["rel"]:
                            R.add("warn", name, "External links", f"opens a new tab without the safe setting (noopener): {h[:60]}")
                        if a.check_external:
                            st = head_ok(l["abs"], status_cache)
                            if st != 200:
                                R.add("warn", name, "External links", f"{h[:60]} → {st}")
            for f in info["forms"]:
                if not f["action"] and not f["handled"]:
                    R.add("fail", name, "Forms send somewhere", "form has no action: messages would go nowhere")
            m = sorted({x.group(0).strip() for x in PLACEHOLDER.finditer(info["text"])})
            if m:
                R.add("fail", name, "No placeholder text", ", ".join(f'"{x}"' for x in m)[:100])
            if a.expect_phone:
                digits = re.sub(r"\D", "", a.expect_phone)[-10:]
                for ph in set(re.findall(r"\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}", info["text"])):
                    if re.sub(r"\D", "", ph)[-10:] != digits:
                        R.add("fail", name, "Phone number", f"shows {ph}, expected {a.expect_phone}")
                tel = [l["href"] for l in info["links"] if l["href"].startswith("tel:")]
                for tl in tel:
                    if re.sub(r"\D", "", tl)[-10:] != digits:
                        R.add("fail", name, "Phone number", f"call button dials {tl}")
            kb = info["bytes"] / 1024
            if kb > 3000:
                R.add("warn", name, "Page weight", f"{kb:,.0f} KB (aim under 1,500 KB)")
            if not local and info["seconds"] > 4:
                R.add("warn", name, "Load time", f"{info['seconds']} s to fully load")

            # --- each width: overflow, tap targets, tiny text, screenshot
            slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-") or "home"
            for w in widths:
                pg.set_viewport_size({"width": w, "height": 900})
                pg.wait_for_timeout(250)
                mob = pg.evaluate(MOBILE_JS)
                if mob["over"]:
                    R.add("fail", name, f"No sideways scrolling ({w}px)", "wider than the screen: " + ", ".join(mob["culprits"]))
                if w <= 420:
                    if mob["small"] > 0:
                        R.add("warn", name, "Tap targets on phones", f"{mob['small']} buttons/links smaller than 32px")
                    if mob["tiny"] > 0:
                        R.add("warn", name, "Text size on phones", f"{mob['tiny']} text blocks under 12px")
                if w in (min(widths), max(widths)):
                    kind = "phone" if w == min(widths) else "desktop"
                    pg.screenshot(path=str(out / "shots" / f"{slug}-{kind}.png"), full_page=True)
            pg.close()

        # --- site-wide
        for path, label, level in (("sitemap.xml", "sitemap.xml", "warn"), ("robots.txt", "robots.txt", "warn")):
            st = head_ok(urljoin(base, path), status_cache)
            if st != 200:
                R.add(level, "site", label, "missing (helps search engines find every page)")
        st = head_ok(urljoin(base, "this-page-does-not-exist-qa"), {})
        if st == 200:
            R.add("warn", "site", "404 page", "missing pages return 200 instead of a 'not found' page")
        def biz_types(blocks):
            found = []
            for s in blocks:
                try:
                    j = json.loads(s)
                except Exception:
                    continue
                items = j if isinstance(j, list) else j.get("@graph", [j]) if isinstance(j, dict) else []
                for it in items:
                    ty = it.get("@type") if isinstance(it, dict) else None
                    for x in (ty if isinstance(ty, list) else [ty]):
                        if x and x not in GENERIC_TYPES:
                            found.append(x)
            return found
        if pages and not any(biz_types(pg_["ld"]) for pg_ in pages.values()):
            R.add("warn", "site", "Business details for search", "no business details for Google (name, address, phone, hours) in the page code")
        titles = [p_["title"] for p_ in pages.values()]
        dup = {t for t in titles if titles.count(t) > 1 and t}
        if dup:
            R.add("warn", "site", "Unique page titles", "repeated: " + "; ".join(list(dup)[:3]))
        browser.close()
    if httpd:
        httpd.shutdown()

    # --- write report
    fails, warns = R.count("fail"), R.count("warn")
    verdict = "PASS" if fails == 0 and warns == 0 else ("PASS with notes" if fails == 0 else "NEEDS FIXES")
    L = [f"# QA report: {host if not local else pathlib.Path(a.target).name}", "",
         f"**Result: {verdict}** · {len(pages)} pages · {fails} to fix · {warns} worth improving · checked at widths {a.widths}px", ""]
    L += ["| Page | Title | Load | Weight |", "|---|---|---|---|"]
    for n, i in pages.items():
        L.append(f"| `{n}` | {i['title'][:50].replace('|', '/')} | {i['seconds']} s | {i['bytes']/1024:,.0f} KB |")
    L.append("")
    for level, head in (("fail", "## Must fix before launch"), ("warn", "## Worth improving")):
        rows = [i for i in R.items if i["level"] == level]
        if rows:
            L += [head, ""] + [f"- **{i['check']}** · `{i['page']}` · {i['detail']}" for i in rows] + [""]
    checked = ["Pages load with no script errors", "No sideways scrolling at each width", "Images load and have descriptions",
               "Internal links and #anchors work", "External links open safely", "Page titles and search descriptions",
               "One main heading per page", "Share previews (title, description, image)", "Favicon", "Phone tap targets and text size",
               "No placeholder text", "Forms send somewhere", "Page weight", "sitemap.xml, robots.txt, 404 page", "Business details for search"]
    if a.expect_phone:
        checked.append(f"Phone number matches {a.expect_phone} everywhere")
    L += ["## What was checked", ""] + [f"- {c}" for c in checked] + ["", "Screenshots of every page (phone and desktop) are in `shots/`."]
    (out / "qa-report.md").write_text("\n".join(L) + "\n")
    (out / "qa-report.json").write_text(json.dumps({"verdict": verdict, "pages": list(pages), "items": R.items}, indent=2))
    print("\n".join(L[:3]))
    print(f"Report: {out / 'qa-report.md'}")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
