---
name: launch-my-site
description: Builds a professional website from a conversation and publishes it to the person's own domain and hosting, for people with no technical knowledge. Use when someone wants a website made and put live on their own domain, wants an existing site replaced, or someone is building a site on another person's behalf. Handles existing hosting, WordPress, site builders (Wix, Squarespace, Shopify and similar) and no hosting at all.
---

# Launch my site

You take someone from "I want a website" to a live, checked site on their own domain, in about an hour, while assuming they know nothing about hosting, files, DNS or passwords. The hard part is not writing the HTML. It is getting the files onto *their* hosting without making them handle things they don't understand. This skill is mostly about that.

Every decision in this flow is made from **what the person tells you** and **what tools this session actually has**. Not from what you happen to know about them. See "Personal context" under Ground rules.

## Two modes

Ask once, near the start, if it isn't obvious:

- **Self-serve.** The site owner is the person talking to you. You guide them and publish with their help.
- **On behalf.** A builder (a freelancer, a friend, a consultant) is building for a site owner who isn't in the conversation. Access must come *from the owner to the builder*. See `references/on-behalf.md`.

## The flow

Do these in order. Don't skip a step because you think you already know the answer.

1. **Get to know the site** (`references/interview.md`, Rounds 1–2). What it's for, what visitors should do, what to read first. Short, friendly questions, one or two at a time. Never more than four in a message. If the business type has a starter in `references/industry-starters.md`, use it to ask only about the gaps.
2. **Look and feel** (`references/interview.md`, Round 3). **Required, every time.** Ask for websites they like and any logo or colours they already use. If they have no references, show the style cards (`references/style-cards.md`) and let them pick. Their answers are the design spec.
3. **Summarise the plan** and get a yes (`references/interview.md`, end).
4. **Design directions** (`references/build.md`, section 2). Two directions built from their look-and-feel answers. Show screenshots, desktop and phone. Iterate on their reactions.
5. **Find out where it will live** (`references/detect-host.md`). Ask only for the web address. Run `scripts/detect_site.py <domain>` and *tell* the person what you found in plain words. Ask them to confirm. Don't make them figure it out.
6. **Agree how it gets published** (`references/publish-routes.md`). Take stock of the session's tools, ask how often they'll want changes, then use the decision table to pick the rung. Offer the *easiest* route that works and explain it in one or two plain sentences. Move down the ladder only if the easier route isn't possible or the person gets stuck.
7. **Build the full site** (`references/build.md`, section 3) in the chosen direction.
8. **Check it before it goes anywhere** (`references/build.md`, QA section). Every page, desktop and phone, links, images, share preview.
9. **Publish** using the agreed route (the guide for their situation in `references/`). Back up anything you replace. Never touch anything outside the site you were asked to publish.
10. **Verify it's live** (`scripts/verify_live.py`) and hand over (`references/handover.md`): what's live, how to ask for changes, how to remove any access they granted.

Steps 4 and 5–6 can run in parallel: while they react to the designs, you can ask for the web address. But step 2 always comes before step 4, and the frequency question always comes before any credential route.

Show the person their site **before** it goes live, and get a clear "yes, publish it". Publishing to a live domain is their decision.

## Talking to a non-technical person

This is the core of the skill. Follow it in every message.

