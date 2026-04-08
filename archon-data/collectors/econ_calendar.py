"""Economic calendar and Fed speaker schedule collector.

Data sources:
- FRED release calendar (public API, requires FRED_API_KEY)
- Federal Reserve Board website (public, no key)

Provides upcoming economic data releases (CPI, NFP, GDP, FOMC) and
Fed speaker appearances with hawk/dove classifications.
"""

import os
from datetime import date, datetime, timedelta

from .cache import get_cached, set_cached

FRED_KEY = os.environ.get("FRED_API_KEY", "")

# ── High-impact FRED releases to track ───────────────────────

# Maps FRED release IDs to human-readable names and impact levels.
# Release IDs from: https://fred.stlouisfed.org/releases
TRACKED_RELEASES = {
    10:  {"name": "CPI (Consumer Price Index)", "impact": "high", "category": "inflation"},
    46:  {"name": "PCE Price Index", "impact": "high", "category": "inflation"},
    50:  {"name": "Employment Situation (NFP)", "impact": "high", "category": "labor"},
    53:  {"name": "GDP (Advance/Prelim/Final)", "impact": "high", "category": "growth"},
    21:  {"name": "FOMC Meeting Statement", "impact": "critical", "category": "fed"},
    20:  {"name": "FOMC Minutes", "impact": "high", "category": "fed"},
    83:  {"name": "Retail Sales", "impact": "medium", "category": "consumer"},
    13:  {"name": "PPI (Producer Prices)", "impact": "medium", "category": "inflation"},
    18:  {"name": "Industrial Production", "impact": "medium", "category": "growth"},
    82:  {"name": "ISM Manufacturing PMI", "impact": "high", "category": "growth"},
    14:  {"name": "Housing Starts / Building Permits", "impact": "medium", "category": "housing"},
    11:  {"name": "Consumer Confidence", "impact": "medium", "category": "consumer"},
    322: {"name": "Beige Book", "impact": "medium", "category": "fed"},
    103: {"name": "Jobless Claims (Weekly)", "impact": "medium", "category": "labor"},
    101: {"name": "Michigan Consumer Sentiment", "impact": "medium", "category": "consumer"},
    95:  {"name": "Durable Goods Orders", "impact": "medium", "category": "growth"},
}


# ── Fed official classifications ─────────────────────────────

# Current FOMC voting and non-voting members with lean classification.
# Updated manually. Lean can shift — these are baseline tendencies.
FED_OFFICIALS = {
    "Jerome Powell": {"role": "Chair", "lean": "swing", "votes": True},
    "John Williams": {"role": "Vice Chair (NY Fed)", "lean": "dove", "votes": True},
    "Philip Jefferson": {"role": "Vice Chair", "lean": "dove", "votes": True},
    "Michelle Bowman": {"role": "Governor", "lean": "hawk", "votes": True},
    "Christopher Waller": {"role": "Governor", "lean": "hawk", "votes": True},
    "Lisa Cook": {"role": "Governor", "lean": "dove", "votes": True},
    "Adriana Kugler": {"role": "Governor", "lean": "dove", "votes": True},
    "Michael Barr": {"role": "Governor (Supervision)", "lean": "dove", "votes": True},
    # Regional Fed presidents (2026 voters rotate — update annually)
    "Austan Goolsbee": {"role": "Chicago Fed", "lean": "dove", "votes": False},
    "Raphael Bostic": {"role": "Atlanta Fed", "lean": "swing", "votes": False},
    "Susan Collins": {"role": "Boston Fed", "lean": "swing", "votes": False},
    "Mary Daly": {"role": "San Francisco Fed", "lean": "dove", "votes": False},
    "Thomas Barkin": {"role": "Richmond Fed", "lean": "swing", "votes": False},
    "Patrick Harker": {"role": "Philadelphia Fed", "lean": "swing", "votes": False},
    "Loretta Mester": {"role": "Cleveland Fed", "lean": "hawk", "votes": False},
    "Neel Kashkari": {"role": "Minneapolis Fed", "lean": "hawk", "votes": False},
    "James Bullard": {"role": "St. Louis Fed", "lean": "swing", "votes": False},
    "Lorie Logan": {"role": "Dallas Fed", "lean": "hawk", "votes": False},
    "Alberto Musalem": {"role": "St. Louis Fed", "lean": "swing", "votes": False},
    "Jeffrey Schmid": {"role": "Kansas City Fed", "lean": "hawk", "votes": False},
}


