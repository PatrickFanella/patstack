#!/usr/bin/env python3
"""Inventory tracked and visible repository evidence without reading content."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path


CODE_SUFFIXES = {
    ".c", ".cc", ".cpp", ".cs", ".go", ".java", ".js", ".jsx", ".kt",
    ".php", ".py", ".rb", ".rs", ".sh", ".sql", ".swift", ".ts", ".tsx",
}
DOC_SUFFIXES = {".md", ".mdx", ".rst", ".txt", ".adoc"}
TEST_PATTERN = re.compile(r"(^|/)(tests?|specs?)(/|$)|(_test|\.test|\.spec)\.")
PLAN_PATTERN = re.compile(
    r"(^|/)(plans?|roadmaps?|adrs?|runbooks?)(/|$)"
    r"|(^|/)[^/]*(plan|roadmap|readiness)([-_.]|$)"
)
CI_PATTERN = re.compile(r"(^|/)(\.github|\.gitea|\.gitlab|ci)(/|$)")
BUILD_NAMES = {
    "Makefile", "Taskfile.yml", "justfile", "package.json", "pyproject.toml",
    "Cargo.toml", "go.mod", "pom.xml", "build.gradle", "docker-compose.yml",
    "compose.yml", "Dockerfile",
}


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
    return result.stdout.rstrip("\n") if result.returncode == 0 else ""


def nonempty(value: str) -> list[str]:
    return [line for line in value.splitlines() if line]


def categorize(paths: list[str]) -> dict[str, list[str]]:
    categories: dict[str, list[str]] = {
        "instructions": [],
        "architecture_and_docs": [],
        "plans_and_runbooks": [],
        "code": [],
        "tests": [],
        "build_and_dependencies": [],
        "ci": [],
    }
    for value in paths:
        path = Path(value)
        lowered = value.lower()
        if path.name == "AGENTS.md":
            categories["instructions"].append(value)
        if PLAN_PATTERN.search(lowered):
            categories["plans_and_runbooks"].append(value)
        if path.suffix.lower() in DOC_SUFFIXES or path.name.lower().startswith(
            ("readme", "codemap", "architecture")
        ):
            categories["architecture_and_docs"].append(value)
        if TEST_PATTERN.search(lowered):
            categories["tests"].append(value)
        elif path.suffix.lower() in CODE_SUFFIXES:
            categories["code"].append(value)
        if path.name in BUILD_NAMES or path.name.startswith(
            ("requirements", "package-lock", "pnpm-lock", "yarn.lock")
        ):
            categories["build_and_dependencies"].append(value)
        if CI_PATTERN.search(lowered):
            categories["ci"].append(value)
    return {key: sorted(set(values)) for key, values in categories.items()}


def collect(repo_arg: str, limit: int) -> dict[str, object]:
    requested = Path(repo_arg).expanduser().resolve()
    repo = Path(git(requested, "rev-parse", "--show-toplevel")).resolve()
    if repo != requested:
        raise SystemExit(f"Requested repository root {requested} resolves to parent {repo}; pass the intended Git root explicitly")
    files = sorted(
        nonempty(
            git(
                repo,
                "ls-files",
                "--cached",
                "--others",
                "--exclude-standard",
                "--",
            )
        )
    )
    categories = categorize(files)
    summarized = {
        key: {
            "count": len(values),
            "paths": values[:limit],
            "truncated": len(values) > limit,
        }
        for key, values in categories.items()
    }
    return {
        "repository": str(repo),
        "branch": git(repo, "branch", "--show-current") or "(detached)",
        "head": git(repo, "rev-parse", "--short=12", "HEAD", check=False)
        or "(unborn)",
        "status_entries": nonempty(
            git(repo, "status", "--short", "--untracked-files=all")
        ),
        "visible_file_count": len(files),
        "categories": summarized,
    }


def markdown(data: dict[str, object]) -> str:
    lines = [
        "# Repository Evidence Inventory",
        "",
        f"- Repository: `{data['repository']}`",
        f"- Branch: `{data['branch']}`",
        f"- HEAD: `{data['head']}`",
        f"- Visible files: {data['visible_file_count']}",
        f"- Working-tree entries: {len(data['status_entries'])}",
        "",
    ]
    for name, section in data["categories"].items():
        title = name.replace("_", " ").title()
        suffix = " (sample truncated)" if section["truncated"] else ""
        lines.extend([f"## {title}", "", f"- Count: {section['count']}{suffix}"])
        lines.extend(f"- `{path}`" for path in section["paths"])
        if not section["paths"]:
            lines.append("- No matching files")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("repo", nargs="?", default=".")
    parser.add_argument("--format", choices=("json", "markdown"), default="json")
    parser.add_argument("--limit", type=int, default=40)
    args = parser.parse_args()
    if args.limit < 1 or args.limit > 500:
        parser.error("--limit must be between 1 and 500")
    data = collect(args.repo, args.limit)
    if args.format == "markdown":
        print(markdown(data), end="")
    else:
        print(json.dumps(data, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
