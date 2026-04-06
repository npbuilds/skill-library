"""Historical analog matching — finds past periods resembling current conditions.

Compares the current macro/sentiment/vol/positioning fingerprint against a
library of historical reference periods and returns the closest matches.
Each analog includes what happened next (forward returns), why the match
fits, and where it diverges from today.

Design choices:
- Uses a curated library of reference periods rather than raw time-series
  backtesting. This is intentional — the value is in qualitative "this
  rhymes with" analysis, not pseudo-scientific curve-fitting.
- Similarity is a weighted composite of regime, VIX level, yield curve,
  credit conditions, and positioning — not a single metric.
- Forward outcomes from analogs are descriptive, not predictive. They
  inform scenario thinking, not position sizing.

Reference periods are hand-curated from well-known market episodes.
As the Archon accumulates daily snapshots, those become a second source
of analogs for more recent/relevant matching.
"""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path

SNAPSHOTS_DIR = Path(__file__).parent.parent / "snapshots"


# ── Historical Reference Library ────────────────────────────────
# Each entry represents a distinct market episode with its fingerprint
# and what followed. This is the "institutional memory" of the system.

REFERENCE_PERIODS: list[dict] = [
    # ── Crisis / Panic episodes ──────────────────────────────
    {
        "id": "covid_crash_2020",
        "label": "COVID Crash (Mar 2020)",
        "period": "2020-02-20 to 2020-03-23",
        "fingerprint": {
            "regime": "deflation",
            "vix_level": 82.7,
            "vix_regime": "crisis",
            "term_structure": "backwardation",
            "yield_curve": "steepening",
            "hy_spread": 10.8,
            "credit_cycle": "stress",
            "sentiment_score": 5,
            "growth_direction": "falling",
            "inflation_direction": "falling",
            "positioning": "extreme_fear",
        },
        "forward_outcome": {
            "1m_spx": +20.0,
            "3m_spx": +35.0,
            "6m_spx": +40.0,
            "narrative": (
                "V-shaped recovery driven by unprecedented fiscal + monetary stimulus. "
                "SPX bottomed Mar 23, recovered to ATH by Aug 2020. The fastest bear "
                "market recovery in history. Lesson: when policy response is overwhelming, "
                "don't fight the tape."
            ),
        },
        "key_features": [
            "VIX >80 (all-time high area)",
            "Credit market seizure (HY >1000 bps)",
            "Massive fiscal response ($2.2T CARES Act)",
            "Fed emergency rate cut to zero + unlimited QE",
            "Forced liquidation across all asset classes",
        ],
    },
    {
        "id": "gfc_lehman_2008",
        "label": "Global Financial Crisis — Lehman (Sep-Nov 2008)",
        "period": "2008-09-15 to 2008-11-20",
        "fingerprint": {
            "regime": "deflation",
            "vix_level": 80.0,
            "vix_regime": "crisis",
            "term_structure": "backwardation",
            "yield_curve": "steepening",
            "hy_spread": 20.0,
            "credit_cycle": "stress",
            "sentiment_score": 3,
            "growth_direction": "falling",
            "inflation_direction": "falling",
            "positioning": "extreme_fear",
        },
        "forward_outcome": {
            "1m_spx": -15.0,
            "3m_spx": -25.0,
            "6m_spx": -10.0,
            "narrative": (
                "Unlike COVID, the GFC had no immediate V-recovery. SPX didn't bottom "
                "until March 2009 (5 months later). Credit markets remained frozen for "
                "quarters. Lesson: systemic banking crises take longer to resolve than "
                "exogenous shocks."
            ),
        },
        "key_features": [
            "Banking system insolvency (not just illiquidity)",
            "Credit default swap contagion",
            "Counterparty risk cascading through system",
            "Delayed and initially inadequate policy response",
            "Housing market collapse as root cause",
        ],
    },
    # ── Stagflation / Inflation episodes ─────────────────────
    {
        "id": "stagflation_2022",
        "label": "Inflation Shock + Rate Hikes (2022)",
        "period": "2022-01-01 to 2022-10-12",
        "fingerprint": {
            "regime": "stagflation",
            "vix_level": 33.0,
            "vix_regime": "elevated",
            "term_structure": "contango",
            "yield_curve": "inverting",
            "hy_spread": 5.5,
            "credit_cycle": "late_cycle",
            "sentiment_score": 20,
            "growth_direction": "falling",
            "inflation_direction": "rising",
            "positioning": "bearish",
        },
        "forward_outcome": {
            "1m_spx": -5.0,
            "3m_spx": +10.0,
            "6m_spx": +15.0,
            "narrative": (
                "SPX bottomed Oct 12, 2022 at 3,577 — a 27% peak-to-trough decline. "
                "The pivot wasn't the Fed (they kept hiking), but peak inflation expectations. "
                "Once CPI started declining, markets priced in the eventual pause. "
                "60/40 had its worst year since 1937 as bonds offered no hedge."
            ),
        },
        "key_features": [
            "CPI >9% — highest since 1981",
            "Fed hiking at fastest pace in 40 years",
            "60/40 portfolio failure (stocks AND bonds down)",
            "Commodity super-spike (oil, grains, metals)",
            "Dollar strength crushing EM and international",
        ],
    },
    {
        "id": "volcker_1980",
        "label": "Volcker Tightening (1980-1982)",
        "period": "1980-01-01 to 1982-08-12",
        "fingerprint": {
            "regime": "stagflation",
            "vix_level": 35.0,  # estimated — VIX didn't exist yet
            "vix_regime": "elevated",
            "term_structure": "contango",
            "yield_curve": "deeply_inverted",
            "hy_spread": 7.0,
            "credit_cycle": "stress",
            "sentiment_score": 15,
            "growth_direction": "falling",
            "inflation_direction": "rising",
            "positioning": "bearish",
        },
        "forward_outcome": {
            "1m_spx": -3.0,
            "3m_spx": +5.0,
            "6m_spx": +30.0,
            "narrative": (
                "Volcker broke inflation's back by pushing Fed funds to 20%. Two recessions "
                "(1980, 1981-82). But once it was clear inflation was defeated, the greatest "
                "bull market in history began (Aug 1982). Lesson: the pain of tightening "
                "creates the foundation for the next bull."
            ),
        },
        "key_features": [
            "Fed funds rate reached 20%",
            "Double-dip recession",
            "Inflation expectations 'de-anchored' then re-anchored",
            "Massive dollar strength",
            "Gold peaked at $850 then collapsed",
        ],
    },
    # ── Goldilocks / Low-vol episodes ────────────────────────
    {
        "id": "goldilocks_2017",
        "label": "Low-Vol Goldilocks (2017)",
        "period": "2017-01-01 to 2017-12-31",
        "fingerprint": {
            "regime": "goldilocks",
            "vix_level": 10.0,
            "vix_regime": "complacent",
            "term_structure": "contango",
            "yield_curve": "normal",
            "hy_spread": 3.5,
            "credit_cycle": "mid_cycle",
            "sentiment_score": 75,
            "growth_direction": "rising",
            "inflation_direction": "stable",
            "positioning": "bullish",
        },
        "forward_outcome": {
            "1m_spx": +5.0,
            "3m_spx": -10.0,
            "6m_spx": -2.0,
            "narrative": (
                "2017 was the lowest-vol year on record — SPX went up every month. "
                "Then Feb 2018 brought 'Volmageddon': XIV (inverse VIX) blew up, "
                "VIX spiked from 10 to 50 in days. Lesson: extended low-vol breeds "
                "complacency and complex vol-selling structures that amplify the eventual spike."
            ),
        },
        "key_features": [
            "VIX averaged 11 for the year (record low)",
            "SPX up every single month",
            "Massive short-vol complex ($2T+ notional)",
            "Tax reform euphoria",
            "Synchronized global growth narrative",
        ],
    },
    {
        "id": "mid_cycle_2019",
        "label": "Mid-Cycle Extension (2019)",
        "period": "2019-01-01 to 2019-12-31",
        "fingerprint": {
            "regime": "goldilocks",
            "vix_level": 16.0,
            "vix_regime": "normal",
            "term_structure": "contango",
            "yield_curve": "flat_to_inverted",
            "hy_spread": 3.8,
            "credit_cycle": "mid_cycle",
            "sentiment_score": 55,
            "growth_direction": "rising",
            "inflation_direction": "stable",
            "positioning": "neutral",
        },
        "forward_outcome": {
            "1m_spx": +2.0,
            "3m_spx": -30.0,  # COVID hit
            "6m_spx": -5.0,
            "narrative": (
                "Fed pivoted from hiking to cutting ('insurance cuts'). SPX rallied 29% "
                "in 2019. Yield curve inverted briefly (Aug 2019), raising recession fears, "
                "but the mid-cycle extension worked — until COVID. Lesson: yield curve "
                "inversion can give false positives or have very long lead times."
            ),
        },
        "key_features": [
            "Fed 'insurance cuts' after Dec 2018 tightening mistake",
            "Yield curve briefly inverted (Aug 2019)",
            "US-China trade war uncertainty",
            "Manufacturing recession, services strong",
            "Earnings growth stalled but multiples expanded",
        ],
    },
    # ── Reflation episodes ───────────────────────────────────
    {
        "id": "reflation_2020_h2",
        "label": "Post-COVID Reflation (H2 2020 — H1 2021)",
        "period": "2020-06-01 to 2021-06-30",
        "fingerprint": {
            "regime": "reflation",
            "vix_level": 25.0,
            "vix_regime": "elevated",
            "term_structure": "contango",
            "yield_curve": "steepening",
            "hy_spread": 4.5,
            "credit_cycle": "early_cycle",
            "sentiment_score": 60,
            "growth_direction": "rising",
            "inflation_direction": "rising",
            "positioning": "bullish",
        },
        "forward_outcome": {
            "1m_spx": +4.0,
            "3m_spx": +10.0,
            "6m_spx": +15.0,
            "narrative": (
                "Classic early-cycle reflation: everything rallied. Small caps massively "
                "outperformed large caps. Value beat growth. Commodities surged. "
                "Crypto entered mania phase. The 'everything rally' powered by "
                "stimulus checks + reopening demand."
            ),
        },
        "key_features": [
            "Massive fiscal stimulus ($1.9T American Rescue Plan)",
            "Fed holding at zero with forward guidance",
            "Vaccine rollout reopening the economy",
            "Small caps > large caps (IWM > SPY by 20%+)",
            "Commodity super-cycle narrative emerging",
        ],
    },
    {
        "id": "reflation_2016",
        "label": "Trump Reflation Trade (Nov 2016 — Jan 2018)",
        "period": "2016-11-08 to 2018-01-26",
        "fingerprint": {
            "regime": "reflation",
            "vix_level": 12.0,
            "vix_regime": "complacent",
            "term_structure": "contango",
            "yield_curve": "steepening",
            "hy_spread": 4.0,
            "credit_cycle": "mid_cycle",
            "sentiment_score": 70,
            "growth_direction": "rising",
            "inflation_direction": "rising",
            "positioning": "bullish",
        },
        "forward_outcome": {
            "1m_spx": +3.0,
            "3m_spx": +8.0,
            "6m_spx": +12.0,
            "narrative": (
                "Post-election reflation trade: tax cuts + deregulation + infrastructure "
                "spending narrative. Financials and industrials led. Small caps outperformed. "
                "Ended with the Feb 2018 Volmageddon when the vol-selling complex imploded."
            ),
        },
        "key_features": [
            "Tax reform expectations (realized Dec 2017)",
            "Deregulation narrative (especially financials)",
            "Rising rates with rising equities",
            "USD strength initially, then weakened in 2017",
            "Synchronized global growth",
        ],
    },
    # ── Taper tantrum / Policy error ─────────────────────────
    {
        "id": "taper_tantrum_2013",
        "label": "Taper Tantrum (May-Sep 2013)",
        "period": "2013-05-22 to 2013-09-18",
        "fingerprint": {
            "regime": "goldilocks",
            "vix_level": 20.0,
            "vix_regime": "normal",
            "term_structure": "contango",
            "yield_curve": "steepening",
            "hy_spread": 5.0,
            "credit_cycle": "mid_cycle",
            "sentiment_score": 40,
            "growth_direction": "rising",
            "inflation_direction": "stable",
            "positioning": "neutral",
        },
        "forward_outcome": {
            "1m_spx": +3.0,
            "3m_spx": +8.0,
            "6m_spx": +12.0,
            "narrative": (
                "Bernanke mentioned tapering QE, 10Y yield spiked from 1.6% to 3.0%. "
                "EM currencies crashed. But the Fed didn't actually taper until Dec 2013, "
                "and equities resumed their rally. Lesson: the announcement/expectation "
                "causes more damage than the actual tightening."
            ),
        },
        "key_features": [
            "10Y yield spike from 1.6% to 3.0%",
            "EM selloff (fragile five currencies)",
            "Gold crashed from $1,600 to $1,200",
            "Fed ultimately delayed the actual taper",
            "Communication policy failure",
        ],
    },
    {
        "id": "q4_2018_tantrum",
        "label": "Q4 2018 Tightening Tantrum",
        "period": "2018-10-01 to 2018-12-24",
        "fingerprint": {
            "regime": "deflation",
            "vix_level": 36.0,
            "vix_regime": "panic",
            "term_structure": "backwardation",
            "yield_curve": "flattening",
            "hy_spread": 5.3,
            "credit_cycle": "late_cycle",
            "sentiment_score": 12,
            "growth_direction": "falling",
            "inflation_direction": "falling",
            "positioning": "bearish",
        },
        "forward_outcome": {
            "1m_spx": +8.0,
            "3m_spx": +15.0,
            "6m_spx": +20.0,
            "narrative": (
                "Powell said rates were 'a long way from neutral' in Oct 2018, SPX dropped 20%. "
                "Christmas Eve 2018 was the bottom. Powell pivoted to dovish in Jan 2019, "
                "eventually cut 3 times. Lesson: Fed policy errors create the best buying "
                "opportunities when the Fed has room to reverse."
            ),
        },
        "key_features": [
            "Fed hiking into slowing growth",
            "Powell 'long way from neutral' comment",
            "Quantitative tightening (balance sheet runoff)",
            "US-China trade war escalation",
            "Christmas Eve panic selling (SPX -20% from peak)",
        ],
    },
    # ── Slow grind / Complacency ─────────────────────────────
    {
        "id": "dot_com_peak_2000",
        "label": "Dot-Com Bubble Peak (Jan-Mar 2000)",
        "period": "2000-01-01 to 2000-03-24",
        "fingerprint": {
            "regime": "goldilocks",
            "vix_level": 24.0,
            "vix_regime": "normal",
            "term_structure": "contango",
            "yield_curve": "inverting",
            "hy_spread": 5.5,
            "credit_cycle": "late_cycle",
            "sentiment_score": 90,
            "growth_direction": "rising",
            "inflation_direction": "rising",
            "positioning": "extreme_greed",
        },
        "forward_outcome": {
            "1m_spx": -5.0,
            "3m_spx": -12.0,
            "6m_spx": -15.0,
            "narrative": (
                "NASDAQ peaked Mar 10, 2000 at 5,048 and didn't recover for 15 years. "
                "SPX took 7 years. But the crash was slow initially — a tech-specific "
                "rotation masked the severity. Value dramatically outperformed growth "
                "for the next 7 years."
            ),
        },
        "key_features": [
            "Extreme euphoria and IPO mania",
            "Narrow leadership (tech/telecom only)",
            "Yield curve inverted",
            "Fed hiking cycle ongoing",
            "P/E ratios at historic extremes",
        ],
    },
    {
        "id": "ai_euphoria_2024",
        "label": "AI/Mag7 Euphoria (2024)",
        "period": "2024-01-01 to 2024-07-16",
        "fingerprint": {
            "regime": "goldilocks",
            "vix_level": 13.0,
            "vix_regime": "complacent",
            "term_structure": "contango",
            "yield_curve": "inverted",
            "hy_spread": 3.1,
            "credit_cycle": "mid_cycle",
            "sentiment_score": 78,
            "growth_direction": "rising",
            "inflation_direction": "falling",
            "positioning": "bullish",
        },
        "forward_outcome": {
            "1m_spx": -8.0,
            "3m_spx": +2.0,
            "6m_spx": +5.0,
            "narrative": (
                "Magnificent 7 drove 60%+ of SPX returns. Market breadth was historically "
                "narrow. July 2024 rotation: small caps surged as large-cap tech pulled back. "
                "AI capex narrative persisted. Lesson: narrow leadership can persist far "
                "longer than expected but creates fragile market structure."
            ),
        },
        "key_features": [
            "Mag 7 concentration at historic levels",
            "AI capex spending > $200B/year",
            "HY spreads near historic tights",
            "Fed on hold at 5.25-5.50%",
            "Disinflation continuing but slowly",
        ],
    },
]


