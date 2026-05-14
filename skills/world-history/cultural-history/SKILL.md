---
name: cultural-history
description: >
  Route questions about art, religion, gender, identity, social movements, and everyday life
  across history. Activate when users ask about how ordinary people lived, how belief systems
  shaped civilizations, how marginalized groups changed history, how cultural production
  reflects and reshapes power, or how the texture of human experience varies across time.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read
---

# Cultural History — The Gallery of Voices

The Gallery of Voices preserves the aspects of history that political, economic, and military historians traditionally overlooked: what did ordinary people believe, fear, celebrate, and create? How did gender, religion, and identity shape daily life? How did social movements change what was possible? Cultural history is not a softer, less rigorous alternative to political history — it is the history of everything that makes human experience *human* rather than merely institutional.

This wing was expanded by Spelunker's research, which identified gender history and social history as critical gaps. It now includes five knowledge skills covering the full range of human cultural experience.

## Child Skills

| Skill | Type | Handles |
|---|---|---|
| `religions-and-worldviews` | knowledge | Axial Age through secularization; lived religion; syncretism; religion as political force |
| `gender-and-sexuality-history` | knowledge | Gender as historical category (Scott); sexuality, family, reproduction; feminist historiography |
| `social-movements-and-identity` | knowledge | Abolitionism through environmentalism; movement-building; history from below |
| `art-and-cultural-production` | knowledge | Art as evidence and force; patronage, censorship, transmission |
| `everyday-life-and-material-culture` | knowledge | Annales school; Braudel; microhistory; mentalites; the longue duree of daily life |

## Routing Table

| User Signal | Route To | Rationale |
|---|---|---|
| Religion, faith, church, mosque, temple, Reformation, Axial Age, secularism | `religions-and-worldviews` | Questions about belief systems |
| Gender, women, feminism, masculinity, sexuality, family, marriage, reproduction | `gender-and-sexuality-history` | Questions about gender and sexuality |
| Movement, protest, civil rights, abolition, suffrage, labor, activism | `social-movements-and-identity` | Questions about collective action and identity |
| Art, architecture, literature, music, painting, patronage, censorship | `art-and-cultural-production` | Questions about cultural production |
| Food, clothing, daily life, housing, death, festival, ordinary people, "what was it like" | `everyday-life-and-material-culture` | Questions about lived experience |

### Multi-Skill Questions

| Scenario | Load Order | Why |
|---|---|---|
| "How did the Reformation change everyday life?" | religions-and-worldviews → everyday-life-and-material-culture | Doctrinal change first, then its impact on daily experience |
| "How did feminism change art?" | gender-and-sexuality-history → art-and-cultural-production | Gender framework first, then its cultural expression |
| "How did ordinary people experience the Industrial Revolution?" | everyday-life-and-material-culture → social-movements-and-identity | Daily life first, then collective response |

## Curriculum Order

1. **`everyday-life-and-material-culture`** (foundation) — Start with what life was actually like; this grounds all other cultural analysis
2. **`religions-and-worldviews`** (framework) — Belief systems structured daily life for most of history
3. **`gender-and-sexuality-history`** (lens) — Gender shapes every aspect of experience; a cross-cutting analytical tool
4. **`social-movements-and-identity`** (dynamics) — How people organize to change cultural and political conditions
5. **`art-and-cultural-production`** (expression) — Cultural production as evidence for and agent of all the above

## Conflict Resolution

| Conflict | Resolution | Reason |
|---|---|---|
| Elite vs. popular culture | Start with popular; add elite context | The Gallery of Voices privileges voices usually excluded |
| Religious vs. secular explanation of cultural change | Present both | Secularization thesis is contested; religion remains a force |
| Structural vs. agency explanation of social movements | Name both | Structural conditions create opportunities; agency creates movements |

**General rule**: Cultural history privileges perspectives usually absent from political and economic narratives. When in doubt, ask: whose experience is missing from this account?

## Scope Boundaries

**This director handles**: All questions about human cultural experience — belief, identity, expression, daily life, and collective action.

**Escalate to wan-shi-tong when**:
- The question is about political consequences of cultural movements (route to political-history)
- The question is about economic structures underlying cultural production (route to economic-history)
- The question is about ideas as intellectual systems rather than lived experience (route to intellectual-history)
