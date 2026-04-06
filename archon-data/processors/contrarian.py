"""Contrarian scorecard — powering §2 Consensus vs. Contrarian.

Synthesizes positioning (COT), sentiment (VIX, composite), behavioral
(Google trends), and market structure (breadth, credit) data into a
structured matrix of consensus beliefs vs. where second-level thinking
disagrees.

Each contrarian view has:
- consensus_belief: What the crowd thinks
- contrarian_read: Where second-level thinking disagrees
- evidence: List of data points supporting the contrarian view
- confidence: H / M / L
- error_type: level / timing / distribution (Marks's three consensus error types)
- actionability: How tradeable this contrarian view is right now

The output feeds directly into Marks's §2 commentary framework.
"""

from __future__ import annotations


def compute_contrarian_scorecard(
    sentiment: dict,
    cot: dict,
    trends: dict,
    market: dict,
    regime: dict,
    risk: dict,
    private_markets: dict,
    assets: dict | None = None,
    sectors: dict | None = None,
) -> dict:
    """Compute the full contrarian scorecard.

    Returns:
        pendulum_position: Where on Marks's fear↔greed pendulum (0-100)
        consensus_beliefs: List of identified consensus views
        contrarian_views: List of contrarian disagreements with evidence
        crowding_alerts: Positions crowded enough for reversal risk
        consensus_accuracy: Which consensus views are probably right
    """
    views = []
    crowding = []

    # ── 1. Equity sentiment: fear vs complacency ─────────────
    equity_view = _assess_equity_consensus(sentiment, cot, market, trends)
    if equity_view:
        views.append(equity_view)

    # ── 2. Gold crowding ─────────────────────────────────────
    gold_view = _assess_gold_crowding(cot, assets)
    if gold_view:
        views.append(gold_view)
        if gold_view.get("_crowding"):
            crowding.append(gold_view["_crowding"])

    # ── 3. Credit complacency vs stress ──────────────────────
    credit_view = _assess_credit_consensus(private_markets, sentiment)
    if credit_view:
        views.append(credit_view)

    # ── 4. Inflation expectations divergence ─────────────────
    inflation_view = _assess_inflation_consensus(regime, trends, assets)
    if inflation_view:
        views.append(inflation_view)

    # ── 5. Rotation durability ───────────────────────────────
    rotation_view = _assess_rotation_consensus(sectors, market, regime)
    if rotation_view:
        views.append(rotation_view)

    # ── 6. Private market complacency ────────────────────────
    pm_view = _assess_private_market_consensus(private_markets)
    if pm_view:
        views.append(pm_view)

    # ── 7. VIX term structure signal ─────────────────────────
    vol_view = _assess_vol_consensus(sentiment, cot)
    if vol_view:
        views.append(vol_view)

    # ── Pendulum position ────────────────────────────────────
    pendulum = _compute_pendulum(sentiment, cot, trends)

    # ── Separate into consensus beliefs and contrarian reads ─
    consensus_beliefs = []
    contrarian_reads = []
    for v in views:
        # Strip internal keys
        clean = {k: v for k, v in v.items() if not k.startswith("_")}
        consensus_beliefs.append({
            "belief": clean["consensus_belief"],
            "strength": clean.get("consensus_strength", "moderate"),
        })
        contrarian_reads.append(clean)

    return {
        "pendulum": pendulum,
        "consensus_beliefs": consensus_beliefs,
        "contrarian_views": contrarian_reads,
        "crowding_alerts": crowding,
        "view_count": len(views),
    }


# ── Individual Consensus Assessments ─────────────────────────


