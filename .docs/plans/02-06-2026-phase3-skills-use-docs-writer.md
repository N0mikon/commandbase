---
git_commit: 6227f53
last_updated: 2026-02-06
last_updated_by: planning-code
topic: "Update Skills to Use docs-writer Agent"
tags: [plan, implementation, skills, docs-writer, refactor]
status: implemented
references:
  - newskills/researching-code/SKILL.md
  - newskills/researching-web/SKILL.md
  - newskills/researching-frameworks/SKILL.md
  - newskills/planning-code/SKILL.md
  - newskills/handing-over/SKILL.md
  - newskills/debugging-code/SKILL.md
  - .docs/plans/02-06-2026-phase2-docs-writer-agent.md
  - .docs/plans/02-06-2026-framework-feature-adoption.md
---

# Phase 3: Update Skills to Use `docs-writer` Agent

## Overview

Replace direct Write calls in 6 doc-creating skills with delegation to `docs-writer`. Each skill will still define its own body section structure, but frontmatter generation and file creation move to the agent.

## Current State Analysis

### Skills That Write to `.docs/`

| Skill | Output Directory | Template File | Frontmatter Location |
|-------|-----------------|---------------|---------------------|
| `researching-code` | `.docs/research/` | `templates/research-document-template.md` | In template |
| `researching-web` | `.docs/research/` | `templates/web-research-document-template.md` | In template (non-standard YAML code block!) |
| `researching-frameworks` | `.docs/references/` | `templates/framework-research-template.md` | In template |
| `planning-code` | `.docs/plans/` | `templates/plan-template.md` | In template |
| `handing-over` | `.docs/handoffs/` | None (inline in SKILL.md:76-145) | Inline in SKILL.md |
| `debugging-code` | `.docs/debug/` | `templates/debug-session-template.md` | In template |

**NOT updating:** `learning-from-sessions` — writes to `~/.claude/skills/`, not `.docs/`. Different format entirely.

### Change Pattern

Each skill changes from:
```
Write findings to `.docs/research/MM-DD-YYYY-description.md`
[inline frontmatter template]
[inline section template]
```

To:
```
When ready to save findings, spawn a docs-writer agent via Task:
- doc_type: "research"
- topic: "<research topic>"
- tags: [research, <relevant-tags>]
- content: <your compiled findings as markdown>
- references: [<key files>] (optional)

The agent handles frontmatter, naming, and file creation.
```

### What Each Skill Keeps

Each skill still defines its OWN body sections (content structure). The `docs-writer` agent only handles frontmatter + file creation:

- `researching-code`: Summary, Detailed Findings, Code References, Architecture Notes, Open Questions
- `researching-web`: Summary, Detailed Findings, Source Conflicts, Currency Assessment, Open Questions
- `researching-frameworks`: Framework Docs Snapshot, Dependency Compatibility, Architecture Decisions
- `planning-code`: Overview, Current State, Phases, Success Criteria
- `handing-over`: What I Was Working On, What I Accomplished, Key Learnings, Files Changed, Next Steps
- `debugging-code`: Current Focus, Symptoms, Eliminated, Evidence, Resolution

## Desired End State

- All 6 skills delegate `.docs/` file creation to `docs-writer`
- No skill contains its own frontmatter template
- Each skill still defines its own body section structure
- All `.docs/` output files have identical frontmatter format
- `researching-web` no longer uses embedded YAML code fence format

## What We're NOT Doing

- Not changing body section templates — only removing frontmatter from them
- Not changing skill logic or behavior — only the file creation mechanism
- Not updating `learning-from-sessions` — different output target

## Implementation Approach

For each skill:
1. Edit SKILL.md: replace Write-to-docs instructions with docs-writer delegation instructions
2. Edit template file: remove frontmatter template, keep body sections
3. Special case: `handing-over` has inline template — extract body sections, replace with delegation

## Changes Required

### 1. `researching-code`

**Files to edit:**
- `newskills/researching-code/SKILL.md` (lines ~103-107) — Replace Write instructions with docs-writer delegation
- `newskills/researching-code/templates/research-document-template.md` (lines ~20-29) — Remove frontmatter, keep body sections

