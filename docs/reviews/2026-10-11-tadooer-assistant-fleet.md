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
These results prove transport startup and static catalog discovery. No
production authenticated read or mutation was performed, and no model session
or paid inference was used for qualification.

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

Authentication is pending on all six hosts. No automation-token prefix was found in the searched configuration, state,
local data, private assistant configuration or application-support locations
on any host. The search reported only paths and permission metadata for
candidates; no secret values were printed. This is evidence for those searched
locations, not a claim about every file on every disk. The desktop login remains separate from assistant credentials.
Create a scoped token in Tadooer Connections and enter it on the chosen device
through `~/.local/bin/tadooer-setup-token`; the local prompt hides input and
writes a private file. Then verify an authorized read against the real server.
Do not place credentials in chat or Git. Separate revocable device tokens are
preferred.

This deployment covers the known user's Codex and Claude Code configurations.
No separate Claude Desktop app/configuration was found in the standard checked
locations. It does not establish hosted ChatGPT/Claude connector access, OAuth
provider approval, macOS signing, mobile availability or a public desktop
release. Product release scope stays with the Tadooer roadmap and source docs.

Canonical procedure: [Tadooer assistant installation](../TADOOER-ASSISTANTS.md).
The pre-existing dirty Tadooer desktop worktree was preserved; the adapter was
built in a separate pinned checkout. These source changes are committed locally
in codex-skills; publication of its existing branch was not part of this rollout.
