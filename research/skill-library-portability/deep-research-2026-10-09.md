RESEARCH BRIEF
CORE CLAIM CONFIDENCE: Likely
Brief ID: SPK-20261009-univ01

Question: What is missing from the plan to make this skill library scalable and usable in arbitrary future agent systems?
Depth: deep. Date: 2026-10-09. Twelve propositions investigated; five architecture candidates compared; two design-refinement rounds; adversarial and counterfactual checks completed. Repository inspected at `460343b520ac2c0401c01fd8abeaf27a203354f8`.

The proposed shared core is a sound starting point, but the plan needs explicit compatibility levels, native packages, session lifecycle handling, caller-isolated context, and evidence that selection improves outcomes. “Loads successfully” cannot stand in for “works well.” The recommended next step is a small portability release with conformance tests, followed by an optional measured resolver. A universally effective execution layer remains unproven. [1][2][3][4][5]

This brief supersedes the implementation order suggested in the preceding conversation. It does not supersede the initial audit’s test results. Supporting evidence, claim decomposition, and implementation gates accompany this brief in the same directory.

KEY FINDINGS

- **Separate readable, resolvable, executable, and behaviorally qualified compatibility.** Standards establish formats/interfaces; runtime and empirical evidence expose additional constraints. Confidence: Likely because native-client behavior and cross-harness studies support the distinction. [1][2][3][6][7]
- **Native bundles should be a first-class interface; gateways should be optional.** Existing native skill clients already load directories. Confidence: Likely because Agent Skills, Gemini, and Hermes describe direct loading, although installation details vary. [1][2][6][8]
- **Evaluate the resolver before making it mandatory.** Curated-skill gains do not transfer automatically to retrieval from a large library. Confidence: Likely because controlled retrieval conditions materially change benchmark outcomes. [3][4]
- **Fix consumer isolation before encouraging concurrent use.** Current search reads shared recent usage, and telemetry’s session ID identifies the server process. Confidence: Likely because source inspection and a mock probe establish the unfiltered context path, without claiming a measured ranking or privacy incident. [5]
- **Add session, conflict, and effort contracts.** Compaction, version mismatches, permissions, and excessive procedures can defeat otherwise valid packages. Confidence: Likely because client guidance and empirical failures support these concrete missing cases. [2][7][9][10]
- **Make releases complete and verifiable, without building an unnecessary execution platform.** Provenance and update policy are different from a checksum; task delegation is different from content distribution. Confidence: Likely because release-verification and protocol specifications explicitly address those distinctions. [11][12][13]

DETAILED FINDINGS

**1. Keep the standards-compatible package; put richer contracts beside it.**

The Agent Skills specification defines `SKILL.md`, optional supporting directories, string-valued metadata, and experimental tool declarations. It does not standardize the proposed structured capability/dependency schema. Confidence: Likely because the normative fields are directly inspectable. Keep custom requirements in a separately versioned manifest, rather than implying every native client understands them. [1]

Proposed compatibility labels:

| Level | Claim permitted | Required evidence |
|---|---|---|
| Readable | Instructions load | Parser and identity checks |
| Resolvable | Required files and dependencies are available | Complete closure and path validation |
| Executable | Environment, tools, and authorization permit required steps | Runtime capability/policy checks |
| Qualified | Demonstrated useful on a defined task cohort | Recorded evaluations for exact skill/model/harness/environment versions |

These are proposed library labels, not an external certification. Qualification should expire or require revalidation after relevant changes. A text-only system can qualify for a reasoning skill without qualifying for a scripted or multi-agent workflow.

**2. Support native files, MCP, and a minimal application interface.**

Gemini and Hermes have native skill behavior; xAI can consume remote MCP, but its documented API does not support `require_approval`. Hermes installation also has discovery, precedence, and update semantics. Confidence: Likely because these are documented host differences. A shared protocol does not erase them. [6][7][8]

Recommended minimum interface: `search`, `get_manifest`, `get_file`, and `resolve_dependencies`. Provide native directory releases and the existing MCP interface first. Add an HTTP wrapper or SDK only for a real consuming application. A browser-only system may accept uploaded text but lack resource/tool execution; describe that as a limited profile rather than inventing compatibility.

MCP supports structured results, optional output schemas, resource links, and distinct tool/protocol error handling. Confidence: Likely because the tools specification defines these explicitly. Preserve those distinctions in adapter conformance tests, including a text/JSON fallback and unsupported-artifact behavior. [18]

