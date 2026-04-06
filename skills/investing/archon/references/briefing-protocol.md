# Daily Briefing Generation Protocol

The Archon's protocol for generating a comprehensive daily intelligence briefing. This document governs report structure, investor voice commentary, narrative flow, and the synthesis that transforms raw data into actionable intelligence.

## Design Template

Use the **Weathered Cyberpunk** template for all HTML briefings. See `skills/artifacts/master-artificer/references/templates/weathered-cyberpunk.md` for the full design system (colors, typography, components, effects, light/dark toggle).

---

## Report Architecture

The briefing follows a **narrative arc**, not just a data dump. It tells a story: *here's the world we're in → here's what the crowd thinks → here's what they're missing → here's what to do about it → here's what could go wrong.*

### Section Order & Investor Voice Assignments

Each section has a **primary data source**, an **investor voice** that provides analytical commentary, and a **narrative connector** that bridges to the next section.

---

#### 0. WHAT CHANGED (Delta Block)
**Position:** First thing after header, before regime banner
**Data:** Diff against prior briefing (requires persisted prior-day data)
**Format:** 3-5 bullet summary of the most significant moves since last report

```
SINCE LAST BRIEFING (24H Δ)
━━━━━━━━━━━━━━━━━━━━━━━━━━━
▲ VIX: 31.1 (+2.3) — crossed panic threshold
▼ Nasdaq: -1.8% — mega-cap sell-off accelerating
▲ Oil: +3.2% — Brent broke $85
─ Fed Funds: unchanged at 3.64%
⚡ NEW: Gold positioning hit extreme crowded long (41.7% OI)
```

**Voice:** None — this is pure signal. Let the numbers speak.

**Connector → Regime:** *"These moves sharpen the regime picture..."*

---

#### 1. REGIME CLASSIFICATION (Banner)
**API:** `get_regime`
**Investor Voice:** 🏛️ **Ray Dalio** — Regime identification and All-Weather quadrant positioning
**Skill consulted:** `regime-intelligence/macro-cycles`

**Dalio's commentary should include:**
- Which quadrant of the 2×2 (growth × inflation) matrix we're in
- Confidence level and whether we're at a boundary between regimes
- Historical analog: "The last time we saw this configuration was [period] — here's what happened"
- What the debt cycle position implies about regime duration
- Which asset classes historically perform in this regime (from All-Weather framework)

**Format:**
```
DALIO'S REGIME READ
━━━━━━━━━━━━━━━━━━
"We are in a [quadrant] regime with [X]% confidence. The pattern most closely
resembles [historical analog]. In that period, [what happened]. The debt cycle
is [position], which suggests [duration/intensity]. All-Weather positioning
favors [assets] and underweights [assets]."
```

**Connector → Sentiment:** *"Given this regime, the key question becomes: what does the market already believe?"*

---

#### 2. CONSENSUS VS. CONTRARIAN (New Section)
**Position:** Immediately after regime banner
**APIs:** `get_contrarian_scorecard` (master), `get_sentiment`, `get_cot_positioning`, `get_google_trends`
**Investor Voice:** 📝 **Howard Marks** — Second-level thinking, consensus error analysis
**Skill consulted:** `value-quality/second-level-thinking`

**The core table:**
```
WHAT CONSENSUS BELIEVES           vs.    WHERE SECOND-LEVEL THINKING DISAGREES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Consensus view]                   →     [Contrarian read + why] (Confidence: H/M/L)
```

**Marks's commentary should include:**
- Where on his pendulum (greed ↔ fear) the market sits today
- Which consensus views are most likely wrong and why (the three error types: level, timing, distribution)
- The "what's priced in" analysis — reverse-engineer expectations from current prices
- Whether the current environment rewards contrarian or consensus positioning
- Explicit identification of which contrarian views have *all three requirements* (disagree + be right + wait long enough)

**Format:**
```
MARKS'S MEMO — WHERE IS THE PENDULUM?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"The pendulum is at [position]. [Summary of where consensus is wrong].
The most actionable contrarian view is [view] because [reasoning].
But contrarian doesn't mean always opposing — consensus is right about [X]."
```

