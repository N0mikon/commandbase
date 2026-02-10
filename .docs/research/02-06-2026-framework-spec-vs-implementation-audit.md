---
date: 02-06-2026
last_updated: 2026-02-09
last_updated_by: docs-updater
last_updated_note: "Added git_commit frontmatter; updated counts (24->46 skills, 7->8 agents, 1->5 hooks); updated paths from newskills/newagents/newhooks to plugins/; updated recommendations to reflect partial adoption of allowed-tools, PreCompact, SessionStart, PostToolUseFailure, and Stop hooks"
git_commit: 8e92bba
topic: Framework spec vs current implementation audit
sources: [framework-docs-snapshot.md, dependency-compatibility.md, architecture-decisions.md, deployed skills/agents/hooks]
references:
  - plugins/commandbase-core/skills/
  - plugins/commandbase-code/skills/
  - plugins/commandbase-vault/skills/
  - plugins/commandbase-services/skills/
  - plugins/commandbase-research/skills/
  - plugins/commandbase-git-workflow/skills/
  - plugins/commandbase-session/skills/
  - plugins/commandbase-meta/skills/
  - plugins/commandbase-core/agents/
  - plugins/commandbase-code/agents/
  - plugins/commandbase-research/agents/
  - plugins/commandbase-git-workflow/hooks/hooks.json
  - plugins/commandbase-session/hooks/hooks.json
  - .docs/references/framework-docs-snapshot.md
  - .docs/references/dependency-compatibility.md
  - .docs/references/architecture-decisions.md
---

# Framework Spec vs Implementation Audit

Research comparing the Claude Code skills/agents/hooks spec (from Context7 research) against our current commandbase implementations to identify gaps, compliance issues, and adoption opportunities.

## Executive Summary

**Original audit (Feb 6):** 24 skills, 7 agents, 1 hook -- all compliant with the core spec.

**Current state (Feb 9):** 46 skills across 8 plugins, 8 agents across 3 plugins, 5 hooks across 2 plugins. Plugin marketplace conversion restructured all paths from `newskills/`/`newagents/`/`newhooks/` to `plugins/<plugin>/skills|agents|hooks/`.

**Key finding:** We now use 1 of 6 advanced skill features (`allowed-tools` on `reviewing-security`), 4 of 12 hook events (PostToolUse, PreCompact, SessionStart, PostToolUseFailure, Stop), and 0 of 3 advanced agent features. Several original recommendations have been partially adopted.

## 1. Skills Audit (46 skills across 8 plugins)

### Compliance: 100%

| Check | Result |
|-------|--------|
| Naming (kebab-case gerund) | 46/46 pass |
| Description formula ("Use this skill when...") | 46/46 pass |
| Required frontmatter (name, description) | 46/46 pass |
| Progressive disclosure (reference/, templates/) | Used by several skills |

### Advanced Features Adoption

| Feature | Available Since | Currently Used | Assessment |
|---------|----------------|----------------|------------|
| `context: fork` | Current spec | 0/46 skills | **Still worth evaluating** -- could prevent context pollution from heavy research skills |
| `skills` preloading | Current spec | 0/46 skills | **Still worth adopting** -- `starting-projects` calls `researching-frameworks`; should declare dependency |
| `hooks` in frontmatter | Current spec | 0/46 skills | Low priority -- no clear use case yet |
| `allowed-tools` | Current spec | **1/46 skills** | **Partially adopted** -- `reviewing-security` uses `allowed-tools: Read, Grep, Glob, LS, Bash, AskUserQuestion` |
| `disable-model-invocation` | Current spec | 0/46 skills | Low priority -- current auto-invocation behavior is fine |
| `agent` frontmatter key | Current spec | 0/46 skills | Low priority -- unclear benefit |

### Recommendations for Skills

1. **Add `skills` preloading** where composition exists (still not adopted):
   - `starting-projects` -> depends on `researching-frameworks`
   - `implementing-plans` -> depends on `validating-code`
   - `committing-changes` -> depends on `reviewing-security` (for public repos)

2. **Evaluate `context: fork`** for heavy-context skills (still not adopted):
   - `researching-code` -- spawns many subagents, could pollute context
   - `debating-options` -- parallel research could benefit from isolation
   - `researching-frameworks` -- external doc fetching could pollute context

3. **Expand `allowed-tools`** adoption (partially done):
   - `reviewing-security` -- DONE (uses `Read, Grep, Glob, LS, Bash, AskUserQuestion`)
   - `researching-code` -> restrict to `Read, Grep, Glob, LS, Task` (no Edit/Write/Bash) -- still pending
   - `researching-web` -> restrict to `WebSearch, WebFetch, Task` -- still pending

