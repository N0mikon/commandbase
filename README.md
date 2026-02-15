# commandbase

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Plugins](https://img.shields.io/badge/plugins-8-green.svg)](#plugins)
[![Skills](https://img.shields.io/badge/skills-46-purple.svg)](#plugins)

Skills, agents, and hooks that give Claude Code a repeatable workflow: brainstorm, research, design, structure, plan, implement.

## Table of Contents

- [Why commandbase](#why-commandbase)
- [Overview](#overview)
- [Architecture](#architecture)
- [Plugins](#plugins)
- [Windows Setup](#windows-setup)
- [Development](#development)
- [Acknowledgments](#acknowledgments)
- [Contributing](#contributing)
- [License](#license)

## Why commandbase

I'm not a professional developer. I use Claude Code to build things I can't build alone, and I got tired of every session being a blank slate where Claude forgets everything and I re-explain the same stuff.

[HumanLayer](https://github.com/humanlayer/humanlayer) and [Superpowers](https://github.com/obra/superpowers) both solved parts of this. HumanLayer's `thoughts/` system handles context management: `file:line` references instead of pasting code, handoffs instead of compacting, and a research-plan-implement workflow. Superpowers has iron law gates that force Claude to follow steps instead of skipping them, with tables that preempt every rationalization Claude tries. I borrowed from both and built my own version because I wanted to understand how they work, not just use them.

The `.docs/` system is based on HumanLayer's `thoughts/`. The gate logic comes from Superpowers. The BRDSPI workflow (brainstorm, research, design, structure, plan, implement) started as HumanLayer's RPI and I guessed at what the B, D, and S might be in their upcoming release.

This is a work in progress and probably has some bad ideas in it. If you spot something, open an issue.

## Overview

Eight plugins, split by domain. Install `commandbase-core` first since it has the shared docs agents everything else depends on. Then pick the domains you care about:

- **Code, Vault, Services** each walk through the same phases (brainstorm → research → design → structure → plan → implement), just tuned for their context. Software projects, Obsidian vaults, or homelab Docker stacks.
- **Git workflow** keeps Claude from running raw `git commit` and routes everything through a review skill.
- **Session** tracks what you're working on across conversations so you don't start from scratch every time.
- **Research** fetches live docs and web sources so Claude isn't guessing from stale training data.
- **Meta** helps you build new skills, agents, and hooks without starting from a blank file.

## Architecture

For a visual guide to how plugins, skills, agents, and hooks connect, see [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

## Plugins

| Plugin | Description | Skills | Agents | Hooks |
|--------|-------------|:------:|:------:|:-----:|
| [commandbase-core](plugins/commandbase-core/README.md) | Shared docs agents + utility skills. Install first. | 5 | 4 | 0 |
| [commandbase-code](plugins/commandbase-code/README.md) | BRDSPI phases for software projects | 8 | 3 | 0 |
| [commandbase-vault](plugins/commandbase-vault/README.md) | Obsidian vault management: notes, links, templates | 8 | 0 | 0 |
| [commandbase-services](plugins/commandbase-services/README.md) | Homelab Docker infrastructure: compose, proxy, config | 6 | 0 | 0 |
| [commandbase-research](plugins/commandbase-research/README.md) | Web + framework docs with sourced output | 4 | 1 | 0 |
| [commandbase-git-workflow](plugins/commandbase-git-workflow/README.md) | Git commits routed through review + security checks | 5 | 0 | 1 |
| [commandbase-session](plugins/commandbase-session/README.md) | Cross-session context with branching + worktrees | 4 | 0 | 4 |
| [commandbase-meta](plugins/commandbase-meta/README.md) | Tools for authoring new skills, agents, and hooks | 6 | 0 | 0 |

## Quick Start

Install `commandbase-core` first. Other plugins depend on its agents. After that, install whichever ones you want in any order.

## Windows Setup

### Required: Set Git Bash Path

Claude Code must use Git Bash (not WSL bash) for hook execution. Without this, `${CLAUDE_PLUGIN_ROOT}` paths get mangled and all plugin hooks fail.

```cmd
setx CLAUDE_CODE_GIT_BASH_PATH "C:\Program Files\Git\bin\bash.exe"
```

Restart Claude Code after setting this.

**Why this matters:** Windows has multiple `bash.exe` installs. `C:\Windows\System32\bash.exe` is WSL, `C:\Program Files\Git\usr\bin\bash.exe` is MINGW. Claude Code may pick the wrong one, which strips path separators from `${CLAUDE_PLUGIN_ROOT}`.

## Development

### Editing Skills

Skills live at `plugins/<plugin>/skills/<skill>/SKILL.md`. Edit them directly in the plugin directory. No build step.

### Commit Enforcement

Three layers prevent direct `git commit` / `git push` calls and route everything through `/committing-changes`:

1. **CLAUDE.md rule** - your global `CLAUDE.md` Git Workflow section tells Claude to always use the skill
2. **PostToolUse nudge hook** - bundled in `commandbase-git-workflow`, warns if a bare commit is attempted
3. **Deny rules** - manually configured in `~/.claude/settings.json` (see `plugins/commandbase-git-workflow/SETUP.md`)

## Acknowledgments

commandbase builds on ideas from two projects:

- **[HumanLayer](https://github.com/humanlayer/humanlayer)** - the `thoughts/` directory for context management, `file:line` references as documentation, handoffs instead of compacting, and the research-plan-implement workflow. My `.docs/` system is a reworked version of their `thoughts/` pattern, and BRDSPI grew out of their RPI phases.
- **[Superpowers](https://github.com/obra/superpowers)** - the iron law gate logic, rationalization prevention tables, and the idea that skills need to actually stop Claude from skipping steps instead of politely suggesting it follow them.

## Contributing

Fork the repo, make your changes in a feature branch, test them locally, and open a PR. If you're adding a new skill, use `/creating-skills` to scaffold it.

## License

[MIT](LICENSE)
