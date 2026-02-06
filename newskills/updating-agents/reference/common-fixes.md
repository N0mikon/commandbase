# Common Fixes

Fix patterns for issues found during agent audits. Each fix includes before/after examples.

## Frontmatter Fixes

### Missing name field

**Issue:** Frontmatter lacks `name` property.

**Before:**
```yaml
---
description: "Analyzes codebase components..."
tools: Read, Grep, Glob, LS
model: sonnet
---
```

**After:**
```yaml
---
name: code-analyzer
description: "Analyzes codebase components..."
tools: Read, Grep, Glob, LS
model: sonnet
---
```

**Note:** Name must match the filename minus `.md`.

### Missing description field

**Issue:** Frontmatter lacks `description` property.

**Before:**
```yaml
---
name: code-analyzer
tools: Read, Grep, Glob, LS
model: sonnet
---
```

**After:**
```yaml
---
name: code-analyzer
description: "Analyzes codebase implementation details. Call the code-analyzer agent when you need to find detailed information about specific components."
tools: Read, Grep, Glob, LS
model: sonnet
---
```

### Unknown property in frontmatter

**Issue:** Frontmatter contains unrecognized properties (may be typos).

**Before:**
```yaml
---
name: my-agent
description: "..."
tools: Read, Grep
modle: sonnet
colour: blue
---
```

**After:**
```yaml
---
name: my-agent
description: "..."
tools: Read, Grep
model: sonnet
---
```

**Note:** `modle` was a typo for `model`. `colour` is not a recognized property - remove it.

### Both tools and disallowedTools present

**Issue:** Mutual exclusivity violation.

**Before:**
```yaml
---
name: my-agent
description: "..."
tools: Read, Grep, Glob, LS, Edit
disallowedTools: Bash, Task
---
```

**After (prefer allowlist):**
```yaml
---
name: my-agent
description: "..."
tools: Read, Grep, Glob, LS, Edit
---
```

**Note:** `tools` (allowlist) is preferred. Only use `disallowedTools` when the agent needs most tools and you want to exclude a few.

## Name Fixes

### Name uses gerund form

**Issue:** Agent name uses skill-style gerund (verb-ing) instead of noun/role form.

**Common patterns to fix:**

| Current (gerund) | Suggested (noun/role) |
|-------------------|----------------------|
| reviewing-code | code-reviewer |
| analyzing-code | code-analyzer |
| locating-docs | docs-locator |
| finding-patterns | pattern-finder |
| updating-docs | docs-updater |
| searching-web | web-researcher |

**Migration steps:**
1. Rename file: `mv old-name.md new-name.md`
2. Update `name:` field in frontmatter
3. Update any references to this agent in other agents or skills
4. Verify agent still loads correctly

### Name doesn't match filename

**Issue:** `name` field doesn't match filename minus `.md`.

**Before (filename: `code-analyzer.md`):**
```yaml
---
name: code-analyzer
---
```

**After (update name to match filename):**
```yaml
---
name: code-analyzer
---
```

**Alternative:** Rename the file to match the name field. The file is the source of truth for identity, so decide which is correct and align the other.

### Name has vague suffix

**Issue:** Name ends in `-helper`, `-handler`, `-manager`, or `-util`.

**Before:**
```yaml
name: code-helper
```

**After:**
```yaml
name: code-analyzer
```

**Note:** Choose a specific role suffix: `-analyzer`, `-locator`, `-finder`, `-updater`, `-researcher`, `-validator`, `-builder`, `-reviewer`.

## Description Fixes

### Description uses skill-style opener

**Issue:** Description starts with "Use this skill when..." (skill pattern, not agent pattern).

**Before:**
```yaml
description: "Use this skill when analyzing codebase components to understand how they work."
```

**After:**
```yaml
description: "Analyzes codebase implementation details. Call the code-analyzer agent when you need to find detailed information about specific components."
```

**Formula:** `"[Capability statement]. [Delegation trigger]."`

### Description uses first person

**Issue:** Description says "I help" or similar.

**Before:**
```yaml
description: "I analyze code and help you understand how components work together."
```

**After:**
```yaml
description: "Analyzes codebase implementation details including component interactions and data flows. Call when you need to understand how specific parts of the codebase work."
```

### Description lacks delegation trigger

**Issue:** Description states capability but not when to delegate.

**Before:**
```yaml
description: "Finds files and directories in the codebase using pattern matching and keyword search."
```

