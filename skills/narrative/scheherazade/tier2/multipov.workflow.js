export const meta = {
  name: 'multipov-chapter',
  description: 'Multi-POV chapter production: N blind Rashomon generators against a frozen spine, per-POV gate pipelines, cross-POV + corpus-memory barrier critics with single-scene repair, macro judge',
  whenToUse: 'When a chapter renders ONE event through multiple POVs coordinated by a spine document (Gate-2-approved). For serialized multi-scene chapters use scheherazade.workflow.js instead — POVs-of-one-event parallelize; scenes-in-sequence do not.',
  phases: [
    { title: 'Generate+Gate', detail: 'per-POV: generate → consistency (HARD, cap revisions) → quality (SOFT, cap revisions); POV chains independent' },
    { title: 'Barrier', detail: 'cross-POV coherence (HARD) + corpus-memory (SOFT) over the whole suite; single-scene repair + single-check re-run on failure' },
    { title: 'Macro', detail: 'whole-story-judge over the assembled suite' },
  ],
}

// ---- args normalization (the injected args global can arrive as a JSON string) ----
let A = args
if (typeof A === 'string') { A = JSON.parse(A) }
if (!A || !A.spine_path || !Array.isArray(A.povs) || A.povs.length < 2 || !A.scratch_root || !A.vault) {
  throw new Error('args must include: spine_path, vault, scratch_root, povs[>=2] ({pov, title, out_file, character_files[], extra_reading[]}), and optionally caps, corpus_globs, skills_root, word_range')
}
const CAPS = Object.assign({ consistency: 3, quality: 3, repair: 2 }, A.caps || {})
for (const k of Object.keys(CAPS)) { if (!CAPS[k] || CAPS[k] < 1) CAPS[k] = 3 }
const SKILLS = A.skills_root || 'skills'
const WORDS = A.word_range || '1,800-2,600'
const CORPUS = (A.corpus_globs && A.corpus_globs.length) ? A.corpus_globs.join(' + ') : (A.vault + '/Drafts/*.md + ' + A.vault + '/WIP/prose/*.md')
const journal = { runs: [], cures: [], escalations: [] }

// ---- budget-guarded agent wrapper: a dead/skipped agent halts the run cleanly ----
async function ask(prompt, opts) {
  if (budget.total && budget.remaining() < 20000) { throw new Error('__halt:budget') }
  const r = await agent(prompt, opts)
  if (r === null || r === undefined) { throw new Error('__halt:agent-died:' + ((opts && opts.label) || 'unlabeled')) }
  return r
}

const VERDICT = {
  type: 'object',
  properties: {
    verdict: { type: 'string', enum: ['PASS', 'REJECT', 'FAIL'] },
    findings: { type: 'string', description: 'evidence-anchored findings, verbatim quotes' },
    cure_set: { type: 'string', description: 'if not PASS: the minimal cures, exact lines, per file' },
  },
  required: ['verdict', 'findings'],
}
const MACRO_VERDICT = {
  type: 'object',
  properties: {
    verdict: { type: 'string', enum: ['PASS', 'MACRO_FAIL'] },
    findings: { type: 'string' },
    structural_notes: { type: 'string' },
    next_chapter_needs: { type: 'string' },
  },
  required: ['verdict', 'findings'],
}

const DISCIPLINE = 'Judging discipline per ' + SKILLS + '/_shared/critic-core.md: evidence-anchored (verbatim quotes), reason before verdict, steelman before FAIL.'
const RASHOMON = 'FORBIDDEN READING: ' + A.vault + '/Drafts/ and ' + A.vault + '/WIP/prose/ and every other POV\'s scene file — the Spine carries every cross-scene fact you need; invent locally only what stays local to your station.'

function scenePath(p) { return A.scratch_root + '/' + p.out_file }

function genPrompt(p) {
  return 'You are a PROSE GENERATOR for the Nokaren novel — write ONE scene file: the ' + p.pov.toUpperCase() +
    ' POV ("' + p.title + '").\n\nMANDATORY READING, in order:\n1. THE SPINE (frozen truth — every pin is binding, especially render-ownership, the knowledge-matrix rules for your POV, your §C brief with its HARD LEXICON and budgets, and §D suite bans): ' + A.spine_path +
    '\n2. Character truth: ' + (p.character_files || []).join(' · ') +
    '\n3. Voice contract: ' + A.vault + '/_meta/voice-house.md (your mutation is in your Spine brief)' +
    '\n4. Texture canon: ' + (p.extra_reading || []).join(' · ') +
    '\n\n' + RASHOMON +
    '\n\nLength ' + WORDS + ' words. Title line (# ' + p.title + '), then pure prose — no frontmatter, no notes.' +
    '\nWrite the scene to: ' + scenePath(p) +
    '\nYour final message: the file path, word count, and a 3-line self-check naming which banned moves you verified absent. Nothing else.'
}

