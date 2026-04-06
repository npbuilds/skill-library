# Style Evolution Observer — Quick Reference


## Quick Reference

| Signal | Dimension(s) affected | Direction |
|--------|----------------------|-----------|
| "too busy" / "too much" | Density | → Sparse |
| "too empty" / "needs more" | Density | → Rich |
| "make it warmer" / "too cold" | Temperature | → Warm |
| "more contrast" / "pops more" | Contrast | → Bold |
| "too flashy" / "tone it down" | Contrast, Emotional Register | → Muted, → Serious |
| "love the animation" | Motion Feel | reinforce current |
| "too much movement" | Motion Feel | → Static |
| Chose geometric shapes | Geometry | → Geometric |
| Chose organic/natural forms | Geometry | → Organic |
| Used monospace/grid layout | Precision | → Mechanical |
| Used handwritten/textured feel | Precision | → Expressive |
| Referenced retro/vintage | Temporal Register | → Retro |
| Referenced futuristic/novel | Temporal Register | → Futuristic |

## Confidence Scoring

```
volume      = log(n + 1) / log(21)          # 0→0, 5→0.42, 12→0.67, 20→1.0
consistency = 1 - stdev(observations) / 0.5  # 1.0 if all identical, 0.0 if spread ≥0.5
recency     = weighted avg where weight = 0.5^(age / 10)  # half-life of 10 outputs

confidence  = min(1.0, volume * max(0, consistency) * recency)
```
