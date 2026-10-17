# Running it like an engagement

A good agency feels calm to work with because the client always knows three things: what's happening now, what they need to do, and what comes next. This file is how the skill gives that feeling.

## The project file

Keep one file for the whole job: `project.json`, managed by `scripts/project.py`. It holds the business facts, decisions, approvals, open items and what's live. It is the memory of the engagement.

```
python scripts/project.py init "Maria's Bakery" --domain mariasbakery.com --mode self
python scripts/project.py set goal "Get pickup orders"                  # any field, dot paths ok
python scripts/project.py fact "Hours: Tue–Sun 7am–3pm" --source "Google profile"
python scripts/project.py decide "Warm & local style" --why "Owner picked style 3"
python scripts/project.py todo "Owner: send 5 photos of the shop" --owner owner
python scripts/project.py approve brief                                  # records the sign-off, with date
python scripts/project.py brief    > brief.md                            # the one-page brief
python scripts/project.py status                                         # where things stand, in plain words
```

- **Create it as soon as you know the business name.** Update it as you go; don't batch.
- **Every fact that will appear on the site goes in with its source.** No source, no fact on the site.
- **When a conversation resumes** (new day, new device, `project.json` attached), run `status` first and pick up from there. Never re-ask anything the file already answers.
- **On-behalf mode:** set `--mode behalf` and record the owner's name and how to reach them.
- **Send the owner the latest `project.json` at the end of every phase** (with the recap), and tell them: "If we pick this up in a new chat, attach this file and say you're back." A new chat can't see earlier files on its own. If the conversation is linked to their computer, also save it in their folder.
- At handover it becomes their record of the job.

## The five phases and their gates

Each phase ends with a short recap and a **clear yes** from the owner before the next one starts. Record each yes with `project.py approve <gate>`. If they say "looks fine, carry on", that's a yes. Silence is not.

| # | Phase | Ends with | Gate |
|---|---|---|---|
| 1 | **Discovery** — interview, look and feel, competitor scan, facts gathered | The one-page brief | `brief` |
| 2 | **Look** — two directions, then refinements | The chosen direction | `look` |
| 3 | **Build** — copy, full site, QA report | Full site + QA report + screenshots | `site` |
| 4 | **Go live** — access, DNS snapshot, publish, verify | Live site, verified | `golive` |
| 5 | **Handover** — handover document, access removal, one-week check | Handover document sent | `handover` |

Never skip a gate, even when the owner is in a hurry. When they are, make each gate a one-line yes ("Here's the brief in five lines. Good to go?").

## The one-page brief (end of discovery)

Generate it with `project.py brief`, then send it as a short message or a document. It has exactly these parts:

1. **The goal:** one sentence. ("Get more pickup orders from people nearby.")
2. **Who it's for, and what they should do:** the visitor and the main button.
3. **Pages:** names, one line each.
4. **Look:** the references or style they picked, and their logo/colours.
5. **Facts we'll use:** each with its source. Anything unconfirmed is listed as "left out until you confirm".
6. **Where it will live:** the web address and what detection found, in plain words.
7. **What I need from you:** photos, confirmations, logins they'll do themselves, with who and by when.
8. **What happens next:** the phases, roughly how long each takes, and the next gate.
9. **Not included:** legal pages, paid ads, stock photography, ongoing editing (unless agreed).

Keep it to one screen. A brief nobody reads is worse than no brief.

## Status recaps

At the end of each phase, and whenever the owner comes back after a gap, send a recap in this shape:

> **Where we are:** Phase 3 of 5, building the site.
> **Done since last time:** Copy for all 5 pages; full site built; QA report passed (2 small fixes made).
> **Waiting on you:** A yes on the full site (screenshots attached).
> **Next:** Once you say yes, I'll check your domain's email settings and put the site live.

## The decision log

Every choice that shapes the site goes in with its reason (`project.py decide`). Colours, page list, what was left out and why, which publishing route. When the owner later asks "why is it like this?", the answer is there, and the handover document lists the main decisions.

## Communication rules (on top of SKILL.md)

- **No surprises.** Say what you're about to do before anything changes, and what changed after.
- **One ask at a time from the owner,** with a clear "reply with X" so it's easy to answer.
- **Time estimates in plain terms** ("about 20 minutes of your time today, the rest is me").
- **Own mistakes in one line and show the fix.** Don't over-apologise.
- **Revisions:** two rounds per phase are normal. On a third, summarise what has changed so far and ask what would make it right, rather than tweaking at random.
