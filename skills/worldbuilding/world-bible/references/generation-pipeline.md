# World Generation Pipeline

The order in which world elements should be created, derived from Dwarf Fortress's procedural generation and Azgaar's Fantasy Map Generator. Each layer constrains the next — creating downstream means upstream must exist first.

## The Pipeline

```
Layer 0: PHYSICS & METAPHYSICS
  What are the rules? What's the fantasy system?
  │
  ▼
Layer 1: GEOGRAPHY & COSMOLOGY
  How big? What shape? Continents, oceans, stars?
  (Constrained by: physics — plate tectonics, gravity, stellar mechanics)
  │
  ▼
Layer 2: CLIMATE & BIOMES
  Temperature, rainfall, seasons, ecosystems
  (Constrained by: geography — latitude, altitude, ocean currents, rain shadows)
  │
  ▼
Layer 3: ECOLOGY
  Flora, fauna, food webs, the 10 Getz niches
  (Constrained by: climate + fantasy system — what grows where, what eats what)
  │
  ▼
Layer 4: RESOURCES & SCARCITY
  What's rare, what's abundant, where it concentrates
  (Constrained by: geology + ecology — ores in mountains, timber in forests)
  │
  ▼
Layer 5: PEOPLES & CULTURES
  Who lives where, how they adapted to their environment
  (Constrained by: climate + resources + ecology — coastal people fish, mountain people mine)
  │
  ▼
Layer 6: LANGUAGE & NAMING
  How cultures sound, what they call things
  (Constrained by: isolation/contact patterns — related cultures share roots)
  │
  ▼
Layer 7: RELIGION & MYTHOLOGY
  What cultures believe and why
  (Constrained by: environment + fantasy system + history — desert people worship rain)
  │
  ▼
Layer 8: POLITICAL STRUCTURES
  How power is organized
  (Constrained by: geography + resources + culture + religion — river empires centralize, mountain cultures fragment)
  │
  ▼
Layer 9: TRADE & ECONOMICS
  How goods and value move
  (Constrained by: resources + geography + politics — trade routes follow rivers, bottlenecks create cities)
  │
  ▼
Layer 10: TECHNOLOGY & INSTITUTIONS
  What tools exist, how knowledge is organized
  (Constrained by: resources + economics + fantasy system — you build with what you have)
  │
  ▼
Layer 11: HISTORY
  What happened over time
  (Constrained by: everything above — history is the record of all these systems interacting)
  │
  ▼
Layer 12: CURRENT STATE
  The world as it is "now" — when the story begins
  (Constrained by: all of history — the present is the sum of everything that came before)
```

## How to Use the Pipeline

### You Don't Have to Build in Order

The pipeline shows **dependency**, not **creation order**. You can start anywhere — but if you define Layer 8 (politics) before Layer 4 (resources), you'll need to backfill: what resource scarcity makes this political structure necessary?

### The Three Entry Points

**Top-down** (start at Layer 0):
Best for hard SF or highly systematic worlds. Define physics first, derive everything else. Herbert's Dune was built this way — start with desert ecology, derive Fremen culture.

**Middle-out** (start at Layers 5-8):
Best for character-driven or political stories. Define the cultures and conflicts first, then ask what geography and resources would produce these tensions. Martin's Westeros was built this way.

**Bottom-up** (start at Layer 12):
Best for immediate stories. Define the current situation, then backfill history and systems as needed. Most RPG worldbuilding works this way — build the village first, then the kingdom.

### The Backfill Rule

Whenever you define something at a lower layer, check one layer up:
- You defined a trade route (Layer 9) → What geographic feature does it follow? (Layer 1)
- You defined a religion (Layer 7) → What environmental condition does it respond to? (Layer 2-3)
- You defined a political structure (Layer 8) → What resource does it control? (Layer 4)

If you can't answer the upstream question, you've found a gap. Fill it or flag it.

## Azgaar's Generation Order (Detailed)

From the Fantasy Map Generator's actual algorithm:

1. **Heightmap** → defines land/sea, elevation
2. **Temperature** → from latitude + altitude
3. **Precipitation** → from wind patterns + ocean proximity + rain shadows
4. **Biomes** → from temperature + precipitation (Whittaker classification)
5. **Rivers** → flow downhill, collect rainfall, create valleys
6. **Cultures** → placed in habitable zones, expand based on terrain accessibility
7. **States** → political entities formed by cultures, bounded by geography
8. **Religions** → placed at cultural centers, spread along trade routes or culture boundaries
9. **Settlements** → at river crossings, harbors, resource nodes, route intersections
10. **Trade routes** → connect settlements following terrain (prefer rivers, valleys, passes)
11. **Military** → positioned at borders, bottlenecks, valuable sites

This order works because each step constrains the next. Rivers can't exist without elevation. Cultures can't settle without habitable biomes. States can't form without cultures. Trade can't flow without settlements.

## The Fantasy System as Pipeline Disruptor

The fantasy system enters at Layer 0 and distorts every subsequent layer:

| If the fantasy system... | Pipeline disruption |
|-------------------------|---------------------|
| Creates energy | New biomes possible; ecology shifts |
| Enables fast travel | Geography matters less; empires can be larger |
| Enables fast communication | Politics centralizes; information becomes the key resource |
| Requires a rare material | That material's location determines the political landscape |
| Mutates organisms | Ecology is unstable; new niches constantly opening |
| Preserves the dead | Decomposition fails; nutrient cycling breaks; undead as a political force |
| Reads minds | Privacy doesn't exist; social structures radically different |
| Controls weather | Agriculture is political; climate is a weapon |

Every disruption cascades. Trace it through each subsequent layer.
