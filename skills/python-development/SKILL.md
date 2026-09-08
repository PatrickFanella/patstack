---
name: python-development
description: Python tooling, packaging, settings, uv environments, and pytest; select the procedure for the requested change.
---

# python-development

Identify whether the task concerns application code, a utility, packaging, configuration, environment management, or tests. Preserve the project package manager and import layout; use its declared Python version.

## Select a mode

- Python configuration management via environment variables and typed settings. Read [the procedure](references/modes/python-configuration/guide.md).
- Create distributable Python packages with proper project structure, setup.py/pyproject.toml, and publishing to PyPI. Read [the procedure](references/modes/python-packaging/guide.md).
- Implement comprehensive testing strategies with pytest, fixtures, mocking, and test-driven development. Read [the procedure](references/modes/python-testing-patterns/guide.md).
- Python patterns for utility scripts, generators, document/data tooling, and small automation. Read [the procedure](references/modes/python-tooling-patterns/guide.md).
- Master the uv package manager for fast Python dependency management, virtual environments, and modern Python project workflows. Read [the procedure](references/modes/uv-package-manager/guide.md).

Resource paths inside a mode are relative to that mode directory. Run its scripts from that directory or use absolute script paths, passing the target repository explicitly.
