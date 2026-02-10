---
git_commit: 8e92bba
last_updated: 2026-02-09
last_updated_by: docs-updater
last_updated_note: "Added frontmatter, updated file reference from legacy ~/.claude/skills path to plugin path, noted expanded enforcement sections in SKILL.md"
references:
  - plugins/commandbase-core/skills/debating-options/SKILL.md
---

# Research: debating-options Skill

## Overview

The `debating-options` skill (`plugins/commandbase-core/skills/debating-options/SKILL.md`) launches parallel research agents to investigate multiple options, then synthesizes findings into a structured decision matrix with recommendation. It operates in two modes: Objective (default) and Advocate.

**Trigger phrases**: `/debating-options`, `debate these options`, `compare these choices`, `which should I choose`

## Modes

| Mode | Default | When to Use |
|------|---------|-------------|
| **Objective** | Yes | User wants facts and tradeoffs to decide themselves |
| **Advocate** | No | User is unsure, wants persuasive cases to help clarify thinking |

## Objective Mode Process (Default)

### 5-Step Workflow (SKILL.md Gate Function + Process sections)

1. **IDENTIFY OPTIONS**: Extract 2-4 distinct options from context
2. **LAUNCH RESEARCHERS** (parallel): One background agent per option, reports facts without advocacy
3. **WAIT FOR RESULTS**: Collect all research findings, ensure all agents complete
4. **SYNTHESIZE** (judge agent): Create decision matrix with 5-6 criteria, rate each option, provide recommendation
5. **PRESENT TO USER**: Show decision matrix and recommendation

### Objective Researcher Template

```
You are a RESEARCHER analyzing this option:

**Option:** [OPTION]
**Context:** [BACKGROUND IF RELEVANT]

Your job is to research this option objectively. Report facts, not advocacy.

Cover:
- What is this option? (brief description)
- Key strengths (factual, not persuasive)
- Key weaknesses (honest limitations)
- Best use cases (when this option fits)
- Poor use cases (when to avoid)
```

## Advocate Mode Process

### Activation

Switch to Advocate mode when user:
- Says "I'm not sure", "help me decide", "I can't choose"
- Explicitly requests advocate mode
- Seems paralyzed by the decision
- Wants to understand *why* each option matters

### Advocate Agent Template

```
You are an ADVOCATE for this position:

**Your Position:** [OPTION]

Your job is to argue FOR this position. Be persuasive but honest.

Consider:
- When would this option be most valuable?
- What problems does it solve?
- What are the genuine strengths?

Also acknowledge 1-2 weaknesses (intellectual honesty), framed as manageable trade-offs.
```

## Decision Matrix Format

### Judge/Synthesizer Template

```
## Decision Matrix

| Criteria | [Option 1] | [Option 2] | [Option 3] |
|----------|------------|------------|------------|
| [criterion] | [rating + note] | [rating + note] | [rating + note] |

Include 5-6 meaningful criteria relevant to the decision domain.
Use ratings: Strong, Moderate, Weak

## Synthesis
[2-3 sentences on core trade-offs]

## Recommendation
**Winner: [Option]**
[3-4 sentences explaining why]
```

## Parallel Agent Spawning Pattern

### Implementation Configuration (SKILL.md Implementation Notes section)

- **Agent type**: `subagent_type: general-purpose` for all agents
- **Researchers/Advocates**: `model: haiku` (fast, parallel)
- **Judge/Synthesizer**: `model: sonnet` (synthesis quality matters)
- **Execution**: `run_in_background: true` for parallel execution
- **Collection**: Use `TaskOutput` to collect results before judging

### Workflow Architecture

```
User Input
    ↓
Option Identification (2-4 options)
    ↓
Parallel Spawn → [Agent 1] [Agent 2] [Agent 3] [Agent N]
    ↓              ↓          ↓          ↓          ↓
TaskOutput ← [Result 1] [Result 2] [Result 3] [Result N]
    ↓
Judge Agent (synthesis)
    ↓
Decision Matrix + Recommendation
    ↓
User Presentation
```

## Example Invocations

**Objective (default):**
```
User: /debating-options React vs Vue vs Svelte for my new project
```
Response: Launches 3 objective researchers, synthesizes into matrix.

**Advocate:**
```
User: /debating-options I'm not sure whether to use REST or GraphQL
User: /debating-options --advocate Kubernetes vs Docker Swarm
```
Response: Launches advocates who argue for each option, judge decides.

## File Reference

- Main: `plugins/commandbase-core/skills/debating-options/SKILL.md`
