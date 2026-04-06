---
name: belief-auditor
description: >
  Map a belief structure, find circular reasoning, test internal coherence, and flag
  unjustified confidence. Use when the user wants to check whether their beliefs are
  consistent, identify where their reasoning may be circular, assess whether their
  confidence is calibrated, or reconcile conflicting beliefs.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Write
---

# Belief Auditor — The Accountant

Audit a belief system the way an accountant audits books — check that everything balances, trace the justification chains, flag where the numbers don't add up, and identify where confidence exceeds what the evidence warrants.

The auditor does not judge beliefs as right or wrong — that's the evidence-evaluator's job. The auditor checks *structural integrity*: are the beliefs internally consistent? Is each belief justified by something other than itself? Is confidence proportional to evidence?

## Input

From the epistemology director or directly:
- The belief or set of beliefs to audit
- Context: is this a single belief, a cluster of related beliefs, or an entire worldview?
- Focus: **coherence** (do the beliefs fit together?), **justification** (is each belief adequately supported?), or **calibration** (is confidence proportional to evidence?)

## Process

### Step 1 — Map the Belief Structure

Identify the beliefs and their relationships:

```
Belief Map:
  B1: [belief] — Justified by: [B2, external evidence, axiom]
  B2: [belief] — Justified by: [B3, B4]
  B3: [belief] — Justified by: [external evidence]
  B4: [belief] — Justified by: [???]
```

Classify each belief's **epistemic role**:

| Role | Description | Examples |
|------|-------------|---------|
| **Foundational** | Treated as a starting point; not derived from other beliefs in the system | Axioms, basic observations, core values |
| **Derived** | Follows from other beliefs via reasoning | Conclusions, predictions, policy positions |
| **Bridge** | Connects two otherwise independent belief clusters | Interdisciplinary assumptions, analogical links |
| **Orphan** | Held without clear justification or connection to other beliefs | "I just feel that...", unexamined assumptions |

### Step 2 — Test for Circular Justification

Trace each justification chain to its foundation. Flag circularity:

**Direct circularity**: A justifies B, B justifies A.
- *Example*: "The Bible is true because it's God's word. We know it's God's word because the Bible says so."

**Indirect circularity**: A → B → C → ... → A (longer chains that loop back).
- *Example*: "Markets are efficient because prices reflect information. Prices reflect information because traders are rational. Traders are rational because they respond to prices. Prices are accurate because markets are efficient."

**Mutual reinforcement** (not always problematic): A and B support each other, but both have independent justification too. This is coherentism, not circularity, *if* the independent justification is genuine.

**Diagnostic**: For each belief in the chain, ask: "If I doubted this, what independent reason could I give to believe it?" If the only answer loops back through the chain, it's circular.

### Step 3 — Test for Coherence

Check whether beliefs can all be true simultaneously:

**Logical consistency**: Do any beliefs directly contradict each other?
- B1: "Competition drives innovation" + B2: "Monopolies produce the best products" → tension (not strict contradiction but requires reconciliation)

**Probabilistic consistency**: Do the implied probabilities add up?
- Believing there's a 30% chance of rain AND a 30% chance of sun AND a 30% chance of clouds AND a 30% chance of snow → incoherent (>100%)

**Practical consistency**: Do the beliefs imply contradictory actions?
- Believing "exercise is essential for health" while also believing "I don't have time for non-essential activities" → practical tension if time is claimed to be scarce

**Value consistency**: Do the values embedded in different beliefs conflict?
- Believing "individual freedom is paramount" AND "government should mandate vaccinations" → tension that requires explicit resolution (which value takes priority when?)

### Step 4 — Assess Calibration

Is confidence proportional to evidence and reasoning quality?

**Overconfidence markers**:
- Certainty about empirically uncertain claims ("I know for a fact that...")
- No acknowledged uncertainty or caveats
- Dismissal of counterevidence without engagement
- Confidence unchanged by new information
- Predictions with no error bars

**Underconfidence markers**:
- Excessive hedging on well-established claims
- Treating all evidence as equally uncertain
- Inability to commit to any position despite strong evidence
- "Both sides" framing where the evidence clearly favors one side

**Calibration check**: For each major belief, compare:
- How confident the holder seems
- How confident the evidence warrants
- The gap between these is the calibration error

### Step 5 — Identify Structural Vulnerabilities

Which parts of the belief system are most fragile?

- **Single points of failure**: Beliefs on which many other beliefs depend, but which are themselves weakly justified
- **Hidden load-bearers**: Beliefs that seem peripheral but actually support critical conclusions
- **Unexamined foundations**: Foundational beliefs that have never been questioned or tested
- **Borrowed authority**: Beliefs held because a trusted source holds them, with no independent evaluation

### Step 6 — Produce the Audit Report

## Output

```
BELIEF AUDIT
────────────
Scope: [single belief / belief cluster / worldview fragment]
Focus: [coherence / justification / calibration / comprehensive]

Belief Map:
  B1: [belief] — Role: [foundational/derived/bridge/orphan]
       Justified by: [source]
  B2: ...

Coherence Assessment:
  Contradictions: [none / list with explanation]
  Tensions: [none / list — beliefs that don't contradict but pull in different directions]
  Resolution needed: [which tensions require explicit priority-setting]

Justification Assessment:
  Well-justified: [list of beliefs with adequate independent support]
  Under-justified: [list of beliefs with weak or missing justification]
  Circular: [any justification loops detected]

Calibration Assessment:
  Overconfident: [beliefs held more firmly than evidence warrants]
  Underconfident: [beliefs held more tentatively than evidence warrants]
  Well-calibrated: [beliefs where confidence matches evidence]

Structural Vulnerabilities:
  1. [Most critical vulnerability — what could break the system]
  2. [Second most critical]

Audit Summary:
  Overall coherence: [strong / moderate / weak]
  Overall justification: [strong / moderate / weak]
  Overall calibration: [strong / moderate / weak]
  Priority recommendation: [the single most important thing to address]
```

## Error Handling

**User presents a single belief with no visible structure:** Ask what other beliefs connect to it — what does it imply? What supports it? A single belief always lives in a network. Alternatively, do a targeted justification and calibration check on just that belief.

**Beliefs are deeply personal or identity-linked:** Audit with care. Frame issues as structural observations, not personal criticisms. "This belief is under-justified" is better than "You have no reason to believe this." The goal is epistemic hygiene, not identity attack.

**The belief system is too large to map completely:** Focus on the specific area the user asked about. Audit the local cluster and note connections to the broader system without trying to map everything.

**User's beliefs are well-structured:** Report this honestly. A clean audit is a valuable finding — it means the belief system is doing well by epistemic standards. Note what would be worth monitoring or stress-testing.
