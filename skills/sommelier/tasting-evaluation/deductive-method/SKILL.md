---
name: deductive-method
description: >
  Apply the Court of Master Sommeliers Deductive Tasting Grid to systematically
  evaluate any wine. Use when describing a wine from scratch, practicing blind
  tasting, or building a structured evidence chain from sight through nose
  through palate to a final conclusion about grape, region, and vintage.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
---

# The Deductive Method — The Grid

## skill-metadata
- skill-id: sommelier/tasting-evaluation/deductive-method
- skill-type: knowledge
- parent: sommelier/tasting-evaluation
- version: 1.0.0
- references: deductive-method/references/deductive-grid-schema.md

## description
Encodes the CMS Deductive Tasting Grid as structured reasoning knowledge. Covers the full four-phase sequence — Sight, Nose, Palate, Conclusion — and teaches students to build a logical evidence chain from visual observation through to grape, region, and vintage identification. Essential foundation for blind tasting, exam preparation, and structured wine description.

---

## When This Applies

Use this skill when the user is:
- Working through a blind tasting and needs to know what to observe and in what order
- Describing a wine in structured, exam-ready language
- Trying to identify a wine from its observable characteristics
- Preparing for CMS (Court of Master Sommeliers), WSET, or BNIC exams
- Learning to write a professional tasting note
- Conducting pairing research that requires understanding a wine's structural profile

---

## The Grid Structure

The deductive grid is not a checklist. It is a **detective's case file** built in real time.

Each phase produces evidence. Each piece of evidence narrows the field of possibilities. By the time you reach the Conclusion, you have assembled enough facts to make an informed deductive leap — not a guess, but a reasoned argument.

The sequence is non-negotiable:

1. **Sight** — Establishes what the wine looks like before any expectation is formed by smell or taste. Color, clarity, and development are assessed cold.
2. **Nose** — First sensory engagement. Condition is assessed first (clean or flawed?). If flawed, the investigation pivots to fault diagnosis before continuing. If clean, intensity, development, and aroma categories are mapped.
3. **Palate** — The structural measurement. Sweetness, acid, tannin, alcohol, body, texture, and finish are assessed in sequence. These are the data points that will drive the conclusion.
4. **Conclusion** — The deductive leap. Using all evidence from Sight, Nose, and Palate together, reason toward: grape variety (or blend), region/appellation, vintage range, and quality level.

Think of it this way: Sight is the crime scene. Nose is the witness statement. Palate is the forensic evidence. Conclusion is the closing argument.

---

## SIGHT

### Clarity
- **Clear** — No suspended particles; normal and expected in most commercial wines
- **Hazy** — Could indicate unfiltered/unfined wine (common in natural wines, some Champagnes sur lie), a fault (protein instability, refermentation), or simply serving temperature effects. Note without alarm; context matters.

### Brightness
- **Dull** — May indicate age, filtration issues, or low acidity
- **Bright** — Normal healthy wine
- **Day-Bright** — Vivid, luminous; often signals freshness and good acid
- **Brilliant** — Exceptional clarity and luminosity; often young, high-acid wines or precisely made still wines

### Color — White Wines
Work from youngest to oldest. Color deepens with age, botrytis, oxidation, and warmer climates.

| Color | Suggests |
|---|---|
| Water-white | Very young, neutral variety (e.g., Pinot Grigio, Muscadet), possibly reductive winemaking |
| Straw | Young, fresh; classic for unoaked whites (Sauvignon Blanc, young Chardonnay) |
| Yellow | Some age or medium ripeness; possibly light oak, warmer climate, or a year of bottle age |
| Gold | Significant oak aging, late harvest concentration, botrytis, or 3–8+ years of age |
| Amber | Oxidative aging (Sherry, Madeira, aged Rioja Blanco, skin-contact "orange" wines), or significant age |
| Brown | Deep age or oxidation — may be intentional (Tawny Port, PX Sherry, old Sauternes) or a fault |

### Color — Red Wines
Red wines lose color and shift from blue/purple hues toward garnet and then brick/tawny as they age.

