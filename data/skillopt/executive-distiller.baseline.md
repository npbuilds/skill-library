# Executive Distiller — The Full Pyramid Principle

The full implementation of Minto's Pyramid Principle: SCQA introduction at the top, a single governing thought, recursive 2–5-way decomposition under it, MECE-validated at every level. The output is a structured document that the reader can skim top-down or read in full and get the same answer.

For the canonical specification, see [[minto-scqa]]. For the introduction-only variant, see `scqa-formatter`. For short-form output, see `bluf-shaper`.

## When to Use This Skill

| Use executive-distiller | Don't use it |
|---|---|
| Output will be a memo, brief, or board document (1–10 pages) | Output is a slack message or single screen — use `bluf-shaper` |
| Reader will skim, then drill down on points that matter to them | Reader will read narratively start-to-finish — use `scqa-formatter` |
| Multiple supporting threads need to be organized hierarchically | Single-thread argument — `scqa-formatter` is enough |
| Audience tag is `exec` AND length budget is medium-to-long | Audience is LLM (use `cursed-speech`), peer (`scqa-formatter`), or self (`scqa-formatter` minimal) |

## Process

### Step 1 — Build the SCQA introduction

Call `scqa-formatter` for the introduction. Receive: the four-component intro (S/C/Q/A). The Answer becomes the top of your pyramid.

### Step 2 — Generate level-1 subthoughts under the Answer

Decompose the Answer into 2–5 supporting thoughts. Each subthought must:

1. **Summarize what's grouped under it** (Minto Rule 1: ideas at any level summarize the ideas grouped below them)
2. **Be the same kind of idea as its siblings** (Minto Rule 2: sibling consistency)
3. **Be in logical order with siblings** (Minto Rule 3: time, structure, or importance)

Apply the MECE check (see Step 4).

### Step 3 — Recurse for each subthought

For each level-1 subthought, decide: does this need its own subthoughts, or is it atomic enough? If it needs subthoughts, repeat Step 2 at level 2. Continue until atomic.

Practical depth limit: ≤4 levels. If you find yourself going deeper, the structure has the wrong granularity; reconsider the level-1 decomposition.

### Step 4 — MECE check at every grouping

For each grouping (the Answer's children, then each subthought's children, etc.), apply:

| Test | Question |
|---|---|
| **Mutually Exclusive** | Could a relevant fact reasonably go in two of these buckets? If yes, restructure. |
| **Collectively Exhaustive** | Is there an obvious fact that doesn't fit any bucket? If yes, add one or restructure. |
| **False parallel check** | Are sibling labels structurally parallel (e.g., all noun phrases, all verb phrases)? If not, fix the parallelism. |

If MECE fails at any level, the pyramid will leak. Fix before continuing recursion.

### Step 5 — Sentence-level scaffolding

For each leaf node (atomic subthought), call `argument-structure` (cross-domain — writing/rhetoric) with the audience tag. Receive: appropriate sentence-level structure (Toulmin claim+warrant+grounds, Rogerian common-ground, classical introduction-body-conclusion, or volta-shaped).

This is what makes the leaves *land* — without sentence-level scaffolding, even a perfect pyramid reads as bullet-point soup.

### Step 6 — Assemble the document

Standard executive memo template:

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

## Output Format

The output is the assembled memo (above). Plus a metadata block for downstream skills:

```
DISTILLATION METADATA
─────────────────────
Pyramid depth:        [N levels]
MECE checks passed:   [list of groupings checked]
MECE issues flagged:  [list, if any]
Argument-structure calls: [N calls, audience: exec]
Length:               [word count]
```

## Common Failure Modes

| Failure | Response |
|---|---|
| Level-1 has 6+ subthoughts | Pyramid is too flat at the top — group into 2–4 super-categories first |
| MECE fails repeatedly at same level | Wrong organizing principle; try a different decomposition axis (time vs structure vs importance) |
| Atomic leaves are still 100+ words | Either the leaf isn't atomic (recurse further) or the writing is bloated (call `clarity-engine` cross-domain — neocortex) |
| SCQA introduction's Answer doesn't match the body's top-level | Pyramid is incoherent; the Answer must equal the structure beneath it. Re-do Step 1 or restructure the body |
| Length budget exceeded | Cut from the leaves up — strip atomic detail before cutting structural depth |

## Output Contract for `six-eyes`

Called from Phase 5 with audience tag `exec` and length budget medium-to-long:
- Returns the full assembled memo
- Plus the metadata block (depth, MECE results, length)
- If MECE issues flagged, route back to `statement-grader` for re-scoring on the specificity and root-vs-symptom axes — MECE failures often indicate upstream framing failures

## Scope Boundaries

- **executive-distiller handles:** building the recursive pyramid, applying MECE at each level, calling `argument-structure` for sentence-level scaffolding, assembling the memo template.
- **executive-distiller does NOT:** judge whether the executive should approve the recommendation (that's the reader's job). Does not write the appendices in detail (they're scoped placeholders).

## Connections

- `minto-scqa` (binding-vow) — canonical reference for the Pyramid Principle and MECE
- `scqa-formatter` (binding-vow) — provides the SCQA introduction (Step 1)
- `bluf-shaper` (binding-vow) — sibling for short-form variant
- `argument-structure` (writing/rhetoric) — sentence-level scaffolding (Step 5; cross-domain call)
- `clarity-engine` (neocortex) — escalation path for bloated leaves
- `claim-decomposer` (research) — useful for the level-1 decomposition step on complex topics

## Sources

- Minto, B. (1987, 2003). *The Pyramid Principle*. (Full canonical specification of the Pyramid + MECE rules.)
- See [[minto-scqa]] for the BLUF/SCQA/Pyramid comparator and the MECE failure-mode catalog.
