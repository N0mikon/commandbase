---
date: 2026-02-09
status: complete
topic: "CLAUDE_PLUGIN_ROOT Windows Path Bug and Cross-Platform Hook Strategies"
tags: [research, hooks, plugins, windows, mingw, CLAUDE_PLUGIN_ROOT, cross-platform]
git_commit: 8e92bba
---

# CLAUDE_PLUGIN_ROOT Windows Path Bug and Cross-Platform Hook Strategies

## Research Question
How does Claude Code resolve `${CLAUDE_PLUGIN_ROOT}` in plugin hooks, and how can we make plugin hooks work cross-platform (especially on Windows/MINGW) for distribution?

## Summary
`${CLAUDE_PLUGIN_ROOT}` has multiple critical bugs on Windows/MINGW that are documented across 10+ GitHub issues. The variable is an environment variable set by Claude Code before hook execution, but on Windows it produces mangled paths (stripped separators, mixed separator styles). No official fix exists as of Feb 2026. The best cross-platform workaround is quoting the variable and using `python` (not `python3`). An alternative is a resolver script that reads `installed_plugins.json` when the variable fails.

## Detailed Findings

### How ${CLAUDE_PLUGIN_ROOT} Works
**Sources:** [Hooks reference](https://code.claude.com/docs/en/hooks), [Plugins reference](https://code.claude.com/docs/en/plugins-reference)

- It's an **environment variable** set by Claude Code before executing hook commands
- Contains the absolute path to the plugin's cached root directory
- Resolves to `~/.claude/plugins/cache/<marketplace>/<plugin>/<version>/`
- Also used in `.mcp.json` and other JSON configs
- Does NOT work in command markdown files (skills, agents) — only in JSON configs

### Windows Bugs (6 documented)

**Bug 1: Path separator stripping/mangling**
**Source:** [Issue #11984](https://github.com/anthropics/claude-code/issues/11984), [Issue #18527](https://github.com/anthropics/claude-code/issues/18527)

On MINGW/Git Bash, backslashes are stripped entirely:
```
Expected: C:\Users\Jason\.claude\plugins\cache\...
Received: UsersJason.claudepluginscache...
```
The path becomes a relative path appended to CWD, producing nonsense like `C:\code\project\UsersJason.claude...`.

**Bug 2: Mixed separator styles**
**Source:** [Issue #18527](https://github.com/anthropics/claude-code/issues/18527)

Windows path + Unix append: `C:\Users\...cache\plugin\version/scripts/hook.py` — bash can't resolve mixed separators.

**Bug 3: Variable not set at all**
**Source:** [Issue #189 (claude-plugins-official)](https://github.com/anthropics/claude-plugins-official/issues/189)

On some Windows configurations, `${CLAUDE_PLUGIN_ROOT}` expands to empty string. Scripts fail with "Cannot find module '/scripts/file.js'".

**Bug 4: Paths with spaces**
**Source:** [Issue #16152](https://github.com/anthropics/claude-code/issues/16152), [Issue #15481](https://github.com/anthropics/claude-code/issues/15481)

Unquoted `${CLAUDE_PLUGIN_ROOT}` with spaces in path (e.g., `C:\Users\JOHN DOE\...`) causes shell to split on space.

**Bug 5: Stale cache version**
**Source:** [Issue #15642](https://github.com/anthropics/claude-code/issues/15642)

After plugin updates, variable may point to old cached version directory.

**Bug 6: python3 vs python**
**Source:** [Issue #16154](https://github.com/anthropics/claude-code/issues/16154)

Windows doesn't have `python3` — only `python`. Cross-platform hooks must use `python`.

### Required Windows Setup: CLAUDE_CODE_GIT_BASH_PATH
**Source:** [Issue #16602](https://github.com/anthropics/claude-code/issues/16602)

Without `CLAUDE_CODE_GIT_BASH_PATH=C:\Program Files\Git\bin\bash.exe`, Claude Code uses cmd.exe for hooks, which can't interpret bash syntax, `$HOME`, or `.sh` scripts.

### Cross-Platform Workarounds

**Option A: Quote the variable + use `python`**
```json
{
  "command": "python \"${CLAUDE_PLUGIN_ROOT}/scripts/hook.py\""
}
```
Fixes spaces-in-path but doesn't fix separator stripping on MINGW.

**Option B: CPR (Claude Plugin Root) resolver script**
**Source:** [Issue #9354](https://github.com/anthropics/claude-code/issues/9354)

A bootstrap script that tries `${CLAUDE_PLUGIN_ROOT}` first, then falls back to reading `~/.claude/plugins/installed_plugins.json` via jq:
```bash
jq -r '.plugins | to_entries[] | select(.key | contains("plugin-name")) | .value.installPath' ~/.claude/plugins/installed_plugins.json
```

**Option C: Inline the hook logic**
**Source:** [Issue #189 (claude-plugins-official)](https://github.com/anthropics/claude-plugins-official/issues/189)

Replace external script calls with inline bash that doesn't depend on the variable. Only works for simple hooks.

**Option D: Use $CLAUDE_PROJECT_DIR for project-local scripts**
Works for scripts in the project repo, not for plugin-bundled scripts.

### Plugin Cache Structure
```
~/.claude/plugins/
├── cache/<marketplace>/<plugin>/<version>/
│   ├── .claude-plugin/plugin.json
│   ├── hooks/hooks.json
│   ├── scripts/
│   └── skills/
├── marketplaces/
└── installed_plugins.json  # tracks versions + installPath
```

`installed_plugins.json` format:
```json
{
  "plugin-name@marketplace": [{
    "scope": "user",
    "installPath": "/home/user/.claude/plugins/cache/marketplace/plugin/2.4.7",
    "version": "2.4.7"
  }]
}
```

## Source Conflicts
- Official docs say `${CLAUDE_PLUGIN_ROOT}` is "available in all command hooks" — multiple issues prove this is not reliably true on Windows.
- Issue #9354 says it's NOT available in command markdown (skills) — only JSON configs. This limits where plugins can reference their own files.
- Some issues report the variable as empty, others report it with mangled separators — suggests the bug manifests differently depending on shell (cmd.exe vs PowerShell vs Git Bash vs MSYS2).

## Currency Assessment
- Most recent source: January-February 2026 (issues #18527, #19037, #19542)
- Topic velocity: Active — new issues filed monthly
- Confidence in currency: High — multiple open/recent issues confirm bugs persist
- Core issues (#11984, #18527) remain open or closed-as-duplicate without fix

## Open Questions
1. Does `installed_plugins.json` use `installPath` as the key, or is the structure different? Need to verify on the actual file.
2. Would a Python-based resolver (reading installed_plugins.json without jq dependency) be more portable?
3. Is there a way to detect the shell type at hook execution time and branch between `cygpath -w` (MINGW) vs direct path (Unix)?
4. Should commandbase hooks use `python` instead of `python3` for cross-platform? This would break Linux systems where only `python3` exists and `python` is Python 2.
5. When will Anthropic actually fix `${CLAUDE_PLUGIN_ROOT}` on Windows? The issue has been open since at least v2.0.47.

## Sources
- [Hooks reference - Claude Code Docs](https://code.claude.com/docs/en/hooks)
- [Plugins reference - Claude Code Docs](https://code.claude.com/docs/en/plugins-reference)
- [Plugin bash hooks fail on Windows (#18527)](https://github.com/anthropics/claude-code/issues/18527)
- [CLAUDE_PLUGIN_ROOT not resolving on Windows (#189)](https://github.com/anthropics/claude-plugins-official/issues/189)
- [CLAUDE_PLUGIN_ROOT portability (#11984)](https://github.com/anthropics/claude-code/issues/11984)
- [CLAUDE_PLUGIN_ROOT in command markdown (#9354)](https://github.com/anthropics/claude-code/issues/9354)
- [Plugin cache stale version (#15642)](https://github.com/anthropics/claude-code/issues/15642)
- [Hooks fail with spaces in path (#16152)](https://github.com/anthropics/claude-code/issues/16152)
- [security-guidance spaces in path (#15481)](https://github.com/anthropics/claude-code/issues/15481)
- [python3 fails on Windows (#16154)](https://github.com/anthropics/claude-code/issues/16154)
- [CLAUDE_CODE_GIT_BASH_PATH required (#16602)](https://github.com/anthropics/claude-code/issues/16602)
- [Windows hook paths incorrectly converted (#19037)](https://github.com/anthropics/claude-code/issues/19037)
- [SessionStart hooks hang (#9542)](https://github.com/anthropics/claude-code/issues/9542)
- [Env var not propagated in hooks (#9447)](https://github.com/anthropics/claude-code/issues/9447)