# ── Matching Engine ─────────────────────────────────────────────


def find_analogs(
    briefing: dict,
    top_n: int = 5,
    min_similarity: float = 0.3,
) -> dict:
    """Find historical periods most similar to current conditions.

    Args:
        briefing: The full output from generate_briefing().
        top_n: Number of top matches to return.
        min_similarity: Minimum similarity score (0-1) to include.

    Returns:
        current_fingerprint: The derived fingerprint for today's conditions
        analogs: Ranked list of matching historical periods
        composite_outlook: Weighted-average forward return from analogs
        divergence_warnings: Where the current setup differs from all analogs
    """
    # Extract current fingerprint from briefing data
    current = _extract_fingerprint(briefing)

    # Score each reference period
    scored = []
    for ref in REFERENCE_PERIODS:
        similarity = _compute_similarity(current, ref["fingerprint"])
        if similarity >= min_similarity:
            divergences = _find_divergences(current, ref["fingerprint"])
            scored.append({
                "id": ref["id"],
                "label": ref["label"],
                "period": ref["period"],
                "similarity": round(similarity, 3),
                "forward_outcome": ref["forward_outcome"],
                "key_features": ref["key_features"],
                "divergences": divergences,
                "match_reasons": _explain_match(current, ref["fingerprint"]),
            })

    # Also check saved snapshots for recent analogs
    snapshot_matches = _check_snapshot_analogs(current)
    scored.extend(snapshot_matches)

    # Sort by similarity (highest first)
    scored.sort(key=lambda x: x["similarity"], reverse=True)
    analogs = scored[:top_n]

    # Composite forward outlook (similarity-weighted)
    composite = _compute_composite_outlook(analogs)

    # Find features unique to today (not well-represented in any analog)
    divergence_warnings = _find_novel_features(current, analogs)

    return {
        "current_fingerprint": current,
        "analog_count": len(analogs),
        "analogs": analogs,
        "composite_outlook": composite,
        "divergence_warnings": divergence_warnings,
        "note": (
            "Historical analogs inform scenario thinking — they are not predictions. "
            "No two market periods are identical. Use these as mental models, not trading signals."
        ),
    }


