#!/usr/bin/env python3
"""
Create or update WordPress pages through the built-in REST API, using an Application Password.

    python publish_wordpress.py --title "Home" --slug home --html section.html            # creates a DRAFT
    python publish_wordpress.py --title "Home" --slug home --html section.html --publish  # only after the owner said yes
    python publish_wordpress.py --list                                                     # show existing pages

.env keys: WP_SITE (https://example.com), WP_USER, WP_APP_PASSWORD

Notes:
- The HTML is placed in a single Custom HTML block, so the theme's editor shows it as one block.
- If a page with the slug exists, it is updated (its previous content is saved under backups/ first).
- Global CSS belongs in the theme's Additional CSS / site editor, not in each page.
"""
import argparse
import datetime as dt
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from _common import load_env, require  # noqa: E402

try:
    import requests
except ImportError:
    sys.exit("Missing dependency: pip install requests")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--env", default=".env")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--title")
    ap.add_argument("--slug")
    ap.add_argument("--html", help="file with the page body HTML")
    ap.add_argument("--template", default="", help="page template slug, e.g. a full-width template if the theme has one")
    ap.add_argument("--publish", action="store_true", help="publish instead of saving as draft")
    a = ap.parse_args()

    env = load_env(a.env, ["WP_SITE", "WP_USER", "WP_APP_PASSWORD"])
    require(env, ["WP_SITE", "WP_USER", "WP_APP_PASSWORD"])
    base = env["WP_SITE"].rstrip("/") + "/wp-json/wp/v2"
    s = requests.Session()
    s.auth = (env["WP_USER"], env["WP_APP_PASSWORD"].replace(" ", ""))
    s.headers["User-Agent"] = "launch-my-site/1.0"

    me = s.get(base + "/users/me", params={"context": "edit"}, timeout=30)
    if me.status_code in (401, 403):
        sys.exit("WordPress rejected the application password (revoked, wrong user, or API blocked by a security plugin).")
    me.raise_for_status()
    print(f"Signed in to {env['WP_SITE']} as {me.json().get('name')}")

    if a.list:
        for p in s.get(base + "/pages", params={"per_page": 100, "context": "edit", "status": "any"}, timeout=30).json():
            print(f"  {p['id']:>6}  {p['status']:8}  /{p['slug']}  {p['title']['raw']}")
        return

    if not (a.title and a.slug and a.html):
        sys.exit("Give --title, --slug and --html (or use --list).")
    body = pathlib.Path(a.html).read_text()
    content = f"<!-- wp:html -->\n{body}\n<!-- /wp:html -->"
    data = {"title": a.title, "slug": a.slug, "content": content, "status": "publish" if a.publish else "draft"}
    if a.template:
        data["template"] = a.template

    existing = s.get(base + "/pages", params={"slug": a.slug, "context": "edit", "status": "any"}, timeout=30).json()
    if existing:
        page = existing[0]
        bdir = pathlib.Path("backups") / dt.datetime.now().strftime("%Y%m%d-%H%M%S")
        bdir.mkdir(parents=True, exist_ok=True)
        (bdir / f"wp-page-{a.slug}.json").write_text(json.dumps(page, indent=2))
        print(f"Backed up current page to {bdir.resolve()}")
        if not a.publish and page["status"] == "publish":
            data["status"] = "publish"  # don't unpublish a live page by accident
            print("Note: page is already live; updating it keeps it live.")
        r = s.post(f"{base}/pages/{page['id']}", json=data, timeout=60)
    else:
        r = s.post(base + "/pages", json=data, timeout=60)
    r.raise_for_status()
    p = r.json()
    print(f"{'Published' if p['status']=='publish' else 'Saved as draft'}: {p['title']['rendered']}  ->  {p['link']}")
    if p["status"] != "publish":
        print("Share the preview with the owner and publish only after they say yes.")


if __name__ == "__main__":
    main()
