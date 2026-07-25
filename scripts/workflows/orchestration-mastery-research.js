export const meta = {
  name: 'orchestration-mastery-research',
  description: 'Deep research: the HUMAN skill of orchestrating AI agents — competency model, mastery rubrics, deliberate practice, management transfer, market signal, failure modes',
  phases: [
    { title: 'Research', detail: '6 tracks x 3 finder angles, then per-track synthesis' },
    { title: 'Verify', detail: 'adversarial refutation of critical claims, 2 lenses each' },
    { title: 'Synthesize', detail: 'assemble eight-section spelunker-format report body' },
  ],
}

const DATE = args.date
const BRIEF_ID = args.briefId

const TRACKS = [
  {
    key: 'competency',
    question: 'What distinct sub-skills does 2025-2026 evidence identify for HUMANS directing AI agents effectively? (candidates: task decomposition, verification/eval design, context management, delegation calibration, feedback-loop design, spec/prompt authoring, architecture judgment) What do expert practitioners report as the load-bearing skills?',
    angles: [
      'Practitioner accounts: engineering blog posts, conference talks, and essays by heavy agent users (Anthropic engineering blog, Claude Code power users, Simon Willison, Cursor/Devin/Copilot workflow writeups, "how I work with agents" essays 2025-2026). Extract the skills THEY say matter.',
      'Academic and industry HCI/human-factors literature on human-AI teaming, supervisory control of autonomous systems, and human-agent interaction (CHI/CSCW/HAI papers 2023-2026, Microsoft/Google/Anthropic research on developer-agent collaboration).',
      'Vendor curricula and official guidance: Anthropic Academy / AI Fluency framework, OpenAI Academy, Google/Microsoft agentic-AI courses, enterprise enablement guides — what skills do the companies building agents teach humans?',
    ],
  },
  {
    key: 'rubrics',
    question: 'What existing rubrics, maturity models, competency frameworks, or eval instruments exist for assessing HUMANS at directing AI agents (not for evaluating the agents)? What distinguishes expert from novice in observed practice?',
    angles: [
      'AI fluency / AI literacy frameworks with named dimensions (e.g. Anthropic AI Fluency: Delegation, Description, Discernment, Diligence; UNESCO/OECD AI literacy; academic AI-literacy scales with psychometrics).',
      'Expert-vs-novice empirical studies: prompt engineering skill studies, developer productivity studies with AI assistants (METR RCT 2025, GitHub/Microsoft studies), observed differences between heavy effective users and ineffective users.',
      'Enterprise agentic-AI maturity models (consultancies, vendors) and any certification/assessment schemes for agent-management or AI-collaboration skill.',
    ],
  },
  {
    key: 'practice',
    question: 'What does skill-acquisition science prescribe for building expertise in a young, ill-structured domain with no established pedagogy — and what are the documented pitfalls of self-designed rubrics and self-assessment?',
    angles: [
      'Deliberate practice research: Ericsson core findings AND boundary conditions/critiques (Macnamara et al. meta-analyses; domains where deliberate practice explains little; what deliberate practice requires: immediate feedback, defined subskills, effortful reps at edge of ability).',
      'Expertise in ill-structured domains: Dreyfus skill-acquisition model, Schoen reflective practitioner, cognitive flexibility theory (Spiro), naturalistic decision making (Klein), adaptive expertise vs routine expertise — how experts form when the domain lacks stable rules.',
      'Self-assessment pitfalls: Dunning-Kruger and its critiques, calibration training, criterion drift in self-designed rubrics, rubric design best practice (anchored behavioral rating scales), and journaling/after-action-review evidence as feedback substitutes.',
    ],
  },
  {
    key: 'management',
    question: 'How much of human agent-orchestration skill is isomorphic to existing managerial/delegation science and supervisory-control practice? What transfers cleanly and what breaks with AI agents?',
    angles: [
      'Delegation and management science: span of control research, situational leadership, trust-but-verify management patterns, how new managers learn to stop doing and start directing (management-transition literature, e.g. "The First 90 Days", Drucker, manager-of-managers scaling).',
      'Human supervisory control of automation: Sheridan supervisory control theory, air traffic control and incident-command staffing/attention models, function allocation, levels of automation (Parasuraman/Sheridan/Wickens) — quantitative findings on how many autonomous units one human can supervise.',
      'What breaks with AI agents specifically: trust calibration with imperfect automation (Lee & See), differences between delegating to humans vs to LLM agents (no theory of mind, non-stationary capability, verbose plausibility), 2024-2026 commentary on managing agents vs managing people.',
    ],
  },
  {
    key: 'market',
    question: 'Is human agent-orchestration capability rewarded in the 2025-2026 labor market — as a standalone skill or as a multiplier on domain expertise? What is the evidence from roles, hiring language, and compensation?',
    angles: [
      'Job-market data: role titles (AI orchestrator, agent engineer, forward-deployed engineer, AI operations), posting volumes, salary data 2025-2026 (LinkedIn, Indeed, levels.fyi commentary, a16z/sequoia hiring commentary).',
      'Institutional reports: WEF Future of Jobs 2025, McKinsey/BCG agentic-AI workforce reports, LinkedIn emerging-jobs and skills-of-the-future reports — what do they say about human agent-management skills?',
      'Domain-expertise multiplier: evidence that domain experts (medicine/biotech/finance) who direct AI outperform either pure AI-skill generalists or non-AI domain experts; healthcare+AI hiring signals; "AI will not replace you, someone using AI will" evidence quality.',
    ],
  },
  {
    key: 'failure',
    question: 'What are the documented failure modes of humans delegating to AI/automation — and the evidenced mitigations? (over-verification/attention-capping, abdication/rubber-stamping, automation complacency, deskilling, infra rabbit-holes)',
    angles: [
      'Automation complacency and automation bias literature (Parasuraman & Manzey, aviation/clinical decision support findings), vigilance decrement, and 2025-2026 evidence of AI-induced deskilling (e.g. the 2025 endoscopy/colonoscopy deskilling study, GPS/navigation deskilling analogies, education studies).',
      'Practitioner postmortems and studies of agent-workflow failures: over-trust/rubber-stamping of agent output, review fatigue with AI-generated code (2025-2026 studies on PR review quality), the METR finding that devs were slower with AI while believing they were faster, verification collapse at scale.',
      'Evidenced mitigations: verification/eval design, staged autonomy ladders, checklists (Gawande evidence), calibrated trust interventions, after-action reviews, sampling-based QA instead of full review — what actually works to keep the human effective.',
    ],
  },
]

