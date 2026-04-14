---
name: thesis-forge
description: >
  Crystallize a product thesis from vision, signals, and possibility mapping. A thesis is a
  specific, falsifiable bet: "We believe [this capability surface] will [create this value]
  for [these people] because [this is becoming possible now]." Every thesis carries explicit
  kill criteria. Use when moving from exploration to commitment.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Write bash Glob Grep Agent
---

# Thesis Forge — Crystallizing the Bet

A thesis is not a plan. It's not a roadmap. It's not a spec. A thesis is a **falsifiable belief about why something should exist**.

The thesis forge takes the raw material from Sense and Envision — frontier signals, emergence events, capability maps, possibility spaces, vision narratives — and compresses them into a sharp, testable statement that can be seeded.

Every thesis has a kill switch. If you can't articulate what would prove the thesis wrong, it's not a thesis — it's a wish.

## Thesis Structure

A complete thesis has five components:

```
THESIS: {initiative name}

BELIEF: We believe that [capability surface] will [create specific value]
        for [specific people/context] because [specific enabler/change].

EVIDENCE:
  For:     {what supports this belief — signals, data, emergence events}
  Against: {what challenges it — counter-signals, risks, unknowns}
  Missing: {what we'd need to know to be more confident}

KILL CRITERIA:
  - {observable condition that would falsify the thesis}
  - {observable condition that would falsify the thesis}
  - {time-bound: if X hasn't happened by Y, reconsider}

SEED REQUIREMENTS:
  Domains needed: {which domain orchestrators}
  Minimum capability: {what must exist before seeding}
  First signal to watch: {earliest indicator of thesis validity}
```

## Process

### Step 1 — Select from Possibility Map

Read the latest possibility map from `envision/possibility-mapper`. Choose the possibility to crystallize based on:

- **Conviction** — How strongly do the signals support this?
- **Capability readiness** — Can we actually seed this with what exists?
- **Strategic fit** — Does this align with active themes in the product narrative?
- **Option value** — Even if this specific product doesn't work, what does the attempt teach us?

### Step 2 — Articulate the Belief

Write the BELIEF statement. It must be:

- **Specific** — Not "AI can help with writing." Instead: "A capability surface that combines prose-orchestrator's voice analysis with game-theory's incentive design will produce positioning language that converts 3x better than generic copywriting."
- **Falsifiable** — There must be an observable outcome that could prove it wrong.
- **Grounded** — Connected to actual capability that exists or is emerging, not fantasy.
- **Time-aware** — Why NOW? What changed that makes this thesis viable today?

### Step 3 — Gather Evidence (Both Directions)

Actively seek evidence FOR and AGAINST the thesis:

**For:** What signals, emergence events, frontier developments, or user behaviors support this?
**Against:** What could go wrong? What assumption is weakest? Where's the counter-evidence?

If the thesis can't survive 5 minutes of adversarial questioning, it shouldn't be seeded. Engage `spelunker` for deeper research on critical assumptions when needed.

### Step 4 — Define Kill Criteria

Kill criteria must be:
- **Observable** — Based on something you can actually see, not something you have to interpret
- **Time-bound** — Include a deadline. "If we don't see X by {date}, reconsider."
- **Pre-committed** — Write them down BEFORE seeding. Kill criteria written after the fact are useless because you'll rationalize around them.

### Step 5 — Specify Seed Requirements

What does the Seed director need to know?
- Which domain orchestrators to engage
- What minimum capability must exist
- What the first feedback signal to watch for is
- What constraints should channel the emergence

## Thesis Quality Checks

Before a thesis is accepted:

| Check | Pass Criteria |
|---|---|
| **Specificity** | Could someone who disagrees point to exactly what they disagree with? |
| **Falsifiability** | Is there an observable outcome that would kill the thesis? |
| **Evidence balance** | Has evidence against been actively sought, not just evidence for? |
| **Time-grounding** | Is there a clear reason this is viable NOW but wasn't before? |
| **Kill commitment** | Are kill criteria written in advance, not retroactively? |
| **Strategic coherence** | Does this fit the product narrative, or does the narrative need updating? |

## Connection to The Loom Cycle

**Input from:** possibility-mapper (the chosen possibility), capability-radar (readiness), frontier-antenna (timing), signal-reader (market)

**Output to:** Seed director (condition-designer receives the thesis + seed requirements)

**Update:** narrative-keeper records the thesis in the product narrative. initiative-tracker creates a new initiative in `seed` state.
