---
name: counterfactual-prober
description: >
  Active disconfirmation. Given a synthesized brief, generate "if the conclusion were false,
  what should we observe in the world?" predictions and search for those signatures. Stronger
  than passive adversarial search ("X debunked"), which only finds what others have already
  written. Plugged into Spelunker Phase 5 between the existing adversarial search and
  backpropagation. Triggered in `deep` mode by default; optional in `standard`.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Write WebSearch WebFetch
---

# Counterfactual Prober — Active Disconfirmation

Spelunker's existing Phase 5 adversarial search asks: "has anyone written 'X is wrong'?" That's passive — it only finds critique that already exists. This skill asks the harder question: "if X were wrong, what should we observe in the world that we haven't yet looked for?" — and then goes and looks for those signatures.

This is the difference between reading reviews of a movie and watching the movie yourself.

## Guiding Principles

1. **Predictions, not opinions.** A counterfactual is a falsifiable observation, not a belief. "If passive flows are NOT 68% of the market, we should see active funds outperforming index funds over the same period."
2. **Look for the signature, not the conclusion.** Search for the empirical pattern, not for someone else who already concluded the original claim is wrong.
3. **Absence of the signature is weak evidence FOR the claim.** Presence of the signature is strong evidence AGAINST.
4. **Probe the load-bearing claims, not the trivia.** Counterfactual probing is expensive — apply it to claims whose downgrade would change the brief's overall conclusion.

## How to Run

### Input

- The synthesized brief from `evidence-synthesizer` (after the existing Phase 5 adversarial search has run)
- The dependency graph from `claim-decomposer`
- Depth mode: `standard` (probe top 1 critical claim) or `deep` (probe all critical claims and the highest-priority supporting claims)

### Steps

#### Step 1 — Select Claims to Probe

Identify load-bearing claims:
- All claims tagged Confirmed or Likely that are flagged `critical` priority
- Plus, in `deep` mode, the top 2 Likely-tagged `supporting` claims (downgrading these would cascade through the dependency graph)

Skip:
- Speculative or Contested claims (already low-confidence; counterfactual would not change much)
- Definitional claims (no empirical signature to probe)
- Claims already invalidated in the existing Phase 5 adversarial search

#### Step 2 — Generate Counterfactual Predictions

For each selected claim, generate 2-4 specific empirical predictions of the form:

> "If [claim] were FALSE, then we should observe [specific empirical pattern] because [causal mechanism]."

Examples:

- Claim: "Passive flows are ~68% of the US fund market as of mid-2025."
  - CF1: We should see significant active-fund outperformance vs. index over 2020-2025 (active managers would beat the benchmark if they were actually running most of the money).
  - CF2: Index reconstitution events should NOT cause measurable price dislocations (no concentrated passive bid).
  - CF3: Mega-cap concentration should be stable or declining (passive flows are what's accumulating in mega-caps).

- Claim: "Drug X reduces mortality by 30% in population Y."
  - CF1: Healthcare mortality stats for population Y should NOT show a divergence after Drug X's approval.
  - CF2: Insurance actuarial tables for Y should show similar mortality before/after market access.
  - CF3: Replications of the trial in other populations should fail to find the effect.

The predictions must be:
- **Specific** — name a measurable quantity, time window, and direction
- **Independent of the original evidence** — don't search the same studies that grounded the original claim
- **Mechanistically motivated** — explain WHY the signature should appear if the claim is false

#### Step 3 — Search for Each Signature

For each counterfactual prediction, run a focused search using `source-triangulator` (or directly via WebSearch if simpler). Look for the empirical pattern, not for the conclusion.

Bad search: `"passive ownership share is not 68%"` (looking for the conclusion)
Good search: `"active vs passive fund performance 2020-2025 cumulative return"` (looking for the signature)

Record per prediction:
- The search queries used
- What was found (the actual empirical observation, not someone's interpretation)
- Whether the signature is `present` (CF supported, original claim weakened), `absent` (CF refuted, original claim strengthened), or `mixed/inconclusive`

#### Step 4 — Update Confidence Tags

For each probed claim, aggregate the counterfactual results:

| Result pattern | Effect on claim |
|----------------|-----------------|
| All CFs absent (signatures of falsity NOT found) | Confirmed stays Confirmed; Likely upgraded to Confirmed if other criteria met |
| Most CFs absent, 1 mixed | No change (confidence stays where the original adversarial search left it) |
| ≥1 CF present (signature of falsity FOUND) | Downgrade by one tier and feed into evidence-synthesizer for cascade re-run |
| Most CFs inconclusive (couldn't measure the signature) | No change, but document the limit in Gaps |

The downgrade then triggers the existing Phase 5 backpropagation cascade through the dependency graph.

### Output

Append to the brief a new section between Phase 5's existing output and Phase 6's presentation:

```
COUNTERFACTUAL PROBE
────────────────────
Claims probed: <N>

For each claim:

  Claim <id>: "<text>"
  Original confidence: <tier>

  CF1: If false, we'd observe: <prediction>
       Searched: <queries>
       Found: <observation>
       Verdict: signature [present | absent | inconclusive]

  CF2: ...

  Aggregate: <signature pattern> → confidence change: <tier> → <tier> | unchanged

Cascade triggered: yes | no
  If yes: list of dependent claims also re-evaluated
```

## Error Handling

**No CFs are searchable (claim is too abstract or about future events):** Document as a known limit; do not invent searches that don't bear on the claim. Return "no probe possible" for that claim.

**All CFs return inconclusive (data simply isn't there):** This is itself worth noting — it means the claim is essentially unfalsifiable with current data, which should soften any high-confidence tag. Recommend downgrading Confirmed to Likely on grounds of "unfalsifiable in practice."

**Search results contradict the original claim AND the counterfactual signature is present:** Strong evidence of error in the original brief. Surface this prominently and recommend a Phase 4 re-run, not just a tag downgrade.

## Scope Boundaries

**Does NOT:** Replace the passive adversarial search in Phase 5 — it complements it.
**Does NOT:** Probe every claim. Token cost is too high. Apply to load-bearing claims only.
**Does NOT:** Generate predictions for claims that are inherently non-empirical (definitions, value judgments, predictions about pure preference).
