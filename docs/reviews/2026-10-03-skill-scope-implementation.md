# Approved skill scope implementation

The user approved retiring llama-line-client and integrating useful procedures from obsidian-vault, use-my-browser, stripe and wait-what. This release also completes the reviewed consolidations of grilling, handoff and show-me-your-work. Original library folders remain preserved; retired entrypoints are excluded from optional profile activation rather than aliased.

| Previous entrypoint | Current owner |
|---|---|
| llama-line-client | Retired; original preserved for recovery |
| obsidian-vault | Four vault root instructions and shared note-discovery reference |
| use-my-browser | verify-behavior browser-diagnosis reference |
| stripe | stripe-billing-operations personal overlay; managed Stripe plugin retains API and development guidance |
| wait-what | unslop re-explanation mode |
| grilling | requirements-interview |
| handoff | session-handoff |
| show-me-your-work | implementation-plan decision-trail reference |

Optional activation now excludes twelve vault-owned names and Edda’s play-edda in addition to curated and retired names. Eligible reservoir entries fall from 183 to 165. The active core profile remains five skills. Broader project and area moves in the review remain proposals.

The combined personal description cap of 8,000 characters is repository policy in scripts/validate.py, not a connected-app requirement. This release uses 7,995 characters. OS, system and plugin-owned skills retain their owners.

Validation passed: repository structure validation, all 21 unit tests, skill-creator checks for the four changed entrypoints, and git diff whitespace checks. An independent offline forward trial exercised four Stripe/browser cases; its report is linked below. It made no external requests and does not establish live payment or browser behavior. Two suggested clarifications about correlation metadata and unresolved refunds were incorporated.

Deployment scope: three personal owners (unslop, verify-behavior, stripe-billing-operations), one shared owner (session-handoff), four vault root instructions and four note references, plus one Claude skill link. The installer selectors preserve unrelated destination drift. Existing dirty OPERATING-MODEL.md, patreon-manager source and runtime-bundles work are outside this release.

Scoped deployment commands:

```sh
rtk proxy python -B scripts/install.py plan --only-skill unslop --only-skill verify-behavior --only-skill stripe-billing-operations --only-shared session-handoff
rtk proxy python -B scripts/install.py apply --only-skill unslop --only-skill verify-behavior --only-skill stripe-billing-operations --only-shared session-handoff
rtk proxy python -B scripts/install.py verify --only-skill unslop --only-skill verify-behavior --only-skill stripe-billing-operations --only-shared session-handoff
rtk proxy python -B scripts/vault-agents.py plan
rtk proxy python -B scripts/vault-agents.py apply
rtk proxy python -B scripts/vault-agents.py verify
rtk proxy python -B scripts/link-workstation.py plan --only-link /home/onnwee/.claude/skills/stripe-billing-operations
rtk proxy python -B scripts/link-workstation.py apply --only-link /home/onnwee/.claude/skills/stripe-billing-operations
rtk proxy python -B scripts/link-workstation.py verify --only-link /home/onnwee/.claude/skills/stripe-billing-operations
```

Personal/shared installation and Claude source links retain transaction journals, verified before-state backups and guarded rollback via the respective script with `rollback --run PATH`. Vault deployment records before-state backups under `~/.local/state/vault-agent-deployments/`; restoration must preserve later edits. The four vault baseline reconciliations are documented separately and were accepted only after deployed bytes matched the committed pre-change source.

Fresh local discovery must show the new Stripe owner, no retired entrypoints, and vault/Edda owners only in their local scopes. Existing conversations retain their initial skill catalog; these checks do not establish fleet parity or hot reload.

[Offline forward trial](2026-10-03-stripe-browser-forward-test.md)
