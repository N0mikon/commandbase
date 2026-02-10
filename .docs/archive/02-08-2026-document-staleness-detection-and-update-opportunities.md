---
date: 2026-02-08
status: complete
topic: "Document Staleness Detection and Update Opportunities"
tags: [research, docs-updater, staleness, skills, agents, document-lifecycle]
git_commit: 8e92bba
last_updated: 2026-02-09
last_updated_by: docs-updater
last_updated_note: "Frontmatter refresh - updated references to current plugin paths, bumped git_commit from e35080c (23 commits behind)"
archived: 2026-02-09
archive_reason: "Research fully implemented in commit e4648b4 (auditing-docs skill + 4 upstream auto-update integrations). All referenced files moved from newagents/newskills/ to plugins/ during marketplace restructure (commit 87a19a3). Document value is historical only."
references:
  - plugins/commandbase-core/agents/docs-updater.md
  - plugins/commandbase-git-workflow/skills/committing-changes/SKILL.md
  - plugins/commandbase-code/skills/implementing-plans/SKILL.md
  - plugins/commandbase-core/agents/docs-writer.md
  - plugins/commandbase-core/agents/docs-analyzer.md
  - plugins/commandbase-core/agents/docs-locator.md
  - plugins/commandbase-git-workflow/skills/auditing-docs/SKILL.md
---

# Document Staleness Detection and Update Opportunities

**Date**: 2026-02-08
**Branch**: master

## Research Question

Two questions investigated:
1. What would a new skill for methodically checking old documents one-by-one look like? What exists today and what gaps would it fill?
2. Where could docs-updater be called more frequently to prevent documents from going stale?

## Summary

The codebase has a mature document lifecycle system with 10+ `.docs/` subdirectories, 4 specialized agents (docs-writer, docs-updater, docs-analyzer, docs-locator), and 20+ skills that create/read documents. However, docs-updater is only invoked in **2 places** — `/committing-changes` and `/implementing-plans` — and both are reactive (triggered by other workflows). There is no proactive, standalone mechanism to audit document health across the full `.docs/` directory.

## Detailed Findings

### Current docs-updater Integration Points

**Entry Point 1: `/committing-changes` (Step 2, lines 62-93)**
- Trigger: Automatic pre-commit gate
- Scope: All tracked `.docs/*.md` files with `git_commit` frontmatter
- Threshold: Only flags docs >5 commits behind HEAD
- User control: yes/skip/pick options
- Limitation: Only runs during commits — if you go many sessions without committing, staleness accumulates silently

**Entry Point 2: `/implementing-plans` (lines 186-194)**
- Trigger: At start and end of plan implementation
- Scope: Only `.docs/` files referenced in the plan being implemented
- Limitation: Only checks plan-referenced docs, not the full `.docs/` directory

### The Four Document Agents

| Agent | Role | Staleness Detection | Write Access |
|-------|------|---------------------|--------------|
| **docs-writer** | Creates new documents | None (records git_commit only) | Yes |
| **docs-updater** | Updates stale or archives obsolete docs | Active (git_commit comparison + reference checks) | Yes |
| **docs-analyzer** | Extracts insights from docs | Passive (reports commits behind) | No |
| **docs-locator** | Finds relevant docs by topic | Awareness only (notes dates) | No |

### Gap Analysis: What's Missing

**Problem 1: No standalone document audit skill**
- No skill exists to methodically walk through all documents, assess each one, and update/archive as needed
- The closest is `/committing-changes` Step 2, but it's embedded in the commit flow and uses a >5 commit threshold
- There's no way to say "review all my docs for freshness" as a standalone operation

**Problem 2: docs-updater is under-called**
- Only 2 invocation points across 40+ skills
- Skills that READ documents never check freshness before trusting content:
  - `/taking-over` reads handoffs without staleness check
  - `/planning-code` reads upstream research/design/structure docs without checking
  - `/designing-code` reads research artifacts without checking
  - `/structuring-code` reads design docs without checking
  - `/starting-projects` reads framework reference docs without checking
  - `/importing-vault` reads all `.docs/` types without checking
  - `/resuming-sessions` reads handoffs and learnings without checking
- These skills could be reading outdated information and making decisions based on stale context

### Staleness Detection Mechanism

