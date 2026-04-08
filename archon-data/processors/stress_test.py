"""Scenario stress testing engine — "if X happens, what breaks?"

Takes a trigger shock (oil spike, VIX explosion, credit blowout, rate surge,
USD crash, etc.) and traces the transmission cascade through asset classes,
sectors, and risk factors. Returns impact estimates with confidence levels
and the historical precedent for each cascade step.

This is NOT a Monte Carlo simulation. It's a qualitative-quantitative hybrid
that uses known transmission mechanisms (backed by rough empirical magnitudes)
to reason through second- and third-order effects. The value is in surfacing
non-obvious linkages, not in precise point estimates.

Key concepts:
- Trigger: The initial shock (e.g., "oil to $100")
- Transmission: How the shock propagates (e.g., oil → CPI → Fed hawkish → rates up)
- Cascade: The full chain of effects across asset classes
- Severity: How much damage (mild/moderate/severe/extreme)
- Confidence: How well-established the transmission mechanism is (high/medium/low)
"""

from __future__ import annotations



# ── Scenario Library ────────────────────────────────────────────
# Pre-built scenarios with known transmission mechanisms.
# Each scenario can also be triggered ad-hoc with custom parameters.

SCENARIO_LIBRARY: dict[str, dict] = {
    "oil_spike": {
        "label": "Oil Price Spike",
        "description": "Crude oil surges above $100/bbl on supply disruption or geopolitical event",
        "trigger": {"asset": "oil", "direction": "up", "magnitude": "+40%"},
        "transmission": [
            {
                "step": 1,
                "channel": "Direct input costs",
                "effect": "Transportation and energy costs spike immediately",
                "assets_affected": {"XLE": "+15-25%", "airlines": "-20-30%", "transports": "-10-15%"},
                "confidence": "high",
            },
            {
                "step": 2,
                "channel": "CPI passthrough",
                "effect": "Headline CPI rises 0.5-1.0% within 2-3 months as energy flows through",
                "assets_affected": {"TIPS": "+2-4%", "TLT": "-3-5%", "gold": "+5-10%"},
                "confidence": "high",
            },
            {
                "step": 3,
                "channel": "Fed reaction function",
                "effect": "Fed forced to maintain/increase hawkish stance; rate cut expectations repriced",
                "assets_affected": {"2Y_yield": "+30-50bp", "growth_stocks": "-5-10%", "HYG": "-2-3%"},
                "confidence": "medium",
            },
            {
                "step": 4,
                "channel": "Consumer squeeze",
                "effect": "Gasoline price surge acts as regressive tax; consumer confidence falls",
                "assets_affected": {"XLY": "-8-12%", "retail": "-10-15%", "autos": "-10-15%"},
                "confidence": "medium",
            },
            {
                "step": 5,
                "channel": "EM contagion",
                "effect": "Oil-importing EM countries face twin deficit pressure, currency weakness",
                "assets_affected": {"EEM": "-8-12%", "EM_FX": "-5-8%", "USD": "+2-4%"},
                "confidence": "medium",
            },
        ],
        "historical_precedent": "2022 Russia-Ukraine (Brent $130), 2008 ($147), 1973 OPEC embargo",
        "regime_shift_risk": "Pushes toward stagflation if growth is already softening",
        "net_spx_impact": "-8 to -15%",
        "time_horizon": "2-6 months for full cascade",
    },

    "vix_spike": {
        "label": "Volatility Explosion",
        "description": "VIX spikes above 50 on systemic shock or forced deleveraging",
        "trigger": {"asset": "VIX", "direction": "up", "magnitude": ">50"},
        "transmission": [
            {
                "step": 1,
                "channel": "Vol-targeting deleveraging",
                "effect": "Risk parity and vol-target funds mechanically sell equities as vol rises",
                "assets_affected": {"SPY": "-10-20%", "IWM": "-15-25%", "EEM": "-12-20%"},
                "confidence": "high",
            },
            {
                "step": 2,
                "channel": "Margin calls and liquidation",
                "effect": "Leveraged positions force-sold; correlations spike toward 1.0",
                "assets_affected": {"all_equities": "-5-10% additional", "crypto": "-20-30%", "HYG": "-5-8%"},
                "confidence": "high",
            },
            {
                "step": 3,
                "channel": "Flight to quality",
                "effect": "Treasury rally (if not an inflation shock); gold bid; cash hoarding",
                "assets_affected": {"TLT": "+5-10%", "GLD": "+3-8%", "SHY": "+1%", "USD": "+3-5%"},
                "confidence": "medium",
            },
            {
                "step": 4,
                "channel": "Options market stress",
                "effect": "Dealer gamma exposure flips negative, amplifying moves in both directions",
                "assets_affected": {"SPX_realized_vol": "2x implied", "bid_ask_spreads": "3-5x normal"},
                "confidence": "high",
            },
            {
                "step": 5,
                "channel": "Policy response",
                "effect": "Fed/Treasury likely to intervene with liquidity facilities if VIX >50 persists",
                "assets_affected": {"reversal_probability": "high within 1-3 weeks"},
                "confidence": "medium",
            },
        ],
        "historical_precedent": "COVID Mar 2020 (VIX 82), Volmageddon Feb 2018 (VIX 50), GFC Oct 2008 (VIX 80)",
        "regime_shift_risk": "Temporarily forces any regime into crisis mode regardless of fundamentals",
        "net_spx_impact": "-15 to -30% peak drawdown",
        "time_horizon": "1-4 weeks for acute phase, 2-6 months for recovery",
    },

    "credit_blowout": {
        "label": "Credit Market Seizure",
        "description": "HY spreads blow out to 800+ bps on credit event or contagion",
        "trigger": {"asset": "HY_spread", "direction": "up", "magnitude": ">800bp"},
        "transmission": [
            {
                "step": 1,
                "channel": "Primary market freeze",
                "effect": "New issuance market shuts down; companies cannot refinance maturing debt",
                "assets_affected": {"HYG": "-10-15%", "LQD": "-5-8%", "leveraged_loans": "-8-12%"},
                "confidence": "high",
            },
            {
                "step": 2,
                "channel": "Bank earnings hit",
                "effect": "Loan loss provisions spike; bank stocks de-rate on credit quality fears",
                "assets_affected": {"XLF": "-15-25%", "regional_banks": "-20-35%", "BDCs": "-20-30%"},
                "confidence": "high",
            },
            {
                "step": 3,
                "channel": "Private credit contagion",
                "effect": "BDC NAV discounts widen to 25-35%; private credit fund redemptions begin",
                "assets_affected": {"BDC_nav": "-15-25%", "PE_secondaries": "-20-30%"},
                "confidence": "medium",
            },
            {
                "step": 4,
                "channel": "Leveraged buyout stress",
                "effect": "PE portfolio companies with floating rate debt face cash flow crisis",
                "assets_affected": {"PE_gp_stocks": "-25-40%", "CLOs": "-10-15%"},
                "confidence": "medium",
            },
            {
                "step": 5,
                "channel": "Equity contagion",
                "effect": "Credit stress historically leads equity by 2-4 weeks; SPX follows HY down",
                "assets_affected": {"SPY": "-12-20%", "IWM": "-18-28%", "XLF": "-5-10% additional"},
                "confidence": "high",
            },
        ],
        "historical_precedent": "GFC 2008 (HY >2000bp), COVID Mar 2020 (HY >1000bp), 2015-16 energy credit (HY >800bp)",
        "regime_shift_risk": "Forces deflation regime; Marks's 'credit cycle' enters stress phase",
        "net_spx_impact": "-15 to -25%",
        "time_horizon": "1-3 months for acute phase, 6-12 months for full resolution",
    },

    "rate_shock": {
        "label": "Interest Rate Shock",
        "description": "10Y Treasury yield surges 100+ bps on inflation surprise or fiscal concerns",
        "trigger": {"asset": "10Y_yield", "direction": "up", "magnitude": "+100bp"},
        "transmission": [
            {
                "step": 1,
                "channel": "Duration damage",
                "effect": "Long-duration assets reprice immediately; TLT falls ~15% per 100bp move",
                "assets_affected": {"TLT": "-12-17%", "LQD": "-5-8%", "TIPS": "-3-5%"},
                "confidence": "high",
            },
            {
                "step": 2,
                "channel": "Growth stock de-rating",
                "effect": "Higher discount rate compresses growth multiples; unprofitable tech worst hit",
                "assets_affected": {"QQQ": "-10-15%", "ARKK": "-20-30%", "biotech": "-15-20%"},
                "confidence": "high",
            },
            {
                "step": 3,
                "channel": "Housing market pressure",
                "effect": "Mortgage rates spike; affordability collapses; housing activity slows sharply",
                "assets_affected": {"homebuilders": "-15-25%", "VNQ": "-8-12%", "mortgage_REITs": "-15-20%"},
                "confidence": "high",
            },
            {
                "step": 4,
                "channel": "Fiscal sustainability concerns",
                "effect": "Higher debt service costs; fiscal space narrows; deficit hawks activate",
                "assets_affected": {"30Y_yield": "+80-120bp", "USD": "+2-5%", "gold": "+3-5%"},
                "confidence": "medium",
            },
            {
                "step": 5,
                "channel": "EM capital flight",
                "effect": "Higher US rates attract global capital; EM currencies weaken; EM bonds sell off",
                "assets_affected": {"EEM": "-8-15%", "EM_debt": "-10-15%", "EM_FX": "-5-10%"},
                "confidence": "high",
            },
        ],
        "historical_precedent": "2022 rate shock (10Y: 1.5% → 4.3%), Taper Tantrum 2013 (10Y: 1.6% → 3.0%)",
        "regime_shift_risk": "May trigger stagflation if growth is already slowing",
        "net_spx_impact": "-10 to -20%",
        "time_horizon": "1-3 months for full cascade",
    },

    "dollar_crash": {
        "label": "Dollar Crash",
        "description": "DXY drops 10%+ on loss of reserve currency confidence or twin deficit fears",
        "trigger": {"asset": "DXY", "direction": "down", "magnitude": "-10%"},
        "transmission": [
            {
                "step": 1,
                "channel": "Import price surge",
                "effect": "Imported goods more expensive; headline inflation rises 0.5-1.0%",
                "assets_affected": {"TIPS": "+3-5%", "commodities": "+8-15%", "gold": "+10-15%"},
                "confidence": "high",
            },
            {
                "step": 2,
                "channel": "Multinational earnings boost",
                "effect": "US companies with international revenue see FX-driven earnings uplift",
                "assets_affected": {"mega_cap_tech": "+3-5%", "industrials": "+3-5%"},
                "confidence": "medium",
            },
            {
                "step": 3,
                "channel": "EM relief rally",
                "effect": "Weaker dollar reduces EM debt burden and improves trade balances",
                "assets_affected": {"EEM": "+10-15%", "EM_FX": "+5-10%", "EM_debt": "+5-8%"},
                "confidence": "high",
            },
            {
                "step": 4,
                "channel": "Treasury demand destruction",
                "effect": "Foreign holders less willing to buy USD-denominated assets; yields rise",
                "assets_affected": {"TLT": "-5-10%", "10Y_yield": "+50-100bp"},
                "confidence": "medium",
            },
            {
                "step": 5,
                "channel": "De-dollarization acceleration",
                "effect": "Central banks accelerate reserve diversification; gold and crypto bid",
                "assets_affected": {"GLD": "+5-10% additional", "BTC": "+15-25%", "CNY_assets": "+5-10%"},
                "confidence": "low",
            },
        ],
        "historical_precedent": "2002-2008 dollar decline (DXY 120→70), Plaza Accord 1985 (-40% over 2yr)",
        "regime_shift_risk": "Pushes toward reflation/stagflation via imported inflation",
        "net_spx_impact": "-5 to +5% (mixed — helps multinationals, hurts purchasing power)",
        "time_horizon": "3-12 months for full cascade",
    },

    "china_shock": {
        "label": "China Financial Crisis",
        "description": "China property/banking system failure triggers capital flight and global contagion",
        "trigger": {"asset": "China_financials", "direction": "down", "magnitude": "-30%"},
        "transmission": [
            {
                "step": 1,
                "channel": "Commodity demand collapse",
                "effect": "China consumes 50%+ of industrial metals; copper, iron ore, oil all fall sharply",
                "assets_affected": {"copper": "-20-30%", "oil": "-15-25%", "iron_ore": "-25-35%"},
                "confidence": "high",
            },
            {
                "step": 2,
                "channel": "Supply chain disruption",
                "effect": "Chinese factory output drops; global supply chains re-strained",
                "assets_affected": {"tech_hardware": "-10-15%", "autos": "-10-15%", "industrials": "-8-12%"},
                "confidence": "medium",
            },
            {
                "step": 3,
                "channel": "EM contagion",
                "effect": "Commodity-exporting EMs (Brazil, Australia, South Africa) hit hardest",
                "assets_affected": {"EEM": "-15-25%", "AUD": "-10-15%", "BRL": "-12-18%"},
                "confidence": "high",
            },
            {
                "step": 4,
                "channel": "Global growth downgrade",
                "effect": "Global GDP growth marked down 1-2%; central banks pivot dovish",
                "assets_affected": {"TLT": "+5-10%", "2Y_yield": "-50-100bp", "gold": "+5-10%"},
                "confidence": "medium",
            },
            {
                "step": 5,
                "channel": "Capital flight to US",
                "effect": "Paradoxically bullish for USD and US Treasuries as safe haven demand surges",
                "assets_affected": {"USD": "+5-10%", "TLT": "+3-5% additional", "SPY": "-5-10% then rally"},
                "confidence": "medium",
            },
        ],
        "historical_precedent": "2015-16 China devaluation/capital flight, 1997 Asian Financial Crisis",
        "regime_shift_risk": "Pushes toward deflation via commodity/demand channel",
        "net_spx_impact": "-10 to -20%",
        "time_horizon": "3-9 months for global propagation",
    },

    "ai_bubble_pop": {
        "label": "AI Capex Disappointment",
        "description": "AI revenue fails to justify capex; Mag7 earnings miss on AI spending ROI",
        "trigger": {"asset": "Mag7", "direction": "down", "magnitude": "-25%"},
        "transmission": [
            {
                "step": 1,
                "channel": "Concentration unwind",
                "effect": "SPX drops disproportionately because Mag7 = 30%+ of index weight",
                "assets_affected": {"QQQ": "-20-30%", "SPY": "-12-18%", "SOXX": "-25-35%"},
                "confidence": "high",
            },
            {
                "step": 2,
                "channel": "Semiconductor cascade",
                "effect": "NVIDIA and semicap orders cancelled/pushed out; datacenter buildout slows",
                "assets_affected": {"NVDA": "-35-50%", "AVGO": "-25-35%", "semicap": "-30-40%"},
                "confidence": "high",
            },
            {
                "step": 3,
                "channel": "Passive fund rebalance",
                "effect": "Index funds forced to sell as weights drop; reflexive selling loop",
                "assets_affected": {"SPY_outflows": "significant", "QQQ_outflows": "severe"},
                "confidence": "medium",
            },
            {
                "step": 4,
                "channel": "Rotation to value/small cap",
                "effect": "Money rotates from growth to value, from large to small, from US to intl",
                "assets_affected": {"IWM": "+5-10%", "EFA": "+3-5%", "XLF": "+3-5%", "RSP": "outperforms SPY"},
                "confidence": "medium",
            },
            {
                "step": 5,
                "channel": "Venture capital freeze",
                "effect": "AI startup funding dries up; private market valuations written down",
                "assets_affected": {"VC_marks": "-30-50%", "IPO_market": "frozen", "PE_gp_stocks": "-15-20%"},
                "confidence": "medium",
            },
        ],
        "historical_precedent": "Dot-com bust 2000-02 (NASDAQ -78%), Crypto winter 2022 (-65%)",
        "regime_shift_risk": "Could trigger rotation from growth-led goldilocks to value-led reflation",
        "net_spx_impact": "-15 to -25%",
        "time_horizon": "3-12 months for full de-rating",
    },
}


