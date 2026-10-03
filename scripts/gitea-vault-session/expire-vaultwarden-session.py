#!/usr/bin/python3
"""Expire the locally saved CLI session without logging credentials."""
from pathlib import Path
import json, os, subprocess, time
root = Path.home() / ".local/state/gitea-agent"
session = root / "vaultwarden-session"
if not session.exists():
    raise SystemExit(0)
policy = json.loads((root / "vaultwarden-session-policy.json").read_text())
if time.time() - session.stat().st_mtime < policy["max_age_seconds"]:
    raise SystemExit(0)
env = os.environ.copy()
env["BW_SESSION"] = session.read_text().strip()
result = subprocess.run(["/usr/bin/bw", "lock"], env=env, capture_output=True, timeout=30)
session.unlink(missing_ok=True)
print("Saved Vaultwarden CLI session expired and removed.")
raise SystemExit(result.returncode)
