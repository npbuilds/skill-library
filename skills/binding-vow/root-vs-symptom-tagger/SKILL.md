---
name: root-vs-symptom-tagger
description: >
  Pick the right root-cause method (5 Whys / Fishbone / dependency mapping / Current Reality
  Tree) for a problem statement based on typology and stakes, and tag each atomic claim as
  root or symptom. Use during binding-vow's Phase 3 decomposition. Delegates dependency
  mapping to research/claim-decomposer. Returns method recommendation plus per-claim
  root-vs-symptom tags.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Write
---

# Root-vs-Symptom Tagger — The Method Router

The four root-cause methods (5 Whys, Fishbone, dependency mapping, CRT) are not interchangeable. Each has a sweet spot and a failure mode. This skill picks the right method for the problem at hand and tags each atomic claim as root or symptom so downstream phases know what's load-bearing.

The skill is a *router*, not a method implementation. For two of the four methods (dependency mapping and full CRT) it delegates. For 5 Whys and Fishbone it produces the structured output directly.

For the foundational comparison, see [[root-cause-methods-comparator]] in the vault.

## Method Selection

Selection driven by the typology tag (from `problem-typology`) and stakes (from `stakes-assessor`):

| Typology | Stakes | Recommended method |
|---|---|---|
| Well-defined | Low | 5 Whys (start; upgrade if chain feels forced) |
| Well-defined | Medium | Fishbone (covers multiple causes; low overhead) |
| Ill-defined | Any | Fishbone (default; surfaces categorical causes) |
| Wicked | Medium | Dependency mapping (call `claim-decomposer`) |
| Wicked | High | CRT (high cost, high yield) |
| Mess | Any | Step out — call `ackoff-mess`; consider dissolution before root-cause work |
| Adaptive | Any | Stakeholder rotation (not root-cause) → call `values-excavator` |

Default fallback: Fishbone if typology and stakes don't clearly point to another method.

## Per-Claim Tagging

After picking the method, run it (or delegate). Receive the cause structure. Then tag each atomic claim:

| Tag | Definition |
|---|---|
| **Root** | A claim that, if false, makes other claims also-false. Causally upstream. |
| **Symptom** | A claim that's downstream of a root; treating it does not address upstream causes. |
| **Contributing** | Causally relevant but not at the root or terminal-symptom level. |
| **Ambient** | True but not causally connected to the rest (context, not cause). |

Tagging rules:
- A statement may have multiple roots (Fishbone, CRT). Tag all roots; don't force one-root reduction.
- Symptoms typically outnumber roots 3-10x. If you find one root and ten symptoms, that's normal.
- Ambient claims should be small in number. If many claims are ambient, the decomposition is over-broad.

## Process

### Step 1 — Read typology and stakes inputs

From `problem-typology` and `stakes-assessor` outputs. If either is missing, return `deferred — diagnosis incomplete`.

### Step 2 — Select method

Apply the selection table above. If `claim-decomposer` returned atomic claims already (Phase 3 calls it before this skill), the dependency graph is already available — prefer dependency-mapping if claims have rich dependency structure.

### Step 3 — Apply or delegate

| Method | Action |
|---|---|
| 5 Whys | Run inline (sequential causation chain) |
| Fishbone | Run inline (categorical brainstorm; 6M categories or domain-appropriate) |
| Dependency mapping | Delegate to `claim-decomposer` (research); receive DAG |
| CRT | Inline if user trained on Goldratt; otherwise defer with note |

### Step 4 — Tag each claim

Apply the four-way tagging (Root / Symptom / Contributing / Ambient) to each atomic claim from `claim-decomposer` (Phase 3) or to each cause from the inline method.

### Step 5 — Verify

A valid tagging satisfies:
- At least one Root tag (or explicit "no root surfaced; this is symptom-level" verdict)
- Symptoms have a causal path to at least one Root
- No claim is tagged both Root and Symptom

## Output Format

```
ROOT-VS-SYMPTOM — [first 60 chars of statement...]
─────────────────────────────────────────────
Method used: [5 Whys | Fishbone | dependency mapping | CRT | inline+delegated]
Method rationale: [why this method given typology + stakes]

Cause structure:
[Method-appropriate diagram or list — chain for 5 Whys; categorical for Fishbone;
DAG reference for dependency; logic tree for CRT]

Per-claim tags:
  Claim 1: [text] — Tag: [Root | Symptom | Contributing | Ambient] — Causal note
  Claim 2: ...
  ...

Roots identified:        [count, list]
Load-bearing symptoms:   [symptoms that, if treated, materially help even without root resolution]
Ambient (context only):  [list]
```

## Edge Cases

| Pattern | Handling |
|---|---|
| Typology is Mess | Don't run root-cause work; route to `ackoff-mess` reference and return "method N/A — dissolution before root analysis" |
| Typology is Adaptive | Don't run root-cause work; root-cause framing is wrong for adaptive challenges. Route to `stakeholder-rotator` and `values-excavator` |
| 5 Whys chain feels forced (each "why" is a strain) | Upgrade to Fishbone. The forced feeling means the linear pathway is wrong |
| Fishbone produces 15+ causes | Group into super-categories first; the brainstorm is too granular |
| Multiple plausible roots | Tag all of them; downstream skills will use stakes-weighted prioritization |
| No root surfaces after running method | Surface explicitly: "no root identified at this depth — either the statement is too narrow (symptom-only) or the root is upstream of stated scope." Recommend Phase 1 re-intake with broader framing |

## Output Contract for `six-eyes`

Called from Phase 3 (Decompose) after `claim-decomposer` has run. Receives the atomic claim list. Returns:
- Selected method
- Per-claim tags
- Roots identified (drives Phase 4 reframing focus)
- Load-bearing symptoms (drives where to intervene if root is intractable)

If method is delegated (dependency / CRT), include the delegation note and any external skill outputs in the response.

## Connections

- `problem-typology` (binding-vow) — upstream input; drives method selection
- `stakes-assessor` (binding-vow) — upstream input; drives method selection at the margin
- `claim-decomposer` (research) — delegation target for dependency mapping; also provides the atomic claim list this skill tags
- `ackoff-mess` (binding-vow) — escalation path for Mess typology
- `values-excavator` (philosophy/ethics) — escalation path for Adaptive typology
- `wicked-vs-tame` (binding-vow) — reference for typology-driven method choice
- `root-cause-methods-comparator` (vault — `skill-lab/`) — foundational comparator of the four methods

## Sources

- Toyoda, S. / Ohno, T. (Toyota) — 5 Whys
- Ishikawa, K. (1960s) — Fishbone / Ishikawa diagram
- Goldratt, E. M. (1994). *It's Not Luck*. — Current Reality Tree
- See [[root-cause-methods-comparator]] for the full comparator and selection criteria.
