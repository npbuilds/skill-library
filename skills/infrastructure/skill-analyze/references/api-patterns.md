# Anthropic API Patterns

Reference for API interactions used by skill-analyze. All calls use the Anthropic Messages API.

## Authentication

```bash
# Verify API key is available
if [ -z "$ANTHROPIC_API_KEY" ]; then
  echo "ANTHROPIC_API_KEY not set — falling back to local heuristics"
  exit 0
fi
```

## Token Counting

Use the dedicated token counting endpoint to get exact counts without generating a response.

```python
import anthropic

client = anthropic.Anthropic()

# Count tokens for a piece of content
response = client.messages.count_tokens(
    model="claude-sonnet-4-6",
    messages=[{"role": "user", "content": skill_content}]
)
token_count = response.input_tokens
```

## Description Quality Prompt

```python
quality_prompt = f"""Evaluate this Claude Code skill description for trigger quality.

Description: {description}

Rate each dimension 1-10 and explain:
1. **Specificity**: How precisely does it define when to trigger?
2. **Coverage**: Does it cover all legitimate use cases?
3. **False-positive risk**: Could unrelated prompts accidentally trigger this?
4. **Differentiation**: How distinct is it from a generic skill?

Respond in JSON:
{{"specificity": {{"score": N, "reason": "..."}}, "coverage": {{"score": N, "reason": "..."}}, "false_positive_risk": {{"score": N, "reason": "..."}}, "differentiation": {{"score": N, "reason": "..."}}, "suggestions": ["...", "..."]}}
"""
```

## Content Review Prompt

```python
review_prompt = f"""Review this Claude Code SKILL.md for quality and suggest improvements.

{skill_content}

Evaluate:
1. Writing conciseness (any verbose sections?)
2. Instruction clarity (could an AI follow these unambiguously?)
3. Progressive disclosure (should any content move to references/?)
4. Missing sections (anything important left out?)
5. Redundant content (anything that repeats?)

Respond in JSON:
{{"conciseness": {{"score": N, "issues": [...]}}, "clarity": {{"score": N, "issues": [...]}}, "disclosure": {{"score": N, "issues": [...]}}, "completeness": {{"score": N, "missing": [...]}}, "redundancy": {{"score": N, "duplicates": [...]}}, "priority_suggestions": ["...", "..."]}}
"""
```

## API Cost Awareness

- Token counting: minimal cost (just the input tokens)
- Description quality: ~200-500 tokens output per analysis
- Content review: ~500-1000 tokens output per review
- Decomposition: ~500-1500 tokens output per suggestion

Recommend batching analysis for multiple skills to minimize API calls. A full analysis of one skill costs approximately 2,000-5,000 tokens total (input + output).

## Error Handling

```python
try:
    response = client.messages.create(...)
except anthropic.AuthenticationError:
    print("Invalid API key — check ANTHROPIC_API_KEY")
except anthropic.RateLimitError:
    print("Rate limited — try again in a moment")
except anthropic.APIError as e:
    print(f"API error: {e}")
```
