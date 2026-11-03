---
name: ci-maintenance
description: Use when a CI run or PR check fails, when watching checks until green on Gitea Actions or GitHub, or when designing pipelines, SAST scanning or pre-commit hooks. Not for test-suite design.
---

# ci-maintenance

Locate the failed job or requested pipeline change. Distinguish local command results from hosted checks. Reuse the existing CI provider and hooks rather than adding a second system; publishing changes requires authorization.

## Select a mode

- Design multi-stage CI/CD pipelines with approval gates, security checks, and deployment orchestration. Read [the procedure](references/modes/deployment-pipeline-design/guide.md).
- Monitor PR checks on Gitea (`tea`) or GitHub (`gh`) and fix failures until green. Read [the procedure](references/modes/loop-on-ci/guide.md).
- Configure Static Application Security Testing (SAST) tools for automated vulnerability detection in application code. Read [the procedure](references/modes/sast-configuration/guide.md).
- Set up Husky pre-commit hooks with lint-staged (Prettier), type checking, and tests in the current repo. Read [the procedure](references/modes/setup-pre-commit/guide.md).

Resource paths inside a mode are relative to that mode directory. Run its scripts from that directory or use absolute script paths, passing the target repository explicitly.
