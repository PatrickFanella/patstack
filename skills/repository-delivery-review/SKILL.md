---
name: repository-delivery-review
description: Audit a repository against its intended capabilities; separate implemented, incomplete, planned, and unverified work.
---

# Repository Delivery Review

Build a defensible project-state assessment without promoting plans or file
presence into verified capability.

## Workflow

1. **Frame the decision.**
   - Identify repository, target revision, requested audience, and whether the
     question concerns completeness, readiness, viability, or all three.
   - Read all applicable `AGENTS.md` files before broad inspection.
2. **Map evidence efficiently.**
   - Run `python3 scripts/collect_repository_evidence.py <repo> --format markdown`.
   - Read the repository map or architecture entrypoint when one exists.
   - Start with decision-relevant docs, plans, runbooks, build interfaces, and
     test surfaces; avoid flat dumps of every document.
3. **Trace claims into implementation.**
   - For each major capability, connect documentation or plan claims to concrete
     code entrypoints, storage/contracts, user surfaces, and tests.
   - Mark intended, scaffolded, implemented, test-verified, and runtime-verified
     states separately.
4. **Run proportional verification.**
   - Prefer repository-documented gates.
   - Use focused checks when the user asks for a bounded review or the full gate
     is expensive.
   - Record exact commands, revision, environment, failures, and skipped checks.
5. **Assess gaps and risk.**
   - Read [references/evidence-rubric.md](references/evidence-rubric.md) before
     assigning completeness, readiness, or viability judgments.
   - Distinguish missing implementation from migration debt, operational work,
     documentation drift, and evidence gaps.
6. **Deliver the assessment.**
   - State the verdict first.
   - Cover implemented capability, incomplete/planned work, verification
     evidence, technical and operational risks, and the most useful next steps.
   - Attach caveats directly to the claims they limit.

## Efficiency Rules

- Use repository maps and referenced plans as routing indexes, not as proof.
- Sample repeated implementation patterns, then deepen inspection where claims
  conflict or risk is high.
- Delegate independent documentation, code, and test inspection when the
  repository is large; keep integration and the final judgment with one agent.
- Do not run expensive, destructive, production-facing, or credentialed checks
  merely to strengthen a report.

## Completion Contract

Finish only when the major claims have file-level evidence, planned state is
separated from implemented state, verification limits are explicit, and the
verdict answers the requested delivery or viability question directly.
