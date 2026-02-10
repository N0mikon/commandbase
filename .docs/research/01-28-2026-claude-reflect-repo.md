---
git_commit: 8e92bba
last_updated: 2026-01-28
last_updated_by: rcode agent
topic: "Claude-Reflect: Two-Stage Self-Learning System"
tags: [research, claude-reflect, hooks, self-learning, corrections, CLAUDE.md]
status: complete
references:
  - CLAUDE.md
  - README.md
  - SKILL.md
  - hooks/hooks.json
  - commands/reflect.md
  - commands/reflect-skills.md
  - commands/skip-reflect.md
  - commands/view-queue.md
  - scripts/capture_learning.py
  - scripts/check_learnings.py
  - scripts/post_commit_reminder.py
  - scripts/session_start_reminder.py
  - scripts/lib/reflect_utils.py
  - scripts/lib/semantic_detector.py
  - scripts/extract_session_learnings.py
  - scripts/extract_tool_errors.py
  - scripts/extract_tool_rejections.py
  - scripts/compare_detection.py
  - .claude-plugin/plugin.json
  - .claude-plugin/marketplace.json
---

# Research: Claude-Reflect — Two-Stage Self-Learning System

**Date**: 2026-01-28
**Repository**: https://github.com/BayramAnnakov/claude-reflect
**Author**: BayramAnnakov (Bayram Annakov)
**Version**: 2.5.0
**License**: MIT
**Branch**: main

## Research Question

How does claude-reflect implement its two-stage self-learning system? What are its hooks, commands, detection methods, data flow, and architecture?

## Summary

Claude-reflect is a Claude Code plugin that implements a two-stage correction learning system:

1. **Capture Stage (automatic)**: Four hooks detect correction patterns in user prompts, back up the queue before compaction, remind after git commits, and show pending learnings at session start. All hooks are Python scripts.
2. **Process Stage (manual)**: The `/reflect` command processes queued learnings with human review and writes to CLAUDE.md files. The `/reflect-skills` command discovers repeating workflow patterns from session history and generates reusable skill files.

The system uses a **hybrid detection approach**: regex patterns for fast real-time capture, plus semantic AI validation (via `claude -p`) during `/reflect` for accuracy and multi-language support. A JSON queue file at `~/.claude/learnings-queue.json` bridges the two stages.

## File Structure

```
claude-reflect/                         (CLAUDE.md:13-22)
├── .claude-plugin/
│   ├── plugin.json                     # Plugin manifest (v2.5.0)
│   └── marketplace.json                # Self-hosted marketplace definition
├── commands/
│   ├── reflect.md                      # Main /reflect command (~1268 lines)
│   ├── reflect-skills.md               # /reflect-skills command (~363 lines)
│   ├── skip-reflect.md                 # /skip-reflect command (~33 lines)
│   └── view-queue.md                   # /view-queue command (~103 lines)
├── hooks/
│   └── hooks.json                      # 4 hook definitions (48 lines)
├── scripts/
│   ├── lib/
│   │   ├── __init__.py
│   │   ├── reflect_utils.py            # Shared utilities (737 lines)
│   │   └── semantic_detector.py        # AI-powered semantic analysis (554 lines)
│   ├── capture_learning.py             # UserPromptSubmit hook (80 lines)
│   ├── check_learnings.py              # PreCompact hook (52 lines)
│   ├── post_commit_reminder.py         # PostToolUse hook (66 lines)
│   ├── session_start_reminder.py       # SessionStart hook (58 lines)
│   ├── extract_session_learnings.py    # CLI: extract user messages from sessions
│   ├── extract_tool_errors.py          # CLI: extract repeated tool errors
│   ├── extract_tool_rejections.py      # CLI: extract tool rejection feedback
│   ├── compare_detection.py            # CLI: compare regex vs semantic detection
│   └── legacy/                         # Deprecated bash scripts (reference only)
├── tests/
│   ├── __init__.py
│   ├── test_integration.py
│   ├── test_reflect_utils.py
│   ├── test_semantic_detector.py
│   └── test_tool_errors.py
├── assets/
│   └── reflect-demo.jpg
├── CLAUDE.md                           # Project instructions
├── CHANGELOG.md                        # Version history
├── DISTRIBUTION.md                     # Marketplace submission materials
├── README.md                           # User documentation
├── RELEASING.md                        # Release process
├── SKILL.md                            # Plugin context skill
└── LICENSE                             # MIT
```

