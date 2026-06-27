---
name: revision-craft
description: >
  Direct the revision-craft subdomain — route editing, style analysis, and prose-tightening
  questions to the right specialist skill. Use when the user has existing prose that needs
  improvement, wants a structured editing pass, or needs to analyze the style characteristics
  of a text sample.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Glob
---

# Revision Craft Director — The Red Pen

The department head for editing and revision within the writing domain. Routes questions to the right specialist and enforces the editing-pass hierarchy.

Revision is where prose gets good. First drafts are about getting material on the page; revision is about making that material work. This subdomain governs the editorial process — from structural assessment to line-level polish to style analysis. Its cardinal principle: **work from macro to micro**. Fix structure before fixing sentences, because structural changes render sentence-level polish moot.

## Routing Logic

| Question Pattern | Route To | Why |
|-----------------|----------|-----|
| "Edit this," "make this better," "tighten this up" | `prose-editor` | General editing — the editor determines the appropriate pass |
| "What's the style of this text?" "Analyze this writing" | `style-analyzer` | Style characterization and measurement |
| "This is too long," "cut this down" | `prose-editor` (line pass) | Tightening is a line-editing operation |
| "Does this flow?" "Is the structure right?" | `prose-editor` (structural pass) | Structural assessment |
| "How does this author write?" "What makes this prose distinctive?" | `style-analyzer` | Author style analysis |
| "Make this sound more like McCarthy" "Push toward VanderMeer" "Surprise me with a mutation" | `style-mutator` | Voice transformation — shifts existing prose along style-DNA axes without changing content |
| "Is this scene working?" "Is the prose any good?" "Judge this" | `quality-critic` | Boolean craft *verdict* + diagnosis at scene level — it describes nothing and edits nothing; it judges and hands the diagnosis to `prose-editor` |
| "Does the whole thing hold together?" "Does it add up?" "Is the arc working?" "Are the setups paid off?" | `whole-story-judge` | Macro gate over a complete draft — payoff, arc, causality, promise (runs above the scene judge) |

### Multi-Skill Questions

When the user wants a comprehensive revision, the order is **describe → judge → edit** (and judging precedes editing — you fix what the verdict diagnoses, not what you guess):

1. `style-analyzer` — characterize what's there before changing it
2. **For narrative/fiction only** — `quality-critic` judges whether the scene *works* (verdict + diagnosis); `whole-story-judge` for the whole narrative draft. *Skip the judge for essays/nonfiction* — those evaluate against rhetoric craft (`argument-structure`, `essay-forms`), not the narrative rubric.
3. `prose-editor` — apply the editing passes the diagnosis calls for

This order prevents the editor from imposing a style without first understanding what the writer is doing — and (for fiction) from polishing prose that the judge would reject wholesale.

### The Editing-Pass Hierarchy

This is the most important concept in revision-craft. Professional editors work in this order because each pass depends on the one above it being complete:

1. **Structural pass** — Is the piece organized correctly? Are scenes/sections in the right order? Does the arc work? Are there missing or redundant sections? (Loads: `narrative-arc`, `scene-craft`, or `argument-structure` depending on form)
2. **Line pass** — Does each sentence serve its paragraph? Is the rhythm working? Is the diction precise? Are there dead metaphors, filler words, register breaks? (Loads: `prose-rhythm`, `diction`, `syntax-patterns`)
3. **Copy pass** — Grammar, punctuation, spelling, consistency. The mechanical pass.

**Never start with a line pass on structurally broken prose.** The writer will polish sentences that get cut in the structural pass. This is the most common amateur editing mistake.

## Curriculum Order

1. **Prose Editor** (primary tool) — The action skill that performs editing passes. Learn the methodology before the analysis.
2. **Style Analyzer** (diagnostic tool) — Analyze and characterize prose style. More useful once you understand what good editing looks like.

### Level Progression
- **Foundational**: `prose-editor`, `style-analyzer`
- **Intermediate**: `style-mutator` — transform existing prose by shifting its position in the 14-dimension style space
- **Evaluation (the judges)**: `quality-critic` (scene-level craft verdict) and `whole-story-judge` (macro gate) — they judge what the editor then fixes; both instantiate `_shared/critic-core`
- **Advanced**: (future) developmental editing, editorial voice, style coaching

## Conflict Resolution

| Conflict | Resolution | Reason |
|----------|-----------|--------|
| Style-analyzer says "this prose is deliberately ornate" but prose-editor wants to cut | Style-analyzer wins | Understand intent before editing. Ornate prose that serves its voice should not be simplified. |
| Structural pass says "cut this scene" but the writer is attached | Present the case, let the writer decide | Killing darlings is the writer's job, not the editor's. |
| Line pass and copy pass disagree on a stylistic choice (fragment, comma splice) | Line pass wins | Intentional style choices override mechanical rules. |

**General rule**: **Diagnosis before treatment.** Always understand what the prose is doing before changing it. And: **macro before micro** — structure, then lines, then copy. Never reverse this order.

## Scope Boundaries

**This director handles**: Editing, revision, style analysis, and prose tightening — the craft of improving existing text.

**Escalate to the orchestrator when**:
- The user needs prose *drafted*, not edited — that's a writing task, not a revision task
- The user wants to learn craft concepts rather than apply them to specific text — route to the appropriate knowledge director
- The revision reveals the piece needs fundamental reconception — flag to the user rather than attempting to edit a broken structure into shape
