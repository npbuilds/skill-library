# The Consumer Research Landscape (2024-2026): What Emptor Must Know

## Research Purpose

This document grounds the **Emptor consumer-research suite** (`skills/consumer-research/`) in evidence. It answers three questions a rigorous purchase-research orchestrator must get right:

1. **Source trust** — which consumer review sources are reliable in 2026, which have degraded, and how to detect fake reviews now that dedicated tools are dead.
2. **Evaluation methodology** — how professional testers and decision scientists structure product evaluations, and which methods measurably improve purchase outcomes.
3. **Tools landscape** — what AI shopping assistants exist, their documented failure modes, and the gaps a personal zero-monetization suite can exploit.

Compiled 2026-06-10 from three parallel web-research passes. Every claim carries a confidence tag per the spelunker framework (`skills/research/spelunker/references/confidence-framework.md`): **Confirmed** (2+ independent sources), **Likely** (strong single source + corroboration), **Speculative** (inference or anecdote), **Contested** (credible sources disagree).

---

## 1. SOURCE TRUST LANDSCAPE

### 1.1 The Trust Tier Model

**Tier 1 — Independent testers (highest trust).** Common structural traits: financial independence (subscriptions/donations, no ads), anonymous retail purchasing or self-funded products, no free manufacturer samples, published methodology.

- **Consumer Reports** — anonymous retail purchasing, no advertising, methodology bulletins for 30+ categories. Weakness: exact weighting formulas are proprietary. **Confidence: Confirmed**
- **Rtings** — versioned test benches since 2019, transparent revenue disclosure, no sponsored content; dominant for TVs/monitors/headphones. Caveat: 2024 TV scoring update was criticized by enthusiast communities (Contested at the margin). **Confidence: Confirmed**
- **Which? (UK)** — no advertising; simulated real-world durability testing (e.g., 30,000 barrel rolls on mattresses ≈ 10 years of use). **Confidence: Confirmed**
- **America's Test Kitchen** — no free samples, no manufacturer trips, no display ads; kitchen/cooking scope only. **Confidence: Confirmed**
- **Project Farm (YouTube)** — self-funded purchases, declines sponsorships, comparative real-world testing; trust rests on creator reputation rather than published protocols. **Confidence: Confirmed**

**Tier 2 — Editorially independent but affiliate-funded.**
- **Wirecutter (NYT)** — 20-40 hour research phases, 50-100 candidates narrowed to 10-15 finalists, multi-week real-world testing; editorial independence maintained post-acquisition, but affiliate revenue is structural and exact rubrics unpublished. **Confidence: Confirmed**
- **Good Housekeeping Institute, TechRadar, CNET** — real testing operations, less methodology transparency, variable update cadence. **Confidence: Likely**

**Tier 3 — Crowd sources (use with verification).**
- **Reddit** — genuine expertise coexists with documented astroturfing: a game-marketing firm bragged about 100+ fake "organic" comments (Feb 2025); coordinated political campaigns documented (Oct 2024); ~1,200+ bot suspensions yearly with many evading detection. **Confidence: Confirmed**
- **YouTube reviewers (general)** — sponsorship and sample-seeding hard to audit. **Confidence: Likely**
- **Capterra (software)** — useful aggregate but vendor-incentive misalignment. **Confidence: Likely**

**Tier 4 — Avoid/downweight heavily.** Generic "best X 2026" affiliate SEO sites and AI content farms. Google's March 2026 core update hit 71% of tracked affiliate domains negatively; AI content farms lost 60-80% of traffic. **Confidence: Confirmed**

### 1.2 Degradation Evidence

- **Google product search is degraded.** Leipzig/Bauhaus-Weimar academic study: product review results "systematically taken over by low quality, trashy SEO content"; ~10% accuracy decline. Emptor must use **site-scoped searches** (`site:rtings.com`, `site:consumerreports.org`), never generic "best X 2026" queries. **Confidence: Confirmed**
- **Fake review scale.** Amazon blocked/removed 275M fake reviews in 2024 ($500M spent); Google removed 240M policy-violating reviews; TripAdvisor removed 8.7% of its platform; only 24% of consumers are confident they can spot a fake. **Confidence: Confirmed**
- **AI-generated reviews** are growing ~80% month-over-month and are largely indistinguishable to humans (55% human detection accuracy in studies). **Confidence: Likely**
- **FTC fake-review rule** (effective 2024-10-21) prohibits buying/selling fake reviews, penalties up to $51,744/violation — usable as a reputational-risk signal for sellers with documented violations. **Confidence: Confirmed**

### 1.3 Fake-Review Detection After Fakespot

