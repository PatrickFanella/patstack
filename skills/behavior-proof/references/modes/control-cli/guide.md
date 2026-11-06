# Control CLI

Use a repeatable local harness to exercise an interactive CLI instead of poking at it manually. First reuse the repo's own test/demo harness if it exists; otherwise assemble a temporary harness from standard local tools.

Paths here are relative to this mode directory; pass the target repository explicitly.

## Harness Loop

1. Identify the command under test and the smallest reproducible workspace.
2. Discover existing local harnesses: package scripts, e2e tests, demo recorders, expect scripts, or PTY helpers.
3. If no harness exists, launch the CLI in an isolated terminal session with deterministic env vars.
4. Capture the current screen before interacting.
5. Send one action at a time: text, Enter, arrows, Escape, Ctrl-C, resize.
6. Wait for a concrete screen pattern or prompt before the next action.
7. Save the transcript and any profile artifacts.
8. Kill the session cleanly.

## Guardrails

- Prefer deterministic waits over sleeps. If you must sleep, explain why.
- Do not send credentials or destructive commands into a controlled session.
- Keep the harness in `/tmp` unless the repo already has a testing/demo harness.
- Do not hard-code paths from another repository. Adapt commands to the current repo's scripts and runtime.
- Clean up tmux sessions, temp dirs, inspector processes, and demo artifacts unless the user asks to keep them.

## Read when needed

- [Harness options](part-04.md): read when no repo-native harness exists and you must choose between tmux, a PTY probe, an inspector or a recorder.
- [Minimal tmux harness](part-05.md): read when driving the CLI through tmux, or attaching a Node inspector.
- [Minimal PTY harness](part-06.md): read when tmux is unavailable and you need deterministic waits.
- [Profiling recipes](part-07.md): read when the task is startup time, a slow operation, a memory leak or a hang.
