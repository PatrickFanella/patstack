# Arch and Omarchy recovery boundaries

Use this reference only after the health collector identifies a problem or the
user asks to repair the local desktop setup.

## Ownership and non-negotiable boundaries

| Component | Owner | Boundary |
| --- | --- | --- |
| `/opt/codex-desktop` | pacman `codex-desktop` package | Never edit, replace, or delete it manually. |
| `codex-update-manager.service` | user-level service | Inspect with `systemctl --user`; do not restart, enable, disable, or replace it without approval. |
| `~/.local/bin/codex` | Omarchy command wrapper | Never replace it with a global npm installation merely to satisfy `codex doctor`. |
| `~/.codex/config.toml` | user configuration | Validate first; change only the smallest relevant setting with approval. |

The collector is evidence, not permission for remediation. Do not use `sudo`,
package reinstalls, service state changes, or wrapper rewrites unless the user
has explicitly requested that exact class of repair.

## Triage

- **Package missing or runtime path absent:** report the package and path
  evidence. A package-manager repair belongs to the user-approved Arch package
  workflow, not an ad-hoc file copy.
- **Updater service inactive or unavailable:** collect `systemctl --user
  status codex-update-manager.service` and relevant user journal entries
  read-only. Distinguish a disabled service, an absent unit, and a failed unit
  before proposing an action.
- **Launcher missing or not executable:** preserve the diagnosis; the Omarchy
  wrapper owner should restore it. Do not substitute `npm install -g`.
- **Config parse failure:** run the repository validator where available and
  identify the exact configuration error. Do not conflate it with package
  health.
- **`codex doctor` update-path mismatch only:** explain that the launcher can
  resolve through Omarchy tooling and an npm target mismatch is expected. No
  repair is indicated without an actual launch or update failure.

## Evidence after an approved repair

Run the collector again and record the changed status, the command or owner
that performed the repair, and any remaining interactive action such as
sign-in or hook trust. Never claim success based only on a running process.
