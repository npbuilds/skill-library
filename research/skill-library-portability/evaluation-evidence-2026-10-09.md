# Evaluation evidence for a portable skill library

Research date: 2026-10-09. Spelunker evidence subtask; primary-source review, not a reproduction. Central conclusion: **Likely** that portability needs an empirical compatibility layer, because published results vary by task, harness, model, retrieval setting, and environment. The claim of universal positive benefit is **not supported and refuted by counterexamples**; the studies evaluate different conditions rather than necessarily disagreeing about the same conditions. Interoperable packaging remains useful even when a particular skill is not useful on a particular task.

## Primary studies (separate evidence units)

### 1. SkillsBench: positive evidence, with restricted scope

[Full text, v4](https://arxiv.org/html/2602.12670v4), [version history](https://arxiv.org/abs/2602.12670). v1: February 13, 2026; v4: June 14, 2026. Table 3 / Appendix I Table 10 reports 87 tasks, 18 model–harness configurations, mean pass rates 33.9% without and 50.5% with curated skills: **+16.6 percentage points**. Configuration gains range +4.1 to +25.7 points. Section 5.1.1 compares the same model under different harnesses and finds differing realized benefits. Section 6.1 explicitly limits generalization to GUI, multi-agent, and very long workflows; requests length-matched and documentation controls; acknowledges nondeterminism and contamination. This is not proof for an arbitrary future runtime. Older figures (+16.2 points, seven configurations) refer to earlier versions.

Affiliation: BenchFlow-led academic/industry collaboration, including OSU, Amazon, Berkeley and numerous others. Benchmark authors are ecosystem participants. Confidence: **Likely** for these source-reported results because they were checked against one authoritative primary paper, not three independent sources; **Likely** that harness identity belongs in compatibility records, because the within-paper comparisons and limited scope support it. No independent replication performed here.

### 2. Realistic retrieval substantially changes the result

[How Well Do Agentic Skills Work in the Wild, v1](https://arxiv.org/html/2604.04323v1), April 6, 2026. UCSB, MIT CSAIL, MIT-IBM Watson AI Lab. Table 2, Claude column: SkillsBench pass rates are **51.2 curated / 35.4 none / 40.1 retrieved with curated skills in pool / 38.4 retrieved without curated skills**. The pool contains about 34,000 public skills. Query-specific refinement improves Terminal-Bench Claude performance from **61.4 to 65.5**, but reduces Kimi SkillsBench with-curated retrieval from **33.5 to 26.7**. This is direct counterevidence to automatic refinement always helping.

Appendix B: three model–harness pairs, three runs per task, 84 SkillsBench and 89 Terminal-Bench tasks. Models and harnesses are paired, so their effects are not separated; timeouts also differ. Coverage judgments use an LLM. Confidence: **Likely** that selection and adaptation deserve their own evaluation, because these experimental conditions materially change outcomes. Results do not establish the effect size at this library's smaller scale.

### 3. SWE-Skills-Bench: version mismatch and weak marginal benefit

[Full text, v1](https://arxiv.org/html/2603.15401v1), March 16, 2026. Nanjing University, MBZUAI, South China University of Technology and UNSW. Table 2 reports **49 skills / 565 task instances**, **39 skills with zero pass-rate lift**, aggregate **89.8% baseline versus 91.0% with skills**, and service-mesh-observability token overhead **450.8%**. Section 4.1 uses only Claude Code with Haiku 4.5. Many tasks have perfect baseline pass rates, creating a ceiling effect. The authors explicitly call this a preliminary work in progress. Descriptions of skill placement differ between sections 3.2 and 4.1, which should be resolved before replication. The paper attributes several negative cases to framework-version conflicts.

Confidence: **Likely** for the source-reported table values because one primary study supports them, without independent replication; **Likely** for environment compatibility as a useful design requirement because failure examples illustrate it. These results cannot establish that 80% of this user's skills are useless, nor generalize across all runtimes.

### 4. Context files can induce extra work

[Evaluating AGENTS.md, v1](https://arxiv.org/html/2602.11988v1), February 12, 2026. ETH Zurich and LogicStar.ai. Section 4.2 / Table 2 reports generated context files increase average cost **20% on SWE-bench Lite and 23% on AGENTbench**, while decreasing resolution in five of eight settings. Developer-written context generally performs better than generated context and sometimes improves the no-context baseline. The study concerns repository instructions, not reusable skill packages; Python-centered coding benchmarks restrict transfer. The introduction's rounded percentages differ from detailed result phrasing, so use section 4.2 and Table 2 rather than conflating the measures.

Confidence: **Likely** that procedural instruction overhead should be measured, because observable extra exploration/testing accompanies the cost change. This is counterevidence to “more guidance always helps,” not a reason to remove essential project rules.

### 5. Failure attribution: prompt size is not the whole cost

[Agent Skills Can Be Harmful, v1](https://arxiv.org/html/2608.11888v1), August 12, 2026. HUST, Microsoft Research/Microsoft, UIUC; lead-author internship at Microsoft Research disclosed. Abstract and results sections report **307 attributed cases: 125 functional failures and 182 efficiency regressions**. Excessive procedure accounts for **114/182 efficiency cases**; excessive verification accounts for **67 cases**, heavy implementation pipelines for **30**. These are counts from a constructed differential failure dataset, **not a deployment failure-rate estimate**. The method compares target runs with successful/cheaper reference runs; manual attribution and selected tasks limit causal and external validity (section VII-B).

Confidence: **Likely** that cost budgets must include induced actions rather than only loaded tokens, because the differential analysis identifies distinct sources of overhead. This paper extends SkillsBench/SWE-Skills-Bench rather than providing an independent task distribution.

## Six changes to the plan (design recommendations, not measured local results)

1. **Make compatibility empirical.** Keep transport/package validation separate from behavioral qualification. Record skill hash, model identifier, harness and adapter versions, task cohort, environment versions, capability profile, and evaluation date. Display “loads successfully” separately from “demonstrated useful.” Requalify affected pairs after model/harness changes. This is an inference supported by studies 1–3.
2. **Use a three-arm test.** Same held-out task, environment, model, and budget: no skill; explicitly selected skill; automatic retrieval/selection. The explicit-minus-none difference measures potential utility; retrieved-minus-explicit exposes routing loss. Include irrelevant-neighbor tasks and genuine no-skill tasks. Record selection false positives and abstention, not merely recall. Compare uncertainty intervals across repeated runs; one failed trial is not sufficient attribution. This is a proposed evaluation design informed by studies 1–3.
3. **Give the resolver permission to return none.** Candidate suggestions and explicit invocation should precede a mandatory autonomous resolver. Allow runtime choice and user override; reject incompatible candidates; expose selection reasons. Do not interpret semantic similarity or high loading rate as success. Evaluate query-specific adaptation as an optional arm and preserve original/adapted hashes. This is an inference from study 2, not proof of an optimal resolver.
4. **Add applicability and conflict checks.** Track supported API/framework versions, filesystem assumptions, output contracts, required state, exclusions, and examples versus binding requirements. Resolve project requirements before generic template defaults. Test combinations of commonly co-loaded skills for incompatible assumptions. Capability names alone cannot encode these distinctions. This recommendation follows studies 3 and 5.
5. **Budget actual execution effort.** Besides context budgets, expose lightweight/standard/deep modes, tool-call and wall-time caps, verification stopping criteria, and fallback paths. Enforce hard caps in the host, because textual recommendations are not execution controls. Track extra work induced by skills and unsuccessful as well as successful runs. Do not treat every checklist step as mandatory for every task. Inference from studies 1, 4 and 5.
6. **Release on utility, not formatting.** Structural validity, schema compliance, and successful retrieval are necessary but insufficient. Maintain small held-out end-to-end suites across a native-file host, an MCP/function-call host, and a minimal local custom runner. Cover reference-only, scripted, and orchestrated skills. Gate changes on acceptable quality/cost tradeoffs per cohort; retire or stop autoloading skills whose marginal value disappears. These are proposed local policies, not thresholds established by the papers.

## Adversarial synthesis

If structured skills inherently improved every agent, gains would persist across skill sets and selection settings. Studies 2–5 supply counterexamples. If skills were generally ineffective, study 1's broad positive aggregate and study 2's successful retrieval/refinement settings would be unexpected. The supported conclusion is conditional value, not universal success or failure.

Do not count all five papers as five independent replications. Studies 2 and 5 reuse SkillsBench; study 5 also uses SWE-Skills-Bench. Author affiliation differs, but shared benchmark/task ancestry reduces evidential independence. SkillsBench has many coauthors; complete funding and individual-author overlap were not exhaustively audited. No benchmark here validates this exact library or promises plug-and-play semantic equivalence.

## Limitations and next experiment

- Sources are primary preprints/full texts, not independently reproduced results; peer-review status was not established for all papers. Numerical values were checked against the indicated source tables or results sections. No paid model runs were made.
- Existing library effectiveness, current Grok/Hermes behavior, subjective creative quality, private data workflows, long-lived agents, and multi-agent execution remain unmeasured in this subtask.
- The exact best router, useful context length, skill-count limit, and regression thresholds are **Speculative** without local experiments. Avoid turning a benchmark's observed compactness association into a universal fixed three-skill rule.
- Propose 12 representative held-out tasks plus negative triggers, three arms, repeated runs, across three integration types. Choose a fixed approved spend and runtime budget before executing. Report artifact correctness, constraint adherence, side effects, elapsed time, tokens, tool calls and failure attribution, not just checklist compliance.

Confidence summary: **Confirmed**: no claim meets the strict three-independent-source threshold in this subtask; **Likely**: source-reported values, version dates, and value of compatibility tests and effort-aware selection; **Contested**: no same-condition scientific disagreement established here (universal benefit is explicitly not supported, with counterexamples); **Speculative**: local effect sizes and optimal router; **Unverifiable**: cross-runtime performance of this library until tested.
