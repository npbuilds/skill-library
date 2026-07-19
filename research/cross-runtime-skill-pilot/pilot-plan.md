# Cross-Runtime Skill Compatibility Pilot

Date: 2026-07-19

## Purpose

Test whether representative canonical skills can be executed by Claude Code and Codex without modifying the existing skill files or Claude workflow.

## Protected surfaces

The pilot must not edit:

- `skills/**`
- `.claude-plugin/**`
- `.claude/**`
- `commands/**`
- `agents/**`
- `hooks/**`
- `CLAUDE.md`
- `AGENTS.md`

## Cases

1. `color-theory`: instruction/reference skill with structured design output.
2. `prose-editor`: transformation skill with explicit process and constraints.
3. `spelunker`: tool-heavy orchestrator with references, web research, and a strict output contract.

## Evaluation

Each runtime output is scored using the library's behavioral rubric:

- Trigger/instruction activation: 40%
- Output relevance: 25%
- Format compliance: 20%
- Completeness: 15%

A case passes at 70 or higher with no activation failure. The overall architecture is considered viable when all three Codex cases pass and no protected Claude surface changes.

## Execution policy

- Read-only sandbox for Codex.
- No file-edit tools requested from Claude.
- No session persistence where supported.
- Identical task prompts and generic runtime-adaptation instruction for both platforms.
