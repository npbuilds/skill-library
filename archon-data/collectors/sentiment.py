"""Sentiment data collector — VIX, Fear/Greed, put/call ratios."""

from datetime import datetime

import requests
import yfinance as yf

from .cache import get_cached, set_cached


def get_vix_data() -> dict:
    """Get VIX level and term structure from yfinance."""
    cached = get_cached("vix_data", ttl_seconds=900)
    if cached:
        return cached

    result = {"timestamp": datetime.now().isoformat()}

    # VIX spot and term structure
    vix_tickers = {"^VIX": "spot", "^VIX3M": "3_month", "^VIX6M": "6_month"}
    for symbol, label in vix_tickers.items():
        try:
            t = yf.Ticker(symbol)
            hist = t.history(period="5d")
            if not hist.empty:
                result[label] = round(hist["Close"].iloc[-1], 2)
        except Exception:
            continue

    # Term structure analysis
    spot = result.get("spot")
    m3 = result.get("3_month")
    if spot is not None and m3 is not None:
        result["term_structure"] = "contango" if m3 > spot else "backwardation"
        result["term_spread"] = round(m3 - spot, 2)

    # VIX regime classification
    if spot is not None:
        if spot < 15:
            result["regime"] = "complacent"
        elif spot < 20:
            result["regime"] = "calm"
        elif spot < 25:
            result["regime"] = "elevated"
        elif spot < 30:
            result["regime"] = "fearful"
        else:
            result["regime"] = "panic"

    set_cached("vix_data", result)
    return result


def get_fear_greed() -> dict:
    """Get CNN Fear & Greed Index."""
    cached = get_cached("fear_greed", ttl_seconds=3600)
    if cached:
        return cached

    result = {"timestamp": datetime.now().isoformat()}

    try:
        url = "https://production.dataviz.cnn.com/index/fearandgreed/graphdata"
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            score = data.get("fear_and_greed", {}).get("score")
            rating = data.get("fear_and_greed", {}).get("rating")
            prev_close = data.get("fear_and_greed", {}).get("previous_close")
            one_week_ago = data.get("fear_and_greed", {}).get("previous_1_week")
            one_month_ago = data.get("fear_and_greed", {}).get("previous_1_month")
            one_year_ago = data.get("fear_and_greed", {}).get("previous_1_year")

            result["score"] = round(score) if score is not None else None
            result["rating"] = rating
            result["previous_close"] = round(prev_close) if prev_close is not None else None
            result["one_week_ago"] = round(one_week_ago) if one_week_ago is not None else None
            result["one_month_ago"] = round(one_month_ago) if one_month_ago is not None else None
            result["one_year_ago"] = round(one_year_ago) if one_year_ago is not None else None
        else:
            result["error"] = f"CNN API returned {resp.status_code}"
    except Exception as e:
        result["error"] = str(e)

    set_cached("fear_greed", result)
    return result


def get_put_call_ratio() -> dict:
    """Get equity and index put/call ratios."""
    cached = get_cached("put_call", ttl_seconds=3600)
    if cached:
        return cached

    result = {"timestamp": datetime.now().isoformat()}

    # Use CBOE data page
    try:
        url = "https://www.cboe.com/us/options/market_statistics/daily/"
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 200:
            # CBOE page may require parsing; fallback to description
            result["note"] = "CBOE put/call data requires page parsing. Use VIX as proxy."
        else:
            result["note"] = "CBOE data unavailable; using VIX data as sentiment proxy"
    except Exception:
        result["note"] = "CBOE data unavailable; using VIX data as sentiment proxy"

    set_cached("put_call", result)
    return result


def get_sentiment_dashboard() -> dict:
    """Aggregate all sentiment indicators into one dashboard."""
    cached = get_cached("sentiment_dashboard", ttl_seconds=3600)
    if cached:
        return cached

    vix = get_vix_data()
    fear_greed = get_fear_greed()
    put_call = get_put_call_ratio()

    result = {
        "vix": vix,
        "fear_greed": fear_greed,
        "put_call": put_call,
        "timestamp": datetime.now().isoformat(),
    }

    # Composite sentiment assessment
    signals = []

    fg_score = fear_greed.get("score")
    if fg_score is not None:
        if fg_score <= 25:
            signals.append(("fear_greed", "extreme_fear"))
        elif fg_score <= 45:
            signals.append(("fear_greed", "fear"))
        elif fg_score <= 55:
            signals.append(("fear_greed", "neutral"))
        elif fg_score <= 75:
            signals.append(("fear_greed", "greed"))
        else:
            signals.append(("fear_greed", "extreme_greed"))

    vix_spot = vix.get("spot")
    if vix_spot is not None:
        if vix_spot > 30:
            signals.append(("vix", "extreme_fear"))
        elif vix_spot > 25:
            signals.append(("vix", "fear"))
        elif vix_spot > 20:
            signals.append(("vix", "elevated"))
        elif vix_spot > 15:
            signals.append(("vix", "neutral"))
        else:
            signals.append(("vix", "complacent"))

    result["signals"] = signals

    # Overall label
    fear_count = sum(1 for _, s in signals if "fear" in s)
    if fear_count >= 2:
        result["overall"] = "fearful"
    elif fear_count == 1:
        result["overall"] = "cautious"
    elif any("greed" in s for _, s in signals):
        result["overall"] = "greedy"
    else:
        result["overall"] = "neutral"

    set_cached("sentiment_dashboard", result)
    return result
