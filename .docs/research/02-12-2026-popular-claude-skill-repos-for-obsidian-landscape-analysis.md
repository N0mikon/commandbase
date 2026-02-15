---
date: 2026-02-12
status: complete
topic: "Popular Claude Skill Repos for Obsidian: Landscape Analysis"
tags: [research, obsidian, claude-skills, community-repos, ecosystem]
git_commit: 9c4c7f4
---

# Popular Claude Skill Repos for Obsidian: Landscape Analysis

**Date**: 2026-02-12
**Branch**: refactor/vault-skill-refinement

## Research Question
What are the most popular Claude skill repos for Obsidian, and what does the broader ecosystem look like?

## Summary

The Obsidian + Claude Code skills ecosystem has exploded since late 2025. **kepano/obsidian-skills** (9.7k stars) dominates as the official reference by Obsidian's CEO. Below it, a rich tier of community repos ranges from complete PKM starter kits (ballred: 938 stars) to visualization skills (axtonliu: 1.3k stars) to self-evolving second brains (huytieu/COG: 151 stars). The Agent Skills open standard (agentskills.io) has achieved industry adoption, and SkillsMP hosts 160,000+ skills. Distribution via plugin marketplace manifests is now formalized.

## Detailed Findings

### Tier 1: Official & High-Authority (1,000+ stars)