# ── Stress Test Engine ──────────────────────────────────────────


def run_stress_test(
    scenario_id: str | None = None,
    custom_trigger: dict | None = None,
    briefing: dict | None = None,
) -> dict:
    """Run a scenario stress test against current market conditions.

    Args:
        scenario_id: Key from SCENARIO_LIBRARY (e.g., "oil_spike", "vix_spike")
        custom_trigger: Custom scenario dict with same structure as library entries
        briefing: Current briefing data (for context-aware severity adjustment)

    Returns:
        scenario: The scenario definition
        cascade: Transmission chain with context-adjusted severity
        portfolio_impact: Estimated impact on common portfolio types
        current_vulnerabilities: Which current positions are most exposed
        hedging_suggestions: Framework-specific hedging ideas
    """
    # Get scenario
    if scenario_id and scenario_id in SCENARIO_LIBRARY:
        scenario = SCENARIO_LIBRARY[scenario_id]
    elif custom_trigger:
        scenario = custom_trigger
    else:
        return {
            "status": "error",
            "message": f"Unknown scenario '{scenario_id}'. Available: {list(SCENARIO_LIBRARY.keys())}",
            "available_scenarios": {
                k: {"label": v["label"], "description": v["description"]}
                for k, v in SCENARIO_LIBRARY.items()
            },
        }

    # Context-aware severity adjustment
    context = _assess_vulnerability_context(briefing) if briefing else {}

    # Build the cascade with context adjustments
    cascade = _build_cascade(scenario, context)

    # Portfolio impact estimates
    portfolio_impact = _estimate_portfolio_impact(scenario, context)

    # Current vulnerabilities
    vulnerabilities = _identify_vulnerabilities(scenario, briefing) if briefing else []

    # Hedging suggestions
    hedges = _suggest_hedges(scenario, context)

    return {
        "status": "ok",
        "scenario": {
            "id": scenario_id,
            "label": scenario.get("label"),
            "description": scenario.get("description"),
            "trigger": scenario.get("trigger"),
            "historical_precedent": scenario.get("historical_precedent"),
            "regime_shift_risk": scenario.get("regime_shift_risk"),
            "net_spx_impact": scenario.get("net_spx_impact"),
            "time_horizon": scenario.get("time_horizon"),
        },
        "cascade": cascade,
        "portfolio_impact": portfolio_impact,
        "current_vulnerabilities": vulnerabilities,
        "hedging_suggestions": hedges,
        "context_adjustments": context,
    }


