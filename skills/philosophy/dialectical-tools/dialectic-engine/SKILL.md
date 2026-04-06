---
name: dialectic-engine
description: >
  Run structured thesis/antithesis/synthesis dialogues and manage multi-round
  point-counterpoint exchanges. Use when the user wants to explore both sides of a
  question systematically, generate a synthesis from opposing views, run a structured
  debate to clarify a complex issue, or produce a balanced analysis by giving each
  perspective its strongest voice.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Write
---

# Dialectic Engine — The Parliament

Convene opposing views, let each speak at full strength, and forge a synthesis from the collision. The dialectic engine doesn't seek compromise (splitting the difference) — it seeks synthesis (a higher-order understanding that incorporates the truths from both sides while resolving their conflict).

## Input

From the dialectical-tools director or directly:
- The question or topic to dialecticize
- Starting positions (if the user has them — otherwise the engine generates them)
- Mode: **classic** (thesis/antithesis/synthesis), **multi-voice** (3+ perspectives), or **iterative** (multiple rounds of refinement)
- Rounds: how many exchanges (default: 3 for classic, user-specified for iterative)

## Process

### Step 1 — Frame the Dialectic

Identify the core tension. Every productive dialectic starts with a genuine disagreement — not a straw fight but a real conflict between positions that both have merit.

- **The question**: What's being debated?
- **The stakes**: Why does it matter which side is right?
- **The tension**: Why can't both sides be fully right simultaneously?

If no genuine tension exists (one side is clearly correct), report this and offer to find a more productive framing.

### Step 2 — Establish the Thesis

The thesis is the initial position — stated as strongly and charitably as possible.

- Present the thesis in its best form (invoke steel-man-forge principles)
- Identify its core insight — the truth it captures
- Note its strongest evidence and arguments
- Acknowledge its known limitations honestly

### Step 3 — Establish the Antithesis

The antithesis is not merely "the thesis is wrong" — it's a positive counter-position that captures a different truth.

- Present the antithesis in its best form (equally steel-manned)
- Identify its core insight — the different truth it captures
- Note its strongest evidence and arguments
- Show specifically where and why it contradicts the thesis

**Quality check**: If the antithesis is weaker than the thesis, strengthen it. A dialectic with an asymmetric fight teaches nothing.

### Step 4 — The Exchange

Run the dialogue. Each side responds to the other's strongest points:

**Round structure:**
```
Thesis:     [opening statement — strongest case]
Antithesis: [response — addresses thesis's strongest points, advances own case]
Thesis:     [reply — addresses antithesis's challenges, refines position]
Antithesis: [reply — addresses thesis's refinement, refines own position]
...
```

**Exchange rules:**
- Each side must address the other's strongest point (no dodging)
- Each side must acknowledge what the other gets right (no blanket denial)
- Each round should refine, not just repeat
- Concessions are signs of strength, not weakness

### Step 5 — Forge the Synthesis

The synthesis is not a compromise (average of two positions) but a transcendence (a new position that captures what's right about both while resolving the conflict).

**Synthesis strategies:**

| Strategy | When It Works | Example |
|----------|-------------|---------|
| **Scope distinction** | Both are right, but in different domains | "Thesis is right for X situations; antithesis is right for Y situations" |
| **Level distinction** | Both are right, but at different levels of analysis | "Thesis is right about individuals; antithesis is right about systems" |
| **Temporal distinction** | Both are right, but at different time scales | "Thesis is right short-term; antithesis is right long-term" |
| **Integration** | Elements from both combine into a stronger position | "Take mechanism from thesis + constraint from antithesis" |
| **Reframing** | The conflict dissolves under a different framing | "The disagreement assumed X; without that assumption, both insights coexist" |

**If synthesis is not possible**: Report this honestly. Some disagreements are genuine and irreducible — they reflect different foundational values, not different analyses. In this case, the dialectic's value is clarifying exactly where and why the disagreement exists.

### Step 6 — Assess the Dialectic

After the exchange:
- **What was learned?** What do we understand now that we didn't before?
- **What was resolved?** Which aspects of the disagreement were settled?
- **What remains contested?** Which aspects are genuinely irreducible?
- **What's the crux?** What single question or value choice determines which side you land on?

## Output

### Classic Mode
```
DIALECTIC
─────────
Question: [the core question]

THESIS: [position name]
  [2-3 paragraph statement of the thesis at full strength]
  Core insight: [the truth this captures]

ANTITHESIS: [position name]
  [2-3 paragraph statement of the antithesis at full strength]
  Core insight: [the different truth this captures]

EXCHANGE:
  Round 1:
    Thesis responds: [addresses antithesis's strongest point]
    Antithesis responds: [addresses thesis's strongest point]
  Round 2:
    Thesis refines: [adjusted position]
    Antithesis refines: [adjusted position]

SYNTHESIS:
  [The higher-order understanding — what's right about both, how the conflict resolves]
  Strategy: [scope/level/temporal/integration/reframing]

  Or if irreducible:
  [Why this disagreement cannot be synthesized, and what determines which side you take]

What was learned: [key insight from the dialectic]
Crux: [the question whose answer determines your position]
```

### Multi-Voice Mode
```
MULTI-VOICE DIALECTIC
─────────────────────
Question: [the core question]

VOICE 1: [perspective name]
  [statement] — Core insight: [truth captured]

VOICE 2: [perspective name]
  [statement] — Core insight: [truth captured]

VOICE 3: [perspective name]
  [statement] — Core insight: [truth captured]

CONVERGENCE: [where voices agree]
DIVERGENCE: [where they split and why]
SYNTHESIS: [integration or honest report of irreducible disagreement]
```

## Error Handling

**No genuine disagreement exists:** Don't manufacture one. Report that the question has a clear answer and offer to find a more productively contested framing.

**One side is clearly stronger:** Check whether the weaker side has been fully steel-manned. If it has and is still weak, report the asymmetry — this is a finding, not a failure. Not every question is 50/50.

**User wants a specific side to win:** Run the dialectic honestly. If their preferred side wins on merit, great. If not, the dialectic is doing its job — showing them the strongest case against their position.

**Synthesis feels forced:** Don't force it. An honest "these positions are genuinely incompatible because they prioritize different values" is more useful than a fake synthesis that papers over real disagreement.
