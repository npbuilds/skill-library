"""CFTC Commitments of Traders data — institutional positioning signals."""

import csv
import io
from datetime import datetime

import requests

from .cache import get_cached, set_cached

# Key contracts to track and their market mapping
CONTRACTS = {
    "E-MINI S&P 500": "equities",
    "U.S. TREASURY BONDS": "bonds_long",
    "10-YEAR U.S. TREASURY NOTES": "bonds_10y",
    "GOLD": "gold",
    "CRUDE OIL, LIGHT SWEET": "oil",
    "EURO FX": "euro",
    "JAPANESE YEN": "yen",
    "BITCOIN": "bitcoin",
    "VIX FUTURES": "vix",
}

# Column indices for the CFTC deafut.txt (futures-only short format)
# This file has NO header row — positions are fixed.
# Col 0: Market and Exchange Names
# Col 1: As-of Date (YYMMDD)
# Col 2: As-of Date (YYYY-MM-DD)
# Col 7: Open Interest (All)
# Col 8: Non-Commercial Long
# Col 9: Non-Commercial Short
COL_NAME = 0
COL_DATE = 2
COL_OI = 7
COL_NC_LONG = 8
COL_NC_SHORT = 9


def get_cot_positioning() -> dict:
    """Get latest CFTC Commitments of Traders positioning data.

    Returns net speculative positioning for key futures contracts,
    with extreme readings flagged.
    """
    cached = get_cached("cot_positioning", ttl_seconds=86400)  # 24h — weekly data
    if cached:
        return cached

    result = {"positions": {}, "timestamp": datetime.now().isoformat()}

    try:
        url = "https://www.cftc.gov/dea/newcot/deafut.txt"
        headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"}
        resp = requests.get(url, headers=headers, timeout=30)

        if resp.status_code != 200:
            result["error"] = f"CFTC data unavailable (HTTP {resp.status_code})"
            return result

        reader = csv.reader(io.StringIO(resp.text))
        latest_by_contract = {}

        for row in reader:
            if len(row) < 10:
                continue

            name = row[COL_NAME].strip().upper()
            matched_key = None
            for contract_name in CONTRACTS:
                if contract_name in name:
                    matched_key = contract_name
                    break

            if matched_key is None:
                continue

            try:
                long_pos = int(row[COL_NC_LONG].strip().replace(",", ""))
                short_pos = int(row[COL_NC_SHORT].strip().replace(",", ""))
                oi = int(row[COL_OI].strip().replace(",", ""))
                report_date = row[COL_DATE].strip()
            except (ValueError, IndexError):
                continue

            net = long_pos - short_pos
            entry = {
                "contract": matched_key,
                "asset_class": CONTRACTS[matched_key],
                "net_speculative": net,
                "long": long_pos,
                "short": short_pos,
                "open_interest": oi,
                "report_date": report_date,
            }

            # Net as % of OI for comparability
            if oi > 0:
                entry["net_pct_oi"] = round(net / oi * 100, 1)
                ratio = net / oi
                if ratio > 0.3:
                    entry["signal"] = "extreme_long"
                elif ratio > 0.15:
                    entry["signal"] = "net_long"
                elif ratio > -0.15:
                    entry["signal"] = "neutral"
                elif ratio > -0.3:
                    entry["signal"] = "net_short"
                else:
                    entry["signal"] = "extreme_short"

            # Keep most recent per contract
            existing = latest_by_contract.get(matched_key)
            if existing is None or report_date > existing.get("report_date", ""):
                latest_by_contract[matched_key] = entry

        result["positions"] = latest_by_contract

        # Summary
        extreme_longs = [k for k, v in latest_by_contract.items() if v.get("signal") == "extreme_long"]
        extreme_shorts = [k for k, v in latest_by_contract.items() if v.get("signal") == "extreme_short"]
        if extreme_longs:
            result["crowded_longs"] = extreme_longs
        if extreme_shorts:
            result["crowded_shorts"] = extreme_shorts
        result["contracts_tracked"] = len(latest_by_contract)

    except Exception as e:
        result["error"] = str(e)

    set_cached("cot_positioning", result)
    return result
