"""Fund flow proxy collector using ETF volume analysis.

True fund flow data (EPFR, ICI) requires paid subscriptions. This collector
proxies institutional capital flows using publicly available ETF data:

1. Volume-weighted flow signals: unusual volume + price direction reveals
   whether institutions are accumulating or distributing
2. ETF relative volume: current volume vs 20-day average flags abnormal flows
3. Cross-asset flow map: where is capital moving between asset classes?

Data source: yfinance (free, no API key)
"""

import math
from datetime import datetime, timedelta

import yfinance as yf

from .cache import get_cached, set_cached

# ETFs that proxy institutional capital flows across asset classes
FLOW_ETFS = {
    # Equities
    "SPY":  {"name": "S&P 500",           "asset_class": "us_equity",    "style": "large_cap"},
    "QQQ":  {"name": "Nasdaq 100",        "asset_class": "us_equity",    "style": "growth"},
    "IWM":  {"name": "Russell 2000",      "asset_class": "us_equity",    "style": "small_cap"},
    "RSP":  {"name": "S&P Equal Weight",  "asset_class": "us_equity",    "style": "equal_weight"},
    "EFA":  {"name": "Developed Intl",    "asset_class": "intl_equity",  "style": "developed"},
    "EEM":  {"name": "Emerging Markets",  "asset_class": "intl_equity",  "style": "emerging"},
    # Fixed Income
    "TLT":  {"name": "20Y+ Treasuries",   "asset_class": "fixed_income", "style": "long_duration"},
    "SHY":  {"name": "1-3Y Treasuries",   "asset_class": "fixed_income", "style": "short_duration"},
    "HYG":  {"name": "High Yield Corp",   "asset_class": "fixed_income", "style": "high_yield"},
    "LQD":  {"name": "IG Corporate",      "asset_class": "fixed_income", "style": "investment_grade"},
    "TIP":  {"name": "TIPS (Inflation)",   "asset_class": "fixed_income", "style": "inflation_protected"},
    # Alternatives
    "GLD":  {"name": "Gold",              "asset_class": "alternatives", "style": "gold"},
    "USO":  {"name": "Oil",               "asset_class": "alternatives", "style": "oil"},
    # Sector rotation indicators
    "XLE":  {"name": "Energy",            "asset_class": "sector",       "style": "energy"},
    "XLK":  {"name": "Technology",        "asset_class": "sector",       "style": "technology"},
    "XLF":  {"name": "Financials",        "asset_class": "sector",       "style": "financials"},
    "XLU":  {"name": "Utilities",         "asset_class": "sector",       "style": "utilities"},
}


def get_fund_flow_proxies() -> dict:
    """Get ETF-based fund flow proxy signals.

    Returns:
        flows: Per-ETF flow analysis (volume, relative volume, flow signal)
        asset_class_flows: Aggregated flows by asset class
        rotation_signals: Capital rotation patterns
        risk_appetite: Whether flows favor risk-on or risk-off
    """
    cache_key = "fund_flows"
    cached = get_cached(cache_key, ttl_seconds=3600)  # 1 hour TTL
    if cached:
        return cached

    flows = {}
    for symbol, meta in FLOW_ETFS.items():
        flow_data = _analyze_etf_flow(symbol)
        if flow_data:
            flows[symbol] = {**meta, **flow_data}

    # Aggregate by asset class
    asset_flows = _aggregate_asset_class_flows(flows)

    # Detect rotation signals
    rotation = _detect_rotation(flows, asset_flows)

    # Risk appetite score
    risk_appetite = _compute_risk_appetite(flows, asset_flows)

    result = {
        "flows": flows,
        "asset_class_flows": asset_flows,
        "rotation_signals": rotation,
        "risk_appetite": risk_appetite,
        "etfs_tracked": len(flows),
        "timestamp": datetime.now().isoformat(),
    }

    set_cached(cache_key, result)
    return result


def _analyze_etf_flow(symbol: str) -> dict | None:
    """Analyze volume and price for flow signals on a single ETF."""
    try:
        ticker = yf.Ticker(symbol)
        # Get 30 trading days of history for volume analysis
        hist = ticker.history(period="2mo")
        if len(hist) < 20:
            return None

        # Current values (most recent day)
        current_close = float(hist["Close"].iloc[-1])
        current_volume = float(hist["Volume"].iloc[-1])

        # 20-day average volume
        avg_volume_20d = float(hist["Volume"].iloc[-20:].mean())
        if avg_volume_20d == 0:
            return None

        # Relative volume (current vs 20-day avg)
        rel_volume = current_volume / avg_volume_20d

        # 5-day price change
        if len(hist) >= 6:
            price_5d = float(
                ((hist["Close"].iloc[-1] / hist["Close"].iloc[-6]) - 1) * 100
            )
        else:
            price_5d = None

        # 20-day price change
        price_20d = float(
            ((hist["Close"].iloc[-1] / hist["Close"].iloc[-20]) - 1) * 100
        )

        # Dollar volume (proxy for capital flow magnitude)
        dollar_vol = current_close * current_volume
        avg_dollar_vol = float((hist["Close"] * hist["Volume"]).iloc[-20:].mean())

        # Flow signal classification
        signal = _classify_flow(rel_volume, price_5d, price_20d)

        return {
            "price": _safe_round(current_close),
            "volume": int(current_volume),
            "avg_volume_20d": int(avg_volume_20d),
            "relative_volume": _safe_round(rel_volume),
            "dollar_volume_mm": _safe_round(dollar_vol / 1e6),
            "avg_dollar_volume_mm": _safe_round(avg_dollar_vol / 1e6),
            "price_5d_pct": _safe_round(price_5d),
            "price_20d_pct": _safe_round(price_20d),
            "flow_signal": signal,
        }

    except Exception:
        return None


