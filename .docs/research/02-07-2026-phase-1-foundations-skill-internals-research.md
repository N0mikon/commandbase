---
date: 2026-02-07
status: complete
topic: "Phase 1 Foundations - Skill Internals Research"
tags: [research, phase-1, naming-session, bookmarking-code, implementing-plans, handing-over, learning-from-sessions, updating-skills, updating-agents, voice-tone]
git_commit: 5beb0c1
references:
  - ~/.claude/skills/bookmarking-code/SKILL.md
  - ~/.claude/skills/implementing-plans/SKILL.md
  - ~/.claude/skills/handing-over/SKILL.md
  - ~/.claude/skills/learning-from-sessions/SKILL.md
  - ~/.claude/skills/updating-skills/SKILL.md
  - ~/.claude/skills/updating-agents/SKILL.md
  - .docs/plans/02-07-2026-future-skills-implementation-roadmap.md
---

# Phase 1 Foundations - Skill Internals Research

**Date**: 2026-02-07
**Branch**: master

## Research Question
What are the current implementations of all skills affected by Phase 1 of the future-skills roadmap? What are the integration points, state patterns, and modification surfaces for building /naming-session, voice/tone reference, renames, and skill updates?

## Summary
Phase 1 has 8 work items across 2 sessions. Research covered all 6 affected skills plus the voice/tone reference location. Key finding: no session-scoped state mechanism exists anywhere — /naming-session will be the first. All skills that need modification are single-file (SKILL.md only) except /implementing-plans (has reference/ dir) and /updating-skills (has reference/ dir).

## Detailed Findings

### 1a. /naming-session — Design Inputs

**State patterns across existing skills:**
- `/bookmarking-code` stores state in `.claude/checkpoints.log` (project-root, pipe-delimited text file): `YYYY-MM-DD-HH:MM | checkpoint-name | git-sha`
- `/debugging-code` stores state in `.docs/debug/{slug}.md` (per-debug-session YAML+markdown files)
- `/handing-over` produces `.docs/handoffs/MM-DD-YYYY-description.md` files via docs-writer agent
- No skill currently stores session-scoped metadata that persists across skill invocations within a session

**Existing .docs/ subdirectories** (from docs-writer agent type mapping):
- `.docs/research/` (includes `skills/` sub-dir)
- `.docs/plans/`
- `.docs/handoffs/`
- `.docs/references/`
- `.docs/debug/`
- `.docs/archive/`
- `.docs/future-skills/`
- No `.docs/sessions/` or `.docs/learnings/` directory exists yet

**Consumer skills that would read session name:**
- `/bookmarking-code` — prefix checkpoints with session name (e.g., "auth-mvp:phase-2-done")
- `/handing-over` — use session name in handoff title and metadata
- `/learning-from-sessions` — tag learnings with session context
- `/implementing-plans` — session-named checkpoints after phases

**Open design question — storage location:**
- Option A: `.docs/sessions/` directory (one file per session, matches .docs/ pattern)
- Option B: `.claude/session.json` or similar (project-root, like checkpoints.log)
- Option C: Single index file `.docs/sessions.md` or `.claude/sessions.log`
- Key constraint: must be readable by other skills within the same session without requiring arguments

### 1b. Voice/Tone Reference — Location Survey

**`~/.claude/references/` directory:** Does NOT currently exist. Need to create it.

**Existing directories under `~/.claude/`:**
- `~/.claude/skills/` (24 skill directories)
- `~/.claude/agents/` (agent .md files)
- `~/.claude/hooks/` (hook scripts)
- No `~/.claude/references/` directory

**Current voice/tone guidance scattered across skills:**
- `/discussing-features` — `reference/question-domains.md:86-97` has "Tone & Voice" as a content domain with questions like "Formal or conversational?"
- `/creating-skills` — `reference/validation-rules.md:35` and `reference/description-writing-guide.md` discuss "voice" only in the context of third-person vs first-person for skill descriptions
- `/creating-agents` — Same pattern — "voice" means description voice, not user-facing content voice
- No skill currently has anti-AI-voice patterns, banned phrases, or platform norms

**Global CLAUDE.md:** No voice/tone guidance. Only identity, NEVER rules, scaffolding, and automatic behaviors.

### 1c. /bookmarking-code — Current State

