# Route: site builders (Wix, Squarespace, Shopify, Webflow and similar)

These platforms host the site and the editor together. They don't accept an uploaded HTML site on the main address. Say so early and kindly, then offer three options and recommend one.

> Your site is built with **Squarespace**. Squarespace doesn't let anyone upload a ready-made website, so we have three ways to do this:
> **A.** I design it and we rebuild it inside Squarespace, so you can keep editing it there. *(Best if you want to keep using Squarespace.)*
> **B.** We put the new site on a separate address like **new.yourdomain.com** and leave your current site alone.
> **C.** We move **yourdomain.com** to the new site. Your Squarespace site stops showing, and you'd cancel it later once you're sure nothing else depends on it.

## Before recommending, check what the builder is doing for them

Ask (or check the live site): do they sell products, take bookings or payments, run a blog, collect member logins, or have email lists through the builder? Do they get email @theirdomain through the builder?

- If yes to any: recommend **A** or **B**. Moving the domain (C) can break those.
- Email is the big one. Changing nameservers can stop their email. Changing only the website records (A/CNAME) usually doesn't. Check before any DNS change.

## A. Rebuild inside the builder

- Build the design as normal (`build.md`) and show it.
- Translate it into the builder's terms: page list, sections, fonts, colours (hex values), button labels, spacing, and the exact copy for every block. Produce a short "build sheet" per page.
- Invite route: most builders let owners add a contributor or collaborator by email. Owners grant it in the site's settings under something like "Permissions", "Contributors" or "Team".
- Log-in-and-do-it-with-them route: they open the editor; with a browser tool and permission you make changes section by section, or you guide them with the build sheet.
- Many builders allow custom code blocks (embed HTML/CSS) on paid plans. Use them for a section the native blocks can't match, not for the whole site.

## B. New site on a sub-address

1. Deploy the site to a free static host (`route-no-hosting.md`).
2. Add the sub-address. In the builder's (or registrar's) DNS settings, add a **CNAME** record, e.g. `new` → the static host's address. Most builders' domain settings have "Add record". Walk them through it, or use the static host's "Connect domain" flow, which shows the exact record.
3. Link to it from the main site if they want.

## C. Move the main address

Same as B but for the main address, following the static host's domain instructions. Prefer changing only the **website records** (A/AAAA for the bare domain and CNAME for `www`) rather than the nameservers, so email keeps working. Tell them in advance that the change can take from minutes to a few hours to show everywhere, and that the old site stays reachable on the builder until they cancel it.

Never cancel or delete the builder site for them. Leave that to the owner, after they've checked everything works.
