# Personal Codex skills

This repository authors the personal collection independently of Blacktower’s package catalog. It contains 62 managed personal entrypoints, two shared-personal overrides, and one repository-local Blacktower entrypoint. Two externally owned OS symlinks complete the 64-entrypoint personal catalog.

## Layout and ownership

- `skills/`: authored personal skills, installed as managed copies in `~/.codex/skills`.
- `shared/`: canonical `requirements-interview` and `session-handoff`, installed in `~/.agents/skills`. Duplicate Codex copies are retired.
- `repository-skills/blacktower-development`: installed only in Blacktower’s `.agents/skills`, privately excluded through Git’s local exclude file.
- `authoring/`: non-discovered guidance for maintaining the collection.
- `catalog/proposed-catalog.json`: authoritative target; `capabilities.json` maps all 138 original capabilities to owners and procedures. `retired-names.json` maps retired names, with no compatibility entrypoints.
- `catalog/baseline.json`: pre-migration hashes, modes, and symlinks. `installation.json` records this host’s destinations and immutable archive location.
- `evaluations/`, `tests/`, `reports/`: bounded behavior trials, deterministic tests, discovery measurements, and rollout evidence.

`omarchy` and `diagnose-crash` remain OS-owned symlinks. Their links and `/usr/share/omarchy` targets are protected. The personal `review-agent` duplicate is removed; its system owner is unchanged. Managed plugin caches are outside this installer’s authority.

Original trees are recoverable at `/home/onnwee/.codex/skill-backups/20260908T034154Z-before-consolidation`, outside discovered roots. Imported scripts, assets, and notices remain beside their applicable mode. Resource paths in a mode resolve from that mode’s directory. `<skill-root>` in command examples means the resolved directory of the loaded entrypoint, not the current project directory.

## Installation

Requires Python 3 on Linux; validation additionally needs PyYAML. The installer uses only the standard library. Run from this repository after committing reviewed sources:

```sh
python scripts/validate.py
PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s tests -v
python scripts/install.py plan > /tmp/codex-skills-plan.json
python scripts/install.py apply --through 1
# Use the run path printed by apply for both following batches:
python scripts/install.py apply --resume <run-path> --through 2
python scripts/install.py apply --resume <run-path> --through 3
python scripts/install.py verify
```

Review `plan` before applying. It is read-only and records source revision, destinations, expected/desired trees, ownership, and retired names. Each tree records SHA-256, executable modes, and symlink targets. `apply` writes a journal and verified original backups under `~/.codex/skill-installations/codex-skills/run-*`. Completed operations gain `backupLocation` and actual original state. The installed manifest is `~/.codex/skill-installations/codex-skills/installed.json`.

Apply rejects drift from the recorded baseline or last installed snapshot. Preserve intervening edits and review a reconciliation before updating the baseline; never bypass drift by overwriting it blindly. A repeated successful apply is idempotent. An unfinished batch must be resumed or rolled back. Completed paths are reverified when a later batch resumes.

```sh
python scripts/install.py rollback --run <run-path>
```

Rollback restores only that transaction’s changed destinations and the preceding installed manifest. It preflights all affected paths and preserves intervening edits. Interrupted apply and rollback can resume from journaled stages. Backups and originals remain outside discovery. Retain the repository and run directory until rollback is no longer needed.

## Maintenance

Edit authored sources here; never maintain installed copies as the source of truth. Keep task descriptions concise and put substantial procedures in conditionally loaded references. Preserve plan-only, read-only review, explicit strict review, explicit TypeScript boundary setup, and separate publishing/deployment scope. New capabilities need a concrete trigger, resource links, and an acceptance fixture. General principles belong in relevant conditional references, not new globally discovered entrypoints.

`build_collection.py` is the historical one-time import recipe, not an update command: rerunning it is unsupported after curation. Update the catalog and capability map explicitly when changing ownership. Preserve provenance and licenses when moving resources. The frontend CSV dataset is pinned to MIT-licensed upstream revision `363cd8911f210ec640704101ee820e6e64a63c3b`; its per-file hashes and notices are in `skills/frontend-design/scripts/data/provenance.json` and `notices/`.

Before each release, run validation and focused helper tests, then bounded behavior fixtures. Permit at most one repair-and-retest round per failed behavioral case. Capture fresh `skills/list` in Blacktower and an unrelated repository with `scripts/discovery.py`. Confirm shared owners appear once, retired names are absent, and the Blacktower skill stays local. Source character budgets and runtime metadata measurements are distinct from model token billing; report unavailable token usage explicitly.

There is no remote configured. Publishing or pushing this repository requires a separate request.

The optional library, profiles, profile command, and global Codex/RTK sources are now maintained here. See [the operating model](docs/OPERATING-MODEL.md) and [the September review](reports/2026-09-20-upstream-review.md).