**Files:** Single file: `SKILL.md` (244 lines). No reference/ directory.
**Deployed = Source:** Identical between `~/.claude/skills/bookmarking-code/SKILL.md` and `newskills/bookmarking-code/SKILL.md`

**Checkpoint naming (SKILL.md:196-202):**
- User-provided string, no constraints or prefixes
- Suggested: `plan-approved`, `phase-N-done`, `pre-refactor`, `feature-complete`
- Duplicates handled by using most recent entry (SKILL.md:85)

**Storage:** `.claude/checkpoints.log`, pipe-delimited: `YYYY-MM-DD-HH:MM | checkpoint-name | git-sha`
**Actual log** (commandbase project): 5 entries like `2026-02-06-19:05 | phase-1-done | df48ed0`

**Modification surface for session names:**
- Add: Read session name from /naming-session storage location
- Modify: Checkpoint name format from `name` to `session:name` when session name is available
- Update: Naming Conventions section (SKILL.md:196-202)
- Update: Workflow Integration section (SKILL.md:221-237)

### 1d. /implementing-plans — Current State

**Files:** `SKILL.md` (200 lines) + `reference/verification-workflow.md` (68 lines) + `reference/anti-patterns.md` (45 lines)
**Deployed = Source:** Identical copies.

**Current checkpoint behavior (SKILL.md:166-178):**
- Checkpoint Integration section EXISTS but checkpoints are SUGGESTED, not mandatory
- After phase completion, shows: "Create checkpoint before next phase? /bookmarking-code create 'phase-N-done'"
- User can skip — no enforcement

**Current docs-updater integration:** NONE. No references to `docs-updater`, `docs-writer`, `documentation`, or `handoff` in the skill.

**Phase completion flow (SKILL.md:100-130):**
1. Implement phase changes
2. Run verification commands (Gate Function)
3. Show evidence
4. Update plan checkboxes
5. SUGGEST checkpoint (optional)
6. Proceed to next phase

**Modification surface:**
- Change: Checkpoint from suggested to mandatory (SKILL.md:166-178)
- Add: Auto-create checkpoint with session-aware name after verification passes
- Add: docs-updater trigger for stale plan detection during implementation
- Add: Integration with `.docs/` files referenced in the plan

### 1e. /handing-over — Current State

**Files:** Single file: `SKILL.md` only. No reference/ directory.

**Title generation (SKILL.md:56-63 and docs-writer agent):**
- Handoff filename format: `MM-DD-YYYY-description.md` (generated by docs-writer agent)
- The "description" slug comes from the topic field passed to docs-writer
- Handoff document H1 title: `# Handover: [topic]`

**Existing handoff frontmatter pattern** (from actual files):
```yaml
git_commit: 068c070
last_updated: 2026-02-05
last_updated_by: claude
topic: "Agent audit, compliance fixes, and fleet rename"
tags: [handover, agents, naming, audit]
status: active
references: [list of file paths]
```

**No session awareness:** Zero references to session names, env vars, or persistent session state. The word "session" appears 14 times but always means "Claude conversation session" generically.

**Modification surface:**
- Add: Read session name from /naming-session storage
- Modify: Pass session name as metadata to docs-writer (new frontmatter field: `session:`)
- Modify: Include session name in handoff title when available (e.g., "Handover: [session-name] - [topic]")

### 1f-g. /updating-skills + /updating-agents — Rename Survey

**updating-skills structure:**
- `SKILL.md` + `reference/audit-checklist.md` + `reference/common-fixes.md`
- Frontmatter: `name: updating-skills`
- Self-references: 15+ internal references to "updating-skills" across SKILL.md
- Sibling reference: `SKILL.md:221-233` — "Sibling Skill: /updating-skills" section in updating-agents

**updating-agents structure:**
- `SKILL.md` + `reference/audit-checklist.md` + `reference/common-fixes.md`
- Frontmatter: `name: updating-agents`
- Self-references: 10+ internal references to "updating-agents"
- Sibling reference: `SKILL.md:221-233` — "Sibling Skill: /updating-skills" table comparing both

