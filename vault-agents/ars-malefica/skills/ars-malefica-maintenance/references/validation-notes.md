---
type: reference
status: active
created: '2026-06-04'
updated: 2026-07-24
tags:
- topic/systems-agent-skills
- topic/validation
title: Validation Notes
---

# Validation Notes

## Recommended order

1. Check the target files.
2. Run post-sync integrity validation.
3. Run repository validation.
4. Run workspace and tag validation.
5. Scan staged changes for secrets.
6. Finish with `git diff --check`.

## Useful commands

```bash
python "003 Resources/Systems/Vault Operations/Scripts/post-sync-integrity.py" --root .
python ".opencode/skills/ars-malefica-maintenance/scripts/validate-vault.py" --root .
python ".opencode/skills/ars-malefica-maintenance/scripts/check-workspaces.py" --root .
python "003 Resources/Systems/Vault Operations/Scripts/tag-taxonomy.py" --check
bash ".opencode/skills/ars-malefica-maintenance/scripts/scan-secrets.sh"
git diff --check
```

## What the checks mean

- Post-sync integrity: required folder markers exist; active bodies are unique;
  retired redirect sources have not returned; redirect targets resolve; the
  deletion queue is current; secret-state ignores remain present; sync conflict
  files are absent; Finder metadata remains ignored and untracked. During a
  reviewed migration, tracked deletions pass only when their count and
  NUL-delimited path fingerprint exactly match the approval snapshot in
  `003 Resources/Systems/Vault Migrations/`.
- Vault validation: core notes/folders exist, JSON parses, workspace refs resolve.
- Workspace validation: saved workspace files parse and point at real notes.
- Tag validation: the discovery-facet taxonomy has not drifted.
- Secret scan: staged diff contains no obvious credentials or private keys.
- Diff check: every tracked change is checked for whitespace damage.
