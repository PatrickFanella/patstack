# Skilldeck

Skilldeck discovers agent skills on disk, helps organize named groups, and applies a selection through registered folder ownership or the existing codex-skills backend. Open the TUI with `skilldeck`; automate the same operations with its CLI.

This first release runs on Linux and macOS with Python 3.11 or newer. It uses Textual for the interface and POSIX filesystem locks for changes. Windows is not supported by this release. The working name is Skilldeck; no public package or repository has been published.

## Install and open

From this application's directory:

```sh
uv tool install --editable .
skilldeck
skilldeck discover
skilldeck discover --filter writing
skilldeck roots
skilldeck groups
```

For an isolated checkout without installation, use `uv run --project apps/skilldeck skilldeck` from the repository root. The TUI requires an interactive terminal. Every mutation also has a noninteractive CLI path; `--json` returns structured output.

## Organize and apply

Inspect the detected folders with `skilldeck roots`. Adopt an unmanaged folder by its displayed root ID:

```sh
skilldeck adopt ROOT_ID
skilldeck group create creative-writing poetry editing
skilldeck apply --creative-writing --dry-run
skilldeck apply --creative-writing
skilldeck verify
skilldeck history
skilldeck rollback TRANSACTION_ID
```

Adoption leaves the existing skills in place, makes verified canonical copies in Skilldeck's private library, and records the paths it may subsequently manage. It creates a `current-ROOT_ID` group representing that folder's original selection. In the TUI, deselect this group and select your new group before previewing a narrower selection. `core` is always included; add skills to it when they should remain active across group changes.

Groups combine by union:

```sh
skilldeck apply --creative-writing --research --dry-run
skilldeck apply --group creative-writing --group research
skilldeck group add creative-writing storytelling
skilldeck group remove creative-writing editing
skilldeck group add core fact-check
```

Short flags are accepted only for existing group names. A misspelled group fails instead of applying an empty selection. Duplicate skill names require their displayed `ROOT_ID:skill-name` IDs. `--group NAME` is the stable explicit syntax.

Inactive skills remain in the private library. To add another source folder and import a skill into a registered destination:

```sh
skilldeck root add ~/SkillSources --owner readonly
skilldeck discover
skilldeck import SOURCE_ROOT_ID:storytelling --to TARGET_ROOT_ID
skilldeck group add creative-writing TARGET_ROOT_ID:storytelling
```

Imports do not activate a skill until a group containing it is applied. Create an empty supported destination such as `~/Project/.agents/skills`, register it with `root add PATH --owner unmanaged`, then adopt it. Source folders default to read-only when explicitly registered. For a one-off inspection, use `--root PATH` instead.

## TUI workflow

- Search with Ctrl+F. Enter on a skill toggles it for group editing.
- In Folders, select a root and choose **Adopt folder**. The dialog explains the ownership change.
- **Edit group** creates a group or adds/removes the picked skills. Eligible optional library skills edit canonical existing profiles; adopted skills edit Skilldeck groups.
- Select groups in the sidebar, then **Preview** or Ctrl+P. The preview is checked again when you choose **Apply selection**.
- Recovery lists Skilldeck transactions. Select one and choose **Rollback**. Changes made through the existing deployment backend retain that backend's receipts and rollback commands.
- Ctrl+R rescans. Q exits. The interface adapts to 80×24 and larger terminals.

## Existing codex-skills installations

Skilldeck recognizes the canonical source behind `~/.agents/bin/skill-profile`. It displays eligible optional library skills and named profiles, excludes reserved/retired/blocked names, and sends selected profiles through `skill-profile` and `optional-clients.py`. It preserves the curated personal base, shared core, plugins, vault ownership and project installations.

```sh
skilldeck apply --mobile --dry-run
skilldeck apply --mobile
skilldeck group create creative-writing copywriting storytelling --backend existing
```

The last example requires those names to be eligible in the actual library. Use discovery to choose available skills. Profile edits write only the named canonical `profiles/NAME.txt`, preserve existing comments, and have a Skilldeck backup/receipt. Review and commit these configuration edits with the source repository. The app does not automatically commit, push, or publish them.

An existing backend profile selection applies to optional Codex/shared skills and explicit Claude links. It does not transfer tools, authentication, settings, or permissions. Unsupported Claude contracts stop preview. If the backend fails after Codex activation, the app reports partial completion and retains the backend's recovery state. This bridge is sequential rather than one atomic cross-client transaction.

Skilldeck groups and existing backend profiles cannot be combined in one apply. They have separate ownership and recovery. Explicitly choose `--backend skilldeck` or `--backend existing` when editing or applying groups if the names are ambiguous. For a new machine without this repository, the standalone adoption/library/group workflow requires no codex-skills source.

## State and recovery

Private state defaults to `$XDG_DATA_HOME/skilldeck`, or `~/.local/share/skilldeck`. Use `SKILLDECK_HOME` or `--state PATH` for an isolated registry. It contains `registry.json`, the canonical `library/`, and journaled `transactions/` with verified before-state backups. The state directory has mode 0700; registries and journals have mode 0600. Keep this directory while recovery may be needed.

Apply preflights all registered paths before mutation, verifies copied resources and executable modes, and checks again before replacements. Drift stops application. An interrupted apply blocks later changes until its transaction is rolled back. Rollback preflights every affected path and refuses later edits, including group/registry edits. Undo newer transactions first when they changed the same registry. Unregistered skills and other root files are preserved.

Skilldeck does not rewrite skill instructions or execute their scripts. Adoption is a filesystem ownership decision, not proof of tool compatibility, instruction quality, licensing, or actual agent behavior. Disk discovery also includes installed plugin versions that may be inactive; it is not the client's live skill catalog. Start a fresh client session after changing selection and verify its discovery separately.

See [discovery and ownership rules](docs/discovery-ownership.md) for the supported locations, guardrails, and extension procedure.

## Development

```sh
uv run --extra test pytest
uv build
```

Tests cover discovery scope, adoption, grouping, application, idempotency, imports, resource modes, interrupted recovery, drift, package/installer ownership, CLI flags, existing profile authoring, and an interactive TUI flow.
