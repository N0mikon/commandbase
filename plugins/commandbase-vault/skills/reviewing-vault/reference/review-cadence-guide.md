# Review Cadence Guide

What to check at each review cadence level, with temporal rollup patterns.

## Daily Review (Mode A)

**Focus:** What happened today? What needs attention?

**Time window:** Last 24 hours (or since last daily review).

### Checks
1. **New notes**: List notes created today. For each: does it have proper frontmatter? Is it linked to anything?
2. **Modified notes**: List notes modified today. What changed? Any broken links introduced?
3. **Inbox/triage**: Are there notes in the inbox/triage folder? Surface them for routing.
4. **Tasks due**: Scan for `- [ ]` items with today's date in frontmatter or body.
5. **Quick connections**: For each new note, suggest 1-2 existing notes that might be related (by shared tags, similar titles, or topic overlap).

### Output Format
```
Daily Review — [date]
=====================
New notes: [N]
- [note name] — [folder] — [tags]

Modified notes: [N]
- [note name] — [what changed]

Inbox items: [N]
- [note name] — suggested destination: [folder]

Tasks due: [N]
- [ ] [task] (from [[note]])

Connection suggestions:
- [[new note]] might relate to [[existing note]] (shared tag: #topic)
```

### Rollup
Daily findings feed into weekly synthesis. Keep track of:
- Notes created per day
- Tags used this week
- Inbox throughput (items in vs routed)

## Weekly Synthesis (Mode B)

**Focus:** What patterns emerged this week? What themes connect?

**Time window:** Last 7 days (or since last weekly review).

### Checks
1. **Volume**: How many notes created/modified this week? Compare to previous week.
2. **Theme clusters**: Group this week's notes by tag or folder. Are any themes dominant?
3. **Cross-connections**: Which notes from different days/topics could be linked?
4. **MOC updates needed**: Have new notes been added to topics that have existing MOCs? Are MOC updates needed?
5. **Orphan check**: Any notes created this week with zero incoming links?
6. **Tag drift**: Any new tags introduced this week? Do they fit the taxonomy?
7. **Stale items**: Notes marked as "in-progress" or "draft" for more than a week.

### Output Format
```
Weekly Synthesis — Week of [date]
=================================
Volume: [N] new, [M] modified (previous week: [X] new, [Y] modified)

Theme clusters:
- #topic-a: [N] notes — [brief summary]
- #topic-b: [N] notes — [brief summary]

Cross-connections suggested:
- [[note-1]] and [[note-2]] — [why they relate]

MOC updates needed:
- [[MOC Name]]: add [[new-note-1]], [[new-note-2]]

Orphans this week: [N]
- [[orphan-note]] — suggested link from [[related-note]]

New tags: [list]
Stale drafts: [N]
```

### Rollup
Weekly findings feed into monthly retrospective. Accumulate:
- Weekly note counts (trend line)
- Theme frequency over weeks
- Orphan rate trend

## Monthly Retrospective (Mode C)

**Focus:** What's the vault's overall health? What needs maintenance?

**Time window:** Last 30 days (or since last monthly review).

### Checks
1. **Growth metrics**: Total notes, notes added this month, growth rate.
2. **Stale notes**: Notes not modified in 30+ days. Which are intentionally stable vs forgotten?
3. **Orphan census**: Full orphan detection across the vault (delegate to /linting-vault if needed).
4. **Tag health**: Tag distribution. Are any tags over- or under-used? Tag drift from taxonomy.
5. **Folder balance**: Note distribution across folders. Any folder growing disproportionately?
6. **MOC completeness**: Are MOCs up to date with their topic's notes?
7. **Link density**: Average links per note. Trend vs previous month.
8. **Goal alignment**: If vault has documented goals, how do this month's additions align?

### Output Format
```
Monthly Retrospective — [month year]
=====================================
Vault size: [N] total notes ([+M] this month, [X]% growth)

Top themes this month:
1. #topic — [N] notes
2. #topic — [N] notes
3. #topic — [N] notes

Stale notes (30+ days untouched): [N]
- [note] — last modified [date]

Orphan notes: [N] ([X]% of vault)
Tag health: [N] unique tags, [M] potential issues
Folder distribution: [summary]
Link density: [avg] links/note (trend: [up/down/stable])

Recommended actions:
- [ ] [action item]
- [ ] [action item]
- [ ] [action item]
```

## Temporal Rollup Pattern

Reviews build on each other:

```
Daily → tracks individual note activity
  ↓ feeds into
Weekly → detects patterns across days, suggests connections
  ↓ feeds into
Monthly → assesses vault-wide health, identifies systemic issues
```

**Key principle:** Each cadence level should reference findings from shorter cadences when available. A weekly review that can read this week's daily reviews is more useful than one that starts from scratch.

## Finding Recent Notes

**By creation date:**
```
Grep("^created:", path=vault_path, glob="*.md")
```
Then filter by date range. Or use file modification timestamps via Glob.

**By modification date:**
Use Glob to find recently modified files (Glob returns results sorted by modification time).

**By folder:**
```
Glob("inbox/**/*.md", path=vault_path)
Glob("daily/**/*.md", path=vault_path)
```

## Connecting to Other Skills

- For detailed health metrics during monthly review: delegate to `/linting-vault` Mode B
- For connection suggestions: delegate to `/connecting-vault`
- For acting on stale notes: suggest `/maintaining-vault`
- For routing inbox items: suggest `/capturing-vault` Mode D (inbox processing)
