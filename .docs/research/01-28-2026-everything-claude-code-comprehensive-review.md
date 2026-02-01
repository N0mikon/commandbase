---
git_commit: 22359f4
last_updated: 2026-01-28
last_updated_by: rcode
topic: "Comprehensive Review of everything-claude-code for Suite Enhancement"
tags: [research, workflow, skills, agents, hooks, commands]
status: complete
references:
  - C:/code/everything-claude-code/skills/
  - C:/code/everything-claude-code/commands/
  - C:/code/everything-claude-code/agents/
  - C:/code/everything-claude-code/hooks/hooks.json
  - C:/code/everything-claude-code/contexts/
  - C:/code/everything-claude-code/rules/
---

# Comprehensive Review: everything-claude-code Repository

**Date**: 2026-01-28
**Branch**: master

## Research Question

Conduct a thorough review of everything-claude-code to identify ALL patterns, commands, skills, and agents we could add to our suite - not just the 6 previously identified.

## Executive Summary

The previous research (`01-28-2026-everything-claude-code-patterns.md`) identified only 6 patterns and recommended `/learn` and `/checkpoint`. This comprehensive review found **significantly more** that could enhance our workflow:

| Category | Previously Found | Actually Exists | Gap |
|----------|-----------------|-----------------|-----|
| Skills | 7 mentioned | **16 total** | 9 missed |
| Commands | 6 highlighted | **23 total** | 17 missed |
| Agents | 4 mentioned | **12 total** | 8 missed |
| Contexts | 1 mentioned | **3 total** | 2 missed |
| Rules | 0 mentioned | **8 total** | 8 missed |
| Hooks | 2 mentioned | **14 total** | 12 missed |

---

## HIGH PRIORITY: Commands We Should Add

### 1. `/verify` - Comprehensive Verification
**Source**: `commands/verify.md:1-59`

Pre-commit/pre-PR verification with 6-phase check:
1. Build check
2. Type check
3. Lint check
4. Test suite (with coverage %)
5. Console.log audit
6. Git status

**Why we need it**: Our `/vcode` does spec compliance + code quality but doesn't have this structured verification pipeline. `/verify` would complement `/vcode` as a quick sanity check.

**Arguments**: `quick`, `full`, `pre-commit`, `pre-pr`

### 2. `/plan` - Planning with Confirmation Gate
**Source**: `commands/plan.md:1-113`

Invokes planner agent to:
1. Restate requirements
2. Identify risks
3. Create step-by-step plan
4. **WAIT for user CONFIRM before touching code**

**Why we need it**: Our `/pcode` creates plans but doesn't have the explicit confirmation gate. This pattern prevents wasted implementation.

**Iron Law**: "The planner agent will NOT write any code until you explicitly confirm"

### 3. `/tdd` - Test-Driven Development Enforcement
**Source**: `commands/tdd.md:1-326`

Invokes tdd-guide agent to enforce:
- RED → GREEN → REFACTOR cycle
- 80%+ test coverage
- Tests written BEFORE implementation

**Why we need it**: We don't have explicit TDD enforcement. Our `/icode` could integrate this pattern.

**Iron Law**: "Never skip the RED phase. Never write code before tests."

### 4. `/code-review` - Security and Quality Review
**Source**: `commands/code-review.md:1-40`

Reviews uncommitted changes for:
- **CRITICAL**: Hardcoded secrets, SQL injection, XSS, missing validation
- **HIGH**: Functions >50 lines, files >800 lines, nesting >4, missing error handling
- **MEDIUM**: Mutation patterns, emojis, missing tests

**Why we need it**: Automated quality gate before commits. Could integrate with our `/commit` skill.

**Iron Law**: "Never approve code with security vulnerabilities!"

### 5. `/e2e` - End-to-End Testing
**Source**: `commands/e2e.md:1-340`

Playwright-based E2E testing with:
- Page Object Model pattern
- Multi-browser support (Chrome, Firefox, Safari)
- Artifact capture (screenshots, videos, traces)
- Flaky test detection

**Why we need it**: We have no E2E testing workflow.

### 6. `/eval` - Eval-Driven Development
**Source**: `commands/eval.md:1-120`

Manages evaluation framework:
- `define <name>` - Create eval definition
- `check <name>` - Run evals
- `report <name>` - Generate report with pass@k metrics

**Why we need it**: Formal success metrics beyond "tests pass".

### 7. `/build-fix` - Incremental Error Resolution
**Source**: `commands/build-fix.md:1-29`

Fixes TypeScript/build errors one at a time:
1. Run build
2. Parse first error
3. Show context, explain, fix
4. Re-run build
5. Repeat until green

**Why we need it**: Our `/icode` doesn't have incremental error recovery.

