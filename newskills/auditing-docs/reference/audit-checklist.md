# Document Audit Checklist

Health checks for each `.docs/` document during audit.

## Checks

| Check | Method | Pass Condition |
|-------|--------|----------------|
| Frontmatter exists | Read first 10 lines | Contains `---` delimiters and YAML content |
| git_commit present | Grep frontmatter | `git_commit:` field exists and is not `n/a` |
| git_commit valid | `git rev-parse` | Commit hash resolves in current repo |
| Commits behind | `git rev-list` | Count of commits between git_commit and HEAD |
| status field | Grep frontmatter | `status:` field present (draft, complete, archived) |
| References exist | `ls` each file | Files listed in `references:` frontmatter still exist |

## Staleness Categories

| Category | Condition | Dashboard Label |
|----------|-----------|-----------------|
| CURRENT | 0-2 commits behind | OK |
| STALE | 3+ commits behind, references exist | STALE |
| OBSOLETE | References deleted, or very old handoff (>30 days + >20 commits behind) | OBSOLETE |
| UNKNOWN | No git_commit frontmatter | UNKNOWN |

## Reference Check

For each file in the document's `references:` frontmatter:
1. Run `ls <path>` to check existence
2. Count: X of Y references still exist
3. If 0 of Y exist: strong signal for OBSOLETE
4. If all exist: references are healthy

## Document Type Expectations

| Directory | Expected Staleness | Notes |
|-----------|-------------------|-------|
| `.docs/plans/` | HIGH risk | Implementation changes diverge from plan |
| `.docs/handoffs/` | HIGH risk | Completed/abandoned work stays active |
| `.docs/research/` | MEDIUM risk | Codebase evolves past findings |
| `.docs/design/` | MEDIUM risk | Architecture decisions get superseded |
| `.docs/debug/` | HIGH risk | Often left behind after bugs are fixed |
| `.docs/learnings/` | LOW risk | Knowledge persists regardless of code changes |
| `.docs/references/` | LOW risk | Framework docs change slowly |
| `.docs/brainstorm/` | LOW risk | Captures preferences, rarely needs update |
