# Interoperability evidence — Spelunker Wave 1

Research date: 2026-10-09. Primary documentation reviewed live. This is documentary evidence, not an execution test. Findings concern the proposed architecture rather than an additional repository audit.

## Finding 1: Maintain a standards-compatible core and an explicitly private extension schema

**Likely (high confidence).** Agent Skills standardizes a directory, `SKILL.md`, optional supporting files, and limited frontmatter. `metadata` is a string-to-string map; `compatibility` is free text; `allowed-tools` is experimental. It does not provide the proposed typed dependency/capability resolver contract. Put richer structured requirements in a separate versioned manifest, linking it from namespaced metadata if necessary. Do not describe a custom manifest as universally supported.

Evidence: [Agent Skills specification](https://agentskills.io/specification), frontmatter, metadata, compatibility, and allowed-tools sections. This is normative documentation for the format, not independent evidence of runtime compliance.

Counterevidence to unnecessary adapter work: a standards-compatible instruction-only directory already works in multiple native skill clients; every client does not require a gateway.

## Finding 2: Capability names are insufficient; adapters must carry execution and permission semantics

**Likely (high confidence).** xAI remote MCP accepts Streaming HTTP/SSE and allows tool filtering, but its documented Responses API integration does not support `require_approval` or `connector_id`. Therefore a successful MCP handshake does not prove equivalent permission behavior. Treat capability availability, credentials, authorization policy, filesystem locality, and side effects as distinct checks. Do not infer authorization from a skill's declaration.

Evidence: [xAI Remote MCP](https://docs.x.ai/developers/tools/remote-mcp), SDK support and configuration. If `allowed_tools` is omitted, all server tool definitions enter context; a small allowlisted retrieval surface is valuable.

Independent corroboration: [Gemini CLI skills](https://geminicli.com/docs/cli/skills/) describes activation consent and directory access, demonstrating a materially different activation lifecycle. Test adapter permissions explicitly rather than promising identical behavior.

## Finding 3: Package install layout and update ownership require conformance tests

**Likely (high confidence).** Hermes taps discover direct skill subdirectories, and install supporting directories. It supports native OS filtering and gives bundles precedence on slug collisions; missing bundle members are skipped. Its bundled-skill updater tracks origin hashes to distinguish local edits. These are client semantics that a general “download bundle” API cannot assume.

Evidence: [Hermes Skills System](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills/), platform-specific skills, bundles, GitHub taps, and bundled skill updates. For this repository's domain-nested layout, generate a native install view with collision checks rather than assume tapping the repository root discovers everything.

Recommended test: install two same-name skills, modify one locally, upgrade the release, and confirm deterministic precedence, conflict reporting, and preservation of edits. Package dependencies must fail clearly when required; Hermes bundle skipping must not become silent success for a mandatory workflow dependency.

## Finding 4: Session lifecycle is missing from a retrieval-only contract

**Likely (high confidence).** The Agent Skills integration guide covers compaction protection, activation deduplication, deterministic name precedence, and resolving references relative to skill roots. These concerns occur after retrieval. A capability adapter needs hooks or a documented fallback for session resume/compaction, active revision identity, and resource access.

Evidence: [Agent Skills client implementation](https://agentskills.io/client-implementation/adding-skills-support), steps 1, 4, and 5. It recommends protecting active instructions from pruning and avoiding duplicate activation. Subagent execution is explicitly optional.

Recommendation (inference): maintain a session activation ledger `(skill ID, revision, resource base, activation state)` and rehydrate pinned instructions after context loss. Do not blindly trim mandatory steps to satisfy a token budget; return an explicit over-budget result or a validated smaller variant.

## Finding 5: Add explicit protocol profiles and artifact/error contracts

**Likely (high confidence).** MCP offers structured outputs and optional output schemas, multiple content types, resource links, pagination, and distinct protocol versus execution errors. A plain HTTP/CLI mirror must preserve these semantics, not merely return the same prose. The specification recommends serialized JSON text alongside structured results for backward compatibility.

Evidence: [MCP tools specification, 2025-11-25](https://modelcontextprotocol.io/specification/2025-11-25/server/tools), Tool Result, Structured Content, Output Schema, and Error Handling.

Recommendation (inference): define a minimum text/JSON profile plus optional artifact/multimodal profiles. Test missing resources, expired credentials, schema failure, truncation, and unsupported media. Distinguish “skill loaded” from “executable here.” Record actual supported features instead of only `mcp: true`. Include deterministic resource identifiers and hashes in every adapter's response.

## Finding 6: Keep delegated execution separate from skill distribution

**Likely (high confidence).** A2A describes communication between autonomous peer agents, including shared tasks and richer exchanges; MCP primarily integrates tools/resources inside an agent application. Neither guarantees that retrieved instructions execute correctly.

Evidence: [A2A and MCP comparison](https://a2a-protocol.org/latest/topics/a2a-and-mcp/), horizontal/vertical layers and protocol comparison.

Recommendation (inference): defer A2A until a consumer needs another service to perform the work rather than load the skill. Adding A2A now would increase infrastructure without establishing portable local execution. If that requirement arrives, expose a separate execution service with task lifecycle and artifacts; do not turn the read-only library into an implicit remote agent.

## What this changes in the plan

1. Ship native Agent Skills bundles plus an optional gateway; avoid mandatory network dependence for already compatible clients.
2. Define compatibility tiers: readable, resources resolvable, executable, behaviorally tested. Publish the tested runtime/model/version matrix.
3. Add session lifecycle and policy/permission semantics to adapter conformance.
4. Keep richer manifests explicitly library-specific until standardized; version their schemas separately from skills.
5. Test installation, collisions, local edits, compaction, errors, and artifact access in addition to happy-path task success.
6. Defer delegated-service protocols until needed.

## Independence and uncertainty

Five separate primary-source families: Agent Skills, xAI, Nous/Hermes, Google/Gemini, MCP; A2A supplies a sixth protocol-design perspective. The two Agent Skills pages are one source family, not independent corroboration. Vendor docs establish documented behavior, not independently measured performance. No live agent integrations were run. Universal behavioral equivalence is **Speculative**; “thin adapters suffice” is supportable only for a declared compatibility tier and tested skill subset.
