# Extraction Workflow

The 6-step process for turning session knowledge into reusable skill files.

## Step 1: Check Existing Skills (Dedup-First)

Before creating anything, search for overlap. This prevents skill sprawl and duplicate knowledge.

**Search locations:**
- `.claude/skills/` (project-level)
- `~/.claude/skills/` (user-level)

**Search method:**
```sh
# Find all skill files
rg --files -g 'SKILL.md' .claude/skills ~/.claude/skills 2>/dev/null

# Search by keywords from the discovery
rg -i "keyword1|keyword2|keyword3" .claude/skills ~/.claude/skills 2>/dev/null
```

**Decision matrix:**

| What You Find | Action |
|---------------|--------|
| Nothing related | Create new skill |
| Same trigger, same fix | Update existing skill (add detail, fix errors) |
| Same trigger, different root cause | Create new skill + add `See also:` cross-link |
| Partial overlap | Add variant subsection to existing skill |
| Same domain, different problem | Create new skill + add `See also:` link |
| Stale or incorrect | Archive old skill, create replacement |

**Cross-linking format:**
```markdown
## See Also
- `~/.claude/skills/related-skill/SKILL.md` - Handles [related scenario]
```

## Step 2: Identify the Knowledge

Run these four analysis questions against the session discovery:

1. **What was the problem?** -- Describe the symptom, not the fix. Include exact error messages, unexpected behaviors, or misleading indicators.

2. **What was non-obvious?** -- What made this harder than expected? Misleading error messages? Undocumented behavior? Version-specific quirks? This is the core value of the skill.

3. **What would help next time?** -- If you hit this problem again tomorrow, what shortcut would save time? This becomes the Solution section.

4. **What are the exact trigger conditions?** -- When does this problem appear? Specific framework versions, configurations, environments, or sequences of events. This becomes the description and the Context/Trigger Conditions section.

If any of these questions yields a weak answer ("it was just a typo", "the docs covered this"), the discovery may not be worth extracting. See quality-gates.md for the worth-assessment criteria.

## Step 3: Research Best Practices

Web search adds external validation and catches stale knowledge.

**When to search:**
- The discovery involves a specific technology, framework, or library
- The error message is technology-specific
- The solution involves configuration or version-dependent behavior

**When to skip:**
- Project-internal patterns (custom architecture, team conventions)
- Context-specific solutions (this exact codebase only)
- Stable generic concepts (data structures, algorithms, design patterns)
- The fix is already well-documented in official docs (link to docs instead)

**Search patterns:**
```
"[technology] [problem keyword] best practices 2026"
"[technology] [exact error message]"
"[framework] [version] [behavior] changelog"
```

**What to do with results:**
- If web results confirm the solution: add a References section with URLs
- If web results show a better approach: update the solution, note the improvement
- If web results show the problem is version-specific: add version constraints to trigger conditions
- If web results contradict the solution: investigate before saving -- don't extract unverified knowledge

## Step 4: Structure the Skill

Use the template at `../templates/extracted-skill-template.md` for consistent formatting.

**Key structuring decisions:**

*Frontmatter description:*
Write the description BEFORE the body. The description is the retrieval key -- it determines whether this skill will be found in future sessions. See description-optimization.md for writing effective descriptions.

*Scope decision:*
- **Project-level** (`.claude/skills/`): Problem is specific to this codebase, framework combination, or team workflow
- **User-level** (`~/.claude/skills/`): Problem applies across multiple projects, involves general technology patterns

*Section depth:*
- Problem: 2-4 sentences. Emphasize the misleading aspect.
- Context/Trigger: Exact error strings, framework versions, environment conditions.
- Solution: Numbered steps with code blocks. Each step should be independently verifiable.
- Verification: How to confirm the fix worked. Include test commands or expected output.
- Example: Before/after code or before/after behavior.
- Notes: Edge cases, related issues, version constraints.
- References: URLs from Step 3, related docs, related skills.

## Step 5: Apply Quality Gates

Run every item in quality-gates.md before saving. No exceptions.

## Step 6: Save and Confirm

1. Write the skill file to the chosen location
2. Confirm to the user:

```
Skill extracted: [name]
Location: [path]
Trigger: [first line of description]
Sections: [list]
Quality gates: All passed

This skill will activate in future sessions when similar problems arise.
```
