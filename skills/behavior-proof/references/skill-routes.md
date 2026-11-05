# Companion skills

These routes extend this procedure within the current task. Required steps apply
only under the stated condition; optional helpers do not widen authorization.
Prefer available client-native owners and read invocation limits before use.

| Skill | Relationship | When to load it |
|---|---|---|
| `temporal-py-tests` | optional | When verifying Python Temporal replay, timers or determinism. |
| `playwright-cli-driver` | optional | When the client permits terminal browser QA and no more specific browser contract takes precedence. |

Use the default `skill-stack-router` to resolve these names from the managed
source library without switching Subsets. Open the selected `SKILL.md` and its
needed references, resolving resources from that directory. If the router is
unavailable, use the current skill catalog or inspected managed source paths;
do not guess a tool, run a profile switch, or load the whole group. Reuse already
loaded skills to avoid cycles. Report unavailable required checks explicitly.
