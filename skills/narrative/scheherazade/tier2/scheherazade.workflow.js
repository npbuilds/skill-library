export const meta = {
  name: 'scheherazade',
  description:
    'Tier-2 code-driven Scheherazade: a serialized scene loop that drafts a quality-gated chapter in an existing world (brownfield), gating each scene through consistency (HARD) → quality (SOFT) and the chapter through a macro judge, with a Spelunker-grounded back-edge for missing world. Canon is read-only; all writes land under a scratch run dir.',
  phases: [
    { title: 'Story loop', detail: 'serial: per beat → (back-edge) → draft → consistency → quality' },
    { title: 'Macro', detail: 'whole-story-judge over the accepted chapter' },
    { title: 'Commit', detail: 'promote accepted drafts + write run-journal (gated on macro pass + human sign-off)' },
  ],
}

// ─────────────────────────────────────────────────────────────────────────────
// Scheherazade Tier-2 driver (rev2 — serialized + gated). Code-reviewed: all gate
// accepts enforce their invariant, every agent() goes through ask() (budget check +
// null guard → __halt), and a top-level catch turns any halt into an escalation packet.
//
// Provenance: vault skill-lab/2026-06-27-scheherazade-tier2-scope.md (rev2). The scene
// loop is SEQUENTIAL (not pipeline()) — story scenes share canon + run in order, the side
// of the multi-agent line where parallelism cascades/conflicts.
//
// FS constraint: this body has NO filesystem access. The driver holds only paths + small
// metadata; every Read/Write happens inside an agent() call. Prose never enters memory.
// ─────────────────────────────────────────────────────────────────────────────

// ===== 1. VERDICT SCHEMAS — the machine-checkable contract ====================
// Discriminated (`status`) so cap-exhaustion can't flow on as a silent null. Evidence is
// LOCATED (source_path + line_locator + evidence_line) so the quote-verifier can confirm
// it is verbatim, not hallucinated.

const CONSISTENCY_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['status', 'violations'],
  properties: {
    status: { type: 'string', enum: ['pass', 'fail'] },
    violations: {
      type: 'array',
      items: {
        type: 'object',
        additionalProperties: false,
        required: ['rule_id', 'source_path', 'line_locator', 'evidence_line', 'fix', 'missing_world'],
        properties: {
          rule_id: { type: 'string', description: 'the canon rule/axiom violated, or a stable id' },
          source_path: { type: 'string', minLength: 1 },
          line_locator: { type: 'string', minLength: 1 },
          evidence_line: { type: 'string', description: 'the offending verbatim line from the DRAFT' },
          fix: { type: 'string', description: 'the smallest change that resolves the contradiction' },
          missing_world: {
            type: 'boolean',
            description: 'true if the contradiction is "the world lacks something this scene needs" (back-edge), not "the scene contradicts the world"',
          },
        },
      },
    },
  },
}

const QUALITY_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['status', 'dimensions', 'diagnosis', 'editor_handoff'],
  properties: {
    status: { type: 'string', enum: ['pass', 'fail'] },
    dimensions: {
      type: 'array',
      description: 'one entry per required rubric dimension for the medium profile',
      items: {
        type: 'object',
        additionalProperties: false,
        required: ['name', 'floor_met', 'source_path', 'line_locator', 'evidence_line'],
        properties: {
          name: { type: 'string' },
          floor_met: { type: 'boolean' },
          source_path: { type: 'string', minLength: 1 },
          line_locator: { type: 'string', minLength: 1 },
          evidence_line: { type: 'string', description: 'the verbatim line that justifies the floor_met call' },
        },
      },
    },
    diagnosis: { type: 'string', description: 'what specifically to fix; empty if status=pass' },
    editor_handoff: { type: 'string', description: 'the concrete instruction for prose-editor; empty if pass' },
  },
}

