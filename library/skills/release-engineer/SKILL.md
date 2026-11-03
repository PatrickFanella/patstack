---
name: release-engineer
description: "Release Blacktower packages: builds, installers, generated schemas, bundled skill index, migrations, release notes. Use when a Blacktower change alters what users install or upgrade. Not for other repositories."
metadata:
  blacktower-pack: engineering
  blacktower-kind: internal
  blacktower-tier: niche
  blacktower-capabilities: dev-workflows,release,engineer
---

# Release Engineer

Use this skill when a change affects what users install, what the package ships,
or how upgrades behave.

## Release-safe workflow

1. **Classify the release impact**
   - runtime-only patch
   - config/schema migration
   - CLI installer behavior
   - bundled skill catalog
   - generated asset/schema
   - package file list

2. **Update required artifacts**
   - `blacktower.schema.json` after schema changes
   - `src/skills/index.json` and `src/skills/index.md` after skill changes
   - README/docs for user-visible behavior
   - release artifact verification scripts for packaged files

3. **Validate package readiness**
   - Use `references/release-surface.md` as the checklist.
   - Use `templates/release-notes.md` for release summaries.
   - Use `scripts/release_changed_files.py <paths...>` to group changed files by
     release surface.

4. **Run checks**
   - `bun run check:ci`
   - `bun run typecheck`
   - `bun test`
   - `bun run build`
   - package/release verifier if changed

## Guardrails

- Do not silently remove packaged assets users may depend on.
- Do not change installer defaults without docs.
- Do not commit generated artifacts without the source changes that generated
  them.
- Do not call a release ready if package validation was skipped.
