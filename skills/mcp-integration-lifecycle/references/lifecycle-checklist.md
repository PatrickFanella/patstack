# MCP Lifecycle Checklist

Use this reference for transport details after the core workflow identifies the
likely failing boundary.

## Configuration source

- Identify the exact client instance, profile, workspace, and host.
- Resolve every global, workspace, plugin-managed, and generated server entry.
- Compare the client's effective listing with the file believed to be active.
- Check duplicate server IDs only after deciding which entry is canonical.
- Record executable/URL identity and version before changing configuration.

## Stdio

- Use an absolute executable when client `PATH` may differ from the shell.
- Match arguments, working directory, and required environment exactly.
- Require protocol JSON on stdout; route diagnostics to stderr.
- Run `scripts/probe_stdio_mcp.py` before changing the client.
- If the probe succeeds but the client hangs, compare protocol version,
  startup timeout, environment inheritance, stale child processes, and the
  client's first logged JSON-RPC event.

## Streamable HTTP

- Verify the configured URL after redirects; do not assume `/mcp`.
- Check DNS/TLS, HTTP status, `Content-Type`, and MCP protocol/session headers.
- Confirm whether the endpoint accepts `POST`, `GET`, or both according to the
  server's supported transport version.
- Use nonmutating initialization/catalog requests for protocol testing.
- Keep session IDs scoped to the initialized session. Do not replay another
  client's session ID.
- Distinguish reverse-proxy/auth redirects and HTML error pages from MCP JSON.

## Initialize and catalog

- Require matching JSON-RPC IDs and a supported negotiated protocol version.
- Send `notifications/initialized` only after successful `initialize`.
- Compare tool, resource, and prompt names plus descriptions, schemas, and
  capabilities with the canonical catalog or a known-good client.
- Treat unknown methods, missing entries, and schema differences as catalog or
  version drift, not transport health.

## Approval modes

- Read the affected client's supported mode names and semantics before editing.
- Check global defaults, per-server policy, and per-tool overrides.
- Confirm that discovery and initialization do not require write approval.
- Test a known read-only operation first. Leave write, destructive, send,
  purchase, and access-control actions gated as intended.

## OAuth

- Determine whether the server expects OAuth, a static bearer token, or another
  credential; do not mix the flows.
- For OAuth, verify protected-resource metadata, authorization-server metadata,
  client registration, redirect URI, state/PKCE, scopes, token audience,
  refresh, secure storage, and revocation through the client's supported flow.
- Never copy tokens between clients or expose them in commands, logs, or config.
- Treat `401` as an authentication challenge and `403` as an authenticated
  authorization/scope decision, subject to the server's documented behavior.

## Reload and smallest-fix verification

1. Change only the first failed boundary.
2. Parse/validate the edited config without displaying secrets.
3. Use the documented reload, reconnect, or restart path for the affected
   client; do not assume hot reload.
4. Re-run the independent transport/initialize/catalog checks.
5. Confirm the effective client entry and reconnect state.
6. Run one nonmutating end-to-end operation.
7. Report skipped checks and avoid declaring full recovery from process
   existence or catalog discovery alone.
