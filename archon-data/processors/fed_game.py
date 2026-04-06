"""Fed game theory model — strategic interaction analysis.

Models the Fed-Market-Fiscal interaction as a multi-player game where
each player has objectives, constraints, and strategic options. The model
doesn't predict Fed actions — it maps the decision space, identifies
dominant strategies, and computes where market pricing diverges from
the game-theoretic equilibrium.

Players:
1. The Fed — dual mandate (inflation target + max employment), credibility
2. The Market — prices in expectations, can force the Fed's hand via
   financial conditions
3. Fiscal Authority — deficit spending, debt issuance, political constraints

Key game dynamics:
- Fed vs Market: The "forward guidance game" — Fed signals, market prices,
  Fed reacts to market pricing, creating a reflexive loop
- Fed vs Fiscal: When fiscal dominance emerges, the Fed loses independence
- Market pricing vs reality: When market-implied probabilities diverge from
  the game-theoretic equilibrium, there's a trade
"""

from __future__ import annotations

from datetime import datetime


def analyze_fed_game(
    regime: dict,
    macro: dict,
    yields: dict,
    sentiment: dict | None = None,
    calendar: dict | None = None,
) -> dict:
    """Analyze the current Fed-Market-Fiscal game state.

    Returns:
        fed_position: Current Fed strategic position and constraints
        market_expectations: What the market is pricing
        divergence: Where market pricing diverges from game equilibrium
        scenarios: Probability-weighted Fed action scenarios
        dominant_strategy: The game-theoretic dominant strategy
        fiscal_constraint: Whether fiscal dominance is a factor
    """
    fed = _assess_fed_position(regime, macro)
    market_exp = _assess_market_expectations(yields, macro)
    fiscal = _assess_fiscal_constraint(macro, yields)
    divergence = _compute_divergence(fed, market_exp)
    scenarios = _build_scenarios(fed, market_exp, fiscal, regime)
    dominant = _identify_dominant_strategy(fed, fiscal, regime)

    return {
        "fed_position": fed,
        "market_expectations": market_exp,
        "fiscal_constraint": fiscal,
        "divergence": divergence,
        "scenarios": scenarios,
        "dominant_strategy": dominant,
        "timestamp": datetime.now().isoformat(),
    }


def _assess_fed_position(regime: dict, macro: dict) -> dict:
    """Assess the Fed's current strategic position and constraints."""
    indicators = macro.get("indicators", {})
    inflation_signal = macro.get("inflation_signal")
    labor_signal = macro.get("labor_signal")

    # Current rate
    fed_funds = indicators.get("FEDFUNDS", {}).get("value")
    core_pce_yoy = indicators.get("PCEPILFE", {}).get("yoy_change")
    cpi_yoy = indicators.get("CPIAUCSL", {}).get("yoy_change")
    unemployment = indicators.get("UNRATE", {}).get("value")
    unrate_change = indicators.get("UNRATE", {}).get("change")

    # Fed's objective function
    inflation_gap = None
    if core_pce_yoy is not None:
        inflation_gap = core_pce_yoy - 2.0  # distance from 2% target

    # Mandate tension: is the dual mandate in conflict?
    mandate_tension = "none"
    if inflation_signal == "hot" and labor_signal in ("weak", "moderate"):
        mandate_tension = "high"  # Stagflationary — cutting helps jobs, hurts inflation
    elif inflation_signal == "hot" and labor_signal == "strong":
        mandate_tension = "low"  # Clear: tighten
    elif inflation_signal in ("cool", "target") and labor_signal in ("weak",):
        mandate_tension = "low"  # Clear: ease
    else:
        mandate_tension = "moderate"

    # Credibility constraint
    credibility_risk = "low"
    if inflation_gap is not None and inflation_gap > 1.0:
        credibility_risk = "high"  # Inflation well above target
    elif inflation_gap is not None and inflation_gap > 0.5:
        credibility_risk = "moderate"

    # Policy space (room to cut/hike)
    policy_space = {}
    if fed_funds is not None:
        policy_space["room_to_cut"] = fed_funds  # how much they can cut before zero
        policy_space["restrictive"] = fed_funds > 3.5
        policy_space["neutral_estimate"] = 2.5  # rough r-star proxy

    # Strategic options
    options = _enumerate_fed_options(
        inflation_gap, unemployment, unrate_change, fed_funds, mandate_tension
    )

    return {
        "fed_funds_rate": fed_funds,
        "inflation_gap": _safe_round(inflation_gap),
        "unemployment": unemployment,
        "inflation_signal": inflation_signal,
        "labor_signal": labor_signal,
        "mandate_tension": mandate_tension,
        "credibility_risk": credibility_risk,
        "policy_space": policy_space,
        "strategic_options": options,
    }


