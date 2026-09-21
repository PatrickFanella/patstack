---
type: reference
status: active
created: '2026-06-04'
updated: 2026-06-11
tags:
- systems/agent-skills
- workflows
title: Workflow Map
---

# Workflow Map

## Routing

- Journal → `003 Resources/Periodic Notes/`
- Resource → `003 Resources/Media/<medium>/`
- Thread → `001 Projects/Threads/`
- Work → `001 Projects/Works/<type>/` (Blog Posts, Social Posts, Software, Essays, Videos, Zines, Music, Releases, Documentation)
- Documentation → `003 Resources/Documentation/` or `003 Resources/Systems/`

## Capture fields

- Journal: none or very little.
- Resource: title, medium, source URL, threads when relevant.
- Thread: title, core question, related sources/works.
- Work: title, publish target, optional `goal-publish-date`, `soft-due-date`, `hard-due-date`.
- Documentation: title and function (`Guide`, `Runbook`, `Decision`, `Reference`, `Plan`, `Roadmap`).

## Automation

- Templater auto-applies correct template for 22 folder mappings.
- QuickAdd provides 30 capture choices for all note types.
- Kanban boards track publishing pipelines: SubBlog (Ideas→Drafting→Review→Scheduled→Published), Social (Planned→Writing→Scheduled→Posted), Software (Idea→Planning→Building→Testing→Released).

## Defaults

- Capture first.
- Route immediately.
- Add structure only after the note exists.
- Tags use canonical hierarchy: `type/*`, `domain/*`, `status/*`, `project/*`.
