---
name: git-advanced-workflows
description: Git conflicts, worktrees, history repair, and PR preparation; hosted operations follow the configured remote.
---

# git-advanced-workflows

Resolve the repository, requested comparison, and configured remote first. Preserve unrelated work. Read-only Git inspection, requested history edits, PR preparation, and publishing have separate authorization boundaries.

## Select a mode

- Automate changelog generation from commits, PRs, and releases following Keep a Changelog format. Read [the procedure](references/modes/changelog-automation/guide.md).
- Resolve merge conflicts non-interactively, validate build and tests, and finalize conflict resolution. Read [the procedure](references/modes/fix-merge-conflicts/guide.md).
- Master advanced Git workflows including rebasing, cherry-picking, bisect, worktrees, and reflog to maintain clean history and recover from any situation. Read [the procedure](references/modes/git-advanced-workflows/guide.md).
- GitHub workflow skill for this hub's plugin-first GitHub integration. Read [the procedure](references/modes/github-pro/guide.md).
- Prepare PRs for review by cleaning noisy history, improving PR descriptions, and adding reviewer guidance without changing code behavior. Read [the procedure](references/modes/make-pr-easy-to-review/guide.md).

Resource paths inside a mode are relative to that mode directory. Run its scripts from that directory or use absolute script paths, passing the target repository explicitly.
