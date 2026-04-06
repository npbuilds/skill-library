"""Alert engine — threshold-based signal detection across all data sources.

Scans the full briefing data for conditions that warrant attention:
regime shifts, extreme readings, divergences, crowding, and upcoming
catalysts. Each alert is prioritized, tagged with the relevant investor
framework, and includes an actionability note.

Alert severity levels:
- critical: Requires immediate attention — regime shift, crisis threshold
- warning: Significant signal — extreme reading, divergence, crowding
- watch: Worth monitoring — approaching threshold, notable pattern

This is a processor, not a collector — it operates on data already
collected by other endpoints.
"""

from __future__ import annotations

from datetime import datetime


def generate_alerts(briefing_data: dict) -> dict:
    """Generate alerts from a complete briefing data package.

    Args:
        briefing_data: The full output from generate_briefing().

    Returns:
        alerts: List of alerts sorted by severity then timestamp
        alert_count: Total alerts by severity
        top_alert: The single most important alert right now
    """
    alerts = []

    alerts.extend(_check_regime(briefing_data))
    alerts.extend(_check_volatility(briefing_data))
    alerts.extend(_check_credit(briefing_data))
    alerts.extend(_check_positioning(briefing_data))
    alerts.extend(_check_breadth(briefing_data))
    alerts.extend(_check_private_markets(briefing_data))
    alerts.extend(_check_catalysts(briefing_data))
    alerts.extend(_check_correlations(briefing_data))

    # Sort: critical first, then warning, then watch
    severity_order = {"critical": 0, "warning": 1, "watch": 2}
    alerts.sort(key=lambda a: severity_order.get(a["severity"], 3))

    # Count by severity
    counts = {"critical": 0, "warning": 0, "watch": 0}
    for a in alerts:
        counts[a["severity"]] = counts.get(a["severity"], 0) + 1

    return {
        "alerts": alerts,
        "alert_count": counts,
        "total": len(alerts),
        "top_alert": alerts[0] if alerts else None,
        "timestamp": datetime.now().isoformat(),
    }


# ── Alert Generators ─────────────────────────────────────────


def _check_regime(data: dict) -> list[dict]:
    """Check for regime-related alerts."""
    alerts = []
    regime = data.get("regime", {})
    quadrant = regime.get("quadrant")
    confidence = regime.get("confidence", 0)

    if quadrant == "stagflation":
        alerts.append({
            "severity": "critical" if confidence > 0.5 else "warning",
            "category": "regime",
            "title": "Stagflation regime detected",
            "detail": (
                f"Growth falling + inflation rising (confidence: {confidence:.0%}). "
                "This is the worst quadrant for traditional 60/40 portfolios — "
                "both stocks and bonds can decline simultaneously."
            ),
            "framework": "Dalio (All-Weather)",
            "action": (
                "Overweight commodities, TIPS, and cash. Underweight long-duration "
                "bonds and growth equities. Consider gold allocation."
            ),
        })

    if quadrant and confidence < 0.3:
        alerts.append({
            "severity": "watch",
            "category": "regime",
            "title": "Low regime confidence — transitional period",
            "detail": (
                f"Regime classified as {quadrant} but confidence is only {confidence:.0%}. "
                "The economy may be transitioning between regimes."
            ),
            "framework": "Dalio (regime transitions)",
            "action": (
                "Reduce directional bets. Regime transitions create whipsaw risk. "
                "Wait for confidence to rise above 50% before sizing positions."
            ),
        })

    return alerts


def _check_volatility(data: dict) -> list[dict]:
    """Check VIX and volatility structure."""
    alerts = []
    vix_data = _safe_get(data, "sentiment", "raw", "vix")
    if not vix_data:
        return alerts

    spot = vix_data.get("spot")
    regime = vix_data.get("regime")
    term = vix_data.get("term_structure")
    spread = vix_data.get("term_spread")

    if spot is not None:
        if spot >= 40:
            alerts.append({
                "severity": "critical",
                "category": "volatility",
                "title": f"VIX at crisis level ({spot:.1f})",
                "detail": (
                    "VIX above 40 has occurred in <5% of trading days historically. "
                    "This level signals systemic fear and potential forced liquidation."
                ),
                "framework": "Taleb (tail risk)",
                "action": (
                    "Do NOT sell into panic unless stops are hit. VIX >40 historically "
                    "marks the peak of acute fear — forward 3-month returns are positive "
                    "75%+ of the time from these levels."
                ),
            })
        elif spot >= 30:
            alerts.append({
                "severity": "warning",
                "category": "volatility",
                "title": f"VIX in panic territory ({spot:.1f})",
                "detail": f"VIX at {spot:.1f} ({regime}). Elevated but not crisis.",
                "framework": "Tudor Jones (defense check)",
                "action": (
                    "Reduce position sizes. 2:1 reward/risk minimum for any new trade. "
                    "Don't add to losing positions."
                ),
            })
        elif spot < 13:
            alerts.append({
                "severity": "warning",
                "category": "volatility",
                "title": f"VIX at complacency level ({spot:.1f})",
                "detail": (
                    "Sub-13 VIX signals extreme complacency. Protection is cheap. "
                    "The market is pricing in virtually no risk of disruption."
                ),
                "framework": "Taleb (antifragility)",
                "action": "Buy tail risk protection — OTM puts and VIX calls are cheap.",
            })

    # Term structure signal
    if term == "backwardation" and spot and spot > 25:
        alerts.append({
            "severity": "watch",
            "category": "volatility",
            "title": "VIX backwardation during elevated vol — peak fear signal",
            "detail": (
                f"VIX term structure inverted (spread: {spread:+.2f}). "
                "Market expects vol to DECREASE from here, even though spot is high. "
                "Historically signals peak of acute fear, not the start of a crisis."
            ),
            "framework": "Contrarian (term structure)",
            "action": (
                "Consider selling vol premium or waiting for contango to return "
                "as confirmation that panic is fading."
            ),
        })

    return alerts


