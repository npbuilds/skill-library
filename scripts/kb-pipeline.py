#!/usr/bin/env python3
"""
KB Engine pipeline (Layer 4).

Orchestrates: vault-sync (T0) → gap detection → tier routing → T1 enrichment.

Gap tiers:
  T0 — Registry data → vault note (handled by vault-sync.py, already done)
  T1 — Claude summarizes one skill into a richer vault note ($0.01-0.05/gap)
  T2 — Loom cross-domain synthesis (future, stubbed)
  T3 — Spelunker deep research (future, stubbed)

Usage:
    # Show gaps without processing
    python3 scripts/kb-pipeline.py --vault-dir /path/to/vault --dry-run

    # Enrich up to 5 T1 gaps
    python3 scripts/kb-pipeline.py --vault-dir /path/to/vault --limit 5

    # Enrich a specific skill
    python3 scripts/kb-pipeline.py --vault-dir /path/to/vault --skill rnpv-modeler

    # Budget cap (default $50/month)
    python3 scripts/kb-pipeline.py --vault-dir /path/to/vault --budget 10.00
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

_here = Path(__file__).resolve().parent
PROJECT_ROOT = _here.parent
REGISTRY_PATH = PROJECT_ROOT / "data" / "registry.json"
SPEND_LOG = PROJECT_ROOT / "data" / "maintenance-spend.jsonl"

# Import vault-sync's fenced block updater
sys.path.insert(0, str(_here))
from importlib.machinery import SourceFileLoader
_vs = SourceFileLoader("vault_sync", str(_here / "vault-sync.py")).load_module()
update_fenced_blocks = _vs.update_fenced_blocks
domain_from_location = _vs.domain_from_location

NOW = datetime.now(timezone.utc)
NOW_ISO = NOW.isoformat()
NOW_DATE = NOW.strftime("%Y-%m-%d")

# Cost estimates per tier (USD)
TIER_COSTS = {"T0": 0.0, "T1": 0.03, "T2": 0.20, "T3": 2.00}

# Domain value weights (from plan: biotech-venture, asclepius, archon weighted 2×)
HIGH_VALUE_DOMAINS = {"biotech-venture", "investing", "research"}


# ---------------------------------------------------------------------------
# Budget tracker
# ---------------------------------------------------------------------------

class BudgetTracker:
    """Tracks maintenance spend per month against a cap."""

    def __init__(self, monthly_cap: float = 50.0):
        self.cap = monthly_cap
        self.spent = 0.0
        self._load_current_month()

    def _load_current_month(self):
        """Load spend from maintenance-spend.jsonl for current month."""
        month_prefix = NOW.strftime("%Y-%m")
        if SPEND_LOG.exists():
            for line in SPEND_LOG.read_text().strip().split("\n"):
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                    if entry.get("month") == month_prefix:
                        self.spent += entry.get("cost", 0.0)
                except json.JSONDecodeError:
                    continue

    def would_exceed(self, tier: str) -> bool:
        cost = TIER_COSTS.get(tier, 0.0)
        return (self.spent + cost) > (self.cap * 0.8)  # abort at 80%

    def record(self, tier: str, skill: str, actual_cost: float):
        self.spent += actual_cost
        entry = {
            "ts": NOW_ISO,
            "month": NOW.strftime("%Y-%m"),
            "tier": tier,
            "skill": skill,
            "cost": actual_cost,
            "cumulative": round(self.spent, 4),
        }
        with open(SPEND_LOG, "a") as f:
            f.write(json.dumps(entry) + "\n")

    def summary(self) -> str:
        return f"${self.spent:.2f} / ${self.cap:.2f} ({self.spent/self.cap*100:.0f}%)"


# ---------------------------------------------------------------------------
# Gap detection
# ---------------------------------------------------------------------------

def detect_gaps(registry: dict, vault_dir: Path) -> list[dict]:
    """Compare registry vs. vault state → list of gaps with tier classification."""
    skills = registry.get("skills", {})
    active = {n: s for n, s in skills.items() if s.get("status") != "deprecated"}
    gaps = []

    for name, entry in active.items():
        domain = domain_from_location(entry.get("location", ""))
        note_path = vault_dir / "10-domains" / domain / f"{name}.md"
        score = entry.get("composite_score", 0)

        if not note_path.exists():
            # No vault note at all — T0 (vault-sync should have created it)
            gaps.append({
                "skill": name, "domain": domain, "tier": "T0",
                "reason": "no vault note", "score": score,
            })
            continue

        content = note_path.read_text()

        # Check if note has been enriched beyond the vault-sync template
        if "generated_by: vault-sync" in content:
            # Still the auto-generated template — candidate for T1 enrichment
            # Prioritize by score and domain value
            priority = score
            if domain in HIGH_VALUE_DOMAINS:
                priority *= 2

            gaps.append({
                "skill": name, "domain": domain, "tier": "T1",
                "reason": "vault-sync template only",
                "score": score, "priority": priority,
            })

    # Sort T1 by priority (highest first)
    gaps.sort(key=lambda g: -g.get("priority", g.get("score", 0)))

    return gaps


# ---------------------------------------------------------------------------
# T1: Claude-enriched skill summary
# ---------------------------------------------------------------------------

def fill_t1(name: str, entry: dict, vault_note_path: Path,
            client, model: str = "claude-sonnet-4-20250514") -> dict:
    """Enhance a vault note with a Claude-generated summary.

    Returns: {"status": "enriched", "input_tokens": N, "output_tokens": N, "cost": $}
    """
    # Read the skill's SKILL.md
    loc = entry.get("location", "")
    skill_md_path = PROJECT_ROOT / loc if loc else None
    if not skill_md_path or not skill_md_path.exists():
        return {"status": "skipped", "reason": "SKILL.md not found", "cost": 0.0}

    skill_content = skill_md_path.read_text(errors="replace")
    # Strip YAML frontmatter
    if skill_content.startswith("---"):
        end = skill_content.find("---", 3)
        if end > 0:
            skill_content = skill_content[end + 3:].strip()

    domain = domain_from_location(entry.get("location", ""))
    desc = entry.get("description", "").strip()

    prompt = f"""You are writing a knowledge base article for the skill "{name}" (domain: {domain}).

