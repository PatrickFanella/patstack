---
name: loop-on-ci
description: "PR CI loop: read checks on GitHub (gh pr checks) or Gitea (tea and the commit-status API), fix failures, push, and repeat until required checks are green."
---

# Loop on CI

## Trigger

Need to watch a branch or pull request and iterate on CI failures until all required checks are green.

Identify the forge from `git remote get-url origin` first. On GitHub, use `gh pr checks` as the source of truth; it includes all PR-attached checks, while `gh run list` only covers GitHub Actions. On Gitea (`git.subcult.tv`), `gh` does not work: use `tea --login subcult-agent` and the combined commit status of the PR head, as shown below.

## Workflow

1. Resolve the PR for the current branch.
2. Inspect current PR checks before waiting.
3. If checks already failed, diagnose those failures first.
4. If checks are pending, watch with `gh pr checks --watch --fail-fast`.
5. After each push, re-check the full PR check set and repeat until green.

## Commands

```bash
# Resolve the active PR
gh pr view --json number,url,headRefName

# Inspect all attached checks
gh pr checks --json name,bucket,state,workflow,link

# Watch pending checks and fail fast
gh pr checks --watch --fail-fast

# GitHub Actions logs, when the failing check links to a GHA run
gh run view <run-id> --log-failed

# Gitea: resolve the PR, then read the combined status of its head commit
tea pulls list --login subcult-agent --repo <owner>/<repo> --output json
tea api --login subcult-agent /repos/<owner>/<repo>/commits/<head-sha>/status

# Gitea Actions runs; each status target_url links to its log
tea api --login subcult-agent "/repos/<owner>/<repo>/actions/tasks?limit=20"
```

## Guardrails

- Keep each fix scoped to a single failure cause when possible.
- Do not bypass hooks (`--no-verify`) to force progress.
- If the failure is clearly unrelated to the PR and appears fixed on main, merge latest main instead of bloating the PR with unrelated fixes.
- If failures are flaky, retry once and report flake evidence.
- Re-run `gh pr checks --json name,bucket,state,workflow,link` (or the Gitea status call) after every push; the check set can change.

## Output

- Current CI status
- Failure summary and fixes applied
- PR URL once checks are green
