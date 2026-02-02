---
git_commit: 7d7f5915f90db26e1a3fc52db6ac2e68d6d705a2
last_updated: 2026-01-28
last_updated_by: rcode
topic: "Claudeception - Autonomous Skill Extraction from Sessions"
tags: [research, skill-extraction, continuous-learning, meta-skill, claudeception]
status: complete
references:
  - SKILL.md
  - README.md
  - WARP.md
  - scripts/claudeception-activator.sh
  - resources/research-references.md
  - resources/skill-template.md
  - examples/nextjs-server-side-error-debugging/SKILL.md
  - examples/prisma-connection-pool-exhaustion/SKILL.md
  - examples/typescript-circular-dependency/SKILL.md
---

# Research: Claudeception (blader/Claudeception)

**Date**: 2026-01-28
**Repository**: https://github.com/blader/Claudeception
**Author**: blader
**Commits**: 15 (latest: 7d7f591)
**License**: MIT

## Research Question

Analyze the Claudeception repository's architecture, skill extraction patterns, quality gates, activation mechanisms, and research foundations as a reference for skill-creator tooling.

## Summary

Claudeception is a **meta-skill** - a Claude Code skill whose purpose is to create other skills. It monitors work sessions for non-obvious discoveries and autonomously extracts reusable knowledge into new SKILL.md files. It combines two activation modes (automatic semantic matching + forced evaluation hook), strict quality gates, and an academic research foundation (Voyager, CASCADE, SEAgent, Reflexion). The repo is lean (10 files, 15 commits) and focused entirely on the skill definition + supporting resources.

## Detailed Findings

### Repository Structure

```
Claudeception/
├── SKILL.md                                          # Main skill definition (389 lines)
├── README.md                                         # Installation + usage docs (187 lines)
├── WARP.md                                           # Warp.dev guidance (55 lines)
├── LICENSE                                           # MIT
├── scripts/
│   └── claudeception-activator.sh                    # Hook script (39 lines)
├── resources/
│   ├── research-references.md                        # Academic foundations (184 lines)
│   └── skill-template.md                             # Template for extracted skills (96 lines)
└── examples/
    ├── nextjs-server-side-error-debugging/SKILL.md   # Example extracted skill
    ├── prisma-connection-pool-exhaustion/SKILL.md     # Example extracted skill
    └── typescript-circular-dependency/SKILL.md        # Example extracted skill
```

No build system, no dependencies, no tests. Pure markdown + one bash script.

### Core Skill Definition (SKILL.md)

**Frontmatter** (`SKILL.md:1-22`):
```yaml
name: claudeception
description: |
  Claudeception is a continuous learning system that extracts reusable knowledge from work sessions.
  Triggers: (1) /claudeception command to review session learnings, (2) "save this as a skill"
  or "extract a skill from this", (3) "what did we learn?", (4) After any task involving
  non-obvious debugging, workarounds, or trial-and-error discovery.
version: 3.0.0
allowed-tools:
  - Read, Write, Edit, Grep, Glob, WebSearch, WebFetch, Skill, AskUserQuestion, TodoWrite
```

The description is optimized for semantic matching with multiple trigger phrases. Version 3.0.0 indicates significant iteration (from `claude-code-continuous-learning-skill` repo → rebranded to Claudeception).

**Allowed Tools**: Notably includes `WebSearch` and `WebFetch` for researching best practices before creating skills, and `Skill` for invoking other skills during extraction.

### Six-Step Extraction Process (SKILL.md:66-278)

1. **Check for Existing Skills** (`SKILL.md:66-103`): Searches `SKILL_DIRS` array across project-level (`.claude/skills`), user-level (`~/.claude/skills`), and codex-level (`~/.codex/skills`) using `rg` commands. Decision matrix determines: create new, update existing, add variant subsection, or deprecate. Uses semantic versioning (patch/minor/major).

2. **Identify the Knowledge** (`SKILL.md:105-111`): Four-question framework:
   - What was the problem?
   - What was non-obvious?
   - What would help solve faster next time?
   - What are exact trigger conditions?

3. **Research Best Practices** (`SKILL.md:113-155`): Web search step before creating skills. Always searches for technology-specific topics, post-2025 changes, official docs. Skips for project-internal patterns. Search strategy: official docs → best practices → common issues → review → cite.

4. **Structure the Skill** (`SKILL.md:157-195`): YAML frontmatter + seven sections: Problem, Context/Trigger Conditions, Solution, Verification, Example, Notes, References.

5. **Write Effective Descriptions** (`SKILL.md:197-213`): Emphasis on semantic matching optimization. Requires specific symptoms, context markers, action phrases. Example demonstrates error-message-level specificity.

