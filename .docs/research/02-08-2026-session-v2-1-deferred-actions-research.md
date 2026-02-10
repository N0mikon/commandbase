---
date: 2026-02-08
status: active
topic: "Session Skills v2.1 Deferred Actions Research"
tags: [research, session-skills, bare-repo, worktrees, hooks, transcripts, v2.1]
git_commit: 8e92bba
references:
  - plugins/commandbase-session/skills/ending-session/SKILL.md
  - plugins/commandbase-session/skills/starting-session/SKILL.md
  - plugins/commandbase-session/skills/learning-from-sessions/SKILL.md
  - plugins/commandbase-session/skills/resuming-session/SKILL.md
  - plugins/commandbase-session/scripts/detect-session.py
  - plugins/commandbase-session/scripts/session_utils.py
  - plugins/commandbase-session/hooks/hooks.json
  - plugins/commandbase-git-workflow/scripts/nudge-commit-skill.py
  - plugins/commandbase-git-workflow/hooks/hooks.json
  - .docs/learnings/02-08-2026-end-to-end-test-session-learnings.md
---

# Session Skills v2.1 Deferred Actions Research

**Date**: 2026-02-08
**Branch**: master
**Source**: `.docs/learnings/02-08-2026-end-to-end-test-session-learnings.md` (11 deferred actions)

## Research Question

What is the current state of all files that need modification to address the 11 deferred actions from the end-to-end test session learnings? What are the exact locations, current implementations, and constraints for each change?

## Summary

Research covers 5 areas: ending-session skill (bare repo git commands + worktree cleanup), detect-session hook (Claude UUID capture + meta.json persistence), nudge hook (skill-awareness suppression), transcript format (post-session learning extraction), and hook installation (manual vs plugin). All findings are verified with file:line references.

## Detailed Findings

### 1. ending-session Skill — Bare Repo + Worktree Issues

**File**: `plugins/commandbase-session/skills/ending-session/SKILL.md`

**Bare repo git commands (3 locations need `git -C "$bare"`):**
- Line 168: `cd {container}` — container is not a git repo, should use `git -C "$bare"`
- Line 169: `git worktree remove {type}/{session-name}` — needs `-C "$bare"` and absolute path
- Line 170: `git branch -d {type}/{session-name}` — needs `-C "$bare"`
- Line 234: `cd {container}` (discard mode) — same issue
- Line 235: `git worktree remove --force {type}/{session-name}` — same
- Line 236: `git branch -D {type}/{session-name}` — same

**Container path determination (line 53):**
```bash
container=$(dirname "$(git rev-parse --git-common-dir)")
```
This correctly finds the container. Need to add: `bare="$container/.bare"`

**Worktree removal from inside worktree (no handling exists):**
- Lines 89, 123: Skill does `cd {container}/main` for merge operations
- Lines 168, 234: Skill does `cd {container}` for worktree removal — but Claude Code's cwd is still inside the worktree being removed
- Claude Code cannot change its actual working directory mid-session
- On MINGW/Windows, the OS locks directories with active processes, causing `Permission denied`
- After partial removal, git unregisters the worktree but the directory persists (ghost state)
- No `git worktree prune` or ghost detection exists in the skill

**Squash merge flow (for context):**
1. Lines 86-118: Dry-run merge with `--no-commit --no-ff`, abort
2. Lines 120-125: Actual `git merge --squash` from `{container}/main`
3. Lines 127-149: CLAUDE.md review
4. Line 153: Delegates to `/committing-changes`
5. Lines 155-163: Learning check (suggests `/learning-from-sessions` if errors exist)
6. Lines 165-171: Worktree + branch removal
7. Lines 173-175: session-map.json update to `status: "ended"`

### 2. detect-session.py — Claude UUID Capture

**File**: `plugins/commandbase-session/scripts/detect-session.py`

**Current UUID handling:**
- Line 27: Captures `session_id` from hook input: `input_data.get("session_id", "")`
- Lines 62, 70: Outputs it to stderr for display only
- NOT persisted to meta.json or any file

**Session matching (lines 41-52):**
- Reads `session-map.json` via `read_session_map(cwd)`
- Iterates entries, matches by normalized worktree path
- Extracts name, branch, status, worktree from matching entry

