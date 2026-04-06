"""Forecast calibration tracker — measures the Archon's predictive accuracy.

Logs predictions with probabilities and resolution dates, then scores them
against actual outcomes using Brier scores and calibration curves. Over time,
this reveals which investor frameworks have genuine predictive power in which
regimes and which are noise.

Key concepts:
- Brier score: mean squared error of probability forecasts (0 = perfect, 1 = worst)
- Calibration: when you say 70%, does it happen ~70% of the time?
- Resolution: a prediction is "resolved" when the outcome is known
- Sharpness: how far from 50% your predictions are (sharper = more useful if calibrated)

Predictions are stored in a single JSON file (predictions.json) in the
snapshots directory, with each prediction having a unique ID, creation date,
resolution date (when known), and outcome.
"""

from __future__ import annotations

import json
import uuid
from datetime import date
from pathlib import Path

PREDICTIONS_FILE = Path(__file__).parent.parent / "snapshots" / "predictions.json"


# ── Prediction Management ────────────────────────────────────


def log_prediction(
    claim: str,
    probability: float,
    framework: str,
    category: str,
    resolve_by: str,
    regime_context: str | None = None,
    evidence: list[str] | None = None,
    tags: list[str] | None = None,
) -> dict:
    """Log a new prediction for future calibration.

    Args:
        claim: The specific, falsifiable prediction (e.g., "VIX below 25 by April 15")
        probability: Assigned probability (0.0 to 1.0)
        framework: Which investor framework generated this (e.g., "Marks", "Soros")
        category: Domain category (regime, credit, equity, vol, rotation, etc.)
        resolve_by: Date by which the prediction should be resolved (YYYY-MM-DD)
        regime_context: What regime was active when prediction was made
        evidence: List of evidence points supporting the prediction
        tags: Optional tags for filtering

    Returns:
        The logged prediction record with its unique ID.
    """
    prediction = {
        "id": str(uuid.uuid4())[:8],
        "claim": claim,
        "probability": max(0.0, min(1.0, probability)),
        "framework": framework,
        "category": category,
        "created": date.today().isoformat(),
        "resolve_by": resolve_by,
        "regime_context": regime_context,
        "evidence": evidence or [],
        "tags": tags or [],
        "status": "open",
        "outcome": None,  # True/False when resolved
        "resolved_date": None,
        "resolution_notes": None,
    }

    predictions = _load_predictions()
    predictions.append(prediction)
    _save_predictions(predictions)

    return prediction


def resolve_prediction(
    prediction_id: str,
    outcome: bool,
    notes: str | None = None,
) -> dict | None:
    """Resolve a prediction with its actual outcome.

    Args:
        prediction_id: The prediction's unique ID
        outcome: True if the predicted event occurred, False if not
        notes: Optional resolution notes

    Returns:
        The updated prediction record, or None if not found.
    """
    predictions = _load_predictions()

    for p in predictions:
        if p["id"] == prediction_id:
            p["status"] = "resolved"
            p["outcome"] = outcome
            p["resolved_date"] = date.today().isoformat()
            p["resolution_notes"] = notes
            _save_predictions(predictions)
            return p

    return None


def get_open_predictions() -> list[dict]:
    """Get all unresolved predictions, sorted by resolve_by date."""
    predictions = _load_predictions()
    open_preds = [p for p in predictions if p["status"] == "open"]
    open_preds.sort(key=lambda p: p.get("resolve_by", "9999"))
    return open_preds


def get_overdue_predictions() -> list[dict]:
    """Get predictions past their resolve_by date that haven't been resolved."""
    today = date.today().isoformat()
    return [
        p for p in _load_predictions()
        if p["status"] == "open" and p.get("resolve_by", "9999") < today
    ]


# ── Auto-Extraction from Briefing Data ───────────────────────


