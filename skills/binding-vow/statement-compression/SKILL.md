---
name: statement-compression
description: >
  Route an audited problem statement to the right compression format by audience — BLUF, Minto
  pyramid, SCQA, or Claude-prompt structure — grounded in the Minto reference. Activate at
  six-eyes Phase 5 (Compress) once a statement has passed audit and needs to be shaped for a
  specific reader. This director owns the "say it in the form this audience needs" question.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read
---

# Statement Compression — Director

A correct statement in the wrong shape still fails. This director realizes six-eyes' Phase 5
(Compress): it routes a clean, audited statement to the compression format that fits its
audience tag. Compression is force — giving up scope to gain precision — so the audience tag
from `problem-diagnosis` is the controlling input here.

## Routing Table

| Audience / need | Child skill | Output |
|---|---|---|
| exec — fastest possible | `bluf-shaper` | Bottom-Line-Up-Front: one-sentence answer, minimal background, priority-ordered discussion |
| exec / public — substantial doc | `executive-distiller` | Full recursive Minto Pyramid (calls writing/rhetoric/argument-structure) |
| peer / self — narrative intro | `scqa-formatter` | Situation / Complication / Question / Answer |
| LLM — prompt | `cursed-speech` | Anthropic canonical order: role → context → data → examples → numbered instructions → output format → self-check |
| (reference) | `minto-scqa` | Reference: Minto Pyramid, SCQA, MECE, BLUF |

## Routing Logic

1. Read the audience tag from the diagnosis profile. It maps directly to the format above.
2. For LLM audiences, `cursed-speech` additionally recommends downstream skills the formulated
   prompt should invoke — surface those to the user.
3. Pull `minto-scqa` whenever a writer needs the *why* behind the format choice.
4. Hand the compressed statement back to `six-eyes` for the final `statement-grader` pass.

## Scope Boundaries

- **In scope:** shaping an already-audited statement for a target audience.
- **Out of scope:** auditing the statement's logic (→ `statement-audit`), choosing the audience
  (→ `problem-diagnosis`). Compress *after* audit, never before — compressing a flawed statement
  just hides the flaw.
