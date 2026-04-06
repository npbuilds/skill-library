---
name: counterfactual-reasoner
description: >
  Run "what if" analysis: construct counterfactual scenarios, assess causal claims, and
  explore possibility space. Use when the user needs to evaluate what would have happened
  under different choices, assess whether X actually caused Y, stress-test a plan by
  exploring alternative scenarios, or reason about possibility and necessity.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Write
---

# Counterfactual Reasoner — The Pathfinder

Explore the roads not taken. Counterfactual reasoning asks "what would have happened if...?" — the most powerful question for learning from decisions, assessing causation, and stress-testing plans. It's how we distinguish between "X happened and then Y happened" and "X *caused* Y."

## Input

From the decision-theory director or directly:
- The counterfactual question or causal claim to evaluate
- Context: what actually happened (the factual baseline)
- Mode: **causal** (did X cause Y?), **exploratory** (what if X had been different?), or **prospective** (what if we do X in the future?)

## Process

### Step 1 — Establish the Factual Baseline

Before reasoning about alternatives, pin down what actually happened:
- The key decision or event in question
- The actual outcome
- The circumstances (what else was true at the time)
- The timeline

### Step 2 — Construct the Counterfactual

Vary the minimal set of conditions needed to answer the question. Good counterfactual reasoning follows the **minimal departure** principle: change as little as possible from the actual world, then trace the consequences.

**Counterfactual construction rules:**

| Rule | Why | Example |
|------|-----|---------|
| **Change one thing at a time** | Isolates the causal contribution of each factor | "What if we'd launched a month earlier?" not "What if everything were different?" |
| **Keep background conditions stable** | The counterfactual world should be as similar to the actual world as possible | If asking "what if we'd hired differently," don't also assume the market was different |
| **Respect causal structure** | Changes propagate forward in time, not backward | If asking "what if it rained?", don't assume the rain also changes yesterday's weather |
| **Consider multiple paths** | The same cause can produce different outcomes through different mechanisms | "If we'd raised prices, customers might have left OR perceived higher quality" |

### Step 3 — Trace the Consequences

Follow the counterfactual change through its causal chain:

```
Counterfactual: [what changes]
  → Immediate effect: [first consequence]
    → Second-order effect: [consequence of the consequence]
      → Downstream effect: [further propagation]
    → Alternative second-order: [another path the consequence could take]
```

At each step, assess:
- **Probability**: How likely is this consequence? (near-certain / probable / possible / unlikely)
- **Sensitivity**: Does a small change in the counterfactual produce a large change in outcome? (indicates instability)
- **Convergence**: Do different paths from the counterfactual converge on the same outcome? (indicates robustness)

### Step 4 — Assess Causal Claims (for causal mode)

To evaluate "X caused Y," apply counterfactual tests:

**But-for test**: Would Y have happened even without X? If yes → X was not a necessary cause. If no → X was at least a necessary condition.

**INUS condition**: X may be an Insufficient but Necessary part of an Unnecessary but Sufficient condition. (The match caused the fire — but only given oxygen, fuel, and dryness. The match alone is insufficient; but within that set of conditions, it's necessary.)

**Causal strength assessment:**

| Finding | Causal Status | Confidence |
|---------|--------------|------------|
| Y would not have happened without X, and X reliably produces Y | X is a strong cause of Y | High |
| Y would not have happened without X, but X only sometimes produces Y | X is a contributing cause (necessary but not sufficient) | Moderate |
| Y might have happened anyway, but X made it more likely | X is a risk factor / probabilistic cause | Moderate |
| Y would have happened regardless of X | X is not a cause of Y (mere correlation or coincidence) | High |
| Cannot determine | Causal relationship is uncertain | Low — flag for further investigation |

**Common causal fallacies to check:**
- Post hoc ergo propter hoc (after X, therefore because of X)
- Confounding (Z causes both X and Y, creating false X→Y appearance)
- Reverse causation (Y actually causes X)
- Selection bias (we only see cases where both X and Y are present)

### Step 5 — Evaluate Robustness

How sensitive is the conclusion to the counterfactual construction?

- **Vary the counterfactual slightly**: Does the conclusion change with small adjustments?
- **Test multiple counterfactuals**: Do different "what if" questions converge on the same insight?
- **Check for butterfly effects**: Are there points where a tiny change cascades into radically different outcomes? (If so, causal claims should be held with less confidence)
- **Consider the closest possible world**: Among all the ways things could have been different, what's the most realistic alternative?

### Step 6 — Extract the Lesson

Counterfactual reasoning is most valuable when it produces an actionable insight:

- **For past decisions**: "Given what we know now, the decision was [good/bad] because [the counterfactual shows that alternatives would have been better/worse/similar]"
- **For causal claims**: "X [did/did not/partially] cause Y because [counterfactual test results]"
- **For future planning**: "If we want to avoid Y, the leverage point is [the factor whose counterfactual most changes the outcome]"

## Output

```
COUNTERFACTUAL ANALYSIS
───────────────────────
Mode: [causal / exploratory / prospective]
Question: [the counterfactual question]
Factual baseline: [what actually happened]

Counterfactual Scenario:
  Change: [what's different]
  Minimal departure: [confirmation that only necessary conditions were varied]

Consequence Trace:
  → [immediate effect] — Probability: [near-certain/probable/possible/unlikely]
    → [second-order effect] — Probability: [level]
      → [downstream effect] — Probability: [level]

Causal Assessment (if applicable):
  Claim: [X caused Y]
  But-for test: [would Y have happened without X?]
  Causal status: [strong cause / contributing cause / risk factor / not a cause / uncertain]
  Confounders considered: [potential confounding factors]

Robustness:
  Sensitivity: [how much does the conclusion change with small adjustments?]
  Convergence: [do multiple counterfactuals point the same way?]

Key Insight:
  [The single most important lesson from this counterfactual analysis]

Caveat: [Limitations — e.g., "Counterfactuals about complex systems carry inherent uncertainty"]
```

## Error Handling

**Counterfactual is too broad:** "What if the Industrial Revolution hadn't happened?" is unanswerable — too many variables change. Narrow to specific, testable counterfactuals. Suggest 2-3 more precise versions.

**Multiple causation:** Many outcomes have multiple causes. Don't force a single-cause explanation. Report the causal contribution of each factor and their interactions.

**Hindsight contamination:** When analyzing past decisions, bracket knowledge of the actual outcome. Evaluate the counterfactual based on what was knowable at the time. Flag if the user is engaging in outcome-biased reasoning (route to bias-detector).

**Unfalsifiable counterfactual:** Some counterfactuals can't be empirically tested. Acknowledge this limitation but note that reasoning about them can still be more or less disciplined. The goal is the best inference given available information.
