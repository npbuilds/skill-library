---
name: aroma-lexicon
description: >
  Build and apply wine tasting vocabulary using Ann Noble's Wine Aroma Wheel —
  a three-tier hierarchy of 119 terms. Use when identifying specific aromas,
  understanding what aromatic observations reveal about grape variety, origin,
  and winemaking, or when improving blind tasting precision and tasting note
  quality.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
---

# The Aroma Lexicon — Noble's Wheel

## skill-metadata
- skill-id: sommelier/tasting-evaluation/aroma-lexicon
- skill-type: knowledge
- parent: sommelier/tasting-evaluation
- version: 1.0.0

## description
Encodes Ann Noble's UC Davis Wine Aroma Wheel as structured knowledge, providing a three-tier controlled vocabulary for nose assessment. Covers all 12 aroma categories with diagnostic value for grape, region, and winemaking technique. Maps primary, secondary, and tertiary aromas to development stages and provides a diagnostic aroma-to-identity index.

---

## When This Applies

Use this skill when the user:
- Wants to build or expand their wine tasting vocabulary
- Struggles to find words for what they are smelling or tasting
- Is writing a tasting note and needs precision in aroma description
- Is studying for CMS, WSET, or MW examinations and needs controlled vocabulary
- Has detected an aroma and wants to know what it reveals about the wine's origin, grape, or winemaking
- Is practicing blind tasting and the nose stage is the bottleneck

---

## The Noble Wine Aroma Wheel

In 1984, Dr. Ann Noble, a sensory scientist at the University of California Davis, developed the Wine Aroma Wheel to solve a specific problem: wine tasters used inconsistent, vague, and poetic language that made communication impossible. "This wine smells romantic" or "it has forest notes" could mean a hundred different things to different people.

Noble's solution was a controlled vocabulary based on sensory science: a three-tier hierarchical wheel that moves from the most general category (Tier 1) down through subcategories (Tier 2) to specific, precise descriptors (Tier 3). The wheel is now the standard reference for trained wine professionals worldwide and forms the basis for the aroma vocabulary in the CMS and WSET curricula.

**Why controlled vocabulary matters for blind tasting:**
1. **Consistency**: The same descriptor means the same thing to all trained tasters. "Cassis" (blackcurrant) is unambiguous; "dark fruit" is not.
2. **Diagnostic power**: Specific aromas at Tier 3 have known chemical causes and known origins. "Petrol/kerosene" = TDN (1,1,6-trimethyl-1,2-dihydronaphthalene), produced in Riesling as it ages. Once you know this, that aroma is not just descriptive — it is evidence.
3. **Communication**: Writing a tasting note that says "brioche, cream, and fresh lime with a mineral finish" communicates precisely to another trained taster. "Yeasty and citrus-y" does not.

**The three tiers:**
- **Tier 1** — 12 broad categories (e.g., Fruity, Floral, Earthy)
- **Tier 2** — Subcategories within each Tier 1 (e.g., under Fruity: Citrus, Berry, Tropical, Stone)
- **Tier 3** — Specific, precise descriptors (e.g., under Citrus: lemon, grapefruit, lime, lemon curd, orange peel)

Use the most specific tier you can confidently reach. "Citrus" is better than "Fruity." "Grapefruit + lime" is better than "Citrus."

---

## Tier 1 — 12 Categories

### 1. Fruity

**What produces it**: Esters (primarily from fermentation), grape-derived volatile compounds, and some varietal thiols. The most prominent aroma category in young wines.

**Tier 2 subcategories and diagnostic value**:

- **Citrus** (lemon, lime, grapefruit, orange peel, lemon curd, yuzu): Cool-climate white wines; high-acid varieties; Riesling (lime, lemon), Chardonnay at the cool end (lemon, grapefruit), Sauvignon Blanc (grapefruit, lime), Champagne and sparkling base wines, Albariño (lemon, lime zest)

- **Stone fruit** (peach, apricot, nectarine, plum, cherry, cherry pit): White stone fruit (peach, apricot) → Viognier (signature), Gewürztraminer, white Burgundy, warmer Riesling, Roussanne; Red stone fruit (plum, cherry, cherry pit) → Pinot Noir, Sangiovese, Grenache, Barbera, Gamay, Syrah at the red-fruit end

