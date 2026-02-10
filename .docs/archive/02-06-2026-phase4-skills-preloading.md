---
git_commit: 8e92bba
last_updated: 2026-02-09
last_updated_by: docs-updater
last_updated_note: "Archived — plan was deferred (skills preloading not supported in SKILL.md frontmatter) and all newskills/* references now obsolete (moved to plugins/)"
topic: "Add skills Preloading to Skill Frontmatter"
tags: [plan, implementation, skills, preloading, frontmatter]
status: archived
archived: 2026-02-09
archive_reason: "Plan was explicitly deferred (skills frontmatter feature never adopted by Claude Code framework). All referenced newskills/* paths deleted — skills now live under plugins/*/skills/. Codebase has fully migrated to plugin architecture."
references:
  - newskills/starting-projects/SKILL.md
  - newskills/implementing-plans/SKILL.md
  - newskills/committing-changes/SKILL.md
  - .docs/references/framework-docs-snapshot.md
  - .docs/plans/02-06-2026-framework-feature-adoption.md
---

# Phase 4: Add `skills` Preloading to Skill Frontmatter

## Overview

Declare real skill dependencies so they're preloaded when the parent skill runs. Three skills have clear cross-references to other skills that should be declared as dependencies.

## IMPORTANT: Spec Discrepancy — Research Required

**Conflicting evidence on whether `skills` works in SKILL.md frontmatter:**

- **Framework-docs-snapshot.md** (from Context7 MCP, 2026-02-06): Lists `skills` as valid optional SKILL.md frontmatter: "**`skills` preloading**: Load other skills as dependencies in skill frontmatter"
- **Official Claude Code subagents docs** (from web research, 2026-02-06): Documents `skills` only as a subagent frontmatter field for injecting skill content into an agent's context at startup. The skill specification page does not mention `skills` in its frontmatter table.

**Resolution:** `/researching-web` step below must resolve this before implementation. If `skills` only works in agent frontmatter, this phase needs redesign.

## Current State Analysis

### Skills with Cross-References

**1. `starting-projects/SKILL.md`**
- References `/researching-frameworks` at lines 21, 32, 58 (direct invocation)
- Line 58: Delegates to `/researching-frameworks` with tech stack arguments
- Primary dependency — other skills mentioned are workflow overview only

**2. `implementing-plans/SKILL.md`**
- References `/validating-code` at lines 191, 197 (run validation after each phase)
- References `/bookmarking-code` at lines 177, 183, 185, 187, 191, 198 (checkpoint management)

**3. `committing-changes/SKILL.md`**
- References `/reviewing-security` at lines 135, 232 (security review for public repos)

## Desired End State

Each skill declares its dependencies in frontmatter so they're preloaded at invocation time.

### Proposed Changes

**`starting-projects`:**
```yaml
---
name: starting-projects
description: "Use this skill when..."
skills: [researching-frameworks]
---
```

**`implementing-plans`:**
```yaml
---
name: implementing-plans
description: "Use this skill when..."
skills: [validating-code, bookmarking-code]
---
```

**`committing-changes`:**
```yaml
---
name: committing-changes
description: "Use this skill when..."
skills: [reviewing-security]
---
```

## What We're NOT Doing

- Not adding `skills` to every skill that mentions another — only where there's a direct invocation dependency
- Not changing skill body content — frontmatter-only edits
- Not preloading skills that are merely referenced in workflow documentation

## Implementation Approach

Frontmatter-only edits to 3 SKILL.md files. No body changes.

## Changes Required

### 1. `starting-projects/SKILL.md`

Add `skills: [researching-frameworks]` to frontmatter.

### 2. `implementing-plans/SKILL.md`

Add `skills: [validating-code, bookmarking-code]` to frontmatter.

### 3. `committing-changes/SKILL.md`

Add `skills: [reviewing-security]` to frontmatter.

### 4. Deploy

```bash
cp newskills/starting-projects/SKILL.md ~/.claude/skills/starting-projects/SKILL.md
cp newskills/implementing-plans/SKILL.md ~/.claude/skills/implementing-plans/SKILL.md
cp newskills/committing-changes/SKILL.md ~/.claude/skills/committing-changes/SKILL.md
```

## Pre-Implementation Research (REQUIRED)

### `/researching-web`: Verify `skills` in SKILL.md Frontmatter

This research is **mandatory** before implementation due to the spec discrepancy.

- Search: "Claude Code SKILL.md skills frontmatter preloading 2026"
- Search: "Claude Code skill dependencies preload"
- Search: "site:github.com anthropics claude-code skills frontmatter"
- Verify: Does `skills` in SKILL.md frontmatter actually preload dependent skills?
- Verify: Or does `skills` only work in agent `.md` frontmatter?
- Verify: Check Claude Code changelog for when `skills` was added to skill frontmatter (if ever)

**If `skills` only works in agent frontmatter:**
- This phase needs redesign
- Options: (a) document dependencies in body text only (current state), (b) use `context: fork` with agent that has `skills` preloaded, (c) defer until framework adds skill-level `skills` support

### `/researching-frameworks`: Context7 Verification

- Re-query Context7 MCP for the exact SKILL.md frontmatter specification
- Verify whether the `skills` field was documented accurately or was a conflation with agent frontmatter

## Research Result (2026-02-06)

**GATE FAILED.** The `skills` field does NOT work in SKILL.md frontmatter.

### Evidence

- **Official SKILL.md frontmatter reference** (`code.claude.com/docs/en/skills`): Lists 10 valid fields: `name`, `description`, `argument-hint`, `disable-model-invocation`, `user-invocable`, `allowed-tools`, `model`, `context`, `agent`, `hooks`. No `skills` field.
- **Official subagent frontmatter reference** (`code.claude.com/docs/en/sub-agents`): Lists `skills` as an agent-only field: "Skills to load into the subagent's context at startup."
- **Framework-docs-snapshot.md was incorrect**: Context7 MCP conflated agent and skill frontmatter when it listed `skills` as valid SKILL.md frontmatter. This has been corrected.

### Decision: Defer (Option C)

Deferred until Claude Code adds `skills` support to SKILL.md frontmatter. Current state (skills reference each other via `/skill-name` in body text) works fine.

**Revisit when:** Claude Code changelog mentions `skills` in SKILL.md frontmatter, or a new framework-docs research reveals the feature has been added.

## Success Criteria

- [x] `/researching-web` confirms `skills` works in SKILL.md frontmatter (GATE) — **FAILED, phase deferred**
- [ ] ~~All 3 SKILL.md files have valid `skills` frontmatter~~ (N/A - deferred)
- [ ] ~~Skill invocation still works~~ (N/A - deferred)
- [ ] ~~Dependent skills are available during parent skill execution~~ (N/A - deferred)
- [ ] ~~No regressions in skill behavior~~ (N/A - deferred)
- [ ] ~~All edited skills deployed to `~/.claude/skills/`~~ (N/A - deferred)

## Dependencies

- **Blocked by:** Framework support for `skills` in SKILL.md frontmatter (not yet available)
- **Blocks:** Nothing
