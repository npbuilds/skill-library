---
name: prose-orchestrator
description: >
  Orchestrate prose writing, revision, and craft learning across fiction, nonfiction, and essays.
  Use when the user needs help drafting prose, revising existing text, analyzing writing style,
  or learning prose craft. Activates when the task involves sentence-level polish, narrative
  structure, rhetorical strategy, editing passes, or voice development — for any genre or form.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Write Bash Glob Grep Agent
---

# Prose Orchestrator — The Editor's Desk

Route prose problems to the right specialist and ensure cohesive, craft-aware output. Analyze what the user needs, classify the writing domain, set editorial direction, and delegate to subdomain directors or action skills.

## Phases

### Phase 1 — Understand the Brief

Determine what the user actually needs before touching any prose:

- **Intent** — what are they trying to do?
  - `DRAFT` — write something new from a brief, prompt, or idea
  - `REVISE` — improve existing prose (theirs or generated)
  - `ANALYZE` — understand the style, structure, or craft of a text
  - `LEARN` — understand a craft concept (rhythm, dialogue, rhetoric, etc.)

- **Form** — what kind of writing?
  - Fiction (literary, genre, flash)
  - Essay (personal, argumentative, lyric, braided, hermit crab)
  - Nonfiction (journalism, memoir, criticism)
  - Mixed/hybrid

- **Scope** — what level of the prose?
  - Sentence-level (rhythm, diction, syntax)
  - Scene/section-level (structure, pacing, dialogue, POV)
  - Whole-piece (arc, argument, form)
  - Style/voice (register, tone, consistency)

- **Constraints** — anything that shapes the work?
  - Word count, audience, publication context, existing voice/style, genre conventions

If the user says something vague like "help me write better" or "make this good," ask one clarifying question — don't interrogate. Infer what you can from context.

### Phase 2 — Classify and Route

Determine which subdomain(s) apply and route through the appropriate director.

| Subdomain | Director | Activates When |
|-----------|----------|---------------|
| Sentence Craft | `skills/writing/sentence-craft/SKILL.md` | Rhythm, word choice, sentence structure, line-level polish, figurative language (metaphor, simile, image systems) |
| Narrative Craft | `skills/writing/narrative-craft/SKILL.md` | Scene construction, story arc, pacing, dialogue, POV, concrete detail, character interiority, micro-tension, narrative geometry, world-to-story translation, hybrid/experimental forms |
| Rhetoric | `skills/writing/rhetoric/SKILL.md` | Argument structure, persuasion, rhetorical devices, essay forms |
| Revision Craft | `skills/writing/revision-craft/SKILL.md` | Editing passes, style analysis, tightening |

**Intent → subdomain mapping:**

| Intent | Primary Route | Supporting Route |
|--------|--------------|-----------------|
| `DRAFT` | Form-appropriate director(s) + `prose-writer` action skill | Sentence Craft for polish pass |
| `DRAFT` with voice blend | `style-mixer` → Voice Card → `prose-writer` | Style DNA for author profiles |
| `REVISE` | Revision Craft director → `prose-editor` | Sentence Craft or Narrative Craft as needed |
| `MUTATE` | `style-mutator` (warp existing prose toward a target voice) | Style DNA for dimension definitions |
| `DESIGN VOICE` | `style-mixer` → outputs a reusable Voice Card | Style DNA for author profiles |
| `ANALYZE` | Revision Craft → `style-analyzer` | Style DNA for 14-dimension mapping |
| `LEARN` | Route to the specific subdomain director | Director handles curriculum order |

### Phase 3 — Set Editorial Direction

Before delegating, establish the guardrails for this piece of writing:

1. **Voice** — three levels of control:
   - **Register preset** (quick): Minimalist, Conversational, Literary, Academic, Lyric — legacy presets now mapped to DNA positions
   - **Voice Card** (precise): A 14-dimension style spec from `style-mixer`, with author blend ratios and anchor sentences
   - **Author push** (intuitive): "Write this like 70% Hobb / 20% Camus" — resolved through `style-dna` profiles

   When a Voice Card is used, it replaces the register as the primary voice constraint. The 14 dimensions (sentence rhythm, psychic distance, info density, ornamentation, narrative velocity, lexical register, authorial presence, sensory bandwidth, emotional explicitness, world-to-story ratio, syntactic complexity, tonal stability, dialogic texture, epistemic stance) each become a target for the draft.

