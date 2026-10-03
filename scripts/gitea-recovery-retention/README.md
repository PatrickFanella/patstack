# Gitea recovery and retention checks

`gitea-package-retention-audit.py` is an audit-only daily check. It never calls
a package, registry, Docker, database, or filesystem delete operation.

It selects the newest passing Almaz restore-drill receipt, derives the restored
dump path beneath that receipt's `restore/` directory, and extracts only the
`public.package_version` table-data entry with `pg_restore`. The dump is mounted
read-only into a disposable, networkless PostgreSQL image. Its extracted ID
count must equal the receipt's package-version count. A package version can only
be reviewed when its exact ID appears in that recovered set.

The audit retains permanent tags, signature/attestation sidecars, versions in
the 180-day window, runtime and cached-image references, and all versions when
any host, Compose source, receipt, or recovery extraction cannot be verified.
It inventories running and stopped containers plus cached Docker images on the
six known hosts. Compose files are read only when their paths are supplied by
container labels; the collector extracts only `git.subcult.tv` image references
from files at most 1 MiB and fails closed when a supplied source is unavailable.

The user service and timer run from this source after installation. Receipts
belong in the private runtime directory configured by the service unit.
