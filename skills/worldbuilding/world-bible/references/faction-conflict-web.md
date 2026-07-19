# Faction Conflict Web

Maps the relationships between all major factions, civilizations, and power groups in the world. Every political artifact, intercepted communication, or historical account is shaped by these relationships.

> This document is a living graph. Add factions as they're created, then define the edges between them.
>
> To design a *conflict itself* (why a war/rebellion/rivalry starts, how it escalates, what holds it, how it ends), use the `conflict-design` skill — its output (the five stated/felt axes, the metastable equilibrium and what tips it) populates the edges below.

## How to Use This Document

Each faction gets a node. Each relationship between factions gets a typed edge. The combination creates a conflict web — a map of tension, alliance, dependency, and dormant hostility that drives every political event in the world.

## Faction Nodes

For each faction, define:

```
### [Faction Name]
**Type**: [empire / city-state / corporation / religious order / insurgency / guild / nomadic confederation / other]
**Core drive**: [what they want above all else — one sentence]
**Resource base**: [what they control that gives them power]
**Vulnerability**: [what they need but don't control]
**Fantasy system relationship**: [how they interact with the magic/metaphysical element — do they control it, fear it, depend on it, deny it?]
**Internal tension**: [the fault line within the faction that could split it — ideological, generational, regional]
```

The **vulnerability** field is the most important. A faction's vulnerability determines who has leverage over them, which drives alliances and conflicts. If Faction A controls what Faction B needs, that's a power relationship regardless of military strength.

<!-- Add factions as they're created:

### [Example Faction]
**Type**: empire
**Core drive**: Maintain monopoly on [resource]
**Resource base**: Controls the only known [resource] deposits
**Vulnerability**: Dependent on [other faction] for food imports
**Fantasy system relationship**: Uses the system to enforce control; access restricted to ruling class
**Internal tension**: Provincial governors increasingly resent central authority
-->

## Relationship Edges

Define the relationship between every pair of factions that interact:

```
[Faction A] ←→ [Faction B]
**Type**: [allied / rival / vassal / trading partner / cold war / proxy war / ideological opposition / parasitic / symbiotic]
**Surface**: [what the relationship looks like publicly]
**Reality**: [what's actually happening beneath the surface — may differ from surface]
**Trigger**: [what event would escalate or transform this relationship]
**History**: [how this relationship formed and what resentments linger]
```

The **trigger** field is critical for narrative. Every relationship has a breaking point — an event that would shift allies into enemies, or force cold wars hot. These triggers are potential plot catalysts.

<!-- Add relationships as factions are defined:

### [Faction A] ←→ [Faction B]
**Type**: trading partner (surface) / parasitic (reality)
**Surface**: Formal trade agreement, diplomatic exchanges, joint festivals
**Reality**: Faction A's terms systematically drain Faction B's rare resource at below-market rates
**Trigger**: If Faction B discovers an alternative buyer, or if a new leader refuses the old terms
**History**: Agreement signed after Faction B's defeat in the [war], presented as "generous terms"
-->

## Conflict Web Visualization

When enough factions exist, map the full web:

```
            allied
    [A] ─────────── [B]
     │                │
     │ vassal          │ cold war
     │                │
    [C]              [D]
     │                │
     │ trading         │ proxy war
     │                │
    [E] ─────────── [F]
          rivals
```

Mark each edge with its type. Look for:
- **Triangles**: A is allied with B, B is allied with C, but A and C are rivals — unstable, something has to give
- **Chains of dependency**: A depends on B depends on C — if C falls, the chain collapses upward
- **Isolated factions**: No allies, multiple rivals — either very powerful or about to be destroyed
- **Bottleneck factions**: Everyone depends on them for something — immense leverage, immense target

## Power Balance Rules

1. **No faction should be invincible.** Every faction's strength creates a corresponding vulnerability. Military power requires resources. Economic power requires stability. Magical power requires access.
2. **Alliances should be uncomfortable.** The best alliances are between factions that need each other but don't trust each other. Comfortable alliances are boring.
3. **Historical grievances don't die.** A faction that was conquered, betrayed, or humiliated remembers. Even if the current relationship is peaceful, the resentment is a dormant trigger.
4. **Power vacuums are the most dangerous events in the world.** When a major faction falls or weakens, every relationship on the web shifts. Map what happens if each faction suddenly disappeared.
