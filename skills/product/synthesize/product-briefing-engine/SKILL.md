---
name: product-briefing-engine
description: >
  Generate the Weekly Product Synthesis — not a status report but a strategic narrative about
  what the intelligence system is becoming, what it learned this week, what's surprising, what
  needs attention, and what to do next. The Loom's equivalent of Archon's daily briefing.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Write Bash Glob Grep Agent
---

# Product Briefing Engine — Weekly Product Synthesis

Every week, the product suite deserves a moment of strategic reflection. Not a status update — a **synthesis**. What is the system becoming? What did it learn? What surprised us? What needs attention?

The Weekly Product Synthesis is modeled on Archon's daily investment briefing but adapted for the cadence and character of product cultivation.

## Briefing Structure

### S0: What Changed

*10-second scan — do I need to read further?*

- Initiative state transitions this week
- Frontier developments with product implications (from frontier-antenna)
- Emergence events detected (from emergence-detector)
- Feedback loop anomalies (from adaptation-observer)
- Significant decisions made (from decision-journal)

Format: bullet list, max 10 items. If nothing changed, say "Quiet week."

### S1: The System Now

*What can the intelligence system do today that it couldn't last week?*

- New capabilities surfaced or significantly improved
- Domain maturity changes
- Living capability snapshot (summarize capability-radar if available)

This section is the system's **self-portrait** — updated weekly.

### S2: What's Emerging

*The most important section. What surprised us?*

- Unexpected behaviors in surfaced products
- Cross-domain capability combinations nobody designed
- User behaviors that diverge from expectations
- Signals from germinating/emerging initiatives

**Tone here should be curious, not analytical.** "We noticed..." not "Data shows..."

### S3: Strategic Synthesis

*The Loom's own thinking about what the patterns mean.*

- Cross-product patterns (from pattern-weaver)
- Thesis validation/invalidation updates
- Active theme status (from product-narrative.md)
- Strategic questions to sit with this week

**Tone here should be opinionated.** Make claims. Ask hard questions. "This pattern suggests X. **But does it hold if Y changes?**"

### S4: Tensions & Risks

*Where is the system fighting itself?*

- Capability gaps blocking surfaced products
- Portfolio concentration (too many bets in one area?)
- Feedback loops showing unhealthy dynamics
- Burnout risk (the solo builder is a single point of failure)
- Stale initiatives that need composting decisions

**This section must be honest.** Not everything is going well. Name what isn't.

### S5: Next Moves

*What to do next week, framed as cultivation actions.*

Top 3 priorities. Each must be:
- **Specific** — Not "work on the product." Instead: "Run prototype-grower on initiative X using design + writing domains."
- **Framed as cultivation** — "Create conditions for..." not "Build feature..."
- **Connected to a signal** — Why this action now? What signal triggered it?

## Tone and Voice

The Weekly Product Synthesis should read like a **gardener's journal crossed with a strategist's notebook.**

- Reflective but decisive
- Honest about what's not working
- Curious about surprises
- Opinionated about strategy — make bold claims, then challenge them
- Concise — the full briefing should be readable in 5 minutes

**Good:** "Initiative X germinated faster than expected. The design × game-theory combination is producing experience patterns we haven't seen before. **Is this a genuine capability or are we seeing what we want to see?**"

**Bad:** "This week we continued to make progress on Initiative X. The team is working hard and we expect good results."

## Generation Process

1. **Collect inputs:**
   - `loom-briefings/initiative-log.md` — state changes
   - `loom-briefings/emergence-log.md` — new entries
   - `loom-briefings/product-narrative.md` — active themes
   - Latest adaptation-observer outputs (if any)
   - Latest pattern-weaver report (if any)
   - Latest frontier-antenna brief (if any)

2. **Read previous briefing** — for continuity and delta tracking

3. **Generate each section** in order S0 → S5

4. **Self-check:** Does the briefing say anything surprising? If every section is "business as usual," either the system truly didn't change (rare) or the briefing isn't looking hard enough.

5. **Save** to `loom-briefings/YYYY-MM-DD.md`

6. **Trigger narrative-keeper** — Does anything in this briefing warrant updating the product narrative?

## Connection to Archon's Model

| Archon (Daily Investment Briefing) | The Loom (Weekly Product Synthesis) |
|---|---|
| Signal Board | S0: What Changed |
| Regime & Macro | S1: The System Now |
| Sentiment & Positioning | S2: What's Emerging |
| Market Dashboard | — (no equivalent; products don't have tickers) |
| Risk & Scenarios | S4: Tensions & Risks |
| Portfolio Review | S3: Strategic Synthesis |
| Actionable Intelligence | S5: Next Moves |
