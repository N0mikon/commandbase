---
git_commit: 8e92bba
last_updated: 2026-02-09
last_updated_by: docs-updater
last_updated_note: "Added missing frontmatter (was 61 commits behind with no git_commit). Content verified accurate against 8 live agent files in plugins/. No content changes needed."
type: research
category: web-research
references: []
---

# Agent Creation Skills for Claude & Best Practices

**Date**: 2026-02-05
**Type**: Web Research
**Topic**: Claude Code agent creation, design patterns, and best practices

---

## Executive Summary

Comprehensive research on creating agents for Claude Code and best practices for agent design. Covers the official specification, architectural patterns, community resources, and anti-patterns. Key takeaway: agents are Markdown files with YAML frontmatter that define specialized AI assistants with isolated context windows, specific tool access, and custom system prompts.

---

## 1. Claude Code Agent Specification

### File Format

Agents are **Markdown files with YAML frontmatter**. The body contains the system prompt.

```markdown
---
name: code-reviewer
description: Reviews code for quality and best practices
tools: Read, Glob, Grep
model: sonnet
---

You are a code reviewer. Analyze code and provide specific,
actionable feedback on quality, security, and best practices.
```

### Frontmatter Fields

| Field | Type | Required | Description |
|:------|:-----|:---------|:------------|
| `name` | string | Yes | Unique identifier, lowercase with hyphens |
| `description` | string | Yes | **When Claude should delegate** - critical for auto-invocation |
| `tools` | array | No | Tools available to the agent. Inherits all if omitted |
| `disallowedTools` | array | No | Tools to deny (removed from inherited set) |
| `model` | string | No | `sonnet`, `opus`, `haiku`, or `inherit` (default: `inherit`) |
| `permissionMode` | string | No | `default`, `acceptEdits`, `dontAsk`, `bypassPermissions`, `plan` |
| `skills` | array | No | Skills loaded into the agent's context at startup |
| `hooks` | object | No | Lifecycle hooks scoped to this agent |
| `memory` | string | No | Persistent memory: `user`, `project`, or `local` |

### Storage Locations (Priority Order)

| Location | Scope | Priority |
|:---------|:------|:---------|
| `--agents` CLI flag | Current session | 1 (highest) |
| `.claude/agents/` | Current project | 2 |
| `~/.claude/agents/` | All projects | 3 |
| Plugin `agents/` dir | Where plugin enabled | 4 (lowest) |

