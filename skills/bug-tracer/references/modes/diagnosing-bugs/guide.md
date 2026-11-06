# Diagnosing bugs

A discipline for hard bugs. Skip phases only when explicitly justified.

When exploring the codebase, read `CONTEXT.md` (if it exists) to get a clear mental model of the relevant modules, and check ADRs in the area you're touching.

Paths here are relative to this mode directory; pass the target repository explicitly.

## Redact

This skill has you show commands, outputs and captured artifacts. **Redact every secret first**: write `<REDACTED>` in its place. Build loops against env vars, so the credential stays in the environment rather than in what you show. Captured artifacts carry auth headers: quote only the lines that carry the signal.

If the redacted output is not enough to diagnose the bug, say so and ask the user.

## Phases

Take the phases in order. Read each phase's procedure when you reach it, and move on only when its gate holds.

1. [Build a feedback loop](part-03.md): read first. Gate: one tight, red-capable command that you have already run. If you cannot build one, stop and ask as that phase describes; never hypothesise without a loop.
2. [Reproduce + minimise](part-04.md): read once the loop exists. Gate: the user's exact symptom reproduces, and every remaining element of the repro is load-bearing.
3. [Hypothesise](part-05.md): read once the repro is minimal. Gate: 3–5 ranked, falsifiable hypotheses, shown to the user.
4. [Instrument](part-06.md): read when testing those hypotheses. One variable at a time; tag every debug log.
5. [Fix + regression test](part-07.md): read once a hypothesis is confirmed.
6. [Cleanup](part-08.md): read before declaring done.