The same capability label can hide different semantics: a web tool may return snippets or full source text; a filesystem may be local or sandboxed; delegation may have isolated or shared context. Proposed adapter checks should cover result shape, provenance, locality, limits, and policy—not just tool names. This is an engineering inference from documented differences. [2][6][7]

**3. Separate skill utility from selection quality.**

SkillsBench v4, dated June 14, reports 87 tasks and 18 model–harness configurations, with average pass rates of 33.9% without skills and 50.5% with curated skills. That supports potential value, not universal efficacy. The same paper discusses harness effects and scope limits. Confidence: Likely because these are directly reported results, not replicated here. [3]

A separate retrieval study uses approximately 34,000 skills. Its Claude SkillsBench condition reports 51.2% for curated skills, 35.4% without skills, and 40.1% when retrieving from a pool containing curated skills. Refinement helps some conditions but hurts another. Confidence: Likely because these controlled comparisons directly test selection/adaptation, while model–harness pairings and benchmark reuse limit generalization. [4]

Change the resolver contract: it may return `no_match`, `incompatible`, or `needs_clarification`; explicit skill selection remains available. Initially return ranked suggestions with reasons. Do not silently rewrite canonical instructions for each query. If adaptation is later tested, retain both original and adapted hashes and treat it as a distinct experimental condition.

Proposed three-arm evaluation, holding runtime, task, environment, and budget fixed:

| Arm | What it isolates |
|---|---|
| No skill | Host’s baseline capability |
| Explicit, preselected skill | Skill’s potential utility |
| Automatically retrieved skill | Routing and selection loss or benefit |

Include negative triggers, near-neighbor distractors, repeated runs, and uncertainty intervals. Compare artifact correctness and cost as well as formatting. A large library must be allowed to say that it has nothing useful for a task.

**4. Budget induced work, not just prompt tokens.**

SWE-Skills-Bench reports limited aggregate improvement and environment-version conflicts, but it uses one principal runtime/model configuration and has many ceiling tasks. The August failure analysis attributes many selected efficiency regressions to extra procedure, including unnecessary verification; its cases are not a deployment failure-rate estimate. Confidence: Likely because the studies identify concrete mechanisms with explicit sampling limits. [9][10]

Add proposed effort profiles with maximum elapsed time, tool calls, recursion depth, and context allocation. Mark steps as mandatory, conditional, or optional; preserve necessary evidence standards. Host-enforced limits should stop or return partial results when exhausted. Do not cut mandatory instructions mid-section to satisfy a token count. A smaller variant must be authored and evaluated, not assumed equivalent.

**5. Preserve activation through compaction and resume.**

The Agent Skills client guide addresses activation deduplication, compaction protection, and relative resource resolution. Confidence: Likely because these are explicit client responsibilities, beyond initial retrieval. [2]

Maintain a proposed activation record with skill ID, release digest, loaded resource hashes, resource base, execution mode, and completed stages. A resumed session rehydrates the same revision. Pin `stable` to a concrete release at task start; do not switch versions mid-workflow. Persist user-authorized task state separately from reusable methodology.

For side-effecting workflows, define retry and cancellation behavior at the host. LangGraph documents scoped checkpoints, and AWS’s durable-execution guidance distinguishes retry semantics and notes that they do not imply exactly-once execution across a workflow. Confidence: Likely because these are independent implementation references for persistence/replay concerns. Do not implement a new scheduler inside the library merely to describe these requirements. [14][15]

**6. Fix a specific isolation gap in this repository.**

`server.py:485` reads the shared usage log; `server.py:497` passes its recent skill names into search without caller filtering. `server.py:34` defines a process-wide session ID. The isolated probe changed only fake history labeled agent-A versus agent-B and observed different history seeds passed for the same query. Confidence: Likely because code and probe agree. This establishes shared contextual inputs, not the size of any rank change or private data exfiltration. [5]

Recommended immediate policy: anonymous remote searches are context-free by default. If a caller explicitly supplies recent skill IDs for its own task, treat them as request-local hints. Do not treat a claimed caller ID as authentication. Keep shared content caches separate from user/task context; private caches, if later added, require authorization-scoped keys. Introduce distinct server-instance, request, run, and parent-run IDs.

**7. Complete identity and release lifecycle.**