**Key Rule**: "Fix one error at a time for safety!"

### 8. `/refactor-clean` - Dead Code Removal
**Source**: `commands/refactor-clean.md:1-28`

Safe dead code removal:
1. Run analysis tools (knip, depcheck, ts-prune)
2. Categorize by safety (SAFE/CAUTION/DANGER)
3. Delete with test verification at each step
4. Rollback if tests fail

**Iron Law**: "Never delete code without running tests first!"

### 9. `/test-coverage` - Coverage Analysis and Generation
**Source**: `commands/test-coverage.md:1-28`

Analyzes coverage and generates missing tests:
1. Run tests with coverage
2. Find files below 80%
3. Generate unit/integration/E2E tests
4. Verify new tests pass
5. Show before/after metrics

---

## HIGH PRIORITY: Agents We Should Add

### 1. `planner` Agent
**Source**: `agents/planner.md:1-120`
**Tools**: Read, Grep, Glob
**Model**: Opus

Expert planning specialist that:
- Analyzes requirements
- Breaks down into phases
- Identifies dependencies and risks
- Creates detailed implementation plans

**Red Flags Checklist** (`planner.md:110-117`):
- Large functions (>50 lines)
- Deep nesting (>4 levels)
- Duplicated code
- Missing error handling
- Missing tests

### 2. `architect` Agent
**Source**: `agents/architect.md:1-17`
**Tools**: Read, Grep, Glob
**Model**: Opus

System architecture specialist for:
- Technical trade-off evaluation
- Pattern recommendations
- Scalability analysis
- Future growth planning

### 3. `code-reviewer` Agent
**Source**: `agents/code-reviewer.md:1-32`
**Tools**: Read, Grep, Glob, Bash
**Model**: Opus

Proactive code review for:
- Quality and simplicity
- Security vulnerabilities
- Input validation
- Test coverage
- Performance (time complexity)

### 4. `security-reviewer` Agent
**Source**: `agents/security-reviewer.md:1-19`
**Tools**: Read, Write, Edit, Bash, Grep, Glob
**Model**: Opus

Security specialist for:
- OWASP Top 10
- Hardcoded secrets
- Injection attacks
- Auth/authz verification
- Vulnerable dependencies

### 5. `tdd-guide` Agent
**Source**: `agents/tdd-guide.md:1-281`
**Tools**: Read, Write, Edit, Bash, Grep
**Model**: Opus

TDD enforcement with:
- RED-GREEN-REFACTOR cycle
- 80%+ coverage enforcement
- Unit/Integration/E2E guidance
- Test smell detection

### 6. `build-error-resolver` Agent
**Source**: `agents/build-error-resolver.md:1-19`
**Tools**: Read, Write, Edit, Bash, Grep, Glob
**Model**: Opus

Build error resolution with minimal diffs.

### 7. `refactor-cleaner` Agent
**Source**: `agents/refactor-cleaner.md:1-18`
**Tools**: Read, Write, Edit, Bash, Grep, Glob
**Model**: Opus

Dead code cleanup with safety tracking.

### 8. `e2e-runner` Agent
**Source**: `agents/e2e-runner.md:1-110`
**Tools**: Read, Write, Edit, Bash, Grep, Glob
**Model**: Opus

Playwright E2E testing specialist.

---

## MEDIUM PRIORITY: Contexts (Mode Switching)

### 1. `dev` Context
**Source**: `contexts/dev.md:1-21`

```markdown
Mode: Active development
Focus: Implementation, coding, building features

Behavior:
- Write code first, explain after
- Prefer working solutions over perfect solutions
- Run tests after changes

Priorities:
1. Get it working
2. Get it right
3. Get it clean
```

### 2. `research` Context
**Source**: `contexts/research.md:1-26`

```markdown
Mode: Exploration, investigation, learning
Focus: Understanding before acting

Behavior:
- Read widely before concluding
- Ask clarifying questions
- Document findings as you go
- Don't write code until understanding is clear

Process:
1. Understand the question
2. Explore relevant code/docs
3. Form hypothesis
4. Verify with evidence
5. Summarize findings
```

### 3. `review` Context
**Source**: `contexts/review.md:1-22`

```markdown
Mode: PR review, code analysis
Focus: Quality, security, maintainability

Behavior:
- Read thoroughly before commenting
- Prioritize by severity (critical > high > medium > low)
- Suggest fixes, don't just point out problems
- Check for security vulnerabilities

Checklist:
- Logic errors, edge cases, error handling
- Security (injection, auth, secrets)
- Performance, readability, test coverage
```

**Why contexts matter**: They provide instant mode switching. Our skills have Iron Laws for enforcement, but contexts are lighter-weight behavioral nudges.

---

## MEDIUM PRIORITY: Rules We Should Add

