# GitHub Pro

GitHub workflow procedure for repositories whose remote is `github.com`. Use the `gh` CLI with non-interactive flags. Most repositories in this setup live on Gitea at `git.subcult.tv`, where `gh` does not work: use `tea --login subcult-agent` (or `tea api` for endpoints it lacks) and treat GitHub copies as mirrors.

## Use When

- Inspecting PR context, changed files, CI status, or review comments.
- Creating/updating/commenting issues.
- Reviewing or commenting on PRs.
- Fixing GitHub Actions failures.
- Preparing commits or repo contribution workflow.
- Turning plans into GitHub issues/PRDs.

## Integration Stance

- **Primary:** `gh` CLI with non-interactive flags, after `gh auth status`.
- **Optional:** a GitHub MCP server or plugin when the active client has one connected; do not use both for the same action.
- **Gitea:** `tea`, not `gh`.

## Workflow

1. Confirm the remote is GitHub (`git remote get-url origin`) and check auth with `gh auth status`.
2. Inspect branch, diff, files, PR context, and CI before acting.
3. Stage or modify only intended files.
4. Use concise Conventional Commit messages when committing is explicitly requested.
5. For PR/issue actions, return URLs and summarize changes.
6. Never force-push, amend, or publish destructive actions unless explicitly requested.

## Resources

### Curated references

Former merged-skill dumps were distilled into these lookup files:

- `references/curated/gh-address-comments.md` — Gh Address Comments guidance.
- `references/curated/gh-cli.md` — Gh Cli guidance.
- `references/curated/gh-fix-ci.md` — Gh Fix Ci guidance.
- `references/curated/git-commit.md` — Git Commit guidance.
- `references/curated/make-repo-contribution.md` — Make Repo Contribution guidance.
- `references/curated/to-issues.md` — To Issues guidance.
- `references/curated/to-prd.md` — To Prd guidance.


### Extracted resource directories

- `references/` — curated resources extracted from prior merged skill material.
- `scripts/` — curated resources extracted from prior merged skill material.
- `assets/` — curated resources extracted from prior merged skill material.