def _check_credit(data: dict) -> list[dict]:
    """Check credit market stress signals."""
    alerts = []
    credit = _safe_get(data, "private_markets", "credit")
    if not credit:
        return alerts

    hy_spread = credit.get("hy_spread")
    bdc_discount = credit.get("bdc_nav_discount")
    credit_cycle = credit.get("credit_cycle")

    # HY spread thresholds (percentage points)
    if hy_spread is not None:
        if hy_spread >= 7.0:
            alerts.append({
                "severity": "critical",
                "category": "credit",
                "title": f"HY spreads at crisis level ({hy_spread:.2f}%)",
                "detail": "Spreads above 700 bps signal potential credit market seizure.",
                "framework": "Marks (credit cycle)",
                "action": "Avoid all credit risk. Cash and Treasuries only.",
            })
        elif hy_spread >= 5.0:
            alerts.append({
                "severity": "warning",
                "category": "credit",
                "title": f"HY spreads signaling stress ({hy_spread:.2f}%)",
                "detail": "Spreads above 500 bps indicate credit markets repricing risk.",
                "framework": "Marks (credit cycle)",
                "action": "Reduce HY exposure. Move up in quality (BBB → A → AA).",
            })

    # BDC NAV discount
    if bdc_discount is not None and bdc_discount < -20:
        alerts.append({
            "severity": "warning",
            "category": "credit",
            "title": f"BDC NAV discount severe ({bdc_discount:.1f}%)",
            "detail": (
                "BDCs trading at >20% discount to book value signals the market "
                "expects significant unrealized credit losses in private lending."
            ),
            "framework": "Greenblatt (public-private divergence)",
            "action": (
                "Private credit funds likely face write-downs next quarter. "
                "Watch for forced secondary sales as opportunity."
            ),
        })

    # Credit-equity divergence
    vix = _safe_get(data, "sentiment", "raw", "vix", "spot")
    if hy_spread is not None and vix is not None:
        if hy_spread < 4.0 and vix > 25:
            alerts.append({
                "severity": "warning",
                "category": "credit",
                "title": "Credit-equity divergence: spreads tight while VIX elevated",
                "detail": (
                    f"HY spreads at {hy_spread:.2f}% (tight) but VIX at {vix:.0f}. "
                    "Credit typically lags equity vol — spreads may widen with a lag."
                ),
                "framework": "Marks (timing error)",
                "action": "Don't trust tight spreads as 'all clear.' Credit is lagging, not leading.",
            })

    return alerts


def _check_positioning(data: dict) -> list[dict]:
    """Check for crowded positioning."""
    alerts = []
    cot = data.get("cot_positioning", {})

    crowded_longs = cot.get("crowded_longs", [])
    for contract in crowded_longs:
        pos = _safe_get(cot, "positions", contract)
        if pos:
            alerts.append({
                "severity": "warning",
                "category": "positioning",
                "title": f"Crowded long: {contract} ({pos.get('net_pct_oi', 0):.1f}% OI)",
                "detail": (
                    f"Speculative positioning in {contract} is at extreme long levels. "
                    "Crowded trades create sharp reversal risk on any catalyst."
                ),
                "framework": "Soros (reflexive reversal)",
                "action": f"Trim or hedge {contract} exposure. Don't initiate new longs here.",
            })

    crowded_shorts = cot.get("crowded_shorts", [])
    for contract in crowded_shorts:
        pos = _safe_get(cot, "positions", contract)
        if pos:
            alerts.append({
                "severity": "warning",
                "category": "positioning",
                "title": f"Crowded short: {contract} ({pos.get('net_pct_oi', 0):.1f}% OI)",
                "detail": (
                    f"Speculative positioning in {contract} is at extreme short levels. "
                    "Short squeeze risk is elevated."
                ),
                "framework": "Soros (reflexive reversal)",
                "action": f"Avoid shorting {contract}. Consider contrarian long for squeeze.",
            })

    return alerts


