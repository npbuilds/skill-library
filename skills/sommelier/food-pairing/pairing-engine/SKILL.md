---
name: pairing-engine
description: >
  Generate 3-5 structured wine recommendations for any dish across entry,
  mid-range, and premium price tiers. Use when the user describes a specific
  dish and wants concrete wine suggestions with reasoning. Also handles reverse
  pairing (user has a wine, wants food suggestions) and flags impossible
  pairings with honest alternatives.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read
---

# The Pairing Engine — The Matchmaker

**Type:** Action
**Suite:** Bacchus

## Description
Generates specific wine pairing recommendations for any dish, cuisine, or occasion. Accepts dish descriptions, ingredient lists, or cuisine styles as input. Runs a structured five-step analysis — weight matching, elimination constraints, pairing strategy, tiered recommendations, and error flagging — and outputs a prioritized list with clear rationale. Handles reverse pairing (wine-first) and flags genuinely difficult pairings honestly.

---

## How to Run

### Input
Accept any of the following input forms — the more detail, the more precise the recommendation:
- **Specific dish name:** "Chicken tikka masala", "Boeuf bourguignon", "Grilled branzino with lemon and capers"
- **Ingredient list:** "Pork belly, kimchi, gochujang, sesame, rice"
- **Cuisine style + protein:** "Moroccan lamb"
- **Cooking method + protein:** "Charcoal-grilled beef short ribs"
- **Occasion type:** "Wine list for a 10-course Italian tasting menu", "Bottles for a casual BBQ"
- **Budget range:** Accept alongside any of the above
- **Reverse pairing:** "I have a 2019 Barolo — what should I cook?" or "We're opening a white Burgundy tonight — what's for dinner?"

---

### Step 1: Identify the Dominant Structural Elements of the Dish

Analyze the dish against these five dimensions before making any recommendations:

**Weight (light / medium / heavy):**
Determined by fat content, cooking method, sauce richness, and ingredient density.
- Light: ceviche, sashimi, steamed fish, light salads, fresh pasta with olive oil
- Medium: roasted chicken, pasta in tomato sauce, grilled salmon, pork tenderloin
- Heavy: braised short ribs, cassoulet, beef Wellington, duck confit, mole negro, tagine

**Acid level (low / medium / high):**
- Low: plain cream sauces, butter-based preparations, grilled meat with no sauce
- Medium: tomato-based preparations, light citrus, mild fermentation
- High: ceviche (lime-cured), vinaigrette-dressed dishes, kimchi-based dishes, Thai dishes with lime + tamarind

**Heat/spice level (none / mild / medium / high):**
This determines which elimination constraints to trigger (see Step 2).
- None: European classical preparations
- Mild: Indian korma, mild salsa, Provençal herbs
- Medium: tikka masala, Thai pad thai, Mexican enchiladas
- High: vindaloo, green curry, very spicy kimchi jjigae, phaal

**Dominant protein (if any):**
- Fish/shellfish: tannin alert → restrict or eliminate tannic reds
- Poultry: neutral, can go white or lighter red
- Pork: wide range — lighter reds to fuller whites
- Lamb: earthy reds, tannic reds
- Beef: the tannin + protein pairing; full-bodied reds are primary candidates
- Vegetarian: match to the dominant cooking character — earthy, fatty, acidic, creamy

**Dominant sauce (if any):**
The sauce overrides the protein in determining wine direction.
- Cream: full whites, light reds
- Tomato: high-acid wines, Sangiovese-family
- Reduction (red wine): match the wine family
- Butter: Chardonnay, white Burgundy
- Oil/olive oil: aromatic whites, rosé, lighter reds
- Fermented (soy, miso, gochujang): umami pairing logic — Champagne, Chablis, off-dry whites

---

### Step 2: Apply Elimination Constraints

Run through this checklist and eliminate any wine families that fail:

| Condition | Eliminate |
|---|---|
| High spice/heat level | High-tannin reds (Barolo, Cabernet Sauvignon, Shiraz), high-alcohol wines (15%+ ABV) |
| Delicate protein (raw fish, shellfish, light steamed fish) | Full-bodied reds, heavily oaked whites, any wine over ~13.5% ABV |
| Sweet dessert dish | All dry wines (they will taste bitter and sour by contrast) |
| Vinegar-dominant dressing | All high-acid wines (competing acidity makes both taste harsh) |
| Very bitter vegetables (artichoke-heavy) | Tannic reds, high-alcohol wines |
| High-fat, rich braised preparation | Very light, low-acid wines (they will be overwhelmed) |

Flag any dish where multiple constraints are triggered simultaneously — this is a genuinely difficult pairing territory (see Error Handling).

---

### Step 3: Determine Pairing Strategy

Select one of three strategies based on the dish analysis:

**Complement** — Find wines that share flavor compounds or structural characteristics with the dish:
- When to use: European classical cuisine, dishes with a dominant single flavor profile, grilled preparations
- Method: identify the most distinctive flavor element of the dish → find wines with documented shared compounds
- Examples: goat cheese + Sancerre (shared herbaceous/pyrazine compounds), truffle + Barolo (shared earthy/mineral depth), char-grilled meat + oaked red (shared Maillard/char compounds)