- **Tropical fruit** (mango, pineapple, guava, passion fruit, banana, melon): Warm-climate or New World whites; Marlborough Sauvignon Blanc (passion fruit = varietal thiol 4-MMP); warm-climate Chardonnay (pineapple, mango); Viognier in warm sites; banana note in carbonic maceration wines (Beaujolais Nouveau); some Champagne (pineapple in dosage-heavy styles)

- **Berry** (strawberry, raspberry, blackberry, blackcurrant/cassis, blueberry, cranberry): Strawberry → Pinot Noir (cool climate), Gamay, Grenache rosé; Raspberry → Pinot Noir, Grenache, cool-climate Syrah; Blackberry → Syrah/Shiraz, Zinfandel, Malbec; Cassis/blackcurrant → Cabernet Sauvignon (signature varietal thiol 4-MMP + pyrazines); Blueberry → Malbec, Primitivo, Carignan; Cranberry → cool-climate Pinot Noir, Nebbiolo (acidic red fruit)

- **Tree fruit** (apple, pear, quince): Green apple → unoaked Chardonnay (Chablis), Pinot Gris, Chenin Blanc; Ripe apple → aged white Burgundy, Alsace; Pear → Viognier, Pinot Blanc, Austrian whites; Quince → aged Chenin Blanc (Vouvray), Rioja Blanco

- **Dried fruit** (fig, date, raisin, prune, dried cherry, dried apricot, marmalade): Age-derived concentration or deliberate drying; Amarone (dried cherry, fig, chocolate); Tawny Port (fig, date, raisin, walnut); Sauternes aged (dried apricot, marmalade, orange peel); aged Barolo (dried rose, dried cherry); Madeira (dried apricot, orange peel, caramel)

---

### 2. Floral

**What produces it**: Terpenes — specifically geraniol, linalool, nerol, and citronellol — which are either grape-derived (strongly aromatic varieties) or yeast-derived during fermentation. Cool climates preserve terpenes; warm climates can degrade them.

**Tier 2 subcategories and diagnostic value**:

- **Rose** (fresh rose, dried rose, rose petal, rose water): Fresh rose → Gewürztraminer, young Muscat, Grenache rosé, Pinot Noir; Dried rose → Nebbiolo (signature), aged Pinot Noir, Grenache; Rose water → Gewürztraminer (signature, along with lychee)

- **Violet / Iris** (violet, iris, lavender): Nebbiolo (violet is the most diagnostic varietal floral marker, alongside tar), Malbec, Cabernet Franc, young Tempranillo, Mourvèdre

- **White flowers** (jasmine, orange blossom, honeysuckle, elderflower, acacia): Viognier (jasmine, honeysuckle — signature); Riesling (acacia, orange blossom in warmer styles); Muscat (orange blossom, grape blossom); Torrontés (signature white flower bomb, characteristic of Argentina); Grüner Veltliner (acacia, white pepper — not floral-dominated but present)

- **Blossom** (apple blossom, cherry blossom): Lighter whites and cool-climate varieties; Pinot Blanc, Auxerrois, some Soave

**Aromatic variety indicator**: Strong floral notes in a wine are one of the most reliable indicators of an aromatic variety (Riesling, Gewürztraminer, Muscat, Viognier, Torrontés). Non-aromatic varieties (Chardonnay, Cabernet Sauvignon, Pinot Noir) can show light floral notes, particularly with cool-climate growing or reductive winemaking, but will not lead with floral intensity.

---

### 3. Spicy

**What produces it**: Either grape-derived (rotundone for pepper; eugenol for some spice notes) or oak-derived (eugenol, vanilla, cinnamon from barrel treatment). The source matters diagnostically.

**Tier 2 subcategories and diagnostic value**:

- **Pepper** (white pepper, black pepper): White pepper = rotundone (found in Grüner Veltliner [signature] and Northern Rhône Syrah [signature]); Black pepper = Syrah/Shiraz broadly, Zinfandel, some Grenache, some Mourvèdre

- **Warm spices** (cinnamon, clove, nutmeg, allspice, star anise): Can be grape-derived (some Grenache, Gewürztraminer) or oak-derived (French and American oak release eugenol and other spice volatiles); Licorice/anise → Cabernet Sauvignon, Malbec, some Grenache (Southern Rhône)

- **Oak-derived spice** (vanilla, cedar, toasted spice, coconut): Vanilla → American oak (oak lactones, particularly β-methyl-γ-octalactone); Cedar/pencil shavings → French oak; Toast → higher-toast barrels; Coconut → new American oak specifically. The presence of these aromas indicates barrel aging. Their intensity indicates how new or how heavily toasted the oak was.