# ── Fingerprint Extraction ──────────────────────────────────────


def _extract_fingerprint(briefing: dict) -> dict:
    """Extract a standardized fingerprint from briefing data."""
    regime = briefing.get("regime", {})
    sentiment = briefing.get("sentiment", {})
    vix = _safe_get(sentiment, "raw", "vix") or {}
    composite = _safe_get(sentiment, "composite") or {}
    market = briefing.get("market", {})
    risk = briefing.get("risk", {})
    private_markets = briefing.get("private_markets", {})
    yields = briefing.get("yield_curve", {})

    # Determine positioning stance from sentiment + market context
    score = composite.get("score", 50) if isinstance(composite, dict) else 50
    if score > 80:
        positioning = "extreme_greed"
    elif score > 65:
        positioning = "bullish"
    elif score > 35:
        positioning = "neutral"
    elif score > 15:
        positioning = "bearish"
    else:
        positioning = "extreme_fear"

    # Credit data
    credit = private_markets.get("credit", {})
    hy_spread = credit.get("hy_spread")
    if hy_spread is None:
        hy_spread = credit.get("hy_oas")

    # Yield curve shape
    curve_shape = yields.get("curve_shape", "unknown")
    spread_10y2y = yields.get("spread_10y_2y")
    if spread_10y2y is not None:
        if spread_10y2y < -0.5:
            curve_shape = "deeply_inverted"
        elif spread_10y2y < 0:
            curve_shape = "inverted"
        elif spread_10y2y < 0.3:
            curve_shape = "flat"
        elif spread_10y2y < 1.0:
            curve_shape = "normal"
        else:
            curve_shape = "steepening"

    return {
        "regime": regime.get("quadrant", "unknown"),
        "vix_level": vix.get("spot"),
        "vix_regime": vix.get("regime", "unknown"),
        "term_structure": vix.get("term_structure", "unknown"),
        "yield_curve": curve_shape,
        "hy_spread": hy_spread,
        "credit_cycle": credit.get("credit_cycle", "unknown"),
        "sentiment_score": score,
        "growth_direction": _infer_direction(regime.get("growth_score", 0)),
        "inflation_direction": _infer_direction(regime.get("inflation_score", 0)),
        "positioning": positioning,
    }


