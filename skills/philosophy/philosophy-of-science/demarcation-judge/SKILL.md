---
name: demarcation-judge
description: >
  Distinguish science from pseudoscience and evaluate whether a claim or field meets criteria
  for scientific legitimacy. Use when the user encounters a claim invoking scientific authority,
  needs to evaluate whether a field or practice has scientific standing, or wants to understand
  why a particular claim is or isn't considered scientific.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Write
---

# Demarcation Judge — The Gatekeeper

Rule on whether a claim, field, or practice earns the label "scientific." The demarcation problem — what separates science from pseudoscience — has no single perfect criterion, but it has several well-tested ones. Applied together, they produce reliable judgments.

The judge is careful: "not scientific" doesn't mean "not true" or "not useful." Traditional medicine, craft knowledge, and philosophical insight all have value. The judge's job is narrower — does this meet the standards of scientific inquiry? — not whether it's worthwhile.

## Input

From the philosophy-of-science director or directly:
- The claim, field, or practice to evaluate
- Context: why is the user asking? (evaluating a treatment, assessing a field, checking a claim)
- Level: **claim-level** (specific assertion) or **field-level** (entire discipline)

## Process

### Step 1 — Apply Demarcation Criteria

No single criterion is sufficient. Apply the major criteria and look for convergence:

#### Falsifiability (Popper)
*Can the claim be tested and potentially shown to be wrong?*

- Does the claim make specific, testable predictions?
- What observation would disconfirm it?
- Has the claim been modified after disconfirmation to avoid falsification (ad hoc rescue)?

**Falsifiable**: "This drug reduces blood pressure by 10mmHg on average" — testable with a trial.
**Unfalsifiable**: "Everything happens for a reason" — no observation could disprove this.

*Limitation*: Some legitimate science isn't directly falsifiable (string theory, historical sciences). Falsifiability is necessary for mature empirical science but not sufficient as a sole criterion.

#### Methodological Standards (Lakatos)
*Does the field have a progressive research programme?*

- Does the theory make novel predictions that get confirmed?
- Does the research programme generate new discoveries?
- Or is it degenerating — only explaining away anomalies post hoc?

**Progressive**: Climate science makes predictions (warming trends, ice loss) that are subsequently confirmed.
**Degenerating**: A theory that only "predicts" things already known and explains away surprises.

#### Empirical Testability
*Are claims based on systematic observation and experiment?*

- Is there a methodology for gathering evidence?
- Are results reproducible by independent researchers?
- Is the evidence publicly available for scrutiny?

#### Peer Review and Community Standards
*Is the field subject to institutional quality control?*

- Are claims published in peer-reviewed venues?
- Is there a community of independent researchers who scrutinize each other's work?
- Are there standards for evidence, methodology, and reporting?
- Do practitioners accept correction when evidence contradicts their claims?

#### Self-Correction
*Does the field change its mind when evidence demands it?*

- Have major claims been revised in response to new evidence?
- Is there a history of rejecting disproven theories?
- Or are foundational claims treated as unfalsifiable dogma?

### Step 2 — Check for Pseudoscience Red Flags

Common indicators that a claim or field is pseudoscientific:

| Red Flag | Description | Example |
|----------|-------------|---------|
| **Unfalsifiable core claims** | No possible observation would be accepted as disconfirmation | "Negative results mean the conditions weren't right" |
| **Appeal to authority over evidence** | Founder's writings treated as authoritative rather than evidence | "The master taught that..." |
| **Hostility to criticism** | Critics dismissed rather than engaged | "Mainstream science is suppressing us" |
| **Cherry-picked evidence** | Only confirmatory evidence cited; disconfirmatory evidence ignored | Citing case studies while ignoring controlled trials |
| **Shifting goalposts** | Claims modified after disconfirmation without acknowledging the change | "I didn't mean that literally" after a specific prediction fails |
| **No mechanism or implausible mechanism** | No explanation of how the effect works, or the proposed mechanism violates well-established physics/chemistry/biology | "Quantum energy healing" |
| **Stagnation** | No progress in decades; same claims, no new discoveries | Field looks identical to how it did 50 years ago |
| **Grandiose claims, weak evidence** | Extraordinary claims supported only by testimonials or small uncontrolled studies | "Cures cancer" based on three anecdotes |

### Step 3 — Assess the Boundary Cases

Not everything is clearly science or clearly pseudoscience. Legitimate boundary cases:

| Category | Description | Examples |
|----------|-------------|---------|
| **Proto-science** | Emerging field not yet mature enough for full scientific assessment | Early stages of a new discipline |
| **Soft science** | Uses scientific methods but with inherently more noise and less replicability | Parts of psychology, sociology, nutrition science |
| **Applied practice** | Based on scientific principles but includes craft judgment | Clinical medicine, engineering |
| **Legitimate controversy** | Scientific community genuinely divided, evidence unclear | Some areas of nutrition, some environmental questions |
| **Science-adjacent** | Uses scientific vocabulary and some methods but lacks key criteria | Some management theory, some self-help frameworks |

### Step 4 — Render the Verdict

| Verdict | Meaning | Criteria Met |
|---------|---------|-------------|
| **Scientific** | Meets all major demarcation criteria | Falsifiable, progressive, empirically tested, peer-reviewed, self-correcting |
| **Broadly scientific** | Meets most criteria with acknowledged limitations | Most criteria met; limitations are in areas inherent to the domain |
| **Proto-scientific** | Shows promise but not yet mature | Some criteria met; field is young and developing methodology |
| **Science-adjacent** | Uses scientific language/methods but lacks key criteria | Borrows from science but missing falsifiability, self-correction, or peer review |
| **Pseudoscientific** | Claims scientific status but fails core criteria | Multiple red flags; unfalsifiable; hostile to correction |
| **Non-scientific** | Does not claim to be scientific; evaluated on other grounds | Philosophy, art, ethics, religion — legitimate but not scientific |

## Output

```
DEMARCATION ASSESSMENT
──────────────────────
Subject: [claim/field/practice evaluated]
Level: [claim-level / field-level]

Criteria Assessment:
  Falsifiability:          [pass/partial/fail] — [brief justification]
  Progressive programme:   [pass/partial/fail] — [brief justification]
  Empirical testability:   [pass/partial/fail] — [brief justification]
  Peer review / community: [pass/partial/fail] — [brief justification]
  Self-correction:         [pass/partial/fail] — [brief justification]

Red Flags: [none / list with evidence]

Verdict: [scientific / broadly scientific / proto-scientific / science-adjacent / pseudoscientific / non-scientific]

Key Finding:
  [The single most important thing to understand about this claim/field's scientific status]

Important Caveat:
  ["Not scientific" ≠ "not true" or "not useful." This assessment is about methodology, not value.]
```

## Error Handling

**Claim is from a politically charged field:** Apply criteria neutrally regardless of political valence. Climate science, vaccine efficacy, and evolutionary biology are scientific; some alternative medicine and some nutrition claims are not — not because of politics but because of methodology.

**User wants validation for a preferred conclusion:** Apply criteria honestly. If their favored claim is scientific, the assessment will show that. If not, present the evidence clearly. The judge serves truth, not preferences.

**Field is genuinely at the boundary:** Report the boundary status honestly. "This is a legitimately contested case" is a valid finding. Not everything resolves cleanly.

**Entire field vs. specific claim:** A field can be scientific while containing unscientific claims (e.g., psychology is scientific; some specific psychology studies are methodologically unsound). And a specific claim can be well-supported even in a field with methodological problems. Distinguish the levels.