const MACRO_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['status', 'payoff', 'arc', 'causal', 'promise_kept', 'coherence', 'dropped_setups'],
  properties: {
    status: { type: 'string', enum: ['pass', 'fail'] },
    payoff: { type: 'string' },
    arc: { type: 'string' },
    causal: { type: 'string' },
    promise_kept: { type: 'string' },
    coherence: { type: 'string' },
    dropped_setups: {
      type: 'array',
      items: {
        type: 'object',
        additionalProperties: false,
        required: ['setup', 'source_path', 'line_locator', 'evidence_line'],
        properties: {
          setup: { type: 'string', description: 'the planted promise that was never paid off' },
          source_path: { type: 'string', minLength: 1 },
          line_locator: { type: 'string', minLength: 1 },
          evidence_line: { type: 'string', description: 'the verbatim line where the setup was planted (quote-auditable)' },
        },
      },
    },
  },
}

// The quote-verifier's report: which cited evidence_lines do NOT occur in their file.
const QUOTE_AUDIT_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['all_verified', 'fabricated'],
  properties: {
    all_verified: { type: 'boolean' },
    fabricated: {
      type: 'array',
      items: {
        type: 'object',
        additionalProperties: false,
        required: ['source_path', 'line_locator', 'claimed_line'],
        properties: {
          source_path: { type: 'string', minLength: 1 },
          line_locator: { type: 'string', minLength: 1 },
          claimed_line: { type: 'string' },
        },
      },
    },
  },
}

// The blind A/B improvement judge (reward-hacking break). The judge sees two unlabeled
// drafts and only says which is better — it is NOT told which is the revision, and the
// driver swaps the A/B slot each round to cancel position bias.
const IMPROVEMENT_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['which', 'reason'],
  properties: {
    which: { type: 'string', enum: ['A', 'B', 'tie'], description: 'which unlabeled draft is better as prose' },
    reason: { type: 'string' },
  },
}

// Back-edge: classify a missing-world stub so the builder knows where it belongs in the DAG.
const STUB_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['stubs'],
  properties: {
    stubs: {
      type: 'array',
      items: {
        type: 'object',
        additionalProperties: false,
        required: ['need', 'dag_stage', 'wants_grounding', 'generative'],
        properties: {
          need: { type: 'string', description: 'the world element the scene needs but the world lacks' },
          dag_stage: {
            type: 'string',
            enum: ['systems', 'geo', 'cultures', 'belief', 'factions', 'tech', 'history', 'revelation', 'characters'],
          },
          wants_grounding: { type: 'boolean', description: 'true if a real-world analog would ground it (economy/ecology/tech/governance/social)' },
          generative: { type: 'boolean', description: 'true if "how should X work?" (→ Spelunker agentic-researcher) vs "what are analogs for X?" (investigative)' },
        },
      },
    },
  },
}

const GROUNDING_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['brief_path', 'summary'],
  properties: {
    brief_path: { type: 'string', description: 'path under <scratch_root>/_research/ where the grounded brief was written' },
    summary: { type: 'string', description: '2-4 sentence grounded design the generator should honor' },
  },
}

const SCENE_REF_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['draft_path', 'scene_id', 'attempt_id', 'word_count', 'output_hash', 'input_hashes'],
  properties: {
    draft_path: { type: 'string' },
    scene_id: { type: 'string' },
    attempt_id: { type: 'string' },
    word_count: { type: 'integer' },
    output_hash: { type: 'string', description: 'content hash of the draft file written (cache key + journal)' },
    input_hashes: {
      type: 'array',
      items: { type: 'string' },
      description: 'content hashes of the canon/prior files read (so a changed vault invalidates cache)',
    },
  },
}

const COMMIT_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['committed_paths', 'journal_path', 'audit_clean'],
  properties: {
    committed_paths: { type: 'array', items: { type: 'string' } },
    journal_path: { type: 'string' },
    audit_clean: { type: 'boolean', description: 'false if any write landed OUTSIDE scratch_root' },
  },
}

// ===== 2. AGENT PROMPTS — wrappers around the existing skills ==================
// Each prompt tells the subagent to (a) load the relevant skill via the skill-library MCP
// `get_skill`, (b) do the file I/O, (c) return ONLY the schema object. Critics run under a
// different persona than the generator (self-preference guard).