# ── Similarity Scoring ──────────────────────────────────────────


# Feature weights — what matters most for analog matching
FEATURE_WEIGHTS = {
    "regime": 0.20,         # Regime quadrant match is the single most important factor
    "vix_level": 0.15,      # Vol level drives market behavior
    "vix_regime": 0.05,     # Categorical vol regime (redundant with level but useful)
    "term_structure": 0.05, # VIX term structure shape
    "yield_curve": 0.12,    # Yield curve shape predicts recessions
    "hy_spread": 0.10,      # Credit stress level
    "credit_cycle": 0.08,   # Credit cycle phase
    "sentiment_score": 0.08,  # Overall sentiment positioning
    "growth_direction": 0.07, # Growth direction (rising/falling)
    "inflation_direction": 0.05, # Inflation direction
    "positioning": 0.05,    # Market positioning stance
}


def _compute_similarity(current: dict, reference: dict) -> float:
    """Compute weighted similarity between two fingerprints (0 to 1)."""
    total_weight = 0.0
    total_score = 0.0

    for feature, weight in FEATURE_WEIGHTS.items():
        cur_val = current.get(feature)
        ref_val = reference.get(feature)

        if cur_val is None or ref_val is None:
            continue  # Skip features we can't compare

        total_weight += weight
        score = _compare_feature(feature, cur_val, ref_val)
        total_score += weight * score

    if total_weight == 0:
        return 0.0

    return total_score / total_weight


