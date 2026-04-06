---
name: style-mutator
description: >
  Transform existing prose by pushing it along specific style-DNA axes. Use when the user has
  a passage and wants to see what happens when it's warped toward a different author, dimension,
  or Voice Card. The mutator is experimental and discovery-oriented — less controlled than the
  mixer, more surprising. Works on any source prose: user drafts, prose-writer output, or passages
  for study.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Write Glob
---

# Style Mutator — The Warp Engine

Take existing prose and push it somewhere it hasn't been. The mutator is the experimental counterpart to the mixer — where the mixer designs voices deliberately, the mutator *discovers* them by warping what already exists.

## How to Run

### Input

The user provides:

1. **The passage** — existing prose to transform (their own draft, a prose-writer output, or a passage they want to experiment with)
2. **The mutation direction** — one of:
   - **Author push**: "Push this toward McCarthy" — shift the passage toward an author's DNA profile
   - **Dimension push**: "More syncopated rhythm, less emotional explicitness" — shift specific dimensions
   - **Voice Card push**: "Mutate this toward [Voice Card name]" — shift toward a designed blend
   - **Wild mutation**: "Surprise me" — the mutator chooses a mutation that it thinks would be interesting based on the passage's current position

### Steps

1. **Analyze the source**: Read the passage and estimate its current position on the 14-dimension scale. This doesn't need to be precise — a rough map of where it currently sits is enough to determine which dimensions to shift.

2. **Determine the delta**: Compare the source position to the mutation target. The interesting mutations are where the *gap is largest* — those are the dimensions where the transformation will be most audible.

   For author pushes, focus on the target author's *signature dimensions* (their extreme scores), not their mid-range dimensions. "Push toward McCarthy" means:
   - Rhythm → 5 (syncopated)
   - Emotional explicitness → 1 (submerged)
   - Tonal stability → 1 (monotonal/grave)
   - Sensory bandwidth → 4.5 (high, external)
   - Syntactic complexity → 2 (paratactic chains)

   It does NOT mean: adopt McCarthy's mid-range psychic distance or his mid-range narrative velocity. Those aren't what make him sound like McCarthy.

