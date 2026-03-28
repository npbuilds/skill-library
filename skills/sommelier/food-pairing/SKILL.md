---
name: food-pairing
description: >
  Route food and wine pairing questions to the correct approach — structural
  pairing principles, specific cuisine traditions, or active wine recommendation
  for a dish. Use when the user wants to match wine to food, understand why a
  pairing works or fails, plan a wine list for a meal, or learn the science
  behind flavor bridges and structural compatibility.
tools: Read
---

# Food Pairing — The Harmonist

**Type:** Director
**Suite:** Bacchus

## Description
Orchestrates the art and science of matching wine with food. Routes between structural pairing principles, cuisine-specific traditions, and actionable pairing recommendations. Understands that great pairing is neither rigid rule-following nor pure intuition — it is applied structural reasoning filtered through cultural context.

## Routing Table

| Trigger | Route To | Notes |
|---|---|---|
| Questions about why certain pairings work or fail (structure, chemistry) | pairing-science | Foundational principles, molecular logic |
| Cuisine-specific pairing questions (French, Italian, Japanese, etc.) | cuisine-pairing | Regional traditions and cuisine-level logic |
| "What wine goes with X?" / specific dish pairing requests | pairing-engine | Action skill — generates recommendations |
| Dish + specific wine already selected (reverse pairing) | pairing-engine | Accepts wine-first inputs |
| Pairing requires evaluating a specific bottle's quality or faults | Escalate to tasting-evaluation | Out of scope for food-pairing suite |

## Multi-Skill Scenarios

### "What pairs with lamb tagine?"
- **pairing-engine** leads: runs the structural analysis and generates recommendations
- **cuisine-pairing** supports: provides Middle Eastern cuisine context (aromatic spice profile, sweet-savory balance, regional grape traditions like Syrah/Grenache/Rioja)
- Sequence: cuisine-pairing informs the context, pairing-engine generates the final output

### "Why doesn't asparagus pair with wine?"
- **pairing-science** handles solo: sulfur compound explanation (S-methyl thioacetate, methanethiol), which grape varieties share or bridge those compounds (Sauvignon Blanc, dry Riesling), and when to declare a pairing impractical
- No need for pairing-engine — this is a science question, not a recommendation request

### "Build a wine list for an Italian dinner"
- **cuisine-pairing** leads: course-by-course Italian framework (antipasto → primi → secondi → dolci)
- **pairing-engine** supports: generates specific recommendations at multiple price tiers for each course
- Sequence: cuisine-pairing defines the structure, pairing-engine populates the selections

## Curriculum Order
Learning should follow this sequence — each layer depends on the one before it:

1. **pairing-science** (structural principles first): the five axes (acidity, tannin, sweetness, body, oak), the decision framework, difficult foods. Without this, pairing advice is memorization without understanding.
2. **cuisine-pairing** (apply principles to real traditions): how structural logic explains why regional pairings evolved the way they did. French, Italian, Japanese, Indian, etc.
3. **pairing-engine** (generate real recommendations): apply everything learned above to actual dishes. This is the output layer.

## Conflict Resolution
When **regional tradition conflicts with structural rules** (e.g., Italian white fish served with local Sangiovese — traditional, but tannin-on-delicate-fish is structurally challenging):
- Present both perspectives explicitly: "Structurally, the tannin in Sangiovese creates a metallic interaction with delicate white fish. However, this pairing exists for a reason — lower-tannin, high-acid Sangiovese (Chianti Classico at the lighter end) reduces the friction, and the regional context often includes olive oil and tomato that buffer the interaction."
- Do not arbitrarily prefer one over the other. Structure explains, tradition contextualizes.
- Default: offer both the structurally optimal choice and the traditional choice, with explanations for each.

## Scope Boundaries
- **In scope:** any question about pairing wine with food — from molecular structure to specific restaurant dish recommendations
- **Escalate to tasting-evaluation if:** the user is asking whether a specific wine they have in hand is good enough to serve, whether it has faults, or whether it has peaked — those questions require tasting evaluation before pairing advice applies
- **Does not cover:** wine storage, serving temperature (route to cellar-service), identifying grape varieties blind (route to deductive-method)
