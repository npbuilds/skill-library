"""Composite sentiment index — normalizes and weights multiple indicators."""

from datetime import datetime


def compute_sentiment_score(sentiment_data: dict, market_data: dict) -> dict:
    """Compute a 0-100 composite sentiment score.

    0 = Extreme Fear, 50 = Neutral, 100 = Extreme Greed

    Components and weights:
    - CNN Fear/Greed: 30% (direct market sentiment)
    - VIX level:      25% (implied volatility / fear)
    - Market breadth:  20% (RSP vs SPY divergence as health signal)
    - VIX term:        15% (contango = calm, backwardation = stressed)
    - Momentum:        10% (market trend as sentiment confirmation)
    """
    components = {}
    scores = []
    weights = []

    # 1. CNN Fear/Greed (0-100 already)
    fg = sentiment_data.get("fear_greed", {}).get("score")
    if fg is not None:
        components["fear_greed"] = {"raw": fg, "normalized": fg}
        scores.append(fg)
        weights.append(0.30)

    # 2. VIX level (inverted — high VIX = low score)
    vix_spot = sentiment_data.get("vix", {}).get("spot")
    if vix_spot is not None:
        # VIX 10 → score 90, VIX 20 → 50, VIX 30 → 10, VIX 40+ → 0
        vix_norm = max(0, min(100, 100 - (vix_spot - 10) * (100 / 30)))
        components["vix"] = {"raw": vix_spot, "normalized": round(vix_norm, 1)}
        scores.append(vix_norm)
        weights.append(0.25)

    # 3. Market breadth (RSP vs SPY YTD divergence)
    breadth_div = market_data.get("breadth_divergence")
    if breadth_div is not None:
        # Positive divergence (equal-weight leading) = healthy breadth
        # Range: -10 to +10 → 0 to 100
        breadth_norm = max(0, min(100, 50 + breadth_div * 5))
        components["breadth"] = {
            "raw": breadth_div,
            "normalized": round(breadth_norm, 1),
        }
        scores.append(breadth_norm)
        weights.append(0.20)

    # 4. VIX term structure
    vix_term = sentiment_data.get("vix", {}).get("term_structure")
    if vix_term is not None:
        term_spread = sentiment_data.get("vix", {}).get("term_spread", 0)
        # Contango (positive spread) = calm = higher score
        # Backwardation (negative spread) = stressed = lower score
        term_norm = max(0, min(100, 50 + term_spread * 10))
        components["vix_term"] = {
            "raw": vix_term,
            "spread": term_spread,
            "normalized": round(term_norm, 1),
        }
        scores.append(term_norm)
        weights.append(0.15)

    # 5. Market momentum (S&P 500 YTD)
    sp500_ytd = None
    for name, data in market_data.get("indices", {}).items():
        if "S&P" in name or "500" in name:
            sp500_ytd = data.get("ytd_pct")
            break
    if sp500_ytd is not None:
        # Range: -20% to +20% → 0 to 100
        momentum_norm = max(0, min(100, 50 + sp500_ytd * 2.5))
        components["momentum"] = {
            "raw": sp500_ytd,
            "normalized": round(momentum_norm, 1),
        }
        scores.append(momentum_norm)
        weights.append(0.10)

    # Weighted composite
    if scores and weights:
        total_weight = sum(weights)
        composite = sum(s * w for s, w in zip(scores, weights)) / total_weight
    else:
        composite = 50  # neutral default

    # Label
    if composite <= 20:
        label = "extreme_fear"
    elif composite <= 35:
        label = "fear"
    elif composite <= 50:
        label = "cautious"
    elif composite <= 65:
        label = "neutral"
    elif composite <= 80:
        label = "greed"
    else:
        label = "extreme_greed"

    return {
        "score": round(composite, 1),
        "label": label,
        "components": components,
        "component_count": len(components),
        "timestamp": datetime.now().isoformat(),
    }
