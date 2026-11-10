# Subsets user skill stacks

This adapter is the Subsets owner for the user-level skills from patstack's
`skills/`, `shared/` and qualified `library/skills/` sources. One selection
combines the 26-skill core with requested task sets. Individual links expose the
same reviewed sources under Agents, Codex, Claude, Copilot, Cursor and OpenCode.
App/package/system and project/vault skills retain their locations and owners.

See [the task guide](../../docs/SKILL-GROUPS.md) and
[membership reference](../../profiles/CATALOG.md). The pinned application is
`@subcult/subsets@0.2.0-alpha.6`; the source bundle is versioned independently.

## Build and preview

Validate, test and commit the source first. Build from an `umask 022` checkout:

```sh
rtk proxy python -B scripts/validate.py
rtk proxy python -B -m unittest discover -s tests -v
rtk proxy python -B scripts/stack-catalog.py --check
rtk proxy python -B runtime-bundles/subsets-fleet/scripts/build-bundle.py
```

The command prints an immutable deployment folder. Its manifest records the
source revision and file snapshots. Use that folder's `scripts/skill-profile`
with `plan core` before deployment. Inspect all changed paths, transfer records,
client exclusions and protected entries. Do not reset a baseline to pass drift.

Deploy that folder's `scripts/deploy-host.py` with `--node` and `--python` set to
the target host's inspected runtime paths. The application must already be the
pinned version. Deployment preserves unrelated launchers/state and records a
host receipt; it returns to core from the new source.

## First migration

`catalog/skill-stacks.json` names supported user roots and predecessor receipts.
Takeover locks those predecessors and checks exact current snapshots before
changing skill paths. Only recorded known owners can transfer. The same
transaction backs up/replaces the active views, releases transferred path
records from the old manifests, and writes the Subsets ownership marker.
Unknown entries and hidden/system skills are protected; collisions and linked
client roots refuse migration. The source-link installer skips transferred
views; the legacy personal and optional installers refuse user selection.

The public Subsets package is a separate product from this personal bundle.
Updating a local package is not npm publication or a fleet rollout.

## Switch, verify and recover

```sh
rtk proxy subsets apply --operate-homelab --dry-run
rtk proxy subsets apply --operate-homelab
rtk proxy subsets apply --group core
rtk proxy ~/.agents/bin/skill-profile verify core
```

Start a fresh agent session after switching. File/link verification does not
establish missing tools, authentication, application restart or execution in
all clients. The router can read an inactive specialist without a switch.

Transactions are under `~/.local/state/subsets-fleet/profiles/run-*`. Use the
recorded directory with `~/.agents/bin/skill-profile rollback --run`, newest run
first; an older run refuses while a newer one is recorded. Rollback restores
original paths only when current state still matches that run; it refuses later
edits. Rolling back the takeover puts the released records back into the
predecessor manifests and keeps records that `link-workstation.py` wrote later.
After takeover, predecessor rollbacks refuse to reclaim transferred paths.
Activation rechecks catalogs, stack lists and selected skill folders against
the bundle manifest, including files added after the build.

Roll back a detached Claude root with `prepare-client-root.py rollback --run`
after the Subsets takeover rollback. Entries added to the root after detachment
move to that run's `preserved-entries/` folder before the link is restored.
Retain backups and immutable source folders while needed for recovery. Removing
a view is deactivation, not canonical source deletion.
