---
name: bias-detector
description: >
  Identify cognitive biases distorting a decision, judgment, or argument. Use when the user
  suspects their thinking may be biased, wants to check a decision for common reasoning
  errors, needs to understand why a group made an irrational choice, or wants to debias
  a specific judgment before acting on it.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Write
---

# Bias Detector — The Mirror

Hold up a mirror to thinking and show the distortions. Cognitive biases are not character flaws — they're predictable patterns in how human cognition processes information under time pressure, complexity, and uncertainty. Identifying them is the first step to correcting for them.

Read `references/bias-catalog.md` for the complete catalog with examples and debiasing strategies.

## Input

From the decision-theory director or directly:
- The decision, judgment, or reasoning to scan for biases
- Context: what was the situation? What information was available? What was the time pressure?
- Mode: **comprehensive** (scan for all major biases) or **targeted** (check for a specific suspected bias)

## Process

### Step 1 — Understand the Reasoning

Before scanning for biases, understand the reasoning being evaluated:
- What conclusion was reached (or is being reached)?
- What information was considered?
- What information was available but not considered?
- What was the process? (Deliberate analysis, gut feeling, group discussion, etc.)

### Step 2 — Scan by Bias Category

Check each category systematically. Within each, focus on the biases most relevant to the specific situation.

#### Information Processing Biases
*How we select, interpret, and weight information*

| Bias | Pattern | Diagnostic Question |
|------|---------|-------------------|
| **Confirmation bias** | Seeking/favoring information that confirms existing beliefs | Was disconfirming evidence actively sought? |
| **Anchoring** | Over-relying on the first piece of information encountered | Would a different starting point yield a different estimate? |
| **Availability heuristic** | Judging probability by how easily examples come to mind | Are vivid/recent examples distorting frequency estimates? |
| **Framing effect** | Responding differently to the same information based on presentation | Would the conclusion change if the same facts were framed differently? |
| **Base rate neglect** | Ignoring population-level statistics in favor of specific cases | What's the base rate? Has it been considered? |
| **Survivorship bias** | Drawing conclusions only from visible successes | What about the cases that failed/disappeared? |

#### Decision-Making Biases
*How we evaluate options and make choices*

| Bias | Pattern | Diagnostic Question |
|------|---------|-------------------|
| **Sunk cost fallacy** | Continuing because of past investment rather than future value | If starting fresh today, would you make the same choice? |
| **Status quo bias** | Preferring the current state disproportionately | Is inaction being held to a lower standard than action? |
| **Loss aversion** | Weighting losses ~2x more than equivalent gains | Are potential losses being overweighted relative to potential gains? |
| **Endowment effect** | Overvaluing what you already have | Would you acquire this at the price you'd need to sell it? |
| **Present bias** | Overweighting immediate outcomes vs. future ones | How would this look from a year / five years out? |
| **Omission bias** | Preferring harm from inaction over equal harm from action | Is doing nothing really less harmful, or does it just feel that way? |

#### Social Biases
*How others' behavior and opinions affect our thinking*

| Bias | Pattern | Diagnostic Question |
|------|---------|-------------------|
| **Groupthink** | Conformity pressure suppressing dissent | Was there a genuine devil's advocate? Were dissenting views penalized? |
| **Authority bias** | Deferring to authority regardless of their domain expertise | Is the authority actually an expert in *this specific area*? |
| **Bandwagon effect** | Believing something because many others do | Would you hold this view if no one else did? |
| **In-group bias** | Favoring ideas/people from one's own group | Would this idea be evaluated differently if it came from an outsider? |

#### Retrospective Biases
*How we evaluate past decisions and events*

| Bias | Pattern | Diagnostic Question |
|------|---------|-------------------|
| **Hindsight bias** | "I knew it all along" after learning the outcome | What was actually knowable at the time of the decision? |
| **Outcome bias** | Judging decisions by results rather than process | Was this a good process that got unlucky, or a bad process that got lucky? |
| **Attribution error** | Attributing others' behavior to character, own to circumstances | Would you explain your own similar behavior the same way? |
| **Narrative fallacy** | Constructing a coherent story that oversimplifies causal chains | Is this narrative capturing the actual complexity, or smoothing it? |

