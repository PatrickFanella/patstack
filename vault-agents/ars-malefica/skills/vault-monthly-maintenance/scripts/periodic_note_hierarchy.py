#!/usr/bin/env python3
"""Move flat periodic notes into the calendar hierarchy used by periodicPaths.js."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import sys
import tempfile
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path

try:
    import yaml  # type: ignore
except ImportError:  # pragma: no cover - the vault environment includes PyYAML
    yaml = None

PERIODIC_ROOT = Path("003 Resources/Periodic Notes")
KINDS = ("Daily", "Weekly", "Monthly", "Quarterly", "Yearly")
PERIODS = {kind: kind.lower() for kind in KINDS}
NAME_PATTERNS = {
    "Daily": re.compile(r"^\d{4}-\d{2}-\d{2}$"),
    "Weekly": re.compile(r"^(\d{4})-W(\d{2})$"),
    "Monthly": re.compile(r"^\d{4}-\d{2}$"),
    "Quarterly": re.compile(r"^(\d{4})-Q([1-4])$"),
    "Yearly": re.compile(r"^\d{4}$"),
}
PATH_METADATA = {
    "Daily": ("title", "date", "day", "week", "month", "quarter", "year", "period"),
    "Weekly": (
        "title",
        "week",
        "week-segment",
        "week-start",
        "week-end",
        "month",
        "quarter",
        "year",
        "period",
    ),
    "Monthly": ("title", "month", "month-start", "month-end", "quarter", "year", "period"),
    "Quarterly": ("title", "quarter", "quarter-start", "quarter-end", "year", "period"),
    "Yearly": ("title", "year", "period"),
}
WIKILINK = re.compile(r"\[\[([^\]|#]+)(#[^\]|]+)?(\|[^\]]+)?\]\]")


class MigrationError(Exception):
    pass


@dataclass(frozen=True)
class CalendarPaths:
    year: str
    quarter: str
    month: str
    week: str
    segment: str
    segment_start: date
    segment_end: date


@dataclass
class Note:
    kind: str
    source: Path
    key: str
    frontmatter: dict
    raw_frontmatter: str
    body: str
    newline: str = "\n"
    target: bool = False


@dataclass
class Output:
    note: Note
    destination: Path
    segment: CalendarPaths
    text: str = ""
    body_hash_before: str = ""
    body_hash_after: str = ""


def rel(path: Path) -> str:
    return path.as_posix()


def sha256(data: str | bytes) -> str:
    if isinstance(data, str):
        data = data.encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def paths_for_day(day: date) -> CalendarPaths:
    iso_year, iso_week, iso_day = day.isocalendar()
    week_start = day - timedelta(days=iso_day - 1)
    week_end = week_start + timedelta(days=6)
    month_start = day.replace(day=1)
    next_month = date(day.year + (day.month == 12), day.month % 12 + 1, 1)
    month_end = next_month - timedelta(days=1)
    month = f"{day.year:04}-{day.month:02}"
    return CalendarPaths(
        year=f"{day.year:04}",
        quarter=f"{day.year:04}-Q{(day.month - 1) // 3 + 1}",
        month=month,
        week=f"{iso_year:04}-W{iso_week:02}",
        segment=f"{month}-W{iso_week:02}",
        segment_start=max(week_start, month_start),
        segment_end=min(week_end, month_end),
    )


def parse_key(kind: str, key: str) -> list[CalendarPaths]:
    if not NAME_PATTERNS[kind].fullmatch(key):
        raise ValueError("filename does not match its legacy type")
    if kind == "Daily":
        return [paths_for_day(date.fromisoformat(key))]
    if kind == "Weekly":
        match = NAME_PATTERNS[kind].fullmatch(key)
        assert match
        monday = date.fromisocalendar(int(match[1]), int(match[2]), 1)
        sunday = monday + timedelta(days=6)
        segments = [paths_for_day(monday)]
        if (monday.year, monday.month) != (sunday.year, sunday.month):
            segments.append(paths_for_day(sunday))
        return segments
    if kind == "Monthly":
        return [paths_for_day(date.fromisoformat(f"{key}-01"))]
    if kind == "Quarterly":
        match = NAME_PATTERNS[kind].fullmatch(key)
        assert match
        return [paths_for_day(date(int(match[1]), (int(match[2]) - 1) * 3 + 1, 1))]
    return [paths_for_day(date(int(key), 1, 1))]


def destination_for(kind: str, key: str, paths: CalendarPaths) -> Path:
    base = PERIODIC_ROOT / paths.year
    if kind == "Yearly":
        return base / f"{key}.md"
    base /= paths.quarter
    if kind == "Quarterly":
        return base / f"{key}.md"
    base /= paths.month
    if kind == "Monthly":
        return base / f"{key}.md"
    base /= paths.segment
    return base / f"{paths.segment if kind == 'Weekly' else key}.md"


def parse_frontmatter(text: str) -> tuple[dict, str, str, str]:
    newline = "\r\n" if text.startswith("---\r\n") else "\n"
    if not text.startswith(f"---{newline}"):
        raise ValueError("missing frontmatter")
    end = text.find(f"{newline}---{newline}", 3 + len(newline))
    if end == -1:
        raise ValueError("unterminated frontmatter")
    raw = text[3 + len(newline) : end]
    body = text[end + len(newline) * 2 + 3 :]
    if yaml is not None:
        class UniqueKeyLoader(yaml.SafeLoader):
            pass

        def construct_mapping(loader, node, deep=False):
            mapping = {}
            for key_node, value_node in node.value:
                key = loader.construct_object(key_node, deep=deep)
                if key in mapping:
                    raise ValueError(f"duplicate frontmatter key: {key}")
                mapping[key] = loader.construct_object(value_node, deep=deep)
            return mapping

        UniqueKeyLoader.add_constructor(
            yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, construct_mapping
        )
        try:
            parsed = yaml.load(raw, Loader=UniqueKeyLoader) or {}
        except Exception as exc:
            raise ValueError(f"invalid YAML frontmatter: {exc}") from exc
        if not isinstance(parsed, dict):
            raise ValueError("frontmatter is not a mapping")
        return parsed, raw, body, newline

    parsed: dict[str, object] = {}
    for line in raw.splitlines():
        if not line or line[0].isspace() or line.startswith("-"):
            continue
        match = re.match(r"^([A-Za-z0-9_-]+):(?:\s*(.*))?$", line)
        if not match:
            raise ValueError(f"invalid frontmatter line: {line}")
        if match[1] in parsed:
            raise ValueError(f"duplicate frontmatter key: {match[1]}")
        parsed[match[1]] = (match[2] or "").strip(" '\"")
    return parsed, raw, body, newline


def read_inventory(root: Path) -> tuple[list[Note], list[str], dict[str, int]]:
    notes: list[Note] = []
    malformed: list[str] = []
    counts = {kind.lower(): 0 for kind in KINDS}
    for kind in KINDS:
        folder = root / PERIODIC_ROOT / kind
        if not folder.exists():
            continue
        for source in sorted(folder.iterdir()):
            source_rel = source.relative_to(root)
            if not source.is_file() or source.suffix != ".md":
                malformed.append(f"{rel(source_rel)}: unexpected entry in legacy type directory")
                continue
            key = source.stem
            try:
                parse_key(kind, key)
                text = source.read_bytes().decode("utf-8")
                frontmatter, raw_frontmatter, body, newline = parse_frontmatter(text)
                declared = frontmatter.get("period")
                if declared not in (None, PERIODS[kind]):
                    raise ValueError(f"frontmatter period is {declared!r}, expected {PERIODS[kind]!r}")
            except (OSError, UnicodeError, ValueError) as exc:
                malformed.append(f"{rel(source_rel)}: {exc}")
                continue
            notes.append(Note(kind, source_rel, key, frontmatter, raw_frontmatter, body, newline))
            counts[kind.lower()] += 1
    return notes, malformed, counts


def target_identity(path: Path) -> tuple[str, str, CalendarPaths]:
    parts = path.relative_to(PERIODIC_ROOT).parts
    if len(parts) < 2 or not re.fullmatch(r"\d{4}", parts[0]):
        raise ValueError("unexpected entry in target hierarchy")
    stem = path.stem
    if len(parts) == 2 and stem == parts[0]:
        kind, key = "Yearly", stem
    elif len(parts) == 3 and stem == parts[1]:
        kind, key = "Quarterly", stem
    elif len(parts) == 4 and stem == parts[2]:
        kind, key = "Monthly", stem
    elif len(parts) == 5 and stem == parts[3] and re.fullmatch(r"\d{4}-\d{2}-W\d{2}", stem):
        kind, key = "Weekly", stem
    elif len(parts) == 5 and NAME_PATTERNS["Daily"].fullmatch(stem):
        kind, key = "Daily", stem
    else:
        raise ValueError("path does not match target hierarchy")
    if kind == "Weekly":
        month, week = key.rsplit("-W", 1)
        first = date.fromisoformat(f"{month}-01")
        candidate = next((paths_for_day(first + timedelta(days=i)) for i in range(31)
                          if (first + timedelta(days=i)).month == first.month
                          and paths_for_day(first + timedelta(days=i)).segment == key), None)
        if candidate is None or candidate.segment.split("-W")[1] != week:
            raise ValueError("invalid week segment")
        paths = candidate
    else:
        paths = parse_key(kind, key)[0]
    expected = destination_for(kind, key, paths)
    if path != expected:
        raise ValueError(f"misplaced target; expected {rel(expected)}")
    return kind, key, paths


def read_target_inventory(root: Path) -> tuple[list[Note], list[str], dict[str, int]]:
    notes: list[Note] = []
    malformed: list[str] = []
    counts = {kind.lower(): 0 for kind in KINDS}
    base = root / PERIODIC_ROOT
    if not base.exists():
        return notes, malformed, counts
    for source in sorted(base.rglob("*")):
        if not source.is_file():
            continue
        source_rel = source.relative_to(root)
        if source.parent == base:
            continue
        if source.relative_to(base).parts[0] in KINDS:
            continue
        if source.suffix != ".md":
            malformed.append(f"{rel(source_rel)}: unexpected entry in target hierarchy")
            continue
        try:
            kind, key, _ = target_identity(source_rel)
            text = source.read_bytes().decode("utf-8")
            frontmatter, raw_frontmatter, body, newline = parse_frontmatter(text)
            if frontmatter.get("period") != PERIODS[kind]:
                raise ValueError(f"frontmatter period is {frontmatter.get('period')!r}, expected {PERIODS[kind]!r}")
        except (OSError, UnicodeError, ValueError) as exc:
            malformed.append(f"{rel(source_rel)}: {exc}")
            continue
        notes.append(Note(kind, source_rel, key, frontmatter, raw_frontmatter, body, newline, True))
        counts[kind.lower()] += 1
    return notes, malformed, counts


def scaffold_only(body: str) -> bool:
    lines = [line for line in body.splitlines() if line]
    canonical = (
        r"# \d{4}-W\d{2}",
        r"\[\[003 Resources/Periodic Notes/Periodic Notes Hub\|Periodic Notes Hub\]\]",
        r"## Week shape",
        r"- Most repeated pattern:",
        r"- Clearest change:",
        r"- Thing that drained energy:",
        r"- Thing that created energy:",
        r"## Carry forward as a question",
        r"-",
        r"## Notes changed this week",
        r"```dataview",
        r'TABLE file\.link AS "Note", file\.folder AS "Folder", file\.mtime AS "Updated"',
        r'FROM ""',
        r'WHERE file\.mtime >= date\("\d{4}-\d{2}-\d{2}"\)',
        r'  AND file\.mtime <= date\("\d{4}-\d{2}-\d{2}"\)',
        r'  AND file\.name != "\d{4}-W\d{2}"',
        r"SORT file\.mtime DESC",
        r"LIMIT 25",
        r"```",
    )
    return len(lines) == len(canonical) and all(
        re.fullmatch(pattern, line) for pattern, line in zip(canonical, lines)
    )


def metadata_for(kind: str, key: str, paths: CalendarPaths) -> dict[str, str]:
    if kind == "Daily":
        day = date.fromisoformat(key)
        return {
            "title": key,
            "date": key,
            "day": day.strftime("%A"),
            "week": paths.week,
            "month": paths.month,
            "quarter": paths.quarter,
            "year": paths.year,
            "period": "daily",
        }
    if kind == "Weekly":
        return {
            "title": paths.segment,
            "week": paths.week,
            "week-segment": paths.segment,
            "week-start": paths.segment_start.isoformat(),
            "week-end": paths.segment_end.isoformat(),
            "month": paths.month,
            "quarter": paths.quarter,
            "year": paths.year,
            "period": "weekly",
        }
    if kind == "Monthly":
        next_month = date(paths.segment_start.year + (paths.segment_start.month == 12), paths.segment_start.month % 12 + 1, 1)
        return {
            "title": key,
            "month": key,
            "month-start": f"{key}-01",
            "month-end": (next_month - timedelta(days=1)).isoformat(),
            "quarter": paths.quarter,
            "year": paths.year,
            "period": "monthly",
        }
    if kind == "Quarterly":
        quarter = int(key[-1])
        start = date(int(key[:4]), (quarter - 1) * 3 + 1, 1)
        end = date(start.year + (quarter == 4), quarter % 4 * 3 + 1, 1) - timedelta(days=1)
        return {
            "title": key,
            "quarter": key,
            "quarter-start": start.isoformat(),
            "quarter-end": end.isoformat(),
            "year": paths.year,
            "period": "quarterly",
        }
    return {"title": key, "year": key, "period": "yearly"}


def rewrite_frontmatter(note: Note, paths: CalendarPaths) -> str:
    values = metadata_for(note.kind, note.key, paths)
    lines = note.raw_frontmatter.splitlines()
    found: set[str] = set()
    for index, line in enumerate(lines):
        match = re.match(r"^([A-Za-z0-9_-]+):", line)
        if match and match[1] in values:
            key = match[1]
            lines[index] = f"{key}: {values[key]}"
            found.add(key)
    for key in PATH_METADATA[note.kind]:
        if key not in found:
            lines.append(f"{key}: {values[key]}")
    return f"---{note.newline}" + note.newline.join(lines) + f"{note.newline}---{note.newline}"


def old_week_bounds(key: str) -> tuple[date, date]:
    match = NAME_PATTERNS["Weekly"].fullmatch(key)
    assert match
    start = date.fromisocalendar(int(match[1]), int(match[2]), 1)
    return start, start + timedelta(days=6)


def rewrite_week_generated(body: str, note: Note, paths: CalendarPaths) -> str:
    source_start, source_end = old_week_bounds(note.key)
    lines = body.splitlines(keepends=True)
    for index, line in enumerate(lines):
        ending = "\r\n" if line.endswith("\r\n") else ("\n" if line.endswith("\n") else "")
        content = line.removesuffix(ending)
        if content == f"# {note.key}":
            lines[index] = f"# {paths.segment}{ending}"
        elif re.fullmatch(r'WHERE file\.mtime >= date\("\d{4}-\d{2}-\d{2}"\)', content):
            lines[index] = f'WHERE file.mtime >= date("{paths.segment_start}"){ending}'
        elif re.fullmatch(r'  AND file\.mtime <= date\("\d{4}-\d{2}-\d{2}"\)', content):
            lines[index] = f'  AND file.mtime <= date("{paths.segment_end}"){ending}'
        elif re.fullmatch(r'  AND file\.name != "[^\"]+"', content):
            lines[index] = f'  AND file.name != "{paths.segment}"{ending}'
    rewritten = "".join(lines)
    assert source_start <= paths.segment_start <= paths.segment_end <= source_end
    return rewritten


LEGACY_TARGET = re.compile(
    r"^003 Resources/Periodic Notes/(Daily|Weekly|Monthly|Quarterly|Yearly)/([^/]+)$"
)
NAV_MARKERS = re.compile(
    r"(?:\*\*(?:Period|Adjacent|Week|Month|Quarter|Year|Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday):\*\*|"
    r"← (?:Yesterday|Last Week)|Tomorrow →|Next Week →|All (?:Daily|Weekly|Monthly|Quarterly|Yearly))"
)


def calendar_target(target: str, context: CalendarPaths) -> str | None:
    suffix = ".md" if target.endswith(".md") else ""
    match = LEGACY_TARGET.fullmatch(target.removesuffix(".md"))
    if not match:
        return None
    kind, key = match.groups()
    try:
        candidates = parse_key(kind, key)
    except (ValueError, OverflowError):
        return None
    if len(candidates) == 1:
        paths = candidates[0]
    else:
        paths = min(candidates, key=lambda item: abs((item.segment_start - context.segment_start).days))
    return destination_for(kind, key, paths).with_suffix("").as_posix() + suffix


def rewrite_generated_navigation(body: str, context: CalendarPaths) -> tuple[str, int]:
    lines = body.splitlines(keepends=True)
    in_fence = False
    fence_type = ""
    in_comment = False
    last_heading = ""
    generated_query = False
    rewrites = 0
    for index, line in enumerate(lines):
        stripped = line.strip()
        if in_comment:
            if "-->" in line:
                in_comment = False
            continue
        if "<!--" in line:
            if "-->" not in line.split("<!--", 1)[1]:
                in_comment = True
            continue
        if stripped.startswith("```"):
            if in_fence:
                in_fence = False
                fence_type = ""
                generated_query = False
            else:
                in_fence = True
                fence_type = stripped[3:].strip()
                generated_query = last_heading in {
                    "## Daily notes this month",
                    "## Monthly notes this quarter",
                    "## Quarterly notes this year",
                }
            continue
        if in_fence:
            if fence_type == "dataview" and generated_query and re.fullmatch(
                r'\s*FROM "003 Resources/Periodic Notes/(Daily|Weekly|Monthly|Quarterly|Yearly)"\s*',
                line.rstrip("\r\n"),
            ):
                ending = "\r\n" if line.endswith("\r\n") else ("\n" if line.endswith("\n") else "")
                indent = line[: len(line) - len(line.lstrip())]
                lines[index] = f'{indent}FROM "{PERIODIC_ROOT.as_posix()}"{ending}'
                rewrites += 1
            continue
        if stripped.startswith("#"):
            last_heading = stripped
        if not NAV_MARKERS.search(line):
            continue

        def replace(match: re.Match[str]) -> str:
            nonlocal rewrites
            selected = calendar_target(match[1], context)
            if selected is None:
                return match[0]
            rewrites += 1
            return f"[[{selected}{match[2] or ''}{match[3] or ''}]]"

        lines[index] = WIKILINK.sub(replace, line)
    return "".join(lines), rewrites


def semantic_frontmatter(raw: str, kind: str) -> str:
    keys = set(PATH_METADATA[kind])
    return "".join(
        line for line in raw.splitlines(keepends=True)
        if not (re.match(r"^([A-Za-z0-9_-]+):", line) and line.split(":", 1)[0] in keys)
    ).rstrip("\r\n")


def make_plan(root: Path) -> tuple[dict, list[Output], dict[Path, str]]:
    legacy_notes, legacy_malformed, counts = read_inventory(root)
    target_notes, target_malformed, target_counts = read_target_inventory(root)
    malformed = legacy_malformed + target_malformed
    if legacy_notes and target_notes:
        state = "partial"
    elif legacy_notes:
        state = "pending"
    else:
        state = "complete"
    outputs: list[Output] = []
    splits: list[str] = []
    for note in legacy_notes + target_notes:
        if note.target:
            segments = [target_identity(note.source)[2]]
        else:
            segments = parse_key(note.kind, note.key)
        if len(segments) > 1:
            if note.kind != "Weekly" or not scaffold_only(note.body):
                malformed.append(f"{rel(note.source)}: cross-month weekly note contains substantive content")
                continue
            splits.append(rel(note.source))
        outputs.extend(Output(note, destination_for(note.kind, note.key, segment), segment) for segment in segments)

    destinations: dict[Path, list[Output]] = {}
    collisions: list[str] = []
    for output in outputs:
        destinations.setdefault(output.destination, []).append(output)

    planned_text: dict[Path, str] = {}
    preservation: list[dict[str, str]] = []
    link_rewrites = 0
    for output in outputs:
        body = output.note.body
        if output.note.kind == "Weekly" and not output.note.target:
            body = rewrite_week_generated(body, output.note, output.segment)
        body, rewritten = rewrite_generated_navigation(body, output.segment)
        link_rewrites += rewritten
        output.text = rewrite_frontmatter(output.note, output.segment) + body
        canonical_before = output.note.body
        if output.note.kind == "Weekly" and not output.note.target:
            canonical_before = rewrite_week_generated(canonical_before, output.note, output.segment)
        canonical_before = rewrite_generated_navigation(canonical_before, output.segment)[0]
        parsed_output = parse_frontmatter(output.text)
        before_semantic = semantic_frontmatter(output.note.raw_frontmatter, output.note.kind) + "---BODY---" + canonical_before
        after_semantic = semantic_frontmatter(parsed_output[1], output.note.kind) + "---BODY---" + body
        output.body_hash_before = sha256(before_semantic)
        output.body_hash_after = sha256(after_semantic)
        if output.body_hash_before != output.body_hash_after:
            raise MigrationError(f"content invariant failed for {rel(output.note.source)} -> {rel(output.destination)}")
        planned_text[output.destination] = output.text
        preservation.append(
            {
                "source": rel(output.note.source),
                "destination": rel(output.destination),
                "sha256": output.body_hash_before,
            }
        )

    selected_outputs: list[Output] = []
    for destination, candidates in sorted(destinations.items(), key=lambda item: rel(item[0])):
        texts = {candidate.text.encode("utf-8") for candidate in candidates}
        if len(texts) > 1:
            collisions.append(f"{rel(destination)} has differing source and destination content")
            continue
        selected_outputs.append(next((candidate for candidate in candidates if not candidate.note.target), candidates[0]))

    if malformed or collisions:
        state = "partial"
        planned_text = {}

    report = {
        "mode": "dry-run",
        "state": state,
        "inventory": counts,
        "target_inventory": target_counts,
        "outputs": len(outputs),
        "moves": len(legacy_notes) - len(splits),
        "splits": splits,
        "collisions": collisions,
        "malformed": malformed,
        "link_rewrites": link_rewrites,
        "defects": malformed + collisions,
        "atomicity": "staged and validated before per-file atomic replacement; interruption recovery is supported, but the filesystem provides no multi-file transaction",
        "content_preservation": {"passed": True, "files": preservation},
    }
    if malformed or collisions:
        report["content_preservation"]["passed"] = False
    return report, selected_outputs, planned_text


def apply_plan(root: Path, report: dict, outputs: list[Output], planned_text: dict[Path, str]) -> None:
    if report["malformed"] or report["collisions"]:
        raise MigrationError("refusing to apply a plan with malformed notes or collisions")
    output_paths = {output.destination for output in outputs}
    sources = {output.note.source for output in outputs}
    staging_root = Path(tempfile.mkdtemp(prefix=".periodic-hierarchy-", dir=root))
    try:
        for path, text in planned_text.items():
            staged = staging_root / path
            staged.parent.mkdir(parents=True, exist_ok=True)
            staged.write_bytes(text.encode("utf-8"))
        for output in outputs:
            staged = staging_root / output.destination
            if not staged.is_file() or staged.read_bytes() != output.text.encode("utf-8"):
                raise MigrationError(f"staged byte validation failed: {rel(output.destination)}")
        for output in outputs:
            destination = root / output.destination
            destination.parent.mkdir(parents=True, exist_ok=True)
            os.replace(staging_root / output.destination, destination)
        for output in outputs:
            if (root / output.destination).read_bytes() != output.text.encode("utf-8"):
                raise MigrationError(f"post-write byte validation failed: {rel(output.destination)}")
        for source in sorted(sources):
            if source not in output_paths and (root / source).exists():
                (root / source).unlink()
    finally:
        shutil.rmtree(staging_root, ignore_errors=True)
    for kind in KINDS:
        folder = root / PERIODIC_ROOT / kind
        if folder.exists():
            try:
                folder.rmdir()
            except OSError as exc:
                raise MigrationError(f"legacy directory is not empty after validation: {rel(folder.relative_to(root))}") from exc
    report["mode"] = "apply"
    report["state"] = "complete"
    report["inventory"] = {kind.lower(): 0 for kind in KINDS}
    report["target_inventory"] = {
        kind.lower(): sum(output.note.kind == kind for output in outputs) for kind in KINDS
    }


def print_human(report: dict) -> None:
    inventory = report["inventory"]
    print(f"mode: {report['mode']}")
    print(f"state: {report['state']}")
    print("inventory: " + ", ".join(f"{kind}={count}" for kind, count in inventory.items()))
    print("target inventory: " + ", ".join(f"{kind}={count}" for kind, count in report["target_inventory"].items()))
    print(f"outputs: {report['outputs']} (moves={report['moves']}, splits={len(report['splits'])})")
    print(f"collisions: {len(report['collisions'])}")
    print(f"malformed: {len(report['malformed'])}")
    print(f"link rewrites: {report['link_rewrites']}")
    print(f"content preservation: {'passed' if report['content_preservation']['passed'] else 'failed'}")
    for key in ("splits", "collisions", "malformed"):
        for item in report[key]:
            print(f"{key[:-1]}: {item}")


def main() -> int:
    parser = argparse.ArgumentParser(usage="periodic_note_hierarchy.py ROOT [--apply] [--json]")
    parser.add_argument("root")
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    try:
        report, outputs, planned_text = make_plan(root)
        if args.apply:
            apply_plan(root, report, outputs, planned_text)
        if args.json:
            print(json.dumps(report, indent=2, sort_keys=True))
        else:
            print_human(report)
        return 1 if report["malformed"] or report["collisions"] else 0
    except (MigrationError, OSError, UnicodeError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
