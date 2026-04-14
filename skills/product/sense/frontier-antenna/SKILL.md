---
name: frontier-antenna
description: >
  Translate AI frontier developments into product opportunities. Consumes neocortex/frontier-scanner
  output and reframes it through a product lens — not "what's new in AI" but "what does this
  make buildable that wasn't before?" Use when a new model drops, a capability shifts, or the
  tool ecosystem changes and you need to understand the product implications.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Write bash Glob Grep Agent
---

# Frontier Antenna — Product Opportunity Translator

Neocortex's frontier-scanner watches what's happening in AI. The frontier-antenna watches what it **means for products**. Same signal, different lens.

"Claude now has 1M context" is a frontier scan finding. "We can now build a product that holds an entire codebase in memory" is a frontier-antenna finding.

## Process

### Step 1 — Ingest Frontier Intelligence

Read the latest from neocortex's frontier scanning system:
- `data/frontier-scans.jsonl` for recent scan entries
- Engage `neocortex/frontier-scanner` via Agent for real-time scans if data is stale

For each development, extract:
- **What changed** — the raw capability shift
- **Magnitude** — incremental improvement or step-change?
- **Timeline** — available now, weeks, months?

### Step 2 — Product Lens Translation

For each significant development, answer three questions:

1. **What does this make possible?** — New product categories, new capability surfaces, new interaction paradigms that didn't exist before this development.
2. **What does this make obsolete?** — Existing products, workarounds, or manual processes that this development makes unnecessary.
3. **What does this make urgent?** — Windows of opportunity that will close. First-mover advantages. Capabilities that will be commoditized soon.

### Step 3 — Opportunity Classification

Classify each opportunity:

| Class | Definition | Action |
|---|---|---|
| **Unlock** | Entirely new product category now possible | Flag for Envision — thesis-forge |
| **Upgrade** | Existing surface can be meaningfully improved | Flag for Evolve — amplifier |
| **Commoditize** | Something we do becomes table-stakes | Flag for Evolve — pruning-engine |
| **Window** | Temporary advantage before others catch up | Flag urgently for Seed |

### Step 4 — Output

Produce a **frontier opportunity brief**:

```
=== FRONTIER ANTENNA — {date} ===

Developments scanned: {count}
Opportunities identified: {count}

--- UNLOCKS ---
{development}: {what it makes possible}
  Product implication: {specific product opportunity}
  Confidence: {High/Medium/Low}
  Time window: {how long before this is commoditized}

--- UPGRADES ---
{development}: {what it improves}
  Affected surfaces: {which existing products benefit}

--- COMMODITIZATIONS ---
{development}: {what it makes table-stakes}
  Action needed: {differentiate or deprioritize}

--- WINDOWS ---
{development}: {temporary advantage}
  Window estimate: {weeks/months before others catch up}
  Urgency: {act now / monitor / low}
```

## When NOT to Use

- For raw frontier scanning without product context → use neocortex/frontier-scanner directly
- For deep research on a specific technology → use spelunker
- For market/competitive analysis → use signal-reader