def _assess_equity_consensus(
    sentiment: dict, cot: dict, market: dict, trends: dict
) -> dict | None:
    """Is the crowd positioned for more downside or recovery?"""
    evidence = []

    # Composite sentiment
    composite = _safe_get(sentiment, "composite", "score")
    composite_label = _safe_get(sentiment, "composite", "label")
    vix = _safe_get(sentiment, "raw", "vix", "spot")
    vix_regime = _safe_get(sentiment, "raw", "vix", "regime")

    # COT equity positioning
    spx_cot = _safe_get(cot, "positions", "E-MINI S&P 500")
    spx_net_pct = _safe_get(spx_cot, "net_pct_oi") if spx_cot else None

    # Breadth
    breadth = _safe_get(market, "breadth_divergence")
    breadth_signal = _safe_get(market, "breadth_signal")

    # Google trends greed
    greed_signal = _safe_get(trends, "themes", "greed", "theme_signal")
    how_to_invest = _safe_get(
        trends, "themes", "greed", "keywords", "how to invest", "intensity"
    )

    if composite is None:
        return None

    # Determine consensus
    if composite < 35 and vix_regime in ("panic", "elevated"):
        # Consensus is fearful
        consensus = "More downside ahead — defensive positioning warranted"
        consensus_strength = "strong" if composite < 25 else "moderate"

        # Contrarian: is the fear overdone?
        contrarian_evidence = []
        if breadth and breadth > 3:
            contrarian_evidence.append(
                f"Breadth divergence +{breadth:.1f}% — average stock outperforming indices"
            )
        if spx_net_pct is not None and spx_net_pct < -5:
            contrarian_evidence.append(
                f"Specs net short S&P at {spx_net_pct:.1f}% OI — crowded short = squeeze fuel"
            )
        if greed_signal == "declining":
            contrarian_evidence.append(
                "Retail greed searches declining — capitulation signal"
            )
        if how_to_invest == "surging":
            contrarian_evidence.append(
                "'How to invest' surging — new money looking for entry points"
            )

        if contrarian_evidence:
            return {
                "domain": "equities",
                "consensus_belief": consensus,
                "consensus_strength": consensus_strength,
                "contrarian_read": (
                    "Fear may be overdone — breadth and positioning suggest "
                    "the sell-off is concentrated in mega-cap, not broad-based"
                ),
                "evidence": contrarian_evidence,
                "confidence": "M" if len(contrarian_evidence) >= 2 else "L",
                "error_type": "level",
                "actionability": (
                    "Watch for VIX mean reversion below 25 as entry signal. "
                    "Equal-weight over cap-weight if breadth holds."
                ),
            }

    elif composite > 65:
        # Consensus is greedy
        consensus = "Bull market continues — stay long and add"
        contrarian_evidence = []
        if spx_net_pct and spx_net_pct > 10:
            contrarian_evidence.append(
                f"Specs extremely long at {spx_net_pct:.1f}% OI — crowded"
            )
        if vix and vix < 15:
            contrarian_evidence.append(
                f"VIX at {vix:.1f} — complacency, cheap to buy protection"
            )

        if contrarian_evidence:
            return {
                "domain": "equities",
                "consensus_belief": consensus,
                "consensus_strength": "strong",
                "contrarian_read": (
                    "Positioning is crowded long — the asymmetry now favors "
                    "owning downside protection over adding equity exposure"
                ),
                "evidence": contrarian_evidence,
                "confidence": "M",
                "error_type": "timing",
                "actionability": "Buy puts or VIX calls as portfolio insurance.",
            }

    else:
        # Mixed / no strong consensus — note the ambiguity
        return {
            "domain": "equities",
            "consensus_belief": "No strong directional consensus — market is uncertain",
            "consensus_strength": "weak",
            "contrarian_read": (
                "Uncertainty itself is the signal. When consensus is absent, "
                "the next catalyst (earnings, Fed, geopolitical) will have outsized impact."
            ),
            "evidence": [
                f"Composite sentiment at {composite:.0f} (neutral zone)",
                f"VIX at {vix:.1f} ({vix_regime})" if vix else "VIX unavailable",
                f"Breadth divergence: {breadth:+.1f}% ({breadth_signal})"
                if breadth else "Breadth unavailable",
            ],
            "confidence": "L",
            "error_type": "distribution",
            "actionability": (
                "Position for the catalyst, not the direction. "
                "Straddles or barbells outperform directional bets here."
            ),
        }


