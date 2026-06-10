# Counterfactual Prober — Quick Reference


## Quick Reference

| Result pattern | Effect on claim |
|----------------|-----------------|
| All CFs absent (signatures of falsity NOT found) | Confirmed stays Confirmed; Likely upgraded to Confirmed if other criteria met |
| Most CFs absent, 1 mixed | No change (confidence stays where the original adversarial search left it) |
| ≥1 CF present (signature of falsity FOUND) | Downgrade by one tier and feed into evidence-synthesizer for cascade re-run |
| Most CFs inconclusive (couldn't measure the signature) | No change, but document the limit in Gaps |

## Formula / Pseudocode

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
