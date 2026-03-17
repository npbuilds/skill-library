# Rating Rubric

## Auto-Score (0-100)

Computed from 5 factors, weighted:

### Token Efficiency (30%)
```
if body_words <= 1500: score = 100
elif body_words >= 5000: score = 0
else: score = round(100 * (5000 - body_words) / 3500)
```

### Progressive Disclosure (20%)
```
if body_words <= 1000: score = 100  (small enough to be self-contained)
elif reference_files > 0: score = 100  (good disclosure)
elif body_words <= 1500: score = 50  (borderline, no refs yet)
else: score = 0  (large body with no refs)
```

### Description Quality (20%)
```
if 20 <= description_words <= 60: score = 100
elif 15 <= description_words < 20: score = 80
elif 60 < description_words <= 100: score = 60
elif description_words < 15: score = 20
else: score = 10  (> 100 words)
```

### Structure (15%)
```
if 3 <= section_count <= 6: score = 100
elif section_count == 2: score = 80
elif section_count == 7 or section_count == 8: score = 70
elif section_count < 2: score = 30
else: score = max(0, 100 - (section_count - 8) * 15)
```

### Documentation (15%)
```
if reference_files > 0 or example_files > 0: score = 100
elif body_words <= 800: score = 70  (small and self-contained is OK)
elif body_words <= 1500: score = 40
else: score = 0  (large with no supporting docs)
```

### Final Computation
```
auto_score = round(
  token_efficiency * 0.30 +
  progressive_disclosure * 0.20 +
  description_quality * 0.20 +
  structure * 0.15 +
  documentation * 0.15
)
```

## Manual Rating (1-5)

User-assigned subjective rating:
- **5**: Essential skill, use frequently, works perfectly
- **4**: Very useful, reliable, minor improvements possible
- **3**: Useful but has notable issues or limited scope
- **2**: Rarely useful or frequently needs manual intervention
- **1**: Basically unused or broken

## Composite Score

```
if manual_rating is null:
  composite_score = auto_score
else:
  manual_scaled = (manual_rating / 5) * 100
  composite_score = round(auto_score * 0.7 + manual_scaled * 0.3)
```
