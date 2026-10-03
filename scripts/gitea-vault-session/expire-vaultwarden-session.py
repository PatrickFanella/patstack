#!/usr/bin/python3
"""Expire the locally saved CLI session without logging credentials."""
from pathlib import Path
import json
import os
import subprocess
import tempfile
import time


def expire(root: Path, now: float | None = None) -> int:
    session = root / "vaultwarden-session"
    if not session.exists():
        return 0
    observed = session.stat()
    policy = json.loads((root / "vaultwarden-session-policy.json").read_text())
    checked_at = time.time() if now is None else now
    age = checked_at - observed.st_mtime
    if age < policy["max_age_seconds"]:
        return 0
    env = os.environ.copy()
    env["BW_SESSION"] = session.read_text().strip()
    code = None
    try:
        code = subprocess.run(["/usr/bin/bw", "lock"], env=env,
                              capture_output=True, timeout=30).returncode
    except (OSError, subprocess.TimeoutExpired):
        pass
    # A concurrent local unlock must not lose its freshly written key.
    removed = not session.exists()
    if not removed:
        current = session.stat()
        if (current.st_ino, current.st_mtime_ns) == (observed.st_ino, observed.st_mtime_ns):
            session.unlink()
            removed = True
    result = ("expired" if code == 0 and removed else
              "superseded_by_fresh_session" if code == 0 and not removed else "expiry_incomplete")
    receipt = {"checked_at_unix": checked_at, "session_saved_unix": observed.st_mtime,
               "age_seconds": age, "cli_lock_returncode": code,
               "session_removed": removed,
               "result": result}
    with tempfile.NamedTemporaryFile(mode="w", dir=root, delete=False) as stream:
        json.dump(receipt, stream, indent=2)
        stream.write("\n")
        temporary = Path(stream.name)
    temporary.chmod(0o600)
    temporary.replace(root / "vaultwarden-session-expiry-receipt.json")
    print("Saved Vaultwarden CLI session expiry checked; private receipt recorded.")
    return 0 if code == 0 else 1


if __name__ == "__main__":
    raise SystemExit(expire(Path.home() / ".local/state/gitea-agent"))
