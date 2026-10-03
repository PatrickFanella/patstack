"""Both the CLI and TUI use the same plan/apply contracts."""
from __future__ import annotations

import argparse
from dataclasses import asdict
import json
from pathlib import Path
import sys

from . import __version__
from .legacy import Legacy
from .manager import Manager
from .storage import DeckError, Store


def printable_plan(plan):
    if "operations" in plan:
        return {**{key: value for key, value in plan.items() if key != "operations"},
                "operations": [{key: op[key] for key in ["path", "action", "skill"] if key in op}
                               for op in plan["operations"] if "action" in op]}
    return plan


def backend_for(manager, groups, legacy, backend="auto"):
    if backend == "existing":
        if not legacy:
            raise DeckError("No existing codex-skills backend detected")
        return legacy
    if backend == "skilldeck":
        return manager
    local = manager.store.load()["groups"]
    custom = set(groups) - {"core"}
    if custom and custom <= local.keys():
        return manager
    if legacy and custom <= legacy.groups().keys() and not (custom & (local.keys() - {"core"})):
        if custom or not manager.store.load()["roots"]:
            return legacy
    if custom & (local.keys() - {"core"}) and legacy and custom & legacy.groups().keys():
        raise DeckError("Apply Skilldeck groups and existing backend profiles separately; they have different owners")
    return manager


def edit_group(manager, legacy, action, name, references, backend="auto"):
    managed = manager.store.load()["skills"]
    if backend == "auto":
        local_match = any(ref in managed or any(row["name"] == ref for row in managed.values()) for ref in references)
        backend = "existing" if legacy and not local_match and (references or not manager.store.load()["roots"]) else "skilldeck"
    if backend == "existing":
        if not legacy:
            raise DeckError("No existing codex-skills backend detected")
        return legacy.edit_group(manager.store, action, name, references)
    return manager.edit_group(action, name, references)