def _assess_gold_crowding(cot: dict, assets: dict | None) -> dict | None:
    """Is gold positioning dangerously crowded?"""
    gold_cot = _safe_get(cot, "positions", "GOLD")
    if not gold_cot:
        return None

    net_pct = gold_cot.get("net_pct_oi", 0)
    signal = gold_cot.get("signal", "neutral")

    gold_ytd = _safe_get(assets, "assets", "Gold (GLD)", "ytd_pct") if assets else None

    if signal == "extreme_long" or net_pct > 30:
        evidence = [
            f"Gold specs net long at {net_pct:.1f}% OI — extreme crowding",
        ]
        if gold_ytd is not None:
            evidence.append(f"Gold YTD: {gold_ytd:+.1f}% — strong rally fueling the crowd")

        crowding_alert = {
            "asset": "Gold",
            "net_pct_oi": net_pct,
            "direction": "long",
            "risk": "Crowded long creates sharp reversal risk on any dollar strength or rate spike",
        }

        return {
            "domain": "gold",
            "consensus_belief": "Gold is a safe haven — buy and hold for protection",
            "consensus_strength": "strong",
            "contrarian_read": (
                "Gold positioning is at extreme levels. The 'safe haven' trade "
                "is now the consensus trade, which paradoxically makes it less safe. "
                "A sharp reversal is possible on any USD strength catalyst."
            ),
            "evidence": evidence,
            "confidence": "H",
            "error_type": "timing",
            "actionability": (
                "Trim long gold positions or buy put protection. "
                "Don't initiate new longs at these positioning levels."
            ),
            "_crowding": crowding_alert,
        }

    return None


def _assess_credit_consensus(
    private_markets: dict, sentiment: dict
) -> dict | None:
    """Is credit pricing in enough risk?"""
    hy_spread = _safe_get(private_markets, "credit", "hy_spread")
    bdc_discount = _safe_get(private_markets, "credit", "bdc_nav_discount")
    credit_cycle = _safe_get(private_markets, "credit", "credit_cycle")
    vix = _safe_get(sentiment, "raw", "vix", "spot")

    if hy_spread is None:
        return None

    evidence = []

    # Tight spreads + high VIX = divergence
    if hy_spread < 4.0 and vix and vix > 25:
        evidence.append(
            f"HY spreads at {hy_spread:.2f}% ({hy_spread*100:.0f} bps, tight) while VIX at {vix:.0f} — "
            "equity market pricing fear that credit isn't"
        )

    # BDC NAV discount signals unrealized losses
    if bdc_discount is not None and bdc_discount < -10:
        evidence.append(
            f"BDCs at {bdc_discount:.1f}% NAV discount — public market pricing "
            "credit losses that private funds haven't marked"
        )

    # Late cycle classification
    if credit_cycle in ("late_cycle", "stress"):
        evidence.append(f"Credit cycle classified as {credit_cycle}")

    if len(evidence) >= 2:
        return {
            "domain": "credit",
            "consensus_belief": (
                "Credit is fine — spreads are tight, no systemic risk"
            ),
            "consensus_strength": "strong",
            "contrarian_read": (
                "Credit spreads are lagging equity vol — the divergence between "
                "tight HY spreads and wide BDC NAV discounts suggests credit "
                "hasn't repriced to match equity fear. Spreads typically widen "
                "with a lag when VIX sustains above 25."
            ),
            "evidence": evidence,
            "confidence": "H" if len(evidence) >= 3 else "M",
            "error_type": "timing",
            "actionability": (
                "Underweight HY bonds. If BDC NAV discounts widen past -20%, "
                "that's the signal that credit stress is becoming real."
            ),
        }

    return None


