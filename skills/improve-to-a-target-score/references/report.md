# Score report

When the work ends in a pull request, edit its description, not a comment, to add this section before the closing model line. Otherwise put it in the final reply.

```markdown
## Score rounds

Target: 9/10 from every member. Rounds: 3

| Judge | Round 0 | Round 1 | Round 2 | Round 3 |
| --- | --- | --- | --- | --- |
| Claude Opus | 6/10 | 8/10 | 8.5/10 | 9/10 |
| GPT Sol | 6.5/10 | 8/10 | 9/10 | 9/10 |
| Gemini Pro | 6/10 | 7.5/10 | 8.5/10 | 9/10 |
| Reference: <product> (mean) | 8.3/10 | 8.5/10 | 8.8/10 | 9/10 |
```

For a program ruler, use one row per metric and the gate's result per round.

Write `no score` where a member gave none; never invent one. Leave out scores from non-blocking members. Below the table, list what changed in each round, the declined findings with reasons, before and after screenshots or measurements, and usage or cost if the client exposed it.