6. **Save the Skill** (`SKILL.md:215-222`): Project-level (`.claude/skills/[name]/SKILL.md`) or user-level (`~/.claude/skills/[name]/SKILL.md`). Optional `scripts/` subdirectory.

### Activation Mechanism

**Dual-mode activation:**

1. **Semantic Matching** (passive): Claude Code's native skill system matches the description field against current context at ~100 tokens per skill. The multi-trigger description is designed to surface on debugging, workarounds, skill-related phrases, and retrospective keywords.

2. **Forced Evaluation Hook** (active, `scripts/claudeception-activator.sh:1-39`): A `UserPromptSubmit` hook that injects a mandatory evaluation prompt on every user interaction:
   ```
   MANDATORY SKILL EVALUATION REQUIRED
   1. COMPLETE the user's request first
   2. EVALUATE: Did this require non-obvious investigation?
   3. IF YES: ACTIVATE Skill(claudeception)
   4. IF NO: SKIP
   ```

   The hook uses `cat << 'EOF'` to output a formatted prompt injection. Installed via `~/.claude/settings.json` under `hooks.UserPromptSubmit`. The README notes this "achieves higher activation rates than relying on semantic description matching alone."

### Quality Gates (SKILL.md:258-269)

Nine-item checklist:
- Description contains specific trigger conditions
- Solution has been verified to work
- Content is specific enough to be actionable
- Content is general enough to be reusable
- No sensitive information (credentials, internal URLs)
- Skill doesn't duplicate existing documentation or skills
- Web research conducted when appropriate
- References section included if web sources consulted
- Current best practices (post-2025) incorporated

### Anti-Patterns (SKILL.md:271-277)

Five explicitly prohibited patterns:
1. **Over-extraction**: Not every task deserves a skill
2. **Vague descriptions**: "Helps with React problems" won't surface
3. **Unverified solutions**: Only extract what actually worked
4. **Documentation duplication**: Link to docs, add what's missing
5. **Stale knowledge**: Version and date everything

### Retrospective Mode (SKILL.md:225-234)

Triggered by `/claudeception` command. Five-step protocol:
1. Review session conversation history
2. Identify skill candidates with justifications
3. Prioritize by reuse value
4. Extract top 1-3 skills
5. Summarize what was created and why

### Self-Reflection Prompts (SKILL.md:236-244)

Five introspection questions run after each task:
- "What did I just learn that wasn't obvious before starting?"
- "If I faced this exact problem again, what would I wish I knew?"
- "What error message or symptom led me here, and what was the actual cause?"
- "Is this pattern specific to this project, or would it help in similar projects?"
- "What would I tell a colleague who hits this same issue?"

### Automatic Trigger Conditions (SKILL.md:358-370)

Five criteria for automatic activation (any one suffices):
1. Non-obvious debugging (>10 min investigation, not in docs)
2. Error resolution where message was misleading
3. Workaround discovery requiring experimentation
4. Configuration insight differing from standard patterns
5. Trial-and-error success (multiple approaches tried)

### Academic Research Foundation (resources/research-references.md)

Six papers inform the design:

| Paper | Year | Key Concept Applied |
|-------|------|-------------------|
| **Voyager** (Wang et al.) | 2023 | Ever-growing skill library, self-verification, compositional skills |
| **CASCADE** | 2024 | Meta-skills (skills for acquiring skills), knowledge codification |
| **SEAgent** (Sun et al.) | 2025 | Learning from trial-and-error, failures and successes |
| **Reflexion** (Shinn et al.) | 2023 | Self-reflection prompts, verbal reinforcement, long-term memory |
| **EvoFSM** | 2024 | Experience pools, strategy distillation, warm-starting |
| **Professional Agents** | 2024 | Quality criteria for specialized expertise |

Also references Anthropic's engineering blog on agent skills and official Claude Code skills docs.

### Skill Template (resources/skill-template.md)

96-line template with:
- YAML frontmatter (name, description, author, version, date)
- Seven sections: Problem, Context/Trigger Conditions, Solution, Verification, Example, Notes
- Extraction checklist as HTML comment (10 items)
- Emphasis on description precision for semantic matching

### Example Skills

Three fully-formed example skills demonstrate the output format:

1. **nextjs-server-side-error-debugging** (`examples/nextjs-server-side-error-debugging/SKILL.md`):
   - Trigger: empty browser console + 500 errors in Next.js
   - Description includes 4 specific trigger conditions
   - Solution: 4 steps (check terminal, add error handling, check production logs, common causes list)