def _assess_inflation_consensus(
    regime: dict, trends: dict, assets: dict | None
) -> dict | None:
    """Are inflation expectations aligned or divergent across measures?"""
    regime_quad = _safe_get(regime, "quadrant")
    inflation_signal = _safe_get(trends, "themes", "inflation", "theme_signal")
    inflation_search = _safe_get(
        trends, "themes", "inflation", "keywords", "inflation", "intensity"
    )

    oil_ytd = _safe_get(assets, "assets", "Oil (USO)", "ytd_pct") if assets else None

    if regime_quad not in ("stagflation", "reflation"):
        return None

    evidence = []
    if oil_ytd and oil_ytd > 20:
        evidence.append(f"Oil YTD +{oil_ytd:.0f}% — supply-driven inflation pressure")
    if inflation_search in ("surging", "elevated"):
        evidence.append(f"'Inflation' search interest {inflation_search} — retail feeling the pinch")
    if regime_quad == "stagflation":
        evidence.append("Regime classified as stagflation — growth slowing + inflation sticky")

    if evidence:
        return {
            "domain": "inflation",
            "consensus_belief": (
                "Inflation is transitory / under control — the Fed will handle it"
            ),
            "consensus_strength": "moderate",
            "contrarian_read": (
                "Multiple inflation signals are flashing while markets still price "
                "a 'soft landing' — the risk is that inflation proves stickier than "
                "consensus expects, forcing the Fed to hold rates higher for longer."
            ),
            "evidence": evidence,
            "confidence": "M",
            "error_type": "level",
            "actionability": (
                "Overweight commodities and TIPS. Underweight long-duration bonds. "
                "Energy sector leadership is a proxy for this thesis."
            ),
        }

    return None


def _assess_rotation_consensus(
    sectors: dict | None, market: dict, regime: dict
) -> dict | None:
    """Is the current sector leadership durable or a trap?"""
    if not sectors:
        return None

    leaders = _safe_get(sectors, "leaders", default=[])
    laggards = _safe_get(sectors, "laggards", default=[])
    breadth_div = _safe_get(market, "breadth_divergence")

    if not leaders or not laggards:
        return None

    # Defensive leadership in a non-recessionary regime = potential trap
    defensive_leaders = {"Utilities", "Consumer Staples", "Healthcare"}
    cyclical_leaders = {"Energy", "Materials", "Industrials", "Financials"}
    growth_leaders = {"Technology", "Consumer Discretionary", "Communications"}

    leader_set = set(leaders)
    regime_quad = _safe_get(regime, "quadrant")

    evidence = []

    # Energy + defensive leading while tech lags
    if leader_set & {"Energy"} and "Technology" in laggards:
        evidence.append(
            f"Energy leading ({leaders[0]}) while Tech lagging — "
            "classic stagflation rotation"
        )

    # Breadth divergence adds context
    if breadth_div and breadth_div > 3:
        evidence.append(
            f"Equal-weight outperforming cap-weight by {breadth_div:.1f}% — "
            "rotation away from mega-cap is real"
        )

    if breadth_div and breadth_div < -3:
        evidence.append(
            f"Cap-weight outperforming equal-weight by {abs(breadth_div):.1f}% — "
            "narrow leadership, fragile market"
        )

    if evidence:
        return {
            "domain": "rotation",
            "consensus_belief": (
                f"Current leadership ({', '.join(leaders[:2])}) will continue"
            ),
            "consensus_strength": "moderate",
            "contrarian_read": (
                "Sector rotation tends to overshoot. When everyone chases the "
                "same factor (value/energy in stagflation), the premium gets "
                "crowded. Watch for exhaustion signals in the leaders."
            ),
            "evidence": evidence,
            "confidence": "L",
            "error_type": "timing",
            "actionability": (
                "Don't chase momentum in leaders. Look for quality laggards — "
                "sectors being unfairly punished that have durable earnings."
            ),
        }

    return None


