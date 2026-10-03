# Optional skill profiles

Source: `codex-skills/profiles`. Run `~/.agents/bin/skill-profile list` for live eligible counts and `plan PROFILE` for the exact selection. Profiles add optional shared skills alongside the curated Codex base. Managed interview/handoff skills remain present. Global curated or retired entrypoint names are filtered out, even under `--all`.

Use `activate PROFILE`, `deactivate` for core, and `status` for drift. Restart agent sessions after a change. Edit and commit canonical sources in `codex-skills`; installed copies are not independent authorship locations. See `docs/OPERATING-MODEL.md` in that repository.

The following specialists are optional. Their curated procedures live under
`library/skills/`; older optional source versions are archived under
`authoring/optional-originals/2026-10-03/` with file hashes in the catalog.

| Profile | Adds to the five-skill core |
|---|---|
| infrastructure | kubernetes-development, terraform-module-library |
| charting | lightweight-charts |
| reverse-engineering | reverse-engineering |
| smart-contracts | solidity-security |

For example, run `rtk proxy ~/.agents/bin/skill-profile plan infrastructure`,
then `activate infrastructure` when needed. Profiles can be combined. Use
`deactivate` to return to core. These selections govern Codex optional shared
skills; Claude uses explicit source links and needs its own deliberate link
selection. No specialist is active in the default core.

Additional focused profiles are mobile, terminal-ui, browser-extension-development,
temporal and learning-exercises. They respectively select React Native, OpenTUI,
userscript/VS Code extension work, the two Temporal procedures, and exercise scaffolding.
Known blocked qualifications are filtered even under --all. See docs/PROJECT-SKILLS.md
for guarded local/worktree selections and matching Claude optional links.
