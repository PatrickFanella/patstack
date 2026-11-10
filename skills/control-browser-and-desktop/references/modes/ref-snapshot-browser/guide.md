# ref-snapshot-browser procedure

Reviewed source clients: claude, codex, opencode. Check the actual client tools before following this procedure. Resolve its scripts, references and assets from this directory, not from the outer skill root.

# ref-snapshot-browser

Fast browser automation CLI for AI agents. Chrome/Chromium via CDP with
accessibility-tree snapshots and compact `@eN` element refs.

Install: `npm i -g ref-snapshot-browser && ref-snapshot-browser install`

## Start here

This file is a discovery stub, not the usage guide. Before running any
`agent-browser` command, load the actual workflow content from the CLI:

```bash
ref-snapshot-browser skills get core             # start here — workflows, common patterns, troubleshooting
ref-snapshot-browser skills get core --full      # include full command reference and templates
```

The CLI serves skill content that always matches the installed version,
so instructions never go stale. The content in this stub cannot change
between releases, which is why it just points at `skills get core`.

## Specialized skills

Load a specialized skill when the task falls outside browser web pages:

```bash
ref-snapshot-browser skills get electron          # Electron desktop apps (VS Code, Slack, Discord, Figma, ...)
ref-snapshot-browser skills get slack             # Slack workspace automation
ref-snapshot-browser skills get dogfood           # Exploratory testing / QA / bug hunts
ref-snapshot-browser skills get vercel-sandbox    # ref-snapshot-browser inside Vercel Sandbox microVMs
ref-snapshot-browser skills get agentcore         # AWS Bedrock AgentCore cloud browsers
```

Run `ref-snapshot-browser skills list` to see everything available on the
installed version.

## Why ref-snapshot-browser

- Fast native Rust CLI, not a Node.js wrapper
- Works with any AI agent (OpenCode, Blacktower, Codex, Cursor, Continue, Windsurf, etc.)
- Chrome/Chromium via CDP with no Playwright or Puppeteer dependency
- Accessibility-tree snapshots with element refs for reliable interaction
- Sessions, authentication vault, state persistence, video recording
- Specialized skills for Electron apps, Slack, exploratory testing, cloud providers

## Observability Dashboard

The dashboard runs independently of browser sessions on port 4848 and can also be opened through a proxied or forwarded URL such as `https://dashboard.agent-browser.localhost`. Agents should stay on the dashboard origin: session tabs, status, and stream traffic are proxied internally, so session ports do not need to be exposed.
