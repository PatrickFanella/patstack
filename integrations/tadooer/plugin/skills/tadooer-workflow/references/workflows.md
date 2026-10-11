# Workflow details

Use the live schema for argument wrappers and scope requirements. This is a
selection guide, not a replacement tool catalog.

- Tasks: `suite.tasks.list`, `create`, `update`, `set_completed`, `deleted` and
  `restore`. Read revisions. A deletion preview may include children.
- Projects/tags: `suite.projects.list`, `suite.tags.list` and their advertised
  mutation tools. A complete tag replacement must retain tags outside the
  user's requested change.
- Hierarchy and checklist items are different entities. Use
  `suite.tasks.hierarchy` for child tasks and `suite.subtasks.list`/`mutate` for
  checklist items. Reorders need the complete current set and revisions.
- History/recurrence: discover `suite.tasks.history`, archive/unarchive and
  `suite.recurrence.*`. Preserve imported provenance. Ending a series and
  deleting an occurrence have different effects.
- Time: `suite.time.report` uses calendar dates in the owner's planning zone;
  edits use `suite.time_entries.mutate` and current revisions. Focus-generated
  entries and time on archived tasks may be read-only.
- Planning: inspect `suite.planning.day_plan`, preferences, `suite.day_order.*`
  and `suite.schedule.*`. Moving/removing a Baikal time block affects a real
  calendar resource. Google Calendar integration is separate from Suite sync.
- Focus: inspect `suite.active_session.get` and use only advertised lifecycle
  commands. Another device may be the controller; takeover is consequential.
- Templates, sets, pools and habits: inspect current records and the preview's
  exact number of tasks before confirming instantiation or mutations.
- Preferences: use the read revision and preserve the complete intended
  preferences. Reminder enabling affects scheduled delivery. A notification
  test needs the dedicated test scope and an explicit user request; queued or
  delivered receipts do not prove the user saw a message.

For detailed capability mapping consult the Tadooer repository's
`docs/product/assistant-capabilities.md` and its generated JSON inventory. Some
features may exist in the application without corresponding MCP tools. The
live catalog is the authority for availability.
