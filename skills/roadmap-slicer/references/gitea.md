# Gitea notes

Behaviour marked *observed* was checked on Gitea 28.3.0 (API version 28.3.0, the release after 1.27) on 2026-11-07, in a throwaway repository. Check `GET /version` on older or newer instances before relying on it.

## Contents

- [How the hierarchy maps onto Gitea](#how-the-hierarchy-maps-onto-gitea)
- [Dependency behaviour](#dependency-behaviour)
- [Calls the script makes](#calls-the-script-makes)
- [Labels, milestones, pins and boards](#labels-milestones-pins-and-boards)
- [Manual path](#manual-path)
- [Failures](#failures)

## How the hierarchy maps onto Gitea

Gitea has no parent or sub-issue link. The script builds the hierarchy from parts Gitea does have:

- Each tracking issue (the roadmap and each epic) has a **checklist** of its children. The issue list shows a done/total progress bar computed from those checkboxes, and `refresh` ticks them.
- Each **dependency** points from the tracking issue to its children (epic → work issues, roadmap → epics), so a tracking issue cannot close before its children.
- Child-to-child dependencies set the work order.
- A hidden marker, `<!-- roadmap-slicer:<slug>:<id> -->`, identifies each issue, so reruns find what exists. It is invisible in the rendered issue (*observed*).
- Mermaid blocks render as diagrams, and `#n` references link and preview (*observed*).

## Dependency behaviour

- Dependencies must be enabled per repository: `internal_tracker.enable_issue_dependencies` on `GET /repos/{owner}/{repo}`. The script stops before writing if they are off. Enabling them is a repository setting; do it only with the owner's agreement, by `PATCH /repos/{owner}/{repo}` with the whole `internal_tracker` object and the flag set to true.
- Closing an issue that has an open blocker fails with **412 Precondition Failed**, for work issues and tracking issues alike (*observed*).
- **A PR that merges before its issue's blockers close does not close the issue, and nothing reports it.** The PR merges and the `Closes #n` keyword is skipped (*observed*). `refresh` finds these issues through the timeline's merged `pull_ref` events. With `--apply` it closes them once their blockers are closed, and until then it reports them.
- Closing keywords (`close`, `fix` and `resolve`, in their usual forms) act from PR descriptions and commit messages, not from comments.
- Dependencies can cross repositories: the request body carries `owner` and `repo`. The script creates only same-repository edges. To add a cross-repository blocker by hand, use the same call with the other repository's owner and name.

## Calls the script makes

All calls go through `tea api -i`, so tea's stored login authenticates them and no token reaches the command line. `tea api` exits 0 even on HTTP errors, so the script reads the status line itself.

| Purpose | Call |
|---|---|
| Repository settings | `GET /repos/{o}/{r}` |
| Find existing issues by marker | `GET /repos/{o}/{r}/issues?state=all&type=issues` (paged) |
| Labels | `GET /repos/{o}/{r}/labels`, `GET /orgs/{o}/labels`, `POST /repos/{o}/{r}/labels` with `exclusive: true` |
| Milestones | `GET`/`POST /repos/{o}/{r}/milestones` |
| Create an issue | `POST /repos/{o}/{r}/issues` with label **IDs** and a milestone ID |
| Rewrite a body | `PATCH /repos/{o}/{r}/issues/{n}` |
| Add labels (`--update`) | `POST /repos/{o}/{r}/issues/{n}/labels` |
| Dependencies | `GET`/`POST /repos/{o}/{r}/issues/{n}/dependencies`; the body `{owner, repo, index}` names the blocker |
| Pin | `GET /repos/{o}/{r}/new_pin_allowed`, then `POST /repos/{o}/{r}/issues/{n}/pin` |
| Refresh | `GET /repos/{o}/{r}/issues/{n}` and `/timeline`, then `PATCH` the state and body |

## Labels, milestones, pins and boards

- **Labels**: a `/` in a name makes a scoped label, and `exclusive` allows only one label per scope on an issue. The script creates `Planning/Roadmap`, `Planning/Epic`, `Planning/Single-PR` and `Planning/Spike` as exclusive labels when it needs them, and reuses them when they exist. Every other label must already exist. Use the repository's own type and priority taxonomy (`type:feature`, `Kind/Feature` and so on) rather than adding a parallel one. Queue labels such as `ready-for-agent` and `agent:*` can trigger automation, so apply them only when asked.
- **Milestones**: name them after a release or phase, not an epic. Missing ones are created.
- **Pins**: an instance allows few pinned issues (three by default). The script pins only when `new_pin_allowed` says there is room, and otherwise reports it.
- **Project boards**: not automated. The API supports them (`/repos/{o}/{r}/projects`, its columns, and `POST .../columns/{column_id}/issues/{issue_id}`). The `issue_id` there is the issue's global `id`, not its number. If the user wants a board, create it once and add the issues.

## Manual path

Without Python, publish in the same order the script uses:

1. Create the role labels, then any milestone.
2. Create the roadmap and each epic with a stub body that contains only the marker.
3. Create the work issues in execution order with full bodies, following the [single-PR template](../assets/single-pr.md) or the [spike template](../assets/spike.md): `tea issues create --login LOGIN --repo O/R --title ... --description-file body.md --labels Planning/Single-PR`.
4. Rewrite the roadmap and epic bodies from the [roadmap template](../assets/roadmap.md) and [epic template](../assets/epic.md), now that the numbers are known.
5. Add every dependency: `tea api --login LOGIN -X POST /repos/O/R/issues/N/dependencies -d '{"owner":"O","repo":"R","index":BLOCKER}'`.
6. Read back `GET .../issues/N/dependencies` for each issue.

## Failures

- **`labels not in the repository`**: an issue names a label that does not exist. Use an existing name, or create the label deliberately and run again.
- **`issue dependencies are disabled`**: see [Dependency behaviour](#dependency-behaviour).
- **403 or 404 on writes**: the login cannot write issues in that repository. Report the missing access; do not switch to another person's credentials.
- **Interrupted run**: run again. Existing issues are matched by marker, missing ones are created, and missing dependencies are added. Tracking bodies are rewritten whenever something new is created.
- **A wrong issue was created**: close it with a comment. Deleting issues needs administrator rights and loses history. Then fix the plan and run again. A closed issue is still matched by its marker, so remove its key from the plan or give the replacement a new key.