def _enumerate_fed_options(
    inflation_gap: float | None,
    unemployment: float | None,
    unrate_change: float | None,
    fed_funds: float | None,
    mandate_tension: str,
) -> list[dict]:
    """Enumerate the Fed's strategic options with payoffs."""
    options = []

    # Option 1: Hold
    hold_payoff = "positive" if mandate_tension == "high" else "neutral"
    options.append({
        "action": "hold",
        "description": "Keep rates unchanged — wait for more data",
        "payoff_if_correct": "Credibility maintained, optionality preserved",
        "payoff_if_wrong": "Behind the curve on whichever mandate is deteriorating faster",
        "game_theory_note": (
            "Hold is the dominant strategy when mandate tension is high — "
            "moving in either direction risks policy error"
        ),
        "probability_weight": 0.5 if mandate_tension == "high" else 0.3,
    })

    # Option 2: Cut
    if fed_funds is not None and fed_funds > 1.0:
        cut_rationale = (
            "Support employment" if mandate_tension == "high"
            else "Normalize from restrictive territory"
        )
        options.append({
            "action": "cut_25bp",
            "description": f"Cut 25bp — {cut_rationale}",
            "payoff_if_correct": "Supports growth without reigniting inflation",
            "payoff_if_wrong": "Inflation re-accelerates, credibility damaged",
            "game_theory_note": (
                "Cutting signals the Fed prioritizes employment over inflation — "
                "markets will test whether inflation is truly controlled"
            ),
            "probability_weight": (
                0.3 if inflation_gap and inflation_gap > 0.5
                else 0.4
            ),
        })

    # Option 3: Hike
    if inflation_gap and inflation_gap > 0.5:
        options.append({
            "action": "hike_25bp",
            "description": "Hike 25bp — reassert inflation-fighting credibility",
            "payoff_if_correct": "Inflation expectations anchored, credibility restored",
            "payoff_if_wrong": "Overtightening into weakness, recession risk increases",
            "game_theory_note": (
                "Hiking when inflation is above target but growth is slowing is "
                "the Volcker playbook — painful short-term but credibility-preserving"
            ),
            "probability_weight": 0.15 if mandate_tension == "high" else 0.1,
        })

    # Option 4: Forward guidance shift
    options.append({
        "action": "guidance_shift",
        "description": "Change forward guidance without rate action",
        "payoff_if_correct": "Moves financial conditions without committing to action",
        "payoff_if_wrong": "Market front-runs and over-prices the shift",
        "game_theory_note": (
            "The cheap option — Fed gets market to do the work via expectations. "
            "But this is a one-shot game: once guidance credibility is spent, "
            "only actual rate moves work."
        ),
        "probability_weight": 0.15,
    })

    # Normalize probabilities
    total = sum(o["probability_weight"] for o in options)
    if total > 0:
        for o in options:
            o["probability_weight"] = _safe_round(o["probability_weight"] / total)

    return options


def _assess_market_expectations(yields: dict, macro: dict) -> dict:
    """Assess what the bond market is pricing about Fed policy."""
    curve = yields.get("yields", {})
    indicators = macro.get("indicators", {})

    rate_2y = curve.get("2Y", {}).get("value")
    rate_10y = curve.get("10Y", {}).get("value")
    fed_funds = indicators.get("FEDFUNDS", {}).get("value")
    spread_10y2y = yields.get("spread_10y2y")

    # Market-implied rate expectations
    implied_cuts = None
    if rate_2y is not None and fed_funds is not None:
        # 2Y yield roughly prices in expected Fed funds over next 2 years
        # If 2Y < fed_funds, market expects cuts
        implied_cuts = _safe_round((fed_funds - rate_2y) * 4)  # rough: each 25bp = 1 cut

    # Term premium signal
    term_premium = None
    if rate_10y is not None and rate_2y is not None:
        term_premium = _safe_round(rate_10y - rate_2y)

    # What's priced in
    pricing_narrative = _build_pricing_narrative(
        fed_funds, rate_2y, rate_10y, implied_cuts, spread_10y2y
    )

    return {
        "fed_funds": fed_funds,
        "two_year": rate_2y,
        "ten_year": rate_10y,
        "spread_10y2y": spread_10y2y,
        "implied_cuts_2y": implied_cuts,
        "term_premium": term_premium,
        "pricing_narrative": pricing_narrative,
    }


