# Portable Skill Library — revised implementation plan

Status: first implementation completed and validated locally; not deployed. Created: 2026-10-09. Scope updated: 2026-10-11. Implementation started: 2026-10-12. Research basis: [Spelunker deep brief](deep-research-2026-10-09.md).

## Current scope — minimal upkeep and drift prevention

This section supersedes the broader implementation sequence below. Author each field in one place; derive duplicated values and delivery outputs automatically. Keep Git as the single source of truth, standard skill files, the existing registry, and the existing MCP service. Avoid new manual bookkeeping or separately maintained skill variants.

1. **Synchronization:** derive duplicated registry fields, including declared versions, from skill files through the existing sync script; retain registry-only metadata in the registry and reject mismatches automatically.
2. **Complete delivery:** fix existing exports to include required supporting files and accurate dependency metadata; add individual supporting-file retrieval to MCP. Flag unresolved dependencies rather than claim an incomplete export is self-contained.
3. **Agent isolation:** remove implicit shared recent-history influence from anonymous searches and distinguish task attribution from server-instance identity.
4. **Automated consistency checks:** stamp generated outputs with their source revision, validate hashes and package completeness, and extend existing deployment convergence checks. Generate any added metadata rather than require another manually maintained catalog.
5. **Small portability pilot:** test three representative workflows through native files and MCP, including missing-capability behavior. Add a custom-system bridge when a specific consumer needs one.

First reviewable implementation: synchronization, export completeness, and agent isolation, with targeted tests. The website stays in place. Synchronization, export completeness, and isolation changes are implemented and validated locally. Deployment remains pending review.

## First implementation results — 2026-10-12

- Registry sync now derives declared versions (normalizing numeric major/minor values); corrected 22 mismatches without replacing registry-owned fields. Missing files also prevent a clean-sync report.
- Existing export command now copies non-hidden authored supporting files, preserves actual metadata, records source revision/working-tree state, and hashes file bytes. Symlinks fail explicitly. Related skills remain external and dependency validation is explicitly unverified; no automatic dependency resolver was added.
- MCP adds `list_skill_files` and `get_skill_file` for selective text/binary retrieval, with containment checks and a 256 KiB read limit. Minimal `get_skill` calls omit agent definitions as well as references.
- Search no longer reads shared recent usage as task context. Anonymous remote telemetry separates instance identity from per-event attribution; local stdio remains explicitly process-attributed.
- Codex source allowlist, updater validation, documentation, CI script checks, and generated infrastructure inventory reflect the new tools. Installed plugin and hosted service remain unchanged; deploy server first, then update the plugin.
- Validation: 142 MCP tests passed; 13 script suites passed; plugin configuration/manifest checks passed; registry sync, file-placement, and diff checks passed. The retrieval regression gate passed (curated recall@5 0.867; synthetic recall@5 0.760, within existing tolerance).
- Delivery smoke test: color-theory (4 files), design-orchestrator (10), and spelunker (6) produced matching native/MCP hashes for all authored files. The orchestrator reports 10 unbundled registry dependencies.

Remaining current-scope work: rollout and live convergence verification, plus a behavioral portability pilot covering actual host capabilities and missing-capability handling. The delivery smoke test does not establish cross-host execution equivalence. Broader features below remain deferred.

## Bug review and next checks — 2026-10-12

Fixed export replacement rollback, registry metadata incorrectly inherited by same-name external skills, and telemetry cap bypass caused by unique anonymous event IDs. File retrieval now uses a bounded read even if the file grows after its size check; listing hashes large assets without loading them entirely into memory.

Added real stdio and HTTP MCP integration tests for three representative skills. Both transports deliver bytes matching native exports, deny invalid paths, and report an unsupported execution tool as an error. This tests the retrieval contract and missing-tool behavior; it does not measure model-level workflow quality.

Deployment now bakes the validated source revision into the image, exposes it with the registry hash at `/health`, and verifies both after rollout. Existing Firestore convergence checks remain in place. No new manually authored catalog or extra service was introduced.

## Backlog — retained, not scheduled

