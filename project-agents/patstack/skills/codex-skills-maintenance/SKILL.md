---
name: codex-skills-maintenance
description: "Codex-skills repository upkeep. Use to inventory skills, change a skill's scope, profile or deploy map, import or update upstream skills, or check discovery after an upgrade. Not for running a skill's own task."
---

# Skill maintenance

Read root AGENTS.md and docs/OPERATING-MODEL.md in the canonical patstack checkout. Installed personal/shared copies and project selections are deployments; system, OS and plugin packages keep their owners. Inspect current Git status and destination drift before proposing a change.

For an inventory, run the bundled `scripts/audit_skills.py`; its defaults include both personal and shared installations. Metadata/structure findings are review clues, not proof that a procedure works. Use `catalog/qualification.json` for canonical owner, client contract, evidence and blocked entries. Compare task-visible discovery, a fresh local app-server probe and installed plugin state rather than treating recursive cache counts as active skills.

For a scope or behavior change, read [audit criteria](references/audit-criteria.md). Preserve useful resources and provenance, define an expected task and a nearby task that should not activate it, and adapt unsupported tool contracts before qualification. Read [external intake](references/external-intake.md) only for importing/updating upstream skills or an explicit skills CLI request.

Author the canonical source, update catalog paths and qualification evidence, then run `python3 -B scripts/validate.py` and `python3 -B -m unittest discover -s tests -v` from the source repository. Validate changed skill entrypoints with the current system `skill-creator`. Test substantial behavior using offline fixtures or authorized bounded operations; report the proof boundary.

Commit only reviewed paths. Use `umask 022` to avoid deployment mode drift. Subsets owns user skill selection and generated client views: build the reviewed `subsets-fleet` bundle, preview the installed selector, deploy and verify it. Do not run the legacy personal/profile/client-link installers after ownership transfer. Vault files use vault-agents.py; project/worktree selections use project-skills.py. Preserve locks, receipt-backed adoption, transaction backups and later edits. Regenerate the task guide with `scripts/stack-catalog.py`. Confirm owners and retired names in fresh discovery from actual destinations and a real worktree. Existing sessions retain their initial catalog; local evidence does not establish fleet, provider or publication state.
