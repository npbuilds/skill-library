# Skill Test — Quick Reference


## Formula / Pseudocode

```
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

## Formula / Pseudocode

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

## Formula / Pseudocode

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
