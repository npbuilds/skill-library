# Domain Routing — Tool Chain Selection

When a research question arrives, route it to the optimal tool chain based on the domain. A question may span multiple domains — use the primary domain for the main investigation and secondary domains for corroboration.

## Domain Detection

Classify by scanning the question for domain signals:

| Domain | Signal Words | Primary Tools | Corroboration Tools |
|--------|-------------|---------------|-------------------|
| Biomedical | disease, drug, treatment, clinical, patient, gene, protein, symptom, diagnosis, FDA, trial, therapy, dosage, side effect | PubMed (search_articles, get_article_metadata), ClinicalTrials MCP (search_trials, get_trial_details) | WebSearch for news, WebFetch for org pages |
| Academic/Scientific | study, research, paper, published, journal, findings, hypothesis, methodology, peer-reviewed | PubMed (if life sciences), WebSearch for preprints/repos, WebFetch for institutional pages | Google Drive for internal docs |
| Business/Financial | company, revenue, market, stock, valuation, acquisition, competitor, SEC, earnings, funding | WebSearch for news and filings, WebFetch for company pages | Google Drive for internal analysis |
| Technical | library, framework, API, documentation, bug, version, release, specification, protocol | WebSearch for docs and repos, WebFetch for official docs | PubMed if CS-adjacent |
| Legal/Regulatory | law, regulation, statute, ruling, compliance, court, jurisdiction, amendment | WebSearch for legal databases and news, WebFetch for gov pages | N/A |
| Current Events | today, recent, latest, breaking, announced, this week, just happened | WebSearch (prioritize recency), WebFetch for source pages | N/A |
| Historical | when did, history of, origin, originally, founded, first | WebSearch, WebFetch for reference sources | PubMed if medical history |
| General/Mixed | (no strong signal) | WebSearch as starting point, refine based on initial results | Expand to domain-specific tools as the topic clarifies |

## Search Strategy by Depth Mode

### Quick Mode (3-5 sources)
- 1 direct WebSearch query
- 1 lateral query (rephrase or broaden)
- Fetch top 2-3 results
- Skip adversarial self-check
- Appropriate for: factual lookups, quick verifications, well-established facts

### Standard Mode (10+ sources, triangulated)
- 2-3 WebSearch queries (direct + lateral + domain-specific)
- Fetch top 5-7 results
- Cross-reference key claims across sources
- 1 adversarial search (search for the opposite claim)
- Appropriate for: research questions, contested topics, important decisions

### Deep Mode (exhaustive, citation-traced)
- 4-6 search queries across multiple strategies
- Fetch 10+ results
- Trace claims to primary sources
- Full adversarial pass (actively search for counterevidence)
- Check temporal validity (is this still current?)
- Appropriate for: high-stakes decisions, academic-grade research, deeply contested topics

## Tool-Specific Guidance

### WebSearch
- Start broad, then narrow based on results
- Always run at least one query with negating terms ("X does NOT" or "problems with X") for adversarial checking
- Check publication dates — prefer recent for current events, authoritative for established facts

### WebFetch
- Use to read full articles when search snippets are insufficient
- Particularly valuable for official documentation, institutional reports, and methodology sections
- Will fail on paywalled content — note this as a limitation, don't silently skip

### PubMed (search_articles, get_article_metadata, get_full_text_article)
- Use for ANY biomedical or life sciences claim
- Prefer systematic reviews and meta-analyses over individual studies
- Check publication type: RCT > cohort study > case report > opinion
- Use find_related_articles to discover adjacent research

### ClinicalTrials MCP (search_trials, get_trial_details, analyze_endpoints)
- Use when claims involve drug efficacy, treatment protocols, or clinical outcomes
- Check trial phase: Phase 3 results > Phase 2 > Phase 1
- Note trial status: COMPLETED with results > RECRUITING > TERMINATED

### Google Drive (google_drive_search, google_drive_fetch)
- Use when the research question may relate to internal documents
- Particularly valuable for corroborating business claims against internal data
- Always note when findings come from internal vs. public sources

## Lateral Search Strategies

When direct searches fail, try:
1. **Synonym expansion** — search for related terms, medical vs. common names, brand vs. generic
2. **Upstream search** — who would have produced this information? Search for the likely source directly
3. **Adjacent search** — search for closely related topics that might mention the target claim in passing
4. **Authority search** — search for known experts or institutions in the field + the topic
5. **Temporal search** — add year constraints to find when information first appeared or last changed
