## Finding Deduplication

When multiple reviewers report issues at the same location:

### Merge Rules

1. **Same file:line, same issue** — Merge into one finding, credit all reviewers
2. **Same file:line, different issues** — Keep as separate findings
3. **Same issue, different locations** — Keep separate but cross-reference
4. **Conflicting severity** — Use the higher severity rating
5. **Conflicting recommendations** — Include both with reviewer attribution

### Deduplication Process

```
For each finding in all reviewer reports:
  1. Check if another finding references the same file:line
  2. If yes, check if they describe the same issue
  3. If same issue: merge, keeping the more detailed description
  4. If different issue: keep both, tag as "co-located"
  5. Use highest severity among merged findings
```
