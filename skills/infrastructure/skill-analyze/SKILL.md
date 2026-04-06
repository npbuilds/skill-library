---
name: skill-analyze
description: >
  Analyze skills using the Anthropic API for precise token counting, description quality
  evaluation, content review, and decomposition suggestions. Use when the user wants deep
  AI-powered analysis of a skill beyond what local heuristics provide, or wants exact token counts.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Bash Grep Glob
---

# Skill Analyze — The Oracle

AI-powered skill analysis using the Anthropic API. Provides capabilities beyond local heuristics: precise token counting, description quality evaluation, content review, and decomposition suggestions.

## Prerequisites

Requires `ANTHROPIC_API_KEY` environment variable. If not set, operations fall back to local heuristics with a note about what's unavailable.

Check availability:
```bash
[ -n "$ANTHROPIC_API_KEY" ] && echo "API available" || echo "API unavailable — using local fallbacks"
```

## Operations

### 1. Precise Token Counting

Count exact tokens for a skill's content using the Anthropic token counting API.

**With API:**
- Read the skill's SKILL.md content
- Call the Anthropic messages API with the content to get exact token count
- Update the registry's `precise_tokens` field
- Compare to the heuristic estimate and report accuracy

**Local fallback:**
- Use `scripts/compute-tokens.sh` for the ~4 chars/token estimate
- Report that precise counting requires the API

Read `references/api-patterns.md` for the API call patterns.

### 2. Description Quality Analysis

Evaluate a skill's trigger description for specificity, coverage, and false-positive risk.

**With API:**
- Send the description to Claude with a structured prompt asking it to evaluate:
  - **Specificity**: How precisely does the description define when to trigger?
  - **Coverage**: Does it cover all legitimate use cases?
  - **False-positive risk**: Could unrelated prompts accidentally trigger this skill?
  - **Differentiation**: How distinct is it from other skill descriptions?
- Return a structured quality report with scores and suggestions

**Local fallback:**
- Check word count (20-60 ideal), action verb presence, trigger phrase patterns
- Flag generic descriptions ("helps with development") vs specific ones

### 3. Content Review

AI reads the SKILL.md body and suggests improvements.

**With API:**
- Send the full SKILL.md content to Claude with a review prompt
- Ask for evaluation of: writing conciseness, instruction clarity, progressive disclosure usage, missing sections, redundant content
- Return prioritized improvement suggestions

**Local fallback:**
- Report body word count, section count, reference file presence
- Flag known threshold violations from health checks

### 4. Decomposition Suggestions

For complex skills, AI proposes specific fork strategies.

**With API:**
- Send the skill content plus the decomposition strategies from `skills/skill-fork/references/decomposition-strategies.md` (when available)
- Ask Claude to identify natural split points, suggest child skill names and scopes
- Return a structured decomposition plan

**Local fallback:**
- Flag skills over threshold (>6 sections, >3000 words)
- Suggest manual review for decomposition opportunities

## Usage

Invoke for a single skill:
1. Read the target skill's SKILL.md
2. Check for `ANTHROPIC_API_KEY`
3. Run the requested operation (or all operations for a full analysis)
4. Update registry with any new data (precise_tokens, analysis notes)
5. Present results

## Output Format

```
ANALYSIS — skill-registry
━━━━━━━━━━━━━━━━━━━━━━━━━
API Status:  ✓ connected

Token Count:
  Heuristic:  1,422
  Precise:    1,490  (heuristic is 4.6% under)

Description Quality:
  Specificity:    9/10 — clear trigger phrases
  Coverage:       8/10 — covers browse, search, add, update, remove, sync
  False-positive: 2/10 — low risk, well-differentiated
  Suggestions:    none

Content Review:
  ✓ Well-structured, good progressive disclosure
  ⚠ Consider moving the auto-score table to a reference file

Decomposition:
  Not needed — skill is well-scoped (4 sections, 683 body words)
```