const CANON_RULE = (world) =>
  `CANON IS READ-ONLY. You may READ from ${world}. You may WRITE ONLY under the scratch run dir given below. Never write under ${world}.`

// The committed world a reader must consult = canon (read-only) PLUS any world the back-edge
// built earlier this run. Readers that only looked at canon would never see a freshly built stub.
const WORLD_READ = (args) =>
  `the committed world — canon at ${args.world_state} (READ-ONLY) PLUS any world built this run under ${args.scratch_root}/committed/world/`

const HASH_RETURN =
  'Also return output_hash = a stable content hash (sha256 via a shell command, or a content digest) of the draft file you wrote, and input_hashes = the same kind of hash for each canon/prior file you read.'

function groundingPrompt(stub, args) {
  const route = stub.generative
    ? `This is a GENERATIVE design question — route through Spelunker's agentic-researcher branch to produce grounded candidate designs.`
    : `This is an INVESTIGATIVE question — use Spelunker's standard triangulation to find real-world analogs.`
  return `You are the grounding agent. Load the \`spelunker\` skill via get_skill and apply it at depth "standard" (NEVER "deep" — this runs inside a generation loop). ${route}
Question/stub: "${stub.need}" (DAG stage: ${stub.dag_stage}).
World context: read ${WORLD_READ(args)} so the grounding is consistent with what's already established.
${CANON_RULE(args.world_state)} Scratch run dir: ${args.scratch_root}
Write the grounded brief to ${args.scratch_root}/_research/ and return ONLY: {brief_path, summary}. The summary is the grounded design the worldbuilder must honor.`
}

function stubBuildPrompt(stub, grounding, args) {
  return `You are the world-builder for a back-edge stub. Load \`worldbuilding-orchestrator\` via get_skill and route to the right stage skill for DAG stage "${stub.dag_stage}".
Build: "${stub.need}".
${grounding ? `Honor this grounded design (do not contradict it): ${grounding.summary}` : ''}
Read ${WORLD_READ(args)} and keep the new element consistent with it (axioms, factions, systems).
${CANON_RULE(args.world_state)} Scratch run dir: ${args.scratch_root}
Write the new world element to ${args.scratch_root}/committed/world/ (the scratch world-state lane), append a line to ${args.scratch_root}/_log/generation-log.md, and return ONLY the absolute path you wrote (a plain string). The consistency critic will gate it next.`
}

function discoverStubsPrompt(beat, accepted, args) {
  return `You are the iceberg-test probe. Given the beat to be written next, decide what world it needs that may not exist yet (proactive back-edge).
Beat: ${JSON.stringify(beat)}
Read ${WORLD_READ(args)} and the accepted scenes so far: ${JSON.stringify(accepted.map((a) => a.path))}.
Return ONLY {stubs:[...]} — empty if the world already supports this beat. Only list a stub if the scene genuinely cannot be written truthfully without it. ${CANON_RULE(args.world_state)}`
}

function classifyStubsPrompt(findings) {
  return `Classify these missing-world findings into DAG stubs the builder can act on. Findings: ${JSON.stringify(findings)}. Return ONLY {stubs:[...]} per the schema.`
}

function gateStubPrompt(builtPath, args) {
  return `You are Critic-1 for a freshly built world element at ${builtPath}. Load \`worldbuilding-critic\` via get_skill. Audit it against ${WORLD_READ(args)} (axioms/systems). Cite verbatim lines (source_path + line_locator). Any violation ⇒ status:"fail". Return ONLY the CONSISTENCY schema. ${CANON_RULE(args.world_state)}`
}

