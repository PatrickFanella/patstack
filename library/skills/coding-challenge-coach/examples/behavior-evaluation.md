# Initial behavior evaluation

Evaluated 2026-08-10 with isolated ephemeral Codex runs in a read-only `/tmp`
workspace. The comparison runs did not load this skill; the skill runs read
`SKILL.md` and `references/state-contract.md`. Times are wall-clock seconds from
the command runner. Token counts are the client-reported usage and include the
host instruction/catalog context, so they are comparison evidence rather than
the activation-file size.

## Scenario 1: begin coaching without a stated goal or language

Prompt: `I want to get better at coding. Start me with challenges and track my progress.`

Assertions:

- Keep the baseline pending rather than inventing a level.
- Ask one concise setup question that resolves goal and language/runtime.
- Do not generate an arbitrary challenge before the execution target is known.

| Variant | Time | Input / cached / output tokens | Result |
|---|---:|---:|---|
| Baseline | 7.39s | 19,062 / 9,984 / 80 | Partial: asked for goal and language, but also requested an unsupported beginner/intermediate/advanced self-rating and offered chat-only tracking. |
| With skill | 20.44s | 90,683 / 73,728 / 657 | Pass: stated zero attempts and baseline pending, asked one combined goal plus language/runtime question, and deferred Diagnostic A. |

## Scenario 2: request help on an order-preserving deduplication failure

Prompt summary: a Python implementation uses `list(set(xs))`; a test expects
first-occurrence order; the learner asks what is wrong.

Assertions:

- Identify order preservation as the relevant contract.
- Give the smallest useful hint.
- Do not provide replacement code before an explicit full-solution request.

| Variant | Time | Input / cached / output tokens | Result |
|---|---:|---:|---|
| Baseline | 5.03s | 19,097 / 9,984 / 70 | Fail: identified the issue but immediately supplied the complete replacement function. |
| With skill | 11.21s | 40,679 / 28,160 / 262 | Pass: explained the first-occurrence invariant without supplying replacement code. |

## Trigger assertions

Expected positive prompts:

- “Assess my coding level with a baseline.”
- “Give me the next Python challenge.”
- “Review my attempt and update my progress.”
- “I am stuck on the active challenge; give me a hint.”
- “Build the next coding-practice block.”

Expected near-miss negatives:

- “Implement this endpoint for me.”
- “Fix the production build.”
- “Review this pull request for regressions.”
- “Explain what a Python decorator is.”
- “Generate a benchmark report.”

The description explicitly includes the positive intents and excludes ordinary
implementation work where the agent is expected to author the solution.
