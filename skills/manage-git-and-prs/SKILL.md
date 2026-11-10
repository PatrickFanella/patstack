---
name: manage-git-and-prs
description: Manage Git history and worktrees or prepare and ship a focused branch
  through its authorized PR workflow.
---

# manage-git-and-prs

Inspect the exact checkout, common directory, remotes and dirty state first. A PR request does not authorize merging, deployment or destructive history changes.

Select the matching procedure below and load only that procedure and its needed resources. Each procedure retains its own client, tool and invocation limits. Internal handoffs use the matching procedure below rather than reloading this entrypoint. A reference does not authorize delegation, publication, deployment or an unrelated mutation.

- **repair history and prepare PRs**: Use when resolving merge conflicts, rebasing, bisecting, using worktrees or reflog recovery, automating changelogs, or preparing a PR on Gitea or GitHub. Read [the procedure](references/base-workflow.md).
- **branch shipper**: Ship the current branch: review for bugs and intent fit, run or add tests, commit focused work, open or update the PR (Gitea via tea, GitHub via gh). Use before handing off a branch. Read [the procedure](references/modes/branch-shipper/guide.md).
- **worktree lanes**: Worktree lanes: create, track, integrate and prune Git worktrees under .blacktower/worktrees for risky, parallel or multi-agent work. Read [the procedure](references/modes/worktree-lanes/guide.md).

Read [conditional companions](references/skill-routes.md) only when their stated condition applies.
