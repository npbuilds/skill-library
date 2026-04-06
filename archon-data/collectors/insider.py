"""OpenInsider scraper for insider buying signals."""

import re
from datetime import datetime

import requests

from .cache import get_cached, set_cached


def _clean_html(s: str) -> str:
    """Remove HTML tags from a string."""
    return re.sub(r"<[^>]+>", "", s).strip()


def get_insider_buys() -> dict:
    """Get recent notable insider purchases from OpenInsider."""
    cached = get_cached("insider_buys", ttl_seconds=21600)  # 6 hours
    if cached:
        return cached

    result = {"transactions": [], "timestamp": datetime.now().isoformat()}

    try:
        url = "https://openinsider.com/screener?s=&o=&pl=100&ph=&ll=&lh=&fd=30&fdr=&td=0&tdr=&feession=&cession=&sidTabbedPanels1=tab-insider-buy-702&cnt=25&page=1"
        headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"}
        resp = requests.get(url, headers=headers, timeout=15)

        if resp.status_code == 200:
            html = resp.text
            rows = re.findall(r"<tr[^>]*>(.*?)</tr>", html, re.DOTALL)

            for row in rows[:25]:
                cells = re.findall(r"<td[^>]*>(.*?)</td>", row, re.DOTALL)
                if len(cells) >= 12:

                    filing_date = _clean_html(cells[1])
                    ticker = _clean_html(cells[3])
                    insider_name = _clean_html(cells[4])
                    title = _clean_html(cells[5])
                    trade_type = _clean_html(cells[6])
                    price = _clean_html(cells[7])
                    qty = _clean_html(cells[8])
                    owned = _clean_html(cells[9])
                    delta_own = _clean_html(cells[10])
                    value = _clean_html(cells[11])

                    if ticker and "Purchase" in trade_type:
                        result["transactions"].append(
                            {
                                "filing_date": filing_date,
                                "ticker": ticker,
                                "insider": insider_name,
                                "title": title,
                                "price": price,
                                "value": value,
                                "delta_ownership": delta_own,
                            }
                        )
        else:
            result["error"] = f"OpenInsider returned {resp.status_code}"

    except Exception as e:
        result["error"] = str(e)

    # Identify cluster buys (multiple insiders buying same ticker)
    ticker_counts: dict[str, int] = {}
    for txn in result["transactions"]:
        t = txn["ticker"]
        ticker_counts[t] = ticker_counts.get(t, 0) + 1

    result["cluster_buys"] = [
        {"ticker": t, "insider_count": c} for t, c in ticker_counts.items() if c >= 2
    ]

    result["total_transactions"] = len(result["transactions"])

    set_cached("insider_buys", result)
    return result
