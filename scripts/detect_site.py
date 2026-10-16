#!/usr/bin/env python3
"""
Work out where a website lives and what it runs on, from just the domain.

    python detect_site.py example.com
    python detect_site.py example.com --json

Uses public DNS-over-HTTPS and a normal web request. Needs only `requests`.
Prints a plain-language summary plus the evidence, and a suggested situation:
  hosting-panel | wordpress | site-builder | static-host | no-hosting | unknown
"""
import argparse
import json
import re
import socket
import sys

try:
    import requests
except ImportError:
    sys.exit("Missing dependency: pip install requests")

UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36"}

# (name, kind, evidence regexes applied to headers+html+dns text)
FINGERPRINTS = [
    ("Wix", "site-builder", [r"x-wix-", r"static\.wixstatic\.com", r"wix\.com website builder", r"\bwixdns\.net"]),
    ("Squarespace", "site-builder", [r"squarespace", r"static1\.squarespace\.com"]),
    ("Shopify", "site-builder", [r"x-shopify", r"cdn\.shopify\.com", r"myshopify\.com"]),
    ("Webflow", "site-builder", [r"webflow", r"assets\.website-files\.com"]),
    ("GoDaddy Website Builder", "site-builder", [r"img1\.wsimg\.com", r"godaddy website builder", r"secureserver\.net.*website builder"]),
    ("Weebly / Square Online", "site-builder", [r"weebly", r"editmysite\.com", r"square online"]),
    ("Carrd", "site-builder", [r"carrd\.co"]),
    ("Framer", "site-builder", [r"framer\.com", r"framerusercontent", r"\bframer\b"]),
    ("Ghost", "site-builder", [r"ghost\.io", r'generator" content="ghost']),
    ("Hostinger Website Builder", "site-builder", [r"zyrosite", r"zyro"]),
    ("WordPress.com (hosted)", "wordpress", [r"wordpress\.com", r"wp\.com"]),
    ("WordPress", "wordpress", [r"/wp-content/", r"/wp-includes/", r'generator" content="wordpress', r"wp-json"]),
    ("Netlify", "static-host", [r"x-nf-request-id", r"server: netlify", r"netlify\.app"]),
    ("Vercel", "static-host", [r"x-vercel-id", r"server: vercel", r"vercel\.app"]),
    ("Cloudflare Pages", "static-host", [r"pages\.dev"]),
    ("GitHub Pages", "static-host", [r"github\.io", r"server: github\.com"]),
]

PARKED = [r"domain (is )?for sale", r"this domain (name )?(has been|is) (registered|parked)", r"parked (free|domain)",
          r"buy this domain", r"sedoparking", r"parkingcrew", r"domain parking", r"bodis"]
PLACEHOLDER = [r"coming soon", r"under construction", r"default web site page", r"index of /", r"apache2? (ubuntu )?default page",
               r"welcome to nginx", r"it works!", r"future home of", r"website is (almost )?ready", r"this site is under development"]


def doh(name, rtype):
    try:
        r = requests.get("https://cloudflare-dns.com/dns-query", params={"name": name, "type": rtype},
                         headers={"accept": "application/dns-json"}, timeout=10)
        return [a["data"].rstrip(".") for a in r.json().get("Answer", []) if a.get("type") in (1, 2, 5, 15, 28)]
    except Exception:
        return []


def port_open(host, port, timeout=3):
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except Exception:
        return False


