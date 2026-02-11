# commandbase

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Plugins](https://img.shields.io/badge/plugins-8-green.svg)](#plugins)
[![Skills](https://img.shields.io/badge/skills-46-purple.svg)](#plugins)

Personal Claude Code workflow tools — skills, agents, and hooks for the BRDSPI workflow (brainstorm, research, design, structure, plan, implement).

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Plugins](#plugins)
- [Quick Start](#quick-start)
- [Windows Setup](#windows-setup)
- [Development](#development)
- [Contributing](#contributing)
- [License](#license)

## Overview

commandbase is a collection of Claude Code plugins that give your AI assistant a structured workflow for tackling software projects, managing Obsidian vaults, and running homelab infrastructure. Instead of freeform prompting, you get repeatable phases: brainstorm direction, research the problem, design the architecture, structure files, plan implementation, then build it.

Eight plugins split the work by domain. `commandbase-core` provides shared documentation agents that the rest depend on. The domain plugins — code, vault, services — each follow the same BRDSPI phase pattern adapted to their context. Supporting plugins handle git workflow, session continuity, web research, and tooling for authoring new skills.

## Architecture

For a visual guide to how plugins, skills, agents, and hooks connect, see [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

## Plugins

| Plugin | Description | Skills | Agents | Hooks |
|--------|-------------|:------:|:------:|:-----:|
| [commandbase-core](plugins/commandbase-core/README.md) | Shared docs agents + utility skills. Install first. | 5 | 4 | 0 |
| [commandbase-code](plugins/commandbase-code/README.md) | Code BRDSPI workflow for software projects | 8 | 3 | 0 |
| [commandbase-vault](plugins/commandbase-vault/README.md) | Vault BRDSPI workflow for Obsidian vault management | 8 | 0 | 0 |
| [commandbase-services](plugins/commandbase-services/README.md) | Services BRDSPI workflow for homelab Docker infrastructure | 6 | 0 | 0 |
| [commandbase-research](plugins/commandbase-research/README.md) | Web and framework research with sourced output | 4 | 1 | 0 |
| [commandbase-git-workflow](plugins/commandbase-git-workflow/README.md) | Opinionated git commit workflow with security review | 5 | 0 | 1 |
| [commandbase-session](plugins/commandbase-session/README.md) | Session continuity with git branching + worktrees | 4 | 0 | 4 |
| [commandbase-meta](plugins/commandbase-meta/README.md) | Skill, agent, and hook authoring tools | 6 | 0 | 0 |

## Quick Start

You'll need [Claude Code](https://docs.anthropic.com/en/docs/claude-code) installed.

```bash
# Add commandbase as a marketplace source
/plugin marketplace add /path/to/commandbase

# Install core first (other plugins depend on its agents)
/plugin install commandbase-core

# Then install whichever domain plugins you want
/plugin install commandbase-code
/plugin install commandbase-vault
/plugin install commandbase-services
/plugin install commandbase-research
/plugin install commandbase-git-workflow
/plugin install commandbase-session
/plugin install commandbase-meta
```

Order matters for one thing: `commandbase-core` goes first. After that, install in any order you like.

## Windows Setup

### Required: Set Git Bash Path

Claude Code must use Git Bash (not WSL bash) for hook execution. Without this, `${CLAUDE_PLUGIN_ROOT}` paths get mangled and all plugin hooks fail.

```cmd
setx CLAUDE_CODE_GIT_BASH_PATH "C:\Program Files\Git\bin\bash.exe"
```

Restart Claude Code after setting this.

**Why this matters:** Windows has multiple `bash.exe` installs — `C:\Windows\System32\bash.exe` for WSL, `C:\Program Files\Git\usr\bin\bash.exe` for MINGW. Claude Code may pick the wrong one, which strips path separators from `${CLAUDE_PLUGIN_ROOT}`.

## Development

### Bare Repo Layout

This repo uses the bare repo + worktrees pattern. The container lives at `/c/code/commandbase/`, the main worktree at `/c/code/commandbase/main/`. Session worktrees are created as peers (e.g., `feature/auth-mvp/`). `session-map.json` tracks active sessions at the container level.

### Editing Skills

Skills live at `plugins/<plugin>/skills/<skill>/SKILL.md`. Edit them directly in the plugin directory — there's no separate build step.

### Commit Enforcement

Three layers prevent direct `git commit` / `git push` calls and route everything through `/committing-changes`:

1. **CLAUDE.md rule** — `~/.claude/CLAUDE.md` Git Workflow section tells Claude to always use the skill
2. **PostToolUse nudge hook** — bundled in `commandbase-git-workflow`, warns if a bare commit is attempted
3. **Deny rules** — manually configured in `~/.claude/settings.json` (see `plugins/commandbase-git-workflow/SETUP.md`)

## Contributing

Fork the repo, make your changes in a feature branch, test them locally, and open a PR. If you're adding a new skill, use `/creating-skills` to scaffold it.

## License

[MIT](LICENSE)
