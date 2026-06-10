# Audience Classifier — Quick Reference


## The Five Audience Tags

| Tag | Who | Channel typical | Time budget | Routes to |
|---|---|---|---|---|
| **LLM** | A language model that will execute the resulting prompt | API call, in-context | Model-consumed (~10K tokens fine) | `cursed-speech` |
| **Exec** | Decision-maker, time-pressured, trust intact | Slack, email, brief, deck | 30 sec – 5 min | `bluf-shaper` (short) or `executive-distiller` (memo) |
| **Peer** | Collaborator with parallel context | Doc, email, meeting | 2–15 min | `scqa-formatter` |
| **Self** | The user thinking through their own problem | Note, scratch buffer | Whatever's needed | `scqa-formatter` (skip Q step) or Polya restatement |
| **Public** | Mixed-audience reader who may be skeptical | Essay, post, talk, public memo | 5 min – 30 min | `executive-distiller` (with Concern-priming) or `scqa-formatter` (Concern-priming variant) |

## Quick Reference

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

## Quick Reference

| Sub-context | Values | Used by |
|---|---|---|
| **Time budget** | ≤30s / 30s–5min / 5–30min / open | `bluf-shaper` vs `executive-distiller` choice |
| **Skepticism level** | trusting / neutral / skeptical | SCQA variant selection (standard vs Concern-priming) |
| **Channel** | slack / email / doc / deck / verbal / API | Length and formatting bounds |
| **Familiarity** | high context / partial context / cold | Background-section depth |

## Edge Cases

| Pattern | Handling |
|---|---|
| Statement specifies two audiences explicitly (e.g., "for the CEO and the LLM that will analyze it") | Run compression twice. Tag both audiences; orchestrator's deep mode will produce both shapes. |
| Statement has no explicit audience signals | Default to `self` (the user is thinking, no recipient specified) with low confidence. Recommend the user specify if a different audience is intended. |
| Audience is a class of person, not an individual ("for engineering managers") | Treat as `peer` (collective collaborator). Skepticism level depends on the topic. |
| Audience is an LLM but the user wrote it as if for a human | Tag `LLM` but flag the prose-shaped framing — `cursed-speech` will need to restructure for the canonical order. |
| Audience is "everyone" or "the world" | Tag `public`; flag low confidence; recommend narrowing scope. Public-as-mass-audience usually conceals a more specific intended reader. |

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
