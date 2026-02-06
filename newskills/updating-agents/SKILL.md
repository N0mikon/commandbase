---
name: updating-agents
description: "Use this skill when auditing existing agents for validation issues, updating agents to fix compliance problems, or checking agent health after specification changes. This includes running validation checks against all agents, fixing frontmatter issues, correcting noun-form naming violations, rewriting descriptions to follow the delegation trigger formula, validating tool sets and model selections, and checking system prompt Contract Format compliance."
---

# Updating Agents

You are systematically auditing and updating existing agents to ensure they follow the agent specification and Contract Format conventions. This skill activates when checking agent health or fixing compliance issues and produces audit reports or updated agent files.

**Violating the letter of these rules is violating the spirit of these rules.**

## The Iron Law

```
NO UPDATE WITHOUT SHOWING THE DIFF FIRST
```

Every change must be shown as a before/after diff and approved before applying. Batch updates are prohibited - one agent at a time.

**No exceptions:**
- Don't auto-fix without showing the proposed change
- Don't update multiple agents in one operation
- Don't skip user approval for any fix
- Don't assume the audit is correct - verify findings against actual content

## The Gate Function

```
BEFORE updating any agent:

1. IDENTIFY: Mode (audit vs update) and target (single agent or "all")
2. VERIFY: Target agent(s) exist in ~/.claude/agents/
3. READ: Full agent .md file (no offset/limit)
4. AUDIT: Run all 6 check categories
5. REPORT: Show findings with specific line references
6. If update mode: PROPOSE fixes one at a time with diffs
7. ONLY THEN: Apply approved changes

Skip verification = breaking a working agent
```

## Mode Detection

Parse the user's request to determine mode:

| Input | Mode | Target |
|-------|------|--------|
| `/updating-agents audit agent-name` | Audit | Single agent |
| `/updating-agents audit all` | Audit | All agents |
| `/updating-agents update agent-name` | Update | Single agent |
| `/updating-agents agent-name` | Audit | Single agent (default) |

**No batch update mode.** To update multiple agents, run update on each individually.

## Mode A: Audit

Read-only analysis of agent(s) against validation rules.

**Single Agent Audit:**
1. Read `~/.claude/agents/[agent-name].md` completely
2. Run all 6 audit categories (see Audit Categories below)
3. Produce audit report showing findings
4. No changes made

**All Agents Audit:**
1. List all `.md` files in `~/.claude/agents/`
2. Run audit on each agent
3. Produce summary table:

```
AGENT AUDIT SUMMARY
====================
| Agent                    | Issues |
|--------------------------|--------|
| codebase-analyzer        | 0 OK   |
| codebase-locator         | 0 OK   |
| docs-updater             | 1 WARN |
| ...                      | ...    |

Total: X agents, Y with issues
Run `/updating-agents update [agent-name]` to fix specific agents.
```

## Mode B: Update

Interactive fix workflow for a single agent.

**Process:**
1. Run audit first (same as Mode A)
2. If no issues: "Agent passes all validation checks."
3. If issues found, for each issue:
   - Show the finding with line reference
   - Propose the fix
   - Show before/after diff
   - Ask for approval
   - Apply if approved, skip if declined
   - Re-validate after fix
4. Repeat until all issues resolved or user stops

**User approval is required for every change.** Never auto-apply.

**Only fix what the audit found.** If you notice something that could be "improved" but wasn't flagged by the 6 audit categories, do not propose it. The checklist is the scope. Unsolicited improvements - rewriting prose, reorganizing sections, tightening wording - are out of scope even if they would genuinely help.

## Audit Categories

Six categories, checked in order. See `./reference/audit-checklist.md` for full details.

### 1. Frontmatter Validation

- Starts with `---`, ends with `---`
- Valid YAML dictionary
- Only allowed properties: `name`, `description`, `tools`, `disallowedTools`, `model`, `permissionMode`, `skills`, `hooks`, `memory`
- Required: `name`, `description`
- Unknown properties flagged (may indicate typo)

### 2. Name Validation

- Matches `^[a-z0-9-]+$`
- No leading/trailing/consecutive hyphens
- Max 64 characters
- Matches filename minus `.md`
- Uses noun/role form (not gerund - flag `-ing` suffix on verb component)
- No vague suffixes (`-helper`, `-handler`, `-manager`)

### 3. Description Validation

