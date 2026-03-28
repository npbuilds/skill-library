---
name: sommelier-lab
description: >
  Route questions at the experimental frontier of wine knowledge — synesthetic
  tasting notes, coached blind tasting practice, climate change projections for
  wine regions, and molecular flavor pairing science. Use when the user wants
  to explore wine creatively, practice for a sommelier exam, understand the
  science behind non-obvious pairings, or speculate on the future of wine
  geography.
tools: Read
---

# Sommelier Lab — The Experiment

> **Type:** Director
> **Suite:** Bacchus
> **Domain:** Sommelier

## Description

The experimental wing of the Bacchus suite — routes to creative, scientific, and forward-looking wine skills that go beyond conventional sommelier knowledge. Handles synesthetic description, blind tasting practice and exam coaching, climate science applied to specific wine regions, and the molecular chemistry of food and wine pairing. Where Bacchus gets curious, speculative, and rigorous in equal measure.

---

## Routing Table

| Skill | Handles |
|---|---|
| `synesthetic-notes` | Describing wine through other sensory domains — color, music, landscape, texture, emotion. Non-technical communication, creative tasting notes, metaphor and translation. |
| `blind-tasting-trainer` | Structured blind tasting practice sessions, exam preparation (CMS, WSET), grid coaching, deductive reasoning, diagnostic pattern reinforcement. |
| `climate-projections` | Scientific projections for specific wine regions under climate change, 2050–2100 scenarios, emerging frontier regions, variety transition. |
| `molecular-pairing` | Aroma compound chemistry, the flavor network research, compound-based pairing hypotheses, and the scientific basis (and limits) of molecular gastronomy pairing. |

---

## Multi-Skill Scenarios

**"Describe this wine as music."**
Routes to `synesthetic-notes`. The request is explicitly cross-sensory — musical structure, tempo, mood, and emotional arc map to wine's structure, texture, complexity, and finish.

**"Help me study for my WSET Level 3 exam."**
Routes to `blind-tasting-trainer`. Specify exam format (WSET Level 3 Systematic Approach to Tasting Wine) and generate structured practice sessions with the appropriate grid vocabulary and difficulty level.

**"How will Burgundy change in 50 years?"**
Routes to `climate-projections`. Requires the scientific modeling data for Burgundy specifically — harvest date shifts, acid preservation challenges, altitude vineyard dynamics, and the speculative question of variety transition.

**"Why does chocolate and red wine actually not work?"**
Routes to `molecular-pairing` + (optionally) pairing-science. Molecular analysis of the tannin-tannin clash (red wine tannins + chocolate tannins = drying, harsh), sugar imbalance (sweet chocolate makes dry wine taste harsh), and the shared compound myth. Then the structural explanation from pairing-science.

**"Write me a poetic tasting note for this 2015 Barolo."**
Routes to `synesthetic-notes`. Pulls from the wine → landscape, wine → emotion, and wine → music frameworks to produce a literary tasting note with metaphorical resonance.

**"I want to understand why Champagne works with oysters scientifically."**
Routes to `molecular-pairing`. The methylpyrazine and marine aldehyde explanation, plus CO₂ and acid mechanics.

**"What wine should I bring to a highly technical blind tasting group?"**
Routes to `blind-tasting-trainer` for the diagnostic profile (what makes a wine interesting/deceptive for experienced tasters) + potentially `wine-futures` (if the goal is to bring an emerging region wine that challenges assumptions).

---

## Curriculum

Unlike most director skills, Sommelier Lab has **no strict curriculum order**. The four skills serve different purposes and can be engaged in any sequence:

- `synesthetic-notes` is a creative and communication tool — use when description and language are the goal
- `blind-tasting-trainer` is a practice and exam tool — use when skill-building and certification are the goal
- `climate-projections` is a scientific and forward-looking tool — use when understanding structural change is the goal
- `molecular-pairing` is an analytical and discovery tool — use when understanding the chemistry of what we taste is the goal

Users may naturally move between all four: a WSET student might use blind-tasting-trainer for exam prep, then molecular-pairing to understand why certain grape varieties have diagnostic aroma compounds, then synesthetic-notes to develop their descriptive language.

---

## Philosophy of This Director

Sommelier Lab explicitly invites:
- **Speculative thinking**: climate projections beyond 10 years, hypothetical pairing experiments, cross-domain analogies
- **Metaphor and creative language**: synesthetic description is not imprecision — it is a different kind of precision
- **Cross-domain connections**: wine connects to music, architecture, geology, chemistry, history, literature. Follow those threads.
- **Scientific rigor where it exists**: molecular pairing and climate science are grounded in peer-reviewed research. Call that out.
- **Honest uncertainty**: where science is uncertain, label it. Where projections are speculative, say so. The discipline of distinguishing confirmed knowledge from plausible extrapolation is part of the skill.

**Label speculation clearly.** When this director generates content that is forward-looking, hypothetical, or extrapolated beyond current data, it marks it as such. This is the standard throughout all four skills in this director.

---

## Scope

Sommelier Lab is where Bacchus goes beyond conventional sommelier knowledge. It is not the place for basic pairing recommendations (that belongs in `pairing-science`) or straightforward regional wine education (that belongs in the regional skills). It is specifically for:
- Creative and non-literal description of wine
- Structured exam and study preparation
- Scientific analysis of climate and chemistry as they relate to wine
- Pushing the boundaries of what wine conversation can include

Cross-links to the writing domain (for literary tasting notes), the research domain (for science-deep-dive requests), and the investing domain (for climate change as an investment thesis) are all possible and encouraged when the conversation expands into those territories.
