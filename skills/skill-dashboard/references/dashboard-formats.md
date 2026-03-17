# Dashboard Format Reference

## ASCII Art Components

### Bar Charts
Use block characters scaled to a 10-character width:
- `█` (U+2588) — filled block
- `░` (U+2591) — empty block
- Scale: `bar_width = round(value / max_value * 10)`

### Borders
- `══` double line for major section borders
- `──` single line for subsection dividers
- `━━` heavy line for headers

### Status Indicators
- `✓` (U+2713) — healthy / passing
- `⚠` (U+26A0) — warning
- `✗` (U+2717) — critical / failing
- `—` (U+2014) — null / not applicable

### Column Alignment
- Left-align names and text
- Right-align numbers
- Use 2-space minimum gap between columns
- Minimum column widths: Name=20, Type=12, Score=5, Tokens=7

## Number Formatting
- Token counts: comma-separated thousands (1,638)
- Scores: integer, no decimals (85)
- Ratings: fraction format (4/5)
- Percentages: integer with % (73%)
