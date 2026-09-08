---
name: dependency-upgrade
description: Upgrade dependencies with lockfile evidence, breaking-change analysis, proportional testing, and rollback.
metadata:
  blacktower-pack: engineering
  blacktower-kind: workflow
  blacktower-tier: standard
  blacktower-capabilities: safe dependency upgrade,breaking changes,framework migration,lockfile changes,compatibility analysis
---

# dependency-upgrade

Upgrade dependencies with lockfile evidence, breaking-change analysis, proportional testing, and rollback.

Select the relevant procedure from [the task guide](guide.md). Load only that procedure, not the complete reference collection.

Keep the requested scope and repository conventions. Report evidence for the operation actually performed.

For a routine Python dependency update using uv, select the environment and package-manager procedure in `python-development`; reserve this skill’s major-upgrade phases for demonstrated compatibility work. Inspect the requested target and lockfile, update only that dependency, and run focused checks. If offline resolution fails, report the missing cached package without claiming an updated lock.
