---
name: prototype-grower
description: >
  Grow rapid capability prototypes — not wireframes or mockups but living demonstrations of
  capability combinations. Shows what happens when you combine specific domains for a product
  use case. Use when a seed specification needs to become tangible, or when "show me" is
  more useful than "tell me."
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Write Bash Glob Grep Agent
---

# Prototype Grower — Living Demonstrations

A prototype in AI-native product design isn't a wireframe. It isn't a mockup. It isn't a clickable dummy. It's a **living demonstration** — a real capability combination running in a constrained context that shows what the product could become.

"Here's what happens when you combine design + writing + data science for this use case" — and then actually doing it.

## What Makes a Good Prototype

**Living:** It actually works. It uses real capabilities, not simulations.
**Bounded:** It operates within the seed specification's constraints.
**Observable:** You can see what it does, including unexpected behaviors.
**Disposable:** It's meant to teach, not to ship. Kill it without regret.

## Process

### Step 1 — Read the Seed Specification

From `seed/condition-designer`, extract:
- Capability ingredients (which domains to combine)
- Constraints (hard, soft, open space)
- What we're watching for (expected emergence, surprise zones)

### Step 2 — Choose Prototype Form

| Form | When | How |
|---|---|---|
| **Live demonstration** | When the capabilities can be combined in a conversation | Run the capability combination in real-time, observing what happens |
| **Artifact** | When the output is a tangible thing (document, visualization, analysis) | Produce the artifact using the combined capabilities |
| **Interactive build** | When the prototype needs a surface users can touch | Engage `master-artificer` for creative coding |
| **Scenario walkthrough** | When the product is too complex for a single demo | Walk through a specific user scenario, invoking capabilities at each step |

### Step 3 — Grow the Prototype

Execute the capability combination within the seed's constraints:

1. **Engage domain orchestrators** specified in the seed. Provide the constraint context.
2. **Let them interact.** Don't over-direct. The point is to see what the combination produces.
3. **Observe and record.** What worked? What was unexpected? Where did capabilities clash?
4. **Note emergence.** Did the combination produce behaviors or outputs beyond what either domain could alone?

### Step 4 — Document What Grew

```markdown
# Prototype Report: {initiative name}

## What We Grew
{Description of what the prototype does/produces}

## Capabilities Combined
{Which domains, how they interacted}

## What Worked
{Behaviors and outputs that validated the thesis}

## What Surprised Us
{Unexpected behaviors — the most valuable section}

## What Clashed
{Where capabilities fought each other or produced incoherent output}

## Emergence Observed
{Behaviors beyond what was specified — flag for emergence-detector}

## Recommendation
{Seed further / redesign conditions / compost the idea}
```

## Cross-Domain

- **master-artificer** — For interactive prototypes that need a visual or interactive surface. Provide the capability combination spec and let master-artificer build it.
- **All domain orchestrators** — The prototype grower is the only skill that routinely engages multiple domain orchestrators simultaneously. It's the rehearsal for what The Loom does at scale.
