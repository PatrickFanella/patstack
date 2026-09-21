#!/usr/bin/env python3
"""Deterministically inventory and structurally audit Codex skills."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
import json
from pathlib import Path
import re
import sys
from typing import Any

import yaml


FRONTMATTER = re.compile(r"\A---\s*\n(.*?)\n---\s*(?:\n|$)", re.DOTALL)
FENCED_BLOCK = re.compile(r"```.*?```", re.DOTALL)
MARKDOWN_LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
VALID_NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


@dataclass
class SkillRecord:
    name: str
    path: str
    root: str
    ownership: str
    folder: str
    lines: int
    description_words: int
    extra_frontmatter: list[str]
    has_openai_yaml: bool
    openai_yaml_valid: bool
    default_prompt_mentions_skill: bool
    short_description_length: int | None
    scripts: int
    references: int
    assets: int
    missing_links: list[str]
    issues: list[str]


def default_roots() -> list[tuple[str, Path]]:
    home = Path.home()
    return [
        ("personal", home / ".agents" / "skills"),
        ("system", home / ".codex" / "skills" / ".system"),
        ("plugins", home / ".codex" / "plugins" / "cache"),
        ("runtime", home / ".cache" / "codex-runtimes"),
    ]


def ownership_for(path: Path) -> str:
    resolved = path.resolve()
    personal_root = (Path.home() / ".agents" / "skills").resolve()
    if resolved == personal_root or personal_root in resolved.parents:
        return "personal"
    text = str(resolved)
    if "/.codex/skills/.system/" in text:
        return "managed-system"
    if "/.codex/plugins/cache/" in text:
        return "managed-plugin"
    if "/.cache/codex-runtimes/" in text:
        return "managed-runtime"
    if "/.agents/skills/" in text:
        return "repository"
    return "repository"


def count_files(path: Path) -> int:
    return sum(1 for item in path.rglob("*") if item.is_file()) if path.is_dir() else 0


def parse_openai_yaml(skill_dir: Path, name: str) -> tuple[bool, bool, bool, int | None, list[str]]:
    path = skill_dir / "agents" / "openai.yaml"
    if not path.is_file():
        return False, False, False, None, ["missing agents/openai.yaml"]
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        interface = data.get("interface") or {}
        prompt = str(interface.get("default_prompt") or "")
        short = interface.get("short_description")
        short_length = len(str(short)) if short is not None else None
        issues: list[str] = []
        if f"${name}" not in prompt:
            issues.append("default_prompt does not mention $skill-name")
        if short_length is None or not 25 <= short_length <= 64:
            issues.append("short_description length is outside 25-64")
        return True, True, f"${name}" in prompt, short_length, issues
    except (OSError, yaml.YAMLError, AttributeError) as error:
        return True, False, False, None, [f"invalid agents/openai.yaml: {error}"]


def missing_markdown_links(skill_dir: Path, body: str) -> list[str]:
    body = FENCED_BLOCK.sub("", body)
    missing: list[str] = []
    for target in MARKDOWN_LINK.findall(body):
        target = target.split("#", 1)[0].strip()
        if not target or "://" in target or target.startswith("#"):
            continue
        if not (skill_dir / target).exists():
            missing.append(target)
    return sorted(set(missing))


def audit_skill(path: Path, root_label: str) -> SkillRecord:
    text = path.read_text(encoding="utf-8")
    match = FRONTMATTER.search(text)
    issues: list[str] = []
    metadata: dict[str, Any] = {}
    body = text
    if not match:
        issues.append("missing YAML frontmatter")
    else:
        body = text[match.end():]
        try:
            metadata = yaml.safe_load(match.group(1)) or {}
        except yaml.YAMLError as error:
            issues.append(f"invalid YAML frontmatter: {error}")
    name = str(metadata.get("name") or "")
    description = str(metadata.get("description") or "")
    extra = sorted(set(metadata) - {"name", "description"})
    if not name:
        issues.append("missing name")
    elif not VALID_NAME.fullmatch(name):
        issues.append("name is not lowercase hyphen-case")
    if not description:
        issues.append("missing description")
    if extra:
        issues.append("frontmatter contains fields beyond name/description")
    if len(text.splitlines()) > 500:
        issues.append("SKILL.md exceeds 500 lines")

    skill_dir = path.parent
    has_yaml, yaml_valid, prompt_ok, short_length, yaml_issues = parse_openai_yaml(skill_dir, name)
    issues.extend(yaml_issues)
    missing = missing_markdown_links(skill_dir, body)
    if missing:
        issues.append("missing relative Markdown links")
    return SkillRecord(
        name=name,
        path=str(path),
        root=root_label,
        ownership=ownership_for(path),
        folder=skill_dir.name,
        lines=len(text.splitlines()),
        description_words=len(description.split()),
        extra_frontmatter=extra,
        has_openai_yaml=has_yaml,
        openai_yaml_valid=yaml_valid,
        default_prompt_mentions_skill=prompt_ok,
        short_description_length=short_length,
        scripts=count_files(skill_dir / "scripts"),
        references=count_files(skill_dir / "references"),
        assets=count_files(skill_dir / "assets"),
        missing_links=missing,
        issues=issues,
    )


def render_markdown(records: list[SkillRecord]) -> str:
    ownership = Counter(record.ownership for record in records)
    duplicate_names = {
        name: paths
        for name, paths in (
            (name, [record.path for record in records if record.name == name])
            for name in sorted({record.name for record in records})
        )
        if name and len(paths) > 1
    }
    issue_records = [record for record in records if record.issues]
    lines = [
        "# Codex Skill Catalog Audit",
        "",
        f"- Skills scanned: {len(records)}",
        f"- Skills with structural findings: {len(issue_records)}",
        f"- Exact duplicate names: {len(duplicate_names)}",
        "",
        "## Ownership",
        "",
        "| Ownership | Skills |",
        "|---|---:|",
    ]
    lines.extend(f"| {key} | {value} |" for key, value in sorted(ownership.items()))
    lines.extend(["", "## Findings", ""])
    if not issue_records:
        lines.append("No structural findings.")
    for record in sorted(issue_records, key=lambda item: (item.ownership, item.name, item.path)):
        lines.append(f"### `{record.name or record.folder}`")
        lines.append("")
        lines.append(f"- Path: `{record.path}`")
        lines.append(f"- Ownership: {record.ownership}")
        lines.append(f"- Lines: {record.lines}")
        for issue in record.issues:
            lines.append(f"- Finding: {issue}")
        for target in record.missing_links:
            lines.append(f"- Missing link: `{target}`")
        lines.append("")
    lines.extend(["## Exact Name Collisions", ""])
    if not duplicate_names:
        lines.append("None.")
    for name, paths in duplicate_names.items():
        lines.append(f"### `{name}`")
        lines.append("")
        lines.extend(f"- `{path}`" for path in paths)
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--root",
        action="append",
        default=[],
        metavar="LABEL=PATH",
        help="Additional root; repeatable",
    )
    parser.add_argument(
        "--no-default-roots",
        action="store_true",
        help="Scan only roots supplied with --root",
    )
    parser.add_argument("--format", choices=("json", "markdown"), default="json")
    parser.add_argument("--output")
    args = parser.parse_args()

    roots = [] if args.no_default_roots else default_roots()
    for value in args.root:
        if "=" not in value:
            parser.error("--root must use LABEL=PATH")
        label, raw_path = value.split("=", 1)
        roots.append((label, Path(raw_path).expanduser()))

    seen: set[Path] = set()
    records: list[SkillRecord] = []
    for label, root in roots:
        if not root.exists():
            continue
        for path in sorted(root.rglob("SKILL.md")):
            resolved = path.resolve()
            if resolved in seen:
                continue
            seen.add(resolved)
            try:
                records.append(audit_skill(path, label))
            except (OSError, UnicodeError) as error:
                print(f"warning: could not audit {path}: {error}", file=sys.stderr)

    if args.format == "markdown":
        output = render_markdown(records)
    else:
        grouped: dict[str, list[str]] = defaultdict(list)
        for record in records:
            for issue in record.issues:
                grouped[issue].append(record.path)
        output = json.dumps(
            {
                "skillCount": len(records),
                "issueCounts": {key: len(value) for key, value in sorted(grouped.items())},
                "skills": [asdict(record) for record in records],
            },
            indent=2,
        ) + "\n"

    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
    else:
        sys.stdout.write(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