> "Project subagents (`.claude/agents/`) are ideal for subagents specific to a codebase. Check them into version control so your team can use and improve them collaboratively."
> — [Claude Code Docs](https://code.claude.com/docs/en/sub-agents)

### Memory Scopes

| Scope | Location | Shared? |
|:------|:---------|:--------|
| `user` | `~/.claude/agent-memory/<name>/` | Across all projects |
| `project` | `.claude/agent-memory/<name>/` | Via version control |
| `local` | `.claude/agent-memory-local/<name>/` | Project-specific, gitignored |

### Built-in Agents

| Agent | Model | Tools | Purpose |
|:------|:------|:------|:--------|
| Explore | Haiku | Read-only | File discovery, code search |
| Plan | Inherits | Read-only | Codebase research for planning |
| general-purpose | Inherits | All | Complex research, multi-step tasks |

---

## 2. Agent Design Best Practices

### System Prompt Architecture

**Source**: [Anthropic - Effective Context Engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)

**Progressive Disclosure** - Reveal information in layers:
1. **Metadata**: Name/description loaded at startup (no context cost)
2. **Primary docs**: SKILL.md loaded when relevant
3. **Supplementary**: Referenced files loaded dynamically as needed

**"Right Altitude" Principle**: Balance between overly rigid rules and vague guidance. Prompts should be "specific enough to guide behavior effectively yet flexible enough to provide strong heuristics."

**Contract Format** for system prompts:
- Role (1 line)
- Success criteria (bullets)
- Constraints (explicit boundaries)
- Uncertainty handling (permission to say "I don't know")
- Output format

**Structure**: Use XML tags or Markdown headers. "Models are tuned to pay extra attention to certain headings."

**Minimalism**: "Start with minimal prompts using your strongest available model, then iteratively add clear instructions based on identified failure modes."

**Context is finite**: "Every new token introduced depletes this budget. Carefully curate tokens available to the LLM."

### Degrees of Freedom

From [Anthropic Skills Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices):

> "Think of Claude as a robot exploring a path:
> - **Narrow bridge with cliffs**: One safe way forward. Provide specific guardrails (low freedom). Example: database migrations.
> - **Open field with no hazards**: Many paths lead to success. Give general direction and trust Claude (high freedom). Example: code reviews."

### Description Writing (Critical for Auto-Delegation)

The `description` field determines **when Claude automatically delegates** to an agent. It must clearly express:
- What the agent specializes in
- When it should be invoked
- What distinguishes it from other agents

> "Claude often ignores an appropriate sub-agent unless you name it explicitly" — making description quality crucial for auto-selection.

---

## 3. Architecture Patterns

### When to Use Single vs Multi-Agent

**Source**: [Anthropic - Building Effective Agents](https://www.anthropic.com/research/building-effective-agents)

**Single Agent** - Best when:
- Straightforward workflow within one reasoning context
- Simple tasks where coordination overhead isn't justified
- Debugging ease is important

**Multi-Agent** - Best when:
- 3+ major functions needed
- Tasks are parallelizable
- Context isolation improves quality (each agent gets fresh 200k window)
- Performance: Multi-agent "outperformed single-agent Claude Opus 4 by 90.2%" on research evaluations

**Trade-off**: Multi-agent adds 2-4x latency and ~15x token usage but pays off for complex, parallelizable work.

### Six Composable Patterns (Anthropic)

1. **Augmented LLM** - Foundation: LLM + retrieval + tools + memory
2. **Prompt Chaining** - Sequential steps, each processing previous output
3. **Routing** - Classify inputs → specialized handlers
4. **Parallelization** - Independent subtasks run simultaneously
5. **Orchestrator-Workers** - Central LLM breaks down and delegates dynamically
6. **Evaluator-Optimizer** - One generates, another provides feedback

**Production Rule**: "Give each subagent one job, and let an orchestrator coordinate. Make the orchestrator responsible for global planning, delegation, and state."

### Three Operating Principles for Subagents

From [Zach Wills tutorial](https://zachwills.net/how-to-use-claude-code-subagents-to-parallelize-development/):

1. **Parallel Execution** - Speed through concurrent specialized agents
2. **Sequential Handoffs** - Automation through agent pipelines
3. **Context Isolation** - Quality by preventing context contamination

---

## 4. Tool Design for Agents

**Source**: [Anthropic - Writing Tools for Agents](https://www.anthropic.com/engineering/writing-tools-for-agents)

### Core Principles

- **Less is more**: "More tools don't always lead to better outcomes"
- **Self-evidence**: "If engineers can't definitively say which tool applies, agents will struggle even more"
- **Token efficiency**: Return only high-signal information
- **Actionable errors**: Guide agents toward proper inputs, don't just return error codes

### Tool Description Quality

> "Even minor refinements dramatically improve performance—Claude Sonnet 3.5 achieved state-of-the-art SWE-bench results after precise description improvements"

- Use unambiguous parameter names (`user_id` not `user`)
- Explain specialized query formats
- Define terminology and clarify resource relationships

### Poka-Yoke (Error-Proofing)

- Use naturally occurring formats from internet text
- Require absolute paths instead of relative (improved reliability "flawlessly")
- Give models thinking space before forcing format decisions
- Eliminate excessive escaping overhead

---

## 5. Error Handling & Recovery

### Agent-Specific Error Taxonomy

From [ArXiv research](https://arxiv.org/abs/2509.25370):

1. Tool Hallucination
2. Argument Hallucination
3. Invalid Tool Invocation
4. Partial Tool Execution
5. Tool Output Hallucination
6. Invalid Intermediate Reasoning
7. Re-entrant Error Handling Failures

### Recovery Patterns

**Three-Phase Verification Cycle** (Anthropic Agent SDK):
1. **Gather Context** → Search and retrieve
2. **Take Action** → Execute via tools
3. **Verify Work** → Evaluate and iterate

**Self-Correction Mechanisms**:
- Rules-based validation: Define explicit rules, explain which failed and why
- Visual feedback: Screenshots/rendered outputs for UI tasks
- LLM-as-judge: Separate model evaluates fuzzy criteria

---

## 6. Evaluation & Testing

**Source**: [Anthropic - Demystifying Evals](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)

### Evaluation-Driven Development

1. Run Claude on representative tasks **without** the agent. Document failures.
2. Create evaluations: 3 scenarios testing identified gaps
3. Establish baseline performance
4. Write minimal instructions addressing gaps
5. Iterate: Execute evals, compare to baseline, refine

### Metrics

- **pass@k**: At least one correct solution across k attempts
- **pass^k**: All k trials succeed (critical for production reliability)
- **Start small**: 20-50 tasks from real failures is sufficient initially

### Key Principle

> "Avoid overly rigid step-checking since agents regularly find valid approaches that eval designers didn't anticipate. Grade outcomes, not processes."

---

## 7. Anti-Patterns to Avoid

### Architecture

- Using complex frameworks without understanding underlying mechanisms
- Adding agents that don't provide meaningful specialization
- Over-coordinating: "Using a complex pattern when basic sequential orchestration would suffice"

### Context & Memory

- Relying on context window as memory (costs spike, quality drops)
- "Dumb RAG": Dumping everything into a vector DB without curation
- Verbose auto-generated prompts requiring manual trimming

### Tool Design

- Replicating API endpoints without considering agent ergonomics
- Too many overlapping tools creating decision paralysis
- Returning verbose low-level data consuming agent context
- Vague error responses instead of actionable guidance

### Sub-Agent Specific

- **Activation failures**: Agents ignored without explicit naming
- **No iteration**: Declining work creates fresh instance, losing context
- **Token budget**: Multiple agents rapidly consume 200k limit
- **Transparency**: Internal reasoning invisible, making debugging impossible
- **Non-determinism**: Identical tasks produce inconsistent results

### Security

> "Permission sprawl is the fastest path to unsafe autonomy. Treat tool access like production IAM. Start from deny-all; allowlist only what a subagent needs."

---

## 8. Community Resources

### Agent Collections

| Repository | Size | Notes |
|:-----------|:-----|:------|
| [VoltAgent/awesome-claude-code-subagents](https://github.com/VoltAgent/awesome-claude-code-subagents) | 100+ agents | Largest curated collection |
| [wshobson/agents](https://github.com/wshobson/agents) | 112 agents, 73 plugins | Three-tier model strategy |
| [hesreallyhim/awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code) | 75+ repos | 22.9k stars, comprehensive |
| [VoltAgent/awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills) | 200+ skills | Cross-platform compatible |

### Marketplaces

- [SkillsMP](https://skillsmp.com/) - Independent agent skills aggregator
- [Build with Claude](https://www.buildwithclaude.com/) - Plugins, agents, commands, skills
- [Claude Code Marketplace](https://claudecodemarketplace.net/) - Community extensions
- [claudemarketplaces.com](https://claudemarketplaces.com/) - AI tools & extensions

### Key Tutorials

- [Parallelizing Development with Subagents](https://zachwills.net/how-to-use-claude-code-subagents-to-parallelize-development/) - Practical multi-agent example
- [Agent Skills Deep Dive](https://leehanchung.github.io/blogs/2025/10/26/claude-skills-deep-dive/) - Technical architecture analysis
- [Build Your First Skill](https://medium.com/@richardhightower/build-your-first-claude-code-skill-a-simple-project-memory-system-that-saves-hours-1d13f21aff9e) - Step-by-step tutorial

---

## Primary Sources

### Anthropic Official
- [Create custom subagents](https://code.claude.com/docs/en/sub-agents)
- [Building Effective AI Agents](https://www.anthropic.com/research/building-effective-agents)
- [Effective Context Engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- [Writing Tools for Agents](https://www.anthropic.com/engineering/writing-tools-for-agents)
- [Building Agents with the Claude Agent SDK](https://claude.com/blog/building-agents-with-the-claude-agent-sdk)
- [Multi-Agent Research System](https://www.anthropic.com/engineering/multi-agent-research-system)
- [Demystifying Evals for AI Agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)
- [Agent Skills Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- [Effective Harnesses for Long-Running Agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- [Equipping Agents for the Real World](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
- [Framework for Safe and Trustworthy Agents](https://www.anthropic.com/news/our-framework-for-developing-safe-and-trustworthy-agents)
- [Plugins reference](https://code.claude.com/docs/en/plugins-reference)
- [Extend Claude with skills](https://code.claude.com/docs/en/skills)
- [Subagents in the SDK](https://platform.claude.com/docs/en/agent-sdk/subagents)

### Community & Industry
- [Agent Design Patterns - Lance Martin](https://rlancemartin.github.io/2026/01/09/agent_design/)
- [Sub-Agent Anti-Patterns - Steve Kinney](https://stevekinney.com/courses/ai-development/subagent-anti-patterns)
- [Six Levels of Agentic Behavior - Vellum](https://www.vellum.ai/blog/levels-of-agentic-behavior)
- [Choosing Multi-Agent Architecture - LangChain](https://blog.langchain.com/choosing-the-right-multi-agent-architecture/)
- [Single vs Multi-Agent - Redis](https://redis.io/blog/single-agent-vs-multi-agent-systems/)
- [Error Recovery Strategies - GoCodeo](https://www.gocodeo.com/post/error-recovery-and-fallback-strategies-in-ai-agent-development)
- [Where LLM Agents Fail - ArXiv](https://arxiv.org/abs/2509.25370)
- [Common AI Agent Mistakes - WildNet Edge](https://www.wildnetedge.com/blogs/common-ai-agent-development-mistakes-and-how-to-avoid-them)

### Research Papers
- [ArXiv: PALADIN - Self-Correcting LLM Agents](https://arxiv.org/html/2509.25238v1)
- [ArXiv: Architecting Resilient LLM Agents](https://arxiv.org/pdf/2509.08646)
- [Knight Columbia: Levels of Autonomy for AI Agents](https://knightcolumbia.org/content/levels-of-autonomy-for-ai-agents-1)
