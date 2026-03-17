---
description: Quick health overview of all registered skills
---

Read `data/registry.json` and display a compact status table of all registered skills.

Show each skill's name, type, health status, lifecycle status, composite score, and estimated total tokens. Sort by composite score descending. Use status indicators: `✓` healthy, `⚠` warning, `✗` critical.

At the bottom, show aggregate stats:
- Total skills registered (active/deprecated/archived breakdown)
- Total always-loaded metadata tokens
- Skills with warnings or critical issues (count)
- Average composite score

Format as an ASCII table. Keep output concise — this is a quick glance dashboard.