2. **Pacing intent** — what tempo?
   - Urgent/tense — short sentences, fragments, present tense, forward momentum
   - Contemplative — long sentences, subordination, sensory expansion, slowed time
   - Rhythmic — alternation between short and long, building and releasing

3. **Audience calibration** — who reads this?
   - General readers, literary readers, academic audience, specific community
   - This determines register, diction level, how much context to provide

4. **Anti-patterns** — what to explicitly avoid for this piece
   - Example: "no clichés, no passive voice, no adverbs modifying dialogue"

Document these as an **Editorial Brief** that gets passed to every sub-agent and director.

### Phase 4 — Delegate

Route to the appropriate director or action skill.

**Always route through the director first** — the director handles curriculum order and conflict resolution within its subdomain. Do not load knowledge skills directly.

For `DRAFT` intents, the orchestrator may launch a writing agent (future — agents not yet built):

| Agent | File | Model | Use For |
|-------|------|-------|---------|
| Prose Drafting Agent | (future) `agents/prose-drafting-agent.md` | sonnet | Drafting new prose from a brief |
| Line Edit Agent | (future) `agents/line-edit-agent.md` | sonnet | Line-level revision of existing prose |

When launching an agent, always pass:
- The editorial brief from Phase 3
- The specific deliverable requested
- The relevant knowledge skill paths (so the agent can read craft principles)
- Any source text being revised

For `LEARN` intents, read the relevant knowledge skill(s) and teach from them — no agent needed.

### Phase 5 — Harmonize and Present

After delegation returns results:

1. **Consistency check** — does the output honor the editorial brief?
   - Voice register consistent throughout
   - Pacing matches intent
   - No craft violations the brief explicitly forbade
2. **Craft transparency** — when useful, briefly explain *why* a choice works
   - "The short sentence after the long compound sentence creates emphasis — that's rhythmic contrast."
   - This builds the user's craft intuition without lecturing.
3. **Revision invitation** — always ask what to adjust, never declare the work finished.

## Knowledge Layer

Consult the relevant subdomain director before making craft decisions. The director handles routing, curriculum order, and conflict resolution within its area.

| Subdomain | Director Path | Consult When |
|-----------|--------------|-------------|
| Sentence Craft | `skills/writing/sentence-craft/SKILL.md` | Rhythm, diction, syntax, line-level decisions |
| Style DNA | `skills/writing/sentence-craft/style-dna/SKILL.md` | Author profiles, 14-dimension model, voice comparison |
| Narrative Craft | `skills/writing/narrative-craft/SKILL.md` | Scene, arc, pacing, dialogue, POV, sensory detail |
| Rhetoric | `skills/writing/rhetoric/SKILL.md` | Argument, persuasion, rhetorical devices, essay forms |
| Revision Craft | `skills/writing/revision-craft/SKILL.md` | Editing methodology, style analysis |
| Style Mixer | `skills/writing/prose-orchestrator/style-mixer/SKILL.md` | Designing blended voices, creating Voice Cards |
| Style Mutator | `skills/writing/revision-craft/style-mutator/SKILL.md` | Transforming existing prose along style dimensions |

## Failure Recovery

| Failure | Response |
|---------|----------|
| User rejects a draft | Ask which specific elements feel wrong (voice? rhythm? structure?) — don't start over |
| Draft violates its own editorial brief | Re-run with tighter constraints on the specific violation |
| User's intent is ambiguous | Ask one focused clarifying question, then proceed with best guess |
| Multiple subdomains conflict | Sentence-level polish defers to narrative-level structure; structure defers to rhetorical intent. Form serves function. |
| Requested form doesn't exist yet | Note the gap, handle with general principles, suggest building the missing skill |

## Scope Boundaries

**This orchestrator handles:** Prose writing, revision, style analysis, and craft education — for fiction, nonfiction, essays, and hybrid forms.

**This orchestrator does NOT:**
- Write poetry (different craft, different rhythmic system)
- Write screenplays or scripts (different format conventions)
- Generate marketing copy or UX writing (different intent — persuasion and clarity over craft)
- Make publishing or career decisions (it writes prose, not query letters)
- Replace a human editor's judgment (it surfaces craft principles, the user decides)