def list_scenarios() -> dict:
    """List all available pre-built stress test scenarios."""
    return {
        "scenarios": {
            k: {
                "label": v["label"],
                "description": v["description"],
                "trigger": v["trigger"],
                "net_spx_impact": v["net_spx_impact"],
                "time_horizon": v["time_horizon"],
            }
            for k, v in SCENARIO_LIBRARY.items()
        },
        "count": len(SCENARIO_LIBRARY),
    }


# ── Context Assessment ──────────────────────────────────────────


def _assess_vulnerability_context(briefing: dict) -> dict:
    """Assess current market context to adjust scenario severity.

    Key principle: a shock hits harder when the market is already vulnerable.
    VIX at 30 + late credit cycle + narrow breadth = amplified impact.
    """
    if not briefing:
        return {"adjustment": "neutral", "factor": 1.0}

    vulnerability_score = 0  # 0=resilient, higher=more vulnerable
    factors = []

    # VIX level — higher VIX means less margin for error
    vix = _safe_get(briefing, "sentiment", "raw", "vix", "spot")
    if vix is not None:
        if vix > 30:
            vulnerability_score += 2
            factors.append(f"VIX already elevated at {vix:.0f} — less buffer for additional shock")
        elif vix > 20:
            vulnerability_score += 1
            factors.append(f"VIX at {vix:.0f} — moderately elevated, some vulnerability")
        elif vix < 14:
            vulnerability_score += 1
            factors.append(f"VIX at {vix:.0f} — complacency means positions are oversized")

    # Credit cycle
    credit_cycle = _safe_get(briefing, "private_markets", "credit", "credit_cycle")
    if credit_cycle in ("late_cycle", "stress"):
        vulnerability_score += 2
        factors.append(f"Credit cycle at {credit_cycle} — amplifies any stress scenario")
    elif credit_cycle == "mid_cycle":
        vulnerability_score += 1
        factors.append("Credit cycle mid-cycle — moderate absorption capacity")

    # Regime
    regime = briefing.get("regime", {})
    quadrant = regime.get("quadrant")
    if quadrant == "stagflation":
        vulnerability_score += 2
        factors.append("Stagflation regime — worst quadrant for absorbing shocks")
    elif quadrant == "deflation":
        vulnerability_score += 1
        factors.append("Deflationary regime — already under stress")

    # Market breadth
    breadth = _safe_get(briefing, "market", "breadth_divergence")
    if breadth is not None and breadth < -5:
        vulnerability_score += 1
        factors.append(f"Narrow leadership (divergence: {breadth:.1f}%) — fragile market structure")

    # Sentiment
    score = _safe_get(briefing, "sentiment", "composite", "score")
    if score is not None:
        if score > 80:
            vulnerability_score += 1
            factors.append("Extreme greed — everyone positioned the same way")
        elif score < 20:
            # Extreme fear actually provides cushion (already priced in)
            vulnerability_score -= 1
            factors.append("Extreme fear — much already priced in, limits downside")

    # Convert to adjustment factor
    if vulnerability_score >= 5:
        adjustment = "severe"
        factor = 1.5
    elif vulnerability_score >= 3:
        adjustment = "elevated"
        factor = 1.25
    elif vulnerability_score >= 1:
        adjustment = "moderate"
        factor = 1.1
    elif vulnerability_score <= -1:
        adjustment = "cushioned"
        factor = 0.8
    else:
        adjustment = "neutral"
        factor = 1.0

    return {
        "adjustment": adjustment,
        "factor": round(factor, 2),
        "vulnerability_score": vulnerability_score,
        "factors": factors,
    }


