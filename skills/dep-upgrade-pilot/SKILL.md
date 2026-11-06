---
name: dep-upgrade-pilot
description: Use when upgrading a dependency or framework across a major version, with breaking-change analysis, lockfile review and rollback. Not for a routine uv bump; use python-uv-workbench.
metadata:
  blacktower-pack: engineering
  blacktower-kind: workflow
  blacktower-tier: standard
  blacktower-capabilities: safe dependency upgrade,breaking changes,framework migration,lockfile changes,compatibility analysis
---

# dep-upgrade-pilot

Upgrade dependencies with lockfile evidence, breaking-change analysis, proportional testing, and rollback.

## Rules for every upgrade

- Read the target's changelog and migration guide before changing anything.
- Upgrade one dependency, one major version at a time, and run the tests and build after each step. Never upgrade everything at once.
- Bulk commands such as `npm audit fix`, `npm-check-updates -u`, `--force` and `--legacy-peer-deps` change more than the target; run them only when the user asked for that scope.
- Work on a branch with a rollback path, and preserve uncommitted user work before any rollback; the sample rollback script assumes a clean tree.

Read only the [task guide](guide.md) entries whose trigger matches the work. Keep the requested scope and repository conventions. Report evidence for the operation actually performed.

For a routine Python dependency update using uv, select the environment and package-manager procedure in `python-uv-workbench`; reserve this skill’s major-upgrade phases for demonstrated compatibility work. Inspect the requested target and lockfile, update only that dependency, and run focused checks. If offline resolution fails, report the missing cached package without claiming an updated lock.
