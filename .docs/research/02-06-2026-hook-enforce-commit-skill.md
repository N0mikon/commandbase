# Hook to Enforce Commits via /committing-changes Skill

**Date:** 02-06-2026
**Query:** How to create a Claude Code hook that enforces all commits go through the /committing-changes skill
**Status:** Complete

## Key Findings

### The Problem

Claude Code can run `git commit` directly via the Bash tool, bypassing any workflow skill like `/committing-changes`. We want a hook that blocks direct `git commit` commands and forces usage of the skill instead.

### Solution Architecture

**Two-layer approach:**

1. **PreToolUse hook on Bash** — Intercepts `git commit` commands before they execute
2. **Transcript parsing** — Checks whether the `/committing-changes` skill was invoked in the current session

### How PreToolUse Hooks Work

When Claude attempts to use the Bash tool, the hook receives JSON via stdin:

```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/transcript.jsonl",
  "cwd": "/current/directory",
  "hook_event_name": "PreToolUse",
  "tool_name": "Bash",
  "tool_input": {
    "command": "git commit -m 'some message'"
  }
}
```

**Blocking mechanism:**
- **Exit 0** — Allow the command
- **Exit 2** — Block the command; stderr is fed back to Claude as feedback
- **JSON output** — Can return `permissionDecision: "deny"` with a reason

### Implementation Options

#### Option A: Simple Block (Recommended)

Block ALL `git commit` commands from Bash and redirect to the skill. This is the simplest and most reliable approach.

```python
#!/usr/bin/env python3
"""Block git commit commands — must use /committing-changes skill."""
import json
import re
import sys

def main():
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)

    command = input_data.get("tool_input", {}).get("command", "")

    # Match git commit commands (with or without flags)
    if re.search(r'\bgit\s+commit\b', command):
        print(
            "BLOCKED: Direct git commit is not allowed. "
            "Use the /committing-changes skill instead. "
            "Tell the user: 'I need to use /commit to make commits.'",
            file=sys.stderr
        )
        sys.exit(2)

    sys.exit(0)

if __name__ == "__main__":
    main()
```

**Pros:** Simple, reliable, no transcript parsing needed
**Cons:** Blocks git commit even when invoked FROM the skill (need allowlisting)

#### Option B: Transcript-Aware Block

Parse the transcript to check if the `/committing-changes` skill was recently invoked:

```python
#!/usr/bin/env python3
"""Block git commit unless /committing-changes skill is active."""
import json
import re
import sys

def skill_was_invoked(transcript_path):
    """Check if committing-changes skill was invoked in this session."""
    try:
        with open(transcript_path, 'r') as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    # Look for Skill tool invocations
                    if (entry.get("tool_name") == "Skill" and
                        "committing-changes" in str(entry.get("tool_input", {}))):
                        return True
                except json.JSONDecodeError:
                    continue
    except (FileNotFoundError, PermissionError):
        pass
    return False

def main():
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)

    command = input_data.get("tool_input", {}).get("command", "")

    if not re.search(r'\bgit\s+commit\b', command):
        sys.exit(0)  # Not a commit command, allow

    transcript_path = input_data.get("transcript_path", "")
    if transcript_path and skill_was_invoked(transcript_path):
        sys.exit(0)  # Skill was invoked, allow the commit

    print(
        "BLOCKED: Direct git commit is not allowed. "
        "Use /committing-changes (or /commit) skill instead.",
        file=sys.stderr
    )
    sys.exit(2)

if __name__ == "__main__":
    main()
```

**Pros:** Allows commits that originate from the skill
**Cons:** More complex, transcript parsing may be fragile across versions

#### Option C: Also Block git push

Extend to block `git push` as well, since the skill handles both:

```python
# Add to the regex:
if re.search(r'\bgit\s+(commit|push)\b', command):
```

### Hook Configuration

Add to `~/.claude/settings.json` (global) or `.claude/settings.json` (project):

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"$CLAUDE_PROJECT_DIR/.claude/hooks/enforce-commit-skill.py\"",
            "timeout": 5000,
            "statusMessage": "Checking commit policy..."
          }
        ]
      }
    ]
  }
}
```

For global enforcement (all projects):
```json
// In ~/.claude/settings.json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "python3 ~/.claude/hooks/enforce-commit-skill.py",
            "timeout": 5000,
            "statusMessage": "Checking commit policy..."
          }
        ]
      }
    ]
  }
}
```

### Alternative: Deny Rule in Settings

A simpler (but less flexible) approach — use Claude Code's built-in deny rules:

```json
{
  "deny": [
    "Bash(git commit:*)",
    "Bash(git push:*)"
  ]
}
```

**Pros:** Zero code, built-in feature
**Cons:** Hard blocks with no feedback message, user sees a generic deny, Claude can't explain why or redirect to the skill

### Considerations

1. **The skill itself runs git commit** — Option B (transcript-aware) is needed if you want the skill's own `git commit` calls to succeed. Option A requires the skill to work around the block (e.g., by using a different mechanism or being exempted).

2. **Hook snapshots** — Claude Code captures hooks at startup. Changes to hook scripts take effect on next session, not mid-conversation.

3. **Performance** — PreToolUse hooks fire on EVERY Bash command. Keep the script fast (< 100ms). The simple regex check in Option A is near-instant.

4. **Cross-platform** — Use `python3` instead of bash for Windows compatibility (relevant for this repo's MINGW environment).

## Source Conflicts

- Some GitHub issues report that PreToolUse hooks don't consistently block tool calls ([#4362](https://github.com/anthropics/claude-code/issues/4362)), but official docs confirm this is the intended mechanism. May be version-dependent.
- The `deny` rule approach is simpler but less documented for git-specific patterns.

## Sources

- [Hooks reference - Claude Code Docs](https://code.claude.com/docs/en/hooks)
- [Automate workflows with hooks - Claude Code Docs](https://code.claude.com/docs/en/hooks-guide)
- [Preventing git commit --amend with Claude Code Hooks](https://kreako.fr/blog/20250920-claude-code-commit-amend/)
- [Claude Code: Allow Bash(git commit:*) considered harmful](https://microservices.io/post/genaidevelopment/2025/09/10/allow-git-commit-considered-harmful.html)
- [bash_command_validator_example.py - GitHub anthropics/claude-code](https://github.com/anthropics/claude-code/blob/main/examples/hooks/bash_command_validator_example.py)
- [Skill Activation Hook - Claude Fast](https://claudefa.st/blog/tools/hooks/skill-activation-hook)
- [Inside Claude Code Skills - Mikhail Shilkov](https://mikhail.io/2025/10/claude-code-skills/)
- [GitHub - disler/claude-code-hooks-mastery](https://github.com/disler/claude-code-hooks-mastery)
- [GitHub - karanb192/claude-code-hooks](https://github.com/karanb192/claude-code-hooks)