# ── Cascade Builder ─────────────────────────────────────────────


def _build_cascade(scenario: dict, context: dict) -> list[dict]:
    """Build the transmission cascade with context-adjusted severity."""
    factor = context.get("factor", 1.0)
    cascade = []

    for step in scenario.get("transmission", []):
        adjusted = {
            "step": step["step"],
            "channel": step["channel"],
            "effect": step["effect"],
            "assets_affected": step["assets_affected"],
            "confidence": step["confidence"],
        }

        # Add severity note if context amplifies
        if factor > 1.1:
            adjusted["context_note"] = (
                f"Impact amplified ~{factor:.1f}x by current vulnerability context"
            )
        elif factor < 0.9:
            adjusted["context_note"] = (
                "Impact may be cushioned — extreme fear already priced in"
            )

        cascade.append(adjusted)

    return cascade


# ── Portfolio Impact ────────────────────────────────────────────


def _estimate_portfolio_impact(scenario: dict, context: dict) -> dict:
    """Estimate impact on common portfolio types."""
    factor = context.get("factor", 1.0)

    # Parse the net_spx_impact range
    spx_impact = scenario.get("net_spx_impact", "0%")
    low, high = _parse_impact_range(spx_impact)
    adjusted_low = low * factor
    adjusted_high = high * factor

    portfolios = {
        "60_40_traditional": {
            "description": "60% US equity / 40% US Agg bonds",
            "estimated_impact": f"{adjusted_low * 0.65:+.0f}% to {adjusted_high * 0.65:+.0f}%",
            "note": "Bond hedge may or may not work depending on scenario type",
        },
        "all_equity": {
            "description": "100% diversified equity",
            "estimated_impact": f"{adjusted_low:+.0f}% to {adjusted_high:+.0f}%",
            "note": "Full exposure to equity cascade",
        },
        "risk_parity": {
            "description": "Leveraged risk parity (Dalio-style)",
            "estimated_impact": f"{adjusted_low * 0.8:+.0f}% to {adjusted_high * 0.8:+.0f}%",
            "note": "Leverage amplifies vol shock; forced deleveraging likely",
        },
        "barbell": {
            "description": "Taleb barbell: 85% T-bills + 15% aggressive",
            "estimated_impact": f"{adjusted_low * 0.2:+.0f}% to {adjusted_high * 0.2:+.0f}%",
            "note": "Maximum drawdown capped by T-bill allocation; aggressive tail gains if vol spikes",
        },
    }

    return portfolios


