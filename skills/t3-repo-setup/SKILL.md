---
name: t3-repo-setup
description: "Use when onboarding a repository into T3 dev environments: launcher recipe, isolated worktree previews, tests and project actions. Not for running an already configured preview."
---

# T3 repository setup

Use this skill when asked to prepare a new or existing repository for our T3 development environment workflow. For an already configured repository that only needs a preview or test run, read the installed agent guide and use its commands; do not rebuild its configuration. Do not invent a product or deploy production.

## Inspect the repository and host

Read the nearest AGENTS.md and `~/.local/share/t3-dev-environments/AGENT-GUIDE.md`. Confirm the current host, absolute Git root, branch, dirty state, and canonical origin. Preserve current work. Use the selected host or current thread host; clarify only a material ambiguity. Do not replicate to every host.

Inspect package manifests, lockfiles, existing dev scripts, Compose files, CI, and environment templates. Determine toolchain versions, install/start commands, readiness path, databases, migrations, seed data, fast tests, and required broader verification. Read environment variable names without printing populated secret values. For an empty repository, use the user's chosen stack if available; otherwise clarify it before inventing a runnable app.

## Add or reuse a recipe

The canonical launcher source is `/home/onnwee/Work/Tools/t3-dev-environments` on Kvant; its private remote is `https://git.subcult.tv/PatrickFanella/t3-dev-environments`. On another host, inspect that source through existing authorized access. Installed copies under `~/.local/share/t3-dev-environments` are deployment targets. If source access is unavailable, prepare a patch and report the blocker; do not fork installed configuration.

Read current `dev.py`, `profiles.json`, `install.py`, and README. Reuse a compatible recipe. For a new one, derive setup/start/test/verify commands from the repository and follow the current schema. Check that the tools image supports the actual runtime. Unsupported stacks require an appropriate image or launcher change with validation; do not silently change the app's stack.

Keep each worktree's source snapshot, ports, caches, database, and test state separate. Use explicit nonsecret development values and synthetic data. Populated `.env` files are excluded: adding one is not an integration mechanism. If an external integration is required, identify its sandbox credentials, callback URL, and network needs; do not put real credentials in recipes or disable isolation to make a test pass.

Preserve test failures and repository gates. Describe the actual `verify` scope; custom commands must account for migrations. Preserve existing repository-owned setup, particularly Subcult OS.

## Install and prove the workflow

Run launcher regression tests after code or recipe changes. Deploy reviewed launcher files to the selected host with before-state checks and backups, preserving unrelated changes. Register the project through T3's supported UI/CLI/API if needed; never edit its live SQLite state. Run the installer and read back the intended actions and worktree default. Check root-name/profile matching; handle aliases without renaming the checkout.

From the intended worktree, prove dependency setup, app readiness, source sync after an owned temporary edit, a relevant test, exit status, and cleanup. Restore only your temporary edit. Confirm worktree isolation without borrowing another thread's preview. For remote previews, verify the printed tunnel command uses the exact worktree root and the tunneled URL responds. Do not stop other threads to free a slot.

Report host/root/revision, recipe and source changes, actions installed, preview access, exact checks and failures, remaining integration limits, and retained processes/data. Link the maintained guide from repository instructions when appropriate, preserving existing requirements. Follow the host documentation policy for operational changes. Commit scoped changes; publish only when authorized. A configured hook is not proof that a new T3 thread ran it.
