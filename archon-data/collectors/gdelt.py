"""GDELT Project collector — real-time geopolitical event monitoring."""

from datetime import datetime

import requests

from .cache import get_cached, set_cached

# GDELT GKG (Global Knowledge Graph) API
GDELT_API = "https://api.gdeltproject.org/api/v2/doc/doc"

# Geopolitical themes to track (GDELT GCAM themes)
THEMES_TO_TRACK = {
    "TAX_FNCACT_TARIFF": "tariffs",
    "ECON_SANCTIONS": "sanctions",
    "MILITARY_ATTACK": "military_conflict",
    "WMD": "weapons_mass_destruction",
    "CRISISLEX_CRISISLEXREC": "crisis",
    "GENERAL_GOVERNMENT": "government_policy",
    "ECON_INFLATION": "inflation",
    "ECON_INTEREST_RATE": "interest_rates",
    "EPU_POLICY": "policy_uncertainty",
}

# Geopolitical hotspot queries
HOTSPOT_QUERIES = [
    {"name": "iran_conflict", "query": "Iran conflict war Hormuz military", "market": "oil, defense, risk-off"},
    {"name": "china_taiwan", "query": "China Taiwan military strait invasion", "market": "semiconductors, defense, risk-off"},
    {"name": "russia_ukraine", "query": "Russia Ukraine war ceasefire peace", "market": "energy, european equities, wheat"},
    {"name": "us_china_trade", "query": "US China tariff trade war sanctions", "market": "equities, supply chain, EM"},
    {"name": "middle_east", "query": "Israel Gaza Hamas Hezbollah Red Sea Houthi", "market": "oil, shipping, defense"},
    {"name": "ai_regulation", "query": "artificial intelligence regulation policy AI act", "market": "tech, semiconductors"},
]


def get_geopolitical_monitor() -> dict:
    """Monitor geopolitical events and their market-relevant intensity.

    Uses GDELT's free API to track event volumes, sentiment tone, and
    intensity across key geopolitical hotspots.
    """
    cached = get_cached("geopolitical_monitor", ttl_seconds=3600)  # 1 hour
    if cached:
        return cached

    result = {
        "hotspots": {},
        "alerts": [],
        "timestamp": datetime.now().isoformat(),
    }

    headers = {"User-Agent": "Mozilla/5.0"}

    for hotspot in HOTSPOT_QUERIES:
        try:
            params = {
                "query": hotspot["query"],
                "mode": "TimelineVolInfo",
                "timespan": "7d",
                "format": "json",
            }
            resp = requests.get(GDELT_API, params=params, headers=headers, timeout=15)

            if resp.status_code != 200:
                continue

            data = resp.json()
            timeline = data.get("timeline", [])

            if not timeline:
                continue

            # Get the volume timeline data
            vol_series = timeline[0].get("data", []) if timeline else []

            if not vol_series:
                continue

            # Compute metrics from the volume series
            volumes = [entry.get("value", 0) for entry in vol_series if entry.get("value") is not None]

            if not volumes:
                continue

            recent = volumes[-24:] if len(volumes) >= 24 else volumes  # last 24 data points
            avg_volume = sum(volumes) / len(volumes) if volumes else 0
            recent_avg = sum(recent) / len(recent) if recent else 0
            peak = max(volumes)
            latest = volumes[-1] if volumes else 0

            hotspot_data = {
                "name": hotspot["name"],
                "query": hotspot["query"],
                "affected_markets": hotspot["market"],
                "article_volume_7d": sum(volumes),
                "avg_daily_volume": round(avg_volume, 1),
                "recent_volume": round(recent_avg, 1),
                "peak_volume": peak,
                "latest_volume": latest,
                "data_points": len(volumes),
            }

            # Intensity classification
            if avg_volume > 0:
                intensity_ratio = recent_avg / avg_volume
                hotspot_data["intensity_ratio"] = round(intensity_ratio, 2)

                if intensity_ratio > 2.0:
                    hotspot_data["intensity"] = "surging"
                    result["alerts"].append({
                        "hotspot": hotspot["name"],
                        "level": "high",
                        "message": f"{hotspot['name']} coverage surging at {intensity_ratio:.1f}x normal",
                        "affected_markets": hotspot["market"],
                    })
                elif intensity_ratio > 1.3:
                    hotspot_data["intensity"] = "elevated"
                elif intensity_ratio > 0.7:
                    hotspot_data["intensity"] = "normal"
                else:
                    hotspot_data["intensity"] = "declining"
            else:
                hotspot_data["intensity"] = "minimal"

            result["hotspots"][hotspot["name"]] = hotspot_data

        except Exception as e:
            result["hotspots"][hotspot["name"]] = {
                "name": hotspot["name"],
                "error": str(e),
            }

    # Tone analysis for top hotspots
    for name in list(result["hotspots"].keys())[:3]:  # Top 3 by volume
        hotspot = result["hotspots"][name]
        if "error" in hotspot:
            continue
        try:
            query_text = next(h["query"] for h in HOTSPOT_QUERIES if h["name"] == name)
            params = {
                "query": query_text,
                "mode": "ToneChart",
                "timespan": "7d",
                "format": "json",
            }
            resp = requests.get(GDELT_API, params=params, headers=headers, timeout=10)
            if resp.status_code == 200:
                tone_data = resp.json()
                if tone_data:
                    avg_tone = tone_data.get("avgTone")
                    if avg_tone is not None:
                        hotspot["avg_tone"] = round(avg_tone, 2)
                        if avg_tone < -3:
                            hotspot["tone_label"] = "very_negative"
                        elif avg_tone < -1:
                            hotspot["tone_label"] = "negative"
                        elif avg_tone < 1:
                            hotspot["tone_label"] = "neutral"
                        else:
                            hotspot["tone_label"] = "positive"
        except Exception:
            pass

    # Overall geopolitical risk level
    alert_count = len(result["alerts"])
    surging = sum(1 for h in result["hotspots"].values() if h.get("intensity") == "surging")
    elevated = sum(1 for h in result["hotspots"].values() if h.get("intensity") == "elevated")

    if surging >= 2 or alert_count >= 3:
        result["overall_risk"] = "extreme"
    elif surging >= 1 or elevated >= 2:
        result["overall_risk"] = "elevated"
    elif elevated >= 1:
        result["overall_risk"] = "moderate"
    else:
        result["overall_risk"] = "low"

    result["hotspots_tracked"] = len(result["hotspots"])
    result["source"] = "GDELT Project"

    set_cached("geopolitical_monitor", result)
    return result