def _compare_feature(feature: str, current, reference) -> float:
    """Compare a single feature between current and reference (0 to 1)."""

    # Categorical features — exact match or partial credit
    if feature in ("regime", "credit_cycle", "positioning"):
        if current == reference:
            return 1.0
        # Partial credit for "adjacent" categories
        adjacency = {
            ("goldilocks", "reflation"): 0.4,
            ("reflation", "goldilocks"): 0.4,
            ("stagflation", "reflation"): 0.3,
            ("reflation", "stagflation"): 0.3,
            ("deflation", "stagflation"): 0.3,
            ("stagflation", "deflation"): 0.3,
            ("goldilocks", "deflation"): 0.1,
            ("deflation", "goldilocks"): 0.1,
            ("mid_cycle", "early_cycle"): 0.5,
            ("early_cycle", "mid_cycle"): 0.5,
            ("late_cycle", "mid_cycle"): 0.5,
            ("mid_cycle", "late_cycle"): 0.5,
            ("late_cycle", "stress"): 0.4,
            ("stress", "late_cycle"): 0.4,
            ("early_cycle", "late_cycle"): 0.2,
            ("late_cycle", "early_cycle"): 0.2,
            ("bullish", "extreme_greed"): 0.5,
            ("extreme_greed", "bullish"): 0.5,
            ("bearish", "extreme_fear"): 0.5,
            ("extreme_fear", "bearish"): 0.5,
            ("neutral", "bullish"): 0.4,
            ("bullish", "neutral"): 0.4,
            ("neutral", "bearish"): 0.4,
            ("bearish", "neutral"): 0.4,
        }
        return adjacency.get((str(current), str(reference)), 0.0)

    # Categorical features — exact match only
    if feature in ("vix_regime", "term_structure", "yield_curve",
                    "growth_direction", "inflation_direction"):
        return 1.0 if current == reference else 0.0

    # Numeric features — distance-based with feature-specific scale
    if feature == "vix_level":
        # VIX similarity: within 5 points = high match, 20+ = no match
        if isinstance(current, (int, float)) and isinstance(reference, (int, float)):
            diff = abs(current - reference)
            return max(0, 1.0 - diff / 20.0)

    if feature == "hy_spread":
        # HY spread: within 0.5% = high match, 5%+ = no match
        if isinstance(current, (int, float)) and isinstance(reference, (int, float)):
            diff = abs(current - reference)
            return max(0, 1.0 - diff / 5.0)

    if feature == "sentiment_score":
        # Sentiment: within 10 points = high match, 50+ = no match
        if isinstance(current, (int, float)) and isinstance(reference, (int, float)):
            diff = abs(current - reference)
            return max(0, 1.0 - diff / 50.0)

    return 0.0