**Connector → Market Vitals:** *"With consensus mapped, let's examine what the live data actually shows..."*

---

#### 3. MARKET VITALS (Gauge Row)
**API:** `get_sentiment`, `get_regime`, market data
**Investor Voice:** ⚔️ **Paul Tudor Jones** — Defense-first risk read
**Skill consulted:** `risk-architecture/position-sizing`

**Tudor Jones's commentary (brief, tactical):**
- Is this a "play defense" or "play offense" environment?
- Does the current VIX level offer 2:1 reward/risk on any trade?
- What's the stop-loss level for the market? (Where does the thesis break?)

**Format:** 1-2 sentence voice block below the gauges.
```
TUDOR JONES DEFENSE CHECK: "[Assessment]. [Key level]. [Action bias]."
```

**Connector → Equities:** *"The defensive posture frames how we read the equity tape..."*

---

#### 4. EQUITY INDICES + BREADTH DIVERGENCE
**API:** `get_asset_performance`, `market_snapshot`
**Investor Voice:** 🔭 **Stanley Druckenmiller** — Liquidity lens, big trade identification
**Skill consulted:** `regime-intelligence` + Archon Loop Phase 3

**Druckenmiller's commentary should include:**
- Whether the breadth divergence signals a *tradeable rotation* or just noise
- Where the liquidity is flowing (sector flows, fund flows if available)
- Whether this setup is the kind where you "bet big" or "stay small"
- His flexibility test: "What new information would make me reverse this view?"

**Format:**
```
DRUCKENMILLER'S LIQUIDITY READ
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"[Assessment of rotation/liquidity]. [Size of opportunity]. [Conviction level].
I'd reverse if [invalidation trigger]."
```

**Connector → Sectors:** *"The rotation story becomes clearer in the sector breakdown..."*

---

#### 5. SECTOR ROTATION HEAT MAP
**API:** `get_asset_performance`
**Investor Voice:** 🏭 **Buffett/Munger** — Quality lens on sector leaders and laggards
**Skill consulted:** `value-quality/quality-compounders`

**Buffett/Munger commentary should include:**
- Which leading sectors have *durable* competitive advantages vs. cyclical momentum
- Whether the lagging sectors contain quality businesses being unfairly punished
- The Munger inversion: "What would make the current leaders become laggards?"
- Quality vs. momentum distinction: "Is energy leading because of quality or because of a temporary supply shock?"

**Format:**
```
BUFFETT/MUNGER QUALITY CHECK
━━━━━━━━━━━━━━━━━━━━━━━━━━━
"[Quality assessment of sector rotation]. [Which sectors have moats vs. momentum].
[Munger inversion warning]."
```

**Connector → Cross-Asset:** *"Zooming out from sectors to asset classes reveals the bigger picture..."*

---

#### 6. CROSS-ASSET PERFORMANCE
**API:** `get_asset_performance`
**Investor Voice:** 🔄 **George Soros** — Reflexivity analysis, feedback loop identification
**Skill consulted:** `reflexivity-sentiment/reflexivity-theory`

**Soros's commentary should include:**
- Which assets are in a reflexive feedback loop (price changes reinforcing fundamentals)?
- Where in the boom-bust 8-phase model each major asset sits
- Identification of the "far-from-equilibrium" condition: which asset is furthest from fair value due to reflexive dynamics?
- The credit reflexivity check: are rising/falling asset prices affecting credit conditions?

**Format:**
```
SOROS'S REFLEXIVITY MAP
━━━━━━━━━━━━━━━━━━━━━━
Phase assessment for key assets:
• [Asset]: Phase [N] — [description]. Feedback loop: [positive/negative/neutral].
• [Asset]: Phase [N] — [description]. Feedback loop: [positive/negative/negative].
"The most dangerous reflexive dynamic right now is [X] because [Y]."
```

**Connector → Yield Curve:** *"The bond market's view of the world adds another dimension..."*

---

#### 7. YIELD CURVE + MACRO INDICATORS
**API:** `get_regime` (FRED data)
**Investor Voice:** 🏛️ **Ray Dalio** — Debt cycle positioning
**Skill consulted:** `regime-intelligence/monetary-regime` + `regime-intelligence/fiscal-regime`

