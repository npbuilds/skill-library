---
name: regions-terroir
description: >
  Route wine geography, terroir science, and appellation law questions to the
  correct specialist knowledge. Use when the user wants to understand a specific
  wine region, learn why a region tastes the way it does, understand how soil
  and climate shape wine, or navigate the legal classification systems governing
  wine production worldwide.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read
---

# Regions & Terroir — The Cartographer

## Description
Maps the wine world from soil to appellation boundary. Routes questions about place, climate, geology, and legal designation to the correct specialist. Distinguishes Old World tradition from New World innovation, explains why the same grape tastes different across latitudes, and interprets appellation law when rules shape what ends up in the glass.

## Skill Type
director

## Routing Table
| Sub-skill | Handles |
|---|---|
| `old-world-atlas` | France, Italy, Spain, Germany, Portugal, Austria, Greece, Georgia — regional profiles, appellations, soil maps, producer benchmarks |
| `new-world-atlas` | United States, Australia, New Zealand, South Africa, Argentina, Chile — regional profiles, emerging appellations, cult producers |
| `terroir-science` | Soil types and wine character, climate classification (Winkler, Huglin), mesoclimate factors, the minerality debate, continental/maritime/Mediterranean distinctions |
| `appellation-law` | EU PDO/PGI framework, AOC/AOP, DOC/DOCG, DO/DOCa, AVA, GI systems, label law, classification systems (1855 Bordeaux, Burgundy Grand Cru, VDP) |

## Multi-Skill Scenarios

### Scenario 1 — "Why does Barolo taste different from Chianti?"
**Skills engaged:** `terroir-science` + `old-world-atlas`
**Routing logic:** This is a comparative regional question with a geological and varietal underpinning. `terroir-science` explains the role of calcareous clay (Barolo) vs. galestro/alberese (Chianti Classico), altitude, and continental vs. maritime differences. `old-world-atlas` provides the Piedmont Nebbiolo profile alongside the Tuscan Sangiovese profile, including specific commune differences within each zone.

### Scenario 2 — "Is Walla Walla worth exploring for Syrah lovers?"
**Skills engaged:** `new-world-atlas` + `terroir-science`
**Routing logic:** `new-world-atlas` covers the Columbia Valley AVA and Walla Walla sub-AVA — soil composition, benchmark producers, stylistic fingerprint. `terroir-science` explains the high-altitude, desert-continental climate, diurnal range, and how it compares to Northern Rhône granite/granite-schist conditions that produce the Syrah benchmark the question implies.

### Scenario 3 — "Can a Côtes du Rhône label say 'Grand Cru'?"
**Skills engaged:** `appellation-law` + `old-world-atlas`
**Routing logic:** `appellation-law` leads — Côtes du Rhône is a regional AOC with no Grand Cru tier; the label claim would be prohibited under EU PDO rules. `old-world-atlas` provides the Southern Rhône appellation hierarchy (CdR → Villages → Châteauneuf-du-Pape) to contextualize what the question is really asking.

### Scenario 4 — "Why are Santorini whites so mineral and salty?"
**Skills engaged:** `terroir-science` + `old-world-atlas`
**Routing logic:** `terroir-science` explains volcanic pumice and pozzolan soils, proximity to the sea, the basket-trained vine system (kouloura) that shields grapes from Aegean winds, and the science of saline character in volcanic-soil wines. `old-world-atlas` provides the Assyrtiko profile, Santorini's PDO rules, and the context of ungrafted vines in phylloxera-free pumice.

### Scenario 5 — "How does Napa Cabernet compare to Pauillac?"
**Skills engaged:** `old-world-atlas` + `new-world-atlas` + `terroir-science`
**Routing logic:** All three converge. `terroir-science` compares maritime Bordeaux with continental-Mediterranean Napa, the Winkler heat index difference, and how warm nights affect tannin structure vs. acid retention. `old-world-atlas` delivers the Pauillac profile. `new-world-atlas` delivers Oakville/Rutherford/Napa hillside profiles. Resolution: acknowledge that both can be world-class while explaining why the flavor signatures diverge.

### Scenario 6 — "What do German wine labels actually mean?"
**Skills engaged:** `appellation-law` + `old-world-atlas`
**Routing logic:** `appellation-law` leads with the Prädikat ripeness system (Kabinett through TBA), the VDP private classification, and mandatory label elements under EU law. `old-world-atlas` supports with Mosel and Rheingau regional context to make the abstract rules tangible.

## Curriculum Order
For users building systematic knowledge of wine regions and terroir, the recommended learning sequence is:

1. **`terroir-science` first** — Establish the *why* before the *where*. Understanding soil drainage, climate heat summation, and aspect gives every subsequent regional fact a physical cause rather than a string of memorized names.
2. **`appellation-law` second** — The rules that govern what a region can call itself and what it can put in the bottle. This frames all regional knowledge within a legal and quality-assurance structure.
3. **`old-world-atlas` third** — The foundational wine world. French, Italian, Spanish, German, and Portuguese regions carry most of the world's appellation law complexity; understanding them unlocks the reference grammar of fine wine.
4. **`new-world-atlas` fourth** — Read in light of everything above. New World regions are best understood as adaptations of Old World models to new climates, new soils, and deliberately fewer legal constraints.

## Conflict Resolution

### When climate data conflicts with appellation rules
Climate indices (Winkler, Huglin) may classify a zone as warmer or cooler than its appellation-mandated grape varieties imply. Example: some southern Burgundy villages have Winkler Region III heat loads but must produce Pinot Noir (a Region I–II grape). Resolution: present both the scientific classification and the legal reality honestly. Explain that appellation law locks in historical practice; climate change is creating real tension between the two. Do not dismiss either framework.

### When "New World" quality exceeds "Old World" expectations
The 1976 Judgment of Paris is the canonical case, but the question recurs. Resolution: avoid framing quality as a competition. Acknowledge that trophy-priced Napa Cabernet, Barossa old-vine Shiraz, and Marlborough Sauvignon Blanc can objectively match or outperform European counterparts in blind tasting. Contextualize this without undermining the legitimate heritage and complexity-per-acre advantage that centuries of site selection give Old World Grand Cru vineyards. Quality is not geography-exclusive.

## Scope Boundaries
- **Escalate to `grape-encyclopedia`** when a question about a region is primarily a question about a grape variety — e.g., "What makes Nebbiolo so tannic?" is a grape question, not a Barolo question. `old-world-atlas` can supply context, but the mechanistic answer (tannin structure, late-ripening phenology, color instability) belongs in `grape-encyclopedia`.
- **Escalate to `wine-service`** (if available) when the question shifts from *where is this wine from* to *how should I serve or store it*.
- **Escalate to `vintage-analysis`** (if available) when the question is specifically about whether a given year was good in a given region, rather than about the region itself.
