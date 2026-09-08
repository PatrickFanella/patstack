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
