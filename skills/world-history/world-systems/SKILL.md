---
name: world-systems
description: >
  Route questions about comparative civilizations, environmental history, demographic forces,
  deep history, and technology as a civilizational force. Activate when users ask big-picture
  questions about why civilizations rise and fall, how climate and disease shape history,
  what happened before agriculture, or how structural forces operate beneath the surface.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read
---

# World Systems — The Observatory

The Observatory is where Wan Shi Tong's library looks at the longest time scales and the largest patterns. While other wings focus on specific types of history (political, economic, cultural), the Observatory asks: what are the deep structural forces — environmental, demographic, technological — that operate beneath all of them? This is the wing of Braudel's longue duree, Diamond's geographic determinism, Turchin's cliodynamics, and David Christian's Big History.

The Observatory also houses the most methodologically adventurous skills: deep-history pushes the starting point of history back 200,000+ years; environmental-history treats climate as a historical actor; and comparative-civilizations evaluates grand theories that treat entire civilizations as units of analysis.

## Child Skills

| Skill | Type | Handles |
|---|---|---|
| `comparative-civilizations` | knowledge | Grand theories of civilizational rise/fall: Spengler, Toynbee, Diamond, Morris, Turchin |
| `environmental-history` | knowledge | Climate, disease, ecology as historical forces; the Anthropocene |
| `deep-history` | knowledge | 200,000+ years before agriculture; Big History; cognitive revolution |
| `demographic-and-structural-forces` | knowledge | Population, urbanization, cliodynamics, secular cycles, elite overproduction |
| `technology-and-civilizational-change` | knowledge | General-purpose technologies as inflection points; Mokyr's knowledge economics |
| `comparative-analysis-engine` | action | Structured comparison across time and space |

## Routing Table

| User Signal | Route To | Rationale |
|---|---|---|
| Civilization, rise and fall, Diamond, why did the West dominate | `comparative-civilizations` | Grand comparative questions |
| Climate, disease, plague, environment, Anthropocene, ecology | `environmental-history` | Environmental forces |
| Before agriculture, prehistoric, Big History, cognitive revolution, Neolithic | `deep-history` | Deep time |
| Population, demography, migration, Turchin, secular cycle, elite overproduction | `demographic-and-structural-forces` | Structural forces |
| Technology, invention, printing press, industrial, AI as historical force | `technology-and-civilizational-change` | Technological transformation |
| "Compare X and Y," "what do these have in common," structured comparison | `comparative-analysis-engine` | Action: formal comparison |

### Multi-Skill Questions

| Scenario | Load Order | Why |
|---|---|---|
| "Why did Europe colonize the world and not the other way around?" | comparative-civilizations → environmental-history → technology-and-civilizational-change | Grand divergence question requiring all three lenses |
| "How did the Black Death reshape Europe?" | environmental-history → demographic-and-structural-forces | Disease first, then its structural demographic consequences |
| "Is AI as transformative as the printing press?" | technology-and-civilizational-change → comparative-analysis-engine | Technology framework first, then structured comparison |

## Curriculum Order

1. **`deep-history`** (foundation) — Start at the beginning; understand what came before civilization
2. **`environmental-history`** (context) — The physical world humans inhabit shapes what they can do
3. **`demographic-and-structural-forces`** (dynamics) — Population and structural forces that drive change
4. **`comparative-civilizations`** (synthesis) — Grand frameworks for comparing across civilizations
5. **`technology-and-civilizational-change`** (application) — How technology transforms the structural conditions
6. **`comparative-analysis-engine`** (action) — Tool for formal comparison; requires all five knowledge skills as context

## Conflict Resolution

| Conflict | Resolution | Reason |
|---|---|---|
| Geographic determinism vs. institutional explanation | Present both; name Diamond vs. Acemoglu | The debate is ongoing and both have evidence |
| Environmental forces vs. human agency | Always acknowledge both | Pure determinism ignores human choices; pure agency ignores material constraints |
| Quantitative (cliodynamics) vs. qualitative analysis | Complementary; quantitative identifies patterns, qualitative explains mechanisms | Neither alone is sufficient |

**General rule**: The Observatory deals in the largest patterns and longest timescales. Always remind the user that grand theories illuminate but also obscure — every generalization about "civilizations" hides enormous internal variation.

## Scope Boundaries

**This director handles**: Big-picture, long-timescale, structural questions about human civilization.

**Escalate to wan-shi-tong when**:
- The question is about a specific political event (route to political-history)
- The question is about specific economic systems (route to economic-history)
- The question is about cultural or intellectual content rather than structural forces (route to cultural-history or intellectual-history)
