---
name: codex-desktop-maintenance
description: "Codex Desktop on Sputnik: audit the Arch/Omarchy openai-codex-desktop install after an update, or when the desktop app or codex launcher fails, before proposing any repair."
---

# Codex Desktop Maintenance

Diagnose the installed desktop setup without altering it. This skill owns the
Arch/Omarchy health workflow on Sputnik, the only fleet host with Codex Desktop
(Kvant moved to Debian on 2026-11-03 and no longer has it). It does not replace
Codex with npm, modify the pacman-owned runtime, or repair a different machine
by assumption.

## Workflow

1. Confirm the target is Sputnik (run there, or `ssh sputnik`) and state
   whether the request is an audit or an explicitly authorized repair.
2. Run `scripts/collect_health.py --format markdown`. It uses metadata reads,
   and `pacman -Q` only; it never writes files, invokes package changes, or
   starts/stops services.
3. Interpret the result against the expected layout (observed 2026-11-03): the
   AUR package `openai-codex-desktop` installs the app under `/usr/lib/chatgpt`
   with `/usr/bin/codex-desktop` linking to `chatgpt`; the `codex` CLI is the
   mise shim reached through `~/.local/bin/codex`. Updates come through the
   package manager; there is no separate updater service.
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
- If the collector cannot query `pacman`, report the limitation rather than
  guessing.

## Completion

Finish an audit with the observed runtime, launchers, package, and
configuration status, plus any safe next step. Finish a repair only after
an explicit user-approved change and a fresh successful health collection.
