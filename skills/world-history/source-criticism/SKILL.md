---
name: source-criticism
description: >
  Evaluate historical sources through primary and secondary source classification, internal
  and external criticism, bias detection, provenance analysis, the hermeneutic circle, and
  digital source authentication. Use when encountering a historical document, artifact, or
  claim that needs assessment of what it can and cannot tell us about the past.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
---

# Source Criticism — The Craft of Evaluating Evidence

Source criticism is applied epistemology for historians. It answers the question: given this piece of evidence from the past, what can we reliably conclude — and what remains uncertain? The craft emerged from philological and biblical criticism in the 19th century (Ranke's *wie es eigentlich gewesen* — "as it actually was") and has evolved through the Annales school, postcolonial critique, and digital humanities into a sophisticated analytical framework.

This skill bridges to `epistemology` in the philosophy domain and `source-triangulator` in the research domain.

## When This Applies

- User encounters a specific historical document, text, artifact, or image
- User asks "how do we know" a particular historical claim
- User presents a source as unquestionable evidence
- User needs to distinguish between what a source *says* and what it *means*
- User asks about forgeries, propaganda, or contested evidence
- User evaluates a secondary source (historical monograph, article, textbook)

## Primary vs. Secondary Sources

The classification is relational, not absolute. The same document can be primary for one question and secondary for another.

**Primary sources** are created during or near the period under study by participants or witnesses. They include:
- Official documents (treaties, laws, decrees, census records)
- Personal testimony (diaries, letters, memoirs, oral histories)
- Material evidence (artifacts, architecture, coinage, textiles)
- Visual evidence (paintings, photographs, maps, film)
- Textual evidence (chronicles, inscriptions, literary works)

**Secondary sources** are created after the period by scholars analyzing primary sources. They include monographs, journal articles, textbooks, and documentaries.

**The key principle:** Primary sources are not more "truthful" than secondary sources. They are *closer to the event* but also more embedded in its biases. A general's memoir about a battle he lost is primary and biased. A historian's analysis fifty years later is secondary but may be more accurate.

## The Two Axes of Criticism

### External Criticism (Authenticity)

Is this source what it claims to be? External criticism establishes authenticity before interpretation begins.

| Question | Method | Example |
|---|---|---|
| Is this genuine or forged? | Paleography, carbon dating, chemical analysis, provenance chain | The Hitler Diaries (1983) — exposed through anachronistic paper and ink |
| When was it created? | Dating techniques, internal chronological references, stylistic analysis | Dead Sea Scrolls dating through C-14 and paleography |
| Who created it? | Attribution analysis, handwriting, linguistic fingerprinting | Disputed Shakespearean authorship through computational stylistics |
| Has it been altered? | Comparison with other copies, interpolation detection | Medieval chronicle additions by later scribes |

### Internal Criticism (Reliability)

Assuming the source is authentic, how reliable is its content?

**Positive criticism** — What does this source contain that is credible?
- Does the author have direct knowledge of the events described?
- Is the account consistent with other independent sources?
- Does the author report details that work against their own interests? (Criterion of embarrassment)
- Are the specific details verifiable against material evidence?

**Negative criticism** — What might be wrong, distorted, or omitted?
- **Bias of position**: What was the author's social position, political allegiance, institutional role?
- **Bias of purpose**: Was this created to inform, persuade, justify, condemn, or entertain?
- **Bias of access**: What could the author observe directly vs. what did they hear secondhand?
- **Bias of convention**: What genre conventions shaped the account? (Medieval saints' lives follow templates regardless of the individual saint)
- **Silence**: What is NOT mentioned? Absences can be as revealing as presences.

## The Bias Detection Framework

Bias is not a disqualification — every source is biased. The goal is not to find "unbiased" sources but to understand *how* each source is biased and factor that into interpretation.

### The PACT Protocol

For any source, assess:

1. **P — Perspective**: From whose viewpoint is this written? What can they see? What is hidden from them?
2. **A — Audience**: Who was the intended recipient? How does audience shape what is said and unsaid?
3. **C — Context**: What was happening when this was created? What pressures, incentives, or constraints operated on the creator?
4. **T — Type**: What genre is this? (Official report, personal letter, propaganda poster, legal deposition) Genre conventions shape content.

### Corroboration Protocol

When evaluating a claim across sources:

1. **Convergence**: Multiple independent sources agree → higher confidence
2. **Divergence**: Sources disagree → investigate why (different perspectives? different information? deliberate distortion?)
3. **Singular attestation**: Only one source makes this claim → lower confidence, but not necessarily wrong (some events are poorly documented)
4. **Independent vs. dependent**: Do confirming sources stem from a single original? (Multiple medieval chronicles may copy from one lost original)

## The Hermeneutic Circle

Understanding a source requires understanding its context; understanding the context requires understanding the sources. This circularity is not a flaw — it is the structure of historical interpretation.

**In practice:**
1. Read the source with initial understanding
2. Research the context (author, period, conditions)
3. Re-read the source with contextual knowledge — new meanings emerge
4. The new reading refines your understanding of the context
5. Iterate until interpretation stabilizes

The circle never fully closes. Historical interpretation is always provisional and revisable in light of new evidence or new questions.

## Digital Source Challenges

Modern source criticism must contend with:

- **Digital provenance**: Screenshots can be fabricated; metadata can be altered; AI-generated content can mimic historical documents
- **Archival bias**: What gets digitized shapes what gets studied. Digitization is not neutral — it reflects institutional priorities and funding
- **Scale vs. depth**: Distant reading (computational analysis of large corpora) reveals patterns invisible to close reading, but can miss nuance and context
- **The internet as source**: Websites, social media, databases — born-digital sources with their own authentication challenges

## Source Evaluation Template

When evaluating a specific source, structure the analysis as:

```
SOURCE: [Identify the source]
TYPE: [Primary/Secondary | Genre | Medium]
CREATOR: [Who | When | Where | Position]
AUDIENCE: [Intended recipient(s)]
PURPOSE: [To inform / persuade / justify / record / entertain]
CONTEXT: [Conditions of creation]
RELIABILITY: [What it can tell us | What it cannot tell us]
CORROBORATION: [What other sources say | Where they agree/disagree]
CONCLUSION: [What this source contributes to understanding the question]
```