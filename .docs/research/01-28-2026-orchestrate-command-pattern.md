---
git_commit: 448f0d2
last_updated: 2026-02-01
last_updated_by: docs-updater
last_updated_note: "Updated after 8 commits - refreshed skill names to match current conventions"
topic: "/orchestrate Command - Agent Pipelines"
tags: [research, orchestrate, agents, workflow]
status: complete
references:
  - C:/code/everything-claude-code/commands/orchestrate.md
  - C:/code/everything-claude-code/rules/agents.md
---

# Research: /orchestrate Command Pattern

**Date**: 2026-01-28
**Source**: everything-claude-code

## Summary

Chains agents in predefined sequences with structured handoffs. Supports 4 predefined workflows (feature, bugfix, refactor, security) plus custom agent sequences.

## Predefined Workflows (`commands/orchestrate.md:9-33`)

| Workflow | Agent Chain |
|----------|-------------|
| **feature** | planner → tdd-guide → code-reviewer → security-reviewer |
| **bugfix** | explorer → tdd-guide → code-reviewer |
| **refactor** | architect → code-reviewer → tdd-guide |
| **security** | security-reviewer → code-reviewer → architect |

## Execution Pattern (`commands/orchestrate.md:35-43`)

1. **Invoke agent** with context from previous agent
2. **Collect output** as structured handoff document
3. **Pass to next agent** in chain
4. **Aggregate results** into final report

## Handoff Document Format (`commands/orchestrate.md:44-65`)

```markdown
## HANDOFF: [previous-agent] -> [next-agent]

### Context
[Summary of what was done]

### Findings
[Key discoveries or decisions]

### Files Modified
[List of files touched]

### Open Questions
[Unresolved items for next agent]

### Recommendations
[Suggested next steps]
```

## Final Report Format (`commands/orchestrate.md:99-134`)

```
ORCHESTRATION REPORT
====================
Workflow: feature
Task: Add user authentication
Agents: planner -> tdd-guide -> code-reviewer -> security-reviewer

SUMMARY
-------
[One paragraph summary]

AGENT OUTPUTS
-------------
Planner: [summary]
TDD Guide: [summary]
Code Reviewer: [summary]
Security Reviewer: [summary]

FILES CHANGED
-------------
[List all files modified]

TEST RESULTS
------------
[Test pass/fail summary]

SECURITY STATUS
---------------
[Security findings]

RECOMMENDATION
--------------
[SHIP / NEEDS WORK / BLOCKED]
```

## Custom Workflows (`commands/orchestrate.md:160-164`)

```
/orchestrate custom "architect,tdd-guide,code-reviewer" "Redesign caching layer"
```

## Parallel Execution (`commands/orchestrate.md:136-149`)

For independent checks:
```markdown
### Parallel Phase
Run simultaneously:
- code-reviewer (quality)
- security-reviewer (security)
- architect (design)

### Merge Results
Combine outputs into single report
```

## Adaptation for Commandbase

### RPI Workflow Automation

Create `/rpi` command that chains our skills:

```
/rpi feature "Add user authentication"
```

**Skill Chain** (using current skill names):
```
researching-codebases → planning-codebases → implementing-plans → validating-implementations
```

**Handoff Documents**:
- researching-codebases outputs: `.docs/research/MM-DD-YYYY-topic.md`
- planning-codebases outputs: `.docs/plans/MM-DD-YYYY-topic.md`
- implementing-plans outputs: Implementation + phase verification
- validating-implementations outputs: Validation report

### Workflow Types

| Workflow | Chain | Use Case |
|----------|-------|----------|
| **feature** | research → plan → implement → validate | New functionality |
| **bugfix** | research → implement → validate | Bug investigation and fix |
| **refactor** | research → plan → implement → validate | Code restructuring |
| **research** | research only | Understanding codebase |

### Trade-offs

**Pros**:
- Full automation of RPI workflow
- Consistent handoff format
- Aggregated final report

**Cons**:
- Less control at each step
- May skip user confirmation points
- Current manual workflow allows iteration

### Recommendation

**Low priority** - Our manual workflow (researching-codebases → planning-codebases → implementing-plans → validating-implementations) allows user control at each step. Automation is nice-to-have but not essential. Consider after other improvements are stable.

## Code References

- Command definition: `C:/code/everything-claude-code/commands/orchestrate.md:1-173`
- Predefined workflows: `commands/orchestrate.md:9-33`
- Handoff format: `commands/orchestrate.md:44-65`
- Final report: `commands/orchestrate.md:99-134`
- Custom workflows: `commands/orchestrate.md:160-164`
