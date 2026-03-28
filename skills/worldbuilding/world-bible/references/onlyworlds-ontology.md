# OnlyWorlds Element Ontology

Adapted from the OnlyWorlds open standard — the most complete attempt at a universal schema for fictional world elements. 22 element types organized into 5 categories.

Source: github.com/OnlyWorlds/OnlyWorlds

Use this as a reference when deciding what types of world elements to create. You don't need to use all 22 — but knowing they exist helps you identify what's missing from your world.

## Categories and Element Types

### Beings (who exists)

| Type | What It Represents | Key Fields |
|------|-------------------|------------|
| **Character** | An individual person/entity | Name, species, traits, beliefs, relationships, faction |
| **Species** | A type of being | Physical traits, lifespan, habitat, culture, abilities |
| **Creature** | Non-sapient beings | Habitat, behavior, diet, danger level, ecological niche |
| **Family** | A lineage or bloodline | Members, history, reputation, holdings, alliances |

### Groups (how they organize)

| Type | What It Represents | Key Fields |
|------|-------------------|------------|
| **Collective** | Any organized group | Purpose, structure, membership, territory |
| **Institution** | Formal organization | Type (military, religious, academic, commercial), hierarchy, resources |
| **Title** | A rank or role | Who holds it, what power it grants, how it's obtained |

### Places (where things happen)

| Type | What It Represents | Key Fields |
|------|-------------------|------------|
| **Location** | Any named place | Type (city, ruin, natural feature), population, resources, dangers |
| **Zone** | A region or territory | Climate, biome, controlling faction, borders |
| **Map** | A visual/spatial reference | Scale, elements shown, relationship to other maps |
| **Marker** | A point of interest on a map | Type, coordinates, description |
| **Pin** | A narrative marker on a map | Associated event/character, time period |

### Concepts (what shapes the world)

| Type | What It Represents | Key Fields |
|------|-------------------|------------|
| **Ability** | A power or skill | Source, cost, limits, who can use it |
| **Language** | A communication system | Speakers, writing system, related languages |
| **Law** | A rule or regulation | Jurisdiction, enforcement, penalties, who it serves |
| **Phenomenon** | Something that happens | Frequency, cause, effects, who's affected |
| **Trait** | A quality or characteristic | Who/what has it, how it manifests |

### Narrative (what happens)

| Type | What It Represents | Key Fields |
|------|-------------------|------------|
| **Event** | Something that happened | When, where, who was involved, consequences |
| **Narrative** | A story thread | Characters involved, current state, tension |
| **Object** | A significant item | Owner, powers, history, location |
| **Relation** | A connection between elements | Type (alliance, rivalry, dependency), strength, history |

## Using This Ontology

### As a Creation Checklist

When building a new civilization or region, scan the 22 types:
- Beings: Do you have named characters? Defined species? Creatures in the ecosystem?
- Groups: What institutions exist? What titles carry power?
- Places: Is the geography defined? Key locations named?
- Concepts: What languages exist? What laws govern? What phenomena occur?
- Narrative: What events shaped this place? What objects matter? What relationships define it?

### As a Relationship Map

Every element type can relate to every other type. The most valuable relationships:

```
Character ── belongs to ── Institution
Character ── holds ── Title
Character ── possesses ── Ability
Institution ── controls ── Zone
Institution ── enforces ── Law
Event ── happened at ── Location
Event ── involved ── Character
Event ── caused ── Phenomenon
Object ── owned by ── Character
Object ── created by ── Institution
Species ── inhabits ── Zone
Creature ── fills niche in ── Zone (cross-ref ecology-design)
```

### Mapping to Artifact Types

| OnlyWorlds Type | Artifact Directory |
|----------------|-------------------|
| Location, Zone | `artifacts/regions/` |
| Collective, Institution, Species | `artifacts/civilizations/` |
| Event, Narrative | `artifacts/histories/` |
| Ability, Phenomenon, Language | `artifacts/lore/` |
| Relation (sensitive), Object (stolen) | `artifacts/intercepted/` |
