"""Kenneth French factor returns — academic factor data for free."""

import csv
import io
import zipfile
from datetime import datetime, timedelta

import requests

from .cache import get_cached, set_cached

# French data library URLs for key factors
FACTOR_FILES = {
    "market_rf": "F-F_Research_Data_Factors_daily_CSV.zip",
    "momentum": "F-F_Momentum_Factor_daily_CSV.zip",
}

BASE_URL = "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp"


def get_factor_returns() -> dict:
    """Get recent daily factor returns from Kenneth French Data Library.

    Returns Mkt-RF, SMB (size), HML (value), and UMD (momentum) factor
    returns for the last 30 trading days, plus trailing performance stats.
    """
    cached = get_cached("factor_returns", ttl_seconds=86400)  # 24h
    if cached:
        return cached

    result = {"factors": {}, "timestamp": datetime.now().isoformat()}

    # Fetch Fama-French 3 factors + RF
    try:
        ff3 = _fetch_ff_zip(FACTOR_FILES["market_rf"])
        if ff3:
            for factor_name in ["Mkt-RF", "SMB", "HML", "RF"]:
                if factor_name in ff3:
                    series = ff3[factor_name]
                    result["factors"][factor_name] = _summarize_factor(factor_name, series)
    except Exception as e:
        result["ff3_error"] = str(e)

    # Fetch momentum factor
    try:
        mom = _fetch_ff_zip(FACTOR_FILES["momentum"])
        if mom and "Mom" in mom:
            result["factors"]["UMD"] = _summarize_factor("UMD (Momentum)", mom["Mom"])
    except Exception as e:
        result["momentum_error"] = str(e)

    # Factor regime assessment
    if len(result["factors"]) >= 3:
        result["regime"] = _assess_factor_regime(result["factors"])

    result["source"] = "Kenneth French Data Library"
    result["note"] = "Returns in percent. Daily frequency."

    set_cached("factor_returns", result)
    return result


def _fetch_ff_zip(filename: str) -> dict | None:
    """Download and parse a French data library CSV zip file."""
    url = f"{BASE_URL}/{filename}"
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(url, headers=headers, timeout=30)
    if resp.status_code != 200:
        return None

    with zipfile.ZipFile(io.BytesIO(resp.content)) as zf:
        csv_name = [n for n in zf.namelist() if n.endswith(".CSV") or n.endswith(".csv")]
        if not csv_name:
            return None

        with zf.open(csv_name[0]) as f:
            text = f.read().decode("utf-8", errors="ignore")

    # Parse the CSV — French files have header rows before data
    lines = text.strip().split("\n")
    data_started = False
    headers = []
    rows = []

    for line in lines:
        line = line.strip()
        if not line:
            if data_started:
                break  # End of daily data section (annual data follows)
            continue

        parts = [p.strip() for p in line.split(",")]

        # Detect header row (contains factor names)
        if not data_started:
            if any(p in parts for p in ["Mkt-RF", "SMB", "HML", "Mom", "RF"]):
                headers = parts
                data_started = True
                continue
            # Also check for date-like first column
            if len(parts) >= 3 and len(parts[0]) == 8 and parts[0].isdigit():
                headers = ["Date"] + [f"Col{i}" for i in range(1, len(parts))]
                data_started = True

        if data_started:
            if len(parts[0]) != 8 or not parts[0].isdigit():
                continue  # Skip non-data rows
            rows.append(parts)

    if not headers or not rows:
        return None

    # Build dict of factor -> list of (date, value)
    factors = {}
    for i, name in enumerate(headers):
        if i == 0:
            continue  # Skip date column
        name = name.strip()
        if not name:
            continue
        series = []
        for row in rows[-60:]:  # Last 60 trading days
            if i < len(row):
                try:
                    val = float(row[i].strip())
                    date_str = row[0].strip()
                    series.append({"date": date_str, "value": val})
                except ValueError:
                    continue
        if series:
            factors[name] = series

    return factors


def _summarize_factor(name: str, series: list) -> dict:
    """Summarize a factor return series."""
    if not series:
        return {"name": name, "error": "no data"}

    values = [s["value"] for s in series]
    last_30 = values[-30:] if len(values) >= 30 else values
    last_5 = values[-5:] if len(values) >= 5 else values

    cumulative_30d = sum(last_30)
    cumulative_5d = sum(last_5)
    latest = values[-1]

    return {
        "name": name,
        "latest_daily": round(latest, 3),
        "cumulative_5d": round(cumulative_5d, 3),
        "cumulative_30d": round(cumulative_30d, 3),
        "avg_daily_30d": round(sum(last_30) / len(last_30), 4),
        "positive_days_30d": sum(1 for v in last_30 if v > 0),
        "observations": len(values),
        "last_date": series[-1]["date"],
    }


def _assess_factor_regime(factors: dict) -> dict:
    """Determine which factor regime we're in based on recent returns."""
    regime = {"timestamp": datetime.now().isoformat()}

    smb = factors.get("SMB", {}).get("cumulative_30d", 0)
    hml = factors.get("HML", {}).get("cumulative_30d", 0)
    umd = factors.get("UMD", {}).get("cumulative_30d", 0)
    mkt = factors.get("Mkt-RF", {}).get("cumulative_30d", 0)

    # Value vs Growth
    if hml > 1.0:
        regime["value_growth"] = "strong_value"
    elif hml > 0:
        regime["value_growth"] = "mild_value"
    elif hml > -1.0:
        regime["value_growth"] = "mild_growth"
    else:
        regime["value_growth"] = "strong_growth"

    # Size factor
    if smb > 1.0:
        regime["size"] = "small_caps_leading"
    elif smb > -1.0:
        regime["size"] = "neutral"
    else:
        regime["size"] = "large_caps_leading"

    # Momentum
    if umd > 2.0:
        regime["momentum"] = "strong_trend"
    elif umd > 0:
        regime["momentum"] = "mild_trend"
    elif umd > -2.0:
        regime["momentum"] = "reversal_risk"
    else:
        regime["momentum"] = "momentum_crash"

    # Market
    if mkt > 3.0:
        regime["market"] = "strong_risk_on"
    elif mkt > 0:
        regime["market"] = "mild_risk_on"
    elif mkt > -3.0:
        regime["market"] = "mild_risk_off"
    else:
        regime["market"] = "strong_risk_off"

    # Composite regime label
    if regime["value_growth"].startswith("strong_value") and regime["size"] == "small_caps_leading":
        regime["composite"] = "value_rotation"
        regime["note"] = "Classic risk-on rotation from growth to value and small caps"
    elif regime["market"].startswith("strong_risk_off") and regime["momentum"] in ("reversal_risk", "momentum_crash"):
        regime["composite"] = "risk_off_unwind"
        regime["note"] = "Broad deleveraging — crowded trades reversing"
    elif regime["market"].startswith("strong_risk_on") and regime["momentum"].startswith("strong"):
        regime["composite"] = "momentum_driven"
        regime["note"] = "Trend-following dominated — momentum carries"
    else:
        regime["composite"] = "mixed"
        regime["note"] = "No dominant factor regime — selective stock-picking environment"

    return regime
