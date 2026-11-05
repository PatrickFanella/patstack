# Fleet ownership compatibility for Subsets stacks

The owner authorized installation on all six homelab devices and refresh of
T3/Codex/Claude clients that need the new skill discovery. Kvant already has
the unified selection. The other devices use the November 3 fleet rename
receipts rather than the personal installer's `installed.json` format.

`catalog/fleet-skill-predecessors.json` pins source-tree fingerprints from
the two revisions named by those receipts. Ownership transfer requires the
actual canonical source tree to match that pinned identity. The historical
recipe could add group-write under umask 0002; only that bit is normalized for
source-identity comparison. Executable and other permission bits, bytes, paths
and link targets still participate. The transaction captures and guards full
actual snapshots, including modes; no old receipt or baseline is rewritten to
accept a local edit. Unmatched copies remain protected.

The legacy generated Claude root on Almaz can be detached with
`prepare-client-root.py`. Its plan accepts only the known user-owned generated
profile layout, backs up the original link, and creates individual views to
the same backing entries. It does not write the backing sources. Undo the
selection transaction before undoing this separate root migration.
The selector accepts the resulting child views only when the complete root
still matches that transaction's installed receipt, its journal is complete,
and the original root-link backup matches. It replaces views for canonical
skills while retaining their original backing copies and unknown app views.

Deployment still requires a safe core plan. Specialist sets blocked by local
collisions are recorded as unavailable in the host's category-plan receipt;
they do not authorize discarding local edits or prevent a safe core rollout.
On the observed Sputnik inventory, three modified specialist copies differ
from the pinned source and therefore retain their current state.

Fixtures cover historical receipt transfer without a synthetic baseline,
changed bytes/permissions refusing identity, generated-root recovery and
unchanged application backing sources. Host receipts establish deployment;
fresh discovery and service/process readback establish client refresh separately.
