# Panel brief

Fill every placeholder and send the same text to each member. Delegated members get no conversation history, so the brief carries all context. Leave the target score out.

```text
Review only. Do not edit files, commit, push, comment on pull requests or start subagents.

Work: <what it is and who uses it>
Request: <the user's goal in one or two sentences>
Out of scope: <what this run will not change>
Material: <absolute paths to screenshots, labelled by view and theme; repo path and diff command for code>
References: <labelled screenshots of comparable products, or "none">

Score the work, and each reference separately, from 1 to 10 in each category and overall:
<categories; for UI: hierarchy, typography, spacing and layout, color and contrast, iconography, consistency>

For the work only, list the changes that would raise its score most, highest impact first.
Each item: the view or file, what is wrong, the specific fix. Skip changes outside the request.

Reply:
SCORES
<name>: overall <n>/10; <category> <n>/10, ...
FIXES
F1 <view or file>: <problem>. Fix: <change>
```

For a code review, use the categories correctness, simplicity and fit with the surrounding code, and send the diff command instead of screenshots.
