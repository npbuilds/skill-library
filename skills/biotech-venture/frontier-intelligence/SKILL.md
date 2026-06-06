---
name: frontier-intelligence
description: >
  Direct frontier signal-scanning, mindshare quantification, data-generation monitoring, and
  emerging-target radar to the appropriate specialist skill. Activate when the question is "what is
  emerging?" — which targets and modalities are accreting attention and data before they are drug
  classes, how fast, and which are worth tracking. This director owns the front of the funnel: it
  reads the second derivative of the literature, capital, and data-engine signals and emits a ranked
  watchlist of candidates for the analog engine to place on the historical arc.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read
---

# Frontier Intelligence Director

Every drug class was once an unfashionable preprint. The alpha in early discovery is not spotting new biology — thousands of papers claim that weekly — but detecting the *inflection* where a target or modality begins to accrete real attention and real data before consensus prices it in. This director routes the "what is emerging?" question to specialists that read acceleration rather than volume, subtract single-lab and hype artifacts, and convert raw frontier signal into a ranked, lead-time-tagged watchlist. It is the radar that feeds the analog engine (`modality-trajectory`); together they are the discovery layer upstream of Asclepius's diligence pillars.

## Child Skills

| Skill | Type | When to Use |
|-------|------|-------------|
| signal-scanner | knowledge | Measuring the second derivative (acceleration) of literature and preprint volume per target/modality, citation-burst detection, patent/grant velocity, and first-IND translation events — the raw velocity layer |
| mindshare-tracker | knowledge | Quantifying attention as a 0–100 momentum score from conference share-of-voice, financing flows, and NewCo formation, with an explicit reflexivity and anti-hype overlay — the attention layer |
| data-generation-monitor | knowledge | Reading each new data-engine release (pQTL/MR atlases, DepMap, Perturb-seq, biobanks) as a forward signal, scored by net-new orthogonal convergences on a target — the substrate-data layer |
| emerging-target-radar | knowledge | Fusing velocity + attention + convergence into a ranked watchlist of target×modality candidates, each tagged with lead time, NewCo events, and historical pattern — the integrator |

## Routing Logic

| Question Signal | Route To | Examples |
|-----------------|----------|----------|
| Is the literature accelerating, publication/preprint velocity, citation burst, when did this become hot | signal-scanner | "Is interest in TL1A actually accelerating or already saturated?" |
| Mindshare, hype vs substance, conference buzz, how much capital/attention, is this overheated | mindshare-tracker | "Is the molecular-glue space froth or durable?" |
| New dataset, screen, biobank, atlas, what does this release imply, is the target pre-validated by data | data-generation-monitor | "UKB-PPP just released — which targets did it nominate?" |
| What should I be tracking, give me the watchlist, rank emerging targets, what's the next class | emerging-target-radar | "What are the 10 most trackable emerging target×modality bets right now?" |
| Velocity + attention | signal-scanner then mindshare-tracker | "Is this real momentum or manufactured?" |
| Full frontier scan | All four, ending in emerging-target-radar | "Scan the frontier and hand me a ranked watchlist" |

## Multi-Skill Questions

1. **Is this real momentum or manufactured froth?**: "Everyone's talking about X — should I care?"
   - Load signal-scanner to measure whether literature/preprint acceleration and first-IND events actually precede the talk
   - Load mindshare-tracker to score the attention and apply the reflexivity/anti-hype overlay (gate raw buzz against Consensus evidence-maturity)
   - Synthesize: durable inflection shows acceleration in *data and translation events*, not just review articles and Twitter; froth shows attention outrunning evidence

2. **Does this data release change the picture?**: "A new screen just dropped — does it nominate anything?"
   - Load data-generation-monitor to count net-new orthogonal convergences the release creates on candidate targets
   - Load emerging-target-radar to fold confirmed convergences into the watchlist with updated lead-time tags
   - Synthesize: a single orthogonal-evidence convergence (e.g., cis-pQTL+MR causal hit that is also a selective DepMap dependency) is worth more than ten correlative papers

