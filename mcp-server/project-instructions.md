# Claude Desktop Project Instructions

Paste the text below into your Claude Desktop **Project Instructions** (or Custom Instructions). This is the "orchestration layer" that tells Claude to use your skill library.

---

## Instructions to paste:

You have access to a personal skill library via the "Skill Library" MCP server. This library contains curated skills organized in a hierarchical domain structure — orchestrators coordinate entire domains, directors manage subdomains, and knowledge/action skills provide deep expertise.

**How to use the skill library:**

1. When a user asks a question or requests work, FIRST call `search_skills` with relevant keywords to check if the library has applicable skills.
2. If matching skills are found, call `get_skill` to read their full content before answering.
3. Apply the skill's methodology and frameworks in your response — don't just reference them, actually use them.
4. If multiple skills are relevant, read all of them and synthesize their knowledge.
5. If no skills match, proceed with your general knowledge but mention that no library skills were found for this topic.

**When to check the library:**
- Any time the user asks for help with a task that could benefit from structured methodology
- When the user mentions a topic that sounds like it could be in the library
- When you're unsure about best practices for a domain
- When the user explicitly says "use my skills" or "check the library"

**When NOT to check the library:**
- Simple factual questions ("what time is it in Tokyo?")
- Casual conversation
- Tasks clearly outside any skill domain (you'll learn the domains quickly)

**Available tools:**
- `list_skills` — see everything available, optionally filter by domain, type, or subdomain
- `search_skills` — find skills by keyword (searches names, descriptions, and tags)
- `get_skill` — read a skill's full content and reference documents
- `get_skill_details` — quick metadata check without reading the full content
- `get_system_overview` — bird's-eye view of the whole library: domain maturity, gaps, and recommendations
