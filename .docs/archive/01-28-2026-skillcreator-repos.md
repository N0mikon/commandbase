---
git_commit: 8e92bba
last_updated: 2026-02-09
last_updated_by: docs-updater
last_updated_note: "Archived - master index of external skill creator repos/tools. All actionable research from listed repos has been consumed and implemented in commandbase plugin architecture. Individual deep-dive research docs already archived."
topic: "Skill Creator Tools & Repos for Claude Code - Master Index"
tags: [research, skill-creator, skill-factory, external-repos, marketplaces, awesome-lists, reference-index]
status: archived
archived: 2026-02-09
archive_reason: "Completed external research index. All referenced repos were surveyed and findings consumed during commandbase skill/plugin development (creating-skills at plugins/commandbase-meta/skills/creating-skills/, learning-from-sessions at plugins/commandbase-session/skills/learning-from-sessions/). No local code references. Individual repo deep-dives already archived. Document serves only as historical record of what was surveyed."
references:
  - https://github.com/anthropics/skills
  - https://github.com/alirezarezvani/claude-code-skill-factory
  - https://github.com/FrancyJGLisboa/agent-skill-creator
  - https://github.com/metaskills/skill-builder
  - https://github.com/YYH211/Claude-meta-skill
  - https://github.com/blader/Claudeception
  - https://github.com/BayramAnnakov/claude-reflect
---

# Skill Creator Tools & Repos for Claude Code

**Date:** 2026-01-28
**Purpose:** Comprehensive list of skill/agent/command creator tools for Claude Code

---

## Official Tools

### Anthropic Skills Repository
- **URL:** https://github.com/anthropics/skills
- **Key Files:** `scripts/init_skill.py`, `scripts/package_skill.py`
- **Purpose:** Official template generator and packaging utility
- **Notable:** Reference implementation from Anthropic

---

## Skill Factory / Generator Tools

### Claude Code Skill Factory
- **URL:** https://github.com/alirezarezvani/claude-code-skill-factory
- **Author:** alirezarezvani
- **Features:** 10 slash commands, 5 guide agents, 6 core factories
- **Commands:** `/build`, `/validate-output`, `/install-skill`, `/test-factory`
- **Notable:** Most comprehensive production toolkit (v1.4.0)

### Agent Skill Creator
- **URL:** https://github.com/FrancyJGLisboa/agent-skill-creator
- **Author:** FrancyJGLisboa
- **Features:** 6-phase autonomous agent creation methodology
- **Phases:** Discovery → Design → Architecture → Detection → Implementation → Testing
- **Notable:** Uses `-cskill` naming suffix for generated skills

### Skill Builder
- **URL:** https://github.com/metaskills/skill-builder
- **Author:** metaskills
- **Stars:** 70+
- **Features:** Templates, references, migration guides
- **Notable:** `converting-sub-agents-to-skills.md` guide

### Claude Meta-Skill
- **URL:** https://github.com/YYH211/Claude-meta-skill
- **Author:** YYH211
- **Features:** Meta-skill teaching skill creation
- **Triggers:** "create skill", "write skill", "SKILL.md", "skill guidelines"
- **Notable:** Templates (Basic & Workflow patterns), quality checklists

---

## Learning & Pattern Extraction

### Claudeception
- **URL:** https://github.com/blader/Claudeception
- **Author:** blader
- **Features:** Autonomous skill extraction from sessions
- **Activation:** Automatic detection or `/claudeception` command
- **Notable:** Strict quality filters, research-backed approach

### Claude-Reflect
- **URL:** https://github.com/BayramAnnakov/claude-reflect
- **Author:** BayramAnnakov
- **Features:** Two-stage self-learning system
- **Commands:** `/reflect`, `/reflect-skills`, `/reflect --dedupe`
- **Notable:** Hooks detect corrections, syncs to CLAUDE.md and skill files

### Claude Code Continuous Learning Skill
- **URL:** https://github.com/blader/claude-code-continuous-learning-skill
- **Author:** blader
- **Features:** Persistent learning across sessions

---

## Example Projects & Showcases

### Claude Code Showcase
- **URL:** https://github.com/ChrisWiles/claude-code-showcase
- **Author:** ChrisWiles
- **Features:** Complete example with hooks, skills, agents, commands, GitHub Actions
- **Notable:** Production-ready patterns, code review agent

