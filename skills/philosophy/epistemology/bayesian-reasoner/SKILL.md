---
name: bayesian-reasoner
description: >
  Update credences given new evidence, calibrate confidence levels, and identify base-rate
  neglect. Use when the user needs to reason about how new evidence should change their
  beliefs, check whether their confidence is proportional to the evidence, understand
  conditional probabilities, or practice calibrated reasoning.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Write
---

# Bayesian Reasoner — The Calibrator

Update beliefs like a scientist updates hypotheses — proportionally to the evidence, neither too much nor too little. Bayesian reasoning is the formal framework for learning from evidence, and its most practical application is calibration: ensuring your confidence matches what the evidence actually warrants.

## Input

From the epistemology director or directly:
- The hypothesis or belief to update
- The new evidence
- The prior credence (how confident before the evidence — if unknown, estimate)
- Mode: **update** (compute posterior given evidence), **calibrate** (check whether confidence matches evidence), or **diagnose** (identify base-rate neglect or other probabilistic errors)

## Process

### Step 1 — Specify the Bayesian Components

| Component | Symbol | Meaning | How to Estimate |
|-----------|--------|---------|----------------|
| **Prior** | P(H) | Credence in hypothesis before new evidence | Base rates, background knowledge, previous evidence |
| **Likelihood** | P(E\|H) | Probability of seeing this evidence if hypothesis is true | How well does the hypothesis predict this specific evidence? |
| **Marginal likelihood** | P(E) | Probability of this evidence under all hypotheses | P(E\|H)P(H) + P(E\|¬H)P(¬H) |
| **Posterior** | P(H\|E) | Credence in hypothesis after seeing evidence | Bayes' theorem: P(H\|E) = P(E\|H) × P(H) / P(E) |

### Step 2 — Apply Bayes' Theorem

**Core formula**: P(H|E) = P(E|H) × P(H) / P(E)

**Odds form** (often more intuitive):
- Prior odds: P(H) / P(¬H)
- Likelihood ratio: P(E|H) / P(E|¬H)
- Posterior odds = Prior odds × Likelihood ratio

The likelihood ratio is the key number — it measures how much the evidence discriminates between hypothesis and alternative. A ratio of 10 means the evidence is 10× more likely under the hypothesis than the alternative.

### Step 3 — Check for Common Errors

#### Base Rate Neglect
The most common Bayesian error. People focus on the evidence and ignore how common the hypothesis is to begin with.

*Classic example*: A test is 99% accurate. 1% of the population has the condition. You test positive. What's the probability you have it?

Answer: ~50%, not 99%. Because: P(H|E) = (0.99 × 0.01) / (0.99 × 0.01 + 0.01 × 0.99) ≈ 0.50

The base rate (1%) matters enormously. Always ask: "How common is this prior to any evidence?"

#### Confirmation Bias as Bad Bayesian Updating
Proper updating considers P(E|H) AND P(E|¬H). Confirmation bias occurs when people only consider whether the evidence is consistent with their hypothesis (high P(E|H)) without asking whether it's also consistent with alternatives (high P(E|¬H)). Evidence that's equally likely under both hypotheses has a likelihood ratio of 1 — it's not evidence at all.

#### Neglecting Alternative Hypotheses
Bayes' theorem compares hypotheses. Evaluating P(E|H) alone is meaningless — you need P(E|¬H) or P(E|H₂). Always ask: "What else could explain this evidence?"

#### Insensitivity to Sample Size
Small samples produce noisy evidence. A single anecdote (N=1) provides a weak likelihood ratio. A large study provides a strong one. The strength of the update should scale with the evidential quality.

### Step 4 — Calibration Check

Compare stated confidence to warranted confidence:

| Stated Confidence | Evidence Warrants | Calibration |
|---|---|---|
| "I'm 90% sure" | Posterior ≈ 0.90 | Well-calibrated |
| "I'm 90% sure" | Posterior ≈ 0.60 | Overconfident — evidence is weaker than you think |
| "I'm 50/50" | Posterior ≈ 0.85 | Underconfident — evidence is stronger than you think |

**Calibration practice**: For claims you're "90% sure" about, you should be wrong about 10% of the time. If you're wrong more often, you're overconfident. If less often, you're underconfident.

### Step 5 — Present the Update

## Output

```
BAYESIAN ANALYSIS
─────────────────
Hypothesis: [H]
Evidence: [E]

Prior: P(H) = [value] — Basis: [base rate / background knowledge / previous evidence]
Likelihood: P(E|H) = [value] — Reasoning: [how well H predicts E]
Alternative: P(E|¬H) = [value] — Reasoning: [how well alternatives predict E]
Likelihood ratio: [P(E|H) / P(E|¬H)] = [value]

Posterior: P(H|E) = [value]

Update: [prior] → [posterior] — Shift: [how much and in which direction]
Interpretation: [what this means in plain language]

Calibration Check:
  Your stated confidence: [if provided]
  Warranted confidence: [posterior]
  Assessment: [well-calibrated / overconfident / underconfident]

Errors Detected:
  [Base rate neglect / confirmation bias / neglecting alternatives / none]

Key Insight: [the most important thing about this update]
```

## Error Handling

**Prior is unknown:** Use reference class data (similar situations), principle of indifference (equal priors when genuinely ignorant), or maximum entropy (least informative prior consistent with constraints). Be explicit about which method and why.

**Evidence is qualitative, not quantitative:** Bayesian reasoning still applies — estimate likelihood ratios qualitatively. "This evidence is about 3× more likely if H is true than if not" is imprecise but useful. Don't pretend to false precision.

**Multiple pieces of evidence:** Update sequentially — each posterior becomes the next prior. Or combine: the total likelihood ratio is the product of individual likelihood ratios (assuming conditional independence). Flag if independence assumption is questionable.

**User resists updating:** Cognitive inertia is real. Show the math gently. "Given this evidence and your prior, Bayes' theorem gives [X]. If that feels wrong, let's check whether your prior or the likelihood estimate needs adjusting."