def _classify_flow(rel_volume: float, price_5d: float | None, price_20d: float) -> str:
    """Classify the flow signal based on volume and price action.

    Key patterns:
    - accumulation: high volume + rising price (institutional buying)
    - distribution: high volume + falling price (institutional selling)
    - stealth_accumulation: normal volume + grinding higher (quiet buying)
    - capitulation: very high volume + sharp decline (forced selling / panic)
    - squeeze: high volume + sharp rise from oversold (short squeeze / FOMO)
    - neutral: no notable pattern
    """
    if price_5d is None:
        return "neutral"

    if rel_volume > 2.0 and price_5d < -5:
        return "capitulation"
    elif rel_volume > 2.0 and price_5d > 5:
        return "squeeze"
    elif rel_volume > 1.3 and price_5d > 1:
        return "accumulation"
    elif rel_volume > 1.3 and price_5d < -1:
        return "distribution"
    elif rel_volume < 0.8 and price_20d > 3:
        return "stealth_accumulation"
    elif rel_volume < 0.8 and price_20d < -3:
        return "stealth_distribution"
    else:
        return "neutral"


def _aggregate_asset_class_flows(flows: dict) -> dict:
    """Aggregate flow signals by asset class."""
    from collections import defaultdict

    classes = defaultdict(lambda: {
        "signals": [],
        "avg_rel_volume": [],
        "avg_price_5d": [],
        "total_dollar_vol_mm": 0,
    })

    for symbol, data in flows.items():
        ac = data.get("asset_class", "other")
        classes[ac]["signals"].append(data.get("flow_signal", "neutral"))
        if data.get("relative_volume") is not None:
            classes[ac]["avg_rel_volume"].append(data["relative_volume"])
        if data.get("price_5d_pct") is not None:
            classes[ac]["avg_price_5d"].append(data["price_5d_pct"])
        classes[ac]["total_dollar_vol_mm"] += data.get("dollar_volume_mm", 0)

    result = {}
    for ac, agg in classes.items():
        avg_rv = sum(agg["avg_rel_volume"]) / len(agg["avg_rel_volume"]) if agg["avg_rel_volume"] else None
        avg_p5 = sum(agg["avg_price_5d"]) / len(agg["avg_price_5d"]) if agg["avg_price_5d"] else None

        # Dominant signal
        signal_counts = {}
        for s in agg["signals"]:
            signal_counts[s] = signal_counts.get(s, 0) + 1
        dominant = max(signal_counts, key=signal_counts.get) if signal_counts else "neutral"

        result[ac] = {
            "dominant_signal": dominant,
            "avg_relative_volume": _safe_round(avg_rv),
            "avg_price_5d_pct": _safe_round(avg_p5),
            "total_dollar_volume_mm": _safe_round(agg["total_dollar_vol_mm"]),
            "etf_count": len(agg["signals"]),
        }

    return result


