# Synthesize — Quick Reference


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

## Quick Reference

| File | Purpose | Primary Writer |
|---|---|---|
| `loom-briefings/product-narrative.md` | The evolving product story | narrative-keeper |
| `loom-briefings/initiative-log.md` | Initiative states and transitions | initiative-tracker |
| `loom-briefings/emergence-log.md` | Unexpected capability combinations | pattern-weaver |
| `loom-briefings/decision-journal.md` | Product decisions with reasoning | narrative-keeper |
