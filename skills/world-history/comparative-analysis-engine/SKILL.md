---
name: comparative-analysis-engine
description: >
  Build structured comparisons of historical phenomena across time and space. Use when the
  user wants to compare two or more empires, revolutions, economic crises, or technological
  transitions, producing an analysis of what they share, where they diverge, what explains
  the difference, and what the comparison reveals that studying either case alone would miss.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
tools: Read
---

# Comparative Analysis Engine — Structured Comparison Across History

This is an action skill that produces structured comparisons of historical phenomena. Unlike the `historical-analogy-engine` (which compares a *current* situation to historical parallels), the comparative-analysis-engine compares *historical cases to each other* — empire to empire, revolution to revolution, crisis to crisis — to identify what they share, where they differ, and what the comparison reveals.

## When This Applies

- User asks to compare two or more historical phenomena ("compare the Roman and British empires")
- User asks what two historical events have in common
- User asks why two similar situations had different outcomes
- User wants a structured comparison for learning or writing

## The Four-Step Method

### Step 1 — Define the Comparison

Specify exactly what is being compared and why:
- **Cases**: Which specific phenomena? (Be precise — "the Roman Empire 27 BCE–476 CE" not just "Rome")
- **Question**: What is the comparison trying to illuminate? (Similarities? Differences? A specific causal question?)
- **Framework**: What lens are we using? (Political, economic, structural, cultural?)

### Step 2 — Map Shared Features

Identify genuine structural similarities. For each shared feature:
- State the commonality
- Provide evidence from each case
- Assess how deep the similarity goes (surface resemblance vs. structural parallel)

### Step 3 — Map Divergences

Identify where the cases differ. For each difference:
- State the divergence
- Explain what caused the difference (different conditions, different choices, different contexts)
- Assess whether the difference undermines the comparison or makes it more informative

### Step 4 — Synthesize

Produce the comparative insight — what does putting these cases side by side reveal?
- **What the comparison illuminates**: patterns visible only through comparison
- **What it obscures**: aspects of each case that the comparison framework misses
- **The key takeaway**: the one thing this comparison teaches that studying either case alone would miss

## Output Template

```
COMPARISON: [Case A] vs. [Case B] (+ optional Case C)
QUESTION: [What this comparison is trying to answer]
FRAMEWORK: [Political / Economic / Structural / Cultural]

SHARED FEATURES:
  1. [Commonality] — Evidence from A | Evidence from B
  2. [Commonality] — Evidence from A | Evidence from B
  3. [Commonality] — Evidence from A | Evidence from B

DIVERGENCES:
  1. [Difference] — A did X because... | B did Y because...
  2. [Difference] — A shows... | B shows...
  3. [Difference] — A's outcome... | B's outcome...

EXPLANATORY FACTORS:
  [Why the cases diverged despite similarities — the analytical payoff]

SYNTHESIS:
  [The comparative insight: what this reveals that studying either alone would miss]

LIMITS:
  [What this comparison framework obscures or oversimplifies]
```

## Comparison Types

| Type | Question | Example |
|---|---|---|
| **Most Similar Systems** | Same structure, different outcome — why? | French vs. Russian Revolution: both followed Brinton's sequence, but consolidation differed |
| **Most Different Systems** | Different structure, same outcome — why? | Roman Empire vs. Han Dynasty: very different institutions, similar collapse dynamics |
| **Diachronic** | Same place, different time — what changed? | China under Ming vs. Qing: what continuities persisted across dynastic change? |
| **Synchronic** | Same time, different place — what varied? | 1848 revolutions: why did they succeed in some European countries and fail in others? |

## Anti-Patterns

- **Cherry-picking**: Selecting only features that support a predetermined conclusion
- **False equivalence**: Treating surface resemblance as deep structural similarity
- **Ignoring context**: Comparing across such different contexts that the comparison becomes meaningless
- **Asymmetric knowledge**: Knowing one case deeply and the other superficially, producing a biased comparison