def _assess_private_market_consensus(private_markets: dict) -> dict | None:
    """Are private market valuations realistic?"""
    exit_window = _safe_get(private_markets, "exit_window", "exit_window")
    gp_ytd = _safe_get(private_markets, "exit_window", "gp_avg_ytd")
    divergence = _safe_get(private_markets, "divergence", "overall_divergence")
    divergences = _safe_get(private_markets, "divergence", "divergences", default=[])

    if not exit_window:
        return None

    evidence = []

    if exit_window in ("frozen", "narrowing"):
        evidence.append(
            f"PE/VC exit window is {exit_window} — cannot realize investments"
        )
    if gp_ytd is not None and gp_ytd < -20:
        evidence.append(
            f"PE GP stocks down {gp_ytd:.0f}% YTD — market doubts fee/carry revenue"
        )
    if divergence in ("elevated", "severe"):
        for d in divergences:
            evidence.append(
                f"{d['asset_class']}: {d['public_proxy']} → {d['signal']}"
            )

    if len(evidence) >= 2:
        return {
            "domain": "private_markets",
            "consensus_belief": (
                "Private market valuations are reasonable — the denominator effect "
                "is manageable and marks will hold"
            ),
            "consensus_strength": "moderate",
            "contrarian_read": (
                "Public proxies are screaming that private marks are stale. "
                "GP stock weakness signals the market expects fee/carry impairment. "
                "The next wave of quarterly marks will likely show write-downs, "
                "creating forced selling by funds hitting allocation limits."
            ),
            "evidence": evidence,
            "confidence": "H" if len(evidence) >= 3 else "M",
            "error_type": "timing",
            "actionability": (
                "Avoid new commitments to private credit funds. Watch for GP-led "
                "secondary sales as forced liquidity events — these create "
                "opportunity for buyers."
            ),
        }

    return None


def _assess_vol_consensus(sentiment: dict, cot: dict) -> dict | None:
    """Is the VIX term structure telling a different story?"""
    vix_spot = _safe_get(sentiment, "raw", "vix", "spot")
    term_structure = _safe_get(sentiment, "raw", "vix", "term_structure")
    term_spread = _safe_get(sentiment, "raw", "vix", "term_spread")
    vix_cot = _safe_get(cot, "positions", "VIX FUTURES")
    vix_net_pct = _safe_get(vix_cot, "net_pct_oi") if vix_cot else None

    if not vix_spot or not term_structure:
        return None

    evidence = []

    # Backwardation = market expects vol to decrease (panic is peaking)
    if term_structure == "backwardation" and vix_spot > 25:
        evidence.append(
            f"VIX term structure in backwardation (spread: {term_spread:+.1f}) — "
            "market pricing peak fear NOW, expecting vol to decrease"
        )
        if vix_net_pct is not None and vix_net_pct < 0:
            evidence.append(
                f"Specs net short VIX at {vix_net_pct:.1f}% OI — "
                "betting on vol decline from here"
            )

        return {
            "domain": "volatility",
            "consensus_belief": (
                f"VIX at {vix_spot:.0f} means panic — get out of the way"
            ),
            "consensus_strength": "strong",
            "contrarian_read": (
                "VIX backwardation during high spot VIX historically signals "
                "peak fear, not the start of a crisis. Backwardation means the "
                "market itself expects volatility to DECREASE — the term structure "
                "is contrarian to the spot level."
            ),
            "evidence": evidence,
            "confidence": "M",
            "error_type": "timing",
            "actionability": (
                "Sell VIX puts (if experienced) or wait for contango to return as "
                "confirmation that the panic is fading. Don't buy protection at "
                "peak fear — it's expensive."
            ),
        }

    # Contango + low VIX = complacency
    elif term_structure == "contango" and vix_spot < 15:
        evidence.append(
            f"VIX at {vix_spot:.0f} with steep contango — "
            "complacency, protection is cheap"
        )

        return {
            "domain": "volatility",
            "consensus_belief": "Low vol will persist — smooth sailing ahead",
            "consensus_strength": "moderate",
            "contrarian_read": (
                "Low VIX with steep contango is the best time to buy protection — "
                "it's cheap and the market is pricing minimal risk of disruption."
            ),
            "evidence": evidence,
            "confidence": "M",
            "error_type": "distribution",
            "actionability": (
                "Buy tail risk protection (OTM puts, VIX calls). "
                "The cost is minimal and the payoff is convex."
            ),
        }

    return None


# ── Pendulum Computation ─────────────────────────────────────


