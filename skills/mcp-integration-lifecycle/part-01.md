# MCP Integration Lifecycle

Treat an MCP integration as a pipeline:

`config source → transport → initialize → catalog → policy/auth → reload → operation`

Find the first failing boundary. Do not compensate in a later boundary with
longer timeouts, duplicate server entries, broader approvals, or unrelated
credentials.
