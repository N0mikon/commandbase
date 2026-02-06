---
name: creating-hooks
description: "Use this skill when creating Claude Code hooks (PreToolUse, PostToolUse, SessionStart, Stop, etc.), configuring deny rules in settings.json, or debugging hook execution issues. Covers hook lifecycle events, exit code semantics, Windows/MINGW compatibility, self-block deadlocks with skills, the 3-layer enforcement pattern, and known pitfalls. Trigger phrases: 'create a hook', 'add a hook', 'hook not firing', 'deny rule', 'enforce workflow'."
---

# Creating Hooks

You are creating or debugging Claude Code hooks — deterministic shell commands that enforce rules Claude can't rationalize away. Use this skill as a reference for hook development patterns, known pitfalls, and the correct approach for each use case.

**Violating the letter of these rules is violating the spirit of these rules.**

## The Iron Law

```
NO HOOK WITHOUT TESTING EXIT CODES AND CHECKING FOR SELF-BLOCK
```

Every hook must be tested with mock input before deployment, and every blocking hook must be checked against existing skills for deadlock.

**No exceptions:**
- Don't deploy without testing `echo '{"tool_name":"Bash","tool_input":{"command":"..."}}' | python3 hook.py`
- Don't block a pattern without checking if any skill uses it
- Don't mix exit code 2 with JSON stdout (exit 2 ignores JSON)
- Don't skip the restart — hooks snapshot at session startup

## The Gate Function

```
BEFORE deploying any hook:

1. CHOOSE: Right event type (see Decision Guide)
2. WRITE: Script with proper JSON parsing and exit codes
3. TEST: Mock input via stdin, verify exit codes and stderr
4. SELF-BLOCK CHECK: Does any skill use the pattern being blocked?
   - If YES: Use PostToolUse nudge, not PreToolUse block
   - If NO: PreToolUse block is safe
5. DENY AUDIT: Identify patterns no skill should ever use → add deny rules
6. DEPLOY: Copy script to ~/.claude/hooks/, merge settings-snippet.json
7. RESTART: New session required for hooks to take effect
8. VERIFY: Run the triggering command in a live session

Skip testing = broken hooks in production
Skip self-block check = deadlocked skills
```

## Hook Event Decision Guide

| You Want To... | Use Event | Can Block? | Notes |
|---|---|---|---|
| Prevent a dangerous command | `PreToolUse` | Yes (exit 2) | Check for self-block with skills |
| Nudge toward correct workflow | `PostToolUse` | No (feedback only) | Exit 2 sends stderr to Claude |
| Validate before commit | `PreToolUse` on Bash | Yes | Block-at-commit pattern |
| Auto-format after edits | `PostToolUse` on Edit\|Write | No | Most common use case |
| Inject context at start | `SessionStart` | No | stdout added to Claude context |
| Re-inject after compaction | `SessionStart` matcher "compact" | No | Preserves critical rules |
| Keep Claude working | `Stop` | Yes | MUST check `stop_hook_active` |
| Block user prompt | `UserPromptSubmit` | Yes | No matcher support |
| Auto-approve trusted tool | `PermissionRequest` | Yes | Use with caution |
| Log all tool calls | `PostToolUse` | No | Use async for performance |

## Hook Lifecycle (All 12 Events)

| Event | When | Can Block? | Exit 2 Effect |
|-------|------|------------|---------------|
| `SessionStart` | Session begins/resumes | No | stdout added as Claude context |
| `UserPromptSubmit` | User submits prompt | Yes | Blocks prompt, erases it |
| `PreToolUse` | Before tool executes | Yes | Blocks the tool call |
| `PermissionRequest` | Permission dialog appears | Yes | Denies permission |
| `PostToolUse` | After tool succeeds | No | stderr shown to Claude as feedback |
| `PostToolUseFailure` | After tool fails | No | stderr shown to Claude |
| `Notification` | Claude sends notification | No | stderr shown to user only |
| `SubagentStart` | Subagent spawns | No | stderr shown to user only |
| `SubagentStop` | Subagent finishes | Yes | Prevents subagent stopping |
| `Stop` | Claude finishes responding | Yes | Prevents stopping, continues |
| `PreCompact` | Before context compaction | No | stderr shown to user only |
| `SessionEnd` | Session terminates | No | stderr shown to user only |

## Exit Code Rules

| Exit Code | Meaning | stdout | stderr |
|-----------|---------|--------|--------|
| **0** | Success, allow | Parsed as JSON (if valid) | Shown in verbose mode only |
| **1** | Non-blocking error | Ignored | Shown to user in verbose mode |
| **2** | Blocking error | **Ignored entirely** | **Fed to Claude as feedback** |