def _parse_impact_range(impact_str: str) -> tuple[float, float]:
    """Parse impact strings like '-8 to -15%' into (low, high) tuple."""
    import re
    numbers = re.findall(r'[+-]?\d+\.?\d*', impact_str)
    if len(numbers) >= 2:
        return float(numbers[0]), float(numbers[1])
    elif len(numbers) == 1:
        val = float(numbers[0])
        return val, val
    return 0.0, 0.0


# ── Vulnerability Identification ────────────────────────────────


def _identify_vulnerabilities(scenario: dict, briefing: dict) -> list[dict]:
    """Identify which current positions/conditions are most exposed."""
    if not briefing:
        return []

    vulnerabilities = []
    trigger = scenario.get("trigger", {})
    trigger_asset = trigger.get("asset", "")

    # Check if we're already trending in the stress direction
    regime = briefing.get("regime", {})
    quadrant = regime.get("quadrant")

    if trigger_asset == "oil" and quadrant == "stagflation":
        vulnerabilities.append({
            "exposure": "Regime already stagflationary",
            "severity": "high",
            "detail": "Oil spike would intensify existing stagflation, not create a new regime shift",
        })

    if trigger_asset == "VIX":
        vix = _safe_get(briefing, "sentiment", "raw", "vix", "spot")
        if vix is not None and vix > 25:
            vulnerabilities.append({
                "exposure": f"VIX already at {vix:.0f}",
                "severity": "high",
                "detail": "Starting from elevated vol means less room before forced-selling thresholds hit",
            })

    if trigger_asset == "HY_spread":
        credit_cycle = _safe_get(briefing, "private_markets", "credit", "credit_cycle")
        if credit_cycle in ("late_cycle", "stress"):
            vulnerabilities.append({
                "exposure": f"Credit cycle already {credit_cycle}",
                "severity": "high",
                "detail": "Late/stress credit cycle means less buffer before defaults accelerate",
            })

    # Check market breadth
    breadth = _safe_get(briefing, "market", "breadth_divergence")
    if breadth is not None and breadth < -3:
        vulnerabilities.append({
            "exposure": f"Narrow market breadth ({breadth:.1f}%)",
            "severity": "medium",
            "detail": "Narrow leadership means if leaders crack, index has no support underneath",
        })

    # Check HY spread level
    hy = _safe_get(briefing, "private_markets", "credit", "hy_spread")
    if hy is not None and hy > 5.0:
        vulnerabilities.append({
            "exposure": f"HY spreads already wide ({hy:.2f}%)",
            "severity": "medium",
            "detail": "Credit markets already signaling stress; additional shock amplifies",
        })

    return vulnerabilities


