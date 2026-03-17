# Behavioral Evaluation Rubric

Scoring criteria for behavioral test cases. Each test case is scored on 4 dimensions.

## Dimensions

### Trigger Accuracy (40%)

Did the skill activate when expected?

| Score | Criteria |
|-------|----------|
| 100 | Correct trigger/no-trigger decision |
| 50 | Triggered but with low confidence or partial match |
| 0 | Wrong decision (false positive or false negative) |

### Output Relevance (25%)

Does the response address the prompt's intent?

| Score | Criteria |
|-------|----------|
| 100 | Response directly addresses the prompt |
| 70 | Response is related but misses key aspects |
| 30 | Response is tangentially related |
| 0 | Response is unrelated to the prompt |

### Format Compliance (20%)

Does output match the skill's documented format?

| Score | Criteria |
|-------|----------|
| 100 | Output matches documented format exactly |
| 70 | Output is structured but deviates from documented format |
| 30 | Output is unstructured but contains the right information |
| 0 | Output format is completely wrong |

### Completeness (15%)

Are all expected elements present?

| Score | Criteria |
|-------|----------|
| 100 | All `expect_contains` items present |
| Score | Proportional to items found vs expected |
| 0 | None of the expected items found |

## Per-Test Score

```
test_score = round(
  trigger_accuracy * 0.40 +
  output_relevance * 0.25 +
  format_compliance * 0.20 +
  completeness * 0.15
)
```

## Per-Skill Score

```
skill_test_score = round(mean(test_scores))
```

## Pass/Fail Threshold

- **PASS**: skill_test_score >= 70 AND no test has trigger_accuracy == 0
- **FAIL**: skill_test_score < 70 OR any test has trigger_accuracy == 0
