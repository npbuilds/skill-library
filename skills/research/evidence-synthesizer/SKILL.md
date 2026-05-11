---
name: evidence-synthesizer
description: >
  Assemble verified evidence bundles into a structured research brief with confidence-tagged
  findings, evidence maps, and explicit gap reporting. Use when atomic claims have been
  investigated and need to be synthesized into a coherent, honest, user-facing research
  output with auditable confidence assessments.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Write
---

# Evidence Synthesizer — The Assembler

Take the evidence bundles from source-triangulator and weave them into a single research brief that is both scannable and auditable. Every finding gets a confidence tag. Every gap gets named. The user should be able to read the Key Findings in 30 seconds or trace any claim back to its source chain in 3 minutes.

## How to Run

### Input

From the Spelunker orchestrator:
- All evidence bundles from source-triangulator (one per atomic claim)
- The original question and claim decomposition from claim-decomposer
- The depth mode used for this investigation (quick / standard / deep) — required for overall confidence assessment
- The confidence framework (read `../spelunker/references/confidence-framework.md`)

### Steps

#### Step 1 — Finalize Confidence Tags

Review each evidence bundle's preliminary confidence tag against the confidence framework criteria:

1. **Verify tag criteria are strictly met.** The triangulator assigns preliminary tags — the synthesizer is the quality gate.
2. **Respect confidence ceilings.** If the triangulator flagged a ceiling (from upstream dependencies), enforce it. A claim's final tag cannot exceed its ceiling.
3. **Apply aggregation rules.** If the overall conclusion depends on multiple claims, the conclusion's confidence cannot exceed the weakest critical claim. Use the decomposer's priority field to identify which claims are critical (load-bearing) vs. supporting vs. contextual.
4. **Check for cross-claim interactions.** Does evidence from one claim affect the confidence of another? (e.g., if a premise is downgraded, conclusions depending on it must also be downgraded)
5. **Document the reasoning.** Every tag gets a because-clause: "Tagged [level] because [specific criteria met/not met, with evidence counts]."

**Post-adversarial re-assessment:** The synthesizer may be called a second time after Phase 5 (adversarial pass) downgrades claims. When re-invoked:
- Accept the updated confidence tags
- Re-run the overall confidence assessment (Step 4)
- Update the evidence map to reflect adversarial findings
- Add a "Post-Adversarial Changes" note documenting what changed and why

#### Step 2 — Build the Evidence Map

Construct the provenance chain for each finding:

```
Finding → Atomic Claim → Evidence → Source

Example:
"Creatine is safe for long-term use in healthy adults"
  ← Claim #2: Creatine monohydrate is safe at 5g/day for 1+ years
    ← Evidence: 3 independent sources agree
      ← Source A: [Study, Tier 1, 2019]
      ← Source B: [Meta-analysis, Tier 1, 2021]
      ← Source C: [Institutional review, Tier 1, 2023]
    ← Independence verified: Different research groups, different methodologies
    ← Adversarial check: No credible contradicting evidence found
  → Confidence: Confirmed
```

The evidence map must be traceable — any reader should be able to follow from the finding back to the original source.

#### Step 3 — Compile Gaps and Limitations

Aggregate all limitations from the evidence bundles into a single section:

**Categories of gaps:**

1. **Unanswered claims** — atomic claims that could not be verified (tagged Unverifiable)
2. **Access limitations** — paywalled sources, inaccessible databases, rate-limited tools
3. **Evidence quality gaps** — claims where only low-tier sources were available
4. **Scope limitations** — aspects of the original question that fell outside available evidence
5. **Temporal limitations** — evidence that may be outdated, or rapidly evolving areas where currency is uncertain
6. **Tool limitations** — specific capabilities that were unavailable (e.g., no access to specialized databases)

**For each gap, state:**
- What is missing
- Why it matters (how would it change the conclusion if the gap were filled?)
- What would resolve it (a specific database, study type, or expert consultation)

#### Step 4 — Assess Overall Confidence

Synthesize a meta-assessment of the investigation quality:

- How many claims were Confirmed vs. Likely vs. Speculative vs. Contested vs. Unverifiable?
- Did the adversarial self-check find significant counterevidence?
- Were there significant access or tool limitations?
- **What depth mode was used?** (This caps the overall confidence — see below)
- How confident should the user be in acting on these findings?

**Overall confidence levels:**
- **High confidence:** Majority of critical claims are Confirmed, no Contested claims, adversarial check passed. **Requires standard or deep mode.** Quick mode cannot achieve High confidence regardless of claim tags.
- **Moderate confidence:** Mix of Confirmed and Likely, no unresolved Contested claims, minor gaps. This is the ceiling for quick-mode investigations.
- **Low confidence:** Critical claims are Speculative or Contested, significant gaps, limited source access
- **Insufficient evidence:** Too many Unverifiable claims to draw a conclusion — state this clearly rather than forcing an answer

**Depth-mode qualifier:** Include the depth-mode qualifier from the confidence framework in the brief header. The user must always know whether adversarial verification was performed.

#### Step 5 — Format the Research Brief

Read `references/synthesis-templates.md` for the exact output format.

Assemble the final output with these sections in order:

1. **Header** — Question, depth mode, date
2. **Key Findings** — The scannable summary (30-second read)
3. **Detailed Findings** — Each claim with full evidence chain (3-minute deep dive)
4. **Evidence Map** — Visual provenance chains
5. **Gaps & Limitations** — What wasn't found and why it matters
6. **Confidence Summary** — Aggregate assessment
7. **Sources** — Ranked by relevance and authority
8. **Next Steps** — What to investigate further if the user needs more

#### Step 6 — Persistence (optional)

If the user wants this output persisted to their Obsidian vault, call `vault-writer` (`infrastructure/vault-writer`) with the brief as a `type: note` artifact and the relevant `target_domain`, `slug`, and `tags`. Pass `companion_source_path` if the full output should also be archived to `Raw/`. The vault-writer integrity report will list any unresolved wikilinks the caller should address (either by linking to existing notes or by leaving as known skill-library refs). When invoked standalone (not from spelunker), the synthesizer can call vault-writer directly.

### Output

A complete research brief formatted per `references/synthesis-templates.md`. The brief is self-contained — a reader should be able to understand the findings, assess their reliability, and identify what remains unknown without needing any additional context.

## Error Handling

**All claims are Unverifiable:** Do not produce a research brief with false conclusions. State clearly that the available tools and sources are insufficient to answer the question. Suggest alternative approaches (specific databases, expert consultation, primary research).

**Evidence bundles are inconsistent:** If the triangulator's evidence bundles contain internal contradictions (supporting the claim in one search, contradicting it in another), flag this as Contested rather than silently resolving it.

**Original question cannot be answered from the evidence:** State this explicitly. The evidence may answer a related but different question — present what CAN be concluded, clearly distinguish it from the original question, and identify the gap.

**Depth mode was insufficient:** If synthesis reveals the topic is more complex than the selected depth mode can handle, recommend the user re-run at a deeper level. Note which specific claims need more investigation.
