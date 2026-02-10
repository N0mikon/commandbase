---
date: 2026-02-08
status: complete
topic: "Plugin Conversion Analysis - Skills, Agents, and Hooks to Marketplace Plugins"
tags: [research, plugin-marketplace, skills, agents, hooks, packaging, dependencies]
git_commit: 8e92bba
last_updated: 2026-02-09
last_updated_by: docs-updater
last_updated_note: "Updated after 10 commits - conversion complete, refreshed plugin structures to match actual implementation, resolved open questions, updated session plugin for v2 rearchitecture"
references:
  - plugins/commandbase-core/
  - plugins/commandbase-code/
  - plugins/commandbase-vault/
  - plugins/commandbase-services/
  - plugins/commandbase-research/
  - plugins/commandbase-git-workflow/
  - plugins/commandbase-session/
  - plugins/commandbase-meta/
  - .claude-plugin/marketplace.json
  - .docs/research/02-08-2026-plugin-marketplace-repo-best-practices-for-claude.md
---

# Plugin Conversion Analysis — Skills, Agents, and Hooks to Marketplace Plugins

## Research Question
How should the 47 skills, 8 agents, and 4 hooks in commandbase be organized into marketplace plugins, considering their dependency graph, domain boundaries, and the official plugin structure?

## Summary
The commandbase repo contains 47 skills across 3 domain-specific BRDSPI chains (Code, Vault, Services), plus general workflow tools, research skills, meta/audit skills, session management, and 4 enforcement hooks. The architecture follows a **core + domain plugins** model: a core plugin holds shared agents and standalone utility skills, while each workflow domain (code, vault, services, research, git, session, meta) ships as its own self-contained plugin.

## Detailed Findings

### 1. Complete Component Inventory

**47 Skills** organized by domain:
- **Code BRDSPI** (7): brainstorming-code, researching-code, designing-code, structuring-code, planning-code, implementing-plans, starting-refactors
- **Vault BRDSPI** (8): brainstorming-vault, starting-vault, researching-vault, designing-vault, structuring-vault, planning-vault, implementing-vault, importing-vault
- **Services BRDSPI** (6): brainstorming-services, researching-services, designing-services, structuring-services, planning-services, implementing-services
- **Research** (5): researching-code, researching-web, researching-frameworks, researching-repo, researching-vault (some shared with BRDSPI chains)
- **Git Workflow** (3): committing-changes, reviewing-changes, reviewing-security
- **Session Management** (4): starting-session, resuming-session, ending-session, learning-from-sessions (v2: git branching + worktrees)
- **Meta/Audit** (5): creating-skills, creating-agents, auditing-skills, auditing-agents, auditing-docs
- **Debugging/Security** (3): debugging-code, reviewing-security, creating-hooks
- **Utility** (6): bookmarking-code, creating-posts, creating-prs, debating-options, validating-code, starting-projects, learning-from-sessions, updating-claude-md

**8 Agents** in 4 layers:
- **Location**: code-locator, docs-locator
- **Analysis**: code-analyzer, code-librarian, docs-analyzer
- **Write**: docs-updater, docs-writer
- **External**: web-researcher

**5 Hooks** (all personal workflow):
- nudge-commit-skill (PostToolUse — enforces /committing-changes)
- detect-session (SessionStart — auto-detects session context from worktree)
- track-errors (PostToolUseFailure — real-time error logging)
- harvest-errors (Stop — backfills error log from transcript)
- trigger-learning (PreCompact — nudges /learning-from-sessions)

### 2. Dependency Graph — Critical Clusters

#### Foundation Layer (Required by Everything)
Every BRDSPI skill spawns `docs-writer` to create `.docs/` artifacts. Four skills auto-refresh stale docs via `docs-updater`. This makes the docs agent set a **hard dependency for all plugins**.

**Foundation agents**: docs-writer, docs-updater, docs-locator, docs-analyzer

#### Code Research Cluster
`/researching-code` spawns code-locator, code-analyzer, and code-librarian. These three agents are only used by code-focused skills.

**Code agents**: code-locator, code-analyzer, code-librarian

#### Web Research Cluster
`/researching-web` and `/researching-frameworks` spawn web-researcher agents. This is independent of codebase research.

**Web agent**: web-researcher

#### Artifact Chain Pattern
Each BRDSPI domain follows: Brainstorm → Research → Design → Structure → Plan → Implement, where each step reads upstream `.docs/` artifacts and writes downstream ones. This creates a tight coupling within each domain but loose coupling between domains.

#### Commit Enforcement Chain
`/committing-changes` depends on `/reviewing-security` and `/auditing-docs`. The `nudge-commit-skill` hook enforces this skill. These must travel together.

### 3. Plugin Architecture: Core + Domain Plugins

Each domain is its own self-contained plugin. A core plugin holds shared agents and standalone utility skills.

---

