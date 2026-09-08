---
name: blacktower-development
description: Blacktower plugin, session lifecycle, control UI, and release changes; use only in the Blacktower repository.
---

# blacktower-development

Apply only inside Blacktower. Select control UI, plugin composition, release artifacts, or session lifecycle. OpenCode references here describe the software under development, not tools that Codex must have.

## Select a mode

- Design and review Blacktower control surfaces, including TUI sidebar, OpenTUI dashboard, control-center web UI, status boards, terminal UX, accessibility, state displays, and operator-facing. Read [the procedure](references/modes/control-surface-designer/guide.md).
- Safely change Blacktower/OpenCode plugin integration points. Read [the procedure](references/modes/plugin-integrator/guide.md).
- Prepare and verify Blacktower builds, package artifacts, installers, generated schemas, bundled skills, migrations, and release notes. Read [the procedure](references/modes/release-engineer/guide.md).
- Diagnose and change Blacktower delegated-session lifecycle behavior. Read [the procedure](references/modes/session-warden/guide.md).

Resource paths inside a mode are relative to that mode directory. Run its scripts from that directory or use absolute script paths, passing the target repository explicitly.
