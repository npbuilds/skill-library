# Archon v2 — Daily Briefing Protocol

> **DEPRECATED (2026-05-11):** Retained for future briefing reactivation but no longer referenced by `archon/SKILL.md` v2.1. Current mode is conversational analysis with optional vault persistence — see `conversational-loop.md`. To reactivate briefings, remove this header and rewire from the orchestrator.

The protocol for generating a focused, opinionated daily investment intelligence briefing. Frameworks are invisible scaffolding — applied directly as analytical lenses, never as persona voice blocks.

## Reference Mockup

See `skills/investing/archon/references/briefing-mockup.md` in the project root for the exact format and tone to follow.

---

## Narrative Arc

The briefing tells a story in 7 sections:
1. **Here's what changed** (Signal Board)
2. **Here's the world we're in** (Regime & Macro)
3. **Here's what the crowd thinks — and where they're wrong** (Sentiment & Positioning)
4. **Here's what the tape says** (Market Dashboard)
5. **Here's what could go wrong** (Risk & Scenarios)
6. **Here's how our bets are doing** (Portfolio Review)
7. **Here's what to do about it** (Actionable Intelligence)

---

## Tone

**Opinionated + Socratic.** Make bold analytical claims, then challenge them. Every section should include at least one **bolded question** that keeps the analysis honest.

Examples of good tone:
- "Gold's 5 consecutive down days while geopolitical risk worsened is the clearest reflexive reversal signal in this briefing."
- "**At +34% YTD, is energy still a trade or is it a crowded consensus?**"
- "What would change this view? Two things: (1) Hormuz de-escalation, (2) a dovish Fed pivot."

Examples of bad tone (never do this):
- "Dalio would say that..."
- "As Marks observes in his latest memo..."
- "Soros's reflexivity theory suggests..."

Instead, apply the framework directly:
- "The regime quadrant is stagflation with high confidence — falling growth and rising inflation confirmed by GDPNow going negative."
- "The pendulum sits at 52 — not extreme enough for pure contrarianism."
- "Oil's reflexive feedback loop (higher prices → increased Iranian war capacity → more disruption → higher prices) is intact but approaching climax."

---

## Format Rules

- **Tables first, then analytical paragraphs.** Data tables are compact dashboards. Analysis follows in 2-3 paragraphs that connect dots across tables.
- **No persona monologue blocks.** Never: `BUFFETT/MUNGER QUALITY CHECK` followed by a quoted speech. Instead: integrate the quality lens into the sector analysis naturally.
- **No generic connectors.** Never: "Zooming out to the full asset universe..." Instead: jump directly to the next section. The narrative arc provides implicit flow.
- **Sections with nothing notable collapse to a status line.** E.g., "Private markets: no changes since last briefing. Credit cycle stable."
- **Maximum 550 lines.** Every sentence must earn its place.

---

## Section Specifications

### §0 — SIGNAL BOARD

**Purpose:** 10-second scan — do I need to read further?

**Contains:**
1. **Delta table**: Changes since last briefing (compact, same format as v1 — this works well)
2. **Top 3 alerts**: From the alert engine, ranked by severity
3. **Data health row**: `DATA HEALTH [score/100]` with per-source status from `_health`
4. **Portfolio snapshot**: Equity, daily P&L, deployed %, open positions count

**Data tools:** `get_delta()`, `get_alerts()`, `get_portfolio()`, `get_pipeline_health()` (from `_health` in generate_briefing)

**Format:**
```
SINCE LAST BRIEFING (date → date)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
▲/▼ [asset]: [old] → [new] ([change])
⚡ ALERT: [description]

DATA HEALTH [XX/100]
Source: STATUS (age) | Source: STATUS (age) | ...

PORTFOLIO SNAPSHOT
Equity: $X (+X%) | Deployed: X% | Positions: N
Today: +/- $X | Best: [position] | Worst: [position]
```

---

### §1 — REGIME & MACRO LANDSCAPE

**Purpose:** What world are we in? How confident are we? What would change it?

**Contains:**
1. **Macro dashboard table**: Regime quadrant, key indicators (Fed Funds, CPI, Core PCE, unemployment, yields, GDPNow, ISM)
2. **Analytical paragraphs** (2-3):
   - Regime assessment with confidence and what's changed since last briefing
   - Debt cycle position and historical analog
   - Fed constraints and reflexivity check (bond market creating self-fulfilling dynamics?)
3. **"What would change this view?"** — explicit invalidation conditions

**Frameworks applied invisibly:** Dalio (regime quadrant, debt cycle), Soros (bond market reflexivity), game theory (Fed constraints)

**Data tools:** `get_regime_and_macro()`

---

### §2 — SENTIMENT & POSITIONING

**Purpose:** What does the crowd believe? Where is it wrong?