| Color | Suggests |
|---|---|
| Purple | Very young, primary fruit, high anthocyanin; likely < 3 years old (young Zinfandel, Malbec, Syrah) |
| Ruby | Youthful to mid-aged; most red wines in their drinking window fall here |
| Garnet | Some development; translucency increasing; common in Pinot Noir, aged Cabernet, Sangiovese |
| Tawny | Significant age or oxidative aging; Nebbiolo (Barolo/Barbaresco) develops tawny tones; also Port styles |
| Brown | Advanced age, heat damage, or heavy oxidation — a fault indicator if unintentional |

### Rim Variation
The color at the rim (thin edge of the tilted glass) vs the core (center of the wine) is one of the most reliable age indicators.

- **No variation (rim = core)** — Young wine; anthocyanins still fully intact
- **Color difference (rim paler/more orange than core)** — Age; anthocyanins are polymerizing and precipitating. An orange or brick rim on a red wine is a strong indicator of maturity (5+ years, or earlier in a warm vintage or lighter variety like Pinot Noir)
- **Wide variation** — Significant age; the wine is in or past its window

### Viscosity / Legs / Tears
The streaks of wine that run down the inside of the glass after swirling are caused by the **Marangoni effect** — surface tension differential between water and alcohol.

- **Thick, slow legs** → Higher alcohol and/or residual sugar
- **Thin, fast legs** → Lower alcohol
- **What they do NOT indicate**: Quality. Legs/tears are not a quality marker. Never use them to compliment or criticize a wine. This is one of the most common misconceptions in wine service.

### Gas Bubbles
- **Persistent fine bubbles rising from a point** — Traditional method sparkling wine (tirage creates nucleation points)
- **Few large bubbles at rim** — Charmat/tank method or slight carbonation
- **Bubbles in a still wine** — Possible slight refermentation in bottle; may be a flaw, or intentional in some styles (Vinho Verde, Txakoli, Muscadet pétillant naturel)

### Sediment
- **Fine powdery deposit** — Tartrate crystals (not a fault; temperature-induced precipitation); or fine lees in unfiltered wine
- **Chunky dark sediment** — Tannin-pigment polymers from age in red wine; expected in aged Cabernet, Vintage Port, old Rhône
- **Cork bits** — Service issue, not a wine fault

### Staining
- **Deep staining on the glass above the wine line** — High extract, likely a full-bodied, concentrated red; also older wines where tannin polymerization has created sediment

---

## NOSE

### Step 1 — Condition: Clean vs Flawed
Before anything else: is the wine clean?

- **Clean** — Proceed with intensity, development, and aroma assessment
- **Flawed** — Stop. Identify which fault descriptor applies. Route to `fault-diagnosis` skill for systematic identification and "send it back?" protocol. Common triggers: wet cardboard (TCA/cork taint), vinegar (VA), nail polish (ethyl acetate), rotten eggs (reduction/H2S), musty basement (TCA), bandaid (brett). Do not continue the grid until condition is assessed.

### Intensity
How powerfully do the aromas present themselves without swirling, and after?

- **Delicate** — Restrained; aromas require concentration to detect; common in cool-climate aromatic whites (Mosel Riesling), aged wines where aromatics have faded
- **Moderate** — Clearly present but not dominating; most mid-range wines
- **Powerful** — Aromas leap from the glass; concentrated; common in warm-climate varieties, late harvest, some Burgundy Grand Cru

Intensity is diagnostic: high intensity + low alcohol is a marker of cool-climate concentration (sugar ripeness separate from flavor ripeness). High intensity + high alcohol is a warm-climate marker.

### Development / Age
- **Youthful** — Primary fruit dominant; fresh, vibrant, uncomplex
- **Vinous** — The wine is "winey" rather than specifically fruity; some development beginning
- **Developing** — Secondary and early tertiary aromas emerging alongside primary fruit; the transition stage
- **Complex** — Multiple aroma layers; primary + secondary + tertiary all present; the wine has fully evolved
- **Tired/Over the Hill** — Aromas have faded, oxidized, or lost definition; the window has closed

### Fruit Condition
Fruit condition tells you about climate, harvest timing, and hang time.

