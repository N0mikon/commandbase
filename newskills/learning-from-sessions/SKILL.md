---
name: learning-from-sessions
description: "Use this skill to extract reusable knowledge from work sessions. This includes reviewing what was learned during debugging, saving non-obvious discoveries or workarounds as skill files, running /learn to capture session learnings, responding to 'save this as a skill' or 'what did we learn', and extracting knowledge after trial-and-error investigation that produced a solution."
---

# Learning from Sessions

You are extracting reusable knowledge from work sessions and saving it as skill files or CLAUDE.md entries. This skill activates when a session produces non-obvious discoveries, debugging breakthroughs, workarounds, or configuration insights worth preserving for future sessions.

**Violating the letter of these rules is violating the spirit of these rules.**

## The Iron Law

```
NO EXTRACTION WITHOUT VERIFICATION AND USER APPROVAL
```

Never save a skill that wasn't verified during the session. Never save without explicit user confirmation. Unverified knowledge is worse than no knowledge -- it misleads future sessions.

**No exceptions:**
- Don't extract "should work" solutions that weren't tested
- Don't save without showing the user the draft first
- Don't extract every fix -- most aren't worth saving
- Don't skip the dedup check because "this is definitely new"

## The Gate Function

```
BEFORE extracting knowledge:

1. DETECT: Recognize that extractable knowledge exists (trigger conditions or user request)
2. DEDUP: Search existing skills before creating (rg across skill directories)
3. ANALYZE: Run 4 identification questions + worth assessment
4. COMPLEXITY: Simple → proceed. Complex → suggest /rcode first.
5. RESEARCH: Web search for technology-specific topics (skip for project-internal)
6. DRAFT: Structure using the extracted-skill-template
7. VALIDATE: Run quality gates checklist
8. CONFIRM: Present to user for approval
9. ONLY THEN: Save to the appropriate location

Skip any step = risk saving bad knowledge
```

## When to Activate

### Automatic Recognition

Watch for these signals during sessions:

- **Non-obvious debugging**: Investigation took multiple attempts, the root cause wasn't what the error message suggested, or the fix required domain-specific knowledge not in docs
- **Misleading errors**: The error message pointed to the wrong location or cause, and the actual fix was elsewhere
- **Workaround discovery**: The standard approach didn't work, requiring experimentation to find an alternative
- **Configuration insight**: Setup differed from documented patterns, or undocumented options were required
- **Trial-and-error success**: Multiple approaches were tried before finding one that worked

When you recognize these signals, suggest extraction:
```
This session produced a non-obvious discovery: [brief description].
This could be worth saving as a reusable skill. Want me to extract it?
```

### Explicit Invocation

When the user says `/learn`, "save this as a skill", "what did we learn", or similar:
- Switch to Retrospective Mode (see below)
- Review the full session for extraction candidates

## Self-Reflection Prompts

After completing a significant task, run these questions internally:

1. "What did I just learn that wasn't obvious before starting?"
2. "If I faced this exact problem again, what would I wish I knew?"
3. "What error message or symptom led me here, and what was the actual cause?"
4. "Is this pattern specific to this project, or would it help in similar projects?"
5. "What would I tell a colleague who hits this same issue?"

If any question produces a substantive answer, suggest extraction to the user.

## Extraction Workflow

### Step 1: Dedup Check

Search existing skills BEFORE doing anything else.

```sh
# Search skill directories for related content
rg --files -g 'SKILL.md' .claude/skills ~/.claude/skills 2>/dev/null
rg -i "keyword1|keyword2" .claude/skills ~/.claude/skills 2>/dev/null
```

**Decision matrix:**

| What You Find | Action |
|---------------|--------|
| Nothing related | Proceed to Step 2 |
| Same trigger, same fix | Update existing skill instead of creating new |
| Same trigger, different cause | Create new + cross-link to existing |
| Partial overlap | Add variant to existing skill |
| Stale or incorrect | Archive old, create replacement |

See ./reference/extraction-workflow.md for the full dedup process.

### Step 2: Identify the Knowledge

Answer these four questions:

1. **What was the problem?** -- The symptom, not the fix. Include exact errors.
2. **What was non-obvious?** -- Why was this harder than expected?
3. **What would help next time?** -- The shortcut for future sessions.
4. **What are the trigger conditions?** -- When does this problem appear?

If answers are thin ("it was just a typo"), the discovery fails the worth assessment. See ./reference/quality-gates.md for the full criteria.

### Step 2.5: Complexity Check

After identifying the knowledge, assess whether it needs deeper research before structuring.

**Simple -- proceed directly to Step 3:**
- Known technology with a straightforward fix
- Single-step solution verified in this session
- Would produce a flat SKILL.md with no reference files

**Complex -- suggest `/researching-code` first:**
- Involves unfamiliar technology, APIs, or protocols
- Would benefit from seeing how others solved this problem
- Would produce a skill needing `reference/` subdirectory
- Cross-cutting concern spanning multiple tools or systems
- User expresses uncertainty about how to structure the knowledge

When suggesting research:
> This discovery is complex enough to benefit from upfront research. Consider running `/researching-code` to analyze similar patterns and existing solutions, then return here to extract the skill with those findings as context.

When the user returns from `/researching-code`, check `.docs/research/` for new findings and incorporate them into the extraction.

### Step 3: Research Best Practices

