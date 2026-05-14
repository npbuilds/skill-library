---
name: rhetoric
description: >
  Direct the rhetoric subdomain — route persuasion, argument, essay form, and rhetorical device
  questions to the right specialist skill. Use when the user is writing to persuade, constructing
  an argument, choosing an essay form, or wants to deploy rhetorical devices effectively.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Glob
---

# Rhetoric Director — The Essayist's Compass

The department head for rhetoric and persuasive writing within the writing domain. Routes questions to the right specialist, defines the learning order, and resolves conflicts between persuasive strategies.

Rhetoric governs writing that aims to convince, argue, or persuade — from classical appeals to modern essay forms. It is the domain of the essayist, the critic, and any writer who wants their prose to change minds, not just describe experience. Rhetoric is not opposed to narrative — the best persuasive writing uses story, sensory detail, and voice. But its organizing principle is the argument, not the scene.

## Routing Logic

| Question Pattern | Route To | Why |
|-----------------|----------|-----|
| Ethos, pathos, logos, credibility, emotional appeals | `rhetorical-appeals` | The three classical modes of persuasion |
| Essay structure, counterarguments, Toulmin, thesis placement | `argument-structure` | How arguments are built and organized |
| Anaphora, tricolon, parallelism, chiasmus, specific devices | `rhetorical-devices` | Deployable techniques for emphasis and rhythm |
| "What form should this essay take?" lyric, braided, hermit crab | `essay-forms` | Form selection and its implications |
| "How do I make this more persuasive?" (vague) | `rhetorical-appeals` first | Start with the foundational framework, then route deeper |

### Multi-Skill Questions

Load in this order when multiple skills apply:

1. `rhetorical-appeals` — what mode of persuasion is the writer using? Is it the right one?
2. `argument-structure` — is the argument organized effectively?
3. `essay-forms` — is the form serving the argument?
4. `rhetorical-devices` — are the right devices deployed for emphasis and rhythm?

This order goes from strategy to tactics: choose the right persuasive mode, organize the argument, pick the form, then refine with devices.

## Curriculum Order

1. **Rhetorical Appeals** (foundation) — Ethos, pathos, logos, kairos. The framework everything else builds on.
2. **Argument Structure** (organization) — How to build and arrange an argument. The Toulmin model's "warrant" concept is the single most useful idea in rhetoric pedagogy.
3. **Essay Forms** (form) — The vessel the argument lives in. Form should emerge from content, not precede it.
4. **Rhetorical Devices** (technique) — The deployable tools. Most useful after you understand what you're trying to accomplish.

### Level Progression
- **Foundational**: All four current skills
- **Intermediate**: (future) audience analysis, concession strategies, evidence deployment
- **Advanced**: (future) implied argument, the essay as art form, rhetoric of silence

## Conflict Resolution

| Conflict | Resolution | Reason |
|----------|-----------|--------|
| Appeals says "use pathos" but argument-structure says "this needs more logos" | Depends on audience | Hostile or skeptical audiences need logos first; sympathetic audiences respond to pathos. Route to `rhetorical-appeals` for audience analysis. |
| Essay-forms says "use lyric essay" but argument-structure says "make the thesis explicit" | Essay-forms wins | Lyric essays argue through juxtaposition, not explicit thesis. The form determines the argument style. |
| Rhetorical-devices says "use anaphora here" but sentence-craft says "vary your openers" | Rhetoric wins when persuading | Deliberate repetition for rhetorical effect overrides variety-as-default. Route to sentence-craft only for non-rhetorical prose. |
| Argument-structure says "address the counterargument" but the essay form is personal/narrative | Both apply, different methods | In narrative essays, counterarguments can be embodied in experience rather than stated as propositions. |

**General rule**: **Strategy over tactics** — get the persuasive mode and structure right before polishing with devices. And: **form constrains technique** — a lyric essay's tools differ from an argumentative essay's, even when both are persuading.

## Scope Boundaries

**This director handles**: Persuasive writing, argument construction, essay form selection, and rhetorical device deployment — the craft of writing that aims to convince.

**Escalate to the orchestrator when**:
- The problem is sentence-level (rhythm, diction, syntax) — that's sentence-craft territory
- The problem is narrative (scene, pacing, dialogue) without a persuasive aim — that's narrative-craft territory
- The user needs a full editing pass — that's revision-craft territory
- The user needs prose drafted — the orchestrator routes to action skills

## Cross-Domain Connections

- **Worldbuilding/cultures-societies**: A culture's value system constrains which rhetorical strategies feel authentic. A collectivist culture emphasizes communal appeals; an honor culture uses shame and glory. Rhetoric written for in-world audiences must respect the target culture's persuasion conventions.



## Related Skills

- **visual-communication** — Rhetoric and visual-communication are complementary persuasion crafts. Both manage attention, structure arguments, and use contrast/repetition/emphasis to drive meaning — one with words, the other with images.
