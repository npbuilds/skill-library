# Interface Philosopher — Quick Reference


## 1. Who Initiates?

| Model | The System | The Human | Both |
|---|---|---|---|
| **When** | Ambient intelligence, monitoring, prevention | Explicit tool use, search, creation | Collaborative work, shared canvas |
| **Trust required** | High — user must trust the system to act without prompting | Low — user controls all interactions | Medium — both parties contribute |
| **Failure mode** | Annoying (too much) or invisible (too little) | Underutilized (user doesn't know what's possible) | Coordination overhead |

## 2. How Much Does the System Reveal?

| Transparency Level | What the User Sees | When Appropriate |
|---|---|---|
| **Opaque** | Only the output. No reasoning shown. | Simple tasks, high trust, aesthetics matter more than understanding |
| **Translucent** | Output + brief explanation of approach | Most product interactions. Builds trust without overwhelming. |
| **Transparent** | Output + full reasoning + alternatives considered | Expert tools, high-stakes decisions, learning contexts |
| **Glass box** | The user can see and modify the system's process | Developer tools, customizable AI, power users |

## 3. What Modality?

| Modality | Strengths | When to Use |
|---|---|---|
| **Language** | Natural, nuanced, unbounded expressiveness | Exploration, open-ended questions, complex reasoning |
| **Visual** | Pattern recognition, spatial reasoning, overview | Data, relationships, comparisons, dashboards |
| **Structured** | Precision, scannability, machine-readability | Reports, specifications, configurations |
| **Ambient** | Zero-friction, contextual, unobtrusive | Monitoring, reminders, status, background processing |
| **Multimodal** | Rich communication, matching message to medium | Complex outputs, explanations, presentations |

## 4. What's the Relationship Model?

| Model | Metaphor | Implication |
|---|---|---|
| **Tool** | Hammer | User has full control. System does exactly what's asked. No initiative. |
| **Assistant** | Secretary | System has limited initiative. Reminds, organizes, executes. |
| **Collaborator** | Colleague | Shared agency. System contributes ideas, pushes back, disagrees. |
| **Advisor** | Consultant | System has domain expertise. Recommends, user decides. |
| **Agent** | Employee | System has delegated authority. Acts within boundaries. Reports back. |
| **Companion** | Partner | Ongoing relationship. Shared history. Mutual adaptation. |

## Quick Reference

| Approach | When | Risk |
|---|---|---|
| **Hide it** | User needs confidence, stakes are low | Over-trust, invisible errors |
| **Quantify it** | User is analytical, stakes are high | Probability numbers create false precision |
| **Qualify it** | General use, building trust | Language like "likely" is interpreted differently by different people |
| **Visualize it** | User can handle nuance, comparison contexts | Visual complexity, misinterpretation |
| **Embody it** | The product IS about exploration and uncertainty | Users may want answers, not uncertainty |
