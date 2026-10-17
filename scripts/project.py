#!/usr/bin/env python3
"""
The engagement's memory: one project.json per site build.

    python project.py init "Maria's Bakery" --domain mariasbakery.com [--mode self|behalf] [--file project.json]
    python project.py set goal "Get pickup orders"          # dot paths ok: set look.style "Warm & local"
    python project.py add pages "Menu"                       # append to a list field
    python project.py fact "Open Tue-Sun 7am-3pm" --source "Google profile"
    python project.py decide "Warm & local style" --why "Owner picked style 3"
    python project.py todo "Send 5 shop photos" --owner owner [--due 2026-10-20]
    python project.py done 2                                 # mark todo #2 done
    python project.py approve brief|look|site|golive|handover [--note "said yes in chat"]
    python project.py live "https://mariasbakery.com" --note "Replaced coming-soon page; backup in /backup-2026-10-17"
    python project.py status                                 # plain-language summary
    python project.py brief                                  # one-page brief (markdown)

Uses only the standard library. Never store passwords, tokens or keys here.
"""
import argparse
import datetime as dt
import json
import pathlib
import re
import sys

GATES = ["brief", "look", "site", "golive", "handover"]
PHASES = {
    "brief": "Discovery",
    "look": "Look and feel",
    "site": "Build and check",
    "golive": "Go live",
    "handover": "Handover",
}
SECRET = re.compile(
    r"((password|passwd|pwd|pass|token|api[_-]?key|secret)\s*[:=]\s*\S{4,}"   # "password: hunter2", "token=abc123"
    r"|ssh-(rsa|ed25519) [A-Za-z0-9+/]{20,}|BEGIN [A-Z ]*PRIVATE KEY"
    r"|\b(?=[A-Za-z0-9_\-]*\d)(?=[A-Za-z0-9_\-]*[A-Za-z])[A-Za-z0-9_\-]{32,}\b"            # long key-like strings
    r"|\b[a-z]{4}( [a-z]{4}){5}\b)",                                                       # WordPress app password format
    re.I)
SECRET_FIELD = re.compile(r"(^|\.)(password|passwd|pwd|pass|token|api[_-]?key|secret|credentials?)$", re.I)


def now():
    return dt.datetime.now().strftime("%Y-%m-%d %H:%M")


def load(path):
    p = pathlib.Path(path)
    if not p.exists():
        sys.exit(f"No project file at {p}. Start one with: project.py init \"Business name\"")
    return json.loads(p.read_text())


def save(path, data):
    data["updated"] = now()
    pathlib.Path(path).write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def guard(text, field=""):
    if SECRET.search(text or "") or SECRET_FIELD.search(field or ""):
        sys.exit("That looks like it contains a password, token or key. Secrets never go in the project file.")


def set_path(d, dotted, value):
    keys = dotted.split(".")
    for k in keys[:-1]:
        d = d.setdefault(k, {})
    d[keys[-1]] = value


def get_path(d, dotted, default=None):
    for k in dotted.split("."):
        if not isinstance(d, dict) or k not in d:
            return default
        d = d[k]
    return d


def current_phase(data):
    for g in GATES:
        if g not in data["approvals"]:
            return g
    return None


def cmd_init(a):
    p = pathlib.Path(a.file)
    if p.exists() and not a.force:
        sys.exit(f"{p} already exists. Use --force to start over (the old file is kept as {p}.bak).")
    if p.exists():
        p.rename(p.with_suffix(p.suffix + ".bak"))
    data = {
        "business": a.name,
        "domain": a.domain or "",
        "mode": a.mode,
        "owner": {"name": a.owner or "", "contact": ""},
        "goal": "",
        "audience": "",
        "main_action": "",
        "pages": [],
        "look": {"references": [], "style": "", "logo": "", "colours": []},
        "hosting": {"situation": "", "summary": "", "route": "", "change_frequency": ""},
        "facts": [],
        "decisions": [],
        "todos": [],
        "approvals": {},
        "live": [],
        "not_included": ["Legal pages (privacy, terms)", "Paid ads", "Stock photography", "Ongoing edits unless agreed"],
        "created": now(),
    }
    save(p, data)
    print(f"Started {p} for {a.name}.")