const CONFIDENCE_RULES = 'Confidence vocabulary (spelunker framework): Confirmed = 2+ independent sources agree OR one primary/peer-reviewed source directly establishes it; Likely = one good source or consistent secondary sources; Speculative = weak/anecdotal; Contested = credible sources disagree; Unverifiable = no evidence could be found either way. Source tiers: Tier 1 = peer-reviewed research, official primary docs, or primary data; Tier 2 = reputable secondary reporting or practitioner accounts with evidence; Tier 3 = blogs, vendor marketing, anecdote.'

const FINDINGS_SCHEMA = {
  type: 'object',
  required: ['findings'],
  properties: {
    findings: {
      type: 'array',
      items: {
        type: 'object',
        required: ['claim', 'detail', 'sources', 'confidence', 'critical'],
        properties: {
          claim: { type: 'string', description: 'One-sentence specific claim' },
          detail: { type: 'string', description: '2-4 sentences with key numbers, names, dates' },
          sources: {
            type: 'array',
            items: {
              type: 'object',
              required: ['title', 'url', 'tier'],
              properties: {
                title: { type: 'string' },
                url: { type: 'string' },
                publisher: { type: 'string' },
                date: { type: 'string' },
                tier: { type: 'integer', minimum: 1, maximum: 3 },
              },
            },
          },
          confidence: { type: 'string', enum: ['Confirmed', 'Likely', 'Speculative', 'Contested', 'Unverifiable'] },
          critical: { type: 'boolean', description: 'true if this claim would materially shape a competency model or practice plan' },
        },
      },
    },
  },
}

