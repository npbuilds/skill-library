---
name: evolve
description: >
  Route product evolution work — observing how surfaced products change through use,
  amplifying emergent successful patterns, pruning what isn't working, and designing
  self-improving feedback systems. Activates when a product is live and the question
  is "how is it growing, and what should we do about it?"
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Write Bash Glob Grep Agent
---

# Evolve — The Adaptation Engine

The product is alive. It was seeded, it germinated, it emerged, it was surfaced. Now it's in the world, being used, changing from interaction. Evolve manages this growth — not by redesigning the product, but by observing its adaptation and making strategic interventions.

The key insight: most of what needs to happen post-surface is **not adding things**. It's noticing what's happening, amplifying what works, and pruning what doesn't.

## Child Skills

| Skill | Type | When to Route |
|---|---|---|
| `adaptation-observer` | action | Watching how the product-in-use differs from the product-as-designed |
| `amplifier` | action | Strengthening emergent successful patterns |
| `pruning-engine` | action | Deciding what to compost, simplify, or let atrophy |
| `learning-loops` | knowledge | Frameworks for self-improving systems |

## Routing Logic

| Signal | Route To |
|---|---|
| "What's happening?", "how are users behaving?", "what changed?" | adaptation-observer |
| "This is working — how do we get more?" | amplifier |
| "This isn't working", "simplify", "cut", "compost" | pruning-engine |
| "How does it get better on its own?", "self-improvement" | learning-loops |
| "Full evolution review" | adaptation-observer → amplifier + pruning-engine → learning-loops |

## Curriculum Order

```
adaptation-observer (observe first) → learning-loops (understand how learning works)
→ amplifier (strengthen good) → pruning-engine (remove bad)
```

## The Evolve → Synthesize Connection

Evolution signals feed directly into Synthesize:
- **pattern-weaver** — Evolution patterns across multiple products reveal meta-capabilities
- **narrative-keeper** — Significant evolution events become turning points in the product narrative
- **initiative-tracker** — Evolution state transitions get recorded