function draftPrompt(beat, accepted, args) {
  return `You are the generator. Load \`prose-orchestrator\` via get_skill and draft ONE scene.
Beat / editorial brief: ${JSON.stringify(beat)}
Medium: ${args.medium}. Use the appropriate Voice Card from ${args.world_state}.
Iceberg rule: pull in ONLY the world-context a character needs in THIS scene — read it from ${WORLD_READ(args)}.
Continuity: these prior scenes are already accepted; stay consistent with their events. Read them: ${JSON.stringify(accepted.map((a) => a.path))}.
${CANON_RULE(args.world_state)} Scratch run dir: ${args.scratch_root}
Write the candidate to ${args.scratch_root}/drafts/ and return ONLY the SCENE_REF object. ${HASH_RETURN}`
}

function consistencyPrompt(ref, accepted, args) {
  return `You are Critic-1 (consistency) — a DIFFERENT persona than the writer. Load \`worldbuilding-critic\` and \`character-belief-tracker\` via get_skill.
Read the draft at ${ref.draft_path}. Read ${WORLD_READ(args)} and the accepted scenes ${JSON.stringify(accepted.map((a) => a.path))}.
Audit for: contradictions with canon (axioms/systems/factions), character-belief leaks across revelation layers, and continuity breaks vs accepted scenes.
For EVERY violation, cite the offending VERBATIM line from the draft with its source_path and line_locator. If a violation is really "the world lacks something this scene needs," set missing_world:true (routes to the back-edge, not a redraft).
HARD gate: any violation ⇒ status:"fail" with a non-empty violations array; a clean draft ⇒ status:"pass" with an EMPTY violations array. Return ONLY the CONSISTENCY schema object.`
}

function quoteAuditPrompt(evidenceList) {
  return `You are the quote-verifier. For each entry, open source_path and check whether claimed_line occurs VERBATIM at line_locator (whitespace-insensitive, but no paraphrase counts).
Entries: ${JSON.stringify(evidenceList)}
Return ONLY {all_verified, fabricated:[...]} listing every entry whose line was NOT found. A fabricated citation invalidates the verdict.`
}

function redraftPrompt(ref, violations, args) {
  return `You are the generator, revising for CONSISTENCY only (do not polish prose yet). Load \`prose-orchestrator\` via get_skill.
Read the draft at ${ref.draft_path}. Fix exactly these canon violations, making the SMALLEST change each:
${JSON.stringify(violations.map((v) => ({ rule: v.rule_id, line: v.evidence_line, fix: v.fix })))}
${CANON_RULE(args.world_state)} Write the revised candidate to ${args.scratch_root}/drafts/ as a NEW attempt and return ONLY the SCENE_REF object. ${HASH_RETURN}`
}

function qualityPrompt(ref, args) {
  return `You are Critic-2 (quality) — a DIFFERENT persona than the writer. Load \`quality-critic\` via get_skill and use the "${args.medium}" rubric profile.
Read the draft at ${ref.draft_path}. Judge the alive/earned axis, NOT conventional-vs-bold (that is the human's fork). For each REQUIRED dimension, cite a verbatim line that justifies your floor_met call (cite-or-fail). Steelman any patterned rule-break before failing it.
status:"pass" requires EVERY required dimension floor_met:true. Return ONLY the QUALITY schema object; on fail also fill diagnosis + editor_handoff.`
}

function editorPrompt(ref, handoff, args) {
  return `You are prose-editor. Load \`prose-editor\` via get_skill. Read the draft at ${ref.draft_path} and apply this targeted revision: ${handoff}
Do not introduce canon changes. ${CANON_RULE(args.world_state)} Write the revised attempt to ${args.scratch_root}/drafts/ and return ONLY the SCENE_REF object. ${HASH_RETURN}`
}

function improvementPrompt(aPath, bPath) {
  return `You are a blind A/B prose judge. Two unlabeled drafts of the same scene (you are NOT told which came first):
A: ${aPath}
B: ${bPath}
Read both. Which is better as prose on the alive/earned axis? Judge only the text; "tie" is allowed and is the honest answer when neither is clearly better. Return ONLY {which:"A"|"B"|"tie", reason}.`
}

