---
date: 2026-02-09
status: complete
topic: "README.md best practices for Claude Code plugin marketplaces"
tags: [research, readme, marketplace, documentation, plugins]
git_commit: f30a465
references:
  - .claude-plugin/marketplace.json
  - CLAUDE.md
  - README.md
  - plugins/
---

# README.md Best Practices for Claude Code Plugin Marketplaces

## Research Question
What are the best practices for creating a README.md for an open-source Claude Code plugin marketplace repository?

## Summary
Cross-referencing general README best practices (GitHub docs, Make a README, Awesome README), plugin marketplace patterns (VS Code, npm, Homebrew, WordPress), and Claude Code-specific conventions (Anthropic official plugins, plugin documentation) reveals a clear structure for marketplace READMEs. The key insight: Claude Code plugin READMEs should combine the "what/why/how" universals with marketplace-specific installation flows and skill inventories that let users evaluate plugins before installing.

## Detailed Findings

### 1. Universal README Structure (Consensus Across All Sources)
**Sources:** GitHub Docs, Make a README, Best-README-Template, FreeCodeCamp

Every authoritative source agrees on these essential sections in order:
1. **Title + One-liner** - Project name and single-sentence description
2. **Badges** - 2-4 max (license, version, build status). Use shields.io for consistency
3. **Description/About** - What it does, who it's for, why it exists
4. **Table of Contents** - For documents longer than ~4 screens
5. **Installation** - Step-by-step with prerequisites
6. **Usage** - Examples with expected output. "Use examples liberally"
7. **Contributing** - How to contribute
8. **License** - Essential for open source

Key principle from Make a README: "Too long is better than too short."
Key principle from Awesome README: Position compelling information "above the fold."

### 2. Plugin Marketplace README Patterns
**Sources:** VS Code Extension API, npm Docs, WordPress Plugin Handbook, Homebrew Tap Docs

Plugin ecosystems add these sections beyond the universal structure:
- **Plugin/Extension Inventory** - What's included, with brief descriptions
- **Prerequisites/Compatibility** - Required versions, dependencies, platform support
- **Installation Flow** - Marketplace-specific commands (not just git clone)
- **Configuration** - Post-install setup steps
- **Troubleshooting** - Common installation/runtime issues
- **Screenshots/Demos** - Visual proof of functionality

VS Code pattern: README.md IS the marketplace page. It should sell the extension.
npm pattern: Focus on composability, quick-start code example in first 10 lines.
WordPress pattern: Strict metadata headers, version compatibility matrix, changelog.
Homebrew pattern: Repository naming conventions, formula listing, dependency docs.

### 3. Claude Code Plugin-Specific Conventions
**Sources:** Anthropic official plugins (claude-plugins-official), Claude Code plugin docs, community repos

From Anthropic's official plugins (code-review, plugin-dev, feature-dev):
- **Overview section** with key capabilities as bullet list
- **Commands/Skills section** with subsections per command showing:
  - What it does (numbered steps)
  - Usage (shell command)
  - Features (bullet list)
- **Installation** using `/plugin marketplace add` and `/plugin install` commands
- **Requirements** listing dependencies (e.g., `gh` CLI, specific APIs)
- **Best Practices** with "when to use" and "when not to use"
- **Troubleshooting** with Issue/Solution pairs

Plugin discovery via `/plugin > Discover` UI or marketplace commands.
Team distribution via `.claude/settings.json` with `extraKnownMarketplaces`.

### 4. Commandbase-Specific Context
The commandbase repo has unique characteristics that should shape its README:
- **8 plugins** in a single marketplace with dependency ordering (core first)
- **46 skills + 8 agents + 5 hooks** across all plugins
- **BRDSPI workflow** pattern shared across code/vault/services domains
- **Windows/MINGW requirement** for path handling (`CLAUDE_CODE_GIT_BASH_PATH`)
- **Bare repo + worktrees** development pattern
- **Session management** (v2) with git branching and error tracking
- **3-layer commit enforcement** (CLAUDE.md rule + hook + deny rules)
- **Existing README.md** is incomplete (only Windows setup, 18 lines)
- **No LICENSE file** exists yet

### 5. Badge Recommendations
**Sources:** Daily.dev badge best practices, shields.io

For a Claude Code marketplace repo:
- **License badge** (once added)
- **Plugin count badge** (custom: "8 plugins")
- **Skills count badge** (custom: "46 skills")
- **Platform badge** (Windows/MINGW)
Limit to 2-4 badges. Use shields.io for consistency.

## Recommended README Structure for commandbase

Based on cross-referencing all sources, the recommended structure:

```
1. Title + badges
2. One-liner description
3. Quick overview (what this is, who it's for)
4. Plugin inventory table (name, description, skills/agents/hooks counts)
5. Quick start (marketplace add + install core + install others)
6. Plugin details (expandable sections per plugin with skill listings)
7. Windows setup (CLAUDE_CODE_GIT_BASH_PATH requirement)
8. Development (bare repo layout, editing skills, commit enforcement)
9. Documentation (.docs/ structure, auditing, staleness tracking)
10. Contributing
11. License
```

## Source Conflicts
- **Section ordering**: Some sources put Installation before Description. Consensus favors Description first for marketplace repos since users browse before installing.
- **Badge count**: Ranges from "as many as relevant" to "2-4 max". Consensus: fewer is better for personal/niche projects.
- **Table of Contents**: Some say always include, others say GitHub auto-generates. For marketplace READMEs with inventory tables, explicit TOC helps navigation.

## Currency Assessment
- Most recent sources: 2025-2026 (Claude Code plugin docs, VS Code extension API)
- Topic velocity: Fast-moving (Claude Code plugin system is actively evolving)
- Confidence in currency: High for general practices, Medium for Claude Code-specific (ecosystem is new)

## Open Questions
1. Should each plugin have its own README.md in addition to the marketplace README?
2. What license should commandbase use? (MIT is most common for Claude Code plugins)
3. Should the README include animated GIFs demonstrating skill invocation?
4. How to handle the BRDSPI workflow explanation without overwhelming new users?