# ── FRED Release Calendar ────────────────────────────────────


def get_upcoming_releases(lookahead_days: int = 21) -> dict:
    """Fetch upcoming economic data releases from FRED.

    Uses the FRED releases/dates endpoint to get scheduled releases
    within the lookahead window. Falls back to a static calendar
    if FRED_API_KEY is not available.

    Returns:
        releases: List of upcoming releases with dates and impact levels
        catalyst_weeks: Weeks with 3+ high-impact releases flagged
        fomc_dates: Upcoming FOMC meeting dates specifically highlighted
    """
    cache_key = "econ_calendar"
    cached = get_cached(cache_key, ttl_seconds=3600 * 6)  # 6 hour TTL
    if cached:
        return cached

    today = date.today()
    end_date = today + timedelta(days=lookahead_days)

    releases = []

    if FRED_KEY:
        releases = _fetch_fred_releases(today, end_date)

    if not releases:
        releases = _build_static_calendar(today, end_date)

    # Identify catalyst-dense weeks
    catalyst_weeks = _identify_catalyst_weeks(releases)

    # Pull out FOMC dates specifically
    fomc_dates = [
        r for r in releases
        if r.get("category") == "fed" and "FOMC" in r.get("name", "")
    ]

    result = {
        "releases": releases,
        "catalyst_weeks": catalyst_weeks,
        "fomc_dates": fomc_dates,
        "lookahead_days": lookahead_days,
        "timestamp": datetime.now().isoformat(),
    }

    set_cached(cache_key, result)
    return result


def _fetch_fred_releases(start: date, end: date) -> list[dict]:
    """Fetch release dates from FRED API."""
    try:
        import requests

        url = "https://api.stlouisfed.org/fred/releases/dates"
        params = {
            "api_key": FRED_KEY,
            "file_type": "json",
            "realtime_start": start.isoformat(),
            "realtime_end": end.isoformat(),
            "include_release_dates_with_no_data": "true",
        }
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        releases = []
        for entry in data.get("release_dates", []):
            try:
                release_id = int(entry.get("release_id", 0))
            except (TypeError, ValueError):
                continue
            if release_id in TRACKED_RELEASES:
                meta = TRACKED_RELEASES[release_id]
                releases.append({
                    "date": entry.get("date"),
                    "name": meta["name"],
                    "impact": meta["impact"],
                    "category": meta["category"],
                    "release_id": release_id,
                    "days_until": (date.fromisoformat(entry["date"]) - start).days,
                })

        # Sort by date
        releases.sort(key=lambda r: r["date"])
        return releases

    except Exception as e:
        import sys
        print(f"FRED releases fetch failed: {e}", file=sys.stderr)
        return []


def _build_static_calendar(start: date, end: date) -> list[dict]:
    """Build a static approximate calendar when FRED API isn't available.

    Uses known recurring patterns:
    - NFP: first Friday of each month
    - CPI: ~13th of each month
    - FOMC: roughly every 6 weeks (8 meetings/year)
    - Jobless claims: every Thursday
    """
    releases = []

    current = start
    while current <= end:
        weekday = current.weekday()  # 0=Mon, 6=Sun
        day = current.day
        month = current.month

        # NFP — first Friday
        if weekday == 4 and day <= 7:
            releases.append({
                "date": current.isoformat(),
                "name": "Employment Situation (NFP) [estimated]",
                "impact": "high",
                "category": "labor",
                "days_until": (current - start).days,
                "estimated": True,
            })

        # CPI — around the 13th (Tue/Wed/Thu)
        if 11 <= day <= 14 and weekday in (1, 2, 3):
            # Only add once per month
            already = any(
                r["category"] == "inflation" and r["name"].startswith("CPI")
                and r["date"][:7] == current.isoformat()[:7]
                for r in releases
            )
            if not already:
                releases.append({
                    "date": current.isoformat(),
                    "name": "CPI (Consumer Price Index) [estimated]",
                    "impact": "high",
                    "category": "inflation",
                    "days_until": (current - start).days,
                    "estimated": True,
                })

        # Jobless claims — every Thursday
        if weekday == 3:
            releases.append({
                "date": current.isoformat(),
                "name": "Jobless Claims (Weekly)",
                "impact": "medium",
                "category": "labor",
                "days_until": (current - start).days,
                "estimated": True,
            })

        current += timedelta(days=1)

    releases.sort(key=lambda r: r["date"])
    return releases


