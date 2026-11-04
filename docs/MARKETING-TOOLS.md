# Shared marketing tools

The shared procedures `voice-ledger`, `content-recaster`, and `launch-dossier` are authored under `shared/` in this repository. Their source provenance identifies the reviewed Okara files by SHA-256. The full research archive remains separate at `~/Work/Research/Okara/2026-10-19` on Kvant. No public redistribution license was established for the imported originals.

Use `$voice-ledger` to define or review written voice, `$content-recaster` to adapt an actual source asset into selected channels, and `$launch-dossier` to create or refresh a complete product packet. Existing agent sessions keep their initial skill catalog; start a fresh session after installation. The launch-dossier skill includes the original Subcult starter and seven drafting prompts as portable assets.

## Product sources and reading copies

- Subsets editing source: `~/Work/Tools/subsets/docs/marketing/` on Kvant.
- CLPR editing source for this task: `/home/onnwee/.t3/worktrees/clpr/t3-471fd5e5/docs/marketing/` on Kvant.
- Generic template editing source: `shared/launch-dossier/assets/` in this repository.
- Synced reading bundle on each device: `~/Work/Research/Marketing-Packets/2026-10-19/`, containing `subsets/`, `clpr/`, and `generic/`.

The reading bundle's `SOURCE-MANIFEST.json` records original source and reading-copy hashes. Internal packet links remain local. Links into other repository documents are rewritten to their source revision on Gitea so the reading copy does not assume a matching checkout on every device. This is a versioned, manual sync snapshot; no recurring scheduler or automatic bidirectional writer was configured.

## Guarded deployment and updates

`scripts/marketing-fleet.py` handles only the three shared procedures, their Claude links when the client root permits them, and the dated marketing reading bundle. It uses the canonical installer transaction, backup, verification, and rollback functions. It refuses unmanaged conflicting paths and later edits, preserves matching installations under their existing owner, and leaves generated Claude roots under their generator's ownership.

After reviewing, validating, and committing selected skill sources, create a new frozen payload with explicit packet paths:

```sh
rtk proxy python3 scripts/marketing-fleet.py bundle --payload /path/to/new-payload.json --packet subsets=/path/to/subsets/docs/marketing --packet clpr=/path/to/clpr/docs/marketing --packet generic=/path/to/patstack/shared/launch-dossier/assets
rtk proxy python3 scripts/marketing-fleet.py plan --payload /path/to/new-payload.json --host sputnik
rtk proxy python3 scripts/marketing-fleet.py apply --payload /path/to/new-payload.json --host sputnik
rtk proxy python3 scripts/marketing-fleet.py verify --payload /path/to/new-payload.json --host sputnik
```

Review the plan before apply. Existing reading-copy edits cause refusal rather than an overwrite. Receipts, before-state backups, and the last plan are under `~/.local/state/marketing-fleet/` on each host. The `rollback` command with that host and payload restores the most recent recorded transaction only after checking for later changes. It leaves unmanaged source files and research archives alone. Kvant's shared-skill installation retains its separate canonical installer receipt.

## October 19 deployment result

Deployed source revision: `a92bf87`. All three shared skill directories and the reading bundle were verified on Kvant, Sputnik, Soyuz, Dozor, Almaz, and NUC. Fresh Codex app-server `skills/list` calls reported each new skill once and enabled on all six devices.

Claude links were installed on Kvant, Sputnik, Soyuz, Dozor, and NUC. Almaz's `~/.claude/skills` points to `~/.agents/.generated/skill-profiles/full/skills`; that generated root was preserved, so these three Claude links were not added there. This does not block their verified Codex discovery on Almaz.

Canonical validation and all 48 unit tests passed, including the new fleet adapter's idempotency, rollback, destination-drift, and foreign-owner checks. All three skill entrypoints passed the system validator. The five Subsets packet files passed Markdown lint using the same documentation configuration as the CLPR packet, and local packet/asset links were checked. The Subsets demo remains a storyboard; no new install/apply/rollback product qualification or public campaign execution is claimed.

Kvant's detailed verification and discovery records are under `~/.local/state/marketing-fleet/`. These establish deployment and discovery, not execution of every procedure by each client.