The prior audit reproduced incomplete exports and found 22 substantive registry/content version discrepancies. SLSA describes verification of provenance against trusted expectations; TUF distinguishes rollback/freeze and inconsistent-update threats. Confidence: Likely because the local findings and normative references support separate content identity, trusted origin, and update state. [5][11][12]

Proposed release requirements: namespace plus stable skill ID; schema version separate from skill version; full dependency/file digest closure; license and origin; environment constraints; explicit deprecation/replacement; install lockfile; atomic installation; known-good rollback. Support strict required dependencies and separately optional calls. Cycles require explicit bounded recursion or rejection, not unlimited traversal.

A digest proves equality to an expected digest, not trust in the source that supplied it. For this single-owner repository, begin with pinned Git releases and verified CI provenance. GitHub supports artifact attestations, so a custom signing service is unnecessary initially. Broader third-party auto-updates could later justify a stronger update framework. This is a staged design recommendation, not a claim that signatures validate instruction quality. [11][12][16]

**8. Reuse telemetry conventions; keep raw content optional.**

Current OpenTelemetry GenAI conventions include skill name, source URI, and resource-name attributes, but the agent conventions remain marked Development and warn that content may be sensitive. Confidence: Likely because the current official repository defines these fields and their maturity. [17]

Map to those conventions behind a versioned internal event schema. Add skill digest, release, adapter/harness/model versions, outcome, tokens, latency, tool calls, and failure category. Record selection separately from loading and completion. Preserve the existing default of omitting remote raw search text; adding `resolve(task=...)` must not reintroduce raw task logging by accident. [5]

**9. Scale content distribution before adding distributed execution.**

The deployment limits the service to one instance, maintenance uses an in-process lock, and the embedding cache hashes the entire registry. Confidence: Likely because these are direct code/config observations. No load test was run, so no capacity limit or latency improvement is claimed. [5]

Recommended changes: cache immutable files by digest, rebuild embeddings from per-skill content/model/chunker inputs, prebuild release indexes, and separate maintenance from the read service before raising instance limits. Keep the first implementation as one codebase with clear boundaries. Add object storage/CDN or a larger search backend only when measurements justify them.

A2A describes peer-agent delegation while MCP connects tools/resources. Confidence: Likely because the protocol authors state the boundary. Defer A2A and a central executor until a consumer needs the library service to perform work rather than supply instructions. [13]

**10. Candidate comparison and revised recommendation.**

Hard requirements: preserve the canonical source; support more than one integration class; disclose missing capabilities; preserve host policy. The following scores are explicit engineering judgments, not measured results. Scale 1–5; weights: host reach 30%, behavior control 25%, maintenance simplicity 20%, reproducibility 15%, offline operation 10%.

| Candidate | Reach | Behavior | Simplicity | Reproducibility | Offline | Weighted |
|---|---:|---:|---:|---:|---:|---:|
| Native file distribution alone | 4 | 2 | 5 | 4 | 5 | 3.80 |
| MCP-only gateway | 4 | 3 | 4 | 2 | 1 | 3.15 |
| HTTP API/SDK as primary interface | 3 | 3 | 3 | 4 | 4 | 3.25 |
| Central execution service | 2 | 4 | 1 | 4 | 1 | 2.50 |
| Native releases + MCP + optional adapters + qualification | 5 | 4 | 3 | 5 | 5 | 4.35 |

Grounding: the candidates correspond to native clients, the existing MCP service, standard application-side retrieval, or delegated-agent architectures. Confidence: Speculative for the comparative ranking because the weights and expected operating costs are judgments, not local comparative trials. [1][2][5][13]

Refinement round 1: repair the hybrid’s complexity by removing mandatory task resolution, API proliferation, and central execution. Keep a small common retrieval core plus native releases. Refinement round 2: add compatibility labels, session state requirements, and staged qualification; do not try to encode every possible tool capability before testing representative hosts. Stop after two rounds because further additions do not resolve an observed requirement without new consumer evidence.

Sensitivity: for local-only hosts, plain native bundles can win on simplicity. For remote-only clients, MCP may be sufficient. If consumers need remote execution rather than instruction reuse, a separate executor becomes relevant. No architecture can guarantee equivalent outcomes from arbitrary models or bypass a host’s lack of extension hooks.

EVIDENCE MAP

Claim IDs refer to the accompanying method document. Counterfactual checks tested the following signatures of failure; both positive and negative evidence were retained.

