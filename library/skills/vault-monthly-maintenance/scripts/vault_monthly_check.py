#!/usr/bin/env python3
"""Monthly ars-malefica vault maintenance report.

Reports metadata gaps and maintenance queues without printing secrets.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

try:
    import yaml  # type: ignore
except Exception:  # pragma: no cover - fallback path
    yaml = None

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from periodic_note_hierarchy import (  # pyright: ignore[reportMissingImports]  # noqa: E402
    KINDS,
    PERIODIC_ROOT,
    PERIODS,
    destination_for,
    parse_key,
    paths_for_day,
)

EXCLUDE_PREFIXES = ("004 Archives/", ".obsidian/", ".trash/", ".superpowers/", ".smart-env/")
PERIODIC_SCAN_EXCLUDE_PREFIXES = EXCLUDE_PREFIXES + (
    "003 Resources/Templates/",
    "003 Resources/Systems/System Docs Vault/",
)
PERIODIC_SCAN_EXCLUDE_PARTS = frozenset(
    {".git", "node_modules", "vendor", "dist", "build", "coverage", "__pycache__"}
)
CANONICAL_PREFIXES = ("001 Projects/", "002 Areas/", "003 Resources/Systems/")
CANONICAL_EXCLUDE_PREFIXES = (
    "001 Projects/Works/Distributed Creature ARG/",
    "001 Projects/Works/Documentation/Developer Community Engagement Kit/",
    ".opencode/skills/",
    "003 Resources/Systems/Ableton Performance System/",
    "003 Resources/Systems/System Docs Vault/",
    "003 Resources/Systems/Vault Migrations/Design History/",
)
KIND_BY_PERIOD = {period: kind for kind, period in PERIODS.items()}
IDENTITY_KEY_BY_KIND = {
    "Daily": "date",
    "Weekly": "week-segment",
    "Monthly": "month",
    "Quarterly": "quarter",
    "Yearly": "year",
}

# These parent notes predate automatic ancestor creation. Each exception names
# one absent path and the latest interval end among its known legacy children.
# Existing but malformed files are never exempt. No Q3 or August month parent
# is exempt, so missing 2026-Q3 and 2026-08 parents remain defects.
LEGACY_SPARSE_PARENT_EXCEPTIONS = {
    "003 Resources/Periodic Notes/2026/2026-Q1/2026-Q1.md": date(2026, 3, 18),
    "003 Resources/Periodic Notes/2026/2026-Q1/2026-02/2026-02.md": date(2026, 2, 22),
    "003 Resources/Periodic Notes/2026/2026-Q1/2026-02/2026-02-W07/2026-02-W07.md": date(2026, 2, 15),
    "003 Resources/Periodic Notes/2026/2026-Q1/2026-03/2026-03.md": date(2026, 3, 18),
    "003 Resources/Periodic Notes/2026/2026-Q1/2026-03/2026-03-W11/2026-03-W11.md": date(2026, 3, 9),
    "003 Resources/Periodic Notes/2026/2026-Q1/2026-03/2026-03-W12/2026-03-W12.md": date(2026, 3, 18),
    "003 Resources/Periodic Notes/2026/2026-Q2/2026-Q2.md": date(2026, 6, 30),
    "003 Resources/Periodic Notes/2026/2026-Q2/2026-05/2026-05.md": date(2026, 5, 19),
    "003 Resources/Periodic Notes/2026/2026-Q2/2026-05/2026-05-W20/2026-05-W20.md": date(2026, 5, 16),
    "003 Resources/Periodic Notes/2026/2026-Q2/2026-05/2026-05-W21/2026-05-W21.md": date(2026, 5, 19),
    "003 Resources/Periodic Notes/2026/2026-Q2/2026-06/2026-06-W23/2026-06-W23.md": date(2026, 6, 7),
    "003 Resources/Periodic Notes/2026/2026-Q2/2026-06/2026-06-W24/2026-06-W24.md": date(2026, 6, 11),
    "003 Resources/Periodic Notes/2026/2026-Q2/2026-06/2026-06-W26/2026-06-W26.md": date(2026, 6, 23),
    "003 Resources/Periodic Notes/2026/2026-Q3/2026-07/2026-07.md": date(2026, 7, 29),
    "003 Resources/Periodic Notes/2026/2026-Q3/2026-07/2026-07-W31/2026-07-W31.md": date(2026, 7, 29),
    "003 Resources/Periodic Notes/2026/2026-Q3/2026-08/2026-08-W32/2026-08-W32.md": date(2026, 8, 7),
    "003 Resources/Periodic Notes/2026/2026-Q3/2026-08/2026-08-W33/2026-08-W33.md": date(2026, 8, 12),
    "003 Resources/Periodic Notes/2026/2026-Q3/2026-08/2026-08-W34/2026-08-W34.md": date(2026, 8, 22),
}


def read_frontmatter(text: str):
    if not text.startswith("---\n"):
        return None, text
    end = text.find("\n---\n", 4)
    if end == -1:
        return "INVALID", text
    raw = text[4:end]
    body = text[end + 5 :]
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
            data = yaml.load(raw, Loader=UniqueKeyLoader) or {}
            if not isinstance(data, dict):
                return "INVALID", body
            return data, body
        except Exception:
            return "INVALID", body
    data = {}
    current = None
    for line in raw.splitlines():
        if not line.strip():
            continue
        stripped = line.strip()
        if stripped.startswith("-") and current:
            data.setdefault(current, []).append(line[1:].strip().strip('"\''))
            continue
        if ":" not in line:
            return "INVALID", body
        key, value = line.split(":", 1)
        current = key.strip()
        value = value.strip().strip('"\'')
        data[current] = [] if value == "" else value
    return data, body


def included(path: Path) -> bool:
    s = path.as_posix()
    return path.suffix.lower() == ".md" and not any(s.startswith(prefix) for prefix in EXCLUDE_PREFIXES)


def canonical(path: str) -> bool:
    return (
        path.startswith(CANONICAL_PREFIXES)
        and not path.startswith(CANONICAL_EXCLUDE_PREFIXES)
        and "/Sources/" not in path
        and "/.opencode/" not in path
    )


def git_check_ignore(root: Path, rel: str) -> bool:
    try:
        result = subprocess.run(
            ["/usr/bin/git", "check-ignore", "-q", rel],
            cwd=root,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )
        return result.returncode == 0
    except FileNotFoundError:
        return False


def read_json_object(path: Path) -> dict:
    try:
        value = json.loads(path.read_text())
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return {}
    return value if isinstance(value, dict) else {}


def read_json_list(path: Path) -> list:
    try:
        value = json.loads(path.read_text())
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return []
    return value if isinstance(value, list) else []


def ui_state_paths(root: Path) -> list[str]:
    try:
        result = subprocess.run(
            ["/usr/bin/git", "status", "--short", "--ignored", "--", ".obsidian"],
            cwd=root,
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError:
        return []

    names = ("bookmarks.json", "graph.json", "workspace.json", "workspace-mobile.json")
    return sorted(
        line[3:]
        for line in result.stdout.splitlines()
        if line[3:].endswith(names)
    )


def metadata_text(value) -> str | None:
    if isinstance(value, (date, datetime)):
        return value.isoformat()
    return value if isinstance(value, str) else None


def normalized_period_key(kind: str, value) -> str:
    if kind == "Yearly" and isinstance(value, int) and not isinstance(value, bool):
        return str(value)
    if kind == "Daily" and isinstance(value, date) and not isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, str):
        return value
    raise ValueError(f"invalid {IDENTITY_KEY_BY_KIND[kind]} metadata")


def segment_paths(key: str):
    match = re.fullmatch(r"(\d{4}-\d{2})-W\d{2}", key)
    if not match:
        raise ValueError("invalid week segment key")
    first = date.fromisoformat(f"{match[1]}-01")
    for offset in range(31):
        day = first + timedelta(days=offset)
        if day.month != first.month:
            break
        paths = paths_for_day(day)
        if paths.segment == key:
            return paths
    raise ValueError("invalid week segment key")


def periodic_identity(frontmatter: dict, stem: str):
    period = frontmatter.get("period")
    kind = KIND_BY_PERIOD.get(period)
    if kind is None:
        return None
    metadata_key = IDENTITY_KEY_BY_KIND[kind]
    key = stem if metadata_key not in frontmatter else normalized_period_key(kind, frontmatter[metadata_key])
    paths = segment_paths(key) if kind == "Weekly" else parse_key(kind, key)[0]
    return kind, key, paths, destination_for(kind, key, paths)


def interval_end(kind: str, key: str, paths) -> date:
    if kind == "Daily":
        return date.fromisoformat(key)
    if kind == "Weekly":
        return paths.segment_end
    if kind == "Monthly":
        first = date.fromisoformat(f"{key}-01")
        return date(first.year + (first.month == 12), first.month % 12 + 1, 1) - timedelta(days=1)
    if kind == "Quarterly":
        quarter = int(key[-1])
        return date(int(key[:4]) + (quarter == 4), quarter % 4 * 3 + 1, 1) - timedelta(days=1)
    return date(int(key), 12, 31)


def periodic_scan_included(path: Path) -> bool:
    text = path.as_posix()
    return (
        path.suffix.lower() == ".md"
        and not any(text.startswith(prefix) for prefix in PERIODIC_SCAN_EXCLUDE_PREFIXES)
        and not PERIODIC_SCAN_EXCLUDE_PARTS.intersection(path.parts)
    )


def in_canonical_hierarchy(path: Path) -> bool:
    try:
        parts = path.relative_to(PERIODIC_ROOT).parts
    except ValueError:
        return False
    return bool(parts and re.fullmatch(r"\d{4}", parts[0]))


def required_parent_paths(kind: str, paths) -> list[Path]:
    parents = {
        "Yearly": [],
        "Quarterly": [Path(paths.year) / f"{paths.year}.md"],
        "Monthly": [
            Path(paths.year) / f"{paths.year}.md",
            Path(paths.year) / paths.quarter / f"{paths.quarter}.md",
        ],
        "Weekly": [
            Path(paths.year) / f"{paths.year}.md",
            Path(paths.year) / paths.quarter / f"{paths.quarter}.md",
            Path(paths.year) / paths.quarter / paths.month / f"{paths.month}.md",
        ],
        "Daily": [
            Path(paths.year) / f"{paths.year}.md",
            Path(paths.year) / paths.quarter / f"{paths.quarter}.md",
            Path(paths.year) / paths.quarter / paths.month / f"{paths.month}.md",
            Path(paths.year) / paths.quarter / paths.month / paths.segment / f"{paths.segment}.md",
        ],
    }
    return [PERIODIC_ROOT / path for path in parents[kind]]


def target_parent_identity(path: Path) -> tuple[str, str, object]:
    parts = path.relative_to(PERIODIC_ROOT).parts
    if len(parts) == 2:
        kind, key = "Yearly", path.stem
    elif len(parts) == 3:
        kind, key = "Quarterly", path.stem
    elif len(parts) == 4:
        kind, key = "Monthly", path.stem
    elif len(parts) == 5:
        kind, key = "Weekly", path.stem
    else:
        raise ValueError("invalid canonical parent path")
    paths = segment_paths(key) if kind == "Weekly" else parse_key(kind, key)[0]
    if destination_for(kind, key, paths) != path:
        raise ValueError("invalid canonical parent path")
    return kind, key, paths


def hierarchy_health(root: Path) -> dict[str, list[str]]:
    base = root / PERIODIC_ROOT
    report = {
        "misplaced_periodic_notes": [],
        "missing_required_parent_notes": [],
        "invalid_segment_ranges": [],
        "duplicate_period_keys": [],
        "legacy_type_folders": [],
    }
    for kind in KINDS:
        folder = base / kind
        if folder.is_dir():
            report["legacy_type_folders"].append(folder.relative_to(root).as_posix())

    identities: dict[tuple[str, str], list[str]] = {}
    canonical_identities: dict[str, tuple[str, str]] = {}
    children: list[tuple[str, str, object]] = []
    missing_parents: set[str] = set()
    for path in sorted(root.rglob("*.md")):
        relative_path = path.relative_to(root)
        canonical_file = in_canonical_hierarchy(relative_path)
        if not canonical_file and not periodic_scan_included(relative_path):
            continue
        relative = path.relative_to(root).as_posix()
        text = path.read_text(errors="replace")
        frontmatter, _ = read_frontmatter(text)
        if not isinstance(frontmatter, dict) or frontmatter.get("period") not in KIND_BY_PERIOD:
            if canonical_file:
                report["misplaced_periodic_notes"].append(relative)
            continue
        try:
            identity = periodic_identity(frontmatter, path.stem)
            assert identity is not None
            kind, key, paths, expected = identity
        except (OverflowError, TypeError, ValueError):
            report["misplaced_periodic_notes"].append(relative)
            if frontmatter.get("period") == "weekly":
                report["invalid_segment_ranges"].append(relative)
            continue

        identities.setdefault((PERIODS[kind], key), []).append(relative)
        if relative_path != expected:
            report["misplaced_periodic_notes"].append(relative)
        elif canonical_file:
            canonical_identities[relative] = (kind, key)
        children.append((kind, key, paths))

        if kind == "Weekly":
            expected_range = {
                "week": paths.week,
                "week-segment": paths.segment,
                "week-start": paths.segment_start.isoformat(),
                "week-end": paths.segment_end.isoformat(),
                "month": paths.month,
            }
            if any(metadata_text(frontmatter.get(name)) != value for name, value in expected_range.items()):
                report["invalid_segment_ranges"].append(relative)

    for kind, key, paths in children:
        child_end = interval_end(kind, key, paths)
        for parent in required_parent_paths(kind, paths):
            parent_text = parent.as_posix()
            expected_kind, expected_key, _ = target_parent_identity(parent)
            actual = canonical_identities.get(parent_text)
            if actual == (expected_kind, expected_key):
                continue
            if actual is None and not (root / parent).exists():
                exception_end = LEGACY_SPARSE_PARENT_EXCEPTIONS.get(parent_text)
                if exception_end is not None and child_end <= exception_end:
                    continue
            missing_parents.add(parent_text)

    report["missing_required_parent_notes"] = sorted(missing_parents)
    report["duplicate_period_keys"] = sorted(
        path
        for paths in identities.values()
        if len(paths) > 1
        for path in paths
    )
    for paths in report.values():
        paths.sort()
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", nargs="?", default=".")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    cutoff = date.today() - timedelta(days=90)
    core_plugins = read_json_object(root / ".obsidian/core-plugins.json")
    community_plugins = read_json_list(root / ".obsidian/community-plugins.json")
    rows = []
    for path in sorted(root.rglob("*.md")):
        rel = path.relative_to(root)
        if not included(rel):
            continue
        text = path.read_text(errors="replace")
        fm, body = read_frontmatter(text)
        updated = fm.get("updated") if isinstance(fm, dict) else None
        stale = False
        if isinstance(updated, str):
            try:
                stale = datetime.fromisoformat(updated.strip("'\"")).date() < cutoff
            except ValueError:
                stale = True
        rows.append(
            {
                "path": rel.as_posix(),
                "has_frontmatter": isinstance(fm, dict),
                "invalid_frontmatter": fm == "INVALID",
                "type": fm.get("type") if isinstance(fm, dict) else None,
                "status": fm.get("status") if isinstance(fm, dict) else None,
                "updated": updated,
                "stale_updated": stale,
                "has_outgoing_links": "[[" in body,
                "is_workbench": isinstance(fm, dict) and fm.get("type") == "workbench",
            }
        )

    report = {
        "root": str(root),
        "non_archive_markdown": len(rows),
        "missing_frontmatter": sum(not r["has_frontmatter"] for r in rows),
        "invalid_frontmatter": sum(r["invalid_frontmatter"] for r in rows),
        "missing_type": sum(r["has_frontmatter"] and not r["type"] for r in rows),
        "missing_status": sum(r["has_frontmatter"] and not r["status"] for r in rows),
        "stale_updated": sum(r["stale_updated"] for r in rows),
        "no_outgoing_links": sum(not r["has_outgoing_links"] for r in rows),
        "canonical_missing_type": [r["path"] for r in rows if canonical(r["path"]) and not r["type"]],
        "canonical_missing_status": [r["path"] for r in rows if canonical(r["path"]) and not r["status"]],
        "canonical_missing_updated": [r["path"] for r in rows if canonical(r["path"]) and not r["updated"]],
        "stale_workbenches": [r["path"] for r in rows if r["is_workbench"] and r["stale_updated"]],
        "inbox_markdown": [r["path"] for r in rows if r["path"].startswith("000 Inbox/")],
        "official_sync_enabled": core_plugins.get("sync") is True,
        "remotely_save_plugin_enabled": "remotely-save" in community_plugins,
        "remotely_save_data_ignored": git_check_ignore(root, ".obsidian/plugins/remotely-save/data.json"),
        "paperless_data_ignored": git_check_ignore(root, ".obsidian/plugins/paperless/data.json"),
        "ui_state_paths": ui_state_paths(root),
    }
    hierarchy = hierarchy_health(root)
    report.update(hierarchy)
    report["hierarchy_defect_counts"] = {key: len(paths) for key, paths in hierarchy.items()}

    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print("# Vault Monthly Check")
        for key, value in report.items():
            if isinstance(value, list):
                print(f"{key}: {len(value)}")
                for item in value[:20]:
                    print(f"- {item}")
                if len(value) > 20:
                    print(f"- ... {len(value) - 20} more")
            else:
                print(f"{key}: {value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
