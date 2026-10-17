# Launch runbook

Going live is where amateur jobs break things that were working: business email, Google rankings, an old shop page someone still uses. Follow this in order, every time. Tick each step in the project file (`project.py todo … --owner me` / `done`).

## 1. Before publishing (start of the Go live phase)

- [ ] **QA report passes** (`qa_report.py`): no "must fix" items. Warnings are explained to the owner or fixed.
- [ ] **Owner said yes to the full site** (`project.py approve site`).
- [ ] **DNS snapshot taken** (once the publishing route is agreed, before anything changes): `python scripts/dns_snapshot.py theirdomain.com`. Don't read the technical summary out; tell the owner in plain words:
  > "Your address also handles your email (with Company X). I'll only touch the website part, so your email keeps working."
- [ ] **If the old site has pages that people or Google know about**, write a redirect map: old address → new page. Collect the old addresses from the old site's menu, its sitemap (`/sitemap.xml`), and a `site:theirdomain.com` search. Anything without a match redirects to the homepage. See "Redirects" below.
- [ ] **Things that depend on the old site** are listed and have a plan: online shop, bookings, member logins, forms that feed another system, email sign-up lists, an "order online" link printed on menus or vans.
- [ ] **Backup plan** written down: what will be saved (old files, old WordPress homepage setting), where, and the one step that restores it.
- [ ] **Launch time** agreed: a quiet time for the business (not Friday afternoon for a restaurant), with the owner reachable for 30 minutes after.

## 2. Launch

- [ ] Back up first (the deploy scripts do this automatically; via the browser, download or rename the existing files before uploading).
- [ ] Publish using the agreed route.
- [ ] If DNS has to change, **change only the website records** (A/AAAA for the bare domain, CNAME or A for `www`). Never change nameservers or MX unless the person explicitly wants to move everything, and only after the new place has copied **every** record from the snapshot.
- [ ] Put redirects in place (if any).
- [ ] Record what's live: `project.py live https://theirdomain.com --note "…"`.

## 3. Straight after launch (same session)

- [ ] `python scripts/verify_live.py https://theirdomain.com` → all OK.
- [ ] `python scripts/qa_report.py https://theirdomain.com --out qa-live --expect-phone "…"` → no new failures compared with the pre-launch report.
- [ ] **Email is safe:** `python scripts/dns_snapshot.py theirdomain.com --compare dns-before-theirdomain.com.json` → "Email is safe". If not, restore the records shown before doing anything else, and tell the owner plainly.
- [ ] **SSL works** on both `https://theirdomain.com` and `https://www.theirdomain.com` (no browser warning, padlock shows). `http://` redirects to `https://`.
- [ ] `www` and the bare domain both show the new site (or one redirects to the other).
- [ ] Contact/booking form: send a real test message and confirm it arrived where the owner expects. Tell the owner to expect it.
- [ ] Click every main button on a real phone-sized screen: call button dials the right number, booking link opens the right page.
- [ ] Old addresses from the redirect map land on the right new pages.

## 4. If something goes wrong

Stop, restore, then explain. In that order.

- **Site broken or wrong:** restore the backup (the one step written down earlier), confirm the old site is back, then tell the owner what happened in one or two sentences and what you'll do differently.
- **Email stopped:** compare with the snapshot and put the missing records back exactly as they were. DNS changes can take up to a few hours to settle everywhere; say so.
- **SSL warning:** usually the host hasn't issued the certificate yet (wait 15–60 minutes and check the host's SSL page), or a CAA record blocks the host's certificate company (the snapshot shows CAA).
- **Old version still showing:** caching. Hard refresh (Ctrl+Shift+R / Cmd+Shift+R); clear the host's cache if it has one.

## 5. One week later

Offer to set this up as a scheduled check at handover (only with the owner's yes):

- [ ] Site is up on both addresses, SSL valid.
- [ ] Form still delivers (ask the owner if they've received any messages).
- [ ] Google has started to index it: a `site:theirdomain.com` search shows the new pages, or Search Console shows no errors.
- [ ] Email still works (`dns_snapshot.py --compare`).
- [ ] Send the owner a two-line update either way.

## Redirects

When a new site replaces an old one, old page addresses must lead somewhere, or visitors and Google hit "not found" pages and the business loses rankings it earned.

- **Static site on a host with a control panel (Apache):** add lines to `.htaccess` in the site's folder, one per old page:
  `Redirect 301 /old-services-page /services.html`
  Keep it short, and back up `.htaccess` first.
- **WordPress:** use the host's or a redirection plugin's screen (with the owner's OK to install it), or ask the host's support with a message you write.
- **Static hosts (Netlify, Cloudflare Pages):** a `_redirects` file in the site folder: `/old-page  /new-page  301`.
- **Site builders:** most have a "URL redirects" screen under SEO settings.
- Test each redirect after launch (part of the checklist above).
