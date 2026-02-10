---
git_commit: 8e92bba
last_updated: 2026-02-09
last_updated_by: docs-updater
topic: "Adopt Framework Features from Spec Audit"
tags: [plan, index, framework-adoption, skills, agents, hooks]
status: archived
archived: 2026-02-09
archive_reason: "All 7 phase plans archived (phases 1,2,3,5,7 implemented; phase 4 deferred; phase 6 skipped). Master index is complete and no longer active."
references:
  - .docs/research/02-06-2026-framework-spec-vs-implementation-audit.md
  - .docs/references/framework-docs-snapshot.md
---

# Adopt Framework Features from Spec Audit

## Overview

Apply findings from the framework spec vs implementation audit to adopt high-value features across our 24 skills and 7 agents. This is the **master index** — each phase has its own self-contained plan file.

**Research basis:** `.docs/research/02-06-2026-framework-spec-vs-implementation-audit.md`

## Phase Plans

| Phase | Plan File | Summary | Status |
|-------|-----------|---------|--------|
| 1 | [Docs Frontmatter Standard](02-06-2026-phase1-docs-frontmatter-standard.md) | Define shared `.docs/` frontmatter standard | implemented |
| 2 | [Docs Writer Agent](02-06-2026-phase2-docs-writer-agent.md) | Create `docs-writer` agent to enforce the standard | implemented |
| 3 | [Skills Use Docs Writer](02-06-2026-phase3-skills-use-docs-writer.md) | Update 6 skills to delegate file creation to `docs-writer` | implemented |
| 4 | [Skills Preloading](02-06-2026-phase4-skills-preloading.md) | Add `skills` preloading to skill frontmatter | deferred |
| 5 | [Allowed Tools](02-06-2026-phase5-allowed-tools.md) | Add `allowed-tools` to `reviewing-security` | implemented |
| 6 | [Agent Categories](02-06-2026-phase6-agent-categories.md) | Add `category` to agent frontmatter | skipped |
| 7 | [Hook Event Fix](02-06-2026-phase7-hook-event-fix.md) | Fix framework-docs-snapshot hook event count | implemented |

## Dependency Order

```
Phase 1 (standard definition)
   └─> Phase 2 (agent that enforces the standard)
         └─> Phase 3 (skills delegate to the agent)

Phase 4, 5, 6, 7 are independent of each other and Phases 1-3
```

Phases 1-3 are sequential. Phases 4-7 can be done in any order.

## Explicitly NOT Doing

- `context: fork` — Was deferred due to bugs; now stable per web research (Claude Code 2.1+). Separate plan if desired.
- TypeScript hook SDK migration — Only 1 hook; Python works fine (ADR-002 stands).
- PreCompact hook — Medium effort, no current pain point. Separate plan if needed.
- `disable-model-invocation`, `color`, `hooks` in skill frontmatter — Low priority per audit.
- `allowed-tools` on research skills — Write needed for `.docs/` output; body instructions are the guardrail.
- New agent fields (`disallowedTools`, `permissionMode`, `memory`) — Discovered in web research; worth a separate evaluation plan.

## Deployment Checklist

After all phases complete:
- [ ] Copy new agent: `cp newagents/docs-writer.md ~/.claude/agents/`
- [ ] Copy modified skills: each `newskills/*/SKILL.md` to `~/.claude/skills/*/SKILL.md`
- [ ] Copy skill templates: each `newskills/*/templates/*.md` to `~/.claude/skills/*/templates/`
- [ ] Copy modified agents: each `newagents/*.md` to `~/.claude/agents/`
- [ ] Verify Phase 4-6 changes are frontmatter-only edits (no body changes)
- [ ] Verify Phase 3 template changes removed frontmatter but preserved body sections