def _check_breadth(data: dict) -> list[dict]:
    """Check market breadth signals."""
    alerts = []
    market = data.get("market", {})
    breadth = market.get("breadth_divergence")

    if breadth is not None:
        if breadth > 5:
            alerts.append({
                "severity": "watch",
                "category": "breadth",
                "title": f"Extreme breadth divergence: equal-weight leading by {breadth:.1f}%",
                "detail": (
                    "The average stock is significantly outperforming the cap-weighted "
                    "index. This suggests the sell-off is concentrated in mega-cap names, "
                    "not broad-based — which is typically healthier."
                ),
                "framework": "Druckenmiller (rotation detection)",
                "action": "Favor equal-weight (RSP) over cap-weight (SPY). Rotation is real.",
            })
        elif breadth < -5:
            alerts.append({
                "severity": "warning",
                "category": "breadth",
                "title": f"Narrow leadership: cap-weight leading by {abs(breadth):.1f}%",
                "detail": (
                    "Only a few mega-cap names are holding up the index. Narrow leadership "
                    "is historically fragile — when the leaders crack, there's nothing underneath."
                ),
                "framework": "Druckenmiller (liquidity lens)",
                "action": "Market is fragile. Any rotation out of leaders will accelerate the decline.",
            })

    return alerts


def _check_private_markets(data: dict) -> list[dict]:
    """Check private market stress signals."""
    alerts = []
    pm = data.get("private_markets", {})

    exit_window = _safe_get(pm, "exit_window", "exit_window")
    gp_ytd = _safe_get(pm, "exit_window", "gp_avg_ytd")
    divergence = _safe_get(pm, "divergence", "overall_divergence")

    if exit_window == "frozen":
        alerts.append({
            "severity": "warning",
            "category": "private_markets",
            "title": "PE/VC exit window frozen",
            "detail": (
                f"GP stocks avg {gp_ytd:+.0f}% YTD. IPO market weak. "
                "Private funds cannot exit investments — liquidity trapped."
            ) if gp_ytd is not None else "PE/VC exit window classified as frozen.",
            "framework": "Greenblatt (forced selling)",
            "action": (
                "Avoid new PE/VC commitments. Watch for GP-led secondary sales "
                "and denominator-effect forced selling as buying opportunities."
            ),
        })

    if divergence == "severe":
        alerts.append({
            "severity": "critical",
            "category": "private_markets",
            "title": "Severe public-private valuation divergence",
            "detail": (
                "Multiple private asset classes show meaningful divergence from "
                "public proxies. Private marks are likely stale and write-downs "
                "are imminent."
            ),
            "framework": "Marks + Greenblatt (credit cycle + forced selling)",
            "action": "Expect LP capital calls and secondary market dislocation. Prepare cash.",
        })
    elif divergence == "elevated":
        alerts.append({
            "severity": "watch",
            "category": "private_markets",
            "title": "Elevated public-private divergence",
            "detail": (
                "Public proxies suggest private valuations haven't caught up to "
                "market reality. Quarterly marks may disappoint."
            ),
            "framework": "Greenblatt (complexity premium)",
            "action": "Monitor BDC NAV discounts and GP stock performance for escalation.",
        })

    return alerts


def _check_catalysts(data: dict) -> list[dict]:
    """Check for imminent catalysts from the economic calendar."""
    alerts = []

    # Check if calendar data is in the briefing (may not be if endpoint wasn't called)
    calendar = data.get("calendar", {})
    releases = _safe_get(calendar, "releases", "releases", default=[])

    for r in releases:
        days = r.get("days_until", 999)
        impact = r.get("impact", "")

        if impact == "critical" and days <= 3:
            alerts.append({
                "severity": "critical",
                "category": "catalyst",
                "title": f"{r['name']} in {days} day{'s' if days != 1 else ''}",
                "detail": (
                    f"Critical market-moving event on {r['date']}. "
                    "Position sizing and hedging should account for this."
                ),
                "framework": "Tudor Jones (event risk)",
                "action": "Reduce position sizes ahead of the event. Don't gamble on the outcome.",
            })
        elif impact == "high" and days <= 2:
            alerts.append({
                "severity": "warning",
                "category": "catalyst",
                "title": f"{r['name']} in {days} day{'s' if days != 1 else ''}",
                "detail": f"High-impact release on {r['date']}.",
                "framework": "Tudor Jones (event risk)",
                "action": "Factor into position sizing. Avoid adding risk before the release.",
            })

    return alerts


def _check_correlations(data: dict) -> list[dict]:
    """Check for correlation regime changes."""
    alerts = []
    risk = data.get("risk", {})
    corr = risk.get("correlations", {})

    stock_bond = corr.get("stock_bond")
    regime = corr.get("stock_bond_regime")

    if stock_bond is not None and stock_bond > 0.5:
        alerts.append({
            "severity": "warning",
            "category": "correlation",
            "title": f"Positive stock-bond correlation ({stock_bond:.2f})",
            "detail": (
                "Stocks and bonds are moving together — diversification benefit "
                "is impaired. In a positive correlation regime, traditional 60/40 "
                "fails to provide downside protection."
            ),
            "framework": "Dalio (All-Weather) + Taleb (turkey problem)",
            "action": (
                "Add alternative diversifiers: gold, managed futures, or cash. "
                "Bonds are not hedging equity risk right now."
            ),
        })

    return alerts


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
