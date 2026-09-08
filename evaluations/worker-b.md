# Worker B paired workflow evaluation

All source was read-only. Evaluation-only artifacts are under `.runtime/eval-b`; baseline and candidate arms each received separate copies of the synthetic fixture. No network mutation, remote GitHub command, production action, push, publishing action, or image generation was performed. Token accounting was unavailable.

The candidate has clear gains in three trials: raw Kubernetes manifests route through `kubernetes-development` instead of a Helm-only procedure; Blacktower lifecycle work has a repository-only `blacktower-development → session-warden` entrypoint; and `hatch-pet` distinguishes repair, validation, and creation without starting generation. Its frontend palette lookup is the strongest concrete result: the bundled helper exited 0 with three results. The backup helper failed because its packaged `scripts/data/colors.csv` is missing.

The most consequential functional failure is shared by the paired `repository-delivery-review` trial. Although both invocations passed an arm fixture, both reported `/home/onnwee/Work/tools/codex-skills`, 1,285 visible files, and an unborn catalog branch. The collector therefore ignored its passed repository argument and is unsuitable as beta-readiness evidence until repaired.

The captured CI payload was safely inspected locally in both arms:

```
test / unit: failure — unit test failed | AssertionError: expected status 200, received 500\n  at tests/api.test.ts:18:5
```

Candidate `ci-maintenance` correctly distinguishes local from hosted check state in its entrypoint, but its selected loop guide immediately instructs `gh pr view`, `gh pr checks`, and `gh run view`. It needs a local-captured-payload mode for this request. Candidate `dependency-upgrade` is better organized but still lacks a uv-specific path; an offline lock correctly failed because `httpx==0.27.0` was absent from cache. The requested target version was also unspecified.

For the Blacktower toy lifecycle fixture, both relevant lifecycle procedures led to the right condition: `running` with a missing worker must transition to `cancelled`, and stale later events must not overwrite a terminal state. TypeScript compilation could not be verified because the local `tsc` shim said no Node version is set. No Blacktower code was changed.

The existing-pet artifact contains only metadata. Candidate repair/validation routing correctly did not generate anything and correctly requires the actual v2 atlas, run manifest, chroma key, and QA artifacts before deterministic validation. The candidate-only new-pet routing test likewise stopped before any generation; `creation.md` explicitly says planning or inspection does not authorize image generation.

Exact command evidence and per-trial selected entrypoints, files read, actions, constraints, questions, unnecessary loads, and observed outputs are in `evaluations/worker-b.json`.

## Repair-and-retest round 1

The original observations remain recorded above and in the JSON. This retest used seven local tool calls; token usage remains unavailable. It made no candidate-source edit. Small reusable fixture inputs and checks were copied for commit under `evaluations/fixtures/worker-b`; caches and other transient files were excluded.

The repository-evidence collector repair passes both sides of its boundary. After initializing `.runtime/eval-b/candidate` as a separate Git repository, the collector exited 0 and named that exact repository, with `Branch: main`, `HEAD: 1717c2088216`, and 11 visible files. A nested `deploy` path exited 1 with the explicit resolved-parent/root diagnostic. This fixes the original silent ancestor-repository result.

The dependency path now correctly routes routine uv work through `python-development → uv-package-manager`. Its package-management procedure supplies `uv add --upgrade <package>`. With the evaluation’s network restriction, `uv lock --offline` still exited 1 because `httpx==0.27.0` was not cached; no update was claimed and the actual target version remains a required user choice.

The CI guide now has a captured-payload inspection mode with an explicit inspect-only stopping point. The same captured failure was parsed locally, with no `gh`, push, rerun, or monitoring command.

Using supplied fixture values, I added and checked deployment resource settings: requests are CPU `100m` and memory `128Mi`; limits are CPU `250m` and memory `256Mi`. The local fixture check printed `resource limits fixture check passed: requests 100m/128Mi, limits 250m/256Mi`. `kubectl` is still absent, so no dry-run result is claimed.

For the lifecycle fixture, Node 26 directly executed the TypeScript test through its type-stripping path and printed `lifecycle ok: running -> cancelled -> cancelled`. This demonstrates both the missing-worker cancellation and terminal-state preservation; it is not presented as a TypeScript compiler check. Node emitted only a non-blocking missing-`type: module` package warning.

Finally, Pillow created a deliberately invalid 1×1 RGBA atlas and the real pet validator rejected it with exit 1 and `expected 1536x2288 for a v2 pet, got 1x1`. No artwork generation occurred.
