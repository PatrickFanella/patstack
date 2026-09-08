---
name: clonedeps
description: Inspect dependency source at the lockfile-resolved version; obtain only the repositories needed for the investigation.
metadata:
  blacktower-pack: core
  blacktower-kind: workflow
  blacktower-tier: core
  blacktower-capabilities: dependency source inspection,upstream implementation,sdk internals,pinned source checkout
---

# clonedeps

## Use this skill

Clone important project dependency source code into an ignored local workspace so the active agent can inspect library internals. Use when the user asks to clone dependencies, inspect dependency/source internals, understand SDK/framework behavior from source, debug library implementation details, or make core dependency repos locally readable. Do not use for ordinary API/docs questions where ordinary documentation lookup is enough.



## Resources

- `references/detailed-guide.md` — detailed framework and edge cases; load only the sections needed for the task.
