---
name: executive-communication
description: >
  Write at executive grade — memos, decks, board materials, decision recommendations,
  status updates — using BLUF structure, audience-tuned vocabulary, and explicit reasoning.
  Reference when drafting any document that will be read by a senior audience under time
  pressure. Executive communication is the highest-leverage written skill in any senior
  role: one good memo creates an artifact that travels across the organization and lives
  for months.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read
---

# Executive Communication — The Highest-Leverage Written Skill

A senior leader's written output gets read in two modes simultaneously: skimmed (busy CEO scrolling on a phone between meetings) and deep-read (board member preparing for the meeting). The strong document serves both modes on the same page. The weak document forces the reader to choose: skim and miss the substance, or deep-read and burn time the reader doesn't have.

## Key Concepts

### BLUF — Bottom Line Up Front

The single most important principle in executive writing: the headline conclusion goes at the top, before any setup or context.

```
BLUF Structure:
1. ONE-LINE BOTTOM LINE — The conclusion / recommendation / key fact
2. Three-bullet summary — What supports the bottom line
3. (For longer docs) Body with full reasoning
```

This serves both reading modes: the skimmer gets the answer in 3 lines; the deep-reader has the full reasoning available below.

Hand off to `binding-vow/bluf-shaper` for the canonical BLUF craft.

### The Minto Pyramid for Longer Docs

For documents longer than a single page, structure the body using the Minto Pyramid:

- **Top**: The one main idea (= the bottom line)
- **Middle**: 3–5 supporting arguments
- **Bottom**: Evidence and detail under each supporting argument

Each level summarizes what's beneath it. The reader can stop at any level and have a coherent answer. Hand off to `binding-vow/minto-scqa` for the canonical Minto craft.

### The SCQA Opener

For situations where context is needed before the bottom line (rare but real), use SCQA:

- **Situation** — Shared context (what we both know)
- **Complication** — What changed; what makes this newsworthy
- **Question** — The implicit question the reader is now holding
- **Answer** — Your bottom line

SCQA delivers the bottom line second, but only after establishing why the bottom line matters. Use sparingly.

### Common Executive Document Types

| Type | Length | Structure |
|---|---|---|
| **Decision memo** | 1–2 pages | BLUF + recommendation + supporting reasoning + risks + ask |
| **Status update** | 1 page or short email | BLUF + key results + risks + asks |
| **Board memo** | 5–10 pages | BLUF + KPIs + program updates + risks + asks |
| **Investment memo** | 5–15 pages | BLUF + thesis + diligence + valuation + recommendation |
| **Strategy doc** | 5–20 pages | BLUF + situation + options + recommended path + plan |
| **Slack / email update** | 3–8 sentences | BLUF + key facts + ask |

### Tone Calibration

Executive writing tone:

- **Direct, not deferential** — "I recommend X" not "perhaps it might be worth considering X"
- **First-person, where appropriate** — "I recommend" / "I'd want to verify"; not always third-person
- **Active voice** — "We should do X" not "X should be done"
- **Quantified where possible** — "$40M" not "significant capital"
- **Confident, not arrogant** — Confidence in your view; humility about what you don't know
- **Brief, not terse** — Short, but not gnomic

### Common Failure Modes

| Failure | Looks Like | Fix |
|---|---|---|
| Buried lede | The conclusion is on page 3 | BLUF |
| No conclusion | All analysis, no recommendation | Make a call; surface the call up top |
| Hedge-soup | "Perhaps we might consider possibly" | Confidence; commit |
| Acronym fog | "Our PoC for Q2 PoS uplift on the BTD candidate" | Define on first use |
| Wall of text | Long paragraphs, no white space | Bullet, break, structure |
| No specific ask | Document ends without "what I need from you" | Always end with the ask |

### The Audience-First Filter

Before writing, ask: who is reading this, what do they care about, and what decision do they need to make? The document is built backward from the answer to those questions. Hand off to `binding-vow/audience-classifier` for the canonical audience taxonomy.

## Self-Coaching Track

**For your situation (MD → biotech VC/operator):**

1. **Audit your current written outputs.** Pull a recent memo, board update, or strategic doc you've written. Score against BLUF, structure, ask clarity, tone calibration. Where does it score well? Where does it lag?

2. **Build a templates library.** For each document type you regularly produce (decision memo, board update, investment thesis), have a reusable template with the BLUF structure baked in.

3. **Practice BLUF daily.** Every Slack update, every status email, every quick note. Lead with the bottom line. Reps build the muscle.

4. **Get feedback from senior readers.** Ask someone senior to read a recent memo and tell you (a) what they understood from the first 30 seconds, (b) what they'd want changed. Iterate.

5. **For high-stakes documents, do a Minto outline first.** Don't draft prose until the structure is right. Outline → review structure → draft prose. Saves rewriting.

6. **Hand off to binding-vow for the substantive craft.** `bluf-shaper` and `executive-distiller` are the source of methodology; reference them for any high-stakes doc.

## Teach / Mentor-Others Track

**When coaching a junior or peer through executive communication:**

1. **BLUF is the highest-leverage idea.** Many mentees bury the lede. Show one BLUF example, ask them to BLUF-ify a recent doc, watch the comprehension improvement.

2. **Force the audience-first filter.** Mentees often draft for themselves, not the audience. Coach the explicit "who reads this and what do they need" pre-question.

3. **Coach against hedge-language.** Many mentees, especially from clinical backgrounds, default to hedged language. The reframe: hedging where there's genuine uncertainty is honest; hedging where there's not is weak.

4. **Templates accelerate the muscle.** Mentees often re-architect every doc from scratch. Coach a template library; reuse the structure, vary the content.

5. **The senior-reader feedback loop is irreplaceable.** Coach mentees to deliberately solicit reads from senior people. The feedback compounds quickly.

6. **Acronym discipline.** Mentees from acronym-heavy fields (medicine, regulatory) often write fog-grade prose. Coach: define every acronym on first use, even ones that feel obvious.

## When This Applies

- Writing any document that will be read by a senior audience
- Drafting board materials or board updates
- Writing decision memos or strategy docs
- Preparing investment theses or diligence memos
- Quick wins on email and Slack updates

## Cross-Domain Connections

- **binding-vow/bluf-shaper, executive-distiller, minto-scqa** — Source craft for executive writing
- **binding-vow/audience-classifier** — Audience taxonomy
- **executive-presence/meeting-mastery** — Meeting agendas and follow-ups are executive comm artifacts
- **executive-presence/board-readiness** — Board materials are exec comm at board level
- **personal-positioning/cover-letter-craft** — Cover letters are exec-comm-adjacent
- **writing/prose-editor** — Final pass on every exec document