| Repo | Stars | Skills | Focus | Last Active |
|------|-------|--------|-------|-------------|
| [kepano/obsidian-skills](https://github.com/kepano/obsidian-skills) | 9,700 | 5 | Official Obsidian format skills (markdown, bases, canvas, CLI, defuddle) | Jan 2026 |
| [axtonliu/axton-obsidian-visual-skills](https://github.com/axtonliu/axton-obsidian-visual-skills) | 1,300 | 3 | Excalidraw, Mermaid, Canvas diagram generation | Feb 2026 |

**kepano/obsidian-skills** is the gold standard — created by Steph Ango (Obsidian CEO), provides authoritative format knowledge for wikilinks, callouts, properties, Bases files, and Canvas. These are *reference skills* (format knowledge), not *workflow skills* (automation). Installation: place in `/.claude` folder at vault root.

**axtonliu/axton-obsidian-visual-skills** fills the visualization gap with diagram generation from text. Marked "experimental" but actively maintained. Supports multilingual input.

### Tier 2: Complete PKM Systems (50-1,000 stars)

| Repo | Stars | Commands/Skills | Focus | Last Active |
|------|-------|-----------------|-------|-------------|
| [ballred/obsidian-claude-pkm](https://github.com/ballred/obsidian-claude-pkm) | 938 | 4 commands + 4 agents + 2 skills | Complete PKM starter kit with goal-aligned workflows | Jan 2026 |
| [huytieu/COG-second-brain](https://github.com/huytieu/COG-second-brain) | 151 | 7 skills | Self-evolving second brain (braindump, briefing, analysis, consolidation) | 2026 |
| [ArtemXTech/claude-code-obsidian-starter](https://github.com/ArtemXTech/claude-code-obsidian-starter) | 92 | 4 skills | Quick start for projects, tasks, clients, routines | 2026 |
| [gapmiss/obsidian-plugin-skill](https://github.com/gapmiss/obsidian-plugin-skill) | 75 | 1 comprehensive skill | Obsidian plugin development (27 ESLint rules) | Nov 2025 |
| [ksanderer/claude-vault](https://github.com/ksanderer/claude-vault) | 62 | CLI commands | Cross-device sync with GitHub backend, PARA structure | Jan 2026 |
| [googlicius/obsidian-steward](https://github.com/googlicius/obsidian-steward) | 49 | Built-in commands + skills | Autonomous agent with BM25 search, multi-model support | 2026 |

**ballred/obsidian-claude-pkm** is the closest competitor to commandbase-vault — it provides `/daily`, `/weekly`, `/push`, `/onboard` plus 4 agents. Key differentiators: goal-aligned cascading objectives, modular rules for path-specific conventions, hooks for auto-commits. 15-minute setup.

**huytieu/COG-second-brain** (Cognition + Obsidian + Git) is notable for its self-evolving design — daily braindumps, intelligence briefings, weekly pattern analysis, monthly knowledge consolidation. Multi-AI support (Claude, Kiro, Gemini CLI, Codex).

### Tier 3: Specialized & Template Repos (5-50 stars)

| Repo | Stars | Commands/Skills | Focus | Last Active |
|------|-------|-----------------|-------|-------------|
| [belumume/claude-skills](https://github.com/belumume/claude-skills) | 40 | 9 (1 Obsidian) | Study vault builder from course materials | 2026 |
| [ashish141199/obsidian-claude-code](https://github.com/ashish141199/obsidian-claude-code) | 26 | 9 commands | Template: daily, atomic notes, research, brainstorm, tasks | Nov 2025 |
| [jykim/claude-obsidian-skills](https://github.com/jykim/claude-obsidian-skills) | 25 | 17 skills | PKM automation: links, YAML, canvas, mermaid, video, image | 2026 |
| [ZanderRuss/obsidian-claude](https://github.com/ZanderRuss/obsidian-claude) | 5 | 31 commands + 27 agents + 19 skills | Comprehensive academic research workflow | Jan 2026 |

**ZanderRuss** is the most feature-rich repo by far (31 commands, 27 agents, 19 skills) but has only 5 stars — suggesting complexity may hurt adoption. Includes full academic research pipeline, PARA framework, and 3-layer quality control.

**jykim/claude-obsidian-skills** has the widest skill variety: PKM management, Obsidian-specific (canvas, links, YAML, mermaid, markdown structure), plus video/image processing and format conversion (DOCX, EPUB).

### Obsidian Plugins (Not Skills — Different Category)

These embed Claude inside the Obsidian UI rather than providing Claude Code skills:

| Plugin | Approach |
|--------|----------|
| [YishenTu/claudian](https://github.com/YishenTu/claudian) | Claude Agent SDK sidebar integration |
| [Roasbeef/obsidian-claude-code](https://github.com/Roasbeef/obsidian-claude-code) | Native plugin with full vault access |
| [derek-larson14/obsidian-claude-sidebar](https://forum.obsidian.md/t/claude-code-from-the-sidebar/109634) | Sidebar terminal for Claude Code |
| [RAIT-09/obsidian-agent-client](https://github.com/RAIT-09/obsidian-agent-client) | Multi-agent (Claude, Codex, Gemini) with @notename syntax |
| [googlicius/obsidian-steward](https://github.com/googlicius/obsidian-steward) | Autonomous agent with BM25 search |

These are relevant context but outside commandbase-vault's scope (we build Claude Code skills, not Obsidian plugins).

## Ecosystem Infrastructure

### Agent Skills Standard
- Published Dec 18, 2025 at [agentskills.io](https://agentskills.io)
- Adopted by Microsoft, OpenAI, Atlassian, Figma, Cursor, GitHub
- Progressive disclosure: metadata (~100 tokens) → instructions (<5000 tokens) → resources (on demand)
- Skills portable across Claude Code, Codex CLI, and other compatible agents

### Distribution Channels
- **Anthropic official**: [github.com/anthropics/skills](https://github.com/anthropics/skills) — document skills (DOCX, PDF, PPTX, XLSX)
- **Plugin marketplace**: Formal system via `marketplace.json` manifests, installable via `/plugin marketplace add`
- **SkillsMP**: Community registry with 160,000+ skills at [skillsmp.com](https://skillsmp.com/)
- **Awesome lists**: [travisvn/awesome-claude-skills](https://github.com/travisvn/awesome-claude-skills), [BehiSecc/awesome-claude-skills](https://github.com/BehiSecc/awesome-claude-skills), [jqueryscript/awesome-claude-code](https://github.com/jqueryscript/awesome-claude-code)

### Security Warning
Snyk researchers (Feb 2026) scanned 3,984 skills from public registries and found **13.4% had critical-level vulnerabilities**. Only install skills from trusted sources.

## Competitive Analysis: commandbase-vault vs Community

### What community repos do that we don't

| Capability | Who Has It | commandbase-vault |
|-----------|-----------|-------------------|
| Daily note creation/review | ballred, COG, ashish, ZanderRuss, ArtemXTech | Missing |
| Weekly/monthly synthesis | ballred, COG, ZanderRuss | Missing |
| Quick capture (web clips, voice, fleeting notes) | ZanderRuss, ashish | Missing |
| Smart linking / connection discovery | ZanderRuss, jykim | Missing |
| MOC auto-generation/maintenance | ZanderRuss (moc-agent) | Missing |
| Standalone vault linting | jykim (obsidian-links) | Embedded in implementing-vault only |
| Frontmatter validation | jykim (obsidian-yaml-frontmatter) | Embedded in implementing-vault only |
| Visualization (Excalidraw, Mermaid, Canvas) | axtonliu, jykim | Missing |
| Content transformation (flashcards, note-to-blog) | ZanderRuss | Missing |
| Academic research pipeline | ZanderRuss (13 commands) | Out of scope |
| Study vault generation | belumume | Out of scope |
| Plugin development | gapmiss | Out of scope |
| Self-evolving knowledge consolidation | COG | Missing |
| Inbox processing (PARA-based) | ZanderRuss, ballred | Missing |
| Git workflow integration | ballred, ksanderer | Exists via commandbase-git-workflow |
| Goal-aligned cascading objectives | ballred | Out of scope |
| Multi-model support | COG (Claude, Kiro, Gemini, Codex) | Claude-only (by design) |

### What we do that community repos don't

| Capability | commandbase-vault | Community |
|-----------|-------------------|-----------|
| Full BRDSPI workflow chain | 8 skills in sequence | No repo has this |
| Brainstorm → Research → Design → Structure → Plan → Implement | Complete pipeline | Fragmented across repos |
| .docs/ artifact system | Mandatory research/design/plan docs | No equivalent |
| Vault philosophy discovery (Zettelkasten vs PARA vs hybrid) | brainstorming-vault | Hardcoded to one methodology |
| Iron Law + Gate Function architecture | All skills | No equivalent rigor |
| Rationalization prevention | All skills | No equivalent |
| Integration with code workflow (session, git, research plugins) | Full commandbase ecosystem | Standalone repos |
| .docs/ → vault import pipeline | importing-vault | No equivalent |

### Key Insight
Community repos excel at **daily operations** (what you do WITH a vault). commandbase-vault excels at **vault architecture** (how you SET UP a vault). These are complementary, not competing. The gap analysis from our previous research (02-12-2026-vault-skills-gap-analysis) correctly identified daily operations as the #1 gap.

## Repos Worth Studying for New Skill Design

| Repo | Study For | Why |
|------|----------|-----|
| ballred/obsidian-claude-pkm | reviewing-vault, capturing-vault | Best daily/weekly workflow design, hooks pattern, 4 agents |
| huytieu/COG-second-brain | reviewing-vault | Self-evolving pattern: braindump → briefing → analysis → consolidation |
| ZanderRuss/obsidian-claude | connecting-vault, linting-vault | smart-link, graph-analysis, moc-agent, tag-agent patterns |
| jykim/claude-obsidian-skills | linting-vault | obsidian-links (link validation), obsidian-yaml-frontmatter (schema validation) |
| ashish141199/obsidian-claude-code | capturing-vault | Lightweight /day, /new, /log patterns |

## Source Conflicts

- **ZanderRuss star count vs feature richness**: Most comprehensive repo (31+27+19 = 77 components) but only 5 stars. Either complexity hurts adoption, or the repo is new and hasn't been discovered yet.
- **axtonliu star count**: awesome-claude-code lists 2.2k stars but GitHub shows 1.3k — may indicate rapid change or different counting.
- **COG multi-model claim**: Claims support for Claude, Kiro, Gemini CLI, Codex — unclear how well non-Claude agents work with the same skill files.

## Currency Assessment
- Most recent source: February 2026
- Topic velocity: Very fast-moving (new repos weekly, Agent Skills standard only 2 months old)
- Confidence: High for top repos (verified via GitHub), medium for star counts (fluctuating rapidly)

## Open Questions
- Should we reference or recommend kepano/obsidian-skills as a complementary install alongside commandbase-vault?
- Is there value in publishing commandbase-vault to SkillsMP for discoverability?
- Should new daily-operations skills follow ballred's agent-based pattern or COG's self-evolving pattern?
- How do we differentiate from ballred (closest competitor) while potentially learning from their design?
