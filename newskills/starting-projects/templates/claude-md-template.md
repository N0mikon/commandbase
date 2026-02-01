# CLAUDE.md Template

Use this template when generating a project's CLAUDE.md file.

## Principles

- **Less is more**: Keep under 60 lines if possible, never exceed 300 lines
- **Universally applicable**: Only include information relevant to EVERY session
- **Progressive disclosure**: Point to other docs instead of including everything
- **No code style rules**: Let linters handle formatting
- **WHAT, WHY, HOW structure**: Cover these three aspects concisely

## Template

````markdown
# [Project Name]

[One sentence: what this project is and its purpose]

## Project Structure

```
[Brief directory layout - only key directories]
```

## Development

### Quick Start
```bash
[Single command to get started, e.g., "bun install && bun dev"]
```

### Key Commands
```bash
[command]  # [what it does - keep to 4-6 most important commands]
```

### Verification
Run before committing: `[single verification command or script]`

## Architecture Notes

[2-3 sentences on key architectural decisions - only if non-obvious]

## Additional Context

For detailed documentation, see:
- `[path/to/doc]` - [brief description]

## Automatic Behaviors

When I mention a repeat problem ("this happened before", "same issue again", etc.), offer to save the solution as a learned pattern to `~/.claude/skills/learned/`.
````

## Generation Process

1. **Draft the CLAUDE.md** based on discovery and research:
   - Extract the essential WHAT (project identity, structure)
   - Distill the WHY (purpose, in one sentence)
   - Define the HOW (key commands, verification steps)

2. **Review for conciseness**:
   - Remove anything not universally applicable
   - Remove code style instructions (rely on linters)
   - Remove detailed explanations (use progressive disclosure)
   - Ensure it would be useful whether working on any part of the project

3. **Present for approval**:
   ```
   Here's your CLAUDE.md. I've kept it concise and focused on what Claude needs for every session:

   [Show the content]

   Key principles applied:
   - [X] Under 60 lines
   - [X] No code style rules (handled by [linter])
   - [X] Pointers to detailed docs instead of inline content
   - [X] Only universally applicable information

   Want me to adjust anything?
   ```

4. **Write the file** after approval

## What NOT to Include

See ./reference/claude-md-guidelines.md for the full list of anti-patterns.