**Dalio's commentary should include:**
- Where we are in the short-term debt cycle (early, mid, late)
- Whether the yield curve shape signals monetary policy conflict with markets
- The fiscal dominance question: is government debt issuance starting to drive rates more than Fed policy?
- Historical debt cycle analog and what came next

**Format:** 1-2 sentence voice block.
```
DALIO'S DEBT CYCLE READ: "[Position in cycle]. [Key risk]. [Historical analog]."
```

**Connector → Risk:** *"The macro picture feeds directly into the risk architecture..."*

---

#### 8. RISK ARCHITECTURE
**API:** `get_risk_dashboard`
**Investor Voice:** 🦢 **Nassim Taleb** — Antifragility assessment
**Skill consulted:** `risk-architecture/tail-risk` + `risk-architecture/correlation-regimes`

**Taleb's commentary should include:**
- The antifragility score: is the portfolio positioned to *benefit* from disorder, or is it fragile?
- Whether current correlations indicate a "turkey problem" (smooth sailing hiding tail risk)
- Barbell recommendation: what's the specific safe/aggressive split for this environment?
- Which "black swan" scenarios are being underpriced by the market?
- The convexity check: are there positions with limited downside and unlimited upside available?

**Format:**
```
TALEB'S ANTIFRAGILITY CHECK
━━━━━━━━━━━━━━━━━━━━━━━━━━
Fragility score: [Antifragile / Robust / Fragile]
"[Assessment]. The tail risk the market is ignoring is [X].
Barbell prescription: [Y]% in [safe assets], [Z]% in [convex bets on X]."
```

**Connector → Factors:** *"The factor landscape reveals whether systematic strategies are working or breaking..."*

---

#### 9. FACTOR RETURNS
**API:** `get_factor_returns`
**Investor Voice:** 📊 **Jim Simons** — Quantitative pattern read
**Skill consulted:** Data science skills for statistical analysis

**Simons-style commentary should include:**
- Statistical significance of current factor co-movements (are value+momentum co-moving? historically unusual?)
- Base rate analysis: what happened in past periods with this factor signature?
- Whether the current factor environment suggests systematic strategies are working or in drawdown
- Alternative data signal quality: are non-traditional signals confirming or contradicting factor readings?

**Format:**
```
QUANTITATIVE PATTERN CHECK
━━━━━━━━━━━━━━━━━━━━━━━━━
"[Statistical observation]. [Base rate from history]. [Whether this is regime-normal or anomalous].
Signal confidence: [H/M/L] based on [N] historical analogs."
```

**Connector → Positioning:** *"The factor shifts explain part of the positioning picture..."*

---

#### 10. CFTC POSITIONING
**API:** `get_cot_positioning`
**Investor Voice:** 🔄 **Soros** — Crowding and reflexive reversal risk
**Skill consulted:** `reflexivity-sentiment/sentiment-signals`

**Soros's commentary should include:**
- Which positions are crowded enough to create reflexive reversal risk
- The information asymmetry: when everyone holds the same belief, what information would cause the biggest move?
- Positioning vs. price divergences (crowd short while price rises = squeeze fuel)

**Format:** Brief voice block.
```
SOROS ON CROWDING: "[Most dangerous crowded trade]. [Reversal catalyst]. [Squeeze risk]."
```

**Connector → Special Situations:** *"Beyond macro positioning, the micro picture reveals overlooked opportunities..."*

---

#### 11. SPECIAL SITUATIONS + INSIDER SIGNALS (New Section)
**APIs:** `get_special_situations`, `get_insider_signals`
**Investor Voice:** 🔍 **Joel Greenblatt** — Forced selling, institutional blind spots
**Skill consulted:** `special-situations/spinoffs-restructuring` + `special-situations/insider-signals`

**Greenblatt's commentary should include:**
- Any recent spinoffs, restructurings, or corporate actions creating forced selling
- Insider buying clusters (>3 insiders buying within 2 weeks = strong signal)
- Complexity premium opportunities (holding company discounts, stub trades)
- Why institutions are forced to ignore these (mandate constraints, size requirements, index reconstitution)