These ideas remain available for later work. They are not prerequisites for the current scope and should be reconsidered when the listed need appears. The research detail below is retained for reference; it does not authorize expanding the immediate implementation.

| Backlog item | Revisit when |
|---|---|
| Automatic task resolver, abstention, and query-specific adaptation | The pilot shows selection is a material bottleneck; compare against explicit selection and no-skill baselines first |
| Rich capability/dependency manifests, deterministic dependency solver, and lockfiles | A real consumer needs constraints the current package metadata cannot express |
| Stable/experimental channels, atomic installers, rollback, provenance attestations, and local overlays | Consumers need independently pinned installations, third-party distribution, or preserved local customizations |
| Additional runtime adapters, HTTP API, language SDKs, and a custom loader | A named system cannot use native files or the existing MCP service |
| Broad compatibility qualification and larger behavioral evaluation suites | More runtimes or higher-stakes workflows justify coverage beyond the small pilot; prefer generated records |
| Activation ledger, compaction/resume support, effort budgets, and execution conflict checks | A target host needs explicit long-running workflow support |
| Expanded outcome telemetry and OpenTelemetry integration | Existing measurements cannot explain quality, cost, or integration failures |
| Incremental embeddings, content caching, maintenance separation, and horizontal scaling | Measured build cost, latency, or concurrency warrants the work; separate maintenance coordination before scale-out |
| Automated factual-freshness review and upstream-change monitoring | Time-sensitive skills or observed integration changes justify targeted review |
| Static website data generated from Git, offline/PWA support, and single-file HTML snapshots | Offline browsing, sharing, or website simplification becomes a concrete requirement |
| SQLite distribution or other local search formats | A custom consumer needs a queryable single-file data package |
| A2A, central execution service, or workflow engine | A consumer needs delegated execution rather than skill retrieval |
| Public marketplace, multi-tenant control plane, new vector database, or custom signing service | Concrete distribution, isolation, scale, or trust requirements exceed existing tools |

## Research design reference — broader scope, deferred

The following phases preserve the original research proposal. Items beyond the current scope above belong to the backlog, even where the original text describes them as requirements or acceptance criteria.

## Intended outcome

Connect a new agent system through native Agent Skills files, MCP, or a small application-side loader. Keep one canonical library. Publish what is readable, resource-complete, executable, and behaviorally qualified for a particular runtime/model/environment. Do not promise arbitrary agents will produce equivalent results.

A successful fourth integration should reuse the same release and conformance suite, without requiring changes to the canonical skills. This is an acceptance target, not a guarantee about systems with closed interfaces.

## Architecture boundary

```text
Canonical Git library + registry
              |
Validate -> resolve package dependencies -> build immutable release
              |
     manifest + file digests + index + provenance
          /                          \
Native directory bundles       shared retrieval core
                                      |
                              MCP / optional HTTP or SDK
          \                          /
          host capability and policy adapter
                       |
         host executes; records qualified outcomes
```

Library owns discovery, package identity, dependency closure, retrieval, and qualification records. Host owns authorization, credentials, tools, execution, cancellation, hard budgets, and durable task state. CI owns releases and maintenance. A future remote execution service would be a separate component.

## Phase 0 — identity, isolation, and baseline

**Work**

- Make remote anonymous search context-free. Remove the implicit shared usage-log seed from that path; optionally accept bounded request-local recent skill IDs.
- Separate instance/request/run/parent-run identity. Preserve legacy events as approximate historical attribution, rather than relabeling them as true user sessions.
- Normalize version metadata through the registry sync path; add immutable content identity. Preserve original author version text when normalization is ambiguous.
- Define supported behavior and existing tests before changing transport or SDK versions.

**Acceptance**

- Interleaving agent A and B requests cannot change B’s contextual search inputs unless B explicitly supplies that context. Content/index updates are tested separately.
- Fresh requests on different service instances use the same release/index and produce equivalent context-free retrieval results under the same configuration.
- A version mismatch is visible; a skill revision can be traced to a Git commit and package digest.

