# Agent configuration source of truth

Author personal Codex skills, optional skill profiles, and Kvant's Codex bootstrap in this repository. Installed copies are deployments. Edit a source once, validate, commit, preview, apply, and verify. Keep the source repository private until redistribution and publication scope are reviewed.

## Ownership

| Material | Authority | Deployment |
|---|---|---|
| Curated personal skills | `skills/` and `catalog/proposed-catalog.json` | `~/.codex/skills/` via `scripts/install.py` |
| Shared interview and handoff | `shared/` | `~/.agents/skills/`; preserved by profile switching |
| Optional reservoir | `library/skills/` | Eligible skills copied to `~/.agents/skills/` by the profile command |
| Optional profile membership | `profiles/*.txt` | `~/.agents/skill-profiles` links here |
| Profile command | `scripts/skill-profile` | `~/.agents/bin/skill-profile` links here |
| Global Codex context and RTK | `instructions/` | `~/.codex/AGENTS.md` and `RTK.md` link here |
| Shared docs policy and HOMELAB | Machinum canonical policy/host briefings | Guarded `sync-briefings.py` generates `~/.homelab/HOMELAB.md` |
| Blacktower package and fleet enablement | Blacktower source and Estate Config `skills/hosts.json` | Estate Config's host-selected deployment |
| Four-vault instructions and local skills | `vault-agents/<vault>/AGENTS.md` and `vault-agents/<vault>/skills/`; deployment map in `catalog/vault-agents.json` | Each vault's `AGENTS.md`, `.agents/skills/`, and compatible `.opencode/skills/` copies via `scripts/vault-agents.py`; existing optional-library copies are also mapped. Blacktower package copies retain their package owner and need a separate release. |
| OS/system/plugin skills | Their owning package or plugin | Their managed directories; never edit their caches |

The 322-skill reservoir is preserved for selection and research, not a blanket endorsement. Some entries have been superseded by curated owners. Profiles filter curated and retired names, so old entrypoints cannot silently undo consolidation. Keep substantial optional procedures behind references in the owning skill.

Blacktower and personal Codex are separate distributions. Do not copy one over the other. Sputnik's `codex-skills` command uses Estate Config and toggles Codex configuration; Kvant's profile command manages optional shared copies. A future shared UI should call these explicit backends and show ownership, pending changes, and restart requirements. It must never edit package caches directly or pretend one profile applies identically to all clients.

## Daily use

```sh
rtk proxy ~/.agents/bin/skill-profile status
rtk proxy ~/.agents/bin/skill-profile list
rtk proxy ~/.agents/bin/skill-profile plan docs-research
rtk proxy ~/.agents/bin/skill-profile activate docs-research
rtk proxy ~/.agents/bin/skill-profile deactivate
```

These profiles change the optional shared skills, not the curated Codex base or plugin skills. Start a fresh agent session after changing discovery. The current conversation retains the catalog loaded at its start.

Use `requirements-interview` for a requested `grill-me` or `grill-with-docs`; its named mode supports deeper rounds without turning ordinary tasks into interviews. `unslop` is required for every user-facing prose response and documentation edit. Load it once per session; preserve facts and uncertainty. `code-review` owns blast-radius review. `implementation-plan` owns a reviewable decision trail for long efforts.

## Maintenance

Read the repository AGENTS.md, then the relevant `authoring/writing-for-agents/` reference when editing agent instructions. Define a specific trigger, an observable result, and nearby cases that should not trigger it. Preserve existing invocation policies; upstream Cursor/Claude frontmatter is not automatically Codex policy.

1. Check Git status and installed drift. Preserve intentional installed changes back into their source after reviewing the diff. Never rewrite the installer baseline just to obtain a pass.
2. Edit source files and any changed catalog ownership. Keep upstream URL, exact revision, file hash, license, and adaptation notes in the review ledger.
3. Run `rtk proxy python scripts/validate.py` and `rtk proxy python -m unittest discover -s tests -v`. Use behavioral trials for changed workflows and report which were simulated versus run in a new model session.
4. Commit reviewed source. Run `rtk proxy python scripts/install.py plan` and inspect changed destinations, then `apply` and `verify`. The install journal records verified backups and supports `rollback --run PATH`.
5. For source links, use `scripts/link-workstation.py plan`, inspect, then `apply`. Its recorded before-state guards replacements and its journal supports rollback.
6. Capture fresh discovery with `scripts/discovery.py`. Check owners appear once, retired names stay absent, and repo-local skills remain local.

To update an optional skill already active, edit its canonical library source and reconcile the active copy deliberately; drift is a stop, not a reason to overwrite. `promote` exists for an intentional active edit/new skill, preserves the replaced library version, and refuses curated owners. Review and commit its repository diff afterward.

## Claude Code on Kvant

Claude's `~/.claude/CLAUDE.md` links to `instructions/CLAUDE.md`, which imports
the shared global context. The workstation link manifest exposes the current
63 curated personal skills and five active shared skills through individual
links in `~/.claude/skills/`. Its two existing OS-owned skills and account-synced
skills keep their owners. System and Codex plugin skills are not copied.
After changing optional profile membership, review Claude's links too; the
manifest records this selection and does not automatically follow new names.

Use `python scripts/claude-mcp.py plan`, then `apply` and `verify`, to add
portable Codex MCP entries to Claude's user configuration. The script preserves
other state, refuses conflicting entries, and saves a private backup before
writing. It excludes the Codex desktop bridge and invalid or unsupported
entries. Registration does not establish connectivity or transfer OAuth login.
Run Claude's MCP health check separately and start a fresh session after changes.
To undo an added MCP entry, remove it only if it still matches the imported
entry; do not restore the entire backup over newer Claude state. Source-link
rollback uses the recorded `link-workstation.py` transaction.

