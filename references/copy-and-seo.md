# Copywriting and local SEO

The words are half of what makes a site look professional. Generic copy ("We are committed to excellence") reads as cheap no matter how good the design is. Write the copy as its own step, show it to the owner, and get a yes before it goes into the design (it can be approved together with the full site at the `site` gate if the owner prefers fewer steps).

## Voice

Before writing, set the voice in three lines and record it (`project.py set voice "…"`):

- **Who's talking:** "the owner, first person plural" (we) or "the business" (it). Small businesses usually sound best as "we".
- **Three words for the tone**, taken from the owner's own words where possible: "straight-talking, warm, local".
- **Words they use, and words to avoid.** If the owner says "AC", don't write "HVAC solutions". If they say "we'll come out", don't write "on-site service".

## Rules for every page

- **Say what it is, for whom, and where, in the first screen.** "AC repair and installation in Springfield and nearby towns."
- **Benefit first, then the fact behind it.** "Know the price before we start: every repair is quoted upfront." Not "Upfront quotes."
- **Specific beats impressive.** "We call back within an hour, 7am–7pm" beats "Fast, reliable service". Only use specifics the owner confirmed.
- **One idea per section, short paragraphs**, headings a skim-reader can follow on their own.
- **Every page ends with the main action** (call, book, order), worded as the visitor would say it: "Book a repair", not "Submit".
- **Never invent:** no reviews, numbers, awards, licences, years in business or guarantees that aren't in the project file with a source.
- **No filler words:** "solutions", "world-class", "passionate about", "one-stop shop", "cutting-edge", "seamless", "elevate".
- **Read it aloud.** If a sentence sounds like an ad, rewrite it like the owner talking to a customer at the counter.

## How to present copy to the owner

Send it page by page in plain text (not inside the design), with a line on top: "Here's the wording. Change anything that doesn't sound like you." Track their edits; they are the best voice guide you'll get. Update the voice line if they consistently change something.

## Local SEO basics (every site)

Most small businesses are found by "[service] near me" and "[service] [town]" searches. Do these on every build:

- **Page titles:** `Service in Town | Business name` for service pages, `Business name | Main service in Town` for the homepage. Unique on every page, under 65 characters.
- **Search descriptions:** one plain sentence per page, 50–160 characters, with the town and a reason to click.
- **One H1 per page** that says what the page is about, in words people search.
- **Name, address, phone (NAP) identical everywhere:** site footer, contact page, structured data, and their Google Business profile. Mismatches confuse Google. If the owner has a Google Business profile, match it exactly (or tell them what to update there).
- **Structured data:** a `LocalBusiness` block (or a more specific type such as `HVACBusiness`, `Bakery`, `Restaurant`, `Dentist`) in JSON-LD on the homepage, using only confirmed facts:

```html
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"HVACBusiness","name":"…","url":"https://…","telephone":"+1-…",
 "address":{"@type":"PostalAddress","streetAddress":"…","addressLocality":"…","addressRegion":"…","postalCode":"…","addressCountry":"US"},
 "areaServed":["…","…"],"openingHours":["Mo-Fr 07:00-19:00"],"image":"https://…/og-image.png"}
</script>
```
  Service-area businesses without a public address: leave out `streetAddress`, keep `areaServed`.
- **Service area pages** only if the owner serves distinct towns and there's something true and specific to say about each. Never generate near-identical town pages; Google treats them as spam.
- **`sitemap.xml` and `robots.txt`** in the site root (the build generates both; `robots.txt` points to the sitemap).
- **Image file names and descriptions** in plain words ("ac-unit-install-springfield.jpg", alt "Technician installing a new outdoor AC unit").
- **A real 404 page** that links back home and shows the phone number.
- **Fast pages:** compressed images (WebP or JPEG at sensible sizes), no huge background videos on phones. The QA report flags heavy pages.

## After launch (goes in the handover document)

- Submit the sitemap in Google Search Console (owner's account; write the steps for them).
- Update the Google Business profile's website link to the new address.
- Ask five happy customers for a Google review this month (give them the exact message to send).
