# Canonical Template — Anthropic Structural Order

The literal template `cursed-speech` produces. Components are in the order Anthropic's prompting canon recommends (current as of Claude Opus 4.7 / Sonnet 4.6 / Haiku 4.5). When the canon updates, re-read [Prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices) and adjust this file.

The placeholders in `[brackets]` are filled at assembly time.

---

## Template

```
SYSTEM (component 1 — Role):
You are a [domain] expert specializing in [subdomain]. [Optional one-sentence
expansion of expertise framing.]


USER (components 2–7):

[2. Context / motivation]
[One paragraph explaining what we're trying to accomplish and why it matters.
Anthropic's heuristic: "Claude is smart enough to generalize from the
explanation." Don't just say what — say why.]

[3. Longform data — placed BEFORE the query]
<documents>
  <document index="1">
    <source>[source name or filename]</source>
    <document_content>
[content here, or {{PLACEHOLDER}} for variable injection]
    </document_content>
  </document>
  [additional documents as <document index="2">, <document index="3">, ...]
</documents>

[4. Examples — 3 to 5; relevant, diverse, structured]
<examples>
  <example>
    <input>[representative input that mirrors the actual use case]</input>
    <output>[desired output in the exact format we want produced]</output>
  </example>

  <example>
    <input>[edge case 1 — different from example 1]</input>
    <output>[output handling this edge case]</output>
  </example>

  <example>
    <input>[edge case 2 — covers another structural variation]</input>
    <output>[output]</output>
  </example>

  [optional 4th and 5th examples covering further edge cases]
</examples>

[5. Instructions — numbered when order or completeness matters]
Your task:

1. [first concrete step]
2. [second step]
3. [third step]
4. [...]

[Any scope clarification — Claude 4.7 is literal: "Apply this to every section,
not just the first one" if relevant.]

[6. Output format]
Place your answer in <answer> tags. [Specify any structural requirements:
"Use a markdown table for the comparison; use prose paragraphs for the
analysis."]

Do not include preambles like "Here is..." or "Based on..."

[7. Self-check]
Before finishing, verify your answer against these criteria:
- [criterion 1 — usually correctness check]
- [criterion 2 — usually completeness check]
- [criterion 3 — usually format check]

If any criterion fails, revise before submitting.
```

---

## Notes on Each Component

### Component 1 — Role assignment

- A single-sentence role steers tone and scope reliably.
- Avoid overloading: "You are an expert who is also a coach who also writes poetry" produces muddled outputs. Pick one.
- Set the role in the system message, not the user message — the model treats system as more authoritative.

### Component 2 — Context

- Anthropic's stated heuristic: "Show your prompt to a colleague with minimal context. If they'd be confused, Claude will be too."
- Two sentences is typically enough. More is fine if the task genuinely requires it.
- Don't smuggle instructions into the context; instructions live in component 5.

### Component 3 — Longform data placement

- The 30% quality improvement on multi-document inputs comes from putting data BEFORE the query, not after.
- Use the `<documents><document index="n">` structure even for a single document. The structure is what Claude is trained on.
- Add `<source>`, `<title>`, `<author>` subtags as relevant — they help with citation.

### Component 4 — Examples

- 3–5 is the sweet spot per Anthropic's docs. Fewer = unreliable shape; more = pattern overfitting.
- *Diverse* matters more than *many*. Each example should add something new.
- Examples MUST be wrapped in `<example>` / `<examples>` tags. Plain text examples get confused with instructions.
- For thinking-heavy tasks, examples can include `<thinking>` tags inside the output to demonstrate reasoning style.

### Component 5 — Instructions

- Use numbered lists when the steps are sequential and order matters.
- Use bullet points when steps are parallel and order is incidental.
- "Apply this to every section" — state scope explicitly. Claude 4.7 is more literal than predecessors.

### Component 6 — Output format

- Always tell Claude what to DO, not what NOT to do. "Use prose paragraphs" beats "don't use bullets."
- XML tags around output (`<answer>`, `<summary>`, `<analysis>`) make output parseable downstream and reduce preamble.
- For structured outputs (JSON, YAML), use Anthropic's Structured Outputs feature instead of asking in the prompt.

### Component 7 — Self-check

- "Before you finish, verify [criterion]" reliably catches errors for coding, math, and structured analysis tasks.
- Keep criteria concrete. "Verify the answer is correct" is too vague; "Verify each cited number appears in the source documents" is concrete.
- Self-check is not an afterthought — it's a documented capability gain in Anthropic's evals.

---

## What Changed in 2026 (Claude 4.6 / 4.7)

These are recent and easy to miss:

- **Prefilling is deprecated.** Don't add prefilled assistant messages on the last turn. Use Structured Outputs or explicit format instructions instead.
- **Adaptive thinking** (`thinking: {type: "adaptive"}`) replaces extended thinking with `budget_tokens`. The prompt can guide thinking with general instructions ("think thoroughly") rather than prescriptive step-by-step plans — Claude's reasoning often exceeds what a human would prescribe.
- **More literal instruction following.** State scope explicitly.
- **Effort levels matter.** Set `effort` (low/medium/high/xhigh/max) explicitly; `cursed-speech` recommends one alongside the prompt.

---

## Anti-patterns to Avoid

| Anti-pattern | Why it fails | Use instead |
|---|---|---|
| "You are the world's best expert" | Vague flattery; doesn't steer behavior | "You are a [domain] expert specializing in [subdomain]" |
| Long context at the end of the prompt | Loses the 30% quality improvement | Long context FIRST, query last |
| 1 or 2 examples | Insufficient pattern signal | 3–5 |
| Examples without `<example>` tags | Confused with instructions | Always wrap in `<example>` / `<examples>` |
| "Don't be verbose" / "Don't use jargon" | Negative instructions land weakly | "Use one paragraph" / "Use plain language" |
| Prefilled assistant message | Deprecated on Claude 4.6+ | Use output format instructions or Structured Outputs |
| "Think step by step" without thinking enabled | The model knows; the phrase is a tell | Just enable adaptive thinking; don't say "think step by step" |

---

## Sources

- [Prompting best practices (Anthropic, current)](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices) — canonical reference; read this before assembling
- [Prompt engineering overview](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview)
- [Anthropic GitHub interactive tutorial](https://github.com/anthropics/prompt-eng-interactive-tutorial)
- [[cursed-speech-foundations]] (vault) — distillation note on the structural order and what changed
