# Subsets task stacks and user-skill ownership

The owner requested one Subsets manager for user-level skills across clients,
a substantial general core, and task sets that combine disciplines. App and
repository-specific skills retain their current owners and locations.

## Selection

The reviewed source inventory has 220 selectable canonical owners: 52 curated,
six shared and 162 specialists. The historical source labels remain for
provenance, not runtime activation. Core contains 40 skills. Eleven overlapping
task sets add the procedures useful for an outcome; core is always unioned in.
Every selectable owner belongs to at least one profile. Earlier category files
are archived under `authoring/profile-history/2026-11-05` outside discovery.

The guide and membership catalog are generated from profile files, metadata
and `catalog/skill-stacks.json`. The router retains conditional companion links
and can read inactive sources without a stack switch. Cursor and Copilot use
the explicitly configured Claude-compatible file contract; this does not
establish tool or provider equivalence.

## Ownership transfer

The Subsets adapter builds sources from all three trees. It exposes selected
sources through individual links in the configured client roots, without
replacing roots. The first takeover checks existing installer receipts under
locks, backs up every affected path, releases only transferred records from
the predecessor manifests, and writes the new ownership marker in the same
transaction. No baseline is reset or unowned same-name path overwritten.

The selector protects app/package/system/unknown entries. Local drift, linked
roots, escaping paths, modified source files, unknown stack members, and changed
ownership receipts stop the affected operation. The old personal/profile/link
writers cannot reclaim the new views. Original files and ownership manifests
remain recoverable, with all-path rollback preflight and refusal of later edits.

Subsets application changes add native Copilot/Cursor discovery, recognize
the new owner, preserve package identity inside managed roots, and inventory
curated/shared/specialist sources together. Older backend layouts remain
supported. The application package is a separate local artifact; no npm
publication or other-host rollout is implied.

## Verification

Patstack's 87 Python tests passed, including receipt-backed migration,
cross-client switching, reverse rollback, conflict/drift refusal, source/root
escape checks, preservation of app/system owners, and complete profile coverage.
The existing suite includes the retained 11-case design scanner suite.
Source validation, generated-guide checking and local Markdown links passed.

Subsets application type checking and 30 Node tests passed, including existing
TUI behavior plus new discovery/owner/inventory cases. A disposable Codex home
confirmed one discovered entry when the same physical skill is linked through
both `.agents` and `.codex`. This is discovery evidence, not a model-execution
trial or proof of discovery in Copilot, Cursor, Claude or OpenCode.

Host deployment receipts and a fresh discovery capture establish the actual
local rollout. Remote CI, merge state, fleet parity and npm publication remain
separate claims.
