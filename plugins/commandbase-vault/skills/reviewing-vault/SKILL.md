---
name: reviewing-vault
description: "Use this skill when performing periodic vault reviews to surface patterns, track progress, and maintain knowledge freshness. This includes daily note reviews scanning recent additions, weekly synthesis connecting themes across notes, monthly retrospectives identifying stale or orphaned content, and generating review summaries with actionable insights. Activate when the user says 'review vault', 'daily review', 'weekly synthesis', 'what changed this week', or 'vault retrospective'."
---

# Reviewing Vault

You are running periodic reviews on an Obsidian vault to surface patterns, track progress, and maintain knowledge freshness. This skill supports three cadences (daily, weekly, monthly) with temporal rollup — each level builds on findings from shorter cadences.

**Violating the letter of these rules is violating the spirit of these rules.**

## The Iron Law

```
NO REVIEW WITHOUT READING VAULT CLAUDE.MD FIRST
```

The vault CLAUDE.md defines conventions, tag taxonomy, folder structure, and goals. Without reading it, you cannot evaluate what's healthy vs problematic.

**No exceptions:**
- Don't assess tag drift without knowing the taxonomy
- Don't check folder balance without knowing the intended structure
- Don't evaluate orphans without understanding the MOC strategy
- Don't review without a time window — always scope by cadence

## The Gate Function

```
BEFORE producing any review:

1. READ: Vault CLAUDE.md for conventions, goals, structure
2. SCOPE: Determine cadence (daily/weekly/monthly) and time window
3. GATHER: Collect notes created/modified in the time window
4. ANALYZE: Run cadence-appropriate checks from review-cadence-guide.md
5. SYNTHESIZE: Produce actionable review summary
6. ONLY THEN: Present findings with suggested actions

Skip CLAUDE.md read = wrong baselines = misleading review
```

## Initial Response

When invoked, determine the review cadence:

**If cadence is specified:**
```
Running [daily/weekly/monthly] review...
Time window: [start] to [end]
[Read vault CLAUDE.md, then execute the appropriate mode]
```

**If no cadence specified, ask:**

Use AskUserQuestion:
```
question: "What type of vault review would you like?"
options:
  - "Daily review" — scan today's notes, surface quick connections
  - "Weekly synthesis" — detect patterns across this week
  - "Monthly retrospective" — full vault health assessment
```

## Modes

### Mode A: Daily Review

Use this mode for quick daily check-ins on vault activity.

**Steps:**
1. Read vault CLAUDE.md for conventions
2. Find notes created/modified in the last 24 hours
3. Check inbox/triage folder for unrouted items
4. Scan for tasks due today
5. Suggest connections between new notes and existing content
6. Present daily review summary

See ./reference/review-cadence-guide.md "Daily Review" for detailed checks and output format.

### Mode B: Weekly Synthesis

Use this mode for pattern detection and cross-connection discovery across the week.

**Steps:**
1. Read vault CLAUDE.md for conventions
2. Collect all notes from the past 7 days
3. Group by theme/tag clusters
4. Identify cross-connections between notes from different days
5. Check for MOC updates needed
6. Detect orphans and tag drift from this week
7. Present weekly synthesis

See ./reference/review-cadence-guide.md "Weekly Synthesis" for detailed checks and output format.

### Mode C: Monthly Retrospective

Use this mode for comprehensive vault health assessment.

**Steps:**
1. Read vault CLAUDE.md for conventions and goals
2. Compute growth metrics (total notes, monthly additions, rate)
3. Identify stale notes (30+ days untouched)
4. Run orphan census (or delegate to `/linting-vault` Mode B for full analysis)
5. Assess tag health and folder balance
6. Check MOC completeness
7. Evaluate goal alignment if goals are documented
8. Present monthly retrospective with recommended actions

See ./reference/review-cadence-guide.md "Monthly Retrospective" for detailed checks and output format.

## Cross-Skill Delegation

Reviews may surface issues better handled by other skills:

- **Health metrics depth**: Delegate to `/linting-vault` Mode B for full vault lint
- **Connection suggestions**: Delegate to `/connecting-vault` for detailed link analysis
- **Stale note cleanup**: Suggest `/maintaining-vault` for batch operations
- **Inbox routing**: Suggest `/capturing-vault` Mode D for inbox processing

## Output Behavior

Present review results directly in the response. Reviews are informational — they surface findings and suggest actions but don't make changes.

After presenting:
```
Would you like me to save this review to .docs/vault-health/ or act on any of these findings?
```

## Self-Improvement

Before finishing, review this skill execution:

- If errors occurred (tool failures, skill failures, repeated attempts), suggest:
  > **Suggestion**: [N] errors occurred during this execution.
  > Consider running `/extracting-patterns` to capture learnings.
  >
  > Errors: [brief summary of error types]
- Only suggest when errors are meaningful — use judgment about significance.
- Do not auto-run. Suggest only.

## Red Flags - STOP and Verify

If you notice any of these, pause:

- Reviewing without reading vault CLAUDE.md first
- Making changes to notes during a review (reviews are read-only)
- Running a monthly review without scoping the time window
- Ignoring the temporal rollup (weekly should reference daily patterns)
- Presenting raw data without synthesis or actionable suggestions

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "The vault is small, no need for monthly review" | Small vaults benefit from review too. Patterns emerge early. |
| "Tags look fine at a glance" | Check against the taxonomy. Drift is subtle. |
| "No one reads review summaries" | The summary surfaces actions. The user decides what to act on. |
| "I'll just run a quick lint instead" | Linting checks structure. Reviews check meaning and patterns. |
| "Daily review is too frequent" | Daily is quick — 5 notes take 30 seconds to review. |

## The Bottom Line

**Read conventions. Scope by cadence. Surface patterns. Suggest actions.**

Reviews are the vault's feedback loop — they turn raw activity into insight. This is non-negotiable. Every review. Every cadence.
