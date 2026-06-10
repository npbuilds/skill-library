---
name: synthesis-translator
description: >
  Convert a Spelunker research brief into one of four target formats — executive memo, VC pitch
  bullets, tweet thread, or decision memo — while preserving citations and confidence tags.
  Spelunker has one default output (long-form brief); this skill multiplies that into the formats
  the user actually publishes/uses. Callable as the optional last step of Spelunker Phase 6, or
  standalone on any existing brief in `research/`.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Write
---

# Synthesis Translator — The Format Multiplier

Spelunker produces auditable research briefs. But auditable briefs are rarely the right artifact for the destination — VC interviews want 3-bullet conviction statements, portfolio writeups want executive memos, social posts want tweet threads, decision memos want a recommendation with a counter-position. This skill takes one brief and produces the right shape without stripping the epistemic discipline.

## Guiding Principles

1. **Citations survive translation.** A claim in the original brief carries `[N]`; that `[N]` survives in every output format. The References section comes along.
2. **Confidence tags are not optional.** A tweet thread can compress them to icons (✓ Confirmed, ◐ Likely, ? Speculative) but cannot drop them.
3. **No new claims.** The translator restructures and compresses; it does not introduce assertions absent from the source brief.
4. **Honest about format limits.** A 280-character tweet cannot capture nuance — flag what was cut.

## How to Run

### Input

- A Spelunker research brief (Markdown, in the format defined by `../evidence-synthesizer/references/synthesis-templates.md`)
- A target format: `memo` | `pitch` | `thread` | `decision`
- Optional: target audience descriptor (e.g., "VC partner with biotech focus", "personal Twitter followers", "internal product team") — affects tone but not content

### Steps

#### Step 1 — Parse the Source Brief

Extract:
- The original question and depth mode
- Key Findings (with their confidence tags)
- The full citation list
- Any Contested or Speculative findings (these get special handling per format)
- The Brief ID

#### Step 2 — Apply Format-Specific Compression

**Format: `memo` (executive memo, ~1 page)**

```
Memo: <restated question, framed as an answer>
Brief: <SPK-id> · Depth: <mode> · Date: <date>

TL;DR: <2-3 sentences capturing the highest-confidence answer with an inline confidence indicator>

Key findings:
  1. [Confidence] <Finding> [N]
  2. [Confidence] <Finding> [N]
  3. [Confidence] <Finding> [N]

What's not settled:
  - <Contested finding> [N] — both positions and what would resolve

Recommended action: <if and only if the original brief had a Next Steps section, surface its top item>

References:
  [N] <full citations from the source brief>
```

**Format: `pitch` (3-bullet VC-style conviction statements)**

```
On <topic>:

  • <Confidence-tagged claim, ≤25 words> [N]
  • <Confidence-tagged claim, ≤25 words> [N]
  • <Confidence-tagged claim, ≤25 words> [N]

Where I'm uncertain: <one sentence naming the highest-priority Speculative or Contested element>

Sources: <inline citation list, can be condensed>
```

Each bullet should make a falsifiable claim, not a vague summary. Tag-icons (✓ for Confirmed, ◐ for Likely, ? for Speculative, ⚠ for Contested) are acceptable for compression.

**Format: `thread` (tweet thread, 5-9 tweets)**

Tweet 1 (hook): The answer in one sentence with the highest-confidence finding.
Tweets 2-N (one per finding, 220 char max each):
- Lead with the confidence icon
- State the finding
- One link or citation handle (`(see [1])`) — full citation in the final tweet
Final tweet: Methodology note + brief ID + link to full brief.

Cap at 9 tweets. If the brief has more findings, pick the 7 highest-confidence ones and note: "Cut 3 lower-confidence findings — see brief for full picture."

**Format: `decision` (decision memo with recommendation)**

```
Decision Memo: <decision question — must be a question with a discrete set of answers>
Brief: <SPK-id> · Date: <date>

Recommendation: <option> — confidence: <tier>

Why:
  1. [<Confidence>] <Finding supporting the recommendation> [N]
  2. [<Confidence>] <Finding supporting the recommendation> [N]

Counter-position:
  <The strongest case for an alternative option, drawn from any Contested or Speculative findings in the brief>

Sensitivity:
  This recommendation would change if: <specific finding that, if it flipped, would change the answer> [N]

Open questions before deciding:
  - <From the brief's Gaps section, the highest-priority unresolved item>

References:
  [N] <full citations>
```

The "Sensitivity" section is mandatory for `decision` — it forces the brief's load-bearing claim into focus.

#### Step 3 — Honesty-Preserving Compression Rules

- Never upgrade a confidence tag in translation. Likely stays Likely.
- Never drop a Contested finding silently — it must appear in either the body or a "What's not settled" section.
- If the brief's overall confidence was "Insufficient evidence," the output must state this prominently in the first 50 words. Do not produce an executive memo or pitch from an insufficient-evidence brief without that warning.
- If compression forces dropping findings, list what was cut at the bottom of the output.

### Output

The translated artifact in the requested format, plus a footer:

```
─────────────────────────────────────
Translated from: <SPK-id> (<original depth mode>)
Format: <memo|pitch|thread|decision>
Findings included: <N> of <M> from source brief
Findings cut: <list, if any>
```

## Error Handling

**Source brief lacks citations:** Refuse to translate. Output: "Source brief has no inline `[N]` citations — translation would propagate unsourced claims. Re-run the brief with citation discipline first." This is the citation-discipline contract from P0; the translator enforces it at egress.

**Source brief is missing depth mode:** Default to displaying "depth: unknown" — do not assume.

**Format choice doesn't match the brief shape:** E.g., asking for `decision` format on a brief that doesn't address a discrete decision. Output a warning and ask the user whether to (a) reformulate as the closest valid format, or (b) abort.

## Scope Boundaries

**Does NOT:** Add new findings, sources, or analysis.
**Does NOT:** Change confidence tags.
**Does NOT:** Translate between languages — output is in the source brief's language.
**Does NOT:** Optimize for engagement metrics on social formats — honesty over virality.