**Contrast** — Choose wines whose structure actively counters the dish's dominant character:
- When to use: Asian cuisines (molecular evidence favors contrast), spicy dishes, sweet-salty preparations, very rich or fatty dishes
- Method: identify the dish's most challenging element → find a wine whose opposing character neutralizes it
- Examples: spicy Thai food + off-dry Riesling (sweetness counters heat), Roquefort + Sauternes (sweetness counters salt), fried food + Champagne (acid + bubbles counter fat)

**Regional** — Apply "what grows together goes together" as the primary heuristic:
- When to use: European cuisine with a clear regional identity (French, Italian, Spanish, German)
- Method: identify the cuisine's home region → default to wines from that region as the primary recommendation
- Override if: structural constraints are violated by the regional match (then explain both)

---

### Step 4: Generate 3-5 Recommendations at Different Price Tiers

For each recommendation, provide: grape variety, region/producer style, and a 1-2 sentence explanation of why it works structurally or contextually.

**Tier structure:**
- **Entry (under $25):** everyday accessible pairing, widely available
- **Mid-range ($25-75):** elevated pairing, restaurant or special occasion at home
- **Premium ($75+):** the definitive pairing, ideal bottle for this dish

If budget is specified by the user, concentrate recommendations in that range and note what's available outside it.

**Output format for each recommendation:**
> **[Grape/Style]** — [Region/Style descriptor]
> *Why it works:* [1-2 sentences of structural or flavor rationale]
> *Price tier:* [Entry / Mid / Premium]

---

### Step 5: Flag Difficult Pairings

If Step 2 identified any elimination constraints, or if the dish analysis reveals genuine pairing difficulty, name the challenge explicitly before giving recommendations.

**Format for difficult pairing flag:**
> **Pairing note:** [Name the challenging element, e.g., "The gochujang and sesame oil in this dish create an umami + heat double challenge"]. [Explain the constraint and what it eliminates]. [Describe the workaround strategy used in the recommendations below.]

Do not bury the difficulty — a user who knows their pairing is genuinely challenging will appreciate honesty more than a confident recommendation that fails at the table.

---

### Reverse Pairing (If User Already Has a Wine)

When the user presents a wine and wants to find matching food:

1. Load the wine's structural profile: grape variety → acidity level, tannin level, body, sweetness, oak influence, approximate weight
2. Treat the wine's structure as fixed and find foods whose dominant elements match or complement
3. Apply the same Decision Framework from pairing-science in reverse: what dish weight matches this wine's body? What protein handles this tannin level? What sauce would echo or contrast this wine's flavor profile?
4. Generate 3-5 food suggestions with rationale

**Examples:**
- 2019 Barolo → high tannin, high acid, full body, complex earthy/floral → braised beef or lamb, Piedmontese pasta (tajarin with ragu), aged hard cheese (Parmigiano, Comté), truffle preparations
- 2020 Alsatian Gewürztraminer → off-dry, full body, low acid, aromatic (lychee, rose, ginger) → Thai or Indian food (spice aromatic affinity), Alsatian choucroute or pork, fresh ginger preparations, fruit-forward dishes
- NV Champagne Brut → high acid, bubbles, yeasty, light body → oysters, fried food, sushi, eggs, smoked salmon, delicate first courses

---

## Output Structure

Present the final output in this order:

**1. Primary recommendation** (best overall match — not necessarily the most expensive)

**2. Alternative 1** (different budget tier from primary)

**3. Alternative 2** (different style/grape family)

**4. Alternative 3** (optional: regional match if not already covered)

**5. "Unexpected but excellent" pairing** — if one genuinely exists. A pairing that most guests wouldn't think of but that works at the structural level. Present with explanation. If no genuine unexpected pairing exists, omit this section rather than fabricating one.

**6. "Common mistake" warning** — the most frequent wrong pairing for this dish, and why it fails. One sentence. This is the most valuable single piece of information for a guest making an uninformed choice.

---

## Error Handling

**Extremely spicy dish (maximum heat):**
Do not recommend wine as the primary option. State clearly: "Wine is not the optimal pairing at this heat level. The most honest recommendation is [sparkling water with citrus / cold beer / sake / lassi] because [brief reason]. If wine is required, [off-dry sparkling or lowest-alcohol Riesling] will cause the least friction."

**Artichoke or asparagus-dominant dish:**
Warn before recommending. State: "This dish contains [artichoke/asparagus], which creates [cynarin receptor suppression / sulfur compound interaction] that makes most wine pairings challenging." Then recommend the specific exceptions (dry rosé / Grüner Veltliner for artichoke; Sauvignon Blanc / dry Riesling for asparagus) and explain why these varieties are the exceptions.

**Dessert dish without sweet wine:**
Do not recommend a dry wine. State: "Dry wine will taste thin, sour, and bitter alongside this dessert — the dessert's sweetness makes the wine seem harsher by contrast. A sweet wine is required here." Then recommend appropriate sweet options (Late Harvest, Sauternes, Port, Banyuls, Moscato d'Asti depending on dessert type).

**No good pairing exists:**
Some combinations genuinely have no excellent wine pairing. If this is the case (extremely challenging dish with multiple conflicting constraints), say so directly and recommend the best available option with honest caveats. The mark of expertise is knowing the limits of the domain.
