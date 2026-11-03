---
name: thermo-twin-audit
description: "Thermos: run both thermo-nuclear reviews (bugs/security and code quality) in parallel on one branch, then merge their findings. Use for thermos or a double thermo review."
disable-model-invocation: true
---

# Thermos

Run the two thermo review passes as async background subagents in parallel, then synthesize their results.

## Workflow

1. Determine the review scope from the user request, PR, current branch, or relevant changed files.
2. Gather the diff and any file/context excerpts needed for reviewers to evaluate the change without guessing.
3. Launch two background subagents in the same message with the client's subagent tool (Agent in Claude Code, `spawn_agent` in Codex, task in OpenCode). Tell each to read and follow its review prompt; no dedicated subagent types are installed:
   - The `thermo-nuclear-review` prompt (now `diff-inspector` mode `thermo-nuclear-review`) for bugs, breakages, security, devex regressions, feature-flag leaks, and other branch-audit risks.
   - The `thermo-nuclear-code-quality-review` prompt (now `diff-inspector` mode `thermo-nuclear-code-quality-review`) for maintainability, structure, file-size growth, spaghetti, abstractions, and codebase-health risks.
   If the client has no subagent tool, run the two passes one after the other yourself.
4. Pass each subagent the same scoped diff/file context and ask it to return prioritized findings with file references and evidence.
5. After both finish, synthesize the results with findings first, deduplicated across reviewers. Weight overlapping findings more heavily, resolve disagreements with your own judgment, and keep summaries brief.

If individual background summaries are already visible to the user, do not restate them wholesale. Surface the unified verdict, the highest-signal findings, and any remaining uncertainty.
