# Decomposition Strategies

Patterns for splitting skills. Choose based on how the parent skill's content is organized.

## Strategy: Responsibility Split

**When**: Sections cluster around distinct responsibilities (most common).

Split by grouping `## ` sections that serve the same function. Each group becomes a child skill.

Example: A skill with "Create", "Validate", "Export" sections → three children, one per verb.

## Strategy: Audience Split

**When**: Different sections serve different invokers (user vs Claude vs automation).

Split by who uses each section. One child for user-facing operations, one for internal/automated ones.

Example: A skill with manual commands AND automated hooks → user-facing child + automation child.

## Strategy: Complexity Tier

**When**: A skill has both simple and advanced operations.

Split into a "basic" child (common operations, low token cost) and an "advanced" child (complex operations, heavier context).

Example: A registry skill with "browse" (simple) + "migration" (complex) → two tiers.

## Strategy: Domain Split

**When**: A skill spans multiple knowledge domains.

Split along domain boundaries. Each child stays within a single domain.

Example: A "project setup" skill covering Python + JavaScript → one child per language.

## Naming Convention

Child skills inherit the parent name with a suffix:
- Responsibility split: `parent-create`, `parent-analyze`, `parent-manage`
- Audience split: `parent-interactive`, `parent-automated`
- Complexity tier: `parent-core`, `parent-advanced`
- Domain split: `parent-python`, `parent-js`

## Shared References

When multiple children need the same reference file:
1. Keep one canonical copy in the first child's `references/`
2. Other children reference it via cross-skill path: `skills/<first-child>/references/<file>`
3. Update `shares_references_with` in all children's registry entries
4. The `shared_references` network map in registry.json tracks these

## Post-Fork Checklist

- [ ] Each child has valid SKILL.md with unique, specific description
- [ ] No section from parent is missing across all children
- [ ] Shared references are tracked in registry
- [ ] Parent marked as deprecated with replacement pointers
- [ ] All children pass health checks
- [ ] All children registered with correct `forked_from`
- [ ] Parent updated with `forked_into` list
