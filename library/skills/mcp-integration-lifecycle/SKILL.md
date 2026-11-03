---
name: mcp-wire-tracer
description: "MCP client integration: register stdio or HTTP servers; diagnose launch or initialize failures, missing tools, OAuth or approval config, cross-client differences and reloads. Not for writing a server."
---

# MCP Integration Lifecycle

Treat an MCP integration as a pipeline:

`config source → transport → initialize → catalog → policy/auth → reload → operation`

Find the first failing boundary. Do not compensate in a later boundary with
longer timeouts, duplicate server entries, broader approvals, or unrelated
credentials.

## Workflow

1. Capture the failing client, exact operation, error, server ID, and transport.
2. Resolve the authoritative configuration source the client actually reads.
   Distinguish global, workspace, plugin-managed, and generated configuration.
   Inspect the client's effective server listing when available.
3. Record the effective command, arguments, working directory, environment, and
   executable identity for stdio; record the final URL, headers, redirects, and
   auth mechanism for HTTP. Redact secrets in all output.
4. Verify transport without invoking application tools:
   - For stdio, run `scripts/probe_stdio_mcp.py` against the exact configured
     command and environment.
   - For HTTP, inspect status, redirects, content type, and MCP session/version
     headers using nonmutating requests. Read
     `references/lifecycle-checklist.md` before probing HTTP or OAuth.
5. Require a valid `initialize` response, send `notifications/initialized`,
   then verify the advertised `tools/list`, `resources/list`, and
   `prompts/list` capabilities. Compare names and schemas with the server's
   source of truth or the working client; do not rely only on counts.
6. Inspect the client's tool approval policy separately from server health.
   Preserve existing policy unless the user requests a change. Never broaden
   approval merely to make discovery or initialization succeed.
7. Treat OAuth as an HTTP authorization lifecycle owned by the client and
   authorization server. Do not place OAuth tokens in stdio environment
   variables, config files, logs, probe arguments, or hand-written headers.
8. Apply the smallest change at the first failed boundary. Avoid changing
   server code when the exact server passes independently.
9. Use the client's documented reload/reconnect path. A configuration edit is
   not active until the client has re-read it.
10. Re-run the independent probe, inspect the effective client listing, reconnect
    the affected client, and perform one nonmutating tool/resource call when
    application-level verification is required.

## Stdio Probe

Run the bundled probe without a shell:

```bash
python3 scripts/probe_stdio_mcp.py \
  --env MCP_DATA_DIR=/absolute/path \
  --expect-tool example_read \
  -- /absolute/path/to/server --flag value
```

The probe launches only its own child, sends `initialize`, and lists each
catalog capability the server advertises. It prints a stable JSON summary and
terminates that child without calling advertised tools, resources, or prompts.
Use `--show-stderr` only after checking that server logs cannot contain secrets.

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

## Completion Contract

Report the first failed boundary, evidence, exact change, and checks rerun. Do
not claim recovery until:

- the intended configuration source and effective server entry agree;
- transport and `initialize` succeed;
- expected tools, resources, prompts, and their schemas are present;
- approval and OAuth behavior match the intended boundary;
- the affected client reloads and reconnects; and
- one safe end-to-end operation succeeds when the server depends on a live
  application or remote service.

Mark every unavailable or skipped check as unverified.