def cmd_set(a):
    d = load(a.file)
    guard(a.value, a.field)
    val = a.value
    try:
        val = json.loads(a.value)
    except Exception:
        pass
    set_path(d, a.field, val)
    save(a.file, d)
    print(f"Set {a.field}.")


def cmd_add(a):
    d = load(a.file)
    guard(a.value, a.field)
    lst = get_path(d, a.field)
    if lst is None:
        lst = []
        set_path(d, a.field, lst)
    if not isinstance(lst, list):
        sys.exit(f"{a.field} is not a list.")
    lst.append(a.value)
    save(a.file, d)
    print(f"Added to {a.field}.")


def cmd_fact(a):
    d = load(a.file)
    guard(a.text)
    d["facts"].append({"fact": a.text, "source": a.source or "", "confirmed": bool(a.source), "added": now()})
    save(a.file, d)
    print("Fact recorded." + ("" if a.source else " No source yet: it stays off the site until confirmed."))


def cmd_decide(a):
    d = load(a.file)
    guard(a.text)
    d["decisions"].append({"decision": a.text, "why": a.why or "", "when": now()})
    save(a.file, d)
    print("Decision logged.")


def cmd_todo(a):
    d = load(a.file)
    guard(a.text)
    d["todos"].append({"id": len(d["todos"]) + 1, "task": a.text, "owner": a.owner, "due": a.due or "", "done": False})
    save(a.file, d)
    print(f"To-do #{len(d['todos'])} added.")


def cmd_done(a):
    d = load(a.file)
    for t in d["todos"]:
        if t["id"] == a.id:
            t["done"] = True
            t["done_at"] = now()
            save(a.file, d)
            print(f"To-do #{a.id} done.")
            return
    sys.exit(f"No to-do #{a.id}.")


def cmd_approve(a):
    d = load(a.file)
    if a.gate not in GATES:
        sys.exit(f"Gate must be one of: {', '.join(GATES)}")
    earlier = [g for g in GATES[: GATES.index(a.gate)] if g not in d["approvals"]]
    if earlier and not a.force:
        sys.exit(f"Earlier gate(s) not approved yet: {', '.join(earlier)}. Get those first (or --force if the owner explicitly skipped).")
    d["approvals"][a.gate] = {"when": now(), "note": a.note or ""}
    save(a.file, d)
    nxt = current_phase(d)
    print(f"Approved: {PHASES[a.gate]}." + (f" Next: {PHASES[nxt]}." if nxt else " All phases complete."))


def cmd_live(a):
    d = load(a.file)
    d["live"].append({"url": a.url, "note": a.note or "", "when": now()})
    save(a.file, d)
    print("Recorded what's live.")


def cmd_status(a):
    d = load(a.file)
    ph = current_phase(d)
    n = GATES.index(ph) + 1 if ph else len(GATES)
    out = [f"# {d['business']}" + (f" — {d['domain']}" if d.get("domain") else "")]
    out.append(f"**Where we are:** " + (f"Phase {n} of 5, {PHASES[ph].lower()}." if ph else "All five phases done."))
    done = [f"{PHASES[g]} ({v['when'][:10]})" for g, v in d["approvals"].items()]
    if done:
        out.append("**Approved so far:** " + "; ".join(done) + ".")
    owner_todos = [t for t in d["todos"] if not t["done"] and t["owner"] == "owner"]
    my_todos = [t for t in d["todos"] if not t["done"] and t["owner"] != "owner"]
    if owner_todos:
        out.append("**Waiting on you:** " + "; ".join(t["task"] + (f" (by {t['due']})" if t["due"] else "") for t in owner_todos) + ".")
    if my_todos:
        out.append("**On my list:** " + "; ".join(t["task"] for t in my_todos) + ".")
    unconfirmed = [f["fact"] for f in d["facts"] if not f["confirmed"]]
    if unconfirmed:
        out.append("**Left off the site until confirmed:** " + "; ".join(unconfirmed) + ".")
    if d["live"]:
        out.append("**Live:** " + ", ".join(x["url"] for x in d["live"]) + ".")
    if ph:
        out.append(f"**Next gate:** your yes on the {PHASES[ph].lower()} phase.")
    print("\n\n".join(out))


