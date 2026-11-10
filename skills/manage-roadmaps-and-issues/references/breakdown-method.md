# Breakdown method

How to cut a finished plan into a roadmap whose issues each become one PR. The rules come from established practice, summarized in [Sources](#sources), and are adjusted for a small team that hands issues to coding agents.

## Contents

- [Choosing the levels](#choosing-the-levels)
- [Slicing work issues](#slicing-work-issues)
- [Sizing](#sizing)
- [Dependencies and order](#dependencies-and-order)
- [Writing each issue](#writing-each-issue)
- [Agent or human](#agent-or-human)
- [Anti-patterns](#anti-patterns)
- [Sources](#sources)

## Choosing the levels

Most schemes have one more level than a solo developer needs. Jira uses Initiative, Epic, Story and Sub-task. Linear uses Initiative, Project, Milestone, Issue and Sub-issue. Rust and Kubernetes keep design in a document and a thin tracking issue beside it. Without cross-team coordination, Epic and Story both mean "a group of PRs". Use three levels:

| Level | Use it when | Content |
|---|---|---|
| Roadmap | Always, one per plan or release | Goal, decisions, links and the execution order. It holds no design detail; that stays in the plan. |
| Epic | A feature needs three or more PRs, or ships on its own schedule | Its children in execution order and its exit criteria. |
| Work issue | Always | One PR: outcome, acceptance criteria, verification, blockers and exclusions. |

With fewer than about eight work issues, or no natural feature grouping, leave out epics; the roadmap is enough. An epic with one or two children is bookkeeping, so fold it into the roadmap.

Milestones are optional. Use one when the plan has a release date or several releases. Name it after the release, not the epic, so one milestone can span epics. Labels classify issues; milestones schedule them; dependencies order them.

## Slicing work issues

Start with a **walking skeleton**: the thinnest end-to-end path through every layer that proves the architecture works, such as a schema, an endpoint, a minimal UI and a test. Thicken it slice by slice. Each work issue should be a **vertical slice**: a narrow but complete path through the layers it touches, demonstrable or verifiable on its own. Horizontal splits like "all the models" or "all the endpoints" hide integration risk until the end.

When a slice is too large, split it with the first of these patterns that applies (Lawrence's order):

1. **Workflow steps**: do the first and last steps, then add the middle ones.
2. **Operations**: separate create, read, update and delete.
3. **Business rule variations**: handle the common rule first and add each variation as its own slice.
4. **Data variations**: support one data shape, format or locale, then the others.
5. **Entry methods**: start with the simplest input, such as an API or form, and add richer ones later.
6. **Major effort**: the first variant carries the infrastructure, and later variants are cheap.
7. **Simple/complex**: ship the simple core and defer the edge cases.
8. **Defer performance**: make it work, then make it fast, as separate slices.
9. **Spike**: when you cannot tell how to split, investigate first.

Prefer splits that reveal low-value work you can drop, and splits that yield roughly equal pieces.

Some changes cannot be sliced vertically:

- **Wide refactors and schema changes**: use expand, migrate, contract. Add the new form beside the old, move callers in batches sized by blast radius, then remove the old form. Each step is its own issue, and the chain gets hard edges.
- **Refactoring that enables a feature**: give it its own issue, ahead of the feature. Do not hide it inside a feature PR. "Make the change easy, then make the easy change."
- **Incomplete user-facing features**: merge behind a flag so the slices stay small, and make removing the flag the final rollout issue.

## Sizing

- **S** (1 point): under about 100 changed lines, one area.
- **M** (2 points): roughly 100 to 400 lines with its tests.
- **L** (3 points): near the limit of one review or one agent session. Treat it as a prompt to split, and keep it only when splitting would produce PRs that cannot merge on their own.

Anything larger is not a work issue. Count tests in the size. A new API ships with a caller in the same PR, because an endpoint nobody uses cannot be verified. The script uses these points for the critical path.

## Dependencies and order

Add an edge "B is blocked by A" only when B cannot merge, or cannot be verified, without A: a shared schema, contract, migration or decision. "It would be nicer to do A first" is not an edge. Extra edges hide parallel work, and a missing hard edge produces a PR that cannot merge. Ask of each edge: if A were dropped, would B have to change?

The script orders the work this way:

1. Topological sort, so blockers always come first.
2. Risk first: a spike or a `risk: high` issue goes ahead of routine work. Uncertain work belongs at the start, while there is still time to change the plan. Shape Up calls this pushing scopes uphill early.
3. Critical path next: among ready issues, the one heading the longest weighted chain goes first. Splitting work on the critical path shortens the roadmap; splitting work off it does not.
4. The plan's own order breaks the remaining ties.

**Waves** group issues by dependency depth. Issues in one wave never depend on each other, so the wave shows what can run in parallel. The **frontier** is the set of open issues with no open blockers. Issues are created in execution order, so issue numbers roughly follow the order of work.

Put a spike before any issue that depends on an unresolved assumption. A spike is time-boxed, its deliverable is a decision recorded on the issue, and it blocks the work that depends on the answer.

## Writing each issue

Treat each issue as the full prompt for whoever implements it, possibly an agent with no access to the plan. Repeat the context it needs; do not rely on the plan file.

- **Title**: an imperative outcome, such as "Email a sign-in link on request", not "Email stuff" or "Backend for magic links".
- **Summary**: what changes for a user or caller, and why. One to three sentences.
- **Acceptance criteria**: observable, testable outcomes written as a checklist. Use Given/When/Then only for rule-heavy behaviour. Include the negative case when it matters, for example "Unknown addresses get the same response and no email."
- **Verification**: the exact command or check that proves the criteria, so an implementer cannot report done without running it.
- **Code boundaries**: the modules or directories where the work starts. Avoid line numbers and code snippets; they go stale.
- **Out of scope**: neighbouring work that belongs to another issue, named so the PR does not absorb it.
- **Notes**: anything the implementer would otherwise ask about, such as conventions, flags or a gotcha in the plan.

A work issue is ready when its blockers are listed, its criteria are testable, it has a verification command, and its exclusions are stated. It is done when its PR has merged with `Closes #n` and checks have passed on the head commit.

## Agent or human

Mark every work issue `afk` (an agent can finish it alone) or `hitl` (it needs a human checkpoint), and give the reason for `hitl`. Default to `hitl` for these:

- production changes and rollouts;
- security, authentication, payments and personal data;
- choices of taste or product judgement;
- accounts, credentials or purchases;
- device or field testing.

Prefer slicing so that most issues are `afk` and each human checkpoint is its own small issue.

## Anti-patterns

- **Layer tickets**, such as "database", "API" and "UI", that integrate only at the end.
- **Kitchen-sink PRs**: an issue whose acceptance list spans several features.
- **Hidden prerequisites**: a refactor or migration buried inside a feature issue.
- **Decision tickets with no owner**: an open question written as a task. Make it a spike or ask now.
- **Dependency spaghetti**: every issue blocked by its predecessor in a straight line. This usually means order was confused with dependency.
- **Duplicates**: search open issues and earlier roadmaps before publishing.
- **Copying the plan into every issue**: give each issue the context it needs and link the rest.

## Sources

- Google engineering practices, [Small CLs](https://google.github.io/eng-practices/review/developer/small-cls.html): self-contained changes, separate refactors, sizing.
- Humanizing Work, [Guide to splitting user stories](https://www.humanizingwork.com/the-humanizing-work-guide-to-splitting-user-stories/): Lawrence's patterns and their order.
- Basecamp, Shape Up [chapter 12](https://basecamp.com/shapeup/3.3-chapter-12) and [chapter 13](https://basecamp.com/shapeup/3.4-chapter-13): scopes, and doing the uncertain work first.
- Bill Wake, [INVEST](https://xp123.com/articles/invest-in-good-stories-and-smart-tasks/); Jeff Patton, user story mapping and the walking skeleton; Martin Fowler, [ParallelChange](https://martinfowler.com/bliki/ParallelChange.html) and [Feature Toggles](https://martinfowler.com/articles/feature-toggles.html).
- GitHub, [Copilot coding agent: best results](https://docs.github.com/en/copilot/tutorials/cloud-agent/get-the-best-results): the issue is the prompt, and some work stays with a human.
- Matt Pocock's to-issues skill ([aihero.dev](https://www.aihero.dev/skills-to-issues)): tracer-bullet issues marked AFK or HITL.
- Linear, [conceptual model](https://linear.app/docs/conceptual-model); the Rust and Cargo tracking-issue process.
