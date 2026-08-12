---
name: ariadne
description: >
  Personal project-manager for working-idea threads. Sweeps configured project vaults'
  ideas ledgers for open threads gone stale, surfaces them one line each, then runs a
  capped interactive triage — advance / sharpen / snooze / drop — writing every decision
  back to the thread note and the ledger. Use when surfacing stale threads, reviewing an
  ideas ledger, running a cross-vault thread review, or when the session-start nudge
  reports stale threads. The contract: threads never go stale silently, and drop happens
  only on the user's explicit word.
type: action
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Write Edit Bash Glob Grep
---

# Ariadne — Never Lose the Thread

Working-idea threads die of silence, not of rejection. Ariadne guarantees that every open thread in a project vault's ideas folder is periodically re-surfaced and deliberately handled — advanced, sharpened, parked, or explicitly dropped — until it reaches `resolved` or `dropped`. It is a follow-through companion, not a task manager: it never decides for the user, it only refuses to let a decision go unmade forever.

## Non-Negotiables

1. **Drop only on the user's explicit word.** Write `status: dropped` only when the user's own message in this conversation says to drop the thread. Never infer a drop from age, tone, apparent abandonment, or a shrug. If ambiguous, keep the thread open and say so.
2. **Ledger fidelity.** When writing back, edit only the triaged thread's own note fields and its own ledger row. Never reorder, reformat, or rewrite untouched rows or notes.
3. **Snooze honesty.** A thread with `snooze_until` in the future is silent — excluded from stale lists and nudges until that date. Snoozing is the sanctioned way to park a thread without dropping it.
4. **No guessed paths.** Every vault path, folder name, and threshold comes from the user's local config. If the config is missing, print the setup instructions (see `references/setup-and-config.md`) and stop. Never scan a path the config didn't name.
5. **Respect the cap.** Triage at most `triage_cap` threads per run (default 5) unless the user passes `--all`. The rest are listed, not interrogated.

## Input

- **Config** — `~/.config/ariadne/config.json` (override with `$ARIADNE_CONFIG`). Lives outside any repo; full schema and install steps in `references/setup-and-config.md`. Names the vaults, each vault's ideas folder (default `Ideas`) and ledger file (default `_index.md`), `stale_days` (default 21), and `triage_cap` (default 5).
- **Runtime arguments** (all optional):
  | Argument | Effect |
  |---|---|
  | `<vault>` | Restrict the run to the vault whose label or path matches |
  | `--all` | Lift the triage cap; triage every stale thread |
  | `--digest` | Non-interactive sweep; report only, no questions, no decisions |
  | `--table` | Print the stale table and stop (no triage) |

- **Thread-note contract** — each thread is one markdown note in the vault's ideas folder with YAML frontmatter. Ariadne reads `type: idea`, `status: open | in-progress | resolved | dropped`, `next_step`, and `touches_canon` (read-only); it owns two additional fields it writes itself: `last_touched` (date of the last triage decision or substantive advance) and `snooze_until` (optional date). Staleness = days since `last_touched`, falling back to file modification time for notes that predate ariadne.

## Process

1. **Scan.** Run `python3 <library_root>/scripts/ariadne_scan.py --json` (`library_root` from config) for the deterministic stale list. If the scanner is unavailable, read each configured ideas folder's frontmatter directly and apply the same rules: status `open` or `in-progress`, not snoozed, `last_touched` (or mtime) older than `stale_days`.
2. **Surface.** Print the full stale table, one line per thread: thread | vault | days stale | current `next_step`. If nothing is stale, say so, report open/snoozed counts, and stop.
3. **Triage.** Take the top `triage_cap` threads by days stale. For each, ask exactly one question with these options (use the ask-user-question mechanism when available, plain chat otherwise):
   - **Advance** — work the next step now or restate progress; update `next_step` to whatever is now next.
   - **Sharpen** — the step is too vague to start. Rewrite it together into a concrete action startable in ~15 minutes.
   - **Snooze** — park it deliberately; ask for (or propose) a `snooze_until` date.
   - **Drop** — only if the user's reply explicitly says drop (Non-Negotiable 1); set `status: dropped`.
   - Skipping is always allowed and writes nothing.
4. **Write back.** For every decision (not skips): update the thread note's frontmatter (`status`, `next_step`, `snooze_until` as applicable, and always `last_touched: <today>`), then update that thread's row in the ledger file so note and ledger never diverge. Edit in place.
5. **Summarize.** Close with: decisions made this run (thread → verb), threads still stale and untriaged, oldest untriaged age, and snoozed threads waking within a week.

## Output

**Triage summary** (end of every interactive run):

```
Ariadne — <date>
Triaged: <n> · advanced <a> · sharpened <s> · snoozed <z> · dropped <d>
Still stale: <m> threads (oldest <x>d) — run again or pass --all
Waking soon: <thread> (<date>), …
```

**Digest mode** (`--digest`, phase-2 contract for scheduled headless runs): sweep all configured vaults, make no decisions and ask no questions, and write one queue note per vault at the config's `digest_note` path (skip vaults where it is null), overwriting the previous digest. The note contains the stale table, counts, and a generated-on date — nothing else. Digest mode must be safe to run unattended: it only ever creates or overwrites its own digest note.

## Related Skills

`vault-writer` (infrastructure) is the schema-strict gate for creating *new* vault notes; ariadne only edits existing thread notes and ledgers in place, so it does not route through it. If a triage decision spawns a genuinely new artifact, hand that to the vault's own conventions rather than growing ariadne.
