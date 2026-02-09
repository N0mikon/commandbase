# commandbase

Personal Claude Code workflow tools — skills, agents, and hooks for the RPI workflow (research, plan, implement, validate).

## Windows Setup

### Required: Set Git Bash Path

Claude Code must use Git Bash (not WSL bash) for hook execution. Without this, `${CLAUDE_PLUGIN_ROOT}` paths are mangled and all plugin hooks fail.

```cmd
setx CLAUDE_CODE_GIT_BASH_PATH "C:\Program Files\Git\bin\bash.exe"
```

Restart Claude Code after setting this.

**Why:** Windows has multiple `bash.exe` installs (`C:\Windows\System32\bash.exe` for WSL, `C:\Program Files\Git\usr\bin\bash.exe` for MINGW). Claude Code may pick the wrong one, causing path separator stripping in `${CLAUDE_PLUGIN_ROOT}`.
