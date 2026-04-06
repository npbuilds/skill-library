# Scenario Planner — Quick Reference


## Quick Reference

| Category | Example Forces |
|----------|---------------|
| **AI capability** | Will reasoning improve faster than multimodal? Will context windows keep growing? |
| **Tool ecosystem** | Will MCP become standard? Will agent frameworks converge or fragment? |
| **Cost/access** | Will frontier models get cheaper? Will open-source close the gap? |
| **Regulation** | Will AI regulation constrain capabilities? Enable new markets? |
| **Usage patterns** | Will AI shift from chat to agentic? From individual to team-based? |

## Quick Reference

| Element | Description |
|---------|-------------|
| **Name** | A memorable label (not "Scenario 1" — something evocative) |
| **Narrative** | 2-3 sentences describing this world |
| **Key features** | What's true in this future that isn't true today? |
| **Library implications** | What skills become more/less valuable? What new domains emerge? |
| **Probability estimate** | Rough likelihood (these should sum to ~100% across the set) |

## Quick Reference

| Question | Assessment |
|----------|-----------|
| Does our current build plan still make sense? | [yes / partially / no] |
| Which planned skills become more valuable? | [list] |
| Which planned skills become less relevant? | [list] |
| What skills would we wish we'd built? | [list] |
| What skills would we regret building? | [list] |

## Step 5 — Classify Actions

| Action Type | Definition | Example |
|------------|-----------|---------|
| **Robust** | Works in 4+ of 5 scenarios | Building cross-domain connection skills (valuable regardless of AI direction) |
| **Contingent** | Works in 1-2 scenarios only | Building a domain that only matters if a specific AI capability materializes |
| **Hedging** | Costs little now, pays off big in one scenario | Adding a reference file that prepares a skill for a capability that might arrive |
| **No-regret** | Positive in all scenarios, even if magnitude varies | Improving clarity-engine (explanation is always valuable) |

## Quick Reference

| Scenario | Signpost | Source |
|----------|----------|--------|
| [Name] | [Observable indicator] | [Where to watch for it] |

## Formula / Pseudocode

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
