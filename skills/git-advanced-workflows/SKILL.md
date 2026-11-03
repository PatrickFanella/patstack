---
name: git-advanced-workflows
description: Use when resolving merge conflicts, rebasing, bisecting, using worktrees or reflog recovery, automating changelogs, or preparing a PR on Gitea or GitHub. Not for reviewing code changes.
---

# git-advanced-workflows

Resolve the repository, requested comparison, and configured remote first. Preserve unrelated work. Read-only Git inspection, requested history edits, PR preparation, and publishing have separate authorization boundaries.

## Select a mode

- Automate changelog generation from commits, PRs, and releases following Keep a Changelog format. Read [the procedure](references/modes/changelog-automation/guide.md).
- Resolve merge conflicts non-interactively, validate build and tests, and finalize conflict resolution. Read [the procedure](references/modes/fix-merge-conflicts/guide.md).
- Master advanced Git workflows including rebasing, cherry-picking, bisect, worktrees, and reflog to maintain clean history and recover from any situation. Read [the procedure](references/modes/git-advanced-workflows/guide.md).
- GitHub-hosted repositories only: PR context, issues, review comments, and Actions failures through `gh`. For Gitea repositories use `tea --login subcult-agent`. Read [the procedure](references/modes/github-pro/guide.md).
- Prepare PRs for review by cleaning noisy history, improving PR descriptions, and adding reviewer guidance without changing code behavior. Read [the procedure](references/modes/make-pr-easy-to-review/guide.md).

Resource paths inside a mode are relative to that mode directory. Run its scripts from that directory or use absolute script paths, passing the target repository explicitly.