**Key distinction**: When you smell pepper, determine whether it is fresh/bright (white pepper → rotundone from grape) or warm/integrated (black pepper from Syrah, or clove/cinnamon from oak). This tells you whether the spice is terroir-derived or winemaking-derived — a diagnostically important difference.

---

### 4. Vegetative / Herbaceous

**What produces it**: Primarily methoxypyrazines (3-isobutyl-2-methoxypyrazine, IBMP) in grapes; also green-harvest decisions, under-ripe fruit, and some regional/varietal characteristics. These aromas are associated with cooler climates or earlier harvesting.

**Tier 2 subcategories and diagnostic value**:

- **Green bell pepper / capsicum**: Methoxypyrazine signature; Cabernet Sauvignon (especially cool climate or early-harvested), Cabernet Franc (even more prominent), Sauvignon Blanc (characteristic at cool end), Carmenère (very high pyrazine — diagnostic for Chilean Carmenère), Merlot at its coolest

- **Asparagus / artichoke**: Sauvignon Blanc under specific conditions; Grüner Veltliner (asparagus note is characteristic, along with white pepper); Vinho Verde

- **Grass / freshly cut hay**: Sauvignon Blanc (especially Loire: Sancerre, Pouilly-Fumé); cool-climate whites broadly; Muscadet

- **Mint / eucalyptus**: Australian Cabernet Sauvignon, especially Coonawarra (eucalyptus is a defining marker of Coonawarra — controversy exists whether it is terroir-derived or adjacent eucalyptus trees contributing to the microclimate); some Chilean Cabernet

- **Herbes de Provence / garrigue / thyme / rosemary**: Southern Rhône, Languedoc, Provençe, Corsica — these are classic Old World terroir markers, not fault indicators

- **Olive / tapenade**: Cabernet Sauvignon (especially Bordeaux and southern French), Syrah (Provençal style)

**Important context**: Pyrazine/herbal notes are often misidentified as faults by tasters trained on riper, more fruit-forward styles. In Sancerre, Pouilly-Fumé, Chinon, and cool-climate Cabernet, herbaceousness is a varietal and regional characteristic, not a defect. Only flag as potentially undesirable when it completely suppresses fruit and indicates under-ripe harvest.

---

### 5. Nutty

**What produces it**: Oxidative aging (acetaldehyde at moderate levels, and additional products of controlled oxidation); also toasted oak; malolactic fermentation at some levels.

**Tier 2 subcategories and diagnostic value**:

- **Walnut / hazelnut**: Oxidative aging in whites; aged white Burgundy (hazelnuts are a characteristic tertiary note of aged Meursault and Puligny-Montrachet); also Sherry (Amontillado, Oloroso) and Madeira

- **Almond**: Young wines (benzaldehyde from cherry pit and some stone fruit); also some Soave (Garganega has characteristic almond note); Fino Sherry lightly

- **Toast / roasted nut**: Oak influence + oxidation; heavily oaked whites; aged Champagne sur lees (roasted hazelnut from autolysis)

**Diagnostic note**: Nutty aromas in a still white table wine almost always indicate either: (a) controlled oxidative aging (Sherry-influenced, aged Burgundy), (b) extended time on lees, or (c) the wine is beginning to tire (unwanted oxidation). Context is everything.

---

### 6. Caramelized

**What produces it**: Heat concentration (botrytis, late harvest, drying), high residual sugar at barrel stage, and some Maillard reaction in oak.

**Tier 2 subcategories and diagnostic value**:

- **Honey / beeswax**: Botrytis-affected wines (Sauternes, TBA, Tokaji Aszú); aged Chenin Blanc (Vouvray moelleux/liquoreux); aged white Burgundy in exceptional years; some aged Riesling Auslese+

- **Caramel / butterscotch / toffee**: Diacetyl from MLF (see fault-diagnosis threshold for when excessive); dessert wine concentration; Tawny Port (caramel is a signature — oxidative plus sugar concentration); some Marsala

- **Dried fruit / marmalade** (overlap with Fruity-Dried): Sauternes, Beerenauslese, TBA; aged Madeira (marmalade is a classic Madeira tertiary note)

---

### 7. Woody