const TRACK_SYNTH_SCHEMA = {
  type: 'object',
  required: ['track_summary', 'key_claims', 'durable_principles', 'gaps'],
  properties: {
    track_summary: { type: 'string', description: '4-8 sentence synthesis of what the track established' },
    key_claims: FINDINGS_SCHEMA.properties.findings,
    durable_principles: { type: 'array', items: { type: 'string' }, description: 'Principles likely stable across tool churn' },
    gaps: { type: 'array', items: { type: 'string' }, description: 'What could not be established' },
  },
}

const VERDICT_SCHEMA = {
  type: 'object',
  required: ['refuted', 'reasoning'],
  properties: {
    refuted: { type: 'boolean' },
    reasoning: { type: 'string', description: '2-4 sentences' },
    counter_evidence: { type: 'string', description: 'URL/title of counter-evidence if any, else empty string' },
    suggested_confidence: { type: 'string', enum: ['Confirmed', 'Likely', 'Speculative', 'Contested', 'Unverifiable'] },
  },
}

function finderPrompt(track, angle) {
  return 'You are one finder agent in a multi-agent deep-research workflow (date: ' + DATE + '). The research subject is the HUMAN skill of orchestrating AI agents — how a person becomes expert at directing fleets of AI agents. Explicitly OUT of scope: agent frameworks, architectures, tools, or benchmarks of the agents themselves (already researched elsewhere).\n\nTRACK QUESTION: ' + track.question + '\n\nYOUR ASSIGNED SEARCH ANGLE (stay in this lane; other agents cover other angles): ' + angle + '\n\nUse web search extensively (if WebSearch/WebFetch are not loaded, load them via ToolSearch first). Run at least 4-6 distinct searches with varied phrasing. Prefer primary sources; open the actual source when a claim is load-bearing. Return 4-8 substantive findings.\n\n' + CONFIDENCE_RULES + '\n\nRules: every claim must name its evidence (real URLs you actually saw — never fabricate a source); include concrete numbers/names/dates in detail; mark critical=true only for claims that would materially shape a competency model, rubric, or practice plan for a human learning agent orchestration. Your final output is consumed programmatically via the structured output tool.'
}

function synthPrompt(track, found) {
  return 'You are the synthesis agent for one track of a deep-research workflow on the HUMAN skill of orchestrating AI agents (date: ' + DATE + ').\n\nTRACK QUESTION: ' + track.question + '\n\nBelow are raw findings from 3 finder agents who searched different angles. Merge duplicates (keep the union of their sources), re-assess confidence per the rules (a claim two finders found independently via different sources strengthens to Confirmed), discard findings with fabricated-looking or missing sources, and select the 4-7 KEY claims for this track. Keep each claim one sentence, specific, with its merged sources array. Mark critical=true where a claim should shape the competency model / rubric / practice plan. Also extract durable_principles (statements likely to survive tool churn 2023-2028) and gaps (what the finders could not establish).\n\n' + CONFIDENCE_RULES + '\n\nRAW FINDINGS (JSON):\n' + JSON.stringify(found, null, 1)
}

