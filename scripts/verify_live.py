#!/usr/bin/env python3
"""
Check a live site: pages, linked CSS/JS/images, and the share preview tags.

    python verify_live.py https://example.com
    python verify_live.py https://example.com --pages index.html about.html contact.html

Without --pages it follows internal links from the homepage (one level deep).
Exit code 0 = everything OK.
"""
import argparse
import re
import sys
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse

try:
    import requests
except ImportError:
    sys.exit("Missing dependency: pip install requests")

UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36"}


class Refs(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.assets, self.meta, self.title = set(), set(), {}, ""
        self._in_title = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "a" and a.get("href"):
            self.links.add(a["href"])
        if tag in ("img", "script") and a.get("src"):
            self.assets.add(a["src"])
        if tag == "link" and a.get("href") and (a.get("rel") or "") in ("stylesheet", "icon"):
            self.assets.add(a["href"])
        if tag == "meta":
            k = a.get("property") or a.get("name")
            if k:
                self.meta[k] = a.get("content", "")
        if tag == "title":
            self._in_title = True

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False

    def handle_data(self, data):
        if self._in_title:
            self.title += data


def get(url):
    try:
        return requests.get(url, headers=UA, timeout=20)
    except Exception as e:
        return e


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("url")
    ap.add_argument("--pages", nargs="*")
    a = ap.parse_args()
    base = a.url.rstrip("/") + "/"
    host = urlparse(base).netloc

    home = get(base)
    if isinstance(home, Exception) or home.status_code != 200:
        code = home if isinstance(home, Exception) else home.status_code
        if not isinstance(home, Exception) and home.status_code in (403, 429, 503) and \
                re.search(r"just a moment|captcha|challenge|attention required", home.text[:5000], re.I):
            print("The host's bot protection blocked this automated check (it does this to scripts, not visitors).")
            print("Verify in a real browser instead, e.g. with the browser tool or by asking the owner to open the site.")
            sys.exit(2)
        sys.exit(f"Homepage didn't load: {code}")
    refs = Refs()
    refs.feed(home.text)

    pages = [base] + [urljoin(base, p) for p in (a.pages or []) if p not in ("index.html", "")]
    if not a.pages:
        for href in refs.links:
            u = urljoin(base, href.split("#")[0])
            if urlparse(u).netloc == host and u not in pages and not re.search(r"\.(png|jpe?g|gif|pdf|zip|svg)$", u):
                pages.append(u)

    problems, checked_assets = [], set()
    for page in pages:
        r = get(page)
        status = r if isinstance(r, Exception) else r.status_code
        print(f"  {status}  {page}")
        if status != 200:
            problems.append(f"{page} returned {status}")
            continue
        pr = Refs()
        pr.feed(r.text)
        for key in ("og:title", "og:description", "og:image", "twitter:card"):
            if not pr.meta.get(key):
                problems.append(f"{page} is missing the share tag {key}")
        if not pr.title.strip():
            problems.append(f"{page} has no <title>")
        for src in pr.assets:
            u = urljoin(page, src)
            if urlparse(u).netloc != host or u in checked_assets:
                continue
            checked_assets.add(u)
            ar = get(u)
            astatus = ar if isinstance(ar, Exception) else ar.status_code
            if astatus != 200:
                problems.append(f"asset {u} returned {astatus}")
        for href in pr.links:
            if href.startswith("#") and len(href) > 1 and f'id="{href[1:]}"' not in r.text:
                problems.append(f"{page} links to missing anchor {href}")

    og = refs.meta.get("og:image")
    if og:
        ir = get(urljoin(base, og))
        ok = not isinstance(ir, Exception) and ir.status_code == 200 and ir.headers.get("content-type", "").startswith("image/")
        print(f"  {'OK ' if ok else 'BAD'}  share image {og}")
        if not ok:
            problems.append("share image doesn't load as an image")

    print(f"\nChecked {len(pages)} page(s) and {len(checked_assets)} asset(s).")
    if problems:
        print("Problems:")
        for p in problems:
            print("  - " + p)
        print("(A 403 can be the host's bot protection; confirm in a real browser.)")
        sys.exit(1)
    print("Everything is live and loading.")


if __name__ == "__main__":
    main()
