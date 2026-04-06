"""CoinGecko collector — crypto market data, sentiment, and trending."""

from datetime import datetime

import requests

from .cache import get_cached, set_cached

BASE_URL = "https://api.coingecko.com/api/v3"
HEADERS = {"User-Agent": "ArchonInvestmentResearch/1.0", "Accept": "application/json"}

# Key crypto assets to track
TRACKED_COINS = ["bitcoin", "ethereum", "solana", "cardano", "avalanche-2"]


def get_crypto_dashboard() -> dict:
    """Get comprehensive crypto market data from CoinGecko.

    Returns market overview (total cap, BTC dominance, fear/greed),
    top coin prices/changes, trending coins, and DeFi stats.
    Free API — 30 calls/min rate limit.
    """
    cached = get_cached("crypto_dashboard", ttl_seconds=1800)  # 30 min
    if cached:
        return cached

    result = {"timestamp": datetime.now().isoformat()}

    # 1. Global market data
    try:
        resp = requests.get(f"{BASE_URL}/global", headers=HEADERS, timeout=10)
        if resp.status_code == 200:
            data = resp.json().get("data", {})
            result["global"] = {
                "total_market_cap_usd": _trillions(data.get("total_market_cap", {}).get("usd")),
                "total_volume_24h_usd": _billions(data.get("total_volume", {}).get("usd")),
                "btc_dominance": _round_safe(data.get("market_cap_percentage", {}).get("btc")),
                "eth_dominance": _round_safe(data.get("market_cap_percentage", {}).get("eth")),
                "active_cryptocurrencies": data.get("active_cryptocurrencies"),
                "market_cap_change_24h_pct": _round_safe(data.get("market_cap_change_percentage_24h_usd")),
            }
    except Exception as e:
        result["global_error"] = str(e)

    # 2. Top coins with detailed data
    try:
        params = {
            "vs_currency": "usd",
            "ids": ",".join(TRACKED_COINS),
            "order": "market_cap_desc",
            "sparkline": "false",
            "price_change_percentage": "1h,24h,7d,30d",
        }
        resp = requests.get(f"{BASE_URL}/coins/markets", params=params, headers=HEADERS, timeout=10)
        if resp.status_code == 200:
            coins = resp.json()
            result["coins"] = {}
            for coin in coins:
                result["coins"][coin["symbol"].upper()] = {
                    "name": coin.get("name"),
                    "price": coin.get("current_price"),
                    "market_cap": _billions(coin.get("market_cap")),
                    "volume_24h": _billions(coin.get("total_volume")),
                    "change_24h_pct": _round_safe(coin.get("price_change_percentage_24h")),
                    "change_7d_pct": _round_safe(coin.get("price_change_percentage_7d_in_currency")),
                    "change_30d_pct": _round_safe(coin.get("price_change_percentage_30d_in_currency")),
                    "ath": coin.get("ath"),
                    "ath_change_pct": _round_safe(coin.get("ath_change_percentage")),
                    "rank": coin.get("market_cap_rank"),
                }
    except Exception as e:
        result["coins_error"] = str(e)

    # 3. Trending coins (what retail is searching for)
    try:
        resp = requests.get(f"{BASE_URL}/search/trending", headers=HEADERS, timeout=10)
        if resp.status_code == 200:
            trending = resp.json().get("coins", [])
            result["trending"] = [
                {
                    "name": t["item"]["name"],
                    "symbol": t["item"]["symbol"],
                    "rank": t["item"].get("market_cap_rank"),
                    "score": t["item"].get("score"),
                }
                for t in trending[:7]
            ]
    except Exception as e:
        result["trending_error"] = str(e)

    # 4. Fear & Greed Index (alternative.me — crypto-specific)
    try:
        resp = requests.get(
            "https://api.alternative.me/fng/?limit=7",
            headers=HEADERS, timeout=10,
        )
        if resp.status_code == 200:
            fng_data = resp.json().get("data", [])
            if fng_data:
                latest = fng_data[0]
                result["fear_greed"] = {
                    "value": int(latest.get("value", 0)),
                    "label": latest.get("value_classification", ""),
                    "timestamp": latest.get("timestamp"),
                }
                # 7-day trend
                if len(fng_data) >= 7:
                    values = [int(d.get("value", 50)) for d in fng_data]
                    result["fear_greed"]["avg_7d"] = round(sum(values) / len(values))
                    result["fear_greed"]["trend"] = (
                        "improving" if values[0] > values[-1]
                        else "deteriorating" if values[0] < values[-1]
                        else "stable"
                    )
    except Exception as e:
        result["fng_error"] = str(e)

    # 5. DeFi data
    try:
        resp = requests.get(f"{BASE_URL}/global/decentralized_finance_defi", headers=HEADERS, timeout=10)
        if resp.status_code == 200:
            defi = resp.json().get("data", {})
            result["defi"] = {
                "defi_market_cap": defi.get("defi_market_cap"),
                "defi_dominance": _round_safe(float(defi.get("defi_dominance", 0))),
                "defi_volume_24h": defi.get("trading_volume_24h"),
                "top_defi_coin": defi.get("top_coin_name"),
            }
    except Exception as e:
        result["defi_error"] = str(e)

    # Composite crypto regime
    btc = result.get("coins", {}).get("BTC", {})
    fng = result.get("fear_greed", {})
    global_data = result.get("global", {})

    btc_30d = btc.get("change_30d_pct")
    fng_val = fng.get("value")
    cap_change = global_data.get("market_cap_change_24h_pct")

    if btc_30d is not None and fng_val is not None:
        if fng_val <= 25 and btc_30d < -10:
            result["crypto_regime"] = "capitulation"
            result["crypto_note"] = "Extreme fear + falling prices — historically contrarian bullish for BTC"
        elif fng_val <= 25:
            result["crypto_regime"] = "fear"
            result["crypto_note"] = "Fear elevated but prices holding — watch for washout or recovery"
        elif fng_val >= 75 and btc_30d > 20:
            result["crypto_regime"] = "euphoria"
            result["crypto_note"] = "Extreme greed + parabolic prices — late-stage momentum, increased risk"
        elif fng_val >= 75:
            result["crypto_regime"] = "greed"
            result["crypto_note"] = "Greed elevated — risk of pullback increasing"
        else:
            result["crypto_regime"] = "neutral"
            result["crypto_note"] = "No extreme readings — range-bound sentiment"

    result["source"] = "CoinGecko + Alternative.me"
    set_cached("crypto_dashboard", result)
    return result


def _round_safe(val, digits=2):
    """Round a value, returning None for None."""
    if val is None:
        return None
    try:
        return round(float(val), digits)
    except (ValueError, TypeError):
        return None


def _billions(val):
    """Convert to billions with label."""
    if val is None:
        return None
    try:
        return f"${val / 1e9:.1f}B"
    except (ValueError, TypeError):
        return None


def _trillions(val):
    """Convert to trillions with label."""
    if val is None:
        return None
    try:
        return f"${val / 1e12:.2f}T"
    except (ValueError, TypeError):
        return None
