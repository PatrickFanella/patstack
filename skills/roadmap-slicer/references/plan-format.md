# Plan file format

`scripts/roadmap.py` reads one JSON file. [The example](../assets/plan.example.json) is a complete plan with a spike, two epics and seven work issues; copy it and replace the content.

## Top level

| Field | Required | Meaning |
|---|---|---|
| `slug` | yes | Stable identifier for this roadmap: lowercase letters, digits and hyphens. It goes into a hidden marker in every issue, which is how reruns find issues that already exist. Never change it after publishing. |
| `codes` | no | `true` by default: titles get codes such as `[Epic A]` and `[A3]`. Set `false` for plain titles. |
| `roadmap` | yes | See below. |
| `epics` | no | List of epics. Leave it out for small plans. |
| `issues` | yes | List of work issues, in any order. The script orders them. |

## `roadmap`

| Field | Required | Meaning |
|---|---|---|
| `title` | yes | Becomes `[Roadmap] <title>`. |
| `goal` | yes | One paragraph: the outcome and why it matters. |
| `plan` | no | Where the full plan lives: a path at a commit, a URL or a wiki page. |
| `decisions` | no | Settled product and technical decisions that every issue relies on. |
| `rules` | no | Delivery rules shared by every PR, such as flags, migrations or required checks. |
| `out_of_scope` | no | Work deliberately left out of this roadmap. |
| `milestone` | no | Milestone title for the roadmap issue. It is created if missing. |
| `labels` | no | Extra existing label names. |

## `epics[]`

| Field | Required | Meaning |
|---|---|---|
| `key` | yes | Identifier used by issues' `epic` field. |
| `title` | yes | Outcome-phrased name. |
| `summary` | no | One or two sentences, shown in the roadmap and the epic. |
| `exit` | no | Criteria beyond "all children merged", such as a qualification run or a flag state. |
| `out_of_scope` | no | Exclusions specific to this epic. |
| `milestone`, `labels`, `code` | no | `code` overrides the automatic letter. |

Epics have no `blocked_by`. Put dependencies on their work issues.

## `issues[]`

| Field | Required | Meaning |
|---|---|---|
| `key` | yes | Identifier for `blocked_by` references. |
| `title` | yes | Imperative outcome. |
| `summary` | yes | What changes and why. |
| `kind` | no | `task` (default) or `spike`. |
| `epic` | no | Epic key. Without it, the issue hangs off the roadmap directly. |
| `blocked_by` | no | Keys of issues that must close first. Only hard edges. |
| `size` | no | `S`, `M` (default) or `L`. Anything larger must be split. |
| `risk` | no | `high` moves the issue ahead of routine work at the same depth. |
| `mode` | no | `afk` (default) or `hitl`. |
| `hitl_reason` | with `hitl` | Why a human is needed. |
| `acceptance` | tasks | Testable outcomes; rendered as a checklist. |
| `verify` | tasks | Commands or checks that prove the criteria. A warning if missing. |
| `question` | spikes | The question the spike answers. |
| `timebox` | no | Spike time limit. Defaults to "one working session". |
| `paths` | no | Code boundaries where the work starts. |
| `out_of_scope` | no | Neighbouring work this PR must not absorb. |
| `notes` | no | Free text for the implementer. |
| `milestone`, `labels`, `code` | no | `labels` must already exist in the repository or organization. |

## What the checker enforces

The following are errors and block publishing:

- missing required fields;
- an unknown or duplicate key;
- an unknown epic or blocker;
- a self-dependency or a cycle, which the checker prints;
- a size outside S, M and L;
- a task without acceptance criteria, or a spike without a question;
- an epic with no issues;
- `blocked_by` on an epic.

The following are warnings, to consider and then either fix or accept:

- an L issue;
- a task without verification;
- an epic with fewer than three issues;
- an issue outside every epic when epics exist;
- more than five blockers on one issue;
- more than 60 issues in total.