3. **Apply the mutation**: Rewrite the passage, shifting it along the identified dimensions. Preserve the *content* (what happens, what is said, what is described) while transforming the *voice* (how it's rendered).

   **Mutation intensity levels**:
   - **Nudge** (default): Shift 1-2 points on the target dimensions. The passage should still be recognizably itself but with a new coloring.
   - **Push**: Shift 2-3 points. The passage is audibly different. The original voice is still faintly visible.
   - **Shove**: Shift 3+ points. The passage is transformed. The original voice is gone; the new voice has taken over.
   - **Collision**: Push toward an author who is maximally different from the source on most dimensions. The result will be strange and may not work — but when it does, it produces the most interesting discoveries.

4. **Present the result**: Show the mutated passage alongside a brief mutation report:
   - Which dimensions were shifted and by how much
   - What changed in the prose and why
   - What was lost and what was gained
   - Suggestions for further mutation or stabilization

### Output

The mutated passage plus a mutation report. Optionally, if the user likes the result, generate a Voice Card that captures the mutated voice for future use.

## Mutation Techniques by Dimension

When shifting a specific dimension, these are the concrete prose transformations to apply:

### Sentence Rhythm (toward syncopated)
- Vary sentence length dramatically — follow a 40-word sentence with a 4-word one
- Introduce fragments after extended builds
- Let the short sentence carry the weight

### Sentence Rhythm (toward metronomic)
- Normalize sentence lengths to 12-20 words
- Remove fragments
- Smooth the rhythm into a steady, workmanlike beat

### Psychic Distance (toward microscopic)
- Replace external description with internal sensation
- Use free indirect discourse — the character's vocabulary in the narrator's grammar
- Sensory detail becomes physical/proprioceptive, not just visual
- Remove all observations the character wouldn't make

### Psychic Distance (toward telescopic)
- Replace internal sensation with external observation
- Introduce narrator commentary or historical context
- Allow observations the character couldn't make (wider knowledge)
- Summarize emotional states rather than rendering them

### Information Density (toward dense)
- Layer meaning — each sentence should carry factual, metaphorical, and tonal content
- Add allusion, implication, and subtext
- Compress — say more in fewer words

### Information Density (toward sparse)
- One idea per sentence
- Let meaning live in the white space between statements
- Remove subtext — the surface is the only level

### Ornamentation (toward baroque)
- Introduce figurative language — metaphor, simile, extended imagery
- Let descriptions become elaborate
- Use unusual word combinations and synesthetic detail

### Ornamentation (toward austere)
- Strip figurative language to only the essential
- Replace metaphor with plain statement
- Trust concrete nouns and active verbs to do the work

### Narrative Velocity (toward dilated)
- Expand moments — more sensory detail, more internal reaction
- Let conversations play out in real time
- Add the beats between beats

### Narrative Velocity (toward compressed)
- Summarize what can be summarized
- Skip transitions — jump from significant moment to significant moment
- Cover more time in fewer words

### Lexical Register (toward elevated)
- Replace common words with precise, formal alternatives
- Introduce archaic or literary constructions
- Let the grammar become more elaborate

### Lexical Register (toward demotic)
- Replace formal vocabulary with plain alternatives
- Introduce contractions and conversational rhythms
- Let the prose sound like someone talking

### Authorial Presence (toward performative)
- Introduce narrator opinion, commentary, or asides
- Allow digressions
- Let the narrator address the reader or comment on their own storytelling

### Authorial Presence (toward invisible)
- Remove all narrator commentary
- Let events speak for themselves
- The narrator should be a clear window, not a personality

### Sensory Bandwidth (toward somatic)
- Add non-visual senses — smell, texture, proprioception, temperature
- Ground abstract ideas in physical sensation
- Let the body respond to events before the mind processes them

### Sensory Bandwidth (toward conceptual)
- Replace sensory detail with analytical observation
- Let characters think about events rather than feel them physically
- Prioritize ideas over textures

### Emotional Explicitness (toward surfaced)
- Name the emotions
- Let characters reflect on what they feel
- Give internal states full sentences

### Emotional Explicitness (toward submerged)
- Remove emotion words — replace "she felt grief" with the objective correlative
- Let the reader infer from action, image, and omission
- Trust the situation to carry the feeling

### Syntactic Complexity (toward hypotactic)
- Nest clauses — qualifications inside qualifications
- Use subordinating conjunctions (although, because, while, since, when)
- Let sentences build to delayed resolutions

### Syntactic Complexity (toward paratactic)
- Simple clauses joined by "and," "but," or juxtaposition
- No subordination — everything gets the same grammatical weight
- Short, declarative, chained

### Tonal Stability (toward polytonal)
- Introduce tonal shifts within paragraphs — humor next to dread, intimacy next to coldness
- Let register break deliberately
- Undercut gravity with lightness, or lightness with gravity

### Tonal Stability (toward monotonal)
- Hold one emotional register throughout
- Remove humor from serious passages (or seriousness from comic ones)
- Let the consistency become its own kind of intensity

### Dialogic Texture (toward idiolectal)
- Give each character distinct vocabulary, rhythm, and verbal tics
- Let class, region, and personality show in speech patterns
- Characters should be identifiable by dialogue alone

### Dialogic Texture (toward transparent)
- Normalize character speech patterns
- Let dialogue serve information exchange
- Remove verbal tics and distinctive speech patterns

### Epistemic Stance (toward uncertain)
- Introduce doubt — unreliable perception, contradictory details, things that don't add up
- Let the narrator be wrong or limited
- Foreground the limits of knowing

### Epistemic Stance (toward certain)
- Clarify ambiguities
- Let the narrator be authoritative
- Present reality as stable and knowable

## Wild Mutation Algorithm

When the user says "surprise me," the mutator:

1. Analyzes the source passage's current DNA position
2. Identifies its 3 most extreme dimensions (the signature of the current voice)
3. Selects a mutation that *inverts* 1-2 of those extremes while preserving the third
4. This produces maximum transformation while keeping one anchor of familiarity

Example: If the source is high rhythm variance + high ornamentation + low emotional explicitness (McCarthy-adjacent), the wild mutation might invert the ornamentation to austere and the rhythm to metronomic while keeping the submerged emotion — producing something closer to Camus-meets-Butler.

## Scope Boundaries

**This skill handles**: Transforming existing prose by shifting its position in the 14-dimension style space.

**This skill does NOT**:
- Write new prose from scratch (that's `prose-writer`)
- Design voice specifications without source prose (that's `style-mixer`)
- Perform structural or content revisions (that's `prose-editor`)
- The mutator changes *how* something is said, never *what* is said
