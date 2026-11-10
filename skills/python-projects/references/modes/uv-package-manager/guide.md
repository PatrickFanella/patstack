# uv package manager

Use uv for Python dependency management, virtual environments, interpreter installs and lockfile workflows.

Paths here are relative to this mode directory; pass the target repository explicitly.

## Rules for every task

- Work with the project's existing `pyproject.toml`, `uv.lock` and `.python-version`; check `uv --version` before relying on a newer feature.
- For a routine bump, update only the dependency the task names (`uv lock --upgrade-package <name>`). Upgrade every package only when the user asks for that.
- If offline resolution fails, report the missing cached package instead of claiming an updated lock.
- Install uv itself only when it is missing and the user agrees; prefer the project's or system's package manager over piping an installer to a shell.

## Read when needed

- [Quick start](part-05.md): read when creating a new uv project or installing its first dependencies.
- [Virtual environments](part-06.md): read when creating or activating a venv, or running a command through `uv run`.
- [Package management](part-07.md): read when adding, removing, upgrading or locking dependencies.
- [Python versions](part-08.md): read when installing an interpreter or pinning the project's Python version.
- [Project configuration](part-09.md): read when editing uv settings in `pyproject.toml`, or migrating from requirements.txt or poetry.
- [Advanced patterns](references/advanced-patterns.md): read for workspaces and monorepos, CI integration, or Docker builds.
- [Installation](part-04.md): read only when uv is missing on the machine.
