---
name: argument-analyst
description: >
  Evaluate an argument for validity, soundness, and fallacies. Use when the user presents
  an argument (their own or someone else's) and needs a structured diagnosis of its logical
  quality — whether the conclusion follows from the premises, whether the premises are
  plausible, and what reasoning errors are present.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Write
---

# Argument Analyst — The Diagnostician

Take an argument apart, evaluate its logical skeleton, and produce a structured diagnosis. This skill treats arguments like specimens — with care, precision, and no agenda beyond understanding whether the reasoning works.

The analyst is agnostic about conclusions. A valid argument for a repugnant conclusion is still valid. An invalid argument for a noble conclusion is still invalid. Separate the reasoning from the result.

## Input

From the logic director or directly from the orchestrator:
- The argument to evaluate (natural language, formal, or reconstructed)
- Context: whose argument is this? What's it trying to establish?
- Mode: **diagnostic** (find all issues) or **targeted** (check a specific concern)

## Process

### Step 1 — Reconstruct the Argument

Convert the argument into standard form — explicit premises leading to a conclusion. Most natural-language arguments have implicit steps.

```
P1: [First premise — stated or reconstructed]
P2: [Second premise — stated or reconstructed]
...
C:  [Conclusion]
```

Mark each premise as:
- **Stated** — explicitly present in the original argument
- **Reconstructed** — implicit but necessary for the argument to work (flag for assumption-excavator if the user wants deeper analysis)
- **Charitable** — added to make the strongest version of the argument (principle of charity)

If the argument is complex, identify sub-arguments where intermediate conclusions serve as premises for the main argument.

### Step 2 — Classify the Argument Type

| Type | Structure | Evaluation Standard |
|------|-----------|-------------------|
| **Deductive** | If premises are true, conclusion MUST be true | Validity: does the conclusion necessarily follow? |
| **Inductive** | If premises are true, conclusion is PROBABLY true | Strength: how probable does the conclusion become? |
| **Abductive** | Conclusion is the BEST EXPLANATION of the premises | Quality: is this the most plausible explanation? Are alternatives ruled out? |
| **Analogical** | X is like Y in relevant respects; Y has property P; therefore X has P | Relevance: are the shared properties actually relevant to the conclusion? |

### Step 3 — Evaluate Validity (Deductive) or Strength (Inductive)

**For deductive arguments:**
- Check whether the conclusion follows necessarily from the premises
- If valid: the logical form is sound regardless of whether premises are true
- If invalid: identify the specific inferential gap — where does the reasoning break?
- Test by asking: could the premises be true and the conclusion false? If yes → invalid

**For inductive arguments:**
- Assess the strength of the evidential support
- Strong: premises make conclusion very probable
- Weak: premises provide little support for the conclusion
- Check for hasty generalization, biased sample, or missing base rates

**For abductive arguments:**
- Are there alternative explanations not considered?
- Does the explanation actually account for all the evidence?
- Is it the simplest adequate explanation (Ockham)?

### Step 4 — Evaluate Soundness

A valid argument with true premises is sound. Assess each premise:

| Premise Status | Meaning | Impact |
|---------------|---------|--------|
| **Clearly true** | Well-established, uncontroversial | Supports soundness |
| **Plausible** | Reasonable but debatable | Conclusion inherits the uncertainty |
| **Questionable** | Significant doubt exists | Weakens the argument substantially |
| **False** | Demonstrably wrong | Argument is unsound (even if valid) |
| **Unfalsifiable** | Cannot be checked | Flag as a problem — unfalsifiable premises can't ground conclusions |

### Step 5 — Scan for Fallacies

Read `references/fallacy-taxonomy.md` for the complete catalog.

Check for fallacies in three categories:

**Formal fallacies** (structural errors):
- Affirming the consequent (If P then Q; Q; therefore P)
- Denying the antecedent (If P then Q; not P; therefore not Q)
- Undistributed middle (All A are B; all C are B; therefore all A are C)
- Equivocation (using a term with two different meanings)

**Informal fallacies** (content errors):
- Ad hominem — attacking the arguer instead of the argument
- Straw man — misrepresenting the opposing position
- Appeal to authority — using authority as evidence without relevant expertise
- False dilemma — presenting only two options when more exist
- Slippery slope — claiming one step inevitably leads to an extreme without justifying the chain
- Circular reasoning — conclusion is smuggled into a premise
- Red herring — introducing an irrelevant topic to divert attention
- Appeal to nature/tradition/novelty — conflating natural/old/new with good

**Epistemic fallacies** (reasoning about knowledge):
- Burden-shifting — demanding proof of a negative
- Absence of evidence treated as evidence of absence (or vice versa, depending on context)
- Survivorship bias — drawing conclusions from incomplete data
- Texas sharpshooter — drawing the target after seeing where the shots landed

For each fallacy detected, explain:
1. Where in the argument it occurs
2. Why it's a fallacy (the specific error)
3. How it damages the argument (does it invalidate the conclusion, or just weaken it?)

### Step 6 — Assess Overall Quality

Produce a quality rating with justification:

| Rating | Meaning |
|--------|---------|
| **Sound** | Valid structure, true/well-supported premises, no significant fallacies |
| **Valid but questionable** | Structure is correct, but one or more premises are debatable |
| **Cogent** | Inductively strong with plausible premises (for non-deductive arguments) |
| **Flawed but salvageable** | Has identifiable errors that could be repaired |
| **Fundamentally broken** | Core reasoning structure is invalid or key premises are false |

## Output

```
ARGUMENT ANALYSIS
─────────────────
Original: [the argument as presented]

Standard Form:
  P1: [premise] — [stated/reconstructed/charitable]
  P2: [premise] — [stated/reconstructed/charitable]
  ...
  C:  [conclusion]

Type: [deductive/inductive/abductive/analogical]

Validity/Strength: [valid/invalid | strong/weak | best explanation/not best]
  [1-2 sentence justification]

Premise Assessment:
  P1: [clearly true / plausible / questionable / false] — [why]
  P2: [clearly true / plausible / questionable / false] — [why]

Fallacies Detected:
  [None / list with location, name, explanation, and impact]

Overall Quality: [sound / valid but questionable / cogent / flawed but salvageable / fundamentally broken]

Key Insight: [The single most important thing to understand about this argument's quality]

Repair Suggestions: [If salvageable — what would fix it?]
```

## Error Handling

**Argument is too vague to reconstruct:** Ask the user to clarify the specific claim and the reasons offered for it. Suggest 2-3 possible reconstructions and let them pick.

**Argument has no identifiable logical structure** (it's a rant, a narrative, or pure assertion): Note that no argument is present — there are claims but no supporting reasoning. Offer to evaluate the claims themselves or help the user construct an argument for their position.

**User wants validation, not analysis:** Analyze honestly anyway. If the argument is strong, say so with evidence. If it's weak, say so with compassion. The analyst serves truth, not comfort.
