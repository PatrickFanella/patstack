---
name: skill-stack-router
description: Use when a task needs skills beyond the active list, or a procedure has required or optional companion skills. Route through default owners and load qualified specialists on demand; keep the current Subsets selection unless a different working stack is requested.
---

# Route skills without switching stacks

Default skills are the entry points. Load only the specialist instructions
needed for the current task; reading a library skill does not activate a
Subsets group, register tools, or install dependencies.

## Choose the procedure

1. Match the task to the current client's available skills first. Prefer its
   system/plugin owner for supported artifacts or services, then the relevant
   personal, shared, or project-local owner. Do not replace those owners with
   an optional duplicate. Respect the current repository's instructions.
2. For related work, consult the selected skill's `references/skill-routes.md`
   when present. Resolve its companions with:

   ```sh
   python3 <skill-root>/scripts/lookup.py --from ui-craft --client codex
   ```

   `<skill-root>` is this loaded router's directory; `--client` is the current
   client (`codex`, `claude`, `opencode`, `copilot`, or `cursor`). Cursor and
   Copilot use the configured Claude-compatible file contract, not assumed
   tool or provider equivalence.
3. For a task outside the active defaults, select a task stack from
   [the group map](references/groups.md), then list or resolve specialists:

   ```sh
   python3 <skill-root>/scripts/lookup.py --group mobile-and-interfaces --client codex
   python3 <skill-root>/scripts/lookup.py --skill rn-expo-builder --client codex
   ```

4. Open the returned `SKILL.md` and only its applicable references. Resolve
   their resources relative to that skill's returned directory. Check its
   invocation restrictions and actual tools before following it. An
   explicit-only skill requires an explicit user request, not a router match.

## Follow relationships deliberately

- **Required** means required when the edge's stated condition applies. Load
  it before claiming that part of the outcome; it does not authorize extra
  work. If it is unavailable, report the dependent step as blocked or
  unverified and continue independent work.
- **Optional** means a helper for the stated condition. Load it only when it
  adds something the current procedure needs. It must not widen an audit to
  edits, an implementation to deployment, or a draft to publication.
- Keep a set of already loaded skills for this task. Reuse them rather than
  following cycles or recursively opening every related skill. Do not load
  whole categories, spawn agents, or execute scripts just because an edge
  mentions them. Current authorization and delegation limits still apply.

The lookup is read-only. It uses the source behind the installed Subsets
selector, with the managed library link as a fallback; `--source` is for an
explicit reviewed checkout or a test fixture. It rejects archived, blocked,
unreviewed, retired, duplicate, local-only and unsupported optional routes.
Qualification describes the source contract, not proof of live tool access.

Stay on the current selection for a one-off specialist task. Switch stacks
only when the user requests a persistent set of directly discoverable skills,
the client cannot read the source library, or the work needs a different
client/tool environment. A profile switch alone cannot provide missing tools.