def _explain_match(current: dict, reference: dict) -> list[str]:
    """Generate human-readable reasons why two fingerprints match."""
    reasons = []

    if current.get("regime") == reference.get("regime"):
        reasons.append(f"Same regime quadrant: {current['regime']}")

    cur_vix = current.get("vix_level")
    ref_vix = reference.get("vix_level")
    if cur_vix is not None and ref_vix is not None and abs(cur_vix - ref_vix) < 10:
        reasons.append(f"Similar VIX level ({cur_vix:.0f} vs {ref_vix:.0f})")

    if current.get("yield_curve") == reference.get("yield_curve"):
        reasons.append(f"Same yield curve shape: {current['yield_curve']}")

    if current.get("credit_cycle") == reference.get("credit_cycle"):
        reasons.append(f"Same credit cycle phase: {current['credit_cycle']}")

    if current.get("growth_direction") == reference.get("growth_direction"):
        reasons.append(f"Same growth direction: {current['growth_direction']}")

    if current.get("inflation_direction") == reference.get("inflation_direction"):
        reasons.append(f"Same inflation direction: {current['inflation_direction']}")

    if current.get("term_structure") == reference.get("term_structure"):
        reasons.append(f"Same VIX term structure: {current['term_structure']}")

    if current.get("positioning") == reference.get("positioning"):
        reasons.append(f"Same positioning stance: {current['positioning']}")

    return reasons