function refutePrompt(claim, lens) {
  const lensDesc = lens === 0
    ? 'EVIDENCE-QUALITY lens: check whether the cited sources actually support the claim as stated — open the sources if possible, look for misreading, cherry-picking, vendor motivation, retraction, or replication failure.'
    : 'OVERGENERALIZATION lens: check whether the claim overreaches its evidence — wrong population, outdated context, survivorship bias, or a contested literature presented as settled. Search for credible sources that disagree.'
  return 'You are an adversarial verifier in a deep-research workflow (date: ' + DATE + '). Your job is to try to REFUTE the following claim. Default to refuted=true if, after genuine effort, the evidence does not hold up as stated; refuted=false only if the claim survives your attack (possibly with a downgraded suggested_confidence).\n\n' + lensDesc + '\n\nUse web search (load WebSearch/WebFetch via ToolSearch if needed).\n\nCLAIM: ' + claim.claim + '\nDETAIL: ' + claim.detail + '\nCLAIMED CONFIDENCE: ' + claim.confidence + '\nCITED SOURCES: ' + JSON.stringify(claim.sources) + '\n\n' + CONFIDENCE_RULES
}

async function runTrack(track) {
  const finders = await parallel(track.angles.map((angle, i) => () =>
    agent(finderPrompt(track, angle), { label: 'find:' + track.key + ':' + (i + 1), phase: 'Research', schema: FINDINGS_SCHEMA, effort: 'medium' })
  ))
  const found = finders.filter(Boolean).flatMap(r => r.findings)
  log('track ' + track.key + ': ' + found.length + ' raw findings from ' + finders.filter(Boolean).length + '/3 finders')
  const synth = await agent(synthPrompt(track, found), { label: 'synth:' + track.key, phase: 'Research', schema: TRACK_SYNTH_SCHEMA, effort: 'high' })
  return { track: track.key, question: track.question, rawCount: found.length, synth }
}

phase('Research')
const trackResults = (await parallel(TRACKS.map(t => () => runTrack(t)))).filter(Boolean)

const allClaims = trackResults.flatMap(r => (r.synth && r.synth.key_claims ? r.synth.key_claims : []).map(c => ({ ...c, track: r.track })))
const norm = s => s.toLowerCase().replace(/[^a-z0-9 ]/g, '').slice(0, 90)
const seen = new Set()
const deduped = []
for (const c of allClaims) {
  const k = norm(c.claim)
  if (!seen.has(k)) { seen.add(k); deduped.push(c) }
}
const criticalAll = deduped.filter(c => c.critical)
const byTrack = {}
for (const c of criticalAll) { (byTrack[c.track] = byTrack[c.track] || []).push(c) }
const critical = Object.values(byTrack).flatMap(list => list.slice(0, 4)).slice(0, 24)
if (criticalAll.length > critical.length) log('balanced verification: ' + critical.length + ' of ' + criticalAll.length + ' critical claims (up to 4 per track) — remainder carry track-synth confidence unverified')
log('claims: ' + allClaims.length + ' raw, ' + deduped.length + ' deduped, ' + critical.length + ' critical -> adversarial verify')

phase('Verify')
const verified = await parallel(critical.map((c, ci) => () =>
  parallel([0, 1].map(lens => () =>
    agent(refutePrompt(c, lens), { label: 'refute' + (lens === 0 ? 'A' : 'B') + ':' + c.track + ':' + (ci + 1), phase: 'Verify', schema: VERDICT_SCHEMA, effort: 'medium' })
  )).then(vs => {
    const votes = vs.filter(Boolean)
    const refutes = votes.filter(v => v.refuted).length
    const verdict = votes.length === 0 ? 'unverified' : refutes === votes.length ? 'refuted' : refutes > 0 ? 'contested' : 'survived'
    return { ...c, verdict, votes }
  })
))
const vOK = verified.filter(Boolean)
const tallies = {
  finderAgents: trackResults.length * 3,
  tracks: trackResults.length,
  rawFindings: trackResults.reduce((a, r) => a + r.rawCount, 0),
  dedupedClaims: deduped.length,
  criticalVerified: vOK.length,
  survived: vOK.filter(v => v.verdict === 'survived').length,
  contested: vOK.filter(v => v.verdict === 'contested').length,
  refuted: vOK.filter(v => v.verdict === 'refuted').length,
}
log('verify done: ' + tallies.survived + ' survived / ' + tallies.contested + ' contested / ' + tallies.refuted + ' refuted of ' + tallies.criticalVerified)

