---
name: tasting-evaluation
description: >
  Route wine tasting and evaluation questions through the Court of Master
  Sommeliers Deductive Tasting Grid and WSET Systematic Approach to Tasting.
  Use when evaluating a specific wine, practicing blind tasting, identifying
  wine faults, or assessing wine quality using structured scoring frameworks.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read
---

# Tasting & Evaluation — The Palate

## skill-metadata
- skill-id: sommelier/tasting-evaluation
- skill-type: director
- parent: sommelier/bacchus
- version: 1.0.0

## description
Routes wine tasting and evaluation questions to four specialist child skills covering the full evaluation pipeline. Handles the CMS deductive grid, fault identification, quality scoring, and aroma vocabulary. Use when a user wants to taste, describe, score, diagnose, or understand any aspect of wine evaluation.

---

## Child Skills

| Skill ID | File | Handles |
|---|---|---|
| deductive-method | tasting-evaluation/deductive-method/SKILL.md | Blind tasting, grid-based analysis, sight/nose/palate/conclusion |
| fault-diagnosis | tasting-evaluation/fault-diagnosis/SKILL.md | Off aromas, wine faults, "send it back?" decisions |
| quality-assessment | tasting-evaluation/quality-assessment/SKILL.md | BLIC framework, scoring systems, readiness, quality ladders |
| aroma-lexicon | tasting-evaluation/aroma-lexicon/SKILL.md | Aroma wheel, vocabulary, primary/secondary/tertiary, diagnostic mapping |

---

## Routing Table

| User Signal | Route To | Why |
|---|---|---|
| "How do I taste wine systematically?" / "What is the deductive grid?" / "Walk me through a blind tasting" | deductive-method | CMS grid is the structured framework for systematic evaluation |
| "This wine smells weird" / "Is this wine corked?" / "What is TCA?" / "Something is off about this bottle" | fault-diagnosis | Fault identification requires specific compound knowledge and a diagnostic protocol |
| "Is this wine good?" / "How do I score a wine?" / "Is this ready to drink?" / "What does 95 points mean?" | quality-assessment | Quality and readiness questions require BLIC framework and scoring system knowledge |
| "What does petrichor mean on a tasting note?" / "How do I build wine vocabulary?" / "What causes that barnyard smell?" | aroma-lexicon | Aroma identification and vocabulary questions belong to the lexicon skill |
| "Write a tasting note for this wine" | deductive-method + aroma-lexicon | Tasting notes require the grid structure plus controlled vocabulary |

---

## Multi-Skill Question Handling

Some questions span more than one child skill. Resolve as follows:

**Scenario 1: "Is this wine faulty or just funky?"**
Load `fault-diagnosis` first. If the compound is identified as a confirmed fault (TCA, VA above threshold, mousiness), close with a definitive verdict. If the compound is in the flaw/style ambiguity zone (brett at low levels, reduction in natural wine), supplement with `quality-assessment` to apply the BLIC framework and assess whether the flaw degrades overall quality.

**Scenario 2: "I'm doing a blind tasting — how do I describe what I'm smelling?"**
Load `deductive-method` for the grid structure and sequencing, then pull `aroma-lexicon` for controlled vocabulary at the nose stage. The grid tells the user what to look for; the lexicon gives them the words.

**Scenario 3: "This 2008 Barolo is showing tar and roses but also something leathery and earthy — is it ready?"**
Load `aroma-lexicon` to confirm the tertiary character of the aromas (leather, earth = tertiary development), then load `quality-assessment` for the readiness assessment protocol (development stage + structural softening). The aroma interpretation informs the drink-window verdict.

**Scenario 4: "My tasting note says high acid, grippy tannin, cassis — what wine is this?"**
Load `deductive-method` for the deductive leap logic (structural signature → grape → region), then supplement with `aroma-lexicon` if specific aromas need unpacking.

**Scenario 5: "I'm studying for my WSET Level 3 — how does quality get assessed?"**
Load `quality-assessment` for the BLIC framework and quality ladder (WSET is its native context), then offer `deductive-method` as the analytical foundation. Always flag which skill addresses which part of the exam syllabus.

---

## Curriculum Order

The skills are designed to be learned in sequence. Each builds on the last.

