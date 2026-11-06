---
name: repo-atlas
description: Use when orienting in an unfamiliar repository, or creating or incrementally updating codemap.md files with the bundled inventory script. Not for one how-does-X-work question (repo-research-trail) or architecture redesign (boundary-drafter).
compatibility: Requires a git repository and a Node.js-compatible runtime or Bun for the bundled codemap helper.
metadata:
  blacktower-pack: core
  blacktower-kind: tool-wrapper
  blacktower-tier: core
  blacktower-capabilities: repository map,codebase orientation,module ownership,architecture navigation
---

# repo-atlas

Map repository structure and update existing code maps incrementally using the bundled inventory helper.

## Rules for every run

- For orientation alone, read existing `codemap.md` files, the tree and entry points, and report. Write `codemap.md` files, `.blacktower/codemap.json` or the `AGENTS.md` Repository Map section only when the user asked for codemaps.
- Map core code and configuration only. Tests, documentation, translations, build output and dependencies stay out of the include patterns.
- With existing state, update only the folders the change detection reports as affected.

Read only the [task guide](guide.md) entries whose trigger matches the work.

Keep the requested scope and repository conventions. Report evidence for the operation actually performed.
