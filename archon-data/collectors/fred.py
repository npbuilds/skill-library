"""FRED API collector for macroeconomic data. Requires FRED_API_KEY env var."""

import os
from datetime import datetime, timedelta

from .cache import get_cached, set_cached

# FRED series IDs for the Archon's regime intelligence
SERIES = {
    # Growth indicators
    "GDPC1": "Real GDP",
    "UNRATE": "Unemployment Rate",
    "PAYEMS": "Nonfarm Payrolls",
    "USSLIND": "Leading Economic Index",
    # Inflation indicators
    "CPIAUCSL": "CPI All Urban",
    "PCEPILFE": "Core PCE",
    "T5YIE": "5Y Breakeven Inflation",
    "MICH": "Michigan Inflation Expectations",
    # Monetary indicators
    "FEDFUNDS": "Fed Funds Rate",
    "M2SL": "M2 Money Supply",
    # Yield curve
    "DGS10": "10Y Treasury Yield",
    "DGS2": "2Y Treasury Yield",
    "DGS3MO": "3M Treasury Yield",
    "T10Y2Y": "10Y-2Y Spread",
    "T10Y3M": "10Y-3M Spread",
}

# Real estate and credit series for private markets monitor
PRIVATE_MARKET_SERIES = {
    # Real estate
    "CSUSHPINSA": "Case-Shiller US Home Price Index",
    "MORTGAGE30US": "30Y Mortgage Rate",
    "HOUST": "Housing Starts",
    "PERMIT": "Building Permits",
    "RRVRUSQ156N": "Rental Vacancy Rate",
    "NAHBHMI": "NAHB Housing Market Index",
    # Credit spreads
    "BAMLH0A0HYM2": "HY OAS Spread",
    "BAMLC0A4CBBB": "BBB OAS Spread",
    "BAMLC0A1CAAA": "AAA OAS Spread",
    # Leveraged lending
    "DRTSCILM": "Bank Lending Standards (C&I Loans)",
    # Real rates
    "DFII10": "10Y TIPS Real Yield",
}


def _get_fred_client():
    """Create FRED API client. Returns None if no API key."""
    api_key = os.environ.get("FRED_API_KEY")
    if not api_key:
        return None
    try:
        from fredapi import Fred

        return Fred(api_key=api_key)
    except ImportError:
        return None


def _get_series_latest(fred, series_id: str, periods: int = 18) -> dict | None:
    """Get latest value and recent history for a FRED series."""
    try:
        data = fred.get_series(series_id, observation_start=datetime.now() - timedelta(days=periods * 31))
        if data.empty:
            return None

        latest = data.dropna().iloc[-1]
        latest_date = data.dropna().index[-1]

        result = {
            "value": round(float(latest), 4),
            "date": latest_date.strftime("%Y-%m-%d"),
        }

        # Calculate changes where meaningful
        if len(data.dropna()) >= 2:
            prev = data.dropna().iloc[-2]
            result["prev_value"] = round(float(prev), 4)
            result["change"] = round(float(latest - prev), 4)

        # YoY change for monthly/quarterly series
        if len(data.dropna()) >= 12:
            year_ago_idx = max(0, len(data.dropna()) - 13)
            year_ago = data.dropna().iloc[year_ago_idx]
            if year_ago != 0:
                result["yoy_change"] = round(
                    ((float(latest) / float(year_ago)) - 1) * 100, 2
                )

        return result
    except Exception as e:
        return {"error": str(e)}


