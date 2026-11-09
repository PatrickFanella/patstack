# claude-bg-handoff procedure

Invoke this mode only on an explicit request for this procedure.

Reviewed source clients: claude. Check the actual client tools before following this procedure. Resolve its scripts, references and assets from this directory, not from the outer skill root.

Write a handoff summary of the current conversation so a fresh agent can continue the work. Instead of saving it, launch a background agent seeded with the summary as its prompt: `claude --bg --name "<descriptive name>" "<handoff summary>"`. It starts in the current working directory and returns immediately; the user manages it with `claude agents`.

Always pass `-n`/`--name` with a descriptive name (e.g. `--name "Fix login bug"`); it sets the display name shown in the job list, session picker, and terminal title.

Include a "suggested skills" section in the summary, naming which skills the next agent should call the Skill tool for.

Do not duplicate content already captured in other artifacts (specs, plans, ADRs, issues, commits, diffs). Reference them by path or URL instead.

Redact any sensitive information, such as API keys, passwords, or personally identifiable information, since the summary becomes the agent's prompt.

If the user passed arguments, treat them as a description of what the next session will focus on and tailor the summary accordingly.

This needs the Claude Code CLI (`claude --bg`). In Codex or OpenCode, or when `claude` is not on PATH, use the `relay-baton` skill instead and tell the user.
