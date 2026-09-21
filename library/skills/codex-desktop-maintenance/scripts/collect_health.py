#!/usr/bin/env python3
"""Collect read-only health evidence for the local Arch/Omarchy Codex setup."""

from __future__ import annotations

import argparse
import json
import os
import platform
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


RUNTIME_PATH = Path("/opt/codex-desktop")
LAUNCHER_PATH = Path.home() / ".local/bin/codex"
CONFIG_PATH = Path.home() / ".codex/config.toml"
UPDATER_UNIT = "codex-update-manager.service"


def path_status(path: Path) -> dict[str, Any]:
    """Return metadata only; do not open or modify the target."""
    result: dict[str, Any] = {"path": str(path), "exists": path.exists()}
    if not result["exists"]:
        return result

    try:
        stat = path.lstat()
        result["kind"] = "symlink" if path.is_symlink() else (
            "directory" if path.is_dir() else "file"
        )
        result["mode"] = oct(stat.st_mode & 0o777)
        result["executable"] = os.access(path, os.X_OK)
        if path.is_symlink():
            result["link_target"] = os.readlink(path)
    except OSError as exc:
        result["error"] = str(exc)
    return result


def run_readonly(command: list[str]) -> dict[str, Any]:
    """Execute bounded diagnostic commands whose arguments are fixed here."""
    try:
        completed = subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True,
            timeout=10,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {"available": False, "error": str(exc)}

    return {
        "available": True,
        "returncode": completed.returncode,
        "stdout": completed.stdout.strip(),
        "stderr": completed.stderr.strip(),
    }


def config_status(path: Path) -> dict[str, Any]:
    result: dict[str, Any] = {"path": str(path), "exists": path.exists()}
    if not result["exists"]:
        return result

    try:
        import tomllib

        with path.open("rb") as handle:
            config = tomllib.load(handle)
        result["parse_ok"] = True
        result["mcp_server_names"] = sorted(
            config.get("mcp_servers", {}).keys()
            if isinstance(config.get("mcp_servers", {}), dict)
            else []
        )
        result["enabled_plugin_count"] = sum(
            1
            for value in config.get("plugins", {}).values()
            if isinstance(value, dict) and value.get("enabled") is True
        )
    except (OSError, ValueError, TypeError) as exc:
        result["parse_ok"] = False
        result["error"] = str(exc)
    return result


def collect() -> dict[str, Any]:
    return {
        "collected_at_utc": datetime.now(timezone.utc).isoformat(),
        "read_only": True,
        "host": {
            "system": platform.system(),
            "release": platform.release(),
            "machine": platform.machine(),
        },
        "expected_components": {
            "desktop_runtime": path_status(RUNTIME_PATH),
            "omarchy_launcher": path_status(LAUNCHER_PATH),
            "config": config_status(CONFIG_PATH),
        },
        "resolved_codex_command": shutil.which("codex"),
        "pacman_codex_desktop": run_readonly(["pacman", "-Q", "codex-desktop"]),
        "update_manager": run_readonly(
            [
                "systemctl",
                "--user",
                "show",
                UPDATER_UNIT,
                "--property=LoadState,ActiveState,UnitFileState",
                "--no-page",
            ]
        ),
    }


def markdown(data: dict[str, Any]) -> str:
    components = data["expected_components"]
    service = data["update_manager"]
    package = data["pacman_codex_desktop"]
    lines = [
        "# Codex Desktop Health",
        "",
        f"- Collected (UTC): {data['collected_at_utc']}",
        f"- Host: {data['host']['system']} {data['host']['release']} ({data['host']['machine']})",
        f"- Read-only collector: {data['read_only']}",
        f"- Resolved `codex`: {data['resolved_codex_command'] or 'not found'}",
        "",
        "## Expected components",
        "",
    ]
    for label, item in components.items():
        details = [f"exists={item['exists']}"]
        if "kind" in item:
            details.append(f"kind={item['kind']}")
        if "executable" in item:
            details.append(f"executable={item['executable']}")
        if "parse_ok" in item:
            details.append(f"parse_ok={item['parse_ok']}")
        if "error" in item:
            details.append(f"error={item['error']}")
        lines.append(f"- {label}: " + ", ".join(details))

    lines.extend(
        [
            "",
            "## Package and updater service",
            "",
            f"- `pacman -Q codex-desktop`: returncode={package.get('returncode', 'unavailable')}; {package.get('stdout') or package.get('error') or 'no output'}",
            f"- `{UPDATER_UNIT}`: returncode={service.get('returncode', 'unavailable')}; {service.get('stdout') or service.get('error') or 'no output'}",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--format", choices=("json", "markdown"), default="json")
    args = parser.parse_args()
    data = collect()
    if args.format == "markdown":
        print(markdown(data))
    else:
        print(json.dumps(data, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
