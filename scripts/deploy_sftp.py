#!/usr/bin/env python3
"""
Publish a static site over SFTP (SSH key preferred, password supported). Works with almost any host.

    python deploy_sftp.py --site ./site --dry-run
    python deploy_sftp.py --site ./site

.env keys:
  SFTP_HOST, SFTP_USER, SFTP_PORT (default 22),
  SFTP_KEY_FILE (path to private key)  or  SFTP_PASSWORD,
  REMOTE_DIR (the folder that serves the site, e.g. public_html or /var/www/site),
  SITE_URL

Safety: before uploading, fetches a one-time marker file through SITE_URL to prove
REMOTE_DIR really serves that domain (and removes the marker); backs up every file
it will overwrite; never deletes site files.
"""
import argparse
import datetime as dt
import pathlib
import secrets
import stat
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from _common import load_env, require, site_files  # noqa: E402

try:
    import paramiko
    import requests
except ImportError:
    sys.exit("Missing dependency: pip install paramiko requests")

KEYS = ["SFTP_HOST", "SFTP_USER", "SFTP_PORT", "SFTP_KEY_FILE", "SFTP_PASSWORD", "REMOTE_DIR", "SITE_URL"]


def exists(sftp, path):
    try:
        sftp.stat(path)
        return True
    except IOError:
        return False


def ensure_dir(sftp, path):
    parts, cur = path.strip("/").split("/"), "/" if path.startswith("/") else ""
    for part in parts:
        cur = f"{cur}{part}" if cur in ("", "/") else f"{cur}/{part}"
        if not exists(sftp, cur):
            sftp.mkdir(cur)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--site", required=True)
    ap.add_argument("--env", default=".env")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    env = load_env(args.env, KEYS)
    require(env, ["SFTP_HOST", "SFTP_USER", "REMOTE_DIR", "SITE_URL"])
    if not env.get("SFTP_KEY_FILE") and not env.get("SFTP_PASSWORD"):
        sys.exit("Set SFTP_KEY_FILE (preferred) or SFTP_PASSWORD in .env.")
    site, by_dir = site_files(args.site)
    root = env["REMOTE_DIR"].rstrip("/")

    t = paramiko.Transport((env["SFTP_HOST"], int(env.get("SFTP_PORT") or 22)))
    if env.get("SFTP_KEY_FILE"):
        key_path = env["SFTP_KEY_FILE"]
        key = None
        for cls in (paramiko.Ed25519Key, paramiko.RSAKey, paramiko.ECDSAKey):
            try:
                key = cls.from_private_key_file(key_path)
                break
            except Exception:
                continue
        if key is None:
            sys.exit(f"Couldn't read the private key at {key_path}.")
        t.connect(username=env["SFTP_USER"], pkey=key)
    else:
        t.connect(username=env["SFTP_USER"], password=env["SFTP_PASSWORD"])
    sftp = paramiko.SFTPClient.from_transport(t)

    # Prove REMOTE_DIR serves SITE_URL with a short-lived marker file
    token = secrets.token_hex(8)
    marker = f"{root}/.lms-check-{token}.txt"
    with sftp.open(marker, "w") as fh:
        fh.write(token)
    try:
        r = requests.get(f"{env['SITE_URL'].rstrip('/')}/.lms-check-{token}.txt", timeout=20,
                         headers={"User-Agent": "Mozilla/5.0 (deploy-check)"})
        ok = r.ok and token in r.text
    except Exception:
        ok = False
    finally:
        sftp.remove(marker)
    if not ok:
        sys.exit(f"STOP: {root} does not appear to serve {env['SITE_URL']}. Nothing was changed.")
    print(f"Confirmed {root} serves {env['SITE_URL']}")

    plan = []
    for sub, files in sorted(by_dir.items()):
        rdir = f"{root}/{sub}" if sub else root
        for p in files:
            plan.append((rdir, p, "replace" if exists(sftp, f"{rdir}/{p.name}") else "add"))
    for rdir, p, action in plan:
        print(f"  {action:7} {rdir}/{p.name}")
    if args.dry_run:
        print("Dry run: nothing changed.")
        return

    backup = pathlib.Path("backups") / dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    for rdir, p, action in plan:
        if action == "replace":
            dest = backup / rdir.lstrip("/") / p.name
            dest.parent.mkdir(parents=True, exist_ok=True)
            sftp.get(f"{rdir}/{p.name}", str(dest))
    if backup.exists():
        print(f"Backed up replaced files to {backup.resolve()}")

    for rdir, p, _ in plan:
        ensure_dir(sftp, rdir)
        sftp.put(str(p), f"{rdir}/{p.name}")
        sftp.chmod(f"{rdir}/{p.name}", stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)
    print(f"Uploaded {len(plan)} file(s).")
    sftp.close()
    t.close()
    print(f"Done. Now run: python verify_live.py {env['SITE_URL']}")


if __name__ == "__main__":
    main()
