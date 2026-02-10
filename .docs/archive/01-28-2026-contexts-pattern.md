---
git_commit: 8e92bba
last_updated: 2026-02-09
last_updated_by: docs-updater
last_updated_note: "Archived - completed external research, pattern evaluated but not adopted (low priority), 56 commits behind HEAD with no local references"
topic: "Contexts - Mode Switching via CLI"
tags: [research, contexts, modes, cli]
status: archived
archived: 2026-02-09
archive_reason: "Completed research with external-only references. Pattern was evaluated but recommendation was 'low priority' and was never implemented. Skills already enforce behavior via Iron Laws, making contexts redundant."
references:
  - C:/code/everything-claude-code/contexts/dev.md
  - C:/code/everything-claude-code/contexts/research.md
  - C:/code/everything-claude-code/contexts/review.md
  - C:/code/everything-claude-code/the-longform-guide.md
---

# Research: Contexts Pattern

**Date**: 2026-01-28
**Source**: everything-claude-code

## Summary

Contexts are short markdown files that inject mode-specific behavior via CLI flags. Instead of loading all configuration every session, contexts enable surgical injection for different work modes (development, research, review).

## Available Contexts

### Development (`contexts/dev.md:1-21`)

```markdown
Mode: Active development
Focus: Implementation, coding, building features

## Behavior
- Write code first, explain after
- Prefer working solutions over perfect solutions
- Run tests after changes
- Keep commits atomic

## Priorities
1. Get it working
2. Get it right
3. Get it clean

## Tools to favor
- Edit, Write for code changes
- Bash for running tests/builds
- Grep, Glob for finding code
```

### Research (`contexts/research.md:1-27`)

```markdown
Mode: Exploration, investigation, learning
Focus: Understanding before acting

## Behavior
- Read widely before concluding
- Ask clarifying questions
- Document findings as you go
- Don't write code until understanding is clear

## Tools to favor
- Read, Grep, Glob, WebSearch, WebFetch
- Task with Explore agent

## Output Format
Findings first, recommendations second
```

### Review (`contexts/review.md:1-23`)

```markdown
Mode: PR review, code analysis
Focus: Quality, security, maintainability

## Behavior
- Read thoroughly before commenting
- Prioritize issues by severity
- Suggest fixes, don't just point out problems
- Check for security vulnerabilities

## Review Checklist
- Logic errors, edge cases
- Error handling, security
- Performance, readability
- Test coverage

## Output Format
Group findings by file, severity first
```

## Activation Mechanism

Via CLI flags using shell aliases (`the-longform-guide.md:66-75`):

```bash
# Add to .bashrc or .zshrc
alias claude-dev='claude --system-prompt "$(cat ~/.claude/contexts/dev.md)"'
alias claude-review='claude --system-prompt "$(cat ~/.claude/contexts/review.md)"'
alias claude-research='claude --system-prompt "$(cat ~/.claude/contexts/research.md)"'
```

**Authority hierarchy** (`the-longform-guide.md:62`):
- System prompt (highest) > User messages > Tool results

## Limitations

- **Single context per session** - Cannot combine multiple contexts
- **No dynamic switching** - Must restart Claude to change context
- **Not plugin-distributed** - Manual installation required
- **Session-scoped** - Active for entire session duration

## Adaptation for Commandbase

### RPI Phase Contexts

Create contexts aligned with RPI workflow:

**research.md** (for /rcode):
```markdown
Mode: Codebase research
Focus: Understanding before synthesis

## Behavior
- Spawn agents before answering
- Every claim needs file:line reference
- Document, don't evaluate

## Tools to favor
- Task with code-locator, code-analyzer
- Grep, Glob, Read
```

**plan.md** (for /pcode):
```markdown
Mode: Implementation planning
Focus: Research before planning

## Behavior
- Read existing code before proposing changes
- Consider multiple approaches
- Get user confirmation before finalizing

## Tools to favor
- Task with code-librarian
- Read for understanding existing code
```

**implement.md** (for /icode):
```markdown
Mode: Plan execution
Focus: Follow plan exactly, verify each phase

## Behavior
- Fresh verification before claiming done
- Show evidence (exit codes, pass counts)
- Don't skip phases

## Tools to favor
- Edit, Write for code changes
- Bash for verification commands
```

**validate.md** (for /vcode):
```markdown
Mode: Implementation validation
Focus: Stage 1 (spec) before Stage 2 (quality)

## Behavior
- Read plan FULLY first
- Compare line-by-line to implementation
- Independent verification (don't trust icode)

## Tools to favor
- Read for plan and code comparison
- Bash for fresh verification
```

### Trade-offs

**Pros**:
- Clear mode separation
- Reduces conflicting instructions
- Surgical context loading

**Cons**:
- Requires shell aliases (not pure Claude Code)
- Cannot switch mid-session
- Skills already enforce behavior via Iron Laws

### Recommendation

**Low priority** - Our skills already have strong enforcement patterns (Iron Law, Gate Function). Contexts would be redundant unless we find skills aren't being followed.

## Code References

- dev.md: `C:/code/everything-claude-code/contexts/dev.md:1-21`
- research.md: `C:/code/everything-claude-code/contexts/research.md:1-27`
- review.md: `C:/code/everything-claude-code/contexts/review.md:1-23`
- Activation: `C:/code/everything-claude-code/the-longform-guide.md:54-75`