### 1. `agents.md` - Agent Orchestration Guidelines
**Source**: `rules/agents.md:1-49`

- When to use which agent
- Parallel execution patterns
- Multi-perspective analysis (split role sub-agents)

### 2. `coding-style.md` - Code Quality Standards
**Source**: `rules/coding-style.md:1-71`

- **Immutability rule**: Always create new objects, never mutate
- File organization: 200-400 lines typical, 800 max
- Error handling templates
- Input validation with Zod
- Quality checklist (11 items)

### 3. `git-workflow.md` - Git Standards
**Source**: `rules/git-workflow.md:1-45`

- Commit format: `<type>: <description>`
- PR workflow with 5 steps
- Feature implementation workflow

### 4. `performance.md` - Model Selection
**Source**: `rules/performance.md:1-47`

Model selection strategy:
| Model | Use For |
|-------|---------|
| Haiku 4.5 | Lightweight agents, code generation (90% capability, 3x savings) |
| Sonnet 4.5 | Main development work, orchestration |
| Opus 4.5 | Complex architectural decisions |

### 5. `security.md` - Security Standards
**Source**: `rules/security.md:1-36`

- Mandatory security checks
- Secret management
- Security response protocol

### 6. `testing.md` - Testing Requirements
**Source**: `rules/testing.md:1-30`

- 80% minimum coverage
- TDD workflow (RED-GREEN-IMPROVE)
- Agent support mapping

---

## MEDIUM PRIORITY: Hook Patterns

### Session Lifecycle Hooks

**SessionStart** (`hooks/hooks.json:68-79`):
- Load previous context
- Detect package manager
- Show recent sessions

**SessionEnd** (`hooks/hooks.json:146-167`):
- Persist session state
- Evaluate session for patterns (continuous learning)

**PreCompact** (`hooks/hooks.json:56-67`):
- Save state before context compaction
- Log compaction timestamp

### Quality Enforcement Hooks

**TypeScript Checker** (`hooks/hooks.json:113-122`):
- PostToolUse on `.ts`/`.tsx` Edit
- Runs `tsc --noEmit`
- Shows type errors for edited file

**Console.log Warning** (`hooks/hooks.json:123-132`):
- PostToolUse on JS/TS Edit
- Scans for console.log statements
- Warns about debug statements

**Prettier Auto-Format** (`hooks/hooks.json:103-112`):
- PostToolUse on `.ts`/`.tsx`/`.js`/`.jsx` Edit
- Runs `npx prettier --write`
- Auto-formats code

### Safety Hooks

**Git Push Review** (`hooks/hooks.json:25-34`):
- PreToolUse on `git push`
- Logs reminder to review changes

**Doc File Blocker** (`hooks/hooks.json:35-44`):
- PreToolUse on Write for `.md`/`.txt`
- Blocks random doc creation
- Allows README, CLAUDE, AGENTS, CONTRIBUTING

**Suggest Compact** (`hooks/hooks.json:45-54`):
- PreToolUse on Edit/Write
- Tracks tool call count per session
- Suggests compaction at 50 calls, then every 25

---

## LOWER PRIORITY: Advanced Skills

### 1. `eval-harness` - Formal Evaluation Framework
**Source**: `skills/eval-harness/SKILL.md:1-186`

- Capability evals (test new functionality)
- Regression evals (ensure no breakage)
- Code-based graders (deterministic checks)
- Model-based graders (Claude evaluates outputs)
- pass@k and pass^k metrics

### 2. `iterative-retrieval` - Smarter Context Retrieval
**Source**: `skills/iterative-retrieval/SKILL.md:1-203`

4-phase loop for subagent context:
1. DISPATCH (broad search)
2. EVALUATE (score relevance 0-1)
3. REFINE (update keywords)
4. LOOP (max 3 cycles)

**Key insight** (`iterative-retrieval/SKILL.md:17-19`):
> Standard approaches fail:
> - Send everything: Exceeds context limits
> - Send nothing: Agent lacks critical information
> - Guess what's needed: Often wrong

### 3. `continuous-learning-v2` - Instinct Architecture
**Source**: `skills/continuous-learning-v2/SKILL.md:1-258`

Atomic learned behaviors with confidence scoring:
- Triggers via PreToolUse/PostToolUse hooks
- Background observer (Haiku model)
- Confidence 0.3-0.9 based on observation frequency
- Evolution path: instincts → skills/commands/agents

### 4. `verification-loop` - 6-Phase Quality Gates
**Source**: `skills/verification-loop/SKILL.md:1-121`

1. Build check
2. Type check
3. Lint check
4. Test suite (80% coverage)
5. Security scan
6. Diff review