The detection algorithm (from `committing-changes/SKILL.md:67-76`):
1. Find all `.md` files in `.docs/`
2. Filter to git-tracked files only
3. Extract `git_commit:` from frontmatter (first 10 lines)
4. Skip files without commit hash or with `n/a`
5. Count commits between doc's commit and HEAD via `git rev-list`
6. Report files that are behind, sorted by staleness

The docs-updater agent then performs deeper analysis:
- Checks if referenced files still exist
- Runs `git diff --name-only <commit>..HEAD` to see what changed
- Decides: UPDATE (content still relevant) or ARCHIVE (obsolete/superseded)

### Document Types That Go Stale

| Type | Directory | Staleness Risk | Why |
|------|-----------|---------------|-----|
| Plans | `.docs/plans/` | HIGH | Implementation changes diverge from plan |
| Research | `.docs/research/` | MEDIUM | Codebase evolves past findings |
| Handoffs | `.docs/handoffs/` | HIGH | Completed/abandoned work stays as active handoffs |
| References | `.docs/references/` | LOW | Framework docs change slowly |
| Design | `.docs/design/` | MEDIUM | Architecture decisions get superseded |
| Structure | `.docs/structure/` | MEDIUM | File layout changes during implementation |
| Brainstorm | `.docs/brainstorm/` | LOW | Captures preferences, rarely needs update |
| Debug | `.docs/debug/` | HIGH | Often left behind after bugs are fixed |
| Refactors | `.docs/refactors/` | HIGH | Scope changes as refactor progresses |
| Learnings | `.docs/learnings/` | LOW | Knowledge persists regardless of code changes |

## Opportunity 1: New `/auditing-docs` Skill

A standalone skill for methodically reviewing all documents would fill the gap. It would:

- Walk every `.docs/` subdirectory
- For each document: run staleness detection, spawn docs-updater one-by-one
- Present results as a summary dashboard
- Give the user control over each update/archive decision
- Track progress through the audit (useful for large `.docs/` directories)

This is fundamentally different from the existing integration points because:
- It's proactive (user-initiated review) not reactive (embedded in another workflow)
- It covers ALL documents, not just tracked/plan-referenced ones
- It's methodical — one document at a time with user decisions
- It provides a holistic view of document health

## Opportunity 2: Adding docs-updater Calls to Existing Skills

Skills that read upstream documents could check freshness before trusting the content:

**High-value integration points:**
1. `/taking-over` — Before resuming from a handoff, check if the handoff is stale
2. `/planning-code` — Before using research/design/structure docs as input, verify they're current
3. `/designing-code` — Before reading research artifacts, check freshness
4. `/resuming-sessions` — Before loading handoffs and learnings, check freshness

**Medium-value integration points:**
5. `/structuring-code` — Before reading design docs as input
6. `/starting-projects` — Before reading framework reference docs
7. `/importing-vault` — Before importing docs to vault, verify freshness

**Implementation pattern for each:**
- Before reading the upstream doc, run the staleness detection script
- If stale (>5 commits behind), warn the user: "This document is N commits behind HEAD. Update before proceeding?"
- If yes: spawn docs-updater, then continue with updated doc
- If skip: continue with stale doc (user's choice)

## Code References

- `newagents/docs-updater.md:1-181` — Full agent definition
- `newagents/docs-writer.md` — Document creation agent (records git_commit)
- `newagents/docs-analyzer.md` — Read-only analysis agent (reports staleness passively)
- `newagents/docs-locator.md` — Document discovery agent
- `newskills/committing-changes/SKILL.md:62-93` — Stale doc detection + docs-updater spawn
- `newskills/implementing-plans/SKILL.md:186-194` — Plan-scoped staleness check

## Architecture Notes

- The `git_commit` frontmatter field is the cornerstone of staleness detection — written by docs-writer at creation time
- docs-updater refreshes `git_commit` to current HEAD after updates
- The `.docs/archive/` directory exists as a destination for obsolete docs but is only created by docs-updater
- No skill currently creates or manages `.docs/archive/` directly

## Open Questions

1. Should the new audit skill run docs-updater sequentially (one at a time with user approval) or batch (assess all, present dashboard, then execute)?
2. Should upstream-reading skills hard-gate on staleness (refuse to proceed with stale docs) or soft-warn (proceed but note the risk)?
3. What staleness threshold makes sense for the audit skill? The current >5 commits may be too generous for an explicit audit.
4. Should the audit skill also check for orphaned documents (docs whose referenced files were all deleted)?