| Descriptor | What It Implies |
|---|---|
| Tart | Cool climate or early harvest; high acid; characteristic of cool-climate Burgundy, Germany, Champagne base wines |
| Ripe | Optimal ripeness; balance of freshness and flavor development; moderate climate or ideal vintage |
| Overripe | Warm climate or late harvest; rich and lush; characteristic of Napa Cabernet, Barossa Shiraz, warm vintages |
| Jammy | Very warm climate or very ripe harvest; cooked berry quality; can signal high sugar/alcohol |
| Candied | Residual sugar influence or very ripe; some dessert wines; some New World styles |
| Baked | Heat stress during growing season; sun-baked quality; can indicate vintage heat events or storage heat damage |
| Dried | Age-related concentration, or dried fruit styles (Amarone, Passito); also late harvest |
| Bruised | Oxidative damage or poor fruit selection; can indicate brett-compromised fruit |

### Fruit Types — Diagnostic Value

**Citrus**: Lemon, lime, grapefruit, yuzu, lemon curd
- Diagnostic: High-acid whites; cool climates; Riesling (lime, lemon), Sauvignon Blanc (grapefruit, lime), Chardonnay (lemon, grapefruit at cool end), Champagne base wines, Txakoli

**Stone Fruit**: Peach, apricot, nectarine, plum, cherry, cherry pit
- Diagnostic: White stone fruit (peach, apricot) = Viognier, warmer Riesling, white Burgundy, Gewürztraminer; Red stone fruit (plum, cherry) = Pinot Noir, Sangiovese, Grenache, Barbera

**Tropical Fruit**: Mango, pineapple, passion fruit, guava, banana
- Diagnostic: Warm climate or new world whites; Marlborough Sauvignon Blanc (passion fruit), warm Chardonnay (pineapple), Viognier in warm sites; also Champagne (pineapple, banana in riper dosage styles)

**Berry Fruit**: Strawberry, raspberry, blackberry, blackcurrant (cassis), blueberry, cranberry
- Diagnostic: Strawberry/raspberry = Pinot Noir, cool Grenache, Gamay; Blackberry = Syrah, Zinfandel, Malbec; Cassis = Cabernet Sauvignon (signature aroma); Blueberry = Malbec, Primitivo; Cranberry = cool-climate Pinot Noir, Nebbiolo

**Tree Fruit**: Apple, pear, quince
- Diagnostic: Green apple = Chardonnay (especially unoaked), Pinot Gris, Chablis; Ripe apple = Alsace Pinot Gris, aged white Burgundy; Pear = Viognier, Austrian whites, Pinot Blanc

**Dried Fruit**: Fig, date, raisin, prune, dried apricot, dried cherry
- Diagnostic: Age or concentration; Amarone/Recioto (dried cherry/fig); aged Barolo (dried rose, cherry); Tawny Port (fig, date, raisin); Sauternes aged (dried apricot, marmalade)

### Non-Fruit Aromas

**Floral**
- Rose (dried vs fresh) → Pinot Noir, Nebbiolo (dried rose, violet), Gewürztraminer (rose petal), Grenache
- Violet/Iris → Nebbiolo (key signature), Malbec, Cabernet Franc
- White flowers (jasmine, honeysuckle, orange blossom) → Viognier (signature), Riesling, Muscat, Torrontés
- Acacia → Young Riesling, Soave (Garganega), Grüner Veltliner

**Herbal / Vegetal**
- Green pepper/capsicum (pyrazines) → Cabernet Sauvignon (cool climate), Cabernet Franc (characteristic), Sauvignon Blanc
- Asparagus → Sauvignon Blanc (can indicate overripe/under-ripe pyrazines), Grüner Veltliner
- Olive tapenade → Cabernet Sauvignon, Syrah (Provençal garrigue)
- Herbes de Provence/garrigue → Southern Rhône, Provençe, Languedoc
- Mint/eucalyptus → Australian Cabernet (Coonawarra especially), some Chilean Cabernet
- Fresh herbs (thyme, rosemary, lavender) → Grenache, Southern Rhône

**Spice**
- White pepper → Grüner Veltliner (signature; rotundone), Northern Rhône Syrah (signature)
- Black pepper → Syrah/Shiraz broadly, Zinfandel
- Cinnamon, clove → Gewürztraminer (spice character), some Grenache, some oak
- Star anise/licorice → Cabernet Sauvignon, Malbec, some Grenache
- Note: grape-derived spice (rotundone = pepper in GV/Syrah) vs oak-derived spice (vanilla, clove, nutmeg from barrel)

