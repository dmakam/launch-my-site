# Finding out where the site lives

The person shouldn't have to know what hosting is. Get the domain, detect the rest, then confirm in plain words.

**Don't shortcut this step** with account data a connector happens to expose (a list of their domains, a hosting dashboard) or with what you remember about them. Ask for the address and run the detector. A connector becomes useful later, when the person has confirmed which company it is and you're choosing how to publish (`publish-routes.md`).

## Step 1: ask for the address, nothing else

> What's the web address for your business, like yourbusiness.com? It's the address people type to find you, and it's often on your business card or email signature. If you don't have one yet, that's fine. Just tell me.

## Step 2: run the detector

```
python scripts/detect_site.py example.com
```

It needs only `requests` and uses public DNS-over-HTTPS, so it works anywhere. It reports:

- **Registrar hints and nameservers**: who controls the domain's settings (DNS). Nameservers often name the host or DNS provider.
- **Where the website points (A/CNAME)**: the server or platform actually serving it.
- **What's live now**: HTTP status, redirects, server headers, and page fingerprints.
- **Platform**: WordPress, Wix, Squarespace, Shopify, Webflow, GoDaddy Website Builder, Weebly/Square, Carrd, Framer, Ghost, a static host (Netlify, Vercel, Cloudflare Pages, GitHub Pages), a hosting "parked" or "coming soon" page, or nothing at all.
- **Control panel hints**: whether the server answers like a typical control-panel host (cPanel, Plesk, DirectAdmin ports), which suggests file-based hosting.
- **A plain-language summary** you can adapt for the person.

## Step 3: map the result to a situation

| What you found | Situation | Guide |
|---|---|---|
| WordPress site | Existing WordPress | `route-wordpress.md` |
| Wix / Squarespace / Shopify / Webflow / builder fingerprints, or nameservers/A records pointing at a builder | Site builder | `route-site-builder.md` |
| Generic web server, a hosting "default page", "coming soon", or an empty/simple HTML site; control-panel ports open | Hosting with a control panel | `route-hosting-panel.md` |
| Static host (Netlify, Vercel, Cloudflare Pages, GitHub Pages) | Already on a static host | `route-no-hosting.md`, "already on a static host" section |
| Domain doesn't resolve, registrar parking page, "domain for sale", or no domain yet | No hosting | `route-no-hosting.md` |

If signals conflict (for example nameservers at one company and the site at another), that's normal: the domain's settings live in one place and the website in another. Note both. Publishing happens where the *website* lives; pointing a domain somewhere new happens where the *DNS* lives.

## Step 4: confirm, don't quiz

Say what you found and ask for a yes. Use the wording for their situation:

- **Hosting with a control panel:**
  > I looked up yourbusiness.com. Your domain and website are both with **Company A**, and right now it shows a "coming soon" page. Does that sound like who you pay for your website?
- **Domain and website at different companies:**
  > The address is registered with **Company A**, and the website itself is hosted by **Company B**. Does that sound right?
- **WordPress:**
  > Your site is a **WordPress** site hosted with **Company B**. Do you want the new design to replace it, or should I keep WordPress so you can still edit pages yourself?
- **Site builder:**
  > Your site is built on **Wix**. Wix doesn't accept a site built somewhere else, so we have a few options. I'll explain them in a minute.
- **Domain only:**
  > You own the address through **Company A**, but there's no website on it yet. Do you remember buying hosting along with it? Many people already pay for some without knowing.
- **No address yet:**
  > No problem. Tell me a few names you like and I'll check which are available and what they cost, including the yearly renewal. I won't buy anything without your OK.

## If they don't recognise the company name

> That's normal. Search your email for "yourbusiness.com" or "hosting". You'll usually find a receipt from the company. Or check your card statement for a yearly charge. I'll wait.

## When detection can't tell

- Behind a security service (requests are challenged or blocked):
  > I can't see who's behind your site from the outside. When you log in to the company you pay for your website, what do you see on the main screen? A screenshot works too.
- Nothing live and no clear host: treat as no hosting, but ask "Do you remember buying hosting along with the domain?" before recommending anything new.
