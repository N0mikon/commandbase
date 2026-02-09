---
date: 2026-02-08
status: complete
topic: "Plugin Conversion Analysis - Skills, Agents, and Hooks to Marketplace Plugins"
tags: [research, plugin-marketplace, skills, agents, hooks, packaging, dependencies]
git_commit: e4648b4
references:
  - newskills/*/SKILL.md
  - newagents/*.md
  - newhooks/*/
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
- **Session Management** (4): naming-session, handing-over, taking-over, resuming-sessions
- **Meta/Audit** (5): creating-skills, creating-agents, auditing-skills, auditing-agents, auditing-docs
- **Debugging/Security** (3): debugging-code, reviewing-security, creating-hooks
- **Utility** (6): bookmarking-code, creating-posts, creating-prs, debating-options, validating-code, starting-projects, learning-from-sessions, updating-claude-md

**8 Agents** in 4 layers:
- **Location**: code-locator, docs-locator
- **Analysis**: code-analyzer, code-librarian, docs-analyzer
- **Write**: docs-updater, docs-writer
- **External**: web-researcher

**4 Hooks** (all personal workflow):
- nudge-commit-skill (PostToolUse — enforces /committing-changes)
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
└── agents/              (if plugins can bundle agents)
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
│   ├── researching-web/
│   ├── researching-frameworks/
│   └── researching-repo/
└── agents/
    └── web-researcher.md
```
**4 components**: 3 skills + 1 agent
**Audience**: Anyone who wants structured, sourced web research with documentation output

---

**Plugin 6: `commandbase-git-workflow`** (Commit & PR Workflow)
```
commandbase-git-workflow/
├── .claude-plugin/plugin.json
├── skills/
│   ├── committing-changes/
│   ├── reviewing-changes/
│   ├── reviewing-security/
│   ├── creating-prs/
│   └── auditing-docs/
└── hooks/               (if plugins can bundle hooks)
    └── nudge-commit-skill.py
```
**6 components**: 5 skills + 1 hook
**Audience**: Anyone who wants opinionated git commit workflow enforcement

---

**Plugin 7: `commandbase-session`** (Session Management)
```
commandbase-session/
├── .claude-plugin/plugin.json
├── skills/
│   ├── naming-session/
│   ├── handing-over/
│   ├── taking-over/
│   ├── resuming-sessions/
│   └── learning-from-sessions/
└── hooks/
    ├── track-errors.py
    ├── harvest-errors.py
    └── trigger-learning.py
```
**8 components**: 5 skills + 3 hooks
**Audience**: Users who want session continuity and error-driven learning

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

#### Open Questions for Plugin Conversion
1. **Can plugins bundle agents?** The official structure shows `skills/` and `commands/` but not `agents/`. If agents can't be bundled, the foundation layer needs an alternative distribution method.
2. **Can plugins bundle hooks?** Same question — hooks are Python scripts with settings.json configuration. No evidence of hook bundling in plugin structure.
3. **Plugin dependencies**: Can one plugin declare a dependency on another? The marketplace system supports version tracking but dependency chains aren't documented.
4. **Reference files**: Skills have `reference/` and `templates/` subdirectories. Do these deploy correctly within the plugin skill directory?
5. **Settings injection**: The commit enforcement hook requires deny rules in `settings.json`. Can plugins modify settings?

### 5. Personal vs General Purpose Classification

**General purpose** (publishable to marketplace):
- All BRDSPI skills (Code, Vault, Services)
- All research skills
- All code/docs agents
- Meta/audit skills
- bookmarking-code, validating-code, creating-prs, debating-options, starting-projects

**Personal workflow** (need generalization for marketplace):
- committing-changes — opinionated commit workflow, but broadly useful with minor tweaks
- naming-session — tied to `.claude/sessions/` structure
- resuming-sessions — tied to `.claude/sessions/` structure
- handing-over — useful generally, slightly personalized
- learning-from-sessions — depends on session error tracking hooks
- All 4 hooks — tied to personal enforcement patterns

**Archived** (skip):
- discussing-features — absorbed by brainstorming-code + designing-code

### 6. Conversion Effort Estimate per Plugin

| Plugin | Skills | Agents | Hooks | Effort | Notes |
|--------|--------|--------|-------|--------|-------|
| commandbase-core | 5 | 4 | 0 | Medium | Agent bundling question must be answered first |
| commandbase-code | 8 | 3 | 0 | Medium | Largest skill count, many reference files |
| commandbase-vault | 8 | 0 | 0 | Low | All skills, no unique agents |
| commandbase-services | 6 | 0 | 0 | Low | All skills, no unique agents |
| commandbase-research | 3 | 1 | 0 | Low | Clean separation, few dependencies |
| commandbase-git-workflow | 5 | 0 | 1 | Medium | Hook bundling question, settings injection |
| commandbase-session | 5 | 0 | 3 | High | Most personal, hook bundling, session structure |
| commandbase-meta | 6 | 0 | 0 | Low | Standalone, no dependencies |

## Architecture Notes

### Iron Law + Gate Function Pattern
Every skill follows the same enforcement structure: Iron Law (NO X WITHOUT Y), Gate Function (step-by-step checklist), Red Flags (STOP conditions), Rationalization Prevention (excuse→reality table). This is a unique architectural pattern that could be documented as a "skill authoring convention" in the marketplace README.

### BRDSPI Workflow
The Brainstorm→Research→Design→Structure→Plan→Implement chain is the core innovation. Each step reads upstream `.docs/` artifacts and writes downstream ones. This artifact-chaining pattern is what makes the domain-based plugin split natural — each domain has its own artifact chain but shares the docs infrastructure.

### Staleness Auto-Update
4 skills (taking-over, planning-code, designing-code, resuming-sessions) check `git_commit` frontmatter and spawn `docs-updater` if documents are >3 commits behind HEAD. This is a cross-cutting concern that lives in commandbase-core via the docs-updater agent.

## Code References
- Skills: `C:/code/commandbase/newskills/*/SKILL.md` (47 files)
- Agents: `C:/code/commandbase/newagents/*.md` (8 files)
- Hooks: `C:/code/commandbase/newhooks/*/` (4 directories)
- Deployed skills: `C:/Users/Jason/.claude/skills/` (mirrors newskills/)
- Deployed agents: `C:/Users/Jason/.claude/agents/` (mirrors newagents/)
- Deployed hooks: `C:/Users/Jason/.claude/hooks/` (mirrors newhooks/)
- Prior research: `.docs/research/02-08-2026-plugin-marketplace-repo-best-practices-for-claude.md`

## Open Questions
1. **Agent bundling**: Can plugins include agent .md files? This is the #1 blocker — if not, commandbase-core and commandbase-code need restructuring.
2. **Hook bundling**: Can plugins include hook scripts and settings.json modifications? Affects commandbase-git-workflow and commandbase-session.
3. **Plugin dependencies**: Can `commandbase-code` declare a dependency on `commandbase-core`? If not, shared agents may need to be duplicated across plugins.
4. **Reference file deployment**: Do `reference/` and `templates/` subdirectories within skills deploy correctly in plugins?
5. **Marketplace scope**: Single marketplace repo containing all 8 plugins, or separate repos per plugin?
6. **Cross-platform portability**: Should skills be adapted for the Agent Skills open standard (agentskills.io) to target OpenAI Codex too?
7. **Personal vs public**: Should personal workflow plugins (session, git-workflow) be published as-is, generalized, or kept private?
