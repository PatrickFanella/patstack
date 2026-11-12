---
name: hillclimb
description: "Improve work in scored rounds until it reaches a target: a panel of models from three providers scores it out of 10 (UI, design, copy, code), or a program measures it (eval, test pass count, size, time). Use for \"council\", \"hill climb\" or \"keep going until it scores 9/10\". Not for a one-off review (review-code-changes)."
---

# hillclimb

Turn the request into a score, then change the work and re-score it until every judge meets the target. The score decides, not your opinion of a change. A round's findings never widen the requested scope.

## 1. Choose the ruler

Prefer a program when one can measure the goal: an eval's pass count, a test suite, a benchmark, a token or byte count. Build it first if it does not exist, and check that it separates a known-bad case from a known-good one. Use a model panel for qualities no program measures, such as visual design, readability or copy.

State the target, the direction that counts as better, and a round cap. Use the user's numbers; otherwise the target is 9/10 from every panel member and the cap is 10 rounds. A two-stage goal keeps the first stage as a gate: "pass every case, then cut the descriptions to a third" means every cut must still pass every case.

## 2. Score round 0

Fix known issues, address open PR comments and run the relevant checks first, so the panel judges current work. Then score the unchanged work as round 0.

For UI, capture the same views every round with the client's browser or preview tools: the main screens, both themes when the app has them, and the states the user named. Add screenshots of comparable products when the user gives or names them, and have the panel score those references every round. Scores drift between rounds, so judge the gap to the references, not the absolute number.

## 3. Run a panel round

No model is fixed. Use the members the user names; otherwise pick the strongest model each of three providers currently offers, at high reasoning effort. In T3 Code, resolve them with `orchestrator_capabilities` and start one read-only `delegate_task` per member in parallel, a new one every round. Claude Code's `Agent` tool runs Claude models only; reach other providers through T3 or a read-only CLI such as `codex exec`. If three providers or a named member cannot be reached, say so; never substitute a model silently.

Send every member the same [panel brief](references/panel-brief.md). Do not tell members the target score: members who know it score toward it.

Check each result against the work as it arrives and plan fixes while the others run, but do not edit files a member is still reading. A member the user marks non-blocking holds up no round, and its score stays out of the record. To save usage, the user may have only the cheapest member score until it reaches the target before adding the rest; only rounds with every blocking member count toward stopping.

## 4. Change and re-score

Act on findings that improve the work within scope; decline the rest in one line with the reason. With a program ruler, make one change, re-measure, and keep it only when the score improves past noise and the gate passes; otherwise revert it in full. Commit each kept change separately. Then re-capture the same views or re-run the same measurement as the next round.

## 5. Stop

Stop when every blocking member meets the target in the same round on the current work, or the program meets the target with the gate passing. Also stop at the round cap or after three rounds without gain, and report where it stands. Never lower the target to finish. Changing the ruler makes earlier scores incomparable, so restart at round 0 if you must.

Report the rounds in the [score report](references/report.md) format.

Load [companion procedures](references/skill-routes.md) only when their stated condition applies.
