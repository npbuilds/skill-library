# Cursed Speech — Quick Reference


## Quick Reference

| # | Component | Shape | Purpose |
|---|---|---|---|
| 1 | **Role assignment** | `system: "You are a [domain] expert..."` | Steers tone and scope |
| 2 | **Context / motivation** | One paragraph; explain *why* the task matters | Claude generalizes from explanation |
| 3 | **Longform data** | `<documents><document index="n"><source/><document_content/></document></documents>` | Place ABOVE the query — this is the 30% win |
| 4 | **Examples** | `<examples><example>...</example></examples>` (3–5) | Shape output format and tone; cover edge cases |
| 5 | **Instructions** | Numbered list when order matters | Sequential steps |
| 6 | **Output format** | "Place your answer in `<answer>` tags" — tell Claude what TO do, not what NOT to do | Makes output parseable downstream |
| 7 | **Self-check** | "Before you finish, verify your answer against [criteria]" | Catches errors reliably for coding/math/structured analysis |

## Quick Reference

| Task type | Recommended effort |
|---|---|
| Coding, agentic loops, multi-step tool use | **xhigh** |
| Knowledge work, vision, memory tasks, intelligence-sensitive | **high** (minimum for these) |
| Cost-sensitive but still needs reasoning | **medium** |
| Short scoped tasks, latency-sensitive, simple lookups | **low** |
| Maximum capability, willing to pay for diminishing returns | **max** (test before defaulting) |

## Failure Modes

| Failure | Response |
|---|---|
| Input statement unaudited | Return "deferred — run statement-grader first" |
| Audience tag is not `LLM` | Return "wrong skill — route to bluf-shaper / scqa-formatter / executive-distiller" |
| Downstream task is unspecified | Ask for it; cursed-speech needs to know what Claude should DO with the prompt |
| No examples available for the task | Output a 3–5 placeholder structure with `<example>[CONSTRUCT FROM TASK]</example>` and flag in metadata that examples need to be added before execution |
| Static map AND runtime search return nothing | Output "no skill recommendations" — don't fabricate |
| Anthropic's prompting canon has been updated (e.g., new model, deprecated technique) | The reference doc cites the canonical URL; read it directly. Cursed-speech's structure may need a tweak |
