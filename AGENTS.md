# Personal Codex skill collection

Use `rtk` for shell commands. Author in this repository; installed copies are deployment targets.

Keep the catalog and capability map complete. Validate with `python scripts/validate.py` and `python -m unittest discover -s tests` before installation. Never bypass installer drift detection or alter OS-managed skills, system skills, or plugin caches.

Skill bodies should select a task mode and load only its relevant references. Preserve authorization, provenance, executable resources, and the user's requested stopping point. Archive originals outside discovery; do not create aliases for retired names.

For agent-instruction edits, read `authoring/writing-for-agents/guide.md` and the relevant referenced part. For source ownership, optional profiles, RTK, HOMELAB, and installation, read `docs/OPERATING-MODEL.md`. New upstream-derived procedures need pinned provenance and a positive/near-miss acceptance case.

For skill inventories, source changes, profile selection or deployment changes, read the local `.agents/skills/codex-skills-maintenance/SKILL.md` when deployed, otherwise its canonical source at `project-agents/patstack/skills/codex-skills-maintenance/SKILL.md`.

<!-- managed-project-skills:start -->
For skill, profile, qualification or deployment changes, read `.agents/skills/codex-skills-maintenance/SKILL.md`. This local procedure is authored in this repository; use the guarded project selection deployment for other worktrees. Read `docs/PROJECT-SKILLS.md` for selection commands.
<!-- managed-project-skills:end -->
