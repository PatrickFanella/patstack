# Optional skill profiles

Source: `codex-skills/profiles`. Run `~/.agents/bin/skill-profile list` for live eligible counts and `plan PROFILE` for the exact selection. Profiles add optional shared skills alongside the curated Codex base. Managed interview/handoff skills remain present. Curated or retired entrypoint names are filtered out, even under `--all`.

Use `activate PROFILE`, `deactivate` for core, and `status` for drift. Restart agent sessions after a change. Edit and commit canonical sources in `codex-skills`; installed copies are not independent authorship locations. See `docs/OPERATING-MODEL.md` in that repository.
