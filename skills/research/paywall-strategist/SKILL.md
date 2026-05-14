---
name: paywall-strategist
description: >
  Systematically work around source paywalls before tagging a claim Unverifiable. Searches for
  preprint mirrors (bioRxiv, SSRN, arXiv, institutional repositories), extracts available
  abstracts, surfaces adjacent open-access work, and generates ask-the-author email templates.
  Plugged into Spelunker's Reentry Protocol Level 1 — must be exhausted before escalating to
  Level 2 (decompose further) or tagging the claim Unverifiable.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Write WebSearch WebFetch
---

# Paywall Strategist — The Access Negotiator

Half the high-quality biotech literature is paywalled. The same is true for legal databases, financial research, and many institutional reports. Tagging "Unverifiable — paywalled" without first checking for legitimate open-access mirrors is lazy research and violates Guiding Principle #4 (trace to primary sources).

This skill exists so Spelunker can honestly say "I tried these specific avenues" before giving up.

## Guiding Principles

1. **Open-access first.** Most published research has a legitimate open mirror. Find it before declaring defeat.
2. **Use legal channels only.** No Sci-Hub, no Library Genesis, no shadow libraries. The skill helps users find papers they can legitimately access; it does not bypass copyright.
3. **An abstract is a partial source, not a non-source.** A well-extracted abstract often answers ~70% of the verification question.
4. **Ask the author when stuck.** Most academic authors will share their own paper on request. The cost is one email.

## How to Run

### Input

From the Spelunker orchestrator (typically via source-triangulator hitting a paywall):
- The paywalled URL or DOI
- The atomic claim being verified
- Optional: the user's institutional affiliation (some users have library access we should suggest)

### Steps

#### Step 1 — Identify the Source

Extract the canonical identifier:
- DOI → use as primary key (DOIs resolve to authoritative metadata)
- arXiv ID, SSRN ID, NBER number → use as primary key
- URL only → fetch the page, extract title/authors/year, then search for canonical IDs

Record: title, authors, year, journal/venue, DOI (if any).

#### Step 2 — Search Open-Access Mirrors

Run these searches in order. Stop at the first hit, but record what was tried.

**For biomedical/life-sciences claims:**
1. `unpaywall.org/<DOI>` — checks ~30M open-access copies
2. `europepmc.org/article/MED/<PMID>` — Europe PMC mirrors many NIH-funded papers
3. `biorxiv.org` / `medrxiv.org` search by title — preprints often free
4. `pubmedcentral.gov` (PMC) — NIH open-access archive
5. Author's institutional repository (search "<author last name> <university> repository")

**For finance/economics claims:**
1. `ssrn.com` search by title — most working papers are free
2. `nber.org/papers` — NBER working papers
3. `repec.org` (RePEc) — economics archive
4. Federal Reserve / IMF / World Bank publication search if the paper is policy-adjacent

**For tech/CS/AI claims:**
1. `arxiv.org` search by title or author
2. `semanticscholar.org` — often surfaces the open PDF in the right sidebar
3. `paperswithcode.com` — for ML papers, may have the PDF link
4. Author's personal page or GitHub Pages site

**For all domains:**
1. `Google Scholar` for the title — the right-side "[PDF]" link is the legal open copy when present
2. `OpenAlex` (api.openalex.org/works/doi:<DOI>) — returns `open_access.is_oa` and `oa_url` when available

#### Step 3 — Extract What's Available

Even when the full text remains paywalled:
1. Fetch and extract the **abstract** — almost always free.
2. Extract the **figures and tables** if available via the publisher's "free preview" mode.
3. Extract the **methods section** if the journal uses methods-open-access (some Nature/Science articles do).
4. Note the **citations to/from** this work via OpenCitations or Semantic Scholar — adjacent open-access papers may discuss the same claim.

#### Step 4 — Find Adjacent Open-Access Work

Search for:
- Preprints by the same authors on the same topic (often a non-paywalled draft of the same finding)
- Systematic reviews or meta-analyses that include this paper (the review's discussion summarizes the finding)
- Conference papers vs. journal papers — if the journal is paywalled, the conference version may be free
- Replication studies (e.g., on osf.io)

These are not substitutes for the original, but they may corroborate or contextualize.

#### Step 5 — Generate Ask-the-Author Template

If the paper truly cannot be accessed and the claim is critical, generate a polite request the user can send to the corresponding author. Template:

```
Subject: Request for PDF — "<paper title>"

Dear Dr. <last name>,

I'm researching <one-sentence claim/topic> and your paper "<title>" (<journal>, <year>) appears to be the most directly relevant primary source. The published version is behind a paywall I don't currently have access to.

Would you be willing to share a copy of the manuscript? I'm happy to share what I'm working on if helpful.

Thank you for considering,
<user name>
```

Surface the corresponding author's email (usually in the abstract or first page of the paper, or on their institutional page).

### Output

```
PAYWALL STRATEGIST RESULT
─────────────────────────
Original source: <title>, <authors>, <year>, DOI: <doi>

Open-access mirror found: yes | no
  If yes: <URL>, mirror type (preprint / institutional / OA journal / unpaywall)
  If no: searched [list of mirrors], none available

Available extractions:
  - Abstract: [text or "not extracted"]
  - Methods: [text or "not extracted"]
  - Figures/tables: [N extracted, or "not available"]

Adjacent open-access work:
  - [Title] (citation): [why relevant — same authors / cites this / replication / etc.]
  - ...

Author contact (if needed):
  - Corresponding: <name>, <email>
  - Email template: see above

RECOMMENDATION:
  [verifiable_from_extractions | partially_verifiable_from_adjacent | author_outreach_recommended | truly_unverifiable]
```

If the claim is verifiable from the extractions or adjacent work, hand back to source-triangulator with the new evidence so the bundle can be updated. If author outreach is the only path, the orchestrator should escalate to Reentry Protocol Level 4 (user assist).

## Error Handling

**DOI doesn't resolve:** The paper may have been retracted or merged. Check `retractionwatch.com` and surface this — a retracted source is itself important evidence.

**Unpaywall / OpenAlex API down:** Fall back to manual Google Scholar search.

**No open mirror exists, no adjacent work, no author contact:** Hand back to Spelunker with `truly_unverifiable` recommendation. Document everything tried so the Gaps section is honest.

## Scope Boundaries

**Does NOT:** Bypass paywalls illegally. No Sci-Hub, no shared institutional credentials, no "12ft.io"-style scrapers.
**Does NOT:** Replace primary access. If a claim is critical, the user should still try to access the paper directly through their institution.
**Does NOT:** Vouch for preprints' rigor. Preprints lack peer review and should be tagged accordingly in the evidence bundle.
