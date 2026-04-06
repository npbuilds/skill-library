"""Market data collector using yfinance. No API key required."""

import math
from datetime import datetime, timedelta

import yfinance as yf

from .cache import get_cached, set_cached

# Core indices and assets
INDICES = {
    "^GSPC": "S&P 500",
    "^IXIC": "Nasdaq",
    "^RUT": "Russell 2000",
}

CROSS_ASSETS = {
    "^VIX": "VIX",
    "GLD": "Gold (GLD)",
    "USO": "Oil (USO)",
    "BTC-USD": "Bitcoin",
    "DX-Y.NYB": "Dollar (DXY)",
    "TLT": "20Y Treasury (TLT)",
    "HYG": "High Yield (HYG)",
}

BREADTH = {
    "SPY": "S&P 500 (Cap-Weight)",
    "RSP": "S&P 500 (Equal-Weight)",
}

SECTORS = {
    "XLE": "Energy",
    "XLF": "Financials",
    "XLK": "Technology",
    "XLV": "Healthcare",
    "XLI": "Industrials",
    "XLP": "Consumer Staples",
    "XLU": "Utilities",
    "XLY": "Consumer Discretionary",
    "XLB": "Materials",
    "XLRE": "Real Estate",
    "XLC": "Communications",
}

# Private market proxy ETFs and stocks
REIT_ETFS = {
    "VNQ": "Vanguard Real Estate ETF",
    "IYR": "iShares US Real Estate",
    # XLRE omitted — already tracked in SECTORS
    # Data center REITs covered by EQIX in REIT_SUBSECTORS
}

REIT_SUBSECTORS = {
    "PLD": "Prologis (Industrial)",
    "AMT": "American Tower (Cell Towers)",
    "EQIX": "Equinix (Data Centers)",
    "O": "Realty Income (Retail/Net Lease)",
    "SPG": "Simon Property (Malls)",
    "AVB": "AvalonBay (Apartments)",
    "VTR": "Ventas (Healthcare RE)",
    "BXP": "BXP Inc (Office)",
}

BDC_AND_CREDIT = {
    "BIZD": "BDC Index ETF",
    "ARCC": "Ares Capital (BDC)",
    "OBDC": "Blue Owl Capital (BDC)",
    "BXSL": "Blackstone Secured Lending",
}

PE_GP_STOCKS = {
    "BX": "Blackstone",
    "KKR": "KKR & Co",
    "APO": "Apollo Global",
    "ARES": "Ares Management",
    "CG": "Carlyle Group",
    "OWL": "Blue Owl Capital",
}

VC_PROXIES = {
    "ARKK": "ARK Innovation (VC proxy)",
    "IGV": "iShares Software (SaaS proxy)",
    "IPO": "Renaissance IPO ETF",
    "XBI": "Biotech (VC exit proxy)",
}


def _ytd_return(ticker_obj: yf.Ticker) -> float | None:
    """Calculate YTD return for a ticker using prior-year close as baseline.

    Fetches an extra week before Jan 1 to find the last trading day of the
    prior year. This avoids the Jan 1-2 overnight gap that would make YTD
    returns inconsistent with published figures.
    """
    try:
        current_year = datetime.now().year
        # Start a week before Jan 1 to capture the prior year's last close
        fetch_start = datetime(current_year, 1, 1) - timedelta(days=7)
        hist = ticker_obj.history(start=fetch_start, end=datetime.now())
        if len(hist) < 2:
            return None
        # Find the last close before the current year
        prior_year = hist[hist.index < f"{current_year}-01-01"]
        if prior_year.empty:
            # Fallback: use first available close
            return ((hist["Close"].iloc[-1] / hist["Close"].iloc[0]) - 1) * 100
        baseline = prior_year["Close"].iloc[-1]
        return ((hist["Close"].iloc[-1] / baseline) - 1) * 100
    except Exception:
        return None


def _safe_info(ticker_obj: yf.Ticker, field: str, default=None):
    """Safely get a field from ticker info."""
    try:
        return ticker_obj.info.get(field, default)
    except Exception:
        return default


def _safe_round(val, digits=2):
    """Round a value, returning None for NaN/None."""
    if val is None or (isinstance(val, float) and (math.isnan(val) or math.isinf(val))):
        return None
    return round(val, digits)


