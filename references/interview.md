# The interview

Goal: enough to build something good, in as few questions as possible. Ask one or two at a time, conversationally. Skip anything you can look up yourself from links they give you. Don't skip a question because you think you already know the answer from outside this conversation (see "Personal context" in SKILL.md).

## Round 1: what and who (always)

1. **"What's the website for?"** A business, a person, an event, a project, a fan page, a portfolio?
   - Changes: page list, tone, whether you need a booking/contact form, which industry starter applies.
2. **"Who should feel what when they land on it, and what should they do next?"** Prompt with examples if they're stuck: "Customers should trust you enough to call", "Fans should feel inspired", "Recruiters should see your work fast."
   - Changes: the homepage story and the main button. A good structure is *Feel → Do → Believe*: make them feel the problem or the origin, show what you do, then give proof.

## Round 2: content (ask, but offer to find it)

3. **"Is there anything I should read first?"** An existing site, Google Business profile, social profiles, a menu, a brochure. Offer: "Send me links and I'll pull the details myself."
4. **Industry gaps.** If `industry-starters.md` has their business type, send its "Ask" list as one message with tickable options. Example for HVAC: "Which of these do you offer? AC repair, new systems, heating repair, tune-ups, duct work, 24/7 emergency. And what can I show as proof: licence number, years in business, warranties, real reviews?"
   - Anything they don't confirm stays off the site. Never invent services, credentials or reviews.

## Round 3: look and feel (required, every time)

Ask this as one message, before any design work:

> Before I design anything, two quick ones about the look:
> 1. **Are there any websites you like the look of?** They can be from any industry, even a competitor. Send the links, or just say "no idea."
> 2. **Do you have a logo, photos, or colours you already use**, like on your truck, sign, uniforms or business cards? A phone photo is fine.
>
> If nothing comes to mind, no problem. I'll show you a few style samples with your name on them and you can pick.

Then branch:

- **They send sites they like.** Open each one. Say back in plain words what you'll take from it: "Clean and white like the first one, big phone number at the top like the second." Get a nod, then build the two directions from that.
- **They send a logo, photos or colours.** Both directions use them. The logo is used exactly as supplied, never redrawn or recoloured. Pull the main colours from it.
- **"No idea" or no answer.** Render style cards (`style-cards.md`) with their name, headline and button, send the image, and ask which is closest. Don't move on to directions without a pick.
- **Never offer styles as words only** ("1. Bold & local, 2. Clean & modern, 3. Friendly family"). Owners can't judge a style from a label. If the script can't run, build quick visual samples another way (screenshots of simple HTML), but always show pictures.
- **No logo.** Say you'll use the business name in a clean font as a placeholder, and that a real logo can drop in later.

Style cards are the only visuals before the brief is approved. Design directions, logos and mockups come after the owner's yes on the brief (Phase 2).

Don't ask about fonts or colours in the abstract ("What colour scheme do you want?"). Their reactions to pictures ("too dark", "more formal", "he always wears black") are the real spec.

## Round 4: the practical bits

5. **"What's the web address for your business?"** Add a fallback for people who aren't sure: "That's the address people type to find you, like yourbusiness.com. It's often on your business card or email signature. If you don't have one yet, that's fine." No address means the no-hosting route.
6. **Don't ask who they pay for hosting.** Run `detect_site.py` and *tell them* what you found (`detect-host.md`). Only ask if detection is unclear.
7. **"After it's live, how often will you want to change things?"** Never / now and then / regularly. **Ask this before proposing any publishing route.** It decides whether a repeatable route (and possibly a credential) is worth setting up.
8. **On behalf mode only: "Who owns the domain and hosting, and how do you usually reach them?"** See `on-behalf.md`.

## What not to ask

- Technical questions they can't answer ("Static or dynamic?", "Do you have SSH?", "What's your docroot?", "Do you have cPanel?"). Detect or decide it yourself.
- Things you can look up from links they gave you (business hours on their Google profile, facts on their existing site).
- Legal pages unless they ask. Mention once, at handover, if their site collects personal data.

## Summarise before designing: the one-page brief

Record answers in the project file as you go (`scripts/project.py`, see `engagement.md`). At the end of discovery, send the one-page brief (`project.py brief`) and get a yes (`project.py approve brief`). In conversation it can be as short as:

> Here's what I'll make: a 5-page site for Northside Heating & Air: Home, Services, About, Service Areas, Book Online. Two main buttons everywhere: "Call (555) 010-0100" and "Book online". It'll use the clean, bright style you picked, with your logo and truck photos. I'm leaving out reviews until you send some. Sound right?

If the publishing route isn't settled yet (that happens in the Go live phase), say so: "I've checked where your address is hosted. Once the site is approved, we'll pick the easiest way to put it live."
