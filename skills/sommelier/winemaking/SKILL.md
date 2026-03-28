---
name: winemaking
description: >
  Route winemaking questions — viticulture, vinification, special production
  methods, and alternative techniques — to the correct specialist knowledge.
  Use when the user wants to understand how wine is grown or made, how sparkling
  or fortified wines are produced, or what distinguishes natural, orange, or
  biodynamic wine from conventional production.
tools: Read
---

# Winemaking — The Vigneron

## Description
Master routing intelligence for all winemaking and viticulture questions. Distinguishes between farming philosophy, cellar technique, specialized production methods, and alternative approaches. Presents traditional and modern techniques fairly when they conflict, and routes to grape-encyclopedia when a production question is really about how a particular variety expresses its character through the winemaking choices made for it.

## Skill Type
**Director** — routes to sub-skills; does not answer directly

## Routing Table

| Query Type | Route To |
|---|---|
| Farming methods, vine training, canopy management | `viticulture` |
| Organic vs biodynamic vs conventional farming | `viticulture` |
| Phylloxera, rootstocks, vine age | `viticulture` |
| Harvest timing decisions, yield control | `viticulture` |
| Fermentation process (yeast, temperature, vessels) | `vinification` |
| Maceration techniques (punch-down, pump-over, cold soak) | `vinification` |
| Malolactic fermentation and its effect | `vinification` |
| Oak treatment, fining, filtration | `vinification` |
| Sulfur dioxide use and the natural wine SO₂ debate | `vinification` |
| Champagne/sparkling wine production | `special-methods` |
| Port, Sherry, Madeira fortified wine production | `special-methods` |
| Botrytis, ice wine, passito/appassimento sweet wines | `special-methods` |
| Amarone making (appassimento process) | `special-methods` |
| Natural wine philosophy and practice | `alternative-winemaking` |
| Orange/amber wine (skin-contact whites) | `alternative-winemaking` |
| Pét-nat and ancestral method sparkling | `alternative-winemaking` |
| Clay, concrete, amphora, and qvevri winemaking | `alternative-winemaking` |
| Carbonic and semi-carbonic maceration | `alternative-winemaking` |
| Whole cluster fermentation | `alternative-winemaking` |
| Biodynamic winemaking calendar and practice | `alternative-winemaking` |

## Multi-Skill Scenarios

### Scenario 1: Amarone Production
**Query:** "How is Amarone della Valpolicella made?"
**Analysis:** The defining characteristic of Amarone is appassimento — grape drying after harvest. This is a special production method that goes beyond standard vinification.
**Route:** `special-methods` (passito/appassimento section)
**Note:** If the user follows up asking about the Corvina grape and its character, route to `grape-encyclopedia/indigenous-varieties`.

### Scenario 2: Organic vs Biodynamic
**Query:** "What's the difference between biodynamic and organic farming?"
**Analysis:** Both are farming philosophies, not winemaking techniques. The distinction lives in the vineyard.
**Route:** `viticulture` (Farming Philosophy section)
**Note:** If the user then asks about biodynamic calendars and tasting-day implications, route to `alternative-winemaking` (biodynamic winemaking).

### Scenario 3: Pét-Nat Explained
**Query:** "What exactly is pét-nat and how is it different from Champagne?"
**Analysis:** Pét-nat (pétillant naturel) is the ancestral method of sparkling wine production, and the question explicitly requests a comparison to traditional method Champagne.
**Route:** `alternative-winemaking` (pét-nat section), with cross-reference to `special-methods` (Champagne/méthode traditionnelle)
**Note:** The comparison requires both sub-skills. Handle in sequence: define pét-nat fully, then reference the méthode traditionnelle contrast.

### Scenario 4: Carbonic Maceration
**Query:** "Why does Beaujolais Nouveau taste like banana and bubblegum?"
**Analysis:** The banana/bubblegum aroma in Beaujolais Nouveau is caused by isoamyl acetate produced during carbonic maceration fermentation. This is an alternative/special winemaking technique.
**Route:** `alternative-winemaking` (carbonic/semi-carbonic maceration section)

### Scenario 5: Oak and MLF Interaction
**Query:** "What is malolactic fermentation and why does it make Chardonnay taste buttery?"
**Analysis:** MLF is a cellar technique. The "buttery" character (diacetyl) is a direct product of the lactic acid conversion. Standard vinification topic.
**Route:** `vinification` (Malolactic Conversion section)

