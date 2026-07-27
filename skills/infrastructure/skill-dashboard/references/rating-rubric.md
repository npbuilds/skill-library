# Rating Rubric

This document explains the active scoring model. The executable source of truth
is `mcp-server/shared.py`; MCP tools and maintenance scripts must import that
implementation rather than copying formulas.

## Auto-Score (0-100)

The automatic score combines six normalized axes:

| Axis | Weight | Signal |
|---|---:|---|
| Structure | 22% | Section density and description quality |
| Depth | 28% | Body-length sweet spot and reference coverage |
| Connectivity | 22% | `depends_on` plus `referenced_by` graph edges |
| Freshness | 17% | Time since `last_modified`, with gradual decay |
| Feedback | 11% | Mean append-only feedback rating, mapped from 1-5 to 20-100 |
| Usage | 0% | Recorded and displayed for observability, but not treated as quality |

The weights sum to 100%. Usage remains an explicit zero-weight axis because load
frequency is operational evidence, not reliable evidence of quality.

### Axis behavior

- **Structure:** favors useful section density and descriptions of 20-60 words.
- **Depth:** favors 300-5,000 body words and adds credit for reference files.
- **Connectivity:** rises as valid dependency and reverse-reference edges grow.
- **Freshness:** starts at 100 for changes within seven days and decays gradually.
- **Feedback:** averages 1-5 feedback events; no feedback is neutral at 50.
- **Usage:** reports relative loads without moving the score.

The final automatic score is:

```text
auto_score = round(
  structure    * 0.22 +
  depth        * 0.28 +
  connectivity * 0.22 +
  freshness    * 0.17 +
  usage        * 0.00 +
  feedback     * 0.11
)
```

## Manual Rating (1-100)

`manual_rating` is a persistent human quality judgment on the same 0-100 scale:

- **90-100:** essential and excellent
- **75-89:** strong and reliable
- **50-74:** useful with meaningful gaps
- **25-49:** weak or rarely useful
- **1-24:** broken, misleading, or effectively unused

This differs from append-only `feedback.jsonl` events, which remain 1-5 ratings
and feed the automatic feedback axis.

## Composite Score

```text
if manual_rating is null:
  composite_score = auto_score
else:
  composite_score = round(auto_score * 0.60 + manual_rating * 0.40)
```

Use `compute_auto_score` and `compute_composite_score` from
`mcp-server/shared.py` for all writes. Do not reimplement these formulas in
commands, hooks, or maintenance scripts.
