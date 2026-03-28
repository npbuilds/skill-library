"""
CLI for the Skill Library — query stats, list skills, and check gaps from your terminal.

Usage (after pip install -e .):
    skills stats              # summary of all usage
    skills stats color-theory # stats for one skill
    skills list               # list all skills
    skills gaps               # show search gaps
    skills feedback <name> <rating> [--note "..."]

Or run directly:
    python cli.py stats
"""

import json

import click

from shared import (
    REGISTRY_PATH, USAGE_LOG, GAPS_LOG, FEEDBACK_LOG,
    load_log as _load_log,
)


def _load_registry() -> dict:
    try:
        return json.loads(REGISTRY_PATH.read_text())
    except FileNotFoundError:
        click.echo(f"Registry not found at {REGISTRY_PATH}", err=True)
        raise SystemExit(1)
    except json.JSONDecodeError as e:
        click.echo(f"Registry has invalid JSON: {e}", err=True)
        raise SystemExit(1)


@click.group()
def main():
    """Skill Library CLI — query your skill analytics from the terminal."""
    pass


@main.command()
@click.argument("skill_name", required=False)
def stats(skill_name):
    """Show usage and feedback stats (all skills or one specific skill)."""
    usage = _load_log(USAGE_LOG)
    feedback = _load_log(FEEDBACK_LOG)
    gaps = _load_log(GAPS_LOG)

    if not usage and not feedback and not gaps:
        click.echo("No analytics data yet. Use skills in Claude Desktop to start building stats.")
        return

    if skill_name:
        _show_skill_stats(skill_name, usage, feedback)
    else:
        _show_summary(usage, feedback, gaps)


def _show_skill_stats(name, usage, feedback):
    uses = [e for e in usage if e.get("skill") == name]
    fb = [e for e in feedback if e.get("skill") == name]

    click.echo(f"\n  {name}")
    click.echo(f"  {'─' * len(name)}")
    click.echo(f"  Uses: {len(uses)}")

    if uses:
        first = uses[0].get("timestamp", "?")[:10]
        last = uses[-1].get("timestamp", "?")[:10]
        click.echo(f"  First: {first}  Last: {last}")

    if fb:
        ratings = [e["rating"] for e in fb if "rating" in e]
        if ratings:
            avg = sum(ratings) / len(ratings)
            click.echo(f"  Rating: {avg:.1f}/5 ({len(ratings)} reviews)")
        notes = [e["note"] for e in fb if e.get("note")]
        for n in notes[-3:]:
            click.echo(f"    \"{n}\"")
    else:
        click.echo("  Rating: no feedback yet")
    click.echo()


def _show_summary(usage, feedback, gaps):
    # Usage counts
    counts: dict[str, int] = {}
    for e in usage:
        s = e.get("skill", "?")
        counts[s] = counts.get(s, 0) + 1

    if counts:
        click.echo("\n  SKILL USAGE")
        click.echo("  ───────────")
        sorted_usage = sorted(counts.items(), key=lambda x: x[1], reverse=True)
        click.echo(f"  Total loads: {len(usage)}  |  Unique skills: {len(counts)}\n")

        # Bar chart
        max_count = sorted_usage[0][1] if sorted_usage else 1
        max_name_len = max((len(name) for name, _ in sorted_usage[:10]), default=10)
        for name, count in sorted_usage[:10]:
            bar_len = int((count / max_count) * 20)
            bar = "█" * bar_len + "░" * (20 - bar_len)
            click.echo(f"  {name:<{max_name_len}}  {bar} {count}")

        # Unused
        try:
            registry = _load_registry()
            all_skills = set(registry.get("skills", {}).keys())
            unused = sorted(all_skills - set(counts.keys()))
            if unused:
                click.echo(f"\n  Never used ({len(unused)}): {', '.join(unused[:10])}")
                if len(unused) > 10:
                    click.echo(f"    ... and {len(unused) - 10} more")
        except SystemExit:
            pass

    # Feedback
    if feedback:
        click.echo("\n  FEEDBACK")
        click.echo("  ────────")
        fb_by_skill: dict[str, list[int]] = {}
        for e in feedback:
            s = e.get("skill", "?")
            r = e.get("rating")
            if r is not None:
                fb_by_skill.setdefault(s, []).append(r)

        for s, ratings in sorted(fb_by_skill.items(), key=lambda x: sum(x[1]) / max(len(x[1]), 1), reverse=True):
            avg = sum(ratings) / len(ratings)
            stars = "★" * round(avg) + "☆" * (5 - round(avg))
            click.echo(f"  {s}: {stars} {avg:.1f}/5 ({len(ratings)})")

    # Gaps
    if gaps:
        click.echo("\n  GAPS")
        click.echo("  ────")
        gap_counts: dict[str, int] = {}
        for e in gaps:
            q = e.get("query", "?")
            gap_counts[q] = gap_counts.get(q, 0) + 1
        for q, count in sorted(gap_counts.items(), key=lambda x: x[1], reverse=True)[:5]:
            click.echo(f"  \"{q}\" — {count}x")

    click.echo()