## Detailed Findings

### 1. Plugin Registration

**Plugin manifest** (`.claude-plugin/plugin.json:1-19`):
```json
{
  "name": "claude-reflect",
  "version": "2.5.0",
  "description": "Self-learning system for Claude Code that captures corrections and updates CLAUDE.md automatically",
  "author": { "name": "Bayram Annakov", "url": "https://github.com/bayramannakov" },
  "repository": "https://github.com/bayramannakov/claude-reflect",
  "license": "MIT",
  "keywords": ["claude-code", "self-learning", "corrections", "CLAUDE.md", "memory", "learnings"]
}
```

**Self-hosted marketplace** (`.claude-plugin/marketplace.json:1-14`):
```json
{
  "name": "claude-reflect-marketplace",
  "plugins": [{ "name": "claude-reflect", "source": "./" }]
}
```

**Installation**:
```bash
claude plugin marketplace add bayramannakov/claude-reflect
claude plugin install claude-reflect@claude-reflect-marketplace
```

Hooks are auto-loaded from `hooks/hooks.json` — no explicit `"hooks"` field in `plugin.json` (a v2.1.1 fix for duplicate hooks error; `CHANGELOG.md:41-42`).

### 2. Hook System

Four hooks defined in `hooks/hooks.json:1-48`. All use Python3 scripts via `${CLAUDE_PLUGIN_ROOT}`.

#### 2a. UserPromptSubmit — Correction Capture

- **File**: `hooks/hooks.json:3-12`
- **Script**: `scripts/capture_learning.py:1-80`
- **Matcher**: `""` (every user prompt)
- **Purpose**: Detect correction patterns in real-time and queue them

**Data flow** (`capture_learning.py:24-70`):
1. Reads JSON from stdin: `{"prompt": "user's text"}`
2. Calls `detect_patterns(prompt)` from `reflect_utils.py`
3. If pattern matched, calls `create_queue_item()` and appends to queue
4. Prints capture feedback to stdout: `📝 Learning captured: '...' (confidence: 85%)`
5. Always exits 0 (never blocks)

#### 2b. PreCompact — Queue Backup

- **File**: `hooks/hooks.json:14-23`
- **Script**: `scripts/check_learnings.py:1-52`
- **Matcher**: `""` (all compactions)
- **Purpose**: Back up queue before context compaction

**Logic** (`check_learnings.py:17-42`):
1. Loads queue from `~/.claude/learnings-queue.json`
2. If non-empty, creates backup at `~/.claude/learnings-backups/pre-compact-YYYYMMDD-HHMMSS.json`
3. Prints informational message about backup and reminds to `/reflect`

#### 2c. PostToolUse (Bash) — Commit Reminder

- **File**: `hooks/hooks.json:25-34`
- **Script**: `scripts/post_commit_reminder.py:1-66`
- **Matcher**: `"Bash"` (only Bash tool)
- **Purpose**: Remind to `/reflect` after git commits

**Logic** (`post_commit_reminder.py:18-56`):
1. Reads JSON from stdin with `tool_input.command`
2. Checks if command contains `"git commit"` (skips `--amend`)
3. Loads queue to show count of pending learnings
4. Outputs JSON with `hookSpecificOutput.additionalContext` containing reminder

#### 2d. SessionStart — Pending Learnings Reminder

- **File**: `hooks/hooks.json:36-46`
- **Script**: `scripts/session_start_reminder.py:1-58`
- **Matcher**: `""` (all session starts)
- **Purpose**: Show pending learnings count at session start

**Logic** (`session_start_reminder.py:17-48`):
1. Checks `CLAUDE_REFLECT_REMINDER` env var (can be disabled with `"false"`)
2. Loads queue, exits if empty
3. Shows up to 5 items with confidence scores
4. Prints `💡 Run /reflect to review and apply`

### 3. Detection System

#### 3a. Regex Patterns (Real-Time)