def _identify_catalyst_weeks(releases: list[dict]) -> list[dict]:
    """Flag weeks with 2+ high-impact releases (catalyst-dense)."""
    from collections import defaultdict

    weeks = defaultdict(list)
    for r in releases:
        if r["impact"] in ("high", "critical"):
            # ISO week number
            d = date.fromisoformat(r["date"])
            week_key = f"{d.year}-W{d.isocalendar()[1]:02d}"
            weeks[week_key].append(r["name"])

    return [
        {"week": wk, "high_impact_count": len(names), "releases": names}
        for wk, names in sorted(weeks.items())
        if len(names) >= 2  # 2+ high-impact in one week = catalyst dense
    ]


# ── Fed Speaker Schedule ─────────────────────────────────────


def get_fed_speakers() -> dict:
    """Get Fed official information and lean classifications.

    Note: Live Fed speaker schedule scraping is fragile (federalreserve.gov
    doesn't have a stable API). Instead, we provide the official roster with
    hawk/dove classifications so the briefing can contextualize any scheduled
    speeches the user knows about.

    Returns:
        officials: Dict of Fed officials with role, lean, voting status
        hawk_dove_balance: Summary of current FOMC lean balance
        key_voices: Most market-moving speakers ranked
    """
    cache_key = "fed_speakers"
    cached = get_cached(cache_key, ttl_seconds=3600 * 24)  # 24h TTL
    if cached:
        return cached

    hawks = [name for name, info in FED_OFFICIALS.items() if info["lean"] == "hawk"]
    doves = [name for name, info in FED_OFFICIALS.items() if info["lean"] == "dove"]
    swings = [name for name, info in FED_OFFICIALS.items() if info["lean"] == "swing"]

    voting_hawks = [n for n in hawks if FED_OFFICIALS[n]["votes"]]
    voting_doves = [n for n in doves if FED_OFFICIALS[n]["votes"]]
    voting_swings = [n for n in swings if FED_OFFICIALS[n]["votes"]]

    result = {
        "officials": FED_OFFICIALS,
        "hawk_dove_balance": {
            "hawks": len(hawks),
            "doves": len(doves),
            "swings": len(swings),
            "voting_hawks": len(voting_hawks),
            "voting_doves": len(voting_doves),
            "voting_swings": len(voting_swings),
            "lean_summary": (
                "dovish" if len(voting_doves) > len(voting_hawks) + 1
                else "hawkish" if len(voting_hawks) > len(voting_doves) + 1
                else "balanced"
            ),
        },
        "key_voices": [
            {"name": "Jerome Powell", "reason": "Chair sets the tone — all other voices are secondary"},
            {"name": "Christopher Waller", "reason": "Most influential hawk — his shifts signal policy turns"},
            {"name": "John Williams", "reason": "NY Fed runs market operations — closest to market plumbing"},
            {"name": "Philip Jefferson", "reason": "Vice Chair — Powell's likely successor, markets weight his views"},
        ],
        "timestamp": datetime.now().isoformat(),
    }

    set_cached(cache_key, result)
    return result


# ── Combined Calendar ────────────────────────────────────────


def get_economic_calendar() -> dict:
    """Get the combined economic calendar: releases + Fed speaker context.

    This is the master function that the MCP endpoint calls.
    """
    releases = get_upcoming_releases()
    fed = get_fed_speakers()

    # Count upcoming events by category
    category_counts = {}
    for r in releases.get("releases", []):
        cat = r.get("category", "other")
        category_counts[cat] = category_counts.get(cat, 0) + 1

    return {
        "releases": releases,
        "fed_context": fed,
        "category_summary": category_counts,
        "next_critical": next(
            (r for r in releases.get("releases", []) if r["impact"] == "critical"),
            None,
        ),
        "next_high_impact": next(
            (r for r in releases.get("releases", []) if r["impact"] == "high"),
            None,
        ),
    }
