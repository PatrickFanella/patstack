---
name: verify-behavior
description: Verify UI, CLI, API, build, or performance claims using runnable evidence; distinguish smoke checks from regressions.
---

# Verify Behavior

Translate the requested claim into observable behavior and choose a verification mode:

- **Conformance:** Check a current property against explicit expectations. A new endpoint returning the required schema can pass without an older implementation.
- **Regression:** Reproduce the defect in the relevant baseline and show the same check passing after the fix. Without a valid baseline, report the current result and the limit on the regression claim.
- **Performance:** Compare baseline and treatment using the same workload, environment, and measurement method. Report noise or confounds instead of attributing every difference to the change.

Identify the surface the claim actually concerns. Build success verifies a build; it does not establish browser usability, deployed behavior, or data correctness.

Reuse the repository's existing harness. For a missing harness, create the smallest isolated, deterministic probe needed for this claim. A user request for a reusable verification harness may produce a project-local skill under `.agents/skills`; keep its instructions specific to that application's launch command, test data, and expected behavior.

Use a terminal/PTY harness for interactive CLI behavior, browser automation for UI behavior, and direct client requests for API behavior. Discover available tooling rather than assuming a named agent, MCP server, or another host's configuration path. Respect any more specific browser or runtime instructions.

Inspect the result payload as well as process exit status. A command that exits zero with an error object has not satisfied the claim. Capture enough evidence to reproduce the conclusion, avoiding credentials and unnecessary user data.

Conclude with PASS, FAIL, or INCONCLUSIVE for the named mode and claim. Include the command or interaction, artifact location, expected result, observed result, and material limitations. Keep local, staging, and production evidence distinct.

## Surface procedures

- Run compile and type-check commands and report failures. Read [the procedure](references/modes/check-compiler-errors/guide.md).
- Build or adapt a local harness to drive, inspect, and profile an interactive CLI or TUI without external services. Read [the procedure](references/modes/control-cli/guide.md).
- Build or adapt a local browser/CDP harness to drive and inspect a web, IDE, or Electron UI. Read [the procedure](references/modes/control-ui/guide.md).
- For regression or performance comparisons only, capture a valid baseline and treatment and compare artifacts. Read [the procedure](references/modes/verify-this/guide.md).
- Test local or remote web applications with browser automation and QA workflows. Read [the procedure](references/modes/webapp-testing/guide.md).
- For live-session debugging, misleading fetch results, hidden DOM state, or save/publish evidence, read [browser diagnosis](references/browser-diagnosis.md). Keep the current client's browser/tool routing in force.

Resource paths inside a mode are relative to that mode directory. Run its scripts from that directory or use absolute script paths, passing the target repository explicitly.

## Conditional design notes

- [prove it works](references/principles/prove-it-works.md) — consult only for this specific design or execution concern.
- [make operations idempotent](references/principles/make-operations-idempotent.md) — consult only for this specific design or execution concern.