Defined in `scripts/lib/reflect_utils.py:168-234`. Five categories:

**Explicit Patterns** (`reflect_utils.py:172-174`):
- `remember:` — confidence 0.90, decay 120 days

**Guardrail Patterns** (`reflect_utils.py:206-215`):
- `don't add X unless` — "dont-unless-asked", confidence 0.90
- `only change what I asked` — "only-what-asked", confidence 0.90
- `stop refactoring unrelated` — "stop-unrelated", confidence 0.90
- `don't over-engineer` — confidence 0.85
- `don't refactor unless` — confidence 0.85
- `leave X alone` — confidence 0.85
- `don't add comments/docstrings/annotations` — confidence 0.85
- `minimal changes` — confidence 0.80

**Correction Patterns** (`reflect_utils.py:192-201`):
- `^no[,. ]+` — "no," (strong)
- `^don't/do not` — (strong)
- `^stop/never` — (strong)
- `that's wrong/incorrect` — (strong)
- `^actually[,. ]` — (weak)
- `^I meant/said` — (strong)
- `^I told you/already told` — (strong, 0.85 confidence)
- `use X not Y` — (strong, limited gap)

**Positive Patterns** (`reflect_utils.py:177-181`):
- `perfect!/exactly right/that's exactly` — confidence 0.70
- `that's what I wanted/great approach` — confidence 0.70
- `keep doing this/love it/excellent/nailed it` — confidence 0.70

**False Positive Patterns** (`reflect_utils.py:219-227`):
- Ends with `?` (questions)
- Task request openers (`please/can you/could you`)
- Task verbs (`help/fix/check/review`)
- Error descriptions and bug reports
- Task requests (`I need/want/would like`)

#### 3b. Confidence Scoring

`detect_patterns()` at `reflect_utils.py:237-324`:

- **"I told you"** pattern: 0.85, 120 days decay
- **3+ patterns**: 0.85, 120 days
- **2 patterns**: 0.75, 90 days
- **1 strong pattern**: 0.70, 60 days
- **1 weak pattern**: 0.55, 45 days

**Length adjustment** (`reflect_utils.py:314-320`):
- Short messages (<80 chars): +0.10 boost (capped at 0.90)
- Medium messages (150-300 chars): -0.10 reduction
- Long messages (>300 chars): -0.15 reduction

#### 3c. Semantic AI Detection (During /reflect)

`scripts/lib/semantic_detector.py:1-554`:

- Uses `claude -p --output-format json` to call Claude CLI
- Multi-language support — understands corrections in any language
- Returns structured JSON: `{is_learning, type, confidence, reasoning, extracted_learning}`
- 30-second timeout per call
- Graceful fallback to regex if CLI unavailable

**Prompt template** (`semantic_detector.py:16-38`): Asks Claude to classify messages as correction/positive/explicit and extract concise actionable statements.

**Contradiction detection** (`semantic_detector.py:426-538`): `detect_contradictions(entries)` finds conflicting CLAUDE.md entries using semantic analysis. Used by `/reflect --dedupe`.

**Tool error validation** (`semantic_detector.py:240-418`): `validate_tool_error()` and `validate_tool_errors()` use Claude to determine if repeated tool errors should become CLAUDE.md guidelines.

### 4. Queue Data Model

**Storage**: `~/.claude/learnings-queue.json`

**Item structure** (`CLAUDE.md:118-129`):
```json
{
  "type": "auto|explicit|positive|guardrail",
  "message": "user's original text",
  "timestamp": "ISO8601",
  "project": "/path/to/project",
  "patterns": "matched pattern names",
  "confidence": 0.75,
  "sentiment": "correction|positive",
  "decay_days": 90
}
```

**Queue operations** (`reflect_utils.py:128-150`):
- `load_queue()` — reads JSON, returns `[]` on error
- `save_queue(items)` — writes with `indent=2`, creates parent dirs
- `append_to_queue(item)` — load + append + save
- `create_queue_item(...)` — factory function with defaults (`reflect_utils.py:327-346`)

**Backup location**: `~/.claude/learnings-backups/` (`reflect_utils.py:22-24`)

### 5. Commands

#### 5a. /reflect — Main Processing Command