**Critical:** Exit 2 ignores JSON stdout. Don't mix exit 2 with JSON output — choose one approach:
- Simple block/allow → use exit codes (0 or 2) with stderr messages
- Structured control → use exit 0 with JSON `permissionDecision` in stdout

## Patterns

### Pattern 1: Smart Dispatcher (Early Exit)

Don't run expensive logic on every Bash call. Filter first:

```python
command = input_data.get("tool_input", {}).get("command", "")
if not re.search(r'\bgit\s+commit\b', command):
    sys.exit(0)  # Exit fast for non-matching commands
# ... expensive validation only for matching commands
```

### Pattern 2: Block-at-Commit (Not Block-at-Write)

Blocking Edit/Write mid-plan confuses the agent. Validate at commit time instead:

```
GOOD: PreToolUse on Bash → detect git commit → validate → block if checks fail
BAD:  PreToolUse on Edit|Write → block mid-edit → agent confused/frustrated
```

### Pattern 3: PostToolUse Nudge

Detect violations after they happen, send feedback for future compliance:

```python
if re.search(r"\bgit\s+(commit|push)\b", command):
    print("NOTICE: Use /committing-changes for commits.", file=sys.stderr)
    sys.exit(2)  # stderr delivered to Claude as feedback
```

### Pattern 4: 3-Layer Enforcement

When enforcing a workflow skill without deadlock:

1. **CLAUDE.md rule** — `NEVER do X, ALWAYS use /skill`. ~70-80% compliance.
2. **PostToolUse nudge** — Detects violations, sends feedback. No deadlock.
3. **Deny rules** — Hard-blocks patterns the skill never uses. No deadlock.

### Pattern 5: Stop Hook Loop Prevention

Stop hooks MUST check `stop_hook_active`:

```bash
ACTIVE=$(jq -r '.stop_hook_active' < /dev/stdin)
if [ "$ACTIVE" = "true" ]; then exit 0; fi
# ... rest of hook logic
```

### Pattern 6: Progressive Enforcement

Don't start with hard blocks. Escalate over time:
1. **Week 1:** PostToolUse logging (observe patterns)
2. **Week 2:** PostToolUse warnings (nudge behavior)
3. **Week 3:** PreToolUse blocking (enforce rules)

## Critical Pitfalls

### Platform-Specific

