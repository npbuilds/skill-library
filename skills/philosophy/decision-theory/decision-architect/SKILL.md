---
name: decision-architect
description: >
  Structure a decision under uncertainty: enumerate options, model outcomes, assign
  probabilities, clarify values, and recommend a decision framework. Use when the user
  faces a complex choice with multiple options, uncertain outcomes, or unclear trade-offs
  and needs the decision laid out clearly before choosing.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Write
---

# Decision Architect — The Cartographer

Map the decision landscape before the user walks into it. Most bad decisions aren't caused by picking the wrong option — they're caused by not seeing the options clearly, not understanding the trade-offs, or not knowing what you actually value. The architect makes the invisible structure of a decision visible.

## Input

From the decision-theory director or directly:
- The decision to structure (what needs to be decided)
- Context: timeline, constraints, who's affected, reversibility
- Known options (if any — the architect may find more)
- The user's stated objectives (what they're trying to achieve)

## Process

### Step 1 — Frame the Decision

Before structuring, ensure the right question is being asked:

- **Scope**: What exactly is being decided? (Not "what should I do with my career" but "should I take offer A or stay at current job?")
- **Decision-maker**: Who has the authority to decide?
- **Timeline**: When must a decision be made? Is delay an option?
- **Reversibility**: Can this be undone? At what cost?
- **Dependencies**: Does this decision depend on or affect other decisions?

A well-framed decision is half-solved. Many "impossible" decisions become clear once framed precisely.

### Step 2 — Enumerate Options

List all available options, including:

- **The obvious options**: what the user is already considering
- **The null option**: what happens if they do nothing / maintain status quo
- **The creative options**: novel alternatives not yet considered (combine elements, sequence decisions, find a third way)
- **The delay option**: is "decide later with more information" viable?

For each option, note:
- What it commits to and what it preserves
- Whether it's reversible
- What information it reveals (some options are informative even if suboptimal)

### Step 3 — Model Outcomes

For each option, identify the plausible outcomes:

```
Option A:
  Outcome A1 (best case):  [description] — Probability: [estimate]
  Outcome A2 (base case):  [description] — Probability: [estimate]
  Outcome A3 (worst case): [description] — Probability: [estimate]
```

**Probability estimation principles:**
- Use reference classes when available (what happened in similar situations?)
- Distinguish uncertainty (unknown probabilities) from risk (known probabilities)
- Acknowledge when you're estimating vs. when you have data
- Watch for anchoring — the first number you think of is often wrong

**Outcome assessment principles:**
- Consider second-order effects, not just immediate results
- Consider who is affected besides the decision-maker
- Consider both tangible and intangible outcomes
- Consider the outcome of the option *conditional on the world state*, not in isolation

### Step 4 — Clarify Values

What does the decision-maker actually value? Often this is the hardest and most illuminating step.

**Elicit value dimensions:**
- What are you optimizing for? (return, safety, growth, freedom, relationships, time)
- What's your risk tolerance? (risk-averse, risk-neutral, risk-seeking)
- What would you regret most? (minimizing maximum regret is often more intuitive than maximizing expected value)
- What's non-negotiable? (constraints that eliminate options regardless of payoff)

**Common value conflicts in decisions:**
- Security vs. opportunity
- Short-term vs. long-term
- Personal vs. collective benefit
- Financial vs. non-financial value
- Known-good vs. unknown-possibly-better

If values are unclear, route to `ethics/values-excavator` for deeper excavation.

### Step 5 — Select Decision Framework

Match the decision to the appropriate analytical framework:

| Situation | Framework | How It Works |
|-----------|-----------|-------------|
| Probabilities estimable, outcomes quantifiable | **Expected Value** | Probability × payoff for each outcome; choose highest EV |
| Outcomes quantifiable but probabilities unknown | **Minimax Regret** | For each option, calculate worst-case regret; minimize the maximum regret |
| High uncertainty, catastrophic downside possible | **Maximin** | Choose the option whose worst-case outcome is least bad |
| Decision is sequential / information will arrive | **Decision Tree / Real Options** | Map the decision sequence; value the option to learn and adapt |
| Multiple competing objectives | **Multi-Criteria Decision Analysis** | Score each option against each criterion; weight criteria by importance |
| Risk of ruin / non-ergodic situation | **Kelly Criterion / Ruin Avoidance** | Never bet enough to face ruin, even if EV is positive |

Read `references/decision-frameworks.md` for detailed framework descriptions.

### Step 6 — Sensitivity Analysis

Test how robust the recommendation is:

- **What would change the answer?** Identify the assumption whose falsity would flip the decision
- **How sensitive to probabilities?** If the key probability shifted by 20%, would the choice change?
- **How sensitive to values?** If the user valued X slightly more than Y, would the choice change?
- **What information would be most valuable?** What could the user learn that would most change the analysis?

A robust decision survives sensitivity analysis. A fragile one depends on precise estimates — flag this.

## Output

```
DECISION ARCHITECTURE
─────────────────────
Decision: [precisely framed question]
Decision-maker: [who] | Timeline: [when] | Reversibility: [high/medium/low]

Options:
  A. [option] — Reversible: [yes/no] | Commits to: [what]
  B. [option] — Reversible: [yes/no] | Commits to: [what]
  C. [null option / status quo]
  D. [creative option, if found]

Outcome Model:
  Option A: [best/base/worst case with probabilities]
  Option B: [best/base/worst case with probabilities]
  ...

Value Dimensions:
  Primary: [what matters most]
  Secondary: [what also matters]
  Constraints: [non-negotiables]
  Key trade-off: [the central tension]

Recommended Framework: [name] — Because: [why this framework fits]

Analysis:
  [Framework-specific analysis — EV calculation, regret matrix, decision tree, etc.]

Sensitivity:
  The answer changes if: [key assumption]
  Most valuable information: [what to learn before deciding]

Decision Map:
  If you value [X] most → [option]
  If you value [Y] most → [option]
  If uncertainty is the main concern → [option]
```

## Error Handling

**Decision is trivial:** If analysis reveals one option dominates on all dimensions, say so. Not every decision needs a framework — sometimes the answer is obvious once structured.

**Too many options to analyze:** Group into categories, eliminate dominated options first (any option that's worse than another on all dimensions), then analyze the remaining contenders.

**User can't articulate values:** Use comparison-based elicitation. "Would you prefer guaranteed $50K or a 50% chance of $120K?" reveals risk preferences. "If you had to sacrifice X or Y, which goes?" reveals value ranking.

**Decision involves other agents' responses:** Flag that this is a strategic interaction and may benefit from game-theoretic analysis (cross-domain to game-theory). Decision theory handles individual choice; game theory handles interactive choice.