**Hook configuration** (`hooks/hooks.json:34-42`):
```json
"SessionStart": [{
  "hooks": [{
    "type": "command",
    "command": "bash -c 'python3 ${CLAUDE_PLUGIN_ROOT}/scripts/detect-session.py'"
  }]
}]
```

**What needs to change:**
- After session match (line 52): read meta.json from session dir
- Initialize `claudeSessionIds` array if missing
- Append current `session_id` if not already present
- Write updated meta.json atomically via `session_utils.atomic_write_json()`

**session_utils.py functions available:**
- `get_session_dir(cwd, session_name)` (lines 203-224) — returns `.claude/sessions/{name}/` path
- `atomic_write_json(path, data)` (lines 231-252) — temp file + `os.replace()` atomic write
- `read_session_map(cwd)` (lines 119-131) — reads session-map.json
- `normalize_path(path)` (lines 21-33) — MINGW path conversion

### 3. nudge-commit-skill.py — Skill-Awareness

**File**: `plugins/commandbase-git-workflow/scripts/nudge-commit-skill.py`

**Current detection (lines 14-20):**
```python
if input_data.get("tool_name") != "Bash":
    sys.exit(0)
command = input_data.get("tool_input", {}).get("command", "")
if re.search(r"\bgit\s+(commit|push)\b", command):
```

**No suppression mechanism exists.** No env var checks, no transcript parsing, no temp file flags.

**Available hook input fields:**
- `session_id` — Claude session UUID
- `transcript_path` — full path to session transcript JSONL
- `cwd` — working directory
- `tool_name` — tool that was executed
- `tool_input` — tool parameters (command string for Bash)

**Viable suppression approaches (ranked):**

1. **Transcript parsing** (most reliable): Read `transcript_path`, check if `Skill` tool was invoked with `committing-changes`. Cons: must parse potentially large JSONL on every Bash call.

2. **Temp sentinel file** (practical): `/committing-changes` skill writes a flag file before git commands, hook checks for it. Cons: cleanup needed, race conditions if skill fails.

3. **Comment marker in command** (simplest): Skill adds `# commandbase-skill-invoked` to git commands, hook checks for it. Cons: fragile, visible in bash history.

