# Tadooer assistant installation

`integrations/tadooer/` in this repository owns the personal assistant plugin,
workflow skill, setup helper and fleet deployment policy. The Tadooer repository
owns the server, desktop applications and MCP adapter. System/plugin package
caches are installation targets and are never edited directly.

The desktop client and assistant integration use the same Tadooer instance but
different credentials. Signing into the app does not authorize an MCP client.
The fleet installer registers one user-level stdio server named `tadooer` and
installs the skill-only `tadooer-assistant@subcult-tadooer` plugin through each
client's native marketplace CLI. This avoids duplicate plugin and global MCP
servers. Existing assistants, plugins, approvals and models remain unchanged.

## Build and deploy

Pin a reviewed Tadooer Git revision, build `@suite/mcp-stdio` from an isolated
checkout, and run its tests. Pass the bundled `dist/main.mjs` to
`scripts/tadooer-assistant-host.py`. The runtime is copied outside worktrees;
the launcher records an absolute supported Node path and requires Node 24+.
For each host, stage the source plugin/runtime, inspect `plan`, then run `apply`
and `verify`. Saved plans guard configuration hashes; private receipts contain
backups and exact deployment hashes. Native CLIs own their plugin caches.

Known personal hosts: Kvant, Sputnik, Soyuz, Dozor, Almaz and NUC. Linux user
homes are `/home/onnwee`; Soyuz uses `/Users/onnwee`. Codex CLI and its desktop
runtime share the user's Codex configuration unless an installation explicitly
sets another `CODEX_HOME`. Claude Code uses its user configuration. Claude Desktop has a separate connector/configuration contract; this installer
targets Claude Code. Inventory a desktop installation separately before
claiming that it has working Tadooer access.

## Authentication

Settings are stored in `~/.config/tadooer/mcp.json` (or `TADOOER_MCP_CONFIG`):

```json
{
  "url": "https://tadooer.subcult.tv",
  "tokenFile": "/absolute/path/to/private/automation-token"
}
```

Create a scoped automation token in Tadooer Connections. Run
`~/.local/bin/tadooer-setup-token` on the target device and paste it into the
hidden local prompt. Use separately revocable tokens for devices when possible.
The helper refuses replacement of an existing token. Never place a token in
chat, a manifest, shell arguments, Git, or deployment receipts. The adapter
requires a regular, current-user-owned token file with mode `0600`.

Installation and tool-catalog discovery do not prove authenticated server
access. After credential setup, initialize the exact launcher, compare the
advertised schemas and perform one authorized read. Keep task content out of
deployment reports. If no token is found, record authentication as pending;
never manufacture credentials through the database or copy desktop cookies.

## Desktop and release evidence

Current Tadooer source includes Linux and macOS packaging, first-run server
selection, tray/menu-bar behavior, native notifications and opt-in autostart.
Build success does not establish signing, notarization, hardware behavior or a
published release. Consult the product-owned `docs/operations/desktop.md`,
release manifests and Gitea roadmap #136 before stating platform availability.
Older `Productivity Suite` and newer `Tadooer` profiles have separate settings.
Preserve both during installation and upgrades.

The canonical product repository is
[subculture-collective/tadooer](https://git.subcult.tv/subculture-collective/tadooer).
Its [installation and release roadmap](https://git.subcult.tv/subculture-collective/tadooer/issues/136)
distinguishes Linux/macOS, mobile, hosting and Google-backed sync gates.

## Guarded commands and recovery

The reviewed runtime revision and per-host Node/Python paths are in
`catalog/tadooer-assistant.json`. For a built adapter, run this sequence from
this repository, substituting the selected host's manifest values:

```sh
rtk proxy python scripts/tadooer-assistant-host.py plan --host kvant \
  --runtime /absolute/build/apps/mcp-stdio/dist/main.mjs \
  --node /usr/bin/node --revision REVIEWED_GIT_SHA
rtk proxy python scripts/tadooer-assistant-host.py apply --host kvant \
  --runtime /absolute/build/apps/mcp-stdio/dist/main.mjs \
  --node /usr/bin/node --revision REVIEWED_GIT_SHA
rtk proxy python scripts/tadooer-assistant-host.py verify --host kvant \
  --runtime /absolute/build/apps/mcp-stdio/dist/main.mjs \
  --node /usr/bin/node --revision REVIEWED_GIT_SHA
```

Remote deployment uses SSH and `--python` when the remote default is unsuitable.
The private receipt is `~/.local/state/tadooer-assistant/deployment.json`.
Each apply preserves a distinct `before-*` directory with configuration copies
and their hashes. The installer refuses changed plans and managed launchers.
It does not automatically restore whole client configurations after a failure.
For recovery, compare current state against this transaction, remove only its
unchanged Tadooer registrations through each native client CLI, and retain any
newer settings. A full-file restoration requires confirming that no later
client changes would be lost. Versioned plugin/runtime payloads stay available
for inspection and deliberate rollback.