### 5. `strategic-compact` - Context Management
**Source**: `skills/strategic-compact/SKILL.md:1-58`

- Tracks tool calls per session
- Suggests compaction at logical boundaries
- Default threshold: 50 calls

---

## LOWER PRIORITY: Instinct Commands

### `/instinct-status`
**Source**: `commands/instinct-status.md:1-79`

Shows all learned instincts grouped by domain with confidence bars.

### `/instinct-export`
**Source**: `commands/instinct-export.md:1-91`

Exports instincts for sharing (strips sensitive info).

### `/instinct-import`
**Source**: `commands/instinct-import.md:1-120`

Imports instincts from teammates or other sources.

### `/evolve`
**Source**: `commands/evolve.md:1-130`

Clusters related instincts into skills/commands/agents.

---

## LOWER PRIORITY: Language-Specific Commands

### Go Commands
- `/go-build` - Fix Go build errors (`commands/go-build.md`)
- `/go-review` - Go code review (`commands/go-review.md`)
- `/go-test` - Go TDD workflow (`commands/go-test.md`)

### Go Agents
- `go-build-resolver` - Build error resolution (`agents/go-build-resolver.md`)
- `go-reviewer` - Go-specific code review (`agents/go-reviewer.md`)

---

## Documentation and Maintenance Commands

### `/update-codemaps`
**Source**: `commands/update-codemaps.md:1-17`

Generates architecture documentation:
- `codemaps/architecture.md`
- `codemaps/backend.md`
- `codemaps/frontend.md`
- `codemaps/data.md`

### `/update-docs`
**Source**: `commands/update-docs.md:1-31`

Syncs documentation from source-of-truth:
- Reads package.json scripts
- Reads .env.example
- Generates docs/CONTRIB.md and docs/RUNBOOK.md

---

## Recommended Enhancement Priorities

### Tier 1: Essential (Add First)
| Item | Type | Why |
|------|------|-----|
| `/verify` | Command | Quick pre-commit sanity check |
| `/plan` | Command | Confirmation gate before implementation |
| `/tdd` | Command | TDD enforcement |
| `planner` | Agent | Better planning than our current approach |
| `code-reviewer` | Agent | Automated quality review |

### Tier 2: High Value (Add Soon)
| Item | Type | Why |
|------|------|-----|
| `/code-review` | Command | Security/quality gate for `/commit` |
| `/build-fix` | Command | Incremental error recovery |
| `dev` context | Context | Mode switching for implementation |
| `research` context | Context | Mode switching for exploration |
| `security-reviewer` | Agent | Security-focused review |

### Tier 3: Good to Have
| Item | Type | Why |
|------|------|-----|
| `/e2e` | Command | E2E testing workflow |
| `/refactor-clean` | Command | Dead code removal |
| `/test-coverage` | Command | Coverage analysis |
| `tdd-guide` | Agent | TDD enforcement |
| Rules files | Rules | Codified standards |

### Tier 4: Advanced (Consider Later)
| Item | Type | Why |
|------|------|-----|
| `/eval` | Command | Formal evaluation metrics |
| Hooks | Hooks | Session lifecycle management |
| `iterative-retrieval` | Skill | Smarter agent context |
| `continuous-learning-v2` | Skill | Instinct-based learning |
| `/orchestrate` | Command | Agent pipelines |

---

## Integration with Our RPI Workflow

```
Current:  /rcode → /pcode → /icode → /vcode → /commit

Enhanced: /rcode → /plan → /pcode → /icode → /verify → /vcode → /code-review → /commit

Where:
- /plan adds confirmation gate after research
- /verify adds quick sanity check after implementation
- /code-review adds security/quality gate before commit
```

---

## Open Questions

1. Should we adopt the contexts pattern or continue with Iron Laws in skills?
2. Should hooks be implemented for session lifecycle or is that overkill?
3. Should `/verify` be standalone or integrated into `/vcode`?
4. Should `/code-review` be integrated into `/commit` or standalone?
5. How do we handle Go-specific commands if we don't always work in Go?

---

## Code References

- `C:/code/everything-claude-code/commands/verify.md:7-33` - Verification phases
- `C:/code/everything-claude-code/commands/plan.md:28-35` - Planner process
- `C:/code/everything-claude-code/commands/tdd.md:39-47` - TDD cycle
- `C:/code/everything-claude-code/agents/planner.md:110-117` - Red flags checklist
- `C:/code/everything-claude-code/agents/code-reviewer.md:8-32` - Review categories
- `C:/code/everything-claude-code/contexts/dev.md:7-20` - Dev mode definition
- `C:/code/everything-claude-code/rules/coding-style.md:3-20` - Immutability rule
- `C:/code/everything-claude-code/hooks/hooks.json:113-122` - TypeScript checker hook
