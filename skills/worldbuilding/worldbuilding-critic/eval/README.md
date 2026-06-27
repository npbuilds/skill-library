# Validity Harness — `worldbuilding-critic`

Mirrors the `quality-critic` harness (see `_shared/critic-core` §"Build the validity harness"). It tests whether the soundness judge is **valid**, in both failure directions:

- **Let an unsound system through (false-pass)** — passing free/unbounded/decorative/unruled systems. The core failure to avoid.
- **Reject a sound-but-unconventional one (false-fail)** — most importantly, wrongly failing a *deliberately soft* magic (Sanderson's 1st Law: soft magic is valid if it doesn't resolve the conflict). A conformity-style judge fails this.

## What it measures

`validity-set.yaml` holds sound-vs-unsound pairs with neutral slots — `fail_passage` (must FAIL) and `pass_passage` (must PASS) — tagged by `kind` (the rubric dimension under test: cost / limits / propagation / brightline / plausibility / soft-magic).

Headline metrics from `score-validity.py`:
- **UNSOUND-TOLERANCE** = false-pass rate. A valid critic scores **0%**.
- **SOFT-MAGIC CONFORMITY** = false-fail rate on `soft-magic-trap`. A valid critic scores **0%** (it must not punish a soundly-handled soft system).

## Protocol

1. **Run the critic blind** on `fail_passage` and `pass_passage` separately (profile `system`). Do not show it the gold labels, `rationale`, `trap`, or `kind`. Record only PASS/FAIL on the item's **target dimension**.
2. **Write verdicts** to JSON:
   ```json
   { "cost-01": {"fail_passage": "FAIL", "pass_passage": "PASS"} }
   ```
3. **Score:** `python3 score-validity.py verdicts.json` — exit 0 = PASS (every item usable, false-pass ≤ threshold, false-fail ≤ threshold). Missing/malformed verdicts force a FAIL.

## When it fails

- **False-pass** → the critic accepted an unsound system without citing the axiom/consequence that earns the dimension (the evidence-anchor cap isn't firing). Tighten Layer 2.
- **False-fail on `soft-magic-trap`** → the critic is judging *form* (unexplained = bad) instead of *function* (does the soft magic resolve the plot?). Re-read `_shared/critic-core` §steelman and the soft-system note in `references/soundness-rubric.md`.

## Drift calibration

When a human disagrees in real use (a system the critic passed that's actually broken, or failed that's actually fine), add it as a new pair tagged by `kind`. The set grows toward the human signal.

## Extending the set

Add pairs per system type (economy, society, technology — each has a spine dimension and characteristic stress-tests; see `references/stress-tests.md`), and a pair for each stress-test (enforcement-physics, monopoly-on-violence, consolidation, missing-consequence, exploit). Keep both halves targeting the same dimension.