**Format:**
```
GREENBLATT'S OVERLOOKED CORNER
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Spinoffs/Restructurings: [list or "none this week"]
Insider clusters: [notable insider buying patterns]
"The institutional blind spot right now is [X] because [Y]."
```

**Connector → Private Markets:** *"Beyond public market micro-catalysts, the private markets tell a parallel story with a 6-12 month lag..."*

---

#### 11.5. PRIVATE MARKETS MONITOR (New Section)
**API:** `get_private_markets`
**Investor Voice:** 📝 **Howard Marks** (credit cycle) + 🔍 **Joel Greenblatt** (public-private divergence)
**Skill consulted:** `asset-universe/alternatives` + `risk-architecture/correlation-regimes`

**Content structure:**

```
PRIVATE MARKETS MONITOR
━━━━━━━━━━━━━━━━━━━━━━

RE CYCLE: [expansion/recovery/late_cycle/contraction] (score: X)
CREDIT CYCLE: [expansion/mid_cycle/late_cycle/stress] (score: X)
EXIT WINDOW: [wide_open/open/narrowing/frozen] (score: X)
DIVERGENCE: [normal/elevated/severe]

┌─ Real Estate ──────────────────────────────────┐
│ Residential: [cycle phase] — [key signals]     │
│ Structural: [new economy vs office spread]     │
│ REIT regime: [bull/positive/correction/bear]   │
└────────────────────────────────────────────────┘

┌─ Private Credit ───────────────────────────────┐
│ HY spread: [X bps] — [signal]                  │
│ BDC NAV discount: [X%] — [signal]              │
│ Lending standards: [tightening/easing/neutral] │
└────────────────────────────────────────────────┘

┌─ PE/VC Exit Window ────────────────────────────┐
│ IPO market: [YTD %] — [signal]                 │
│ GP stocks: [avg YTD %] — fundraising health    │
│ Growth multiples (ARKK): [YTD %]               │
└────────────────────────────────────────────────┘
```

**Marks's commentary (credit lens) should include:**
- Where in his credit cycle framework we sit — are standards loosening (fuel for future problems) or tightening (cleaning up past excess)?
- Whether BDC NAV discounts are pricing in enough pain or if further write-downs are coming
- The "race to the bottom" check: are private credit managers competing on terms in ways that create future risk?
- His pendulum applied to credit: where between "we'll lend to anyone" and "we won't lend to anyone"?

**Greenblatt's commentary (divergence lens) should include:**
- Where public-private valuation gaps create opportunity (forced selling by funds needing liquidity)
- Whether GP stock performance suggests fee/carry revenue is at risk
- The "complexity premium" in private markets: are discounts rational (credit risk) or structural (illiquidity premium being mispriced)?
- Where fund-level forced selling might create opportunity (denominator effect, GP-led secondaries)

**Format:**
```
MARKS ON THE CREDIT CYCLE
━━━━━━━━━━━━━━━━━━━━━━━━
"[Credit cycle position]. [Lending standards assessment]. [What the BDC market
is telling us about unrealized losses]. Confidence: [H/M/L]."

GREENBLATT ON PUBLIC-PRIVATE DIVERGENCE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"[Divergence assessment]. [Where forced selling creates opportunity].
[Whether GP stock weakness signals fee/carry problems]. Confidence: [H/M/L]."
```

**Connector → Geopolitical:** *"These private market dynamics play out within a geopolitical context that shapes which themes persist..."*

---

#### 12. GEOPOLITICAL MONITOR (New Section)
**API:** `get_geopolitical_monitor`
**Investor Voice:** None (data-forward) — but flag where geopolitical risk intersects with other investor voices
**Skill consulted:** `geopolitical-overlay`

**Content:**
- Hot spot risk levels (escalation probability)
- Energy security implications
- Secular theme tracking (AI capex, deglobalization, demographics)
- Which sectors/assets are most exposed to each geopolitical risk

**Connector → Crypto:** *"The alternative asset picture, including digital assets..."*

---

#### 13. CRYPTO MARKET
**API:** `get_crypto_dashboard`
**Investor Voice:** 📝 **Howard Marks** — Second-level thinking on extreme fear/greed
**Skill consulted:** `value-quality/second-level-thinking`