def cmd_brief(a):
    d = load(a.file)
    L = [f"# Website brief: {d['business']}", ""]
    L += ["**Goal:** " + (d.get("goal") or "_to confirm_"), ""]
    L += ["**Who it's for:** " + (d.get("audience") or "_to confirm_") + "  ",
          "**Main button:** " + (d.get("main_action") or "_to confirm_"), ""]
    L += ["**Pages**", ""] + [f"- {p}" for p in d.get("pages", [])] + ([""] if d.get("pages") else ["- _to confirm_", ""])
    look = d.get("look", {})
    L += ["**Look:** " + ", ".join(x for x in [look.get("style", ""), ("references: " + ", ".join(look["references"])) if look.get("references") else "", ("logo: " + look["logo"]) if look.get("logo") else ""] if x) or "**Look:** _to choose_", ""]
    conf = [f for f in d["facts"] if f["confirmed"]]
    unconf = [f for f in d["facts"] if not f["confirmed"]]
    L += ["**Facts we'll use**", ""] + [f"- {f['fact']} _(source: {f['source']})_" for f in conf] + (["- _none yet_"] if not conf else []) + [""]
    if unconf:
        L += ["**Left out until you confirm**", ""] + [f"- {f['fact']}" for f in unconf] + [""]
    h = d.get("hosting", {})
    L += ["**Where it will live:** " + (d.get("domain") or "_no address yet_") + (f". {h['summary']}" if h.get("summary") else ""), ""]
    owner_todos = [t for t in d["todos"] if not t["done"] and t["owner"] == "owner"]
    L += ["**What I need from you**", ""] + ([f"- {t['task']}" + (f" (by {t['due']})" if t["due"] else "") for t in owner_todos] or ["- Nothing yet"]) + [""]
    L += ["**What happens next**", "",
          "1. Discovery — this brief (your yes)",
          "2. Look — two directions, you pick and refine",
          "3. Build — full site, checked on desktop and phone, with a QA report",
          "4. Go live — on your address, nothing changes without your OK",
          "5. Handover — a short document with everything you need", ""]
    L += ["**Not included:** " + ", ".join(d.get("not_included", [])) + "."]
    print("\n".join(L))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--file", default="project.json")
    sp = ap.add_subparsers(dest="cmd", required=True)
    p = sp.add_parser("init"); p.add_argument("name"); p.add_argument("--domain"); p.add_argument("--mode", choices=["self", "behalf"], default="self"); p.add_argument("--owner"); p.add_argument("--force", action="store_true"); p.set_defaults(f=cmd_init)
    p = sp.add_parser("set"); p.add_argument("field"); p.add_argument("value"); p.set_defaults(f=cmd_set)
    p = sp.add_parser("add"); p.add_argument("field"); p.add_argument("value"); p.set_defaults(f=cmd_add)
    p = sp.add_parser("fact"); p.add_argument("text"); p.add_argument("--source"); p.set_defaults(f=cmd_fact)
    p = sp.add_parser("decide"); p.add_argument("text"); p.add_argument("--why"); p.set_defaults(f=cmd_decide)
    p = sp.add_parser("todo"); p.add_argument("text"); p.add_argument("--owner", choices=["owner", "me"], default="me"); p.add_argument("--due"); p.set_defaults(f=cmd_todo)
    p = sp.add_parser("done"); p.add_argument("id", type=int); p.set_defaults(f=cmd_done)
    p = sp.add_parser("approve"); p.add_argument("gate"); p.add_argument("--note"); p.add_argument("--force", action="store_true"); p.set_defaults(f=cmd_approve)
    p = sp.add_parser("live"); p.add_argument("url"); p.add_argument("--note"); p.set_defaults(f=cmd_live)
    p = sp.add_parser("status"); p.set_defaults(f=cmd_status)
    p = sp.add_parser("brief"); p.set_defaults(f=cmd_brief)
    a = ap.parse_args()
    a.f(a)


if __name__ == "__main__":
    main()
