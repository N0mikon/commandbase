# Common Fixes

Fix patterns for issues found during skill audits. Each fix includes before/after examples.

## Frontmatter Fixes

### Missing name field

**Issue:** Frontmatter lacks `name` property.

**Before:**
```yaml
---
description: "Use this skill when..."
---
```

**After:**
```yaml
---
name: skill-directory-name
description: "Use this skill when..."
---
```

**Note:** Name must match the directory name exactly.

### Missing description field

**Issue:** Frontmatter lacks `description` property.

**Before:**
```yaml
---
name: my-skill
---
```

**After:**
```yaml
---
name: my-skill
description: "Use this skill when [primary situation]. This includes [specific use case], [another use case], and [edge case]."
---
```

### Invalid property in frontmatter

**Issue:** Frontmatter contains disallowed properties.

**Before:**
```yaml
---
name: my-skill
description: "..."
author: John Doe
version: 1.0.0
---
```

**After:**
```yaml
---
name: my-skill
description: "..."
metadata:
  author: John Doe
  version: 1.0.0
---
```

**Note:** Move custom properties under `metadata` key.

## Name Fixes

### Name not gerund form

**Issue:** Skill name uses noun or verb-noun form instead of gerund.

**Common patterns to fix:**

| Current | Suggested |
|---------|-----------|
| code-review | reviewing-code |
| skill-validator | validating-skills |
| test-runner | running-tests |
| doc-generator | generating-docs |
| error-handler | handling-errors |

**Migration steps:**
1. Rename directory: `mv old-name new-name`
2. Update `name:` field in frontmatter
3. Update any cross-references in other skills
4. Update documentation that references the old name

### Name doesn't match directory

**Issue:** `name` field doesn't match directory name.

**Before (directory: `my-skill/`):**
```yaml
---
name: myskill
---
```

**After:**
```yaml
---
name: my-skill
---
```

**Note:** Directory name is authoritative. Update `name` field to match.

## Description Fixes

### Description doesn't start with WHEN formula

**Issue:** Description describes WHAT but not WHEN.

**Before:**
```yaml
description: "A skill for validating code against plans and checking test results."
```

**After:**
```yaml
description: "Use this skill when validating code against plans, checking test results, or verifying implementation completeness. This includes running spec compliance checks, executing automated tests, and comparing code to plan specifications."
```

### Description uses first person

**Issue:** Description says "I help" or similar.

**Before:**
```yaml
description: "I help you write better commit messages and manage your git workflow."
```

**After:**
```yaml
description: "Use this skill when writing commit messages, managing git workflow, or preparing changes for commit. This includes staging specific files, writing descriptive messages, and following repository conventions."
```

### Description contains angle brackets

**Issue:** Description has `<` or `>` characters.

**Before:**
```yaml
description: "Use this skill when creating <component> files or generating <type> definitions."
```

**After:**
```yaml
description: "Use this skill when creating component files or generating type definitions. This includes React components, TypeScript interfaces, and styled-components."
```

**Note:** Replace placeholders with concrete examples.

### Description too long

**Issue:** Description exceeds 1024 characters.

**Fix approach:**
1. Remove redundant phrases
2. Consolidate overlapping use cases
3. Focus on primary triggers, move details to body
4. Aim for 200-400 characters

## Structure Fixes

### SKILL.md over 500 lines

**Issue:** Main file exceeds line limit.

**Fix approach:**
1. Identify content that can be extracted:
   - Detailed reference material
   - Example templates
   - Long checklists
2. Create `reference/` subdirectory
3. Move extracted content to intention-revealing filenames
4. Replace with skinny pointers: `See ./reference/filename.md for [topic]`

**Example extraction:**
```markdown
<!-- Before: inline in SKILL.md -->
## Validation Rules
[100 lines of detailed rules...]

<!-- After: in SKILL.md -->
## Validation Rules

See ./reference/validation-rules.md for the complete validation checklist.

<!-- In reference/validation-rules.md -->
# Validation Rules
[100 lines of detailed rules...]
```

### Extraneous files present

**Issue:** Directory contains README.md, CHANGELOG.md, etc.

**Fix:** Delete the files. Skills should only contain:
- SKILL.md (required)
- reference/ (optional)
- templates/ (optional)
- scripts/ (optional)
- assets/ (optional)

## Enforcement Pattern Fixes

### Missing Iron Law section

**Issue:** Skill lacks enforcement pattern opener.

**Add after opening paragraph:**
```markdown
## The Iron Law

\`\`\`
[ONE ABSOLUTE RULE IN ALL CAPS SPECIFIC TO THIS SKILL]
\`\`\`

[Brief explanation of why this rule matters.]

**No exceptions:**
- [Specific violation to avoid]
- [Another violation]
- [Another violation]
```

**Customize the rule** based on the skill's purpose. Don't copy generic text.

### Missing Gate Function section

**Add after Iron Law:**
```markdown
## The Gate Function

\`\`\`
BEFORE [main action this skill performs]:

1. [First prerequisite check]
2. [Second prerequisite check]
3. [Mode or path determination]
4. [Input validation]
5. ONLY THEN: [Begin the actual work]

Skip any step = [consequence specific to this skill]
\`\`\`
```

### Missing Red Flags section

**Add before Rationalization Prevention:**
```markdown
## Red Flags - STOP and [Action Verb]

If you notice any of these, pause:

- [Warning sign 1 specific to this skill]
- [Warning sign 2]
- [Warning sign 3]
- [Warning sign 4]
```

### Missing Rationalization Prevention table

**Add after Red Flags:**
```markdown
## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "[Common shortcut excuse]" | [Why it's wrong] |
| "[Another excuse]" | [Why it matters] |
| "[Third excuse]" | [What actually happens] |
```

### Missing Bottom Line section

**Add at end:**
```markdown
## The Bottom Line

**[Bold summary of the skill's core discipline.]**

[Reinforcing sentence.] This is non-negotiable. Every [scope]. Every time.
```
