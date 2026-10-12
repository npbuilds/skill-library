# Spelunker deep-research method and claim map

Date: 2026-10-09. Question: what is missing from the proposed plan for a scalable skill library usable by arbitrary future agent systems, and how should the implementation order change?

Primary workflow: Spelunker deep mode, with agentic-researcher candidate comparison, source triangulation, source-interest review, evidence synthesis, and counterfactual probing. Two independent research branches handled runtime interoperability and empirical evaluation while the primary agent investigated release integrity, session isolation, execution lifecycle, observability, and repository evidence. This document records framing; findings are in the deep research brief.

## Claim decomposition

All claims are technical. “Any system” is framed as any host with a supported instruction/file/tool interface; automatic integration into closed systems is not assumed.

| ID | Atomic proposition being tested | Type | Priority | Dependency | Verification |
|---|---|---|---|---|---|
| C1 | A standards-compatible skill package can be a common distribution substrate | Factual | Critical | none | Agent Skills spec and native runtimes |
| C2 | File/protocol compatibility alone establishes executable and effective behavior | Universal/comparative | Critical | C1 | Capability, permission, lifecycle differences and empirical cross-harness results |
| C3 | Automatic skill selection reliably adds value over no skills | Comparative | Critical | none | Original retrieval and outcome benchmarks, negative cases |
| C4 | A thin adapter needs only tool-name translation | Evaluative | Critical | C2 | Compaction, artifacts, consent, retry and runtime contracts |
| C5 | Current service context is isolated between concurrent consumers | Factual | Critical | none | Code inspection plus isolated mock probe |
| C6 | Existing versions/hashes fully specify a reproducible trusted execution | Evaluative | Critical | none | Prior audit, dependency closure, provenance and update standards |
| C7 | A central execution engine or A2A is necessary for skill distribution | Evaluative | Supporting | C1,C4 | Protocol scope and native-loader counterexamples |
| C8 | More procedure/context consistently improves outcomes | Comparative | Supporting | C3 | Benchmark failures and cost/latency evidence |
| C9 | Custom telemetry vocabulary is necessary | Existential | Supporting | none | Current OpenTelemetry GenAI/skill conventions |
| C10 | Adapter validation can be limited to happy-path loading | Evaluative | Supporting | C2,C4,C6 | Installation, collisions, drift, failure and session lifecycle |
| C11 | Immediate horizontal scaling is safe under current maintenance design | Factual/evaluative | Supporting | C5 | Deployment limit, in-process lock and workload separation |
| C12 | The full proposed platform is necessary before the first useful release | Evaluative | Supporting | C1-C11 | Five candidate architectures, two refinement rounds, sensitivity analysis |

## Search families

- Agent Skills specification/client guide: schema extensions, compaction, activation deduplication, relative paths.
- MCP tools/versioning/security: structured outputs, error semantics, untrusted annotations, permission boundaries.
- xAI/Hermes/Gemini official docs: native installation, unsupported approval fields, tool and file access.
- Original SkillsBench and follow-on retrieval/failure studies: aggregate benefit, harmful/neutral cases, no-skill baseline, library scale, token cost.
- SLSA, TUF, GitHub attestations: artifact identity, authenticated provenance, downgrade/freeze, practical build support.
- LangGraph and AWS durable-execution docs: checkpoints, replay, retry and external effect semantics.
- OpenTelemetry official GenAI repository: existing skill attributes, maturity and content sensitivity.
- A2A primary protocol comparison: delegation versus distribution.

Searches deliberately included counterexamples to “skills always improve performance,” “thin adapters are sufficient,” and “another orchestration protocol is required.” Source families are grouped by upstream author/organization, not counted once per URL. Technical publisher docs establish documented behavior, not independent performance evidence.

## Local counterfactual probe

Hypothesis: search context is caller-isolated. Expected if true: a different caller's history is excluded from the current query's recent-skill seed.

Method: import server, replace registry/index/logging with fakes, call identical query twice with histories labeled agent-A and agent-B. Capture arguments supplied to the index. No real files, telemetry, model calls or deployments are changed by the probe.

Observed: each history is passed to `recent_skills` without caller filtering. Code also defines `session_id` as server-process UUID, explicitly shared by HTTP requests. Evidence: `output/audits/2026-10-09/deep-research/search-context-probe.json`.

Bounded conclusion: cross-consumer graph-ranking influence and unsuitable run attribution are possible under current implementation. The probe does not measure rank changes or demonstrate private data exfiltration.

## Method adaptations and limits

Official maintained references are assessed as normative primary evidence of current documented behavior, even when a publication date is absent; retrieval dates are stated and no publication dates invented. This adapts the source-triangulator's blanket treatment of undated pages, which would otherwise demote live specifications solely for lacking article-style dates. Such sources do not establish empirical efficacy. Benchmark papers remain scoped to their actual revisions, tasks and harnesses.

The research uses disclosed affiliations/source ownership to identify overlapping incentives. Funding not disclosed remains unknown; it is not treated as proof of independence or wrongdoing. No universal effectiveness claim receives a high-confidence label from vendor documentation.
