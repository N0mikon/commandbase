---
date: 2026-02-09
status: complete
topic: "commandbase workflow architecture for visualization"
tags: [research, workflow, architecture, BRDSPI, agents, hooks, sessions, plugins, visualization]
git_commit: ba0736e
references:
  - plugins/commandbase-code/skills/brainstorming-code/SKILL.md
  - plugins/commandbase-code/skills/researching-code/SKILL.md
  - plugins/commandbase-code/skills/designing-code/SKILL.md
  - plugins/commandbase-code/skills/structuring-code/SKILL.md
  - plugins/commandbase-code/skills/planning-code/SKILL.md
  - plugins/commandbase-code/skills/implementing-plans/SKILL.md
  - plugins/commandbase-session/hooks/hooks.json
  - plugins/commandbase-session/scripts/session_utils.py
---

# commandbase Workflow Architecture for Visualization

## Research Question
How do skills, agents, hooks, and plugins interact across the commandbase system? This research maps the full workflow architecture to inform designing a visual workflow map.

## Summary
commandbase implements an 8-plugin system with 46 skills, 8 agents, and 5 hooks. The core workflow pattern is BRDSPI (Brainstorm → Research → Design → Structure → Plan → Implement), which chains skills through a shared `.docs/` artifact pipeline. Agents handle delegation (research, documentation, staleness), hooks manage lifecycle events (session detection, error tracking, commit enforcement), and cross-plugin dependencies flow through commandbase-core as the foundation layer.

## Detailed Findings

### 1. BRDSPI Skill Chain Flow

The primary workflow follows this artifact pipeline:

```
Brainstorm → .docs/brainstorm/{topic}.md
   ↓ (optional input)
Research → .docs/research/MM-DD-YYYY-{topic}.md
   ↓ (mandatory input, with staleness check)
Design → .docs/design/MM-DD-YYYY-{topic}.md
   ↓ (optional input)
Structure → .docs/structure/MM-DD-YYYY-{topic}.md
   ↓ (optional input, with staleness check)
Plan → .docs/plans/MM-DD-YYYY-{topic}.md
   ↓ (mandatory input)
Implement → (updates checkboxes in plan, creates checkpoints)
```

Each skill reads upstream artifacts (with staleness detection) and writes its own via the docs-writer agent. Three domain plugins (code, vault, services) implement parallel BRDSPI chains.

**Staleness Detection Pattern**: designing-code and planning-code auto-refresh upstream artifacts by checking `git_commit:` in frontmatter. If >3 commits behind HEAD, they spawn docs-updater to refresh or archive.

**Checkpoint Integration**: planning-code suggests `create "plan-approved"`, implementing-plans creates `"phase-N-done"` after each verified phase, starting-refactors creates `"pre-refactor-<area>"` before audit.

### 2. Agent Delegation System

8 agents across 3 plugins handle specialized tasks:

| Agent | Plugin | Model | Tools | Primary Job |
|-------|--------|-------|-------|-------------|
| docs-writer | core | haiku | Write, Read, Bash, Glob | Creates standardized .docs/ files with frontmatter |
| docs-updater | core | opus | Read, Grep, Glob, LS, Edit, Bash | Updates stale docs or archives obsolete ones |
| docs-locator | core | sonnet | Grep, Glob, LS | Finds relevant documents across .docs/ |
| docs-analyzer | core | sonnet | Read, Grep, Glob, LS | Extracts high-value insights from documents |
| code-analyzer | code | sonnet | Read, Grep, Glob, LS | Analyzes codebase implementation details |
| code-librarian | code | sonnet | Grep, Glob, Read, LS | Finds similar patterns and usage examples |
| code-locator | code | sonnet | Grep, Glob, LS | Locates files and components by topic |
| web-researcher | research | sonnet | WebSearch, WebFetch | Searches web for current sourced information |

**Key delegation patterns**:
- **Parallel Research → Synthesis**: Skills decompose into 2-4 angles, spawn parallel agents, wait for ALL, then synthesize. Used by researching-web, structuring-code, starting-refactors, planning-code.
- **Staleness Check → Conditional Update**: Read frontmatter git_commit → calculate commits behind → if >3, spawn docs-updater → updater decides UPDATE or ARCHIVE.
- **Create Output via docs-writer**: All 23 domain skills spawn docs-writer with structured input (doc_type, topic, tags, content).

**Notable**: docs-updater uses opus (most powerful model) because it makes critical archive-vs-update decisions. docs-writer uses haiku (fastest) because it's a standardized formatting task.

docs-writer is the most spawned agent — 23 skills across all domain plugins use it. docs-updater is spawned by 6 skills across 4 plugins (resuming-session, committing-changes, auditing-docs, designing-code, implementing-plans, planning-code).

### 3. Hook System

5 hooks across 2 plugins manage lifecycle events:

| Hook | Plugin | Event | Script | Exit Code |
|------|--------|-------|--------|-----------|
| Session Detection | session | SessionStart | detect-session.py | 2 (feedback) |
| Error Tracking | session | PostToolUseFailure | track-errors.py | 0 (silent) |
| Error Harvesting | session | Stop | harvest-errors.py | 0 (always) |
| Learning Nudge | session | PreCompact | trigger-learning.py | 2 (feedback) |
| Commit Enforcement | git-workflow | PostToolUse:Bash | nudge-commit-skill.py | 2 (feedback) |

**Exit code semantics**: 0 = silent, 1 = error, 2 = inject stderr into conversation as feedback.

**Hook lifecycle during a session**:
1. **Start**: detect-session.py reads session-map.json, matches worktree → session, appends Claude UUID to meta.json, prints context (exit 2)
2. **During**: track-errors.py appends failures to errors.log (subagent-only); nudge-commit-skill.py detects bare `git commit/push` and reminds about /committing-changes
3. **Before compact**: trigger-learning.py counts errors, reminds about /learning-from-sessions if any exist
4. **End**: harvest-errors.py parses full transcript, deduplicates against errors.log, backfills empty entries

**Two error tracking strategies**: real-time (track-errors.py for subagent errors) + batch (harvest-errors.py for complete transcript analysis at session end).

**Hooks never invoke skills directly** — they prepare state (errors.log, meta.json) and send nudges via stderr. Users or Claude decide when to run skills.

### 4. Cross-Plugin Dependencies

**Dependency hierarchy**:
```
commandbase-core (foundation — no dependencies)
├── Exports: docs-writer, docs-updater, docs-locator, docs-analyzer
├── Exports: /bookmarking-code, /validating-code, /starting-projects
└── Required by: code, vault, services, research, git-workflow, session

commandbase-code → depends on core, references /committing-changes, /bookmarking-code
commandbase-vault → depends on core, references /committing-changes, /bookmarking-code
commandbase-services → depends on core, references /committing-changes, /bookmarking-code
commandbase-research → depends on core (docs agents + docs-locator + docs-analyzer)
commandbase-git-workflow → depends on core, exports /committing-changes
commandbase-session → depends on core, references /committing-changes, /bookmarking-code
commandbase-meta → standalone (no dependencies)
```

**Most-referenced skill**: /committing-changes — invoked by implementing-plans, debugging-code, ending-session, validating-code, starting-projects, reviewing-changes. It's the universal commit entry point.

**Shared .docs/ artifact pipeline**: 10 doc types (research, plan, design, structure, brainstorm, debug, refactor, handoff, learnings, reference) written by domain skills and read by downstream skills with staleness detection.

### 5. Session Lifecycle

**Start** (/starting-session):
- Detects repo layout (bare-worktree vs regular)
- Creates git branch + worktree for isolation
- Registers in container-level session-map.json
- Creates .claude/sessions/{name}/ directory with meta.json

**During** (hooks):
- SessionStart hook bridges context into conversation
- PostToolUseFailure tracks errors to errors.log
- PreCompact nudges learning extraction

**End** (/ending-session — 3 modes):
- **Merge**: squash merge to main, remove worktree + branch, invoke /committing-changes
- **Handoff**: keep branch open, create .docs/handoffs/ document, update status to "handed-off"
- **Discard**: force-remove worktree + branch after confirmation

**Resume** (/resuming-session — 3 modes):
- **Mode A (Worktree)**: Active session — read meta.json, errors.log, checkpoints, verify git state
- **Mode B (Handoff)**: Handed-off session — read handoff doc with staleness check, absorb context
- **Mode C (Picker)**: Multiple candidates — unified picker showing all active/handed-off sessions

**Learning** (/learning-from-sessions):
- Reads errors.log, identifies non-obvious discoveries
- Writes to .docs/learnings/ via docs-writer
- Can parse previous transcripts via claudeSessionIds in meta.json

**State files**:
- `{container}/session-map.json` — registry of all sessions
- `{worktree}/.claude/sessions/{name}/meta.json` — session metadata + Claude UUIDs
- `{worktree}/.claude/sessions/{name}/errors.log` — JSONL error tracking
- `{worktree}/.claude/sessions/{name}/checkpoints.log` — checkpoint history

### 6. Three-Layer Commit Enforcement

1. **CLAUDE.md rule** (`~/.claude/CLAUDE.md`): Instructs Claude to always use /committing-changes
2. **PostToolUse hook** (nudge-commit-skill.py): Detects bare git commit/push, sends reminder via exit 2
3. **Deny rules** (`~/.claude/settings.json`): Blocks `git add -A`, `git add .`, `git push --force`, `git reset --hard`, etc. at the tool level

## Architecture Notes

- All agents are spawned via the Task tool with `subagent_type` parameter
- Parallel spawning for independent research; sequential for dependent tasks
- The .docs/ directory is the primary inter-skill communication bus
- Document frontmatter (git_commit, status, tags) enables automated freshness management
- Session hooks use shared session_utils.py for path normalization, session resolution, and atomic file operations

## Open Questions

- How best to visually represent the BRDSPI chain branching across 3 domain plugins (code, vault, services)?
- Should the workflow map show agent delegation as a separate layer or inline with skill flows?
- How to represent the temporal dimension (session lifecycle hooks fire at different conversation stages)?
