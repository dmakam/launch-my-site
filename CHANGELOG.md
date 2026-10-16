# Changelog

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
