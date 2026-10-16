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
- **Favicon and page titles** on every page.
- **Contact forms** need somewhere to send messages. Options, simplest first: a form service with a free plan (the person signs up with their email and you paste the form address in), a `mailto:` link, or an endpoint they already run. If none is set up, don't fake success. Show the email address instead, or tell the owner plainly.
- **No unlicensed media.** Photos of real people only if supplied with permission. Embeds (videos, maps) via the provider's own embed or link.
- **Unofficial sites** about real people or brands: "Unofficial fan site, not affiliated with ..." in header and footer.

## 4. QA before showing "final"

Run a real browser (e.g. Playwright) over every page, at desktop and phone widths:

- [ ] Every page loads with no console errors
- [ ] No horizontal overflow at 360–1440 px
- [ ] Every internal link resolves; every `#anchor` exists; external links open in a new tab with `rel="noopener"`
- [ ] Every image loads (not broken, not a placeholder)
- [ ] Interactive parts work: menu, filters, search, form states
- [ ] Facts and links verified against sources (e.g. each external link goes where its label says)
- [ ] Share tags present on every page and the share image is 1200×630
- [ ] Text is readable: sensible contrast, no text over busy images without an overlay
- [ ] Screenshots of every page saved for the approval message

## 5. Approval

Send the screenshots (desktop for each page plus the homepage on a phone) and ask for a clear "yes, publish". Make every change they ask for, re-run QA, and show it again before publishing.
