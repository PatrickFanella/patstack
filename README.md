# patstack

![patstack: the rack mark and wordmark beside three registered plates](brand/readme-banner.png)

patstack is a personal library of skills for coding agents (Codex, Claude Code, OpenCode, GitHub Copilot and Cursor), with the task profiles that group them and the scripts that validate and install them. A skill is a folder with a `SKILL.md` file and optional references and scripts that an agent loads when a task matches its description.

The repository is published as it is used: profiles, instructions and deployment scripts assume one person's machines and accounts. Read it for ideas or copy individual skills. For a smaller set of skills with the personal setup removed, use [generic-skills](https://github.com/subculture-collective/generic-skills).

## What is in it

- **Curated skills** in `skills/`: everyday work such as planning and implementing changes, fixing bugs, reviewing diffs, Git and pull requests, CI, auth, APIs, web UI styling, writing, and language guides for Go, Python, TypeScript, Rust and PostgreSQL.
- **Shared workflow skills** in `shared/`: requirements, handoffs, product launch preparation, writing voice guides and the router that finds other skills.
- **A specialist library** in `library/skills/`: a larger pool that task profiles draw from.
- **Task profiles** in `profiles/`: `core` (26 everyday skills) and 11 task sets that add skills around an outcome: `build-and-ship`, `build-agent-tools`, `creative-production`, `data-and-decisions`, `diagnose-and-repair`, `fiction-and-worlds`, `learn-and-practice`, `mobile-and-interfaces`, `operate-homelab`, `product-and-launch` and `research-and-write`. Sets overlap and can be combined. [docs/SKILL-GROUPS.md](docs/SKILL-GROUPS.md) explains each one and [profiles/CATALOG.md](profiles/CATALOG.md) lists every member.
- **Global instructions** in `instructions/`, rendered into each client's global instruction file by `scripts/global-instructions.py`.
- **Project and vault instructions** in `project-agents/` and `vault-agents/`, installed by `scripts/project-skills.py` and `scripts/vault-agents.py`.
- **Catalogs** in `catalog/`: the target collection, capability owners, skill routes, retired names and provenance.
- **Validation and tests**: `scripts/validate.py` checks the catalog, provenance, resource links and syntax; `tests/` runs the installers and profile selection against disposable fixtures.

## Using the skills

[Subsets](https://github.com/subculture-collective/subsets) is the skill manager that installs these profiles. It links the selected skills into each client's skill folder and records what it changed so a selection can be rolled back.

```sh
subsets apply --build-and-ship --dry-run   # preview core plus one task set
subsets apply --build-and-ship
subsets apply --research-and-write --product-and-launch
subsets apply --group core                 # return to the everyday core
```

The bundle Subsets installs is built from `runtime-bundles/subsets-fleet/`; its [README](runtime-bundles/subsets-fleet/README.md) covers building and deploying it. Start a new agent session after changing the selection so the client discovers the new skills.

To use a single skill without Subsets, copy its folder into your client's skill directory (for example `~/.claude/skills/<name>` or `~/.codex/skills/<name>`). Some skills reference companion skills or scripts in their own folder; read the `SKILL.md` first.

## Checks

You need Python 3 and PyYAML.

```sh
python scripts/validate.py --source-only    # catalog, provenance, links and syntax
python scripts/stack-catalog.py --check     # generated task-stack guides are current
python -m unittest discover -s tests -v     # installer and selection tests in fixtures
```

After changing a profile, regenerate the guide and catalog with `python scripts/stack-catalog.py`.

## Layout

```txt
skills/            curated skills
shared/            shared workflow skills
library/skills/    specialist skill library
profiles/          core and task-set membership
instructions/      global agent instructions
project-agents/    project skills and instruction blocks
vault-agents/      instructions and skills for note vaults
runtime-bundles/   Subsets adapter bundle
catalog/           collection, ownership and provenance data
scripts/           validators, generators and installers
tests/             fixture tests
authoring/         notes on maintaining the collection
brand/             logo and brand guide
```

## Contributing

Report bugs and request features in [GitHub issues](https://github.com/subculture-collective/patstack/issues). Ask questions and share ideas in [GitHub Discussions](https://github.com/subculture-collective/patstack/discussions). Open pull requests on GitHub against `main`. CI runs the three checks above on every pull request. Edit the source files here, not installed copies. When moving or importing a resource, keep its license and notices with it.

## License

Original contributions are licensed under the GNU General Public License, version 3 or (at your option) any later version (`GPL-3.0-or-later`). See [LICENSE](LICENSE).

Third-party code, documentation, fonts, data and other assets keep their own licenses, copyright notices and attribution. Those notices sit beside the material they cover.