**File**: `commands/reflect.md:1-1268` (the largest file in the repo)
**Allowed tools**: Read, Edit, Write, Glob, Bash, Grep, AskUserQuestion, TodoWrite

**Arguments**:
- `--dry-run` — preview without writing
- `--scan-history` — scan ALL past sessions
- `--days N` — limit history scan to N days (default: 30)
- `--targets` — show detected CLAUDE.md files
- `--review` — show queue with confidence/decay status
- `--dedupe` — find and consolidate similar CLAUDE.md entries
- `--include-tool-errors` — include tool execution errors

**Workflow** (10 steps, `reflect.md:66-1268`):

1. **Initialize TodoWrite tracking** (`reflect.md:66-116`) — mandatory task list for all phases
2. **Handle special arguments** (`reflect.md:120-326`) — `--targets` shows CLAUDE.md files with line counts and >150 line warnings; `--review` shows confidence/decay table; `--dedupe` runs contradiction detection then similarity grouping
3. **First-run detection** (`reflect.md:328-361`) — checks `~/.claude/projects/PROJECT/.reflect-initialized`; offers historical scan on first run
4. **Load queue** (`reflect.md:617-621`) — reads `learnings-queue.json`
5. **Semantic validation** (`reflect.md:623-681`) — runs `validate_queue_items()` on queue items; filters non-learnings; enhances with `extracted_learning`; `remember:` items always kept
6. **Session reflection** (`reflect.md:683-741`) — analyzes current session for missed corrections; extracts tool rejections (HIGH confidence)
7. **Historical scan** (if `--scan-history`, `reflect.md:377-615`) — scans ALL session JSONL files; extracts corrections + tool rejections + tool errors; dynamic language detection; mandatory presentation of raw matches
8. **Project-aware filtering** (`reflect.md:747-816`) — same project = show normally; different project + global pattern = show with warning; different project + project-specific = auto-skip
9. **Skill context detection** (`reflect.md:773-816`) — reasons about whether correction relates to a skill invocation; offers routing to skill file
10. **Deduplication, presentation, confirmation, apply** (`reflect.md:817-1268`) — semantic dedup within batch; summary table with AskUserQuestion; final confirmation gate; writes to CLAUDE.md/AGENTS.md/skill files; clears queue

**Multi-target sync** (`reflect.md:21-58`):

| Target | Path | Notes |
|--------|------|-------|
| Global CLAUDE.md | `~/.claude/CLAUDE.md` | Always enabled |
| Project CLAUDE.md | `./CLAUDE.md` | If exists |
| Subdirectory CLAUDE.md | `./**/CLAUDE.md` | Auto-discovered |
| Skill files | `./commands/*.md` | When correction relates to skill |
| AGENTS.md | `./AGENTS.md` | Industry standard format |

**Skill improvement routing** (`reflect.md:773-964`): When a correction follows a skill invocation (e.g., `/deploy`), `/reflect` detects this context and offers routing the learning to the skill file's steps or guardrails section rather than CLAUDE.md.

**AGENTS.md format** (`reflect.md:1148-1175`): Uses marker comments `<!-- Auto-generated by claude-reflect -->` for replaceable section.

**Section headers for CLAUDE.md** (`reflect.md:1219-1224`):
- `## LLM Model Recommendations`
- `## Tool Usage`
- `## Project Conventions`
- `## Guardrails`
- `## Common Errors to Avoid`
- `## Environment Setup`

#### 5b. /reflect-skills — Skill Discovery

**File**: `commands/reflect-skills.md:1-363`
**Allowed tools**: Read, Write, Bash, Glob, Grep, AskUserQuestion, TodoWrite

**Arguments**: `--days N`, `--project <path>`, `--all-projects`, `--dry-run`

**Key design principle** (`reflect-skills.md:21-35`): Uses AI **reasoning** to detect patterns, not regex/keyword matching. Same intent in different phrasings is recognized semantically.