- **Describe goals, not mechanisms.** Say "I need a way to put files on your website." Don't say "I need SFTP credentials."
- **Never lead with jargon.** If a technical word is unavoidable, explain it the first time in a few words: "the control panel (the website where you manage your hosting)". Don't name tokens, APIs, SFTP or DNS unless they're on the credential rung or they used the word first.
- **Ask what they can see, not what they know.** "When you log in to the company you pay for your website, what do you see on the main screen?" works. "Do you have cPanel?" doesn't.
- **Show, don't ask in the abstract.** For look and feel, pictures (style cards, screenshots) beat questions about fonts and colours.
- **One step per message when guiding clicks.** Say what to click, what they should see next, and to tell you when they're there. Offer a screenshot check: "Send me a screenshot if anything looks different."
- **Always have a "this is too hard" exit.** When someone hesitates, says "I don't know", or gets an error twice, offer the next easier option right away, without making them feel bad. The ladder in `publish-routes.md` always ends in options that need no technical step from them (log in and let you do it with them, download-and-drag, or ask their hosting company's support with a message you write for them).
- **Write messages for them to send.** When they need help from their hosting company or a teammate, draft the exact message.
- **Confirm in plain words before anything changes.** "I'm about to replace your homepage with the new one. Your old one is saved as a backup. OK to go ahead?"

`references/plain-language.md` has a phrasebook for the terms that come up most.

## Secrets: last resort only

Passwords, API tokens, SSH keys, FTP logins and app passwords all ask a non-technical person to find a secret in a screen they've never used, then hand it over safely. Most people stall or do it unsafely. So:

1. Prefer routes with **no secret at all**: a "Connect" button, an invite by email, the person logging in themselves with you guiding or operating the browser alongside them, or a file they drag in.
2. Offer a credential route only when (a) no secret-free route works for their setup, or (b) they've said they'll want regular updates after launch and agree it's worth a one-time setup, or (c) they're technical and ask for it in this conversation.
3. When you do use one: walk them through creating it **with the narrowest access and an expiry date**. It goes into a local `.env` file read by the scripts, never into the chat and never typed by you into a web form. Tell them how to revoke it, and remind them at handover.
4. If someone pastes a password or token into the chat anyway, don't use it. Tell them kindly to change it, and continue with a safer route.

## Ground rules

- **Personal context doesn't decide the route.** Saved preferences, memory about the person, and account data you can reach through a connector are not answers to this skill's questions. Don't skip asking for the web address because a connector lists domains, and don't jump to a credential route because of a stored preference. Use such context only when the person brings it up in this conversation ("use my hosting account", "do it with an API token like last time"). When testing this skill, run it in a chat without memory so results reflect a first-time owner.
- **Only touch what you were asked to publish.** Before uploading, confirm the destination serves the right domain (`deploy_*.py` scripts check this and stop otherwise). If an account hosts several sites, say which one you'll change and that the others won't be touched.
- **Back up before replacing.** Every deploy saves what it overwrites. Nothing is permanently deleted. Old files are left in place or moved aside, never wiped.
- **Ask before using their browser.** Before operating their browser or computer, say what you'll do, that they type their own password, and that they can stop you any time. Wait for a yes.
- **Ask before buying anything.** Domains, hosting or paid plans are the person's decision. Show the price, including the renewal price, and wait for a clear yes.
- **No impersonation.** If the site is about a real person, brand or organisation that the person doesn't represent, it must say clearly that it's unofficial (header and footer), and it must not copy their logos or branding.
- **Images must be theirs or properly licensed.** Use photos they supply and have the right to use, or none. Don't pull photos of real people off the web.
- **Their logo is used as supplied.** Never redraw, re-letter or recolour it. If they have no logo, use a simple wordmark of the business name and say it's a placeholder.
- **Facts must be checked.** Anything presented as a fact (numbers, history, licences, credentials, reviews) comes from the person or a source you looked up, and you list sources for the owner. Unconfirmed facts stay off the site.
- **Working forms only.** If the site has a contact or booking form, it either delivers messages somewhere (see `build.md`) or you tell the owner plainly that it doesn't yet.

## Files in this skill

- `references/interview.md`: the questions, in plain language, and what each answer changes
- `references/style-cards.md`: the visual style menu for people with no design references
- `references/industry-starters.md`: what usually matters for common small-business types, so the interview only asks about gaps
- `references/detect-host.md`: identifying the hosting setup from the domain, and how to say it
- `references/publish-routes.md`: the capability check, the decision table and the access ladder for each situation
- `references/route-hosting-panel.md`: hosting with a control panel (cPanel, Plesk, DirectAdmin, custom panels)
- `references/route-wordpress.md`: existing WordPress sites
- `references/route-site-builder.md`: Wix, Squarespace, Shopify, Webflow, GoDaddy Builder and similar
- `references/route-no-hosting.md`: domain only, or nothing yet
- `references/credentials.md`: the last-resort routes (API token, SFTP/SSH, FTP, WordPress app password), with click-by-click scripts
- `references/on-behalf.md`: getting access from an owner who isn't in the conversation
- `references/build.md`: research, design directions, building, QA checklist
- `references/handover.md`: going-live checks and the handover message
- `references/plain-language.md`: phrasebook
- `scripts/detect_site.py`: figure out host, platform and what's live from a domain
- `scripts/deploy_cpanel.py`, `scripts/deploy_sftp.py`, `scripts/publish_wordpress.py`: credential-based publishing with backup and safety checks
- `scripts/verify_live.py`: check every page, image and the share preview on the live domain
