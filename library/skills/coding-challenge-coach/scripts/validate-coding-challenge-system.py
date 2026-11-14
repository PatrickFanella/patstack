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


def has_field(meta: str, name: str) -> bool:
    return re.search(rf"(?m)^{re.escape(name)}:", meta) is not None


TRACK_IDS = {"typescript", "go", "python"}
TRACK_FIELDS = ("track-id", "language", "toolchain", "workspace", "active-challenge", "phase")
TRACK_SECTIONS = ("## Current state", "## Dimensions", "## Next instruction")
SET_FIELDS = ("set-id", "status", "workspace")
SET_SECTIONS = ("## Puzzles", "## Review", "## Next set guidance")
BLOCK_FIELDS = ("block-id", "status", "phase", "started", "target-attempt-count", "target-language", "workspace")


def check_block(root: Path, active: str, owner: str, errors: list[str]) -> None:
    active_path = root / active
    if not active_path.is_file():
        errors.append(f"{owner} names a block that does not exist: {active}")
        return
    block_meta = frontmatter(active_path.read_text(encoding="utf-8"))
    for required_field in BLOCK_FIELDS:
        if not field(block_meta, required_field):
            errors.append(f"active block lacks {required_field}: {active}")
    if field(block_meta, "status") != "active":
        errors.append(f"{owner} names a block that is not active: {active}")


def check_tracks(root: Path, errors: list[str]) -> list[str | None]:
    """Validate track notes; return each track's active-block (or None)."""
    blocks: list[str | None] = []
    for note in sorted((root / PRACTICE / "Tracks").glob("*.md")):
        rel = note.relative_to(root)
        text = note.read_text(encoding="utf-8")
        meta = frontmatter(text)
        for name in TRACK_FIELDS:
            if not field(meta, name):
                errors.append(f"track note lacks {name}: {rel}")
        track_id = field(meta, "track-id")
        if track_id and track_id not in TRACK_IDS:
            errors.append(f"unknown track-id {track_id!r}: {rel}")
        if field(meta, "phase") not in (None, "baseline", "practice"):
            errors.append(f"track phase must be baseline or practice: {rel}")
        for heading in TRACK_SECTIONS:
            if heading not in text:
                errors.append(f"track note lacks heading {heading}: {rel}")
        block = field(meta, "active-block")
        if block:
            check_block(root, block, str(rel), errors)
        blocks.append(block)
    return blocks


def check_puzzle_sets(root: Path, errors: list[str]) -> None:
    folder = root / PRACTICE / "Puzzle Sets"
    index = folder / "Puzzle Sets.md"
    if not folder.is_dir():
        return
    if not index.is_file():
        errors.append(f"missing puzzle set index: {index.relative_to(root)}")
        return
    meta = frontmatter(index.read_text(encoding="utf-8"))
    if not has_field(meta, "active-set"):
        errors.append("puzzle set index lacks active-set")
    active = field(meta, "active-set")
    if active and not (root / active).is_file():
        errors.append(f"active puzzle set does not exist: {active}")
    for note in sorted(folder.glob("Puzzle Set *.md")):
        rel = note.relative_to(root)
        text = note.read_text(encoding="utf-8")
        set_meta = frontmatter(text)
        for name in SET_FIELDS:
            if not field(set_meta, name):
                errors.append(f"puzzle set note lacks {name}: {rel}")
        if field(set_meta, "status") not in (None, "active", "complete"):
            errors.append(f"puzzle set status must be active or complete: {rel}")
        for heading in SET_SECTIONS:
            if heading not in text:
                errors.append(f"puzzle set note lacks heading {heading}: {rel}")


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

    track_blocks = check_tracks(root, errors)
    check_puzzle_sets(root, errors)

    pointer_text = (root / REQUIRED["pointer"]).read_text(encoding="utf-8")
    active = field(frontmatter(pointer_text), "active-block")
    if active:
        check_block(root, active, "Current Challenge Block.md", errors)
    elif not (track_blocks and all(track_blocks)):
        # The shared pointer may be empty only once every track names its own block.
        errors.append("Current Challenge Block.md lacks active-block")

    ledger_text = (root / REQUIRED["ledger"]).read_text(encoding="utf-8")
    for heading in ("## Current state", "## Baseline dimensions", "## Attempt history", "## Attempt review schema", "## Block review schema"):
        if heading not in ledger_text:
            errors.append(f"ledger lacks heading: {heading}")

    profile_text = (root / REQUIRED["profile"]).read_text(encoding="utf-8")
    for heading in ("## Learning target", "## Evidence-based baseline", "## Coaching contract"):
        if heading not in profile_text:
            errors.append(f"profile lacks heading: {heading}")

    practice_notes = [
        note
        for folder in ("", "Blocks", "Tracks", "Puzzle Sets")
        for note in (root / PRACTICE / folder).glob("*.md")
    ]
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
    sets = list((root / PRACTICE / "Puzzle Sets").glob("Puzzle Set *.md"))
    print(
        f"coding challenge system ok: {len(practice_notes)} notes, {len(blocks)} blocks, "
        f"{len(track_blocks)} tracks, {len(sets)} puzzle sets"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