function macroPrompt(accepted, args) {
  return `You are the macro judge. Load \`whole-story-judge\` via get_skill. Read the accepted chapter scenes in order: ${JSON.stringify(accepted.map((a) => a.path))}.
Judge the WHOLE: payoff realization, arc shape, causal connectivity, promise kept, global coherence. For each dropped setup, cite the verbatim line where it was planted (source_path + line_locator + evidence_line).
status:"fail" if a load-bearing setup is dropped or the arc/coherence breaks; a clean chapter ⇒ status:"pass" with an EMPTY dropped_setups array. Return ONLY the MACRO schema object. ${CANON_RULE(args.world_state)}`
}

function commitPrompt(accepted, macro, spent, args) {
  return `You are the committer + auditor. The chapter passed all gates (macro status: ${macro.status}).
1. Promote each accepted draft to ${args.scratch_root}/committed/prose/ (scratch lane — NOT canon). Accepted (path + output_hash): ${JSON.stringify(accepted)}
2. Append decisions + gate verdicts to ${args.scratch_root}/_log/generation-log.md.
3. Write ${args.scratch_root}/_log/run-journal.md: per-scene revision counts, the macro verdict, the cost so far (${spent} output tokens), and the output_hash + input_hashes for each scene.
4. AUDIT: collect every path written this run. Set audit_clean:false if ANY written path does NOT start with ${args.scratch_root} (that includes anything under ${args.world_state} or the project root). ${CANON_RULE(args.world_state)}
Return ONLY {committed_paths, journal_path, audit_clean}.`
}

// ===== 3. DRIVER HELPERS ======================================================

const DAG_ORDER = ['systems', 'geo', 'cultures', 'belief', 'factions', 'tech', 'history', 'revelation', 'characters']

function guardBudget(reserve = 30000) {
  // Pre-spawn check (P2-1/P3-1): refuse to start expensive work near the ceiling. `total === 0`
  // is a real ceiling (truthiness would skip it), and no ceiling ⇒ total is null ⇒ remaining() Infinity.
  if (budget.total !== null && budget.remaining() < reserve) {
    throw { __halt: true, reason: `budget ceiling reached (${Math.round(budget.remaining() / 1000)}k < ${reserve / 1000}k reserve). Journal up to this point persists.` }
  }
}

// Every spawn goes through ask(): budget-guarded, and a null return (user skip / agent death)
// becomes a __halt that the top-level catch converts into an escalation packet (P1-1/2/4/9/10, P2-1).
async function ask(prompt, opts) {
  guardBudget()
  const r = await agent(prompt, opts)
  if (r === null || r === undefined) {
    throw { __halt: true, reason: `agent "${(opts && opts.label) || '?'}" returned null (skipped or died) — human review needed` }
  }
  return r
}

// Returns true iff every cited evidence_line was found verbatim. Null-safe; a null verdict or a
// null/failed audit is treated as "not verified" so the caller re-judges rather than trusting it.
async function verifyQuotes(verdict) {
  if (!verdict) return false
  const items = verdict.violations || verdict.dimensions || verdict.dropped_setups || []
  const citing = items.filter((x) => x && 'evidence_line' in x)
  // A blank citation locator can't be verified — don't silently drop it (fix: empty-string bypass);
  // distrust the whole verdict so the caller re-judges.
  if (citing.some((x) => !x.source_path || !x.line_locator || !x.evidence_line)) {
    log('⚠ verdict has a blank citation locator — not trusted, re-judging')
    return false
  }
  if (!citing.length) return true
  const ev = citing.map((x) => ({ source_path: x.source_path, line_locator: x.line_locator, claimed_line: x.evidence_line }))
  guardBudget()
  const audit = await agent(quoteAuditPrompt(ev), { schema: QUOTE_AUDIT_SCHEMA, label: 'verify-quotes', phase: 'Story loop' })
  if (!audit) return false
  if (!audit.all_verified) log(`⚠ ${audit.fabricated.length} fabricated citation(s) — verdict not trusted, re-judging`)
  return audit.all_verified
}

