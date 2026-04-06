# Prose Orchestrator — Quick Reference


## Quick Reference

| Subdomain | Director | Activates When |
|-----------|----------|---------------|
| Sentence Craft | `skills/writing/sentence-craft/SKILL.md` | Rhythm, word choice, sentence structure, line-level polish |
| Narrative Craft | `skills/writing/narrative-craft/SKILL.md` | Scene construction, story arc, pacing, dialogue, POV, concrete detail |
| Rhetoric | `skills/writing/rhetoric/SKILL.md` | Argument structure, persuasion, rhetorical devices, essay forms |
| Revision Craft | `skills/writing/revision-craft/SKILL.md` | Editing passes, style analysis, tightening |

## Quick Reference

| Intent | Primary Route | Supporting Route |
|--------|--------------|-----------------|
| `DRAFT` | Form-appropriate director(s) + `prose-writer` action skill | Sentence Craft for polish pass |
| `DRAFT` with voice blend | `style-mixer` → Voice Card → `prose-writer` | Style DNA for author profiles |
| `REVISE` | Revision Craft director → `prose-editor` | Sentence Craft or Narrative Craft as needed |
| `MUTATE` | `style-mutator` (warp existing prose toward a target voice) | Style DNA for dimension definitions |
| `DESIGN VOICE` | `style-mixer` → outputs a reusable Voice Card | Style DNA for author profiles |
| `ANALYZE` | Revision Craft → `style-analyzer` | Style DNA for 14-dimension mapping |
| `LEARN` | Route to the specific subdomain director | Director handles curriculum order |

## Quick Reference

| Agent | File | Model | Use For |
|-------|------|-------|---------|
| Prose Drafting Agent | (future) `agents/prose-drafting-agent.md` | sonnet | Drafting new prose from a brief |
| Line Edit Agent | (future) `agents/line-edit-agent.md` | sonnet | Line-level revision of existing prose |

## Quick Reference

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
