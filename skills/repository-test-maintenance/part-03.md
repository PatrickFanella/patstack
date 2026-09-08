## Remove with evidence

Classify candidates by purpose rather than filename alone:

- Generated builds, coverage, screenshots, and run logs: remove reproducible output within scope; preserve needed diagnostic evidence outside the checkout and update ignore rules.
- Plans and completion reports: remove obsolete tracked documents when requested, repairing references. Preserve current operational runbooks, migration/recovery procedures, compliance requirements, and machine-consumed evidence schemas. Git history preserves tracked history; it does not preserve untracked files.
- Application code: establish that production has no callers before removal. Include lazy routes, dynamic imports, registries, reflection, framework discovery, scripts, and external/public entry points in that analysis.
- Dependencies: inspect build configuration, plugins, generated code, and scripts before accepting a static analyzer's finding.
- Tests: identify the behavior that each candidate does or does not protect.

Treat analyzer output as candidates, not deletion authority. Whole-file reachability does not prove every export is used. Conversely, a symbol referenced only by its own tests may still be a supported external API. Follow the actual entry-point model.

Remove obsolete implementations, their exclusive tests, unused exports/helpers, and stale documentation references together. Keep unrelated dirty work and uncertain untracked material intact. Avoid broad destructive cleanup commands that erase files without classification.