4. **Environment variable** (won't work): Env vars don't persist across separate Bash tool calls in Claude Code.

### 4. Claude Code Transcript Format

**Location**: `~/.claude/projects/{path-encoded-cwd}/{uuid}.jsonl`
- Path encoding: path separators replaced with `--` (e.g., `C--code-commandbase-test-end-to-end-test/`)
- Each `/clear` creates a new UUID and new `.jsonl` file
- Subagent transcripts: `{uuid}/subagents/agent-{id}.jsonl`

**JSONL entry types:**

| Type | Fields | Use for Learning Extraction |
|------|--------|-----------------------------|
| `user` (message) | `message.role`, `message.content` (text) | User questions, context |
| `assistant` (message) | `message.content[]` (text, tool_use, thinking) | Claude's reasoning, tool calls |
| `user` (tool_result) | `toolUseResult`, `is_error`, `tool_use_id` | Errors, results, outcomes |
| `progress` | `data.hookEvent`, `data.command` | Hook execution tracking |
| `system` | `subtype` (turn_duration, stop_hook_summary) | Session metadata |

**Key fields for learning extraction:**
- `message.content[].type: "tool_use"` — tool name + input
- `message.content[].is_error: true` — tool failures
- `message.content[].type: "thinking"` — Claude's reasoning about problems
- `toolUseResult` — structured result (varies by tool: stdout/stderr for Bash, filePath for Read/Edit)
- `timestamp` — ISO 8601 on every entry
- `parentUuid` — links entries into conversation flow

**Error detection patterns:**
- `is_error === true` in tool_result content
- Bash `toolUseResult.stderr` non-empty
- `type === "progress"` with `hookEvent === "PostToolUseFailure"`

**Transcript sizes observed:**
- Small session (~10 min): 200 lines, ~220KB
- Medium session (~30-60 min): 300-345 lines, ~1.2-1.6MB
- Each line: 500-3000 chars depending on content

**Existing parsing code to reuse:**
- `harvest-errors.py` (lines 168-246) provides complete JSONL streaming, entry filtering, tool_use indexing, and error extraction — same pattern works for learning candidate extraction

### 5. Hook Installation — Manual vs Plugin

**Currently installed in `~/.claude/settings.json`** (4 hooks, all manual):

| Hook Event | Script | Plugin Source | Installed? |
|------------|--------|---------------|------------|
| PostToolUse (Bash) | `nudge-commit-skill.py` | commandbase-git-workflow | Yes (manual) |
| PostToolUseFailure (*) | `track-errors.py` | commandbase-session | Yes (manual) |
| PreCompact (*) | `trigger-learning.py` | commandbase-session | Yes (manual) |
| Stop | `harvest-errors.py` | commandbase-session | Yes (manual) |
| **SessionStart** | **detect-session.py** | **commandbase-session** | **NO** |

**Manual scripts location**: `~/.claude/hooks/*.py`
**Plugin scripts location**: `plugins/{plugin}/scripts/*.py`

**Key difference**: Manual hooks use hardcoded `~/.claude/hooks/` paths. Plugin hooks use `${CLAUDE_PLUGIN_ROOT}/scripts/` and import shared `session_utils.py`. The manual versions have standalone session resolution logic (duplicated in each script), while plugin versions share the utility module.

**SessionStart hook is the critical missing piece** — without it:
- No session context injected into conversations
- Claude UUID not captured or persisted
- `/learning-from-sessions` post-session mode can't map session name to transcript files

**To install manually**, add to `~/.claude/settings.json` hooks array:
```json
{
  "matcher": "",
  "hooks": [{
    "type": "command",
    "command": "bash -c 'python3 ~/.claude/hooks/detect-session.py'"
  }]
}
```
And copy `detect-session.py` + `session_utils.py` to `~/.claude/hooks/`.

## Architecture Notes

### meta.json Schema Change

**Current** (`starting-session/SKILL.md:199-209`):
```json
{
  "sessionId": "<single string>",
  "name": "...", "branch": "...", "worktree": "...",
  "created": "...", "gitBranch": "..."
}
```

**Proposed**:
```json
{
  "sessionId": "<session-name for backward compat>",
  "claudeSessionIds": ["<uuid1>", "<uuid2>", ...],
  "name": "...", "branch": "...", "worktree": "...",
  "created": "...", "gitBranch": "..."
}
```

`claudeSessionIds` is an array because:
- `/clear` creates new transcript files with new UUIDs
- A single session lifecycle can span multiple Claude conversations
- `SessionStart` hook fires after each `/clear`, appending new UUIDs

### Worktree Removal Constraint

Claude Code's cwd cannot be changed mid-session. When `/ending-session` runs from inside a session worktree:
- `cd {container}/main` in bash changes the shell's cwd for that command only
- Claude Code's actual working directory remains the worktree
- Windows/MINGW locks directories with active processes
- `git worktree remove` fails with Permission denied
- Partial removal: git unregisters the worktree, directory persists

**Two viable approaches:**
1. **Document manual cleanup**: After `/ending-session`, user must manually `rm -rf` the worktree directory and delete the remote branch
2. **Deferred cleanup script**: `/ending-session` writes a cleanup script that the user runs after exiting Claude Code

### Transcript-Based Learning Extraction

The path from session name to transcript files:
1. Session name → `meta.json` → `claudeSessionIds[]`
2. Session worktree path → path-encoded form (e.g., `/c/code/project/feature/auth` → `C--code-project-feature-auth`)
3. `~/.claude/projects/{encoded-path}/{uuid}.jsonl` for each UUID in array

Parsing approach: reuse `harvest-errors.py` JSONL streaming pattern, but extract conversation sequences (error → investigation → resolution) instead of just errors.

## Open Questions

1. **Should `/ending-session` be run from the session worktree or from main?** Running from main avoids the cwd-lock issue entirely but requires the user to switch directories before ending.
2. **Should manual hook scripts be updated to import session_utils.py?** Currently they have duplicated standalone logic. Importing from the plugin path would create a dependency on the plugin being present.
3. **How large can transcripts get for long sessions?** The observed max was ~1.6MB. Need to consider memory/parsing performance for the post-session learning extraction.
4. **Should the nudge hook use transcript parsing or the simpler sentinel file approach?** Transcript parsing is more reliable but has a performance cost on every Bash tool call.
