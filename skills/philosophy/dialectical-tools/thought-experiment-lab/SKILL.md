---
name: thought-experiment-lab
description: >
  Construct, analyze, and systematically vary thought experiments to test intuitions and
  principles. Use when the user needs to test whether a principle holds under extreme
  conditions, explore the implications of a claim by constructing hypothetical scenarios,
  generate counterexamples, or use imaginative reasoning to clarify conceptual boundaries.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Write
---

# Thought Experiment Lab — The Alchemist

Transmute abstract principles into concrete scenarios. A thought experiment isolates a variable by constructing a world where everything else is controlled — it's the philosopher's equivalent of a controlled experiment, using imagination rather than equipment.

Read `references/classic-experiments.md` for a catalog of famous thought experiments organized by domain.

## Input

From the dialectical-tools director or directly:
- The principle, claim, or intuition to test
- Mode: **construct** (build a thought experiment for a given principle), **analyze** (examine an existing thought experiment), or **vary** (systematically modify a thought experiment to probe its boundaries)
- Domain context: which field's intuitions are we testing? (ethics, metaphysics, epistemology, political philosophy, science)

## Process

### Step 1 — Identify What's Being Tested

A good thought experiment isolates one variable. Identify:
- **The principle under test**: what claim or intuition is being examined?
- **The target variable**: what single factor is being manipulated?
- **The controlled variables**: what's held constant?
- **The intuition at stake**: what response does the thought experiment aim to elicit or challenge?

### Step 2 — Construct the Scenario (for construct mode)

**Design principles:**

| Principle | Why | Example |
|-----------|-----|---------|
| **Minimize moving parts** | Each added variable dilutes the test | Trolley problem: 1 track, 1 lever, 5 vs. 1 person |
| **Make it vivid** | Abstract scenarios don't pump intuitions | "Imagine you're standing at the switch" not "Consider a scenario where..." |
| **Eliminate escape routes** | Foreclose options that avoid the dilemma | "You cannot warn anyone" / "There is no third option" |
| **Make consequences certain** | Remove probability hedges | "The 5 will definitely die" not "might die" |
| **Stipulate knowledge** | Remove epistemic uncertainty | "You know for certain that..." |

**Construction template:**
1. Set the scene (minimal but vivid)
2. Present the choice (clear, binary or few options)
3. Stipulate what's known (remove uncertainty)
4. Close escape routes (no cleverness allowed)
5. Ask the question (what should you do? / what's the right answer? / does the principle still hold?)

### Step 3 — Analyze the Experiment (for analyze mode)

For an existing thought experiment, evaluate:

- **What's it testing?** What principle or intuition is under examination?
- **Is it well-constructed?** Does it isolate the target variable, or do confounds leak in?
- **What intuition does it pump?** What do most people feel, and why?
- **What does the intuition reveal?** Does the intuition support or undermine the principle?
- **Are there disanalogies?** Does the thought experiment differ from real cases in ways that matter?

**Common flaws in thought experiments:**
- Scenario is too unrealistic to pump reliable intuitions
- Hidden variables confound the test (the trolley problem adds "action vs. inaction" to "5 vs. 1")
- Escape routes exist that the experimenter didn't notice
- The intuition pumped may reflect bias rather than moral truth

### Step 4 — Vary Systematically (for vary mode)

Take an existing thought experiment and modify one variable at a time to probe boundaries:

**Variation dimensions:**
- **Numbers**: What if it's 5 vs. 2? 100 vs. 1? 1,000,000 vs. 1?
- **Relationship**: What if one person is your child? A stranger? An enemy?
- **Agency**: What if you act vs. fail to act? Push a button vs. push a person?
- **Knowledge**: What if you're uncertain about the consequences?
- **Reversibility**: What if the harm is temporary vs. permanent?
- **Consent**: What if the affected parties consented vs. didn't?

For each variation, note:
- Does your intuition change? At what point?
- Does the principle under test still hold?
- What does the shift (or stability) reveal about the underlying moral/conceptual structure?

### Step 5 — Extract the Insight

What did the thought experiment reveal?

- **The principle holds**: Even under extreme conditions, the principle produces the intuitively correct result. This is evidence for the principle.
- **The principle breaks**: Under these specific conditions, the principle produces an intuitively unacceptable result. This is a counterexample.
- **Intuitions conflict**: The thought experiment reveals a tension between two intuitions we hold simultaneously. This is the most valuable outcome — it maps the conceptual boundary.

## Output

```
THOUGHT EXPERIMENT
──────────────────
Mode: [construct / analyze / vary]
Principle tested: [the claim or intuition under examination]

Scenario:
  [The thought experiment — vivid, minimal, with escape routes closed]

Question: [what the experiment asks]

Analysis:
  Target variable: [what's being manipulated]
  Controlled variables: [what's held constant]
  Intuition pumped: [what most people feel and why]

Result:
  [The principle holds / breaks / reveals tension]
  Insight: [what we learn from this]

Variations (if vary mode):
  Variation 1: [change] → Intuition: [shifts/holds] → Reveals: [what]
  Variation 2: [change] → Intuition: [shifts/holds] → Reveals: [what]
  ...
  Boundary found: [the point where the intuition flips — this is the conceptual boundary]
```

## Error Handling

**Intuitions vary across people:** This is data, not a problem. Report the variation and what it reveals about different underlying value commitments.

**Scenario is too unrealistic:** Some unrealism is the point — thought experiments isolate variables by removing real-world complexity. But if the unrealism itself distorts intuitions (e.g., requiring impossible physics that changes the moral structure), note this as a limitation.

**User finds the thought experiment disturbing:** Some thought experiments (especially in ethics) are designed to be uncomfortable — that's how they reveal what we really value. But handle with care. Frame as intellectual exploration, not endorsement.
