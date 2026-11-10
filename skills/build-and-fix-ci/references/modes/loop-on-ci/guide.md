# CI inspection scope

When given a captured check payload or logs, inspect those locally first: identify job, conclusion, failing command, and diagnostic. State that captured evidence may be stale. Do not require remote tools for this mode. A request to inspect stops after diagnosis; do not fix, commit, push, rerun, or start ongoing monitoring unless requested. Use the hosted workflow below only when current remote state is needed and available tools permit it.

# Loop on CI

## Trigger

Need to watch a branch or pull request and iterate on CI failures until all required checks are green.

Pick the host from `git remote get-url origin`. Since 2026-11-10 every `subculture-collective` organization repository uses GitHub as `origin`, and its PR checks run there; the required check is `CI gate` or `Mirror CI gate`. On GitHub, `gh pr checks` is the source of truth; it includes all PR-attached checks, while `gh run list` only covers GitHub Actions. After a merge, Kvant copies GitHub to the Gitea mirror within about five minutes, and main-branch deploy and release jobs not yet moved to GitHub Actions run on Gitea Actions there. Inspect those with the Gitea commands below, using the owner and name from the `gitea` remote. Repositories that exist only on Gitea (`origin` on `git.subcult.tv`) keep their PR checks on Gitea: use `tea` with `--login subcult-agent` and the Gitea API. `gh` does not work against Gitea.

## Workflow

1. Resolve the PR for the current branch.
2. Inspect current PR checks before waiting.
3. If checks already failed, diagnose those failures first.
4. If checks are pending, watch with `gh pr checks --watch --fail-fast` on GitHub. `tea` has no watch mode; poll the Gitea commit status every minute or two.
5. After each push, re-check the full PR check set and repeat until green.

## Commands

Gitea (`git.subcult.tv`; PR commands apply to Gitea-only repositories, run commands also to organization mirrors):

```bash
# Resolve the active PR (index, head branch, URL)
tea pulls list --login subcult-agent --state open --fields index,head,url --output simple

# Combined status of every check reported on the head commit
tea api --login subcult-agent "/repos/<owner>/<repo>/commits/$(git rev-parse HEAD)/status"

# Gitea Actions runs for the head commit, their jobs, and a failed job's log
tea api --login subcult-agent "/repos/<owner>/<repo>/actions/runs?head_sha=$(git rev-parse HEAD)"
tea api --login subcult-agent "/repos/<owner>/<repo>/actions/runs/<run-id>/jobs"
tea api --login subcult-agent "/repos/<owner>/<repo>/actions/jobs/<job-id>/logs"
```

GitHub:

```bash
# Resolve the active PR
gh pr view --json number,url,headRefName

# Inspect all attached checks
gh pr checks --json name,bucket,state,workflow,link

# Watch pending checks and fail fast
gh pr checks --watch --fail-fast

# GitHub Actions logs, when the failing check links to a GHA run
gh run view <run-id> --log-failed
```

## Guardrails

- Keep each fix scoped to a single failure cause when possible.
- Do not bypass hooks (`--no-verify`) to force progress.
- If the failure is clearly unrelated to the PR and appears fixed on main, merge latest main instead of bloating the PR with unrelated fixes.
- If failures are flaky, retry once and report flake evidence.
- Re-read the full check set after every push (the Gitea status endpoint, or `gh pr checks --json name,bucket,state,workflow,link`); it can change.

## Output

- Current CI status
- Failure summary and fixes applied
- PR URL once checks are green
