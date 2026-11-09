# Base procedure

Reviewed source clients: codex, claude.

Resolve command and resource paths from the owning skill root, unless a linked reference says otherwise.

# repo-atlas

Map repository structure and update existing code maps incrementally using the bundled inventory helper.

## Rules for every run

- For orientation alone, read existing `codemap.md` files, the tree and entry points, and report. Write `codemap.md` files, `.blacktower/codemap.json` or the `AGENTS.md` Repository Map section only when the user asked for codemaps.
- Map core code and configuration only. Tests, documentation, translations, build output and dependencies stay out of the include patterns.
- With existing state, update only the folders the change detection reports as affected.

Read only the [task guide](../guide.md) entries whose trigger matches the work.

Keep the requested scope and repository conventions. Report evidence for the operation actually performed.
