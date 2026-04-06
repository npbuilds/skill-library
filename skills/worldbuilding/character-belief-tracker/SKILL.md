---
name: character-belief-tracker
description: >
  Track what characters and factions know, believe, and hide — mapped against the world-bible's
  revelation layers. Use when you need to verify what a character would know at a given point
  in the narrative, check for accidental information leaks between revelation layers, or
  map the epistemic state of the world at any moment.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Write Glob
---

# Character Belief Tracker — Who Knows What

Every character in a story operates on incomplete and often incorrect information. The reader may know the truth (dramatic irony), but the characters don't. Tracking who knows what — and who *thinks* they know what — is the difference between a tight narrative and one full of accidental omniscience.

This skill maintains a belief graph: nodes are characters/factions, edges are what they know or believe about each world element, tagged by revelation layer.

## How to Run

### Input

The user provides one of:
1. **Register a character/faction** — add a new node to the belief graph with their initial knowledge state
2. **Update beliefs** — record that a character learned something, was deceived, or changed their understanding
3. **Query** — "What does [character] know about [subject]?" or "Who knows about [subject] at Layer 2?"
4. **Audit** — check for accidental information leaks (characters acting on knowledge they shouldn't have)

### Steps

1. Read the belief graph from `artifacts/meta/belief-graph.md` (create if it doesn't exist)
2. Read `skills/worldbuilding/world-bible/references/revelation-layers.md` for the canonical truth layers
3. Perform the requested operation (register, update, query, or audit)
4. Write the updated belief graph back to `artifacts/meta/belief-graph.md`

### Output

For **queries**: A report of what the character knows/believes about the subject, compared against the canonical truth.
For **audits**: A list of potential information leaks — places where an artifact or narrative moment shows a character acting on knowledge above their belief layer.

## The Belief Graph

### Structure

```yaml
# artifacts/meta/belief-graph.md

characters:
  admiral-voss:
    name: "Admiral Voss"
    faction: "the-ascendancy"
    beliefs:
      origin-of-magic:
        layer: 0                    # Believes the surface story
        belief: "A gift from the Founders"
        confidence: high
        source: "official doctrine"
      the-war:
        layer: 1                    # Knows something doesn't add up
        belief: "The official timeline has gaps"
        confidence: medium
        source: "personal observation of classified archives"

factions:
  the-ascendancy:
    default_layer: 0                # Most members believe the surface story
    exceptions:                     # Individuals who know more
      - admiral-voss
      - director-kerrigan
    institutional_beliefs:
      origin-of-magic:
        official: "A gift from the Founders"
        actual_layer: 0
```

### Belief States

Each belief entry tracks:

| Field | Description |
|-------|-------------|
| `layer` | 0-3, which revelation layer this character has reached for this subject |
| `belief` | What the character actually thinks is true (may be wrong) |
| `confidence` | How certain they are: high, medium, low, doubting |
| `source` | How they came to believe this (observation, told by X, read in Y, deduced) |

### The Confidence Spectrum

```
CERTAIN ─── CONFIDENT ─── UNCERTAIN ─── DOUBTING ─── QUESTIONING
   │              │            │              │             │
   │              │            │              │             │
"I know this"  "I believe"  "I think"    "Something's   "What if
                                          off"           everything
                                                         I know is
                                                         wrong?"
```

Confidence matters because it determines how a character acts. A Layer 0 character with high confidence behaves very differently from a Layer 0 character who's starting to doubt.

## Operations

### Register a Character

Creates a new node. Start with:
- What faction they belong to (inherits faction default beliefs)
- Any exceptions to faction defaults (things they know that the faction doesn't)
- Their relationship to the fantasy system (user, scholar, victim, ignorant)

### Update Beliefs (The Reveal Moment)

When a character learns something new:
1. What did they learn?
2. What layer does this move them to?
3. What was their previous belief?
4. What is their new belief?
5. How confident are they?
6. What was the source? (This matters — a rumor vs. firsthand evidence vs. a trusted friend all create different confidence levels)

### Query Beliefs

"What does Admiral Voss know about the origin of magic?"
→ Returns: Layer 1, believes "the official timeline has gaps," medium confidence, source: personal observation of classified archives.

"Who knows about the origin of magic at Layer 2 or deeper?"
→ Returns: list of characters/factions with Layer 2+ knowledge of that subject.

"What does Admiral Voss believe that's wrong?"
→ Compares Voss's beliefs against the canonical truth in revelation-layers.md, returns discrepancies.

### Audit for Information Leaks

Reads all artifacts and checks:
- Does any artifact written from a character's perspective contain information above that character's belief layer?
- Does any character act on knowledge they haven't been shown acquiring?
- Does any faction's behavior imply knowledge above their default layer?

Returns a report of potential leaks with artifact references.

## Theory of Mind Tracking

For complex narratives, track not just what characters believe, but what they believe *others* believe:

```
voss.beliefs.about(kerrigan).about(origin_of_magic) = Layer 0
  → "Voss thinks Kerrigan believes the official story"

kerrigan.beliefs.about(origin_of_magic) = Layer 2
  → "But Kerrigan actually knows the hidden truth"

This creates dramatic irony:
  → Voss trusts Kerrigan because he thinks they share beliefs
  → Kerrigan is operating with deeper knowledge, unseen by Voss
```

This is computationally simple but narratively powerful. Track it for the 3-5 most important character relationships, not for everyone.

## Integration with Other Skills

- **world-bible**: The canonical truth against which all beliefs are measured
- **lore-writer**: Each artifact's `perspective` field should be consistent with the character's belief state
- **revelation-layers.md**: The source of truth for what's real at each layer
- **consistency-checker** (when built): Will use this graph to validate artifacts

## Cross-Domain Connections

- **Writing/narrative-craft/point-of-view**: A character's belief layer determines their narrative reliability. A character at Layer 0 (surface beliefs) narrating through close-third POV creates dramatic irony when the reader knows Layer 2 truths. Belief states ARE POV constraints.
