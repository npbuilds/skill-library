---
name: systems-craft
description: Route questions about the rules and systems that make a world distinct — magic, metaphysics, naming, and the foundational axioms in the world-bible. Use when designing a magic or technology system, creating a naming language for a culture, checking a world decision against its core rules, or establishing the fundamental constraints that everything else must respect.
tools: Read
---

# Systems Craft — The Rules of the World

Every world has rules. Some are physical (gravity, thermodynamics). Some are magical or metaphysical (what's possible beyond normal physics). Some are linguistic (what do names from this culture sound like). The world-bible is the authoritative record of all of them.

## Routing Table

| What you're building | Skill to load |
|---|---|
| Magic systems, metaphysical substrates, speculative technology rules | `magic-system-design` |
| Hard/soft spectrum for your magic, Sanderson's laws, cost structures | `magic-system-design` (preferred) or `magic-systems` |
| Names for people, places, institutions within a specific culture | `naming-system` |
| Checking a world decision against established axioms; adding new axioms | `world-bible` |

> **Note on duplicates:** `magic-system-design` and `magic-systems` cover overlapping ground — both address hard/soft magic spectra, Sanderson's laws, and cost structures. Prefer `magic-system-design` for new work; `magic-systems` may have supplementary material worth checking for comprehensive design.

## The World-Bible Is Always the Final Authority

Before using any other skill in this director — or any other director — the world-bible should be checked for relevant axioms. If the world has established that "magic requires physical sacrifice," every new magic system element must respect that constraint. The world-bible is not a reference document to consult optionally; it's the source of truth that prevents creative drift.

**Add to the world-bible:** Every major systems decision that has downstream implications belongs in the world-bible. Don't just design a magic system — record its core axioms (source, cost, limits, access) so `character-belief-tracker` and `extrapolation-engine` can reference them.

## Designing Systems With Constraint

The tension between what's *possible* and what's *accessible* is where interesting systems live:

- **Magic source** (where does the power come from?) — sets the cosmological stakes
- **Magic cost** (what does using it take?) — creates dramatic tension and limits
- **Magic limits** (what can't it do?) — prevents narrative short-circuits
- **Magic access** (who can use it?) — determines social and political implications

`magic-system-design` structures these decisions. `naming-system` ensures the language of the magic (spell names, creature names, place names) feels internally consistent with the culture that uses it.

## See Also

- `worldbuilding-orchestrator` — parent orchestrator
- `physical-world` — physical constraints the magic system must coexist with
- `civilizations` — how magic intersects with political power and religion
- `extrapolation-engine` — trace second-order consequences of magic system design
