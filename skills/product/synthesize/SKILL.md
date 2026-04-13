---
name: synthesize
description: >
  Route product synthesis work — cross-product pattern recognition, initiative lifecycle
  tracking, weekly product briefing generation, and product narrative maintenance. Activates
  when the question spans multiple products, asks about the overall product landscape, needs
  a strategic zoom-out, or requests the weekly product synthesis. The Loom's reflective
  intelligence — seeing the meta-pattern across everything.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Write Bash Glob Grep Agent
---

# Synthesize — The Loom's Reflective Intelligence

The director that sees across all products, all domains, all time. While other directors focus on one cognitive mode (sense, envision, seed, surface, evolve), Synthesize holds the whole picture and produces the strategic narrative.

This is where The Loom becomes self-aware — reflecting on what the product suite is becoming, what patterns connect successful initiatives, and what the evolving story means.

## Child Skills

| Skill | Type | When to Route |
|---|---|---|
| `pattern-weaver` | action | Cross-product patterns, meta-capability detection, domain synergy analysis |
| `initiative-tracker` | action | Initiative status, lifecycle transitions, portfolio view |
| `product-briefing-engine` | action | Weekly Product Synthesis generation |
| `narrative-keeper` | action | Product narrative updates, decision history, story evolution |

## Routing Logic

| Signal | Route To |
|---|---|
| "What's the big picture?", "across all products", "meta-pattern" | pattern-weaver |
| "Where are initiatives?", "status", "what's in flight?", "what state is X in?" | initiative-tracker |
| "Brief me", "weekly synthesis", "what should I know?" | product-briefing-engine |
| "What's our story?", "how has thinking evolved?", "product narrative" | narrative-keeper |
| "Something is working across multiple products" | pattern-weaver → narrative-keeper |
| "I need to make a decision about the portfolio" | initiative-tracker → pattern-weaver → product-briefing-engine |

## Multi-Skill Sequences

**Full synthesis cycle:**
initiative-tracker (know the state) → pattern-weaver (see the patterns) → product-briefing-engine (synthesize the brief) → narrative-keeper (update the story)

**Decision support:**
initiative-tracker (context) → pattern-weaver (what's worked before) → route to user for decision → narrative-keeper (record the decision)

## Key Files

This director reads and writes the living documents in `loom-briefings/`:

| File | Purpose | Primary Writer |
|---|---|---|
| `loom-briefings/product-narrative.md` | The evolving product story | narrative-keeper |
| `loom-briefings/initiative-log.md` | Initiative states and transitions | initiative-tracker |
| `loom-briefings/emergence-log.md` | Unexpected capability combinations | pattern-weaver |
| `loom-briefings/decision-journal.md` | Product decisions with reasoning | narrative-keeper |

## Cross-Domain Interfaces

- **prose-orchestrator** — narrative-keeper engages writing for narrative quality
- **All orchestrators** — pattern-weaver reads across every domain for synthesis
- **neocortex/architecture** — pattern-weaver shares structural observations about the library
- **infrastructure-orchestrator** — initiative-tracker may use registry data for capability assessment
