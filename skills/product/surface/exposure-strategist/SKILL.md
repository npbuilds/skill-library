---
name: exposure-strategist
description: >
  Decide which capabilities to surface, when, to whom, and in what sequence. Not everything
  the system can do should be visible. Sequencing exposure builds trust, reveals complexity
  gradually, and prevents overwhelm. Use when a capability is ready and needs an exposure plan.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Write bash Glob Grep Agent
---

# Exposure Strategist — The Art of Revelation

A common failure: surface everything at once. The user drowns. Trust breaks. The product feels chaotic.

The opposite failure: surface too little. The user never discovers what the system can do. Capabilities rot unseen.

The exposure strategist finds the path between: revealing the right capability at the right moment to the right person, building trust with each revelation.

## Exposure Principles

1. **Lead with the core loop.** Surface the one capability that demonstrates the product's essential intelligence first. Everything else builds from there.
2. **Earn the right to complexity.** Each new capability surfaced should be earned by successful use of the previous one.
3. **Surprise strategically.** Occasional "I didn't know it could do that" moments build delight and trust. But too many surprises feel random.
4. **Hide intentionally.** Some capabilities are better discovered than presented. Design discovery paths, not feature tours.
5. **Time exposure to readiness.** The capability must be reliable enough for the audience it's being shown to.

## The Exposure Plan

### Step 1 — Classify the Audience

| Segment | Exposure Approach |
|---|---|
| **Power users / builders** | Surface raw capability early. They'll find the edges themselves. |
| **Early adopters** | Surface with a guided narrative. Show what's possible, let them explore. |
| **General users** | Surface progressively. Start simple, reveal depth over time. |
| **Other agents/systems** | Surface as APIs/interfaces. Optimize for machine readability. |

### Step 2 — Sequence the Capabilities

For each capability to be surfaced, determine:

| Capability | Audience | Timing | Prerequisites | Form |
|---|---|---|---|---|
| {what} | {who sees it} | {when} | {what must come first} | {how it appears} |

Sequencing rules:
- **Foundation before decoration** — Core value first, polish later
- **Familiar before novel** — Connect to what users already understand before introducing new paradigms
- **Reversible before irreversible** — Let users experiment safely before exposing actions with consequences
- **Observable before opaque** — Show transparent intelligence before ambient/invisible intelligence

### Step 3 — Design Discovery Paths

Not all capabilities need to be in a menu. Some are better found:

| Discovery Method | When to Use |
|---|---|
| **Direct presentation** | Core capabilities that define the product |
| **Contextual reveal** | Capabilities that make sense only in specific contexts |
| **Earned unlock** | Advanced capabilities that require prerequisite understanding |
| **Organic discovery** | Capabilities users find by exploring or asking "can you do X?" |
| **Social discovery** | Capabilities users learn about from other users |

### Step 4 — Output the Exposure Plan

```markdown
# Exposure Plan: {initiative name}

## Core Loop (expose first)
{The one capability that demonstrates the product's intelligence}
Audience: {who}
Form: {how}

## Sequence
Phase 1: {capabilities} — {why these first}
Phase 2: {capabilities} — {what they build on from Phase 1}
Phase 3: {capabilities} — {the full depth}

## Hidden Capabilities (discover, don't present)
{capabilities}: discoverable via {method}

## Readiness Gates
{capability}: ready when {condition}

## Trust Milestones
After Phase 1: user trusts {what}
After Phase 2: user trusts {what deeper}
After Phase 3: user trusts {the full capability}
```

## Cross-Domain

- **game-theory-orchestrator** — Progressive disclosure is an incentive design problem. Each revelation should increase the user's motivation to explore further.
- **prose-orchestrator** — Exposure sequencing IS narrative pacing. The order of revelation tells a story.
