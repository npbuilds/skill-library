---
name: historical-analogy-engine
description: >
  Build structured historical analogy analyses for current geopolitical situations. Use when
  the user presents a current event and wants the 3-5 most instructive historical parallels,
  with explicit evaluation of where each analogy holds, where it breaks, and what the
  comparison reveals that studying either case alone would miss.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read
---

# Historical Analogy Engine — Structured Comparison with Built-In Limits

This is an action skill: given a current situation, it produces a structured analysis identifying the most instructive historical parallels, evaluating each analogy's strengths and weaknesses, and synthesizing lessons that survive scrutiny. The engine is designed to prevent the most common abuse of historical analogy — cherry-picking a single parallel and treating it as predictive.

The engine draws on `historical-pattern-recognition` for known recurring dynamics and on the thematic wings for specific case knowledge. It bridges to `applied-history` as the primary output mechanism for historical reasoning about the present.

## When This Applies

- User presents a current event and asks "what's the historical parallel?"
- User asks "is this like [specific historical event]?"
- User wants to test a pundit's historical analogy
- User needs historical context for a strategic, investment, or policy decision

## Input Requirements

The engine needs:
1. **The current situation** — described with enough specificity to compare (not just "tensions in Asia" but "rising power challenging established hegemon in maritime domain")
2. **The domain** — geopolitical, economic, social, technological, or military
3. **The user's purpose** — understanding, decision-making, writing, or debate

## The Five-Step Process

### Step 1 — Decompose the Current Situation

Break the situation into structural components:
- **Actors**: Who are the key players? What are their interests and constraints?
- **Structure**: What is the power distribution? What institutions exist?
- **Dynamics**: What trends are accelerating or decelerating?
- **Triggers**: What proximate events are driving urgency?
- **Stakes**: What outcomes are possible? What is at risk?

### Step 2 — Generate Candidate Analogies (3-5)

Search across the historical record for cases with structural similarity. Prioritize:
- **Structural match**: Similar actor configurations, power distributions, and institutional contexts
- **Dynamic match**: Similar trends and trajectory
- **Diversity**: Include analogies from different eras and regions to avoid confirmation bias
- **At least one contrarian**: Include a case that looks similar on the surface but had a radically different outcome

Do NOT start with the "obvious" analogy. The most cited parallel is often the most misleading (Munich is invoked far more often than it applies).

### Step 3 — Evaluate Each Analogy

For each candidate, produce:

```
ANALOGY: [Historical case]
PERIOD: [When]
STRUCTURAL SIMILARITIES:
  - [Specific parallel 1]
  - [Specific parallel 2]
  - [Specific parallel 3]
STRUCTURAL DIFFERENCES:
  - [Where the analogy breaks 1]
  - [Where the analogy breaks 2]
  - [Where the analogy breaks 3]
OUTCOME: [What happened in the historical case]
LOAD-BEARING CAPACITY: [HIGH / MEDIUM / LOW]
  — How much analytical weight can this analogy support?
KEY LESSON: [The one thing this comparison reveals]
KEY LIMIT: [The one thing this comparison obscures]
```

### Step 4 — Synthesize Across Analogies

Compare what the analogies collectively suggest:
- **Convergence**: Where do multiple analogies point in the same direction?
- **Divergence**: Where do they disagree? What explains the difference?
- **Novel features**: What aspects of the current situation have NO good historical parallel?
- **Confidence assessment**: Given the quality and convergence of analogies, how confident can we be in pattern-based reasoning here?

### Step 5 — Deliver with Limits

Present the analysis with explicit limits:
- Name the strongest analogy and explain why
- Name the most dangerous misapplication and explain why
- State what historical reasoning CAN illuminate about this situation
- State what it CANNOT predict
- Recommend what additional (non-historical) analysis is needed

## Anti-Patterns to Avoid

| Anti-Pattern | Why It's Dangerous | The Fix |
|---|---|---|
| **Single-analogy reasoning** | One parallel becomes a straitjacket | Always generate 3-5 candidates |
| **Similarity bias** | Focusing on matches, ignoring differences | The DIFFERENCES section is mandatory and equal in length to SIMILARITIES |
| **Outcome anchoring** | Assuming the historical outcome will repeat | State the outcome but assess structural differences that might produce a different result |
| **Munich syndrome** | Every threat becomes "appeasement" | Include counter-examples where restraint was correct |
| **Presentism** | Projecting current values onto past actors | Flag anachronistic framing explicitly |

## Output Format

The engine produces a structured document:

1. **Situation Summary** (2-3 sentences)
2. **Analogy Table** (3-5 analogies with the evaluation template above)
3. **Synthesis** (convergence, divergence, novel features)
4. **Confidence Assessment** (high/medium/low with explanation)
5. **Recommended Next Steps** (what additional analysis is needed beyond historical reasoning)
