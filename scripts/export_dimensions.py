#!/usr/bin/env python3
"""Export aesthetic identity dimensions from markdown to JSON.

Parses skills/design/aesthetic-identity/references/dimension-registry.md
and emits app/data/dimensions.json for consumption by the profile page.

Also extracts the "Active Tendencies" section from current-profile.md
for the narrative summary on the profile page.

Usage:
    python3 scripts/export_dimensions.py [--dry-run]

Run after updating dimension-registry.md or current-profile.md to keep
the web profile page in sync with the source-of-truth markdown.
"""

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REGISTRY_PATH = ROOT / "skills" / "design" / "aesthetic-identity" / "references" / "dimension-registry.md"
PROFILE_PATH = ROOT / "skills" / "design" / "aesthetic-identity" / "references" / "current-profile.md"
OUTPUT_PATH = ROOT / "app" / "data" / "dimensions.json"

# Regex patterns
RE_CATEGORY = re.compile(r"^## ([A-Za-z][A-Za-z\s/-]+)$")
RE_DIMENSION = re.compile(r"^### (.+)$")
RE_POLES = re.compile(r"^\*\*(.+?)\*\* ◄.*?► \*\*(.+?)\*\*$")
RE_METRICS = re.compile(r"Position:\s*([\d.]+)\s*\|\s*Confidence:\s*([\d.]+)\s*\|\s*Data points:\s*(\d+)")
RE_MEASURES = re.compile(r"^\s*-\s*What it measures:\s*(.+)$")
RE_EVIDENCE = re.compile(r"^\s*-\s*Evidence:\s*(.+)$")
RE_DISCOVERY_EVIDENCE = re.compile(r"^\s*-\s*Discovery evidence:\s*(.+)$")
RE_DISCOVERED_DATE = re.compile(r"^\s*-\s*Discovered:\s*(\d{4}-\d{2}-\d{2})")


def parse_dimension_registry(text: str) -> dict:
    """Parse the dimension registry markdown into structured data."""
    lines = text.split("\n")
    dimensions = []
    categories = []
    current_category = None
    current_dim = None

    for line_no, line in enumerate(lines, start=1):
        # HTML comments and template section — stop processing dimensions
        if line.strip().startswith("<!--"):
            if current_dim:
                dimensions.append(current_dim)
                current_dim = None
            print(f"Note: Stopped parsing at HTML comment on line {line_no} (template section reached).", file=sys.stderr)
            break

        cat_match = RE_CATEGORY.match(line)
        if cat_match:
            cat_name = cat_match.group(1).strip()
            current_category = cat_name
            if cat_name not in categories:
                categories.append(cat_name)
            continue

        dim_match = RE_DIMENSION.match(line)
        if dim_match:
            # Save previous dimension if any
            if current_dim:
                dimensions.append(current_dim)
            # Skip the FORMAT FOR NEW DIMENSIONS template entry
            name = dim_match.group(1).strip()
            if name.startswith("[") and name.endswith("]"):
                current_dim = None
                continue
            current_dim = {
                "name": name,
                "category": current_category or "Uncategorized",
                "poles": [],
                "position": 0.5,
                "confidence": 0.0,
                "dataPoints": 0,
                "measures": "",
                "evidence": "",
                "discoveredDate": None,
            }
            continue

        if current_dim is None:
            continue

        # Poles line
        poles_match = RE_POLES.match(line.strip())
        if poles_match:
            current_dim["poles"] = [poles_match.group(1).strip(), poles_match.group(2).strip()]
            continue

        # Metrics
        metrics_match = RE_METRICS.search(line)
        if metrics_match:
            pos = float(metrics_match.group(1))
            conf = float(metrics_match.group(2))
            pts = int(metrics_match.group(3))
            # Bounds validation — clamp and warn
            if not (0.0 <= pos <= 1.0):
                print(f"WARNING: Dimension '{current_dim['name']}' position {pos} out of [0,1]; clamping.", file=sys.stderr)
                pos = max(0.0, min(1.0, pos))
            if not (0.0 <= conf <= 1.0):
                print(f"WARNING: Dimension '{current_dim['name']}' confidence {conf} out of [0,1]; clamping.", file=sys.stderr)
                conf = max(0.0, min(1.0, conf))
            if pts < 0:
                print(f"WARNING: Dimension '{current_dim['name']}' dataPoints {pts} negative; setting to 0.", file=sys.stderr)
                pts = 0
            current_dim["position"] = pos
            current_dim["confidence"] = conf
            current_dim["dataPoints"] = pts
            continue

        # What it measures
        measures_match = RE_MEASURES.match(line)
        if measures_match:
            current_dim["measures"] = measures_match.group(1).strip()
            continue

        # Evidence (regular or discovery)
        evidence_match = RE_EVIDENCE.match(line) or RE_DISCOVERY_EVIDENCE.match(line)
        if evidence_match:
            current_dim["evidence"] = evidence_match.group(1).strip()
            continue

        # Discovered date
        discovered_match = RE_DISCOVERED_DATE.match(line)
        if discovered_match:
            current_dim["discoveredDate"] = discovered_match.group(1)
            continue

    # Don't forget the last dimension
    if current_dim:
        dimensions.append(current_dim)

    return {
        "dimensions": dimensions,
        "categories": categories,
    }