def extract_predictions_from_briefing(briefing: dict) -> list[dict]:
    """Auto-extract falsifiable predictions from briefing data.

    Scans regime classification, contrarian views, alert triggers, and
    Fed game scenarios for claims that can be logged as predictions.
    Returns a list of prediction candidates (not yet logged — caller
    decides which to persist).
    """
    candidates = []

    # Regime prediction: will the current regime persist?
    regime = briefing.get("regime", {})
    quadrant = regime.get("quadrant")
    confidence = regime.get("confidence", 0)
    if quadrant and confidence > 0:
        candidates.append({
            "claim": f"Regime remains {quadrant} for the next 30 days",
            "probability": min(0.9, confidence + 0.3),  # regime persistence bias
            "framework": "Dalio",
            "category": "regime",
            "resolve_by": _days_from_now(30),
            "regime_context": quadrant,
            "tags": ["auto_extracted", "regime"],
        })

    # VIX mean reversion
    vix = _safe_get(briefing, "sentiment", "raw", "vix", "spot")
    if vix is not None:
        if vix > 30:
            candidates.append({
                "claim": f"VIX reverts below 25 within 20 trading days (currently {vix:.1f})",
                "probability": 0.70,  # historical base rate for VIX > 30 reverting
                "framework": "Tudor Jones",
                "category": "volatility",
                "resolve_by": _days_from_now(28),
                "regime_context": quadrant,
                "tags": ["auto_extracted", "vol_mean_reversion"],
            })
        elif vix < 14:
            candidates.append({
                "claim": f"VIX spikes above 20 within 30 days (currently {vix:.1f})",
                "probability": 0.55,  # mild base rate for low-vol breakout
                "framework": "Taleb",
                "category": "volatility",
                "resolve_by": _days_from_now(30),
                "regime_context": quadrant,
                "tags": ["auto_extracted", "vol_spike"],
            })

    # Contrarian views become predictions
    contrarian = briefing.get("contrarian", {})
    for view in contrarian.get("contrarian_views", []):
        if view.get("confidence") == "H":
            candidates.append({
                "claim": f"Contrarian view materializes: {view['contrarian_read'][:100]}",
                "probability": 0.60,  # high-confidence contrarian ≈ 60% realized
                "framework": f"Marks ({view.get('domain', 'general')})",
                "category": view.get("domain", "general"),
                "resolve_by": _days_from_now(60),
                "regime_context": quadrant,
                "tags": ["auto_extracted", "contrarian", view.get("domain", "")],
            })

    # Credit cycle prediction
    credit_cycle = _safe_get(briefing, "private_markets", "credit", "credit_cycle")
    if credit_cycle in ("late_cycle", "stress"):
        candidates.append({
            "claim": f"HY spreads widen by 50+ bps within 60 days (credit cycle: {credit_cycle})",
            "probability": 0.55 if credit_cycle == "late_cycle" else 0.70,
            "framework": "Marks",
            "category": "credit",
            "resolve_by": _days_from_now(60),
            "regime_context": quadrant,
            "tags": ["auto_extracted", "credit"],
        })

    # Fed game dominant strategy
    fed_game = briefing.get("fed_game", {})
    dominant = fed_game.get("dominant_strategy", {})
    if dominant.get("strategy") and dominant.get("confidence") in ("H", "M"):
        candidates.append({
            "claim": f"Fed follows {dominant['strategy']} at next FOMC meeting",
            "probability": 0.65 if dominant["confidence"] == "H" else 0.50,
            "framework": "Fed Game Theory",
            "category": "fed",
            "resolve_by": _days_from_now(45),
            "regime_context": quadrant,
            "tags": ["auto_extracted", "fed"],
        })

    return candidates


# ── Calibration Scoring ──────────────────────────────────────


def compute_calibration_report(
    framework: str | None = None,
    category: str | None = None,
    min_predictions: int = 5,
) -> dict:
    """Compute calibration metrics for resolved predictions.

    Args:
        framework: Filter to a specific investor framework (optional)
        category: Filter to a specific category (optional)
        min_predictions: Minimum resolved predictions needed for meaningful stats

    Returns:
        brier_score: Overall Brier score (0 = perfect, 1 = worst)
        calibration_curve: Bucketed calibration (predicted vs actual frequency)
        sharpness: How far from 50% predictions tend to be
        accuracy: Simple % of correct directional calls
        by_framework: Brier scores broken down by framework
        by_category: Brier scores broken down by category
        overdue: Count of predictions past resolve_by date
    """
    predictions = _load_predictions()
    resolved = [p for p in predictions if p["status"] == "resolved"]

    # Apply filters
    if framework:
        resolved = [p for p in resolved if framework.lower() in p.get("framework", "").lower()]
    if category:
        resolved = [p for p in resolved if p.get("category") == category]

    if len(resolved) < min_predictions:
        return {
            "status": "insufficient_data",
            "resolved_count": len(resolved),
            "min_required": min_predictions,
            "message": (
                f"Need at least {min_predictions} resolved predictions for meaningful "
                f"calibration. Currently have {len(resolved)}. Keep logging and resolving."
            ),
            "open_count": len([p for p in predictions if p["status"] == "open"]),
            "overdue_count": len(get_overdue_predictions()),
        }

    # Brier score
    brier = _compute_brier_score(resolved)

    # Calibration curve (bucket by predicted probability)
    cal_curve = _compute_calibration_curve(resolved)

    # Sharpness
    sharpness = _compute_sharpness(resolved)

    # Simple accuracy
    correct = sum(
        1 for p in resolved
        if (p["probability"] >= 0.5 and p["outcome"])
        or (p["probability"] < 0.5 and not p["outcome"])
    )
    accuracy = correct / len(resolved) if resolved else 0

    # Breakdown by framework
    by_framework = _breakdown_by_field(resolved, "framework")

    # Breakdown by category
    by_category = _breakdown_by_field(resolved, "category")

    # Breakdown by regime context
    by_regime = _breakdown_by_field(resolved, "regime_context")

    return {
        "status": "ok",
        "resolved_count": len(resolved),
        "brier_score": round(brier, 4),
        "brier_interpretation": _interpret_brier(brier),
        "calibration_curve": cal_curve,
        "sharpness": round(sharpness, 4),
        "accuracy": round(accuracy, 4),
        "by_framework": by_framework,
        "by_category": by_category,
        "by_regime": by_regime,
        "open_count": len([p for p in predictions if p["status"] == "open"]),
        "overdue_count": len(get_overdue_predictions()),
    }


