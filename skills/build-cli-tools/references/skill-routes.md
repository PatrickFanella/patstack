# Companion procedures

Load a companion only under its stated condition. Current authorization and client-native tool contracts remain authoritative. Read the source once; avoid cycles and do not switch the active profile for a one-off reference.

| Skill | Relationship | When to load it |
|---|---|---|
| `verify-implementation` | optional | When the real CLI must be driven through its flags and exit codes before claiming it works. |
| `bash-scripts` | optional | When the tool ships installer, wrapper or completion scripts. |
| `build-opentui-apps` | optional | When the tool needs a full-screen OpenTUI interface. |
| `golang` | optional | When implementing the CLI in Go. |
| `rust` | optional | When implementing the CLI in Rust. |
| `typescript` | optional | When implementing the CLI in TypeScript. |
| `python-projects` | optional | When implementing an internal automation CLI in Python. |
