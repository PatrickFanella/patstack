## Verify and finish

Run focused checks while editing, then the relevant broad suite on the final changes using CI-compatible runtimes. Fix regressions introduced by the cleanup. Where baseline blockers need repair to make the authorized overhaul usable, repair them and review the expanded diff for unintended behavior changes.

Exercise real-service/browser tiers when changes affect their boundaries. Use disposable services with distinct names, ports, and volumes; restore modified local test configuration and remove only resources created for this run.

After verification, inspect the final diff, whitespace errors, stale references, test discovery, and generated/untracked files. Move generated reports outside the repository if cleanup is part of the request. Do not create a new completion report or plan in the repository merely to document their removal. Update the maintained testing guide instead.

Report:
- Verified branch/commit and upstream relationship.
- What was removed or consolidated and why the important contracts remain.
- Before/after test counts as descriptive evidence, not the success criterion.
- Checks actually run, their results, and any baseline failures or unexecuted tiers.
- Coverage-policy changes and remaining gaps.
- Artifact location and whether changes are uncommitted, committed, or published.

Local verification does not imply a release. Keep commit, push, merge, deployment, and outward communication within the user's existing authorization.