**Contains:**
1. **Sentiment dashboard row**: Composite, VIX, Fear/Greed, pendulum position, COT net equity
2. **Consensus vs. Contrarian table** (keep this — it's one of the strongest elements):
   ```
   | # | What consensus believes | Why it might be wrong | Confidence |
   ```
3. **Analytical paragraphs** (2-3):
   - Pendulum assessment (how far from extremes?)
   - Behavioral signals integration (Google Trends with the positioning context)
   - Fund flow direction (where is capital moving?)
4. **Bolded question** about the most important positioning signal

**Frameworks applied invisibly:** Marks (pendulum, second-level thinking, consensus errors), Soros (crowding, reflexive reversal)

**Data tools:** `get_sentiment_and_positioning()`

---

### §3 — MARKET DASHBOARD

**Purpose:** What is the tape actually saying?

**Contains:**
1. **Index snapshot table**: S&P, Nasdaq, Russell, equal weight — with YTD and 1M
2. **Sector heat map**: Leaders and laggards with ASCII bars + pattern label
3. **Cross-asset snapshot table**: VIX, oil, gold, BTC, dollar, TLT, HYG — YTD and 1M with brief annotation per row
4. **Analytical paragraphs** (2-3):
   - Breadth analysis (the most underappreciated signal)
   - Sector rotation quality assessment (momentum vs. structural?)
   - Reflexivity phase map for 2-3 assets with strongest feedback loops

**Frameworks applied invisibly:** Druckenmiller (liquidity, breadth), Buffett (moat quality of sector leaders), Soros (reflexivity phases), Simons (factor regime)

**Data tools:** `get_market_data()`

---

### §4 — RISK & SCENARIOS

**Purpose:** What could go wrong? What is the distribution of outcomes?

**Contains:**
1. **Risk dashboard row**: Stock-bond correlation, VIX term structure, HY spread, overall risk level
2. **Assessment**: Fragile / Robust / Antifragile with justification
3. **Defense prescription**: What hedges work in this regime? What doesn't?
4. **Scenario cards table** (4 scenarios):
   ```
   | Scenario | Prob | Story | Asymmetry | Invalidation |
   ```
5. **"Has the distribution shifted?"** — compare today's scenario probabilities to last briefing
6. **Game theory note** — strategic interactions between key players

**Frameworks applied invisibly:** Taleb (barbell, antifragility, tail risk), Tudor Jones (defense-first, 2:1 minimum, stop levels)

**Data tools:** `get_risk_dashboard()`, prior briefing scenario cards

---

### §5 — PORTFOLIO REVIEW

**Purpose:** How are our bets doing? Are the theses still valid?

**Contains:**
1. **Open positions table**:
   ```
   # Symbol Dir Entry Current P&L Days Thesis Status
   ```
   Thesis status uses emoji: ✅ Intact, ⚠️ Under review, ❌ Broken
2. **Portfolio metrics row**: Equity, deployed %, realized P&L, unrealized, Sharpe, drawdown, win rate
3. **Thesis health check** (1-2 sentences per position): Is the original thesis still supported by the data?
4. **Trade decisions** (if any): "Decision: reduce QQQ short by 50%. The thesis is partially invalidated by..." — explain reasoning, then execute via `close_position`/`open_position` after the briefing.
5. **Rules evolution** (if applicable): Document any changes to portfolio rules via `adjust_portfolio_rules`

**Data tools:** `get_portfolio()`, `update_positions()`

---

### §6 — ACTIONABLE INTELLIGENCE

**Purpose:** What should we do? What should we watch? What should we avoid?

**Contains:**
1. **Conviction ideas table** (2-3 max):
   ```
   | # | Idea | Direction | Conviction | Asymmetry | Entry trigger | Stop |
   ```
2. **Monitoring list** (3-5 ideas watching for entry): Brief description + trigger condition
3. **Avoid list** (2-3 things data says to stay away from)
4. **Catalyst calendar** (next 2 weeks): Compact table of high-impact events (econ releases, earnings, FOMC)
5. **Special situations** (only if notable): Insider clusters, spinoffs, SEC filings
6. **Private markets / Geo / Crypto**: Integrated where relevant, not standalone sections. Only expand if there's a critical signal.

**Conviction ideas must consider portfolio context:** correlation with existing positions, capital available, regime alignment.

**Data tools:** `get_external_signals()`, `get_private_markets()`

---

### MACRO NARRATIVE UPDATE (Footer)

**Purpose:** Maintain continuity across briefings.

**Contains:**
1. New turning points added to `macro-narrative.md`
2. Theme updates (conviction changes)
3. Retired themes (with reason)
4. Portfolio trades executed today

**Format:** 3-5 bullet points. This is also the instruction to update `archon-briefings/macro-narrative.md`.

---

## Data Collection Sequence

1. Call `generate_briefing()` — all 6 core tools + health
2. Call `get_delta()` — changes since last snapshot
3. Call `get_alerts()` — threshold-based signals
4. Call `get_portfolio()` — current positions
5. Call `update_positions()` — mark-to-market

## Post-Briefing Actions

1. Execute any portfolio trades decided in §5/§6
2. Log predictions for key falsifiable claims
3. Save briefing to `archon-briefings/YYYY-MM-DD.md`
4. Call `save_snapshot()` for tomorrow's delta
5. Update `archon-briefings/macro-narrative.md`
6. Resolve any overdue predictions

---

## Quality Checklist

Before finalizing, verify:
- [ ] All 7 sections present (or collapsed to status line if nothing notable)
- [ ] No persona voice blocks or "X would say" phrasing
- [ ] Every section has at least one bolded question
- [ ] Data health row present in §0
- [ ] Portfolio snapshot present in §0
- [ ] Consensus vs. contrarian table has 4-6 rows with confidence tags
- [ ] Scenario cards have probabilities summing to ~100%
- [ ] All conviction ideas have asymmetry score and stop-loss
- [ ] Macro narrative footer updates specified
- [ ] Total length < 550 lines
- [ ] Stale data (>48h) flagged with warning
