"""Data pipeline health tracker — monitors source freshness and availability.

Every data collection call wraps its result with _meta containing source,
timestamp, cache age, and status. This module aggregates those signals into
a composite confidence score and a compact status row for the briefing header.
"""

from __future__ import annotations

import time
from datetime import datetime


def wrap_with_meta(
    data: dict | list,
    source: str,
    status: str = "ok",
    degraded_reason: str = "",
    cache_age_seconds: int = 0,
) -> dict:
    """Wrap a data result with _meta health information.

    Args:
        data: The actual data payload
        source: Data source name (e.g., "yfinance", "FRED", "CoinGecko")
        status: "ok", "degraded", or "failed"
        degraded_reason: Explanation if degraded
        cache_age_seconds: How old the cached data is

    Returns:
        Dict with "data" and "_meta" keys.
    """
    meta = {
        "source": source,
        "fetched_at": datetime.now().isoformat(timespec="seconds"),
        "cache_age_seconds": cache_age_seconds,
        "status": status,
    }
    if degraded_reason:
        meta["degraded_reason"] = degraded_reason

    if isinstance(data, dict):
        return {**data, "_meta": meta}
    return {"data": data, "_meta": meta}


def collect_health(tool_results: dict[str, dict]) -> dict:
    """Aggregate health from multiple tool results into a summary.

    Args:
        tool_results: Dict of tool_name → result dict (each should have _meta)

    Returns:
        Health summary with composite score and per-source status.
    """
    sources = {}
    total_score = 0
    source_count = 0

    for tool_name, result in tool_results.items():
        meta = result.get("_meta") if isinstance(result, dict) else None
        if meta is None:
            # No health info — mark as unknown
            sources[tool_name] = {"status": "unknown", "age": "?"}
            continue

        status = meta.get("status", "unknown")
        cache_age = meta.get("cache_age_seconds", 0)
        source_name = meta.get("source", tool_name)

        # Score: ok=100, degraded=50, failed=0
        if status == "ok":
            score = 100
        elif status == "degraded":
            score = 50
        else:
            score = 0

        # Penalize stale data (>24h = -20, >48h = -40)
        if cache_age > 172800:  # 48h
            score = max(0, score - 40)
        elif cache_age > 86400:  # 24h
            score = max(0, score - 20)

        total_score += score
        source_count += 1

        # Compact age string
        age_str = _format_age(cache_age)

        sources[tool_name] = {
            "status": status,
            "source": source_name,
            "age": age_str,
            "score": score,
        }
        if meta.get("degraded_reason"):
            sources[tool_name]["reason"] = meta["degraded_reason"]

    composite = round(total_score / source_count) if source_count > 0 else 0

    return {
        "composite_score": composite,
        "source_count": source_count,
        "sources": sources,
        "status_line": _format_status_line(sources, composite),
    }


def _format_age(seconds: int) -> str:
    """Format cache age as human-readable string."""
    if seconds < 60:
        return "live"
    if seconds < 3600:
        return f"{seconds // 60}m"
    if seconds < 86400:
        return f"{seconds // 3600}h"
    return f"{seconds // 86400}d"


def _format_status_line(sources: dict, composite: int) -> str:
    """Format the compact status line for the briefing header."""
    parts = [f"DATA HEALTH [{composite}/100]"]
    for name, info in sources.items():
        status = info["status"].upper()
        age = info["age"]
        if status == "OK":
            parts.append(f"{name}: OK ({age})")
        elif status == "DEGRADED":
            reason = info.get("reason", "")
            parts.append(f"{name}: DEGRADED ({reason[:30]})" if reason else f"{name}: DEGRADED")
        elif status == "FAILED":
            parts.append(f"{name}: FAILED")
        else:
            parts.append(f"{name}: ? ({age})")

    return " | ".join(parts)
