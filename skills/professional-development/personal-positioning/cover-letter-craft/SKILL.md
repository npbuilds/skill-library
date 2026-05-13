---
name: cover-letter-craft
description: >
  Draft firm-specific, thesis-aware cover letters for VC, operator, board, and advisory
  applications. Reference when applying for any role where a cover letter is required or
  optional-but-strategic. The strong cover letter is the highest-ROI artifact in a senior
  search: 30 minutes of work that demonstrates diligence, judgment, and reading-the-firm,
  and that distinguishes the user from the 95% who submit generic letters.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read
---

# Cover Letter Craft — The Highest-ROI Artifact in a Senior Search

Cover letters are widely declared dead by job-search advice; the declaration is wrong, especially for senior and venture roles. A generic cover letter is dead — pattern-matched as low diligence, often filtered out before reaching the hiring partner. A firm-specific, thesis-aware cover letter is the opposite: it demonstrates that the user has read the firm, formed a view, and can articulate that view in 250–400 words. For VC roles especially, where the entire job is diligence and pattern recognition, the cover letter *is* the first diligence exercise.

This skill produces the strong version: a structured five-block letter, sourced from real firm research, edited to the firm's voice, and finishing with a specific ask.

## Key Concepts

### The Five-Block Template

A strong cover letter has five blocks, in order:

1. **Firm-Specific Hook** (1–2 sentences) — A recent deal, a partner essay, a thesis statement from the firm's site, or a public move you have a real reaction to. NOT generic flattery. Demonstrates that you have read the firm.

2. **Earned-Credibility Paragraph** (3–4 sentences) — One trial / one outcome / one regulatory milestone, in the audience's vocabulary. Functions as proof that you can do the work the firm does. Use the `credibility-translation` matrix.

3. **Operator-to-Audience Translation Paragraph** (3–4 sentences) — What that clinical work taught you that maps to what *the firm does* (diligence, portfolio support, IC discussion, founder coaching, etc.). This is the bridge between past credibility and future contribution.

4. **Why This Firm Now Paragraph** (2–3 sentences) — Why this firm specifically, and why this year. Must reference the firm's thesis or recent moves — not generic flattery. This is where most letters fail.

5. **Close with a Specific Ask** (1–2 sentences) — A direct, low-friction ask: a 30-minute conversation, an opportunity to walk through your diligence on [portfolio company], a chance to discuss your fit for the open role. Don't close with "I look forward to hearing from you."

### The Firm-Research Stack (Do Before Drafting)

A cover letter cannot be strong without prior firm research. The research stack:

1. **The firm's public thesis** — Read the firm's site, their About / Strategy / Thesis pages, any recent essays by partners.
2. **Recent deals (last 12–18 months)** — What have they invested in? What stage? What does the deal mix tell you about their thesis?
3. **Recent partner writing or talks** — Substack posts, podcast appearances, conference talks. What is the partner you'd be working under thinking about?
4. **Portfolio companies relevant to your domain** — In biotech, which of their portfolio companies are clinical-stage in your areas of expertise? You may end up working with them.
5. **The fund's vintage and structure** — When did they raise? What size? This tells you their pace and risk tolerance.
6. **(Optional) The LP base** — Public information about LPs (university endowments, family offices, sovereign wealth) tells you about the fund's hold period and accountability structure.

For this research, hand off to `research/spelunker`. Do not skip this step. The research takes 60–90 minutes and is the difference between a strong letter and a generic one.

### Length and Format

- **Length:** 250–400 words. One page. Senior VC/board cover letters under 250 words can read terse; over 400 reads as not having edited.
- **Format:** Plain prose, no bullets. (Bullets in a cover letter signal a resume copy-paste.) Three paragraphs, occasionally four. White space matters.
- **Tone:** Direct, present-tense, first-person, conversational-but-senior. Not formal-stiff ("Dear Sir/Madam"); not over-casual ("Hey there!"). Address the partner by first name + last name if you know who you're writing to.

### Common Physician Failure Modes

Senior MDs writing VC/operator cover letters often fail in specific ways:

| Failure | Looks Like | Why It Fails |
|---|---|---|
| Over-clinical vocabulary | "Phase 2 IRC-adjudicated co-primary endpoint" | Reader doesn't know what's hard about it |
| Under-business framing | Lists clinical work without surfacing investment relevance | Reader can't tell why this matters to them |
| False humility | "I am a clinician interested in learning about investing" | Reads as not-ready; investors want operators who already have a view |
| Generic firm references | "I admire [Firm]'s investment philosophy" | Reads as recycled; demonstrates no actual firm research |
| Asking to be educated | "I'd love to learn how you think about [topic]" | Wrong direction; the letter should demonstrate that *you* have a view |
| Forgetting the ask | "I look forward to hearing from you" | Missed the highest-leverage sentence |