def parser():
    result = argparse.ArgumentParser(description="Discover skills, organize groups, and apply recoverable selections.",
        epilog="Examples: skilldeck · skilldeck discover · skilldeck apply --creative-writing --dry-run")
    result.add_argument("--version", action="version", version=__version__)
    result.add_argument("--state", type=Path, help="Private registry/library directory (or SKILLDECK_HOME)")
    result.add_argument("--project", type=Path, default=Path.cwd(), help="Inspect this checkout and its ancestors")
    result.add_argument("--root", type=Path, action="append", default=[], help="Additional explicit skill root")
    result.add_argument("--no-plugins", action="store_true", help="Skip bounded plugin-cache metadata discovery")
    result.add_argument("--json", action="store_true", help="Machine-readable output")
    commands = result.add_subparsers(dest="command")
    for name, help_text in [("tui", "Open the interactive manager"), ("discover", "List detected skills"),
                            ("roots", "List detected folders and their owners"), ("groups", "List groups and profiles"),
                            ("verify", "Check managed destination hashes"), ("history", "List recoverable transactions")]:
        sub = commands.add_parser(name, help=help_text, epilog=f"Example: skilldeck {name}")
        if name == "discover":
            sub.add_argument("--filter", default="", help="Search skill name, description, owner or path")
    adopt = commands.add_parser("adopt", help="Register an unmanaged folder without changing its skills",
                                epilog="Example: skilldeck adopt ROOT_ID")
    adopt.add_argument("root_id")
    root = commands.add_parser("root", help="Remember an additional search folder",
                               epilog="Example: skilldeck root add ~/SkillSources --owner readonly")
    root.add_argument("action", choices=["add"])
    root.add_argument("path", type=Path)
    root.add_argument("--owner", choices=["readonly", "unmanaged"], default="readonly",
                      help="Read-only source or a folder eligible for explicit adoption")
    importing = commands.add_parser("import", help="Copy a discovered skill into the private library",
                                    epilog="Example: skilldeck import ROOT_ID:skill-name --to TARGET_ROOT_ID")
    importing.add_argument("skill"); importing.add_argument("--to", required=True)
    group = commands.add_parser("group", help="Create or edit a named group",
                                epilog="Example: skilldeck group create creative-writing poetry editing")
    group.add_argument("action", choices=["create", "add", "remove"])
    group.add_argument("name"); group.add_argument("skills", nargs="*")
    group.add_argument("--backend", choices=["auto", "skilldeck", "existing"], default="auto",
                       help="Edit a Skilldeck group or an existing canonical profile")
    for name in ["plan", "apply"]:
        sub = commands.add_parser(name, help="Preview or apply core plus named groups",
                                  epilog=f"Example: skilldeck {name} --creative-writing")
        sub.add_argument("--group", action="append", default=[], help="Group name; repeat to combine groups")
        sub.add_argument("--dry-run", action="store_true", help="Print a read-only plan")
        sub.add_argument("--backend", choices=["auto", "skilldeck", "existing"], default="auto",
                         help="Choose an owner explicitly if names overlap")
    rollback = commands.add_parser("rollback", help="Restore one Skilldeck transaction, preserving later edits",
                                   epilog="Example: skilldeck rollback TRANSACTION_ID")
    rollback.add_argument("transaction")
    return result


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    # Accept output/context options before or after subcommands, without treating
    # typos in reserved options as invented group names.
    global_options, local_options = [], []
    index = 0
    while index < len(argv):
        arg = argv[index]
        if arg in {"--state", "--project", "--root"}:
            global_options += argv[index:index + 2]; index += 2
        elif arg in {"--json", "--no-plugins"}:
            global_options.append(arg); index += 1
        else:
            local_options.append(arg); index += 1
    cli = parser()
    args, extras = cli.parse_known_args(global_options + local_options)
    try:
        manager = Manager(Store(args.state), project=args.project, extra=args.root, plugins=not args.no_plugins)
        legacy = Legacy.find(manager.home)
        if args.command in {"plan", "apply"}:
            available = set(manager.store.load()["groups"]) | (set(legacy.groups()) if legacy else set())
            dynamic = []
            for extra in extras:
                if not extra.startswith("--") or extra[2:] not in available:
                    raise DeckError(f"Unknown option/group {extra!r}; list names with `skilldeck groups`")
                dynamic.append(extra[2:])
            groups = sorted(set(args.group + dynamic))
            backend = backend_for(manager, groups, legacy, args.backend)
            result = backend.plan(groups) if args.command == "plan" or args.dry_run else backend.apply(groups)
            if args.command == "plan" or args.dry_run:
                result = printable_plan(result)
        else:
            if extras:
                cli.error("unrecognized arguments: " + " ".join(extras))
            if args.command in {None, "tui"}:
                if not sys.stdin.isatty() or not sys.stdout.isatty():
                    raise DeckError("The TUI needs an interactive terminal. Use `skilldeck discover --json` for automation.")
                from .tui import SkilldeckApp
                SkilldeckApp(manager, legacy).run(); return 0
            elif args.command == "roots":
                roots, _, warnings = manager.inventory()
                if legacy:
                    extra_roots, _, extra_warnings = legacy.inventory()
                    roots += [root for root in extra_roots if root.path not in {r.path for r in roots}]
                    warnings += extra_warnings
                result = {"roots": [r.record() for r in roots], "warnings": warnings}
            elif args.command == "discover":
                _, skills, warnings = manager.inventory()
                if legacy:
                    _, extra_skills, extra_warnings = legacy.inventory()
                    seen = {s.id for s in skills}
                    skills += [skill for skill in extra_skills if skill.id not in seen]
                    warnings += extra_warnings
                if args.filter:
                    query = args.filter.casefold()
                    skills = [skill for skill in skills if query in " ".join(
                              [skill.name, skill.description, skill.owner, skill.path]).casefold()]
                result = {"skills": [asdict(s) for s in skills], "warnings": warnings}
            elif args.command == "adopt":
                result = manager.adopt(args.root_id)
            elif args.command == "root":
                result = manager.configure_root(args.path, args.owner)
            elif args.command == "import":
                result = manager.import_skill(args.skill, args.to)
            elif args.command == "group":
                result = edit_group(manager, legacy, args.action, args.name, args.skills, args.backend)
            elif args.command == "groups":
                result = {"groups": manager.store.load()["groups"],
                          "existingProfiles": legacy.groups() if legacy else {}}
            elif args.command == "verify":
                result = manager.verify()
            elif args.command == "history":
                result = {"transactions": [{k: row[k] for k in ["id", "label", "status"]}
                                           for row in manager.store.history()]}
            elif args.command == "rollback":
                with manager.store.lock(allow_pending=True):
                    result = {"rolledBack": manager.store.rollback(args.transaction)}
        # One stable JSON object for automation; compact human formatting for lists.
        if args.json or args.command not in {"roots", "discover", "groups"}:
            print(json.dumps(result, indent=2))
        elif args.command == "roots":
            for root in result["roots"]:
                print(f"{root['id']}  {root['client']:8} {root['scope']:8} {root['owner']:24} {root['path']}")
        elif args.command == "discover":
            for skill in result["skills"]:
                print(f"{skill['id']}  {skill['client']:8} {skill['owner']:24} {skill['description']}")
                if skill["issue"]:
                    print("  Needs review: " + skill["issue"])
        else:
            for key, label in [("groups", "Skilldeck"), ("existingProfiles", "Existing backend")]:
                for name, members in result[key].items():
                    print(f"{name:32} {len(members):4} skills  {label}")
        return 0
    except (DeckError, OSError, ValueError) as exc:
        print(json.dumps({"error": str(exc)}) if getattr(args, "json", False) else "skilldeck: " + str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
