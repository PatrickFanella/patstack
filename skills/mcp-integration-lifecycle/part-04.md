## Approval and Authorization Boundaries

- Classify methods from their actual behavior and schema, not their names.
- Keep read-only, write, destructive, external-send, purchase, and access-control
  actions distinguishable in policy.
- Treat approval prompts as client policy; treat authorization failures as
  identity/token scope; treat missing tools as catalog or capability drift.
- Use only approval-mode values supported by the affected client. Confirm their
  semantics from current client configuration or documentation before editing.
- Preserve OAuth discovery, PKCE/state, redirect handling, token storage,
  refresh, and revocation inside the client's supported OAuth flow.
- A bearer token supplied by an environment variable is static credential
  configuration, not proof that OAuth works.
