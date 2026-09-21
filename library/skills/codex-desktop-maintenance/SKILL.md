---
name: codex-desktop-maintenance
description: Audit and safely diagnose the personal Codex Desktop installation on Arch Linux with Omarchy. Use after a desktop or package update, when Codex cannot launch or update, when the CLI wrapper or update-manager service seems unhealthy, or before proposing a repair to the Linux-specific Codex setup.
---

# Codex Desktop Maintenance

Diagnose the installed desktop setup without altering it. This skill owns the
Arch/Omarchy health workflow; it does not replace Codex with npm, modify the
pacman-owned runtime, or repair a different machine by assumption.

## Workflow

1. Confirm the target is this workstation and state whether the request is an
   audit or an explicitly authorized repair.
2. Run `scripts/collect_health.py --format markdown`. It uses metadata reads,
   `pacman -Q`, and user-level `systemctl` queries only; it never writes files,
   invokes package changes, or starts/stops services.
3. Interpret the result against the expected layout: the desktop runtime is
   `/opt/codex-desktop`, `codex-update-manager.service` is user-managed, and
   `~/.local/bin/codex` is the Omarchy-managed launcher.
4. For a config issue, run the current workspace's `.codex/validate` if it is
   present and executable. Report parse or loading errors separately from
   desktop-package health.
5. Read [Arch and Omarchy recovery boundaries](references/arch-omarchy-recovery.md)
   only when an abnormal result needs triage or the user asks for a repair.
6. Propose the smallest owner-correct action. Require explicit authorization
   before any change, then re-run the same read-only collection and report the
   before/after evidence.

## Interpretation rules

- A `codex doctor` npm-update warning alone is not a broken installation on
  this machine; do not replace the launcher just to silence it.
- Keep local, SSH, container, and deployed targets separate. This collector
  describes only the local desktop workstation.
- Do not expose tokens or raw configuration values. Report configuration parse
  status and component names only.
- If the collector cannot query `pacman` or the user service manager, report
  the limitation rather than guessing.

## Completion

Finish an audit with the observed runtime, launcher, updater-service, package,
and configuration status, plus any safe next step. Finish a repair only after
an explicit user-approved change and a fresh successful health collection.
