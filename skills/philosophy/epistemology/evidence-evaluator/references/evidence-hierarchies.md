# Evidence Hierarchies by Domain

Quick-reference for the evidence-evaluator. Each domain has its own hierarchy — what counts as strong evidence varies.

## Empirical / Scientific

```
Strongest ─── Systematic review / meta-analysis (well-conducted)
            │ Randomized controlled trial (pre-registered, adequate power)
            │ Quasi-experimental (natural experiment, regression discontinuity)
            │ Prospective cohort study
            │ Case-control study
            │ Cross-sectional survey
            │ Case report / case series
            │ Expert opinion / clinical experience
Weakest ──── Anecdote / personal testimony
```

**Modifiers**: Pre-registration increases trust. Replication strengthens any level. Industry funding doesn't disqualify but warrants scrutiny. Small samples weaken any design.

## Historical

```
Strongest ─── Primary source (contemporaneous document, artifact, record)
            │ Multiple independent primary sources (corroboration)
            │ Primary source with known bias (acknowledged, adjustable)
            │ Secondary source (scholarly analysis of primaries)
            │ Tertiary source (textbook, encyclopedia)
Weakest ──── Oral tradition / folk memory (valuable but not independently verifiable)
```

**Modifiers**: Proximity to event matters. Independence of sources matters more than quantity. Silence (absence in records that should mention X) is weak evidence.

## Legal / Factual

```
Strongest ─── Physical / forensic evidence (DNA, fingerprints, documents)
            │ Documentary evidence (authenticated records, contracts)
            │ Eyewitness testimony (cross-examined, corroborated)
            │ Expert testimony (qualified, methodology accepted)
            │ Circumstantial evidence (patterns, motive, opportunity)
            │ Character evidence
Weakest ──── Hearsay (out-of-court statements offered for truth)
```

**Modifiers**: Chain of custody affects physical evidence. Cross-examination tests testimony. Multiple independent witnesses strengthen eyewitness accounts.

## Technical / Engineering

```
Strongest ─── Reproducible demonstration (independently verified)
            │ Controlled benchmark (standardized conditions)
            │ Theoretical analysis with empirical validation
            │ Peer-reviewed technical paper
            │ Industry white paper
            │ Expert assessment
Weakest ──── Marketing claims / vendor benchmarks
```

**Modifiers**: Open-source implementations allow verification. Benchmark gaming is common — check methodology. Real-world performance often diverges from controlled benchmarks.

## Normative / Ethical

Evidence hierarchies apply to the **empirical premises** of ethical arguments, not to the normative conclusions themselves.

- "Torture causes lasting psychological damage" → evaluate with empirical hierarchy
- "Torture is wrong" → not evaluable by evidence alone; requires ethical framework (route to dilemma-analyzer)
- "Torture is wrong because it causes lasting psychological damage" → the "because" premise is empirically evaluable; the normative conclusion requires both evidence AND values
