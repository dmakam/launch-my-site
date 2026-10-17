#!/usr/bin/env python3
"""
Record a domain's DNS settings before launch, and check nothing important changed after.

    python dns_snapshot.py mariasbakery.com                         # writes dns-before-<domain>.json and prints a plain summary
    python dns_snapshot.py mariasbakery.com --compare dns-before-mariasbakery.com.json   # after the change

What it records (public DNS, no login needed): nameservers, website records (A/AAAA for the bare domain
and www), email records (MX), email-security and verification records (TXT: SPF, Google/Microsoft
verification; DMARC; common DKIM selectors), CAA, and SOA.

The compare mode is the safety net: it fails loudly if email (MX), SPF, DMARC, DKIM or verification
records disappeared or changed. Website records changing is expected and reported as such.
Exit code: 0 = email-safe, 2 = email or verification records changed.
Needs: pip install requests
"""
import argparse
import datetime as dt
import json
import pathlib
import sys

try:
    import requests
except ImportError:
    sys.exit("Missing dependency: pip install requests")

TYPES = {"A": 1, "NS": 2, "CNAME": 5, "SOA": 6, "MX": 15, "TXT": 16, "AAAA": 28, "CAA": 257}
DKIM_SELECTORS = ["default", "google", "selector1", "selector2", "k1", "s1", "s2", "mail", "dkim", "mx"]
EMAIL_KEYS = {"mx", "spf", "dmarc", "dkim", "verification"}


def doh(name, rtype):
    for url in ("https://cloudflare-dns.com/dns-query", "https://dns.google/resolve"):
        try:
            r = requests.get(url, params={"name": name, "type": rtype}, headers={"accept": "application/dns-json"}, timeout=10)
            j = r.json()
            return sorted({a["data"].rstrip(".") for a in j.get("Answer", []) if a.get("type") == TYPES[rtype]})
        except Exception:
            continue
    return None


def snapshot(domain):
    s = {"domain": domain, "taken": dt.datetime.now().isoformat(timespec="seconds")}
    s["ns"] = doh(domain, "NS")
    s["soa"] = doh(domain, "SOA")
    s["a"] = doh(domain, "A")
    s["aaaa"] = doh(domain, "AAAA")
    s["www"] = doh("www." + domain, "CNAME") or doh("www." + domain, "A")
    s["mx"] = [m for m in (doh(domain, "MX") or []) if m.strip().rstrip(".").strip() not in ("0", "")]  # "0 ." = null MX: no email
    txt = doh(domain, "TXT") or []
    s["spf"] = [t for t in txt if "v=spf1" in t.lower()]
    s["verification"] = [t for t in txt if "verification" in t.lower() or t.lower().strip('"').startswith(("ms=", "apple-domain", "facebook-domain"))]
    s["txt_other"] = [t for t in txt if t not in s["spf"] and t not in s["verification"]]
    s["dmarc"] = doh("_dmarc." + domain, "TXT") or []
    s["dkim"] = {}
    for sel in DKIM_SELECTORS:
        v = doh(f"{sel}._domainkey.{domain}", "TXT") or doh(f"{sel}._domainkey.{domain}", "CNAME")
        if v:
            s["dkim"][sel] = v
    s["caa"] = doh(domain, "CAA") or []
    return s


def summary(s):
    L = [f"DNS for {s['domain']} ({s['taken']})"]
    L.append("  In plain words for the owner: " + ("this address also handles your email, so I'll only change the website part and check your email settings again afterwards."
             if s["mx"] else "this address has no email set up, so there's no email to protect.") + " (Say this; don't read out the lines below.)")
    L.append(f"  Nameservers (who controls the settings): {', '.join(s['ns'] or ['none'])}")
    L.append(f"  Website points to: {', '.join((s['a'] or []) + (s['aaaa'] or [])) or 'nothing'}; www → {', '.join(s['www'] or ['nothing'])}")
    if s["mx"]:
        L.append(f"  EMAIL IS SET UP: {', '.join(s['mx'])}")
        L.append("  → Change only the website records (A/AAAA and www). Do not change nameservers or MX unless the new place copies every record below first.")
    else:
        L.append("  No email on this domain (no MX records).")
    if s["spf"]:
        L.append(f"  SPF (who may send email as this domain): {s['spf'][0][:90]}")
    if s["dmarc"]:
        L.append(f"  DMARC: {s['dmarc'][0][:90]}")
    if s["dkim"]:
        L.append(f"  DKIM keys found for selectors: {', '.join(s['dkim'])}")
    if s["verification"]:
        L.append(f"  Verification records (Google, Microsoft, etc.): {len(s['verification'])}")
    if s["caa"]:
        L.append(f"  CAA (which companies may issue SSL certificates): {', '.join(s['caa'])}")
        L.append("  → If the new host uses a different certificate company, its SSL will fail until CAA allows it.")
    return "\n".join(L)


def compare(before, after):
    problems, notes = [], []
    for k in ("mx", "spf", "dmarc", "verification"):
        b, a = set(before.get(k) or []), set(after.get(k) or [])
        if b - a:
            problems.append(f"{k.upper()} records missing now: {', '.join(sorted(b - a))[:200]}")
        if a - b and b:
            notes.append(f"{k.upper()} records added: {', '.join(sorted(a - b))[:120]}")
    for sel, v in (before.get("dkim") or {}).items():
        if (after.get("dkim") or {}).get(sel) != v:
            problems.append(f"DKIM key for selector '{sel}' changed or is missing")
    if set(before.get("ns") or []) != set(after.get("ns") or []):
        notes.append(f"Nameservers changed: {before.get('ns')} → {after.get('ns')}. Check every record above was copied.")
    for k, label in (("a", "Website (A)"), ("aaaa", "Website (AAAA)"), ("www", "www")):
        if set(before.get(k) or []) != set(after.get(k) or []):
            notes.append(f"{label} changed: {before.get(k) or 'none'} → {after.get(k) or 'none'} (expected when moving the site)")
    if set(before.get("caa") or []) != set(after.get("caa") or []):
        notes.append(f"CAA changed: {before.get('caa')} → {after.get('caa')}")
    return problems, notes


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("domain")
    ap.add_argument("--compare", help="a dns-before-*.json file taken earlier")
    ap.add_argument("--out", help="where to write the snapshot (default dns-before-<domain>.json, or dns-after-… with --compare)")
    a = ap.parse_args()
    domain = a.domain.lower().removeprefix("https://").removeprefix("http://").split("/")[0].removeprefix("www.")
    s = snapshot(domain)
    if s["ns"] is None:
        sys.exit("Couldn't reach public DNS. Check the network and try again.")
    out = pathlib.Path(a.out or f"dns-{'after' if a.compare else 'before'}-{domain}.json")
    out.write_text(json.dumps(s, indent=2) + "\n")
    print(summary(s))
    print(f"\nSaved: {out}")
    if a.compare:
        before = json.loads(pathlib.Path(a.compare).read_text())
        problems, notes = compare(before, s)
        print("\nCompared with", a.compare)
        for n in notes:
            print("  note:", n)
        if problems:
            print("\n  EMAIL OR VERIFICATION RECORDS CHANGED. Restore these before anything else:")
            for p in problems:
                print("   ✗", p)
            sys.exit(2)
        print("  ✓ Email and verification records unchanged. Email is safe.")


if __name__ == "__main__":
    main()