**What produces it**: Oak barrel or stave aging. The degree, type (French vs American), toast level, and age of the oak all determine which volatile compounds are extracted.

**Tier 2 subcategories and diagnostic value**:

- **Vanilla**: American oak β-methyl-γ-octalactone; prominent in Rioja Reserva/Gran Reserva (American oak historically used), New World Chardonnay, New World Cabernet

- **Cedar / cigar box / pencil shavings**: French oak; classic Bordeaux, Napa Cabernet, aged Rioja in French oak, Ribera del Duero; one of the most prized oak markers in fine red wines

- **Toast / char / smoke (oak)**: High-toast barrels; some California Chardonnay, some Californian reds, some Sonoma Pinot Noir

- **Coconut**: Specifically new American oak (whiskylactone); common in New World reds aged in new American oak; if very prominent, oak integration is likely lacking

- **Resin / sawdust**: New or cheap oak; poor oak integration; often a flaw indicator if prominent — suggests the oak is outpacing the wine's ability to absorb it

**Oak integration principle**: Great oak usage is invisible. When the wine has fully integrated its oak, you perceive the effects (complexity, texture, spice) without perceiving the oak itself as a separate, dominant element. When you can smell the planks, the oak is not integrated — either too new, too much, or the wine lacks the concentration to absorb it.

---

### 8. Earthy

**What produces it**: A combination of terroir-derived mineral compounds, microbial activity in the vineyard and winery, and the transformation of grape phenolics during aging. Some earthy aromas are volatile geosmin (see fault-diagnosis), but most classic earthy notes in wine are complex, layered, and prized.

**Tier 2 subcategories and diagnostic value**:

- **Forest floor / leaf litter / undergrowth / truffle**: Classic aged Burgundy Pinot Noir; also aged Bordeaux (forest floor emerges as a tertiary note); Barolo develops truffle over time; Pomerol shows a moist, forest floor earthiness

- **Wet stone / flint / gunflint**: Chablis (Kimmeridgian limestone/chalk); Sancerre (silex soils → "silex" tasting note); Pouilly-Fumé; certain Loire whites; some Muscadet. The French term "pierre à fusil" (gunflint) is used for the specific flinty-mineral note

- **Chalk / mineral (chalk)**: White Burgundy, Champagne, some English sparkling — chalky subsoil contributes a distinctive white-chalk note in the finish

- **Volcanic / graphite / pencil lead**: Etna wines (volcanic soils, distinctive graphite note), some Sicilian wines, Austrian Grüner Veltliner on volcanic soils, some Ribera del Duero, some Côtes du Rhône from volcanic terroirs

- **Iron / blood / iron filing**: Old-vine Pinot Noir, some aged Barolo, some Côte de Nuits reds; the iron note is associated with ferrous-rich soils and ancient vine root systems

- **Petrichor (rain on dry earth)**: Aged Riesling (particularly in Alsace and Rheingau); some aged Grenache; this is a distinct aroma from standard earthiness and is usually a positive complexity marker

---

### 9. Chemical

**What produces it**: This category in Noble's wheel is primarily a fault and flaw indicator. The aromas in this category are produced by chemical processes that are either the product of poor winemaking, contamination, or inadvertent spoilage.

**Tier 2 subcategories (see fault-diagnosis for full detail)**:

- **Sulfur / matchstick**: Excess SO₂ (reduction or over-addition); also some reductive winemaking styles
- **Nail polish / solvent**: Ethyl acetate (VA-associated); see fault-diagnosis
- **Bandaid / rubber**: Brett (4-EP); see fault-diagnosis
- **Vinegar**: Volatile acidity (acetic acid); see fault-diagnosis
- **Geranium**: Geranium taint (sorbate + LAB); see fault-diagnosis

**Routing note**: When a Chemical category aroma is detected, route to `fault-diagnosis` for the diagnostic protocol and "send it back?" decision. Do not attempt to describe chemical aromas as complexity — they require a fault assessment before proceeding.

---

### 10. Pungent

**What produces it**: High volatile compounds, primarily at high concentrations. This category overlaps with fault indicators and extreme stylistic expressions.

**Tier 2 subcategories and diagnostic value**:

- **Alcohol heat**: High ABV; felt on nose and in throat; distinct from body and from tannin heat; should be integrated in a balanced wine
- **Sulfur (at lower concentrations)**: Some natural wines show a slight struck-match note that is stylistic rather than a fault
- **High-VA wines**: Some Italian traditional styles (Barolo from certain producers historically), some natural wines

