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
