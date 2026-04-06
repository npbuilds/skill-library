---
name: grape-encyclopedia
description: >
  Route grape variety questions to the correct specialist knowledge — major
  noble grapes, indigenous and regional varieties, or how the same grape
  expresses differently across terroir. Use when the user asks about any grape
  variety by name, wants to understand flavor signatures, or needs to identify
  a grape from tasting observations.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read
---

# Grape Encyclopedia — The Ampelographer

## Description
Master routing intelligence for all grape variety questions. Identifies whether a query requires structural variety profiles, expression-across-terroir analysis, or deep dives into obscure indigenous grapes. Handles cross-regional comparisons, synonym disambiguation, and classification disputes before escalating to regions-terroir when place has overtaken grape as the real subject.

## Skill Type
**Director** — routes to sub-skills; does not answer directly

## Routing Table

| Query Type | Route To |
|---|---|
| Profile of a major international variety (Cab Sav, Riesling, Chardonnay, etc.) | `noble-grapes` |
| Flavor, structure, or blind tasting diagnosis of a noble variety | `noble-grapes` |
| Benchmarks, aging potential, or blending partners for a major grape | `noble-grapes` |
| How the same grape expresses differently across regions | `grape-expression` |
| "Burgundy vs Oregon Pinot" style comparisons | `grape-expression` |
| Climate effect on a variety (cool vs warm expression) | `grape-expression` |
| Clone selection impact | `grape-expression` |
| Obscure, indigenous, or heritage variety (Xinomavro, Assyrtiko, Furmint, etc.) | `indigenous-varieties` |
| Historical origin of a regional grape | `indigenous-varieties` |
| Synonym and alias disambiguation (Shiraz vs Syrah, Tempranillo aliases) | Handle in director (see Conflict Resolution), then route |
| "What grows in [region]?" with focus on the place | Escalate → `regions-terroir` |
| "Why is Barolo aged so long?" (winemaking question, not grape) | Escalate → `winemaking/special-methods` |

## Multi-Skill Scenarios

### Scenario 1: Comparative Regional Expression
**Query:** "How does Pinot Noir differ between Burgundy and Oregon?"
**Analysis:** This is not a basic variety profile question — it requires understanding how the same grape transforms across two different climates, soils, and winemaking philosophies.
**Route:** `grape-expression` (Pinot Noir case study)
**Note:** If the user follows up asking about specific appellations or Burgundy's classification system, escalate to `regions-terroir`.

### Scenario 2: Indigenous Variety Identification
**Query:** "What is Xinomavro and why do people compare it to Nebbiolo?"
**Analysis:** Xinomavro is an indigenous Greek variety from Naoussa. The Nebbiolo comparison is a stylistic bridge (pale color, brutal tannin, high acid). This does not require noble-grapes routing.
**Route:** `indigenous-varieties`
**Note:** If the user then asks how Xinomavro expresses differently in Naoussa vs Amyndeon, route to `grape-expression`.

### Scenario 3: Climate Impact on a Noble Variety
**Query:** "Why does Chardonnay taste completely different in Chablis vs Napa Valley?"
**Analysis:** The user understands Chardonnay exists but wants to understand transformation — this is expression, not a basic profile.
**Route:** `grape-expression` (Chardonnay style spectrum case study)
**Secondary:** May need `winemaking/vinification` if oak treatment depth is requested.

### Scenario 4: Variety Profile + Blind Tasting Help
**Query:** "How do I identify Nebbiolo in a blind tasting?"
**Analysis:** Structural diagnosis of a noble grape — this is a noble-grapes question.
**Route:** `noble-grapes` (Nebbiolo diagnostic markers)

### Scenario 5: Synonym / Alias Chain
**Query:** "Is Tempranillo the same as Tinto Fino, Tinta Roriz, and Cencibel?"
**Analysis:** This is a classification and synonym question. Handle disambiguation here at the director level, then route to `noble-grapes` for the full profile.
**Route:** Director resolves alias → `noble-grapes` for full Tempranillo profile

### Scenario 6: Indigenous + Expression Hybrid
**Query:** "How does old-vine Grenache in Priorat differ from Châteauneuf-du-Pape?"
**Analysis:** Grenache is a noble grape, but this comparison requires both variety knowledge and expression-across-terroir reasoning.
**Route:** `grape-expression` (Grenache old-vine transformation), supplement with `noble-grapes` if structural baseline needed.

