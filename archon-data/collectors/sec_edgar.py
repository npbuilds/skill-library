"""SEC EDGAR collector — 13F institutional filings and special situations."""

from datetime import datetime, timedelta

import requests

from .cache import get_cached, set_cached

EDGAR_BASE = "https://efts.sec.gov/LATEST"
EDGAR_SUBMISSIONS = "https://data.sec.gov/submissions"

# SEC requires a User-Agent with contact info
HEADERS = {
    "User-Agent": "ArchonInvestmentResearch/1.0 (archon@example.com)",
    "Accept": "application/json",
}


def get_recent_13f_filings(limit: int = 20) -> dict:
    """Get recent 13F-HR filings (institutional holdings disclosures).

    Returns the most recent 13F filings from the SEC EDGAR full-text
    search API, identifying which institutions filed and when.
    """
    cached = get_cached("recent_13f", ttl_seconds=21600)  # 6 hours
    if cached:
        return cached

    result = {"filings": [], "timestamp": datetime.now().isoformat()}

    try:
        params = {
            "q": "\"13F-HR\"",
            "dateRange": "custom",
            "startdt": (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d"),
            "enddt": datetime.now().strftime("%Y-%m-%d"),
            "from": "0",
            "size": str(limit),
        }
        resp = requests.get(
            f"{EDGAR_BASE}/search-index", params=params,
            headers=HEADERS, timeout=15
        )

        if resp.status_code == 200:
            data = resp.json()
            hits = data.get("hits", {}).get("hits", [])
            for hit in hits[:limit]:
                source = hit.get("_source", {})
                result["filings"].append({
                    "filer": source.get("display_names", ["Unknown"])[0] if source.get("display_names") else source.get("entity_name", "Unknown"),
                    "filing_date": source.get("file_date"),
                    "form_type": source.get("form_type", "13F-HR"),
                    "accession": source.get("file_num"),
                })
        else:
            result["error"] = f"EDGAR API returned {resp.status_code}"

    except Exception as e:
        result["error"] = str(e)

    result["count"] = len(result["filings"])
    set_cached("recent_13f", result)
    return result


def get_special_situation_filings(limit: int = 15) -> dict:
    """Get recent special situation filings: spinoffs, activism, and M&A.

    Searches EDGAR for SC 13D (activist stakes >5%), S-1 (IPOs/spinoffs),
    and DEFA14A (proxy/M&A related) filings.
    """
    cached = get_cached("special_situations", ttl_seconds=21600)  # 6 hours
    if cached:
        return cached

    result = {
        "activist_stakes": [],
        "spinoffs_ipos": [],
        "proxy_ma": [],
        "timestamp": datetime.now().isoformat(),
    }

    filing_types = {
        "SC 13D": "activist_stakes",
        "S-1": "spinoffs_ipos",
        "DEFA14A": "proxy_ma",
    }

    for form_type, category in filing_types.items():
        try:
            params = {
                "q": f"\"{form_type}\"",
                "dateRange": "custom",
                "startdt": (datetime.now() - timedelta(days=14)).strftime("%Y-%m-%d"),
                "enddt": datetime.now().strftime("%Y-%m-%d"),
                "from": "0",
                "size": str(limit),
            }
            resp = requests.get(
                f"{EDGAR_BASE}/search-index", params=params,
                headers=HEADERS, timeout=15,
            )

            if resp.status_code == 200:
                data = resp.json()
                hits = data.get("hits", {}).get("hits", [])
                for hit in hits:
                    source = hit.get("_source", {})
                    entity = source.get("display_names", ["Unknown"])[0] if source.get("display_names") else source.get("entity_name", "Unknown")
                    result[category].append({
                        "entity": entity,
                        "filing_date": source.get("file_date"),
                        "form_type": form_type,
                        "description": _form_description(form_type),
                    })
        except Exception:
            continue

    # Summary
    result["total_filings"] = (
        len(result["activist_stakes"])
        + len(result["spinoffs_ipos"])
        + len(result["proxy_ma"])
    )

    if result["activist_stakes"]:
        result["alert"] = f"{len(result['activist_stakes'])} new activist stake(s) filed in last 14 days"

    set_cached("special_situations", result)
    return result


def _form_description(form_type: str) -> str:
    """Return a human-readable description of a filing type."""
    descriptions = {
        "SC 13D": "Activist/beneficial ownership >5% — investor taking an active role",
        "S-1": "Registration statement — IPO or spinoff offering",
        "DEFA14A": "Proxy solicitation — often M&A or shareholder vote related",
    }
    return descriptions.get(form_type, form_type)
