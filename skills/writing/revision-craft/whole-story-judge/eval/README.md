# Validity Harness — `whole-story-judge`

Mirrors the other critic harnesses (see `_shared/critic-core` §"Build the validity harness"). It tests whether the macro judge is **valid**, in both failure directions:

- **Let a broken whole through (false-pass)** — passing a story with a dropped setup, no arc, episodic structure, or a bait-and-switch ending. The core failure to avoid.
- **Reject a sound-but-unconventional whole (false-fail)** — most importantly, wrongly failing an **earned subversion** (a gun deliberately, markedly not fired; an open/ambiguous ending). A conformity judge fails this and would flunk every literary open ending.

## What it measures

`validity-set.yaml` holds sound-vs-broken **story-skeleton** pairs (compact outlines — the macro properties live in the skeleton, so a whole novel isn't needed). Neutral slots: `fail_passage` (must FAIL) / `pass_passage` (must PASS), tagged by `kind` (payoff / arc / causal / coherence / promise / subversion).

Headline metrics from `score-validity.py`:
- **DROPPED-SETUP TOLERANCE** = false-pass rate. A valid judge scores **0%**.
- **MACRO CONFORMITY** = false-fail rate on `subversion-trap`. A valid judge scores **0%** (it must not punish a marked, earned subversion).

## Protocol

1. **Run the judge blind** on `fail_passage` and `pass_passage` separately (level `draft`). Do not show it the gold labels, `rationale`, `trap`, or `kind`. Record only PASS/FAIL on the item's **target dimension**.
2. **Write verdicts** to JSON: `{ "payoff-01": {"fail_passage": "FAIL", "pass_passage": "PASS"} }`
3. **Score:** `python3 score-validity.py verdicts.json` — exit 0 = PASS (every item usable, false-pass ≤ threshold, false-fail ≤ threshold). Missing/malformed verdicts force a FAIL.

## When it fails

- **False-pass** → the judge accepted a broken whole without citing the setup↔payoff (or absence) that the dimension requires — the evidence-anchor cap (a *pair* of locations) isn't firing.
- **False-fail on `subversion-trap`** → the judge is treating every unfired gun as a defect. The tell of a real subversion is that it's **marked** (the text makes you feel the non-payoff) vs **silent** (the text forgot). Re-read `_shared/critic-core` §steelman and the subversion note in `references/macro-rubric.md`.

## Drift calibration

When a human disagrees in real use (a story the judge passed that doesn't actually cohere, or failed that does), add it as a new skeleton pair tagged by `kind`. The set grows toward the human signal.

## Extending the set

Add a `thematic-throughline` pair (advisory), more `subversion-trap` cases (anti-cathartic endings, ambiguous resolutions), and longer real-draft skeletons. Keep both halves targeting the same dimension.
