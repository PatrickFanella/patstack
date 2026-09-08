# Deterministic resource review

## P1 — `plan`, fresh `apply`, and `verify` cannot run until the repository has an initial commit

[`scripts/install.py:82`](../scripts/install.py) unconditionally executes
`git rev-parse HEAD`. This checkout is on `codex/skill-consolidation` with no
commits, and `git rev-parse --verify HEAD` exits with `fatal: Needed a single
revision`. `prepare()` therefore cannot return a plan. The CLI routes `plan`
and `verify` through `prepare()`, and a non-resume `apply` calls `prepare()`
before it can create a transaction.

**Required action:** either make an initial commit a documented, enforced
precondition before this installer is used, or record a deterministic
uncommitted source identity (for example, a content manifest digest) when
`HEAD` is absent.

**Exact limit:** this affects only checkouts without `HEAD`; rollback and an
existing transaction resumed with `--resume` do not call `prepare()`.

## P2 — collection regeneration depends on two host-local draft skills not declared in installation configuration

[`scripts/build_collection.py:91`](../scripts/build_collection.py) reads
`implementation-plan` and `verify-behavior` from the hard-coded path
`/home/onnwee/.codex/skill-audits/2026-09-08-context-functionality/proposed-skills`.
That directory exists on this host, but it is neither inside this repository
nor represented in [`catalog/installation.json`](../catalog/installation.json).
A clone that has the configured archive but lacks this unrelated audit tree
cannot regenerate the collection and fails before it writes those two
entrypoints.

**Required action:** vendor those two source skills or their generated source
into the repository, or add an explicit configurable input with an early,
actionable existence check.

**Exact limit:** this is a one-time/rebuild reproducibility failure in
`build_collection.py`; the already-generated candidate files are present and
the installer does not call this builder.