**Marks's commentary (brief):**
- What Fear & Greed at [level] historically meant for forward returns
- Whether extreme fear is a contrarian buy or a rational response to structural risk
- The "what would make the bears right vs. wrong?" framing

**Format:** 1-2 sentence voice block.

**Connector → Behavioral:** *"The crypto sentiment connects to the broader behavioral landscape..."*

---

#### 14. BEHAVIORAL SIGNALS
**API:** `get_google_trends`
**Investor Voice:** 🧠 **Marks + Soros synthesis** — Crowd behavior meets reflexivity
**Skill consulted:** `reflexivity-sentiment/market-psychology`

**Commentary should include:**
- What retail search behavior reveals about the crowd's emotional state
- Whether retail is leading or lagging institutional positioning
- Reflexive dynamics: is retail fear/greed *causing* the very moves they're reacting to?

**Connector → Predictions:** *"All of this feeds into the probability-weighted scenario framework..."*

---

#### 15. YEAR-END PREDICTIONS (Scenario Cards)
**Investor Voice:** 🎯 **Full Archon Synthesis** — All frameworks converge
**Skill consulted:** All subdomains + game theory (Nash equilibrium, mechanism design)

**The synthesis should include:**
- Probability-weighted scenarios grounded in regime analysis (Dalio)
- Second-level check on each scenario: which is consensus pricing? (Marks)
- Reflexivity risk: which scenario could become self-fulfilling? (Soros)
- Asymmetry assessment: which scenario offers the best risk/reward? (Druckenmiller)
- Tail risk overlay: which scenario has the fattest tail? (Taleb)
- Game theory framing: Fed vs. Market, US vs. China, etc.
- Historical base rates from similar setups

**Format:** Scenario cards + summary table + multi-voice synthesis block.

**Connector → Recommendations:** *"The scenario probabilities translate into concrete positioning..."*

---

#### 16. TACTICAL RECOMMENDATIONS
**Investor Voice:** ⚔️ **Druckenmiller** — Conviction-ranked, asymmetry-scored
**Skill consulted:** Archon Loop Phase 5 synthesis

**Enhancement over current format:**
- Each recommendation gets a **conviction level** (High / Medium / Low / Contrarian)
- Each recommendation gets an **asymmetry score** (estimated reward:risk ratio)
- Each recommendation gets a **Tudor Jones stop**: where the thesis is invalidated
- Split into: HIGHEST CONVICTION (1-2 ideas, sized accordingly) vs. MONITORING (watching for entry)

**Format:**
```
HIGHEST CONVICTION — SIZE THESE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. [Recommendation] — Conviction: HIGH | Asymmetry: 3:1 | Stop: [level]
   Why: [1-2 sentences from relevant investor framework]

MONITORING — WATCH FOR ENTRY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• [Idea] — Entry trigger: [what must happen] | Framework: [which investor]

DATA SAYS AVOID
━━━━━━━━━━━━━━━
• [What to avoid] — Why: [reasoning] | Risk: [what goes wrong]
```

---

#### 17. EARNINGS CALENDAR (New Section, Optional)
**API:** `get_earnings_calendar`
**Investor Voice:** None — pure data
**Content:** Upcoming week's earnings with sector mapping and relevance to current themes

---

## Narrative Connectors

Every section must end with a 1-sentence bridge to the next section. These connectors turn 17 isolated data sections into a single coherent story. The connectors are **not boilerplate** — they should reference specific data from the current section that makes the next section relevant.

**Bad connector:** "Now let's look at the next section."
**Good connector:** "The +4.65% breadth gap above explains why the sector heat map shows energy leading while indices fall — the average stock is quietly outperforming."

## Investor Voice Rules

1. **Voices are analytical, not performative.** Don't write "Buffett would say..." in a folksy accent. Apply their *framework* with precision.
2. **Each voice appears 1-2 times maximum.** More than that dilutes the signal.
3. **Voices can disagree.** If Druckenmiller's read conflicts with Marks's, present both and note the tension. The Archon resolves conflicts per `investor-dna.md` framework interaction rules.
4. **Confidence tagging is mandatory.** Every investor commentary must tag its conclusion as High / Medium / Low confidence with a brief justification.
5. **The user decides.** Voices present analysis and frameworks. They do not tell the user what to do. Recommendations are framed as "the framework suggests" not "you should."

