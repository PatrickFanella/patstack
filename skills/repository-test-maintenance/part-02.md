## Establish the actual baseline

Read applicable repository instructions and inspect the checkout, branch, remotes, worktrees, and dirty/untracked files. If asked to get up to date, fetch configured remotes and compare commits before editing. Determine the authoritative branch from repository evidence. Fast-forward where safe; preserve local changes and unique commits when histories diverge. Do not interpret “up to date” as permission to upgrade every dependency.

Use the runtime and package manager specified by the repository and CI. Record baseline test discovery, results, coverage, type checking, and build status sufficiently to distinguish existing failures from regressions. Run the relevant broad checks once, with logs outside tracked source. A transpiler build is not a TypeScript check; a passing unit run is not proof that integration tests ran.

Inventory source entry points, test tiers, CI jobs, generated outputs, and maintained documentation. Understand the core journeys and high-consequence boundaries before selecting deletions.
