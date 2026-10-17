# Evals: test the skill before every release

Each scenario is a scripted business owner. You (or a second Claude) play the owner; the skill runs as normal. Then grade the transcript against the scenario's rules. A release ships only if every **must** rule passes in every scenario.

These test **behaviour** (what Claude asks, in what order, what it refuses to do), which is where regressions show up. The scripts have their own quick checks at the bottom.

## How to run a scenario

1. Open a **fresh chat with no memory** (in Claude, an incognito chat). Memory and saved preferences leak into the skill's choices and hide bugs.
2. Make sure the skill is installed and switched on.
3. Paste the scenario's **opening line**. Answer follow-up questions using only the **owner facts** in the scenario. If Claude asks something the facts don't cover, answer the way that owner plausibly would ("no idea", "whatever you think") and note it.
4. Stop at the **stop point** (usually before anything is published or bought).
5. Grade: copy the transcript into a new chat with `evals/grade.md` and the scenario, or grade by hand. Record results in `evals/results.md`.

## Scenarios

See `scenarios.md`. Ten owners covering every hosting situation, both modes, a stuck owner, a pushy owner and a risky request.

## Script checks

```
python scripts/project.py --file /tmp/p.json init "Test Co" && python scripts/project.py --file /tmp/p.json status
python scripts/qa_report.py evals/fixtures/broken-site --out /tmp/qa   # must exit 1 and list all 8 planted problems
python scripts/dns_snapshot.py example.com                             # must print nameservers and save a JSON file
python scripts/detect_site.py example.com
python scripts/style_cards.py --name "Test Co" --tagline "Testing" --cta "Call" --out /tmp/sc
```

`evals/fixtures/broken-site` has these planted problems, all of which the QA report must catch: missing image, missing #anchor, broken internal link, a form with no action, "Lorem ipsum", wrong phone number in a call button, a 900px-wide box that scrolls sideways on phones, missing search description.
