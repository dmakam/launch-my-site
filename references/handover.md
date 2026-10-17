# Going live and handing over

The handover is the last impression of the whole job. A professional handover leaves the owner knowing exactly what they have, what they own, what's been removed, and what to do next, without needing to ask.

## Verify on the real domain

Follow `launch-runbook.md`, sections 3 and 4. At minimum:

```
python scripts/verify_live.py https://theirdomain.com
python scripts/qa_report.py https://theirdomain.com --out qa-live --expect-phone "…"
python scripts/dns_snapshot.py theirdomain.com --compare dns-before-theirdomain.com.json
```

If a page returns 403 to the scripts but loads in a browser, it's usually the host's bot protection. Check it in a real browser before worrying.

## The handover document

Send a short document (a file or a document artifact the owner can keep), not just a chat message. Build it from `project.json`. Sections, in this order:

1. **Your site is live** — the address(es), the date, and screenshots of the homepage on desktop and phone.
2. **What's on it** — the pages, one line each.
3. **What we checked** — "Every page on phone, tablet and desktop; all links and images; your phone number on every page; the contact form delivered a test message to [email]; your email settings are unchanged." Attach the QA report.
4. **What you own** — the domain (where it's registered), the hosting (with whom), the site files (backup location), any accounts created for the site (form service, analytics), all in the owner's name.
5. **Access I had, and how it was removed** — each item and its status: "WordPress user 'helper' — deleted on [date]" or "You logged in yourself; I had no separate access." If anything is still active (a token kept for future updates), say what it is, when it expires, and the exact steps to remove it.
6. **Your old site** — where the backup is, and the one step to restore it if ever needed.
7. **Decisions we made** — the main ones from the decision log, with the reason. ("We left out reviews until you have a few on Google.")
8. **Your first 30 days** — a short checklist:
   - Add the sitemap in Google Search Console (steps written out).
   - Update the website link on your Google Business profile, Facebook and Instagram.
   - Ask five happy customers for a Google review (the message to send is below).
   - Check the contact form once a week for the first month.
   - Send me any change you want; small changes are quick.
9. **How to ask for changes** — exactly what to say and where. If a repeatable route was set up: "Just tell me what to change." Otherwise: "We'll do the same quick log-in together."
10. **Not included** — the agreed list (legal pages, paid ads, stock photos…), so expectations stay clear.
11. **Sources** — where each fact on the site came from.

Keep it to two pages. Plain words, no jargon.

## The handover message

A short message that goes with the document:

> **Your site is live at theirdomain.com.** 🎉 Everything's in the attached handover document: what we checked, what you own, and a short checklist for the next 30 days.
>
> **The one thing to do this week:** [the most important item, e.g. update the website link on your Google Business profile].
>
> **If you see the old version:** press Ctrl+Shift+R (Cmd+Shift+R on a Mac). New visitors already see the new one.
>
> I'll check in on [date one week out] to make sure everything's still working[, if you'd like].

## One-week check

Offer it, and only schedule it if the owner says yes. Steps are in `launch-runbook.md`, section 5. Record the yes with `project.py todo "One-week check on [date]"`.

## Close the project

- `project.py approve handover`
- Give the owner `project.json` (their record of the job) along with the handover document.
- In on-behalf mode, send the owner their own copy, especially the access list and how to remove it.
