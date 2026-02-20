# Research Foundations

The extraction workflow in this skill is informed by academic research on how AI agents learn from experience. These papers establish the theoretical basis for why structured knowledge extraction outperforms ad-hoc note-taking.

## Core Papers

### Voyager: An Open-Ended Embodied Agent with Large Language Models
**Wang et al., 2023**

Key contribution: Ever-growing skill library where agents store verified solutions as reusable code. Skills are indexed by description and composed into higher-level behaviors.

What we took: The concept of a growing skill library indexed by descriptions. Skills must be verified before storage (no unverified knowledge). Skills compose -- one extracted skill can reference another.

### CASCADE: Meta-Skills for Learning
**2024**

Key contribution: Meta-skills that teach agents how to learn, codify knowledge, and consolidate memory across sessions.

What we took: This skill IS a meta-skill -- it teaches Claude how to extract knowledge from sessions. The distinction between raw experience and codified knowledge. Not everything experienced is worth codifying.

### SEAgent: Self-Evolving Agents through Trial-and-Error
**Sun et al., 2025**

Key contribution: Agents that learn from trial-and-error by storing failed approaches alongside successful ones, building experiential knowledge pools.

What we took: The value of capturing non-obvious solutions (ones found through trial-and-error, not from documentation). The trigger condition "multiple approaches tried before solution found" comes from this research.

### Reflexion: Language Agents with Verbal Reinforcement Learning
**Shinn et al., 2023**

Key contribution: Self-reflection prompts that transform experience into verbal feedback stored in long-term memory. Agents use this feedback to avoid repeating mistakes.

What we took: The 5 self-reflection prompts that run after task completion. The principle that reflecting on WHY something worked (not just WHAT worked) produces more transferable knowledge.

### EvoFSM: Experience Pools and Strategy Distillation
**2024**

Key contribution: Experience pools where agents accumulate diverse problem-solving strategies, then distill the most effective patterns into reusable strategies.

What we took: The quality gates concept -- not all experience deserves extraction. The worth assessment filters raw experience into high-value patterns. Quantity without quality degrades retrieval.

## Design Principles from Research

These principles recur across the literature and inform the extraction workflow:

1. **Verify before storing**: Every paper emphasizes that unverified knowledge degrades the skill library over time (Voyager, SEAgent).

2. **Description as retrieval key**: Skills are only useful if they can be found. Description quality directly determines retrieval accuracy (Voyager, CASCADE).

3. **Dedup-first**: Duplicate knowledge wastes storage and confuses retrieval. Check before creating (CASCADE, EvoFSM).

4. **Reflect, don't just record**: Raw experience is less transferable than reflected knowledge. The self-reflection prompts force analysis of WHY something worked (Reflexion).

5. **Quality over quantity**: A smaller library of high-quality skills outperforms a large library of mediocre ones (EvoFSM, Voyager).

## Implementation Sources

The practical implementation patterns come from two open-source projects:

- **Claudeception** (blader): 6-step extraction workflow, self-reflection prompts, quality gates, dedup decision matrix, output template with standard sections
- **Claude-Reflect** (BayramAnnakov): Two-stage capture/process architecture, regex+semantic hybrid detection, multi-target routing, skill improvement feedback loop

These projects translated the academic concepts into working Claude Code workflows. This skill synthesizes their best patterns into a single extraction process.