def _build_pricing_narrative(
    fed_funds, rate_2y, rate_10y, implied_cuts, spread
) -> str:
    """Build a human-readable narrative of what the market is pricing."""
    parts = []

    if implied_cuts is not None:
        if implied_cuts > 0:
            parts.append(
                f"The market is pricing ~{implied_cuts:.0f} rate cuts over 2 years "
                f"(2Y yield at {rate_2y:.2f}% vs fed funds at {fed_funds:.2f}%)"
            )
        elif implied_cuts < -1:
            parts.append(
                f"The market expects rate HIKES (2Y at {rate_2y:.2f}% vs fed funds at {fed_funds:.2f}%)"
            )
        else:
            parts.append(
                f"The market expects rates roughly unchanged (2Y at {rate_2y:.2f}% ≈ fed funds at {fed_funds:.2f}%)"
            )

    if spread is not None:
        if spread > 0.5:
            parts.append("Positive term premium suggests market sees growth/inflation ahead")
        elif spread < -0.2:
            parts.append("Inverted curve suggests market sees recession risk")
        else:
            parts.append("Flat-ish curve suggests uncertainty about direction")

    return ". ".join(parts) if parts else "Insufficient data for pricing narrative."


def _assess_fiscal_constraint(macro: dict, yields: dict) -> dict:
    """Assess whether fiscal dominance constrains the Fed."""
    rate_10y = yields.get("yields", {}).get("10Y", {}).get("value")
    rate_30y = yields.get("yields", {}).get("30Y", {}).get("value")
    spread_30y10y = yields.get("spread_30y10y")

    # Fiscal dominance signals
    signals = []
    fiscal_risk = "low"

    # Long end steepening = market pricing term premium for fiscal risk
    if spread_30y10y is not None and spread_30y10y > 0.5:
        signals.append(
            f"30Y-10Y spread at {spread_30y10y:.2f}% — elevated term premium, "
            "possibly reflecting fiscal risk"
        )
        fiscal_risk = "moderate"

    if spread_30y10y is not None and spread_30y10y > 0.8:
        fiscal_risk = "elevated"

    # High absolute rate levels constrain fiscal space
    if rate_10y is not None and rate_10y > 5.0:
        signals.append(
            f"10Y yield at {rate_10y:.2f}% — debt service costs becoming constraining"
        )
        fiscal_risk = "elevated"

    return {
        "fiscal_dominance_risk": fiscal_risk,
        "signals": signals,
        "term_premium_proxy": spread_30y10y,
        "description": (
            "Fiscal dominance occurs when government debt issuance becomes so "
            "large that it drives rates more than Fed policy. The Fed loses "
            "effective control of the long end."
        ) if fiscal_risk != "low" else "Fiscal constraint not currently binding.",
    }


def _compute_divergence(fed: dict, market: dict) -> dict:
    """Compute where market pricing diverges from game equilibrium."""
    divergences = []

    implied_cuts = market.get("implied_cuts_2y")
    mandate_tension = fed.get("mandate_tension")
    inflation_gap = fed.get("inflation_gap")

    if implied_cuts is not None:
        # Market pricing many cuts but inflation still above target
        if implied_cuts > 2 and inflation_gap is not None and inflation_gap > 0.5:
            divergences.append({
                "type": "dovish_market_vs_inflation",
                "description": (
                    f"Market pricing {implied_cuts:.0f} cuts but inflation gap is "
                    f"+{inflation_gap:.1f}%. The market may be underestimating "
                    "the Fed's willingness to hold rates high for credibility."
                ),
                "trade_implication": (
                    "If inflation stays sticky, front-end rates will reprice higher — "
                    "short 2Y Treasuries or buy rate puts."
                ),
                "confidence": "M",
            })

        # Market pricing few cuts but economy weakening
        elif implied_cuts < 1 and mandate_tension == "high":
            divergences.append({
                "type": "hawkish_market_vs_employment",
                "description": (
                    "Market barely pricing any cuts despite rising mandate tension. "
                    "If employment deteriorates further, the Fed will be forced to "
                    "cut faster than priced."
                ),
                "trade_implication": (
                    "Long 2Y Treasuries — if employment weakens, the front end rallies."
                ),
                "confidence": "L",
            })

    return {
        "divergences": divergences,
        "has_tradeable_divergence": len(divergences) > 0,
    }


