---
name: source-evaluator
description: >
  Produce structured evaluations of historical sources using provenance, bias, reliability
  assessment, and the PACT protocol from source-criticism. Use when the user presents a
  specific historical document, artifact, or claim and wants a systematic evaluation of what
  it can and cannot tell us, formatted as a reusable analytical template.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
tools: Read
---

# Source Evaluator — Structured Evidence Assessment

This is an action skill that produces structured evaluations of historical sources. It operationalizes the `source-criticism` knowledge skill into a repeatable output template. Given a specific source — a document, artifact, image, or claim — it produces a systematic assessment of provenance, bias, reliability, and analytical value.

## When This Applies

- User presents a specific historical document and asks "what can this tell us?"
- User encounters a historical claim and wants it evaluated
- User wants to practice source criticism with guided structure
- User needs to assess whether a source is reliable for a specific question

## The Evaluation Process

### Step 1 — Identify

Establish basic facts about the source before interpretation:
- What is it? (Document, artifact, image, statistical record, oral testimony?)
- When was it created? (Date and distance from the events it describes)
- Who created it? (Author, institution, anonymous?)
- Where does it survive? (Archive, museum, digital reproduction?)

### Step 2 — Apply PACT Protocol

From `source-criticism`:
- **P**erspective: From whose viewpoint?
- **A**udience: For whom was this created?
- **C**ontext: What was happening when this was created?
- **T**ype: What genre conventions apply?

### Step 3 — Assess Reliability

- What can this source *credibly* tell us?
- What can it *not* tell us?
- Where might it be biased, incomplete, or misleading?
- What corroborating or contradicting evidence exists?

### Step 4 — Render Verdict

Produce a structured assessment using the template below.

## Output Template

```
═══════════════════════════════════════════
SOURCE EVALUATION
═══════════════════════════════════════════

SOURCE: [Full identification]
TYPE: [Primary / Secondary] | [Genre] | [Medium]
DATE: [Creation date] | [Distance from events: contemporary / near / remote]

CREATOR
  Who: [Author / institution / anonymous]
  Position: [Social, political, institutional role]
  Access: [Direct witness / secondhand / reconstruction]

PACT ANALYSIS
  Perspective: [Whose viewpoint; what they can see; what is hidden]
  Audience: [Intended recipient; how audience shapes content]
  Context: [Conditions of creation; pressures and incentives]
  Type: [Genre conventions that shape content]

RELIABILITY ASSESSMENT
  Credible for: [What this source can tell us]
  Unreliable for: [What this source cannot tell us]
  Key biases: [Specific biases identified]
  Silence: [What is notably absent]

CORROBORATION
  Supported by: [Other sources that confirm]
  Contradicted by: [Other sources that disagree]
  Unique claims: [What only this source asserts]

VERDICT
  Analytical value: [HIGH / MEDIUM / LOW] for [specific question]
  Best used for: [What question this source best answers]
  Handle with care: [Specific warnings for interpretation]
═══════════════════════════════════════════
```

## Anti-Patterns

- **Treating primary = trustworthy**: Primary sources are close to events but embedded in their biases
- **Ignoring genre**: A saint's life, a court chronicle, and a tax record require different evaluation methods
- **Skipping corroboration**: No single source should be the sole basis for a historical claim
- **Binary verdicts**: Sources are not "reliable" or "unreliable" — they are reliable *for specific questions* and unreliable *for others*