def _compute_pendulum(sentiment: dict, cot: dict, trends: dict) -> dict:
    """Compute Marks's fear↔greed pendulum position (0=max fear, 100=max greed).

    Synthesizes multiple signals into a single pendulum reading with
    component breakdown for transparency.
    """
    components = {}
    weights = {}

    # Composite sentiment (heaviest weight — it's already a composite)
    composite = _safe_get(sentiment, "composite", "score")
    if composite is not None:
        components["sentiment_composite"] = composite
        weights["sentiment_composite"] = 0.35

    # VIX regime (inverted — high VIX = fear)
    vix = _safe_get(sentiment, "raw", "vix", "spot")
    if vix is not None:
        # Map VIX 10-50 to pendulum 100-0
        vix_score = max(0, min(100, (50 - vix) / 40 * 100))
        components["vix_level"] = round(vix_score, 1)
        weights["vix_level"] = 0.20

    # COT equity positioning
    spx_cot = _safe_get(cot, "positions", "E-MINI S&P 500")
    if spx_cot:
        net_pct = spx_cot.get("net_pct_oi", 0)
        # Map -20 to +20 → 0 to 100
        cot_score = max(0, min(100, (net_pct + 20) / 40 * 100))
        components["cot_equity"] = round(cot_score, 1)
        weights["cot_equity"] = 0.20

    # Google trends greed vs fear balance
    greed_signal = _safe_get(trends, "themes", "greed", "theme_signal")
    fear_signal = _safe_get(trends, "themes", "fear", "theme_signal")
    if greed_signal or fear_signal:
        signal_map = {"surging": 2, "elevated": 1.5, "normal": 1, "declining": 0.5}
        greed_val = signal_map.get(greed_signal, 1)
        fear_val = signal_map.get(fear_signal, 1)
        # Greed dominance = higher pendulum
        if greed_val + fear_val > 0:
            trend_score = (greed_val / (greed_val + fear_val)) * 100
            components["search_behavior"] = round(trend_score, 1)
            weights["search_behavior"] = 0.15

    # Breadth as a confirming signal
    # (Not directly in inputs but VIX term structure as proxy)
    term = _safe_get(sentiment, "raw", "vix", "term_structure")
    if term:
        term_map = {"contango": 60, "flat": 50, "backwardation": 35}
        components["vol_term_structure"] = term_map.get(term, 50)
        weights["vol_term_structure"] = 0.10

    # Weighted average
    if not components:
        return {"position": 50, "label": "neutral", "components": {}}

    total_weight = sum(weights.values())
    position = sum(
        components[k] * weights[k] / total_weight
        for k in components
    )
    position = round(position, 1)

    # Label
    if position < 20:
        label = "extreme_fear"
    elif position < 35:
        label = "fear"
    elif position < 45:
        label = "cautious"
    elif position < 55:
        label = "neutral"
    elif position < 65:
        label = "optimistic"
    elif position < 80:
        label = "greed"
    else:
        label = "extreme_greed"

    return {
        "position": position,
        "label": label,
        "components": components,
        "interpretation": _pendulum_interpretation(position, label),
    }


def _pendulum_interpretation(position: float, label: str) -> str:
    """Generate Marks-style interpretation of pendulum position."""
    if position < 25:
        return (
            "The pendulum has swung to extreme fear. Historically, this is when "
            "the best buying opportunities emerge — but only for those with the "
            "courage and liquidity to act. The key question: is this fear rational "
            "(structural crisis) or emotional (temporary panic)?"
        )
    elif position < 40:
        return (
            "Fear dominates but hasn't reached capitulation levels. The market "
            "is pricing in bad outcomes — the contrarian question is whether "
            "the bad outcomes are already fully reflected in prices."
        )
    elif position < 60:
        return (
            "The pendulum is near center — neither fear nor greed dominates. "
            "This is the hardest environment for contrarian positioning because "
            "there's no extreme to fade. Wait for the pendulum to swing."
        )
    elif position < 75:
        return (
            "Optimism is building. Not yet at dangerous levels, but this is when "
            "the seeds of future losses are sown. Second-level thinkers should "
            "start building watch lists for defense, not offense."
        )
    else:
        return (
            "Extreme greed — the crowd is convinced nothing can go wrong. "
            "This is when Marks's memo title would be 'It's Time to Be Cautious.' "
            "The best returns from here come from what you DON'T own."
        )


# ── Helpers ──────────────────────────────────────────────────


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
