---
name: source-triangulator
description: >
  Verify individual claims by finding and cross-referencing multiple independent sources.
  Use when an atomic claim needs evidence gathering, source quality evaluation, independence
  verification, and agreement/disagreement mapping. The core verification engine of the
  Spelunker research system.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Write WebSearch WebFetch PubMed ClinicalTrials GoogleDrive
---

# Source Triangulator — The Verifier

Take a single atomic claim and build an evidence bundle around it. Search from multiple angles, evaluate what you find, check whether sources are genuinely independent, and map where they agree and disagree.

The triangulator fights confirmation bias by design: it does not stop at the first supporting source, it checks independence, and it maps disagreements rather than ignoring them.

## How to Run

### Input

From the Spelunker orchestrator (via claim-decomposer):
- One atomic claim to verify
- Claim type (factual, causal, comparative, predictive, definitional, existential, evaluative)
- Claim domain (biomedical, technical, business/financial, etc.) — determines which tools to use
- Claim priority (critical / supporting / contextual) — affects depth allocation
- Depth mode (quick / standard / deep)
- Upstream dependency results (if this claim depends on another):
  - Upstream claim ID, text, and confidence tag
  - **Confidence ceiling rule:** This claim's final confidence cannot exceed its weakest upstream dependency. If the upstream claim is Speculative, this claim is at most Speculative, regardless of how strong its own evidence is.

### Steps

#### Step 1 — Search Strategy Selection

Based on claim type and domain, select search approaches. Read `references/source-evaluation.md` for the full evaluation framework.

**Minimum searches per atomic claim by depth mode:**

Note: These counts are PER CLAIM, not per investigation. The orchestrator's source targets (e.g., "10+ sources" for standard) refer to the total across all claims in the investigation.

| Mode | Direct Queries | Lateral Queries | Domain-Specific | Adversarial |
|------|---------------|-----------------|-----------------|-------------|
| quick | 1 | 0 | 0-1 | 0 |
| standard | 2 | 1 | 1 | 1 |
| deep | 3 | 2 | 2 | 2 |

**Search approach selection by claim type:**

| Claim Type | Primary Approach | Secondary Approach |
|-----------|-----------------|-------------------|
| Factual | Direct search for the specific fact | Authority search (who would have this data?) |
| Causal | Search for studies/experiments testing causation | Search for mechanism explanations |
| Comparative | Search for head-to-head comparisons, benchmarks | Search each side independently |
| Predictive | Search for forecasts, models, expert predictions | Search for base rates and historical precedents |
| Definitional | Search authoritative definitions (standards bodies, textbooks) | Search for usage patterns |
| Existential | Search for direct records or documentation | Search for absence evidence |
| Evaluative | Search for established criteria, standards, expert assessments | Search for outcome-based evidence and alternative evaluations |

#### Step 2 — Execute Searches

Run searches using the selected strategies and tools:

1. **Direct search** — query the claim as stated. Use WebSearch for general topics. Use PubMed for biomedical claims. Use domain-specific tools as indicated by the routing table.

2. **Lateral search** — rephrase the claim using different terminology, search for related concepts that would mention this claim in passing, or search for the likely primary source directly.

3. **Domain-specific search** — use specialized tools (PubMed for medical, ClinicalTrials for drug efficacy, etc.)

4. **Adversarial search** (standard and deep only) — search for the negation or contradiction of the claim. "X does not work", "problems with X", "X debunked", "criticism of X".

For each search, record:
- The exact query used
- The tool used
- Number of results examined
- Which results were selected for evaluation and why

#### Step 3 — Source Evaluation

For each source found, evaluate using the framework in `references/source-evaluation.md`:

**Quick evaluation (all sources):**
- **Authority**: Who produced this? What is their expertise and credibility in this domain?
- **Recency**: Capture the publication date for EVERY source (YYYY-MM-DD if available, YYYY-MM otherwise, YYYY as last resort). If the source has no discoverable date, mark `date: unknown` and treat it as Tier 4 regardless of authority — undated sources cannot anchor a confidence tag because we can't tell if they've been superseded. Apply the recency rule below.
- **Source type**: Peer-reviewed study / institutional report / news article / blog / social media / other

**Recency rule (REQUIRED in standard and deep modes, advisory in quick mode):**

After all sources for a claim are dated, compute the median source age (months from today). Compare against the domain-specific staleness threshold:

| Claim domain | Staleness threshold | Why |
|--------------|--------------------|-----|
| Markets / finance / crypto | 18 months | Fast-moving microstructure, regime changes |
| Tech / AI / software | 18 months | Capabilities and best practices shift fast |
| Biotech / pharma / clinical trials | 36 months | Approvals, retractions, and meta-analyses iterate |
| Regulatory / legal | 24 months | Rulings and guidance evolve |
| Social / political | 24 months | Polling, sentiment, public positions shift |
| Foundational science / physics / math | 60 months | Stable, but watch for paradigm-shifting work |
| Historical / definitional | No threshold | Historical facts don't expire |

