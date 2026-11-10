---
name: manage-roadmaps-and-issues
description: Create and maintain roadmaps and tracker issues, triage reports, or configure
  repository contribution workflows.
---

# manage-roadmaps-and-issues

Choose intake, triage, setup, roadmap publication or maintainer guidance from the request. Filing a bug does not authorize fixing it. Read back authorized tracker writes.

Select the matching procedure below and load only that procedure and its needed resources. Each procedure retains its own client, tool and invocation limits. Internal handoffs use the matching procedure below rather than reloading this entrypoint. A reference does not authorize delegation, publication, deployment or an unrelated mutation.

- **publish a roadmap**: Use when a finished plan, spec or design doc should become Gitea issues: a Roadmap tracking issue listing work in dependency order, optional Epics, and one issue per mergeable PR, wired with native blocking dependencies. Also to extend or refresh such a roadmap. Read [the procedure](references/base-workflow.md).
- **tracer ticket split**: Tickets from a plan: split a plan, spec or conversation into tracer-bullet tickets with blocking edges, published to the configured tracker (Gitea, GitHub, Linear or local files). Read [the procedure](references/modes/tracer-ticket-split/guide.md).
- **tracker bootstrap**: Set up a repo for Matt Pocock's engineering skills: issue tracker (Gitea, GitHub, GitLab or local), triage labels, CONTEXT.md/ADR layout. Run once before tracer-ticket-split, issue-state-triage or the prd-from-context mode of define-requirements. Read [the procedure](references/modes/tracker-bootstrap/guide.md).
- **issue state triage**: Issue triage: move incoming bugs and feature requests through needs-triage, needs-info and ready-for-agent states, write agent briefs, or show what needs attention on the tracker. Read [the procedure](references/modes/issue-state-triage/guide.md).
- **bug intake session**: Use when the user wants a QA session: they report bugs conversationally and you file durable, user-focused issues on the repo's Gitea or GitHub tracker. Read [the procedure](references/modes/bug-intake-session/guide.md).
- **oss maintainer coach**: Open source project guidance from opensource.guide: starting, contributing, onboarding, governance, codes of conduct, funding, security, metrics, legal basics, maintainer burnout. Read [the procedure](references/modes/oss-maintainer-coach/guide.md).

Read [conditional companions](references/skill-routes.md) only when their stated condition applies.
