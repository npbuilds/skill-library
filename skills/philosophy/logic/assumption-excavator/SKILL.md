---
name: assumption-excavator
description: >
  Surface hidden premises, unstated warrants, implicit framing, and background assumptions
  in any argument, proposal, or text. Use when the user suspects something is being taken
  for granted, when an argument "feels off" but the problem isn't obvious, or when preparing
  to evaluate a complex position.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Write
---

# Assumption Excavator — The Miner

Every argument rests on a foundation of things taken for granted. Most of those things are invisible to the arguer. This skill digs them up, labels them, and lays them out for inspection.

The excavator doesn't judge whether assumptions are true — that's the argument-analyst's or evidence-evaluator's job. The excavator's job is to make the invisible visible.

## Input

From the logic director or directly:
- The text, argument, proposal, or claim to excavate
- Context: what domain is this in? (affects which assumptions are domain-standard vs. genuinely hidden)
- Depth: **surface** (quick scan for the most important hidden premises) or **deep** (comprehensive excavation)

## Process

### Step 1 — Identify the Explicit Structure

Before excavating what's hidden, map what's visible:
- What claims are explicitly made?
- What reasons are explicitly given?
- What conclusions are explicitly drawn?

This creates the "visible iceberg" — the part above the waterline.

### Step 2 — Excavate by Category

Dig for hidden assumptions in six categories, from most concrete to most abstract:

#### Factual Assumptions
Things assumed to be true about the world.

*Diagnostic questions:*
- What facts does this argument assume without citing evidence?
- If I asked "how do you know that?", which claims would have no cited support?
- What empirical claims are embedded in the premises?

*Example:* "We should expand into the European market" assumes the European market is accessible, profitable, and that the company has the resources to enter it — none of which may be stated.

#### Definitional Assumptions
Assumed meanings of key terms.

*Diagnostic questions:*
- Are any key terms used without definition?
- Could a reasonable person interpret a key term differently?
- Is a word being used technically but presented as if its meaning is obvious?

*Example:* "AI is dangerous" assumes a shared understanding of both "AI" (narrow AI? AGI? current systems?) and "dangerous" (to whom? in what way? at what probability?).

#### Causal Assumptions
Assumed cause-effect relationships.

*Diagnostic questions:*
- Does the argument assume X leads to Y? Is that causal link established?
- Are there assumed mechanisms connecting premises to conclusions?
- Could correlation be masquerading as causation?

*Example:* "Raising minimum wage will increase unemployment" assumes a specific causal mechanism (employer price sensitivity) while ignoring competing mechanisms (increased spending power, reduced turnover).

#### Value Assumptions
Hidden value judgments or priorities.

*Diagnostic questions:*
- What does this argument assume is good, bad, important, or trivial?
- Whose interests are centered? Whose are invisible?
- What trade-offs are implicitly resolved?

*Example:* "We should optimize for user engagement" assumes engagement is the right metric, that more engagement is better, and that engagement doesn't conflict with other values (user wellbeing, truth, social cohesion).

#### Scope Assumptions
Hidden boundaries on the argument's applicability.

*Diagnostic questions:*
- What time frame is assumed?
- What population or context is assumed?
- What scale is assumed?
- Would the argument still hold if the scope changed?

*Example:* "Remote work increases productivity" — for whom? (knowledge workers vs. manufacturing), measured how? (output per hour vs. total output), over what period? (first month vs. first year).

#### Framing Assumptions
The lens through which the issue is presented, which shapes what counts as relevant.

*Diagnostic questions:*
- What metaphor or framework organizes this argument?
- What alternative framings exist?
- What does the current framing make visible? What does it hide?
- Who benefits from this framing?

*Example:* Framing immigration as a "security issue" centers threats and enforcement. Framing it as an "economic issue" centers labor markets and fiscal impact. Framing it as a "humanitarian issue" centers rights and suffering. The framing determines which facts feel relevant.

### Step 3 — Classify Each Assumption

For each excavated assumption, assess:

| Property | Options | Meaning |
|----------|---------|---------|
| **Visibility** | Hidden / Semi-visible / Visible-but-unchallenged | How buried is it? |
| **Contestability** | Uncontroversial / Debatable / Highly contested | Would reasonable people disagree? |
| **Load-bearing** | Critical / Supporting / Decorative | If this assumption falls, does the argument collapse? |
| **Domain-standard** | Yes / No | Is this a normal background assumption in this field, or genuinely unusual? |

Focus the output on assumptions that are **hidden + contestable + load-bearing** — these are the ones that matter most.

### Step 4 — Test for Assumption Clusters

Assumptions often come in clusters — a set of interrelated background beliefs that form a worldview. Common clusters:

- **Market fundamentalism**: efficiency of markets, rationality of actors, price signals as sufficient information
- **Technological solutionism**: technology can solve social problems, innovation is inherently good, disruption is progress
- **Methodological individualism**: social phenomena reduce to individual choices, structural factors are secondary
- **Deficit framing**: problems arise from what's missing (skill, knowledge, motivation) rather than from systemic barriers

Identifying the cluster often reveals more assumptions than excavating one-by-one.

### Step 5 — Generate Counterfactuals

For each critical assumption, briefly state what changes if the assumption is false:

- "If [assumption] is false, then [consequence for the argument]"

This helps the user see which assumptions are actually load-bearing and which are decorative.

## Output

```
ASSUMPTION EXCAVATION
─────────────────────
Text analyzed: [brief description or quote]

Visible structure:
  Claims: [what's explicitly stated]
  Reasons: [what's explicitly offered as support]
  Conclusion: [what's explicitly concluded]

Hidden Assumptions:
  1. [Assumption] — Category: [factual/definitional/causal/value/scope/framing]
     Visibility: [hidden/semi-visible] | Contestability: [debatable/contested]
     Load-bearing: [critical/supporting] | Domain-standard: [yes/no]
     If false: [what changes]

  2. [Assumption] — Category: [category]
     ...

Assumption Clusters Detected:
  [Cluster name]: [which assumptions belong to it and why]

Most Critical Hidden Assumptions (ranked):
  1. [The assumption whose falsity would most damage the argument]
  2. [Second most critical]
  3. [Third most critical]

Recommended Next Steps:
  - [e.g., "Verify factual assumption #2 with evidence-evaluator"]
  - [e.g., "Run argument-analyst on the full argument with these premises made explicit"]
  - [e.g., "Challenge value assumption #4 via steel-man-forge for the opposing values"]
```

## Error Handling

**Text has no discernible argument:** It may still have assumptions worth excavating. Assertions, questions, and proposals all carry assumptions even without explicit reasoning. Proceed with excavation on the claims themselves.

**Everything is already explicit:** Rare, but possible in formal contexts. Report that the argument is unusually transparent and note any assumptions that are visible but unchallenged.

**Too many assumptions to list:** Focus on the critical + hidden ones. Group domain-standard assumptions into a single note ("This argument operates within standard [framework] assumptions") and spend detail on the genuinely hidden or contested ones.

**User is the arguer and may feel exposed:** Excavation is not accusation. Frame hidden assumptions as natural and universal — everyone has them. The goal is awareness, not blame. "Your argument rests on [assumption], which is worth examining" beats "You're assuming [assumption] without justification."
