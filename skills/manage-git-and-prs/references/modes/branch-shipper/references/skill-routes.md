# Companion skills

These routes extend this procedure within the current task. Required steps apply
only under the stated condition; optional helpers do not widen authorization.
Prefer available client-native owners and read invocation limits before use.

| Skill | Relationship | When to load it |
|---|---|---|
| `review-code-changes` | required | For the pre-shipping correctness review. |
| `verify-implementation` | required | For behavior checks before shipping. |
| `manage-git-and-prs` (base workflow) | required | When preparing or updating the hosted PR. |
| `build-and-fix-ci` | optional | When PR checks need diagnosis or an authorized wait for completion. |

Use the default `find-and-load-skills` to resolve these names from the managed
source library without switching Subsets. Open the selected `SKILL.md` and its
needed references, resolving resources from that directory. If the router is
unavailable, use the current skill catalog or inspected managed source paths;
do not guess a tool, run a profile switch, or load the whole group. Reuse already
loaded skills to avoid cycles. Report unavailable required checks explicitly.
