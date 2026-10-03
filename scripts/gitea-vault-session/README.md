# Saved Vaultwarden CLI session lifetime

These are the authoring copies of Kvant's Gitea agent session expiry helper,
user service, timer, and policy. The user selected four hours for both the
Bitwarden desktop vault and the saved CLI session on October 3, 2026.

The desktop account already has a 240-minute timeout and lock action. Its
application-owned settings are independent of this helper.

The helper checks the age of `~/.local/state/gitea-agent/vaultwarden-session`
each minute. At four hours from the saved session file's modification time,
it invokes `bw lock` with the session passed only in the child environment,
then removes the file. It does not log the key. Other clients and separately
retained session keys are outside this file's lifecycle. A fresh local unlock
must write a private replacement file (mode 0600); do not send the key in chat.

Deploy the helper and policy into the private Gitea agent state directory,
and the units into `~/.config/systemd/user/`. Validate with `systemd-analyze
--user verify`, reload the user daemon, and enable the timer. Disable the
exact timer to stop these checks. No credential is included in this source.

Expiry writes an atomic mode-0600 receipt at
`~/.local/state/gitea-agent/vaultwarden-session-expiry-receipt.json`, containing
only timestamps, lock return code, removal result and status. The saved session
key never enters the receipt. A concurrent fresh unlock is preserved. The
four-hour boundary, active-session preservation, failed-lock handling and
concurrent-unlock cases are tested with isolated fixtures and a mock lock
command; those tests do not lock the real vault or prove natural expiry.