**Plugin 1: `commandbase-core`** (Shared Agents + Standalone Utilities)
```
commandbase-core/
├── .claude-plugin/plugin.json
├── skills/
│   ├── bookmarking-code/
│   ├── updating-claude-md/
│   ├── debating-options/
│   ├── validating-code/
│   └── starting-projects/
└── agents/
    ├── docs-writer.md
    ├── docs-updater.md
    ├── docs-locator.md
    └── docs-analyzer.md
```
**9 components**: 5 skills + 4 agents
**Audience**: Anyone using Claude Code — shared infrastructure for all other plugins

---

**Plugin 2: `commandbase-code`** (Code BRDSPI Workflow)
```
commandbase-code/
├── .claude-plugin/plugin.json
├── skills/
│   ├── brainstorming-code/
│   ├── researching-code/
│   ├── designing-code/
│   ├── structuring-code/
│   ├── planning-code/
│   ├── implementing-plans/
│   ├── starting-refactors/
│   └── debugging-code/
└── agents/
    ├── code-locator.md
    ├── code-analyzer.md
    └── code-librarian.md
```
**11 components**: 8 skills + 3 agents
**Audience**: Developers who want the full Brainstorm→Research→Design→Structure→Plan→Implement chain for code

---

**Plugin 3: `commandbase-vault`** (Vault BRDSPI Workflow)
```
commandbase-vault/
├── .claude-plugin/plugin.json
├── skills/
│   ├── brainstorming-vault/
│   ├── starting-vault/
│   ├── researching-vault/
│   ├── designing-vault/
│   ├── structuring-vault/
│   ├── planning-vault/
│   ├── implementing-vault/
│   └── importing-vault/
└── .mcp.json            (Obsidian MCP configuration)
```
**8 skills**
**Audience**: Obsidian users managing vaults with Claude Code

---

**Plugin 4: `commandbase-services`** (Services BRDSPI Workflow)
```
commandbase-services/
├── .claude-plugin/plugin.json
└── skills/
    ├── brainstorming-services/
    ├── researching-services/
    ├── designing-services/
    ├── structuring-services/
    ├── planning-services/
    └── implementing-services/
```
**6 skills**
**Audience**: Homelab enthusiasts managing Docker infrastructure

---

**Plugin 5: `commandbase-research`** (Web & Framework Research)
```
commandbase-research/
├── .claude-plugin/plugin.json
├── skills/
│   ├── analyzing-research/
│   ├── researching-web/
│   ├── researching-frameworks/
│   └── researching-repo/
└── agents/
    └── web-researcher.md
```
**5 components**: 4 skills + 1 agent
**Audience**: Anyone who wants structured, sourced web research with documentation output and cross-document analysis

---

**Plugin 6: `commandbase-git-workflow`** (Commit & PR Workflow)
```
commandbase-git-workflow/
├── .claude-plugin/plugin.json
├── SETUP.md
├── skills/
│   ├── committing-changes/
│   ├── reviewing-changes/
│   ├── reviewing-security/
│   ├── creating-prs/
│   └── auditing-docs/
├── hooks/
│   └── hooks.json
└── scripts/
    └── nudge-commit-skill.py
```
**6 components**: 5 skills + 1 hook (PostToolUse on Bash)
**Audience**: Anyone who wants opinionated git commit workflow enforcement
**Note**: Hooks are bundled via `hooks.json` with scripts in `scripts/`. SETUP.md documents manual deny-rule configuration for settings.json.

---

**Plugin 7: `commandbase-session`** (Session Management — v2: Git Branching + Worktrees)
```
commandbase-session/
├── .claude-plugin/plugin.json
├── skills/
│   ├── starting-session/
│   ├── resuming-session/
│   ├── ending-session/
│   └── learning-from-sessions/
├── hooks/
│   └── hooks.json
└── scripts/
    ├── detect-session.py
    ├── session_utils.py
    ├── track-errors.py
    ├── harvest-errors.py
    └── trigger-learning.py
```
**8 components**: 4 skills + 4 hooks (SessionStart, PostToolUseFailure, Stop, PreCompact)
**Audience**: Users who want session continuity with git worktree isolation and error-driven learning
**Note**: v2 rearchitected sessions around git branching/worktrees. Skills renamed from naming-session/handing-over/taking-over/resuming-sessions to starting-session/resuming-session/ending-session. detect-session hook added for SessionStart auto-detection.

---

**Plugin 8: `commandbase-meta`** (Skill/Agent Authoring)
```
commandbase-meta/
├── .claude-plugin/plugin.json
└── skills/
    ├── creating-skills/
    ├── creating-agents/
    ├── creating-hooks/
    ├── auditing-skills/
    ├── auditing-agents/
    └── creating-posts/
```
**6 skills**
**Audience**: Skill/agent developers building their own Claude Code extensions

### 4. Plugin Packaging Considerations

#### What the Official Plugin Structure Supports
Based on the marketplace research, plugins contain:
- `.claude-plugin/plugin.json` — Manifest with name, description, version
- `skills/` — Skill .md files (this maps directly to our SKILL.md files)
- `commands/` — Slash command .md files
- `.mcp.json` — MCP server connections

