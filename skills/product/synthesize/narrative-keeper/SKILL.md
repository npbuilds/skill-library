---
name: narrative-keeper
description: >
  Maintain the living product narrative — the evolving story of what this intelligence system
  is, where it came from, where it's going, and what it believes. Use when updating the product
  story after significant events, recording major decisions with reasoning, reflecting on how
  product thinking has evolved, or when someone asks "what's the story of this product suite?"
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Write bash Glob Grep Agent
---

# Narrative Keeper — The Product's Memory

Every intelligence system has a story. Not a marketing narrative — a true story of what was tried, what was learned, what was believed and then revised, what surprised the builder, and what the system is becoming.

The narrative keeper maintains this story as a living document. It's the institutional memory of product decisions, the evolution of product thinking, and the continuous answer to: "What is this system, and what is it becoming?"

## What the Narrative Contains

The product narrative (`loom-briefings/product-narrative.md`) is structured as an evolving document with these sections:

### Active Themes

What the product suite currently believes and is acting on. These are the living strategic convictions.

Format:
```markdown
### Theme: {name}
**Conviction:** {High / Medium / Developing}
**First articulated:** {date}
**Last reinforced:** {date}
**Evidence:** {what supports this belief}
**What would change this:** {falsification criteria}
```

Themes are not features or initiatives — they're beliefs about how intelligence products should work, what users need, or where the market is going.

### Turning Points

Moments where the product thinking changed direction. Each turning point records:

```markdown
### Turning Point: {name}
**Date:** {date}
**What changed:** {the old belief → the new belief}
**Trigger:** {what caused the shift — data, experience, frontier development, conversation}
**Impact:** {what changed as a result — initiatives composted, new seeds planted, priorities reordered}
```

### Composted Experiments

A graveyard that feeds the garden. Each composted initiative gets a brief eulogy:

```markdown
### Composted: {initiative name}
**Lived:** {seed date} → {compost date}
**Thesis:** {what we believed}
**What we learned:** {the valuable insight, even if the initiative failed}
**What survived:** {capabilities, learnings, or patterns that live on elsewhere}
```

### Decision Log

Major product decisions with full context. Not every decision — only the ones that shaped the system's direction.

```markdown
### Decision: {title}
**Date:** {date}
**Context:** {what situation prompted this decision}
**Options considered:** {what alternatives existed}
**Chose:** {what was decided}
**Reasoning:** {why — the actual reasoning, not post-hoc justification}
**What would prove this wrong:** {falsification}
```

### The Story So Far

A periodically updated narrative summary — the "elevator pitch" version of the product story. Written in the past-present-future structure:

- **Where we came from:** How this intelligence system started and what early beliefs shaped it
- **Where we are:** What the system can do today, what's in flight, what's working
- **Where we're going:** Current vision, active themes, strategic direction

This section is rewritten (not appended) whenever the story meaningfully changes.

## When to Update

| Event | What to Update |
|---|---|
| Weekly Product Synthesis completed | Review active themes; update if convictions changed |
| Initiative composted | Add to Composted Experiments |
| Major product decision | Add to Decision Log |
| Product thinking shifts | Add Turning Point; may rewrite The Story So Far |
| New theme emerges from pattern-weaver | Add to Active Themes with Developing conviction |
| Theme conviction strengthens | Update conviction level and evidence |
| Frontier shift changes strategy | Turning Point + theme updates |

## Narrative Quality Principles

1. **Honest, not promotional.** This isn't marketing. Record what actually happened, including mistakes, wrong turns, and surprises. The value is in the truth.

2. **Reasoning over conclusions.** Don't just record what was decided — record WHY. Future-you reading this narrative needs to understand the reasoning to know if it still applies.

3. **Falsification over confirmation.** Every theme and decision includes "what would change this." A conviction without falsification criteria is a bias, not a belief.

4. **Continuity over completeness.** The narrative is a story, not a database. It should read as a coherent evolution of thinking, not a list of disconnected events.

5. **Concise over comprehensive.** Only record what matters. Not every meeting, not every small decision. The narrative should be readable in 10 minutes and cover the full arc.

## Cross-Domain

When narrative quality matters (rewriting The Story So Far, crafting a particularly important Turning Point), engage `prose-orchestrator` with:
- The raw content to be narrated
- Tone: reflective, honest, concise
- Audience: the builder themselves, reading this 6 months from now
- Purpose: institutional memory, not external communication
