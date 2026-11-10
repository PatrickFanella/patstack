# branch-shipper procedure

Reviewed source clients: claude, codex, opencode. Check the actual client tools before following this procedure. Resolve its scripts, references and assets from this directory, not from the outer skill root.

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
gh pr checks --json name,bucket,state,workflow,link   # GitHub remotes, including organization repositories
tea pulls list --login subcult-agent                   # Gitea-only repositories (git.subcult.tv)
tea actions runs list --login subcult-agent
```

Check `git remote -v` first. Organization repositories (`subculture-collective`) use GitHub as `origin`: push the branch there and open the PR with `gh pr create`. A ready PR merges itself once its required check (`CI gate` or `Mirror CI gate`) passes and it has no conflicts; to hold it, open it as a draft or add the label `hold`. Never push an organization repository to its Gitea copy: Gitea is a fast-forward mirror, and the `gitea` remote is fetch-only. A fresh GitHub clone has no `gitea` remote, so commit with command-local `-c user.name='SUBCULT Agent' -c user.email='info@subcult.tv'`. Repositories that exist only on Gitea (`git.subcult.tv`) use `tea` with the `subcult-agent` login (`tea pulls create`, `tea actions runs list`); `gh` does not work for them.

## Guardrails

- Prioritize correctness, security, and regressions over style-only comments.
- Keep commits focused and avoid unrelated file changes.
- If pre-commit checks fail, fix the issues rather than bypassing hooks.
- Judge PR readiness from the hosted check results on the head commit: `gh pr checks` on GitHub, `tea actions runs list` or the commit status API on Gitea-only repositories.

## Output

- Findings summary (critical, warning, note)
- Tests run and outcomes
- PR URL

## Companion skills

Load [required steps and optional helpers](references/skill-routes.md) only when their stated condition applies.
