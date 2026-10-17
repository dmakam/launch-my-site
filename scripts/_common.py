"""Shared helpers for the publishing scripts: .env loading and site file listing."""
import os
import pathlib
import sys

TEXT_EXT = {".html", ".htm", ".css", ".js", ".json", ".txt", ".xml", ".svg", ".md", ".webmanifest"}


def load_env(path, keys):
    """Read KEY=value lines from a .env file; real environment variables win."""
    env = {}
    p = pathlib.Path(path)
    if p.exists():
        for line in p.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip().strip('"').strip("'")
    for k in keys:
        if os.environ.get(k):
            env[k] = os.environ[k]
    return env


def require(env, keys):
    missing = [k for k in keys if not env.get(k)]
    if missing:
        sys.exit(f"Missing in .env: {', '.join(missing)}. Copy env.example to .env and fill it in.")


def site_files(site_dir):
    """Return {relative_subdir: [paths]} for every non-hidden file in the site folder."""
    site = pathlib.Path(site_dir).resolve()
    if not site.is_dir():
        sys.exit(f"Site folder not found: {site}")
    by_dir = {}
    for p in sorted(site.rglob("*")):
        if p.is_file() and not any(part.startswith(".") for part in p.relative_to(site).parts):
            rel = p.parent.relative_to(site).as_posix()
            by_dir.setdefault("" if rel == "." else rel, []).append(p)
    if "" not in by_dir or not any(p.name == "index.html" for p in by_dir[""]):
        sys.exit("The site folder has no index.html at its top level; nothing would show as the homepage.")
    return site, by_dir


def host_of(url):
    return url.split("//")[-1].split("/")[0].lower().removeprefix("www.")