async function drainStubs(stubs, args) {
  // Back-edge: build missing world FIRST, in DAG order, grounding the flagged ones (P1-4).
  if (!stubs || !stubs.length) return
  const sorted = [...stubs].sort((a, b) => DAG_ORDER.indexOf(a.dag_stage) - DAG_ORDER.indexOf(b.dag_stage))
  for (const stub of sorted) {
    let grounding = null
    if (stub.wants_grounding) {
      grounding = await ask(groundingPrompt(stub, args), { schema: GROUNDING_SCHEMA, label: `ground:${stub.dag_stage}`, phase: 'Story loop' })
    }
    const builtPath = await ask(stubBuildPrompt(stub, grounding, args), { label: `build:${stub.dag_stage}`, phase: 'Story loop' })
    const v = await ask(gateStubPrompt(builtPath, args), { schema: CONSISTENCY_SCHEMA, label: `gate-stub:${stub.dag_stage}`, phase: 'Story loop' })
    const honest = await verifyQuotes(v)
    if (!(honest && v.status === 'pass' && v.violations.length === 0)) {
      // P1-3: a stub that can't pass Critic-1 must STOP the beat, not silently feed the next draft.
      throw { __halt: true, reason: `stub "${stub.need}" failed Critic-1 — human review needed before the scene can proceed` }
    }
  }
}

// HARD gate. Accepts ONLY an honest, status:pass, zero-violation verdict (P1-7). Fabricated
// citations re-judge the same draft rather than redrafting from untrusted violations (P2-2).
// No unjudged candidate is ever returned (P3-2): the loop judges at the top each round.
async function consistencyGate(ref, accepted, args, cap = 3) {
  let cur = ref
  for (let t = 0; t <= cap; t++) {
    const v = await ask(consistencyPrompt(cur, accepted, args), { schema: CONSISTENCY_SCHEMA, label: `consistency:a${t}`, phase: 'Story loop' })
    const honest = await verifyQuotes(v)
    if (!honest) {
      if (t === cap) return { status: 'escalated', draft: cur, reason: 'fabricated consistency citations persisted to cap' }
      continue // re-judge the same draft (uses an attempt) — do not redraft from untrusted violations
    }
    if (v.violations.some((x) => x.missing_world)) {
      return { status: 'back_edge', stubsSource: v.violations.filter((x) => x.missing_world) }
    }
    if (v.status === 'pass' && v.violations.length === 0) return { status: 'ok', draft: cur, attempts: t }
    if (t === cap) return { status: 'escalated', draft: cur, reason: 'consistency cap reached' }
    cur = await ask(redraftPrompt(cur, v.violations, args), { schema: SCENE_REF_SCHEMA, label: `redraft:a${t + 1}`, phase: 'Story loop' })
  }
  return { status: 'escalated', draft: cur, reason: 'consistency cap reached' }
}

// One-shot consistency re-check (no redraft loop) used after a quality edit (P1-6).
async function checkConsistencyOnce(ref, accepted, args) {
  const v = await ask(consistencyPrompt(ref, accepted, args), { schema: CONSISTENCY_SCHEMA, label: 'reconsistency', phase: 'Story loop' })
  const honest = await verifyQuotes(v)
  return honest && v.status === 'pass' && v.violations.length === 0
}

