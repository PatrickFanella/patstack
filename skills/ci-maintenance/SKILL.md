---
name: ci-maintenance
description: CI failures, pipelines, pre-commit hooks, and code scanning; distinguish local checks from hosted run results.
---

# ci-maintenance

Locate the failed job or requested pipeline change. Distinguish local command results from hosted checks. Reuse the existing CI provider and hooks rather than adding a second system; publishing changes requires authorization.

## Select a mode

- Design multi-stage CI/CD pipelines with approval gates, security checks, and deployment orchestration. Read [the procedure](references/modes/deployment-pipeline-design/guide.md).
- Monitor PR checks and fix failures until green. Read [the procedure](references/modes/loop-on-ci/guide.md).
- Configure Static Application Security Testing (SAST) tools for automated vulnerability detection in application code. Read [the procedure](references/modes/sast-configuration/guide.md).
- Set up Husky pre-commit hooks with lint-staged (Prettier), type checking, and tests in the current repo. Read [the procedure](references/modes/setup-pre-commit/guide.md).

Resource paths inside a mode are relative to that mode directory. Run its scripts from that directory or use absolute script paths, passing the target repository explicitly.
