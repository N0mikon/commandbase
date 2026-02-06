---
date_created: 2026-02-06
status: current
---

# Architecture Decisions

Technology choices for the commandbase project, recorded with rationale so future sessions don't re-debate settled decisions.

## ADR-001: Use SKILL.md Format for Workflow Tools

**Status:** Accepted
**Date:** 2026-02-06
**Context:** We need a format for defining reusable Claude Code workflow tools (research, plan, implement, validate). Claude Code supports skills (SKILL.md), agents (.md), hooks (scripts), and commands (.md).

**Decision:** Use skills (SKILL.md) as the primary format for workflow tools, with agents and hooks as supporting components.

**Alternatives Considered:**
- Agents only: Too limited — agents can't reference templates, enforce multi-phase workflows, or use progressive disclosure
- Commands only: Deprecated in favor of skills in recent Claude Code versions
- Mixed commands + agents: Skills subsume both and add frontmatter features like `context: fork`, `skills` preloading

**Consequences:**
- Skills provide progressive disclosure (body + reference/ + templates/) matching our workflow complexity
- Skills can preload other skills, enabling composition (e.g., `/starting-projects` calls `/researching-frameworks`)
- Requires maintaining SKILL.md format compliance and 500-line body limit

**Sources:** Context7 `/llmstxt/code_claude_llms_txt`

---

## ADR-002: Use Python for Hooks (Current)

**Status:** Accepted (under review)
**Date:** 2026-02-06
**Context:** Hooks need a runtime to parse JSON from stdin and return JSON on stdout. We need something available on all platforms.

**Decision:** Use Python scripts for hooks (e.g., `nudge-commit-skill.py`).

**Alternatives Considered:**
- TypeScript via `claude-code-hook-sdk`: Better type safety and utility functions, but adds Node.js dependency and `tsx` runtime
- Bash scripts: Too fragile for JSON parsing
- Compiled binaries: Overkill for simple hooks

**Consequences:**
- Python is universally available and simple for JSON parsing
- No type safety — hook input/output contracts are enforced by convention
- Manual JSON parsing boilerplate in each hook
- Works well on Windows/MINGW with `bash -c python` wrapper

**Sources:** Context7 `/mizunashi-mana/claude-code-hook-sdk` (TypeScript alternative)

---

## ADR-003: Commandbase Repo as Source of Truth

**Status:** Accepted
**Date:** 2026-02-06
**Context:** Skills are developed in `commandbase/newskills/` and deployed to `~/.claude/skills/`. We need clarity on which location is authoritative.

**Decision:** The commandbase repo (`newskills/`, `newagents/`, `newhooks/`) is the source of truth. `~/.claude/` is the deployment target.

**Alternatives Considered:**
- `~/.claude/` as source: No version control, no PR review, easy to lose changes
- Symlinks from `~/.claude/` to repo: Fragile on Windows, confusing paths

**Consequences:**
- All changes must be copied back to the repo before committing
- Deployment is a manual `cp -r` step (documented in CLAUDE.md)
- Git history tracks all skill evolution

**Sources:** Project CLAUDE.md

---

## ADR-004: Three-Layer Commit Enforcement

**Status:** Accepted
**Date:** 2026-02-06
**Context:** Direct `git commit` and `git push` bypass our `/committing-changes` skill which handles staged file verification, security review, and stale docs detection.

**Decision:** Enforce `/committing-changes` usage through three layers: CLAUDE.md rule, PostToolUse nudge hook, and settings.json deny rules.

**Alternatives Considered:**
- CLAUDE.md rule only: Can be ignored or forgotten during long sessions
- PreToolUse block hook: Too aggressive — blocks the skill itself from committing
- Git hooks (pre-commit): Can't distinguish between Claude Code and manual commits

**Consequences:**
- CLAUDE.md provides the instruction
- Nudge hook provides soft feedback if direct commit is attempted
- Deny rules hard-block dangerous patterns (`git add -A`, `--no-verify`, `--force`)
- The nudge hook fires false positives when `/committing-changes` runs (known limitation)

**Sources:** `.docs/research/` commit enforcement research