| Claim | Two counterfactual signatures sought | Observation | Disposition |
|---|---|---|---|
| C1 Common package substrate | Native clients require incompatible main files; package resources cannot be represented | Common SKILL.md support found, but richer contracts absent | Narrow common-core claim Likely; custom manifest explicitly separate [1][6][8] |
| C2 Format equals behavior | Same content varies by harness; valid skills hurt task success | Both documented/reported | Broad claim not supported; qualification becomes separate [3][9] |
| C3 Automatic selection adds value reliably | Retrieval loses curated gains; refinement reduces performance | Both appear in retrieval experiments | Universal claim not supported; resolver default deferred [4] |
| C4 Tool-name adapter suffices | Approvals differ; active instructions need compaction handling | Both documented | Narrow translation retained; lifecycle/policy tests added [2][7] |
| C5 Consumers are isolated | Other history enters search; run IDs identify a shared process | Both observed locally | Isolation claim rejected; fix precedes concurrent rollout [5] |
| C6 Versions/hashes fully specify execution | Incomplete closure; trusted origin/update state is unspecified | Local export drift plus verification requirements | Claim not supported; release lock and provenance added [5][11][12] |
| C8 More procedure always helps | Extra checks raise cost; compatible-looking guidance conflicts with project versions | Selected failure cases document both | Universal claim not supported; effort and conflict tests added [9][10] |
| C11 More replicas can be enabled directly | Coordination is process-local; search personalization is instance-local | Both found | Scale serving only after separating state/maintenance [5] |

Backpropagation: the preferred design remains a hybrid distribution layer, but its universal-behavior claim is withdrawn. A mandatory resolver and central executor no longer follow from the evidence. The recommendation to pilot the smaller design is Speculative until locally measured; bounded missing-requirement findings remain Likely.

Source independence: the two Agent Skills pages are one source family. MCP/A2A are protocol-owner perspectives, not runtime outcome tests. Vendor docs establish their own documented interfaces. Retrieval and failure papers reuse some SkillsBench/SWE-Skills tasks, so they are not independent replications on new task distributions. Affiliations are recorded in the evaluation evidence; complete funding disclosure and all author overlaps were not established. No wrongdoing or independence is inferred from missing disclosure.

GAPS & LIMITATIONS

- No published study evaluates this exact 537-skill library. Expected quality lift, optimal router, and acceptable regression thresholds remain unknown until local trials.
- No live Grok/Hermes/Gemini model trials, production load test, or paid model evaluation was run. Runtime documentation is not a conformance certificate.
- Study results are primary source reports, not reproduced measurements. Coding/terminal benchmarks do not establish creative, regulated, long-running, or multi-agent efficacy.
- The local probe demonstrates the search-context path using mocks; it does not quantify rank changes, cross-user outcomes, or data exposure.
- Maintained docs sometimes lack publication dates. Access dates and versioned spec dates are supplied; this is explicitly treated as normative evidence, not time-stamped experimental evidence. Some legacy documentation URLs redirect.
- Complete licensing of every bundled reference and third-party material was not audited. Before broader redistribution, preserve provenance and review actual asset licenses.
- No exhaustive standard defines arbitrary domain capability semantics. The proposed manifest is a library extension, and the minimum useful vocabulary must be learned from adapters.

CONFIDENCE SUMMARY

Confirmed: no universal portability or effectiveness claim meets the strict three-independent-source rule here.
Likely: missing compatibility/lifecycle requirements, documented protocol differences, and bounded local isolation/release findings, because direct primary evidence supports them.
Speculative: architecture scores, local performance gains, implementation economics, and exact rollout thresholds, because they require local experiments.
Contested: no aggregate label used to imply that different benchmark conditions are a direct scientific disagreement; universal improvement is explicitly not supported by counterexamples.
Unverifiable: universal future-system compatibility and this library’s untested runtime/model performance.

Overall: moderate confidence in the missing-requirement findings; lower confidence in predicted benefits of the proposed implementation. Deep-mode adversarial checks completed; no claim of exhaustive coverage of all future systems.

SOURCES

All accessed 2026-10-09. “Publication date not stated” is not an invented publication date. Primary maintained technical references are Tier 1 normative evidence under the documented method adaptation; original preprints are Tier 2 empirical evidence unless peer review is established. Neither category implies independent replication.

