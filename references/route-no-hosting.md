# Route: no hosting yet (or domain only)

A site made of HTML files doesn't need paid hosting. Use a static host with a free plan that accepts a dragged folder: for example Netlify (drag-and-drop deploys), Cloudflare Pages (direct upload) or GitHub Pages. Check current plans before recommending; terms change. Don't push the person into buying hosting.

## Step 1: Get the site online at a temporary address

**Easiest: drag and drop.**
1. "Go to [static host] and sign up with your email or Google account."
2. "Find the option to deploy by dragging a folder (it may say 'Deploy manually' or 'Upload assets'). Drag the folder I sent you onto the page."
3. "It gives you an address like `something.hostname.app`. Send it to me."

With a browser tool and their permission, you can do steps 2–3 while they watch, after they've signed in themselves. Account creation and sign-in are always theirs to do.

Check the temporary address with `verify_live.py` before touching the domain.

## Step 2: Connect their domain

They need the domain itself (bought from a registrar). If they don't have one, help them pick one and let *them* buy it; don't make purchases for them.

1. In the static host, use "Add custom domain" / "Connect domain" and enter their domain. It shows exactly which records to add.
2. If it offers a one-click "Connect"/"Configure automatically" with their registrar, use that. It's the easiest.
3. Otherwise guide them in the registrar's DNS settings to add exactly what the static host lists (typically an A or ALIAS record for the bare domain and a CNAME for `www`).
4. **Check email first.** If they already get email @theirdomain, don't change nameservers, only add or replace the website records. Look at existing MX records before changing anything and leave them alone.
5. Turn on HTTPS in the static host (usually automatic once the domain connects).
6. Tell them DNS changes can take minutes to a few hours, then verify with `verify_live.py`.

## Already on a static host

If `detect_site.py` shows the domain already on a static host they control: deploy a new version the same way they deployed before (drag-and-drop, connected Git repository or CLI). Ask them to log in and you do it with them, or set up a credential route if they want hands-off updates.

## Updates later

- Rarely: they drag the new folder again (or you do it with them logged in).
- Regularly: connect a Git repository (the host then publishes every change automatically), or use the host's deploy token (`credentials.md` rules apply).
