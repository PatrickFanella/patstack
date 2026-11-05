# Skill groups and defaults

The default stack provides entry points for everyday work. Those skills can
load qualified specialists from the managed library without changing Subsets.
A group switch changes the skills the client discovers directly in a new
session; it is useful for a sustained change of working stack, not a prerequisite
for a single specialist task.

## Contents

- [Default layers](#default-layers)
- [Default personal skills](#default-personal-skills)
- [Default shared skills](#default-shared-skills)
- [Subsets groups](#subsets-groups)
- [Required and optional relationships](#required-and-optional-relationships)
- [The design skill integration](#the-design-skill-integration)
- [Selection and client limits](#selection-and-client-limits)

## Default layers

| Layer | Contents | Controlled by Subsets? |
|---|---|---|
| Personal | 52 authored skills in `skills/`, installed in `~/.codex/skills` | No |
| Shared | 6 skills in `shared/`, including `skill-stack-router` | Always included |
| Optional core | `claim-verifier`, `digest-distiller`, `web-lookup` | Always included by the selector |
| Optional specialists | 162 unique activatable library skills across 14 groups, including core | Selected for direct discovery; also readable on demand |
| Project and vault | Skills owned by the current project or vault | Separate guarded selections |
| System, OS and plugins | Skills supplied by their owning package | No; keep their owners |

“Default” means available for selection by the agent. It does not mean every
skill body is loaded on every task. Other installations can remain visible;
returning to `core` does not remove skills owned by another installer.

## Default personal skills

These are the authored personal defaults. Claude exposure uses individual
managed links. Other clients must follow their qualification and tool contracts.

| Skill | Purpose |
|---|---|
| [`api-contract-smith`](../skills/api-contract-smith/SKILL.md) | API contracts and backend protocols: REST/GraphQL, OpenAPI, Node services, and WebSocket lifecycle design. |
| [`auth-gatekeeper`](../skills/auth-gatekeeper/SKILL.md) | Implement or debug authentication and authorization: sessions, OAuth, tokens, roles, and access checks. |
| [`bash-script-craft`](../skills/bash-script-craft/SKILL.md) | Shell scripting, ShellCheck linting, and Bats tests; preserve exit status, quoting, cleanup, and portability. |
| [`behavior-proof`](../skills/behavior-proof/SKILL.md) | Verify UI, CLI, API, build, or performance claims using runnable evidence; distinguish smoke checks from regressions. |
| [`boundary-drafter`](../skills/boundary-drafter/SKILL.md) | Architecture and domain modeling: module boundaries, dependency cycles, CQRS, and domain vocabulary. |
| [`bug-tracer`](../skills/bug-tracer/SKILL.md) | Reproduce and diagnose a defect; choose a tight failing check, isolate the cause, and verify the repair. |
| [`build-sequencer`](../skills/build-sequencer/SKILL.md) | Plan or implement a bounded feature from a spec; map acceptance criteria to changes and executable verification. |
| [`bus-factor-map`](../skills/bus-factor-map/SKILL.md) | Requested security ownership and bus-factor analysis from Git history; identify sensitive-code ownership gaps. |
| [`cf-edge-deploy`](../skills/cf-edge-deploy/SKILL.md) | Cloudflare Workers and Pages deployment; follow the selected product and verify the deployed artifact. |
| [`ci-medic`](../skills/ci-medic/SKILL.md) | CI failures, pipelines, pre-commit hooks, and code scanning; distinguish local checks from hosted run results. |
| [`cli-contract-smith`](../skills/cli-contract-smith/SKILL.md) | CLI design and implementation: flags, subcommands, completions, interactive fallback, and automation contracts. |
| [`dep-source-clone`](../skills/dep-source-clone/SKILL.md) | Inspect dependency source at the lockfile-resolved version; obtain only the repositories needed for the investigation. |
| [`dep-upgrade-pilot`](../skills/dep-upgrade-pilot/SKILL.md) | Upgrade dependencies with lockfile evidence, breaking-change analysis, proportional testing, and rollback. |
| [`diff-inspector`](../skills/diff-inspector/SKILL.md) | Review code changes for actionable defects or requested maintainability concerns; keep repository audits separate. |
| [`eval-bench`](../skills/eval-bench/SKILL.md) | Evaluate LLM behavior with representative datasets, baselines, task metrics, and reproducible results. |
| [`git-surgery`](../skills/git-surgery/SKILL.md) | Git conflicts, worktrees, history repair, and PR preparation; hosted operations follow the configured remote. |
| [`gitea-fleet-tidy`](../skills/gitea-fleet-tidy/SKILL.md) | Audit or modernize Gitea/Forgejo repository settings, issues, workflows, and release organization. |
| [`go-craft`](../skills/go-craft/SKILL.md) | Go concurrency, interfaces, errors, profiling, and tests; use relevant patterns for the existing application. |
| [`mcp-server-forge`](../skills/mcp-server-forge/SKILL.md) | Build MCP servers with explicit tool contracts, transports, errors, and executable interoperability checks. |
| [`mcp-wire-tracer`](../skills/mcp-wire-tracer/SKILL.md) | Diagnose MCP registration, transport, initialization, catalog, auth, and reload boundaries in the active client. |
| [`mtls-trust-chain`](../skills/mtls-trust-chain/SKILL.md) | Configure and diagnose mutual TLS: certificate identity, trust chains, rotation, and service authentication. |
| [`perf-hotpath-probe`](../skills/perf-hotpath-probe/SKILL.md) | Diagnose measured latency, CPU, memory, or throughput regressions using comparable profiles and benchmarks. |
| [`pet-hatchery`](../skills/pet-hatchery/SKILL.md) | Create or repair Codex v2 animated pets; validate atlas geometry, directions, transparency, and packaging. |
| [`pg-plan-reader`](../skills/pg-plan-reader/SKILL.md) | PostgreSQL query plans, indexes, locks, replication, and data-quality checks against the real schema. |
| [`playwright-cli-driver`](../skills/playwright-cli-driver/SKILL.md) | Automate a browser with Playwright CLI for navigation, interaction, inspection, and evidence capture. |
| [`privacy-controls`](../skills/privacy-controls/SKILL.md) | Implement requested personal-data controls: consent, retention, deletion, portability, and auditability. |
| [`prose-unslop`](../skills/prose-unslop/SKILL.md) | Required for every user-facing prose response and documentation edit. Remove filler while preserving meaning, facts, uncertainty and voice; explain again in plain language when an explanation did not land. |
| [`python-uv-workbench`](../skills/python-uv-workbench/SKILL.md) | Python tooling, packaging, settings, uv environments, and pytest; select the procedure for the requested change. |
| [`react-render-tuner`](../skills/react-render-tuner/SKILL.md) | React/Next.js state, rendering, data loading, component APIs, and performance within the existing application. |
| [`red-green-loop`](../skills/red-green-loop/SKILL.md) | Test-first implementation when requested: red-green-refactor, test boundaries, fixtures, and meaningful assertions. |
| [`repo-atlas`](../skills/repo-atlas/SKILL.md) | Map repository structure and update existing code maps incrementally using the bundled inventory helper. |
| [`retrieval-pipeline`](../skills/retrieval-pipeline/SKILL.md) | Retrieval systems: ingestion, vector/keyword search, ranking, citations, and retrieval-quality measurement. |
| [`rust-ownership-async`](../skills/rust-ownership-async/SKILL.md) | Rust ownership, async execution, errors, concurrency, and systems integration within the existing crate design. |
| [`safe-refactor-pass`](../skills/safe-refactor-pass/SKILL.md) | Behavior-preserving refactoring and code simplification; plan changes when requested and verify public contracts. |
| [`sandbox-desktop`](../skills/sandbox-desktop/SKILL.md) | Isolated agent desktop/browser workspace operations and QA; use its MCP surface rather than host desktop control. |
| [`schema-migrator`](../skills/schema-migrator/SKILL.md) | Database schema and data migrations: compatibility, backfills, validation, cutover, and rollback. |
| [`secret-rotation-flow`](../skills/secret-rotation-flow/SKILL.md) | Implement CI/runtime secret storage, delivery, and rotation using the environment’s existing secret provider. |
| [`secure-code-audit`](../skills/secure-code-audit/SKILL.md) | Requested security review or secure coding guidance for Python, JavaScript/TypeScript, and Go. |
| [`setup-wizard-script`](../skills/setup-wizard-script/SKILL.md) | Build an interactive setup script for steps requiring human input; keep secrets hidden and actions reviewable. |
| [`ship-check`](../skills/ship-check/SKILL.md) | Audit a repository against its intended capabilities; separate implemented, incomplete, planned, and unverified work. |
| [`stride-threat-map`](../skills/stride-threat-map/SKILL.md) | Requested repository threat model: assets, trust boundaries, attacker paths, and prioritized mitigations. |
| [`stripe-billing-guard`](../skills/stripe-billing-guard/SKILL.md) | Perform Stripe billing operations such as invoice drafts, refunds and subscription changes. Check account and test/live mode, prevent duplicates, reuse existing authorization, and verify provider receipts. |
| [`sweep-rewriter`](../skills/sweep-rewriter/SKILL.md) | Automate widespread source edits with structural transforms, bounded scope, repeatability, and semantic checks. |
| [`t3-repo-onboard`](../skills/t3-repo-onboard/SKILL.md) | Onboard a repository into T3 development environments with isolated previews, local tests, and project actions. |
| [`tech-doc-writer`](../skills/tech-doc-writer/SKILL.md) | Technical docs, RFCs, README localization, and docs-versus-code checks; preserve source meaning and working links. |
| [`telemetry-signal-forge`](../skills/telemetry-signal-forge/SKILL.md) | Metrics, traces, dashboards, and SLOs; implement telemetry or diagnose a specific monitoring gap. |
| [`test-suite-pruner`](../skills/test-suite-pruner/SKILL.md) | Maintain an oversized or brittle repository test suite while preserving crucial behavior and removing obsolete work. |
| [`throwaway-prototype`](../skills/throwaway-prototype/SKILL.md) | Prototype a state model or competing UI designs in a disposable runnable artifact to answer a specific question. |
| [`ts-type-design`](../skills/ts-type-design/SKILL.md) | TypeScript type design, compiler configuration, and migrations; load framework guidance only for framework-specific work. |
| [`ui-cliche-audit`](../skills/ui-cliche-audit/SKILL.md) | Audit UI originality, scan frontend design patterns with the pinned avoid-ai-design scanner, and review product credibility and missing states; report findings without editing. |
| [`ui-craft`](../skills/ui-craft/SKILL.md) | Implement or refine web interface visuals, responsive layouts, and interaction states within the product design. |
| [`wcag-a11y-audit`](../skills/wcag-a11y-audit/SKILL.md) | Audit or repair web accessibility using keyboard, semantics, contrast, and assistive-technology evidence. |

`omarchy` and `diagnose-crash` are additional OS-owned catalog entries, present
only where their OS owner installs them. They are not authored personal defaults.

## Default shared skills

| Skill | Purpose |
|---|---|
| [`content-recaster`](../shared/content-recaster/SKILL.md) | Adapt existing source content into requested channels. |
| [`launch-dossier`](../shared/launch-dossier/SKILL.md) | Build a source-backed product marketing packet. |
| [`relay-baton`](../shared/relay-baton/SKILL.md) | Record a verified continuation or handoff. |
| [`scope-grill`](../shared/scope-grill/SKILL.md) | Resolve material scope questions; named grill-me and grill-with-docs modes. |
| [`skill-stack-router`](../shared/skill-stack-router/SKILL.md) | Resolve qualified companions and specialists without switching profiles. |
| [`voice-ledger`](../shared/voice-ledger/SKILL.md) | Define a written voice from real brand sources and copy. |

## Subsets groups

The [complete membership catalog](../profiles/CATALOG.md) lists every skill
under each group and identifies overlaps. Counts describe optional members,
not additional personal or shared defaults. The same skill can serve several groups.

| Group | Optional members | Work it covers |
|---|---|---|
| [`core`](../profiles/CATALOG.md#core-3) | 3 | Always active. |
| [`ai-agents`](../profiles/CATALOG.md#ai-agents-25) | 25 | Agent orchestration, client configuration and skill authoring. |
| [`engineering`](../profiles/CATALOG.md#engineering-23) | 23 | Planning, understanding and delivering code changes. |
| [`testing-quality`](../profiles/CATALOG.md#testing-quality-12) | 12 | Review, verification and test work. |
| [`backend-devops`](../profiles/CATALOG.md#backend-devops-8) | 8 | Service code, payments, workflows and infrastructure. |
| [`security`](../profiles/CATALOG.md#security-6) | 6 | Security review, forensics and hardening. |
| [`frontend-mobile`](../profiles/CATALOG.md#frontend-mobile-8) | 8 | Web, mobile, terminal and editor interfaces. |
| [`tooling-homelab`](../profiles/CATALOG.md#tooling-homelab-15) | 15 | Personal tools, homelab services and client setup. |
| [`docs-research`](../profiles/CATALOG.md#docs-research-14) | 14 | Office documents, research and reports. |
| [`learning`](../profiles/CATALOG.md#learning-5) | 5 | Courses, tutoring and practice. |
| [`product-growth`](../profiles/CATALOG.md#product-growth-21) | 21 | Product strategy, marketing and sales. |
| [`creative-media-design`](../profiles/CATALOG.md#creative-media-design-10) | 10 | Images, video, sound, slides and game design. |
| [`writing-nonfiction`](../profiles/CATALOG.md#writing-nonfiction-11) | 11 | Articles, essays, talks and voice. |
| [`writing-worldbuilding`](../profiles/CATALOG.md#writing-worldbuilding-30) | 30 | Fiction craft, worldbuilding and tabletop play. |

## Required and optional relationships

[The relationship catalog](../catalog/skill-routes.json) records 86 conditional
links from 27 skills. Each linked entrypoint has a short companion reference.
Those links cover defaults to specialists, specialists to defaults, and
specialists to other specialists. This is an initial map of reviewed
relationships; unlinked skills keep their existing procedures.

| Example | Relationship | Condition |
|---|---|---|
| `ui-craft` → `behavior-proof` | Required | Before claiming an edited interface works |
| `build-sequencer` → `rn-expo-builder` | Optional | The requested feature targets React Native/Expo |
| `temporal-flow-design` → `temporal-py-tests` | Required | Delivering Python workflows that need replay/determinism proof |
| `story-cowriter` → `outline-to-chapter` | Optional | The writer supplies a complete chapter outline |
| `outline-to-chapter` → `dialogue-doctor` | Optional | A dialogue pass is needed |
| `rival-dossier` → `vs-page-writer` | Optional | The user also requests comparison-page copy |

Required links apply only when their stated condition holds. A plan-only task
does not acquire implementation or deployment work. Optional links are helpers,
not an automatic sequence. Already loaded skills are reused, so cycles between
related tasks do not recursively load more instructions.

The default router returns source paths from the deployed bundle behind
`~/.agents/bin/skill-profile`, with the managed library link as a fallback.
It reads qualification, ownership, group membership, and client support.
The agent then reads the chosen skill and its needed references. This does
not register a slash command, add tools, copy skills, or change a profile.

If a required companion is unavailable, the dependent outcome remains blocked
or unverified. Independent work can continue. Explicit-only skills still need
an explicit request, and a relationship never authorizes delegation, external
publication, or a broader editing scope.

## The design skill integration

[`avoid-ai-design`](https://github.com/funboy322/avoid-ai-design) v0.4.0 is integrated
into the existing default owners at pinned commit
`2b7c71836b06cdf6b3d73265b56490c1b75ad5aa`:

- `ui-cliche-audit` owns the scanner, pattern catalog, and read-only review.
- `ui-craft` uses the same procedure during authorized UI implementation.
- The scanner is optional Node 18+ tooling; a manual review is available.
- The original MIT notice and file hashes are retained. No hook or global CI gate is installed.

Examples: “Audit this page for generic design patterns; report only” selects
the audit owner. “Refine this page using our existing brand rules” selects
the implementation owner and its conditional companions. No Subsets switch
is needed for either. Scanner findings are heuristics to check in context;
a clean scan does not prove usability, accessibility, or design quality.

## Selection and client limits

The switching commands are in [the profile guide](../profiles/README.md).
An explicit switch is useful when you want a whole group directly discoverable
for a sustained session, when the current client cannot read library files,
or when moving to a different client/tool environment. New discovery requires
a fresh session. Existing conversations retain their initial skill metadata.

Profile selection cannot grant missing browser/device access, install a runtime,
transfer authentication, or qualify an unsupported client. System and plugin
artifact owners remain preferred where the current client provides them.
The 48-skill public `@subcult/patstack` pack is a separate export; this private
default stack and the Subsets `core` group are different selections.
