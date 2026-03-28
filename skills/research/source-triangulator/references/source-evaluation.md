# Source Evaluation Framework

A systematic approach to evaluating source quality. Every source the triangulator encounters gets scored on these dimensions.

## Source Type Hierarchy

Ordered by default authority (can be overridden by domain-specific considerations):

### Tier 1 — Primary Authoritative Sources
- **Peer-reviewed research** (published in indexed journals)
- **Systematic reviews and meta-analyses** (strongest form of evidence aggregation)
- **Official government data** (census, regulatory filings, agency reports)
- **Court records and legal filings** (primary legal documents)
- **Raw datasets from authoritative institutions** (WHO, CDC, World Bank)
- **Established reference works** (medical textbooks, engineering handbooks, legal treatises)

**When to trust Tier 1:** Almost always, but still check methodology for studies, and recency for reference works. Even peer-reviewed papers can be retracted, have small samples, or have methodological issues.

### Tier 2 — Authoritative Secondary Sources
- **Institutional reports** (think tanks, research organizations, industry bodies)
- **Reputable journalism with cited sources** (major outlets with editorial standards)
- **Expert commentary and analysis** (identified domain experts writing in their field)
- **Conference proceedings and preprints** (academic but not yet peer-reviewed)
- **Official organizational communications** (press releases, annual reports)

**When to trust Tier 2:** Generally reliable, but trace claims back to primary sources when possible. Institutional bias is common — check the organization's mission and funding.

### Tier 3 — General Sources
- **News articles without explicit citations** (reporting without linking to primary sources)
- **Industry reports from commercial entities** (may have sales incentive)
- **Well-established blogs with track records** (domain-specific, author is known)
- **Wikipedia** (useful as a starting point, NOT as a citation — follow Wikipedia's own citations)
- **Encyclopedic reference sites** (Britannica, specialized wikis with editorial oversight)

**When to trust Tier 3:** For context and leads, not for final evidence. Always trace interesting claims from Tier 3 sources back to their cited origins.

### Tier 4 — Unreliable or Unverifiable Sources
- **Unsourced blog posts** (no citations, no identified expertise)
- **Social media posts** (regardless of follower count)
- **Anonymous content** (forums, anonymous reviews)
- **Content marketing** (articles designed to sell a product or service)
- **Self-published material without peer review** (vanity press, personal sites)

**When to trust Tier 4:** Almost never as evidence. Can be useful for identifying what claims are circulating, but the claims themselves need verification from higher-tier sources.

## Evaluation Dimensions

### Authority
- Who wrote/produced this? What is their domain expertise?
- Is the publishing venue reputable? (journal impact factor, editorial board, organizational standing)
- Has the author published other work in this area?
- **Red flags:** Anonymous authors, self-published with no credentials, expertise mismatch (a computer scientist opining on virology)

### Recency
- When was this produced?
- Is the information time-sensitive? (technology changes fast, geological facts don't)
- Has this been superseded by newer work?
- **Rule of thumb:** For rapidly evolving fields (AI, policy, markets), prefer sources < 2 years old. For established science, older landmark papers may be more authoritative than recent work.

### Methodology (for research sources)
- Was the study design appropriate for the question? (RCT for causation, cohort for correlation)
- Sample size: Is it large enough to detect the claimed effect?
- Controls: Were confounding variables addressed?
- Statistical analysis: Are the methods appropriate? P-values, confidence intervals, effect sizes reported?
- Reproducibility: Has the finding been replicated?
- **Red flags:** Very small samples (< 30 for most studies), no control group, p-hacking indicators (p = 0.049), cherry-picked time periods

### Bias Assessment
- **Funding bias:** Who paid for this research? Industry-funded studies tend to favor the funder's product.
- **Organizational bias:** Does the source organization have a known position on this topic?
- **Selection bias:** Is the source presenting a balanced view or cherry-picking evidence?
- **Survivorship bias:** Are only successful cases being discussed?
- **Publication bias:** Negative results are less likely to be published. Absence of negative studies does not mean absence of negative effects.

### Independence Check
- Does this source cite its own original research/data, or does it rely on other sources?
- If it relies on other sources, who are they? (trace the citation chain)
- Is this source part of a citation cluster? (multiple papers from the same research group)
- **The wire service test:** If two news articles say the same thing, check if they're both quoting the same wire service (AP, Reuters, AFP)
- **The press release test:** If multiple sources make the same claim simultaneously, check if a press release triggered them all

## Domain-Specific Adjustments

### Biomedical
- Evidence hierarchy: Systematic review > RCT > cohort study > case-control > case report > expert opinion
- Check for conflicts of interest (pharma funding, consulting relationships)
- Verify study registration (ClinicalTrials.gov) — unregistered trials are suspect
- Retraction Watch: check if key studies have been retracted

### Technology
- Documentation and official specs outweigh blog posts
- GitHub stars and adoption metrics provide supplementary evidence
- Benchmark methodology matters — apples-to-apples comparisons only
- Release dates matter — a 2-year-old benchmark may be obsolete

### Business/Financial
- SEC filings > press releases > news articles > analyst reports
- Check for short-seller reports or activist investor positions (bias)
- Distinguish between verified financial data and projections
- Industry analysts have track records — check theirs

### Legal
- Case law > legal commentary > news coverage
- Jurisdiction matters — a ruling in one jurisdiction may not apply elsewhere
- Distinguish between binding precedent and persuasive authority
- Check if cases have been overturned or distinguished

## Quick Evaluation Checklist

For rapid assessment during quick-mode research:

- [ ] Who wrote this? (identifiable, credible)
- [ ] Where is it published? (reputable venue)
- [ ] When was it published? (current enough)
- [ ] Does it cite its sources? (traceable claims)
- [ ] Does the author have a conflict of interest? (bias check)
- [ ] Is there an obvious agenda? (advocacy vs. analysis)
