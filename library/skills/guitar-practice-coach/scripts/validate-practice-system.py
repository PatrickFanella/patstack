#!/usr/bin/env python3
"""Validate the durable guitar-practice state without changing it."""

from __future__ import annotations

import argparse
import re
import sys
import zipfile
from pathlib import Path


PRACTICE = Path("001 Projects/Threads/Guitar/Practice")
REQUIRED = {
    "policy": PRACTICE / "Guitar Practice System.md",
    "pointer": PRACTICE / "Current Practice Block.md",
    "ledger": PRACTICE / "Practice Progress Ledger.md",
    "library": PRACTICE / "Practice Material Library.md",
    "log_template": PRACTICE / "Practice Log Template.md",
    "moc": Path("001 Projects/Threads/Guitar/Guitar MOC.md"),
}


def frontmatter(text: str) -> str:
    match = re.match(r"\A---\n(.*?)\n---\n", text, re.DOTALL)
    return match.group(1) if match else ""


def field(meta: str, name: str) -> str | None:
    match = re.search(rf"(?m)^{re.escape(name)}:\s*(.*?)\s*$", meta)
    return match.group(1).strip('"\'') if match else None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    root = args.root.resolve()
    errors: list[str] = []

    for label, relative in REQUIRED.items():
        if not (root / relative).is_file():
            errors.append(f"missing {label}: {relative}")

    project_dirs = sorted(p.name for p in (root / "001 Projects").iterdir() if p.is_dir())
    if project_dirs != ["Threads", "Works"]:
        errors.append(f"001 Projects directories are {project_dirs!r}, expected ['Threads', 'Works']")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    pointer_text = (root / REQUIRED["pointer"]).read_text(encoding="utf-8")
    pointer_meta = frontmatter(pointer_text)
    active = field(pointer_meta, "active-block")
    if not active:
        errors.append("Current Practice Block.md lacks active-block")
    else:
        active_path = root / active
        if not active_path.is_file():
            errors.append(f"active block does not exist: {active}")
        else:
            block_meta = frontmatter(active_path.read_text(encoding="utf-8"))
            for required_field in ("block-id", "status", "started", "target-session-count"):
                if not field(block_meta, required_field):
                    errors.append(f"active block lacks {required_field}: {active}")
            if field(block_meta, "status") != "active":
                errors.append(f"pointer target is not active: {active}")

    ledger_text = (root / REQUIRED["ledger"]).read_text(encoding="utf-8")
    for heading in ("## Current state", "## Review history", "## Weekly review schema", "## Block review schema"):
        if heading not in ledger_text:
            errors.append(f"ledger lacks heading: {heading}")

    practice_markdown = list((root / PRACTICE).glob("*.md")) + list((root / PRACTICE / "Blocks").glob("*.md"))
    for note in practice_markdown:
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

    for tab in (root / "001 Projects/Threads/Guitar/Tabs").glob("*.tg"):
        if not zipfile.is_zipfile(tab):
            errors.append(f"invalid TuxGuitar archive: {tab.relative_to(root)}")

    for pdf in (root / PRACTICE / "Materials").glob("*.pdf"):
        data = pdf.read_bytes()
        if not data.startswith(b"%PDF-") or b"%%EOF" not in data[-2048:]:
            errors.append(f"invalid PDF envelope: {pdf.relative_to(root)}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print(
        "guitar practice system ok: "
        f"{len(practice_markdown)} notes, "
        f"{len(list((root / '001 Projects/Threads/Guitar/Tabs').glob('*.tg')))} TuxGuitar files, "
        f"{len(list((root / PRACTICE / 'Materials').glob('*.pdf')))} PDFs"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
