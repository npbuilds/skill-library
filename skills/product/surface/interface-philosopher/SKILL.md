---
name: interface-philosopher
description: >
  Deep thinking about how intelligence should meet humans. When is language the right
  interface? When visual? When ambient? When should the system be proactive vs. responsive?
  When invisible? The epistemology of AI interfaces — not UX patterns but the philosophical
  foundation for how intelligence presents itself.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Write bash Glob Grep
---

# Interface Philosopher — The Epistemology of AI Surfaces

This isn't UX design. UX design asks "what's the best button placement?" Interface philosophy asks **"should there be a button at all?"**

When intelligence meets humans, every design choice encodes assumptions about the relationship between human and machine, about trust, about agency, about what intelligence owes to the people it serves.

## The Core Questions

### 1. Who Initiates?

| Model | The System | The Human | Both |
|---|---|---|---|
| **When** | Ambient intelligence, monitoring, prevention | Explicit tool use, search, creation | Collaborative work, shared canvas |
| **Trust required** | High — user must trust the system to act without prompting | Low — user controls all interactions | Medium — both parties contribute |
| **Failure mode** | Annoying (too much) or invisible (too little) | Underutilized (user doesn't know what's possible) | Coordination overhead |

**Design question:** Does this intelligence serve users best by waiting to be asked, or by anticipating needs?

### 2. How Much Does the System Reveal?

| Transparency Level | What the User Sees | When Appropriate |
|---|---|---|
| **Opaque** | Only the output. No reasoning shown. | Simple tasks, high trust, aesthetics matter more than understanding |
| **Translucent** | Output + brief explanation of approach | Most product interactions. Builds trust without overwhelming. |
| **Transparent** | Output + full reasoning + alternatives considered | Expert tools, high-stakes decisions, learning contexts |
| **Glass box** | The user can see and modify the system's process | Developer tools, customizable AI, power users |

**Design question:** How much of the intelligence's process should be visible, and to whom?

### 3. What Modality?

| Modality | Strengths | When to Use |
|---|---|---|
| **Language** | Natural, nuanced, unbounded expressiveness | Exploration, open-ended questions, complex reasoning |
| **Visual** | Pattern recognition, spatial reasoning, overview | Data, relationships, comparisons, dashboards |
| **Structured** | Precision, scannability, machine-readability | Reports, specifications, configurations |
| **Ambient** | Zero-friction, contextual, unobtrusive | Monitoring, reminders, status, background processing |
| **Multimodal** | Rich communication, matching message to medium | Complex outputs, explanations, presentations |

**Design question:** What modality best serves this intelligence's message? (Usually: multimodal with a primary mode.)

### 4. What's the Relationship Model?

| Model | Metaphor | Implication |
|---|---|---|
| **Tool** | Hammer | User has full control. System does exactly what's asked. No initiative. |
| **Assistant** | Secretary | System has limited initiative. Reminds, organizes, executes. |
| **Collaborator** | Colleague | Shared agency. System contributes ideas, pushes back, disagrees. |
| **Advisor** | Consultant | System has domain expertise. Recommends, user decides. |
| **Agent** | Employee | System has delegated authority. Acts within boundaries. Reports back. |
| **Companion** | Partner | Ongoing relationship. Shared history. Mutual adaptation. |

**Design question:** What relationship model matches this product's thesis and the user's expectations?

### 5. How Does It Handle Uncertainty?

Intelligence is inherently uncertain. How the interface presents uncertainty defines the product's epistemic character.

| Approach | When | Risk |
|---|---|---|
| **Hide it** | User needs confidence, stakes are low | Over-trust, invisible errors |
| **Quantify it** | User is analytical, stakes are high | Probability numbers create false precision |
| **Qualify it** | General use, building trust | Language like "likely" is interpreted differently by different people |
| **Visualize it** | User can handle nuance, comparison contexts | Visual complexity, misinterpretation |
| **Embody it** | The product IS about exploration and uncertainty | Users may want answers, not uncertainty |

## Applying the Philosophy

When `surface/exposure-strategist` or `surface/experience-weaver` needs philosophical grounding:

1. Start with the thesis — what does this product believe about human-AI interaction?
2. Answer the five core questions for this specific surface
3. Check for consistency — do the answers form a coherent philosophy?
4. Check against the paradigm choice from `envision/paradigm-designer`

## Cross-Domain

- **philosophy-orchestrator** — For deep ethical questions about AI agency, consent, and transparency
- **design-orchestrator** — For translating philosophical positions into aesthetic choices
