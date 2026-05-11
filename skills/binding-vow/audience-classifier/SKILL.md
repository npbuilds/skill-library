---
name: audience-classifier
description: >
  Classify the intended audience of a problem statement as LLM / exec / peer / self / public.
  Use during binding-vow's Phase 2 diagnosis. The audience tag drives the entire compression
  subdomain routing — bluf-shaper for exec, scqa-formatter for peer, cursed-speech for LLM,
  executive-distiller for public. Returns the audience tag plus inferred sub-context such as
  time budget and skepticism level.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Write
---

# Audience Classifier — Who Is This For?

A problem statement that doesn't fit its audience has failed regardless of its other qualities. Statement-grader's audience-fit axis depends on the audience being correctly identified upstream — that's this skill's job. The audience tag drives the entire compression subdomain's routing.

For the canonical mapping of audience → compression skill, see [[minto-scqa]] and the compression skills directly.

## The Five Audience Tags

| Tag | Who | Channel typical | Time budget | Routes to |
|---|---|---|---|---|
| **LLM** | A language model that will execute the resulting prompt | API call, in-context | Model-consumed (~10K tokens fine) | `cursed-speech` |
| **Exec** | Decision-maker, time-pressured, trust intact | Slack, email, brief, deck | 30 sec – 5 min | `bluf-shaper` (short) or `executive-distiller` (memo) |
| **Peer** | Collaborator with parallel context | Doc, email, meeting | 2–15 min | `scqa-formatter` |
| **Self** | The user thinking through their own problem | Note, scratch buffer | Whatever's needed | `scqa-formatter` (skip Q step) or Polya restatement |
| **Public** | Mixed-audience reader who may be skeptical | Essay, post, talk, public memo | 5 min – 30 min | `executive-distiller` (with Concern-priming) or `scqa-formatter` (Concern-priming variant) |

## Detection Signals

Read the statement plus any context the user provided (channel, recipient, purpose). Apply these:

| Signal | Likely audience |
|---|---|
| Output is described as "a prompt", "ask Claude", "send to GPT/Claude" | LLM |
| Recipient is named as a title role (CEO, CMO, board, VP) | Exec |
| Phrase like "memo for the team", "share with engineering", "draft for the working group" | Peer |
| Phrase like "I'm thinking through", "trying to figure out", "for my own clarity" (no specific recipient) | Self |
| Phrase like "publish", "post", "essay", "talk", "newsletter", "public statement" | Public |
| Recipient is a colleague at peer level with similar context | Peer |
| Reader is described as time-pressured or "needs the answer fast" | Exec |
| Reader is described as skeptical, opposed, or requiring persuasion | Public (Concern-priming variant) |
| Output is described as "for me", "for myself", "to remember" | Self |

If multiple audiences are plausible (e.g., "I want to think this through AND share with the team"), default to the *more constrained* audience — sharing imposes more structure than self-thinking, so route Peer.

## Sub-Context Tags

Beyond the primary audience tag, surface sub-context that downstream compression skills can use:

| Sub-context | Values | Used by |
|---|---|---|
| **Time budget** | ≤30s / 30s–5min / 5–30min / open | `bluf-shaper` vs `executive-distiller` choice |
| **Skepticism level** | trusting / neutral / skeptical | SCQA variant selection (standard vs Concern-priming) |
| **Channel** | slack / email / doc / deck / verbal / API | Length and formatting bounds |
| **Familiarity** | high context / partial context / cold | Background-section depth |

These don't change the primary tag; they tune the compression skill's behavior.

## Process

1. **Scan for explicit signals** in the statement and any context (channel, recipient, purpose).
2. **Apply the detection signal table** — count matches per audience tag.
3. **Resolve conflicts.** If multiple tags get matches, apply the "more constrained wins" rule. If genuinely tied, ask the user (this is the right time for L4 user-assist).
4. **Tag sub-context** — time budget, skepticism, channel, familiarity.
5. **Return** primary tag + sub-context.

## Output Format

```
AUDIENCE — [first 60 chars of statement...]
─────────────────────────────────────────────
Primary tag:    [LLM | exec | peer | self | public]
Confidence:     [high | medium | low]
Sub-context:
  Time budget:    [≤30s | 30s–5min | 5–30min | open]
  Skepticism:     [trusting | neutral | skeptical]
  Channel:        [slack | email | doc | deck | verbal | API]
  Familiarity:    [high | partial | cold]
Routes to:      [recommended compression skill, given the primary tag + sub-context]
Rationale:      [which signals matched]
```

## Edge Cases

| Pattern | Handling |
|---|---|
| Statement specifies two audiences explicitly (e.g., "for the CEO and the LLM that will analyze it") | Run compression twice. Tag both audiences; orchestrator's deep mode will produce both shapes. |
| Statement has no explicit audience signals | Default to `self` (the user is thinking, no recipient specified) with low confidence. Recommend the user specify if a different audience is intended. |
| Audience is a class of person, not an individual ("for engineering managers") | Treat as `peer` (collective collaborator). Skepticism level depends on the topic. |
| Audience is an LLM but the user wrote it as if for a human | Tag `LLM` but flag the prose-shaped framing — `cursed-speech` will need to restructure for the canonical order. |
| Audience is "everyone" or "the world" | Tag `public`; flag low confidence; recommend narrowing scope. Public-as-mass-audience usually conceals a more specific intended reader. |

## Output Contract for `six-eyes`

Called from Phase 2 (Diagnose), in parallel with `problem-typology` and `stakes-assessor`. Returns:
- Primary tag
- Sub-context tags
- Recommended compression skill (for Phase 5 routing)

`six-eyes` Phase 5 uses the primary tag to pick the compression skill; the sub-context tunes its behavior. If primary tag is `LLM`, also signal that `cursed-speech` will need the audited statement plus the downstream task description.

## Connections

- `bluf-shaper`, `scqa-formatter`, `executive-distiller`, `cursed-speech` (binding-vow) — downstream consumers of the audience tag
- `problem-typology` (binding-vow) — runs in parallel; some typologies (adaptive, wicked) suggest specific audience patterns
- `stakes-assessor` (binding-vow) — runs in parallel; high stakes often imply exec audience or public
- `minto-scqa` (binding-vow) — canonical audience-fit decision rules for SCQA variant selection
- `statement-grader` (binding-vow) — uses the audience tag to score the audience-fit axis

## Sources

- Minto, B. (1987, 2003). *The Pyramid Principle*. (Audience-driven structure decisions.)
- See [[minto-scqa]] for the canonical audience → structure mapping.