1. **deductive-method** — Start here. The grid is the language of wine evaluation. A student who cannot structure their observations has nothing to assess. Everything else depends on knowing how to move from sight through nose through palate to conclusion.

2. **aroma-lexicon** — Second. Once the grid's structure is understood, the nose stage becomes the most complex. Noble's wheel gives the student controlled vocabulary, prevents imprecise language, and teaches what each aroma category implies about grape, region, and winemaking. The lexicon makes the grid's nose section actionable.

3. **quality-assessment** — Third. Once a student can describe a wine accurately, they can evaluate it. BLIC requires understanding balance across structural elements (which come from the deductive grid) and a developed palate vocabulary (from the lexicon). Scoring systems only mean something after quality criteria are understood analytically.

4. **fault-diagnosis** — Fourth. Faults are the exception to the system, not the rule. A student who does not yet know what "correct" looks like cannot reliably identify what "faulty" looks like. Fault diagnosis is most powerful as a corrective lens applied after the baseline (grid, lexicon, quality) is established.

---

## Level Progression

### Foundational
- User is learning to taste systematically for the first time
- Focus: deductive-method basics (grid walkthrough), core aroma categories, binary quality assessment (like/dislike → why)
- Skills active: deductive-method, aroma-lexicon (Tier 1 only)
- Language: avoid jargon; always define terms on first use

### Intermediate
- User can work through the grid but struggles with conclusions or vocabulary precision
- Focus: deductive leap (structure → grape/region), full aroma lexicon, BLIC framework, fault identification
- Skills active: all four child skills
- Language: introduce exam terminology, use compound names where instructive

### Advanced
- User is preparing for CMS, WSET Diploma, or MW exams, or is a working professional
- Focus: speed and precision in blind tasting, fault compound knowledge at detection threshold level, scoring calibration across systems, readiness windows
- Skills active: all four, with deductive-grid-schema.md reference for rapid lookup
- Language: full technical vocabulary; no hedging on compound names, thresholds, or scoring systems

---

## Conflict Resolution

When evidence from different parts of the grid or different frameworks disagrees, apply the following hierarchy:

| Conflict | Resolution |
|---|---|
| Nose says one thing; palate says another (e.g., nose suggests old wine, palate shows vibrant acid) | Trust the palate over the nose for structural assessment. Palate determines body, tannin, acid, alcohol. Nose is more useful for aroma development stage and style. Report both and reason through the discrepancy. |
| BLIC score is high but reviewer score is low (or vice versa) | Acknowledge the divergence. BLIC is an analytical tool; reviewer scores incorporate personal preference and market context. Flag which scoring system is being applied and why they may disagree. Never conflate analytical quality with commercial scores. |
| Suspected fault vs confirmed fault | Only call a fault confirmed if the sensory descriptor matches a known compound, the detection threshold condition is plausible, and the fault is consistent across multiple sniffs and a sip. If uncertain, route to fault-diagnosis and use the diagnostic protocol. Never definitively condemn a bottle on a single ambiguous impression. |
| Old World restrained style reads as "low quality" on an extraction-focused scale | Flag this explicitly. Apply the WSET quality ladder (most context-neutral) rather than a score calibrated for ripe, extracted styles. Terroir expression and intentional restraint are not quality deficits. |

---

## Scope Boundaries

This skill suite covers **evaluation of wine as a sensory and analytical experience.**

In scope:
- Systematic blind tasting using any recognized grid (CMS, WSET SAT, BNIC)
- Fault and flaw identification
- Quality assessment and scoring system interpretation
- Building and applying aroma vocabulary
- Reading and writing tasting notes
- Assessing wine readiness and drink windows

Out of scope (route to other sommelier skills):
- Grape variety identification by region history → route to sommelier/varieties
- Specific appellation regulations and production rules → route to sommelier/appellations
- Food and wine pairing logic → route to sommelier/pairing
- Cellar management and storage → route to sommelier/cellar
- Service and decanting technique → route to sommelier/service

---

## Learn Block

After substantive responses in this domain, surface:

```learn
Learn ─── Tasting & Evaluation
Next: [skill name] — [one-line reason it builds on what was just discussed]
```
