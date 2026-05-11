---
name: cursed-speech
description: >
  Formulate a problem statement as a Claude prompt in Anthropic's canonical structural order
  — role, context, longform-data-first, examples, numbered instructions, output format,
  self-check. Recommends downstream Archon skills via hybrid static-map plus runtime search,
  plus an effort level. Use when the audience tag is LLM. Returns a complete, ready-to-execute
  prompt block.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Write
---

# Cursed Speech — The LLM Prompt Formulator

Words with binding power require brutal compression and selection. Cursed speech takes an audited problem statement and assembles it into a Claude prompt in the structural order Anthropic's prompting canon recommends. It also recommends which downstream Archon skills the prompt should invoke and what effort level to set.

The skill's restriction (in JJK terms): it only accepts statements that have passed `statement-grader` with all six axes ≥3/5. A statement that hasn't been audited produces a prompt that the model can't act on — the binding power requires the precision.

For the structural foundations and what changed with Claude 4.6/4.7, see [[cursed-speech-foundations]] in the vault. For the canonical template with placeholders, see `references/canonical-template.md`.

## Input Contract

`cursed-speech` accepts:
- A problem statement (audited; if unaudited, route to `statement-grader` first)
- Audience tag: must be `LLM` (this skill is the LLM-only compression path)
- A downstream task description: what should Claude do with this prompt?
- Optional: target Claude model (defaults to Claude Opus 4.7 conventions)
- Optional: any preexisting documents/data to embed

If the input statement hasn't been graded, return: "deferred — run statement-grader first." Do not produce a prompt from an unaudited statement.

## The Canonical Structural Order

Output is assembled in this order. The order is empirical, not aesthetic — Anthropic's docs report up to 30% quality improvement on multi-document inputs from query-at-end placement.

| # | Component | Shape | Purpose |
|---|---|---|---|
| 1 | **Role assignment** | `system: "You are a [domain] expert..."` | Steers tone and scope |
| 2 | **Context / motivation** | One paragraph; explain *why* the task matters | Claude generalizes from explanation |
| 3 | **Longform data** | `<documents><document index="n"><source/><document_content/></document></documents>` | Place ABOVE the query — this is the 30% win |
| 4 | **Examples** | `<examples><example>...</example></examples>` (3–5) | Shape output format and tone; cover edge cases |
| 5 | **Instructions** | Numbered list when order matters | Sequential steps |
| 6 | **Output format** | "Place your answer in `<answer>` tags" — tell Claude what TO do, not what NOT to do | Makes output parseable downstream |
| 7 | **Self-check** | "Before you finish, verify your answer against [criteria]" | Catches errors reliably for coding/math/structured analysis |

### Important Constraints (Claude 4.6 / 4.7)

These follow Anthropic's current canon and are easy to miss:

- **No prefilled assistant messages.** Deprecated as of Claude 4.6; not supported on Mythos Preview. Use Structured Outputs or explicit format instructions.
- **State scope explicitly.** Claude 4.7 is more literal; "apply to every section, not just the first" beats implicit scope.
- **Use adaptive thinking** (`thinking: {type: "adaptive"}`), not extended thinking with `budget_tokens`.
- **Multishot examples can include `<thinking>` tags** to demonstrate reasoning patterns.

## Recommendations

Cursed-speech produces two recommendations alongside the prompt block: an effort level and a list of downstream Archon skills the prompt should invoke.

### Effort Level Routing

Anthropic's effort parameter (max / xhigh / high / medium / low) trades intelligence for cost+latency. Cursed-speech recommends one based on the task:

| Task type | Recommended effort |
|---|---|
| Coding, agentic loops, multi-step tool use | **xhigh** |
| Knowledge work, vision, memory tasks, intelligence-sensitive | **high** (minimum for these) |
| Cost-sensitive but still needs reasoning | **medium** |
| Short scoped tasks, latency-sensitive, simple lookups | **low** |
| Maximum capability, willing to pay for diminishing returns | **max** (test before defaulting) |

Always state the effort level explicitly in the output. The skill is opinionated: a prompt without effort-level guidance is incomplete.

### Skill Recommendation (Hybrid)

Cursed-speech recommends downstream Archon skills the prompt should invoke. Hybrid strategy:

1. **Static map first** (offline-friendly, fast). Read `references/skill-recommendation-map.md` for canonical task-type → skill mappings.
2. **Runtime search** (when MCP available, more accurate). Query `mcp__skill-library__search_skills` with the task description. Merge results with static map; deduplicate.
3. **Output:** 2–4 recommended skills, each with one-line rationale. If a recommended skill is in a domain the user might not have loaded, note that in the rationale.

