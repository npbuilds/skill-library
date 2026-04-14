---
name: condition-designer
description: >
  Design the initial conditions for a product to emerge — what capabilities to combine, what
  constraints to impose, what feedback signals to listen to, and what to intentionally leave
  open for emergence. The product "seed specification." Use when transitioning from thesis
  to the first concrete action.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Write bash Glob Grep Agent
---

# Condition Designer — Planting the Seed

A seed specification is NOT a product spec. A product spec says "build this." A seed specification says "combine these capabilities, impose these constraints, watch for these signals, and leave this open."

The difference: a product spec defines the output. A seed specification defines the **conditions from which output emerges**.

## Inputs

From Envision:
- **Thesis** — The falsifiable belief (from thesis-forge)
- **Paradigm** — The interaction model (from paradigm-designer)
- **Capability ingredients** — Which domains contribute (from possibility-mapper)
- **Experience sketch** — What it feels like, not what it looks like (from vision-architect)

## Process

### Step 1 — Select Capability Ingredients

From the thesis, identify which domain capabilities to combine:

```
Capability 1: {domain/skill} — contributes {what}
Capability 2: {domain/skill} — contributes {what}
Capability 3: {domain/skill} — contributes {what}
```

**Rule of three:** Start with exactly three capabilities. More than three is too complex for initial conditions. Fewer than two isn't a synthesis (route to the single domain instead).

### Step 2 — Define Constraints

Consult `constraint-sculptor` for framework, then specify:

- **Hard constraints** — Absolute boundaries. The product must NOT do this.
- **Soft constraints** — Preferences. The product SHOULD do this, but can flex.
- **Open space** — Areas intentionally left unconstrained for emergence.

The ratio matters: approximately 30% constrained, 70% open for initial seeds. Tighten after observing what emerges.

### Step 3 — Design Feedback Signals

Consult `feedback-architect` for framework, then specify:

- **Primary signal** — The one thing that tells you the seed is germinating
- **Secondary signals** — Supporting indicators
- **Warning signals** — Early indicators of wrong-direction emergence
- **Check interval** — How often to observe (daily? weekly?)

### Step 4 — Specify the Cultivation Budget

Borrowed from Shape Up's "appetite" concept: how much energy to invest before evaluating?

- **Small seed** — 1 week of cultivation. Proof of concept.
- **Medium seed** — 2-3 weeks. Working prototype with real feedback.
- **Large seed** — 4-6 weeks. Full cultivation cycle with multiple feedback rounds.

If you can't scope it to 6 weeks, the thesis needs sharpening.

### Step 5 — Output the Seed Specification

```markdown
# Seed Specification: {initiative name}

## Thesis
{from thesis-forge}

## Capability Ingredients
1. {domain/skill}: {what it contributes}
2. {domain/skill}: {what it contributes}
3. {domain/skill}: {what it contributes}

## Constraints
Hard: {absolute boundaries}
Soft: {preferences}
Open: {intentionally unconstrained areas}

## Feedback Architecture
Primary signal: {what tells us it's working}
Secondary: {supporting indicators}
Warning: {wrong-direction indicators}
Check interval: {frequency}

## Cultivation Budget
Size: {small/medium/large}
Duration: {weeks}
Energy ceiling: {what we're willing to invest}

## What We're Watching For
Expected emergence: {what we hope happens}
Surprise zone: {where unexpected behavior is most likely}

## Kill Criteria
{inherited from thesis, plus any new ones from condition design}
```

## Cross-Domain

- **worldbuilding-orchestrator** — For complex seeds, check systems coherence: "Do these capabilities and constraints produce a coherent system, or will they fight each other?"