- Non-empty string, max 1024 characters
- No angle brackets (`<` or `>`)
- Not first person ("I help", "I am", "My purpose")
- Contains delegation trigger (when the orchestrator should delegate)
- Does NOT start with "Use this skill when..." (that's skill-style)
- Distinguishable from other agents' descriptions

### 4. Tool Set Validation

- `tools` and `disallowedTools` not both present
- If `tools` specified: all names are valid tool names
- Tool set matches agent's stated purpose
- State-modifying tools (Edit, Write, Bash, NotebookEdit) have guardrails in system prompt
- No unnecessary tools: WebSearch on non-web agent, Bash used only for grep-like tasks
- If neither `tools` nor `disallowedTools`: flag as inheriting all tools (intentional?)

### 5. Model & Permission Validation

- `model` is valid value (`sonnet`, `opus`, `haiku`) or absent
- Model matches task complexity: `haiku` for fast/simple, `sonnet` for standard, `opus` for complex reasoning or state modification
- `permissionMode` is valid value (`default`, `acceptEdits`, `dontAsk`, `bypassPermissions`, `plan`) or absent
- `bypassPermissions` flagged for explicit review

### 6. System Prompt Compliance

- Uses "You are..." role statement in first paragraph (not "I am...")
- Has identifiable Core Responsibilities (3-5 items)
- Has Strategy/Process section with workflow steps
- Has Output Format section with example or template
- Has "What NOT to Do" or equivalent enforcement section
- Has meta-reminder or closing identity reinforcement
- Total file under 300 lines (target 80-200)
- No placeholder text or TODOs

## Audit Report Format

**One line per check. No prose, no explanations, no commentary.** The report is a checklist, not an essay.

For each agent audited:

```
AUDIT: [agent-name]
====================

Frontmatter:
  OK Valid YAML
  OK Required fields present
  WARN Unknown property: `color`

Name:
  OK Matches filename
  OK Noun/role form
  WARN Vague suffix: `-handler`

Description:
  OK Under 1024 chars (current: 287)
  WARN Uses skill-style opener "Use this skill when..."

Tool Set:
  OK tools field present
  OK No mutual exclusivity conflict
  WARN Edit tool present but no guardrails in system prompt

Model & Permission:
  OK Model: sonnet (appropriate for analyzer role)
  OK No permissionMode set (default)

System Prompt:
  OK Has role statement
  OK Has Core Responsibilities
  WARN Missing "What NOT to Do" section
  OK Under 300 lines (current: 156)

Summary: 4 issues found (0 ERROR, 4 WARN)
```

**Do NOT** add narrative analysis, improvement suggestions, or commentary beyond the check results. The audit report is a structured checklist, not a review.

## Common Fixes

See `./reference/common-fixes.md` for detailed fix patterns. Key fixes:

| Issue | Fix Approach |
|-------|--------------|
| Missing name field | Add `name: [filename-minus-md]` to frontmatter |
| Name uses gerund form | Propose noun/role rename (e.g. `reviewing-code` -> `code-reviewer`) |
| Skill-style description | Rewrite using delegation trigger formula |
| First-person description | Rewrite in third person with capability + trigger |
| `tools` and `disallowedTools` both present | Remove one based on intent (prefer `tools` allowlist) |
| State-modifying tool without guardrails | Add "What NOT to Do" section with specific restrictions |
| Missing "What NOT to Do" section | Add enforcement section customized to agent's role |
| Over 300 lines | Identify content to condense; agents cannot use reference files |
| Missing role statement | Add "You are..." opening paragraph |

## Sibling Skill: /updating-skills

`/updating-agents` and `/updating-skills` are siblings for different targets:

| Aspect | /updating-agents (this skill) | /updating-skills |
|--------|-------------------------------|-----------------|
| Target | `~/.claude/agents/*.md` | `~/.claude/skills/*/SKILL.md` |
| Naming convention | Noun/role form | Gerund form |
| Description style | Delegation trigger | "Use this skill when..." |
| Structure checks | Single file, under 300 lines | Directory with SKILL.md, under 500 lines |
| Unique checks | Tool set, model, permission, Contract Format | Directory structure, reference nesting, pattern compliance |

If the user wants to audit **skills**, redirect to `/updating-skills`.

## Red Flags - STOP and Verify

If you notice any of these, pause:

- Applying a fix without showing the diff first
- Updating multiple agents in a single operation
- Proceeding after user declines a fix without asking what to do
- Assuming a finding is correct without checking the actual content
- Skipping re-validation after applying a fix
- Judging an agent's system prompt quality beyond the checklist (stick to objective checks)
- Making improvements the audit didn't find (rewriting prose, reorganizing sections, "while we're here" cleanups)
- Writing multi-paragraph explanations in the audit report instead of one-line check results

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "This fix is obvious, no need to show diff" | Show every diff. User context matters. |
| "I'll batch these small fixes together" | One fix at a time. Each needs approval. |
| "The audit said it's wrong, so it's wrong" | Verify against actual content. Audits can have false positives. |
| "User approved the first fix, they'll approve the rest" | Each fix needs explicit approval. |
| "Re-validation is slow, I'll skip it" | Re-validate after every fix. Catches regressions. |
| "The system prompt could be better" | Only check against the checklist. Don't critique style or content beyond spec. |
| "While I'm fixing this, I should also improve..." | Fix only what the audit found. File separate findings for other issues. |
| "The audit report needs more context" | One line per check. Users can ask for detail on specific findings. |

## The Bottom Line

**No update without showing the diff first.**

Audit thoroughly. Fix one at a time. Get approval for every change. Re-validate after every fix. This is non-negotiable. Every agent update. Every time.