### Claude Code Best Practices
- **URL:** https://github.com/awattar/claude-code-best-practices
- **Author:** awattar
- **Features:** Prompt design, safe automation examples

### Claude Code Workflows
- **URL:** https://github.com/shinpr/claude-code-workflows
- **Author:** shinpr
- **Features:** Production-ready development workflows

### Claude Code Workflow Framework
- **URL:** https://github.com/catlog22/Claude-Code-Workflow
- **Author:** catlog22
- **Features:** JSON-driven multi-agent framework

---

## Curated Collections (Awesome Lists)

### Awesome Claude Code
- **URL:** https://github.com/hesreallyhim/awesome-claude-code
- **Features:** Comprehensive resource collection

### Awesome Claude Skills (travisvn)
- **URL:** https://github.com/travisvn/awesome-claude-skills
- **Features:** Curated skills list

### Awesome Claude Skills (VoltAgent)
- **URL:** https://github.com/VoltAgent/awesome-claude-skills
- **Features:** Community skills collection

### Awesome Claude Skills (ComposioHQ)
- **URL:** https://github.com/ComposioHQ/awesome-claude-skills
- **Features:** SDLC coverage patterns

---

## Marketplaces & Distribution

### SkillsMP
- **URL:** https://skillsmp.com/
- **Type:** Skills marketplace aggregator

### Claude Plugins Community Registry
- **URL:** https://claude-plugins.dev/
- **Type:** Community registry with CLI

### Claude Code Plugin Directory
- **URL:** https://www.claudecodeplugin.com/
- **Type:** Plugin directory

### Local Claude Marketplace
- **URL:** https://github.com/dashed/claude-marketplace
- **Author:** dashed
- **Type:** Local marketplace setup

### Claudebase Marketplace
- **URL:** https://github.com/claudebase/marketplace
- **Features:** Developer Kit (24 skills + 14 agents + 21 commands)

---

## Professional Skills Collections

### Claude Code Skills (daymade)
- **URL:** https://github.com/daymade/claude-code-skills
- **Features:** Production-ready professional skills

### Claude Skills (alirezarezvani)
- **URL:** https://github.com/alirezarezvani/claude-skills
- **Features:** Real-world usage, subagents, commands

### OpenSkills (Universal Loader)
- **URL:** https://github.com/numman-ali/openskills
- **Author:** NumMan-Ali
- **Features:** Universal skills loader

---

## Utilities & Helpers

### Claude Code Prompt Improver
- **URL:** https://github.com/severity1/claude-code-prompt-improver
- **Author:** severity1
- **Features:** Intelligent prompt improvement hook

---

## Key Articles & Tutorials

### Skill Activation Research
- **URL:** https://scottspence.com/posts/how-to-make-claude-code-skills-activate-reliably
- **Author:** Scott Spence
- **Finding:** Forced Eval Hook = 84% success rate (best pattern)

### Customization Guide
- **URL:** https://alexop.dev/posts/claude-code-customization-guide-claudemd-skills-subagents/
- **Coverage:** CLAUDE.md, slash commands, subagents, skills hierarchy

### Deep Dive Architecture
- **URL:** https://leehanchung.github.io/blogs/2025/10/26/claude-skills-deep-dive/
- **Author:** Lee Hanchung
- **Coverage:** Internal architecture, meta-programming insights

### Inside Claude Code Skills
- **URL:** https://mikhail.io/2025/10/claude-code-skills/
- **Author:** Mikhail Shilkov
- **Coverage:** Structure, prompts, invocation mechanism

### Enterprise Usage (Sionic AI)
- **URL:** https://huggingface.co/blog/sionic-ai/claude-code-skills-training
- **Coverage:** Running 1,000+ ML experiments/day with skills

---

## Official Documentation

- **Skills:** https://code.claude.com/docs/en/skills
- **Hooks:** https://code.claude.com/docs/en/hooks
- **Plugins:** https://code.claude.com/docs/en/plugins
- **Agent Skills API:** https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
- **Best Practices:** https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices

---

## Key Patterns Identified

1. **Progressive Disclosure:** Metadata → full instructions → bundled resources
2. **Forced Eval Hook:** Three-step commitment for 84% activation success
3. **Three-File Pattern:** `task_plan.md`, `notes.md`, `deliverable.md`
4. **Quality Gates:** "Would this help someone in 6 months?"
5. **Context Management:** Subagents isolate doc fetching to prevent bloat
