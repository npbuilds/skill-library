# Confidence Framework — Epistemic Labeling System

The confidence framework is the spine of every Spelunker output. Every claim in a research brief MUST carry exactly one confidence tag. Tags are not feelings — they are determined by specific, auditable criteria.

## The Five Tiers

### Confirmed

**Tag:** `Confirmed`
**Icon:** checkmark
**Criteria — ALL must be met:**
- 3+ independent sources agree on the substance of the claim
- At least one source is authoritative for the domain (peer-reviewed, official data, institutional report)
- Sources are genuinely independent (not citing each other as primary evidence)
- No credible contradicting sources found

**What "independent" means:** Two news articles citing the same study count as ONE source. The study itself is the source. Two separate studies reaching the same conclusion count as TWO sources.

### Likely

**Tag:** `Likely`
**Icon:** blue circle
**Criteria — ANY of these:**
- 2 independent sources agree, at least one authoritative
- 1 highly authoritative source (landmark study, official government data, established reference work) with no contradicting evidence
- Expert consensus exists but primary evidence is limited

**Upgrade path to Confirmed:** Find one more independent source. Check if existing sources share a common upstream citation.

### Speculative

**Tag:** `Speculative`
**Icon:** yellow circle
**Criteria — ANY of these:**
- Single source only, regardless of quality
- Multiple sources, but all non-authoritative (blogs, opinion pieces, social media)
- Claim is an extrapolation or inference from confirmed data, not directly stated
- Source is authoritative but the claim is tangential to its focus (a passing mention, not the main finding)

**Important:** Speculative does not mean wrong. It means the evidence is insufficient to assign higher confidence. Always state what additional evidence would upgrade the claim.

### Contested

**Tag:** `Contested`
**Icon:** warning triangle
**Criteria — ALL must be met:**
- 2+ credible sources actively disagree on the substance of the claim
- The disagreement is substantive (not just phrasing or emphasis differences)
- Both sides have at least some evidentiary basis

**Handling contested claims:**
1. State the claim as contested upfront
2. Present the strongest version of each position
3. Note the quality of evidence on each side
4. Identify what would resolve the disagreement (a specific study, data point, or methodological question)
5. Never arbitrarily pick a side — that is the user's decision to make

### Unverifiable

**Tag:** `Unverifiable`
**Icon:** question mark
**Criteria — ANY of these:**
- No sources found after exhaustive search (specify what was searched)
- Claim requires access to paywalled, classified, or proprietary data
- Claim is about future events or unknowable states
- Available tools cannot access the necessary databases
- Claim is inherently unfalsifiable

**Critical distinction:**
- "No evidence found" =/= "The claim is false"
- "Unverifiable" means "I cannot check this with available tools and sources"
- Always state WHY it is unverifiable — what would be needed to verify it

## Aggregation Rules

When synthesizing multiple atomic claims into an overall assessment:

- **Overall confidence cannot exceed the weakest critical claim.** If the conclusion depends on a Speculative premise, the conclusion is at most Speculative. Use the claim's priority tag to determine which claims are critical (load-bearing for the conclusion) vs. supporting or contextual.
- **Confirmed + Contested = Contested.** One contested critical element makes the aggregate contested.
- **Multiple Likely claims do NOT aggregate to Confirmed.** Quantity of weak evidence does not equal quality.
- **State the chain explicitly.** "This conclusion is Likely because Claim A is Confirmed but Claim B is only Likely."

## Backpropagation Rules

When a claim's confidence changes (typically during the adversarial pass):

- **Walk the dependency graph downstream.** Every claim that depends on the changed claim must be re-evaluated.
- **Confidence ceiling rule.** A dependent claim's confidence cannot exceed its weakest upstream dependency. If Claim A drops from Confirmed → Contested, Claim C (which depends on A) must drop to at most Contested.
- **Cascade until stable.** If the re-evaluation changes Claim C, check all claims that depend on C.
- **Document every cascade.** "Claim C: Likely → Contested (cascaded from Claim A downgrade)."
- **Re-assess overall confidence.** After all cascades settle, recompute the overall confidence level.

## Depth-Mode Confidence Qualifiers

Confidence tags mean the same thing at every depth — the criteria don't change. But the **rigor of the process** differs, and the user must know this:

| Depth Mode | Adversarial Check | Source Breadth | Qualifier Added to Brief |
|-----------|-------------------|----------------|--------------------------|
| `quick` | Skipped | 3-5 sources | "Quick-mode research — confidence tags reflect available evidence but no adversarial verification was performed. Re-run at standard or deep depth for higher assurance." |
| `standard` | Partial (top 2-3 critical claims) | 10+ sources | None — this is the baseline expectation |
| `deep` | Full (all critical + top supporting) | Exhaustive | "Deep-mode research — full adversarial verification completed." |

**Rules:**
- Tags at quick depth that meet Confirmed criteria are still tagged Confirmed — but the qualifier warns the user that adversarial checking was skipped.
- The overall confidence assessment (synthesizer Step 4) must factor in the depth mode. A quick-mode investigation with all-Confirmed claims gets at most "Moderate confidence" overall (because no adversarial check was run). Only standard and deep modes can achieve "High confidence" overall.
- The depth mode is always stated in the brief header so the reader knows the rigor level.

## Anti-Patterns — What NOT to Do

| Anti-Pattern | Why It's Wrong | Correct Approach |
|-------------|---------------|-----------------|
| Defaulting to Likely when unsure | Masks uncertainty | Use Speculative and state what's missing |
| Treating Wikipedia as authoritative | It's a secondary source | Trace to the cited primary sources |
| Counting news articles as independent | They often share a wire source | Check if they cite the same original report |
| Upgrading confidence because the claim "feels right" | Confirmation bias | Stick to the criteria — evidence counts, not intuition |
| Marking as Confirmed without checking for contradictions | Ignores the "no credible contradicting sources" criterion | Always do an adversarial search |
| Conflating "widely repeated" with "well-evidenced" | Popularity is not evidence | Trace to primary sources regardless of repetition |

## Edge Cases

**Claim is true by definition:** Don't tag — it's not an empirical claim. Note it as definitional.
**Claim has a precise answer but we can't find it:** Unverifiable (with explanation of what database would have it).
**Claim was true historically but may have changed:** Tag the historical claim and note the temporal limitation.
**Claim is about a consensus that shifted:** Contested (note the historical vs. current positions).
