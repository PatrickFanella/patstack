---
name: ars-malefica-maintenance
description: "Vault/repository maintenance for ars-malefica. Use when validating vault structure, archive/redirect hygiene, workspace integrity, plugin/API posture, git safety, or staged secret checks. Triggers: maintenance, validate vault, archive, redirects, workspaces, plugin check, API posture, git safety, secret scan, repo health."
metadata:
  blacktower-pack: personal
  blacktower-kind: workflow
  blacktower-tier: personal
  blacktower-capabilities: dev-workflows,ars,malefica,maintenance
---

# Ars Malefica Maintenance

Use for safe repo/vault upkeep.

## Read first

- `references/vault-map.md` for the current vault surface.
- `references/validation-notes.md` for what to check before commit.
- `references/git-safety.md` for staging and dirty-file rules.
- [[003 Resources/Systems/Vault Improvement Plan|Vault Improvement Plan]] for the improvement roadmap.

## Workflow

1. Inspect the target surface and keep changes reversible.
2. Prefer validation over deletion; archive first, remove later.
3. Keep plugin/API data secret-free; never stage secret-bearing blobs.
4. Verify paperless and remotely-save data.json are gitignored.
5. Run `003 Resources/Systems/Vault Operations/Scripts/maintenance-check.sh`
   before committing. It composes:
   - the post-sync integrity gate
   - `scripts/validate-vault.py`
   - `scripts/check-workspaces.py`
   - the tag-taxonomy drift check
   - recurring-task validation
6. Run the staged secret scan separately after staging.
7. Finish with `git diff --cached --check`.

## Guardrails

- Do not touch unrelated dirty files.
- Do not introduce insecure HTTP or ad hoc secret storage.
- Prefer deterministic scripts over manual one-offs.
- Keep archive mappings and redirects updated when files move.
- Keep structural metadata in properties. Maintain discovery facets under
  `domain/*`, `project/*`, `platform/*`, `medium/*`, `method/*`, `topic/*`, and
  `cadence/*`; reserve `private`, `draft`, and `system` as controls.

## When to use scripts

- Use `validate-vault.py` for vault-level structure and JSON sanity.
- Use `check-workspaces.py` for workspace references and layout integrity (8 workspaces).
- Use `003 Resources/Systems/Vault Operations/Scripts/tag-taxonomy.py --check` for tag drift.
- Use `003 Resources/Systems/Vault Operations/Scripts/post-sync-integrity.py --root .`
  for duplicate bodies, resurrected redirect sources, missing redirect targets,
  stale deletion candidates, folder markers, sync conflict files, and ignored
  OS junk.
- Use `scan-secrets.sh` on staged changes before commit.

## Key surfaces (post Wave 1-6)

- 41 enabled plugins, 10 optimized configs
- 56 templates with canonical metadata and discovery facets, 22 folder auto-mappings
- 30 QuickAdd choices, all targeting real folders
- 8 workspaces, 3 Kanban boards
- Monthly health automation is intentionally deferred; run the validation
  workflow manually when closing a maintenance slice.
