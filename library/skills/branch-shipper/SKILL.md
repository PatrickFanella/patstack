---
name: branch-shipper
description: "Ship the current branch: review for bugs and intent fit, run or add tests, commit focused work, open or update the PR (Gitea via tea, GitHub via gh). Use before handing off a branch. Not for read-only review."
---

# Review and ship

## Trigger

Reviewing changes before shipping. Close key issues, verify behavior, and open or update a PR.

## Workflow

1. Gather context: diff against base branch, uncommitted changes, recent commits, changed files, and user intent from recent relevant chats if useful.
2. Run targeted tests for changed behavior. If no focused tests exist, decide whether to add them or document the gap.
3. Review for correctness, regressions, security, and intent fit. Use parallel subagents for larger diffs.
4. Fix critical issues before finalizing and re-run affected tests.
5. Commit selective files with a concise message.
6. Push branch and open or update a PR.

## Suggested Checks

```bash
git fetch origin main
git diff origin/main...HEAD
git status
gh pr checks --json name,bucket,state,workflow,link   # GitHub remotes
tea pulls list --login subcult-agent                   # Gitea remotes (git.subcult.tv)
tea actions runs list --login subcult-agent
```

Check `git remote -v` first. Gitea repositories on `git.subcult.tv` use `tea` with the `subcult-agent` login (`tea pulls create`, `tea actions runs list`); `gh` does not work for them.

## Guardrails

- Prioritize correctness, security, and regressions over style-only comments.
- Keep commits focused and avoid unrelated file changes.
- If pre-commit checks fail, fix the issues rather than bypassing hooks.
- Judge PR readiness from the hosted check results on the head commit: `gh pr checks` on GitHub, `tea actions runs list` or the commit status API on Gitea.

## Output

- Findings summary (critical, warning, note)
- Tests run and outcomes
- PR URL
