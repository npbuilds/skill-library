---
name: {{SKILL_NAME}}
description: >
  {{DESCRIPTION}}
allowed-tools: {{TOOLS}}
---

# {{SKILL_TITLE}} — {{SKILL_SUBTITLE}}

{{DESCRIPTION_EXPANDED}}

## Routing Logic

<!-- Define which child skill handles which type of question -->
<!-- Use a table: question pattern → child skill → reasoning -->

| Question Pattern | Route To | Why |
|-----------------|----------|-----|
| {{PATTERN_1}} | `{{CHILD_SKILL_1}}` | {{REASON_1}} |
| {{PATTERN_2}} | `{{CHILD_SKILL_2}}` | {{REASON_2}} |

### Multi-Skill Questions

<!-- When should multiple child skills be loaded? In what order? -->

## Curriculum Order

<!-- Define the learning sequence for child skills -->
<!-- Which skill should be read first? Which builds on others? -->

1. **{{CHILD_SKILL_1}}** (foundation) — {{WHY_FIRST}}
2. **{{CHILD_SKILL_2}}** (application) — {{WHY_SECOND}}

### Level Progression
- **Foundational**: {{EXISTING_SKILLS}}
- **Intermediate**: (future skills in this subdomain)
- **Advanced**: (future skills in this subdomain)

## Conflict Resolution

<!-- When child skills give contradictory guidance, how to resolve -->

| Conflict | Resolution | Reason |
|----------|-----------|--------|
| {{CONFLICT_1}} | {{WINNER}} wins | {{REASONING}} |

**General rule**: {{HIERARCHY_PRINCIPLE}}

## Scope Boundaries

**This director handles**: {{IN_SCOPE}}

**Escalate to the orchestrator when**:
- {{ESCALATION_TRIGGER_1}}
- {{ESCALATION_TRIGGER_2}}
