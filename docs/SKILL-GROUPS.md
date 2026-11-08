# Skills and task stacks

Subsets manages the user-level skill selection across clients. Patstack owns
the authored sources, profiles, qualification and relationship catalog.
There is one selected stack, with generated views into one reviewed library;
there is no separate always-installed personal layer.

## Contents

- [Everyday core](#everyday-core)
- [Task sets](#task-sets)
- [Client views and exceptions](#client-views-and-exceptions)
- [Required and optional companions](#required-and-optional-companions)
- [Selection and recovery](#selection-and-recovery)

## Everyday core

`core` selects **41 skills** for frequent repository, web/API, agent-tool,
documentation and operations work. It includes planning, debugging, review,
Git/CI delivery, UI quality, common languages, MCP, data changes, research,
verification and continuation. The UI defaults include the pinned
`avoid-ai-design` scanner and guidance through `ui-cliche-audit` and `ui-craft`.

Core is a working toolkit, not a request to load every skill body. Agents
read the relevant procedure and its needed references. There is no need
to choose a specialist set for an occasional task: the router can resolve
inactive sources from the same library.

## Task sets

The **11 task sets** combine disciplines around an outcome. Core is always
included. Sets overlap deliberately; they are not exclusive professional
categories. Several can be combined. All **220 selectable owners**
belong to at least one set, including core.

| Stack | Added beyond core | Total selected | Use it for |
|---|---|---|---|
| [`core`](../profiles/CATALOG.md#core) | 0 | 41 | Everyday repository work, debugging, delivery, web/API changes, tools, documentation and basic operations. |
| [`build-agent-tools`](../profiles/CATALOG.md#build-agent-tools) | 28 | 69 | Build and configure agents, MCP servers, CLIs, retrieval, evaluations and development environments. |
| [`build-and-ship`](../profiles/CATALOG.md#build-and-ship) | 34 | 75 | Take a feature from understanding and design through implementation, review, tests and a PR. |
| [`creative-production`](../profiles/CATALOG.md#creative-production) | 14 | 55 | Plan and produce visual, audio, video or slide material with a coherent voice and delivery format. |
| [`data-and-decisions`](../profiles/CATALOG.md#data-and-decisions) | 10 | 51 | Investigate evidence, analyze data, compare alternatives and communicate a decision. |
| [`diagnose-and-repair`](../profiles/CATALOG.md#diagnose-and-repair) | 20 | 61 | Reproduce a failure, inspect code/runtime evidence, repair it and prove the result. |
| [`fiction-and-worlds`](../profiles/CATALOG.md#fiction-and-worlds) | 31 | 72 | Develop stories and settings, draft scenes, revise character/dialogue, and maintain continuity. |
| [`learn-and-practice`](../profiles/CATALOG.md#learn-and-practice) | 9 | 50 | Plan learning, study examples, tutor, build exercises and review progress. |
| [`mobile-and-interfaces`](../profiles/CATALOG.md#mobile-and-interfaces) | 10 | 51 | Build and test mobile, terminal, editor, browser and interactive interfaces. |
| [`operate-homelab`](../profiles/CATALOG.md#operate-homelab) | 26 | 67 | Operate services and personal tools, investigate incidents, change infrastructure and verify recovery. |
| [`product-and-launch`](../profiles/CATALOG.md#product-and-launch) | 25 | 66 | Research a market, choose positioning, prepare brand/product copy, refine the interface and plan a launch. |
| [`research-and-write`](../profiles/CATALOG.md#research-and-write) | 26 | 67 | Find and check sources, develop an argument, write or revise, and produce documents. |

The [membership reference](../profiles/CATALOG.md) lists the core and every
set's additions with source links and descriptions. The additions exclude
core duplicates; total selected counts the union.

## Client views and exceptions

| Client view | Path |
|---|---|
| shared | `~/.agents/skills` |
| codex | `~/.codex/skills` |
| claude | `~/.claude/skills` |
| copilot | `~/.copilot/skills` |
| cursor | `~/.cursor/skills` |
| opencode | `~/.config/opencode/skills` |
| opencode-legacy | `~/.opencode/skills` |

Subsets creates individual links to the selected immutable bundle sources.
It does not replace whole client directories. Native views follow the
declared source contracts; Cursor and Copilot use Claude-compatible Agent
Skills files. Shared compatibility roots may also be visible to a client.
Installed files do not prove that tools, authentication or invocation
semantics are identical in every application.

Package/system/plugin skills, app-specific skills and repository/vault
skills retain their owners and locations. Unknown entries are preserved.
A same-name collision requires review instead of overwriting another owner.
The initial takeover requires exact matches to predecessor installer
receipts; changed files stop migration before skill paths change. Released
ownership manifests and original files are backed up in the transaction.

Client location references: [Cursor skills](https://cursor.com/help/customization/skills)
and [Copilot skills](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-skills).

## Required and optional companions

The [relationship catalog](../catalog/skill-routes.json) connects default
and specialist skills, including specialist-to-specialist links. Each link
states its condition. Required steps apply only when that condition holds;
optional helpers are read only when useful. A link does not authorize
edits after an audit, publication after drafting, or agent delegation.

For example, UI implementation requires behavior proof before claiming
success; Python Temporal work can require replay tests; fiction drafting
can consult dialogue or world-continuity specialists. Already loaded
procedures are reused rather than recursively loading the relationship graph.

## Selection and recovery

Preview and apply a task set:

```sh
rtk proxy subsets apply --build-and-ship --dry-run
rtk proxy subsets apply --build-and-ship
rtk proxy subsets apply --group core
```

Start a fresh agent session after changing discovery. To undo a switch,
use the recorded run directory with `~/.agents/bin/skill-profile rollback --run`.
Undo later runs first. Rollback refuses subsequent edits and retains the
canonical sources. Receipts are under `~/.local/state/subsets-fleet/profiles`.

Edit source skills and profiles in patstack, validate and commit, then build
and deploy a new bundle. The legacy personal/profile/link installers must
not reclaim these paths after migration. Project and vault deployers remain
separate. See [the adapter runbook](../runtime-bundles/subsets-fleet/README.md).
