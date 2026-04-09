---
name: physical-world
description: Route questions about the physical environment of a world — terrain, climate, biomes, ecosystems, and technology. Use when the user is designing geography, building an ecosystem, placing civilizations on a map, defining a tech level, or asking how the physical landscape shapes the people who live in it.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read
---

# Physical World — The Stage Beneath the Story

Before societies can exist, the world must have a physical foundation that makes sense. Geography determines trade routes, climate shapes culture, ecosystems provide resources, and technology defines capability. These decisions aren't decoration — they're constraints that make everything else more believable.

## Routing Table

| What you're building | Skill to load |
|---|---|
| Terrain, mountain ranges, rivers, coastlines, resource distribution, how geography shapes civilization | `geography-ecology` |
| Biomes, flora, fauna, food chains, ecological completeness (which species exist and why) | `ecology-design` |
| What the world feels, smells, sounds like — the experiential layer of place | `sensory-worldbuilding` |
| Physical spaces that narrate history through traces, ruins, wear, architecture | `environmental-storytelling` |
| Technology trees, innovation pathways, how tech level shapes society and military | `technology-progression` |

## When to Layer These Skills

These three skills feed each other in a specific order:

1. **Geography first.** Where are the mountains, seas, and rivers? This determines climate zones (rain shadows, ocean currents) and resource distribution (ore near mountains, fertile soil in river deltas).

2. **Ecology second.** Given the climate and terrain from step 1, which biomes emerge? What animals evolve? The Getz 10-niche model in `ecology-design` ensures completeness.

3. **Technology third.** What resources does the geography provide? What tech level does ecology support? A desert civilization develops different tools than a forest one. `technology-progression` connects resource availability to innovation paths.

## Key Design Principles

**Constraints create character.** A world with abundant resources and no geographic barriers produces one kind of civilization; a world with scarce resources and natural chokepoints produces another. Don't design the physical world to be convenient — design it to be interesting, then figure out what kind of people emerge.

**Implied geography.** You don't need to map everything. Define the constraints (this continent is mostly dry, this river is the major trade artery, this mountain range divides two biomes) and let specifics emerge from need.

**Technology as multiplier.** A civilization's technology level multiplies the impact of geography. A pre-iron culture is stopped by a river; an engineering culture bridges or dams it. `technology-progression` tracks this relationship.

## See Also

- `worldbuilding-orchestrator` — parent orchestrator
- `civilizations` — how the physical world shapes the people who live in it
- `systems-craft` — how magic or advanced tech modifies physical rules
- `extrapolation-engine` — trace second-order consequences of physical design choices