---

### 11. Oxidized

**What produces it**: Controlled or uncontrolled oxidation. The primary compound is acetaldehyde, which produces roasted nut and green apple (at high levels) aromas. At higher oxidation levels, aldehydes, Maillard products, and other oxidation compounds accumulate.

**Tier 2 subcategories and diagnostic value**:

- **Sherry-like / nutty / walnut**: Deliberate oxidative aging (Sherry, Madeira, Tawny Port, Vin Jaune, Montilla-Moriles); also a fault in wines not designed for oxidative aging
- **Maderized / cooked**: Excessive unintentional oxidation; see heat damage in fault-diagnosis
- **Apple / stale apple**: Acetaldehyde at moderate levels; common in sherry styles; a fault in fresh table wines

**Distinguishing intentional from unintentional oxidation**: If the wine is a known oxidative style (Sherry, Madeira, Tawny Port, Vin Jaune, Rancio, oxidative Rioja Blanco), the oxidative note is a feature. In any other wine where the style does not call for oxidation, these aromas indicate a fault.

---

### 12. Microbiological

**What produces it**: Secondary fermentation organisms (yeast, LAB) and their metabolic products, beyond the primary fermentation. These aromas are among the most complex and sought-after in fine wine.

**Tier 2 subcategories and diagnostic value**:

- **Yeasty / autolysis** (brioche, fresh bread, cream, biscuit, toast, almonds): Produced by the breakdown of dead yeast cells (autolysis) during extended lees contact; Champagne (brioche = the most iconic lees note); also Crémant, Cava, Franciacorta; Muscadet sur lie; aged white Burgundy; the longer the lees contact, the more pronounced the autolytic character

- **Malolactic / buttery** (butter, cream, crème brûlée at low levels): Diacetyl from Oenococcus oeni during MLF; characteristic of barrel-fermented and barrel-aged Chardonnay; also New World white wines where full MLF is encouraged; at low levels in red wine, adds roundness; fault at high levels (see fault-diagnosis)

- **Brettanomyces** (barnyard, bandaid, leather, animal, horse): Brettanomyces yeast; both here (low levels as complexity) and in the Chemical/fault category (high levels as fault). In traditional Old World reds, low-level Brett is a contested complexity element; in most modern wine, it is a flaw or fault.

- **Lactic / yogurt**: Some LAB-driven styles; some natural wines; high diacetyl blending with lactic notes can indicate a wine that has undergone partial MLF without full resolution

---

## Primary vs Secondary vs Tertiary

This classification describes the origin of the aroma and maps directly to the wine's development stage on the nose.

### Primary Aromas (from the grape)
- **Source**: Grape variety, climate, and vineyard
- **Categories**: Fruity (all subcategories), Floral, Spicy (grape-derived), Vegetative/Herbaceous, some Earthy (terroir mineral)
- **Development stage association**: **Youthful** wines are primary-dominant

**Examples**:
- Cassis and blackcurrant leaf → Primary; Cabernet Sauvignon grape
- Lime and white flower → Primary; Riesling grape + cool vineyard
- Lychee and rose water → Primary; Gewürztraminer varietal terpene
- Green pepper → Primary; methoxypyrazine from grape

### Secondary Aromas (from fermentation)
- **Source**: Yeast metabolism during alcoholic fermentation; lactic acid bacteria during MLF
- **Categories**: Microbiological (lees/yeast, butter/MLF), some Caramelized
- **Development stage association**: **Vinous to Developing** — secondary aromas begin emerging as primary fruit evolves

**Examples**:
- Bread dough, brioche, cream → Secondary; yeast autolysis (lees contact)
- Butter, butterscotch → Secondary; diacetyl from MLF
- Banana → Secondary; isoamyl acetate from carbonic maceration yeast
- Toasted bread → Secondary; barrel fermentation and lees stirring

### Tertiary Aromas (from aging in oak or bottle)
- **Source**: Chemical transformation of wine compounds over time in barrel or bottle; the Maillard reaction, polymerization, and oxidative reactions
- **Categories**: Woody (oak), Earthy (forest floor, truffle), Nutty (oxidative aging), some Caramelized, some Fruity-Dried
- **Development stage association**: **Developing to Complex** — tertiary aromas indicate a wine in or approaching its drinking window

