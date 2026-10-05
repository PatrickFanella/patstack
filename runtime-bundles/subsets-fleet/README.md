# Subsets fleet profiles

This adapter exposes the canonical Kvant categories through Subsets' existing
backend. Its generated deployment contains committed profiles, shared sources,
the optional library, ownership catalogs and the original selection filter.

The adapter installs missing shared skills and qualified Claude links individually.
Existing directories and links keep their owners, including edited core skills.
Only paths recorded by this adapter can be removed when switching categories.
Local changes to those paths stop a switch. Unqualified Claude entries remain
available through the shared Codex selection and appear in `claudeExcluded`.

Preview with `subsets apply --mobile --dry-run`, then select with
`subsets apply --mobile`. Return to core with `subsets apply --group core`.
Start a fresh client session after switching. Existing unrelated skills remain
active; a category selection does not disable installations owned by other tools.

Transactions and verified backups live in
`~/.local/state/subsets-fleet/profiles/run-*`. To roll back, use
`~/.agents/bin/skill-profile rollback --run PATH`, newest transaction first.
Rollback refuses subsequent edits. Preserve this state while recovery is needed.

The installed app is pinned separately from the category source. A source manifest
records the canonical revision and tree hashes. Device rollout receipts record
the previous launchers, hashes, source location and observed verification.
Source parity and CLI checks do not prove discovery in an already-running client.
