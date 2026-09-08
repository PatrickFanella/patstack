# Worker A paired trial evidence

This evaluator was independent from acceptance outcomes but not fully blind: the assignment supplied the two roots, test requests, evidence destination, and earlier frontend-probe context. I did not open `evaluations/acceptance.json`, audit conclusions, or builder scripts.

Fixtures are isolated under `.runtime/eval-a/baseline` and `.runtime/eval-a/candidate`. Neither trial used the network, altered an external system, published anything, or modified either skill root.

The shared Node fixture passed in both workspaces:

```text
{"ok":true,"cases":[1,2,4,5,6,7]}
```

It verifies the local rename, lifecycle union shape, trim/reject feature behavior, endpoint response object, retry-after-one-transient-error behavior, and failure classification for a zero-exit error envelope. The README preservation validator also passed for the relative link, inline code, fenced command, and language-selector markers. The routing validator passed for `shellcheck-configuration` and `k8s-manifest-generator`. `git diff --no-index --check` passed for both corresponding fixture pairs.

The detailed per-request entrypoint selections, resources read, actions, checks, questions, unnecessary loads, limitations, and available metric status are in [`worker-a.json`](worker-a.json). The material observations were: the baseline closest plan skill is refactor-specific and directs GitHub issue publication, so it was only a partial match for plan-only work; the candidate implementation-plan entrypoint matched that stopping point directly; and candidate README-localization preservation passed but its fixture selector did not demonstrate the mode's current-language emphasis requirement.

No reliable per-worker tool-call count or token-usage value was available for the initial trial, so neither has been invented.

## Retest: routing and README-selector repair

The initial observations remain above. This retest was added after the candidate technical-writing root explicitly required current-language selector emphasis and after the initial trial was found to have bypassed the expanded candidate routing surface.

Before selecting requests 2, 4, 5, 6, and 7, I extracted only `name` and `description` frontmatter from every candidate `skills/*/SKILL.md`. The recorded routes are in [retest-routing.json](fixtures/worker-a/retest-routing.json). This retained `architecture-patterns`, `api-development`, and `systematic-debugging` for requests 2, 5, 6, and 7, and changed request 4 from `tdd` to `implementation-plan`, whose description explicitly covers implementing a bounded feature from a specification.

The versioned reusable fixture is [retest.mjs](fixtures/worker-a/retest.mjs), with runtime mirrors retained under `.runtime/eval-a`. It passed when executed directly and through both baseline and candidate mirrors. The retry assertion now proves the required regression path: `oldRetryOnce` rejects on the transient-crash reproducer, while `newRetryOnce` succeeds on a fresh instance of that exact reproducer and reports two attempts. The same check covers the lifecycle discriminants, bounded feature behavior, endpoint JSON field types, and zero-exit error-envelope classification.

The repaired README fixtures preserve the link, inline code, fenced command, marker comments, and one selector per file. They now also emphasize the current language: `**English**` in `README.md`, and `**Español**` in `README.es.md`; each retains a link to the other variant. The README preservation/current-language-emphasis validator passed.

The retest used seven top-level tool invocations: five command-orchestration calls and two patch calls, containing nine local command invocations. That count excludes all initial-trial and frontend-probe work. Token usage remained unavailable. The shell/Kubernetes routing case still records routing only; no script or manifest was created or applied. The parent removed the earlier active frontend-design bytecode cache after its reported provenance; the retest check found no active `__pycache__` path under that skill.
