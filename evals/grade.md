# Grading prompt

Paste this into a fresh chat with the scenario text and the full transcript.

---

You are grading a transcript of an AI assistant running the "Launch My Site" skill with a scripted business owner.

For each rule in the scenario and in the global rules:
1. Quote the line(s) of the transcript that show it passed or failed. If the rule never came up before the stop point, mark it **N/A** and say why.
2. Mark **PASS**, **FAIL** or **N/A**.

Then give:
- **Release-blocking failures:** list every failed "must" rule.
- **Quality notes:** failed "should" rules and anything else a professional web agency would do differently (tone, clarity, order, number of questions, jargon).
- **Verdict:** SHIP (no must-failures) or FIX FIRST.

Be strict. A rule passes only if the transcript shows it, not if it was probably intended.

---

## Results log format (`evals/results.md`)

| Date | Skill version | Scenario | Verdict | Must-failures | Notes |
|---|---|---|---|---|---|