def get_market_snapshot() -> dict:
    """Get current market levels, YTD performance, and breadth."""
    cached = get_cached("market_snapshot", ttl_seconds=900)
    if cached:
        return cached

    result = {"indices": {}, "breadth": {}, "timestamp": datetime.now().isoformat()}

    # Indices
    for symbol, name in INDICES.items():
        try:
            t = yf.Ticker(symbol)
            hist = t.history(period="5d")
            if hist.empty:
                continue
            price = hist["Close"].iloc[-1]
            ytd = _ytd_return(t)
            result["indices"][name] = {
                "symbol": symbol,
                "price": _safe_round(price),
                "ytd_pct": _safe_round(ytd),
            }
        except Exception:
            continue

    # Breadth (SPY vs RSP)
    for symbol, name in BREADTH.items():
        try:
            t = yf.Ticker(symbol)
            ytd = _ytd_return(t)
            hist = t.history(period="5d")
            price = hist["Close"].iloc[-1] if not hist.empty else None
            result["breadth"][name] = {
                "symbol": symbol,
                "price": _safe_round(price) if price else None,
                "ytd_pct": _safe_round(ytd),
            }
        except Exception:
            continue

    # Breadth divergence
    spy_ytd = result["breadth"].get("S&P 500 (Cap-Weight)", {}).get("ytd_pct")
    rsp_ytd = result["breadth"].get("S&P 500 (Equal-Weight)", {}).get("ytd_pct")
    if spy_ytd is not None and rsp_ytd is not None:
        result["breadth_divergence"] = round(rsp_ytd - spy_ytd, 2)
        result["breadth_signal"] = (
            "equal_weight_leading" if rsp_ytd > spy_ytd else "cap_weight_leading"
        )

    set_cached("market_snapshot", result)
    return result


def get_sector_performance() -> dict:
    """Get sector ETF performance for rotation analysis."""
    cached = get_cached("sector_performance", ttl_seconds=900)
    if cached:
        return cached

    result = {"sectors": {}, "timestamp": datetime.now().isoformat()}

    for symbol, name in SECTORS.items():
        try:
            t = yf.Ticker(symbol)
            hist_1m = t.history(period="1mo")
            ytd = _ytd_return(t)
            month_ret = None
            if len(hist_1m) >= 2:
                month_ret = (
                    (hist_1m["Close"].iloc[-1] / hist_1m["Close"].iloc[0]) - 1
                ) * 100

            result["sectors"][name] = {
                "symbol": symbol,
                "ytd_pct": _safe_round(ytd),
                "month_pct": _safe_round(month_ret),
            }
        except Exception:
            continue

    # Sort by YTD performance
    result["leaders"] = sorted(
        result["sectors"].keys(),
        key=lambda s: result["sectors"][s].get("ytd_pct") or -999,
        reverse=True,
    )[:3]
    result["laggards"] = sorted(
        result["sectors"].keys(),
        key=lambda s: result["sectors"][s].get("ytd_pct") or 999,
    )[:3]

    set_cached("sector_performance", result)
    return result


def get_asset_performance() -> dict:
    """Get cross-asset performance table."""
    cached = get_cached("asset_performance", ttl_seconds=900)
    if cached:
        return cached

    result = {"assets": {}, "timestamp": datetime.now().isoformat()}

    for symbol, name in {**CROSS_ASSETS, **INDICES}.items():
        try:
            t = yf.Ticker(symbol)
            hist = t.history(period="5d")
            if hist.empty:
                continue
            price = hist["Close"].iloc[-1]
            ytd = _ytd_return(t)

            # 1-month return
            hist_1m = t.history(period="1mo")
            month_ret = None
            if len(hist_1m) >= 2:
                month_ret = (
                    (hist_1m["Close"].iloc[-1] / hist_1m["Close"].iloc[0]) - 1
                ) * 100

            result["assets"][name] = {
                "symbol": symbol,
                "price": _safe_round(price),
                "ytd_pct": _safe_round(ytd),
                "month_pct": _safe_round(month_ret),
            }
        except Exception:
            continue

    set_cached("asset_performance", result)
    return result


