---
name: coding-challenge-coach
description: Establish an evidence-based coding baseline, generate adaptive original programming challenges, review attempts, diagnose bottlenecks, and maintain the Ars Malefica coding-practice ledger. Use when the user asks to assess their coding level, start or continue coding challenges, get a hint or code review on an active challenge, practice algorithms or software-engineering skills, review progress, or build the next challenge block. Do not use for ordinary implementation work where the user wants the agent to write the solution rather than coach their attempt.
compatibility: Requires Python 3 for the bundled validator and a user-approved local workspace or repository for executable challenges. Network access is optional.
metadata:
  blacktower-pack: personal-learning
  blacktower-kind: workflow
  blacktower-tier: standard
  blacktower-capabilities: coaching,coding,assessment,deliberate-practice
  author: onnwee
  version: '1.0'
---

# Coding Challenge Coach

Treat the vault as durable learning state and executable code, tests, diffs, and
the learner's explanation as evidence. Do not infer ability from job title,
years of experience, solved counts, elapsed time, or one lucky solution.

## Read state first

1. Read `references/state-contract.md` completely.
2. Run `scripts/validate-coding-challenge-system.py --root <vault-root>`.
3. Read, in order:
   - `Coding Challenge Practice System.md`
   - `Learner Profile.md`
   - `Current Challenge Block.md` and its named block
   - `Challenge Progress Ledger.md`, newest review first
   - `Challenge Library.md`
4. Inspect the active challenge workspace, source, tests, and recent attempt
   artifacts when available. Preserve unrelated worktree changes.

If no attempt evidence exists, keep the state `baseline pending`. Never invent a
score or promote the learner from conversation alone.

## Classify the request

- **Baseline intake:** establish goal, target language, runtime, available time,
  accessibility constraints, preferred challenge style, and help policy.
- **Baseline assessment:** create and review a three-to-five challenge diagnostic.
- **Challenge session:** expose one next challenge or the next hint without
  redesigning the block.
- **Attempt review:** run relevant checks, review the explanation, record evidence,
  and choose `continue`, `narrow`, `vary`, or `advance`.
- **Stall diagnosis:** identify one limiting mechanism and reduce one variable.
- **Block review:** assess the evidence gates and create at most one successor.

## Establish the baseline

When language, goal, or execution target cannot be discovered safely, ask one
concise question before generating code. Use a dedicated practice workspace
unless the user explicitly chooses an existing repository.

Create three to five small diagnostic challenges that sample distinct work:

1. implement behavior from a precise specification;
2. diagnose and repair a failing program or test;
3. test, extend, or refactor a small design;
4. add an algorithmic or domain-specific task only when relevant to the goal;
5. finish with a transfer task that changes the surface details.

Keep the baseline short enough to finish. Start with the smallest task that can
separate syntax friction from problem decomposition. Adapt later tasks from
observed evidence; do not front-load an exam. Record each challenge before the
attempt, including permitted resources and the hint policy.

Assess each dimension separately with evidence and confidence:

- specification and decomposition;
- language and tool fluency;
- correctness and edge cases;
- testing and debugging;
- code clarity and maintainability;
- complexity and tradeoff reasoning;
- independence and transfer.

Use bands `not evidenced`, `guided`, `independent`, or `transfer`, not a single
global rank. Complete the baseline only after at least three reviewed attempts,
including one debugging task and one transfer task.

## Coach without taking over

Before revealing help, ask for the learner's current hypothesis, attempted
approach, and observed failure when that evidence is absent. Use the smallest
useful hint and record the highest assistance level used:

0. no hint;
1. clarify the contract or restate the symptom;
2. provide a counterexample, invariant, or diagnostic test;
3. name the relevant concept or tool;
4. outline a plan or pseudocode;
5. show a local code fragment;
6. provide a full solution only after explicit request or after the attempt is
   closed, then require an explanation and a fresh transfer task.

Do not count a solution as independent when code-level help materially supplied
it. Do not withhold safety, destructive-action, or environment warnings as part
of the challenge.

## Review real evidence

Run the challenge's formatter, type checker, tests, or build when available.
Add adversarial or property-focused cases after the learner's attempt when they
materially test the contract. Distinguish passing visible checks from broader
correctness; never claim hidden tests existed when they did not.

Record the prompt/version, language/runtime, workspace and revision or diff,
result of each command, relevant edge cases, assistance level, the learner's
explanation, one strength, one limiting failure, and confidence. Time is optional
context, never a quality score.

## Make one decision

- **Continue:** repeat the current skill at similar difficulty with new surface details.
- **Narrow:** reduce scope, concepts, data size, or tool friction to isolate one bottleneck.
- **Vary:** preserve the core skill but change representation, domain, constraints, or context.
- **Advance:** increase one difficulty axis after repeated independent evidence and a transfer pass.

Change only one main difficulty axis at a time. Prefer one central learning
objective per challenge. A useful review may add no new challenge.

## Update durable state

For an attempt review:

1. Add the attempt to `Challenge Progress Ledger.md`, newest first.
2. Update the ledger's current-state snapshot and `Learner Profile.md` only from evidence.
3. Update the named block when its next instruction or scope changes.
4. Queue reusable or sourced prompts in `Challenge Library.md`; do not promote them merely because they are interesting.

For a block review, assess every gate as `passed`, `partial`, `failed`, or
`not evidenced`. Preserve completed blocks in `Practice/Blocks/`. If advancing,
create exactly one successor, update the stable pointer and Programming MOC, and
state which single difficulty axis changed.

Generate original challenges by default. For external prompts, preserve title,
author or publisher, URL, access conditions, and adaptation notes; link instead
of copying proprietary prompt text or test suites without permission.

## Validate and report

1. Run the coding-practice validator.
2. Run the Ars Malefica vault and workflow validators.
3. Report the coaching decision, evidence used, commands and outcomes, changed
   files, assistance level, confidence, and the exact next instruction.

When maintaining this skill rather than coaching, read
`examples/behavior-evaluation.md` for the initial positive, near-miss, and
with-skill versus baseline checks.

