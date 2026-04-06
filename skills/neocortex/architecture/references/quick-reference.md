# Architecture — Quick Reference


## Child Skills

| Skill | Path | Type | Purpose |
|-------|------|------|---------|
| skill-cartographer | `skill-cartographer/SKILL.md` | Action | Map library coverage, gaps, and structural health |
| pattern-synthesizer | `pattern-synthesizer/SKILL.md` | Action | Find cross-domain patterns, isomorphisms, and unnamed abstractions |
| skill-evolutionist | `skill-evolutionist/SKILL.md` | Action | Track skill maturation over time, propose upgrades, identify staleness |
| growth-architect | `growth-architect/SKILL.md` | Action | Prioritize and sequence what to build next |
| domain-translator | `domain-translator/SKILL.md` | Action | Transfer knowledge and frameworks between domains |
| research-curator | `research-curator/SKILL.md` | Action | Build and maintain living research collections on key topics |
| clarity-engine | `clarity-engine/SKILL.md` | Action | Translate complex concepts into intuitive, visual explanations |

## Routing Logic

| Question Pattern | Route To | Why |
|-----------------|----------|-----|
| "What am I missing?", "Where are the gaps?" | skill-cartographer | Coverage and gap analysis |
| "I see a pattern", "These domains feel similar" | pattern-synthesizer | Cross-domain structural analysis |
| "Is this skill still good?", "What needs updating?" | skill-evolutionist | Maturity and staleness assessment |
| "What should I build next?", "What's the priority?" | growth-architect | Build planning and sequencing |
| "Does this concept apply in another domain?" | domain-translator | Cross-domain knowledge transfer |
| "What's the research on X?", "Build me a reading list" | research-curator | Curated reference collections |
| "Explain this to me", "What does X mean?" | clarity-engine | Concept translation for understanding |
| "How healthy is the library overall?" | skill-cartographer → skill-evolutionist → growth-architect (sequence) | Full structural audit |

## Conflict Resolution

| Conflict | Resolution | Reason |
|----------|-----------|--------|
| Cartographer identifies a gap; growth-architect ranks it low priority | Present both. Gaps exist on a spectrum — some are real but not urgent | Not every gap needs filling now |
| Pattern-synthesizer finds an isomorphism; domain-translator says the transfer doesn't work | Report the structural similarity AND the transfer failure. Understanding why a pattern doesn't transfer is itself insight | Failed transfers teach as much as successful ones |
| Skill-evolutionist flags a skill for upgrade; growth-architect prefers building new skills | Weigh maintenance vs. expansion. A stale foundational skill hurts everything that depends on it — evolution may be higher priority than growth | Foundation health before new construction |
| Multiple skills claim the same question | Route by specificity: if about a specific skill → evolutionist. If about the library shape → cartographer. If about what to build → growth-architect | Specificity determines the specialist |
