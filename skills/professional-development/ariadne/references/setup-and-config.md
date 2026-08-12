# Ariadne — Setup and Config

Ariadne is project-agnostic machinery. Every vault path, folder name, and threshold lives in a user-level config file **outside any repository** — nothing private is ever committed. This mirrors the leak-guard pattern (`$HOME/.config/leak-terms.txt`).

## Config file

Location: `~/.config/ariadne/config.json` (override with the `ARIADNE_CONFIG` environment variable).

```json
{
  "library_root": "<absolute-path-to-your-skill-library-checkout>",
  "stale_days": 21,
  "triage_cap": 5,
  "vaults": [
    {
      "label": "<short-vault-name>",
      "path": "<absolute-path-to-vault>",
      "ideas_dir": "Ideas",
      "index_file": "_index.md",
      "digest_note": null,
      "stale_days": null
    }
  ]
}
```

| Field | Required | Default | Notes |
|---|---|---|---|
| `library_root` | yes | — | Checkout containing `scripts/ariadne_scan.py`; lets the skill find the scanner from any cwd |
| `stale_days` | no | `21` | Global staleness threshold in days |
| `triage_cap` | no | `5` | Max threads triaged per interactive run |
| `vaults[].label` | no | basename of `path` | Short name shown in tables |
| `vaults[].path` | yes | — | Absolute vault root |
| `vaults[].ideas_dir` | no | `Ideas` | Folder of thread notes, relative to vault root |
| `vaults[].index_file` | no | `_index.md` | Ledger file inside `ideas_dir` |
| `vaults[].digest_note` | no | `null` | Vault-relative path for the digest queue note; `null` skips this vault in digest mode |
| `vaults[].stale_days` | no | global | Per-vault threshold override |

## Thread-note contract

Each thread is one markdown note in `ideas_dir` (the ledger `index_file` and `_`-prefixed files are ignored):

```yaml
---
type: idea
status: open          # open | in-progress | resolved | dropped
next_step: "<one line, concretely startable>"
touches_canon: []
last_touched: 2026-01-15   # written by ariadne on every triage decision
snooze_until: 2026-03-01   # optional; thread is silent until this date
---
```

`last_touched` and `snooze_until` are ariadne's two additions to the pre-existing contract. Notes without `last_touched` fall back to file mtime for staleness — the first triage stamps the field and makes staleness sync-proof from then on.

## Session-start nudge (hook)

The hook prints a one-line stale count when you open a session inside a configured vault. Register it in **`~/.claude/settings.json`** (user-level — vault sessions never load this repo's project settings):

```json
"SessionStart": [{
  "hooks": [{
    "type": "command",
    "command": "[ -f '<repo>/hooks/ariadne-session-nudge.sh' ] && bash '<repo>/hooks/ariadne-session-nudge.sh' || true",
    "statusMessage": "Checking idea threads..."
  }]
}]
```

Replace `<repo>` with your skill-library checkout path (point at the main checkout, not a worktree). The hook is silent — and exits 0 — whenever the config is missing, the cwd is not inside a configured vault, or nothing is stale.

## Slash command (optional)

For `/ariadne` in any project, copy the wrapper to your user-level commands:

```bash
cp '<repo>/commands/ariadne.md' ~/.claude/commands/ariadne.md
```

## Invoking without the command

From any session: load the skill via the skill-library MCP server (`get_skill` with `skill_name: "ariadne"`), or run the scanner directly:

```bash
python3 '<repo>/scripts/ariadne_scan.py'          # human table
python3 '<repo>/scripts/ariadne_scan.py' --json   # machine output
```