**Fakespot shut down 2025-07-01** (Mozilla); **ReviewMeta is unmaintained**. Dedicated consumer tooling is gone; successors (RateBud, SureVett) are early-stage — RateBud has documented self-astroturfing on Reddit and suspiciously uniform scores. **Confidence: Confirmed**

What works is an **ensemble of heuristics** — no single signal suffices (hybrid models reach ~93% accuracy on Amazon vs ~55% for humans):

| Signal | Suspicious threshold |
|---|---|
| Review velocity | spike — e.g., >50% of reviews in the last 2 weeks |
| Verified-purchase ratio | < 70% |
| Rating distribution | artificial peaks vs the natural J-curve |
| Account age / history | new accounts, single-burst histories |
| Cross-product patterns | same reviewers across products, same-day posts |
| Linguistic fingerprints | perplexity/syntactic-predictability scoring (NOT generic "AI detector" tools — high false positives) |

**Confidence: Confirmed** (academic + platform-aligned sources).

### 1.4 Category Routing and Freshness

| Category | Route to | Notes |
|---|---|---|
| Electronics (TV/audio/monitors) | Rtings → Consumer Reports | strongest methodology coverage |
| Appliances | Consumer Reports, Which? | durability simulation matters |
| Kitchen | America's Test Kitchen | gold standard, narrow scope |
| Tools/outdoor | Project Farm + CR | comparative testing |
| Software/SaaS | Capterra + TechRadar | verify test timestamps; fastest decay |
| Services (trades, repair) | No institutional source | Reddit + local reviews with astroturf checks; weakest category (**Speculative** — inference from absence) |

**Temporal decay:** review credibility decays ~12 months (Tier 1), ~6 months (Tier 2), ~3 months (software). Briefs must carry freshness stamps and declare their own staleness date. **Confidence: Likely**

---

## 2. EVALUATION METHODOLOGY

### 2.1 Structured Methods Measurably Work

- **Interactive consumer decision aids: 93% of users chose the objectively superior product vs 65% without** (Marketing Science). Combining sorting + elimination tools boosts quality under high choice conflict. **Confidence: Confirmed**
- The classic five-stage consumer decision process (need recognition → search → evaluation → purchase → post-purchase) with structured support produces higher satisfaction and cheaper future searches. **Confidence: Confirmed**

### 2.2 The Defensible Pipeline

1. **Needs elicitation via Jobs-to-be-Done** — identify the functional, emotional, and social job before looking at any product. **Confidence: Confirmed**
2. **MoSCoW constraint capture** — separate genuine must-haves from strongly-wanted features; lock budget **before** price exposure (70% of consumers report being heavily influenced by the first price seen — anchoring). **Confidence: Confirmed**
3. **Elimination-by-aspects** (Tversky 1972) on must-haves in priority order — matches how humans actually decide, prunes the field cheaply, and guards against choice overload (real but conditional per meta-analyses: fires when options are comparable, stakes high, expertise low). **Confidence: Confirmed**
4. **Weighted-sum MCDA on the 3-6 finalists** — explicit weights (lightweight AHP or direct assignment), scores normalized 0-100, each criterion score linked to test data or primary specs, scored blind to brand/price where feasible (halo defense). **Confidence: Confirmed**
5. **Sensitivity analysis** — vary top 2-3 weights ±20% and re-rank. Stable → high confidence. Unstable → present multiple robust options rather than forcing a #1. **Confidence: Confirmed**
6. **Satisficing exit** — maximizers are measurably less satisfied and more regret-prone (Schwartz). When several finalists clear every must-have and survive sensitivity, say so explicitly: "pick on feel." **Confidence: Confirmed**

### 2.3 Bias Defenses to Encode

| Bias | Defense |
|---|---|
| Anchoring | budget locked before any price is displayed |
| Halo/brand effect | feature scoring blind to brand and price |
| Social proof (80% check reviews; 68% buy trending) | weight expert blind testing ≥ crowd sentiment; verify review authenticity first |
| Spec-sheet seduction | "does this feature materially improve the job?" gate |
| Decoy/scarcity effects | ignore urgency framing; compare only on elicited criteria |
| Maximizer regret | satisficing exit; cap finalists at 3-6 |

**Confidence: Confirmed** (each effect individually documented; the defense mapping is design synthesis).

---

## 3. AI SHOPPING TOOLS LANDSCAPE AND FAILURE MODES

### 3.1 What Exists (2025-2026)