def _compute_brier_score(resolved: list[dict]) -> float:
    """Brier score = mean((probability - outcome)^2)."""
    if not resolved:
        return 1.0
    total = 0.0
    for p in resolved:
        prob = p["probability"]
        outcome = 1.0 if p["outcome"] else 0.0
        total += (prob - outcome) ** 2
    return total / len(resolved)


def _compute_calibration_curve(resolved: list[dict]) -> list[dict]:
    """Bucket predictions by probability and compare to actual frequency."""
    buckets = [
        (0.0, 0.2, "0-20%"),
        (0.2, 0.4, "20-40%"),
        (0.4, 0.6, "40-60%"),
        (0.6, 0.8, "60-80%"),
        (0.8, 1.01, "80-100%"),
    ]

    curve = []
    for low, high, label in buckets:
        bucket_preds = [
            p for p in resolved if low <= p["probability"] < high
        ]
        if bucket_preds:
            avg_predicted = sum(p["probability"] for p in bucket_preds) / len(bucket_preds)
            actual_frequency = sum(1 for p in bucket_preds if p["outcome"]) / len(bucket_preds)
            curve.append({
                "bucket": label,
                "count": len(bucket_preds),
                "avg_predicted": round(avg_predicted, 3),
                "actual_frequency": round(actual_frequency, 3),
                "gap": round(abs(avg_predicted - actual_frequency), 3),
                "calibrated": abs(avg_predicted - actual_frequency) < 0.15,
            })
        else:
            curve.append({
                "bucket": label,
                "count": 0,
                "avg_predicted": None,
                "actual_frequency": None,
                "gap": None,
                "calibrated": None,
            })

    return curve


def _compute_sharpness(resolved: list[dict]) -> float:
    """Sharpness = mean(|probability - 0.5|). Higher = more decisive predictions."""
    if not resolved:
        return 0.0
    return sum(abs(p["probability"] - 0.5) for p in resolved) / len(resolved)


def _breakdown_by_field(resolved: list[dict], field: str) -> dict:
    """Compute Brier scores broken down by a categorical field."""
    groups: dict[str, list] = {}
    for p in resolved:
        key = p.get(field, "unknown") or "unknown"
        groups.setdefault(key, []).append(p)

    result = {}
    for key, preds in sorted(groups.items()):
        if len(preds) >= 3:  # need at least 3 for meaningful score
            brier = _compute_brier_score(preds)
            accuracy = sum(
                1 for p in preds
                if (p["probability"] >= 0.5 and p["outcome"])
                or (p["probability"] < 0.5 and not p["outcome"])
            ) / len(preds)
            result[key] = {
                "count": len(preds),
                "brier_score": round(brier, 4),
                "accuracy": round(accuracy, 4),
            }
        else:
            result[key] = {
                "count": len(preds),
                "brier_score": None,
                "accuracy": None,
                "note": "too few predictions for meaningful score",
            }

    return result


def _interpret_brier(score: float) -> str:
    """Human-readable interpretation of Brier score."""
    if score < 0.1:
        return "Excellent — predictions are well-calibrated and sharp"
    elif score < 0.2:
        return "Good — better than naive base rates"
    elif score < 0.25:
        return "Decent — room for improvement but adding value"
    elif score < 0.33:
        return "Mediocre — not much better than coin-flipping"
    else:
        return "Poor — predictions are miscalibrated or uninformative"


# ── Persistence ──────────────────────────────────────────────


def _load_predictions() -> list[dict]:
    """Load all predictions from the predictions file."""
    if not PREDICTIONS_FILE.exists():
        return []
    try:
        return json.loads(PREDICTIONS_FILE.read_text())
    except (json.JSONDecodeError, OSError):
        return []


def _save_predictions(predictions: list[dict]) -> None:
    """Save predictions to the predictions file."""
    PREDICTIONS_FILE.parent.mkdir(parents=True, exist_ok=True)
    PREDICTIONS_FILE.write_text(json.dumps(predictions, indent=2))


# ── Helpers ──────────────────────────────────────────────────


def _days_from_now(days: int) -> str:
    """Return a date string N days from today."""
    from datetime import timedelta
    return (date.today() + timedelta(days=days)).isoformat()


def _safe_get(d: dict | None, *keys, default=None):
    """Safely traverse nested dicts. Default only applies at the terminal key."""
    current = d
    for i, key in enumerate(keys):
        if isinstance(current, dict):
            is_last = (i == len(keys) - 1)
            current = current.get(key, default if is_last else None)
        else:
            return default
    return current
