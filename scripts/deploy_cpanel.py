#!/usr/bin/env python3
"""
Publish a static site through a cPanel-compatible control panel's API (UAPI),
using an API token. No browser.

    python deploy_cpanel.py --site ./site --dry-run
    python deploy_cpanel.py --site ./site

.env keys: CPANEL_HOST, CPANEL_USER, CPANEL_TOKEN, SITE_URL  (CPANEL_PORT optional, default 2083)

Safety: finds the folder that serves SITE_URL's domain and refuses to run if the
account doesn't serve that domain; backs up every text file it will overwrite;
never deletes anything.
"""
import argparse
import datetime as dt
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from _common import TEXT_EXT, host_of, load_env, require, site_files  # noqa: E402

try:
    import requests
except ImportError:
    sys.exit("Missing dependency: pip install requests")

KEYS = ["CPANEL_HOST", "CPANEL_USER", "CPANEL_TOKEN", "CPANEL_PORT", "SITE_URL"]


class Panel:
    def __init__(self, host, user, token, port="2083"):
        self.base = f"https://{host}:{port}"
        self.s = requests.Session()
        self.s.headers["Authorization"] = f"cpanel {user}:{token}"

    def uapi(self, module, func, method="GET", **kw):
        r = self.s.request(method, f"{self.base}/execute/{module}/{func}", timeout=90, **kw)
        if r.status_code in (401, 403):
            sys.exit("The control panel rejected the key (expired, revoked, or wrong username). Nothing was changed.")
        r.raise_for_status()
        data = r.json()
        if not data.get("status"):
            raise RuntimeError(f"{module}/{func}: {data.get('errors')}")
        return data.get("data")

    def api2(self, module, func, **params):
        params.update(cpanel_jsonapi_apiversion=2, cpanel_jsonapi_module=module, cpanel_jsonapi_func=func)
        r = self.s.get(f"{self.base}/json-api/cpanel", params=params, timeout=60)
        r.raise_for_status()
        return r.json().get("cpanelresult", {})

    def docroot_for(self, domain):
        d = self.uapi("DomainInfo", "domains_data", params={"format": "hash"})
        entries = []
        main = d.get("main_domain") or {}
        if main:
            entries.append(main)
        for key in ("addon_domains", "sub_domains", "parked_domains"):
            v = d.get(key) or []
            entries.extend(v.values() if isinstance(v, dict) else v)
        served = {}
        for e in entries:
            if isinstance(e, dict):
                served[e.get("domain", "").lower()] = e.get("documentroot") or main.get("documentroot")
            elif isinstance(e, str):  # parked domains may be bare names sharing the main docroot
                served[e.lower()] = main.get("documentroot")
        return served.get(domain) or served.get("www." + domain), sorted(k for k in served if k)

    def list_dir(self, d):
        try:
            return {f["file"]: f for f in self.uapi("Fileman", "list_files", params={"dir": d})}
        except Exception:
            return None

    def mkdir(self, parent, name):
        self.api2("Fileman", "mkdir", path=parent, name=name)

    def get_text(self, d, name):
        return self.uapi("Fileman", "get_file_content", params={"dir": d, "file": name})["content"]

    def upload(self, d, files):
        handles = [(f"file-{i+1}", (p.name, p.open("rb"))) for i, p in enumerate(files)]
        try:
            return self.uapi("Fileman", "upload_files", method="POST", data={"dir": d, "overwrite": "1"}, files=handles)
        finally:
            for _, (_, fh) in handles:
                fh.close()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--site", required=True, help="local folder containing index.html")
    ap.add_argument("--env", default=".env")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    env = load_env(args.env, KEYS)
    require(env, ["CPANEL_HOST", "CPANEL_USER", "CPANEL_TOKEN", "SITE_URL"])
    domain = host_of(env["SITE_URL"])
    site, by_dir = site_files(args.site)
    panel = Panel(env["CPANEL_HOST"], env["CPANEL_USER"], env["CPANEL_TOKEN"], env.get("CPANEL_PORT", "2083"))

    root, served = panel.docroot_for(domain)
    print("This hosting account serves:", ", ".join(served) or "(none found)")
    if not root:
        sys.exit(f"STOP: {domain} is not served by this account. Nothing was changed.")
    print(f"{domain} is served from: {root}")

    plan = []
    for sub, files in sorted(by_dir.items()):
        rdir = f"{root}/{sub}" if sub else root
        existing = panel.list_dir(rdir)
        for p in files:
            plan.append((rdir, p, "replace" if existing and p.name in existing else "add"))
    for rdir, p, action in plan:
        print(f"  {action:7} {rdir}/{p.name}")
    if args.dry_run:
        print("Dry run: nothing changed.")
        return

    backup = pathlib.Path("backups") / dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    for rdir, p, action in plan:
        if action == "replace" and p.suffix.lower() in TEXT_EXT:
            dest = backup / rdir.lstrip("/") / p.name
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(panel.get_text(rdir, p.name))
    if backup.exists():
        print(f"Backed up replaced files to {backup.resolve()}")

    for sub in sorted(s for s in by_dir if s):
        parent = root
        for part in sub.split("/"):
            if panel.list_dir(f"{parent}/{part}") is None:
                panel.mkdir(parent, part)
                print(f"  created folder {parent}/{part}")
            parent = f"{parent}/{part}"

    for sub, files in sorted(by_dir.items()):
        rdir = f"{root}/{sub}" if sub else root
        res = panel.upload(rdir, files) or {}
        bad = [u for u in res.get("uploads", []) if not u.get("status")]
        if bad:
            sys.exit(f"Upload failed in {rdir}: {json.dumps(bad)}")
        print(f"Uploaded {len(files)} file(s) to {rdir}")

    print(f"Done. Now run: python scripts/verify_live.py {env['SITE_URL']}")


if __name__ == "__main__":
    main()
