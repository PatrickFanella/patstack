# Tadooer assistant fleet installation: October 11, 2026

The personal Tadooer MCP registration and `tadooer-assistant@subcult-tadooer`
plugin version 1.0.1 are installed for Codex and Claude Code on Kvant, Sputnik,
Soyuz, Dozor, Almaz and NUC. All six use the same reviewed plugin payload
`3e4ed44ecec078b3` and adapter built from Tadooer revision
`928af1d88b0ddd8878daf1a87e3871388369121f`. Runtime SHA-256:
`a159e56f9588111c32404c9bb5ec1e59d0ee4efc13caaccb5f3d1a213ae8f5f7`.

## Evidence

For each host, the guarded installer verified both user MCP entries, plugin
configuration and copied payload hashes. Native client plugin listings report
the plugin enabled. A fresh Codex app-server `skills/list` discovers exactly one
`tadooer-assistant:tadooer-workflow` skill from the installed plugin. Existing
conversations retain the catalog they loaded earlier; start a fresh session.

A separate fixture initialized the exact installed launcher and listed its
catalog on every host: protocol status `ok`, 102 tools, including `suite.confirm`.
The fixture used a synthetic credential in a temporary mode-0600 file and an
unused loopback port. It called no application operation and deleted its files.
These results prove transport startup and static catalog discovery. The initial fixture performed no production read or mutation. The follow-up
qualification below completed an authenticated read on every host. No model
session or paid inference was used for qualification.

The product adapter's three test files passed all 11 tests. Canonical skill
validation, Claude plugin validation and `scripts/validate.py` passed. The
canonical repository suite passed all 45 tests with `/usr/bin/python` and a
system PATH. The first run encountered three unrelated mise trust failures in
its temporary-home fixtures; no trust setting was changed to obtain the pass.

## Runtime and recovery

Kvant uses its existing Node 24.18.0; Sputnik and Soyuz use 24.21.0; Almaz uses
24.14.1; NUC uses 24.15.0. Dozor's system Node was below the adapter requirement,
so it uses a private official Node 24.21.0 sidecar. The download hash matches the
official Node checksums; provenance and absolute executable paths are in
`catalog/tadooer-assistant.json`. System runtimes were not replaced.

Private receipts and configuration backups are under each user's
`~/.local/state/tadooer-assistant/`. Runtime/plugin source snapshots are under
`~/.local/share/tadooer-assistant/`. Native client CLIs own their caches.

The first version update refused an existing marketplace with a different
source path. The two changed Kvant launchers were restored only after matching
the attempted update and checking their backup hashes. The installer now checks
owned marketplace sources, migrates through native CLIs and records an
intermediate receipt for retry. Soyuz's first update also refused a concurrently
changed Claude configuration; a fresh plan succeeded. Its unrelated Blacktower
marketplace is malformed, so the bounded installer reads only Tadooer's source
registration instead of requiring every marketplace to load. That unrelated
configuration remains outside this change. Claude requires an explicit native
plugin update after install to advance an already-installed version; final
verification checks both clients against version 1.0.1.

## Authentication and scope

The owner signed into the collaborative Tadooer browser and selected read and
manage permissions for tasks, projects, schedule, focus, habits and templates.
Six separate device tokens were issued through the ordinary session/CSRF
protected API, with `confirm_all` and a 30-day expiry of
`2026-11-10T21:11:30.592Z`. The scope set includes read/write for those six
areas plus `planning:write` for daily planning. No connector recovery, calendar
publication, notification tests or application-settings write scope was added.

Tokens were encrypted in the browser for transfer, decrypted only in process
memory on Kvant and sent to each device through SSH stdin. No plaintext token
was printed or saved in a shared handoff file. Each device saved its credential
at its configured absolute path with current-user ownership and mode `0600`.
The temporary encryption key and encrypted browser download were deleted after
all six hosts verified access. No browser cookie became an MCP credential.

The exact installed MCP launcher on every host initialized, listed 102 tools
and successfully called `suite.tasks.list` against the hosted instance. Task
content was suppressed from receipts and reports. Authentication receipts at
`~/.local/state/tadooer-assistant/authentication.json` record non-secret token
metadata, expiry, confirmation policy and read verification. No production task
mutation was performed; management scopes are granted but write behavior was
not qualified against live records.

The initial searches found no reusable automation token in the searched
configuration, state, local data, private assistant configuration or
application-support locations. These searches reported only paths and
permission metadata for candidates, never secret values. They do not establish
absence on every disk.

Public `/.well-known/oauth-authorization-server` returned the HTML web app on
October 11, so hosted OAuth compatibility remains unqualified. This rollout
uses the verified local stdio adapter and scoped device tokens. The desktop
login remains separate from assistant credentials. Revoke a device's access
in Connections when retiring it; replace expired credentials deliberately with
`tadooer-setup-token` and repeat an authenticated read.

This deployment covers the known user's Codex and Claude Code configurations.
No separate Claude Desktop app/configuration was found in the standard checked
locations. It does not establish hosted ChatGPT/Claude connector access, OAuth
provider approval, macOS signing, mobile availability or a public desktop
release. Product release scope stays with the Tadooer roadmap and source docs.

Canonical procedure: [Tadooer assistant installation](../TADOOER-ASSISTANTS.md).
The pre-existing dirty Tadooer desktop worktree was preserved; the adapter was
built in a separate pinned checkout. The canonical source changes are prepared on an isolated review branch based
on current Gitea main. The original source branch and dirty product worktree
remain available; publication does not merge or deploy a product release.