def _find_divergences(current: dict, reference: dict) -> list[str]:
    """Find important differences between current conditions and reference."""
    divergences = []

    if current.get("regime") != reference.get("regime"):
        divergences.append(
            f"Regime differs: today is {current.get('regime')}, "
            f"analog was {reference.get('regime')}"
        )

    cur_vix = current.get("vix_level")
    ref_vix = reference.get("vix_level")
    if cur_vix is not None and ref_vix is not None and abs(cur_vix - ref_vix) > 15:
        divergences.append(
            f"VIX level significantly different: today {cur_vix:.0f} vs analog {ref_vix:.0f}"
        )

    if current.get("yield_curve") != reference.get("yield_curve"):
        divergences.append(
            f"Yield curve shape differs: today {current.get('yield_curve')}, "
            f"analog was {reference.get('yield_curve')}"
        )

    cur_hy = current.get("hy_spread")
    ref_hy = reference.get("hy_spread")
    if cur_hy is not None and ref_hy is not None and abs(cur_hy - ref_hy) > 2.0:
        divergences.append(
            f"HY spread very different: today {cur_hy:.1f}% vs analog {ref_hy:.1f}%"
        )

    if current.get("credit_cycle") != reference.get("credit_cycle"):
        divergences.append(
            f"Credit cycle phase differs: today {current.get('credit_cycle')}, "
            f"analog was {reference.get('credit_cycle')}"
        )

    return divergences


# ── Composite Outlook ───────────────────────────────────────────


