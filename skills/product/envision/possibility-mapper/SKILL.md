---
name: possibility-mapper
description: >
  Map the full space of possible products from current and emerging capabilities — before
  filtering to what should be built. Combines capability radar output with frontier signals
  to explore what COULD exist. Use when you want to see the landscape of options, find
  non-obvious product ideas, or ensure you're not anchoring on the first idea.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Write Bash Glob Grep Agent
---

# Possibility Mapper — The Option Space Explorer

Before choosing what to build, see what you COULD build. The possibility mapper takes the capability radar (what exists), the frontier antenna (what's becoming possible), and the emergence log (what's surprised us) — and maps the full space of product possibilities.

This is anti-anchoring. Solo builders' most common failure mode is falling in love with the first idea. The possibility mapper forces you to see alternatives before committing.

## Process

### Step 1 — Gather the Inputs

Read:
- Latest capability radar scan (surfaced / latent / emerging capabilities)
- Latest frontier antenna brief (unlocks, upgrades, windows)
- `loom-briefings/emergence-log.md` (unexpected combinations)
- Active initiative states from `loom-briefings/initiative-log.md` (to see white space)

### Step 2 — Generate the Possibility Space

Apply three generation methods:

**Method 1: Capability Combination Matrix**

Pick the top latent capabilities from the radar. Cross them:

```
              | Design    | Data Sci  | Game Theory | Writing   | ...
Design        | —         | dataviz+  | incentive   | brand     |
              |           | aesthetic  | UX          | narrative |
Data Science  |           | —         | strategic   | content   |
              |           |           | analytics   | analytics |
Game Theory   |           |           | —           | persuasion|
              |           |           |             | mechanics |
```

Each cell is a potential product surface. Not all are valuable — the point is to see the space.

**Method 2: User Need Inversion**

Instead of "what can we build?", ask "what problems exist that our capabilities could solve?"

For each domain, list:
- What questions does this domain answer?
- Who outside the library asks those questions?
- What's their current (bad) solution?

**Method 3: Emergence Extrapolation**

For each entry in the emergence log:
- If this emergent behavior were the seed of a product, what would the product look like?
- What other capability combinations might produce similar unexpected value?

### Step 3 — Filter and Classify

For each possibility, quick-assess:

| Possibility | Capability Readiness | Uniqueness | Demand Signal | Type |
|---|---|---|---|---|
| {idea} | {high/medium/low} | {novel/incremental/commodity} | {strong/weak/unknown} | {surface/seed/explore} |

**Types:**
- **Surface** — Capability exists, just needs exposure. Immediate opportunity.
- **Seed** — Capability is 80% there, needs cultivation. Medium-term.
- **Explore** — Interesting but speculative. Needs validation before seeding.

### Step 4 — Output the Possibility Map

```
=== POSSIBILITY MAP — {date} ===
Inputs: {count} capabilities × {count} domains × {count} emergence signals

--- IMMEDIATE SURFACES (capability ready, just needs exposure) ---
1. {possibility}: {one-line description}
   Domains: {which} | Readiness: high | Uniqueness: {assessment}

--- SEEDS WORTH PLANTING (80% ready, needs cultivation) ---
1. {possibility}: {one-line description}
   Domains: {which} | Missing: {what's needed} | Timeline: {estimate}

--- WORTH EXPLORING (speculative, needs validation) ---
1. {possibility}: {one-line description}
   Domains: {which} | Unknown: {what we'd need to learn}

--- ANTI-POSSIBILITIES (tempting but wrong) ---
1. {possibility}: {why it's tempting but shouldn't be built}
```

The anti-possibilities section is as important as the possibilities. It prevents the builder from revisiting ideas that have been thoughtfully rejected.

## Cross-Domain

- **game-theory-orchestrator** (option value) — Not all possibilities are equal. Some are valuable because of what they enable NEXT, not what they deliver now. Option-value analysis from the investing/game-theory domains is critical here.
- **neocortex/scenario-planner** — Possibilities should be stress-tested against multiple futures. A possibility that only works in one scenario is riskier than one that works in several.

## Connection to The Loom Cycle

The possibility map feeds directly into **thesis-forge** — the next step where we go from "here's what's possible" to "here's what we believe and why."
