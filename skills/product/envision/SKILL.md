---
name: envision
description: >
  Route product vision work — designing what the intelligence system should become, exploring
  new interaction paradigms for AI products, mapping the full possibility space, and crystallizing
  falsifiable product theses. Activates when the question is "what should this intelligence
  become?" or "what's possible and what do we believe?"
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Write Bash Glob Grep Agent
---

# Envision — The Imagination Engine

The second cognitive mode. After Sense reads the field, Envision asks the harder question: **given what's possible, what SHOULD this intelligence become?**

This isn't roadmapping. Roadmaps list features on timelines. Envision designs the *shape* of the intelligence — what kind of system are we growing, who does it serve, what does it feel like to interact with it, and why does it deserve to exist?

## Child Skills

| Skill | Type | When to Route |
|---|---|---|
| `vision-architect` | action | Designing the system's future state in experiential terms |
| `paradigm-designer` | knowledge | Exploring and creating new AI interaction paradigms |
| `possibility-mapper` | action | Mapping the full space of what could be built |
| `thesis-forge` | action | Crystallizing a specific, falsifiable product thesis |

## Routing Logic

| Signal | Route To |
|---|---|
| "What should this become?", "long-term vision", "future state" | vision-architect |
| "What kind of interface?", "interaction paradigm", "how should it work?" | paradigm-designer |
| "What could we build?", "show me the options", "explore possibilities" | possibility-mapper |
| "What do we believe?", "product thesis", "why this?" | thesis-forge |
| "I have a vague idea, help me shape it" | possibility-mapper → thesis-forge → vision-architect |

## Curriculum Order

```
paradigm-designer (know the paradigms) → possibility-mapper (explore the space)
→ vision-architect (choose a direction) → thesis-forge (crystallize the bet)
```

## Cross-Domain Interfaces

| Child Skill | Engages | For |
|---|---|---|
| vision-architect | design-orchestrator (aesthetic identity), prose-orchestrator | Vision articulation in experiential and narrative terms |
| paradigm-designer | design-orchestrator, philosophy-orchestrator | Epistemology of human-AI interaction, aesthetic exploration |
| possibility-mapper | game-theory-orchestrator (option value), neocortex/scenario-planner | Strategic valuation of possibilities, future-state modeling |
| thesis-forge | spelunker | Validation research for thesis assumptions |

## The Envision → Seed Handoff

Envision produces a thesis and a vision. Seed receives these and designs the conditions for emergence. The handoff should include:

1. **The thesis** — one sentence, falsifiable, with kill criteria
2. **The paradigm** — what interaction model fits this vision
3. **The capability ingredients** — which domains contribute, at what maturity
4. **The experience sketch** — what it feels like (not how it looks), in 2-3 sentences