| Platform | Pitfall | Fix |
|---|---|---|
| **Windows/MINGW** | `python3 ~/...` fails — Python doesn't expand `~` | Wrap: `bash -c 'python3 ~/.claude/hooks/script.py'` |
| **Windows/MINGW** | Missing `cat`, `jq`, `xargs` | Use Python or Node.js instead of shell pipelines |
| **Windows/Git Bash** | stdout routed to stderr ([#20034](https://github.com/anthropics/claude-code/issues/20034)) | Known bug; use Python for reliable output handling |
| **macOS** | Sandbox blocks `/bin/sh` ([#20211](https://github.com/anthropics/claude-code/issues/20211)) | Plugin hooks affected; user-level hooks unaffected |

### Behavioral

| Pitfall | Consequence | Fix |
|---|---|---|
| Hooks snapshot at startup | Config changes ignored mid-session | Restart Claude Code after every hook change |
| `~/.claude/hooks.log` bloat | Hooks silently stop after ~2.5h ([#16047](https://github.com/anthropics/claude-code/issues/16047)) | Delete log file or implement rotation |
| Shell profile `echo` | Breaks JSON parsing in hooks | Wrap: `if [[ $- == *i* ]]; then echo ...; fi` |
| PreToolUse self-block | Skill's own commands blocked, deadlock | Use PostToolUse nudge + deny rules instead |
| Broad matchers | Expensive logic on every `ls`, `pwd` | Smart dispatcher with early exit |
| Exit 2 + JSON | JSON stdout ignored on exit 2 | Choose one: exit codes OR JSON output |

### Known Bugs

- **PreToolUse exit codes sometimes ignored** ([#21988](https://github.com/anthropics/claude-code/issues/21988))
- **Post/PreToolUse hooks not executing** ([#6305](https://github.com/anthropics/claude-code/issues/6305))
- **False "hook error" on empty output** ([#10463](https://github.com/anthropics/claude-code/issues/10463))
- **Plugin hooks have execution gaps** ([#10225](https://github.com/anthropics/claude-code/issues/10225))

## Anti-Patterns

| Anti-Pattern | Problem | Better Approach |
|---|---|---|
| Block-at-write | Confuses agent mid-plan | Block-at-commit |
| Broad matchers | Expensive validation on `ls` | Smart dispatcher, exit early |
| Silent failures | Hook fails, nobody knows | Log to `logs/` directory |
| Mixing exit 2 + JSON | JSON ignored | Choose one approach |
| No `stop_hook_active` check | Infinite loop | Parse and exit early |
| Trusting CLAUDE.md alone | ~50-80% compliance | Hooks for enforcement |
| Blocking skill patterns | Deadlock | Deny only patterns skill never uses |

## Reference Implementation

From [Anthropic's official example](https://github.com/anthropics/claude-code/blob/main/examples/hooks/bash_command_validator_example.py):

```python
#!/usr/bin/env python3
import json, re, sys

_VALIDATION_RULES = [
    (r"^grep\b(?!.*\|)", "Use 'rg' instead of 'grep'"),
    (r"^find\s+\S+\s+-name\b", "Use 'rg --files' instead of 'find -name'"),
]

def _validate_command(command: str) -> list[str]:
    issues = []
    for pattern, message in _VALIDATION_RULES:
        if re.search(pattern, command):
            issues.append(message)
    return issues

def main():
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON input: {e}", file=sys.stderr)
        sys.exit(1)  # Non-blocking error
    if input_data.get("tool_name") != "Bash":
        sys.exit(0)
    command = input_data.get("tool_input", {}).get("command", "")
    if not command:
        sys.exit(0)
    issues = _validate_command(command)
    if issues:
        for msg in issues:
            print(f"• {msg}", file=sys.stderr)
        sys.exit(2)  # Block and show to Claude

if __name__ == "__main__":
    main()
```

Key patterns: explicit exit codes, JSON error handling, tool name filtering, extensible rules, stderr messaging.

## Hook Input Format

```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/transcript.jsonl",
  "cwd": "/current/directory",
  "permission_mode": "default",
  "hook_event_name": "PreToolUse",
  "tool_name": "Bash",
  "tool_input": {
    "command": "git commit -m 'message'",
    "description": "Commit changes",
    "timeout": 120000
  }
}
```

## Configuration

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "bash -c 'python3 ~/.claude/hooks/my-hook.py'",
            "timeout": 5
          }
        ]
      }
    ]
  }
}
```

**Scope hierarchy:** Managed policy > User (`~/.claude/settings.json`) > Project (`.claude/settings.json`) > Local (`.claude/settings.local.json`) > Plugin > Skill/agent frontmatter

**Timeout defaults:** Command = 600s, Prompt = 30s, Agent = 60s

## Development Checklist

- [ ] Choose the right event (see Decision Guide)
- [ ] Write script with proper JSON parsing and error handling
- [ ] Use `bash -c 'python3 ...'` for Python hooks on Windows/MINGW
- [ ] Test with mock stdin: `echo '{"tool_name":"Bash",...}' | python3 hook.py; echo $?`
- [ ] Verify exit codes: 0 = allow, 2 = block/feedback
- [ ] Check for self-block: does any skill use the pattern being blocked?
- [ ] Add deny rules for patterns no skill should ever use
- [ ] Store source in `newhooks/hookname/` with `settings-snippet.json`
- [ ] Deploy to `~/.claude/hooks/` and merge snippet into settings
- [ ] Restart Claude Code (hooks snapshot at startup)
- [ ] Verify in a live session

## File Organization

```
newhooks/
└── hook-name/
    ├── hook-name.py           # The hook script
    └── settings-snippet.json  # Hook config + related deny rules
```

Deploy: copy `.py` to `~/.claude/hooks/`, merge snippet into `~/.claude/settings.json`.

## Red Flags - STOP and Verify

If you notice any of these, pause:

- About to deploy a hook without testing with mock input
- Using PreToolUse to block a pattern a skill needs (deadlock)
- Mixing exit code 2 with JSON stdout output
- Skipping the restart after config changes
- Using broad matchers without early-exit filtering
- Writing a Stop hook without `stop_hook_active` check
- Blocking Edit/Write tools (block-at-commit instead)

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "I tested it manually, deploy is fine" | Test with mock stdin through the actual script. Manual != automated. |
| "This PreToolUse block won't affect skills" | Check every skill that uses Bash. Self-block creates deadlock. |
| "Exit 2 with JSON gives more control" | Exit 2 ignores JSON stdout entirely. Choose one approach. |
| "I'll restart later" | Hooks snapshot at startup. Your change is invisible until restart. |
| "Matching all Bash is fine for now" | Smart dispatcher with early exit. Don't tax every `ls` and `pwd`. |
| "CLAUDE.md rule is enough" | ~50-80% compliance. Hooks are enforcement. CLAUDE.md is guidance. |

## The Bottom Line

**No hook without testing and self-block verification.**

Choose the right event. Write with proper exit codes. Test with mock input. Check for skill deadlocks. Deploy and restart. Verify live.

This is non-negotiable. Every hook. Every time.
