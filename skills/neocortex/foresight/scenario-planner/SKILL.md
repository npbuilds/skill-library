---
name: scenario-planner
description: >
  Model multiple plausible futures for the AI landscape and stress-test library strategy
  against them. Use when exploring what-if scenarios, preparing for capability shifts,
  evaluating whether a build plan is robust across different futures, or thinking about
  how AI developments could change what the library needs.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Glob Grep
---

# Scenario Planner — The Pathfinder

Maps multiple possible futures and tests which paths lead somewhere useful. Not predicting — *preparing*. The difference matters: prediction says "this will happen." Scenario planning says "here are 3-5 things that could happen — let's make sure our plan works in most of them."

Think of it like packing for a trip where you don't know the weather. You don't predict sun or rain — you pack for both and note which items work regardless.

## Core Function

Build structured scenarios for how the AI landscape and skill library could evolve, then evaluate strategies against those scenarios. Every scenario exercise produces:

1. **A scenario set** — 3-5 plausible, distinct futures (not just optimistic/pessimistic)
2. **Strategy stress-test** — How does the current plan perform in each scenario?
3. **Robust moves** — Actions that work well across most/all scenarios
4. **Contingent moves** — Actions that only make sense if a specific scenario materializes
5. **Signposts** — Observable indicators that tell you which scenario is actually unfolding

## Scenario Construction

### Step 1 — Identify Driving Forces

What are the major uncertainties that could shape the future?

| Category | Example Forces |
|----------|---------------|
| **AI capability** | Will reasoning improve faster than multimodal? Will context windows keep growing? |
| **Tool ecosystem** | Will MCP become standard? Will agent frameworks converge or fragment? |
| **Cost/access** | Will frontier models get cheaper? Will open-source close the gap? |
| **Regulation** | Will AI regulation constrain capabilities? Enable new markets? |
| **Usage patterns** | Will AI shift from chat to agentic? From individual to team-based? |

### Step 2 — Select Key Uncertainties

Pick the 2 most impactful, most uncertain forces. These become the axes of a 2×2 scenario matrix.

```
                    Force A: High
                        │
         Scenario 2     │     Scenario 1
         (High A,       │     (High A,
          Low B)        │      High B)
                        │
  Force B: Low ─────────┼───────── Force B: High
                        │
         Scenario 3     │     Scenario 4
         (Low A,        │     (Low A,
          Low B)        │      High B)
                        │
                    Force A: Low
```

### Step 3 — Build Each Scenario

For each quadrant, construct a narrative:

| Element | Description |
|---------|-------------|
| **Name** | A memorable label (not "Scenario 1" — something evocative) |
| **Narrative** | 2-3 sentences describing this world |
| **Key features** | What's true in this future that isn't true today? |
| **Library implications** | What skills become more/less valuable? What new domains emerge? |
| **Probability estimate** | Rough likelihood (these should sum to ~100% across the set) |

### Step 4 — Stress-Test Strategy

For each scenario, evaluate:

| Question | Assessment |
|----------|-----------|
| Does our current build plan still make sense? | [yes / partially / no] |
| Which planned skills become more valuable? | [list] |
| Which planned skills become less relevant? | [list] |
| What skills would we wish we'd built? | [list] |
| What skills would we regret building? | [list] |

### Step 5 — Classify Actions

| Action Type | Definition | Example |
|------------|-----------|---------|
| **Robust** | Works in 4+ of 5 scenarios | Building cross-domain connection skills (valuable regardless of AI direction) |
| **Contingent** | Works in 1-2 scenarios only | Building a domain that only matters if a specific AI capability materializes |
| **Hedging** | Costs little now, pays off big in one scenario | Adding a reference file that prepares a skill for a capability that might arrive |
| **No-regret** | Positive in all scenarios, even if magnitude varies | Improving clarity-engine (explanation is always valuable) |

### Step 6 — Identify Signposts

For each scenario, what observable signals would tell you it's the one actually unfolding?

| Scenario | Signpost | Source |
|----------|----------|--------|
| [Name] | [Observable indicator] | [Where to watch for it] |

## Scenario Archetypes

Common scenario shapes that recur in AI landscape planning:

### The Leap
One capability jumps dramatically (e.g., reasoning goes from "good" to "superhuman"). Everything that depends on that capability suddenly needs redesigning.
- **Library impact**: Skills that assumed limited capability need urgent upgrades
- **Robust response**: Build skills with adjustable capability assumptions

### The Plateau
A previously fast-improving capability levels off. What everyone assumed would keep getting better... doesn't.
- **Library impact**: Skills optimized for "future capability X" become over-designed
- **Robust response**: Don't build skills that require capabilities that don't exist yet

### The Convergence
Multiple capabilities improve simultaneously and interact in unexpected ways (e.g., reasoning + tool-use + long context = autonomous agents).
- **Library impact**: New skill categories emerge at the intersection
- **Robust response**: Build connective tissue between domains — convergence rewards integration

### The Fragmentation
The AI ecosystem splits (e.g., open vs. closed models diverge, regional regulations create different capability landscapes).
- **Library impact**: Skills may need to account for different capability tiers
- **Robust response**: Keep skills capability-agnostic where possible

## Output Format

```
SCENARIO PLANNING — [Topic]
Time Horizon: [6 months / 1 year / 2 years]
Key Uncertainties: [Force A] × [Force B]

Scenarios:

1. [Evocative Name] (probability: ~N%)
   Narrative: [2-3 sentences]
   Library Impact: [what changes for us]

2. [Evocative Name] (probability: ~N%)
   ...

3-5. ...

Strategy Assessment:
  Robust moves (work in most scenarios):
    - [action]
  Contingent moves (scenario-dependent):
    - [action] — only if [scenario name]
  No-regret moves:
    - [action]
  Signposts to watch:
    - [indicator] → suggests [scenario name]

Recommendation:
  [1-2 sentences: what should we do given this analysis?]
```

## What This Skill Does NOT Do

- **Predict** — Scenarios are plausible futures, not forecasts. Assigning probabilities is for calibration, not prophecy.
- **Decide** — Scenario-planner stress-tests strategies. Growth-architect decides what to build.
- **Evaluate current state** — That's frontier-scanner (for AI) and skill-cartographer (for the library). Scenario-planner takes their data and projects it forward.

## Cross-Domain Connections

- **Neocortex/foresight/frontier-scanner**: Frontier data is the primary input for scenario construction
- **Neocortex/architecture/growth-architect**: Scenario outputs directly inform build plan robustness
- **Neocortex/foresight/briefing-engine**: Scenarios are a key component of strategic briefings
- **Philosophy/decision-theory/decision-architect**: Shared toolkit — both work with uncertainty, options, and outcomes. Decision-architect handles individual decisions; scenario-planner handles strategic futures.
- **Philosophy/decision-theory/counterfactual-reasoner**: Complementary — counterfactual looks backward ("what if X hadn't happened"), scenario-planner looks forward ("what if X happens")
- **Investing/regime-intelligence**: Regime shifts in markets parallel paradigm shifts in AI — similar mental model, different domain