## Curriculum Order
For learners building grape knowledge systematically:

1. **`noble-grapes`** — Start here. Establish structural understanding of the 15 international varieties that dominate the world's wine map. Without this foundation, expression analysis is floating.
2. **`grape-expression`** — Once variety profiles are understood, study how place, climate, and winemaking transform the same variety into radically different wines. This is the conceptual leap that separates intermediate from advanced wine students.
3. **`indigenous-varieties`** — After noble grapes are internalized, the fascinating world of regional/heritage varieties opens up. Context from noble grapes enables useful stylistic comparisons (Xinomavro as "Nebbiolo of Greece").

## Conflict Resolution

### Synonym and Multi-Country Naming
Some grapes are known by fundamentally different names in different countries, creating confusion and classification debates:

| Primary Name | Aliases | Resolution |
|---|---|---|
| Syrah | Shiraz (Australia, South Africa, some New World) | Same grape, different name conventions. Syrah = European usage and cool-climate style. Shiraz = warm-climate, especially Australian. Neither is wrong. Use the name appropriate to the regional context being discussed. |
| Tempranillo | Tinto Fino (Ribera del Duero), Tinta Roriz (Portugal/Douro), Cencibel (La Mancha), Ull de Llebre (Catalonia), Aragonez (southern Portugal) | All are Tempranillo. When discussing a specific region, use the local name to honor regional identity. Master the primary name for international discussions. |
| Garnacha | Grenache (France/international), Cannonau (Sardinia), Grenache Noir | Garnacha = Spanish usage. Grenache = French/international usage. Cannonau = Sardinian designation with DOC protections. Treat as same grape unless the regional designation has legal/quality implications. |
| Albariño | Alvarinho (northern Portugal/Vinho Verde) | Same grape, different national expression and legal regime. Use regional name when discussing that region's wines. |
| Primitivo | Zinfandel (California), Crljenak Kaštelanski (Croatia, ancestral origin) | DNA proven identical. Primitivo = Italy (Puglia). Zinfandel = California. Crljenak = Croatian origin, now mainly academic. Treat as one grape with three identities. |
| Pinot Gris | Pinot Grigio (Italy), Grauburgunder (Germany/Austria), Rulander (Germany, older) | Same grape. Pinot Grigio = light, crisp Italian style. Pinot Gris = fuller Alsatian style or generic. Style implied by name choice. |

**Principle:** When a query uses one regional name but the answer spans multiple regions, establish the synonym chain explicitly before proceeding. Do not assume the user knows that Tinto Fino is Tempranillo.

### Classification Debates
- **Carménère vs Merlot:** For decades Chilean "Merlot" was actually Carménère. The 1994 reclassification is settled science — treat as distinct grapes. When a user asks about Chilean Merlot from before ~2000, note the identification uncertainty.
- **Touriga Nacional vs Touriga Franca:** Both are key Port varieties, often confused. Touriga Nacional = more intense, floral, the prestige grape. Touriga Franca = more volume, softer. Clarify when the distinction matters for quality discussion.
- **Blaufränkisch / Kékfrankos / Lemberger:** Same grape with three national names (Austrian/Hungarian/German-American). No quality hierarchy implied by name.

## Scope Boundaries

### Escalate to `regions-terroir` when:
- The grape question is really a **region question in disguise**: "What makes Barolo special?" starts with Nebbiolo but quickly becomes about Piedmont's DOCG system, communes, and climate.
- The user asks about **specific appellation rules**: "Can I use Cabernet Sauvignon in Burgundy?" — this is a legal/AOC question, not a grape question.
- The user asks about **vintage variation** for a specific region: "Was 2016 a good year for Pinot Noir in Burgundy?" — this requires climate and vintage assessment, not variety knowledge.

### Escalate to `winemaking` when:
- The question is about **how** a wine is made rather than what the grape is: "Why is Amarone so different from Valpolicella?" requires `special-methods` (appassimento), not just Corvina profile.
- The user asks about fermentation, maceration, or élevage choices for a specific variety.

### Stay within `grape-encyclopedia` when:
- The grape is the subject, not incidental to a larger question.
- Synonym resolution, origin stories, DNA analysis, and historical classification belong here.
