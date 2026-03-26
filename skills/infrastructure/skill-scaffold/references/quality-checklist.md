# Skill Quality Checklist

Run through this checklist after scaffolding a new skill. All MUST-PASS items must be satisfied before considering the skill ready.

## MUST-PASS (blocks creation)

- [ ] SKILL.md exists in the skill directory
- [ ] YAML frontmatter has opening and closing `---` delimiters
- [ ] `name` field is present and matches directory name (kebab-case)
- [ ] `description` field is present
- [ ] Description is 20-60 words
- [ ] Description contains at least one action verb: use, create, build, add, update, fix, analyze, check, run, generate, scaffold, fork, test, export, browse, search, manage, audit, review, optimize
- [ ] Description includes trigger phrases ("Use when...", "Use to...")
- [ ] `tools` field is present for action and orchestrator types
- [ ] Body has at least 2 sections (## headings)
- [ ] Body is under 2,000 words
- [ ] Section count is 8 or fewer

## SHOULD-PASS (warnings if failed)

- [ ] `references/` directory exists (for future progressive disclosure)
- [ ] Description is written in third person
- [ ] No duplicate section headings
- [ ] Sections follow a logical order (overview → instructions → output)
- [ ] Body words under 1,500 (ideal range)
- [ ] Description under 60 words (sweet spot for trigger matching)

## NICE-TO-HAVE (informational)

- [ ] `examples/` directory exists for action/orchestrator types
- [ ] Output format section includes a concrete example
- [ ] Error handling section is present
- [ ] Skill references other skills via relative paths (not absolute)
