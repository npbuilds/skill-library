---
name: prose-editor
description: >
  Revise existing prose using the professional editing-pass hierarchy — structural, then line,
  then copy. Use when the user has a draft that needs improvement, wants a specific editing pass,
  or asks to "make this better." Diagnoses before treating.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Write Glob
---

# Prose Editor — The Three Passes

Edit existing prose using the professional editing hierarchy. The cardinal rule: **work from macro to micro.** Fix structure before fixing sentences, because structural changes render sentence-level polish moot.

## How to Run

### Input

The user provides:
1. **Text** — the prose to edit (inline, file path, or clipboard)
2. **Pass type** (optional) — which editing pass to run:
   - `structural` — organization, arc, scene logic, sections
   - `line` — rhythm, diction, syntax, voice consistency
   - `copy` — grammar, punctuation, spelling, consistency
   - `full` — all three in sequence (default if unspecified)
3. **Focus** (optional) — a specific concern ("it's too wordy," "the dialogue feels off," "tighten this")
4. **Constraints** — word count targets, voice register to preserve, anti-patterns

### Steps

**Structural Pass** (loads: `narrative-arc`, `scene-craft`, `argument-structure` as appropriate)
1. Read the full text. Identify the form (fiction, essay, nonfiction).
2. Assess the macro structure: Is it organized effectively? Are sections in the right order? Are there missing or redundant sections?
3. For fiction: Does every scene turn a value? Is the arc working? Is there a sagging middle?
4. For essays: Is the argument structured? Where is the volta/turn? Are counterarguments addressed?
5. Report structural findings. Suggest cuts, reorders, or additions. **Do not line-edit during this pass.**

**Line Pass** (loads: `prose-rhythm`, `diction`, `syntax-patterns`, `concrete-detail`)
1. Read paragraph by paragraph. Apply the diagnostic protocol from `sentence-craft`:
   - Sentence length map — is there rhythmic variety?
   - First-word audit — is there opener variety?
   - Diction check — any vague words, dead metaphors, register breaks, filler?
   - Syntax check — any structural monotony?
2. Check voice consistency. Flag register breaks.
3. Check concrete detail. Flag passages that tell when they should show.
4. Edit the prose. Show changes with brief rationale.

**Copy Pass**
1. Grammar, punctuation, spelling, consistency.
2. Intentional style choices (fragments, comma splices, non-standard punctuation) are preserved — route to the line pass if uncertain.

### Output

Edited prose with change rationale. For the structural pass: a diagnostic report with recommendations rather than direct edits.

## Editing Principles

1. **Diagnose before treating.** Read the full text before making any changes. Understand what the writer is trying to do before deciding what they should change.
2. **Macro before micro.** Never start a line pass on structurally broken prose.
3. **Preserve voice.** The editor's job is to make the writer sound more like themselves, not to impose a different voice.
4. **Explain the why.** Every significant change should have a brief rationale. This builds the writer's craft intuition.
5. **Kill your darlings — but they're the writer's darlings, not yours.** Flag passages that don't serve the piece, but let the writer decide whether to cut.
6. **Style choices are not errors.** Fragments, one-sentence paragraphs, non-standard punctuation, register breaks — these may be intentional. Ask before "fixing" them.

## Common Diagnoses

| Symptom | Likely Problem | Pass | Treatment |
|---------|---------------|------|-----------|
| "It's too long" | Redundancy, over-description, scenes that don't turn | Structural + Line | Cut redundant sections; tighten diction |
| "It doesn't flow" | Rhythm problems, monotonous syntax | Line | Apply rhythm and syntax diagnostics |
| "The dialogue feels off" | On-the-nose dialogue, undifferentiated voices | Line | Route to `dialogue` knowledge skill |
| "It's boring in the middle" | Sagging middle — unclear goals in Act Two | Structural | Give the protagonist a concrete problem |
| "It feels vague" | Abstract diction, lack of concrete detail | Line | Apply diction and concrete-detail diagnostics |
| "The argument doesn't land" | Missing warrant, weak structure | Structural | Route to `argument-structure` |

## Scope Boundaries

**This skill handles**: Editing and revising existing prose — structural assessment, line editing, and copy editing.

**This skill does NOT**:
- Draft new prose (that's `prose-writer`)
- Analyze style without editing (that's `style-analyzer`)
- Make creative decisions for the writer (it diagnoses and suggests; the writer decides)
