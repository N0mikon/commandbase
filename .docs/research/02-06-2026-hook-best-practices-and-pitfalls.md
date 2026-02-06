# Hook Best Practices, Use Cases, and Rules

**Date:** 02-06-2026
**Query:** Best practices, use cases, and rules for creating Claude Code hooks
**Status:** Complete

## TL;DR

Hooks are deterministic shell commands that enforce rules Claude can't rationalize away. The community consensus is: CLAUDE.md for guidance, hooks for enforcement. Key patterns: block-at-commit (not block-at-write), smart dispatchers (not broad matchers), exit code discipline (0/1/2), and progressive enforcement (warn first, then block).

## Best Practices (Cross-Referenced)

### 1. Block-at-Commit, Not Block-at-Write

**Sources:** [Shrivu Shankar](https://blog.sshh.io/p/how-i-use-every-claude-code-feature), [KDnuggets](https://ai-report.kdnuggets.com/p/claude-code-anti-patterns-exposed), [ClaudeLog](https://claudelog.com/mechanics/hooks/)

Blocking Edit/Write tools mid-plan "confuses or frustrates" the agent. Let Claude complete its work, then validate the finished result at commit time.

```
GOOD: PreToolUse on Bash(git commit) → validate → block if tests fail
BAD:  PreToolUse on Edit|Write → block mid-edit → agent confused
```

### 2. Exit Code Discipline

**Sources:** [Official docs](https://code.claude.com/docs/en/hooks), [Anthropic reference implementation](https://github.com/anthropics/claude-code/blob/main/examples/hooks/bash_command_validator_example.py)

| Exit Code | Meaning | stdout | stderr |
|-----------|---------|--------|--------|
| **0** | Success, allow | Parsed as JSON (if valid) | Shown in verbose mode only |
| **1** | Non-blocking error | Ignored | Shown to user in verbose mode |
| **2** | Blocking error | **Ignored** | **Fed to Claude as feedback** |

Critical: exit 2 ignores JSON stdout entirely. Don't mix exit 2 with JSON output — choose one approach.

### 3. Smart Dispatchers Over Broad Matchers

**Sources:** [eesel.ai](https://www.eesel.ai/blog/hooks-in-claude-code), [ClaudeLog](https://claudelog.com/mechanics/hooks/)

Don't run expensive validation on every Bash call. Filter early:

```python
command = input_data.get("tool_input", {}).get("command", "")
if not re.search(r'\bgit\s+commit\b', command):
    sys.exit(0)  # Exit fast for non-matching commands
# ... expensive validation only for matching commands
```

### 4. Progressive Enforcement

**Sources:** [paddo.dev](https://paddo.dev/blog/claude-code-hooks-guardrails/), [karanb192/claude-code-hooks](https://github.com/karanb192/claude-code-hooks)

Start with warnings, escalate to blocks after establishing a baseline:
1. Week 1: PostToolUse logging (observe patterns)
2. Week 2: PostToolUse warnings (nudge behavior)
3. Week 3: PreToolUse blocking (enforce rules)

### 5. Always Quote Shell Variables

**Source:** [Official docs](https://code.claude.com/docs/en/hooks#security-considerations)

```bash
# GOOD
FILE_PATH="$(echo "$INPUT" | jq -r '.tool_input.file_path')"

# BAD — path injection risk
FILE_PATH=$(echo $INPUT | jq -r .tool_input.file_path)
```

### 6. Handle JSON Parsing Failures Gracefully

**Sources:** [Official reference implementation](https://github.com/anthropics/claude-code/blob/main/examples/hooks/bash_command_validator_example.py), [DataCamp](https://www.datacamp.com/tutorial/claude-code-hooks)

```python
try:
    input_data = json.load(sys.stdin)
except json.JSONDecodeError as e:
    print(f"Error: Invalid JSON input: {e}", file=sys.stderr)
    sys.exit(1)  # Non-blocking error, don't disrupt workflow
```

### 7. Prevent Stop Hook Infinite Loops

**Source:** [Official hooks guide](https://code.claude.com/docs/en/hooks-guide#stop-hook-runs-forever)

Stop hooks MUST check `stop_hook_active` to avoid re-triggering:

```bash
ACTIVE=$(jq -r '.stop_hook_active' < /dev/stdin)
if [ "$ACTIVE" = "true" ]; then exit 0; fi
```

### 8. Guard Against Shell Profile Pollution

**Sources:** [Official docs](https://code.claude.com/docs/en/hooks), [DataCamp](https://www.datacamp.com/tutorial/claude-code-hooks)

Unconditional `echo` in `.bashrc`/`.zshrc` breaks hook JSON parsing. Wrap in interactive check:

```bash
if [[ $- == *i* ]]; then
  echo "Shell ready"
fi
```

## Common Use Cases

### Tier 1: High Value, Low Risk
- **Auto-format after edits** — PostToolUse on Edit|Write → run Prettier/ESLint (most common use case)
- **Block destructive commands** — PreToolUse on Bash → block `rm -rf`, fork bombs, `curl|sh`
- **Protect sensitive files** — PreToolUse on Edit|Write|Read → block `.env`, credentials, `.git/`
- **Desktop notifications** — Notification hook → system alert when Claude needs input

### Tier 2: Workflow Enforcement
- **Commit workflow** — PostToolUse nudge + deny rules (our 3-layer pattern)
- **Test gates** — PreToolUse on Bash(git commit) → check if tests passed
- **Branch protection** — PreToolUse on Bash → block direct commits to main
- **Auto-stage files** — PostToolUse on Edit|Write → `git add` modified files

### Tier 3: Advanced
- **Context injection** — SessionStart → load git status, recent issues, env vars
- **Context preservation** — SessionStart with matcher "compact" → re-inject critical rules
- **Audit logging** — PostToolUse → log all tool calls as JSON to `logs/` directory
- **MCP tool hooks** — Match `mcp__<server>__<tool>` patterns for external integrations

## Anti-Patterns

| Anti-Pattern | Problem | Better Approach |
|---|---|---|
| Block-at-write | Confuses agent mid-plan | Block-at-commit |
| Broad matchers | Expensive validation on `ls`, `pwd` | Smart dispatcher, exit early |
| Silent failures | Hook fails, nobody knows | JSON logging to `logs/` directory |
| Mixing exit 2 + JSON | JSON ignored on exit 2 | Choose one: exit codes OR JSON |
| No `stop_hook_active` check | Infinite loop | Parse and exit early if true |
| Shell echo in profile | Breaks JSON parsing | Wrap in interactive check |
| Blocking legitimate workflows | Skill's own commands blocked | Deny only patterns skill never uses |
| One-size-fits-all blocking | Too aggressive | Configurable safety levels |
| Trusting CLAUDE.md for enforcement | ~50-80% compliance | Hooks for enforcement, CLAUDE.md for guidance |

## Known Bugs and Pitfalls

### Critical
- **PreToolUse exit codes sometimes ignored** ([#21988](https://github.com/anthropics/claude-code/issues/21988)) — Hook exits 2 but tool executes anyway. May be version-dependent.
- **Hooks stop after ~2.5 hours** ([#16047](https://github.com/anthropics/claude-code/issues/16047)) — `~/.claude/hooks.log` grows to ~48GB. Fix: delete the log file or implement rotation.
- **Post/PreToolUse hooks not executing** ([#6305](https://github.com/anthropics/claude-code/issues/6305)) — Correctly configured but never fire. Other hook types work fine.

### Cross-Platform
- **Windows: `~` not expanded by Python** — Wrap in `bash -c` for tilde expansion (confirmed in our session)
- **Windows: Git Bash stdout→stderr routing** ([#20034](https://github.com/anthropics/claude-code/issues/20034)) — Hook stdout incorrectly routed to stderr
- **Windows: Missing `cat`, `jq`, `xargs`** — Use Python or Node.js instead of shell pipelines
- **macOS: Sandbox blocks `/bin/sh`** ([#20211](https://github.com/anthropics/claude-code/issues/20211)) — Plugin hooks fail with `ENOENT posix_spawn`

### Configuration
- **Hooks snapshot at startup** — Changes don't take effect mid-session. Must restart or use `/hooks` menu.
- **Plugin hooks execution gaps** ([#10225](https://github.com/anthropics/claude-code/issues/10225)) — Some event types don't fire from plugins
- **Home directory trust** ([#15629](https://github.com/anthropics/claude-code/issues/15629)) — User-level hooks don't trigger when running from `~`
- **False "hook error" messages** ([#10463](https://github.com/anthropics/claude-code/issues/10463)) — Empty output (0 bytes) on exit 0 shown as error

## Hook Types Reference

| Type | Use When | Timeout Default | Can Block? |
|------|----------|----------------|------------|
| `command` | Deterministic rules, regex matching, file checks | 600s (10 min) | Yes (exit 2) |
| `prompt` | Judgment-based decisions, LLM evaluation | 30s | Yes (`ok: false`) |
| `agent` | Multi-turn verification, needs file access | 60s | Yes (`ok: false`) |

## Configuration Scope

| Location | Scope | Shareable | Takes Effect |
|----------|-------|-----------|-------------|
| `~/.claude/settings.json` | All projects | No | Next session |
| `.claude/settings.json` | Single project | Yes (commit) | Next session |
| `.claude/settings.local.json` | Single project | No (gitignored) | Next session |
| Managed policy | Organization | Admin-controlled | Next session |
| Plugin `hooks/hooks.json` | When enabled | Yes | Next session |
| Skill/agent frontmatter | Component lifecycle | Yes | Immediate |

## Anthropic's Official Reference Implementation

From [bash_command_validator_example.py](https://github.com/anthropics/claude-code/blob/main/examples/hooks/bash_command_validator_example.py):

```python
#!/usr/bin/env python3
import json, re, sys

_VALIDATION_RULES = [
    (r"^grep\b(?!.*\|)", "Use 'rg' instead of 'grep'"),
    (r"^find\s+\S+\s+-name\b", "Use 'rg --files | rg pattern' instead of 'find -name'"),
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
        sys.exit(1)
    tool_name = input_data.get("tool_name", "")
    if tool_name != "Bash":
        sys.exit(0)
    command = input_data.get("tool_input", {}).get("command", "")
    if not command:
        sys.exit(0)
    issues = _validate_command(command)
    if issues:
        for message in issues:
            print(f"• {message}", file=sys.stderr)
        sys.exit(2)

if __name__ == "__main__":
    main()
```

Key patterns: explicit exit codes, JSON error handling, tool name filtering, extensible rules, stderr messaging.

## Sources

### Official
- [Hooks Guide](https://code.claude.com/docs/en/hooks-guide)
- [Hooks Reference](https://code.claude.com/docs/en/hooks)
- [Best Practices](https://code.claude.com/docs/en/best-practices)
- [bash_command_validator_example.py](https://github.com/anthropics/claude-code/blob/main/examples/hooks/bash_command_validator_example.py)

### Community Repos
- [disler/claude-code-hooks-mastery](https://github.com/disler/claude-code-hooks-mastery)
- [karanb192/claude-code-hooks](https://github.com/karanb192/claude-code-hooks)
- [ChrisWiles/claude-code-showcase](https://github.com/ChrisWiles/claude-code-showcase)
- [affaan-m/everything-claude-code](https://github.com/affaan-m/everything-claude-code)

### Tutorials
- [DataCamp: Practical Guide to Hooks](https://www.datacamp.com/tutorial/claude-code-hooks)
- [eesel.ai: Complete Guide to Hooks](https://www.eesel.ai/blog/hooks-in-claude-code)
- [paddo.dev: Guardrails That Actually Work](https://paddo.dev/blog/claude-code-hooks-guardrails/)
- [Shrivu Shankar: How I Use Every Feature](https://blog.sshh.io/p/how-i-use-every-claude-code-feature)
- [ClaudeLog: Hooks Mechanics](https://claudelog.com/mechanics/hooks/)

### GitHub Issues
- [#21988: PreToolUse exit codes ignored](https://github.com/anthropics/claude-code/issues/21988)
- [#6305: Post/PreToolUse hooks not executing](https://github.com/anthropics/claude-code/issues/6305)
- [#16047: Hooks stop after ~2.5 hours](https://github.com/anthropics/claude-code/issues/16047)
- [#20034: Git Bash stdout routing](https://github.com/anthropics/claude-code/issues/20034)
- [#20211: Sandbox blocks /bin/sh](https://github.com/anthropics/claude-code/issues/20211)
- [#10225: Plugin hooks don't execute](https://github.com/anthropics/claude-code/issues/10225)
- [#10463: False "hook error" messages](https://github.com/anthropics/claude-code/issues/10463)
- [#15629: Home directory trust issue](https://github.com/anthropics/claude-code/issues/15629)
- [#2814: Configuration not respected](https://github.com/anthropics/claude-code/issues/2814)
