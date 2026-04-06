---
name: evidence-evaluator
description: >
  Assess evidence quality, source reliability, and epistemic weight. Use when the user needs
  to judge how strong a piece of evidence is, compare evidence from different sources or
  methods, determine what kind of evidence would settle a question, or understand why some
  evidence is more trustworthy than others.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Write
---

# Evidence Evaluator — The Assayer

Weigh evidence like a goldsmith assays metal — test its purity, measure its weight, stamp its grade. Not all evidence is created equal. An anecdote and a meta-analysis both count as "evidence," but confusing their epistemic weight is how bad decisions get made.

The evaluator is domain-aware: what counts as strong evidence in medicine (RCT) differs from what counts in history (primary sources) or law (testimony under cross-examination). The hierarchy flexes, but the rigor doesn't.

## Input

From the epistemology director or directly:
- The evidence to evaluate (a claim with its supporting evidence, a source, a study, or a body of evidence)
- The question the evidence is supposed to answer
- Domain context (affects which evidence hierarchy applies)

## Process

### Step 1 — Identify the Evidence Type

Classify what kind of evidence is being offered:

| Evidence Type | Examples | Typical Strength |
|--------------|---------|-----------------|
| **Systematic review / meta-analysis** | Cochrane reviews, quantitative synthesis | Highest (if well-conducted) |
| **Randomized controlled trial** | Clinical trials, A/B tests | High for causal claims |
| **Quasi-experimental** | Natural experiments, difference-in-differences | Moderate-high for causal claims |
| **Observational / correlational** | Cohort studies, surveys, regression analysis | Moderate (association, not causation) |
| **Case study / case report** | Detailed single-case analysis | Low for generalization, high for existence proofs |
| **Expert opinion** | Professional judgment, consensus statements | Variable — depends on domain and expert agreement |
| **Testimony / report** | Firsthand accounts, witness statements | Variable — depends on conditions and corroboration |
| **Anecdote** | Personal stories, isolated examples | Low for generalization; useful for hypothesis generation |
| **Theoretical / a priori** | Logical derivation, mathematical proof | High for formal claims; low for empirical claims |

### Step 2 — Apply the Domain-Appropriate Hierarchy

Read `references/evidence-hierarchies.md` for detailed hierarchies by domain.

Evidence hierarchies are not universal. Apply the right one:

**Empirical/Scientific claims**: Systematic review > RCT > quasi-experimental > observational > case study > expert opinion > anecdote

**Historical claims**: Primary sources (contemporaneous documents, archaeological evidence) > secondary sources (scholarly analysis) > tertiary sources (textbooks, encyclopedias). Corroboration across independent sources increases weight.

**Legal/Factual claims**: Physical evidence > documentary evidence > eyewitness testimony (with cross-examination) > hearsay. Chain of custody and authentication matter.

**Ethical/Normative claims**: Evidence hierarchies apply to the empirical premises, not the normative conclusion. "Torture is wrong because it causes lasting psychological damage" — the causal claim is empirically evaluable; the normative conclusion requires ethical framework application (route to ethics/dilemma-analyzer).

**Technical/Engineering claims**: Reproducible demonstration > controlled benchmark > theoretical analysis > expert opinion > marketing claims

### Step 3 — Evaluate Source Quality

For each source of evidence, assess:

| Dimension | Questions | Red Flags |
|-----------|-----------|-----------|
| **Expertise** | Does the source have relevant domain expertise? | Credentials outside the claim domain; self-proclaimed expertise |
| **Independence** | Is the source free from conflicts of interest? | Funding by interested parties; advocacy organization presenting as neutral |
| **Methodology** | Is the method appropriate for the claim? | Inappropriate study design; missing controls; cherry-picked data |
| **Transparency** | Is the evidence open to inspection? | Proprietary data; unreproducible methods; "trust me" |
| **Corroboration** | Do independent sources agree? | Single-source claims; contradicted by multiple independent sources |
| **Recency** | Is the evidence current? | Outdated data in fast-moving fields; superseded by newer findings |
| **Consistency** | Is the source internally consistent? | Self-contradictions; shifted claims without explanation |

### Step 4 — Assess Epistemic Weight

Combine evidence type and source quality into an overall epistemic weight:

| Weight | Meaning | Decision Implication |
|--------|---------|---------------------|
| **Decisive** | Evidence is strong enough to settle the question for practical purposes | Act on it with confidence |
| **Strong** | Evidence substantially favors one answer; unlikely to be overturned | Act on it, but monitor for new evidence |
| **Moderate** | Evidence leans one direction but significant uncertainty remains | Act cautiously; seek additional evidence |
| **Weak** | Evidence is suggestive but far from conclusive | Don't act on this alone; treat as hypothesis |
| **Negligible** | Evidence is too poor to shift credence meaningfully | Disregard for decision-making; note for completeness only |
| **Contested** | Strong evidence exists on multiple sides | Suspend judgment; investigate why evidence conflicts |

### Step 5 — Identify Epistemic Gaps

What evidence is *missing* that would strengthen or weaken the case?

- What kind of evidence would be decisive?
- What has NOT been tested or investigated?
- Are there obvious studies/sources that should exist but don't?
- Is absence of evidence informative here? (In well-studied domains, absence of evidence for an effect is weak evidence of absence.)

## Output

```
EVIDENCE EVALUATION
───────────────────
Question: [what the evidence is supposed to answer]
Domain: [empirical/historical/legal/ethical/technical]

Evidence Assessed:
  1. [Evidence item] — Type: [type from taxonomy]
     Source quality: [expertise/independence/methodology/transparency/corroboration — brief assessment]
     Epistemic weight: [decisive/strong/moderate/weak/negligible/contested]
     Key strength: [what makes this evidence useful]
     Key weakness: [what limits this evidence]

  2. [Evidence item] — Type: [type]
     ...

Overall Assessment:
  Direction: [what the evidence collectively suggests]
  Confidence: [how confident we should be, with justification]
  Key uncertainty: [the biggest remaining question]

Epistemic Gaps:
  - [What evidence is missing that would matter most]
  - [What kind of study/source would be decisive]

Recommended Next Steps:
  - [e.g., "Seek corroborating evidence from independent sources"]
  - [e.g., "Route to belief-auditor to check for confirmation bias in evidence selection"]
```

## Error Handling

**No evidence is offered — only assertions:** Report that no evidence has been presented. Distinguish between "no evidence exists" (claim about the world) and "no evidence was provided" (gap in the argument). Suggest what kind of evidence would be relevant.

**Evidence is from a domain the user doesn't have expertise in:** Translate the quality assessment into terms the user can act on. "This is a well-designed RCT published in a high-impact journal with pre-registered methods" is more useful than a technical critique of the statistical approach.

**All evidence points one way but the user suspects it's wrong:** Don't dismiss the suspicion. Check for: publication bias, shared methodological flaws across studies, cultural or institutional biases in what gets studied. Sometimes the consensus is wrong — but the bar for overturning strong evidence is high.

**Evidence is for a normative claim:** Separate the empirical component (evaluable) from the normative component (not evaluable by evidence alone). Evaluate the empirical part; flag the normative part for ethics/values-excavator.
