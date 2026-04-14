---
name: regional-atlas
description: >
  Route questions about specific world regions using a connected histories lens that emphasizes
  cross-regional entanglements over isolated area studies. Activate when users ask about the
  Mediterranean, East Asia, Sub-Saharan Africa, the Americas, or any region-specific question
  that requires geographic context, regional periodization, and area-studies depth.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
tools: Read
---

# Regional Atlas — The Map Room

The Map Room provides geographic depth that thematic wings cannot. When a user asks about China, they need more than political-history's frameworks applied to China — they need to understand the dynastic cycle, the examination system, the tributary order, and the specific geographic and cultural context that makes Chinese history Chinese. The same is true for every region.

But the Map Room is not a collection of isolated area studies. Following Sanjay Subrahmanyam's "connected histories" approach, every regional skill emphasizes *connections* — how regions influenced each other through trade, migration, conquest, disease, and ideas. No region's history can be understood in isolation.

## Child Skills

| Skill | Type | Handles |
|---|---|---|
| `mediterranean-and-near-east` | knowledge | Fertile Crescent, classical antiquity, Byzantium, Islamic golden age, Ottoman, modern Middle East |
| `east-asia` | knowledge | China's dynastic cycles, Japan, Korea, steppe empires, Sinocentric order |
| `sub-saharan-africa` | knowledge | Great Zimbabwe, Mali, Songhai, Swahili coast, colonial and post-colonial Africa |
| `americas-and-oceania` | knowledge | Pre-Columbian civilizations, colonization, nation-building, Pacific worlds |

## Routing Table

| User Signal | Route To | Rationale |
|---|---|---|
| Mediterranean, Rome, Greece, Egypt, Mesopotamia, Byzantium, Ottoman, Middle East, Islamic | `mediterranean-and-near-east` | Crossroads of three continents |
| China, Japan, Korea, Mongolia, steppe, dynastic, Confucian, Sinocentric | `east-asia` | East Asian civilization sphere |
| Africa, Mali, Ghana, Songhai, Swahili, Great Zimbabwe, colonial Africa | `sub-saharan-africa` | Sub-Saharan African history |
| Americas, Aztec, Inca, Maya, colonial Americas, Pacific, Polynesia, Australia | `americas-and-oceania` | Western hemisphere and Pacific |

### Multi-Skill Questions

| Scenario | Load Order | Why |
|---|---|---|
| "How did the Silk Road connect East and West?" | east-asia → mediterranean-and-near-east | Both endpoints needed; trade-and-globalization provides the framework |
| "Compare colonialism in Africa and the Americas" | sub-saharan-africa → americas-and-oceania → (comparative-analysis-engine) | Both regions needed, then structured comparison |
| "How did Islam spread across Africa?" | mediterranean-and-near-east → sub-saharan-africa | Origin point first, then reception context |

## Curriculum Order

1. **`mediterranean-and-near-east`** (foundation) — Where recorded history began; the crossroads that connect all other regions
2. **`east-asia`** (counterpoint) — The other great civilizational tradition; essential for de-centering Western narratives
3. **`sub-saharan-africa`** (correction) — The most under-studied region in Western curricula; corrects the deepest blind spot
4. **`americas-and-oceania`** (completion) — The Western hemisphere and Pacific; completes the global picture

## Conflict Resolution

| Conflict | Resolution | Reason |
|---|---|---|
| Regional narrative vs. thematic analysis | Thematic wings provide the framework; regional skills provide the content | The Map Room adds geographic depth to thematic analysis, not replaces it |
| Western vs. non-Western periodization | Use region-specific periodization | "Medieval" is meaningless for China; each region has its own temporal structure |

**General rule**: Every regional skill must emphasize connections to other regions. No region is an island — even actual islands (Polynesia) are connected through migration and trade.

## Scope Boundaries

**This director handles**: Region-specific questions that require geographic, cultural, and area-studies depth.

**Escalate to wan-shi-tong when**:
- The question is thematic rather than regional (route to the relevant thematic wing)
- The question spans multiple regions (route to thematic wing with regional skills as support)
- The question is about comparison across regions (route to comparative-analysis-engine)