**Earth / Mineral**
- Forest floor, leaf litter, undergrowth → Aged Pinot Noir (Burgundy), aged Cabernet
- Wet stone, flinty, gunflint → Chablis (Kimmeridgian limestone), Loire Muscadet, Sancerre
- Chalk, limestone → White Burgundy, Champagne, Sancerre
- Volcanic ash, smoke, graphite → Etna wines, Austrian Grüner Veltliner (volcanic sites), some Ribera del Duero
- Iron, blood → Old-vine Pinot Noir, some aged Barolo
- Petrichor (rain on dry earth) → Aged Riesling, some aged Grenache

**Oak Markers**
- Vanilla → American oak (lactones); very common in Rioja Crianza/Reserva, New World Chardonnay
- Cedar, pencil shavings → French oak; Bordeaux, Napa Cabernet, aged Rioja Gran Reserva
- Toast, charred wood, smoke → Heavily toasted barrels; some New World reds, Californian Chardonnay
- Coconut → American oak (specifically oaklactone); new American oak barrels
- Butterscotch, toffee → Oak + partial oxidation; can also indicate diacetyl (MLF marker)
- Resin, sawdust → New or cheap oak; a sign of poor oak integration

**Biological**
- Brettanomyces (bandaid, barnyard, horse stable) → Brettanomyces yeast contamination; see fault-diagnosis
- Reduction (struck match, rubber, gunflint at high intensity) → H2S; see fault-diagnosis; low level can be stylistic
- Lees/autolysis (brioche, cream, biscuit, bread dough) → Extended sur lie aging; Champagne, Muscadet, aged white Burgundy
- Butter/cream → Malolactic fermentation; typical in barrel-fermented Chardonnay

---

## PALATE — Structure

The palate is where you **measure**, not just describe. Each structural element has a defined scale.

### Sweetness (Residual Sugar)
| Level | RS Range | Sensory |
|---|---|---|
| Bone Dry | < 1 g/L | No sweetness whatsoever; pure dryness |
| Dry | 1–4 g/L | Dry to the perception; trace sugar masked by acidity |
| Off-Dry | 4–12 g/L | Perceptible sweetness but not dominant; food-friendly |
| Medium-Dry | 12–45 g/L | Clear sweetness; typical of Spätlese Riesling |
| Medium-Sweet | 45–120 g/L | Noticeably sweet; Auslese range |
| Sweet | 120–220 g/L | Dessert wine range; Beerenauslese, late harvest |
| Dessert | 220+ g/L | Intensely sweet; TBA, Eiswein, PX Sherry, Sauternes |

Note: perceived sweetness is modulated by acidity. A wine with 20 g/L RS and very high acid can taste medium-dry; a wine with 8 g/L RS and low acid can taste medium-sweet.

### Tannin (Red wines and some skin-contact whites)

**Level scale:**
| Level | Description |
|---|---|
| Low | Barely perceptible grip; light red varieties (Pinot Noir, Gamay) |
| Med- | Light tannin with some presence; Grenache, lighter Tempranillo |
| Medium | Noticeable but integrated; mid-weight reds |
| Med+ | Pronounced structure; firm without being harsh; Cabernet, Sangiovese |
| High | Significant grip and drying effect; young Barolo, young Cabernet, tannic Malbec |

**Nature descriptors (always include these — level alone is insufficient):**
- **Fine-grained / silky** — Small, polymerized tannins; well-made, possibly aged; Pinot Noir, fine Cabernet with age
- **Chalky** — Powdery texture coating the gums; typical of limestone-grown varieties (Sangiovese, Nebbiolo), some Loire Cabernet Franc
- **Grippy** — Textural, dry without being harsh; often a sign of quality in tannic varieties
- **Drying** — Pulls moisture from the gums and cheeks; can be from tannin level or tannin nature (green/unripe tannins)
- **Green / stalky** — Unripe tannins from under-ripe or stemmy fruit; bitter, herbaceous tannin character; a fault in excess
- **Ripe** — Tannins polymerized and softened; fruit in balance; indicates optimal harvest timing or bottle age
- **Coarse / aggressive** — Young, extracted tannins from over-extraction or poor fruit; barrel aging should integrate these