The full skill content is below. Write a clear, educational summary that:
1. Opens with a 1-2 sentence hook explaining what this skill does and why it matters
2. Describes the core methodology, framework, or approach (the "how")
3. Lists 3-5 key concepts or techniques with brief explanations
4. Notes practical applications or when to use this skill
5. Is 300-500 words — concise but substantive

Write in a direct, educational tone. Use markdown formatting (headers, lists, bold).
Do NOT include YAML frontmatter, the skill title, or metadata.
Do NOT repeat the description verbatim — synthesize and explain.

---

Skill description: {desc}

Full skill content:
{skill_content[:8000]}"""

    response = client.messages.create(
        model=model,
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )

    summary = response.content[0].text.strip()
    input_tokens = response.usage.input_tokens
    output_tokens = response.usage.output_tokens
    # Sonnet pricing: $3/M input, $15/M output
    cost = (input_tokens * 3.0 / 1_000_000) + (output_tokens * 15.0 / 1_000_000)

    # Update the vault note's content fence
    existing = vault_note_path.read_text()
    blocks = {"content": summary}
    updated = update_fenced_blocks(existing, blocks)

    # Also update frontmatter to mark as enriched
    updated = updated.replace(
        "generated_by: vault-sync",
        f"generated_by: kb-pipeline\nenriched_at: {NOW_DATE}",
    )

    vault_note_path.write_text(updated)

    return {
        "status": "enriched",
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "cost": round(cost, 4),
    }


# ---------------------------------------------------------------------------
# Pipeline
# ---------------------------------------------------------------------------

def run_pipeline(vault_dir: Path, limit: int = 5, budget_cap: float = 50.0,
                 target_skill: str | None = None, dry_run: bool = False) -> dict:
    """Run the full KB pipeline."""
    reg = json.loads(REGISTRY_PATH.read_text())
    budget = BudgetTracker(monthly_cap=budget_cap)

    print(f"Budget: {budget.summary()}")
    print()

    # Step 1: vault-sync (T0 baseline)
    print("Step 1: vault-sync (T0 baseline)...")
    sync_stats = _vs.sync(vault_dir, dry_run=dry_run)
    print(f"  Created: {sync_stats['created']}, Updated: {sync_stats['updated']}, "
          f"Unchanged: {sync_stats['unchanged']}")
    print()

    # Step 2: detect gaps
    print("Step 2: detecting gaps...")
    gaps = detect_gaps(reg, vault_dir)

    t0 = [g for g in gaps if g["tier"] == "T0"]
    t1 = [g for g in gaps if g["tier"] == "T1"]
    print(f"  T0 gaps: {len(t0)} (should be 0 after vault-sync)")
    print(f"  T1 candidates: {len(t1)} (enrichable with Claude)")
    print()

    # Filter to target skill if specified
    if target_skill:
        t1 = [g for g in t1 if g["skill"] == target_skill]
        if not t1:
            print(f"  Skill '{target_skill}' not found in T1 candidates")
            return {"gaps_detected": len(gaps), "processed": 0}

    if dry_run:
        print("Top 10 T1 candidates (by priority):")
        for g in t1[:10]:
            print(f"  {g['skill']:40s} domain={g['domain']:20s} score={g['score']} priority={g.get('priority', g['score'])}")
        return {"gaps_detected": len(gaps), "processed": 0, "dry_run": True}

    # Step 3: T1 enrichment
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("ANTHROPIC_API_KEY not set — T1 enrichment skipped")
        return {"gaps_detected": len(gaps), "processed": 0, "reason": "no_api_key"}

    import anthropic
    client = anthropic.Anthropic()

    processed = 0
    total_cost = 0.0
    results = []

    print(f"Step 3: enriching up to {limit} T1 gaps...")
    for gap in t1[:limit]:
        name = gap["skill"]
        if budget.would_exceed("T1"):
            print(f"  Budget threshold reached ({budget.summary()}) — stopping")
            break

        domain = gap["domain"]
        note_path = vault_dir / "10-domains" / domain / f"{name}.md"
        entry = reg["skills"][name]

        print(f"  [{processed+1}/{limit}] {name}...", end=" ", flush=True)
        try:
            result = fill_t1(name, entry, note_path, client)
            budget.record("T1", name, result["cost"])
            total_cost += result["cost"]
            processed += 1
            results.append({"skill": name, **result})
            print(f"✅ ({result['input_tokens']}+{result['output_tokens']} tokens, ${result['cost']:.4f})")
        except Exception as e:
            print(f"❌ {e}")
            results.append({"skill": name, "status": "error", "error": str(e)})

    print()
    print(f"Summary: {processed}/{limit} enriched, ${total_cost:.4f} spent")
    print(f"Budget after: {budget.summary()}")

    return {
        "gaps_detected": len(gaps),
        "t1_candidates": len(t1),
        "processed": processed,
        "total_cost": round(total_cost, 4),
        "budget": budget.summary(),
        "results": results,
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="KB Engine pipeline (Layer 4)")
    parser.add_argument("--vault-dir", required=True, help="Path to the Obsidian vault")
    parser.add_argument("--limit", type=int, default=5, help="Max T1 gaps to process (default: 5)")
    parser.add_argument("--budget", type=float, default=50.0, help="Monthly budget cap in USD (default: 50)")
    parser.add_argument("--skill", help="Process a specific skill only")
    parser.add_argument("--dry-run", action="store_true", help="Show gaps without processing")
    args = parser.parse_args()

    vault_dir = Path(args.vault_dir).resolve()
    print(f"KB Pipeline — {NOW_DATE}")
    print(f"Vault: {vault_dir}")
    print(f"Registry: {REGISTRY_PATH}")
    print()

    result = run_pipeline(
        vault_dir=vault_dir,
        limit=args.limit,
        budget_cap=args.budget,
        target_skill=args.skill,
        dry_run=args.dry_run,
    )

    print()
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
