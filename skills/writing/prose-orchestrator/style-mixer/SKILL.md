---
name: style-mixer
description: >
  Blend 2-4 author DNA profiles into a novel Voice Card — a reusable style specification that
  the prose-writer can consume. Use when the user wants to design a specific voice for a project,
  character, or piece by combining elements from different authors. The mixer doesn't average —
  it selects which dimensions to pull from each author.
tools: Read, Write, Glob
---

# Style Mixer — The Blending Desk

Create new voices by combining authorial DNA. The output is a Voice Card — a portable style specification that tells the prose-writer (or any writer-agent) exactly how to sound.

## How to Run

### Input

The user provides one of:

1. **Recipe mode**: "70% Hobb / 20% Camus / 10% VanderMeer" — explicit author ratios
2. **Mood mode**: "I want something intimate but unsettling and ecologically grounded" — the mixer suggests a blend
3. **Pairing mode**: "Give me the Elevated + Polytonal pairing" — references an unusual pairing from `style-dna/references/unusual-pairings.md`
4. **Contrast mode**: "Start with McCarthy but make it funny" — a base author plus a mutation direction

### Steps

1. **Load the DNA**: Read `sentence-craft/style-dna/SKILL.md` and `sentence-craft/style-dna/references/author-profiles.md` to access the 14-dimension model and author profiles.

2. **Resolve the blend**: Convert the user's input into a 14-dimension target profile.

   - **Recipe mode**: For each dimension, calculate the weighted position. But don't just average — identify which dimensions the user *wants* from each author and weight those heavily:
     - "70% Hobb" primarily means: take her psychic distance (5), emotional explicitness (5), and sensory bandwidth (4)
     - "20% Camus" primarily means: take his emotional submersion (1), syntactic simplicity (1.5), and sparse density (2)
     - "10% VanderMeer" primarily means: take his sensory bandwidth (5) and epistemic uncertainty (1)
     - The *signature dimensions* of each author carry more weight than their mid-range dimensions.

   - **Mood mode**: Map the mood descriptors to dimensions, then find the author combination that covers them:
     - "intimate" → psychic distance 4-5 → Hobb, Butler
     - "unsettling" → epistemic stance 1-2, tonal stability 1-2 → VanderMeer, Jackson
     - "ecologically grounded" → sensory bandwidth 4-5, world-dominant → VanderMeer, McCarthy

   - **Pairing mode**: Read the pairing definition and build the blend from its recipe.

   - **Contrast mode**: Start with the base author's full profile, then identify which dimensions to shift and in what direction.

3. **Check for contradictions**: Some dimension combinations create productive tension (that's the point). But some create *incoherence*:
   - Invisible narrator + polytonal = difficult (who's shifting the tone if no one's there?)
   - Microscopic psychic distance + compressed velocity = possible but demands extremely precise execution
   - Extremely dense + extremely syncopated rhythm = may be unreadable

   Flag contradictions but don't prevent them — let the user decide. Some of the best voices live at contradiction points.

4. **Generate the Voice Card**: Output a formatted card (see format below) with the 14-dimension profile, a prose description of how the voice should sound, and 2-3 "anchor sentences" — example sentences that demonstrate the voice in action.

5. **Name the voice**: Give the blend a working name that captures its character. The user can rename it.

### Output: The Voice Card

```markdown
## Voice Card: [Name]

**Blend**: [Author ratios or mood description]
**Character**: [One-sentence description of how this voice sounds]

### Dimension Profile

| Dimension | Target | Primary Source |
|-----------|--------|---------------|
| Sentence Rhythm | [1-5] | [which author this comes from] |
| Psychic Distance | [1-5] | ... |
| Info Density | [1-5] | ... |
| Ornamentation | [1-5] | ... |
| Narrative Velocity | [1-5] | ... |
| Lexical Register | [1-5] | ... |
| Authorial Presence | [1-5] | ... |
| Sensory Bandwidth | [1-5] | ... |
| Emotional Explicitness | [1-5] | ... |
| World-to-Story | [1-5] | ... |
| Syntactic Complexity | [1-5] | ... |
| Tonal Stability | [1-5] | ... |
| Dialogic Texture | [1-5] | ... |
| Epistemic Stance | [1-5] | ... |

### Voice Description

[2-3 paragraphs describing how this voice sounds, what it pays attention to,
how it handles emotion, what its sentences feel like. Written as guidance
for someone who will write in this voice.]

### Anchor Sentences

[2-3 example sentences that demonstrate this voice. These are not from any
author — they are original sentences that show the blend in action.]

### What This Voice Does Well / Struggles With

**Strengths**: [what kinds of scenes, topics, or effects this voice excels at]
**Watch out for**: [what kinds of scenes or effects this voice might struggle with]
```

## Preset Voice Cards

These are ready-made blends for common use cases. The user can use them as-is or as starting points.

### The Legacy Registers

The five original prose-writer registers, now expressed as DNA positions:

| Register | DNA Position |
|----------|-------------|
| **Minimalist** | Rhythm 2, Distance 3, Density 2, Ornament 1.5, Velocity 4, Register 2, Presence 1.5, Sensory 2, Emotion 1.5, World 2, Syntax 1.5, Tone 1.5, Dialogue 2, Epistemic 3 |
| **Conversational** | Rhythm 3, Distance 3, Density 3, Ornament 2.5, Velocity 3, Register 2, Presence 3, Sensory 3, Emotion 3, World 2, Syntax 2.5, Tone 3, Dialogue 3, Epistemic 3 |
| **Literary** | Rhythm 4, Distance 3, Density 3.5, Ornament 4, Velocity 2.5, Register 3.5, Presence 2.5, Sensory 3.5, Emotion 3, World 3, Syntax 3.5, Tone 3, Dialogue 3, Epistemic 3 |
| **Academic** | Rhythm 2, Distance 4, Density 4.5, Ornament 2.5, Velocity 3.5, Register 4.5, Presence 2.5, Sensory 1.5, Emotion 1.5, World 2, Syntax 4, Tone 1.5, Dialogue 2, Epistemic 4.5 |
| **Lyric** | Rhythm 4.5, Distance 2.5, Density 2.5, Ornament 4.5, Velocity 2, Register 3.5, Presence 2.5, Sensory 4, Emotion 3, World 2, Syntax 2.5, Tone 2, Dialogue 1.5, Epistemic 2 |

## Mixing Principles

1. **Signature dimensions carry the identity.** When blending, each author's *extreme* scores matter most. Hobb at psychic distance 5 is her signature. Her sentence rhythm at 3 is unremarkable. The blend should inherit the extremes, not the averages.

2. **Contradiction is generative.** The most interesting voices live where dimensions conflict. Don't smooth out tensions — lean into them and describe how the tension manifests in the prose.

3. **Two authors is a blend. Three is a voice. Four is chaos.** Two-author blends tend to feel like "Author A but with feature X." Three-author blends start to feel like something new. Four-author blends require very clear dimension assignments to avoid incoherence.

4. **The anchor sentences are the test.** If you can't write convincing anchor sentences in the blended voice, the blend doesn't work yet. Revise the profile until the anchors sound right.

5. **Voice Cards are reusable.** Once created, a card can be used across multiple scenes, chapters, or projects. Save them as reference files for recurring voices.

## Scope Boundaries

**This skill handles**: Designing new voice specifications by blending author DNA.

**This skill does NOT**:
- Write prose in the blended voice (that's `prose-writer` consuming the Voice Card)
- Mutate existing prose toward an author (that's `style-mutator`)
- Analyze existing prose to identify its DNA (that's `style-analyzer`)