**Repository targets**: `mcp-server/server.py`, `shared.py`, `scripts/sync-registry.py`, related tests. Do not modify production settings as part of a read-only evaluation.

## Phase 1 — complete native releases

**Work**

- Replace hardcoded export metadata with validated registry/frontmatter values.
- Copy every owned asset required by a package: references, agent definitions, templates, scripts, examples, and eval metadata as appropriate. Avoid accidentally including nested child packages twice.
- Distinguish install-time `requires`, runtime `calls`, optional dependencies, and conceptual `related_to` links. The existing graph cannot be assumed to encode these meanings.
- Preserve the standard `SKILL.md` format. Add a separately versioned structured manifest for this library’s extensions.
- Generate portable native install layouts, resolving flat-name collisions explicitly. Keep a namespaced internal ID separate from a native client’s slug.
- Generate a lockfile for the complete selected dependency graph, file hashes, release digest, license/origin records, and local override identity.
- Install atomically; preserve local modifications through an explicit overlay or conflict report. No silent overwrite, missing required dependency, or mid-run channel update.

**Acceptance**

- Export `design-orchestrator` with its agent files and correct type/dependencies.
- A selected orchestrator and its required children work from an unpacked location outside this repository.
- Missing required files, case/path collisions, path traversal, symlink escape, unsupported major schema versions, incompatible constraints, and unbounded dependency cycles produce useful errors.
- `stable` resolves once to a digest; rollback selects a known-good complete release. A provenance check validates the intended source/builder, not merely the downloaded hash.
- Native-only clients can ignore the custom manifest and still read the standard package. Such clients are not represented as enforcing extension requirements unless their adapter does so.

**Repository targets**: `scripts/package-skill.sh` or a replacement Python builder under `scripts/`; schemas and libraries under an appropriate `mcp-server/` subdirectory; generated artifacts under `exports/` or `output/`; registry mutations through `scripts/sync-registry.py`.

## Phase 2 — bounded retrieval and a small adapter contract

**Minimum operations**

| Operation | Contract |
|---|---|
| `search` | Bounded candidates, release/index identity, explicit no-match, optional request-local context |
| `get_manifest` | Skill ID, versions/digests, dependencies, files/sizes, applicability, evaluation references |
| `get_file` | Skill-relative path within allowed package root; verified bytes/content type; explicit size/error behavior |
| `resolve_dependencies` | Deterministic closure from explicit skill IDs and constraints; lock or conflict report |

These are proposed operation names, not claims that the current server provides them. Keep existing tool names working through a compatibility layer. Do not require an LLM to resolve package dependencies.

**Host profile**

Record content/media support, maximum result size, filesystem locality, runnable languages/environment versions, available tools and result schemas, permission enforcement, context lifecycle hooks, and optional delegation. Validate actual capability semantics. The library’s declaration cannot grant permission.

Use a minimum text/JSON response profile; add artifact/multimodal profiles only when needed. Define structured errors such as `not_found`, `revision_unavailable`, `missing_dependency`, `capability_missing`, `permission_denied`, `budget_exceeded`, and `unsupported_media`. Distinguish tool execution failures from protocol errors; preserve equivalent meaning across interfaces.

**Acceptance**

- Selected files load individually, with stable resource identity, without reloading the whole reference set.
- A new unsupported client feature produces an explicit limited compatibility level or error.
- Duplicate activation is avoided; compaction/resume reloads the pinned instructions/resource base.
- Interrupted reads can retry; ambiguous side-effecting host operations require reconciliation or an idempotent sink rather than blind replay.
- The public retrieval server cannot silently become a remote execution or credential-proxy service.

## Phase 3 — qualify three integration classes

Use one native-file host, one MCP host, and a minimal custom loader. Pick concrete available systems at implementation time; Hermes and Grok remain examples rather than architectural dependencies.

**Starter cohort (proposed)**

Use approximately 12 held-out tasks spanning a knowledge skill, a text transformation, a reference-dependent workflow, an orchestrator, and a script/repository-dependent workflow. Include some tasks where no skill is appropriate. Manually review the expected outputs and preserve a held-out set; generated cases are supplemental.

