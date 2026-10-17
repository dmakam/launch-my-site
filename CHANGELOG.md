# Changelog

## v3.1 (Oct 2026): fixes from the first live test

Found by running scenario 2 (plumber with a domain only) in a fresh chat.

- **Address checked first.** If the owner gives a web address, it's checked in the first reply, before any design. In the test, the domain turned out to be for sale, which was only found after styles and logos.
- **Styles shown as pictures only.** Never offered as a list of words.
- **The brief is unskippable.** No design directions, logos or mockups before the owner's yes on the one-page brief; style cards are the only visuals allowed before it.
- **New "address for sale / expired / someone else's" case** (`detect-host.md`): how to check ownership, recover an expired address, or offer affordable alternatives with first-year and renewal prices.
- **Easier to start.** The skill description now covers casual requests ("make me a website", "get my business online", "redo my website"), and the docs recommend starting with "Use the Launch My Site skill to…".
- Evals: scenario 2 and the global rules now check address-first, picture-only styles and brief-before-design.

## v3 (Oct 2026): professional-services experience

The skill now runs like an agency engagement: a visible process, nothing missed, polished deliverables at every stage, and a clean handover.

### Engagement
- **Five phases with gates** (Discovery → Look → Build and check → Go live → Handover). Each ends with a recap and a clear yes (`references/engagement.md`).
- **Project file** (`scripts/project.py`): business facts with sources, decisions with reasons, to-dos for owner and builder, approvals with dates, what's live. Resumes across sessions with `status`. Refuses to store passwords or keys.
- **One-page brief** generated from the project file at the end of discovery.
- **Quick competitor scan** in discovery.

### Quality
- **Copywriting and local SEO** (`references/copy-and-seo.md`): voice, page rules, no filler, no invented facts; titles, descriptions, structured business data, sitemap, robots, 404, Google Business consistency.
- **QA report** (`scripts/qa_report.py`): pass/fail report with screenshots for a local folder or live site. Checks script errors, sideways scrolling at each width, images and descriptions, links and anchors, titles and descriptions, headings, share previews, favicon, phone tap targets and text size, placeholder text, forms that send nowhere, phone-number consistency, page weight, sitemap/robots/404 and business structured data.

### Launch and handover
- **Launch runbook** (`references/launch-runbook.md`): before/during/after checklists, redirects for old pages, rollback, one-week check.
- **Email protection** (`scripts/dns_snapshot.py`): records DNS before launch and fails loudly if email (MX), SPF, DMARC, DKIM or verification records changed afterwards.
- **Handover document** (`references/handover.md`): what's live, what was checked, what the owner owns, access removed, decisions, first 30 days, sources.

### Testing
- **Evals** (`evals/`): ten scripted owners (Wix bakery, plumber with domain only, lawyer on WordPress, on-behalf build, stuck owner, pushy owner, pasted password, unofficial fan site, returning owner, launch day) with must/should rules, a grading prompt, and fixtures. The QA report must catch all eight planted problems in `evals/fixtures/broken-site`.

### Docs
- **User guide** (`docs/how-to-use.md`).

## v2 (Oct 2026)

Found by running the skill end to end for a sample HVAC business.

### Look and feel
- **New required interview step** (`interview.md`, Round 3): asks for websites they like and any logo, photos or colours, in one message, before any design work.
- **Style cards** (`style-cards.md`, `scripts/style_cards.py`): renders four real homepage samples (Clean & bright, Bold & dark, Warm & local, Classic & formal) with the person's name, headline and button, as one image to send in chat. Used when they have no references.
- **Design directions** (`build.md`) now start from those answers, and say which answer each direction came from.

### Interview
- **Industry starters** (`industry-starters.md`): page lists, must-have sections and "ask" lists for home services, restaurants, salons, professional services and contractors.
- **Web address question** has a fallback for people who aren't sure what it is.
- **The frequency question** ("how often will you want changes?") is now asked before any publishing route is proposed.

### Hosting and publishing
- **Detection can't be shortcut** (`detect-host.md`): always ask for the address and run the detector, even if a connector lists the person's domains.
- **Plain-language confirm scripts** for each situation, plus "don't recognise the company" and "can't tell" scripts.
- **Capability check and decision table** (`publish-routes.md`): the rung is picked from the situation, the tools in this session and the person's answers. A connector only counts as rung 1 if it can publish files.
- **Browser permission script**: say what you'll do, that they type their own password, and that they can stop you, then wait for a yes.

### Ground rules (`SKILL.md`)
- **Personal context doesn't decide the route.** Memory, saved preferences and connector account data are used only when the person brings them up in this conversation.
- **Ask before buying anything.** Show first-year and renewal prices.
- **Their logo is used as supplied.**
- **Unconfirmed facts stay off the site.**
- **The flow is now numbered 1–10**, with look and feel before design and frequency before credentials.