phase('Synthesize')
const reportBody = await agent(
  'You are the final synthesis agent of a deep-research workflow (date: ' + DATE + ', brief ID: ' + BRIEF_ID + ') on the HUMAN skill of orchestrating AI agents. The consumer is an experienced practitioner (MD, biotech, builder of a 528-skill Claude library) designing a deliberate-practice plan: a competency model of 5-7 sub-skills with rubric anchors, a self-audit, a project ladder, and a scoring loop.\n\nWrite the BODY of a research report in this EXACT section structure (markdown, ## headings, uppercase titles):\n\n## CORE CLAIM CONFIDENCE\nOne confidence tag in bold, then a 3-5 sentence assessment of the core claim: "Human agent-orchestration mastery is a definable, practicable competency — its sub-skills can be named, rubric-anchored, and trained through scored reps — and it functions in the labor market primarily as a multiplier on domain expertise." Assess honestly against the evidence, including which parts are weaker.\n\n## KEY FINDINGS\n7-9 numbered findings, each: bold one-sentence claim, [Confidence] tag, one supporting sentence, inline [N] source markers.\n\n## DETAILED FINDINGS\nSix numbered subsections (### 1. through ### 6.), one per track, in this order: competency decomposition; mastery markers & rubrics; deliberate-practice transfer; management/delegation transfer; career market signal; failure modes & mitigations. Each subsection: a "Confidence: [Tag] because ..." line (the word "because" is required), then 4-8 evidence bullets with concrete numbers/names/dates and inline [N] markers. Where an adversarial verdict was contested or refuted, say so explicitly and keep the refuted lore visible tagged do-not-use rather than deleting it.\n\n## EVIDENCE MAP\nA markdown table: Claim | Confidence | Basis — one row per major claim (12-20 rows), Basis names sources and the adversarial verdict where applicable.\n\n## GAPS & LIMITATIONS\nBullets from the track gaps + verification caveats + any silent caps.\n\n## CONFIDENCE SUMMARY\nOne paragraph: what is solid, what is directional, what is speculative.\n\n## SOURCES\nA NUMBERED list. Each entry: [title](url) (publisher, date) — Tier N. Used for: <which findings>. Number them so every [N] marker above resolves. Only sources that appear in the findings data below — never invent one.\n\n## NEXT STEPS\n4-6 numbered actions for the consumer (competency model drafting, rubric anchoring, self-audit, rep ladder, scoring loop, refresh cadence).\n\nRULES: Use ONLY the evidence below (do not import unstated knowledge as fact). Every empirical claim carries an [N] marker. Confidence vocabulary: Confirmed / Likely / Speculative / Contested / Unverifiable. Where verification contested a claim, downgrade it and say why. Plain text only in your reply — the full markdown body, nothing else.\n\nTRACK SYNTHESES (JSON):\n' + JSON.stringify(trackResults.map(r => ({ track: r.track, question: r.question, synth: r.synth })), null, 1) + '\n\nADVERSARIALLY VERIFIED CRITICAL CLAIMS (JSON):\n' + JSON.stringify(vOK.map(v => ({ track: v.track, claim: v.claim, confidence: v.confidence, verdict: v.verdict, votes: v.votes.map(x => ({ refuted: x.refuted, reasoning: x.reasoning })), sources: v.sources })), null, 1),
  { label: 'synthesize:report', phase: 'Synthesize', effort: 'high' }
)

return { tallies, reportBody, trackSummaries: trackResults.map(r => ({ track: r.track, summary: r.synth ? r.synth.track_summary : null, durable: r.synth ? r.synth.durable_principles : [], gaps: r.synth ? r.synth.gaps : [] })), verified: vOK.map(v => ({ track: v.track, claim: v.claim, verdict: v.verdict })) }