# ── Hedging Suggestions ─────────────────────────────────────────


def _suggest_hedges(scenario: dict, context: dict) -> list[dict]:
    """Generate framework-specific hedging suggestions for the scenario."""
    trigger_asset = scenario.get("trigger", {}).get("asset", "")
    hedges = []

    # Universal hedges
    hedges.append({
        "framework": "Tudor Jones",
        "hedge": "Reduce overall position sizes by 30-50%",
        "rationale": "First rule of defense: get smaller. You can always re-enter.",
        "cost": "Opportunity cost if scenario doesn't materialize",
    })

    # Scenario-specific hedges
    if trigger_asset in ("oil", "10Y_yield"):
        hedges.append({
            "framework": "Dalio (All-Weather)",
            "hedge": "Increase TIPS and commodity allocation; reduce nominal bonds",
            "rationale": "Inflation-linked assets hedge the input cost / rate shock channel",
            "cost": "TIPS underperform if inflation expectations fall",
        })
        hedges.append({
            "framework": "Taleb (barbell)",
            "hedge": "Buy OTM puts on QQQ/IWM; fund with premium from selling covered calls",
            "rationale": "Asymmetric payoff: small cost for large payout if cascade plays out",
            "cost": "Premium decay if market stays flat",
        })

    if trigger_asset in ("VIX", "HY_spread", "China_financials"):
        hedges.append({
            "framework": "Marks (contrarian)",
            "hedge": "Prepare buy list of high-quality names at extreme discounts",
            "rationale": "Crisis creates opportunity. Forced selling drives prices below intrinsic value.",
            "cost": "Opportunity cost of cash; risk of catching falling knife",
        })
        hedges.append({
            "framework": "Soros (reflexive)",
            "hedge": "Short credit via HYG puts or CDX protection",
            "rationale": "Credit cascade is self-reinforcing: wider spreads → less lending → more stress",
            "cost": "Carry cost; credit can stay tight longer than expected",
        })

    if trigger_asset in ("DXY", "Mag7"):
        hedges.append({
            "framework": "Druckenmiller (rotation)",
            "hedge": "Rotate from US large-cap to international and small-cap value",
            "rationale": "Dollar weakness / concentration unwind benefits the anti-Mag7 trade",
            "cost": "If dollar strengthens or AI narrative reasserts, trade reverses",
        })

    # Context-dependent
    if context.get("adjustment") in ("severe", "elevated"):
        hedges.append({
            "framework": "Greenblatt (margin of safety)",
            "hedge": "Raise cash to 20-30% of portfolio",
            "rationale": (
                "Current vulnerability context is elevated — cash provides optionality "
                "to buy at better prices after the shock."
            ),
            "cost": "Cash drag if scenario doesn't materialize",
        })

    return hedges


