---
name: steel-man-forge
description: >
  Construct the strongest possible version of an opposing argument. Use when the user wants
  to understand the best case for a position they disagree with, stress-test their own
  position by seeing the strongest opposition, practice intellectual humility, or prepare
  for a debate by anticipating the best counterarguments.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Write
---

# Steel-Man Forge — The Armorer

Build the strongest version of the argument you'd least like to face. If a straw man is the weakest caricature of an opposing view, a steel man is its most formidable form — the version that would be hardest to defeat even if you disagree with it.

Steel-manning is the opposite of motivated reasoning. It requires genuine cognitive empathy — understanding not just what the other side claims but *why a reasonable, informed person might believe it*.

## Input

From the dialectical-tools director or directly:
- The position to steel-man (the one the user wants to see the strongest version of)
- The user's own position (optional — helps identify which steel man is most challenging to them specifically)
- Context: why are they asking? (debate prep, intellectual exercise, genuine uncertainty, testing their own view)
- Scope: **focused** (steel-man a specific claim) or **comprehensive** (steel-man an entire worldview or position)

## Process

### Step 1 — Understand the Position Charitably

Before strengthening, ensure the position is fairly understood. Common failure modes:

- **Weakest-advocate fallacy**: taking the dumbest proponent as representative. Steel-manning uses the *best* advocates.
- **Motte-and-bailey confusion**: confusing the defensible core (motte) with the ambitious overreach (bailey). Steel-man the ambitious version, not just the safe retreat.
- **Historical caricature**: attacking a position as it was understood 50 years ago, not as its best current advocates present it.

Restate the position in terms its strongest advocates would recognize and endorse.

### Step 2 — Identify the Core Insight

Every position that has attracted thoughtful adherents contains at least one genuine insight — a truth, concern, or observation that gives it force. Find it.

Ask:
- What real phenomenon does this position respond to?
- What legitimate concern motivates it?
- What would a thoughtful, well-informed advocate say is the strongest single reason to hold this view?
- What do critics of this position tend to miss or dismiss too quickly?

The core insight is the seed from which the steel man grows.

### Step 3 — Strengthen the Premises

Take each premise of the position and make it as strong as possible:

| Strengthening Move | How | Example |
|-------------------|-----|---------|
| **Replace weak evidence with strong** | Swap anecdotes for data, opinions for studies, correlation for mechanism | "Some people say X" → "Meta-analyses show X with effect size Y" |
| **Narrow overly broad claims** | Restrict to the domain where the claim is strongest | "X is always true" → "X holds in conditions A, B, and C" |
| **Add missing qualifications** | Supply the caveats a careful advocate would include | "X causes Y" → "X is one significant contributing factor to Y, alongside Z" |
| **Ground in established theory** | Connect to well-regarded frameworks | "This seems right" → "This follows from [established principle]" |
| **Address known objections** | Build in responses to the strongest counterarguments | Preemptively handle the top 2-3 objections |

### Step 4 — Strengthen the Argument Structure

Beyond better premises, improve the logical architecture:

- **Choose the strongest argument form** — If the position can be argued deductively, inductively, or abductively, pick the form where it's most compelling
- **Eliminate unnecessary claims** — Strip anything that weakens the overall case. A steel man is lean.
- **Arrange for maximum force** — Lead with the most compelling evidence; build to the strongest point
- **Handle the hardest case** — A steel man that only works for easy cases is bronze at best. Show it handles the difficult cases too.

### Step 5 — The Empathy Test

Check the steel man against this standard: *Would a thoughtful, informed advocate of this position read this steel man and say "Yes, that's my view, and that's actually better than how I usually put it"?*

If not, you've built a sophisticated straw man — it looks strong but doesn't represent what real advocates actually believe. Revise.

### Step 6 — Identify What Would Have to Be True

For the steel man to succeed, certain things would have to be true. List them explicitly:

- Empirical claims that need to hold
- Value premises that need to be accepted
- Causal mechanisms that need to work
- Scope conditions that need to apply

This gives the user a clear map: "If you want to defeat this steel man, here's what you need to challenge."

### Step 7 — Note Genuine Remaining Weaknesses

Even the strongest version of a position has vulnerabilities. A good steel man acknowledges them — this builds credibility and helps the user see the real debate terrain:

- **The strongest counterargument** the steel man doesn't fully answer
- **The empirical question** whose answer would most change the calculus
- **The value tension** that honest advocates of this position wrestle with

## Output

```
STEEL MAN
─────────
Position forged: [the position in its strongest form]

Core Insight: [the genuine truth or concern that gives this position force]

The Steel-Man Argument:
  P1: [strongest version of first premise] — Support: [evidence/reasoning]
  P2: [strongest version of second premise] — Support: [evidence/reasoning]
  ...
  C:  [conclusion, precisely stated]

  [2-3 paragraph narrative version presenting the argument at full force —
   written as a thoughtful advocate would actually argue it]

What Must Be True: [list of conditions for this argument to succeed]

Preemptive Responses to Top Objections:
  Objection 1: [strongest counterargument]
    Steel-man response: [how the strongest advocate would answer]
  Objection 2: [second strongest counterargument]
    Steel-man response: [how they'd answer]

Genuine Remaining Vulnerabilities:
  1. [the point where even the strongest version is weakest]
  2. [the empirical question that could change everything]

Empathy Check: [Would a thoughtful advocate endorse this as a fair, strong representation? Why/why not]
```

**For companion mode** (steel-manning against another skill's analysis):

```
STEEL MAN CHALLENGE
───────────────────
Analysis challenged: [brief description of the primary analysis]
Opposition forged: [the strongest argument against the analysis's conclusion]

[Structured steel man as above, targeted specifically at the primary analysis]

Where the original analysis is most vulnerable to this steel man: [specific point]
Where the original analysis withstands this steel man: [specific point]
```

## Error Handling

**Position is genuinely indefensible:** Extremely rare — even flat-earth arguments have a steelmannable kernel (distrust of institutions, the value of firsthand observation). Find the legitimate concern underneath the wrong conclusion. Steel-man the concern, not the specific claim.

**User wants validation of their own view, not a real steel man:** Build the real steel man anyway. A weak steel man serves no one — it gives false confidence. If the user's position is genuinely stronger, the steel man will make that more visible, not less.

**The steel man is actually more convincing than the user's position:** This happens, and it's the most valuable possible outcome. Present it honestly. The user asked for the strongest opposition — if it turns out to be stronger than expected, that's critical information.

**Position requires domain expertise the user doesn't have:** Build the steel man at the user's level of technical sophistication. A steel man that relies on jargon the user can't evaluate isn't useful — it's just obscurantism.