3. **Build the watchlist**: "What's worth tracking?"
   - Load signal-scanner (velocity), mindshare-tracker (attention), data-generation-monitor (substrate data) for each candidate
   - Load emerging-target-radar to integrate, rank, and tag lead time + NewCo events + historical pattern
   - Hand the ranked candidate objects to `modality-trajectory` for arc-placement and conviction scoring

## Curriculum Order

1. **signal-scanner** — Foundation. Learn to read acceleration, not volume; to strip review/perspective inflation and single-lab artifacts; and to anchor lead time on the literature-inflection → first-IND gap. Everything downstream depends on a clean velocity signal.
2. **data-generation-monitor** — Second. Learn which data engines generate target-validating evidence and how to score a release by orthogonal convergence. Data is the substrate that separates durable signal from narrative.
3. **mindshare-tracker** — Third. Learn to quantify attention and, crucially, to treat reflexivity as structural — capital manufactures the attention it claims to detect — so the score is a timing instrument gated by an evidence-maturity check.
4. **emerging-target-radar** — Last. The integrator. With velocity, data, and attention in hand, learn to fuse them into a ranked, lead-time-tagged watchlist that the analog engine can consume.

## Conflict Resolution

| Conflict | Resolution | Reason |
|----------|------------|--------|
| mindshare-tracker shows surging attention but data-generation-monitor finds no orthogonal convergence | Data takes priority; flag as reflexive froth pending evidence | Attention without substrate data is the canonical hype false-positive; capital can manufacture mindshare faster than biology can validate a target |
| signal-scanner shows literature acceleration but it is concentrated in one lab (high author Herfindahl) | Discount heavily until independent replication appears | >50% of preclinical findings fail to replicate; single-lab acceleration is an artifact, not a class forming |
| emerging-target-radar ranks a candidate highly on signal but NewCo formation is absent | Note the divergence; in a contractionary financing regime absence of NewCos is weaker evidence than usual | NewCo formation is the sharpest venture signal but is regime-dependent (Q1 2025 was the decade's lowest US startup formation); normalize before penalizing |

## Scope Boundaries

**This director handles**: all questions about detecting emerging targets/modalities, measuring literature/preprint/citation/patent/grant velocity, quantifying mindshare and financing/conference attention, monitoring functional-genomics and proteomics data releases, and producing ranked discovery watchlists.

**Route to Asclepius when**:
- The candidate needs arc-placement, nearest-analog matching, or a conviction score (route to `modality-trajectory`)
- The target needs a rigorous human-genetics validation grade (route to `modality-trajectory/target-validation-ladder`)
- A clinical asset already exists and needs PoS or rNPV (route to `probability-of-success` / `asset-valuation`)
- The question is competitive mapping of a *known* clinical-stage field rather than frontier scouting (route to `competitive-intelligence/pipeline-mapper`)

## Cross-Domain Connections

- **Biotech-venture/modality-trajectory**: the analog engine this radar feeds — candidate objects flow from emerging-target-radar into arc-placement and conviction scoring
- **Biotech-venture/competitive-intelligence/pipeline-mapper**: pipeline-mapper maps *known* clinical-stage competitors; frontier-intelligence scouts *pre-clinical* emergence — adjacent halves of the same landscape
- **Investing/reflexivity-theory**: mindshare is reflexive — capital manufactures the attention it claims to detect; Soros's framework is the discipline behind the anti-hype overlay
- **Investing/secular-themes**: distinguishing investable secular biology from transient narrative
- **Product/frontier-antenna, Neocortex/foresight**: the general-purpose frontier-scanning analogs this director specializes for drug discovery
- **Research/spelunker**: deep multi-source verification of an emerging-target claim before it earns a watchlist slot
- **Dual use**: serves a clinical-scientist learning where a field is heading *and* an investor screening which emerging targets to track before they are priced in
