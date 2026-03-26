# Artifact Format

Standard structure for all in-universe artifacts produced by the lore-writer.

## Frontmatter (Required)

Every artifact file begins with YAML frontmatter:

```yaml
---
subject: "The Reach"                    # What this artifact is about
voice: atmospheric                      # Voice register used (see voice-registry.md)
perspective: "unnamed traveler"         # Who in the world wrote/told this
layer: 0                                # Revelation layer (0=surface, 3=deepest truth)
related_axioms:                         # Which world-bible axioms constrain this
  - "faster-than-light communication"
  - "resource scarcity: helium-3"
created: 2026-03-22                     # Date the artifact was produced
---
```

### Field Definitions

| Field | Required | Description |
|-------|----------|-------------|
| `subject` | Yes | The in-world topic — a place, person, event, phenomenon, or concept |
| `voice` | Yes | One of: epistolary, uncanny, mythic, atmospheric, clinical, chronicle, visceral |
| `perspective` | Yes | The in-world author or narrator. Can be named, titled, or described ("a border merchant", "the Office of Naval Intelligence") |
| `layer` | Yes | 0-3. Which revelation layer this artifact presents. Layer 0 = common knowledge. Layer 3 = deepest hidden truth. Most artifacts should be Layer 0 or 1. |
| `related_axioms` | No | References to world-bible axioms this artifact must respect. Helps the consistency-checker (when built). |
| `created` | Yes | Date the artifact file was created |

## Body Content

After frontmatter, the artifact is **pure in-universe text**. No meta-commentary, no author's notes, no "this represents..." framing. The document is what it says it is.

### Structural Conventions by Artifact Type

**Region profile** (`artifacts/regions/`):
- Opens with sensory impression, not geography lesson
- Physical description woven through narrative, not listed
- The perspective character's relationship to the place shapes what's described

**Civilization profile** (`artifacts/civilizations/`):
- Written as if by someone who has opinions about this civilization
- Systems (governance, economy, military) described through their effects on daily life
- What the profile omits reveals the author's blind spots

**Historical account** (`artifacts/histories/`):
- Events presented with causation (even if the chronicler's causation is wrong)
- Named dates, figures, and places anchor the narrative
- The chronicler's bias is embedded in word choice, not stated

**Lore document** (`artifacts/lore/`):
- Myths, sacred texts, folk knowledge, oral traditions
- The culture's voice, not the author's
- Explanatory — these documents exist because a culture needed to explain something

**Intercepted document** (`artifacts/intercepted/`):
- Not meant for the reader — written for someone specific inside the world
- Context is assumed, not explained
- May include redactions, damage, translation notes, or analyst marginalia

## File Naming

Pattern: `<subject-slug>-<voice>.md`

Use lowercase, hyphenated slugs. The voice suffix helps identify the register at a glance.

Examples:
```
artifacts/regions/the-reach-atmospheric.md
artifacts/civilizations/the-ascendancy-clinical.md
artifacts/histories/fall-of-the-second-compact-chronicle.md
artifacts/lore/why-the-stars-went-silent-mythic.md
artifacts/intercepted/voss-to-kerrigan-003-epistolary.md
```

## Cross-Referencing

Artifacts don't exist in isolation. A civilization profile might mention a region. A historical account might reference a faction that has its own profile. An intercepted letter might name a place described in a separate artifact.

### Inline References

When an artifact mentions a subject that has (or should have) its own artifact, mark it with a reference tag:

```
The fleet departed from [[regions/the-reach]] under sealed orders.
```

Format: `[[artifact-type/subject-slug]]`

This does three things:
1. **For the writer**: signals that this subject is important enough to have its own artifact
2. **For the consistency-checker (when built)**: enables validation that referenced artifacts exist and don't contradict this one
3. **For the reader**: creates a web of connections across the world that can be followed

### Orphaned References

A reference to an artifact that doesn't exist yet is called an orphaned reference. This is **not an error** — it's a creative prompt. Orphaned references are a to-do list of artifacts the world needs. The consistency-checker will eventually flag these as "referenced but not yet created."

### Frontmatter References Field

In addition to inline references, the frontmatter can include an explicit list:

```yaml
references:
  - regions/the-reach
  - civilizations/the-ascendancy
  - intercepted/voss-to-kerrigan-003
```

This field is optional but useful for artifacts with many cross-references, making the connection web visible at a glance.

## Versioning

Artifacts are not versioned. Each artifact is a single document that exists in the world at a specific point. If the world's understanding of a subject changes, produce a *new* artifact from a different perspective or revelation layer — don't edit the old one. The accumulation of artifacts about the same subject, from different perspectives and layers, *is* the worldbuilding.
