---
last_updated: 2026-02-02
topic: Blueprint - learning-from-sessions skill
tags: [blueprint, reference, learning-from-sessions]
status: historical
note: "Reference document used to create newskills/learning-from-sessions/. Skill is fully implemented."
---

# Blueprint: `learning-from-sessions` (Reflective Skill Learner)

**Date:** 2026-01-28
**Target:** `newskills/learning-from-sessions/`
**Deploy to:** `~/.claude/skills/learning-from-sessions/`

---

## Purpose

A skill that activates after sessions or during retrospectives to extract reusable knowledge from what just happened -- debugging discoveries, workarounds, corrections, and non-obvious solutions -- and saves them as new skill files or CLAUDE.md entries. Combines Claudeception's autonomous extraction workflow with Claude-Reflect's capture-then-review architecture.

---

## Research Files

- [Claudeception (blader)](file:///C:/code/commandbase/.docs/research/01-28-2026-claudeception-repo.md) -- 6-step extraction workflow, dual activation, quality gates, self-reflection prompts, academic research foundation
- [Continuous Learning Skill (blader)](file:///C:/code/commandbase/.docs/research/01-28-2026-claudeception-continuous-learning-skill.md) -- Same system, earlier version, persistence mechanism explained
- [Claude-Reflect (BayramAnnakov)](file:///C:/code/commandbase/.docs/research/01-28-2026-claude-reflect-repo.md) -- Two-stage capture/process, regex + semantic hybrid detection, correction queue, skill improvement routing
- [Anthropic Skills (official)](file:///C:/code/commandbase/.docs/research/01-28-2026-anthropic-skills-repo.md) -- Validation spec for any generated skills
- [All Repos Index](file:///C:/code/commandbase/.docs/research/01-28-2026-skillcreator-repos.md)

## Cloned Repos (read for reference patterns)

- `C:/code/repo-library/Claudeception/` -- PRIMARY reference: `SKILL.md`, `scripts/claudeception-activator.sh`, `resources/`, `examples/`
- `C:/code/repo-library/claude-code-continuous-learning-skill/` -- Same content as Claudeception (earlier fork)
- `C:/code/repo-library/claude-reflect/` -- `commands/reflect.md`, `commands/reflect-skills.md`, `scripts/lib/reflect_utils.py`, `scripts/lib/semantic_detector.py`, `hooks/hooks.json`
- `C:/code/repo-library/skills/` -- Official validation rules at `skills/skill-creator/scripts/quick_validate.py`

---

## What to Take from Each

### From Claudeception (blader) -- PRIMARY INFLUENCE
- 6-step extraction workflow:
  1. Check for existing skills (dedup-first with `rg` search)
  2. Identify the knowledge (4 analysis questions)
  3. Research best practices (web search for tech-specific topics)
  4. Structure the skill (standard sections)
  5. Write effective descriptions (semantic matching optimization)
  6. Save the skill (project vs user-level)
- Self-reflection prompts (5 introspection questions after each task)
- Quality gates (9-item checklist)
- Anti-patterns (over-extraction, vague descriptions, unverified solutions, doc duplication, stale knowledge)
- Skill lifecycle (Creation → Refinement → Deprecation → Archival)
- Dedup decision matrix (create new / update existing / add variant / deprecate)
- Forced eval hook pattern (`UserPromptSubmit` script injecting evaluation on every prompt)
- Academic research basis (Voyager, CASCADE, SEAgent, Reflexion, EvoFSM)
- Example extracted skills (Next.js debugging, Prisma connection pool, TypeScript circular deps)

### From Claude-Reflect (BayramAnnakov) -- ARCHITECTURE
- Two-stage architecture: automatic capture (hooks) → manual processing (command)
- Queue system: `learnings-queue.json` bridges capture and processing stages
- Regex + semantic hybrid detection:
  - Regex patterns for fast real-time capture (correction, guardrail, positive, explicit patterns)
  - Semantic AI validation during `/reflect` for accuracy
- Confidence scoring with length adjustments
- False positive filtering (questions, task requests, bug reports)
- Multi-target sync: global CLAUDE.md + project CLAUDE.md + subdirectory CLAUDE.md + skill files
- Skill improvement routing: corrections during skill execution route back to the skill file
- Session history scanning (`--scan-history`, `--days N`)
- Deduplication command (`--dedupe`)
- Decay metadata on queue items

### From Anthropic Skills (official) -- VALIDATION
- Any skills generated must pass: name `^[a-z0-9-]+$`, max 64 chars, description max 1024 chars, no angle brackets
- Allowed frontmatter: `name`, `description`, `license`, `allowed-tools`, `metadata`

---

## Proposed Structure

```
newskills/learning-from-sessions/
├── SKILL.md                              # Core workflow (target: 250-350 lines)
├── reference/
│   ├── extraction-workflow.md            # Detailed 6-step process
│   ├── quality-gates.md                  # Checklist, anti-patterns, when NOT to extract
│   ├── description-optimization.md       # How to write descriptions for future retrieval
│   └── research-foundations.md           # Academic papers informing the design
└── templates/
    └── extracted-skill-template.md       # Standard template for generated skills
```

## SKILL.md Frontmatter

```yaml
---
name: learning-from-sessions
description: >
  Use this skill to extract reusable knowledge from work sessions. Activates when:
  (1) reviewing what was learned during a session, (2) a non-obvious debugging
  discovery or workaround was found, (3) user says "save this as a skill" or
  "what did we learn?", (4) running /learn to review session learnings,
  (5) after trial-and-error investigation that produced extractable knowledge.
  Captures debugging discoveries, error resolutions, configuration insights,
  and workarounds as new skill files for future sessions.
---
```

## Core Workflow (for SKILL.md body)

### When to Activate (Automatic Trigger Conditions)
- Non-obvious debugging (>10 min investigation, not in docs)
- Error resolution where the error message was misleading
- Workaround discovery requiring experimentation
- Configuration insight differing from standard patterns
- Trial-and-error success (multiple approaches tried before solution)

### Self-Reflection Prompts (run after completing tasks)
1. "What did I just learn that wasn't obvious before starting?"
2. "If I faced this exact problem again, what would I wish I knew?"
3. "What error message or symptom led me here, and what was the actual cause?"
4. "Is this pattern specific to this project, or would it help in similar projects?"
5. "What would I tell a colleague who hits this same issue?"

### Step 1: Check for Existing Skills (Dedup-First)
Search skill directories before creating:
```sh
SKILL_DIRS=(".claude/skills" "$HOME/.claude/skills")
rg --files -g 'SKILL.md' "${SKILL_DIRS[@]}" 2>/dev/null
rg -i "keyword1|keyword2" "${SKILL_DIRS[@]}" 2>/dev/null
```

Decision matrix:
| Found | Action |
|-------|--------|
| Nothing related | Create new skill |
| Same trigger and fix | Update existing (version bump) |
| Same trigger, different cause | Create new + cross-links |
| Partial overlap | Add variant subsection to existing |
| Stale or wrong | Deprecate + create replacement |

### Step 2: Identify the Knowledge
Four analysis questions:
- What was the problem?
- What was non-obvious about the solution?
- What would help solve this faster next time?
- What are the exact trigger conditions?

### Step 3: Research Best Practices
Web search when the topic involves specific technologies:
- `"[technology] [problem] best practices 2026"`
- `"[technology] [error message] solution 2026"`
- Skip for: project-internal patterns, context-specific solutions, stable generic concepts

### Step 4: Structure and Save
- Use extracted-skill-template.md for consistent format
- Optimize description for semantic matching (exact error messages, framework names, action phrases)
- Save to project (`.claude/skills/`) or user (`~/.claude/skills/`) based on scope
- Apply quality gates before writing

### Step 5: Quality Gates
- Description contains specific trigger conditions
- Solution has been verified to work
- Content is specific enough to be actionable
- Content is general enough to be reusable
- No sensitive information
- Doesn't duplicate existing skills or docs
- Web research conducted when appropriate

### Anti-Patterns
- Over-extraction: not every task deserves a skill
- Vague descriptions: "Helps with React problems" won't surface
- Unverified solutions: only extract what actually worked
- Documentation duplication: link to docs, add what's missing
- Stale knowledge: version and date everything

### Retrospective Mode
When invoked explicitly (/learn or natural language):
1. Review session conversation history
2. Identify skill candidates with justifications
3. Prioritize by reuse value
4. Extract top 1-3 skills
5. Summarize what was created and why

### Output Decision: Skill vs CLAUDE.md Entry
- **New skill file** when: reusable across projects, involves multi-step solution, has clear trigger conditions
- **CLAUDE.md entry** when: project-specific preference, simple convention, correction to existing behavior

---

## Optional: Hook for Automatic Activation

A `UserPromptSubmit` hook can inject evaluation on every prompt (from Claudeception pattern):

```bash
#!/bin/bash
cat << 'EOF'
After completing this request, briefly evaluate:
- Did this require non-obvious investigation?
- Would future sessions benefit from this knowledge?
If YES to both: activate Skill(learning-from-sessions)
If NO: skip silently
EOF
```

This is optional -- the skill works without the hook via semantic matching and explicit invocation. The hook increases activation rate but adds ~25 lines of context per prompt.

---

## Prompt for Separate Window

Copy the following into a new Claude Code session:

```
I need you to build a Claude Code skill called `learning-from-sessions`. This is a reflective meta-skill that extracts reusable knowledge from work sessions and saves it as new skill files.

Working directory: C:/code/commandbase/newskills/learning-from-sessions/

BEFORE writing any code, read these research files and cloned repos for context:

Research files (read all):
- C:/code/commandbase/.docs/research/01-28-2026-claudeception-repo.md
- C:/code/commandbase/.docs/research/01-28-2026-claudeception-continuous-learning-skill.md
- C:/code/commandbase/.docs/research/01-28-2026-claude-reflect-repo.md

Reference repos (read the key files):
- C:/code/repo-library/Claudeception/SKILL.md (PRIMARY model -- the 6-step extraction workflow)
- C:/code/repo-library/Claudeception/scripts/claudeception-activator.sh (hook pattern)
- C:/code/repo-library/Claudeception/resources/skill-template.md (output template)
- C:/code/repo-library/Claudeception/resources/research-references.md (academic basis)
- C:/code/repo-library/Claudeception/examples/ (all 3 example extracted skills)
- C:/code/repo-library/claude-reflect/commands/reflect.md (the /reflect workflow)
- C:/code/repo-library/claude-reflect/commands/reflect-skills.md (skill discovery from sessions)
- C:/code/repo-library/claude-reflect/scripts/lib/reflect_utils.py (detection patterns, queue operations)
- C:/code/repo-library/claude-reflect/scripts/lib/semantic_detector.py (AI validation)
- C:/code/repo-library/claude-reflect/hooks/hooks.json (4 hook definitions)

Blueprint with full instructions:
- C:/code/commandbase/.docs/plans/learning-from-sessions-blueprint.md

Create the skill with this structure:
newskills/learning-from-sessions/
├── SKILL.md                              # Core workflow (250-350 lines)
├── reference/
│   ├── extraction-workflow.md            # Detailed 6-step process with examples
│   ├── quality-gates.md                  # Checklist, anti-patterns, when NOT to extract
│   ├── description-optimization.md       # How to write descriptions for semantic retrieval
│   └── research-foundations.md           # Academic papers informing the design
└── templates/
    └── extracted-skill-template.md       # Standard template for generated skills

Key requirements:
1. SKILL.md frontmatter: name=learning-from-sessions, description with multiple trigger phrases for semantic matching
2. Combine Claudeception's 6-step extraction workflow with Claude-Reflect's two-stage (capture/process) architecture concept
3. Include the 5 self-reflection prompts from Claudeception
4. Include the dedup-first check (search existing skills before creating)
5. Include the quality gates (9-item checklist) and anti-patterns list
6. Include the web research step for technology-specific topics
7. The output decision section: when to create a new skill file vs when to add a CLAUDE.md entry
8. The extracted-skill-template.md should follow Claudeception's structure: Problem, Context/Trigger Conditions, Solution, Verification, Example, Notes, References
9. Description optimization guide should teach writing descriptions as "retrieval keys" for semantic matching
10. Keep SKILL.md under 350 lines -- put depth in reference/ files
11. DO NOT copy content verbatim from repos -- synthesize the best patterns into original content
12. This skill should reference `creating-skills` (the active creator skill) for validation rules and templates when generating new skills
```