def _detect_rotation(flows: dict, asset_flows: dict) -> list[dict]:
    """Detect capital rotation patterns across asset classes."""
    rotations = []

    # Equity → Fixed Income rotation
    eq_flow = asset_flows.get("us_equity", {})
    fi_flow = asset_flows.get("fixed_income", {})
    eq_signal = eq_flow.get("dominant_signal", "neutral")
    fi_signal = fi_flow.get("dominant_signal", "neutral")

    if eq_signal in ("distribution", "capitulation") and fi_signal in ("accumulation", "stealth_accumulation"):
        rotations.append({
            "type": "risk_off_rotation",
            "from": "equities",
            "to": "fixed_income",
            "strength": "strong" if eq_signal == "capitulation" else "moderate",
            "description": "Capital flowing from equities to bonds — classic risk-off",
        })
    elif eq_signal in ("accumulation", "squeeze") and fi_signal in ("distribution",):
        rotations.append({
            "type": "risk_on_rotation",
            "from": "fixed_income",
            "to": "equities",
            "strength": "strong" if eq_signal == "squeeze" else "moderate",
            "description": "Capital flowing from bonds to equities — risk-on",
        })

    # Large cap → Small cap rotation
    spy = flows.get("SPY", {})
    iwm = flows.get("IWM", {})
    spy_signal = spy.get("flow_signal", "neutral")
    iwm_signal = iwm.get("flow_signal", "neutral")

    if spy_signal in ("distribution", "neutral") and iwm_signal == "accumulation":
        rotations.append({
            "type": "small_cap_rotation",
            "from": "large_cap",
            "to": "small_cap",
            "strength": "moderate",
            "description": "Capital rotating from large-cap to small-cap — breadth expanding",
        })

    # US → International rotation
    us_flow = asset_flows.get("us_equity", {})
    intl_flow = asset_flows.get("intl_equity", {})
    if (us_flow.get("dominant_signal") in ("distribution", "neutral") and
            intl_flow.get("dominant_signal") in ("accumulation",)):
        rotations.append({
            "type": "international_rotation",
            "from": "us_equity",
            "to": "intl_equity",
            "strength": "moderate",
            "description": "Capital rotating from US to international markets",
        })

    # Flight to gold
    gld = flows.get("GLD", {})
    if gld.get("flow_signal") in ("accumulation", "squeeze") and gld.get("relative_volume", 0) > 1.5:
        rotations.append({
            "type": "gold_flight",
            "from": "risk_assets",
            "to": "gold",
            "strength": "strong" if gld["relative_volume"] > 2.0 else "moderate",
            "description": f"Heavy gold accumulation (rel vol: {gld['relative_volume']:.1f}x)",
        })

    # Sector rotation: defensive vs cyclical
    defensive_signals = []
    cyclical_signals = []
    for sym, data in flows.items():
        if data.get("style") in ("utilities",):
            defensive_signals.append(data.get("flow_signal", "neutral"))
        elif data.get("style") in ("energy", "financials", "technology"):
            cyclical_signals.append(data.get("flow_signal", "neutral"))

    def_acc = sum(1 for s in defensive_signals if s in ("accumulation", "stealth_accumulation"))
    cyc_dist = sum(1 for s in cyclical_signals if s in ("distribution", "capitulation"))
    if def_acc > 0 and cyc_dist >= 2:
        rotations.append({
            "type": "defensive_rotation",
            "from": "cyclicals",
            "to": "defensives",
            "strength": "strong",
            "description": "Capital flowing from cyclicals to defensives — late-cycle positioning",
        })

    return rotations


def _compute_risk_appetite(flows: dict, asset_flows: dict) -> dict:
    """Compute an overall risk appetite score from flow data.

    Score: 0 (extreme risk-off) to 100 (extreme risk-on)
    """
    score = 50  # Start neutral
    signals = []

    # Equity flows
    eq = asset_flows.get("us_equity", {})
    eq_signal = eq.get("dominant_signal", "neutral")
    if eq_signal in ("accumulation", "squeeze"):
        score += 15
        signals.append("equity_accumulation")
    elif eq_signal in ("distribution", "capitulation"):
        score -= 15
        signals.append("equity_distribution")

    # Fixed income flows (inverse of risk appetite)
    fi = asset_flows.get("fixed_income", {})
    fi_signal = fi.get("dominant_signal", "neutral")
    if fi_signal in ("accumulation",):
        score -= 10
        signals.append("bond_accumulation (risk-off)")
    elif fi_signal in ("distribution",):
        score += 10
        signals.append("bond_distribution (risk-on)")

    # HY vs IG preference
    hyg = flows.get("HYG", {})
    lqd = flows.get("LQD", {})
    if hyg.get("flow_signal") == "accumulation" and lqd.get("flow_signal") != "accumulation":
        score += 10
        signals.append("HY preferred over IG (risk-on)")
    elif lqd.get("flow_signal") == "accumulation" and hyg.get("flow_signal") != "accumulation":
        score -= 10
        signals.append("IG preferred over HY (risk-off)")

    # Gold as fear proxy
    gld = flows.get("GLD", {})
    if gld.get("flow_signal") in ("accumulation", "squeeze"):
        score -= 5
        signals.append("gold_accumulation (hedging)")

    # Small cap vs large cap
    iwm = flows.get("IWM", {})
    spy = flows.get("SPY", {})
    if iwm.get("flow_signal") == "accumulation":
        score += 5
        signals.append("small_cap_accumulation (risk-on)")
    if spy.get("flow_signal") == "capitulation":
        score -= 10
        signals.append("large_cap_capitulation")

    score = max(0, min(100, score))

    if score < 25:
        label = "extreme_risk_off"
    elif score < 40:
        label = "risk_off"
    elif score < 60:
        label = "neutral"
    elif score < 75:
        label = "risk_on"
    else:
        label = "extreme_risk_on"

    return {
        "score": score,
        "label": label,
        "signals": signals,
    }


def _safe_round(val, digits=2):
    """Round a value safely, handling None and NaN."""
    if val is None:
        return None
    try:
        if math.isnan(val) or math.isinf(val):
            return None
        return round(val, digits)
    except (TypeError, ValueError):
        return None
