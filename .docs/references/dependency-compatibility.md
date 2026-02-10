---
git_commit: 8e92bba
last_updated: 2026-02-09
last_updated_by: docs-updater
last_updated_note: "Added git_commit frontmatter, updated hook event count from 7 to 14, updated paths to reflect plugin-based architecture, removed stale verification commands pointing to pre-plugin directories"
date_researched: 2026-02-06
status: current
references:
  - plugins/commandbase-git-workflow/hooks/hooks.json
  - plugins/commandbase-session/hooks/hooks.json
  - plugins/commandbase-meta/skills/creating-hooks/SKILL.md
  - .claude-plugin/marketplace.json
---

# Dependency Compatibility Matrix

## Version Matrix

| Dependency | Version | Compatible With | Notes |
|-----------|---------|-----------------|-------|
| Claude Code CLI | Latest | - | Primary platform |
| Skills Spec | Current (SKILL.md) | Claude Code CLI | Stable format |
| Hooks API | Current (14 events) | Claude Code CLI | Stable, expanding |
| Agents Spec | Current (.md format) | Claude Code CLI | Stable format |
| Plugin Spec | Current (marketplace.json) | Claude Code CLI | Plugin marketplace format |
| Python 3.x | 3.8+ | Claude Code Hooks API | Current hook runtime (all hooks are Python) |
| Node.js / tsx | 18+ | Claude Code CLI | Required for Claude Code itself |

## Known Conflicts

- **Skill `hooks` frontmatter vs global hooks**: Skill-scoped hooks (defined in SKILL.md frontmatter) only run while the skill is active. They do NOT conflict with global hooks in `settings.json`. Both can coexist.

- **Plugin hooks vs user hooks**: Plugin hooks (defined in `plugins/<plugin>/hooks/hooks.json`) are merged with user-level hooks (`~/.claude/settings.json`). Both fire independently. Plugin hooks may require manual installation when skills are copied without the plugin install process (see learnings from end-to-end test session).

- **Hook self-block deadlock**: If a hook triggers the same tool it's attached to (e.g., a PostToolUse hook for `Bash` that runs a bash command), it can cause infinite recursion. Claude Code has guards, but it's a known pitfall. Mitigation: use `matcher` patterns to scope hooks narrowly.

- **Nudge hook false positives inside skills**: The `nudge-commit-skill.py` PostToolUse hook detects `git commit` and `git push` and warns the user, but fires even when `/committing-changes` itself runs these commands. The hook needs skill-awareness to suppress the nudge when the commit originates from within the skill flow.

## Hook Events (14 Total)

| Event | Can Block? | Notes |
|-------|------------|-------|
| `SessionStart` | No | stdout added as Claude context |
| `UserPromptSubmit` | Yes | Blocks prompt, erases it |
| `PreToolUse` | Yes | Blocks the tool call |
| `PermissionRequest` | Yes | Denies permission |
| `PostToolUse` | No | stderr shown to Claude as feedback |
| `PostToolUseFailure` | No | stderr shown to Claude |
| `Notification` | No | stderr shown to user only |
| `SubagentStart` | No | stderr shown to user only |
| `SubagentStop` | Yes | Prevents subagent stopping |
| `Stop` | Yes | Prevents stopping, continues |
| `TeammateIdle` | Yes | Agent teams only |
| `TaskCompleted` | Yes | Prevents task completion |
| `PreCompact` | No | stderr shown to user only |
| `SessionEnd` | No | stderr shown to user only |

Events used in this project: `PostToolUse` (git-workflow), `PostToolUseFailure`, `Stop`, `PreCompact`, `SessionStart` (session).

## Minimum Requirements

- Claude Code CLI: Latest version
- Package manager: npm (for Claude Code)
- OS: Windows (MINGW64), macOS, Linux all supported
- Python: 3.8+ (for all existing hooks)
- Node.js: 18+ (required for Claude Code CLI)

## Setup Verification Commands

```bash
# Verify Claude Code is installed
claude --version

# Verify plugins are installed
ls ~/.claude/plugins/

# Verify marketplace source is configured
cat ~/.claude/settings.json | python -m json.tool

# Test a hook manually (Python, from plugin directory)
echo '{"session_id":"test","transcript_path":"/tmp/t","hook_event_name":"PreToolUse","tool_name":"Bash","tool_input":{"command":"echo test"}}' | python3 plugins/commandbase-git-workflow/scripts/nudge-commit-skill.py
```

## Sources

- Context7: `/llmstxt/code_claude_llms_txt` - Claude Code specification
- `plugins/commandbase-meta/skills/creating-hooks/SKILL.md` - Comprehensive hook reference (14 events, patterns, pitfalls)
- `.docs/learnings/02-08-2026-end-to-end-test-session-learnings.md` - Hook deployment learnings
