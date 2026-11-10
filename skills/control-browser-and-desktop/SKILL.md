---
name: control-browser-and-desktop
description: Operate a permitted browser or isolated desktop, or capture a requested
  host screenshot using the current client tools.
---

# control-browser-and-desktop

Prefer the current client-native browser contract. Keep authenticated sessions, isolated desktops and host capture distinct. Use a named CLI only when applicable; do not switch backends or install tools merely because a reference describes them.

Select the matching procedure below and load only that procedure and its needed resources. Each procedure retains its own client, tool and invocation limits. Internal handoffs use the matching procedure below rather than reloading this entrypoint. A reference does not authorize delegation, publication, deployment or an unrelated mutation.

- **sandbox desktop**: Use when sandbox-desktop MCP tools are available and a task needs an isolated hidden Linux desktop or workspace browser: GUI app QA, sandboxed browsing, stale workspace cleanup. Read [the procedure](references/base-workflow.md).
- **playwright cli driver**: Use when an agent must drive a real browser from the terminal with playwright-cli: open, click, fill, snapshot, screenshot, trace. Read [the procedure](references/modes/playwright-cli-driver/guide.md).
- **ref snapshot browser**: ref-snapshot-browser CLI: use only when the user names ref-snapshot-browser or its snapshot and @ref workflow. Read [the procedure](references/modes/ref-snapshot-browser/guide.md).
- **desktop capture**: Screenshot the desktop, a window, an app or a pixel region with OS tools. Use when explicitly asked or a tool's own capture is unavailable. Read [the procedure](references/modes/desktop-capture/guide.md).
