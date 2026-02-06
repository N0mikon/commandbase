---
date: 02-06-2026
topic: Framework spec vs current implementation audit
sources: [framework-docs-snapshot.md, dependency-compatibility.md, architecture-decisions.md, deployed skills/agents/hooks]
---

# Framework Spec vs Implementation Audit

Research comparing the Claude Code skills/agents/hooks spec (from Context7 research) against our current commandbase implementations to identify gaps, compliance issues, and adoption opportunities.

## Executive Summary

**Current state:** 24 skills, 7 agents, 1 hook — all compliant with the core spec. No violations found.

**Key finding:** We use 0 of 6 advanced skill features, 1 of 12 hook events, and 0 of 3 advanced agent features. The implementation is minimalist by design, but there are 3 high-value features worth adopting and several low-priority features that can be deferred.

## 1. Skills Audit (24 skills)

### Compliance: 100%

| Check | Result |
|-------|--------|
| Naming (kebab-case gerund) | 24/24 pass |
| Description formula ("Use this skill when...") | 24/24 pass |
| Required frontmatter (name, description) | 24/24 pass |
| Progressive disclosure (reference/, templates/) | Used by several skills |

### Advanced Features Not Used

| Feature | Available Since | Currently Used | Assessment |
|---------|----------------|----------------|------------|
| `context: fork` | Current spec | 0/24 skills | **Worth evaluating** — could prevent context pollution from heavy research skills |
| `skills` preloading | Current spec | 0/24 skills | **Worth adopting** — `starting-projects` calls `researching-frameworks`; should declare dependency |
| `hooks` in frontmatter | Current spec | 0/24 skills | Low priority — no clear use case yet |
| `allowed-tools` | Current spec | 0/24 skills | **Worth evaluating** — research skills could be restricted to read-only tools |
| `disable-model-invocation` | Current spec | 0/24 skills | Low priority — current auto-invocation behavior is fine |
| `agent` frontmatter key | Current spec | 0/24 skills | Low priority — unclear benefit |

### Recommendations for Skills

1. **Add `skills` preloading** where composition exists:
   - `starting-projects` → depends on `researching-frameworks`
   - `implementing-plans` → depends on `validating-code`
   - `committing-changes` → depends on `reviewing-security` (for public repos)

2. **Evaluate `context: fork`** for heavy-context skills:
   - `researching-code` — spawns many subagents, could pollute context
   - `debating-options` — parallel research could benefit from isolation
   - `researching-frameworks` — external doc fetching could pollute context

3. **Evaluate `allowed-tools`** for safety:
   - `researching-code` → restrict to `Read, Grep, Glob, LS, Task` (no Edit/Write/Bash)
   - `researching-web` → restrict to `WebSearch, WebFetch, Task`
   - `reviewing-security` → restrict to `Read, Grep, Glob, LS, Task` (no write access)

## 2. Agents Audit (7 agents)

### Compliance: 100%

| Check | Result |
|-------|--------|
| Naming (noun-form kebab-case) | 7/7 pass |
| Description (delegation trigger pattern) | 7/7 pass |
| Body structure (role, process, deliverables) | 7/7 pass |
| Model selection (appropriate for task) | 7/7 pass |
| Sync (deployed = development) | 7/7 pass |

### Advanced Features Not Used

| Feature | Currently Used | Assessment |
|---------|----------------|------------|
| `category` | 0/7 agents | Low priority — no UI benefit confirmed; nice-to-have for organization |
| `color` | 0/7 agents | Low priority — cosmetic |
| Proactive invocation | Partially — descriptions support it | Working as designed |

### Recommendations for Agents

1. **Add `category` field** for organizational clarity:
   - `category: "research"` → code-locator, code-librarian, docs-locator, web-researcher
   - `category: "analysis"` → code-analyzer, docs-analyzer
   - `category: "action"` → docs-updater

2. **No other changes needed** — agents are fully compliant and well-structured.

## 3. Hooks Audit (1 hook, 11 deny rules)

### Compliance: Valid implementation

| Check | Result |
|-------|--------|
| JSON stdin parsing | Correct (with error handling) |
| Exit code discipline | Correct (0=allow, 2=feedback) |
| Self-block avoidance | Correctly uses PostToolUse instead of PreToolUse |
| Windows/MINGW compat | Correct (`bash -c` wrapper for tilde expansion) |
| 3-layer enforcement | All 3 layers functioning |