### Scenario 6: Yeast Philosophy
**Query:** "What's the argument for wild yeast versus commercial yeast?"
**Analysis:** Yeast selection is a fundamental winemaking decision touching fermentation philosophy, natural wine values, and practical risk management.
**Route:** `vinification` (Fermentation section, wild vs cultured yeast), with possible escalation to `alternative-winemaking` if the user wants to explore the natural wine context of the debate

## Curriculum Order

For learners building winemaking knowledge systematically, the order follows the wine's journey from vine to bottle:

1. **`viticulture`** — Start in the vineyard. Everything begins here. The quality, health, and character of the grapes determines the ceiling of what the winemaker can achieve. "You cannot make a great wine from bad grapes, but you can make a bad wine from great grapes."

2. **`vinification`** — Move into the cellar. How grapes are handled from crush to bottling: fermentation, maceration, oak, fining, and stabilization. The technical foundation of winemaking.

3. **`special-methods`** — Once standard winemaking is understood, explore the specialist techniques: sparkling wine production, fortification, and the full spectrum of sweet wine methods. These are vinification taken to logical extremes or supplemented with additional processes.

4. **`alternative-winemaking`** — The natural wine movement, orange wine, pét-nat, and vessel alternatives are best understood in contrast to the conventional winemaking described in viticulture and vinification. The contrast sharpens both.

## Conflict Resolution

### Traditional vs Modern Winemaking Debates
When traditional and modern techniques conflict, present both positions fairly. These debates are not settled — they represent genuine philosophical disagreements among serious producers:

**The Barolo Wars (Traditional vs Modern):**
- *Traditional:* Extended maceration (60–90 days), large Slavonian oak botti (10,000L+), decades required before drinking. Producers: Giacomo Conterno, Bartolo Mascarello, Giuseppe Rinaldi.
- *Modern:* Short maceration (7–10 days), small French barrique, rotary fermenters, accessible within 5–8 years. Producers (1990s): Angelo Gaja (partially), Elio Altare, Paolo Scavino.
- *Resolution:* Both produce world-class wines. The debate has largely resolved into a spectrum where most serious producers are neither purists nor modernists. The market is comfortable with both. Neither is "correct."

**Sulfur Dioxide (The Natural Wine Debate):**
- *Conventional view:* SO₂ is a safe, well-understood preservative essential for wine stability during transport, storage, and aging. Without it, wines are fragile and inconsistent.
- *Natural wine view:* Minimal or zero SO₂ produces more "alive" wines with more terroir expression. The risk of instability is acceptable and honest.
- *Resolution:* Present both positions. Acknowledge that very low-SO₂ winemaking can produce extraordinary wines (and also flawed ones). Acknowledge that high-SO₂ winemaking can produce stable but characterless wines (and also great ones). The dose and timing matter more than the binary debate suggests.

**Oak (New vs Neutral):**
- *New oak advocates:* Adds structure, complexity, vanilla, toast, cedar. In the right proportions, integrates and enhances. Traditional Bordeaux, Napa, and Rioja.
- *Anti-oak view:* Masks terroir, homogenizes flavor profiles, creates internationally styled wines disconnected from their origin. Natural wine movement default.
- *Resolution:* The question is proportion and integration, not presence or absence. A 12-month élevage in 25% new French oak on a serious Pinot Noir is not the same as 18 months in 100% new American oak on a Barossa Shiraz. Both are "new oak" but the effect is completely different.

## Scope Boundaries

### Escalate to `grape-encyclopedia` when:
- The winemaking question is really about **how a variety expresses itself**: "Why does Chardonnay taste so different in Chablis vs Napa?" is about grape expression shaped by terroir and winemaking — route to `grape-expression`.
- The user asks about **which variety is best suited to a technique**: "What grapes work best for skin-contact whites?" — this requires variety knowledge (grape-encyclopedia) alongside alternative-winemaking.
- A specific variety's natural affinity with a technique: "Why is Syrah co-fermented with Viognier in Côte-Rôtie?" — grape-expression provides the context; vinification provides the technical explanation.

### Stay within `winemaking` when:
- The question centers on **process, technique, philosophy, or equipment** rather than the grape's intrinsic character.
- The user wants to understand **why a winemaker makes a specific choice**, regardless of what variety is involved.
- The question concerns **farming decisions** (yield, training, certification), **cellar decisions** (yeast, oak, filtration), or **specialist production methods** (sparkling, fortified, sweet).
