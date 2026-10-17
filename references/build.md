# Building the site

## 1. Research before design

- Read every link the person gave you. Search for anything you'll state as fact: current numbers, titles, dates, addresses, opening hours.
- Keep a source list. It goes in the handover, and facts on the page should match it.
- Gather real content: names, services, prices, testimonials *they* provided. Never invent testimonials, reviews, awards or statistics.

## 2. Two directions, quickly

Start from the look-and-feel answers (`interview.md`, Round 3). Don't design until you have one of: websites they like, their logo or colours, or a style-card pick (`style-cards.md`).

Make two small homepage directions (hero section plus one content section each) that both respect what they chose, and differ in one clear way. For example, if they picked "Clean & bright": one calm and minimal, one with more motion and a bolder headline. If they sent two reference sites: one leaning on each.

- Use their real name, headline, main button and logo. No invented facts.
- Screenshot each at desktop (1440 px) and phone (390 px) and send the images. Don't only describe them.
- Say in one line how they differ and which of their answers each one came from: "A follows the site you liked; B is the same idea with your truck's red."
- Ask which is closer and what to change. Treat their reactions as the spec. Personal details count ("he always wears black" → black-and-white palette).

## 3. Build

- **Plain static files**: `index.html` plus one HTML file per page, an `assets/` folder for CSS, JS and images. Works on every route in this skill.
- **One shared stylesheet and script**, linked with a version: `assets/styles.css?v=1`. Bump the number on every republish.
- **Mobile-first and responsive**: test at 360, 390, 768, 1024 and 1440 px widths with no sideways scrolling.
- **Polish matters.** Default to a design with depth: subtle gradients or textures, considered typography, scroll-reveal animation, hover states. Respect `prefers-reduced-motion`.
- **Fonts**: a web font from a reliable CDN, with a system-font fallback.
- **Share preview**: create a 1200×630 image (`assets/og-image.png`) and add Open Graph and Twitter tags on every page (`og:title`, `og:description`, `og:image` as an absolute https URL, `og:url`, `twitter:card=summary_large_image`). Without this, links shared in chats and social posts show a blank box.
- **Favicon, unique page titles and search descriptions** on every page (`copy-and-seo.md`).
- **Local SEO files:** `sitemap.xml`, `robots.txt` (pointing to the sitemap), a friendly `404.html` with the phone number, and `LocalBusiness` structured data on the homepage using only confirmed facts.
- **Contact forms** need somewhere to send messages. Options, simplest first: a form service with a free plan (the person signs up with their email and you paste the form address in), a `mailto:` link, or an endpoint they already run. If none is set up, don't fake success. Show the email address instead, or tell the owner plainly.
- **No unlicensed media.** Photos of real people only if supplied with permission. Embeds (videos, maps) via the provider's own embed or link.
- **Unofficial sites** about real people or brands: "Unofficial fan site, not affiliated with ..." in header and footer.

## 4. QA report before showing "final"

```
python scripts/qa_report.py site/ --out qa --expect-phone "(555) 010-0100"
```

It checks every page at phone, tablet and desktop widths: script errors, sideways scrolling, images and their descriptions, links and #anchors, titles and search descriptions, headings, share previews, favicon, tap targets and text size on phones, placeholder text, forms that send nowhere, phone number consistency, page weight, sitemap/robots/404 and business structured data. It writes `qa/qa-report.md` and screenshots of every page.

- Fix every "must fix" item, then re-run until it passes. Fix warnings unless there's a reason not to, and note the reason in the project file.
- Also check by eye what a script can't: facts match their sources, copy matches the approved wording, interactive parts (menus, filters) work, text is readable over images.
- For high-stakes builds, ask a second agent that didn't build the site to review it against the brief and the sources.

## 5. Approval (gate `site`)

Send the QA report summary, screenshots (desktop for each page plus the homepage on a phone) and ask for a clear yes. Make every change they ask for, re-run the QA report, and show it again. Record the yes with `project.py approve site`.
