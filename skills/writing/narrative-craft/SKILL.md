---
name: narrative-craft
description: >
  Direct the narrative-craft subdomain — route scene, structure, pacing, dialogue, POV, and
  sensory detail questions to the right specialist skill. Use when the user has a question about
  how stories and scenes work, wants to improve narrative prose beyond the sentence level, or
  needs to understand why a passage lacks tension, clarity, or immersion.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Glob
---

# Narrative Craft Director — The Story Editor's Eye

The department head for narrative-level prose within the writing domain. Routes questions to the right specialist, defines the learning order, and resolves conflicts when different craft principles pull in different directions.

Narrative craft governs everything above the sentence and below the whole piece: how scenes are built, how time is managed, how characters speak, through whose eyes the reader sees, and how concrete detail creates the illusion of a real world. Where sentence-craft makes individual lines work, narrative-craft makes passages, scenes, and sequences work.

## Routing Logic

| Question Pattern | Route To | Why |
|-----------------|----------|-----|
| Story structure, plot, arc, three-act, beginnings/endings | `narrative-arc` | Whole-piece architecture (linear) |
| Non-linear structure, experimental forms, "what shape should this story be," meander, spiral, fractal | `narrative-geometry` | Alternative shapes beyond the arc |
| Scene construction, turning points, "enter late/leave early" | `scene-craft` | Scene-level architecture |
| Tension, tempo, "too slow," "too fast," compression/expansion | `pacing` | Narrative time management |
| Character speech, subtext, "dialogue feels wooden" | `dialogue` | Dialogue craft |
| POV, narrative distance, "head-hopping," omniscient vs close | `point-of-view` | Perspective mechanics |
| "Show don't tell," sensory detail, vague description | `concrete-detail` | Specificity and implication |
| Interiority, "getting inside the character's head," free indirect discourse, rendering consciousness, "telling not showing emotions" | `character-interiority` | Consciousness rendering |
| "Flat prose," "no energy," "why is this boring," page-turning quality without action, engagement in static scenes | `micro-tension` | Line-by-line emotional charge |
| Autofiction, metafiction, fragmented narrative, genre-bending, experimental forms | `hybrid-forms` | When categories break |
| Writing in a built world — exposition, infodump avoidance, iceberg-style revelation | `world-to-story` | Bridge to worldbuilding |
| Rendering a built region's sensory palette in prose; POV attention bias | `sensory-translation` | Bridge to worldbuilding |
| Characters carrying their culture's vocabulary, idiom, syntax, refusal-to-explain | `cultural-voice` | Bridge to worldbuilding |
| "This scene doesn't work" (vague) | Diagnose first | Read the scene, identify the primary weakness, then route |

### Multi-Skill Questions

Some questions need more than one skill. Load them in this order:

1. `concrete-detail` — is the reader grounded in sensory reality?
2. `character-interiority` — is the reader inside the character's consciousness, not just observing it?
3. `scene-craft` — does the scene turn? Does it have a reason to exist?
4. `dialogue` — if dialogue is present, is it carrying weight?
5. `pacing` — is the narrative time management working?
6. `point-of-view` — is the perspective consistent and serving the story?
7. `narrative-arc` — does this scene serve the whole-piece structure?

This order goes micro to macro: ground the reader first, then inhabit the character, then check the scene's internal logic, then check its role in the larger structure.

## Curriculum Order

1. **Concrete Detail** (foundation) — Before anything else, the reader must be able to see, hear, and feel. Sensory specificity is the bedrock skill.
2. **Character Interiority** (consciousness) — Once you can create vivid sensory reality, learn to filter it through a character's mind. The perception filter, somatic emotion, and free indirect discourse.
3. **Scene Craft** (construction) — Once you can ground the reader in a character's experience, structure those experiences into scenes that turn.
4. **Dialogue** (voice) — Scenes often hinge on what characters say — and don't say. The tension between dialogue and interiority is one of fiction's most powerful tools.
5. **Pacing** (time) — Learn to control narrative tempo: when to expand a moment, when to compress a month. Interiority provides the subjective clock; pacing provides the narrative one.
6. **Point of View** (perspective) — The lens through which everything is filtered. Changes everything about what the reader knows and feels.
7. **Narrative Arc** (architecture) — The whole-piece structure. Most useful after you understand scenes, because arcs are made of scenes.

### Level Progression
- **Foundational**: All seven current skills (concrete-detail, character-interiority, scene-craft, dialogue, pacing, point-of-view, narrative-arc)
- **Intermediate**: (future) subplot management, flashback technique, ensemble POV
- **Advanced**: (future) non-linear structure, unreliable narration, experimental narrative forms

## Conflict Resolution

| Conflict | Resolution | Reason |
|----------|-----------|--------|
| Pacing says "cut this scene" but scene-craft says "it turns a value" | Scene-craft wins | A scene that turns has a reason to exist; fix the pacing within it |
| Dialogue says "add subtext" but concrete-detail says "be specific" | Both apply, different layers | Subtext is about what characters mean; specificity is about what readers see. Both coexist. |
| Narrative-arc says "this scene doesn't serve the plot" but it reveals character | Keep the scene | Character revelation is structural work. Arc frameworks that ignore character are incomplete. |
| Point-of-view says "stay in close third" but pacing needs a time jump | POV yields temporarily | Use a section break, shift to summary distance, then return to close. Distance serves pacing here. |
| Three-act structure says "midpoint reversal needed" but Truby says "organic growth from character need" | Present both | These are different frameworks, not conflicting facts. Let the user choose. |

**General rule**: When frameworks disagree (three-act vs. Truby vs. kishotenketsu), **present them as lenses with different strengths**, not as competing truths. When principles disagree (pacing vs. character), **character and specificity win** — readers forgive slow pacing if they're grounded in vivid, particular reality.

## Scope Boundaries

**This director handles**: Scene construction, story structure, pacing, dialogue, point of view, and sensory detail — everything between the sentence and the whole piece.

**Escalate to the orchestrator when**:
- The problem is sentence-level (rhythm, diction, syntax) — that's sentence-craft territory
- The problem is argumentative or persuasive — that's rhetoric territory
- The user needs a full editing pass — that's revision-craft territory

## Cross-Domain Connections

**Worldbuilding bridge cluster (siblings within this director):** `world-to-story`, `sensory-translation`, `cultural-voice`. Together these three skills cover the full handoff from a built world to prose written inside it. Load them as a set when the user is writing fiction in an invented setting.

- **Worldbuilding/narrative-pacing**: Worldbuilding has its own pacing system — revelation spirals and tension archetypes (Cassandra, Randy, Penelope) that control how world-information reaches the reader. When writing in a built world, narrative-craft pacing must harmonize with the worldbuilding revelation architecture.
- **Worldbuilding/lore-writer**: Lore-writer produces in-universe artifacts (letters, myths, reports) using 7 voice registers. These artifacts ARE prose — scene-craft and dialogue principles apply within the artifact's voice constraints.
- **Worldbuilding/character-belief-tracker**: What a character knows (their belief layer in the revelation architecture) determines their POV reliability and narrative distance. Character beliefs constrain point-of-view decisions.
- **Worldbuilding/sensory-worldbuilding**: Upstream input to `sensory-translation`. The five-channel palette is built there; this director translates it to prose.
- **Worldbuilding/cultures-societies + naming-system**: Upstream inputs to `cultural-voice`. Culture is built there; this director translates the seven-pillar profile into voice on the page.
- The user needs prose *drafted*, not just diagnosed — the orchestrator routes to action skills
