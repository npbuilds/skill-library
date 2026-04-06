---
name: claim-decomposer
description: >
  Break complex research questions into individually verifiable atomic claims. Use when a
  question contains multiple assertions, hidden assumptions, compound predicates, or causal
  chains that need separate verification. Produces a structured claim list with verification
  strategies per claim.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Write
---

# Claim Decomposer — The Splitter

Every complex question is built from simpler claims stacked together. This skill takes a research question apart, surfaces hidden assumptions, and produces a numbered list of atomic claims that can each be independently verified.

The decomposer prevents the most common research failure: investigating a compound question as if it were a single thing, then producing a muddled answer that conflates distinct issues.

## How to Run

### Input

From the Spelunker orchestrator:
- The restated research question
- The detected domain (affects decomposition strategy)
- Any user-specified constraints

### Steps

#### Step 1 — Identify the Claim Structure

Read `references/decomposition-patterns.md` for the pattern catalog.

Scan the question for structural signals:

| Signal | Structure | Action |
|--------|-----------|--------|
| "and", "as well as", "also" | Compound — multiple claims joined | Split at each conjunction |
| "because", "since", "therefore" | Causal chain — claim depends on premise | Separate premise from conclusion |
| "if", "assuming", "given that" | Conditional — claim has prerequisite | Extract the prerequisite as its own claim |
| "better than", "more effective than", "compared to" | Comparative — two things measured | Decompose into claims about each thing + the comparison |
| "always", "never", "everyone" | Universal — sweeping scope | Note the scope as a testable claim |
| No signals, but question is broad | Implicit compound — topic has multiple facets | Break into the 2-4 most important facets |

#### Step 2 — Surface Hidden Assumptions

Every question carries assumptions. Make them explicit:

1. **Definitional assumptions** — Does the question assume a specific meaning for a term? ("Is AI dangerous?" assumes we agree on what "AI" and "dangerous" mean)
2. **Existence assumptions** — Does the question assume something exists or is true? ("Why did X cause Y?" assumes X did cause Y)
3. **Scope assumptions** — Does the question assume a time period, population, or context? ("Is X safe?" — safe for whom? at what dose? over what time period?)
4. **Value assumptions** — Does the question embed a judgment? ("Is X the best approach?" — best by what criteria?)

Each surfaced assumption becomes a separate verifiable claim unless it's a pure definitional choice (in which case, note it as a framing decision).

#### Step 3 — Classify Each Atomic Claim

Assign a **type** and a **domain** to each claim. The type determines the verification strategy. The domain determines which tools the source-triangulator should use (see `../spelunker/references/domain-routing.md` for the full tool chain mapping).

**Domain assignment:** Use the domain detected in Phase 1 as the default, but override per-claim when a specific claim belongs to a different domain. Multi-domain questions are common — "Is intermittent fasting good for software developers?" has biomedical claims (fasting's health effects) and behavioral claims (productivity impact). Each claim gets the domain that matches *its* evidence needs.

| Claim Type | Description | Verification Strategy |
|-----------|-------------|----------------------|
| **Factual** | A specific, checkable assertion of fact | Look for authoritative sources, official data, direct evidence |
| **Causal** | X causes/leads to/results in Y | Look for experimental evidence (RCTs), controlled studies, mechanism explanations |
| **Comparative** | X is more/less/better/worse than Y | Look for head-to-head comparisons, benchmarks, meta-analyses |
| **Predictive** | X will happen / X is likely | Look for forecasting models, historical precedents, expert predictions |
| **Definitional** | What X means or how it's classified | Look for authoritative definitions, standard classifications, consensus usage |
| **Existential** | Whether X exists or has occurred | Look for direct evidence, records, documentation |
| **Evaluative** | Whether X is adequate, sufficient, or good (judgment-dependent) | Look for established criteria/standards, expert assessments, outcome-based evidence |

#### Step 4 — Assign Priority

Each claim gets a priority that determines how much investigative effort it receives:

- **Critical** — The conclusion depends on this claim. If this claim falls, the answer changes. Premises in causal chains, core factual assertions, and the main comparison in comparative questions are typically critical.
- **Supporting** — Strengthens a critical claim but isn't load-bearing on its own. Background context, corroborating facts, and secondary comparisons are typically supporting.
- **Contextual** — Useful background that helps the user understand the answer but doesn't affect the conclusion's validity. Definitional claims and scope-setting facts are typically contextual.

**Rule of thumb:** If you removed this claim from the brief, would the conclusion change? Yes → critical. Would the conclusion weaken? → supporting. Would only the framing change? → contextual.

#### Step 5 — Order by Dependency

Some claims depend on others. Map the dependency graph:

- If Claim B assumes Claim A is true, verify A first
- If Claim C is independent of A and B, it can be verified in parallel
- If the conclusion depends on all premises, note that the conclusion's confidence cannot exceed the weakest premise

#### Step 6 — Output the Claim List

Produce a structured output:

```
CLAIM DECOMPOSITION
───────────────────
Original question: [the restated question]

Atomic Claims:
  1. [Claim text] — Type: [factual/causal/etc.] — Domain: [biomedical/technical/etc.] — Depends on: [none/claim#] — Priority: [critical/supporting/contextual] — Strategy: [brief guidance]
  2. [Claim text] — Type: [type] — Domain: [domain] — Depends on: [dependencies] — Priority: [priority] — Strategy: [guidance]
  ...

Hidden Assumptions Surfaced:
  A1. [Assumption text] — Status: [needs verification / framing decision / common ground]
  A2. ...

Dependency Graph:
  [Claim 1] → [Claim 3] (Claim 3 depends on Claim 1)
  [Claim 2] ── (independent, can run in parallel)

Recommended Investigation Order:
  Wave 1 (parallel): Claims [2, 4] (independent)
  Wave 2 (sequential): Claim [1] then Claim [3] (dependency)
  Wave 3: Assumptions [A1] (if not common ground)
```

### Output

A structured claim list ready for the source-triangulator to process. Each claim is:
- Atomic (cannot be meaningfully split further)
- Typed (so the triangulator knows what kind of evidence to seek)
- Domain-tagged (so the triangulator knows which tools to use)
- Priority-ranked: **critical** (conclusion depends on this), **supporting** (strengthens a critical claim), or **contextual** (useful background but not load-bearing)
- Ordered (so dependencies are respected)
- Annotated with verification strategy

## Error Handling

**Question is already atomic:** Return it as a single claim with type classification. Note that no decomposition was needed.

**Question is too vague to decompose:** Return to the orchestrator requesting clarification. Suggest 2-3 specific interpretations for the user to choose from.

**Decomposition produces 15+ claims:** Flag to the orchestrator that the question is extremely broad. Suggest grouping claims into priority tiers (must-verify, should-verify, nice-to-verify) and let the user prioritize.

**Circular dependencies detected:** Flag the logical circularity. This often reveals a flawed question structure that the user should be made aware of.
