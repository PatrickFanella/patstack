# Design intake and skill relationships, November 4, 2026

The owner requested `funboy322/avoid-ai-design` as a default capability, a guide
to Subsets groups, and conditional references between default and optional
skills so ordinary specialist work does not require a profile switch.

## Design intake

The MIT-licensed v0.4.0 source is pinned at
`2b7c71836b06cdf6b3d73265b56490c1b75ad5aa`. Original entrypoint, references,
scanner, tests, and license are archived under
`authoring/upstream/avoid-ai-design/2b7c71836b06cdf6b3d73265b56490c1b75ad5aa/`,
outside discovery. The intake ledger records upstream paths, SHA-256 hashes,
archive paths, and installed resource paths.

`ui-cliche-audit` retains its read-only role and owns the imported scanner and
catalog. `ui-craft` uses an adapted workflow during authorized visual work.
This keeps the default ownership model while adding the requested capability.
No new alias, rewrite-by-default entrypoint, hook, dependency installation,
or mandatory scanner CI gate is introduced. The optional upstream DESIGN.md
CLI examples are retained as reference, not executed or qualified tooling.

Scanner output is advisory. Matches can describe deliberate choices, missing
paths can be skipped silently, rule errors can be swallowed, and a zero exit
status does not establish coverage or rendered quality. Browser and device
checks must follow the active client's tool contract.

## Relationship model

`skill-stack-router` is a sixth shared default. Its standard-library lookup
reads the deployed source's ownership catalogs, qualification, profiles, and
`catalog/skill-routes.json`. It returns paths and restrictions without copying
skills or changing a selection. Personal owners absent from a Subsets bundle
resolve to their existing personal installation. Optional sources must remain
inside the reviewed source root and belong to an activatable group.

The initial graph has 86 conditional edges from 27 entrypoints. Each source
links a small companion reference, including optional-to-optional paths.
Required edges apply only under their condition; optional edges do not widen
the task. Explicit invocation limits, client support, current tools, scope,
and delegation authorization remain authoritative. Already loaded procedures
are reused so bidirectional task links do not recursively load the graph.

## Acceptance cases and proof boundary

| Case | Expected result | Evidence |
|---|---|---|
| Stock React/Tailwind page with gradient text and repeated icon cards | Scanner reports IDs/locations and exits 2 | Retained upstream scanner suite |
| Deliberate page, data-table percentages, route arrow, documented ignores | No corresponding false positives; ignores remain narrow | Retained upstream scanner suite |
| Audit-only request | Read-only owner; no automatic rewrite or DESIGN.md | Adapted entrypoint/workflow inspection; no fresh-model trial |
| Approved font/color choice | Review in context, preserve the system | Adapted workflow inspection and ignore fixtures |
| React Native task while core remains selected | Resolve `rn-expo-builder` and its companions without switching | Router fixture and live read-only lookup |
| `story-cowriter` needs a chapter specialist | Resolve optional `outline-to-chapter` directly | Router fixture |
| Explicit-only spec implementation | Return its explicit-only flag; require a user request before use | Router fixture and source inspection |
| Blocked, archived, retired, local, unsupported or escaping route | Refuse it or report an unavailable companion | Router fixtures |
| Required companion unavailable on current client | Keep the edge's condition and unavailability visible | Router fixture |

Local validation, scanner behavior, relationship integrity, and installation
hash checks establish only their named properties. They do not establish
independent model routing quality, visual/browser outcomes, fleet parity,
remote CI, publication, or tool connectivity. Deployment transactions and
discovery captures are the authority for the actual host installation.

Source validation and all 80 Python tests passed locally. The Python suite ran
the retained 11-case Node scanner suite with an explicit TAP reporter. Routing
fixtures cover cross-group lookup, explicit-only metadata, unavailable required
companions, rejection cases, source-path escape, and unchanged selection state.
The defaults guide was compared with all 52 authored personal skills, six shared
skills, and every member of all 14 canonical profiles.