**Cross-references found across codebase:**
- `CLAUDE.md:31` — "When editing skills via `/updating-skills`..." (needs update)
- `.docs/handoffs/02-02-2026-reviewing-changes-skill.md` — 20+ refs (historical, may not need update)
- `.docs/handoffs/02-05-2026-agent-audit-and-rename.md` — 5+ refs (historical)
- `.docs/research/02-02-2026-reviewing-and-updating-skills-research.md` — 15+ refs (historical)
- `.docs/plans/02-02-2026-updating-skills-skill.md` — 30+ refs (historical)
- `.docs/research/skills/updating-skills.md` — 10+ refs (historical)
- `.docs/plans/02-05-2026-opus-4-6-skill-hardening.md` — 15+ refs (historical)
- `.docs/future-skills/re-evaluate-existing.md` — 4 refs

**Rename scope:**
- MUST update: Deployed skills (both dirs), source skills (both dirs in newskills/), CLAUDE.md line 31
- SHOULD update: `.docs/future-skills/re-evaluate-existing.md` (still actively referenced)
- SKIP: Historical .docs/ files (handoffs, research, plans) — these are snapshot records

### 1h. /learning-from-sessions — Current State

**Files:** `SKILL.md` + `reference/session-review-guide.md` + `reference/output-formats.md`

**Current flow (SKILL.md):**
1. Review conversation for learnings
2. Identify: what was tried, what worked, what failed
3. Categorize: debug finding, workaround, pattern, gotcha
4. **Immediately create** a skill file or CLAUDE.md entry (current behavior)
5. Present to user for confirmation

**Current output formats:**
- New skill file (via /creating-skills)
- CLAUDE.md entry addition
- Reference file addition to existing skill

**Debugging integration:** References `/debugging-code` as an integration point (SKILL.md:219-220). Suggests running after debug sessions. But does NOT read `.docs/debug/` files — it reviews conversation context only.

**No `.docs/learnings/` directory exists.** This is new for the rework.

**Rework scope (from roadmap):**
- Change: From "immediate action" to "capture now, act later"
- Add: `.docs/learnings/` output directory
- Add: Structured learning documents (error context, what tried, what worked)
- Add: Integration with `.docs/debug/` files (pull from debug artifacts, don't duplicate)
- Add: Session name from /naming-session
- Add: Connect to /handing-over (include learnings section)
- Remove: Immediate skill/CLAUDE.md creation (defer to future session)

## Code References

### Skill Files (deployed)
- `~/.claude/skills/bookmarking-code/SKILL.md` — 244 lines, single file
- `~/.claude/skills/implementing-plans/SKILL.md` — 200 lines + 2 reference files
- `~/.claude/skills/handing-over/SKILL.md` — ~180 lines, single file
- `~/.claude/skills/learning-from-sessions/SKILL.md` — ~150 lines + 2 reference files
- `~/.claude/skills/updating-skills/SKILL.md` — ~235 lines + 2 reference files
- `~/.claude/skills/updating-agents/SKILL.md` — ~235 lines + 2 reference files

### State Files
- `.claude/checkpoints.log` — Pipe-delimited checkpoint storage
- `.docs/handoffs/MM-DD-YYYY-description.md` — Handoff documents with YAML frontmatter

### Key Cross-Reference
- `CLAUDE.md:31` — References `/updating-skills` (needs rename to `/auditing-skills`)

## Architecture Notes

**State management pattern:** Skills use two patterns for persistent state:
1. `.claude/` directory (checkpoints.log) — simple append-only logs
2. `.docs/` directory (debug files, handoffs) — structured markdown with YAML frontmatter via docs-writer agent

**Session name would be a new primitive** — no existing mechanism for session-scoped state that multiple skills can read. The closest parallel is checkpoints.log but that's per-checkpoint, not per-session.

**docs-writer agent** handles all `.docs/` file creation with consistent frontmatter. Any new `.docs/` output type (learnings, sessions) should go through docs-writer for consistency.

## Open Questions

1. **Session name storage:** `.claude/session-name` (simple file) vs `.docs/sessions/` (structured) vs env var? Key requirement: readable by downstream skills without explicit passing.
2. **Voice/tone reference scope:** Just anti-AI-voice for social posts? Or broader writing guidance for all skills that produce user-facing text (PRs, commit messages, handoffs)?
3. **Historical .docs/ rename references:** Archive `.docs/research/skills/updating-skills.md` or just leave it as a historical artifact?
4. **Learning capture trigger:** Automatic at session end? On-demand via `/learning-from-sessions`? Prompted by `/handing-over`?
