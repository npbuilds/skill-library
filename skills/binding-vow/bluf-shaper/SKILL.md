---
name: bluf-shaper
description: >
  Shape an audited problem statement as BLUF (Bottom Line Up Front) — one-sentence answer,
  minimum background, priority-ordered discussion, explicit recommendation. Use for
  time-pressured executive readers, military/operational briefings, slack messages, or any
  output where the reader has 30 seconds. Returns a structured BLUF block ready for delivery.
metadata:
  author: nirav
  version: "1.0.1"
compatibility: Designed for Claude Code
allowed-tools: Read Write
---

# BLUF Shaper — Bottom Line Up Front

BLUF is a four-component format: a one-sentence answer, the minimum context to make that answer make sense, the reasoning ranked by priority, and an explicit ask. Used by the US military and adopted by executive communication, BLUF is the right tool when the reader has seconds, not minutes.

For the canonical specification, see [[minto-scqa]] (which covers BLUF alongside Minto's full Pyramid).

## When to Use BLUF (and When Not To)

| Use BLUF | Don't use BLUF |
|---|---|
| Reader has ≤30 seconds before deciding | Reader needs to be persuaded — use SCQA |
| The recommendation is well-grounded and the reader trusts you | Reader is skeptical and needs the reasoning to land before the answer |
| You're delivering to an executive, on-call engineer, or operational decision-maker | You're writing a document for archive or training |
| Channel is short-form (slack, email subject + first line, briefing card) | Channel is a memo or essay |
| Audience tag from `audience-classifier` is `exec` AND length budget is short | Audience is `peer`, `self`, `public`, or `LLM` (different formats apply) |

## Process

### Step 1 — Extract the bottom line

The bottom line is the *answer to the implicit question the reader is bringing*. Not the topic, not the situation, not your reasoning — the answer.

Reformulation discipline:
- Start with a verb if a recommendation: "Approve...", "Hold...", "Pivot..."
- Start with a finding if descriptive: "Q3 revenue will miss plan by 12%."
- Avoid hedging words ("likely", "potentially", "we think") in the bottom line itself — qualify in discussion.

If you cannot state the bottom line in one sentence, the input statement isn't ready for BLUF. Route back to `statement-grader` for re-grading on specificity.

### Step 2 — Compress background to minimum context

Background is the *one or two facts* the reader needs to know to make the bottom line interpretable. Not the whole story; not what you'd put in a briefing memo; the minimum.

Test: if you removed each background sentence, would the bottom line still be interpretable? If yes, remove it.

### Step 3 — Order discussion points by priority

The reader will read top to bottom and stop when they decide. Put the strongest point first, second-strongest next, etc. Do NOT save the punchline for the end (that's narrative; this is BLUF).

Each point should be one sentence or two. Bullets, not paragraphs.

### Step 4 — Make the recommendation explicit

What action do you want the reader to take? Approve a budget? Sign a document? Call a meeting? Be specific:

- "Approve $2M for Q3 onboarding rebuild."
- "Hold the position; don't add."
- "Schedule a 30-min review with the trial team this week."

If the answer is "FYI, no action needed," state that explicitly: "FYI — no decision needed; sharing for awareness."

## Output Format — return EXACTLY this block, labels uppercase, in this order:
BOTTOM LINE: [one sentence answer or recommendation]
BACKGROUND:
- [fact 1; minimum context]
- [fact 2; only if essential]
DISCUSSION:
1. [strongest reason]
2. [second-strongest]
RECOMMENDATION: [specific action requested]

## Failure Modes

| Failure | Response |
|---|---|
| Bottom line is two sentences | Compress further; if you can't, the statement isn't BLUF-ready — re-grade specificity |
| Background takes >3 lines | You're writing a memo, not a BLUF — switch to `executive-distiller` |
| Discussion has >5 points | You're padding; cut to the strongest 3 |
| Recommendation is vague ("we should consider...") | Force specificity: who does what by when? If you can't, the recommendation isn't ready |
| Reader is skeptical of you or the topic | BLUF is wrong format — switch to `scqa-formatter` so the complication earns the answer |

## Output Contract for `six-eyes`

When called from Phase 5 with audience tag `exec` and length budget short:
- Return the structured BLUF block
- Tag any sub-component that failed to compress (e.g., "background didn't compress under 3 lines — flagging for re-grade on specificity")
- If the input wasn't BLUF-shape-able, return "deferred" and recommend rerunning compression with `executive-distiller`

## Scope Boundaries

- **bluf-shaper handles:** assembling a 4-component BLUF block from an audited statement.
- **bluf-shaper does NOT:** decide whether BLUF is the right format (`audience-classifier` does that). If the input is unmistakably wrong-shape (peer audience, persuasion needed), surface this and recommend a different compression skill rather than producing low-quality BLUF.

## Connections

- `minto-scqa` (binding-vow) — canonical reference for BLUF format and its decision rules
- `audience-classifier` (binding-vow, future) — sets the audience tag that routes to this skill
- `scqa-formatter` (binding-vow) — sibling compression skill for peer/skeptical audiences
- `executive-distiller` (binding-vow) — sibling for longer executive memos
- `statement-grader` (binding-vow) — re-grade target if compression fails

## Sources

- US Army Regulation 25-50: *Preparing and Managing Correspondence*. (BLUF format conventions.)
- US Army FM 6-99 — *Brevity Codes*. (BLUF in operational briefings.)
- See [[minto-scqa]] for the comparative analysis of BLUF, SCQA, and Pyramid Principle.
