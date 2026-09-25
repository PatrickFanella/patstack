---
type: reference
status: active
created: '2026-06-04'
updated: 2026-07-26
tags:
- topic/systems-agent-skills
- topic/vault
title: Vault Map
---

# Vault Map

## Active surfaces

- `Home.md` — command center / dashboard with 8 Dataview queries.
- `000 Inbox/` — transient capture with QuickAdd buttons.
- `001 Projects/Threads/` — ongoing themes and synthesis.
- `001 Projects/Works/` — concrete outputs (Blog Posts, Social Posts, Software, Essays, Videos, Zines, Music, Releases, Documentation, Patreon).
- `002 Areas/` — responsibilities and admin (Life, Work, People).
- `003 Resources/` — media (10 subfolders), documentation, templates (55), periodic notes, QuickAdd support.
- `004 Archives/` — archived Threads only; delete other retired material (recover pre-2026-09-25 history from the private history bundle in Documentation-Hub/backups/git-history).

## Maintenance surfaces

- `.obsidian/community-plugins.json` — 41 enabled plugins.
- `.obsidian/appearance.json` — visual posture only.
- `.obsidian/workspaces/*.json` — 8 saved layouts.
- `001 Projects/Works/Blog Posts/SubBlog/SubBlog Pipeline.kanban` — blog pipeline.
- `001 Projects/Works/Social Posts/SUBCULT Marketing/Social Pipeline.kanban` — social pipeline.
- `001 Projects/Works/Software/Software Pipeline.kanban` — software pipeline.
- `003 Resources/Systems/Vault Migrations/Redirects.md` — moved-note map.
- `003 Resources/Systems/Vault Maintenance/Deletion Candidates.md` — safe-delete queue.
- `003 Resources/Systems/Vault Migrations/` — sync and migration records kept
  outside Archives.
- `003 Resources/Systems/Vault Improvement Plan.md` — improvement roadmap.
- `003 Resources/Systems/Vault Maintenance Baseline 2026-07-24.md` — current
  operational truth.
- `003 Resources/Systems/Vault Operations/Scripts/post-sync-integrity.py` —
  deterministic post-sync acceptance gate.
- Monthly health automation is intentionally deferred; there is no external
  `vault-monthly-health` task.

## Safety rules

- Archive unique provenance before deletion; exact copies and superseded shells
  may be deleted after canonical destination and Git recovery checks.
- Keep plugin/token data out of git (paperless, remotely-save, copilot, github-embeds, local-rest-api).
- Maintain redirects for renamed/moved notes.
- Prefer one edit path per task: config, content, or validation.
- Use properties for structure and canonical discovery facets for tags:
  `domain/*`, `project/*`, `platform/*`, `medium/*`, `method/*`, `topic/*`,
  and `cadence/*`.
