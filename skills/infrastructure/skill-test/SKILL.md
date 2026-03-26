---
name: skill-test
description: >
  Test skills for structural correctness and behavioral accuracy. Use when the user wants to
  validate a skill's file structure, run behavioral test cases against a skill, benchmark two
  skill versions side-by-side, or verify that a skill triggers correctly on expected prompts.
tools: Read, Write, Bash, Glob, Grep, Agent
---

# Skill Test — The Prover

Validate skills through structural checks, behavioral test cases, and version benchmarking. Combines local validation with optional API-powered behavioral testing.

## Structural Testing

Structural tests verify file integrity without requiring any API calls.

### How to Run

1. Run `scripts/validate-structure.sh <skill-directory>` for automated checks
2. Read `references/test-patterns.md` for the full structural test suite
3. Report results as pass/fail per check with details on failures

### What It Checks

- SKILL.md format: frontmatter delimiters, required fields (name, description), field types
- Directory structure: expected subdirectories exist, no orphaned files
- Reference integrity: files referenced in SKILL.md body actually exist
- Script executability: files in `scripts/` have execute permissions and shebangs
- Frontmatter consistency: name matches directory, description within word limits
- Cross-references: paths to other skills or references resolve correctly

## Behavioral Testing

Behavioral tests verify that a skill triggers correctly and produces expected output. Two approaches: the `skill-tester` agent (no API needed — evaluates by reasoning about descriptions) or the `skill-analyze` skill (requires Anthropic API for deeper analysis).

### Test Case Format

Test cases are YAML files stored in `test-cases/<skill-name>.yaml`:

```yaml
skill: skill-registry
test_cases:
  - name: "triggers on browse request"
    prompt: "Show me all my skills"
    expect_trigger: true
    expect_contains:
      - "registry"
      - "table"

  - name: "does not trigger on unrelated request"
    prompt: "Write a Python function to sort a list"
    expect_trigger: false

  - name: "handles search filter"
    prompt: "Show me all skills with health warnings"
    expect_trigger: true
    expect_contains:
      - "health"
      - "warning"
```

### Running Behavioral Tests

1. Read the test case file for the target skill
2. Use the Agent tool to launch the `skill-tester` agent (from `agents/skill-tester.md`)
3. The agent runs each test case prompt and evaluates the response
4. Collect results: pass/fail per test case, with explanation for failures
5. Append results summary to the skill's registry changelog and update `manual_notes` if needed

### Evaluation Criteria

Read `references/eval-rubric.md` for the full evaluation rubric. Summary:

- **Trigger accuracy**: Did the skill activate when expected? Did it stay silent when it shouldn't?
- **Output relevance**: Does the response address the prompt's intent?
- **Format compliance**: Does output match the skill's documented format?
- **Completeness**: Are all expected elements present in the response?

## Benchmarking

Compare two versions of a skill (e.g., before and after a refactor) to measure improvement or regression.

### How to Benchmark

1. Provide two skill paths or two git refs containing different versions
2. Run the same test cases against both versions
3. Score each version using the eval rubric
4. Present side-by-side comparison:

```
BENCHMARK — skill-registry (v1 vs v2)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Test Case                v1    v2    Delta
─────────────────────────────────────────
triggers on browse       PASS  PASS   =
handles search filter    FAIL  PASS  +1
does not false trigger   PASS  PASS   =
─────────────────────────────────────────
Total                    2/3   3/3   +1
Score                    67    100   +33
```

## Output Format

Present test results as structured ASCII:

```
TEST RESULTS — skill-registry
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Structural:  5/5 passed
Behavioral:  3/3 passed (requires API)
Overall:     PASS

  ✓ frontmatter valid
  ✓ directory structure correct
  ✓ reference links resolve
  ✓ triggers on browse request
  ✓ handles search filter
```