def _compute_composite_outlook(analogs: list[dict]) -> dict:
    """Compute similarity-weighted average forward returns from analogs."""
    if not analogs:
        return {
            "status": "no_analogs",
            "message": "No sufficiently similar historical analogs found.",
        }

    horizons = ["1m_spx", "3m_spx", "6m_spx"]
    weighted = {h: 0.0 for h in horizons}
    total_weight = 0.0
    narratives = []

    for analog in analogs:
        w = analog["similarity"]
        outcome = analog.get("forward_outcome", {})
        # Only include analogs that have numeric forward return data
        # (snapshot-based analogs may lack these)
        has_returns = any(
            isinstance(outcome.get(h), (int, float)) for h in horizons
        )
        if has_returns:
            total_weight += w
            for h in horizons:
                val = outcome.get(h, 0)
                if isinstance(val, (int, float)):
                    weighted[h] += w * val
        narratives.append(f"[{analog['label']}] {outcome.get('narrative', '')[:120]}...")

    if total_weight == 0:
        return {"status": "no_weight"}

    return {
        "status": "ok",
        "weighted_forward_returns": {
            h: round(weighted[h] / total_weight, 1) for h in horizons
        },
        "analog_count": len(analogs),
        "dominant_analog": analogs[0]["label"] if analogs else None,
        "narrative_summary": narratives[:3],
        "caveat": (
            "These are similarity-weighted averages from past analogs. "
            "History rhymes but doesn't repeat. Use as one input among many."
        ),
    }


# ── Novel Feature Detection ────────────────────────────────────


def _find_novel_features(current: dict, analogs: list[dict]) -> list[str]:
    """Identify aspects of today's conditions not well-represented in analogs."""
    warnings = []

    if not analogs:
        return ["No suitable analogs found — current conditions may be unprecedented."]

    # Check if the best match is still pretty different
    if analogs[0]["similarity"] < 0.5:
        warnings.append(
            f"Best analog match is only {analogs[0]['similarity']:.0%} similar — "
            "current conditions are relatively novel. Treat analogs with extra caution."
        )

    # Check for features where ALL analogs diverge
    all_regimes = [a.get("forward_outcome", {}).get("1m_spx", 0) for a in analogs]
    if all_regimes:
        signs = [1 if x > 0 else -1 for x in all_regimes if x != 0]
        if signs and len(set(signs)) > 1:
            warnings.append(
                "Analogs disagree on 1-month direction — mixed signals. "
                "The analog set does not point to a clear directional view."
            )

    return warnings


# ── Snapshot-Based Analogs ──────────────────────────────────────


def _check_snapshot_analogs(current: dict) -> list[dict]:
    """Check saved daily snapshots for recent analog matches.

    As the system accumulates snapshots, older ones become matchable
    analogs with known forward outcomes (later snapshots show what happened).
    Only matches snapshots at least 30 days old (need enough time for
    forward outcome to be meaningful).
    """
    if not SNAPSHOTS_DIR.exists():
        return []

    today = date.today()
    matches = []

    snapshot_files = sorted(SNAPSHOTS_DIR.glob("20??-??-??.json"))
    for f in snapshot_files:
        try:
            snap_date = date.fromisoformat(f.stem)
        except ValueError:
            continue

        # Need at least 30 days of forward data
        days_ago = (today - snap_date).days
        if days_ago < 30:
            continue

        try:
            data = json.loads(f.read_text())
            briefing = data.get("data", data)
            snap_fp = _extract_fingerprint(briefing)
            similarity = _compute_similarity(current, snap_fp)

            if similarity >= 0.5:  # Higher threshold for snapshot matches
                matches.append({
                    "id": f"snapshot_{f.stem}",
                    "label": f"Archon Snapshot ({f.stem})",
                    "period": f.stem,
                    "similarity": round(similarity, 3),
                    "forward_outcome": {
                        "narrative": (
                            f"This is a saved Archon snapshot from {days_ago} days ago. "
                            "Check the current snapshot to see what happened next."
                        ),
                    },
                    "key_features": [f"Saved snapshot from {f.stem}"],
                    "divergences": _find_divergences(current, snap_fp),
                    "match_reasons": _explain_match(current, snap_fp),
                })
        except (json.JSONDecodeError, OSError, KeyError):
            continue

    return matches


# ── Helpers ─────────────────────────────────────────────────────


def _infer_direction(score: float | None) -> str:
    """Infer direction from a growth or inflation score."""
    if score is None:
        return "unknown"
    if score > 0.15:
        return "rising"
    elif score < -0.15:
        return "falling"
    return "stable"


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