### Hook Event Coverage

| Event | Used | Potential Use Case | Priority |
|-------|------|-------------------|----------|
| PostToolUse | Yes | Commit workflow nudging | Implemented |
| PreToolUse | No | Could add pre-execution validation | Medium — risk of deadlock |
| SessionStart | No | Inject context at session start | **Low — context already injected by CLAUDE.md** |
| PreCompact | No | Preserve critical rules before compaction | **Medium — could help long sessions** |
| Stop | No | Prevent premature stopping in multi-phase work | Low — not a current problem |
| UserPromptSubmit | No | Validate/transform user input | Low — no clear use case |
| SubagentStop | No | Validate subagent output | Low — no clear use case |
| Notification | No | Log/transform notifications | Low |
| SessionEnd | No | Cleanup actions | Low |
| SubagentStart | No | Monitor subagent spawning | Low |
| PostToolUseFailure | No | Log/handle failed tool calls | Low |
| PermissionRequest | No | Auto-approve patterns | Low |

### TypeScript SDK Migration Assessment

| Factor | Python (Current) | TypeScript SDK |
|--------|-----------------|----------------|
| Dependency | Python 3.8+ (already available) | Adds Node.js 18+ and tsx |
| Type safety | None (convention-based) | Full TypeScript types + Zod validation |
| Testing | Manual stdin piping | `runHookCaller` utility |
| Boilerplate | Manual JSON parsing per hook | `preToolRejectHook`, `postToolUpdateFileHook` |
| Maintenance | Simple, minimal | More structured but heavier |

**ADR-002 stands:** Python is fine for our single hook. Revisit if we add 3+ hooks where boilerplate becomes painful.

### Recommendations for Hooks

1. **Consider PreCompact hook** — Preserves CLAUDE.md rules and critical context during long sessions when compaction occurs. Medium effort, medium value.

2. **No immediate migration to TypeScript SDK** — One Python hook doesn't justify the dependency. Revisit at 3+ hooks.

3. **Document the false-positive limitation** — ADR-004 notes the nudge hook fires during `/committing-changes` execution. This is a known, accepted limitation.

## 4. Priority Matrix

### High Value, Low Effort (Do Soon)

| Change | What | Why |
|--------|------|-----|
| Add `skills` preloading | `starting-projects`, `implementing-plans`, `committing-changes` | Documents real dependencies; spec supports it |
| Add `category` to agents | All 7 agents | Organizational clarity; zero risk |

### High Value, Medium Effort (Evaluate)

| Change | What | Why |
|--------|------|-----|
| Add `allowed-tools` to research skills | `researching-code`, `researching-web`, `reviewing-security` | Prevents accidental writes during read-only operations |
| Add `context: fork` to heavy skills | `researching-code`, `debating-options`, `researching-frameworks` | Prevents context pollution from subagent-heavy workflows |
| Add PreCompact hook | New hook script | Preserves critical rules during compaction |

### Low Value (Defer)

| Change | What | Why |
|--------|------|-----|
| `color` on agents | Cosmetic | No functional benefit |
| `disable-model-invocation` | Prevent auto-invocation | Not causing problems currently |
| `hooks` in skill frontmatter | Skill-scoped hooks | No clear use case identified |
| TypeScript SDK migration | Rewrite nudge hook | Only 1 hook; Python works fine |
| SessionStart hook | Context injection | CLAUDE.md already handles this |
| Stop hook | Prevent premature stopping | Not a current pain point |

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

### Skills (24 deployed)
- `C:\Users\Jason\.claude\skills\*\SKILL.md`
- `C:\code\commandbase\newskills\*\SKILL.md`

### Agents (7 deployed)
- `C:\Users\Jason\.claude\agents\*.md`
- `C:\code\commandbase\newagents\*.md`

### Hooks (1 deployed)
- `C:\Users\Jason\.claude\hooks\nudge-commit-skill.py`
- `C:\code\commandbase\newhooks\nudge-commit-skill\nudge-commit-skill.py`
- `C:\code\commandbase\newhooks\nudge-commit-skill\settings-snippet.json`

### Settings
- `C:\Users\Jason\.claude\settings.json`

### Reference Documents
- `C:\code\commandbase\.docs\references\framework-docs-snapshot.md`
- `C:\code\commandbase\.docs\references\dependency-compatibility.md`
- `C:\code\commandbase\.docs\references\architecture-decisions.md`