// SOFT gate. Accepts ONLY honest + status:pass + every required dimension floor_met (P1-5/P1-8).
// The blind, position-swapped A/B judge freezes the scene if the prose didn't actually improve.
async function qualityGate(ref, args, cap = 3) {
  let cur = ref
  let edited = false
  for (let t = 0; t <= cap; t++) {
    const q = await ask(qualityPrompt(cur, args), { schema: QUALITY_SCHEMA, label: `quality:a${t}`, phase: 'Story loop' })
    const honest = await verifyQuotes(q)
    if (!honest) {
      // Never edit from an untrusted diagnosis (fix: QUALITY_UNTRUSTED_EDIT). Re-judge the same draft.
      if (t === cap) return { status: 'escalated', final: cur, edited, reason: 'fabricated quality citations persisted to cap' }
      continue
    }
    const floorsMet = q.dimensions.length > 0 && q.dimensions.every((d) => d.floor_met)
    if (q.status === 'pass' && floorsMet) return { status: 'ok', final: cur, attempts: t, edited }
    if (t === cap) return { status: 'escalated', final: cur, edited, reason: 'quality cap reached' }
    const revised = await ask(editorPrompt(cur, q.editor_handoff, args), { schema: SCENE_REF_SCHEMA, label: `edit:a${t + 1}`, phase: 'Story loop' })
    // Reward-hacking break (P2-9): confirm the PROSE improved, blind, slot-swapped to cancel position bias.
    const revisedIsB = t % 2 === 0
    const [A, B] = revisedIsB ? [cur.draft_path, revised.draft_path] : [revised.draft_path, cur.draft_path]
    const ab = await ask(improvementPrompt(A, B), { schema: IMPROVEMENT_SCHEMA, label: `improved?:a${t + 1}`, phase: 'Story loop' })
    const revisedWon = revisedIsB ? ab.which === 'B' : ab.which === 'A'
    if (!revisedWon) {
      log(`⚠ quality verdict moved but blind A/B says the revision isn't actually better — freezing (suspected reward-hacking)`)
      return { status: 'frozen', final: cur, attempts: t + 1, edited }
    }
    cur = revised
    edited = true
  }
  return { status: 'escalated', final: cur, edited, reason: 'quality cap reached' }
}

async function runScene(beat, accepted, args) {
  // Explicit null-checks so an intentional cap of 0 isn't coerced to 3 (fix: ZERO_REVISION_CAP_IGNORED).
  const cap = args.caps && args.caps.revisions != null ? args.caps.revisions : 3
  const qcap = args.caps && args.caps.quality_revisions != null ? args.caps.quality_revisions : 3
  const draft = await ask(draftPrompt(beat, accepted, args), { schema: SCENE_REF_SCHEMA, label: `draft:${beat.id || ''}`, phase: 'Story loop' })
  const c = await consistencyGate(draft, accepted, args, cap)
  if (c.status === 'back_edge') return { status: 'back_edge', stubsSource: c.stubsSource }
  if (c.status !== 'ok') return { status: 'escalated', reason: c.reason }
  const q = await qualityGate(c.draft, args, qcap)
  if (q.status === 'escalated') return { status: 'escalated', reason: q.reason }
  // P1-6: a quality edit can reintroduce a canon break — re-verify consistency on the final draft.
  if (q.edited && !(await checkConsistencyOnce(q.final, accepted, args))) {
    return { status: 'escalated', reason: 'quality edit reintroduced a canon violation' }
  }
  return {
    status: 'ok',
    accepted: { beat, path: q.final.draft_path, output_hash: q.final.output_hash, input_hashes: q.final.input_hashes },
    flagged: q.status === 'frozen',
  }
}

// ===== 4. ENTRY + THE LOOP (wrapped so any __halt becomes an escalation packet) ====

// The injected `args` global can arrive as a JSON STRING depending on how the caller passes it
// (e.g. a stringified value in the Workflow tool call). Normalize to an object before anything reads it.
const _args = typeof args === 'string' ? JSON.parse(args) : args || {}

if (!_args.scratch_root || !_args.world_state) {
  throw new Error('scheherazade: args must include world_state (read-only canon) + scratch_root (write lane)')
}