**Workflow** (`reflect-skills.md:39-327`):
1. Parse arguments
2. Gather session data using `extract_session_learnings.py`
3. Check existing commands to avoid proposing duplicates
4. Analyze sessions for workflow patterns, misunderstanding patterns, and intent similarity
5. Propose skill candidates grouped by project with confidence levels
6. Assign skills to correct project locations
7. Generate skill files in `.claude/commands/` with frontmatter + steps + guardrails
8. Validate generated files

**Generated skill template** (`reflect-skills.md:254-279`):
```markdown
---
description: [One-line description]
allowed-tools: [Relevant tools based on workflow]
---
## Context
## Your Task
### Steps
### Guardrails
---
*Generated by /reflect-skills from [N] session patterns*
```

#### 5c. /skip-reflect — Discard Queue

**File**: `commands/skip-reflect.md:1-33`
**Allowed tools**: Bash

Simple escape hatch: shows queue count, confirms with user, then writes `[]` to queue file.

#### 5d. /view-queue — View Pending Learnings

**File**: `commands/view-queue.md:1-103`
**Allowed tools**: Bash, Read

Displays queue items with confidence scores, pattern names, and relative timestamps. Includes Python snippet for human-readable time formatting (`view-queue.md:63-90`).

### 6. SKILL.md — Plugin Context

**File**: `SKILL.md:1-65`
**Frontmatter**: `name: claude-reflect`, description references corrections and CLAUDE.md

Provides Claude with context about the plugin when active: available commands, correction detection patterns, learning destinations, and example interaction flow. Acts as a lightweight reference card.

### 7. Session File Parsing

**User message extraction** (`reflect_utils.py:353-415`):
- Reads JSONL files line-by-line
- Filters for `type == "user"` and `isMeta != true`
- Handles both string and list content formats
- Applies skip patterns (XML tags, JSON, tool results, bold text, indented lists, command expansions)

**Tool rejection extraction** (`reflect_utils.py:445-524`):
- Looks for `type == "tool_result"` with `is_error == true`
- Must contain `"The user doesn't want to proceed"`
- Extracts text after `"the user said:"` marker
- Skips empty rejections (no feedback)

**Tool error extraction** (`reflect_utils.py:579-674`):
- Extracts technical errors (`is_error == true`, NOT user rejections)
- Excludes Claude Code guardrails and global behavior issues (`reflect_utils.py:532-543`)
- Matches project-specific patterns: connection errors, env undefined, database errors, module not found, port conflicts (`reflect_utils.py:547-576`)
- Aggregation with minimum occurrence threshold (`reflect_utils.py:677-736`)

### 8. Multi-File Target Discovery

`find_claude_files()` at `reflect_utils.py:41-92`:
- Searches global `~/.claude/CLAUDE.md`
- Searches project root `./CLAUDE.md`
- Walks subdirectories excluding: `node_modules`, `.git`, `venv`, `__pycache__`, `dist`, `build`, etc. (`reflect_utils.py:33-38`)
- Returns list of `{path, relative_path, type}` dicts

`suggest_claude_file()` at `reflect_utils.py:95-121`:
- Simple heuristic: global indicators (`gpt-`, `claude-`, `always`, `never`, `prefer`) → global
- Subdirectory name mentioned in learning → that subdirectory's CLAUDE.md
- Otherwise returns `None` to let Claude decide

### 9. Testing

**141 tests passing** (README badge). Test files:
- `tests/test_reflect_utils.py` — pattern detection, queue operations, session extraction
- `tests/test_semantic_detector.py` — mocked Claude CLI calls, validation logic
- `tests/test_tool_errors.py` — error extraction and aggregation
- `tests/test_integration.py` — end-to-end workflows

CI: GitHub Actions on Windows, macOS, Linux with Python 3.8 and 3.11 (`.github/workflows/test.yml`).

### 10. Version History Highlights

From `CHANGELOG.md:1-104`:

| Version | Date | Key Changes |
|---------|------|-------------|
| 2.5.0 | 2026-01-25 | SessionStart hook for pending learnings reminder |
| 2.4.0 | 2026-01-23 | Guardrail patterns, contradiction detection, capture feedback |
| 2.1.1 | 2026-01-06 | Fix duplicate hooks from plugin.json |
| 2.1.0 | 2026-01-05 | Tool error extraction, TodoWrite tracking |
| 2.0.0 | 2026-01-04 | Python rewrite (Windows support), semantic AI, 90 tests |
| 1.4.x | 2025-12-xx | Confidence scoring, positive feedback, AGENTS.md sync |