**After:**
```yaml
description: "Locates files, directories, and components relevant to a feature or task. Call code-locator with a human language prompt describing what you're looking for."
```

### Description contains angle brackets

**Issue:** Description has `<` or `>` characters.

**Before:**
```yaml
description: "Analyzes <component> files and generates <report> documents."
```

**After:**
```yaml
description: "Analyzes component files and generates report documents. Call when you need detailed breakdowns of specific modules or subsystems."
```

**Note:** Replace placeholders with concrete language.

## Tool Set Fixes

### No explicit tool set (inherits all)

**Issue:** Agent has neither `tools` nor `disallowedTools`, inheriting all parent tools.

**Before:**
```yaml
---
name: code-locator
description: "..."
model: sonnet
---
```

**After:**
```yaml
---
name: code-locator
description: "..."
tools: Grep, Glob, LS
model: sonnet
---
```

**Note:** Determine which tools the agent actually uses in its workflow and list only those.

### State-modifying tool without guardrails

**Issue:** Agent has Edit, Write, or Bash in tools but system prompt lacks restrictions.

**Fix:** Add a "What NOT to Do" section to the system prompt:

```markdown
## What NOT to Do

- DO NOT modify files without explicit instruction to do so
- DO NOT run destructive commands (rm, reset, force push)
- DO NOT make changes beyond what was specifically requested
- When uncertain whether to modify, report findings instead
```

Customize the restrictions to match the agent's specific role and tools.

### Unnecessary tool present

**Issue:** Agent has a tool it doesn't need (e.g., WebSearch on a codebase agent).

**Fix:** Remove the unnecessary tool from the `tools` array. Verify the system prompt doesn't reference the removed tool's functionality.

## Model & Permission Fixes

### Model mismatch for task complexity

**Issue:** Agent with state-modifying tools uses `haiku` model.

**Before:**
```yaml
tools: Read, Grep, Glob, LS, Edit, Bash
model: haiku
```

**After:**
```yaml
tools: Read, Grep, Glob, LS, Edit, Bash
model: opus
```

**Note:** State-modifying agents need stronger reasoning. Use `sonnet` at minimum, `opus` for complex modifications.

### bypassPermissions without justification

**Issue:** Agent has `permissionMode: bypassPermissions` without clear reason.

**Fix:** Change to `default` unless the agent is well-tested and trusted:

**Before:**
```yaml
permissionMode: bypassPermissions
```

**After:**
```yaml
permissionMode: default
```

**Note:** Flag for user review. `bypassPermissions` is appropriate only for mature, well-tested agents.

## System Prompt Fixes

### Missing role statement

**Issue:** System prompt doesn't establish identity in the first paragraph.

**Before (starts with instructions):**
```markdown
## Core Responsibilities

- Find files matching patterns
- Search code for keywords
```

**After (role statement first):**
```markdown
You are a codebase locator that finds files, directories, and components relevant to a feature or task. You respond to natural language descriptions of what the caller is looking for.

## Core Responsibilities

- Find files matching patterns
- Search code for keywords
```

### Missing "What NOT to Do" section

**Issue:** No enforcement section, especially problematic for read-only agents.

**Add before the closing section:**
```markdown
## What NOT to Do

- DO NOT suggest improvements or changes unless explicitly asked
- DO NOT critique the code or identify problems
- DO NOT make assumptions about intent beyond what was asked
- DO NOT include information that wasn't found in the actual codebase
- DO NOT fabricate file paths or line numbers
```

**Customize** based on the agent's role. Read-only agents emphasize "don't suggest changes." State-modifying agents emphasize "don't modify beyond scope."

### Missing meta-reminder

**Issue:** No closing identity reinforcement.

**Add at the end of the system prompt:**
```markdown
REMEMBER: You are a documentarian, not a critic or consultant. Describe what exists. Let the caller decide what to do with the information.
```

**Customize** to match the agent's role and primary discipline.

### Over 300 lines

**Issue:** Agent file exceeds recommended line limit.

**Fix approach:**
1. Unlike skills, agents CANNOT split into reference files - everything must be in one `.md`
2. Identify redundant or overly verbose sections
3. Condense examples to the most essential ones
4. Merge overlapping guidelines
5. Tighten prose - remove filler words and repetitive instructions
6. Target 80-200 lines for most agents

**Note:** This is the hardest fix. Agent content cannot be extracted to reference files like skills can. The only option is to make the content more concise.
