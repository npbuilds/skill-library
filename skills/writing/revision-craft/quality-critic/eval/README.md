# Validity Harness — `quality-critic`

This harness answers the question the research says you cannot skip: **is the critic valid, or merely reliable?** An LLM judge can fail in two opposite directions, and a trustworthy critic does neither:

- **Fooled by polish (style bias)** — passes hollow-but-pretty prose. Puts the generator on a path to competent, lifeless prose.
- **Conformity engine** — fails alive-but-unconventional prose. Crushes creativity; turns the critic into a norm-enforcer.

This set tests both directions with known answers.

## What it measures

`validity-set.yaml` holds matched **adversarial pairs** of three `kind`s. Every item has two neutral slots — `fail_passage` (a valid critic **FAILs** it) and `pass_passage` (a valid critic **PASSes** it):

| kind | `fail_passage` | `pass_passage` | The error it catches |
|---|---|---|---|
| `style-trap` | polished-but-hollow | plain-but-substantive | being **fooled by polish** |
| `transgression-trap` | pretentious / unearned | rule-breaking-but-brilliant | being a **conformity engine** |
| `originality-trap` | competent-but-generic | fresh-and-surprising | tolerating the **predictable** |

Two headline failure rates:

- **style-bias susceptibility** = false-pass rate on `style-trap`s (passed something hollow). A valid critic scores **0%**.
- **conformity rate** = false-fail rate on `transgression-trap`s (failed an earned transgression). **This is the creativity guard** — a valid critic scores **0%**.

## Protocol

1. **Run the critic blind.** For each item, run `quality-critic` (profile `literary-fiction`, level `scene`) on `fail_passage` and on `pass_passage` **separately**. Do **not** show it the gold labels, `rationale`, `trap`, or `kind`. Record only its PASS/FAIL verdict on the item's **target dimension**.
2. **Write verdicts** to a JSON file:
   ```json
   {
     "interiority-01":               {"fail_passage": "FAIL", "pass_passage": "PASS"},
     "transgression-flat-affect-01": {"fail_passage": "FAIL", "pass_passage": "PASS"}
   }
   ```
3. **Score:**
   ```bash
   python3 score-validity.py verdicts.json
   ```
   Exit 0 = harness PASS (every item usable, false-pass ≤ threshold, false-fail ≤ threshold). Exit 1 = FAIL. Missing or malformed verdicts (absent, non-object, empty, or anything other than `PASS`/`FAIL`) are reported as `MISSING`/`UNUSABLE` and force a FAIL — an incomplete run can never pass the gate.

## Pass criteria

- **false-pass rate = 0%** (`--max-false-pass`) — the critic is never fooled into passing something that should fail. A false-pass on a `style-trap` means the evidence-anchor cap (SKILL.md Step 2d) isn't firing.
- **false-fail rate = 0%** (`--max-false-fail`) — the critic never rejects something that should pass. A false-fail on a `transgression-trap` means the steelman test (SKILL.md Step 2e) isn't firing — the critic is enforcing convention.
- Strict because the gold pairs are deliberately unambiguous. On a larger, subtler set, tolerate a small nonzero rate via the two flags.

## When it fails

- **False-pass** → the critic let a passage through **without citing a verbatim line that grounds the pass** (Step 2d), or it accepted pretension it couldn't name an effect for. Tighten the evidence-anchor.
- **False-fail on a transgression-trap** → the critic judged **form instead of function**. Re-read SKILL.md Step 2 (judge the effect) and Step 2e (steelman before FAIL), and check the pass-test in `references/rubric-profiles.md` isn't keying on the conventional *device* instead of the *effect*.

## Drift calibration (closing the loop)

This set is the critic's regression gate, not the ground truth for "good." When the critic runs in a real loop and a **human disagrees at a checkpoint**, add that disagreement as a new pair (the human verdict is the gold label) — tag it by `kind`. The set grows toward the human signal, the only thing that keeps the proxy honest over time.

## Extending the set

Add pairs for: each non-default profile (`genre`, `rpg-playability`, `childrens`, `experimental` — note the inversions), longer `draft`-level passages testing **Arc shape**, more `transgression-trap`s (every celebrated rule-break is a candidate), and any real loop failure the drift alarm surfaces. Keep both halves of every pair targeting the **same** dimension, and set `kind` so the headline metrics stay interpretable.