## Architecture Notes

### Two-Stage Design

The fundamental architectural decision is separating **capture** (automatic, non-blocking hooks) from **processing** (manual, human-reviewed command). This means:

- Hooks never block user workflow — all exit 0, catch all errors
- Queue accumulates learnings across sessions without user intervention
- User explicitly triggers `/reflect` when ready to review
- Human approval gate prevents false positives from reaching CLAUDE.md

### Hybrid Detection Architecture

The regex + semantic approach uses each method's strength:

- **Regex**: Fast, runs on every prompt, no API cost, English-centric but effective for structural patterns
- **Semantic (claude -p)**: Accurate, multi-language, provides clean `extracted_learning` text, but slower and requires CLI availability
- **Fallback**: If semantic fails, regex results are kept — the system degrades gracefully

### Plugin Distribution Model

Uses a self-hosted marketplace (`marketplace.json`) rather than requiring inclusion in an external marketplace. Users add the author's GitHub repo as a marketplace source, then install from it. `DISTRIBUTION.md` documents PR templates for 9+ marketplace/awesome-list submissions.

### Queue as Bridge

The `learnings-queue.json` file serves as an asynchronous message queue between hooks and commands. Items include confidence scores, pattern names, project paths, and decay metadata — enabling project-aware filtering and time-based prioritization during `/reflect`.

### CLAUDE.md as Persistent Memory

The system treats CLAUDE.md files as Claude Code's long-term memory. Since Claude Code loads CLAUDE.md at session start, writing learnings there ensures they persist across sessions. The multi-target approach (global + project + subdirectory + AGENTS.md) provides appropriate scoping.

### Skill Improvement Loop

A distinctive feature: corrections made during skill execution can be routed back to the skill file itself (`commands/reflect.md:773-964`). This creates a feedback loop where skills improve over time from usage corrections, not just CLAUDE.md.

## Code References

- `hooks/hooks.json:3-12` — UserPromptSubmit hook definition
- `hooks/hooks.json:14-23` — PreCompact hook definition
- `hooks/hooks.json:25-34` — PostToolUse (Bash) hook definition
- `hooks/hooks.json:36-46` — SessionStart hook definition
- `scripts/capture_learning.py:47-63` — Pattern detection and queue append logic
- `scripts/lib/reflect_utils.py:172-215` — All regex pattern definitions
- `scripts/lib/reflect_utils.py:237-324` — `detect_patterns()` confidence scoring
- `scripts/lib/reflect_utils.py:353-415` — Session JSONL message extraction
- `scripts/lib/reflect_utils.py:445-524` — Tool rejection extraction
- `scripts/lib/reflect_utils.py:579-674` — Tool error extraction
- `scripts/lib/reflect_utils.py:677-736` — Error aggregation with thresholds
- `scripts/lib/semantic_detector.py:41-118` — `semantic_analyze()` function
- `scripts/lib/semantic_detector.py:180-233` — `validate_queue_items()` batch validation
- `scripts/lib/semantic_detector.py:454-538` — `detect_contradictions()` function
- `commands/reflect.md:66-116` — Mandatory TodoWrite initialization
- `commands/reflect.md:377-615` — Historical scan workflow
- `commands/reflect.md:773-964` — Skill context detection and routing
- `commands/reflect.md:1110-1175` — AGENTS.md sync with marker comments
- `commands/reflect-skills.md:132-184` — AI-powered pattern analysis
- `commands/reflect-skills.md:242-279` — Skill file template
- `.claude-plugin/plugin.json:1-19` — Plugin manifest
- `SKILL.md:1-65` — Plugin context document

## Open Questions

- How does the system handle queue conflicts when multiple sessions write simultaneously? (No locking mechanism visible)
- What is the actual false positive rate of regex detection in production usage?
- How large do CLAUDE.md files get before the >150 line warning becomes actionable?
- The `decay_days` field is defined in queue items but no code actually expires items based on it — is this implemented in `/reflect` via Claude's reasoning or is it unimplemented?
