# Executive Distiller — Quick Reference


## When to Use This Skill

| Use executive-distiller | Don't use it |
|---|---|
| Output will be a memo, brief, or board document (1–10 pages) | Output is a slack message or single screen — use `bluf-shaper` |
| Reader will skim, then drill down on points that matter to them | Reader will read narratively start-to-finish — use `scqa-formatter` |
| Multiple supporting threads need to be organized hierarchically | Single-thread argument — `scqa-formatter` is enough |
| Audience tag is `exec` AND length budget is medium-to-long | Audience is LLM (use `cursed-speech`), peer (`scqa-formatter`), or self (`scqa-formatter` minimal) |

## Quick Reference

| Test | Question |
|---|---|
| **Mutually Exclusive** | Could a relevant fact reasonably go in two of these buckets? If yes, restructure. |
| **Collectively Exhaustive** | Is there an obvious fact that doesn't fit any bucket? If yes, add one or restructure. |
| **False parallel check** | Are sibling labels structurally parallel (e.g., all noun phrases, all verb phrases)? If not, fix the parallelism. |

## Common Failure Modes

| Failure | Response |
|---|---|
| Level-1 has 6+ subthoughts | Pyramid is too flat at the top — group into 2–4 super-categories first |
| MECE fails repeatedly at same level | Wrong organizing principle; try a different decomposition axis (time vs structure vs importance) |
| Atomic leaves are still 100+ words | Either the leaf isn't atomic (recurse further) or the writing is bloated (call `clarity-engine` cross-domain — neocortex) |
| SCQA introduction's Answer doesn't match the body's top-level | Pyramid is incoherent; the Answer must equal the structure beneath it. Re-do Step 1 or restructure the body |
| Length budget exceeded | Cut from the leaves up — strip atomic detail before cutting structural depth |

## Formula / Pseudocode

```
[TITLE — captures the Answer in 8–12 words]

[OPTIONAL: BLUF block at top, for time-pressured readers who skim only this]

INTRODUCTION (SCQA):
  Situation:    ...
  Complication: ...
  Question:     ...
  Answer:       [governing thought, becomes the body's structure]

BODY:
  1. [Level-1 subthought A]
     1.1 [Level-2 sub-A]
         [paragraph using argument-structure scaffolding]
     1.2 [Level-2 sub-B]
         [...]
  2. [Level-1 subthought B]
     2.1 ...
     2.2 ...
  3. [Level-1 subthought C]
     ...

[OPTIONAL] APPENDICES:
  - Methodology / data sources / dissenting views
```

## Formula / Pseudocode

```
DISTILLATION METADATA
─────────────────────
Pyramid depth:        [N levels]
MECE checks passed:   [list of groupings checked]
MECE issues flagged:  [list, if any]
Argument-structure calls: [N calls, audience: exec]
Length:               [word count]
```