def get_private_market_proxies() -> dict:
    """Get private market proxy data — REITs, BDCs, PE GPs, VC proxies."""
    cached = get_cached("private_market_proxies", ttl_seconds=900)
    if cached:
        return cached

    result = {
        "reits": {},
        "reit_subsectors": {},
        "bdcs": {},
        "pe_gps": {},
        "vc_proxies": {},
        "timestamp": datetime.now().isoformat(),
    }

    def _fetch_group(tickers: dict, target: dict):
        for symbol, name in tickers.items():
            try:
                t = yf.Ticker(symbol)
                hist = t.history(period="5d")
                if hist.empty:
                    continue
                price = hist["Close"].iloc[-1]
                ytd = _ytd_return(t)

                hist_1m = t.history(period="1mo")
                month_ret = None
                if len(hist_1m) >= 2:
                    month_ret = (
                        (hist_1m["Close"].iloc[-1] / hist_1m["Close"].iloc[0]) - 1
                    ) * 100

                entry = {
                    "symbol": symbol,
                    "price": _safe_round(price),
                    "ytd_pct": _safe_round(ytd),
                    "month_pct": _safe_round(month_ret),
                }

                # Try to get dividend yield for REITs and BDCs
                div_yield = _safe_info(t, "dividendYield")
                if div_yield is not None:
                    entry["dividend_yield"] = _safe_round(div_yield * 100)

                # NAV for BDCs and REITs (book value per share as proxy)
                bvps = _safe_info(t, "bookValue")
                if bvps is not None and price is not None and bvps > 0:
                    entry["nav_proxy"] = _safe_round(bvps)
                    entry["nav_discount_pct"] = _safe_round(
                        ((price / bvps) - 1) * 100
                    )

                target[name] = entry
            except Exception:
                continue

    _fetch_group(REIT_ETFS, result["reits"])
    _fetch_group(REIT_SUBSECTORS, result["reit_subsectors"])
    _fetch_group(BDC_AND_CREDIT, result["bdcs"])
    _fetch_group(PE_GP_STOCKS, result["pe_gps"])
    _fetch_group(VC_PROXIES, result["vc_proxies"])

    # Compute aggregate signals

    # REIT sector performance spread (industrial/data center vs office)
    industrial = result["reit_subsectors"].get("Prologis (Industrial)", {})
    datacenter = result["reit_subsectors"].get("Equinix (Data Centers)", {})
    office = result["reit_subsectors"].get("BXP Inc (Office)", {})
    if industrial.get("ytd_pct") is not None and office.get("ytd_pct") is not None:
        result["re_structural_spread"] = _safe_round(
            industrial["ytd_pct"] - office["ytd_pct"]
        )
        result["re_structural_signal"] = (
            "new_economy_leading"
            if result["re_structural_spread"] > 5
            else "converging"
            if abs(result["re_structural_spread"]) < 5
            else "office_recovery"
        )

    # BDC aggregate NAV discount
    bdc_discounts = [
        v.get("nav_discount_pct")
        for v in result["bdcs"].values()
        if v.get("nav_discount_pct") is not None
    ]
    if bdc_discounts:
        avg_discount = sum(bdc_discounts) / len(bdc_discounts)
        result["bdc_avg_nav_discount"] = _safe_round(avg_discount)
        if avg_discount < -10:
            result["bdc_signal"] = "credit_stress"
        elif avg_discount < -3:
            result["bdc_signal"] = "cautious"
        elif avg_discount < 5:
            result["bdc_signal"] = "neutral"
        else:
            result["bdc_signal"] = "premium_confidence"

    # PE GP aggregate YTD
    gp_ytds = [
        v.get("ytd_pct")
        for v in result["pe_gps"].values()
        if v.get("ytd_pct") is not None
    ]
    if gp_ytds:
        result["pe_gp_avg_ytd"] = _safe_round(sum(gp_ytds) / len(gp_ytds))

    # VC proxy composite
    vc_ytds = [
        v.get("ytd_pct")
        for v in result["vc_proxies"].values()
        if v.get("ytd_pct") is not None
    ]
    if vc_ytds:
        result["vc_proxy_avg_ytd"] = _safe_round(sum(vc_ytds) / len(vc_ytds))

    set_cached("private_market_proxies", result)
    return result
