# Investigation details

## Code anchor

Before spawning investigators, collect relevant file paths and line ranges, key symbols, recent commits touching the target, PR numbers from merge subjects, and linked ticket IDs. Use:

```bash
git blame -L <start>,<end> <file>
git log --follow -p -- <file>
git log --oneline -20 -- <file>
git log -1 --format=%B <commit>
gh pr view <number> --json title,body,author,createdAt,mergedAt,labels,closingIssuesReferences,comments,reviews
```

Pass this seed context to every investigator so they do not rediscover it.

## Coverage roster

Discover MCPs from the available-tools map or the Cursor `mcps/` directory. Map each to one primary category; record ambiguous mappings in the coverage map. Launch all matching investigators in one message, one agent per category:

1. **Source control** (git, `gh`, comments, tests): implementation-time rationale in PR descriptions, review discussions, tests, commits, and comments. Always spawn.
2. **Issue/ticket tracker** (Linear, Jira, GitHub Issues, Plane, Shortcut): product/business forcing functions, customer or compliance needs, scope changes, and initiatives.
3. **Long-form documents** (Notion, Confluence, Google Docs, Coda): PRDs, RFCs, ADRs, specs, notes, and postmortems.
4. **Real-time team chat** (Slack, Discord, Teams, Mattermost): deliberation, incident decisions, and rationale not recorded elsewhere.
5. **Infrastructure observability** (Datadog, New Relic, Honeycomb, Grafana, Splunk): monitors, metrics, logs, traces, incidents, and runtime signals behind constants or defenses.
6. **Error/exception tracking** (Sentry, Rollbar, Bugsnag, Airbrake): error trajectories, stack traces, release correlations, and defensive-code motivation.
7. **Product analytics warehouse** (Databricks, Snowflake, BigQuery, ClickHouse, dbt, Redshift): usage, flags, experiments, distributions behind thresholds, migrations, and data scale.

Use `subagent_type: generalPurpose`, the configured investigator model (default `grok-4.6-fast-xhigh`), and `readonly: false`. This is agent mode for MCP access, not permission to write. Add `sources/incident-postmortem.md` when the target is defensive (null checks, retries, timeouts, rate limits, feature flags, egress guards, OOM handling).

## Skips and synthesis

Skip only if no matching MCP is available (name it as a gap) or the source is provably irrelevant. “Probably irrelevant” is not enough. The rare inline answer is permitted only after confirming that all seven available category searches would be redundant.

Spawn one `generalPurpose` synthesizer using the configured model (default `claude-fable-5-thinking-max`) and `readonly: false`. Provide investigator findings including nulls/skips, code anchor, original question, `epistemics.md`, and `synthesizer-prompt.md`. It returns the final confidence-weighted, evidence-cited narrative; do not rewrite its confidence language.

## Output conventions

Use the sections listed in SKILL.md. Direct evidence has precise citations (commit hash, PR, ticket, URL, chat permalink, or file:line). Inferences state their evidence chain and use hedged language. Contradictions remain visible. Sources Consulted has one line per investigator:

```text
- <Source>: <what was searched>. <what was found, or "no relevant results," or "skipped. reason">.
```

For example: `- Real-time team chat (Slack): skipped. No matching MCP available in this environment. Gap: conversational record not searched.`

Avoid confident storytelling, treating code as proof of its own intent, recency bias, agreeing with the user's hypothesis without checking, omitting gaps, anticipatory skips, and collapsing investigators into one agent.