## 2. Agents Audit (8 agents across 3 plugins)

### Compliance: 100%

| Check | Result |
|-------|--------|
| Naming (noun-form kebab-case) | 8/8 pass |
| Description (delegation trigger pattern) | 8/8 pass |
| Body structure (role, process, deliverables) | 8/8 pass |
| Model selection (appropriate for task) | 8/8 pass |
| Plugin packaging (plugins/<plugin>/agents/) | 8/8 pass |

### Agent Distribution by Plugin

| Plugin | Agents |
|--------|--------|
| commandbase-core | docs-analyzer, docs-locator, docs-updater, docs-writer |
| commandbase-code | code-analyzer, code-librarian, code-locator |
| commandbase-research | web-researcher |

### Advanced Features Not Used

| Feature | Currently Used | Assessment |
|---------|----------------|------------|
| `category` | 0/8 agents | Low priority -- no UI benefit confirmed; nice-to-have for organization |
| `color` | 0/8 agents | Low priority -- cosmetic |
| Proactive invocation | Partially -- descriptions support it | Working as designed |

### Recommendations for Agents

1. **Add `category` field** for organizational clarity (still not adopted):
   - `category: "research"` -> code-locator, code-librarian, docs-locator, web-researcher
   - `category: "analysis"` -> code-analyzer, docs-analyzer
   - `category: "action"` -> docs-updater, docs-writer

2. **No other changes needed** -- agents are fully compliant and well-structured.

## 3. Hooks Audit (5 hooks across 2 plugins, plus deny rules)

### Compliance: Valid implementation

| Check | Result |
|-------|--------|
| JSON stdin parsing | Correct (with error handling) |
| Exit code discipline | Correct (0=allow, 2=feedback) |
| Self-block avoidance | Correctly uses PostToolUse instead of PreToolUse |
| Windows/MINGW compat | Correct (`bash -c` wrapper for tilde expansion) |
| Plugin packaging | Both plugins use hooks.json manifests |

### Hook Distribution by Plugin

| Plugin | Events Used | Scripts |
|--------|-------------|---------|
| commandbase-git-workflow | PostToolUse | `nudge-commit-skill.py` |
| commandbase-session | PostToolUseFailure, Stop, PreCompact, SessionStart | `track-errors.py`, `harvest-errors.py`, `trigger-learning.py`, `detect-session.py` |

### Hook Event Coverage (updated)

| Event | Used | Implementation | Priority |
|-------|------|----------------|----------|
| PostToolUse | **Yes** | Commit workflow nudging (git-workflow plugin) | Implemented |
| PostToolUseFailure | **Yes** | Error tracking (session plugin) | **Implemented since original audit** |
| Stop | **Yes** | Error harvesting at session end (session plugin) | **Implemented since original audit** |
| PreCompact | **Yes** | Trigger learning before compaction (session plugin) | **Implemented since original audit** |
| SessionStart | **Yes** | Session detection (session plugin) | **Implemented since original audit** |
| PreToolUse | No | Could add pre-execution validation | Medium -- risk of deadlock |
| UserPromptSubmit | No | Validate/transform user input | Low -- no clear use case |
| SubagentStop | No | Validate subagent output | Low -- no clear use case |
| Notification | No | Log/transform notifications | Low |
| SessionEnd | No | Cleanup actions | Low |
| SubagentStart | No | Monitor subagent spawning | Low |
| PermissionRequest | No | Auto-approve patterns | Low |

### TypeScript SDK Migration Assessment

| Factor | Python (Current) | TypeScript SDK |
|--------|-----------------|----------------|
| Dependency | Python 3.8+ (already available) | Adds Node.js 18+ and tsx |
| Type safety | None (convention-based) | Full TypeScript types + Zod validation |
| Testing | Manual stdin piping | `runHookCaller` utility |
| Boilerplate | Manual JSON parsing per hook | `preToolRejectHook`, `postToolUpdateFileHook` |
| Maintenance | Simple, minimal | More structured but heavier |

**ADR-002 reassessment:** We now have 5 Python hooks (exceeding the "revisit at 3+" threshold). The boilerplate is being duplicated across scripts. TypeScript SDK migration should be actively evaluated.

### Recommendations for Hooks

1. ~~**Consider PreCompact hook**~~ -- DONE. Implemented in `commandbase-session` plugin as `trigger-learning.py`.

2. **Evaluate TypeScript SDK migration** -- With 5 hooks now in production, the boilerplate argument against migration is weaker. The duplicate JSON parsing and error handling across 5 scripts could benefit from the SDK's typed helpers.