#### Resolved Questions from Plugin Conversion
1. **Can plugins bundle agents?** YES -- agents are placed in `agents/` directories within plugins. commandbase-core ships 4 agents, commandbase-code ships 3, commandbase-research ships 1.
2. **Can plugins bundle hooks?** YES -- hooks are defined in `hooks/hooks.json` with Python scripts in `scripts/`. Both commandbase-git-workflow and commandbase-session use this pattern.
3. **Plugin dependencies**: Not formally declared in plugin.json, but documented in marketplace.json descriptions (e.g., "Requires commandbase-core") and in CLAUDE.md install instructions.
4. **Reference files**: YES -- `reference/` and `templates/` subdirectories deploy correctly within plugin skill directories. All BRDSPI skills use them.
5. **Settings injection**: NO -- plugins cannot modify settings.json. The git-workflow plugin includes a SETUP.md with manual deny-rule instructions instead.

### 5. Personal vs General Purpose Classification

**General purpose** (publishable to marketplace):
- All BRDSPI skills (Code, Vault, Services)
- All research skills
- All code/docs agents
- Meta/audit skills
- bookmarking-code, validating-code, creating-prs, debating-options, starting-projects

**Personal workflow** (need generalization for marketplace):
- committing-changes -- opinionated commit workflow, but broadly useful with minor tweaks
- starting-session -- creates git branch/worktree for session isolation (v2)
- resuming-session -- resumes session from worktree context (v2)
- ending-session -- merges session branch and cleans up worktree (v2)
- learning-from-sessions -- depends on session error tracking hooks
- All 5 hooks -- tied to personal enforcement patterns

**Archived** (skip):
- discussing-features -- absorbed by brainstorming-code + designing-code (moved to `.docs/archive/`)

### 6. Conversion Status (Completed)

All 8 plugins were converted in commit `87a19a3`, with the session plugin further rearchitected in v2 (commits `92113aa`-`aefcf6f`).

| Plugin | Skills | Agents | Hooks | Status | Notes |
|--------|--------|--------|-------|--------|-------|
| commandbase-core | 5 | 4 | 0 | Done | Agent bundling works as designed |
| commandbase-code | 8 | 3 | 0 | Done | All reference files deployed correctly |
| commandbase-vault | 8 | 0 | 0 | Done | Clean conversion |
| commandbase-services | 6 | 0 | 0 | Done | Clean conversion |
| commandbase-research | 4 | 1 | 0 | Done | Added analyzing-research post-conversion |
| commandbase-git-workflow | 5 | 0 | 1 | Done | hooks.json pattern, SETUP.md for deny rules |
| commandbase-session | 4 | 0 | 4 | Done (v2) | Rearchitected: git branching + worktrees, new skill names, detect-session hook added |
| commandbase-meta | 6 | 0 | 0 | Done | Clean conversion |

## Architecture Notes

### Iron Law + Gate Function Pattern
Every skill follows the same enforcement structure: Iron Law (NO X WITHOUT Y), Gate Function (step-by-step checklist), Red Flags (STOP conditions), Rationalization Prevention (excuse→reality table). This is a unique architectural pattern that could be documented as a "skill authoring convention" in the marketplace README.

### BRDSPI Workflow
The Brainstorm→Research→Design→Structure→Plan→Implement chain is the core innovation. Each step reads upstream `.docs/` artifacts and writes downstream ones. This artifact-chaining pattern is what makes the domain-based plugin split natural — each domain has its own artifact chain but shares the docs infrastructure.

### Staleness Auto-Update
4 upstream-reading skills (resuming-session, planning-code, designing-code, and auditing-docs) check `git_commit` frontmatter and spawn `docs-updater` if documents are >3 commits behind HEAD. This is a cross-cutting concern that lives in commandbase-core via the docs-updater agent.

## Code References
- Plugins: `plugins/commandbase-*/` (8 plugin directories)
- Marketplace manifest: `.claude-plugin/marketplace.json`
- Prior research: `.docs/research/02-08-2026-plugin-marketplace-repo-best-practices-for-claude.md`

**Note**: The legacy `newskills/`, `newagents/`, and `newhooks/` directories were the source of truth at research time. These were restructured into the `plugins/` directory in commit `87a19a3`. The legacy session skills (`newskills/handing-over/`, etc.) were further modified during v2 but are superseded by the plugin versions.

## Remaining Open Questions
1. ~~**Agent bundling**~~: RESOLVED -- yes, plugins support `agents/` directories.
2. ~~**Hook bundling**~~: RESOLVED -- yes, via `hooks/hooks.json` + `scripts/`.
3. ~~**Plugin dependencies**~~: PARTIALLY RESOLVED -- not formally declared, documented in descriptions instead.
4. ~~**Reference file deployment**~~: RESOLVED -- yes, deploys correctly.
5. ~~**Marketplace scope**~~: RESOLVED -- single marketplace repo with 8 plugins.
6. **Cross-platform portability**: Still open. Agent Skills open standard (agentskills.io) compatibility not yet explored.
7. **Personal vs public**: Still open. Session and git-workflow plugins remain personal but functional for others.
