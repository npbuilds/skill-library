---
name: economic-history
description: >
  Route questions about trade, finance, industrialization, economic systems, labor, inequality,
  and material life across history. Activate when users ask about how economies have been
  organized, how wealth has been created and distributed, why some societies industrialized
  and others did not, or how financial systems have evolved and crashed.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read
---

# Economic History — The Counting House

The Counting House holds the material foundations beneath every political event, every cultural movement, every military campaign. Economic history asks: how did people produce, exchange, and distribute the things they needed to survive — and how did those arrangements create the world we recognize? This wing is the strongest bridge between Wan Shi Tong's library and the investing domain (Archon), because financial history directly informs market cycle analysis.

Every question in this wing applies the chronological lens: trade-and-globalization covers Silk Roads to hyperglobalization; money-and-financial-systems covers clay tablets to central bank digital currencies.

## Child Skills

| Skill | Type | Handles |
|---|---|---|
| `trade-and-globalization` | knowledge | Trade networks, integration/fragmentation cycles, Columbian Exchange through WTO |
| `money-and-financial-systems` | knowledge | Evolution of money, credit, banking, financial crises as recurring phenomena |
| `industrialization-and-development` | knowledge | Why industrialization happened where it did; the Great Divergence debate |
| `labor-and-inequality` | knowledge | How societies organize work and distribute rewards; Piketty, Scheidel |

## Routing Table

| User Signal | Route To | Rationale |
|---|---|---|
| Trade, Silk Road, globalization, tariffs, free trade, mercantilism | `trade-and-globalization` | Questions about exchange networks and integration |
| Money, currency, banking, financial crisis, inflation, debt, gold standard | `money-and-financial-systems` | Questions about monetary and financial systems |
| Industrial revolution, development, poverty, why some countries are rich | `industrialization-and-development` | Questions about economic growth and divergence |
| Slavery, labor, wages, inequality, unions, welfare state, Piketty | `labor-and-inequality` | Questions about work, distribution, and stratification |

### Multi-Skill Questions

| Scenario | Load Order | Why |
|---|---|---|
| "Why is Africa poorer than Europe?" | industrialization-and-development → labor-and-inequality → trade-and-globalization | Development framework first, then distribution patterns, then trade structures |
| "What caused the 2008 financial crisis?" | money-and-financial-systems → (bridge to investing/archon) | Financial system dynamics first, then connect to market analysis |
| "How did the slave trade reshape the Atlantic economy?" | labor-and-inequality → trade-and-globalization | Labor system first, then the trade network it created |

## Curriculum Order

1. **`trade-and-globalization`** (foundation) — Material exchange is the most basic economic activity; trade networks create the substrate for everything else
2. **`money-and-financial-systems`** (infrastructure) — Money and credit are the technologies that enable complex economies
3. **`industrialization-and-development`** (transformation) — The great break: why sustained growth became possible and why it remains uneven
4. **`labor-and-inequality`** (distribution) — Who benefits from growth? How have answers to this question shaped political history?

### Level Progression
- **Foundational**: trade-and-globalization, money-and-financial-systems
- **Intermediate**: industrialization-and-development
- **Advanced**: labor-and-inequality

## Conflict Resolution

| Conflict | Resolution | Reason |
|---|---|---|
| Market-driven vs. state-driven explanations | Present both with evidence | This is THE central debate in economic history |
| Geography vs. institutions as cause of development | Name both (Diamond vs. Acemoglu) | The debate is unresolved; evidence supports both partially |
| Quantitative vs. qualitative approaches | Cliometrics complements narrative | Economic history uniquely benefits from both |

**General rule**: Economic history has the strongest quantitative tradition of any historical subdiscipline. Use numbers when available, but never let them obscure the human experience beneath the data.

## Scope Boundaries

**This director handles**: All questions about production, exchange, distribution, and material life across history.

**Escalate to wan-shi-tong when**:
- The question is about political consequences of economic change (route to political-history)
- The question is about ideas driving economic change (route to intellectual-history)
- The question is about applying economic history to present markets (route to applied-history → archon bridge)
