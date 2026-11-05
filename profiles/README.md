# Optional skill profiles

See [the skills and groups guide](../docs/SKILL-GROUPS.md) for defaults, group
membership, and required/optional companion relationships. The default
`skill-stack-router` can load a specialist from the managed source without
switching profiles. Switch for a sustained change of directly discoverable
skills, or when the client cannot read the library.

Source: `patstack/profiles`. Each `NAME.txt` lists the optional library skills
one Subsets category adds; `core.txt` is always active. Curated personal skills
and the shared skills are installed separately and are never listed here.
Retired names, vault-local skills and blocked qualifications are filtered out
even if a profile names them. See `CATALOG.md` for every category's members and
the README's Subsets section for when to pick each one.

Switch with `subsets apply --NAME` (or `--group NAME`), preview with
`--dry-run`, and return with `subsets apply --group core`. The lower-level
selector is `~/.agents/bin/skill-profile` (`list`, `plan`, `activate`,
`deactivate`, `status`, `rollback --run PATH`). Restart agent sessions after a
change. Claude links are created only for skills whose
`catalog/qualification.json` record lists `claude`.

Edit and commit profiles here, then build and deploy a new Subsets bundle; see
`runtime-bundles/subsets-fleet/README.md`.
