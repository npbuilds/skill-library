---
name: pruning-engine
description: >
  Decide what to stop, simplify, or let atrophy. Not "kill features" — compost them. Extract
  the learnings, preserve what's reusable, let the rest go. Every pruning decision feeds the
  Sense director with new signals. Use when something isn't working, is too complex, or has
  served its purpose.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Write bash Glob Grep Agent
---

# Pruning Engine — The Wisdom of Letting Go

Pruning isn't failure. It's cultivation. A gardener prunes to direct energy toward growth. A product builder prunes to direct intelligence toward value.

The pruning engine decides what to compost (fully retire), simplify (reduce complexity), or let atrophy (stop investing, let natural decay handle it).

## When to Prune

| Signal | Interpretation |
|---|---|
| Usage declining steadily | Capability may no longer be needed or may be served better elsewhere |
| Negative feedback increasing | The experience is degrading or expectations have changed |
| Maintenance cost exceeding value | The capability consumes more than it contributes |
| Capability commoditized | Others offer this now. Our version adds no unique value. |
| Thesis invalidated | Kill criteria met. The bet didn't pay off. |
| Energy needed elsewhere | Opportunity cost. A more promising seed needs the attention. |

## Pruning Modes

### Compost (Full Retirement)

The initiative or capability is retired completely. But nothing is wasted:

1. **Document the thesis** — Was it validated or invalidated? Why?
2. **Extract learnings** — What did we learn that applies beyond this initiative?
3. **Preserve reusable capabilities** — Any skills, patterns, or connections worth keeping?
4. **Update the narrative** — narrative-keeper records the composting with full context
5. **Feed Sense** — The freed capability and learnings create new inputs for the next cycle

### Simplify (Reduce Complexity)

The core is valuable but it's grown too complex. Cut back to essentials:

1. **Identify the core loop** — What's the one thing that makes this valuable?
2. **Remove everything else** — Features, options, configurations that don't serve the core
3. **Strengthen what remains** — Freed energy goes into the simplified core
4. **Re-observe** — Does the simplified version perform better?

### Atrophy (Benign Neglect)

Stop investing, but don't actively remove. Let it naturally fade:

1. **When:** The capability isn't harmful but isn't worth active maintenance
2. **Risk:** It degrades slowly and creates a bad experience for the few who find it
3. **Mitigation:** Set a review date. If it hasn't improved by then, compost it.

## The Composting Retrospective

Every composted initiative must produce:

```markdown
# Composting Retrospective: {initiative name}

## Lifespan
Seeded: {date} | Composted: {date} | Peak state: {highest lifecycle state reached}

## The Thesis
{What we believed}

## What Actually Happened
{What the product did in the world}

## Verdict
{Validated / Invalidated / Inconclusive}

## What We Learned
1. {Learning that applies beyond this initiative}
2. {Learning}
3. {Learning}

## What Survives
Capabilities: {skills, patterns, or connections preserved}
Learnings: {insights fed into product narrative}
Conditions: {seed conditions that worked, for reuse}

## What Dies
{What we're letting go of — and why it's okay}
```

## Cross-Domain

- **infrastructure-orchestrator** — For technical cleanup when pruning capabilities (deprecating skills, removing references)
- **synthesize/narrative-keeper** — Every composting is a story event that must be recorded
