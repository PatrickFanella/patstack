# dep-upgrade-pilot procedures

The rules in `SKILL.md` apply to every upgrade. Paths are relative to this directory; pass the target repository explicitly.

- [Semantic versioning review](part-03.md): read when interpreting `^`, `~` or exact version ranges.
- [Dependency analysis](part-04.md): read when auditing outdated or vulnerable packages, or finding why a package is installed.
- [Compatibility matrix](part-05.md): read when companion packages must move together with the target.
- [Staged upgrade strategy](part-06.md): read when planning the upgrade order across several packages.
- [Breaking change handling](part-07.md): read when the changelog lists breaking changes or a codemod exists.
- [Testing strategy](part-08.md): read when choosing which test tiers prove the upgrade.
- [Automated dependency updates](part-09.md): read when configuring Renovate or Dependabot.
- [Rollback plan](part-10.md): read before the first change, so a failed step can be undone.
- [Common upgrade patterns](part-11.md): read when handling lockfiles, peer-dependency conflicts or workspaces.
