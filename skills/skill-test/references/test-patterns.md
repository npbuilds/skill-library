# Structural Test Patterns

Complete list of structural tests that can be run locally without API access.

## File Structure Tests

| ID | Test | How | Severity |
|----|------|-----|----------|
| S01 | SKILL.md exists | Check file at `<dir>/SKILL.md` | critical |
| S02 | Frontmatter delimiters | Count `---` lines, need ≥ 2 | critical |
| S03 | Name field present | Parse frontmatter for `name:` | critical |
| S04 | Name matches directory | Compare `name` to `basename <dir>` | warning |
| S05 | Description present | Parse frontmatter for `description:` | critical |
| S06 | Description word count | 15-100 words | warning |
| S07 | Description has verbs | Check for action verbs | warning |
| S08 | Tools field (action/orch) | Present when type requires it | warning |

## Content Tests

| ID | Test | How | Severity |
|----|------|-----|----------|
| C01 | Has title heading | `# ` after frontmatter | info |
| C02 | Section count 2-8 | Count `## ` outside code blocks | warning |
| C03 | Body under 2000 words | Word count minus frontmatter | warning |
| C04 | Body under 5000 words | Hard limit | critical |
| C05 | No duplicate sections | Check for repeated `## ` headings | warning |
| C06 | Progressive disclosure | `references/` exists when body > 1500 | warning |

## Reference Integrity Tests

| ID | Test | How | Severity |
|----|------|-----|----------|
| R01 | Referenced files exist | Parse `references/` paths in body, verify | warning |
| R02 | No broken cross-refs | Parse `skills/` paths in body, verify | warning |
| R03 | Scripts have shebangs | Check first line of `scripts/*.sh` | info |
| R04 | Scripts are executable | Check file permissions | info |

## Running All Tests

To run the full structural suite on a skill:

```bash
# Quick validation (subset — uses validate-structure.sh)
bash scripts/validate-structure.sh <skill-dir>

# Full suite (run each test ID individually for detailed reporting)
# The skill-test skill orchestrates this by reading each test pattern
# and applying it to the target skill directory
```

## Adding Custom Tests

To add a test pattern, append a row to the appropriate table above with:
- Unique ID (prefix: S=structure, C=content, R=reference)
- Clear test description
- Implementation hint
- Severity level
