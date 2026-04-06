"""Treasury yield curve data from Treasury.gov and yfinance."""

from datetime import datetime

import yfinance as yf

from .cache import get_cached, set_cached

# Treasury yield maturities via yfinance
YIELD_TICKERS = {
    "^IRX": ("3M", 0.25),   # 13-week T-bill
    "^FVX": ("5Y", 5.0),    # 5-year
    "^TNX": ("10Y", 10.0),  # 10-year
    "^TYX": ("30Y", 30.0),  # 30-year
}

# For 2Y we need to use FRED or derive from DGS2 — yfinance doesn't have a clean 2Y ticker
# We'll use yfinance for what it has and supplement


def get_yield_curve() -> dict:
    """Get current Treasury yield curve and spread analysis."""
    cached = get_cached("yield_curve", ttl_seconds=3600)
    if cached:
        return cached

    result = {"yields": {}, "timestamp": datetime.now().isoformat()}

    # Collect available yields from yfinance
    for symbol, (label, maturity) in YIELD_TICKERS.items():
        try:
            t = yf.Ticker(symbol)
            hist = t.history(period="5d")
            if not hist.empty:
                val = hist["Close"].iloc[-1]
                result["yields"][label] = {
                    "value": round(val, 3),
                    "maturity_years": maturity,
                }
        except Exception:
            continue

    # Try to get 2Y from yfinance using the TWO ticker
    try:
        t2y = yf.Ticker("2YY=F")
        hist = t2y.history(period="5d")
        if not hist.empty:
            result["yields"]["2Y"] = {
                "value": round(hist["Close"].iloc[-1], 3),
                "maturity_years": 2.0,
            }
    except Exception:
        pass

    # Spread calculations
    y10 = result["yields"].get("10Y", {}).get("value")
    y2 = result["yields"].get("2Y", {}).get("value")
    y3m = result["yields"].get("3M", {}).get("value")
    y30 = result["yields"].get("30Y", {}).get("value")

    if y10 is not None and y2 is not None:
        spread_10y2y = round(y10 - y2, 3)
        result["spread_10y2y"] = spread_10y2y
    if y10 is not None and y3m is not None:
        spread_10y3m = round(y10 - y3m, 3)
        result["spread_10y3m"] = spread_10y3m
    if y30 is not None and y10 is not None:
        result["spread_30y10y"] = round(y30 - y10, 3)

    # Curve shape classification
    if y10 is not None and y2 is not None:
        spread = y10 - y2
        if spread < -0.2:
            result["curve_shape"] = "deeply_inverted"
        elif spread < 0:
            result["curve_shape"] = "inverted"
        elif spread < 0.25:
            result["curve_shape"] = "flat"
        elif spread < 1.0:
            result["curve_shape"] = "normal"
        else:
            result["curve_shape"] = "steep"

    # Historical context
    if y10 is not None:
        if y10 > 5.0:
            result["rate_regime"] = "restrictive"
        elif y10 > 4.0:
            result["rate_regime"] = "elevated"
        elif y10 > 3.0:
            result["rate_regime"] = "neutral"
        elif y10 > 2.0:
            result["rate_regime"] = "accommodative"
        else:
            result["rate_regime"] = "emergency_low"

    set_cached("yield_curve", result)
    return result