2. **prisma-connection-pool-exhaustion** (`examples/prisma-connection-pool-exhaustion/SKILL.md`):
   - Trigger: P2024 error, "too many connections" in serverless
   - Description lists 4 error message variants
   - Solution: 4 steps (connection pooling service, configure limits, singleton pattern, URL params)

3. **typescript-circular-dependency** (`examples/typescript-circular-dependency/SKILL.md`):
   - Trigger: "Cannot access X before initialization", undefined imports
   - Description lists 5 symptom patterns
   - Solution: detection (madge), 5 resolution strategies, prevention (CI check + ESLint rule)

### Warp.dev Integration (WARP.md)

55-line guidance file for Warp terminal IDE. Documents project overview, key files, skill format, installation paths, and quality criteria. Demonstrates multi-editor support awareness.

### Evolution History

Git log shows clear progression:
1. `2d56f25` - Initial commit as "Claude Code Continuous Learning Skill"
2. `c0daa23` - Rebranded to "Claudeception"
3. `1ce1b99` - Added activation hook for reliable triggering
4. `2dcd0c3` - Enhanced with web research and safer tool restrictions
5. `afd1da2` - Added Step 1 (check existing skills before creating)
6. `a65e134` - Distinguished user-level vs project-level setup

## Code References

- `SKILL.md:1-22` - Frontmatter with trigger description and allowed tools
- `SKILL.md:66-103` - Step 1: Check existing skills (dedup logic + decision matrix)
- `SKILL.md:113-155` - Step 3: Web research protocol before skill creation
- `SKILL.md:157-195` - Step 4: Skill structure template
- `SKILL.md:197-213` - Step 5: Description optimization for semantic matching
- `SKILL.md:258-269` - Quality gates (9-item checklist)
- `SKILL.md:271-277` - Anti-patterns
- `SKILL.md:225-234` - Retrospective mode (`/claudeception` command)
- `SKILL.md:236-244` - Self-reflection prompts
- `SKILL.md:358-370` - Automatic trigger conditions
- `scripts/claudeception-activator.sh:12-39` - Forced evaluation hook (UserPromptSubmit)
- `resources/research-references.md:7-93` - Core papers (Voyager, CASCADE, SEAgent, Reflexion)
- `resources/skill-template.md:1-96` - Output template with extraction checklist

## Architecture Notes

### Key Design Patterns

1. **Meta-Skill Architecture**: The skill creates skills. It's self-referential but scoped - it doesn't modify itself, only produces new SKILL.md files following its template.

2. **Dual Activation (Semantic + Hook)**: Two independent paths to activation ensure coverage. Semantic matching catches natural trigger phrases. The hook forces evaluation on every prompt, acting as a safety net.

3. **Deduplication-First Workflow**: Step 1 searches existing skills before creating. Decision matrix handles: exact match (update), same trigger/different cause (new + cross-links), partial overlap (add variant subsection), stale (deprecate + replace).

4. **Research-Before-Create**: Web search step ensures skills incorporate current best practices, not just session-local knowledge. Explicit skip criteria prevent unnecessary searches for project-internal patterns.

5. **Description-as-Retrieval-Key**: The description field is treated as a search index. Multiple trigger phrases, exact error messages, and technology markers maximize semantic matching surface area.

6. **Quality Over Quantity**: Multiple filtering layers (extraction criteria, quality gates, anti-patterns) prevent low-value skill proliferation. The "would this help someone in 6 months?" heuristic is the central quality test.

7. **Semantic Versioning for Skills**: Patch (typos), minor (new scenario), major (breaking/deprecation) applied to skill files, enabling lifecycle management.

## Patterns Relevant to commandbase

| Pattern | Implementation | Applicability |
|---------|---------------|---------------|
| Forced Eval Hook | `UserPromptSubmit` bash script injecting evaluation prompt | Could adapt for any skill that needs reliable per-session activation |
| Dedup-First Step | `rg` across multiple skill directories before creation | Prevents skill sprawl in any creator tool |
| Description Optimization | Multi-trigger phrases, exact error messages, action verbs | Template for any skill's frontmatter description |
| Web Research Gate | Search before creating technology-specific skills | Ensures freshness, prevents stale knowledge |
| Quality Checklist | 9-item verification before save | Reusable as a validation step in any creation workflow |
| Self-Reflection Prompts | 5 introspection questions post-task | Could integrate into retrospective/learn workflows |

## Open Questions

- The hook injects on **every** `UserPromptSubmit` - no throttling or session-aware filtering. For high-frequency prompts, this adds context overhead on every turn.
- No automated testing of extracted skills. Verification is described as manual.
- The `~/.codex/skills` path in Step 1 suggests awareness of OpenAI Codex CLI, but no further integration details.
- No mechanism for skill sharing or import across users/teams beyond manual git operations.
