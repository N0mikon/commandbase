---
git_commit: 6227f53
last_updated: 2026-02-06
last_updated_by: planning-code
topic: "Add skills Preloading to Skill Frontmatter"
tags: [plan, implementation, skills, preloading, frontmatter]
status: draft
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

## Success Criteria

- [ ] `/researching-web` confirms `skills` works in SKILL.md frontmatter (GATE)
- [ ] All 3 SKILL.md files have valid `skills` frontmatter
- [ ] Skill invocation still works: test `/starting-projects`, `/implementing-plans`, `/committing-changes`
- [ ] Dependent skills are available during parent skill execution
- [ ] No regressions in skill behavior
- [ ] All edited skills deployed to `~/.claude/skills/`

## Dependencies

- **Blocked by:** Nothing (independent of Phases 1-3)
- **Blocks:** Nothing
