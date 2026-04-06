# Bayesian Reasoner — Quick Reference


## Step 1 — Specify the Bayesian Components

| Component | Symbol | Meaning | How to Estimate |
|-----------|--------|---------|----------------|
| **Prior** | P(H) | Credence in hypothesis before new evidence | Base rates, background knowledge, previous evidence |
| **Likelihood** | P(E\|H) | Probability of seeing this evidence if hypothesis is true | How well does the hypothesis predict this specific evidence? |
| **Marginal likelihood** | P(E) | Probability of this evidence under all hypotheses | P(E\|H)P(H) + P(E\|¬H)P(¬H) |
| **Posterior** | P(H\|E) | Credence in hypothesis after seeing evidence | Bayes' theorem: P(H\|E) = P(E\|H) × P(H) / P(E) |

## Quick Reference

| Stated Confidence | Evidence Warrants | Calibration |
|---|---|---|
| "I'm 90% sure" | Posterior ≈ 0.90 | Well-calibrated |
| "I'm 90% sure" | Posterior ≈ 0.60 | Overconfident — evidence is weaker than you think |
| "I'm 50/50" | Posterior ≈ 0.85 | Underconfident — evidence is stronger than you think |
