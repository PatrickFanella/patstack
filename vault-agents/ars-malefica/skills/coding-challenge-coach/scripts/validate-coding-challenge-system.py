#!/usr/bin/env python3
"""Validate durable coding-challenge state without changing it."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


PRACTICE = Path("001 Projects/Threads/Programming/Practice")
REQUIRED = {
    "policy": PRACTICE / "Coding Challenge Practice System.md",
    "profile": PRACTICE / "Learner Profile.md",
    "pointer": PRACTICE / "Current Challenge Block.md",
    "ledger": PRACTICE / "Challenge Progress Ledger.md",
    "library": PRACTICE / "Challenge Library.md",
    "attempt_template": PRACTICE / "Challenge Attempt Template.md",
    "moc": Path("001 Projects/Threads/Programming/Programming MOC.md"),
}


def frontmatter(text: str) -> str:
    match = re.match(r"\A---\n(.*?)\n---\n", text, re.DOTALL)
    return match.group(1) if match else ""


def field(meta: str, name: str) -> str | None:
    match = re.search(rf"(?m)^{re.escape(name)}:\s*(.*?)\s*$", meta)
    return match.group(1).strip("\"'") if match else None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    root = args.root.resolve()
    errors: list[str] = []

    for label, relative in REQUIRED.items():
        if not (root / relative).is_file():
            errors.append(f"missing {label}: {relative}")

    project_root = root / "001 Projects"
    if project_root.is_dir():
        project_dirs = sorted(p.name for p in project_root.iterdir() if p.is_dir())
        if project_dirs != ["Threads", "Works"]:
            errors.append(
                f"001 Projects directories are {project_dirs!r}, expected ['Threads', 'Works']"
            )

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    pointer_text = (root / REQUIRED["pointer"]).read_text(encoding="utf-8")
    active = field(frontmatter(pointer_text), "active-block")
    if not active:
        errors.append("Current Challenge Block.md lacks active-block")
    else:
        active_path = root / active
        if not active_path.is_file():
            errors.append(f"active block does not exist: {active}")
        else:
            block_meta = frontmatter(active_path.read_text(encoding="utf-8"))
            required_fields = (
                "block-id",
                "status",
                "phase",
                "started",
                "target-attempt-count",
                "target-language",
                "workspace",
            )
            for required_field in required_fields:
                if not field(block_meta, required_field):
                    errors.append(f"active block lacks {required_field}: {active}")
            if field(block_meta, "status") != "active":
                errors.append(f"pointer target is not active: {active}")

    ledger_text = (root / REQUIRED["ledger"]).read_text(encoding="utf-8")
    for heading in ("## Current state", "## Baseline dimensions", "## Attempt history", "## Attempt review schema", "## Block review schema"):
        if heading not in ledger_text:
            errors.append(f"ledger lacks heading: {heading}")

    profile_text = (root / REQUIRED["profile"]).read_text(encoding="utf-8")
    for heading in ("## Learning target", "## Evidence-based baseline", "## Coaching contract"):
        if heading not in profile_text:
            errors.append(f"profile lacks heading: {heading}")

    practice_notes = list((root / PRACTICE).glob("*.md")) + list(
        (root / PRACTICE / "Blocks").glob("*.md")
    )
    for note in practice_notes:
        text = note.read_text(encoding="utf-8")
        for match in re.finditer(r"\[\[(.*?)\]\]", text, re.DOTALL):
            raw = match.group(0)
            target = match.group(1).split("|", 1)[0].split("#", 1)[0].strip()
            if "\n" in raw:
                errors.append(f"multiline wikilink in {note.relative_to(root)}: {target!r}")
            if "/" not in target:
                continue
            candidate = root / target
            candidates = [candidate] if candidate.suffix else [candidate, candidate.with_suffix(".md")]
            if not any(path.exists() for path in candidates):
                errors.append(f"missing wikilink target in {note.relative_to(root)}: {target}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    blocks = list((root / PRACTICE / "Blocks").glob("*.md"))
    print(f"coding challenge system ok: {len(practice_notes)} notes, {len(blocks)} blocks")
    return 0


if __name__ == "__main__":
    sys.exit(main())