### 2. `researching-web`

**Files to edit:**
- `newskills/researching-web/SKILL.md` (lines ~126-129) — Replace Write instructions with docs-writer delegation
- `newskills/researching-web/templates/web-research-document-template.md` (lines ~23-42) — Remove embedded YAML code block frontmatter, keep body sections

### 3. `researching-frameworks`

**Files to edit:**
- `newskills/researching-frameworks/SKILL.md` (lines ~174-183) — Replace Write instructions with docs-writer delegation
- `newskills/researching-frameworks/templates/framework-research-template.md` (lines ~8-13, ~89-92) — Remove frontmatter from both sub-templates, keep body sections

### 4. `planning-code`

**Files to edit:**
- `newskills/planning-code/SKILL.md` (lines ~149-153) — Replace Write instructions with docs-writer delegation
- `newskills/planning-code/templates/plan-template.md` (lines ~6-15) — Remove frontmatter, keep body sections

### 5. `handing-over`

**Files to edit:**
- `newskills/handing-over/SKILL.md` (lines ~62-145) — Replace inline template with:
  1. Body section template (kept)
  2. docs-writer delegation instructions (new)
  - Consider extracting to `templates/handover-template.md` for consistency

### 6. `debugging-code`

**Files to edit:**
- `newskills/debugging-code/SKILL.md` (lines ~77-88) — Replace Write instructions with docs-writer delegation
- `newskills/debugging-code/templates/debug-session-template.md` (lines ~15-20) — Remove frontmatter, keep body sections and mutation rules

### 7. Deploy All

```bash
# Copy all edited skills
cp newskills/researching-code/SKILL.md ~/.claude/skills/researching-code/SKILL.md
cp newskills/researching-code/templates/*.md ~/.claude/skills/researching-code/templates/
cp newskills/researching-web/SKILL.md ~/.claude/skills/researching-web/SKILL.md
cp newskills/researching-web/templates/*.md ~/.claude/skills/researching-web/templates/
cp newskills/researching-frameworks/SKILL.md ~/.claude/skills/researching-frameworks/SKILL.md
cp newskills/researching-frameworks/templates/*.md ~/.claude/skills/researching-frameworks/templates/
cp newskills/planning-code/SKILL.md ~/.claude/skills/planning-code/SKILL.md
cp newskills/planning-code/templates/*.md ~/.claude/skills/planning-code/templates/
cp newskills/handing-over/SKILL.md ~/.claude/skills/handing-over/SKILL.md
cp newskills/debugging-code/SKILL.md ~/.claude/skills/debugging-code/SKILL.md
cp newskills/debugging-code/templates/*.md ~/.claude/skills/debugging-code/templates/
```

## Pre-Implementation Research

### `/researching-web`: Agent Delegation Patterns

- Search: "Claude Code skill delegate to agent Task tool pattern 2026"
- Search: "Claude Code docs-writer agent delegation example"
- Verify: What's the best way for a skill to pass structured data to an agent via Task tool?
- Verify: Does the agent receive the full prompt or just a summary?

### `/researching-code`: Current Write Patterns

- Read each skill's SKILL.md to confirm exact line numbers for Write instructions
- Read each template to confirm exact frontmatter boundaries
- Identify any edge cases (e.g., `researching-frameworks` writes 3 files — does docs-writer need to handle multiple files per invocation?)

## Success Criteria

- [x] All 6 skills delegate file creation to `docs-writer`
- [x] No skill contains its own frontmatter template
- [x] Each skill still defines its own body section structure
- [x] Output files from all skills have identical frontmatter format
- [x] `researching-web` no longer uses embedded YAML code fence format
- [ ] Test: run `/researching-code` — produces `.docs/research/` file with standard frontmatter
- [ ] Test: run `/researching-web` — produces `.docs/research/` file with standard frontmatter
- [ ] Test: run `/handing-over` — produces `.docs/handoffs/` file with standard frontmatter
- [x] All edited skills deployed to `~/.claude/skills/`

## Dependencies

- **Blocked by:** Phase 2 (docs-writer agent must exist first)
- **Blocks:** Nothing
