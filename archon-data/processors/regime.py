"""Regime classifier — Dalio's 2x2 quadrant (Growth × Inflation)."""

from datetime import datetime


def classify_regime(macro_data: dict, yield_data: dict) -> dict:
    """Classify the current macro regime into one of four quadrants.

    Quadrants (Dalio framework):
    - Goldilocks:  Growth rising  + Inflation falling
    - Reflation:   Growth rising  + Inflation rising
    - Stagflation: Growth falling + Inflation rising
    - Deflation:   Growth falling + Inflation falling
    """
    indicators = macro_data.get("indicators", {})

    # ── Growth axis scoring (-1 to +1) ──
    growth_signals = []

    # Unemployment trend (falling = positive)
    ue = indicators.get("UNRATE", {})
    if ue.get("change") is not None:
        if ue["change"] < -0.1:
            growth_signals.append(1.0)
        elif ue["change"] > 0.2:
            growth_signals.append(-1.0)
        elif ue["change"] > 0:
            growth_signals.append(-0.5)
        else:
            growth_signals.append(0.3)

    # Unemployment level
    if ue.get("value") is not None:
        if ue["value"] < 4.0:
            growth_signals.append(0.5)
        elif ue["value"] < 5.0:
            growth_signals.append(0.0)
        else:
            growth_signals.append(-0.5)

    # LEI trend
    lei = indicators.get("USSLIND", {})
    if lei.get("change") is not None:
        if lei["change"] > 0:
            growth_signals.append(0.7)
        else:
            growth_signals.append(-0.7)

    # Yield curve (steepening = growth expectations improving)
    spread = yield_data.get("spread_10y2y")
    if spread is not None:
        if spread > 1.0:
            growth_signals.append(0.5)
        elif spread > 0:
            growth_signals.append(0.2)
        elif spread > -0.5:
            growth_signals.append(-0.3)
        else:
            growth_signals.append(-0.8)

    # ── Inflation axis scoring (-1 to +1) ──
    inflation_signals = []

    # Core PCE YoY
    core_pce = indicators.get("PCEPILFE", {})
    if core_pce.get("yoy_change") is not None:
        pce_val = core_pce["yoy_change"]
        if pce_val > 4.0:
            inflation_signals.append(1.0)
        elif pce_val > 3.0:
            inflation_signals.append(0.7)
        elif pce_val > 2.5:
            inflation_signals.append(0.3)
        elif pce_val > 1.5:
            inflation_signals.append(-0.2)
        else:
            inflation_signals.append(-0.7)

    # CPI YoY
    cpi = indicators.get("CPIAUCSL", {})
    if cpi.get("yoy_change") is not None:
        cpi_val = cpi["yoy_change"]
        if cpi_val > 4.0:
            inflation_signals.append(1.0)
        elif cpi_val > 3.0:
            inflation_signals.append(0.5)
        elif cpi_val > 2.0:
            inflation_signals.append(0.0)
        else:
            inflation_signals.append(-0.5)

    # 5Y breakeven
    be5 = indicators.get("T5YIE", {})
    if be5.get("value") is not None:
        if be5["value"] > 3.0:
            inflation_signals.append(0.8)
        elif be5["value"] > 2.5:
            inflation_signals.append(0.3)
        elif be5["value"] > 2.0:
            inflation_signals.append(0.0)
        else:
            inflation_signals.append(-0.5)

    # ── Compute axis scores ──
    growth_score = sum(growth_signals) / len(growth_signals) if growth_signals else 0
    inflation_score = (
        sum(inflation_signals) / len(inflation_signals) if inflation_signals else 0
    )

    # Insufficient data guard
    total_signals = len(growth_signals) + len(inflation_signals)
    if total_signals < 2:
        return {
            "quadrant": "insufficient_data",
            "description": "Not enough indicators to classify regime. Set FRED_API_KEY for full analysis.",
            "confidence": 0.0,
            "growth_score": round(growth_score, 3),
            "inflation_score": round(inflation_score, 3),
            "growth_signals_count": len(growth_signals),
            "inflation_signals_count": len(inflation_signals),
            "timestamp": datetime.now().isoformat(),
        }

    # ── Classify quadrant ──
    if growth_score > 0 and inflation_score <= 0:
        quadrant = "goldilocks"
        description = "Growth rising, inflation contained — risk assets favored"
    elif growth_score > 0 and inflation_score > 0:
        quadrant = "reflation"
        description = "Growth rising with inflation — commodities and value favored"
    elif growth_score <= 0 and inflation_score > 0:
        quadrant = "stagflation"
        description = "Growth falling with rising inflation — defensive assets, commodities, cash"
    else:
        quadrant = "deflation"
        description = "Growth falling, inflation falling — bonds and duration favored"

    # Confidence based on signal agreement
    growth_agreement = (
        abs(growth_score) if growth_signals else 0
    )
    inflation_agreement = (
        abs(inflation_score) if inflation_signals else 0
    )
    confidence = round((growth_agreement + inflation_agreement) / 2, 2)

    return {
        "quadrant": quadrant,
        "description": description,
        "confidence": min(confidence, 1.0),
        "growth_score": round(growth_score, 3),
        "inflation_score": round(inflation_score, 3),
        "growth_signals_count": len(growth_signals),
        "inflation_signals_count": len(inflation_signals),
        "timestamp": datetime.now().isoformat(),
    }
