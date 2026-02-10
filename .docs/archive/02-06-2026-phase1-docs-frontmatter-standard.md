---
git_commit: 8e92bba
last_updated: 2026-02-09
last_updated_by: docs-updater
last_updated_note: "Updated after 37 commits - bumped git_commit to current HEAD; corrected reference path for archived framework-feature-adoption plan"
topic: "Define Shared .docs/ Frontmatter Standard"
tags: [plan, implementation, frontmatter, docs, standards]
status: archived
archived: 2026-02-09
archive_reason: "Fully implemented 29 commits ago (df48ed0). Standard is in active use across all .docs/ files. Superseded by the docs-writer agent (Phase 2) which now enforces this standard at write time."
references:
  - .docs/research/02-06-2026-framework-spec-vs-implementation-audit.md
  - .docs/archive/02-06-2026-framework-feature-adoption.md
---

# Phase 1: Define Shared `.docs/` Frontmatter Standard

## Overview

Establish a single frontmatter standard that all `.docs/` output files follow, eliminating the inconsistencies found across 7 skills that write to `.docs/`.

This phase defines the standard only. Phase 2 creates the `docs-writer` agent that enforces it.

## Current State Analysis

### Inconsistencies Found (from audit research)

| Issue | Current State |
|-------|--------------|
| Frontmatter format | 6 skills use YAML `---`, `researching-web` uses embedded YAML in code fence |
| Date field names | `last_updated`, `date_searched`, `date_researched`, `created`/`updated` |
| Date formats | `YYYY-MM-DD` in some frontmatter, `MM-DD-YYYY` in others |
| `git_commit` | Only 3/7 skills include it |
| `status` values | `complete`, `current`, `draft`, `approved`, `active`, 5-state enum |
| `tags` | 5/7 include, 2 don't |
| `references` | 3/7 include, 4 don't |

### Current Frontmatter by Skill

| Skill | Fields Used | Non-Standard |
|-------|-------------|-------------|
| `researching-code` | git_commit, last_updated, last_updated_by, topic, tags, status, references | None |
| `researching-web` | date_searched, topic, tags, status, query_decomposition, sources | YAML code block instead of `---` delimiters; unique fields |
| `researching-frameworks` | date_researched, sources, primary_framework, status | Different date field name; no git_commit, tags, references |
| `planning-code` | git_commit, last_updated, last_updated_by, topic, tags, status, references | None (closest to ideal) |
| `handing-over` | git_commit, last_updated, last_updated_by, topic, tags, status, references | None (closest to ideal) |
| `debugging-code` | status, trigger, created, updated | ISO timestamps; no git_commit, tags, topic, references |

## Desired End State

A documented frontmatter standard that:
1. Covers all 5 doc types (research, plans, handoffs, references, debug)
2. Uses consistent field names and date formats
3. Distinguishes required from optional fields
4. Defines valid `status` values per doc type

### The Standard

```yaml
---
date: YYYY-MM-DD           # required — creation date, ISO format
status: <type-specific>     # required — see status values per doc type
topic: "<description>"      # required — what this document is about
tags: [<type>, ...]         # required — first tag is doc type, rest are topic tags
git_commit: <short-hash>    # optional — HEAD at time of creation
references: [<file-paths>]  # optional — key files this doc covers/modifies
---
```

**Status values by doc type:**
- `research`: `complete`
- `plans`: `draft` -> `approved` -> `implemented`
- `handoffs`: `active` -> `superseded`
- `references`: `current` -> `stale`
- `debug`: `gathering` -> `investigating` -> `fixing` -> `verifying` -> `resolved`

**File naming:** `MM-DD-YYYY-description.md` (kebab-case) for all date-prefixed docs.

**Title format:** `# [Topic]` (no prefix like "Research:" — let frontmatter `tags` identify the type).

### Key Design Decisions

- **`date` instead of `last_updated`/`date_searched`/`date_researched`/`created`**: One field, one name.
- **`topic` is required**: Forces every doc to have a searchable description.
- **`tags` first element is doc type**: Enables filtering by type without parsing file path.
- **`git_commit` is optional**: Not all contexts have meaningful git state (e.g., web research).
- **`references` is optional**: Debug sessions and web research rarely reference specific files.
- **Dropped fields**: `last_updated_by`, `query_decomposition`, `sources`, `primary_framework`, `trigger` — these are content-specific and belong in the body, not frontmatter.

## What We're NOT Doing

- Not updating existing `.docs/` files to the new standard (that's a separate cleanup task)
- Not enforcing the standard via hooks or validation (the `docs-writer` agent in Phase 2 handles this)
- Not changing body section templates (each skill keeps its own body structure)

## Implementation Approach

The standard is encoded in the `docs-writer` agent system prompt (Phase 2). This phase only defines and documents the standard — no code changes.

## Changes Required

### 1. Document the Standard

The standard definition above will be embedded in the `docs-writer` agent system prompt (Phase 2). No separate "standard document" file is needed — the agent IS the standard.

## Pre-Implementation Research

### `/researching-web`: Frontmatter Best Practices

Before finalizing, verify current best practices:

- Search: "YAML frontmatter standards documentation 2026"
- Search: "Claude Code docs output frontmatter conventions"
- Verify: Is there a community convention we should align with?
- Verify: Are there any frontmatter parsing issues with the proposed field names?

## Success Criteria

- [x] Standard is documented (in this plan and ready for Phase 2 agent prompt)
- [x] Standard covers all 5 doc types (research, plans, handoffs, references, debug)
- [x] All current skill frontmatter fields are accounted for (either standardized or moved to body)
- [x] No ambiguity in field names, date formats, or status values

## Dependencies

- **Blocked by:** Nothing
- **Blocks:** Phase 2 (docs-writer agent), Phase 3 (skill updates)
