# Base procedure

Reviewed source clients: codex, claude.

Resolve command and resource paths from the owning skill root, unless a linked reference says otherwise.

# manage-git-and-prs

Resolve the repository, requested comparison, and configured remote first. Preserve unrelated work. Read-only Git inspection, requested history edits, PR preparation, and publishing have separate authorization boundaries.

## Select a mode

- Automate changelog generation from commits, PRs, and releases following Keep a Changelog format. Read [the procedure](modes/changelog-automation/guide.md).
- Resolve merge conflicts non-interactively, validate build and tests, and finalize conflict resolution. Read [the procedure](modes/fix-merge-conflicts/guide.md).
- Master advanced Git workflows including rebasing, cherry-picking, bisect, worktrees, and reflog to maintain clean history and recover from any situation. Read [the procedure](modes/git-advanced-workflows/guide.md).
- GitHub-hosted repositories, including every `subculture-collective` organization repository: PR context, issues, review comments, and Actions failures through `gh`. For repositories that exist only on Gitea use `tea --login subcult-agent`. Read [the procedure](modes/github-pro/guide.md).
- Prepare PRs for review by cleaning noisy history, improving PR descriptions, and adding reviewer guidance without changing code behavior. Read [the procedure](modes/make-pr-easy-to-review/guide.md).

Resource paths inside a mode are relative to that mode directory. Run its scripts from that directory or use absolute script paths, passing the target repository explicitly.
