# Skills Ecosystem Review

Date: 2026-02-02
Scope: All 18 skills in ~/.claude/skills/

## Research Method

Launched 5 parallel research agents to analyze different dimensions:
1. RPI workflow coverage
2. Session lifecycle skills
3. Quality/safety gate skills
4. Skill interconnections
5. Decision-support skills

## Skills Inventory

| Skill | Category | Trigger Type |
|-------|----------|--------------|
| researching-codebases | RPI - Research | User-invoked |
| planning-codebases | RPI - Plan | User-invoked |
| implementing-plans | RPI - Implement | User-invoked |
| validating-implementations | RPI - Validate | User-invoked |
| checkpointing | Quality Gate | User-invoked |
| committing-changes | Git Operations | User-invoked |
| creating-pull-requests | Git Operations | User-invoked |
| reviewing-security | Safety Gate | Auto + User-invoked |
| discussing-features | Decision Support | User-invoked |
| debating-options | Decision Support | User-invoked |
| debugging-codebases | Recovery | User-invoked |
| learning-from-sessions | Knowledge Capture | User-invoked |
| creating-skills | Meta | User-invoked |
| starting-projects | Session Lifecycle | User-invoked |
| handing-over | Session Lifecycle | User-invoked |
| taking-over | Session Lifecycle | User-invoked |
| updating-claude-md | Maintenance | User-invoked |

## Workflow Coverage Analysis

### RPI Workflow: Strong Coverage

```
Research ─────► Plan ─────► Implement ─────► Validate
    │             │             │               │
    ▼             ▼             ▼               ▼
/researching  /planning    /implementing   /validating
-codebases    -codebases   -plans          -implementations
```

All four RPI phases have dedicated skills with:
- Iron Laws enforcing discipline
- Clear entry/exit conditions
- Checkpoint integration points

### Session Lifecycle: Strong Coverage

```
Start Session                    End Session
     │                               │
     ▼                               ▼
/starting-projects ◄──────► /handing-over
     │                               ▲
     │                               │
     └──► /taking-over ──────────────┘
              │
              ▼
         (resume work)
```

Gap identified: No cold-start orientation skill when there's no handover to take over.

### Quality Gates: Moderate Coverage

| Gate Type | Skill | Trigger | Enforced |
|-----------|-------|---------|----------|
| Secret Detection | reviewing-security | Auto on public commit | Yes (BLOCK) |
| Injection Vulns | reviewing-security | Auto on public commit | Yes (BLOCK) |
| Spec Compliance | validating-implementations | Manual | No |
| Code Quality | validating-implementations | Manual | No |
| Phase Verification | implementing-plans | Per-phase | Soft |
| Checkpoints | checkpointing | Manual | No |

Gaps:
- No pre-PR validation gate
- No test coverage gate
- No auto-debug on validation failure
- Private repos skip security review

### Decision Support: Strong at Entry Points

Strong support exists for:
- Multi-option technical choices (debating-options)
- Feature preference gathering (discussing-features)
- Technology stack selection (starting-projects)

Weak support for mid-workflow decisions:
- Implementation deviation handling
- Validation failure response
- WARN verdict risk assessment

## Identified Gaps

### Critical Missing Skills

1. **reviewing-changes** - Pre-PR quality gate
   - Fills gap between /validating-implementations and /creating-pull-requests
   - Would verify: tests pass, validation done, security reviewed
   - Priority: HIGH

2. **orienting-codebases** - Cold-start orientation
   - For when there's no handover document
   - Would analyze: structure, conventions, key files, recent changes
   - Priority: HIGH

3. **recovering-failures** - Auto-debug on failure
   - When validation fails, auto-spawn debug session
   - Create checkpoint before debugging
   - Link debug session to failure context
   - Priority: MEDIUM

4. **checking-status** - "Where are we?" skill
   - Quick status of current work
   - What phase, what's done, what's next
   - Priority: LOW

5. **maintaining-skills** - Skill lifecycle management
   - Update, deprecate, archive skills
   - Track skill usage and effectiveness
   - Priority: LOW

### Missing Quality Gates

| Gate | Description | Impact |
|------|-------------|--------|
| PR Prerequisites | Verify validation before PR | Prevents broken PRs |
| Test Coverage | Require tests for new code | Reduces regressions |
| Private Repo Security | Security review for private repos | Better habits |
| Breaking Change Detection | Flag API contract changes | Protects consumers |
| Dependency Safety | Check dependency updates | Prevents supply chain issues |

### Workflow Gaps

```
                    ┌─────────────────┐
                    │  GAP: No pre-PR │
                    │  quality gate   │
                    └────────┬────────┘
                             │
Research → Plan → Implement → Validate → ??? → Commit → PR
                                  │
                    ┌─────────────┴───────────────┐
                    │  GAP: No auto-debug         │
                    │  on validation failure      │
                    └─────────────────────────────┘
```

## Skill Interconnections

### Strong Connections
- committing-changes → reviewing-security (auto-invokes for public repos)
- implementing-plans → checkpointing (suggests after each phase)
- planning-codebases → checkpointing (suggests after plan approval)
- handing-over ↔ taking-over (complementary pair)

### Weak Connections (Opportunities)
- validating-implementations → debugging-codebases (manual transition on failure)
- validating-implementations → creating-pull-requests (no prerequisite check)
- learning-from-sessions → creating-skills (complexity check could invoke debating-options)

## Recommendations

### Immediate Actions
1. Create `reviewing-changes` skill to fill pre-PR gap
2. Create `orienting-codebases` for cold-start scenarios
3. Add auto-debug spawn to validation failure path

### Future Considerations
- Unify complexity checks across skills into shared pattern
- Add mode selection visibility and override options
- Create decision support for mid-workflow adaptation points

## Agent Outputs

Full detailed outputs from each research agent available at:
- C:\Users\Jason\AppData\Local\Temp\claude\C--code-commandbase\tasks\aea5883.output (RPI workflow)
- C:\Users\Jason\AppData\Local\Temp\claude\C--code-commandbase\tasks\a0e0080.output (Session lifecycle)
- C:\Users\Jason\AppData\Local\Temp\claude\C--code-commandbase\tasks\a6c7ab5.output (Quality gates)
- C:\Users\Jason\AppData\Local\Temp\claude\C--code-commandbase\tasks\ac7bdf8.output (Interconnections)
- C:\Users\Jason\AppData\Local\Temp\claude\C--code-commandbase\tasks\ac85e81.output (Decision support)