1. [Agent Skills specification](https://agentskills.io/specification). Publication date not stated; live specification. Tier 1. Used for: standard package scope, extension boundary, native substrate.
2. [Agent Skills client implementation](https://agentskills.io/client-implementation/adding-skills-support). Publication date not stated; live guide. Tier 1. Used for: activation, compaction, resource resolution and native/application integration.
3. [SkillsBench v4](https://arxiv.org/html/2602.12670v4). Revised 2026-06-14. Tier 2. Used for: curated-skill benefit, harness variation and benchmark scope.
4. [How Well Do Agentic Skills Work in the Wild, v1](https://arxiv.org/html/2604.04323v1). 2026-04-06. Tier 2. Used for: retrieval degradation and nonuniform refinement effects.
5. Local source snapshot `460343b`, initial audit, and `output/audits/2026-10-09/deep-research/search-context-probe.json`; inspected 2026-10-09. Tier 1. Used for: current registry/export findings, `server.py:29–34, 482–497`, telemetry, cache and deployment/maintenance design. Supporting report: `audit-2026-10-09.md`.
6. [Gemini CLI Agent Skills](https://geminicli.com/docs/cli/skills/). Publication date not stated; live docs. Tier 1. Used for: native activation and permissions as a distinct runtime lifecycle.
7. [xAI Remote MCP Tools](https://docs.x.ai/developers/tools/remote-mcp). Publication date not stated; live docs. Tier 1. Used for: remote integration and unsupported approval parameter.
8. [Hermes Skills System](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills/). Publication date not stated; live docs. Tier 1. Used for: native installation, package discovery and update behavior.
9. [SWE-Skills-Bench v1](https://arxiv.org/html/2603.15401v1). 2026-03-16. Tier 2. Used for: marginal benefit, framework mismatch and evaluation limits.
10. [Agent Skills Can Be Harmful v1](https://arxiv.org/html/2608.11888v1). 2026-08-12. Tier 2. Used for: procedural overhead and selected failure-attribution evidence.
11. [SLSA v1.2: Verifying artifacts](https://slsa.dev/spec/v1.2/verifying-artifacts). Version 1.2; page date not stated. Tier 1. Used for: identity, trusted builder expectations and verification.
12. [TUF security model](https://theupdateframework.io/docs/security/). Publication date not stated; maintained reference. Tier 1. Used for: update-state, rollback/freeze and consistency distinctions.
13. [A2A and MCP](https://a2a-protocol.org/latest/topics/a2a-and-mcp/). Publication date not stated; current protocol guide. Tier 1. Used for: delegation versus distribution boundary.
14. [LangGraph persistence](https://docs.langchain.com/oss/python/langgraph/persistence). Publication date not stated; live docs. Tier 1. Used for: thread-scoped checkpoints and resume semantics.
15. [AWS durable execution: idempotency and retries](https://docs.aws.amazon.com/durable-execution/patterns/best-practices/idempotency/). Publication date not stated; live docs. Tier 1. Used for: side-effect replay and retry guarantees.
16. [GitHub artifact attestations](https://docs.github.com/en/actions/how-tos/secure-your-work/use-artifact-attestations/use-artifact-attestations). Publication date not stated; live docs. Tier 1. Used for: existing provenance tooling rather than custom signing infrastructure.
17. [OpenTelemetry GenAI agent/framework conventions](https://github.com/open-telemetry/semantic-conventions-genai/blob/main/docs/gen-ai/gen-ai-agent-spans.md). Development snapshot, accessed 2026-10-09. Tier 1. Used for: existing skill attributes, maturity and content sensitivity.

18. [MCP tools specification](https://modelcontextprotocol.io/specification/2026-07-28/server/tools). Version dated 2026-07-28. Tier 1. Used for: structured outputs, resources, errors and adapter conformance.

NEXT STEPS

Follow `revised-plan-2026-10-09.md`: first stabilize identity and caller context; then ship a complete native package plus bounded MCP retrieval; qualify the package on three integration classes; evaluate the resolver in shadow mode; scale serving only after workload measurements. Keep canonical skill edits scoped to demonstrated issues.

The first milestone should prove that the same pinned skill set loads with complete references and behaves acceptably in a native-file host, an MCP host, and a minimal custom loader. Do not make delivery contingent on building every future adapter.

─────────────────────────────────────
Was this brief useful? Reply `/feedback spelunker <1-5> [optional notes]` to log.
Brief ID: SPK-20261009-univ01 · Calibrate later: `/calibrate <brief_id> <claim_id> <true|false|partial>`
