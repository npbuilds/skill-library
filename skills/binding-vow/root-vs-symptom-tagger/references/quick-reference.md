# Root Vs Symptom Tagger — Quick Reference


## Quick Reference

| Typology | Stakes | Recommended method |
|---|---|---|
| Well-defined | Low | 5 Whys (start; upgrade if chain feels forced) |
| Well-defined | Medium | Fishbone (covers multiple causes; low overhead) |
| Ill-defined | Any | Fishbone (default; surfaces categorical causes) |
| Wicked | Medium | Dependency mapping (call `claim-decomposer`) |
| Wicked | High | CRT (high cost, high yield) |
| Mess | Any | Step out — call `ackoff-mess`; consider dissolution before root-cause work |
| Adaptive | Any | Stakeholder rotation (not root-cause) → call `values-excavator` |

## Quick Reference

| Tag | Definition |
|---|---|
| **Root** | A claim that, if false, makes other claims also-false. Causally upstream. |
| **Symptom** | A claim that's downstream of a root; treating it does not address upstream causes. |
| **Contributing** | Causally relevant but not at the root or terminal-symptom level. |
| **Ambient** | True but not causally connected to the rest (context, not cause). |

## Step 3 — Apply or delegate

| Method | Action |
|---|---|
| 5 Whys | Run inline (sequential causation chain) |
| Fishbone | Run inline (categorical brainstorm; 6M categories or domain-appropriate) |
| Dependency mapping | Delegate to `claim-decomposer` (research); receive DAG |
| CRT | Inline if user trained on Goldratt; otherwise defer with note |

## Edge Cases

| Pattern | Handling |
|---|---|
| Typology is Mess | Don't run root-cause work; route to `ackoff-mess` reference and return "method N/A — dissolution before root analysis" |
| Typology is Adaptive | Don't run root-cause work; root-cause framing is wrong for adaptive challenges. Route to `stakeholder-rotator` and `values-excavator` |
| 5 Whys chain feels forced (each "why" is a strain) | Upgrade to Fishbone. The forced feeling means the linear pathway is wrong |
| Fishbone produces 15+ causes | Group into super-categories first; the brainstorm is too granular |
| Multiple plausible roots | Tag all of them; downstream skills will use stakes-weighted prioritization |
| No root surfaces after running method | Surface explicitly: "no root identified at this depth — either the statement is too narrow (symptom-only) or the root is upstream of stated scope." Recommend Phase 1 re-intake with broader framing |

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
