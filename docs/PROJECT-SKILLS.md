# Project and client skill selections

Author sources and mappings in patstack. `catalog/project-selections.json` registers the canonical Git owner, source folders, clients and short root instruction block. `.agent-skills.json` in each checkout is a generated receipt of its selection and hashes, not a second editable source. Copies under .agents/skills are generated deployments; Claude and OpenCode use relative links to those copies.

The project installer checks the target’s Git common directory against its registered owner, refuses path escape, symlink parents, unsupported client contracts and destination drift, and preserves every unrelated skill. A checkout gets its own private transaction and verified backups. Root AGENTS text outside the managed block is preserved; later root edits require a reviewed baseline rather than silent overwriting. The current deployed source and code must match committed bytes.

```sh
rtk proxy python -B scripts/project-skills.py plan --project patstack --root /home/onnwee/Work/Tools/patstack
rtk proxy python -B scripts/project-skills.py apply --project patstack --root /home/onnwee/Work/Tools/patstack
rtk proxy python -B scripts/project-skills.py verify --project patstack --root /home/onnwee/Work/Tools/patstack
```

Use the same project ID and the actual isolated checkout path for a worktree. This does not change a global profile. New projects can select reviewed optional library sources through a registered mapping; merely writing a declaration without materializing it does not establish discovery. Existing local facts and procedures should stay with their project owner.

The initial mappings cover patstack maintenance, Studio preparation and its subcult-tv consumer. Root instructions trigger procedures only for the relevant task. CLI `rollback --run PATH` restores this root’s recorded transaction while preserving intervening edits. Discovery and filesystem readback do not prove a model followed the procedure or that external services work.

## Copied worktrees without an installation record

A Git-created worktree can contain committed generated skills without this host's per-worktree installer transaction. A later source update then fails the drift guard. Before registering a root-specific bootstrap baseline in the canonical project selection, compare the complete copied file set, bytes and modes against the exact earlier committed skill source, verify the client links, and match every source hash in `.agent-skills.json`. Store it under `rootBaselines` for that exact checkout; record the source revision and review in `baselineProvenance`. Preserve a differing copy; never register arbitrary current bytes merely to make installation pass. The normal installer still previews the change, saves backups and verifies destination hashes.

## Studio skill ownership

Canonical Studio skill instructions live under `project-agents/subcult-tv/skills/` in patstack. The current subcult-tv selection includes `social-craft`, `studio-reference-study`, `studio-brand-audit` and `studio-brand-handoff`. `studio-brand-system` moved to the Subsets core on November 8, 2026. Their ownership and routing are registered in `catalog/local-owners.json`, `catalog/capabilities.json` and `catalog/qualification.json`; `catalog/project-selections.json` selects the project deployment.

Studio's guides, studies, brand masters and resulting assets remain in `subcult-tv/studio/`. Worktree `.agents/skills/` copies, Claude/OpenCode links and `.agent-skills.json` are generated destinations. Edit the canonical instruction once, validate and commit it, then use the project installer for each intended checkout. System, OS and plugin skills retain their package owners.

## Optional Codex and Claude selection

The same reviewed profile can be previewed for Codex and Claude. Claude linkage is explicit; it does not copy Codex plugins, tools, settings, permissions, accounts or authentication. Unreviewed or blocked client contracts stop application.

```sh
rtk proxy ~/.agents/bin/skill-profile plan mobile
rtk proxy python -B scripts/optional-clients.py plan --profile mobile
rtk proxy ~/.agents/bin/skill-profile activate mobile
rtk proxy python -B scripts/optional-clients.py apply --profile mobile
rtk proxy python -B scripts/optional-clients.py verify --profile mobile
```

Return to core with `skill-profile deactivate`, then `optional-clients.py apply` and `verify` without a profile. The link installer removes only its previously managed optional links, preserving other personal/account-synced skills. Each client starts a fresh session after selection changes. Inspect/rollback its own transaction if the second stage fails; do not claim cross-client success from a Codex-only activation.

The project paths follow the documented [Claude project skill location](https://code.claude.com/docs/en/skills) and [OpenCode skill locations](https://opencode.ai/docs/skills/). Actual Codex discovery is checked through a fresh local app-server; link readback alone does not prove a Claude/OpenCode model invocation.

## Qualification records

`catalog/qualification.json` records each canonical source, owner, supported clients, required tools, last review, routing examples and evidence. `scripts/qualification.py` reports source findings or an exact entry via `--name NAME`. Structure-reviewed and selection-tested are different proof levels; neither proves live task behavior. Unreviewed imports remain reservoir material. Archived sources are preserved and excluded by ownership filtering. Blocked entries cannot be activated by a named profile or --all.

Compatibility-scan requires four named specialist agents and a declared scanner absent from this runtime. Its YAML is repaired, but it remains blocked. The retained poteto-mode import has a folder/name mismatch and also remains blocked. A missing agents/openai.yaml or supported extra frontmatter alone is not a defect.
