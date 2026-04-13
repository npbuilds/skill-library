---
name: capability-radar
description: >
  Produce a living map of what the intelligence system can do today vs. what's been surfaced
  to users. The gap between "possible" and "exposed" is the product opportunity space. Use
  when scanning for untapped capabilities, assessing readiness of capabilities for exposure,
  or building a comprehensive view of the system's current power.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Write Bash Glob Grep Agent
---

# Capability Radar — The Opportunity Gap Map

The most common product failure for intelligence systems isn't building the wrong thing — it's failing to surface what the system already knows how to do.

The capability radar maps three zones:

1. **Surfaced** — Capabilities actively exposed as products. Users interact with these.
2. **Latent** — Capabilities the system has but hasn't exposed. The hidden inventory.
3. **Emerging** — Capabilities that are 60-80% there, not yet reliable enough to surface.

The gap between Surfaced and Latent is the **immediate opportunity space** — no new building required, just exposure decisions. The gap between Latent and Emerging is the **cultivation space** — capabilities worth investing in.

## Scanning Process

### Step 1 — Inventory Surfaced Capabilities

Read `loom-briefings/initiative-log.md` for initiatives in `surfaced`, `evolving`, or `mature` states. These are the capabilities currently meeting the world.

### Step 2 — Map Latent Capabilities

Read `data/registry.json` and scan domain orchestrators for:

- **High-maturity domains** not involved in any surfaced initiative → latent capability
- **Cross-domain combinations** never tested → latent synthesis
- **Skills with high auto_score but zero usage** (read `data/usage.jsonl`) → hidden power
- **Domain orchestrators with mature sub-skills** that haven't been engaged by The Loom → untapped threads

For each domain orchestrator, assess:

| Domain | Maturity | Surfaced In Products? | Latent Capability |
|---|---|---|---|
| {domain} | {mature/growth/emerging} | {yes: which / no} | {what it could contribute} |

### Step 3 — Identify Emerging Capabilities

Consult `neocortex/architecture` (skill-cartographer, growth-architect) for:

- Domains under active development
- Skills recently added or upgraded
- Gap areas being actively filled

Cross-reference with `frontier-antenna` output for capabilities that frontier developments have just made possible.

### Step 4 — Produce the Radar

```
=== CAPABILITY RADAR — {date} ===

--- SURFACED (actively exposed) ---
{capability}: via {initiative/product} — state: {evolving/mature}
{capability}: via {initiative/product} — state: {evolving/mature}

--- LATENT (ready but unexposed) ---
{capability}: from {domain(s)} — readiness: {high/medium}
  Why unexposed: {no initiative / no surface form / no demand signal}
  Opportunity: {what product could this enable}

{capability}: from {domain(s)} — readiness: {high/medium}
  Why unexposed: ...
  Opportunity: ...

--- EMERGING (60-80% ready) ---
{capability}: from {domain(s)} — needs: {what's missing}
  Timeline: {when it could be ready}
  Blocking: {specific skills or capabilities needed}

--- OPPORTUNITY GAPS ---
Top 3 highest-value latent capabilities:
1. {capability} — value: {why}, readiness: {assessment}
2. {capability} — value: {why}, readiness: {assessment}
3. {capability} — value: {why}, readiness: {assessment}

--- SYNTHESIS OPPORTUNITIES ---
Cross-domain combinations never tested:
- {domain A} × {domain B}: potential for {what}
- {domain A} × {domain C}: potential for {what}
```

## Connection to The Loom Cycle

The capability radar feeds:
- **Envision** (possibility-mapper) — the radar IS the raw input for possibility mapping
- **Surface** (exposure-strategist) — latent capabilities ready for exposure decisions
- **Synthesize** (pattern-weaver) — radar trends over time reveal meta-patterns

## When to Run

- **Weekly** as part of the product synthesis cycle
- **On demand** when The Loom is evaluating a new product idea (does the capability already exist?)
- **After frontier shifts** when frontier-antenna identifies an unlock or commoditization