### Acidity

**Level scale:**
| Level | Sensory Cue |
|---|---|
| Low | Flat, round, no salivation; the wine feels fat or flabby |
| Med- | Mild refreshment; gentle mouthwatering |
| Medium | Noticeable freshness; persistent salivation on the sides of the tongue |
| Med+ | Vibrant; strong salivation; mouthwatering; refreshing finish |
| High | Intense; tart; salivation is strong and immediate; may feel sharp |

**How to assess acidity on the palate**: After swallowing, track how much saliva returns under the tongue and along the sides of the mouth. More saliva = higher acid. This is the most reliable assessment method — do not confuse acid with tannin (tannin dries; acid salivates).

### Alcohol

| Level | % ABV | Sensory Cue |
|---|---|---|
| Low | < 11% | No warmth; light, sometimes watery |
| Med- | 11–12.5% | Mild warmth; subtle presence |
| Medium | 12.5–13.5% | Moderate, integrated warmth; most European table wines |
| Med+ | 13.5–14.5% | Noticeable warmth on the finish and throat |
| High | 14.5%+ | Pronounced heat; warming sensation persists; common in Zinfandel, Amarone, Châteauneuf-du-Pape, fortified wines |

Alcohol is felt as **heat** on the finish and back of the throat. Distinguish alcohol heat from tannin grip and from acid sharpness — they are felt in different locations and sensations.

### Body
Body is the overall weight and viscosity in the mouth — a combination of alcohol, residual sugar, glycerol, and extract.

| Level | Reference Point |
|---|---|
| Light | Skim milk; Pinot Grigio, Muscadet, Gamay |
| Medium- | Between skim and whole milk |
| Medium | Whole milk; most mid-weight wines |
| Medium+ | Between whole milk and cream |
| Full | Heavy cream; Amarone, Châteauneuf-du-Pape, Sauternes |

### Texture
Beyond body, texture describes how the wine feels as it moves:
- **Creamy** — MLF, lees contact, or richness from oak
- **Silky** — Fine tannins, good integration; aged wine
- **Grippy** — Structural tannin; youth or variety character
- **Oily / waxy** — Some Riesling (kerosene note), Condrieu, old white Burgundy
- **Tingly** — CO2 (slight spritz in some still wines)
- **Astringent** — Drying, puckering; high tannin or acid; not a compliment in excess

### Complexity
Does the wine offer layers? Do the flavors evolve on the palate, transition mid-palate, and reveal something different on the finish? A complex wine tells a story across the tongue from attack to finish; a simple wine is one-dimensional.

### Finish Length
| Level | Duration | Notes |
|---|---|---|
| Short | < 30 seconds | Flavors fade quickly after swallowing; indicator of lower quality |
| Medium | 30–45 seconds | Acceptable persistence; most table wines |
| Long | > 45 seconds | Flavors persist and evolve; quality indicator |
| Very Long | > 60 seconds | Grand Cru level; wines of exceptional concentration and quality |

The finish should also be assessed for **quality**: is it clean, bitter, tannic, acidic, or alcoholic? A long but harsh finish is not a virtue.

---

## CONCLUSION — The Deductive Leap

The conclusion is where all evidence is synthesized. Work in this order:

### Step 1 — Climate Determination

**Cool Climate Markers**
- High acidity (Med+ to High)
- Lower alcohol (< 13% in reds, < 12.5% in whites)
- Lighter body
- Tart to ripe fruit (not jammy)
- Herbal, mineral, and floral notes prominent
- Lighter color in reds; more water-white to straw in whites
- Examples: Burgundy, Mosel, Champagne, Loire, New Zealand Marlborough, Oregon

**Warm Climate Markers**
- Lower to medium acidity
- Higher alcohol (> 13.5% in reds, > 13% in whites)
- Fuller body
- Ripe to jammy fruit
- Less herbal; more fruit-forward with spice
- Deeper color in reds (purple-ruby); deeper gold in whites
- Examples: Southern Rhône, Napa, Barossa Valley, Priorat, Mendoza, McLaren Vale