The local `claude` launcher links to `scripts/claude-launcher`. It retains mise
version selection and resolves the executable with `mise which` to avoid
recursing through its own PATH entry. Its former wrapper is backed up by the
source-link installer.

Claude keeps its own runtime, model, permissions, hooks, authentication, and
memory. A linked skill that needs a missing tool must report the limitation.

## Runtime instruction chain

### Fleet Gitea identity

`instructions/GITEA.md` owns the shared agent identity guidance. Its deployed copy
is `~/.config/agent-identity/GITEA.md`; user-controlled Codex, Claude and OpenCode
instructions import it without replacing their other guidance. Gitea CLI defaults,
HTTPS credentials and conditional commit attribution select `subcult-agent`.
Other Git hosts retain their existing identity. Explicit service credentials are
separate consumers and require their own access and runtime migration checks.
The user explicitly keeps Switchyard on `open-pilot`; a fleet default or token
scope update must preserve that runtime credential and identity.

`scripts/gitea-agent-host.py` applies a host configuration and records private
before-state backups and hashes. It receives the device token and instruction
text through stdin; never put tokens in arguments or repository files. The
`apply` stage retains existing logins, sets the agent default, installs an
isolated Git helper, replaces only Gitea SSH URL redirects with HTTPS, and adds
conditional Gitea author settings. On macOS, the ordinary tea configuration is
under `~/Library/Application Support/tea/` unless XDG configuration overrides it.

The `normalize` stage receives a parsed tea configuration with the agent login
first and the current file hash, refuses a changed file, preserves the other
logins, and verifies repository-context selection. This step matters because tea
may select the first matching login inside a checkout instead of its marked
default. Final `verify` requires the agent identity both inside and outside a
repository, the agent Git credential, conditional author attribution, HTTPS
transport, and a successful push dry run. A pending context check is not a
completed fleet rollout. The registry audit and local checks do not prove other
devices; retain each host's actual verification receipt.

The `rotate` stage accepts replacement-token configurations through stdin,
checks both the ordinary and isolated tea configurations against their current
hashes, saves private backups, and updates the agent entry in both. It verifies
the authenticated account, access to the admin API, and the exact token selected
by Git. On failure it restores only files that still match this transition's
written hashes, preserving concurrent edits. The six device tokens gained
`write:admin` with user authorization on October 3, 2026; the previous tokens
remain recovery credentials rather than current device defaults.

For rollback, require each touched file to match its receipt's final hash before
restoring its private before-state backup, or removing a file that was originally
absent. Refuse later edits. Preserve retained human credentials and revoke only
the device token being retired; do not restore a whole unrelated configuration
or token inventory from another device.

The client supplies its runtime rules, conversation, available tools, and selected skill metadata. User-controlled Codex context starts at the global AGENTS.md; nearest project instructions add local scope. RTK is required shell guidance. HOMELAB supplies host and documentation policy, with dated history loaded only when relevant. Skills expose names/descriptions for selection; procedures and references are loaded when needed. Exact expansion and context packing depend on the client; filesystem inventory is not a complete runtime prompt trace.

Keep infrastructure history and operating notes in Machinum. Keep executable configuration in its owning repository. Documentation should link to the owner instead of copying editable skill bodies. Fleet rollout of this personal repository requires host inventories, destination mappings, preview, and guarded application; this workstation release does not claim fleet parity.

## Required prose policy across hosts

The canonical Agent Documentation Policy in Machinum requires unslop for every prose response and documentation edit, regardless of optional profile selection. It includes direct file paths so the requirement also works when a client does not automatically select the skill. Load once per session. Kvant uses this repository's managed skill. Almaz, Dozor, and NUC received the same source with hash receipts at `~/.codex/skill-installations/required-unslop.json`; Soyuz and Sputnik retain their existing owners. Review those receipts and preserve local drift before updating remote personal copies. Full personal-catalog fleet deployment remains separate.

## Installing one personal skill

Use `python scripts/install.py plan --only-skill NAME`, then `apply` and `verify`
with the same selector for a bounded personal-skill change. Selected destinations
retain the normal source, drift, backup, and transaction checks. Other skills and
repository-local installs are left untouched; this does not repair or verify
unrelated drift. Saved transactions retain their original scope during resume
and rollback.

`t3-repo-setup` owns onboarding repositories into the T3 development launcher.
Its operational guide and recipe schema remain owned by `t3-dev-environments`.

## Vault-local agent configuration

`vault-agents/` owns the four-vault instruction and skill sources. These skills
remain local to their vaults; they are not added to the curated global catalog.
The complete file mapping is `catalog/vault-agents.json`. Use
`python scripts/vault-agents.py plan`, review destinations, then `apply` and
`verify`. The tool refuses destination drift and records backups under
`~/.local/state/vault-agent-deployments/`. For a later update, reconcile reviewed
destination hashes in the manifest; never replace a drift baseline just to pass.

The personal vault retains eight skills. SUBCULT has its planning skill and
Patreon manager; Machinum and Archivum each have one focused skill. The old
personal OpenCode Patreon entrypoint remains compatible but routes to Studio.
Copied instructions inside Archivum reference collections are not deployment
targets. Test new skills with the skill-creator validator and check routing
against the positive and near-miss cases in `vault-agents/acceptance.md`.
