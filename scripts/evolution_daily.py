#!/usr/bin/env python3
"""Pure helpers for the aggregate-only evolution history.

Firestore stores one ``evolution_daily/{YYYY-MM-DD}`` document per scheduled
run. The document is derived directly from the current registry; no per-skill
history is written or required.
"""

from __future__ import annotations

import json
from datetime import date, datetime, timezone


def _skill_domain_map(registry: dict) -> dict[str, str]:
    network = registry.get("network", {})
    network_domains = network.get("domains", {}) if isinstance(network, dict) else {}
    if not isinstance(network_domains, dict):
        raise ValueError("registry.network.domains must be an object")

    skill_domain: dict[str, str] = {}
    for domain, names in network_domains.items():
        if not isinstance(domain, str) or not domain:
            raise ValueError("registry domain names must be non-empty strings")
        if not isinstance(names, list):
            raise ValueError(f"registry.network.domains.{domain} must be a list")
        for name in names:
            if not isinstance(name, str) or not name:
                raise ValueError(f"registry.network.domains.{domain} contains an invalid skill name")
            if name in skill_domain:
                raise ValueError(
                    f"skill {name!r} is assigned to both {skill_domain[name]!r} and {domain!r}"
                )
            skill_domain[name] = domain
    return skill_domain


def _numeric_score(value, context: str) -> float:
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise ValueError(f"{context}: composite_score must be numeric")
    score = float(value)
    if not 0 <= score <= 100:
        raise ValueError(f"{context}: composite_score must be between 0 and 100")
    return score


def _domain_averages(rows: list[tuple[str, float]], skill_domain: dict[str, str]) -> dict:
    scores: dict[str, list[float]] = {}
    for skill, score in rows:
        scores.setdefault(skill_domain.get(skill, "unknown"), []).append(score)
    return {
        domain: round(sum(values) / len(values), 2)
        for domain, values in sorted(scores.items())
        if values
    }


def build_daily_aggregate(registry: dict, day: str) -> dict:
    """Return ``{date, count, domains}`` for the registry's current scores.

    ``count`` is the number of skills included. ``domains`` holds the mean
    composite score for each domain. Invalid entries or scores fail the build
    so a scheduled run cannot silently overwrite a valid aggregate with zeros.
    """
    date.fromisoformat(day)  # Fail early if a caller supplies a malformed ID.

    skills = registry.get("skills", {})
    if not isinstance(skills, dict):
        raise ValueError("registry.skills must be an object")

    skill_domain = _skill_domain_map(registry)
    rows: list[tuple[str, float]] = []
    for name, entry in skills.items():
        if not isinstance(name, str) or not name:
            raise ValueError("registry skill names must be non-empty strings")
        if not isinstance(entry, dict):
            raise ValueError(f"skill {name!r}: registry entry must be an object")
        if "composite_score" not in entry:
            raise ValueError(f"skill {name!r}: composite_score is required")
        rows.append((name, _numeric_score(entry["composite_score"], f"skill {name!r}")))

    return {
        "date": day,
        "count": len(rows),
        "domains": _domain_averages(rows, skill_domain),
    }


def build_historical_aggregates(raw_rows: list[dict], registry: dict) -> list[dict]:
    """Rebuild raw-backed dates with exactly one sample per skill and date.

    Legacy raw history can contain several event types for the same skill/day.
    The newest timestamp wins, preventing those events from weighting a skill
    multiple times in a domain average. This helper is migration-only; future
    dates are written directly by :func:`build_daily_aggregate`.
    """
    skill_domain = _skill_domain_map(registry)
    latest: dict[tuple[str, str], tuple[datetime, str, float]] = {}

    for index, row in enumerate(raw_rows, start=1):
        if not isinstance(row, dict):
            raise ValueError(f"raw row {index}: expected an object")
        skill = row.get("skill")
        if not isinstance(skill, str) or not skill:
            raise ValueError(f"raw row {index}: skill must be a non-empty string")
        raw_timestamp = row.get("date")
        if not isinstance(raw_timestamp, str):
            raise ValueError(f"raw row {index}: date must be an ISO timestamp")
        try:
            timestamp = datetime.fromisoformat(raw_timestamp.replace("Z", "+00:00"))
        except ValueError as exc:
            raise ValueError(f"raw row {index}: invalid date {raw_timestamp!r}") from exc
        if timestamp.tzinfo is None:
            timestamp = timestamp.replace(tzinfo=timezone.utc)
        timestamp = timestamp.astimezone(timezone.utc)
        day = timestamp.date().isoformat()
        if "composite_score" not in row:
            raise ValueError(f"raw row {index}: composite_score is required")
        score = _numeric_score(row["composite_score"], f"raw row {index}")
        tie_breaker = json.dumps(row, sort_keys=True, separators=(",", ":"), default=str)

        key = (skill, day)
        previous = latest.get(key)
        if previous is None or (timestamp, tie_breaker) > previous[:2]:
            latest[key] = (timestamp, tie_breaker, score)

    by_date: dict[str, list[tuple[str, float]]] = {}
    for (skill, day), (_timestamp, _tie_breaker, score) in latest.items():
        by_date.setdefault(day, []).append((skill, score))

    return [
        {
            "date": day,
            "count": len(rows),
            "domains": _domain_averages(rows, skill_domain),
        }
        for day, rows in sorted(by_date.items())
    ]


def validate_daily_document(doc_id: str, document: dict) -> list[str]:
    """Return schema/semantic errors for one stored daily aggregate."""
    errors: list[str] = []
    try:
        date.fromisoformat(doc_id)
    except (TypeError, ValueError):
        errors.append(f"{doc_id!r}: document ID is not YYYY-MM-DD")

    if not isinstance(document, dict):
        return errors + [f"{doc_id}: document is not an object"]
    if document.get("date") != doc_id:
        errors.append(f"{doc_id}: date field does not match document ID")

    count = document.get("count")
    if not isinstance(count, int) or isinstance(count, bool) or count < 0:
        errors.append(f"{doc_id}: count must be a non-negative integer")

    domains = document.get("domains")
    if not isinstance(domains, dict):
        errors.append(f"{doc_id}: domains must be an object")
        return errors
    for domain, score in domains.items():
        if not isinstance(domain, str) or not domain:
            errors.append(f"{doc_id}: domain names must be non-empty strings")
        if (
            not isinstance(score, (int, float))
            or isinstance(score, bool)
            or not 0 <= score <= 100
        ):
            errors.append(f"{doc_id}: domain {domain!r} score must be between 0 and 100")
    return errors
