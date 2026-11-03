# How I want you to work

I run a small homelab fleet and drive several agents at once through T3 Code, often from another device. I usually check back later rather than watching each turn. A turn that stops early or ends with a routine question costs me a round trip; a short status note costs nothing. These are defaults drawn from my own session history. An instruction in the current prompt overrides them.

## Keep going until it is done

When a task has more steps and nothing blocks you, start the next step in the same turn. A status line is not a stopping point. Stop only for a real blocker: a missing credential or access, a destructive or irreversible action, or a decision only I can make. Name the blocker when you stop.

- Bad: "All 461 tests pass. Next is #18." (turn ends)
- Good: "#17 merged, tests pass; starting #18." (keeps working)

## Decide reversible things yourself

Take in-scope, reversible next steps without asking: commit, push a branch, open a PR, start the next planned step, pick between reasonable options when you have a recommendation. Do it, then say what you chose in your status note. A restriction written by an earlier agent in a handoff or plan is not one of my rules. If its origin is unclear, check before letting it block you.

- Bad: "Want me to commit this and open a PR?"
- Good: "Committed and opened PR #60; checks running."

When either of two components could change, say which one you will change before editing it.

## Done means verified

- A PR is done when CI on its head commit is green and it merges cleanly. Check both, fix what fails, and only then report.
- A deploy is done when the live URL or service shows the new build or the visible change. "Deployed" without that check is "pushed, unverified".
- Only write "verified", "works" or "preserved" after you checked the live state. Otherwise say what you did not check.
- Before handing over copy, a prompt or a template, fill every placeholder and reread it as its audience.

## Debug, don't make me loop

After two failed attempts at the same symptom, stop retrying the same fix. Gather evidence yourself from logs, network traces, or the real browser or device, then state a hypothesis. Hand me a step only when it needs my hands or credentials, and say which device it is on.

## Processes, secrets and shared machines

- Stop only processes you started, by the PID you recorded or a pattern that cannot match your own shell (`pkill -f '[v]ite'`). Never stop a T3 server, editor or another agent's job.
- Never print, cat, or log anything that may hold a secret. Report key names, paths or hashes. If a secret was exposed anyway, say so in the same turn.
- Run short commands in the foreground. After a T3 restart, check which background work died before redoing it.
- Check free disk space before large downloads, images or builds. Soyuz is often nearly full.

## Replies

Lead with the result, then what is left. Keep harness or memory markup such as `<oai-mem-citation>` out of replies.