Web search when the discovery involves specific technology:

```
"[technology] [problem] best practices 2026"
"[technology] [exact error message]"
```

**Skip when:**
- Project-internal patterns (custom architecture, team conventions)
- Context-specific solutions (this exact codebase only)
- Well-documented behavior (link to docs instead of duplicating)

**Act on results:**
- Confirmed solution: add References section with URLs
- Better approach found: update solution, note the improvement
- Version-specific: add version constraints to trigger conditions
- Contradicted: investigate before saving

### Step 4: Structure and Write

Use the template at ./templates/extracted-skill-template.md for the output format:

**Sections:** Problem, Context/Trigger Conditions, Solution (numbered steps with code), Verification, Example (before/after), Notes, References.

**Key decisions:**

*Description:* Write the description FIRST, before the body. Embed exact error messages, framework names, and action verbs. See ./reference/description-optimization.md for the retrieval key formula.

*Scope:*
- **Project-level** (`.claude/skills/`): Problem is specific to this codebase or team
- **User-level** (`~/.claude/skills/`): Problem applies across multiple projects

*Naming:* Kebab-case, descriptive of the problem domain. Examples: `prisma-connection-pool-serverless`, `typescript-circular-import-undefined`, `nextjs-server-error-wrong-location`.

*Validation:* The generated skill must pass the official spec: name `^[a-z0-9-]+$` (max 64 chars), description under 1024 chars (no angle brackets), only allowed frontmatter keys (`name`, `description`, `license`, `allowed-tools`, `metadata`).

### Step 5: Quality Gates

Run every item before saving. See ./reference/quality-gates.md for the full checklist.

**Critical checks:**
- [ ] Description contains specific trigger conditions
- [ ] Solution was verified during this session
- [ ] Content is specific enough to be actionable
- [ ] Content is general enough to be reusable
- [ ] No sensitive information (credentials, internal URLs, API keys)
- [ ] Doesn't duplicate existing skills or official docs
- [ ] Web research conducted when appropriate
- [ ] Frontmatter passes official validation rules
- [ ] Each solution step is independently verifiable

### Step 6: Present and Save

Show the complete draft to the user:

```
I've extracted a skill from this session:

---
[Full skill content]
---

Save to: [path]
Trigger: [first line of description]
Quality gates: All passed

Save this skill?
```

After user approves, write the file and confirm:

```
Skill extracted: [name]
Location: [path]
Files: 1 (SKILL.md)
This skill will activate in future sessions when similar problems arise.
```

## Retrospective Mode

When explicitly invoked (`/learn` or "what did we learn"):

1. **Review**: Scan the session conversation for extraction candidates. Look for debugging sequences, error resolutions, workarounds, corrections, and non-obvious discoveries.

2. **Identify**: List candidates with brief justifications:
   ```
   Session learning candidates:
   1. [Discovery] -- Worth saving because [reason]
   2. [Discovery] -- Worth saving because [reason]
   3. [Discovery] -- Not worth saving: [why it fails the worth assessment]
   ```

3. **Prioritize**: Rank by reuse value. Prefer knowledge that applies across projects, saves significant time, and involves non-obvious solutions.

4. **Extract**: Process the top 1-3 candidates through the full extraction workflow (Steps 1-6). Don't extract more than 3 per session -- quality over quantity.

5. **Summarize**:
   ```
   Session learning summary:
   - Extracted: [count] skill(s)
     - [name] at [path] -- [one-line description]
   - Skipped: [count] candidate(s)
     - [reason for each skip]
   ```

## Output Routing

Not everything belongs in a skill file. Use this decision flow:

**New skill file** when:
- Reusable across projects
- Multi-step solution with clear trigger conditions
- Involves debugging, workarounds, or non-obvious fixes
- Has specific error messages or framework-version triggers

**CLAUDE.md entry** when:
- Project-specific preference or convention
- Simple behavioral correction ("always use X not Y")
- Coding style rule for this project
- One-line guidance that doesn't need a full skill structure

**Handover document** when:
- Session-specific context for continuity
- One-time setup state
- In-progress work state

**Nothing** when:
- Simple typo or syntax error
- One-time issue that won't recur
- Knowledge already well-documented in official docs

## Red Flags - STOP and Reconsider

If you notice any of these, pause:

- About to save without user confirmation
- Solution wasn't verified during this session
- Description is vague ("helps with React problems")
- Extracting more than 3 skills from one session
- Skipping the dedup check
- The discovery is a simple typo or syntax fix
- Content restates official documentation without adding non-obvious insight

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "User will want this saved" | Ask. Never assume. Confirmation is mandatory. |
| "It's obviously worth saving" | Run the worth assessment. Obvious to you isn't obvious to the skill library. |
| "No need to dedup, this is definitely new" | Search anyway. You might find a related skill to update instead. |
| "Web search would slow things down" | If it's technology-specific, search. A few seconds prevents stale knowledge. |
| "The description is good enough" | Test it with 3 scenarios. Every word is a retrieval key. |
| "I'll skip quality gates, the content is solid" | Run the checklist. Every item. Every time. |

## The Bottom Line

**No extraction without verification and user approval.**

Detect the signal. Dedup first. Analyze thoroughly. Research when needed. Structure cleanly. Validate rigorously. Confirm with the user. Then save.

This is non-negotiable. Every extraction. Every time.