const accepted = []
const flags = []
try {
  // Sign-off commit fast-path (fix: SIGNOFF_REGENERATES). When the user re-invokes to approve,
  // commit the EXACT manifest they reviewed — never re-run the nondeterministic loop and commit
  // different prose. The caller passes back the `accepted` array from the awaiting_signoff result.
  if (_args.human_signoff && _args.commit_manifest) {
    phase('Commit')
    const signedCommit = await ask(commitPrompt(_args.commit_manifest, _args.macro || { status: 'pass' }, budget.spent(), _args), { schema: COMMIT_SCHEMA, label: 'commit+audit', phase: 'Commit' })
    if (!signedCommit.audit_clean) return { result: 'canon_breach', commit: signedCommit, note: 'a write landed outside scratch_root — investigate' }
    return { result: 'committed', commit: signedCommit, accepted: _args.commit_manifest, spent: budget.spent() }
  }

  phase('Story loop')
  const beats = _args.chapter_brief || []
  if (!beats.length) throw new Error('scheherazade: args.chapter_brief is empty — nothing to write')
  for (const beat of beats) {
    // Proactive back-edge: build world the beat needs before drafting.
    // beat.skip_probe lets a spine that has pre-built its world opt out (the reactive
    // back-edge in runScene still catches anything the probe would have).
    const probe = beat.skip_probe
      ? { stubs: [] }
      : await ask(discoverStubsPrompt(beat, accepted, _args), { schema: STUB_SCHEMA, label: `probe:${beat.id || ''}`, phase: 'Story loop' })
    await drainStubs(probe.stubs, _args)

    // Run the scene; a reactive back-edge (missing_world found post-draft) drains then retries.
    let outcome = await runScene(beat, accepted, _args)
    let backEdgeRetries = 0
    while (outcome.status === 'back_edge' && backEdgeRetries < 2) {
      const cls = await ask(classifyStubsPrompt(outcome.stubsSource), { schema: STUB_SCHEMA, label: 'classify-stubs', phase: 'Story loop' })
      await drainStubs(cls.stubs, _args)
      outcome = await runScene(beat, accepted, _args)
      backEdgeRetries++
    }

    if (outcome.status !== 'ok') {
      return { result: 'escalated', beat, accepted, flags, reason: outcome.reason || outcome.status, note: 'a scene could not pass its gates within caps — human review needed' }
    }
    accepted.push(outcome.accepted)
    if (outcome.flagged) flags.push(outcome.accepted.beat)
  }

  // ===== 5. MACRO GATE =======================================================
  phase('Macro')
  let macro
  for (let mt = 0; mt <= 1; mt++) {
    macro = await ask(macroPrompt(accepted, _args), { schema: MACRO_SCHEMA, label: `whole-story-judge:a${mt}`, phase: 'Macro' })
    if (await verifyQuotes(macro)) break // planted-setup citations check out
    // A hallucinated dropped-setup citation can't be trusted to fail (or pass) the chapter (fix: MACRO_AUDIT_DISCARDED).
    if (mt === 1) {
      return { result: 'escalated', reason: 'macro judge cited fabricated evidence on both attempts', macro, accepted, flags, spent: budget.spent(), note: 'human review needed' }
    }
  }
  if (macro.status !== 'pass' || macro.dropped_setups.length > 0) {
    return { result: 'macro_fail', macro, accepted, note: 'structural fix needed (dropped setup / arc / coherence) — no commit' }
  }

  // ===== 6. COMMIT (gated on macro pass + human sign-off) ====================
  // D3: this workflow RETURNS the macro verdict for human sign-off. To commit, the caller re-invokes
  // with args.human_signoff:true AND args.commit_manifest=<this accepted array> → the fast-path above
  // promotes the reviewed drafts. (human_signoff with NO manifest = a one-shot pre-approved run.)
  phase('Commit')
  if (!_args.human_signoff) {
    return { result: 'awaiting_signoff', macro, accepted, flags, spent: budget.spent(), note: 'macro passed — re-invoke with args.human_signoff:true AND args.commit_manifest set to this result\'s `accepted` array (also pass args.macro) to commit the reviewed drafts' }
  }
  const commit = await ask(commitPrompt(accepted, macro, budget.spent(), _args), { schema: COMMIT_SCHEMA, label: 'commit+audit', phase: 'Commit' })
  if (!commit.audit_clean) {
    return { result: 'canon_breach', commit, note: 'a write landed outside scratch_root — investigate before trusting this run' }
  }
  return { result: 'committed', commit, macro, accepted, flags, spent: budget.spent() }
} catch (e) {
  if (e && e.__halt) {
    return { result: 'escalated', reason: e.reason, accepted, flags, spent: budget.spent(), note: 'loop halted — human review needed' }
  }
  throw e
}
