# Base procedure

Reviewed source clients: claude, codex, opencode.

Resolve command and resource paths from the owning skill root, unless a linked reference says otherwise.

Do the research inline by default. When the user asked for depth and the client supports background or delegated agents, you may hand the research to one so you keep working; give it the steps below and check its citations when it returns.

1. Investigate the question against **primary sources** (official docs, source code, specs, first-party APIs), not a secondary write-up of them. Follow every claim back to the source that owns it.
2. Report the findings with each claim's source cited, in the reply by default.
3. Write a Markdown note into the repository only when the user asks for one. Then save it where the repo already keeps such notes, match the existing convention, and say where it went; with no convention, ask or keep it outside the repository.

## Companion skills

Load [required steps and optional helpers](skill-routes.md) only when their stated condition applies.