def parse_active_tendencies(text: str) -> list:
    """Extract the Active Tendencies bullet points from current-profile.md."""
    lines = text.split("\n")
    in_section = False
    tendencies = []

    for line in lines:
        if line.startswith("## Active Tendencies"):
            in_section = True
            continue
        if in_section and line.startswith("## "):
            break
        if in_section and line.startswith("- "):
            # Strip leading bullet — bold-prefixed (**...**) bullets are valid tendencies
            tendency = line[2:].strip()
            # Skip italic-only "no signal yet" placeholder lines like "*Tendencies appear when..."
            if tendency.startswith("*") and not tendency.startswith("**"):
                continue
            if tendency:
                tendencies.append(tendency)

    return tendencies


def parse_summary(text: str) -> str:
    """Extract the bimodal summary blockquote from current-profile.md."""
    lines = text.split("\n")
    in_section = False
    summary_parts = []

    for line in lines:
        if line.startswith("## Summary"):
            in_section = True
            continue
        if in_section and line.startswith("## "):
            break
        if in_section and line.startswith("> "):
            summary_parts.append(line[2:].strip())

    return "\n".join(summary_parts).strip()


def parse_last_updated(text: str) -> str:
    """Extract the *Last updated: ...* line from current-profile.md."""
    match = re.search(r"\*Last updated:\s*(\d{4}-\d{2}-\d{2})\*", text)
    return match.group(1) if match else ""


def parse_total_outputs(text: str) -> int:
    """Extract *Total outputs tracked: N* from current-profile.md."""
    match = re.search(r"\*Total outputs tracked:\s*(\d+)\*", text)
    return int(match.group(1)) if match else 0


def main():
    dry_run = "--dry-run" in sys.argv

    # Read source files
    if not REGISTRY_PATH.exists():
        print(f"ERROR: dimension-registry.md not found at {REGISTRY_PATH}", file=sys.stderr)
        return 1

    registry_text = REGISTRY_PATH.read_text(encoding="utf-8")
    if PROFILE_PATH.exists():
        profile_text = PROFILE_PATH.read_text(encoding="utf-8")
    else:
        print(f"WARNING: current-profile.md not found at {PROFILE_PATH} — narrative fields will be empty.", file=sys.stderr)
        profile_text = ""

    # Parse
    parsed = parse_dimension_registry(registry_text)
    tendencies = parse_active_tendencies(profile_text)
    summary = parse_summary(profile_text)
    last_updated = parse_last_updated(profile_text)
    total_outputs = parse_total_outputs(profile_text)

    # Compute aggregates
    dims = parsed["dimensions"]
    avg_confidence = sum(d["confidence"] for d in dims) / len(dims) if dims else 0.0
    high_confidence_count = sum(1 for d in dims if d["confidence"] >= 0.7)
    medium_confidence_count = sum(1 for d in dims if 0.3 <= d["confidence"] < 0.7)
    low_confidence_count = sum(1 for d in dims if d["confidence"] < 0.3)

    output = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "lastUpdated": last_updated,
        "totalDimensions": len(dims),
        "totalOutputsTracked": total_outputs,
        "categories": parsed["categories"],
        "aggregates": {
            "avgConfidence": round(avg_confidence, 3),
            "highConfidence": high_confidence_count,
            "mediumConfidence": medium_confidence_count,
            "lowConfidence": low_confidence_count,
        },
        "summary": summary,
        "activeTendencies": tendencies,
        "dimensions": dims,
    }

    # Validation
    print(f"Parsed {len(dims)} dimensions across {len(parsed['categories'])} categories")
    print(f"  Categories: {', '.join(parsed['categories'])}")
    print(f"  Avg confidence: {avg_confidence:.3f}")
    print(f"  High/Med/Low: {high_confidence_count} / {medium_confidence_count} / {low_confidence_count}")
    print(f"  Active tendencies: {len(tendencies)}")
    if last_updated:
        print(f"  Last updated: {last_updated}")

    # Sanity check
    if len(dims) < 10:
        print(f"\nWARNING: Expected ~17 dimensions, got {len(dims)}. Check the parser.", file=sys.stderr)
    for d in dims:
        if not d["poles"] or len(d["poles"]) != 2:
            print(f"WARNING: Dimension '{d['name']}' has malformed poles: {d['poles']}", file=sys.stderr)

    if dry_run:
        print("\n(dry run — not writing output)")
        return 0

    # Ensure output directory exists
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Write
    OUTPUT_PATH.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(f"\nWrote {OUTPUT_PATH.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
