# Tool Ecosystem — GA Capability Baseline (April 2026)

Living document tracking which Claude platform capabilities are generally available vs. beta. Updated each frontier scan when tool status changes. Skills should reference this to avoid designing around limitations that no longer exist.

## GA Capabilities (production-stable)

### Web Search & Fetch
- **Status:** GA (moved from beta March 2026)
- **Key change:** Tools now auto-write and execute code to filter/process search results *before* they enter the context window. This means:
  - Search results can be deduplicated, sorted, and filtered at the tool layer
  - Skills no longer need to budget context tokens for raw search noise
  - The effective signal density of web search is significantly higher than pre-GA behavior
- **Implication for skills:** Research-oriented skills (spelunker, source-triangulator, research-curator, frontier-scanner) should assume pre-filtered results. Prompt strategies that manually filter search output in-context are now redundant — the tool layer handles first-pass filtering automatically.

### Code Execution
- **Status:** GA
- **Key change:** Free when used with web search or web fetch
- **Implication:** Skills can request computational verification of claims (run calculations, parse data, validate formats) at zero marginal cost when combined with search.

### Programmatic Tool Calling
- **Status:** GA
- **Key change:** Tools can be invoked programmatically, not just conversationally
- **Implication:** Orchestrator skills can chain tool calls more reliably. Multi-step research workflows (search → fetch → parse → verify) can be expressed as deterministic pipelines rather than conversational prompts.

### Tool Search
- **Status:** GA
- **Key change:** Models can discover available tools dynamically
- **Implication:** Skills don't need to hardcode tool names. An orchestrator can discover what tools are available at runtime and adapt its strategy accordingly.

### Memory
- **Status:** GA
- **Key change:** Persistent memory across conversations
- **Implication:** Skills that build cumulative knowledge (research-curator, frontier-scanner scan history) can reference prior findings without re-deriving them.

### MCP Connectors
- **Status:** Expanding (Claude in Excel now supports MCP connectors: S&P Global, FactSet)
- **Implication:** Domain-specific data access is widening. Investing-domain skills may eventually tap financial data feeds directly via MCP rather than web scraping.

## GA with Caveats

### 1M Token Context Window
- **Status:** GA for Opus 4.6 and Sonnet 4.6, but quality caveats remain
- **Key caveat:** Sonnet 4.5 showed 18.5% accuracy at 1M tokens (MRCR benchmark). Anthropic has not published MRCR scores for Sonnet 4.6. Independent testing suggests Sonnet degrades noticeably past ~400K tokens.
- **Practical guidance:**
  - Use 1M for retrieval/indexing tasks (finding needles in haystacks)
  - Do NOT assume reasoning quality holds at 1M — treat reasoning-at-1M as unverified
  - For reasoning-heavy tasks, prefer staying under 200K with better-curated context
  - Opus 4.6 degrades more gracefully than Sonnet at long contexts

## Retired/Deprecated

### 1M Beta Header (Sonnet 4.5 / Sonnet 4)
- **Retiring:** April 30, 2026
- The `context-1m-2025-08-07` beta header will have no effect on Sonnet 4.5 or Sonnet 4 after this date. Requests exceeding 200K will error. Migrate to Sonnet 4.6 or Opus 4.6 for 1M access.

### Claude Haiku 3
- **Retiring:** April 19, 2026
- Migrate to Haiku 4.5.

## How This Affects Scan Methodology

The frontier-scanner's own scanning benefits from these GA changes:
1. **Web search filtering** — Scan queries can request structured extraction (just headlines, dates, capability claims) rather than fetching full blog posts
2. **Code execution** — Can validate benchmark claims computationally during adversarial pass
3. **Tool search** — Future scans can dynamically discover new MCP tools as they appear, without hardcoding source URLs

## Update Protocol

This doc should be updated whenever:
- A capability moves from beta to GA (or vice versa)
- A new tool category becomes available
- A deprecation date passes (move to "Retired" section and eventually remove)
- Quality benchmarks are published that change the practical guidance (especially 1M context MRCR scores)
