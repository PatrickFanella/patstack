# Context management

Read this reference when a task spans sessions or context pressure risks losing decisions. Use the active runtime’s context indicator where available; model limits and tool names vary by host. Do not infer measured token usage from text length.

Keep durable state in the repository’s established handoff location. Record the objective, user constraints, completed changes, exact verification evidence, unresolved decisions, and the next executable step. Link detailed artifacts instead of copying them. Before resuming, inspect current branch, dirty work, and referenced files because saved state can be stale.

Use available session-resume or compaction facilities only when supported by the current runtime. Save material decisions before a transition. A new session should read the handoff and inspect current state, rather than replaying the entire prior conversation. Do not assume Claude-specific commands, a fixed context size, or a particular history directory.

Keep repository instructions focused on project identity, launch/check commands, non-obvious constraints, and links to conditional procedures. General coding advice belongs in neither every entrypoint nor every handoff.

When asked to analyze past sessions, discover the runtime’s actual read-only history tools and locations. Inspect only the relevant records, preserve credentials, and distinguish recorded evidence from current verification.
