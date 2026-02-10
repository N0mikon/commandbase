---
git_commit: 8e92bba
last_updated: 2026-02-09
last_updated_by: docs-updater
last_updated_note: "Bumped git_commit (was 38 commits behind); content verified still accurate, no agents use category field"
topic: "Add category to All Agent Frontmatter"
tags: [plan, implementation, agents, category, organization]
status: archived
archived: 2026-02-09
archive_reason: "Plan was skipped (category not a supported agent frontmatter field) and all newagents/* references deleted — agents moved to plugins/"
references:
  - newagents/code-locator.md          # deleted — agents moved to plugins/
  - newagents/code-librarian.md        # deleted — agents moved to plugins/
  - newagents/code-analyzer.md         # deleted — agents moved to plugins/
  - newagents/docs-locator.md          # deleted — agents moved to plugins/
  - newagents/docs-analyzer.md         # deleted — agents moved to plugins/
  - newagents/docs-updater.md          # deleted — agents moved to plugins/
  - newagents/web-researcher.md        # deleted — agents moved to plugins/
  - .docs/references/framework-docs-snapshot.md
  - .docs/archive/02-06-2026-framework-feature-adoption.md  # moved to archive
---

# Phase 6: Add `category` to All Agent Frontmatter

## Overview

Add `category` field to all agents for organizational clarity, grouping them by function (research, analysis, action).

## IMPORTANT: Spec Discrepancy — Research Required

**Conflicting evidence on whether `category` is a valid agent frontmatter field:**

- **Framework-docs-snapshot.md** (from Context7 MCP, 2026-02-06): Lists `category` as optional agent frontmatter alongside `tools`, `model`, `color`.
- **Official Claude Code subagents docs** (from web research, 2026-02-06): The supported frontmatter fields table lists `name`, `description`, `tools`, `disallowedTools`, `model`, `permissionMode`, `skills`, `hooks`, `memory`. No `category` or `color`.

**Risk level:** Low. If `category` is not recognized, it will be silently ignored — no errors, no breakage. But also no benefit.

**Resolution:** `/researching-web` step below should clarify whether `category` has any runtime effect or is purely informational.

## Current State Analysis

### Agent Frontmatter (all 7 agents)

| Agent | Frontmatter Fields | Has `category`? |
|-------|--------------------|----------------|
| code-locator | name, description, tools, model | No |
| code-librarian | name, description, tools, model | No |
| code-analyzer | name, description, tools, model | No |
| docs-locator | name, description, tools, model | No |
| docs-analyzer | name, description, tools, model | No |
| docs-updater | name, description, tools, model | No |
| web-researcher | name, description, tools, model | No |

All use `model: sonnet` except `docs-updater` which uses `model: opus`.

## Desired End State

All agents have a `category` field for organizational grouping:

| Agent | Category | Rationale |
|-------|----------|-----------|
| code-locator | research | Finds WHERE code lives; read-only tools (Grep, Glob, LS) |
| code-librarian | research | Finds patterns/examples; read-only tools (Grep, Glob, Read, LS) |
| docs-locator | research | Finds documents; read-only tools (Grep, Glob, LS) |
| web-researcher | research | Searches web; read-only tools (WebSearch, WebFetch) |
| code-analyzer | analysis | Analyzes HOW code works; read-only tools (Read, Grep, Glob, LS) |
| docs-analyzer | analysis | Extracts insights from docs; read-only tools (Read, Grep, Glob, LS) |
| docs-updater | action | Modifies files; write tools (Read, Grep, Glob, LS, Edit, Bash) |
| docs-writer | action | Creates .docs/ files (new in Phase 2, already has `category: action` if we add it during creation) |

## What We're NOT Doing

- Not adding `color` — confirmed not in current spec, purely cosmetic
- Not changing any other frontmatter fields
- Not changing agent body content — frontmatter-only edits

## Implementation Approach

Add one line (`category: <value>`) to each agent's frontmatter. No body changes.

## Changes Required

### 1. Research Agents (4 files)

**`newagents/code-locator.md`** — Add `category: research`
**`newagents/code-librarian.md`** — Add `category: research`
**`newagents/docs-locator.md`** — Add `category: research`
**`newagents/web-researcher.md`** — Add `category: research`

### 2. Analysis Agents (2 files)

**`newagents/code-analyzer.md`** — Add `category: analysis`
**`newagents/docs-analyzer.md`** — Add `category: analysis`

### 3. Action Agents (1 existing + 1 new)

**`newagents/docs-updater.md`** — Add `category: action`
**`newagents/docs-writer.md`** — Include `category: action` during Phase 2 creation

### 4. Deploy

```bash
cp newagents/*.md ~/.claude/agents/
```

## Pre-Implementation Research (REQUIRED)

### `/researching-web`: Verify `category` Field

This research is **mandatory** before implementation due to the spec discrepancy.

- Search: "Claude Code agent category frontmatter 2026"
- Search: "Claude Code subagent frontmatter fields supported"
- Search: "site:github.com anthropics claude-code agent category"
- Verify: Is `category` recognized by Claude Code, or silently ignored?
- Verify: Does `category` affect agent discovery, listing (`/agents` command), or delegation?
- Verify: Has `category` been removed from the spec, or was it never officially supported?
- Verify: Are there alternative approaches to agent organization (e.g., naming convention, description keywords)?

**Decision gate:** If `category` is confirmed unsupported:
- Option A: Add it anyway as self-documentation (zero risk, zero runtime benefit)
- Option B: Skip this phase entirely
- Option C: Use description keywords instead for organizational signals

## Success Criteria

- [x] `/researching-web` clarifies `category` field status (GATE) — **RESULT: Not a supported field**
- [x] Decision gate resolved: **Skip implementation** — `category` is community-invented, not in official spec
- [x] Framework-docs-snapshot.md corrected to remove inaccurate `category`/`color` fields
- [x] Research documented at `.docs/research/02-06-2026-agent-category-frontmatter-validity.md`
- [ ] ~~All 8 agents have `category` field in frontmatter~~ — Skipped (field not supported)
- [ ] ~~Agent invocation still works~~ — Skipped (no changes made to agents)
- [ ] ~~All edited agents deployed~~ — Skipped (no changes made to agents)

## Dependencies

- **Blocked by:** Nothing (independent of all other phases; Phase 2 creates docs-writer with category already)
- **Blocks:** Nothing