3. **Document the false-positive limitation** -- ADR-004 notes the nudge hook fires during `/committing-changes` execution. This is a known, accepted limitation.

## 4. Priority Matrix (Updated Feb 9)

### High Value, Low Effort (Do Soon)

| Change | What | Status | Why |
|--------|------|--------|-----|
| Add `skills` preloading | `starting-projects`, `implementing-plans`, `committing-changes` | **Still pending** | Documents real dependencies; spec supports it |
| Add `category` to agents | All 8 agents | **Still pending** | Organizational clarity; zero risk |

### High Value, Medium Effort (Evaluate)

| Change | What | Status | Why |
|--------|------|--------|-----|
| Expand `allowed-tools` to more research skills | `researching-code`, `researching-web` | **Partially done** (`reviewing-security` adopted) | Prevents accidental writes during read-only operations |
| Add `context: fork` to heavy skills | `researching-code`, `debating-options`, `researching-frameworks` | **Still pending** | Prevents context pollution from subagent-heavy workflows |
| Evaluate TypeScript SDK migration | All 5 hooks | **New priority** (was deferred) | 5 hooks now exceed the "revisit at 3+" threshold |

### Completed (since original audit)

| Change | What | Status |
|--------|------|--------|
| Add PreCompact hook | `trigger-learning.py` in commandbase-session | **DONE** |
| Add SessionStart hook | `detect-session.py` in commandbase-session | **DONE** |
| Add Stop hook | `harvest-errors.py` in commandbase-session | **DONE** |
| Add PostToolUseFailure hook | `track-errors.py` in commandbase-session | **DONE** |
| Add `allowed-tools` to `reviewing-security` | `Read, Grep, Glob, LS, Bash, AskUserQuestion` | **DONE** |

### Low Value (Defer)

| Change | What | Why |
|--------|------|-----|
| `color` on agents | Cosmetic | No functional benefit |
| `disable-model-invocation` | Prevent auto-invocation | Not causing problems currently |
| `hooks` in skill frontmatter | Skill-scoped hooks | No clear use case identified |

## 5. Discrepancy: Hook Event Count

The framework-docs-snapshot.md documents 7 hook events, while our `creating-hooks` skill documents 12. The difference:

| Event | In Framework Snapshot | In Creating-Hooks Skill | Status |
|-------|----------------------|------------------------|--------|
| PreToolUse | Yes | Yes | Core |
| PostToolUse | Yes | Yes | Core |
| Notification | Yes | Yes | Core |
| Stop | Yes | Yes | Core |
| SubagentStop | Yes | Yes | Core |
| UserPromptSubmit | Yes | Yes | Core |
| PreCompact | Yes | Yes | Core |
| SessionStart | No | Yes | Lifecycle/expanding |
| SessionEnd | No | Yes | Lifecycle/expanding |
| PostToolUseFailure | No | Yes | Lifecycle/expanding |
| PermissionRequest | No | Yes | Lifecycle/expanding |
| SubagentStart | No | Yes | Lifecycle/expanding |

**Assessment:** The creating-hooks skill is MORE comprehensive than the framework snapshot. The snapshot captured the 7 "core" events from the official docs; the skill includes 5 additional lifecycle events. This is correct — the skill should document all available events. No update needed to the skill.

**Action:** Update framework-docs-snapshot.md to include all 12 events, noting which are core vs lifecycle/expanding.

## Files Referenced

### Skills (46 deployed across 8 plugins)
- `plugins/commandbase-core/skills/` (5 skills)
- `plugins/commandbase-code/skills/` (8 skills)
- `plugins/commandbase-vault/skills/` (8 skills)
- `plugins/commandbase-services/skills/` (6 skills)
- `plugins/commandbase-research/skills/` (4 skills)
- `plugins/commandbase-git-workflow/skills/` (5 skills)
- `plugins/commandbase-session/skills/` (4 skills)
- `plugins/commandbase-meta/skills/` (6 skills)

### Agents (8 deployed across 3 plugins)
- `plugins/commandbase-core/agents/` (docs-analyzer, docs-locator, docs-updater, docs-writer)
- `plugins/commandbase-code/agents/` (code-analyzer, code-librarian, code-locator)
- `plugins/commandbase-research/agents/` (web-researcher)

### Hooks (5 deployed across 2 plugins)
- `plugins/commandbase-git-workflow/hooks/hooks.json` (1 hook: PostToolUse)
- `plugins/commandbase-session/hooks/hooks.json` (4 hooks: PostToolUseFailure, Stop, PreCompact, SessionStart)

### Reference Documents
- `.docs/references/framework-docs-snapshot.md`
- `.docs/references/dependency-compatibility.md`
- `.docs/references/architecture-decisions.md`
