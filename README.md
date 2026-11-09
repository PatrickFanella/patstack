# patstack

![patstack: the rack mark and wordmark beside three registered plates](brand/readme-banner.png)

patstack is the owner's agent skill stack: the personal skills, shared skills,
optional library, profiles, global agent instructions and the guarded tooling
that deploys them to every host. It was called `codex-skills` until 2026-11-03,
and Gitea redirects the old URL. It is separate from Blacktower's package catalog.

The source of truth is [git.subcult.tv/subculture-collective/patstack](https://git.subcult.tv/subculture-collective/patstack).
Gitea pushes it to the private GitHub mirror
[subculture-collective/patstack](https://github.com/subculture-collective/patstack)
on every commit and every 8 hours; open PRs on Gitea, not on GitHub.

Subsets manages the user-level skill selection and generated views across
Agents, Codex, Claude, Copilot, Cursor and OpenCode. Patstack owns 104 selectable
skill sources, a 37-skill everyday core, and 11 overlapping task sets. App,
package, repository and vault skills retain their local owners.

Start with [the task-stack guide](docs/SKILL-GROUPS.md) and
[complete membership reference](profiles/CATALOG.md).

## Brand

patstack has a selected identity: the **A1 Rack system with A3 Registration's plates**, chosen on November 3, 2026 from nine candidates. Rack units stand for the fleet, registered plates for the verify guarantee, and the status labels `[ACTIVE]`, `[WARNING]`, `[VETO]` and `[ARCHIVE]` always agree with the installer's real result. The masters live in SUBCULT Studio; [brand/GUIDE.md](brand/GUIDE.md) explains the rules and `brand/studio-assets.json` records where each copied file came from.

## Layout and ownership

- `skills/`: curated skill sources; selected and exposed by Subsets, not an always-installed Codex base.
- `shared/`: portable workflow sources; Subsets selects them through the same core/task profiles as other skills.
- `repository-skills/blacktower-development`: installed only in Blacktower’s `.agents/skills`, privately excluded through Git’s local exclude file.
- `library/skills/`: specialist source reservoir. Task profiles combine eligible sources from here, `skills/`, and `shared/`.
- `vault-agents/`: root `AGENTS.md` files and local skills for the four vaults, deployed by `scripts/vault-agents.py` (`catalog/vault-agents.json` maps each file, including the library copies of vault skills).
- `project-agents/`: project skills and instruction blocks, deployed by `scripts/project-skills.py` (`catalog/project-selections.json`).
- `instructions/`: the shared working rules (`WORKING.md`), per-host facts (`hosts.json`), Gitea identity and RTK guidance that `scripts/global-instructions.py` renders into every client's global file.
- `runtime-bundles/subsets-fleet/`: the Subsets adapter bundle built and deployed per host.
- `authoring/`: non-discovered guidance for maintaining the collection.
- `catalog/proposed-catalog.json`: authoritative target; `capabilities.json` maps imported and authored capabilities to owners and procedures. `retired-names.json` maps retired names, with no compatibility entrypoints.
- `catalog/baseline.json`: pre-migration hashes, modes, and symlinks. `installation.json` records this host’s destinations and immutable archive location.
- `evaluations/`, `tests/`, `reports/`: bounded behavior trials, deterministic tests, discovery measurements, and rollout evidence.

`omarchy` and `diagnose-crash` are OS-owned symlinks on hosts that still run Omarchy; Debian hosts lack them, and validation reports them as absent. Where they exist, their links and `/usr/share/omarchy` targets are protected. The personal `diff-auditor` duplicate is removed; its system owner is unchanged. Managed plugin caches are outside this installer’s authority.

Original trees are recoverable at `/home/onnwee/.codex/skill-backups/20260908T034154Z-before-consolidation`, outside discovered roots. Imported scripts, assets, and notices remain beside their applicable mode. Resource paths in a mode resolve from that mode’s directory. `<skill-root>` in command examples means the resolved directory of the loaded entrypoint, not the current project directory.

## Installation

User skills are installed through the reviewed Subsets bundle. Validate and
commit source changes, then build and deploy using the
[adapter runbook](runtime-bundles/subsets-fleet/README.md). The first migration
requires exact predecessor receipts and records recoverable backups. Later
switches modify only registered paths and preserve app/package/project owners.

The old personal and optional installers are historical migration tools. They
must not reclaim user skill paths after Subsets takes ownership. Vault and
project-local deployment remain separate.

## Maintenance

Gitea runs source validation and the disposable installer/selection tests on PRs and main. `python scripts/validate.py --source-only` checks the repository without reading installed OS or system skills. Its report lists those owners as unverified; installation verification still requires the normal validator and the destination checks below. CI never installs skills or changes client configuration.

Edit authored sources here; never maintain installed copies as the source of truth. Keep task descriptions concise and put substantial procedures in conditionally loaded references. Preserve plan-only, read-only review, explicit strict review, explicit TypeScript boundary setup, and separate publishing/deployment scope. New capabilities need a concrete trigger, resource links, and an acceptance fixture. General principles belong in relevant conditional references, not new globally discovered entrypoints.

`build_collection.py` is the historical one-time import recipe, not an update command: rerunning it is unsupported after curation. Update the catalog and capability map explicitly when changing ownership. Preserve provenance and licenses when moving resources. The frontend CSV dataset is pinned to MIT-licensed upstream revision `363cd8911f210ec640704101ee820e6e64a63c3b`; its per-file hashes and notices are in `skills/ui-craft/scripts/data/provenance.json` and `notices/`.

Before each release, run validation and focused helper tests, then bounded behavior fixtures. Permit at most one repair-and-retest round per failed behavioral case. Capture fresh `skills/list` in Blacktower and an unrelated repository with `scripts/discovery.py`. Confirm shared owners appear once, retired names are absent, and the Blacktower skill stays local. Source character budgets and runtime metadata measurements are distinct from model token billing; report unavailable token usage explicitly.

Changes land through PRs on Gitea; CI must pass before merge. After a merge, pull the canonical checkout on Kvant (`~/Work/Tools/patstack`) under `umask 022` so installers do not see group-writable modes as drift, then run the relevant deployer. See [the operating model](docs/OPERATING-MODEL.md) and [the September review](reports/2026-09-20-upstream-review.md).

## Subsets TUI and CLI

[Subsets](https://git.subcult.tv/subculture-collective/subsets) owns the standalone skill manager application. It discovers local skills, organizes named groups, and previews/applies selections with recorded ownership and recoverable backups. Its optional adapter edits canonical profiles and calls this repository’s guarded deployment commands.

The application source lives in the sibling `subsets` repository. Original application history remains in commit `88d665b`; the private migration checkpoint preserves the original directory and machine verification report.

```sh
uv tool install --editable ../subsets
subsets
subsets apply --frontend-mobile --dry-run
```

System and plugin directories retain their owners. Existing installer-managed roots use explicit backends. See the [discovery and ownership guidelines](https://git.subcult.tv/subculture-collective/subsets/src/branch/main/docs/discovery-ownership.md) before adopting another folder.

## Subsets task stacks

`core` is the complete everyday default, with 42 skills. Additional stacks mix
planning, implementation, verification, research and communication around a task.
They overlap deliberately and can be combined. There is no hidden, separately
installed personal base.

```sh
rtk proxy subsets apply --build-and-ship --dry-run
rtk proxy subsets apply --build-and-ship
rtk proxy subsets apply --research-and-write --product-and-launch
rtk proxy subsets apply --group core
```

The default router can read an inactive specialist for a one-off task without
switching stacks. Required and optional companion references remain conditional.
Start a fresh client session after changing directly discoverable skills.

[The guide](docs/SKILL-GROUPS.md) lists every stack, its purpose, selected counts,
client roots, exceptions and recovery. [The membership catalog](profiles/CATALOG.md)
lists each core skill and each stack's additions with source links. Regenerate
both with `python scripts/stack-catalog.py`; use `--check` to detect drift.

## License

Original contributions in this repository are licensed under the GNU General
Public License, version 3 or (at your option) any later version
(`GPL-3.0-or-later`). See [LICENSE](LICENSE).

Third-party code, documentation, fonts, data, and other assets retain their own
licenses, copyright notices, and attribution. This license does not replace
those terms or grant rights to upstream material that its authors have not granted.
