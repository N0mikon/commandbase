---
date_researched: 2026-02-06
status: current
---

# Dependency Compatibility Matrix

## Version Matrix

| Dependency | Version | Compatible With | Notes |
|-----------|---------|-----------------|-------|
| Claude Code CLI | Latest | - | Primary platform |
| Skills Spec | Current (SKILL.md) | Claude Code CLI | Stable format |
| Hooks API | Current (7 events) | Claude Code CLI | Stable, expanding |
| Agents Spec | Current (.md format) | Claude Code CLI | Stable format |
| claude-code-hook-sdk | npm latest | Claude Code Hooks API | TypeScript, optional |
| Python 3.x | 3.8+ | Claude Code Hooks API | Current hook runtime |
| Node.js / tsx | 18+ | claude-code-hook-sdk | Required if using SDK |

## Known Conflicts

- **Python hooks vs TypeScript hooks**: No conflict — hooks are independent executables. A project can mix Python and TypeScript hooks. Each hook entry in `settings.json` specifies its own command.

- **Skill `hooks` frontmatter vs global hooks**: Skill-scoped hooks (defined in SKILL.md frontmatter) only run while the skill is active. They do NOT conflict with global hooks in `settings.json`. Both can coexist.

- **Hook self-block deadlock**: If a hook triggers the same tool it's attached to (e.g., a PostToolUse hook for `Bash` that runs a bash command), it can cause infinite recursion. The SDK and Claude Code have guards, but it's a known pitfall. Mitigation: use `matcher` patterns to scope hooks narrowly.

## Minimum Requirements

- Claude Code CLI: Latest version
- Package manager: npm (for hook SDK) or pip (for Python hooks)
- OS: Windows (MINGW64), macOS, Linux all supported
- Python: 3.8+ (for existing Python hooks)
- Node.js: 18+ (only if adopting TypeScript hook SDK)

## Setup Verification Commands

```bash
# Verify Claude Code is installed
claude --version

# Verify skills are loaded
ls ~/.claude/skills/

# Verify agents are loaded
ls ~/.claude/agents/

# Verify hooks are configured
cat ~/.claude/settings.json | python -m json.tool

# Verify hook SDK (if installed)
npx tsx --version

# Test a hook manually (Python)
echo '{"session_id":"test","transcript_path":"/tmp/t","hook_event_name":"PreToolUse","tool_name":"Bash","tool_input":{"command":"echo test"}}' | python ~/.claude/hooks/nudge-commit-skill.py
```

## Migration Path: Python Hooks to TypeScript SDK

If we decide to migrate existing Python hooks to the TypeScript SDK:

1. Install SDK: `npm install -D @mizunashi_mana/claude-code-hook-sdk tsx`
2. Rewrite hook using `runHook()` with typed handlers
3. Update `settings.json` command from `python script.py` to `npx tsx script.ts`
4. Use `preToolRejectHook` for command-blocking hooks (replaces manual JSON parsing)
5. Use `runHookCaller` for unit testing

**Trade-off:** Adds Node.js as a dependency for hooks. Current Python hooks work fine but lack type safety and utility functions.

## Sources

- Context7: `/llmstxt/code_claude_llms_txt` - Claude Code specification
- Context7: `/mizunashi-mana/claude-code-hook-sdk` - Hook SDK docs
- Context7: `/davepoon/claude-code-subagents-collection` - Agent format reference
- Context7: `/davila7/claude-code-templates` - Community patterns
