# Standard CLAUDE.md Sections

Reference for the expected structure and section order in CLAUDE.md files.

## Section Order

```markdown
# [Project Name]
[One sentence: what this project is and its purpose]

## Project Structure
[Brief directory layout - only key directories]

## Development
### Quick Start
[Single command to get started]

### Key Commands
[4-6 most important commands]

### Verification
[Single verification command before committing]

## Architecture Notes (optional)
[2-3 sentences on key architectural decisions - only if non-obvious]

## Additional Context
[Pointers to detailed docs]

## Automatic Behaviors
[Pattern learning detection and learned behaviors]
```

## Section Guidelines

### Title and Purpose (Required)
- Project name as H1
- Single sentence immediately after
- Format: "[Project name] - [what it does and why]"

### Project Structure (Optional)
- Only include if structure isn't obvious
- Key directories only, not every file
- Use code block with tree-style format
- Max 10-15 lines

### Development (Required)
Must include at minimum:
- **Quick Start**: Single command, not multi-step
- **Key Commands**: 4-6 essential commands with comments
- **Verification**: What to run before committing

### Architecture Notes (Optional)
- Only if non-obvious decisions exist
- 2-3 sentences max
- Skip for simple projects

### Additional Context (Recommended)
- Pointers to `.docs/` files
- Format: `- [path] - [brief description]`
- Enables progressive disclosure

### Automatic Behaviors (Recommended)
- Standard pattern learning trigger
- Project-specific learned behaviors
- Format: "When I [trigger], [response]."

## Line Budgets

| Section | Ideal | Max |
|---------|-------|-----|
| Title + Purpose | 2 | 3 |
| Project Structure | 8 | 15 |
| Development | 15 | 25 |
| Architecture Notes | 3 | 5 |
| Additional Context | 5 | 10 |
| Automatic Behaviors | 5 | 10 |
| **Total** | **38** | **68** |

If approaching these limits, content should move to `.docs/` files.
