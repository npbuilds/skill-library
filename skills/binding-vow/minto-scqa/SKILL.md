---
name: minto-scqa
description: >
  Reference the Minto Pyramid Principle, SCQA narrative structure (Situation, Complication,
  Question, Answer), MECE classification, and BLUF (bottom-line-up-front) format. Use when
  binding-vow's compression skills (scqa-formatter, executive-distiller, bluf-shaper) need
  the canonical specification of the structure they produce, or when designing audience-fit
  communication.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
---

# Minto SCQA — The Pyramid Principle Reference

Barbara Minto formalized executive communication at McKinsey in the 1970s. Her three rules — Pyramid Principle, SCQA, and MECE — are the canonical structures for compressing a complex problem into a form an executive can act on. BLUF (US Army origin) is a sibling format with the same logic at a different scale. Together they define what binding-vow's compression subdomain produces.

The core insight: humans don't read top-down by default. Readers reconstruct your structure from your sentences. Give them the structure first, and they read three times faster with higher comprehension.

## The Pyramid Principle

Every document has a single governing thought at the top. That thought is supported by 2–5 subordinate thoughts. Each subordinate thought is supported by 2–5 of its own subordinates. Recurse until atomic.

```
                     [Single governing thought]
                    /             |             \
            [Subthought 1]  [Subthought 2]  [Subthought 3]
              /     \         /     \         /     \
          [...]   [...]   [...]   [...]   [...]   [...]
```

**Three rules** (these are non-negotiable):

1. **Ideas at any level summarize the ideas grouped below them.** Pull-back rule: each parent must be the summary of its children.
2. **Ideas in each grouping are the same kind of idea.** Sibling rule: don't mix categories at the same level.
3. **Ideas in each grouping are logically ordered.** Order rule: time, structure, or importance.

## SCQA — The Story Structure

SCQA frames the introduction so the reader instantly knows why they should care.

| Element | Purpose | Example |
|---|---|---|
| **Situation** | A familiar truth the reader already accepts | "We have grown 3× in the last two years." |
| **Complication** | Something has changed, or a tension has emerged | "But customer churn has accelerated to 12%." |
| **Question** | The implicit question the complication raises | "What's driving the churn and how do we stop it?" |
| **Answer** | The governing thought (top of the pyramid) | "Churn is driven by onboarding; we should rebuild it in Q3." |

The **A** in SCQA *is* the top of the pyramid. The introduction sets up the question that the rest of the document answers. Once you have SCQA, the body of the document is the supporting structure beneath the answer.

**Variants of SCQA** (all valid; pick by audience):

| Variant | Use when |
|---|---|
| Standard SCQA | Reader is informed but unfocused |
| SCRA (Resolution instead of Q→A) | Reader knows the answer; you're proposing what to do |
| Concern-priming SCQA | Reader is skeptical; lead with their objection |

## MECE — Mutually Exclusive, Collectively Exhaustive

When grouping ideas at any level of the pyramid, the grouping must be MECE:

- **Mutually Exclusive** — no overlap between siblings
- **Collectively Exhaustive** — siblings together cover the entire space

Failure modes:

| Failure | Symptom | Fix |
|---|---|---|
| Not ME | "The three reasons are: cost, complexity, and the engineering team's skill." | Cost and complexity overlap; restructure |
| Not CE | "Customers leave for two reasons: price and product." | What about service, alternatives, life changes? |
| False parallel | "The plan has three phases: discovery, planning, and exiting" | "Exiting" isn't parallel to discovery and planning; structural mismatch |

Test for MECE: can a reader place every relevant fact in exactly one bucket? If not, the grouping is wrong.

## BLUF — Bottom Line Up Front

Military / executive format. The structure:

```
BOTTOM LINE: [One sentence — the recommendation or finding]

BACKGROUND: [What changed; minimum context to make the bottom line make sense]

DISCUSSION: [The reasoning, in priority order]

RECOMMENDATION: [Specific action(s) requested]
```

BLUF differs from SCQA in scale and tone: BLUF is for short outputs (email, slack, briefing) where you can't afford an introduction; SCQA is for documents where the introduction earns its space. Use BLUF when the reader has 30 seconds; use SCQA when they have 5 minutes.

## How binding-vow uses Minto

The audience tag (set by `audience-classifier`) drives which structure applies:

| Audience | Default structure | Why |
|---|---|---|
| Exec (decision-maker, time-pressured) | BLUF for short; SCQA-Pyramid for memos | They need the answer first; supporting detail second |
| Peer (collaborator, parallel context) | SCQA | Story structure invites engagement; matches conversational priors |
| Self (your own clarity) | Pyramid (skip SCQA intro) | You already have the situation; you need the structure |
| Public (broad audience, mixed context) | SCQA with Concern-priming | Trust must be built; objections pre-empted |
| LLM | Anthropic-canonical structural order (see `cursed-speech`) | Different audience entirely; format-shape matters more than narrative |

Each compression skill in the binding-vow suite implements one of these structures:

| Compression skill | Implements |
|---|---|
| `bluf-shaper` (binding-vow, future) | BLUF format directly |
| `scqa-formatter` (binding-vow, future) | SCQA introduction + 1-level pyramid |
| `executive-distiller` (binding-vow, future) | Full Pyramid Principle with N-level recursion |
| `cursed-speech` (binding-vow, future) | NOT Minto — Anthropic-canonical order. Minto is for humans; LLMs need different shape. |

The MECE rule applies inside *any* of these skills' outputs and inside `claim-decomposer`'s atomic-claim grouping. MECE failure in decomposition propagates as MECE failure in compression.

## Common Mistakes

- Burying the bottom line. The most common failure. Reader sees three paragraphs of context and gives up before the answer.
- Mixing levels in the pyramid. A subordinate thought that's actually a sibling of its parent.
- False MECE — using parallel-sounding categories that overlap or omit.
- Skipping SCQA's Complication. Without a complication, there is no question, and the answer feels arbitrary.
- Treating BLUF as "just put the conclusion first." BLUF requires the bottom line + recommendation + structured discussion. Stripping the structure is anti-BLUF.

## Connections

- `bluf-shaper`, `scqa-formatter`, `executive-distiller` (binding-vow, future) — implementations
- `cursed-speech` (binding-vow, future) — explicitly does NOT use Minto (different audience)
- `argument-structure` (writing/rhetoric) — Toulmin / Rogerian / classical structures; complements Minto
- `claim-decomposer` (research) — atomic-claim decomposition must be MECE
- `audience-classifier` (binding-vow, future) — picks which Minto variant applies

## Sources

- Minto, B. (1987). *The Pyramid Principle: Logic in Writing and Thinking* (1st U.S. ed.). Pearson. [Multiple later editions; 2009 is widely cited.]
- Minto, B. (2003). *The Minto Pyramid Principle: Logic in Writing, Thinking, and Problem Solving* (3rd ed.). Minto International.
- US Army Regulation 25-50: *Preparing and Managing Correspondence*. (Source of BLUF format conventions.)
- McKinsey & Company internal communication guidelines (Minto's original audience).