def _build_scenarios(
    fed: dict, market: dict, fiscal: dict, regime: dict
) -> list[dict]:
    """Build probability-weighted Fed action scenarios."""
    scenarios = []
    quadrant = regime.get("quadrant", "unknown")

    # Derive scenarios from the Fed's strategic options
    for option in fed.get("strategic_options", []):
        action = option["action"]

        # Adjust probabilities based on regime
        prob = option.get("probability_weight", 0.25)
        if quadrant == "stagflation":
            if action == "hold":
                prob *= 1.3
            elif action == "cut_25bp":
                prob *= 0.7
        elif quadrant == "deflation":
            if action == "cut_25bp":
                prob *= 1.5
            elif action == "hike_25bp":
                prob *= 0.3

        # Market impact assessment
        market_impact = _assess_market_impact(action, market, regime)

        scenarios.append({
            "action": action,
            "probability": _safe_round(prob),
            "description": option["description"],
            "market_impact": market_impact,
            "game_theory_note": option["game_theory_note"],
        })

    # Renormalize, then cap any single scenario at 95%
    total = sum(s["probability"] or 0 for s in scenarios)
    if total > 0:
        for s in scenarios:
            if s["probability"] is not None:
                s["probability"] = _safe_round(
                    min(s["probability"] / total, 0.95)
                )

    return sorted(scenarios, key=lambda s: s.get("probability", 0) or 0, reverse=True)


def _assess_market_impact(action: str, market: dict, regime: dict) -> dict:
    """Assess likely market impact of a Fed action."""
    impacts = {
        "hold": {
            "equities": "neutral to slightly positive (uncertainty reduced)",
            "bonds": "front end stable, long end driven by data",
            "dollar": "supportive (rates stay high)",
            "gold": "neutral",
        },
        "cut_25bp": {
            "equities": "initially positive, but depends on 'why' — growth scare cut is bearish",
            "bonds": "rally (front end leads)",
            "dollar": "weaker",
            "gold": "positive",
        },
        "hike_25bp": {
            "equities": "sharply negative (unexpected tightening)",
            "bonds": "sell-off (front end leads)",
            "dollar": "sharply stronger",
            "gold": "negative",
        },
        "guidance_shift": {
            "equities": "depends on direction of shift",
            "bonds": "front end reprices to new guidance",
            "dollar": "modest move in direction of guidance",
            "gold": "modest inverse to dollar",
        },
    }
    return impacts.get(action, {"note": "impact unclear"})


def _identify_dominant_strategy(fed: dict, fiscal: dict, regime: dict) -> dict:
    """Identify the game-theoretic dominant strategy."""
    mandate = fed.get("mandate_tension", "moderate")
    credibility = fed.get("credibility_risk", "low")
    fiscal_risk = fiscal.get("fiscal_dominance_risk", "low")
    quadrant = regime.get("quadrant", "unknown")

    # Decision logic
    if mandate == "high" and credibility == "high":
        return {
            "strategy": "hold_and_signal",
            "rationale": (
                "High mandate tension + high credibility risk = paralysis. "
                "The Nash equilibrium is to hold rates and use forward guidance "
                "to signal data-dependence. Moving in either direction is a "
                "dominated strategy because the risk of being wrong is symmetric."
            ),
            "confidence": "H",
            "historical_analog": (
                "Similar to 2023 when the Fed held while debating whether "
                "inflation was sticky or transitory with a weakening labor market."
            ),
        }
    elif credibility == "high" and mandate != "high":
        return {
            "strategy": "hawkish_hold_or_hike",
            "rationale": (
                "Credibility is the binding constraint. The Fed must demonstrate "
                "inflation-fighting resolve even if employment softens. The Volcker "
                "lesson: temporary pain preserves long-run credibility."
            ),
            "confidence": "M",
            "historical_analog": "Volcker 1981-82 tightening through recession.",
        }
    elif fiscal_risk in ("elevated",):
        return {
            "strategy": "constrained_easing",
            "rationale": (
                "Fiscal dominance is emerging. The Fed wants to ease but knows "
                "that cutting rates while deficits are large risks losing control "
                "of the long end. The dominant strategy is gradual, well-signaled "
                "cuts to avoid a term premium spike."
            ),
            "confidence": "M",
            "historical_analog": "Post-2020 fiscal expansion constraining monetary normalization.",
        }
    elif quadrant == "deflation":
        return {
            "strategy": "aggressive_easing",
            "rationale": (
                "Both mandates point the same direction — cut decisively. "
                "The risk of doing too little far exceeds the risk of doing too much."
            ),
            "confidence": "H",
            "historical_analog": "March 2020 emergency cuts.",
        }
    else:
        return {
            "strategy": "gradual_normalization",
            "rationale": (
                "No acute pressure on either mandate. The dominant strategy is "
                "gradual normalization toward neutral, adjusting pace based on data."
            ),
            "confidence": "L",
            "historical_analog": "2017-2018 gradual tightening cycle.",
        }


def _safe_round(val, digits=2):
    if val is None:
        return None
    try:
        return round(val, digits)
    except (TypeError, ValueError):
        return None