**Examples**:
- Cedar, tobacco, cigar box → Tertiary; French oak transformation over years of bottle aging
- Forest floor, undergrowth, truffle → Tertiary; aged Burgundy transformation
- Leather, saddle → Tertiary; phenolic transformation in aged red wines
- Petrol/kerosene → Tertiary; TDN formation in aged Riesling
- Dried fruit, fig, marmalade → Tertiary; fruit concentration and drying over long bottle aging

### Development Stage Mapping

| Aroma Character | Development Stage | Interpretation |
|---|---|---|
| Primary fruit dominant; fresh, vibrant | **Youthful** | Wine is young; may benefit from aging or is drinking as designed |
| Primary fruit still present + secondary beginning to emerge | **Vinous** | Wine is transitioning out of youth |
| Primary and secondary present + tertiary emerging | **Developing** | Wine is approaching its window; a preview of full complexity |
| All three tiers present; no single tier dominant | **Complex** | Wine is in its window; drinking at or near peak |
| Primary and secondary faded; tertiary fading; flat | **Tired** | Wine is past its window; aging has progressed past peak complexity |

---

## Diagnostic Mapping — Aroma to Identity

Use these mappings as deductive shortcuts when a specific aroma is detected. Always confirm with structural evidence from the full grid.

| Aroma Detected | What It Suggests | Confirmation Markers |
|---|---|---|
| Cassis + black currant leaf + cedar | Cabernet Sauvignon | High-Med tannin (grippy); full body; long finish |
| Rose petal + pomegranate + earth | Pinot Noir | Low-Med tannin; high acid; garnet translucent color |
| Violet + tar + dried cherry | Nebbiolo | High tannin (chalky); very high acid; garnet-tawny; long aging potential |
| Peach + petrol / kerosene | Aged Riesling | High acid; low-medium body; light color; the petrol indicates TDN from aging |
| White pepper + mineral | Grüner Veltliner | High acid; medium body; white wine; the pepper is rotundone from the grape |
| White pepper + dark fruit + olive | Northern Rhône Syrah | Medium-high tannin; full body; white pepper is rotundone |
| Lychee + rose water + ginger | Gewürztraminer | Low acid; full body; off-dry to sweet tendency; distinctive spice |
| Jasmine + peach + apricot | Viognier | Low acid; full body; richly textured; southern Rhône or varietal |
| Passion fruit + grapefruit + cut grass | Marlborough Sauvignon Blanc | High acid; Med body; green notes from pyrazines; tropical thiols (4-MMP) |
| Band-aid + barnyard | Brettanomyces | Assess level; low = Old World complexity; high = fault; route to fault-diagnosis |
| Struck match + rubber | Reduction (H2S/mercaptan) | Aerate first; if it blows off: H2S; if persistent: mercaptans (fault) |
| Wet cardboard + muted fruit | TCA (cork taint) | Return the bottle; no threshold for acceptability |
| Vanilla + coconut + ripe dark fruit | New American oak | New World red or Rioja in American oak; Cabernet or Tempranillo likely |
| Cedar + tobacco + blackcurrant | French oak + Cabernet | Bordeaux or Napa Cabernet; aged in French oak barrels |
| Brioche + cream + yeast | Champagne autolysis / lees | Traditional method sparkling; quality indicator in Champagne; also aged sur lie whites |
| Roasted hazelnut + lemon curd + mineral | Aged white Burgundy | Chardonnay; French oak + time on lees; Meursault/Puligny-Montrachet |
| Gunflint + oyster shell + lemon | Chablis | High acid; mineral; unoaked Chardonnay from Kimmeridgian limestone |
| Petrichor + peach blossom + honey | Aged Alsace Riesling or Chenin | Complex tertiary development; in window; noble variety with age |
| Dried apricot + orange peel + walnut + caramel | Madeira | Oxidative aging + residual sugar + long barrel time; unmistakable |
| Honey + dried apricot + noble rot | Sauternes / Botrytized wine | Botrytis cinerea concentration; Sémillon dominant in Sauternes |
| Leather + tobacco + dark earth | Aged red (tertiary) | Wine in its window; likely 10+ years; Bordeaux, Barolo, aged Rioja |

---

## Learn Block

After substantive responses using this skill:

```learn
Learn ─── Quality Assessment
Next: With precise aroma vocabulary in place, you can now assess quality analytically — BLIC shows you how to weigh everything you've described against a rigorous standard.
```
