# Offline forward test: new skill adaptations

Scope: simulation from the supplied local instructions and fixtures only. No
provider, browser, service, repository, or messaging action was performed.

## A. Almaz GPU service failure

### Next action

Collect current Almaz evidence before changing anything: the current OS, kernel
and GPU driver; PCI device presence; the accelerator tool's result; container
runtime access to the device; and one representative GPU workload. Trace the
affected service through its effective configuration, runtime, transport,
authentication/policy, persistence and visible behavior. Time- and
host-stamp each observation. Do not restart the service, change the kernel, or
pin/downgrade a kernel from the historical note.

### What can be concluded

The fixture establishes that the PCI probe is absent at its observation time.
This is consistent with the GPU not being available to the host, but does not by
itself identify whether the cause is hardware, firmware, kernel, driver,
power, virtualization or probe configuration. The passing application health
endpoint establishes only its exposed health behavior; it does not prove a
representative GPU-backed workload works. The host serving DNS is independent
evidence that an unrelated host service is available. Kernel `7.0.0-15` was
historically known good, not a current repair recommendation or a basis for a
kernel change.

### Assessment and pointers

The adaptation gives a safe diagnostic branch and prevents an unsupported
kernel rollback. Its main remaining ambiguity is the phrase “GPU service”: the
fixture omits the specific service, accelerator vendor/tool and whether the PCI
probe runs on host or in a guest. The correct next step stays evidence
collection rather than an inferred repair.

Pointers: `vault-agents/Operations/skills/operations-vault/references/operational-evidence.md`,
GPU/post-upgrade branch (current OS/kernel/driver, PCI presence, accelerator,
container runtime and workload; historical kernel is not a universal pin);
the health/incident branch (health endpoint is insufficient for representative
behavior).

## B. Left Field supporter-copy preparation

### Draft

Support SUBCULT, the studio behind Left Field.

### Next actions

Keep this as a local prepared draft. Do not promise weekly field notes, a fixed
cadence, private Discord access, Patreon membership benefits, tier prices, or a
live destination: the fixture lacks current provider/access evidence. If a
future approved design asset accompanies this copy, use the Left Field field
ledger direction—paper `#f4f0e6`, dark ink `#16221f`, rust `#a33c26`—rather than
the retired universal-dark instruction. Before activation, inspect the actual
Patreon offer, existing member state, Discord access, and the branded Support
destination; verify that the central Support page accurately describes the
offer; then obtain the required publication authority and provider readback.

### Assessment and pointers

The exact safe draft is intentionally narrower than the reviewed proposed
support policy. It identifies the studio and product without asserting an
unverified benefit or destination. It respects the reviewed no-fixed-schedule
direction and supersedes the historical weekly field-note promise for new copy.

The skill asks for a Product Claims Register and relevant editorial source, but
the fixture provides no checked product claim beyond the product name. That
prevents a richer value proposition; it does not prevent the short safe draft.
There is no instruction to invent a Patreon URL or to publish, so the missing
live evidence is handled safely.

Pointers: `project-agents/subcult-studio/skills/studio-preparation/SKILL.md`,
supporter-work paragraph (historical fixed promises; no scheduled rewards;
reviewed source); `references/source-routing.md`, supporter-offer entry
(reviewed worktree and no-schedule direction);
`branding/2026-10-01-packs/brands/left-field/GUIDE.md`, opening direction and
color roles; and
`.t3/worktrees/subcult-studio/t3code-96db3bb2/content/patreon/support-redesign-2026-10/site-guidelines.md`,
“Safe copy before reward activation.”

## C. Requested activation of check-agent-compatibility

### User response

I can’t activate `check-agent-compatibility` or report a compatibility score in
this Codex runtime. Its qualification record is blocked: the required
compatibility-scan, startup, validation, and docs-reliability agents, plus the
declared deterministic scanner, are unavailable. The workflow requires those
tools and says to stop rather than invent a score or substitute other agents.

### Assessment and pointers

This is the required near-miss response. No score can be computed because both
the deterministic component and all behavioral review inputs are absent. The
maintenance skill correctly routes the decision to the canonical qualification
record instead of treating the skill's YAML or an ordinary review as proof of
operational support.

The request omits the repository to evaluate, but that is secondary: the
missing runtime contract blocks activation before repository inspection. No
harmful fallback is suggested.

Pointers: `project-agents/codex-skills/skills/codex-skills-maintenance/SKILL.md`,
qualification-record and unsupported-contract directions;
`catalog/qualification.json:445-464` (blocked status, no supported clients,
five required components, positive task, near miss and blocked reason); and
`library/skills/check-agent-compatibility/SKILL.md:9` (report missing runtime
requirements and stop; do not invent scores or substitute agents).

## Overall finding

All three adaptations constrain action to the evidence available. The
operations adaptation keeps historical host notes from becoming repair
commands; Studio routing prevents obsolete cadence promises and unverified
membership claims; and the maintenance qualification record prevents a made-up
compatibility score. The ambiguities identified above are missing fixture
details, not instructions that invite unsafe behavior.