**If the median source age exceeds the threshold:**
1. Append a `Recency warning: median source age = N months, threshold = M months for [domain]` line to the evidence bundle.
2. Downgrade preliminary confidence by one tier (Confirmed → Likely, Likely → Speculative). Document the downgrade.
3. Note in Limitations: "Best available evidence is older than the freshness threshold for this domain. A current systematic review or recent primary source would be needed to upgrade confidence."

**Exception:** If the claim is explicitly historical ("What did regulators say in 2018?"), staleness is irrelevant — note the exception and skip the downgrade.

**Deep evaluation (standard and deep modes):**
- **Methodology**: For studies — was the methodology appropriate? Sample size? Controls?
- **Bias indicators**: Funding sources, organizational affiliation, known advocacy positions
- **Upstream sources**: Does this source cite its own sources? Can we trace the chain?
- **Scope match**: Does the source actually address the specific claim, or just a related topic?

Assign a quality tier to each source:
- **Tier 1**: Peer-reviewed research, official government data, established reference works
- **Tier 2**: Institutional reports, reputable news with cited sources, expert commentary
- **Tier 3**: News without citations, industry reports, well-established blogs
- **Tier 4**: Unsourced blogs, social media, opinion pieces, anonymous content

#### Step 4 — Independence Verification

**This is where most research goes wrong.** Check whether sources are genuinely independent:

1. **Citation chain check**: Do two sources cite the same upstream study or report? If yes, they are ONE source, not two.
2. **Wire service check**: Do news articles share identical phrasing? They likely come from the same wire service (AP, Reuters).
3. **Common author check**: Are the authors connected (same lab, same institution, co-authors on other work)?
4. **Temporal check**: Did all sources appear after a single event (a press release, a viral post)? They may all derive from that single origin.

After independence verification, count truly independent sources:
- 3+ independent → eligible for Confirmed
- 2 independent → eligible for Likely
- 1 or no independence → Speculative at best

#### Step 5 — Agreement/Disagreement Mapping

Map how sources relate to each other:

```
EVIDENCE MAP: [Claim text]
─────────────────────────────
Supporting (agree with claim):
  Source A [Tier 1] — [key finding]
  Source B [Tier 2] — [key finding]
  Independence: A and B are independent ✓ / share upstream ✗

Contradicting (disagree with claim):
  Source C [Tier 1] — [contradicting finding]
  Independence from supporting sources: ✓

Tangential (related but don't directly address):
  Source D [Tier 2] — [what it says and why it's relevant]

Not found:
  [What would constitute strong evidence but could not be located]
```

#### Step 6 — Assign Preliminary Confidence

Using the evidence map, assign a preliminary confidence tag following the criteria in `../spelunker/references/confidence-framework.md`:

- Count independent supporting sources by tier
- Count independent contradicting sources by tier
- Apply the confidence criteria strictly
- Document the reasoning: "Tagged as [level] because [specific criteria met/not met]"

### Output

An evidence bundle containing:

```
EVIDENCE BUNDLE: [Claim text]
───────────────────────────────
Claim type: [factual/causal/etc.]
Claim domain: [domain]
Claim priority: [critical/supporting/contextual]
Searches conducted: [N] queries across [tools used]
Sources found: [N] total, [M] independent
Evidence-based confidence: [tag] — because [reasoning]
Confidence ceiling: [tag if capped by upstream dependency, otherwise "none"]
Preliminary confidence: [the lower of evidence-based and ceiling] — because [reasoning]

Evidence map: [as structured in Step 5]

Source details:
  1. [Source title/URL] — Tier [N] — [1-sentence summary of relevance]
  2. ...

Limitations:
  - [Any searches that failed, sources that were inaccessible, tools that couldn't be used]

Emergent questions:
  - [Any new questions or claims that surfaced during investigation]
```

## Error Handling

**No sources found at all:** Return Unverifiable tag. List all queries attempted and tools used. Suggest alternative approaches (different keywords, adjacent topics, specific databases).

**All sources are Tier 3-4:** Return Speculative tag. Note the evidence quality gap. Suggest where higher-quality sources might exist (specific journals, databases, institutions).

**Sources contradict each other:** Do NOT pick a winner. Return Contested tag. Map the disagreement clearly. Note the quality of evidence on each side. Identify what would resolve the disagreement.

**Primary source is behind a paywall:** Note this explicitly in Limitations. Report what the abstract/preview reveals. Suggest the user access it directly if the claim is critical.

**Search results are overwhelming (50+ hits):** Focus on the highest-quality sources (Tier 1-2 first). For quick mode, stop at 5 evaluated sources. For deep mode, evaluate up to 15.