ChatGPT Shopping Research (+ deprecated Instant Checkout), Perplexity Shopping (deliberately zero-commission), Amazon Rufus, Google AI Overviews shopping, Walmart Sparky, Consumer Reports AskCR (RAG over CR's own tests, subscription-gated), and niche startups (Daydream — fashion; Onton — furniture). Niche players outperform generalists inside their verticals. **Confidence: Confirmed/Likely**

### 3.2 Documented Failure Modes

| Failure | Evidence | Confidence |
|---|---|---|
| Multi-constraint inaccuracy | ChatGPT ~52-64% accuracy on multi-constraint product queries | Confirmed |
| Confident wrongness | Rufus recommends category-inappropriate products, misreads attributes | Confirmed |
| Zombie products | 18-34% of discontinued items remain fully indexed and recommendable; one dead smartwatch appeared in 62% of "top wearables" lists | Confirmed |
| Stale prices/stock | batch feeds, not real-time; wrong prices and availability at checkout | Confirmed |
| Affiliate capture | ChatGPT ~4% transaction fee + 2% affiliate; 28% of consumers suspect sponsored push | Confirmed |
| Scam-merchant poisoning | cloned product pages/branding deceive AI agents; ChatGPT shopping results linked to scam sites | Confirmed |
| Explainability void | users cannot see why X over Y; commission models disincentivize showing reasoning | Confirmed |
| AI-SEO gaming | merchant tools (Goodie, Rank Prompt) now optimize content specifically to influence LLM recommendations | Likely |

### 3.3 Gaps Emptor Exploits

1. **Zero monetization** — no affiliate links, no commissions, ever. Structural trust advantage over every commercial tool.
2. **Full decision-trail transparency** — elicited requirements, weights, evidence, and sensitivity all visible in the brief.
3. **Constraint validation before recommendation** — must-haves verified per finalist, attacking the multi-constraint accuracy ceiling.
4. **Availability/discontinuation verification** — explicit check per finalist, killing zombie recommendations.
5. **Review-authenticity flagging** — the ensemble heuristics of §1.3, undeployed in any mainstream shopping AI.
6. **Merchant trust checks** on every where-to-buy link.
7. **Adversarial posture toward merchant content** — manufacturer/merchant copy treated as claims to verify, not evidence.
8. **Calibration loop** — purchase outcomes resolve brief confidence via `/purchase-review` → `data/calibration.jsonl`, something no commercial tool closes.

---

## Sources (primary references)

**Source trust:** Consumer Reports rating methods (data.consumerreports.org/rating-methods); CR reliability methodology bulletin; Rtings test methodology (rtings.com/tv/learn/how-we-test); ATK editorial standards (americastestkitchen.com/articles/8633); Which? testing (which.co.uk/about-which/which-tests); EngineerFix on Project Farm; Federal Register 2024-18519 (FTC consumer-review rule); eMarketer fake-review concern data; ReviewDriver/Nadernejad fake-review statistics 2025-2026; TraceFuse + TrueStar on Fakespot shutdown; Sparkco + AllSides on Reddit astroturfing; SEO.AI summary of the Leipzig/Bauhaus-Weimar search-quality study; DigitalApplied on the March 2026 Google core update; arXiv 2410.17507 (fake-review buyer network detection); arXiv 2509.21579 (spam detection at scale).

**Methodology:** Marketing Science 19(1) interactive decision aids (pubsonline.informs.org/doi/10.1287/mksc.19.1.4.15178); Tversky 1972 elimination-by-aspects; Schwartz 2002 maximizing-vs-satisficing; Scheibehenne et al. 2010 and Chernev et al. choice-overload meta-analyses (ScienceDirect S1057740814000916); St. Louis Fed on anchoring; Strategyn/Ulwick JTBD; MCDA weight-stability literature (ScienceDirect S0957417425020792).

**Tools landscape:** OpenAI shopping-research announcement; Marketplace Pulse "Amazon's shopping AI is confidently wrong"; ConsumerAffairs on Rufus; Modern Retail on Instant Checkout's failure; Inc. on Walmart/ChatGPT; Alibaba product-insights on discontinued-item recommendation; Cybernews on hijacked ChatGPT shopping results; Chain Store Age consumer-trust survey; Omnisend/Digital Commerce 360 2026 trust report; WebProNews on OpenAI checkout fees; Affiverse on Perplexity's zero-commission stance; Fortune/CNN on Daydream; TechCrunch on Onton; Tech Xplore on 93%-accuracy hybrid fake-review detection.

---

*Maintained by the consumer-research domain. The trust tiers in §1.1 are a 2026 snapshot — `source-trust-atlas` carries the operational version with decay rules; re-verify source independence during `deep` runs and refresh this report annually.*
