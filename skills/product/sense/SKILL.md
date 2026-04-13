---
name: sense
description: >
  Route product sensing work — reading frontier signals through a product lens, detecting
  emergent capability combinations, interpreting external market and technology signals, and
  mapping the gap between what's possible and what's surfaced. Activates when the question is
  "what's becoming possible?" or "what's changing that matters for product?"
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Write Bash Glob Grep Agent
---

# Sense — The System's Peripheral Vision

The first cognitive mode. Before envisioning, seeding, or surfacing anything, The Loom needs to know what's happening — in the AI frontier, in the skill library's own emergent behavior, in the market, and in the gap between current capability and current exposure.

Sense doesn't decide what to build. It decides what's **worth paying attention to**.

## Child Skills

| Skill | Type | When to Route |
|---|---|---|
| `frontier-antenna` | action | AI developments, new model capabilities, tool ecosystem changes — through a product lens |
| `emergence-detector` | action | Unexpected capability combinations in the library, behaviors nobody designed |
| `signal-reader` | knowledge | External signal interpretation: market timing, adoption curves, technology readiness |
| `capability-radar` | action | Mapping possible vs. surfaced capabilities, finding the opportunity gap |

## Routing Logic

| Signal | Route To |
|---|---|
| "What's new in AI that matters for us?" | frontier-antenna |
| "I noticed something unexpected in the system" | emergence-detector |
| "Is the timing right?", "adoption curves", "market signals" | signal-reader |
| "What can we do that we haven't exposed?", "capability gap" | capability-radar |
| "Give me a full field report" | All four in sequence: frontier-antenna → emergence-detector → capability-radar → signal-reader for synthesis |

## Curriculum Order

```
signal-reader (learn the frameworks) → frontier-antenna (apply to AI frontier)
→ capability-radar (map the landscape) → emergence-detector (watch for surprises)
```

## Cross-Domain Interfaces

| Child Skill | Engages | For |
|---|---|---|
| frontier-antenna | neocortex/frontier-scanner | Raw frontier scan data, translated through product lens |
| emergence-detector | All domain orchestrators | Monitoring cross-domain interaction patterns |
| signal-reader | spelunker, archon | Deep research on signals, market timing intelligence |
| capability-radar | infrastructure-orchestrator, neocortex/architecture | Registry health, gap maps, maturity assessments |

## Output

The Sense director produces a **field report** — a structured reading of what's changing, what's emerging, and what demands attention. This feeds directly into the Envision director.
