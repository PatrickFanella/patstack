# Agent configuration source of truth

Patstack owns skill sources, task profiles, relationships and global agent
instructions. Subsets owns user-level skill selection and client views.
Installed files are deployments. Edit source once, validate, commit, preview,
apply and verify. Keep this source repository private until publication scope
and redistribution rights are reviewed.

## Ownership

| Material | Authority | Deployment |
|---|---|---|
| Curated, shared and specialist sources | `skills/`, `shared/`, `library/skills/`, qualification and provenance catalogs | One reviewed Subsets bundle |
| Everyday core and task sets | `profiles/*.txt`, `catalog/skill-stacks.json` | Subsets selects core plus requested task sets |
| User skill views | Bundle sources and Subsets transaction receipts | Individual links under `.agents`, `.codex`, `.claude`, `.copilot`, `.cursor` and OpenCode user roots |
| Conditional companions | `catalog/skill-routes.json`, each owner's companion reference | Default router reads the needed source without a whole-stack switch |
| App, package and system skills | Their owning application/package | Preserved in place; never adopt caches or OS skills |
| Project and worktree skills | `project-agents/`, project selection catalog | Guarded `project-skills.py` deployment |
| Vault instructions and skills | `vault-agents/`, vault deployment catalog | Guarded `vault-agents.py` deployment |
| Global client instructions | `instructions/WORKING.md`, `instructions/hosts.json` | Guarded `global-instructions.py` deployment |
| Source workstation links outside skill views | `catalog/workstation-links.json` | Guarded `link-workstation.py`; transferred skill paths are excluded |
| HOMELAB and documentation policy | Canonical Machinum notes | Documentation-Hub's guarded briefing sync |
| Switchyard OpenCode image skills | `runtime-bundles/switchyard-opencode.json` | Image-owned export and lockfile; separate runtime distribution |
| Blacktower distribution | Blacktower and Estate Config | Its package/release owner; not replaced by personal Subsets selections |

The historical `personal`, `shared` and `optional` source labels describe
provenance and source layout. They no longer determine an always-active runtime
layer. Core is the complete everyday default. The 326-entry reservoir retains
archived and superseded sources for provenance; only eligible canonical owners
are selectable. Retired names have no compatibility entrypoints.

## Daily use

```sh
rtk proxy subsets apply --build-and-ship --dry-run
rtk proxy subsets apply --build-and-ship
rtk proxy subsets apply --research-and-write --product-and-launch
rtk proxy subsets apply --group core
rtk proxy ~/.agents/bin/skill-profile status
```

Start a fresh session after changing discovery. Existing sessions retain their
initial skill metadata. The router can load a one-off specialist from the
managed library without changing the selected stack. Required and optional
companion links apply only under their condition and within current scope.
See [the task guide](SKILL-GROUPS.md) and [membership catalog](../profiles/CATALOG.md).

## Source changes and deployment

1. Inspect source status and destination drift. Preserve installed edits and
   unrelated work. Read the maintenance skill and relevant authoring guidance.
2. Edit source and any affected qualification, provenance, profiles or routes.
   New imported procedures need a pinned revision/license and positive/near-miss
   cases. Preserve invocation and client tool contracts.
3. Regenerate the guide with `python scripts/stack-catalog.py`. Run
   `python -B scripts/validate.py` and
   `python -B -m unittest discover -s tests -v`. Use bounded behavioral fixtures;
   distinguish structural proof from fresh-model and actual client execution.
4. Commit reviewed source and build the Subsets bundle with
   `python -B runtime-bundles/subsets-fleet/scripts/build-bundle.py`.
   Use `umask 022`; mode drift is real drift to the installers.
5. Follow the [adapter runbook](../runtime-bundles/subsets-fleet/README.md) to
   preview, deploy and verify. Confirm protected paths, ownership transfer,
   selected skills and fresh discovery. A local deployment does not prove fleet
   parity, remote CI, authentication or runtime behavior in every client.

The legacy `install.py` personal installer, source `skill-profile` command and
`optional-clients.py` must not reclaim user skill paths after takeover. Their
transaction primitives remain used for backups/recovery and historical tests.
The source-link installer skips transferred skill views while retaining its
other links. Do not bypass a guard or reset an ownership baseline to get a pass.

## Initial ownership transfer and recovery

Subsets adopts a known user skill path only when its current snapshot matches
its predecessor receipt. It releases just those path records from the old
personal and source-link manifests in the same transaction as the generated
views and ownership marker. Original files and both manifests have verified
backups. Unknown entries, app-specific skills and package/system owners remain
untouched; a conflicting selected name stops migration for review.

The adapter holds its selection lock and predecessor locks during takeover.
Subsequent switches change only recorded paths and preserve local drift.
Rollback restores the preceding selection; rollback of the initial takeover
also restores predecessor ownership. Undo later runs first. Later edits stop
rollback before restoration. Keep transaction directories under
`~/.local/state/subsets-fleet/profiles/` while recovery is needed.

## Claude and other clients

The same selector generates all configured native views, not a second Claude
link pass. File compatibility is not tool equivalence. Cursor and Copilot use
Claude-compatible Agent Skills content; OpenCode native views follow declared
OpenCode source contracts. Shared compatibility roots can also be read by
clients. Never infer tool access or identical invocation behavior from a link.

Claude's runtime, hooks, permissions, authentication and MCP remain separate.
`claude-mcp.py` still manages its bounded MCP imports with private backup and
conflict refusal. Registration does not prove connectivity or transfer OAuth.
The local Claude launcher retains mise selection; see its source script.

## Skill names