### Step 3 — Assess Impact

For each bias detected, assess:

| Dimension | Assessment |
|-----------|-----------|
| **Confidence** | How confident are you this bias is operating? [high/medium/low] |
| **Direction** | Which way is it pushing? [toward option X / away from option Y / inflating estimate / etc.] |
| **Magnitude** | How much is it distorting the judgment? [large/moderate/small] |
| **Correctable** | Can the user adjust for it? [yes, by doing X / partially / difficult to correct] |

### Step 4 — Suggest Debiasing Strategies

For each significant bias, recommend a specific debiasing technique:

| Strategy | Works For | How |
|----------|----------|-----|
| **Consider the opposite** | Confirmation bias, anchoring | Deliberately construct the case against your current view |
| **Reference class forecasting** | Planning fallacy, base rate neglect | Find similar past cases; use their distribution as your baseline |
| **Pre-mortem** | Overconfidence, planning fallacy | Imagine the decision failed; explain why |
| **Red team** | Groupthink, confirmation bias | Assign someone to argue against the consensus |
| **Cooling period** | Present bias, emotional reasoning | Delay the decision by a set time; revisit with fresh eyes |
| **Outside view** | Anchoring, narrative fallacy | Ask: what would a neutral advisor say about this situation? |
| **Kill criteria** | Sunk cost, status quo bias | Pre-commit to conditions under which you'll abandon the path |

### Step 5 — Distinguish Bias from Legitimate Reasoning

Not every heuristic is a bias. Flag potential false positives:

- **Gut feeling based on expertise**: An experienced firefighter's "something's wrong" is pattern recognition, not a bias. Domain expertise produces valid intuitions.
- **Reasonable risk aversion**: Loss aversion in high-stakes irreversible situations may be rational, not biased.
- **Prior beliefs based on evidence**: Updating slowly on weak evidence isn't confirmation bias — it's appropriate Bayesian reasoning.
- **Social information**: Following expert consensus isn't authority bias if the experts are genuinely qualified in the relevant domain.

The test: Can the reasoning be justified on its own merits, independent of the psychological mechanism that produced it?

## Output

```
BIAS SCAN
─────────
Subject: [the decision/judgment/reasoning analyzed]
Context: [situation, information available, time pressure]

Biases Detected:

  1. [Bias name] — Category: [information/decision/social/retrospective]
     Evidence: [specific feature of the reasoning that suggests this bias]
     Confidence: [high/medium/low]
     Direction: [how it's distorting the judgment]
     Magnitude: [large/moderate/small]
     Debiasing: [specific recommended strategy]

  2. [Bias name] — Category: [category]
     ...

False Positive Check:
  [Any heuristics that look like biases but may be legitimate reasoning]

Most Critical Bias: [the one distorting the judgment most]

Debiased Perspective:
  [What the judgment/decision looks like after accounting for detected biases]

Caveat: [Limitations — e.g., "This scan was based on the information provided; biases in the information itself may not be detectable"]
```

## Error Handling

**Everything looks biased:** Step back. If every reasoning pattern triggers a bias label, the scan is too sensitive. Focus on biases with high confidence and large magnitude. Some apparent biases are just good heuristics.

**No biases detected:** Possible but uncommon for complex decisions. Report honestly, but note that some biases (especially confirmation bias) are hard to detect from the inside. Suggest the user seek an external perspective.

**User is defensive about biases:** Normalize: "Everyone has these biases — they're features of human cognition, not personal failings. The goal is awareness, not judgment." Focus on the debiasing strategies, not the diagnosis.

**Retrospective analysis (was the past decision biased?):** Apply hindsight-bias correction first. Evaluate the reasoning based on what was knowable at the time, not on what's known now. A decision can be unbiased and still produce a bad outcome.