If both static map and runtime search return nothing relevant, output "no skill recommendations — generic Claude reasoning sufficient" rather than fabricating.

## Process

1. **Verify input.** Confirm statement is graded and audience is `LLM`. Otherwise route back.
2. **Read foundations.** Quickly re-read `references/canonical-template.md` for the current structural order (Anthropic's docs evolve; the template cites the canonical URL).
3. **Assemble components 1–7** from the input statement, downstream task, and any provided data.
4. **Recommend skills** via the hybrid strategy above.
5. **Recommend effort** per the routing table.
6. **Run self-check** against the prompt's specificity, scope, and answerability axes (the colleague test from `[[cursed-speech-foundations]]`: would a colleague with minimal context know what to do?).
7. **Output** the assembled block.

## Output Format

```
CURSED SPEECH — [first 60 chars of statement...]
─────────────────────────────────────────────

PROMPT BLOCK
============

[1. Role]
system: You are a [...] expert specializing in [...].

[2. Context]
[one paragraph explaining why the task matters]

[3. Longform data]
<documents>
  <document index="1">
    <source>[name/path]</source>
    <document_content>
      [content or placeholder]
    </document_content>
  </document>
  [...]
</documents>

[4. Examples]
<examples>
  <example>
    <input>[representative input]</input>
    <output>[desired output]</output>
  </example>
  [3-5 examples covering edge cases]
</examples>

[5. Instructions]
1. [step]
2. [step]
3. [step]
[...]

[6. Output format]
Place your answer in <answer> tags. [Any structural requirements.]

[7. Self-check]
Before finishing, verify:
- [criterion 1]
- [criterion 2]

============
RECOMMENDED EFFORT: [low | medium | high | xhigh | max]
RECOMMENDED ARCHON SKILLS:
  - [skill-name] (domain) — [one-line rationale]
  - [skill-name] (domain) — [one-line rationale]
COLLEAGUE-TEST RESULT: [pass | fail with axis]
```

### Output Contract for `six-eyes`

Phase 5, audience=LLM:
- Return the full prompt block above
- Plus metadata: effort level, skill recommendations, colleague-test result
- If colleague-test fails, route back to `statement-grader` for re-scoring on specificity and audience-fit

## Failure Modes

| Failure | Response |
|---|---|
| Input statement unaudited | Return "deferred — run statement-grader first" |
| Audience tag is not `LLM` | Return "wrong skill — route to bluf-shaper / scqa-formatter / executive-distiller" |
| Downstream task is unspecified | Ask for it; cursed-speech needs to know what Claude should DO with the prompt |
| No examples available for the task | Output a 3–5 placeholder structure with `<example>[CONSTRUCT FROM TASK]</example>` and flag in metadata that examples need to be added before execution |
| Static map AND runtime search return nothing | Output "no skill recommendations" — don't fabricate |
| Anthropic's prompting canon has been updated (e.g., new model, deprecated technique) | The reference doc cites the canonical URL; read it directly. Cursed-speech's structure may need a tweak |

## Scope Boundaries

- **cursed-speech handles:** assembling the canonical 7-component prompt block; effort recommendation; Archon skill recommendation.
- **cursed-speech does NOT:** execute the prompt (that's the user's downstream call); guarantee Claude will do what the prompt asks (it guarantees the prompt is well-formed); decide which Claude model to use (recommend, but the user's deployment chooses).

## Connections

- `cursed-speech-foundations` (vault — `skill-lab/`) — empirical foundations for the canonical order
- `statement-grader` (binding-vow) — required upstream gate; cursed-speech only accepts graded statements
- `audience-classifier` (binding-vow, future) — sets the LLM audience tag that routes to this skill
- `bluf-shaper`, `scqa-formatter`, `executive-distiller` (binding-vow) — siblings for non-LLM audiences
- `growth-architect` (neocortex) — designated maintainer of the static skill-recommendation map (see `references/skill-recommendation-map.md`)
- `mcp__skill-library__search_skills` — runtime call for fresh skill recommendations

## Sources

- Anthropic — [Prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices) (canonical, current)
- Anthropic — [Prompt engineering overview](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview)
- Zhou et al. 2022 — [Least-to-Most Prompting](https://arxiv.org/abs/2205.10625) (empirical anchor for decomposition)
- See [[cursed-speech-foundations]] for the full distillation
