---
name: ecology-design
description: >
  Framework for designing complete, internally consistent ecosystems. Reference when creating
  biomes, flora, fauna, food chains, or any biological element of a world. Uses the Getz
  10-niche model to ensure ecological completeness and the climate-biome cascade to derive
  ecosystems from geography.
---

# Ecology Design — The Web of Life

Most fictional worlds have predators and prey and nothing else. Real ecosystems have decomposers, scavengers, parasites, filter-feeders, symbiotes, and organisms that exist in niches no one thinks about until they're missing. A world with wolves and deer but no fungi is a world where nothing rots — and that's a world that collapses.

This skill provides the framework for designing ecosystems that feel complete, even if you only show 10% of them to the reader (the iceberg principle).

## The Getz 10-Niche Model

Wayne Getz's biomass transformation web organizes all organisms along three axes:

```
         ┌─────────── GATHERER (mobile) ──────────┐
         │                                         │
    Eats plants    Eats animals    Eats dead matter
    ┌─────────┐   ┌──────────┐   ┌───────────────┐
    │Victivore│   │Bestivore │   │ Carcasivore   │
    │(deer,   │   │(wolf,    │   │ (vulture,     │
    │ rabbit) │   │ hawk)    │   │  hyena)       │
    └─────────┘   └──────────┘   └───────────────┘

         ┌─────────── MINER (stationary) ─────────┐
         │                                         │
    Eats plants    Eats animals    Eats dead matter
    ┌─────────┐   ┌──────────┐   ┌───────────────┐
    │Lectivore│   │Zotanophg.│   │ Thanatophage  │
    │(caterpil│   │(barnacle,│   │ (dung beetle, │
    │ lar)    │   │ anemone) │   │  carrion grub)│
    └─────────┘   └──────────┘   └───────────────┘

    Plus:
    ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
    │Detritivor│  │Sarcophage│  │Necrophage│  │Decomposer│
    │(worm,    │  │(parasite │  │(parasite │  │(fungus,  │
    │ millipede│  │ on live  │  │ on dead  │  │ bacteria)│
    │          │  │ hosts)   │  │ hosts)   │  │          │
    └──────────┘  └──────────┘  └──────────┘  └──────────┘
```

### The 10 Niches

| Niche | Role | Real Example | Fantasy Potential |
|-------|------|-------------|-------------------|
| **Victivore** | Mobile plant-eater | Deer, grasshopper | Grazing beasts that migrate with seasons |
| **Lectivore** | Stationary plant-eater | Caterpillar, aphid | Creatures that embed in crystal-trees and feed |
| **Bestivore** | Mobile predator | Wolf, hawk, spider | Apex predators, pack hunters |
| **Zotanophage** | Stationary predator | Barnacle, venus flytrap | Ambush organisms, trap-builders |
| **Carcasivore** | Mobile scavenger | Vulture, hyena | Creatures that follow armies, haunt battlefields |
| **Thanatophage** | Stationary scavenger | Dung beetle, carrion grub | Organisms in ruins, feeding on decay |
| **Detritivore** | Particle consumer | Earthworm, millipede | Soil-makers, the invisible foundation |
| **Sarcophage** | Parasite on living hosts | Tapeworm, tick | Creatures that feed on magic-users, or on cursed energy |
| **Necrophage** | Parasite on dead matter | Certain fungi on corpses | Organisms that grow on the dead, transforming them |
| **Decomposer** | Breaks down all dead matter | Fungi, bacteria | The recyclers — without them, nothing returns to the soil |

**Design rule**: Every ecosystem should have at least one organism in each niche. You don't need to name them all — but knowing they exist makes the 10% you show feel like it's sitting on top of a complete web.

### Fantasy System Interaction

The most interesting ecological question: **how does the fantasy system interact with the food web?**

- If magic is ambient (like cursed energy), some organisms will have evolved to feed on it — a new energy source creates new niches
- If magic requires a rare material, organisms near deposits will evolve around it — crystal-eating insects, metal-filtering plants
- If magic can heal or resurrect, decomposers face competition — what happens to an ecosystem where nothing fully dies?
- If magic corrupts or mutates, the ecosystem near magical sites will be distorted — wrong niches, missing links, organisms that shouldn't exist

## The Climate-Biome Cascade

Ecosystems don't exist randomly. They cascade from physical geography:

```
Latitude + Altitude + Ocean currents
         │
         ▼
    Temperature + Rainfall
         │
         ▼
      Biome Type
         │
         ▼
    Flora (plants shaped by climate)
         │
         ▼
    Fauna (animals shaped by flora + climate)
         │
         ▼
    Food Web (10 niches filled by available organisms)
         │
         ▼
    Human Use (what people harvest, hunt, cultivate)
```

### Biome Quick Reference

| Biome | Temperature | Rainfall | Key Feature |
|-------|-------------|----------|-------------|
| Tropical rainforest | Hot year-round | Very high | Biodiversity maximum; vertical stratification |
| Savanna | Hot, seasonal | Moderate, seasonal | Grasses dominate; large grazers and predators |
| Desert | Hot or cold extremes | Very low | Adaptation to water scarcity; nocturnal life |
| Temperate forest | Seasonal | Moderate | Deciduous cycles; rich soil from leaf litter |
| Taiga/Boreal | Cold, long winters | Low-moderate | Coniferous; few species, high population density |
| Tundra | Very cold | Very low | Permafrost; mosses and lichens; migratory animals |
| Steppe/Grassland | Seasonal extremes | Low-moderate | Grasses; burrowing animals; fire-adapted |
| Wetland | Varies | Saturated | Transition zones; extremely high productivity |
| Alpine | Cold, UV-intense | Varies | Altitude-adapted; similar to tundra but with isolation |
| Deep ocean | Cold, dark | N/A | Chemosynthetic base; pressure-adapted |

### Designing a Fantasy Biome

If the fantasy system changes one physical variable, cascade the consequences:

1. **What changed?** (e.g., "this region has ambient magical energy")
2. **How does that affect the base layer?** (e.g., "plants grow faster and larger")
3. **What new niches open?** (e.g., "organisms that feed on magical energy directly")
4. **What existing niches shift?** (e.g., "predators are larger because prey is larger")
5. **What's the human consequence?** (e.g., "agriculture is incredibly productive here — this region feeds an empire")

## Ecosystem Health Indicators

When designing, check:
- **Energy flow**: Does energy enter (sunlight/magic) and exit (heat/entropy) the system? Closed loops are unrealistic.
- **Nutrient cycling**: Do dead things decompose and return nutrients? Without this, soil depletes.
- **Population balance**: Do predator populations lag behind prey populations? (Lotka-Volterra dynamics)
- **Keystone species**: Is there one species whose removal would collapse the web? These are narratively valuable.
- **Edge effects**: Where biomes meet, biodiversity increases. Borders are the most interesting places.

Read `references/getz-model-detail.md` for the full biomass transformation framework.