def get_macro_data() -> dict:
    """Pull all macro indicators from FRED."""
    cached = get_cached("fred_macro", ttl_seconds=14400)  # 4 hours
    if cached:
        return cached

    fred = _get_fred_client()
    if not fred:
        return {
            "error": "FRED_API_KEY not set. Get a free key at api.stlouisfed.org/api_key",
            "timestamp": datetime.now().isoformat(),
        }

    result = {"indicators": {}, "timestamp": datetime.now().isoformat()}

    for series_id, name in SERIES.items():
        data = _get_series_latest(fred, series_id)
        if data:
            result["indicators"][series_id] = {"name": name, **data}

    # Compute derived signals
    indicators = result["indicators"]

    # Yield curve assessment
    spread_10y2y = indicators.get("T10Y2Y", {}).get("value")
    spread_10y3m = indicators.get("T10Y3M", {}).get("value")
    if spread_10y2y is not None:
        if spread_10y2y < 0:
            result["yield_curve_signal"] = "inverted"
        elif spread_10y2y < 0.5:
            result["yield_curve_signal"] = "flat"
        else:
            result["yield_curve_signal"] = "normal"

    # Growth assessment
    ue_rate = indicators.get("UNRATE", {}).get("value")
    ue_change = indicators.get("UNRATE", {}).get("change")
    if ue_rate is not None and ue_change is not None:
        if ue_rate < 4.0 and ue_change <= 0:
            result["labor_signal"] = "strong"
        elif ue_rate < 5.0:
            result["labor_signal"] = "moderate"
        else:
            result["labor_signal"] = "weak"

    # Inflation assessment
    core_pce = indicators.get("PCEPILFE", {}).get("yoy_change")
    cpi = indicators.get("CPIAUCSL", {}).get("yoy_change")
    if core_pce is not None:
        if core_pce > 3.0:
            result["inflation_signal"] = "hot"
        elif core_pce > 2.5:
            result["inflation_signal"] = "elevated"
        elif core_pce > 1.5:
            result["inflation_signal"] = "target"
        else:
            result["inflation_signal"] = "low"

    set_cached("fred_macro", result)
    return result


def get_private_market_macro() -> dict:
    """Pull real estate and credit spread indicators from FRED."""
    cached = get_cached("fred_private_markets", ttl_seconds=14400)
    if cached:
        return cached

    fred = _get_fred_client()
    if not fred:
        return {
            "error": "FRED_API_KEY not set",
            "timestamp": datetime.now().isoformat(),
        }

    result = {"indicators": {}, "timestamp": datetime.now().isoformat()}

    for series_id, name in PRIVATE_MARKET_SERIES.items():
        data = _get_series_latest(fred, series_id)
        if data:
            result["indicators"][series_id] = {"name": name, **data}

    # Derived signals
    indicators = result["indicators"]

    # Credit spread assessment
    hy_oas = indicators.get("BAMLH0A0HYM2", {}).get("value")
    if hy_oas is not None:
        if hy_oas > 600:
            result["credit_signal"] = "distress"
        elif hy_oas > 450:
            result["credit_signal"] = "stressed"
        elif hy_oas > 350:
            result["credit_signal"] = "elevated"
        else:
            result["credit_signal"] = "normal"

    # Mortgage stress
    mortgage = indicators.get("MORTGAGE30US", {}).get("value")
    if mortgage is not None:
        if mortgage > 7.5:
            result["mortgage_signal"] = "severe_stress"
        elif mortgage > 6.5:
            result["mortgage_signal"] = "stressed"
        elif mortgage > 5.5:
            result["mortgage_signal"] = "elevated"
        else:
            result["mortgage_signal"] = "accommodative"

    # Housing cycle
    starts = indicators.get("HOUST", {}).get("value")
    nahb = indicators.get("NAHBHMI", {}).get("value")
    if nahb is not None:
        if nahb > 55:
            result["housing_cycle"] = "expansion"
        elif nahb > 45:
            result["housing_cycle"] = "neutral"
        elif nahb > 35:
            result["housing_cycle"] = "contraction"
        else:
            result["housing_cycle"] = "severe_contraction"

    # Lending standards (positive = tightening)
    lending = indicators.get("DRTSCILM", {}).get("value")
    if lending is not None:
        if lending > 30:
            result["lending_signal"] = "severe_tightening"
        elif lending > 10:
            result["lending_signal"] = "tightening"
        elif lending > -10:
            result["lending_signal"] = "neutral"
        else:
            result["lending_signal"] = "easing"

    set_cached("fred_private_markets", result)
    return result