# ── Run All Scenarios ───────────────────────────────────────────


def run_all_stress_tests(briefing: dict) -> dict:
    """Run all pre-built scenarios against current conditions.

    Returns a summary of which scenarios would be most damaging
    given the current vulnerability context.
    """
    results = {}
    for scenario_id in SCENARIO_LIBRARY:
        result = run_stress_test(scenario_id=scenario_id, briefing=briefing)
        # Parse worst-case SPX impact for ranking — use the most negative number
        low, high = _parse_impact_range(result["scenario"]["net_spx_impact"] or "0%")
        worst_case = min(low, high)  # most negative = worst case
        results[scenario_id] = {
            "label": result["scenario"]["label"],
            "net_spx_impact": result["scenario"]["net_spx_impact"],
            "vulnerability_count": len(result["current_vulnerabilities"]),
            "context_adjustment": result["context_adjustments"].get("adjustment", "neutral"),
            "amplification_factor": result["context_adjustments"].get("factor", 1.0),
            "worst_case_spx": worst_case,
        }

    # Sort by: vulnerability count first, then worst-case SPX impact (most negative first)
    ranked = sorted(
        results.items(),
        key=lambda x: (x[1]["vulnerability_count"], -x[1]["worst_case_spx"]),
        reverse=True,
    )

    return {
        "scenarios": results,
        "most_dangerous": ranked[0][0] if ranked else None,
        "most_dangerous_label": ranked[0][1]["label"] if ranked else None,
        "context_note": (
            "Scenarios ranked by current vulnerability. The 'most dangerous' scenario "
            "is the one where current conditions amplify the impact the most."
        ),
    }


# ── Helpers ─────────────────────────────────────────────────────


def _safe_get(d: dict | None, *keys, default=None):
    """Safely traverse nested dicts. Default only applies at the terminal key."""
    current = d
    for i, key in enumerate(keys):
        if isinstance(current, dict):
            is_last = (i == len(keys) - 1)
            current = current.get(key, default if is_last else None)
        else:
            return default
    return current