Run the three arms from the research brief: no skill, explicit skill, and retrieved skill. Repeat runs using the same environment and resource ceilings. Add a fourth adaptation arm only after a stable selection baseline exists.

Measure task correctness, constraint adherence, evidence quality, actual tool execution, negative-trigger false activation, elapsed time, tokens, tool calls, and induced work. Use deterministic checks where possible and blinded rubric review where judgments are necessary. Do not allow a model grader’s stylistic preferences to become the only success criterion.

**Failure fixtures**

| Case | Required behavior |
|---|---|
| No relevant skill | Abstain without inventing a match |
| Required tool/reference absent | Explicit failure or declared, tested fallback |
| Context too small | Preserve mandatory instructions; request larger budget or use validated smaller variant |
| Conflicting project/default instructions | Apply host priority policy and report unresolved conflict |
| Duplicate names/local override | Deterministic resolution and visible provenance |
| Interrupted/resumed session | Same revision, recovered activation state, no unintended duplicate effects |
| Concurrent consumers | Isolated task context and attribution |
| Wrong environment/framework version | Exclude or flag incompatible package |
| Malformed/truncated/media-incompatible response | Typed error, no false completion |
| Modified or revoked release | Verify provenance/update policy and avoid silent substitution |

**Release gate**

Set per-cohort quality/cost tolerances before running evaluations. Do not invent a universal percentage threshold from other papers. A minimal release can be qualified for a limited skill subset; unresolved capabilities must remain visible. Update the qualification tuple after changes to skill hash, model, harness, adapter, or meaningful environment dependencies.

## Phase 4 — optional resolver, initially in shadow mode

The resolver recommends skill IDs; dependency resolution remains deterministic. Preserve explicit selection and allow user/host override. Filter applicability and permissions before ranking. Return reasons, alternatives, uncertainty/no-match, expected resource requirements, and a concrete pinned release.

Test ranking against the held-out three-arm baseline. Promote to automatic use only if it delivers useful quality/cost tradeoffs in its intended cohort. Add explicit exclusions and abstention calibration. Avoid promoting frequently loaded skills solely because they are frequently loaded.

Budget total work as well as context: recursion, tool calls, time, and any paid operations. An optional shorter execution mode must preserve the skill’s mandatory contract. Do not silently mutate canonical instructions to fit a query.

## Phase 5 — measured scale and maintenance

- Key embedding reuse by relevant skill bytes, reference-selection policy, chunker/model version, and synthetic-query inputs. Score-only changes must not force full content re-embedding.
- Keep immutable content caching independent of run context and any future authorization boundaries.
- Move maintenance jobs out of the read service or provide appropriate coordination before increasing replicas.
- Measure cold/warm latency, p95/p99 retrieval latency, result sizes, index build time, error rate, and cost at increasing skill count and concurrency. Use measured bottlenecks to decide on object storage/CDN, search backends, or additional instances.
- Separate structural freshness, source-fact review dates, runtime qualification, and deprecated APIs. Review affected skills after upstream changes; do not mass-refresh stable methodology based solely on age.
- Map skill/run events to OpenTelemetry where practical, with an internal schema version because GenAI conventions are still evolving. Omit raw prompts/results by default and retain the existing search-query redaction behavior.

## Defer until there is a concrete requirement

A2A, a universal workflow engine, public marketplace, multi-tenant control plane, new vector database, multiple language SDKs, automatic prompt rewriting, and a custom signing service. Keep extension boundaries, but avoid making the first portable release depend on these systems.

## Decisions the pilot should resolve

- Does native installation outperform the gateway for the selected hosts?
- Which skills supply utility over the host’s baseline, and which should remain explicit-only?
- What capability vocabulary is sufficient without pretending different tools are equivalent?
- Does automatic selection outperform explicit selection enough to justify its overhead?
- Which actual consumers need offline releases, private content, long-running execution, or artifacts?

The next concrete deliverable is the focused implementation described in **Current scope** above. The remaining research proposal stays on the backlog until a concrete need warrants it.