function consistencyPrompt(p) {
  return 'You are the CONSISTENCY CRITIC (Critic-1, HARD gate). Audit ONE scene against the frozen Spine and canon. REJECT or PASS. Read your method skill first: ' + SKILLS + '/worldbuilding/worldbuilding-critic/SKILL.md. ' + DISCIPLINE +
    '\n\nTHE DRAFT: ' + scenePath(p) +
    '\nAUDIT AGAINST, in priority order: (1) THE SPINE (binding contract — §A world-facts + pins, §B knowledge rules for this POV, §C render-ownership, §D bans): ' + A.spine_path +
    '; (2) CANON: ' + [A.vault + '/World-Bible/world-axioms.md'].concat(p.extra_reading || [], p.character_files || []).join(' · ') +
    '\nClassify every invented specific as canon-consistent extrapolation or contradiction. Check knowledge rules line-by-line (no early knowledge, no leaked signals). Return verdict REJECT on any real contradiction, with the minimal cure set (exact lines).'
}

function qualityPrompt(p) {
  return 'You are the QUALITY CRITIC (Critic-2, SOFT gate) judging ONE scene of literary fantasy. Consistency already PASSED — judge alive/earned only. Read your method skill completely first: ' + SKILLS + '/writing/revision-craft/quality-critic/SKILL.md plus its references. LITERARY profile. ' + DISCIPLINE + ' Steelman-before-FAIL; test function not form; never judge bold-vs-safe.' +
    '\n\nTHE DRAFT: ' + scenePath(p) +
    '\nVOICE CONTRACT: ' + A.vault + '/_meta/voice-house.md + the POV brief (§C) and suite budgets (§D) in ' + A.spine_path + ' — enforce the lexicon budgets as quality matters.' +
    '\nCharacter truth: ' + (p.character_files || []).join(' · ') +
    '\nAlso rule: is this POV a distinct nervous system, or the house voice in a mask? Return verdict FAIL only on floor-gate failure; put optional polish in findings (it becomes human forks, not revisions).'
}

function revisePrompt(p, cures, gateName) {
  return 'You are the REVISION HAND for the ' + p.pov + ' scene at ' + scenePath(p) + '. The ' + gateName + ' gate rejected it with this cure set:\n\n' + cures +
    '\n\nApply the MINIMAL cures with Edit — change nothing else; the rest of the scene already passed other gates. Respect the Spine (' + A.spine_path + ') §C brief and §D bans while curing. Your final message: a list of the exact edits made. Nothing else.'
}

// ---- Phase 1: per-POV pipeline, chains independent, no cross-barrier ----
phase('Generate+Gate')
const results = await pipeline(
  A.povs,
  (p) => ask(genPrompt(p), { label: 'gen:' + p.pov, phase: 'Generate+Gate' }).then(() => p),
  async (p) => {
    for (let i = 0; i < CAPS.consistency; i++) {
      const v = await ask(consistencyPrompt(p), { label: 'consistency:' + p.pov + ':a' + (i + 1), phase: 'Generate+Gate', schema: VERDICT })
      journal.runs.push({ pov: p.pov, gate: 'consistency', attempt: i + 1, verdict: v.verdict })
      if (v.verdict === 'PASS') { return p }
      if (!v.cure_set) { throw new Error('__halt:consistency-reject-no-cure:' + p.pov) }
      journal.cures.push({ pov: p.pov, gate: 'consistency', cure: v.cure_set })
      await ask(revisePrompt(p, v.cure_set, 'consistency'), { label: 'cure:consistency:' + p.pov, phase: 'Generate+Gate' })
    }
    journal.escalations.push({ pov: p.pov, gate: 'consistency', reason: 'cap exhausted' })
    throw new Error('__halt:consistency-cap:' + p.pov)
  },
  async (p) => {
    for (let i = 0; i < CAPS.quality; i++) {
      const v = await ask(qualityPrompt(p), { label: 'quality:' + p.pov + ':a' + (i + 1), phase: 'Generate+Gate', schema: VERDICT })
      journal.runs.push({ pov: p.pov, gate: 'quality', attempt: i + 1, verdict: v.verdict })
      if (v.verdict === 'PASS') { return { pov: p.pov, file: scenePath(p), forks: v.findings } }
      if (!v.cure_set) { return { pov: p.pov, file: scenePath(p), forks: v.findings, subfloor: true } }
      journal.cures.push({ pov: p.pov, gate: 'quality', cure: v.cure_set })
      await ask(revisePrompt(p, v.cure_set, 'quality'), { label: 'cure:quality:' + p.pov, phase: 'Generate+Gate' })
    }
    journal.escalations.push({ pov: p.pov, gate: 'quality', reason: 'cap exhausted — escalate, do not ship silently' })
    return { pov: p.pov, file: scenePath(p), escalated: true }
  }
)
const scenes = results.filter(Boolean)
if (scenes.length !== A.povs.length) { return { result: 'escalated', reason: 'a POV chain died', journal } }
if (scenes.some((s) => s.escalated)) { return { result: 'escalated', reason: 'quality cap exhausted on: ' + scenes.filter((s) => s.escalated).map((s) => s.pov).join(', '), journal } }

