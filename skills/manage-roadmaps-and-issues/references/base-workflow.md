# Base procedure

Reviewed source clients: codex, claude.

Resolve command and resource paths from the owning skill root, unless a linked reference says otherwise.

# manage-roadmaps-and-issues

Turn a finished plan into issues that a person or an agent can work from top to bottom. Gitea has no sub-issues, so the hierarchy is built from tracking issues, checklists and native dependencies:

- **Roadmap**: one tracking issue per plan. Goal, decisions, epics, the full execution order in waves, critical path and graph. Pinned.
- **Epic** (optional): a tracking issue for one feature that needs three or more PRs.
- **Work issue**: exactly one reviewable PR. A **spike** is a work issue whose output is a recorded decision.

A PR is not an issue: it closes its work issue with `Closes #n`. Epics depend on their children and the roadmap depends on its epics, so tracking issues close last.

## Where issues live

Since 2026-11-10 every `subculture-collective` organization repository takes branches and PRs on GitHub, and Gitea holds a fast-forward mirror. Issues depend on visibility:

- **Public organization repositories**: new issues go on GitHub, where Issues, Projects and (on products) Discussions are on. Older issues may still be on Gitea until they are moved.
- **Private organization repositories and repositories that exist only on Gitea**: issues stay on Gitea.

`scripts/roadmap.py` publishes to Gitea only. Use it where issues live on Gitea. For a public organization repository, do not publish to the Gitea copy: check the plan with the script as usual, then create the issues on GitHub with `gh issue create` in the printed order, using the `--preview` bodies, and record order with `Blocked by #n` lines. In a GitHub PR, `Closes #n` refers to GitHub's own issue numbers; link a work issue still on Gitea by its full URL.

## Workflow

1. **Read the whole plan.** Finished means the goal, scope and product decisions are settled. If an open question can be answered by investigation, make it a spike. If it needs the user's judgement and changes the breakdown, ask or route to `define-requirements`. Never invent the decision.
2. **Inspect the target repository.** Confirm the Gitea login your environment designates (`tea api /user`), that issue dependencies are enabled (`internal_tracker.enable_issue_dependencies`), and the existing labels, milestones and open roadmaps. Read enough code to name boundaries and verification commands.
3. **Slice and order.** Read [the breakdown method](breakdown-method.md). Write the plan file described in [the plan format](plan-format.md), starting from [the example](../assets/plan.example.json). Keep it outside the repository unless the user wants it committed.
4. **Check.** Run `python3 scripts/roadmap.py check PLAN`. Fix every error. Weigh each warning, then read `--preview` as the implementer of each issue would. Every issue should merge on its own and every edge should be a hard prerequisite.
5. **Publish.** Run `python3 scripts/roadmap.py publish PLAN --repo OWNER/NAME [--login LOGIN]` as a dry run, review the actions, then add `--apply`. A request to create the issues authorizes this step. If the user asked only for a proposed breakdown, stop after step 4 and show the summary.
6. **Report.** `--apply` reads everything back and exits non-zero on a mismatch. Open the roadmap once to confirm it renders. Report the roadmap link, the issue count, the frontier, the critical path, and any assumptions or warnings you accepted.

Labels: the script creates only the exclusive `Planning/*` role labels it needs. Take other labels from the repository's existing taxonomy. Do not apply `ready-for-agent`, `agent:*` or other queue labels unless asked, because they can start automation.

## After publishing

- **The plan changed**: edit the plan file and publish again. Existing issues are matched by a hidden marker and skipped, new issues are created and wired, and the roadmap and epic bodies are regenerated. `--update` also rewrites existing titles, bodies and labels. Check for manual edits before using it.
- **Progress**: `python3 scripts/roadmap.py refresh --repo OWNER/NAME --roadmap N --apply` ticks closed issues in the roadmap and epics and lists the frontier. Gitea will not close an issue while it has open blockers, even from a merged PR's `Closes #n`, and gives no warning. Refresh finds those issues and closes them once their blockers are closed.
- **No Python or tea**: follow the manual path in [Gitea notes](gitea.md), which also covers the API calls, permissions and failure handling.

The script needs Python 3 and `tea` with a login that can write issues. It changes only issues, labels, milestones, dependencies and the pin. If it stops partway, fix the cause and run it again; the markers make a rerun safe.

For companion skills, read [the routes](skill-routes.md) only when their condition applies.