@main.command("list")
@click.option("--domain", "-d", help="Filter by domain")
@click.option("--type", "-t", "skill_type", help="Filter by type")
def list_skills(domain, skill_type):
    """List all skills in the registry."""
    registry = _load_registry()
    skills = registry.get("skills", {})

    results = []
    for name, entry in sorted(skills.items()):
        tags = entry.get("tags", [])
        if domain and f"domain:{domain}" not in tags:
            continue
        if skill_type and entry.get("type") != skill_type:
            continue
        results.append((name, entry))

    if not results:
        click.echo("No skills found matching those filters.")
        return

    click.echo(f"\n  {len(results)} skill(s)\n")

    # Group by domain
    by_domain: dict[str, list] = {}
    for name, entry in results:
        d = next(
            (t.split(":")[1] for t in entry.get("tags", []) if t.startswith("domain:")),
            "untagged",
        )
        by_domain.setdefault(d, []).append((name, entry))

    for d, items in sorted(by_domain.items()):
        click.echo(f"  {d}/")
        for name, entry in items:
            t = entry.get("type", "?")
            score = entry.get("composite_score", "?")
            health = entry.get("health_status", "?")
            icon = "●" if health == "healthy" else "○"
            click.echo(f"    {icon} {name}  [{t}]  score:{score}")
        click.echo()


@main.command()
def gaps():
    """Show search queries that found no or few matching skills."""
    gap_events = _load_log(GAPS_LOG)
    if not gap_events:
        click.echo("No gaps recorded yet.")
        return

    gap_counts: dict[str, dict] = {}
    for e in gap_events:
        q = e.get("query", "?")
        if q not in gap_counts:
            gap_counts[q] = {"count": 0, "zero_results": 0, "last": ""}
        gap_counts[q]["count"] += 1
        if e.get("result_count", 0) == 0:
            gap_counts[q]["zero_results"] += 1
        gap_counts[q]["last"] = e.get("timestamp", "?")[:10]

    click.echo(f"\n  SEARCH GAPS ({len(gap_counts)} unique queries)\n")
    for q, info in sorted(gap_counts.items(), key=lambda x: x[1]["count"], reverse=True):
        zero_pct = (info["zero_results"] / info["count"]) * 100
        click.echo(f"  \"{q}\"")
        click.echo(f"    searched {info['count']}x  |  {zero_pct:.0f}% found nothing  |  last: {info['last']}")
    click.echo()


@main.command("feedback")
@click.argument("skill_name")
@click.argument("rating", type=click.IntRange(1, 5))
@click.option("--note", "-n", default="", help="Optional note about the skill")
def record_feedback(skill_name, rating, note):
    """Record feedback for a skill (rating 1-5)."""
    from server import record_skill_feedback

    result = record_skill_feedback(skill_name, rating, note)
    click.echo(result)


if __name__ == "__main__":
    main()