Use distinct names such as `bug-tracer`, `prose-unslop` and `behavior-proof`.
`catalog/retired-names.json` records earlier names, canonical owners and
procedures. Do not regenerate the historical collection builder over curated
sources or add discovery aliases for retired names. Project/vault skill names
retain their deployer ownership until those deployers can retire old paths.

## Public edition

`catalog/public-edition.json` lists the 42 skills exported to the
`generic-skills` repository and the `@subcult/patstack` npm package, which
Subsets offers as its default optional pack. `generic-skills` has been private
on Gitea since 2026-11-03; its older public GitHub copy is retained but no
longer receives updates. Export from a reviewed checkout:

```sh
python scripts/public-edition.py --check ../generic-skills   # stage and leak-check only
python scripts/public-edition.py ../generic-skills           # export, refresh provenance and README
```

The export copies current sources, keeps each skill's license from the
published copy, rewrites Blacktower notices to the public attribution, moves
frontmatter fields the public validator rejects into `metadata`, and applies the
listed substitutions. It refuses the export if any `forbidden` pattern (fleet
account names, private hosts and paths) remains. Add a substitution or
generalize the source when it does. Review the diff in `generic-skills`, run its
`scripts/validate.py`, open a PR there, and tag a release to publish.

## Global client instructions

Every host's Codex, Claude Code and OpenCode global file is generated. The
shared part is `instructions/WORKING.md`: the owner's working preferences,
written from observed failures in session history and kept as defaults a prompt
can override. When a correction recurs, add a rule there with a short bad/good
example. Per-host facts (home, RTK, vaults, Blacktower, local notes) live in
`instructions/hosts.json`; client differences live in the renderer. The same
run also manages directory context files, which apply only to sessions started
in that folder: `~/.agents/AGENTS.md` everywhere and any `contextFiles` listed
for a host (Soyuz's `~/AGENTS.md`). On RTK hosts it writes `~/.codex/RTK.md` and
`~/.claude/RTK.md`, which `rtk init --show` checks. On Almaz, `~/.agents` is also
the dormant Agent Hub repository; its `AGENTS.md` and `CLAUDE.md` are rendered
with a `contextNote` that points at the hub's own docs, and the two files are
committed on the hub's local branch so its status shows their owner.

Claude expands `@` imports; Codex does not (checked on 2026-11-03 with a
no-tools probe that could not see HOMELAB content). Codex and OpenCode files
therefore tell the agent to open HOMELAB and GITEA itself, and owned content is
inlined rather than imported. Externally owned files stay references: HOMELAB is
generated from Machinum and GITEA is written by `gitea-agent-host.py`, whose
duplicate check finds the `@` path already present.

Preview with `python scripts/global-instructions.py render --host HOST`. Deploy
with `plan --host HOST`, review, then `apply` and `verify`. The first apply on a
host adopts the existing files after backing them up, including Kvant's former
symlinks; later runs refuse a file hand-edited since the last deploy. Receipts
and private backups are under `~/.local/state/agent-global-instructions/`;
`rollback` restores the latest run only when every touched file still matches
its receipt. Start a fresh agent session to load a change.

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
remain recovery credentials rather than current device defaults. The user then
authorized full permissions; all six defaults now use replacement tokens with
the `all` scope. Scope readback and package listing were verified. Token
creation requires account authentication on this instance; using a personal
access token at that endpoint returns `401 auth required` even with `all`.
Keep this distinction when preparing scoped publishing credentials.

For rollback, require each touched file to match its receipt's final hash before
restoring its private before-state backup, or removing a file that was originally
absent. Refuse later edits. Preserve retained human credentials and revoke only
the device token being retired; do not restore a whole unrelated configuration
or token inventory from another device.

The client supplies its runtime rules, conversation, available tools, and selected skill metadata. User-controlled Codex context starts at the global AGENTS.md; nearest project instructions add local scope. RTK is required shell guidance. HOMELAB supplies host and documentation policy, with dated history loaded only when relevant. Skills expose names/descriptions for selection; procedures and references are loaded when needed. Exact expansion and context packing depend on the client; filesystem inventory is not a complete runtime prompt trace.

Keep infrastructure history and operating notes in Machinum. Keep executable configuration in its owning repository. Documentation should link to the owner instead of copying editable skill bodies. Fleet rollout of this personal repository requires host inventories, destination mappings, preview, and guarded application; this workstation release does not claim fleet parity.

## Required prose policy across hosts

The canonical Agent Documentation Policy in Machinum requires `prose-unslop` for every prose response and documentation edit, regardless of the selected task stack. It includes direct file paths so the requirement also works when a client does not automatically select the skill. Load once per session. `prose-unslop` is in the core profile, so every host receives it through its Subsets deployment. The older `~/.codex/skill-installations/required-unslop.json` receipts on Almaz, Dozor and NUC record the pre-Subsets copies and are historical.

## Updating a user skill

Edit its canonical source, validate and commit, then build a new Subsets bundle.
Preview the intended stack and deploy the bundle. Do not reinstall a personal
copy outside the selected stack. Inactive sources remain readable through the
router. Project and vault changes keep their own guarded deployers.

Shared marketing procedures and reading bundles are described in
[Shared marketing tools](MARKETING-TOOLS.md). Product packets remain owned by
their project; a reading copy does not become a competing authoring master.

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
targets. Test new skills with the skill-forge validator and check routing
against the positive and near-miss cases in `vault-agents/acceptance.md`.

## Tadooer assistant integration

`integrations/tadooer/` owns the personal Tadooer workflow plugin for Codex and
Claude Code. Native client installers own deployed caches; the product owns its
MCP runtime. Use the bounded fleet installer and manifest described in
[Tadooer assistant installation](TADOOER-ASSISTANTS.md). Authentication is a
separate check requiring a scoped token stored privately on the device.