## Voice Assignment Summary

| Voice | Sections | Framework |
|-------|----------|-----------|
| Ray Dalio | Regime (§1), Yield Curve/Macro (§7) | All-Weather quadrant, debt cycles, historical analogs |
| Howard Marks | Consensus vs. Contrarian (§2), Crypto (§13) | Second-level thinking, pendulum, consensus error types |
| Paul Tudor Jones | Market Vitals (§3) | Defense-first, 2:1 test, stop-loss levels |
| Stanley Druckenmiller | Equities/Breadth (§4), Recommendations (§16) | Liquidity lens, big trade, conviction sizing |
| Buffett/Munger | Sector Rotation (§5) | Quality vs. momentum, moat durability, inversion |
| George Soros | Cross-Asset (§6), CFTC Positioning (§10) | Reflexivity phases, feedback loops, crowding |
| Nassim Taleb | Risk Architecture (§8) | Antifragility, barbell, convexity, black swans |
| Jim Simons | Factor Returns (§9) | Statistical patterns, base rates, signal confidence |
| Joel Greenblatt | Special Situations (§11), Private Markets (§11.5) | Forced selling, insider clusters, public-private divergence |
| Marks + Greenblatt | Private Markets (§11.5) | Credit cycle pendulum, complexity premium, forced selling |
| Marks + Soros | Behavioral Signals (§14) | Crowd psychology meets reflexivity |
| Full Synthesis | Year-End Predictions (§15) | All frameworks converge |

## Data Source Mapping

| API Endpoint | Section(s) | Required |
|-------------|-----------|----------|
| `get_regime` | §1 Regime, §3 Vitals, §7 Macro | Yes |
| `get_sentiment` | §2 Consensus, §3 Vitals | Yes |
| `market_snapshot` | §0 Delta, §4 Equities | Yes |
| `get_asset_performance` | §4 Equities, §5 Sectors, §6 Cross-Asset | Yes |
| `get_risk_dashboard` | §8 Risk Architecture | Yes |
| `get_factor_returns` | §9 Factors | Yes |
| `get_cot_positioning` | §2 Consensus, §10 CFTC | Yes |
| `get_insider_signals` | §11 Special Situations | Yes |
| `get_special_situations` | §11 Special Situations | Yes |
| `get_geopolitical_monitor` | §12 Geopolitical | Yes |
| `get_crypto_dashboard` | §13 Crypto | Yes |
| `get_google_trends` | §14 Behavioral | Yes |
| `get_contrarian_scorecard` | §2 Consensus vs. Contrarian | Yes |
| `get_private_markets` | §11.5 Private Markets | Yes |
| `get_economic_calendar` | Catalyst awareness across all sections | Yes |
| `get_fund_flows` | §6 Cross-Asset, §14 Behavioral (Soros reflexivity) | Yes |
| `get_fed_game` | §7 Macro/Yield Curve, §15 Predictions | Yes |
| `get_alerts` | Alert feed — cross-section signal detection | Yes |
| `get_delta` | §0 Delta Block (requires prior snapshot) | Yes |
| `get_earnings_calendar` | §17 Earnings | Optional |
| `get_13f_filings` | §11 (supplement) | Optional |

## Generation Checklist

Before finalizing any briefing, verify:

- [ ] Every section has a narrative connector to the next
- [ ] Every investor voice has confidence-tagged conclusions
- [ ] The Consensus vs. Contrarian table is populated (§2)
- [ ] At least one investor voice identifies a *disagreement* with another
- [ ] Recommendations have conviction levels, asymmetry scores, and stop-losses
- [ ] The Delta Block (§0) is populated if prior-day data exists
- [ ] Historical analogs are cited with dates, not just "historically"
- [ ] The report tells a coherent story from regime → consensus → data → predictions → action
- [ ] All 17 core API endpoints are called (including `get_private_markets`, `get_contrarian_scorecard`, `get_delta`)
- [ ] Disclaimer is present in footer
