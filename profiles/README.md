# Task profiles

Subsets selects `core` plus the union of requested task sets. Core contains 27
skills for everyday work; the 11 other sets combine disciplines around an
outcome. There is no separate always-installed personal or shared layer.

See [the guide](../docs/SKILL-GROUPS.md) for purposes, client views and recovery,
and [the membership catalog](CATALOG.md) for every addition. An inactive skill
can be read through the default router without switching the whole stack.

Preview with `subsets apply --build-and-ship --dry-run`, apply with
`subsets apply --build-and-ship`, and return with `subsets apply --group core`.
Start a fresh session after changing discovery. Use the lower-level selector
only for its recorded status, verification or rollback commands.

Edit and commit profiles here. Regenerate the guide with
`python scripts/stack-catalog.py`, then build and deploy a reviewed bundle as
[the adapter runbook](../runtime-bundles/subsets-fleet/README.md) describes.
Previous category files are archived outside discovery under
`authoring/profile-history/2026-11-05/`.
