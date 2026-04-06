"""Earnings calendar collector — upcoming catalysts via yfinance."""

from datetime import datetime, timedelta

import yfinance as yf

from .cache import get_cached, set_cached

# Major companies to track earnings for (by market cap significance)
WATCHLIST = [
    # Magnificent 7
    "AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META", "TSLA",
    # Financials
    "JPM", "BAC", "GS", "MS", "WFC",
    # Healthcare
    "UNH", "JNJ", "LLY", "PFE",
    # Energy
    "XOM", "CVX",
    # Consumer
    "WMT", "COST", "HD", "NKE",
    # Industrials
    "CAT", "BA", "UPS",
    # Semiconductors
    "AMD", "AVGO", "INTC", "TSM",
]


def get_earnings_calendar() -> dict:
    """Get upcoming earnings dates for major companies.

    Returns the next earnings date for each watchlist company,
    grouped by week. Identifies catalyst-dense periods where
    multiple large-caps report, which tend to drive sector-wide moves.
    """
    cached = get_cached("earnings_calendar", ttl_seconds=43200)  # 12 hours
    if cached:
        return cached

    result = {
        "upcoming": [],
        "by_week": {},
        "timestamp": datetime.now().isoformat(),
    }

    today = datetime.now().date()
    cutoff = today + timedelta(days=42)  # 6 weeks out

    for symbol in WATCHLIST:
        try:
            t = yf.Ticker(symbol)
            cal = t.calendar
            if cal is None:
                continue

            # yfinance returns calendar as a dict or DataFrame
            earnings_date = None
            if isinstance(cal, dict):
                # Newer yfinance versions return dict
                ed = cal.get("Earnings Date")
                if ed:
                    if isinstance(ed, list) and len(ed) > 0:
                        earnings_date = ed[0]
                    elif hasattr(ed, "date"):
                        earnings_date = ed
            elif hasattr(cal, "columns"):
                # DataFrame format
                if "Earnings Date" in cal.columns:
                    vals = cal["Earnings Date"].dropna()
                    if not vals.empty:
                        earnings_date = vals.iloc[0]

            if earnings_date is None:
                continue

            # Normalize to date
            if hasattr(earnings_date, "date"):
                ed = earnings_date.date()
            elif hasattr(earnings_date, "to_pydatetime"):
                ed = earnings_date.to_pydatetime().date()
            else:
                continue

            if ed < today or ed > cutoff:
                continue

            # Get basic info
            info = {}
            try:
                info = t.info or {}
            except Exception:
                pass

            entry = {
                "symbol": symbol,
                "name": info.get("shortName", symbol),
                "earnings_date": ed.isoformat(),
                "days_until": (ed - today).days,
                "market_cap_b": round(info.get("marketCap", 0) / 1e9, 1) if info.get("marketCap") else None,
                "sector": info.get("sector"),
            }

            result["upcoming"].append(entry)

            # Group by week
            week_start = ed - timedelta(days=ed.weekday())
            week_key = f"week_of_{week_start.isoformat()}"
            if week_key not in result["by_week"]:
                result["by_week"][week_key] = {
                    "week_start": week_start.isoformat(),
                    "companies": [],
                    "total_market_cap_b": 0,
                }
            result["by_week"][week_key]["companies"].append(symbol)
            if entry["market_cap_b"]:
                result["by_week"][week_key]["total_market_cap_b"] += entry["market_cap_b"]

        except Exception:
            continue

    # Sort by date
    result["upcoming"].sort(key=lambda x: x["earnings_date"])

    # Round market cap totals
    for week in result["by_week"].values():
        week["total_market_cap_b"] = round(week["total_market_cap_b"], 1)
        week["count"] = len(week["companies"])

    # Identify catalyst-dense weeks
    result["catalyst_weeks"] = []
    for week_key, week_data in result["by_week"].items():
        if week_data["count"] >= 3 or week_data["total_market_cap_b"] > 1000:
            result["catalyst_weeks"].append({
                "week": week_data["week_start"],
                "count": week_data["count"],
                "companies": week_data["companies"],
                "total_market_cap_b": week_data["total_market_cap_b"],
                "alert": f"Heavy earnings week: {week_data['count']} major companies, ${week_data['total_market_cap_b']:.0f}B in market cap",
            })

    result["total_upcoming"] = len(result["upcoming"])
    result["source"] = "yfinance"

    set_cached("earnings_calendar", result)
    return result
