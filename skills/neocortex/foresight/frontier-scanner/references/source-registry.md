# Frontier Scanner — Source Registry

Curated sources for AI frontier scanning, organized by signal type. Primary sources produce original information; secondary sources provide analysis and context. Always prefer primary over secondary.

## Tier 1 — Primary Sources (Check Every Scan)

These are where developments are announced first. Non-negotiable.

### Model Labs & Releases
| Source | URL | Signal Type |
|--------|-----|-------------|
| Anthropic Blog | anthropic.com/blog | Claude releases, safety research, capability reports |
| OpenAI Blog | openai.com/blog | GPT releases, API changes, research papers |
| Google DeepMind Blog | deepmind.google/blog | Gemini releases, research breakthroughs |
| Meta AI Blog | ai.meta.com/blog | Llama releases, open-source model research |
| Hugging Face Trending | huggingface.co/models (sort by trending) | Open-source model releases, community momentum |

### Tool Ecosystem
| Source | URL | Signal Type |
|--------|-----|-------------|
| Claude Code Changelog | docs.anthropic.com/en/docs/claude-code | MCP changes, SDK updates, new capabilities |
| MCP Server Registry | github.com/modelcontextprotocol | New integrations, protocol changes |
| Anthropic Agent SDK | github.com/anthropics/agent-sdk | Agent framework patterns, new primitives |

## Tier 2 — High-Signal Analysis (Check Weekly)

These filter noise into insight. Use for context and pattern detection.

### Practitioner Blogs
| Source | Signal Type |
|--------|-------------|
| Simon Willison (simonwillison.net) | Practical AI tool analysis, LLM capability testing |
| Latent Space (latent.space) | AI engineering trends, practitioner interviews |
| The Gradient (thegradient.pub) | Academic-practitioner bridge, research summaries |

### Research Feeds
| Source | Signal Type |
|--------|-------------|
| arXiv cs.AI + cs.CL (daily digest) | Breakthrough papers, new techniques |
| Papers With Code (paperswithcode.com) | Benchmarks, SOTA tracking, method trends |
| Hugging Face Daily Papers (huggingface.co/papers) | Community-curated important papers |

## Tier 3 — Domain-Specific (Check When Relevant)

Cross-reference against library domains when developments touch these areas.

| Domain | Sources to Watch |
|--------|-----------------|
| AI + Investing | Bloomberg AI coverage, QuantConnect blog, Alpaca API changelog |
| AI + Writing | Sudowrite blog, major publisher AI policies, Authors Guild statements |
| AI + Data Science | Kaggle trending, MLflow/Weights & Biases releases, dbt changelog |
| AI + Design | Figma AI features, Adobe Firefly updates, design tool AI integrations |
| AI + Game Theory | DeepMind game-playing research, multi-agent RL papers |
| AI + Wine/Food | Vivino AI features, flavor prediction research, food-tech AI |

## Anti-Sources (Never Cite)

These generate noise, not signal. Skip them even if they appear in search results.

- Hype aggregators that rewrite press releases without analysis
- "Top 10 AI tools" listicles
- LinkedIn thought leadership posts without primary data
- Crypto/Web3 projects rebranding as "AI"
- Paywalled analyst reports that only offer previews (note as inaccessible, don't speculate on contents)

## Scan Protocol

### Quick Scan (weekly scheduled task)
1. Check all Tier 1 primary sources for new announcements
2. Skim Tier 2 practitioner blogs for pattern synthesis
3. Cross-reference any development against library domains using Tier 3

### Deep Scan (on-demand, triggered by [ACTION NEEDED] flags)
1. All of the above, plus:
2. Use spelunker methodology: decompose the development into claims, triangulate across sources, run adversarial pass
3. Trace claims to primary sources (release notes, papers, benchmarks) — not secondary coverage
4. Apply confidence tags from spelunker's framework: Confirmed / Likely / Speculative / Contested / Unverifiable

### Adversarial Layer (borrowed from spelunker Phase 5)
For every significant development:
- Search for "[development] problems", "[development] limitations", "[development] criticism"
- Check if benchmarks are cherry-picked or self-reported vs. independently verified
- Look for what the announcement does NOT say (capability gaps, missing comparisons)
- If a capability claim has no independent verification, tag it Speculative regardless of source prestige
