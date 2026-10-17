---
name: launch-my-site
description: Builds a professional website from a conversation and publishes it to the person's own domain and hosting, for people with no technical knowledge. Use whenever someone wants a website for a business, shop, practice, event or themselves, in any wording ("make me a website", "get my business online", "I need a site for my shop", "redo my website", "put my site live on my domain"), wants an existing site replaced or redesigned, or is building a site on someone else's behalf. Handles existing hosting, WordPress, site builders (Wix, Squarespace, Shopify and similar) and no hosting at all.
---

# Launch my site

You take someone from "I want a website" to a live, checked site on their own domain, in about an hour, while assuming they know nothing about hosting, files, DNS or passwords. The hard part is not writing the HTML. It is getting the files onto *their* hosting without making them handle things they don't understand. This skill is mostly about that.

Every decision in this flow is made from **what the person tells you** and **what tools this session actually has**. Not from what you happen to know about them. See "Personal context" under Ground rules.

## Two modes

Ask once, near the start, if it isn't obvious:

- **Self-serve.** The site owner is the person talking to you. You guide them and publish with their help.
- **On behalf.** A builder (a freelancer, a friend, a consultant) is building for a site owner who isn't in the conversation. Access must come *from the owner to the builder*. See `references/on-behalf.md`.

## The flow: five phases, each with a gate

Run the job like a professional engagement (`references/engagement.md`). Keep a project file from the first answer (`scripts/project.py init`), record facts with their sources and every decision with its reason, and end each phase with a short recap and a **clear yes** before starting the next. Never skip a gate; when the owner is in a hurry, make it a one-line yes. When a conversation resumes, read the project file (`project.py status`) and pick up where it left off without re-asking.

**Phase 1: Discovery** → gate `brief`
1. **Check the address first** (`references/detect-host.md`). If they gave a web address, check it **before anything else**, in your first reply: run `scripts/detect_site.py` (or open the address if the script can't run) and tell them what you found in plain words. If they didn't give one, ask for it early. A problem with the address (it's for sale, owned by someone else, expired, on a site builder) changes the whole plan, so it must surface before any design work.
2. **Get to know the business** (`references/interview.md`, Rounds 1–2). Short, friendly questions, never more than four in a message. Use `references/industry-starters.md` to ask only about the gaps. Pull facts from links they give (old site, Google profile) instead of asking.
3. **Look and feel** (`references/interview.md`, Round 3). **Required, every time.** Websites they like, logo, colours. No references: show the style cards **as a picture** (`references/style-cards.md`). Never offer styles as a list of words to choose from.
4. **Quick competitor scan:** look at two or three local competitors' sites and note, in plain words, what to do better. Ask how often they'll want changes after launch.
5. **The one-page brief** (`project.py brief`). Send it and get a yes. **No design directions, logos or mockups before this yes.** Style cards in step 3 are the only visuals allowed before the brief. When the owner is impatient, make the brief five lines and the yes one word, but never skip it.

**Phase 2: Look** → gate `look`
6. **Two design directions** (`references/build.md`, section 2) from their look-and-feel answers, with desktop and phone screenshots. Refine on their reactions (two rounds is normal).

**Phase 3: Build and check** → gate `site`
7. **Copy first** (`references/copy-and-seo.md`): voice, page-by-page wording, only confirmed facts. Owner reviews it.
8. **Build the full site** (`references/build.md`, section 3) with local SEO built in.
9. **QA report** (`scripts/qa_report.py`): no "must fix" items left. Send the report with screenshots of every page and get the yes.

**Phase 4: Go live** → gate `golive`
10. **Agree the publishing route** (`references/publish-routes.md`): capability check, decision table, easiest route first.
11. **Follow the launch runbook** (`references/launch-runbook.md`): DNS snapshot so email is protected, redirects for old pages, backup, publish, then verify on the live address (verify, QA, email check, form test, SSL).

**Phase 5: Handover** → gate `handover`
12. **Handover document** (`references/handover.md`): what's live, what was checked, what they own, access removed, decisions, first 30 days. Offer the one-week check.

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
- **Protect their email.** Take a DNS snapshot before any address change, change only the website records, and confirm email records are unchanged afterwards (`scripts/dns_snapshot.py`).
- **Back up before replacing.** Every deploy saves what it overwrites. Nothing is permanently deleted. Old files are left in place or moved aside, never wiped.
- **Ask before using their browser.** Before operating their browser or computer, say what you'll do, that they type their own password, and that they can stop you any time. Wait for a yes.
- **Ask before buying anything.** Domains, hosting or paid plans are the person's decision. Show the price, including the renewal price, and wait for a clear yes.
- **No impersonation.** If the site is about a real person, brand or organisation that the person doesn't represent, it must say clearly that it's unofficial (header and footer), and it must not copy their logos or branding.
- **Images must be theirs or properly licensed.** Use photos they supply and have the right to use, or none. Don't pull photos of real people off the web.
- **Their logo is used as supplied.** Never redraw, re-letter or recolour it. If they have no logo, use a simple wordmark of the business name and say it's a placeholder.
- **Facts must be checked.** Anything presented as a fact (numbers, history, licences, credentials, reviews) comes from the person or a source you looked up, and you list sources for the owner. Unconfirmed facts stay off the site.
- **Working forms only.** If the site has a contact or booking form, it either delivers messages somewhere (see `build.md`) or you tell the owner plainly that it doesn't yet.

## Files in this skill

- `references/engagement.md`: phases and gates, the project file, the one-page brief, recaps, decision log
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
- `references/copy-and-seo.md`: voice, copywriting rules, local SEO and structured data
- `references/build.md`: research, design directions, building, QA
- `references/launch-runbook.md`: before/during/after launch, email protection, redirects, rollback, one-week check
- `references/handover.md`: the handover document and message
- `references/plain-language.md`: phrasebook
- `scripts/project.py`: the project file (facts, decisions, to-dos, approvals), the brief and status recaps
- `scripts/detect_site.py`: figure out host, platform and what's live from a domain
- `scripts/dns_snapshot.py`: record DNS before launch and confirm email records are unchanged after
- `scripts/qa_report.py`: pass/fail QA report with screenshots, for a local folder or a live site
- `scripts/deploy_cpanel.py`, `scripts/deploy_sftp.py`, `scripts/publish_wordpress.py`: credential-based publishing with backup and safety checks
- `scripts/verify_live.py`: quick check of every page, image and the share preview on the live domain
- `evals/`: scripted owner scenarios and a grading prompt; run them before releasing changes
