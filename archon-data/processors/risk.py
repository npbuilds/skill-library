"""Risk dashboard — correlations, VIX term structure, breadth analysis."""

import math
from datetime import datetime, timedelta

import pandas as pd
import yfinance as yf

from collectors.cache import get_cached, set_cached


CORRELATION_ASSETS = {
    "SPY": "S&P 500",
    "TLT": "20Y Treasuries",
    "GLD": "Gold",
    "USO": "Oil",
    "DX-Y.NYB": "Dollar",
    "BTC-USD": "Bitcoin",
    "HYG": "High Yield",
}


def _clean_nan(val: float) -> float | None:
    """Convert NaN/inf to None for JSON safety."""
    if val is None or (isinstance(val, float) and (math.isnan(val) or math.isinf(val))):
        return None
    return val


def get_correlation_matrix(window: int = 30) -> dict:
    """Compute rolling correlation matrix for key assets."""
    cached = get_cached("correlations", ttl_seconds=3600)
    if cached:
        return cached

    result = {"window_days": window, "timestamp": datetime.now().isoformat()}

    end = datetime.now()
    start = end - timedelta(days=window + 30)

    prices = {}
    for symbol, name in CORRELATION_ASSETS.items():
        try:
            t = yf.Ticker(symbol)
            hist = t.history(start=start, end=end)
            if not hist.empty:
                returns = hist["Close"].pct_change().dropna().tail(window)
                prices[name] = returns
        except Exception:
            continue

    if len(prices) < 2:
        result["error"] = "Insufficient data for correlation matrix"
        return result

    df = pd.DataFrame(prices)
    corr = df.corr()

    # Build matrix with NaN safety
    result["matrix"] = {}
    for col in corr.columns:
        result["matrix"][col] = {
            row: _clean_nan(round(corr.loc[row, col], 3))
            for row in corr.index
        }

    # Key correlations to highlight
    highlights = []
    for i, a1 in enumerate(corr.columns):
        for a2 in corr.columns[i + 1:]:
            val = corr.loc[a1, a2]
            if math.isnan(val):
                continue
            if abs(val) > 0.7:
                highlights.append({
                    "pair": f"{a1} / {a2}",
                    "correlation": round(val, 3),
                    "strength": "strong_positive" if val > 0 else "strong_negative",
                })
            elif abs(val) < 0.1:
                highlights.append({
                    "pair": f"{a1} / {a2}",
                    "correlation": round(val, 3),
                    "strength": "uncorrelated",
                })

    result["highlights"] = highlights

    # Stock-bond correlation (key regime indicator) — C1 fix
    spy_tlt = None
    if "S&P 500" in corr.index and "20Y Treasuries" in corr.columns:
        raw = corr.loc["S&P 500", "20Y Treasuries"]
        if not math.isnan(raw):
            spy_tlt = round(raw, 3)

    if spy_tlt is not None:
        result["stock_bond_correlation"] = spy_tlt
        if spy_tlt > 0.3:
            result["stock_bond_regime"] = "positive_correlation"
            result["stock_bond_note"] = "Stocks and bonds moving together — inflation-driven regime"
        elif spy_tlt < -0.3:
            result["stock_bond_regime"] = "negative_correlation"
            result["stock_bond_note"] = "Traditional diversification working — growth-driven regime"
        else:
            result["stock_bond_regime"] = "decorrelated"
            result["stock_bond_note"] = "Stock-bond diversification weakening"

    set_cached("correlations", result)
    return result


def get_risk_dashboard(
    sentiment_data: dict, yield_data: dict, market_data: dict
) -> dict:
    """Aggregate risk metrics into a single dashboard."""
    correlations = get_correlation_matrix()

    vix = sentiment_data.get("vix", {})
    vix_spot = vix.get("spot")
    vix_term = vix.get("term_structure")

    result = {
        "vix": {
            "level": vix_spot,
            "regime": vix.get("regime"),
            "term_structure": vix_term,
            "term_spread": vix.get("term_spread"),
        },
        "yield_curve": {
            "shape": yield_data.get("curve_shape"),
            "spread_10y2y": yield_data.get("spread_10y2y"),
            "rate_regime": yield_data.get("rate_regime"),
        },
        "correlations": {
            "stock_bond": correlations.get("stock_bond_correlation"),
            "stock_bond_regime": correlations.get("stock_bond_regime"),
            "highlights": correlations.get("highlights", []),
        },
        "breadth": {
            "divergence": market_data.get("breadth_divergence"),
            "signal": market_data.get("breadth_signal"),
        },
        "timestamp": datetime.now().isoformat(),
    }

    # Overall risk level
    risk_flags = 0
    if vix_spot is not None and vix_spot > 25:
        risk_flags += 1
    if vix_term == "backwardation":
        risk_flags += 1
    if yield_data.get("curve_shape") in ("inverted", "deeply_inverted"):
        risk_flags += 1
    if correlations.get("stock_bond_regime") == "positive_correlation":
        risk_flags += 1

    if risk_flags >= 3:
        result["overall_risk"] = "extreme"
    elif risk_flags >= 2:
        result["overall_risk"] = "elevated"
    elif risk_flags >= 1:
        result["overall_risk"] = "moderate"
    else:
        result["overall_risk"] = "low"

    result["risk_flags"] = risk_flags

    return result
