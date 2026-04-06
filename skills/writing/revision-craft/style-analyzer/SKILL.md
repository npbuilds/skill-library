---
name: style-analyzer
description: >
  Analyze and characterize the style of a prose text — sentence length distribution, diction
  register, vocabulary richness, syntactic patterns, and voice signature. Use when the user wants
  to understand what makes a text's prose distinctive, compare styles, or diagnose style
  inconsistencies.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Bash Glob
---

# Style Analyzer — The Prose X-Ray

Characterize the style DNA of a prose text through both quantitative measurement and qualitative assessment. This skill answers: *What does this prose sound like, and what specific features create that sound?*

## How to Run

### Input

The user provides:
1. **Text** — the prose to analyze (inline, file path, or clipboard)
2. **Purpose** (optional):
   - `characterize` — describe the style (default)
   - `compare` — compare two texts
   - `diagnose` — find style inconsistencies within a single text
   - `match` — identify what features to reproduce when writing in a similar style

### Steps

**Quantitative Pass** (measurable features)

1. **Sentence length distribution**
   - Average sentence length (words)
   - Standard deviation (high = varied rhythm; low = monotonous)
   - Min/max range
   - Percentage of short (< 10 words), medium (10-25), and long (25+)

2. **Opener variety**
   - First word of each sentence, classified by part of speech
   - Percentage starting with subject-pronoun (I, He, She, The, It)
   - Diversity score (unique openers / total sentences)

3. **Vocabulary metrics**
   - Type-Token Ratio (unique words / total words) — higher = richer vocabulary
   - Percentage of Anglo-Saxon vs. Latinate words (sample-based estimate)
   - Average word length (syllables)

4. **Syntactic profile**
   - Percentage of simple, compound, complex, compound-complex sentences
   - Dominant branching direction (right/left/mid)
   - Fragment usage frequency

5. **Readability baseline**
   - Flesch-Kincaid grade level (diagnostic only — not a quality measure)
   - Flesch Reading Ease score

**Qualitative Pass** (requires craft judgment)

1. **Voice/style/tone classification**
   - Voice register: minimalist / conversational / literary / academic / lyric
   - Tone: earnest / ironic / detached / intimate / urgent
   - Narrative distance (Gardner's 1-5 scale, if applicable)

2. **Signature features**
   - What makes this prose sound like *itself*? Identify 3-5 distinctive features.
   - Examples: "Heavy use of fragments for emphasis," "Latinate vocabulary in a conversational register," "Anaphora as primary rhythmic device"

3. **Consistency assessment**
   - Does the style hold across the sample? Flag register shifts, voice breaks, or inconsistent diction.

### Output

A **Style Report** with:
- Quantitative metrics table
- Qualitative assessment (2-3 paragraphs)
- Signature features list
- For `compare` mode: side-by-side metrics and a narrative comparison
- For `diagnose` mode: flagged inconsistencies with locations
- For `match` mode: a checklist of features to reproduce

## Interpretation Guidelines

**Sentence length**: Average 15-20 words = standard readable prose. Below 12 = terse/minimalist. Above 25 = complex/literary. Standard deviation matters as much as average — low SD with any average = flat rhythm.

**Type-Token Ratio**: 0.4-0.5 = normal range for prose. Above 0.6 = unusually rich vocabulary. Below 0.35 = repetitive. Note: TTR is length-sensitive — compare only texts of similar length.

**Readability scores**: Grade 6-8 = accessible general audience. Grade 10-12 = educated general audience. Grade 14+ = specialist/academic. Remember: these measure *ease of decoding*, not quality. Literary prose intentionally exceeds accessible grade levels.

**Important caveat**: Quantitative metrics are diagnostic tools, not quality measures. A high TTR doesn't mean better prose; a low Flesch-Kincaid score doesn't mean bad prose. The numbers help describe *what* the prose is doing. *Whether* it works is a qualitative judgment.

## Scope Boundaries

**This skill handles**: Analyzing and characterizing prose style — measurement, description, comparison, and diagnosis.

**This skill does NOT**:
- Edit prose (that's `prose-editor`)
- Judge quality (it describes features; the user judges quality)
- Analyze content, argument, or narrative structure (only style)
