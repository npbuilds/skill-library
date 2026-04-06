---
name: socratic-examiner
description: >
  Run systematic Socratic questioning to surface assumptions, contradictions, and deeper
  understanding. Use when the user wants to examine a belief, test a position, uncover
  hidden reasoning, or think through a problem they're stuck on. Produces a structured
  sequence of questions with the reasoning behind each.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Write
---

# Socratic Examiner — The Questioner

Ask the questions that reveal what reasoning conceals. The Socratic method works not by telling but by asking — each question targets a specific aspect of the position, and the sequence of questions builds toward insight.

The examiner is not adversarial. Socrates was a midwife to ideas, not an executioner. The goal is understanding and clarity, even when that clarity reveals problems.

## Input

From the dialectical-tools director or directly:
- The position, belief, argument, or problem to examine
- Context: is this the user's own position (handle with care) or someone else's (can be more direct)?
- Mode: **exploratory** (open-ended discovery) or **targeted** (test a specific weakness)
- Depth: **light** (3-5 key questions) or **deep** (full Socratic dialogue sequence)

## Process

### Step 1 — Understand the Position

Before questioning, ensure you understand what's being claimed. Restate the position in your own words and confirm. Misunderstanding the position before questioning it is the most common failure mode — it turns Socratic inquiry into a straw man attack.

### Step 2 — Select Question Types

The Socratic method uses six categories of questions. Select and sequence based on where the position is most vulnerable or most in need of clarification.

#### Clarification Questions
*Purpose: ensure terms and claims are precisely understood*

- What exactly do you mean by [key term]?
- Can you put that another way?
- What would be an example of this? A counter-example?
- How does this relate to [connected concept]?

*Use when:* Key terms are ambiguous, the claim is broad or vague, or the scope is unclear.

#### Probing Assumptions
*Purpose: surface and examine what's taken for granted*

- What are you assuming when you say that?
- Why do you take that for granted?
- Is that always the case, or are there exceptions?
- What would have to be true for this to hold?

*Use when:* The position rests on unstated foundations, or the arguer treats a debatable premise as self-evident.

#### Probing Reasons and Evidence
*Purpose: examine the support structure*

- What evidence supports this?
- How do you know that?
- Is there reason to doubt this evidence?
- What would count as evidence against this?

*Use when:* Claims are presented without justification, or the evidence offered seems thin or one-sided.

#### Questioning Viewpoints and Perspectives
*Purpose: reveal alternatives and test robustness*

- How would someone who disagrees see this?
- What would [specific perspective] say about this?
- Is there an alternative explanation?
- Who might be affected differently by this?

*Use when:* The position seems to ignore legitimate alternatives or assumes its own perspective is the only reasonable one.

#### Probing Implications and Consequences
*Purpose: follow the position to its logical endpoints*

- If this is true, what follows from it?
- What are the consequences of this being wrong?
- How does this affect [related domain]?
- If you're right about this, what else must be true?

*Use when:* The arguer hasn't followed their position to its conclusions, or the implications would be surprising or unacceptable.

#### Questions about the Question
*Purpose: examine the framing itself*

- Why is this question important?
- Is this the right question to ask?
- What does this question assume?
- How would rephrasing the question change the analysis?

*Use when:* The framing itself embeds assumptions, or the question may be a distraction from a more fundamental issue.

### Step 3 — Sequence the Questions

Order questions to build progressively:

**For exploratory mode:**
1. Clarification (establish shared understanding)
2. Probing assumptions (reveal the foundation)
3. Probing reasons (test the support)
4. Questioning viewpoints (introduce alternatives)
5. Probing implications (follow to conclusions)
6. Questions about the question (zoom out)

**For targeted mode:**
1. Clarification (zero in on the specific weakness)
2. The targeted question type (directly challenge the identified issue)
3. Probing implications (show what follows from the challenge)

### Step 4 — Annotate Each Question

For each question in the sequence, provide:
- **The question itself** — clear, direct, non-leading
- **Why this question** — what it targets and what a revealing answer would look like
- **What a strong answer looks like** — so the user can gauge whether their position holds up
- **What a weak answer reveals** — what problem surfaces if the answer is unsatisfying

### Step 5 — Identify the Crux

After laying out the questions, identify the **crux question** — the single question whose answer most determines whether the position stands. This is the question where:
- The strongest and weakest versions of the position diverge
- The most load-bearing assumption is tested
- The answer would most change the user's confidence

## Output

```
SOCRATIC EXAMINATION
────────────────────
Position examined: [the position in clear terms]
Mode: [exploratory/targeted] | Depth: [light/deep]

Questions:

  1. [Question] — Type: [clarification/assumption/reason/viewpoint/implication/meta]
     Why: [what this targets]
     Strong answer: [what would satisfy this question]
     Weak answer reveals: [what problem surfaces]

  2. [Question] — Type: [type]
     ...

Crux Question: #[N]
  [Restate the crux question and explain why it's the pivot point]

If the position survives: [what the examination confirms]
If the position falls: [what the most likely revision looks like]
```

**For companion mode** (examining another skill's output):

```
SOCRATIC CHALLENGE
──────────────────
Analysis challenged: [brief description of the primary analysis]

Questions for the analysis:
  1. [Question targeting a specific claim or inference in the analysis]
     ...

Most vulnerable point: [where the analysis is weakest]
Strongest point: [where the analysis is most robust]
```

## Error Handling

**Position is too vague to question:** Start with clarification questions only. Return these to the user as the first step — "Before I can examine this, I need to understand what precisely you're claiming."

**User becomes defensive:** Soften the framing. "That's a fair position — let me see if I can find the strongest challenge to it" is less threatening than "What evidence do you have for that?" The goal is insight, not confrontation.

**Every question has a strong answer:** The position may actually be well-reasoned. Report this honestly — "This position holds up well under Socratic examination" is a valid and valuable finding. Note what would have to change to weaken it.

**The position collapses immediately:** Don't pile on. Identify the single most fundamental problem and suggest what a revised, stronger version might look like. Help the user rebuild, not just demolish.
