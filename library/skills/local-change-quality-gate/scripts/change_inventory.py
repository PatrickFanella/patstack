#!/usr/bin/env python3
"""Collect a deterministic, read-only summary of a Git working tree."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path


def git(repo: Path, *args: str, check: bool = True) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if check and result.returncode != 0:
        raise SystemExit(result.stderr.strip() or f"git {' '.join(args)} failed")
    return result.stdout.rstrip("\n")


def lines(value: str) -> list[str]:
    return [line for line in value.splitlines() if line]


def numstat(repo: Path, cached: bool) -> list[dict[str, object]]:
    args = ["diff"]
    if cached:
        args.append("--cached")
    args.extend(["--numstat", "--"])
    rows = []
    for line in lines(git(repo, *args)):
        added, deleted, path = line.split("\t", 2)
        rows.append(
            {
                "path": path,
                "added": None if added == "-" else int(added),
                "deleted": None if deleted == "-" else int(deleted),
                "binary": added == "-" or deleted == "-",
            }
        )
    return rows


def collect(repo_arg: str) -> dict[str, object]:
    repo = Path(repo_arg).expanduser().resolve()
    top = Path(git(repo, "rev-parse", "--show-toplevel")).resolve()
    return {
        "repository": str(top),
        "branch": git(top, "branch", "--show-current") or "(detached)",
        "head": git(top, "rev-parse", "--short=12", "HEAD", check=False)
        or "(unborn)",
        "status": lines(git(top, "status", "--short", "--untracked-files=all")),
        "staged": numstat(top, cached=True),
        "unstaged": numstat(top, cached=False),
        "untracked": lines(
            git(top, "ls-files", "--others", "--exclude-standard", "--")
        ),
        "instructions": [
            str(top / path)
            for path in sorted(
                lines(
                    git(
                        top,
                        "ls-files",
                        "--cached",
                        "--others",
                        "--exclude-standard",
                        "--",
                        "AGENTS.md",
                        "*/AGENTS.md",
                    )
                )
            )
        ],
    }


def render_markdown(data: dict[str, object]) -> str:
    output = [
        "# Local Change Inventory",
        "",
        f"- Repository: `{data['repository']}`",
        f"- Branch: `{data['branch']}`",
        f"- HEAD: `{data['head']}`",
        f"- Status entries: {len(data['status'])}",
        f"- Staged files: {len(data['staged'])}",
        f"- Unstaged files: {len(data['unstaged'])}",
        f"- Untracked files: {len(data['untracked'])}",
        "",
    ]
    for title, key in (
        ("Repository instruction files", "instructions"),
        ("Status", "status"),
        ("Staged", "staged"),
        ("Unstaged", "unstaged"),
        ("Untracked", "untracked"),
    ):
        output.extend([f"## {title}", ""])
        values = data[key]
        if not values:
            output.append("- None")
        elif key in {"staged", "unstaged"}:
            for row in values:
                change = "binary" if row["binary"] else f"+{row['added']} -{row['deleted']}"
                output.append(f"- `{row['path']}` ({change})")
        else:
            output.extend(f"- `{value}`" for value in values)
        output.append("")
    return "\n".join(output).rstrip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("repo", nargs="?", default=".")
    parser.add_argument("--format", choices=("json", "markdown"), default="json")
    args = parser.parse_args()
    data = collect(args.repo)
    if args.format == "markdown":
        print(render_markdown(data), end="")
    else:
        print(json.dumps(data, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
