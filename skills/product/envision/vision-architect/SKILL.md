---
name: vision-architect
description: >
  Design the intelligence system's future state in experiential terms — not feature lists
  but what it's like to interact with this intelligence. Produces vision documents that
  describe capabilities and feelings, not screens and buttons. Use when the user needs to
  articulate what a product should become, or when a thesis needs a vivid target state.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Write bash Glob Grep Agent
---

# Vision Architect — Designing the Future State

A product vision for an intelligence system isn't a feature roadmap. It's an experiential description: what it's like to interact with this intelligence when it's working well. Not what it does — what it feels like.

"The system anticipates what you need before you ask, surfaces the right capability at the right moment, and learns your working style so deeply that using it feels like thinking with a second brain" — that's a vision.

"Dashboard with 5 widgets, notification system, and AI-powered search" — that's a feature list. The vision-architect never writes feature lists.

## Process

### Step 1 — Gather Inputs

Read:
- Latest capability radar from `sense/capability-radar` — what's possible
- Active themes from `loom-briefings/product-narrative.md` — what we believe
- The thesis from `envision/thesis-forge` if one exists — what we're betting on
- User context — who is this for, what's their current experience

### Step 2 — Describe the Experience

Write a **future-state narrative** in present tense, as if the product already exists:

- **The moment of first contact** — What happens when someone encounters this intelligence for the first time? What do they feel? Curiosity? Relief? Surprise?
- **The daily rhythm** — What does ongoing interaction look like? Is it active (you come to it) or ambient (it comes to you)? Is it a focused session or a background presence?
- **The surprise moment** — What unexpected thing does the intelligence do that makes the user think "I didn't know it could do that"? This is the emergence signal made experiential.
- **The trust deepening** — How does the relationship between user and intelligence develop over time? What does month 1 feel like vs. month 6?
- **The absence test** — If the user lost access, what would they miss most? This reveals the true value.

### Step 3 — Articulate Design Principles

From the narrative, extract 3-5 design principles that should govern every decision:

Format:
```
1. {Principle name}: {one-sentence principle}
   This means: {specific implication for design decisions}
   This does NOT mean: {common misinterpretation to avoid}
```

### Step 4 — Define the Capability Architecture

Map the vision to the domain capability needed:

```
Vision element: {aspect of the experience}
  Requires: {domain orchestrator(s)}
  Maturity needed: {current maturity vs. required}
  Gap: {what doesn't exist yet}
```

### Step 5 — Output the Vision Document

```markdown
# Vision: {product/initiative name}

## The Experience
{Future-state narrative in present tense, 300-500 words}

## Design Principles
1. {principle}
2. {principle}
3. {principle}

## Capability Architecture
{Vision element → domain mapping}

## What This Is NOT
{Explicit anti-patterns — common interpretations to avoid}

## Kill Signal
{What observation would tell us this vision is wrong?}
```

## Cross-Domain Engagement

- **design-orchestrator** (aesthetic-identity) — When the vision needs visual/emotional language. "What does this intelligence look like when it's thinking?"
- **prose-orchestrator** — When the vision narrative needs crafting. The vision document IS a piece of writing.
- **philosophy-orchestrator** — When the vision touches on how intelligence should relate to humans. Ethical and epistemological grounding.