def reverse_dns(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except Exception:
        return ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("domain")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    domain = re.sub(r"^https?://", "", a.domain.strip()).split("/")[0].lower()
    if domain.startswith("www."):
        domain = domain[4:]

    out = {"domain": domain}
    out["nameservers"] = doh(domain, "NS")
    out["a"] = doh(domain, "A")
    out["www"] = doh("www." + domain, "CNAME") or doh("www." + domain, "A")
    out["mx"] = [m for m in doh(domain, "MX") if len(m.split()) == 2]  # ignore "null MX" (no email)
    out["reverse_dns"] = reverse_dns(out["a"][0]) if out["a"] else ""

    page = {"reachable": False}
    for scheme in ("https", "http"):
        try:
            r = requests.get(f"{scheme}://{domain}/", headers=UA, timeout=15, allow_redirects=True)
            page = {"reachable": True, "status": r.status_code, "final_url": r.url,
                    "headers": {k.lower(): v for k, v in r.headers.items()}, "html": r.text[:200000]}
            break
        except Exception as e:
            page["error"] = str(e)[:200]
    out["page"] = {k: v for k, v in page.items() if k != "html"}

    hay = " ".join([json.dumps(page.get("headers", {})).lower(), page.get("html", "").lower(),
                    " ".join(out["nameservers"] + out["a"] + out["www"]).lower(), out["reverse_dns"].lower(),
                    page.get("final_url", "").lower()])
    hay_hdr = "\n".join(f"{k}: {v}" for k, v in page.get("headers", {}).items()).lower()

    found = []
    for name, kind, pats in FINGERPRINTS:
        if any(re.search(p, hay) or re.search(p, hay_hdr) for p in pats):
            found.append((name, kind))
    # wordpress REST probe (cheap, strong signal)
    if page.get("reachable") and not any(k == "wordpress" for _, k in found):
        try:
            wp = requests.get(f"https://{domain}/wp-json/", headers=UA, timeout=10)
            if wp.ok and "namespaces" in wp.text[:5000]:
                found.append(("WordPress", "wordpress"))
        except Exception:
            pass
    out["platforms"] = [n for n, _ in found]

    html = page.get("html", "").lower()
    out["parked"] = bool(re.search("|".join(PARKED), html))
    out["placeholder"] = bool(re.search("|".join(PLACEHOLDER), html))
    challenged = page.get("status") in (403, 429, 503) and re.search(r"just a moment|captcha|challenge|attention required", html or "")
    out["blocked_by_security_check"] = bool(challenged)

    panel_ports = {}
    if out["a"]:
        ip = out["a"][0]
        for port, label in ((2083, "cPanel"), (8443, "Plesk"), (2222, "DirectAdmin")):
            if port_open(ip, port):
                panel_ports[label] = port
    out["control_panel_ports"] = panel_ports

    kinds = [k for _, k in found]
    if not out["a"] and not out["www"]:
        situation = "no-hosting"
    elif out["parked"]:
        situation = "no-hosting"
    elif "site-builder" in kinds and not ("WordPress" in out["platforms"] and "WordPress.com (hosted)" not in out["platforms"]):
        situation = "site-builder"
    elif "wordpress" in kinds:
        situation = "wordpress"
    elif "static-host" in kinds:
        situation = "static-host"
    elif panel_ports or out["placeholder"]:
        situation = "hosting-panel"
    else:
        situation = "unknown"
    out["situation"] = situation

    # plain summary
    def host_hint(names):
        s = " ".join(names).lower()
        m = re.findall(r"([a-z0-9-]+)\.(com|net|org|io|co|cloud|host)\b", s)
        return sorted({x[0] for x in m})
    lines = []
    ns_owner = host_hint(out["nameservers"])
    if ns_owner:
        lines.append(f"The address's settings (DNS) are managed by: {', '.join(ns_owner)}.")
    if out["reverse_dns"]:
        lines.append(f"The website's server identifies as {out['reverse_dns']}.")
    if out["platforms"]:
        lines.append(f"The live site looks like: {', '.join(out['platforms'])}.")
    if out["parked"]:
        lines.append("Right now the address shows a parked or for-sale page, not a website.")
    elif out["placeholder"]:
        lines.append("Right now the address shows a placeholder (e.g. 'coming soon' or a default server page).")
    if panel_ports:
        lines.append(f"The server looks like typical file-based hosting with a control panel ({', '.join(panel_ports)}).")
    if out["mx"]:
        lines.append("This address has email set up. Don't change nameservers or MX records.")
    if out["blocked_by_security_check"]:
        lines.append("A security check blocked the automatic look; ask what they see when they log in to their provider.")
    if situation == "unknown" and page.get("reachable") and not out["blocked_by_security_check"]:
        lines.insert(0, "A website loads, but I can't tell what it runs on from the outside.")
    if not page.get("reachable"):
        lines.append("The address doesn't load a website at the moment.")
    lines.append(f"Suggested situation: {situation}.")
    out["summary"] = lines

    if a.json:
        print(json.dumps(out, indent=2))
    else:
        print("\n".join(lines))
        print("\nEvidence:")
        for k in ("nameservers", "a", "www", "mx", "reverse_dns", "platforms", "control_panel_ports"):
            print(f"  {k}: {out[k]}")
        p = out["page"]
        if p.get("reachable"):
            print(f"  page: {p.get('status')} {p.get('final_url')}  server={p.get('headers', {}).get('server', '')}")


if __name__ == "__main__":
    main()