### Variants by Application Type

| Application Type | Variations |
|---|---|
| **VC associate / principal application** | Five-block template; lead with diligence judgment |
| **Operating partner / EIR** | Five-block template; lead with operator credibility + sector thesis |
| **CMO / Head of Clin Dev (operator)** | Lead with clinical depth + leadership signal; ask is a meeting with the CEO |
| **Board observer / director** | Lead with governance frame + sector expertise; ask is exploratory conversation |
| **Advisory role** | Lead with specific value you'd add; ask is a 30-minute call to scope |
| **Fellowship / EIR-style program** | Lead with thesis + what you'd use the program for; ask is application context |

## Self-Coaching Track

**For your situation (MD → biotech VC/operator):**

1. **Pick the specific application.** Cover letters are always per-firm, per-role. Pull the JD and identify the target partner (the person who will read this letter).

2. **Run the firm-research stack.** 60–90 minutes. Hand off to `research/spelunker` for the substantive research. Capture in a notes file:
   - The firm's stated thesis (one paragraph)
   - 3 recent deals you can name
   - The most-relevant partner essay or interview (paste a quote or link)
   - 1–2 portfolio companies in your specific clinical area
   - One observation or question you have about the firm's strategy

3. **Draft the five blocks.** Use the template. Don't try to wordsmith; just draft. Block 1 sources from research; Block 2 sources from `credibility-translation`; Block 3 sources from `narrative-architecture`; Block 4 sources from research; Block 5 is the ask.

4. **Edit for length and voice.** Target 300 words. Cut everything that doesn't serve the five blocks. Tone-check: does this sound like *you* talking to a peer-partner, or like a cover letter template?

5. **Run the prose-editor pass.** Hand off to `writing/prose-editor` for the final polish.

6. **Add the BLUF opener.** Many cover letters bury the thesis. The first sentence of Block 1 should be BLUF-style: name the firm + the move + your one-line thesis. Hand off to `binding-vow/bluf-shaper` if needed.

7. **Stress-test the ask.** The closing sentence is the action driver. Read it cold: would a busy partner respond to this? If the ask is vague or burden-heavy, rewrite.

## Teach / Mentor-Others Track

**When coaching a junior or peer through cover letter craft:**

1. **Lead with: "Generic is dead."** Many mentees write cover letters as if filling in a template. Show them what a firm-specific letter looks like, side-by-side with a generic one. The difference is visible at first sentence.

2. **Force the firm-research step.** The single biggest determinant of letter quality is whether the writer did real research. Mentees skip it. Insist; it is the work.

3. **Walk through the five blocks on their actual application.** Don't teach abstractly. Pick a real firm they're applying to, do the research together, then draft each block together. The template transfers after one worked example.

4. **Diagnose common physician failure modes.** Most senior MDs write cover letters with one or more of: over-clinical vocabulary, under-business framing, false humility, no specific ask. Name each as you see it.

5. **The "why this firm now" paragraph is the failure point.** Mentees write generic flattery here. Coach: this paragraph must reference *specific* firm content — a deal, an essay, a move. If they can't fill it specifically, the firm research was inadequate.

6. **The ask is leverage.** The closing sentence is where most letters squander value. Coach mentees toward a low-friction, specific ask: a 30-minute conversation, a chance to walk through diligence on [portfolio company]. Generic "look forward to hearing from you" closures are leaving leverage on the table.

## When This Applies

- Per-application work for VC, operator, board, advisory, or fellowship roles
- When a cover letter is "optional" — for senior roles, it is rarely actually optional
- When current applications are not converting (a strong cover letter is often the missing piece)
- When the user has a warm intro but wants to send a follow-up letter to the partner directly

## Cross-Domain Connections

- **research/spelunker** — Firm research is the substrate; always hand off here first
- **personal-positioning/credibility-translation** — Earned-credibility paragraph draws from the translation matrix
- **personal-positioning/narrative-architecture** — Operator-to-audience paragraph draws from the through-line
- **personal-positioning/audience-tuning** — Letter is tuned per firm-archetype (early-stage thesis-driven, late-stage diligence-heavy, etc.)
- **binding-vow/bluf-shaper** — The opening sentence should be BLUF-shaped
- **binding-vow/audience-classifier** — Audience taxonomy informs tuning
- **writing/prose-editor** — Final polish pass
- **biotech-venture/asclepius** — Source of biotech-substance for the credibility and translation paragraphs