// ---- Phase 2: barrier — both suite critics genuinely need all scenes ----
phase('Barrier')
const fileList = A.povs.map((p) => scenePath(p)).join('\n')
function crossPovPrompt() {
  return 'You are the CROSS-POV COHERENCE CRITIC (HARD gate, suite-level). N POV scenes of ONE event were generated blind against a shared Spine; audit them AGAINST EACH OTHER: physical-fact identity (any fact rendered twice must be identical), clock agreement (build the merged timeline), knowledge-matrix compliance across scenes (the Spine §B/§F ignorance contract), register pins. Perspective differences are legitimate; fact differences are not. ' + DISCIPLINE +
    '\n\nTHE SCENES:\n' + fileList + '\nTHE CONTRACT: ' + A.spine_path +
    '\nReturn REJECT on any incompatible fact, with a cure set naming WHICH FILE deviates from the Spine (prefer curing the deviator; if both comply but differ, name the cheaper edit).'
}
function corpusPrompt() {
  return 'You are the CORPUS-MEMORY CRITIC (SOFT gate, suite-level): audit the new suite against each other AND the existing prose corpus for tic budgets, duplicate moves, and cross-POV idiom bleed. Method: ' + DISCIPLINE + ' + the analysis method of ' + SKILLS + '/writing/revision-craft/style-analyzer/SKILL.md.' +
    '\n\nTHE NEW SUITE:\n' + fileList + '\nTHE CORPUS: ' + CORPUS + '\nTHE BUDGETS (enforce as written): ' + A.spine_path + ' §D.' +
    '\nCount every budgeted move with quotes; sweep openings, closings, and distinctive phrases against the corpus; check per-POV lexicon walls. FAIL only on exceeded budget or verbatim-grade duplication; near-misses are advisories in findings.'
}
async function runBarrierCheck(name, promptFn) {
  for (let i = 0; i <= CAPS.repair; i++) {
    const v = await ask(promptFn(), { label: name + ':a' + (i + 1), phase: 'Barrier', schema: VERDICT })
    journal.runs.push({ gate: name, attempt: i + 1, verdict: v.verdict })
    if (v.verdict === 'PASS') { return v }
    if (i === CAPS.repair || !v.cure_set) { journal.escalations.push({ gate: name, reason: 'repair cap or no cure' }); return null }
    journal.cures.push({ gate: name, cure: v.cure_set })
    // single-scene repair: one hand applies the named cures, then ONLY this check re-runs
    await ask('You are the REPAIR HAND for a suite-level ' + name + ' rejection. Cure set (names the file(s) and exact lines):\n\n' + v.cure_set +
      '\n\nApply the minimal edits with Edit to the named file(s) only, under the Spine (' + A.spine_path + ') §C briefs and §D bans. Final message: exact edits made.', { label: 'repair:' + name, phase: 'Barrier' })
  }
  return null
}
const barrier = await parallel([
  () => runBarrierCheck('cross-pov', crossPovPrompt),
  () => runBarrierCheck('corpus-memory', corpusPrompt),
])
if (!barrier[0]) { return { result: 'escalated', reason: 'cross-POV coherence unresolved within repair cap', journal } }
if (!barrier[1]) { journal.escalations.push({ gate: 'corpus-memory', reason: 'soft gate unresolved — shipping with flag, human decides' }) }

// ---- Phase 3: macro ----
phase('Macro')
const order = (A.assembly_note || 'assembly order = the povs array order') + '\n' + fileList
const macro = await ask('You are the WHOLE-STORY JUDGE (macro gate) at CHAPTER level. Read your method skill first: ' + SKILLS + '/writing/revision-craft/whole-story-judge/SKILL.md. ' + DISCIPLINE + ' Honor the subversion guard (a transformed payoff is not a dropped plant).' +
  '\n\nTHE CHAPTER (read in assembly order):\n' + order +
  '\nTHE CONTRACT: ' + A.spine_path + ' — audit §E plants item by item and §F macro contract clause by clause. Judge: one event with an arc, or parallel exercises? Every ignorance-piece survives? Any removable block (= structural flaw)? What does the next chapter structurally need?',
  { label: 'macro', phase: 'Macro', schema: MACRO_VERDICT })
journal.runs.push({ gate: 'macro', verdict: macro.verdict })
if (macro.verdict === 'MACRO_FAIL') {
  return { result: 'macro_fail', diagnosis: macro.findings, structural_notes: macro.structural_notes || '', journal }
}
return {
  result: 'awaiting_signoff',
  scenes: scenes.map((s) => ({ pov: s.pov, file: s.file, quality_forks: s.forks })),
  macro: { findings: macro.findings, structural_notes: macro.structural_notes || '', next_chapter_needs: macro.next_chapter_needs || '' },
  corpus_memory_flag: barrier[1] ? null : 'unresolved — review before staging',
  journal,
}
