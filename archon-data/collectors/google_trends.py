"""Google Trends collector — search interest as real-time sentiment proxy."""

from datetime import datetime

from .cache import get_cached, set_cached

# Investment-relevant search terms grouped by theme
TREND_QUERIES = {
    "fear": ["stock market crash", "recession", "market crash"],
    "greed": ["buy stocks", "best stocks to buy", "how to invest"],
    "inflation": ["inflation", "gold price", "buy gold"],
    "crypto": ["buy bitcoin", "bitcoin", "crypto"],
    "housing": ["housing market crash", "mortgage rates"],
    "geopolitical": ["war", "oil price"],
}


def get_trend_signals() -> dict:
    """Get Google Trends data for investment-relevant search terms.

    Compares current search interest to recent averages to detect
    spikes in fear, greed, or thematic interest. Spikes in fear-related
    terms are historically contrarian bullish at extremes.
    """
    cached = get_cached("google_trends", ttl_seconds=14400)  # 4 hours
    if cached:
        return cached

    result = {
        "themes": {},
        "alerts": [],
        "timestamp": datetime.now().isoformat(),
    }

    try:
        from pytrends.request import TrendReq

        pytrends = TrendReq(hl="en-US", tz=300, timeout=(10, 25))

        for theme, keywords in TREND_QUERIES.items():
            theme_data = {"keywords": {}, "theme_signal": "normal"}

            try:
                pytrends.build_payload(keywords, timeframe="today 3-m", geo="US")
                df = pytrends.interest_over_time()

                if df.empty:
                    theme_data["error"] = "No data returned"
                    result["themes"][theme] = theme_data
                    continue

                # Drop the 'isPartial' column if present
                if "isPartial" in df.columns:
                    df = df.drop(columns=["isPartial"])

                for kw in keywords:
                    if kw not in df.columns:
                        continue

                    series = df[kw]
                    current = int(series.iloc[-1])
                    avg_90d = round(series.mean(), 1)
                    max_90d = int(series.max())
                    min_90d = int(series.min())

                    # Recent vs average ratio
                    recent_5 = series.tail(5).mean()
                    ratio = round(recent_5 / avg_90d, 2) if avg_90d > 0 else 1.0

                    kw_data = {
                        "current": current,
                        "avg_90d": avg_90d,
                        "max_90d": max_90d,
                        "min_90d": min_90d,
                        "recent_vs_avg": ratio,
                    }

                    # Classify intensity
                    if ratio > 2.0:
                        kw_data["intensity"] = "surging"
                    elif ratio > 1.3:
                        kw_data["intensity"] = "elevated"
                    elif ratio > 0.7:
                        kw_data["intensity"] = "normal"
                    else:
                        kw_data["intensity"] = "declining"

                    theme_data["keywords"][kw] = kw_data

                # Theme-level signal
                ratios = [
                    v["recent_vs_avg"]
                    for v in theme_data["keywords"].values()
                    if "recent_vs_avg" in v
                ]
                if ratios:
                    avg_ratio = sum(ratios) / len(ratios)
                    if avg_ratio > 2.0:
                        theme_data["theme_signal"] = "surging"
                        result["alerts"].append({
                            "theme": theme,
                            "level": "high",
                            "message": f"'{theme}' searches surging at {avg_ratio:.1f}x normal",
                        })
                    elif avg_ratio > 1.3:
                        theme_data["theme_signal"] = "elevated"
                    elif avg_ratio < 0.5:
                        theme_data["theme_signal"] = "very_low"

            except Exception as e:
                theme_data["error"] = str(e)

            result["themes"][theme] = theme_data

        # Composite fear/greed from search trends
        fear_data = result["themes"].get("fear", {})
        greed_data = result["themes"].get("greed", {})

        fear_ratios = [
            v["recent_vs_avg"]
            for v in fear_data.get("keywords", {}).values()
            if "recent_vs_avg" in v
        ]
        greed_ratios = [
            v["recent_vs_avg"]
            for v in greed_data.get("keywords", {}).values()
            if "recent_vs_avg" in v
        ]

        if fear_ratios and greed_ratios:
            fear_avg = sum(fear_ratios) / len(fear_ratios)
            greed_avg = sum(greed_ratios) / len(greed_ratios)
            result["search_sentiment"] = {
                "fear_intensity": round(fear_avg, 2),
                "greed_intensity": round(greed_avg, 2),
                "fear_greed_ratio": round(fear_avg / greed_avg, 2) if greed_avg > 0 else None,
            }
            ratio = fear_avg / greed_avg if greed_avg > 0 else 1.0
            if ratio > 2.0:
                result["search_sentiment"]["label"] = "extreme_fear"
            elif ratio > 1.3:
                result["search_sentiment"]["label"] = "fear"
            elif ratio > 0.7:
                result["search_sentiment"]["label"] = "neutral"
            elif ratio > 0.5:
                result["search_sentiment"]["label"] = "greed"
            else:
                result["search_sentiment"]["label"] = "extreme_greed"

    except ImportError:
        result["error"] = "pytrends not installed. Run: pip install pytrends"
    except Exception as e:
        result["error"] = str(e)

    result["source"] = "Google Trends"
    set_cached("google_trends", result)
    return result