**Moderate/Maritime Climate**: Balance of freshness and ripeness; Bordeaux, Willamette Valley, Margaret River

### Step 2 — Old World vs New World Style

| Marker | Old World Tendency | New World Tendency |
|---|---|---|
| Fruit character | Tart, restrained, subtle | Ripe, forward, expressive |
| Oak | Integrated, older barrels, subtle | More evident new oak, vanilla, coconut |
| Acid | More prominent | Often lower |
| Alcohol | Generally lower | Generally higher |
| Terroir expression | Primary driver | Variety and winemaker-driven |
| Tannin (reds) | Chalky, earthy, structured | Riper, rounder, plummy |
| Earthiness | More prominent | Less prominent; fruit-forward |

### Step 3 — Grape Identification by Structural Signature

**White Wines**

| Structural Signature | Likely Grape |
|---|---|
| High acid + floral (white flowers) + low alcohol + petrol/kerosene with age | Riesling |
| High acid + grassy/herbaceous + grapefruit/passionfruit + pyrazine | Sauvignon Blanc |
| Med-high acid + stone fruit + white flower + full body | Viognier |
| Med acid + lemon/apple + nutty/toasty if oaked + creamy texture | Chardonnay |
| Med acid + white peach/apricot + rose water + lychee + spice | Gewürztraminer |
| High acid + mineral + green apple + slight spritz | Grüner Veltliner or Muscadet |
| High acid + mineral + white flower + waxy texture | Chenin Blanc |

**Red Wines**

| Structural Signature | Likely Grape |
|---|---|
| High acid + high tannin (chalky) + dried rose/violet/tar + garnet to tawny | Nebbiolo (Barolo/Barbaresco) |
| Med acid + grippy tannin (Med+) + cassis + cedar + tobacco + full body | Cabernet Sauvignon |
| High acid + Med tannin + cherry + earthy + garnet | Sangiovese (Chianti/Brunello) |
| Med-high acid + low-med tannin + strawberry/raspberry + earthy + silky | Pinot Noir |
| Med acid + low tannin + red berry + floral + light body | Gamay (Beaujolais) |
| Med-low acid + Med tannin + blueberry + spice + full body | Malbec |
| Med acid + Med+ tannin + dark fruit + white pepper + black olive | Syrah/Shiraz |
| Med-low acid + Med tannin + red fruit + garrigue + spice | Grenache |
| Med acid + high alcohol + blackberry/jam + pepper + full body | Zinfandel/Primitivo |
| Med acid + Med+ tannin + plum/fig + tobacco + full body | Tempranillo |

### Step 4 — Region Narrowing

Once the grape is identified, narrow by structural intensity and style markers:

- Nebbiolo → high acid + chalky tannin + garnet-tawny → Barolo (more power) or Barbaresco (more elegance) → estimate age from development stage
- Cabernet → cedar dominates, restrained → Bordeaux left bank; ripe cassis + mint → Napa; eucalyptus → Coonawarra
- Pinot Noir → earthy + foresty → Burgundy; red fruit + brighter → Oregon or New Zealand
- Chardonnay → steely + no oak + high acid → Chablis; toasty + full + butter → Meursault or New World oaked
- Riesling → petrol + high acid + slate → Mosel; lime + full → Clare Valley; orange peel + complex → Alsace

### Step 5 — Vintage Assessment

- **Color (red wines)**: Purple-ruby = young (< 3 years typically). Ruby-garnet = mid-age (3–8 years). Garnet-tawny = older (8–15+ years). Brown edge = very old or heat-damaged.
- **Development stage**: Youthful = young vintage; Developing = approaching or in window; Complex = peak; Tired = past window
- **Tannin texture**: Young = grippy/drying; Mature = silky/integrated; Old = soft/fading
- **Cross-check**: Color age estimate + nose development + tannin texture should all align. If they don't, reason through why.

---

## Quick Reference

The full grid with decision trees, diagnostic implications, and common misreads is in:
`tasting-evaluation/deductive-method/references/deductive-grid-schema.md`

---

## Learn Block

After substantive responses using this skill:

```learn
Learn ─── Aroma Lexicon
Next: Noble's Wheel gives you the vocabulary to describe what you just detected on the nose — the grid tells you where to look; the lexicon gives you the words.
```
