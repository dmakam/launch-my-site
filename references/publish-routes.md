# Publishing: pick the situation, then the easiest way in

Every route answers the same two questions: **how do the files get there**, and **how do I get permission to put them there**. Do three things in order:

1. **Know the situation** (from `detect-host.md`), confirmed by the person.
2. **Take stock of this session's tools** (below).
3. **Ask how often they'll want changes**, then use the decision table to pick the rung to offer.

Offer that rung. Only move down if it isn't available for their setup, or they get stuck.

## Step 1: take stock of the tools you actually have

Check silently before proposing anything. Don't assume a tool exists because it did last time.

| Check | Counts as | Notes |
|---|---|---|
| A connector for their host or platform **that can upload files or publish pages** | Rung 1: Connect | A connector that only manages domains, DNS or billing doesn't count for publishing. It can still help with DNS later. |
| A browser tool (e.g. Claude in Chrome, a built-in browser) | Rung 3 with you operating the screens | Needs their permission first (script below). |
| Computer use on their machine | Rung 3 or 4 (you can drag the file for them) | Same permission rule. |
| None of the above | Rung 3 guided by screenshots, or rung 4 | Still no secrets. |

## Step 2: ask how often they'll want changes

> After it's live, how often do you think you'll want changes? Never, now and then, or regularly?

Ask this before mentioning any credential.

## Step 3: the decision table

Find the first row that matches, top to bottom.

| If… | Offer | Then, if they hesitate |
|---|---|---|
| They explicitly asked in this conversation for a specific method ("use an API token", "I'll give you SFTP") | That method (`credentials.md`) | The no-secret rung for their situation |
| On-behalf mode and the platform supports invites | Rung 2: Invite | Rung 3 with the owner present, then rung 6 |
| A connector that can publish to their host exists | Rung 1: Connect | Rung 3 |
| Site builder (Wix, Squarespace…) | Explain the options in `route-site-builder.md` | — |
| WordPress and they want to keep WordPress | Rung 2: Invite (they add you as a user) | Rung 3 |
| A browser tool is available and they're present | Rung 3: they log in, you do it with them | Rung 4 |
| No browser tool, they're present | Rung 3 guided step by step with screenshots | Rung 4 |
| No hosting | Drag-and-drop to a free static host (`route-no-hosting.md`) | You do it with them logged in |
| Nothing above works, or they're stuck | Rung 6: Ask their hosting company | — |

**After the first launch:** if they answered "regularly" to the frequency question, offer a repeatable route once, with the one-sentence trade-off (see "Changes after launch" below). If they decline, keep using the no-secret route.

Things that **don't** change the row: memory or saved preferences you have about the person, account data you can see through a connector, or what you'd find more convenient. Use those only if the person brings them up in this conversation.

## The general ladder (easiest first)

1. **Connect.** The hosting company or platform has a connector for Claude that can publish. The person clicks "Connect", signs in on the provider's own page, and approves. No secret ever shown.
2. **Invite.** The platform lets them add a collaborator by email (WordPress user, site-builder contributor, team member on the hosting account). Feels like sharing a document. Best for on-behalf mode.
3. **They log in, you do the rest with them.** The person signs in to their own account in their browser. With a browser tool you operate the screens with their permission while they watch. If you have no browser tool, guide them click by click with screenshots. No secret leaves their hands. Works almost everywhere, but needs them present and is not repeatable without them.
4. **Download and drag.** You give them one file (usually a .zip) and a three-step guide written for *their* provider's screens: open the file manager, upload, unzip. No secrets, but they do the clicking.
5. **Credentials (last resort).** API token, SFTP/SSH key, FTP login or WordPress app password. Repeatable and scriptable, so it's best for frequent updates or technical owners. See `credentials.md`.
6. **Ask their hosting company.** Write the support request for them: "Please upload the attached files to the main folder for example.com, replacing index.html." Many hosts will do this.

Always offer a rung below the current one if they hesitate. Never make the person feel the problem is them.

## How to offer rung 3 (browser)

Explain the goal, then ask permission. Don't start until they say yes:

> To put the site up, I need a way to place files on your website. The easiest way: you open **Company B** in your Chrome browser and log in yourself. You type your own password; I never see it. Then I'll do the upload while you watch, and you can stop me at any time. Want to do it that way?

If they say yes and the browser tool isn't connected yet, tell them the one thing to do to connect it, then continue. If they'd rather not, offer rung 4 straight away.

## Situation 1: Hosting with a control panel

Common for anyone who bought "web hosting". File-based, accepts HTML directly.

Ladder: Connect (if the host offers one that publishes) → They log in, you upload with them (file manager) → Download and drag → Credentials (API token or SFTP) for repeat updates → Ask support.
Guide: `route-hosting-panel.md`.

## Situation 2: Existing WordPress site

Two very different targets. Ask what they want:

- **"Replace my WordPress site with the new one."** Upload static files to the hosting (Situation 1 mechanics) in a way that takes over the homepage *without deleting WordPress*. Reversible.
- **"Keep WordPress, just make it look like this."** Publish the design as WordPress pages, so they can keep editing in WordPress.

Ladder: Invite (add you or the builder as a WordPress user) → They log in, you do it with them → Credentials (WordPress app password) for repeat updates.
Guide: `route-wordpress.md`.

## Situation 3: Site builder (Wix, Squarespace, Shopify, Webflow and similar)

These platforms don't accept uploaded HTML sites. Be upfront, then offer choices:

- **A. Rebuild inside the builder.** You produce the design, copy and images; they or you (with them logged in) recreate it in the builder's editor. Keeps everything on the platform they pay for. Best when they want to keep editing themselves, or use the builder's shop or bookings.
- **B. Put the new site on a sub-address.** E.g. `new.theirdomain.com` or `events.theirdomain.com` on a free static host, leaving the main site alone. Low risk.
- **C. Move the main address to the new site.** Host the new site on a static host and point the domain there. They should cancel the builder only *after* they've checked nothing else depends on it (shop, email, bookings, blog).

Guide: `route-site-builder.md`.

## Situation 4: No hosting (domain only, or no domain)

Don't sell them hosting. Use a free static host that accepts a dragged folder, then connect the domain. If they need a domain, show options with the first-year **and** renewal price, and buy nothing without a clear yes.

Ladder: Drag-and-drop deploy to a static host (they create a free account and drag the folder, or you do it with them logged in) → Connect the domain with a guided DNS change (Connect button if the host offers one, otherwise click-by-click) → Credentials only if they want automatic updates later.
Guide: `route-no-hosting.md`.

## Changes after launch

Use their answer to the frequency question:
- **Never / now and then:** use the same no-secret route each time.
- **Regularly:** after the first launch, offer to set up a repeatable route once (a connected static host, or a credential with narrow access and an expiry date), and explain the trade-off in one sentence: "It takes ten minutes now, and after that I can update your site whenever you ask, without you logging in." If they decline, keep using the no-secret route.
